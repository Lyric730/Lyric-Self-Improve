#!/usr/bin/env python3
"""Record backlink submissions and account credentials in SQLite."""

from __future__ import annotations

import argparse
import hashlib
import sqlite3
from pathlib import Path


SUBMISSION_STATUSES = {
    "submitted",
    "pending",
    "pending_review",
    "pending_email_confirmation",
    "pending_human_verification",
    "blocked",
    "blocked_browser_controller",
    "blocked_captcha",
    "blocked_recaptcha",
    "blocked_turnstile",
    "blocked_auth",
    "failed",
    "failed_after_3_attempts",
    "skipped",
    "skipped_low_dr",
    "skipped_manual_hold",
    "skipped_no_submission_form",
    "skipped_no_public_link",
    "live",
    "live_plain_text",
}

REL_VALUES = {
    "unknown",
    "dofollow",
    "nofollow",
    "ugc",
    "nofollow_ugc",
    "sponsored",
    "me_no_pagerank",
    "live_plain_text",
    "no_link_found",
    "pending_expected_dofollow",
}

VERIFIED_STATUSES = {"live", "live_plain_text"}


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def table_columns(cur: sqlite3.Cursor, table: str) -> set[str]:
    return {row["name"] for row in cur.execute(f"PRAGMA table_info({table})").fetchall()}


def ensure_error_tables(cur: sqlite3.Cursor) -> None:
    cur.execute(
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
        """
    )
    cur.execute(
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
        """
    )
    submission_cols = table_columns(cur, "submissions")
    for column, definition in [
        ("target_url", "TEXT"),
        ("attempt_count", "INTEGER DEFAULT 0"),
        ("last_error_signature", "TEXT"),
        ("priority_tag", "TEXT"),
    ]:
        if column not in submission_cols:
            cur.execute(f"ALTER TABLE submissions ADD COLUMN {column} {definition}")


def target_url_column(cur: sqlite3.Cursor) -> str:
    columns = table_columns(cur, "submissions")
    if "target_url" in columns:
        return "target_url"
    cur.execute("ALTER TABLE submissions ADD COLUMN target_url TEXT")
    return "target_url"


def append_note(old: str | None, new: str | None) -> str | None:
    if not new:
        return old
    if not old:
        return new
    if new in old:
        return old
    return old.rstrip() + "\n" + new


def error_signature(value: str | None, message: str | None) -> str:
    if value:
        return value.strip().lower().replace(" ", "_")[:120]
    base = (message or "unknown_error").strip().lower()
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:10]
    return "error_" + digest


def validate_submission_args(args: argparse.Namespace) -> None:
    status = args.status or "pending"
    rel = args.rel or "unknown"
    if status not in SUBMISSION_STATUSES:
        allowed = ", ".join(sorted(SUBMISSION_STATUSES))
        raise SystemExit(f"unsupported submission status: {status}. Allowed: {allowed}")
    if rel not in REL_VALUES:
        allowed = ", ".join(sorted(REL_VALUES))
        raise SystemExit(f"unsupported rel value: {rel}. Allowed: {allowed}")
    if status in VERIFIED_STATUSES:
        if not args.live_url:
            raise SystemExit(f"status={status} requires --live-url")
        if not args.verified:
            raise SystemExit(
                f"status={status} requires --verified. Run verify_rel.py first, "
                "or manually inspect logged-out public HTML/DOM before recording."
            )
        if not args.evidence:
            raise SystemExit(f"status={status} requires --evidence with the public proof checked")
    if status == "live" and rel in {"unknown", "no_link_found", "pending_expected_dofollow", "live_plain_text"}:
        raise SystemExit("status=live requires a verified link rel such as dofollow/nofollow/ugc/sponsored")
    if status == "live_plain_text" and rel != "live_plain_text":
        raise SystemExit("status=live_plain_text requires --rel live_plain_text")


