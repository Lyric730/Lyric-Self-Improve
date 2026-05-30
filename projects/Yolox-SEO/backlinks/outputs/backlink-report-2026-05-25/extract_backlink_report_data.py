import json
import re
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "backlinks.db"
OUT_DIR = Path(__file__).resolve().parent
OUT_JSON = OUT_DIR / "backlink_report_data.json"


MANUAL_CREDENTIALS = [
    {
        "platform_domain": "picturepush.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "yoloxai",
        "password": "YoloxPP26!4kv",
        "auth_method": "email_password",
        "source_submission_id": 236,
        "credential_status": "confirmed",
        "notes": "PicturePush account created; public page is plain text only, not SEO backlink.",
    },
    {
        "platform_domain": "peertube.ch",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "yoloxai",
        "password": "YoloxPT26!7qv",
        "auth_method": "email_password",
        "source_submission_id": 256,
        "credential_status": "pending_email_confirmation",
        "notes": "PeerTube account request submitted; waiting email verification/approval.",
    },
    {
        "platform_domain": "slideshare.net",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "",
        "password": "YoloxSS26!8kp",
        "auth_method": "email_password",
        "source_submission_id": 212,
        "credential_status": "pending_human_verification",
        "notes": "SlideShare/Scribd account created; upload blocked by human verification.",
    },
    {
        "platform_domain": "clipix.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "",
        "password": "YoloxCX26!5r",
        "auth_method": "email_password",
        "source_submission_id": 205,
        "credential_status": "confirmed",
        "notes": "Clipix account created; public route shows URL as plain text only.",
    },
    {
        "platform_domain": "adlandpro.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "",
        "password": "Yolox-AD-2026!7Qp9",
        "auth_method": "email_password",
        "source_submission_id": 199,
        "credential_status": "pending_email_activation",
        "notes": "Digital Adlandpro account registered; activation required before posting.",
    },
    {
        "platform_domain": "isblog.net",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "yoloxai",
        "password": "Yolox-IB-2026!5Rt8",
        "auth_method": "email_password",
        "source_submission_id": 202,
        "credential_status": "attempted_blocked_captcha",
        "notes": "Signup attempted for yoloxai.isblog.net; captcha blocked completion.",
    },
    {
        "platform_domain": "saashub.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "yolox-ai",
        "password": "缺失：历史未归档，需找回或重置",
        "auth_method": "email_password",
        "source_submission_id": 115,
        "credential_status": "missing_password",
        "notes": "Account/email verification completed, but password was intentionally not archived in earlier notes.",
    },
    {
        "platform_domain": "startupinspire.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "",
        "password": "缺失：历史未归档，需找回或重置",
        "auth_method": "email_password",
        "source_submission_id": 121,
        "credential_status": "missing_password",
        "notes": "Login succeeded after activation and product is under review; exact password not present in DB notes.",
    },
    {
        "platform_domain": "trendystartups.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "Yolox Team",
        "password": "缺失/疑似无效：需重置",
        "auth_method": "email_password",
        "source_submission_id": 113,
        "credential_status": "login_failed_reset_needed",
        "notes": "Account was created, but later login failed with saved/reported credentials.",
    },
    {
        "platform_domain": "heylink.me",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "yoloxai",
        "password": "缺失：历史备注要求不存，需找回或重置",
        "auth_method": "email_password",
        "source_submission_id": 196,
        "credential_status": "missing_password",
        "notes": "Email verification required before public link can be finalized.",
    },
    {
        "platform_domain": "ipernity.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "Yolox Team",
        "password": "缺失：历史未归档，需找回或重置",
        "auth_method": "email_password",
        "source_submission_id": 179,
        "credential_status": "missing_password",
        "notes": "Account exists but requires email confirmation before editing profile.",
    },
    {
        "platform_domain": "blogzet.com",
        "account_email": "liuyouxuan570@gmail.com",
        "username": "yoloxai",
        "password": "缺失：历史未归档，需找回或重置",
        "auth_method": "email_password",
        "source_submission_id": 193,
        "credential_status": "missing_password",
        "notes": "Live dofollow blog post exists; login credential was not preserved in notes.",
    },
    {
        "platform_domain": "flipsnack.com",
        "account_email": "fabry.coffee",
        "username": "",
        "password": "Google OAuth：不单独留存站点密码",
        "auth_method": "google_oauth",
        "source_submission_id": 152,
        "credential_status": "oauth",
        "notes": "Used Google login; published flipbook is nofollow and trial-expiring.",
    },
    {
        "platform_domain": "gifyu.com",
        "account_email": "fabry.coffee",
        "username": "",
        "password": "Google OAuth：不单独留存站点密码",
        "auth_method": "google_oauth",
        "source_submission_id": 178,
        "credential_status": "oauth",
        "notes": "Used Google login; profile link verified nofollow.",
    },
    {
        "platform_domain": "files.fm",
        "account_email": "fabry.coffee",
        "username": "",
        "password": "Google OAuth：不单独留存站点密码",
        "auth_method": "google_oauth",
        "source_submission_id": 176,
        "credential_status": "oauth",
        "notes": "Used Google login; profile link verified nofollow.",
    },
    {
        "platform_domain": "pitchwall.co",
        "account_email": "fabry.coffee",
        "username": "yolox",
        "password": "Google OAuth：不单独留存站点密码",
        "auth_method": "google_oauth",
        "source_submission_id": 108,
        "credential_status": "oauth",
        "notes": "Used Google login; product under review and current outbound is nofollow redirect.",
    },
    {
        "platform_domain": "4shared.com",
        "account_email": "fabry.coffee",
        "username": "",
        "password": "Google OAuth：不单独留存站点密码",
        "auth_method": "google_oauth",
        "source_submission_id": 155,
        "credential_status": "oauth",
        "notes": "Used Google login; uploaded public file but public access currently 403/blocked.",
    },
    {
        "platform_domain": "easel.ly",
        "account_email": "fabry.coffee",
        "username": "",
        "password": "Google OAuth：不单独留存站点密码",
        "auth_method": "google_oauth",
        "source_submission_id": 154,
        "credential_status": "oauth",
        "notes": "Used Google login; public visibility requires paid account.",
    },
]


