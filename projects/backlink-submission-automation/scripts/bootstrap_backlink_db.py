#!/usr/bin/env python3
"""Initialize or extend a portable backlink campaign SQLite database."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS campaign_profile (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        source_id TEXT,
        domain TEXT NOT NULL,
        url TEXT NOT NULL,
        dr INTEGER,
        traffic INTEGER,
        category TEXT,
        submission_type TEXT DEFAULT 'unknown',
        priority INTEGER DEFAULT 0,
        relevance_score INTEGER DEFAULT 0,
        evidence_score INTEGER DEFAULT 0,
        status TEXT DEFAULT 'new',
        notes TEXT,
        discovered_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(source, url)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_table TEXT,
        source_id INTEGER,
        platform_domain TEXT,
        submit_url TEXT,
        target_url TEXT,
        anchor_text TEXT,
        submit_method TEXT,
        submit_time TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending',
        rel_actual TEXT,
        live_url TEXT,
        attempt_count INTEGER DEFAULT 0,
        last_error_signature TEXT,
        priority_tag TEXT,
        error_log TEXT,
        notes TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS submission_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_id INTEGER,
        source_table TEXT,
        source_id INTEGER,
        platform_domain TEXT,
        attempt_no INTEGER,
        status TEXT,
        error_signature TEXT,
        error_message TEXT,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS error_patterns (
        error_signature TEXT PRIMARY KEY,
        occurrence_count INTEGER DEFAULT 0,
        optimization_attempts INTEGER DEFAULT 0,
        status TEXT DEFAULT 'observed',
        priority_tag TEXT,
        first_seen TEXT DEFAULT CURRENT_TIMESTAMP,
        last_seen TEXT DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS account_credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform_domain TEXT NOT NULL,
        account_email TEXT,
        username TEXT,
        password TEXT,
        auth_method TEXT,
        credential_status TEXT,
        source_submission_id INTEGER,
        live_url TEXT,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(platform_domain, account_email, username)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS target_pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        page_type TEXT,
        priority INTEGER DEFAULT 1
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS anchor_texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anchor_text TEXT UNIQUE,
        type TEXT,
        use_count INTEGER DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS spam_blacklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain_pattern TEXT UNIQUE,
        reason TEXT,
        added_date TEXT DEFAULT CURRENT_DATE
    )
    """,
]


DEFAULT_SPAM = [
    ("*.lol", "low-quality spam TLD pattern"),
    ("*casino*", "spam niche"),
    ("*betting*", "spam niche"),
    ("*loan*", "spam niche"),
    ("*pharmacy*", "spam niche"),
    ("*viagra*", "spam niche"),
    ("backlink.*", "backlink farm pattern"),
    ("*-backlinks.*", "backlink farm pattern"),
]


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def upsert_profile(cur: sqlite3.Cursor, profile: dict) -> None:
    for key, value in profile.items():
        cur.execute(
            """
            INSERT INTO campaign_profile (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET
              value=excluded.value,
              updated_at=CURRENT_TIMESTAMP
            """,
            (key, json.dumps(value, ensure_ascii=False)),
        )


def table_columns(cur: sqlite3.Cursor, table: str) -> set[str]:
    return {row["name"] for row in cur.execute(f"PRAGMA table_info({table})").fetchall()}


def add_column_if_missing(cur: sqlite3.Cursor, table: str, column: str, definition: str) -> None:
    if column not in table_columns(cur, table):
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def migrate_existing_tables(cur: sqlite3.Cursor) -> None:
    add_column_if_missing(cur, "candidates", "relevance_score", "INTEGER DEFAULT 0")
    add_column_if_missing(cur, "candidates", "evidence_score", "INTEGER DEFAULT 0")
    add_column_if_missing(cur, "submissions", "target_url", "TEXT")
    add_column_if_missing(cur, "submissions", "attempt_count", "INTEGER DEFAULT 0")
    add_column_if_missing(cur, "submissions", "last_error_signature", "TEXT")
    add_column_if_missing(cur, "submissions", "priority_tag", "TEXT")


def default_anchors_from_profile(profile: dict) -> list[tuple[str, str]]:
    brand = profile.get("brand_name", "ExampleProduct")
    url = profile.get("canonical_url", "https://product.example/")
    positioning = profile.get("positioning", "productivity tool")
    audience = profile.get("audience", "teams")
    one_liner = profile.get("one_liner", f"{brand} helps {audience}.")
    anchors = [
        (brand, "brand"),
        (f"{brand} {positioning}", "brand"),
        (positioning, "lsi"),
        (f"{positioning} for {audience}", "lsi"),
        (f"tools like {brand}", "descriptive"),
        (one_liner, "descriptive"),
        (url, "naked"),
    ]
    configured = profile.get("anchors")
    if configured:
        anchors = [(row[0], row[1] if len(row) > 1 else "custom") for row in configured]
    return anchors


def seed_from_profile(cur: sqlite3.Cursor, profile: dict) -> None:
    canonical = profile.get("canonical_url")
    if canonical:
        cur.execute(
            "INSERT OR IGNORE INTO target_pages (url, page_type, priority) VALUES (?, ?, ?)",
            (canonical, "home", 1),
        )
    for anchor, anchor_type in default_anchors_from_profile(profile):
        cur.execute(
            "INSERT OR IGNORE INTO anchor_texts (anchor_text, type) VALUES (?, ?)",
            (anchor, anchor_type),
        )
    for pattern, reason in DEFAULT_SPAM:
        cur.execute(
            "INSERT OR IGNORE INTO spam_blacklist (domain_pattern, reason) VALUES (?, ?)",
            (pattern, reason),
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, help="Path to SQLite DB")
    parser.add_argument("--profile", help="Product/campaign profile JSON")
    args = parser.parse_args()

    db_path = Path(args.db)
    conn = connect(db_path)
    cur = conn.cursor()
    for statement in SCHEMA:
        cur.execute(statement)
    migrate_existing_tables(cur)

    profile = {}
    if args.profile:
        profile = json.loads(Path(args.profile).read_text(encoding="utf-8"))
        upsert_profile(cur, profile)
    seed_from_profile(cur, profile)

    conn.commit()
    print(f"Initialized {db_path.resolve()}")
    tables = [
        row["name"]
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    ]
    for table in tables:
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:<24} {count:>6}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