def record_submission(args: argparse.Namespace) -> int:
    validate_submission_args(args)
    conn = connect(args.db)
    cur = conn.cursor()
    ensure_error_tables(cur)
    target_col = target_url_column(cur)
    evidence_note = f"evidence: {args.evidence}" if args.evidence else None
    notes = append_note(args.notes, evidence_note)

    if args.id:
        existing = cur.execute("SELECT notes FROM submissions WHERE id=?", (args.id,)).fetchone()
        if not existing:
            raise SystemExit(f"submission id not found: {args.id}")
        cur.execute(
            f"""
            UPDATE submissions
            SET platform_domain=COALESCE(?, platform_domain),
                submit_url=COALESCE(?, submit_url),
                {target_col}=COALESCE(?, {target_col}),
                anchor_text=COALESCE(?, anchor_text),
                submit_method=COALESCE(?, submit_method),
                status=COALESCE(?, status),
                rel_actual=COALESCE(?, rel_actual),
                live_url=COALESCE(?, live_url),
                error_log=COALESCE(?, error_log),
                notes=?
            WHERE id=?
            """,
            (
                args.platform,
                args.submit_url,
                args.target_url,
                args.anchor_text,
                args.method,
                args.status,
                args.rel,
                args.live_url,
                args.error_log,
                append_note(existing["notes"], notes),
                args.id,
            ),
        )
        submission_id = args.id
    else:
        cur.execute(
            f"""
            INSERT INTO submissions (
                source_table, source_id, platform_domain, submit_url, {target_col},
                anchor_text, submit_method, status, rel_actual, live_url, error_log, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                args.source_table,
                args.source_id,
                args.platform,
                args.submit_url,
                args.target_url,
                args.anchor_text,
                args.method,
                args.status or "pending",
                args.rel or "unknown",
                args.live_url,
                args.error_log,
                notes,
            ),
        )
        submission_id = cur.lastrowid

    if args.source_table == "candidates" and args.source_id:
        candidate_status = "submitted"
        if args.status and args.status.startswith("skipped"):
            candidate_status = "skipped"
        elif args.status and args.status.startswith("blocked"):
            candidate_status = "blocked"
        elif args.status in {"failed", "failed_after_3_attempts"}:
            candidate_status = "failed"
        elif args.status in {"live", "live_plain_text"}:
            candidate_status = "live"
        cur.execute(
            "UPDATE candidates SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (candidate_status, args.source_id),
        )

    conn.commit()
    print(f"submission_id={submission_id}")
    conn.close()
    return 0


def record_error(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    ensure_error_tables(cur)
    signature = error_signature(args.error_signature, args.error_message)
    attempt_no = args.attempt_no
    if attempt_no is None and args.submission_id:
        attempt_no = (
            cur.execute(
                "SELECT COALESCE(MAX(attempt_no), 0) + 1 FROM submission_attempts WHERE submission_id=?",
                (args.submission_id,),
            ).fetchone()[0]
        )
    attempt_no = attempt_no or 1
    if attempt_no > 3:
        attempt_no = 3

    cur.execute(
        """
        INSERT INTO submission_attempts (
            submission_id, source_table, source_id, platform_domain, attempt_no,
            status, error_signature, error_message, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            args.submission_id,
            args.source_table,
            args.source_id,
            args.platform,
            attempt_no,
            args.status or "failed",
            signature,
            args.error_message,
            args.notes,
        ),
    )
    cur.execute(
        """
        INSERT INTO error_patterns (
            error_signature, occurrence_count, optimization_attempts,
            status, priority_tag, notes, last_seen
        )
        VALUES (?, 1, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(error_signature) DO UPDATE SET
            occurrence_count=occurrence_count + 1,
            optimization_attempts=optimization_attempts + ?,
            last_seen=CURRENT_TIMESTAMP,
            notes=CASE
                WHEN excluded.notes IS NULL OR excluded.notes='' THEN notes
                WHEN notes IS NULL OR notes='' THEN excluded.notes
                ELSE notes || char(10) || excluded.notes
            END
        """,
        (
            signature,
            1 if args.optimization_attempted else 0,
            "optimization_attempted" if args.optimization_attempted else "observed",
            None,
            args.notes,
            1 if args.optimization_attempted else 0,
        ),
    )

    pattern = cur.execute(
        "SELECT occurrence_count, optimization_attempts FROM error_patterns WHERE error_signature=?",
        (signature,),
    ).fetchone()
    occurrence_count = pattern["occurrence_count"]
    optimization_attempts = pattern["optimization_attempts"]
    pattern_status = "observed"
    priority_tag = None
    should_stop = False
    if occurrence_count >= 3:
        if args.after_optimization or optimization_attempts >= 1:
            pattern_status = "unresolved_high_priority"
            priority_tag = "HIGH_PRIORITY_FIX"
            should_stop = False
        else:
            pattern_status = "needs_optimization"
            priority_tag = "HIGH_PRIORITY_FIX"
            should_stop = True
    cur.execute(
        "UPDATE error_patterns SET status=?, priority_tag=? WHERE error_signature=?",
        (pattern_status, priority_tag, signature),
    )

    if args.submission_id:
        submission_cols = table_columns(cur, "submissions")
        updates = ["status=?", "error_log=COALESCE(?, error_log)"]
        values = [
            "failed_after_3_attempts" if attempt_no >= 3 else "failed",
            args.error_message,
        ]
        if "attempt_count" in submission_cols:
            updates.append("attempt_count=?")
            values.append(attempt_no)
        if "last_error_signature" in submission_cols:
            updates.append("last_error_signature=?")
            values.append(signature)
        if "priority_tag" in submission_cols and priority_tag:
            updates.append("priority_tag=?")
            values.append(priority_tag)
        values.append(args.submission_id)
        cur.execute(
            f"UPDATE submissions SET {', '.join(updates)} WHERE id=?",
            values,
        )

    if args.source_table == "candidates" and args.source_id and attempt_no >= 3:
        cur.execute(
            "UPDATE candidates SET status='failed', updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (args.source_id,),
        )

    conn.commit()
    print(
        f"error_signature={signature} occurrences={occurrence_count} "
        f"pattern_status={pattern_status} attempt_no={attempt_no}"
    )
    if should_stop:
        print("STOP_BATCH_FOR_OPTIMIZATION=1")
    conn.close()
    return 0