def fetch_all(cur, sql, params=()):
    return [dict(row) for row in cur.execute(sql, params).fetchall()]


def count(cur, sql):
    return cur.execute(sql).fetchone()[0]


def upsert_credentials(cur, rows):
    cur.execute(
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
        """
    )
    for row in rows:
        cur.execute(
            """
            INSERT INTO account_credentials (
                platform_domain, account_email, username, password, auth_method,
                credential_status, source_submission_id, live_url, notes, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
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
                row.get("platform_domain"),
                row.get("account_email"),
                row.get("username", ""),
                row.get("password"),
                row.get("auth_method"),
                row.get("credential_status"),
                row.get("source_submission_id"),
                row.get("live_url"),
                row.get("notes"),
            ),
        )


def enrich_credentials(conn):
    cur = conn.cursor()
    rows = []
    for cred in MANUAL_CREDENTIALS:
        row = dict(cred)
        if row.get("source_submission_id"):
            submission = cur.execute(
                "SELECT status, rel_actual, live_url FROM submissions WHERE id=?",
                (row["source_submission_id"],),
            ).fetchone()
            if submission:
                row["live_url"] = submission["live_url"]
                row["notes"] = (
                    f"Submission status={submission['status']}; rel={submission['rel_actual']}. "
                    + row.get("notes", "")
                )
        rows.append(row)
    upsert_credentials(cur, rows)
    conn.commit()


