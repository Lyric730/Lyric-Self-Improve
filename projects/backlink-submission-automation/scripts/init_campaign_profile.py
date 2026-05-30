#!/usr/bin/env python3
"""Create or import a campaign profile folder from structured answers."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse


MISSING_VALUES = {"", "无", "none", "null", "n/a", "na", "not provided"}


def is_missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in MISSING_VALUES
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def slugify(value: str) -> str:
    value = (value or "campaign").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "campaign"


def domain_from_url(url: str) -> str:
    if not url:
        return ""
    if "://" not in url:
        url = "https://" + url
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_profile_json(folder: Path) -> Path | None:
    names = {
        "profile.json",
        "site-profile.json",
        "product-profile.json",
        "campaign-profile.json",
    }
    for path in folder.rglob("*.json"):
        if path.name.lower() in names:
            return path
    return None


def copy_existing_profile(import_path: str, dest_root: Path) -> dict:
    source = import_path.strip()
    local_source: Path
    if re.match(r"^https?://.*\.git/?$", source):
        clone_dir = dest_root / "imported-profile-repo"
        if clone_dir.exists():
            shutil.rmtree(clone_dir)
        subprocess.run(["git", "clone", "--depth", "1", source, str(clone_dir)], check=True)
        local_source = clone_dir
    else:
        local_source = Path(source).expanduser().resolve()

    if not local_source.exists():
        raise SystemExit(f"import path not found: {local_source}")
    if local_source.is_file():
        profile_path = local_source
        profile = read_json(profile_path)
        shutil.copy2(profile_path, dest_root / "profile" / "profile.json")
    else:
        profile_path = find_profile_json(local_source)
        if not profile_path:
            raise SystemExit(f"no profile JSON found under: {local_source}")
        profile = read_json(profile_path)
        shutil.copy2(profile_path, dest_root / "profile" / "profile.json")
        assets_src = local_source / "assets"
        if assets_src.exists():
            shutil.copytree(assets_src, dest_root / "assets", dirs_exist_ok=True)
    (dest_root / "profile" / "source.txt").write_text(str(local_source), encoding="utf-8")
    return profile


def normalize_profile(answers: dict) -> tuple[str, dict, dict]:
    brand = answers.get("brand_name") or answers.get("product_name") or answers.get("产品/品牌名")
    url = answers.get("canonical_url") or answers.get("website_url") or answers.get("官网 URL")
    email = answers.get("contact_email") or answers.get("联系邮箱/注册邮箱")
    if is_missing(brand) or is_missing(url) or is_missing(email):
        raise SystemExit("new profile requires brand_name, canonical_url/website_url, and contact_email")

    brand = str(brand).strip()
    canonical_url = str(url).strip()
    if not canonical_url.startswith(("http://", "https://")):
        canonical_url = "https://" + canonical_url
    target_domain = answers.get("target_domain") or domain_from_url(canonical_url)
    optional = answers.get("optional") or {}

    def get(key: str, default=None):
        value = answers.get(key)
        if is_missing(value):
            value = optional.get(key)
        return default if is_missing(value) else value

    categories = get("categories", [])
    if isinstance(categories, str):
        categories = [x.strip() for x in re.split(r"[,，/|]", categories) if x.strip()]
    tags = get("tags", [])
    if isinstance(tags, str):
        tags = [x.strip() for x in re.split(r"[,，/|]", tags) if x.strip()]

    profile = {
        "campaign_name": get("campaign_name", f"{brand} backlink campaign"),
        "brand_name": brand,
        "canonical_url": canonical_url,
        "target_domain": target_domain,
        "intake": answers.get(
            "intake",
            {
                "mode": answers.get("intake_mode", "unknown"),
                "runtime_agent": answers.get("runtime_agent", ""),
                "structured_input_tool": answers.get("structured_input_tool", ""),
            },
        ),
        "positioning": get("positioning", ""),
        "audience": get("audience", ""),
        "primary_outcome": get("primary_outcome", ""),
        "forbidden_phrases": get("forbidden_phrases", []),
        "contact_email": str(email).strip(),
        "comment_email": get("comment_email", str(email).strip()),
        "submitter_name": get("submitter_name", f"{brand} Team"),
        "hq_country": get("hq_country", ""),
        "hq_city": get("hq_city", ""),
        "categories": categories,
        "tags": tags,
        "one_liner": get("one_liner", ""),
        "short_description": get("short_description", ""),
        "long_description": get("long_description", ""),
        "anchors": get("anchors", [[brand, "brand"], [canonical_url, "naked"]]),
        "assets": get(
            "assets",
            {
                "logo_square": "",
                "logo_wide": "",
                "screenshot": "",
                "pdf": "",
                "public_screenshot_url": "",
            },
        ),
        "min_dr": int(get("min_dr", 20)),
        "manual_hold_domains": get(
            "manual_hold_domains",
            ["producthunt.com", "news.ycombinator.com", "g2.com", "capterra.com", "trustpilot.com"],
        ),
        "candidate_source_mode": get("candidate_source_mode", "bundled_packs"),
        "allow_account_creation": str(
            answers.get("allow_account_creation")
            or answers.get("是否允许我为提交站点创建账号并留存账号密码")
            or ""
        ),
        "password_storage": str(
            answers.get("password_storage")
            or answers.get("密码留存方式")
            or "local_sqlite"
        ),
    }

    missing_optional = [
        key
        for key in (
            "positioning",
            "audience",
            "primary_outcome",
            "categories",
            "tags",
            "one_liner",
            "short_description",
            "long_description",
            "hq_country",
            "hq_city",
        )
        if is_missing(profile.get(key))
    ]
    assets = profile.get("assets", {})
    missing_assets = [k for k, v in assets.items() if is_missing(v)]
    completion = {
        "missing_optional_fields_for_agent": missing_optional,
        "missing_assets_for_agent": missing_assets,
        "agent_actions": [
            "Open the canonical URL and derive missing positioning/copy/categories/tags.",
            "If screenshot/logo is missing, capture homepage screenshot or locate approved assets.",
            "Write completed profile.json before importing candidates.",
        ],
    }
    return slugify(brand), profile, completion


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-root", default="campaigns")
    parser.add_argument("--answers-json", help="Structured Asked answer JSON")
    parser.add_argument("--import-path", help="Existing profile file/folder or Git URL")
    parser.add_argument("--slug", help="Optional campaign folder slug")
    args = parser.parse_args()

    if not args.answers_json and not args.import_path:
        raise SystemExit("provide --answers-json or --import-path")

    answers = read_json(Path(args.answers_json)) if args.answers_json else {}
    mode = (answers.get("profile_mode") or answers.get("mode") or "").lower()
    import_path = args.import_path or answers.get("import_path") or answers.get("profile_path")

    if import_path or mode == "import":
        slug = args.slug or slugify(Path(str(import_path)).stem)
    else:
        slug, _, _ = normalize_profile(answers)
        slug = args.slug or slug

    dest_root = Path(args.campaign_root) / slug
    for sub in ("profile", "assets", "data", "sources", "reports"):
        (dest_root / sub).mkdir(parents=True, exist_ok=True)

    if import_path or mode == "import":
        profile = copy_existing_profile(str(import_path), dest_root)
        completion = {"imported": True, "agent_actions": ["Inspect imported profile and fill missing required fields if any."]}
    else:
        _, profile, completion = normalize_profile(answers)
        (dest_root / "profile" / "profile.json").write_text(
            json.dumps(profile, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    (dest_root / "profile" / "completion-needed.json").write_text(
        json.dumps(completion, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(dest_root.resolve())
    print(dest_root / "profile" / "profile.json")
    print(dest_root / "profile" / "completion-needed.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