def mark_optimization(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    cur = conn.cursor()
    ensure_error_tables(cur)
    signature = error_signature(args.error_signature, None)
    cur.execute(
        """
        INSERT INTO error_patterns (
            error_signature, occurrence_count, optimization_attempts,
            status, priority_tag, notes, last_seen
        )
        VALUES (?, 0, 1, 'optimization_attempted', 'HIGH_PRIORITY_FIX', ?, CURRENT_TIMESTAMP)
        ON CONFLICT(error_signature) DO UPDATE SET
            optimization_attempts=optimization_attempts + 1,
            status='optimization_attempted',
            priority_tag='HIGH_PRIORITY_FIX',
            last_seen=CURRENT_TIMESTAMP,
            notes=CASE
                WHEN notes IS NULL OR notes='' THEN excluded.notes
                ELSE notes || char(10) || excluded.notes
            END
        """,
        (signature, args.notes),
    )
    conn.commit()
    print(f"optimization_recorded={signature}")
    conn.close()
    return 0


def record_account(args: argparse.Namespace) -> int:
    conn = connect(args.db)
    cur = conn.cursor()
    ensure_error_tables(cur)
    cur.execute(
        """
        INSERT INTO account_credentials (
            platform_domain, account_email, username, password, auth_method,
            credential_status, source_submission_id, live_url, notes, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(platform_domain, account_email, username) DO UPDATE SET
            password=excluded.password,
            auth_method=excluded.auth_method,
            credential_status=excluded.credential_status,
            source_submission_id=excluded.source_submission_id,
            live_url=excluded.live_url,
            notes=excluded.notes,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            args.platform,
            args.email,
            args.username or "",
            args.password,
            args.auth_method,
            args.credential_status,
            args.source_submission_id,
            args.live_url,
            args.notes,
        ),
    )
    conn.commit()
    print(f"account={args.platform} {args.email or ''} {args.username or ''}".strip())
    conn.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    s = sub.add_parser("submission")
    s.add_argument("--db", required=True)
    s.add_argument("--id", type=int)
    s.add_argument("--source-table")
    s.add_argument("--source-id", type=int)
    s.add_argument("--platform")
    s.add_argument("--submit-url")
    s.add_argument("--target-url")
    s.add_argument("--anchor-text")
    s.add_argument("--method", default="browser")
    s.add_argument("--status")
    s.add_argument("--rel")
    s.add_argument("--live-url")
    s.add_argument("--verified", action="store_true")
    s.add_argument("--evidence")
    s.add_argument("--error-log")
    s.add_argument("--notes")
    s.set_defaults(func=record_submission)

    e = sub.add_parser("error")
    e.add_argument("--db", required=True)
    e.add_argument("--submission-id", type=int)
    e.add_argument("--source-table")
    e.add_argument("--source-id", type=int)
    e.add_argument("--platform")
    e.add_argument("--attempt-no", type=int)
    e.add_argument("--status", default="failed")
    e.add_argument("--error-signature")
    e.add_argument("--error-message", required=True)
    e.add_argument("--notes")
    e.add_argument("--optimization-attempted", action="store_true")
    e.add_argument("--after-optimization", action="store_true")
    e.set_defaults(func=record_error)

    o = sub.add_parser("optimization")
    o.add_argument("--db", required=True)
    o.add_argument("--error-signature", required=True)
    o.add_argument("--notes", required=True)
    o.set_defaults(func=mark_optimization)

    a = sub.add_parser("account")
    a.add_argument("--db", required=True)
    a.add_argument("--platform", required=True)
    a.add_argument("--email")
    a.add_argument("--username")
    a.add_argument("--password")
    a.add_argument("--auth-method", default="email_password")
    a.add_argument("--credential-status", default="confirmed")
    a.add_argument("--source-submission-id", type=int)
    a.add_argument("--live-url")
    a.add_argument("--notes")
    a.set_defaults(func=record_account)

    args = parser.parse_args()
    if not Path(args.db).exists():
        raise SystemExit(f"DB not found: {args.db}")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