def extract_credentials_from_notes(notes):
    if not notes:
        return []
    found = []
    email_pass = re.findall(
        r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\s*/\s*([^,\s;]+)",
        notes,
    )
    for email, password in email_pass:
        found.append((email, password))
    return found


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    enrich_credentials(conn)

    submissions = fetch_all(
        cur,
        """
        SELECT
            s.id,
            s.source_table,
            s.source_id,
            s.platform_domain,
            COALESCE(l.dr, '') AS dr,
            COALESCE(l.category, '') AS category,
            s.submit_url,
            s.target_yolox_url,
            s.anchor_text,
            s.submit_method,
            s.submit_time,
            s.status,
            COALESCE(s.rel_actual, '') AS rel_actual,
            COALESCE(s.live_url, '') AS live_url,
            COALESCE(s.error_log, '') AS error_log,
            COALESCE(s.notes, '') AS notes
        FROM submissions s
        LEFT JOIN lxx_ai l
            ON s.source_table='lxx_ai' AND s.source_id=l.id
        ORDER BY s.id DESC
        """,
    )

    status_counts = fetch_all(
        cur,
        """
        SELECT status, COUNT(*) AS count
        FROM submissions
        GROUP BY status
        ORDER BY count DESC, status
        """,
    )
    rel_counts = fetch_all(
        cur,
        """
        SELECT COALESCE(rel_actual, 'NULL') AS rel_actual, COUNT(*) AS count
        FROM submissions
        GROUP BY COALESCE(rel_actual, 'NULL')
        ORDER BY count DESC, rel_actual
        """,
    )
    accounts = fetch_all(
        cur,
        """
        SELECT
            c.platform_domain,
            c.account_email,
            c.username,
            c.password,
            c.auth_method,
            c.credential_status,
            c.source_submission_id,
            COALESCE(s.status, '') AS submission_status,
            COALESCE(s.rel_actual, '') AS rel_actual,
            COALESCE(c.live_url, s.live_url, '') AS live_url,
            c.notes,
            c.updated_at
        FROM account_credentials c
        LEFT JOIN submissions s ON s.id = c.source_submission_id
        ORDER BY
            CASE c.credential_status
                WHEN 'confirmed' THEN 1
                WHEN 'pending_email_confirmation' THEN 2
                WHEN 'pending_email_activation' THEN 3
                WHEN 'pending_human_verification' THEN 4
                WHEN 'missing_password' THEN 5
                WHEN 'oauth' THEN 6
                ELSE 7
            END,
            c.platform_domain
        """,
    )
    live_links = fetch_all(
        cur,
        """
        SELECT id, platform_domain, status, COALESCE(rel_actual, '') AS rel_actual,
               COALESCE(live_url, '') AS live_url, COALESCE(notes, '') AS notes
        FROM submissions
        WHERE status LIKE 'live%' OR rel_actual='dofollow'
        ORDER BY
            CASE WHEN status='live' AND rel_actual='dofollow' THEN 0 ELSE 1 END,
            id DESC
        """,
    )
    pending_next = fetch_all(
        cur,
        """
        SELECT id, platform_domain, status, COALESCE(rel_actual, '') AS rel_actual,
               COALESCE(live_url, '') AS live_url, COALESCE(notes, '') AS notes
        FROM submissions
        WHERE status LIKE 'pending%' OR status LIKE '%review%' OR status LIKE '%approval%'
        ORDER BY id DESC
        """,
    )

    summary = [
        {"metric": "Report generated", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"metric": "Database", "value": str(DB_PATH)},
        {"metric": "lxx_ai candidates", "value": count(cur, "SELECT COUNT(*) FROM lxx_ai")},
        {"metric": "submissions records", "value": count(cur, "SELECT COUNT(*) FROM submissions")},
        {"metric": "gefei_226 pool", "value": count(cur, "SELECT COUNT(*) FROM gefei_226")},
        {"metric": "ahrefs_api_results", "value": count(cur, "SELECT COUNT(*) FROM ahrefs_api_results")},
        {
            "metric": "KPI: live dofollow",
            "value": count(cur, "SELECT COUNT(*) FROM submissions WHERE status='live' AND rel_actual='dofollow'"),
        },
        {"metric": "Account credential rows", "value": count(cur, "SELECT COUNT(*) FROM account_credentials")},
    ]

    out = {
        "summary": summary,
        "status_counts": status_counts,
        "rel_counts": rel_counts,
        "accounts": accounts,
        "live_links": live_links,
        "pending_next": pending_next,
        "submissions": submissions,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT_JSON)


if __name__ == "__main__":
    main()
