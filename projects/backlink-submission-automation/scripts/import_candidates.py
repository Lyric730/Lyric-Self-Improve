#!/usr/bin/env python3
"""Import backlink candidates from CSV into the canonical candidates table."""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path
from urllib.parse import urlparse


def table_columns(cur: sqlite3.Cursor, table: str) -> set[str]:
    return {row["name"] for row in cur.execute(f"PRAGMA table_info({table})").fetchall()}


def add_column_if_missing(cur: sqlite3.Cursor, table: str, column: str, definition: str) -> None:
    if column not in table_columns(cur, table):
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def ensure_candidate_columns(cur: sqlite3.Cursor) -> None:
    add_column_if_missing(cur, "candidates", "relevance_score", "INTEGER DEFAULT 0")
    add_column_if_missing(cur, "candidates", "evidence_score", "INTEGER DEFAULT 0")


def normalize_domain(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if "://" not in value:
        value = "https://" + value
    host = urlparse(value).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def infer_type(row: dict) -> str:
    haystack = " ".join(
        str(row.get(k, "")) for k in ("category", "submission_type", "url", "notes")
    ).lower()
    if "github" in haystack or "awesome" in haystack:
        return "github_pr"
    if "comment" in haystack:
        return "blog_comment"
    if "classified" in haystack or "ads" in haystack:
        return "classified"
    if "profile" in haystack or "account" in haystack:
        return "profile"
    if "pdf" in haystack or "document" in haystack or "slides" in haystack:
        return "document"
    if "media" in haystack or "image" in haystack:
        return "media"
    if "directory" in haystack or "tool" in haystack or "startup" in haystack:
        return "directory"
    return "unknown"


def to_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).strip()))
    except ValueError:
        return None


def infer_evidence_score(row: dict) -> int:
    text = " ".join(str(row.get(k, "")) for k in ("notes", "category", "submission_type")).lower()
    score = 0
    if "dofollow" in text:
        score += 15
    if "submit" in text or "list your" in text or "website field" in text:
        score += 10
    if "public" in text or "approved" in text:
        score += 5
    if "nofollow" in text or "ugc" in text or "sponsored" in text:
        score -= 10
    if "manual_hold=true" in text or "captcha" in text or "paid" in text:
        score -= 10
    return max(score, 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--source", default="csv")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    ensure_candidate_columns(cur)
    csv_path = Path(args.csv)
    count = 0
    skipped = 0

    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            url = (row.get("url") or row.get("submit_url") or row.get("backlink_url") or "").strip()
            domain = normalize_domain(row.get("domain") or row.get("root_domain") or url)
            if not url or not domain:
                skipped += 1
                continue
            submission_type = (row.get("submission_type") or "").strip() or infer_type(row)
            cur.execute(
                """
                INSERT INTO candidates (
                    source, source_id, domain, url, dr, traffic, category,
                    submission_type, priority, relevance_score, evidence_score,
                    status, notes, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?, CURRENT_TIMESTAMP)
                ON CONFLICT(source, url) DO UPDATE SET
                    domain=excluded.domain,
                    dr=excluded.dr,
                    traffic=excluded.traffic,
                    category=excluded.category,
                    submission_type=excluded.submission_type,
                    priority=excluded.priority,
                    relevance_score=excluded.relevance_score,
                    evidence_score=excluded.evidence_score,
                    notes=excluded.notes,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (
                    row.get("source") or args.source,
                    row.get("id") or row.get("source_id"),
                    domain,
                    url,
                    to_int(row.get("dr")),
                    to_int(row.get("traffic")),
                    row.get("category"),
                    submission_type,
                    to_int(row.get("priority")) or 0,
                    to_int(row.get("relevance_score")) or 0,
                    to_int(row.get("evidence_score")) or infer_evidence_score(row),
                    row.get("notes"),
                ),
            )
            count += 1
    conn.commit()
    print(f"Imported/updated {count} candidates from {csv_path}")
    if skipped:
        print(f"Skipped {skipped} rows without url/domain")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
