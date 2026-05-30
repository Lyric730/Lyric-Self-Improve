"""
Step 3.5: collect open-licensed keyword fallback images.

This is used when a selected item has no original article image, or when a
source/post screenshot is not good enough. It searches Wikimedia Commons,
filters for licenses that allow commercial use, downloads one image per item,
and records license metadata in final.json.

Input:
  daily/<date>/three-minute-future/work/final.json

Output:
  daily/<date>/three-minute-future/work/keyword-assets/*
  daily/<date>/three-minute-future/work/keyword-images.json
  final.json updated with keywordImagePath / keywordImageMeta

Usage:
  python lines/three-minute-future/search_keyword_images.py 2026-05-23
  python lines/three-minute-future/search_keyword_images.py 2026-05-23 --prefer-keyword
"""

from __future__ import annotations

import argparse
import html
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from enrich_assets import download_image


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISUAL_POLICY_PATH = Path(__file__).resolve().parent / "config" / "visual_asset_policy.json"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "self-media-three-minute-future/0.1 (open-license-image-search)"


TITLE_QUERY_HINTS = [
    (["日本", "AI", "机器人"], ["Japan humanoid robot", "Japanese robot", "service robot Japan"]),
    (["日本", "人工智能机器人"], ["Japan humanoid robot", "Japanese robot", "industrial robot Japan"]),
    (["微软", "人工"], ["AI data center servers", "Microsoft data center", "GPU server"]),
    (["Meta", "裁员"], ["Meta headquarters", "office workspace", "technology office"]),
    (["星巴克"], ["Starbucks store", "coffee shop interior", "retail inventory"]),
    (["高尔夫球包", "机器人"], ["delivery robot", "autonomous delivery robot", "service robot"]),
    (["机器人", "身份证"], ["humanoid robot", "service robot", "robot registration"]),
    (["OpenAI", "绿卡"], ["United States green card", "technology office", "San Francisco office"]),
    (["远程办公"], ["home office laptop", "video meeting laptop", "remote worker laptop", "remote work office"]),
    (["硬件"], ["semiconductor wafer", "GPU server", "data center servers"]),
    (["芯片"], ["semiconductor wafer", "computer chip", "GPU server"]),
    (["国防", "五角大楼"], ["Pentagon aerial view", "data center servers", "cyber defense"]),
    (["机场", "搬行李"], ["airport baggage robot", "airport baggage handling", "service robot"]),
]

TAG_QUERIES = {
    "hardware": ["semiconductor wafer", "GPU server", "data center servers"],
    "robotics": ["humanoid robot", "delivery robot", "industrial robot"],
    "labor": ["office workers technology", "remote work office", "factory automation"],
    "retail": ["retail inventory", "coffee shop interior", "warehouse shelves"],
    "law": ["courtroom gavel", "law technology", "court building"],
    "education": ["classroom technology", "school classroom", "online learning classroom"],
    "defense": ["Pentagon aerial view", "cyber defense", "server room"],
    "healthcare": ["hospital robot", "medical technology", "hospital corridor"],
}

ACCEPTED_LICENSE_TERMS = (
    "cc by",
    "cc-by",
    "cc0",
    "public domain",
    "pd",
    "gfdl",
)

REJECTED_LICENSE_TERMS = (
    "noncommercial",
    "non-commercial",
    "no commercial",
    "fair use",
    "copyrighted",
)


def load_final(date: str) -> tuple[Path, dict[str, Any]]:
    path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "final.json"
    if not path.exists():
        raise SystemExit(f"missing: {path} (run generate_final.py first)")
    return path, json.loads(path.read_text(encoding="utf-8"))


def load_visual_policy() -> dict[str, Any]:
    return json.loads(VISUAL_POLICY_PATH.read_text(encoding="utf-8"))


def strip_markup(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html.unescape(value or ""))
    return re.sub(r"\s+", " ", text).strip()


