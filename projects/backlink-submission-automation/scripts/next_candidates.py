#!/usr/bin/env python3
"""Select the next backlink candidates after DR, relevance, risk, and hold filters."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sqlite3
from pathlib import Path


STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "your",
    "tool",
    "tools",
    "product",
    "platform",
    "software",
    "https",
    "http",
    "www",
    "com",
}


def profile_value(cur: sqlite3.Cursor, key: str, default):
    row = cur.execute("SELECT value FROM campaign_profile WHERE key=?", (key,)).fetchone()
    if not row:
        return default
    try:
        return json.loads(row[0])
    except json.JSONDecodeError:
        return row[0]


def text_tokens(value) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, (list, tuple, set)):
        value = " ".join(str(item) for item in value)
    if isinstance(value, dict):
        value = " ".join(str(item) for item in value.values())
    text = str(value).lower()
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9+-]{2,}", text)
        if token not in STOP_WORDS
    }


def load_profile_terms(cur: sqlite3.Cursor) -> set[str]:
    keys = [
        "brand_name",
        "positioning",
        "audience",
        "primary_outcome",
        "categories",
        "tags",
        "one_liner",
        "short_description",
        "long_description",
    ]
    terms: set[str] = set()
    for key in keys:
        terms.update(text_tokens(profile_value(cur, key, "")))
    return terms


def load_patterns(cur: sqlite3.Cursor) -> list[str]:
    return [
        row[0].lower()
        for row in cur.execute("SELECT domain_pattern FROM spam_blacklist ORDER BY domain_pattern")
    ]


def is_blacklisted(domain: str, patterns: list[str]) -> bool:
    domain = (domain or "").lower()
    for pattern in patterns:
        p = pattern.lower()
        if "*" in p:
            if fnmatch.fnmatch(domain, p):
                return True
        elif domain == p or domain.endswith("." + p):
            return True
    return False


def is_manual_hold(domain: str, holds: list[str]) -> bool:
    domain = (domain or "").lower()
    for hold in holds:
        h = hold.lower().replace("www.", "")
        if domain == h or domain.endswith("." + h):
            return True
    return False


def relevance_score(row: sqlite3.Row, profile_terms: set[str]) -> int:
    if not profile_terms:
        return row["relevance_score"] or 0 if "relevance_score" in row.keys() else 0
    haystack = " ".join(
        str(row[key] or "")
        for key in ("domain", "url", "category", "submission_type", "notes")
        if key in row.keys()
    ).lower()
    hits = {term for term in profile_terms if term in haystack}
    dynamic = min(len(hits) * 4, 24)
    stored = row["relevance_score"] or 0 if "relevance_score" in row.keys() else 0
    return max(stored, dynamic)


def evidence_score(row: sqlite3.Row) -> int:
    stored = row["evidence_score"] or 0 if "evidence_score" in row.keys() else 0
    notes = (row["notes"] or "").lower()
    dynamic = 0
    if "dofollow" in notes:
        dynamic += 15
    if "submit" in notes or "list your" in notes or "website field" in notes:
        dynamic += 10
    if "public" in notes or "approved" in notes:
        dynamic += 5
    if "nofollow" in notes or "ugc" in notes or "sponsored" in notes:
        dynamic -= 10
    if "captcha" in notes or "manual_hold=true" in notes or "paid" in notes:
        dynamic -= 10
    return max(stored, dynamic, 0)


def score(row: sqlite3.Row, profile_terms: set[str]) -> int:
    dr = row["dr"] or 0
    s = row["priority"] or 0
    if dr >= 90:
        s += 50
    elif dr >= 70:
        s += 35
    elif dr >= 40:
        s += 20
    elif dr >= 20:
        s += 10
    st = (row["submission_type"] or "").lower()
    if st in ("github_pr", "directory", "showcase"):
        s += 25
    elif st in ("profile", "document", "media"):
        s += 12
    elif st == "blog_comment":
        s += 5
    elif st == "unknown":
        s -= 5
    s += relevance_score(row, profile_terms)
    s += evidence_score(row)
    return s


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--min-dr", type=int)
    parser.add_argument("--include-manual-hold", action="store_true")
    parser.add_argument("--include-low-dr", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    min_dr = args.min_dr
    if min_dr is None:
        min_dr = int(profile_value(cur, "min_dr", 20))
    profile_terms = load_profile_terms(cur)
    manual_holds = profile_value(cur, "manual_hold_domains", [])
    patterns = load_patterns(cur)

    rows = cur.execute(
        """
        SELECT *
        FROM candidates
        WHERE status IN ('new', 'queued')
        ORDER BY COALESCE(dr, 0) DESC, priority DESC, id ASC
        """
    ).fetchall()

    selected = []
    skipped = []
    for row in rows:
        domain = row["domain"]
        reason = None
        if is_blacklisted(domain, patterns):
            reason = "blacklist"
        elif not args.include_manual_hold and is_manual_hold(domain, manual_holds):
            reason = "manual_hold"
        elif not args.include_low_dr and (row["dr"] is not None) and row["dr"] < min_dr:
            reason = f"low_dr<{min_dr}"
        if reason:
            skipped.append({"id": row["id"], "domain": domain, "reason": reason})
            continue
        item = dict(row)
        item["relevance_score"] = relevance_score(row, profile_terms)
        item["evidence_score"] = evidence_score(row)
        item["score"] = score(row, profile_terms)
        selected.append(item)
    selected.sort(key=lambda r: (-r["score"], -(r.get("dr") or 0), r["id"]))
    selected = selected[: args.limit]

    if args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    else:
        print(f"Selected {len(selected)} candidates (min_dr={min_dr})")
        print("| id | score | rel | ev | DR | domain | type | url |")
        print("|---:|---:|---:|---:|---:|---|---|---|")
        for r in selected:
            print(
                f"| {r['id']} | {r['score']} | {r.get('relevance_score') or 0} | "
                f"{r.get('evidence_score') or 0} | {r.get('dr') or ''} | "
                f"{r['domain']} | {r.get('submission_type') or ''} | {r['url']} |"
            )
        if skipped:
            print(f"\nSkipped by filters: {len(skipped)}")
            for item in skipped[:10]:
                print(f"- #{item['id']} {item['domain']}: {item['reason']}")
            if len(skipped) > 10:
                print(f"- ... {len(skipped) - 10} more")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
