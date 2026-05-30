from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1.0"
WHITESPACE_RE = re.compile(r"\s+")
TRENDING_URL = "https://github.com/trending"
JINA_PREFIX = "https://r.jina.ai/"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_z(value: datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_space(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value).strip()


def build_source_id(repo_full_name: str) -> str:
    digest = hashlib.sha1(repo_full_name.encode("utf-8")).hexdigest()[:12]
    slug = repo_full_name.replace("/", "-").lower()
    return f"gh-{slug}-{digest}"


def fetch_trending_page(language: str, since: str, timeout: int) -> str:
    url = TRENDING_URL
    params = []
    if language:
        params.append(f"language={language}")
    if since:
        params.append(f"since={since}")
    if params:
        url = f"{url}?{'&'.join(params)}"

    proxied = f"{JINA_PREFIX}{url}"
    request = urllib.request.Request(proxied, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "ignore")


def parse_trending_repos(raw_text: str) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    repo_pattern = re.compile(
        r"\[([^\]]+/[^\]]+)\]\(https://github\.com/([^)]+)\)"
    )
    star_pattern = re.compile(r"([\d,]+)\s*stars?\s*(?:today|this week|this month)", re.IGNORECASE)
    desc_lines = raw_text.split("\n")

    matches = list(repo_pattern.finditer(raw_text))
    for match in matches:
        display_name = match.group(1).strip()
        repo_path = match.group(2).strip().rstrip("/")
        if "/" not in repo_path:
            continue
        # Find description: text after the repo link on same or next lines
        start_pos = match.end()
        context = raw_text[start_pos:start_pos + 500]
        desc = ""
        for line in context.split("\n"):
            cleaned = normalize_space(line)
            if cleaned and not cleaned.startswith("[") and not cleaned.startswith("*"):
                desc = cleaned[:300]
                break

        # Try to find star count nearby
        stars_today = ""
        star_match = star_pattern.search(context)
        if star_match:
            stars_today = star_match.group(0)

        repos.append({
            "repo_full_name": repo_path,
            "display_name": display_name,
            "url": f"https://github.com/{repo_path}",
            "description": desc,
            "stars_today": stars_today,
        })

    # Deduplicate
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for repo in repos:
        key = repo["repo_full_name"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(repo)
    return unique


def build_source_item(repo: dict[str, Any], fetched_at: str) -> dict[str, Any]:
    source_id = build_source_id(repo["repo_full_name"])
    title = f"{repo['repo_full_name']}: {repo['description']}" if repo["description"] else repo["repo_full_name"]
    summary = repo.get("description", "")
    stars_info = repo.get("stars_today", "")
    full_text = f"GitHub Trending: {repo['repo_full_name']}\n\n{summary}"
    if stars_info:
        full_text += f"\n\n{stars_info}"

    return {
        "schema_version": SCHEMA_VERSION,
        "source_id": source_id,
        "fetched_at": fetched_at,
        "platform": "github",
        "source_kind": "github_repo",
        "canonical_url": repo["url"],
        "author": {
            "handle": repo["repo_full_name"].split("/")[0],
            "display_name": repo.get("display_name", repo["repo_full_name"]),
            "account_url": f"https://github.com/{repo['repo_full_name'].split('/')[0]}",
        },
        "title": normalize_space(title),
        "language": "en",
        "published_at": fetched_at,
        "participants": [],
        "source_assets": [
            {
                "asset_kind": "github_repo",
                "url": repo["url"],
                "selected_for_text": True,
                "notes": "github trending repo",
            }
        ],
        "content": {
            "primary_text_source": "github_trending",
            "summary": summary or None,
            "full_text": full_text,
            "sections": ["github_trending"],
            "raw_quotes": [],
            "assembly_notes": None,
        },
        "extracted_signals": {
            "release_signals": [],
            "metric_signals": [stars_info] if stars_info else [],
            "named_entities": [repo["repo_full_name"]],
            "task_hints": ["release"],
            "fact_anchors": [title, repo["url"]] + ([stars_info] if stars_info else []),
            "normalization_notes": "github_trending_page",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover GitHub Trending repos as source items")
    parser.add_argument("--out-dir", required=True, help="Output directory for source items")
    parser.add_argument("--language", default="", help="Filter by programming language (e.g. python)")
    parser.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"], help="Trending time range")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP request timeout")
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    fetched_at = isoformat_z(utc_now())

    print(f"Fetching GitHub Trending (language={args.language or 'all'}, since={args.since})...")
    raw = fetch_trending_page(args.language, args.since, args.timeout)
    repos = parse_trending_repos(raw)
    print(f"  Found {len(repos)} trending repos")

    for repo in repos:
        item = build_source_item(repo, fetched_at)
        item_dir = out_dir / item["source_id"]
        item_dir.mkdir(parents=True, exist_ok=True)
        (item_dir / "source_item.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"  {item['source_id']}")

    print(f"github_trending={len(repos)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