def meta_value(extmetadata: dict[str, Any], key: str) -> str:
    value = extmetadata.get(key, {})
    if isinstance(value, dict):
        return strip_markup(str(value.get("value", "")))
    return strip_markup(str(value or ""))


def license_allows_commercial(imageinfo: dict[str, Any]) -> bool:
    ext = imageinfo.get("extmetadata", {}) or {}
    license_text = " ".join(
        [
            meta_value(ext, "LicenseShortName"),
            meta_value(ext, "License"),
            meta_value(ext, "UsageTerms"),
            meta_value(ext, "Restrictions"),
        ]
    ).lower()
    if any(term in license_text for term in REJECTED_LICENSE_TERMS):
        return False
    return any(term in license_text for term in ACCEPTED_LICENSE_TERMS)


def commons_search(query: str, limit: int = 16) -> list[dict[str, Any]]:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|mime|size|extmetadata",
        "iiurlwidth": "1400",
    }
    url = f"{COMMONS_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))

    pages = data.get("query", {}).get("pages", {}) or {}
    images = []
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        mime = str(info.get("mime", "")).lower()
        if not mime.startswith("image/") or "svg" in mime:
            continue
        width = int(info.get("width") or 0)
        height = int(info.get("height") or 0)
        if width < 600 or height < 400:
            continue
        if not license_allows_commercial(info):
            continue
        ext = info.get("extmetadata", {}) or {}
        images.append(
            {
                "title": page.get("title", ""),
                "url": info.get("thumburl") or info.get("url", ""),
                "originalUrl": info.get("url", ""),
                "width": width,
                "height": height,
                "mime": mime,
                "license": meta_value(ext, "LicenseShortName"),
                "attribution": meta_value(ext, "Attribution") or meta_value(ext, "Artist"),
                "credit": meta_value(ext, "Credit"),
                "description": meta_value(ext, "ImageDescription") or meta_value(ext, "ObjectName"),
                "usageTerms": meta_value(ext, "UsageTerms"),
                "commonsDescriptionUrl": info.get("descriptionurl", ""),
                "query": query,
            }
        )
    return sorted(images, key=lambda x: x["width"] * x["height"], reverse=True)


def company_rule_for_item(item: dict[str, Any], visual_policy: dict[str, Any]) -> dict[str, Any] | None:
    raw = f"{item.get('rawTitle', '')} {item.get('title', '')}"
    for rule in visual_policy.get("companyVisualRules", []):
        if any(term in raw for term in rule.get("match", [])):
            return rule
    return None


def candidate_score(candidate: dict[str, Any], rule: dict[str, Any] | None) -> int:
    text = " ".join(
        [
            candidate.get("title", ""),
            candidate.get("description", ""),
            candidate.get("credit", ""),
        ]
    ).lower()
    score = candidate["width"] * candidate["height"]
    if rule:
        for term in rule.get("mustPreferTerms", []):
            if term.lower() in text:
                score += 3_000_000
        company = str(rule.get("company", "")).lower()
        if company and company in text:
            score += 5_000_000
    else:
        query_terms = re.findall(r"[a-zA-Z]{3,}", candidate.get("query", "").lower())
        for term in query_terms:
            if term in text:
                score += 2_000_000
    return score


def company_candidate_allowed(candidate: dict[str, Any], rule: dict[str, Any] | None) -> bool:
    if not rule:
        return True
    text = " ".join(
        [
            candidate.get("title", ""),
            candidate.get("description", ""),
            candidate.get("credit", ""),
            candidate.get("originalUrl", ""),
        ]
    ).lower()
    company_terms = [str(rule.get("company", "")), *rule.get("match", [])]
    return any(term and term.lower().strip() in text for term in company_terms)


