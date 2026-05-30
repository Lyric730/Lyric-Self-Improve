from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
import sys

_CURRENT = Path(__file__).resolve()
SHARED_CANDIDATES = [
    _CURRENT.parents[1] / "shared",
    _CURRENT.parents[2] / "content/pipeline/shared",
]
for candidate in SHARED_CANDIDATES:
    if candidate.exists() and str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from linked_source_enrichment import (
    extract_urls,
    fetch_link_context,
    is_external_link,
    normalize_space,
)

try:
    from jsonschema import validate as jsonschema_validate
except Exception:  # pragma: no cover
    jsonschema_validate = None


SCHEMA_VERSION = "0.1.0"
X_ARTICLE_RE = re.compile(r"x\.com/i/article/(\d+)")
METRIC_RE = re.compile(
    r"\$\d[\d,]*(?:\.\d+)?|\b\d+(?:\.\d+)?%|\b\d+(?:\.\d+)?\s?(?:k|m|b|million|billion)\b",
    re.IGNORECASE,
)
ENTITY_RE = re.compile(r"\b(?:[A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9&.-]+){0,3}|[A-Z]{2,})\b")

RELEASE_TERMS = (
    "launch",
    "launched",
    "release",
    "released",
    "introducing",
    "announced",
    "now available",
    "available today",
    "rollout",
    "new model",
    "new feature",
    "new capability",
    "partnership",
)
TASK_HINT_PATTERNS = {
    "release": (r"\brelease\b", r"\blaunched\b", r"\bintroducing\b", r"\bavailable\b"),
    "workflow": (r"\bworkflow\b", r"\bpipeline\b", r"\bsteps\b"),
    "tutorial": (r"\bguide\b", r"\bhow to\b", r"\btutorial\b"),
    "comparison": (r"\bvs\b", r"\bcompare\b", r"\bbenchmark\b"),
    "opinion_decode": (r"\bwhat this means\b", r"\bwhy\b", r"\bfuture\b"),
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_z(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).expanduser().resolve().read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compact_list(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = normalize_space(value)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        out.append(cleaned)
    return out


def canonicalize_x_url(url: str) -> str:
    cleaned = (url or "").strip()
    match = re.search(r"https?://nitter\.net/([^/]+)/status/(\d+)", cleaned, re.IGNORECASE)
    if match:
        return f"https://x.com/{match.group(1)}/status/{match.group(2)}"
    return cleaned


def release_signals(text: str) -> list[str]:
    lowered = text.lower()
    out = [term for term in RELEASE_TERMS if term in lowered]
    return compact_list(out)


def metric_signals(text: str) -> list[str]:
    return compact_list(METRIC_RE.findall(text))[:24]


def named_entities(text: str) -> list[str]:
    entities = []
    for match in ENTITY_RE.findall(text):
        token = normalize_space(match)
        if len(token) < 2:
            continue
        if token.lower() in {"rt", "pinned", "the", "and"}:
            continue
        entities.append(token)
    return compact_list(entities)[:28]


def task_hints(text: str) -> list[str]:
    lowered = text.lower()
    hints: list[str] = []
    for hint, patterns in TASK_HINT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lowered, re.IGNORECASE):
                hints.append(hint)
                break
    return compact_list(hints)


def build_fact_anchors(
    title: str,
    summary: str,
    release_hits: list[str],
    metric_hits: list[str],
    entities: list[str],
    linked_urls: list[str],
) -> list[str]:
    anchors: list[str] = [title]
    if summary:
        anchors.append(summary)
    anchors.extend(release_hits[:8])
    anchors.extend(metric_hits[:12])
    anchors.extend(entities[:16])
    anchors.extend(linked_urls[:8])
    return compact_list(anchors)[:40]


def display_name_by_handle(profile: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    entries = list(profile.get("benchmark_accounts") or []) + list(profile.get("manual_benchmark_accounts") or [])
    for entry in entries:
        if isinstance(entry, dict):
            handle = str(entry.get("handle") or entry.get("x_handle") or "").lstrip("@").strip()
            if not handle:
                continue
            mapping[handle.lower()] = str(entry.get("display_name") or entry.get("label") or handle)
    return mapping


def detect_x_article_url(post: dict[str, Any]) -> str | None:
    """Return the X Article URL if the post is an X Article, else None."""
    for field in ("title", "summary", "origin_url"):
        value = str(post.get(field, ""))
        match = X_ARTICLE_RE.search(value)
        if match:
            return f"https://x.com/i/article/{match.group(1)}"
    return None


def classify_post(post: dict[str, Any], official_handles: set[str]) -> str:
    """Classify a post into official_x, article_x, or post_x."""
    if detect_x_article_url(post) is not None:
        return "article_x"
    handle = str(post.get("account_handle") or post.get("author") or "").strip().lower()
    if handle in official_handles:
        return "official_x"
    return "post_x"


def build_source_item(
    post: dict[str, Any],
    *,
    fetched_at: str,
    display_name_map: dict[str, str],
    enrich_links: bool,
    max_links: int,
    link_timeout: int,
) -> dict[str, Any]:
    handle = str(post.get("account_handle") or post.get("author") or "").strip()
    handle_lower = handle.lower()
    canonical_url = canonicalize_x_url(post.get("origin_url", ""))
    title = normalize_space(post.get("title", ""))
    summary = normalize_space(post.get("summary", ""))
    base_text = "\n\n".join([part for part in [title, summary] if part]).strip()

    # Detect X Article and fetch full text
    article_url = detect_x_article_url(post)
    is_article = article_url is not None
    article_context: dict[str, Any] | None = None
    assembly_notes: list[str] = []

    if is_article and enrich_links:
        try:
            article_context = fetch_link_context(article_url, timeout=link_timeout, max_chars=5000)
            assembly_notes.append(f"x_article_fulltext:{article_url}")
        except Exception as exc:
            assembly_notes.append(f"x_article_fetch_failed:{article_url} ({type(exc).__name__})")

    url_candidates = [url for url in extract_urls(base_text) if is_external_link(url)]
    url_candidates = compact_list(url_candidates)[: max_links * 2]

    linked_contexts: list[dict[str, Any]] = []
    if enrich_links and url_candidates:
        for url in url_candidates[:max_links]:
            if article_url and url.rstrip("/") == article_url.rstrip("/"):
                continue
            try:
                linked = fetch_link_context(url, timeout=link_timeout)
                linked_contexts.append(linked)
            except Exception as exc:
                assembly_notes.append(f"linked_context_failed:{url} ({type(exc).__name__})")

    full_text_parts = [
        f"Post title: {title}",
        f"Post summary: {summary}" if summary else "",
        f"Canonical URL: {canonical_url}",
    ]

    source_assets = [
        {
            "asset_kind": "x_status",
            "url": canonical_url or post.get("origin_url", ""),
            "selected_for_text": True,
            "notes": "primary social source",
        },
        {
            "asset_kind": "nitter_rss_item",
            "url": post.get("origin_url", ""),
            "selected_for_text": False,
            "notes": "guest-mode rss origin",
        },
    ]

    # Add article full text if available
    if article_context:
        full_text_parts.append(f"X Article full text: {article_url}")
        full_text_parts.append(article_context["text"])
        source_assets.append(
            {
                "asset_kind": "x_article",
                "url": article_url,
                "selected_for_text": True,
                "notes": f"x article fulltext words={article_context['word_count']}",
            }
        )

    for index, linked in enumerate(linked_contexts, start=1):
        full_text_parts.append(f"Linked source {index}: {linked['url']}")
        full_text_parts.append(linked["text"])
        source_assets.append(
            {
                "asset_kind": linked["kind"],
                "url": linked["url"],
                "selected_for_text": True,
                "notes": f"linked context words={linked['word_count']}",
            }
        )
        assembly_notes.append(f"linked_context_used:{linked['url']}")

    full_text = "\n\n".join(part for part in full_text_parts if part).strip()
    combined_for_signals = "\n\n".join([title, summary, full_text])
    release_hits = release_signals(combined_for_signals)
    metric_hits = metric_signals(combined_for_signals)
    entity_hits = named_entities(combined_for_signals)
    hint_hits = task_hints(combined_for_signals)
    fact_hits = build_fact_anchors(
        title=title,
        summary=summary,
        release_hits=release_hits,
        metric_hits=metric_hits,
        entities=entity_hits,
        linked_urls=[entry["url"] for entry in linked_contexts],
    )

    source_kind = "x_article" if is_article else "x_thread"
    primary_text_source = "x_article_fulltext" if article_context else (
        "x_post_with_link_context" if linked_contexts else "x_post"
    )
    host = urlparse(canonical_url).netloc or "x.com"
    return {
        "schema_version": SCHEMA_VERSION,
        "source_id": post["source_id"],
        "fetched_at": fetched_at,
        "platform": "x",
        "source_kind": source_kind,
        "canonical_url": canonical_url or post.get("origin_url", ""),
        "author": {
            "handle": f"@{handle}" if handle else None,
            "display_name": display_name_map.get(handle_lower, handle or None),
            "account_url": f"https://x.com/{handle}" if handle else f"https://{host}",
        },
        "title": title or None,
        "language": post.get("language") or "unknown",
        "published_at": post.get("published_at") or None,
        "participants": [],
        "source_assets": source_assets,
        "content": {
            "primary_text_source": primary_text_source,
            "summary": summary or None,
            "full_text": full_text,
            "sections": compact_list(
                [
                    "x_article" if is_article else "x_post",
                    "linked_context" if linked_contexts else "",
                    "announcement" if "release" in hint_hits else "",
                ]
            ),
            "raw_quotes": [],
            "assembly_notes": "; ".join(assembly_notes) if assembly_notes else None,
        },
        "extracted_signals": {
            "release_signals": release_hits,
            "metric_signals": metric_hits,
            "named_entities": entity_hits,
            "task_hints": hint_hits,
            "fact_anchors": fact_hits,
            "normalization_notes": f"linked_context_count={len(linked_contexts)} is_article={is_article}",
        },
    }


def render_markdown(item: dict[str, Any]) -> str:
    lines = [
        f"# Source Item {item['source_id']}",
        "",
        f"- Platform: {item['platform']}",
        f"- Source Kind: {item['source_kind']}",
        f"- Canonical URL: {item['canonical_url']}",
        f"- Author: {item['author'].get('display_name') or item['author'].get('handle')}",
        f"- Published At: {item.get('published_at', '')}",
        "",
        "## Signals",
        f"- Release Signals: {', '.join(item['extracted_signals'].get('release_signals', []))}",
        f"- Task Hints: {', '.join(item['extracted_signals'].get('task_hints', []))}",
        f"- Fact Anchors: {len(item['extracted_signals'].get('fact_anchors', []))}",
        "",
        "## Content Preview",
        "",
        item["content"]["full_text"][:1500],
    ]
    return "\n".join(lines).rstrip() + "\n"


def load_official_handles(path: str | Path) -> set[str]:
    """Load official handle set (lowercased) from JSON profile or txt file."""
    p = Path(path).expanduser().resolve()
    if p.suffix == ".txt":
        return {
            line.strip().lstrip("@").lower()
            for line in p.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        }
    profile = load_json(p)
    entries = list(profile.get("benchmark_accounts") or []) + list(profile.get("manual_benchmark_accounts") or [])
    handles: set[str] = set()
    for entry in entries:
        if isinstance(entry, str):
            handles.add(entry.strip().lstrip("@").lower())
        elif isinstance(entry, dict):
            h = str(entry.get("handle") or entry.get("x_handle") or "").lstrip("@").strip().lower()
            if h:
                handles.add(h)
    return handles


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--guest-rss-catalog",
        action="append",
        required=True,
        help="Path to guest_rss_catalog.json (can be specified multiple times)",
    )
    parser.add_argument(
        "--account-profile",
        default="configs/image/official_x_account_profile.json",
        help="Path to official_x account profile for handle/display-name mapping.",
    )
    parser.add_argument(
        "--official-handles",
        default="configs/image/official_x_account_profile.json",
        help="Path to official handles file (JSON or txt) for classifying official_x vs post_x.",
    )
    parser.add_argument("--out-root", required=True, help="Directory where source_item artifacts will be written")
    parser.add_argument(
        "--schema",
        default="configs/frameworks/SOURCE_ITEM_SCHEMA.json",
        help="Path to SOURCE_ITEM_SCHEMA.json",
    )
    parser.add_argument("--max-links", type=int, default=2, help="Max linked external URLs to enrich per post")
    parser.add_argument("--link-timeout", type=int, default=25, help="Linked source fetch timeout in seconds")
    parser.add_argument("--disable-link-enrichment", action="store_true", help="Disable external link context fetch")
    args = parser.parse_args()

    # Merge posts from all catalogs
    all_posts: list[dict[str, Any]] = []
    catalog_refs: list[str] = []
    for catalog_path in args.guest_rss_catalog:
        catalog = load_json(catalog_path)
        all_posts.extend(catalog.get("posts", []))
        catalog_refs.append(str(Path(catalog_path).expanduser().resolve()))

    # Deduplicate by source_id
    seen_ids: set[str] = set()
    unique_posts: list[dict[str, Any]] = []
    for post in all_posts:
        sid = post.get("source_id", "")
        if sid and sid not in seen_ids:
            seen_ids.add(sid)
            unique_posts.append(post)

    profile = load_json(args.account_profile)
    official_handles = load_official_handles(args.official_handles)
    out_root = Path(args.out_root).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    source_schema = load_json(args.schema) if Path(args.schema).expanduser().resolve().exists() else None
    display_map = display_name_by_handle(profile)
    fetched_at = isoformat_z(utc_now())

    rows: list[dict[str, Any]] = []
    family_counts: dict[str, int] = {"official_x": 0, "article_x": 0, "post_x": 0}
    schema_errors = 0
    for post in unique_posts:
        family = classify_post(post, official_handles)
        # post_x only needs title+summary for heat signal — skip expensive link enrichment
        enrich = (not args.disable_link_enrichment) and (family != "post_x")
        item = build_source_item(
            post,
            fetched_at=fetched_at,
            display_name_map=display_map,
            enrich_links=enrich,
            max_links=max(1, args.max_links),
            link_timeout=max(5, args.link_timeout),
        )

        # Output to family subdirectory: out_root/official_x/{source_id}/
        target_dir = out_root / family / item["source_id"]
        target_dir.mkdir(parents=True, exist_ok=True)
        out_json = target_dir / "source_item.json"
        out_md = target_dir / "source_item.md"
        dump_json(out_json, item)
        out_md.write_text(render_markdown(item), encoding="utf-8")
        family_counts[family] = family_counts.get(family, 0) + 1

        schema_ok = True
        schema_error = ""
        if source_schema is not None and jsonschema_validate is not None:
            try:
                jsonschema_validate(item, source_schema)
            except Exception as exc:
                schema_ok = False
                schema_error = f"{type(exc).__name__}: {exc}"
                schema_errors += 1

        rows.append(
            {
                "source_id": item["source_id"],
                "source_family": family,
                "canonical_url": item["canonical_url"],
                "schema_ok": schema_ok,
                "schema_error": schema_error,
                "output_json": str(out_json),
                "output_md": str(out_md),
                "linked_context_count": sum(
                    1 for asset in item.get("source_assets", []) if str(asset.get("asset_kind", "")).startswith("linked_")
                ),
            }
        )
        status = f"{family}:ok" if schema_ok else f"{family}:schema_error"
        print(f"{item['source_id']} -> {status}")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": fetched_at,
        "guest_rss_catalog_refs": catalog_refs,
        "out_root": str(out_root),
        "count": len(rows),
        "family_counts": family_counts,
        "schema_errors": schema_errors,
        "results": rows,
    }
    dump_json(out_root / "source_item_manifest.json", manifest)
    print(f"source_items={manifest['count']} families={family_counts} schema_errors={schema_errors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
