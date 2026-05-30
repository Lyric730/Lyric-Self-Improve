#!/usr/bin/env python3
"""Print a concise backlink campaign status report from SQLite."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def table_exists(cur: sqlite3.Cursor, name: str) -> bool:
    return (
        cur.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?",
            (name,),
        ).fetchone()[0]
        > 0
    )


def scalar(cur: sqlite3.Cursor, sql: str, params=()) -> int:
    return cur.execute(sql, params).fetchone()[0]


def print_counts(cur: sqlite3.Cursor, table: str, col: str) -> None:
    if not table_exists(cur, table):
        return
    print(f"\n## {table}.{col}")
    for row in cur.execute(
        f"SELECT COALESCE({col}, 'NULL') value, COUNT(*) count FROM {table} GROUP BY COALESCE({col}, 'NULL') ORDER BY count DESC, value"
    ):
        print(f"- {row['value']}: {row['count']}")


def print_rows(cur: sqlite3.Cursor, title: str, sql: str, limit: int) -> None:
    print(f"\n## {title}")
    rows = cur.execute(sql, (limit,)).fetchall()
    if not rows:
        print("- none")
        return
    headers = rows[0].keys()
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        values = []
        for h in headers:
            v = "" if row[h] is None else str(row[h]).replace("\n", " ")[:140]
            values.append(v)
        print("| " + " | ".join(values) + " |")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if not Path(args.db).exists():
        raise SystemExit(f"DB not found: {args.db}")
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("# Backlink Campaign Report")
    for table in ("candidates", "submissions", "account_credentials"):
        if table_exists(cur, table):
            print(f"- {table}: {scalar(cur, f'SELECT COUNT(*) FROM {table}')}")
    if table_exists(cur, "submission_attempts"):
        print(f"- submission_attempts: {scalar(cur, 'SELECT COUNT(*) FROM submission_attempts')}")
    if table_exists(cur, "error_patterns"):
        unresolved = scalar(
            cur,
            "SELECT COUNT(*) FROM error_patterns WHERE status='unresolved_high_priority'",
        )
        print(f"- high-priority unresolved errors: {unresolved}")
    if table_exists(cur, "submissions"):
        print(
            "- KPI live dofollow: "
            + str(
                scalar(
                    cur,
                    "SELECT COUNT(*) FROM submissions WHERE status='live' AND rel_actual='dofollow'",
                )
            )
        )

    print_counts(cur, "submissions", "status")
    print_counts(cur, "submissions", "rel_actual")
    print_counts(cur, "account_credentials", "credential_status")
    print_counts(cur, "error_patterns", "status")

    if table_exists(cur, "submissions"):
        print_rows(
            cur,
            "Live Dofollow",
            """
            SELECT platform_domain, live_url, rel_actual, submit_time
            FROM submissions
            WHERE status='live' AND rel_actual='dofollow'
            ORDER BY submit_time DESC
            LIMIT ?
            """,
            args.limit,
        )
        print_rows(
            cur,
            "Pending Work",
            """
            SELECT platform_domain, status, rel_actual, live_url, submit_time
            FROM submissions
            WHERE status LIKE 'pending%' OR status LIKE '%review%' OR status LIKE '%approval%'
            ORDER BY submit_time DESC
            LIMIT ?
            """,
            args.limit,
        )
    if table_exists(cur, "account_credentials"):
        print_rows(
            cur,
            "Accounts",
            """
            SELECT platform_domain, account_email, username, auth_method, credential_status, updated_at
            FROM account_credentials
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            args.limit,
        )
    if table_exists(cur, "error_patterns"):
        print_rows(
            cur,
            "High Priority Error Patterns",
            """
            SELECT error_signature, occurrence_count, optimization_attempts, status, priority_tag, last_seen
            FROM error_patterns
            WHERE occurrence_count >= 3 OR status='unresolved_high_priority'
            ORDER BY
                CASE status WHEN 'unresolved_high_priority' THEN 0 WHEN 'needs_optimization' THEN 1 ELSE 2 END,
                occurrence_count DESC
            LIMIT ?
            """,
            args.limit,
        )
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