def queries_for_item(item: dict[str, Any], visual_policy: dict[str, Any]) -> list[str]:
    raw = f"{item.get('rawTitle', '')} {item.get('title', '')}"
    queries: list[str] = []
    rule = company_rule_for_item(item, visual_policy)
    if rule:
        queries.extend(rule.get("queries", []))
    for terms, hints in TITLE_QUERY_HINTS:
        if all(term in raw for term in terms):
            queries.extend(hints)
    for tag in item.get("tags", []):
        queries.extend(TAG_QUERIES.get(tag, []))
    cleaned = re.sub(r"[^\w\u4e00-\u9fff ]+", " ", raw)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if cleaned:
        queries.append(cleaned[:80])

    unique: list[str] = []
    for query in queries:
        if query and query not in unique:
            unique.append(query)
    return unique[:8]


def needs_keyword_image(item: dict[str, Any], prefer_keyword: bool) -> bool:
    if item.get("imagePath"):
        return False
    if prefer_keyword:
        return True
    return not item.get("keywordImagePath") and not item.get("sourceScreenshotPath")


def collect(date: str, prefer_keyword: bool, target_items: set[str] | None = None) -> Path:
    final_path, data = load_final(date)
    visual_policy = load_visual_policy()
    work_dir = PROJECT_ROOT / "daily" / date / LINE_NAME / "work"
    asset_dir = work_dir / "keyword-assets"
    asset_dir.mkdir(parents=True, exist_ok=True)

    used_urls = {
        item.get("keywordImageMeta", {}).get("originalUrl")
        for item in data.get("items", [])
        if item.get("keywordImageMeta", {}).get("originalUrl")
    }
    report: list[dict[str, Any]] = []

    for item in data.get("items", []):
        if target_items and item.get("id") not in target_items:
            continue
        if not needs_keyword_image(item, prefer_keyword):
            continue

        found = None
        rule = company_rule_for_item(item, visual_policy)
        for query in queries_for_item(item, visual_policy):
            try:
                candidates = commons_search(query)
            except Exception as exc:
                report.append({"item": item.get("id"), "query": query, "status": "search-error", "error": str(exc)})
                continue
            candidates = sorted(candidates, key=lambda candidate: candidate_score(candidate, rule), reverse=True)
            for candidate in candidates:
                if not company_candidate_allowed(candidate, rule):
                    continue
                original_url = candidate.get("originalUrl") or candidate.get("url")
                if original_url in used_urls:
                    continue
                image_info = download_image(candidate["url"], asset_dir / item["id"])
                if image_info.get("status") == "downloaded":
                    used_urls.add(original_url)
                    found = {
                        "path": image_info["path"],
                        "meta": {
                            **candidate,
                            "company": rule.get("company") if rule else "",
                            "downloadUrl": candidate["url"],
                            "path": image_info["path"],
                            "provider": "wikimedia-commons",
                        },
                    }
                    break
            if found:
                break

        if found:
            item["keywordImagePath"] = found["path"]
            item["keywordImageMeta"] = found["meta"]
            item["visualFallbackStatus"] = "keyword-image"
            report.append({"item": item.get("id"), "status": "downloaded", "meta": found["meta"]})
            print(f"OK keyword image {item.get('id')} <- {found['meta']['query']}")
        else:
            item["keywordImageMeta"] = {"status": "missing", "queries": queries_for_item(item, visual_policy)}
            if not item.get("visualFallbackStatus"):
                item["visualFallbackStatus"] = "keyword-image-missing"
            report.append({"item": item.get("id"), "status": "missing", "queries": queries_for_item(item, visual_policy)})
            print(f"MISS keyword image {item.get('id')}")

    out_path = work_dir / "keyword-images.json"
    out_path.write_text(
        json.dumps(
            {
                "line": LINE_NAME,
                "publishDate": date,
                "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "provider": "wikimedia-commons",
                "licensePolicy": "free commercial-use compatible",
                "items": report,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    final_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--prefer-keyword", action="store_true", help="use keyword images for items without original images, even if a screenshot exists")
    parser.add_argument("--items", nargs="*", help="optional final item ids to update, for example item-08")
    args = parser.parse_args()

    target_items = set(args.items) if args.items else None
    out_path = collect(args.date, args.prefer_keyword, target_items)
    print(f"OK keyword image report -> {out_path}")


if __name__ == "__main__":
    main()
