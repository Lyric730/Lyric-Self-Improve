#!/usr/bin/env python3
"""Verify public backlink rel from static HTML and optionally update submissions."""

from __future__ import annotations

import argparse
import html
import sqlite3
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict] = []
        self.text_parts: list[str] = []
        self._in_a = False
        self._current: dict | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        data = {k.lower(): v or "" for k, v in attrs}
        self._in_a = True
        self._current = {
            "href": data.get("href", ""),
            "rel": data.get("rel", ""),
            "text": "",
        }

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)
        if self._in_a and self._current is not None:
            self._current["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._current is not None:
            self.links.append(self._current)
            self._current = None
            self._in_a = False


def fetch_html(url: str, timeout: int) -> tuple[str, str]:
    req = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
            )
        },
    )
    with urlopen(req, timeout=timeout) as resp:
        content = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        return content.decode(charset, errors="replace"), resp.geturl()


def classify_rel(rel: str) -> str:
    tokens = set(rel.lower().replace(",", " ").split())
    if "sponsored" in tokens:
        return "sponsored"
    if "nofollow" in tokens and "ugc" in tokens:
        return "nofollow_ugc"
    if "nofollow" in tokens:
        return "nofollow"
    if "ugc" in tokens:
        return "ugc"
    if "me" in tokens:
        return "me_no_pagerank"
    return "dofollow"


def host_matches(href: str, target_domain: str) -> bool:
    if target_domain.lower() in href.lower() and href.startswith(("http://", "https://")):
        host = urlparse(href).netloc.lower().replace("www.", "")
        target = target_domain.lower().replace("www.", "")
        return host == target or host.endswith("." + target)
    return False


def verify(html_text: str, target_domain: str) -> dict:
    parser = LinkParser()
    parser.feed(html_text)
    matches = [link for link in parser.links if host_matches(link["href"], target_domain)]
    if matches:
        classified = []
        for link in matches:
            rel = html.unescape(link.get("rel") or "").strip().lower()
            classified.append(
                {
                    "href": link.get("href"),
                    "rel": rel,
                    "text": (link.get("text") or "").strip()[:120],
                    "rel_actual": classify_rel(rel),
                }
            )
        priority = {
            "dofollow": 0,
            "nofollow": 1,
            "ugc": 2,
            "nofollow_ugc": 3,
            "sponsored": 4,
            "me_no_pagerank": 5,
        }
        best = sorted(classified, key=lambda x: priority.get(x["rel_actual"], 9))[0]
        return {
            "status": "live",
            "rel_actual": best["rel_actual"],
            "matches": classified,
            "reason": "target_anchor_found",
        }
    body_text = " ".join(parser.text_parts)
    if target_domain.lower() in body_text.lower():
        return {
            "status": "live_plain_text",
            "rel_actual": "live_plain_text",
            "matches": [],
            "reason": "target_text_without_anchor",
        }
    return {
        "status": "failed",
        "rel_actual": "no_link_found",
        "matches": [],
        "reason": "target_not_found",
    }


def update_db(db: str, submission_id: int, result: dict, live_url: str) -> None:
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    columns = {row[1] for row in cur.execute("PRAGMA table_info(submissions)").fetchall()}
    if "verification_evidence" not in columns:
        cur.execute("ALTER TABLE submissions ADD COLUMN verification_evidence TEXT")
    if "verified_at" not in columns:
        cur.execute("ALTER TABLE submissions ADD COLUMN verified_at TEXT")
    note = f"verify_rel.py: {result['reason']}; matches={len(result['matches'])}"
    cur.execute(
        """
        UPDATE submissions
        SET status=?, rel_actual=?, live_url=COALESCE(?, live_url),
            verification_evidence=?,
            verified_at=CURRENT_TIMESTAMP,
            notes=CASE
                WHEN notes IS NULL OR notes='' THEN ?
                ELSE notes || char(10) || ?
            END
        WHERE id=?
        """,
        (
            result["status"],
            result["rel_actual"],
            live_url,
            note,
            note,
            note,
            submission_id,
        ),
    )
    conn.commit()
    conn.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url")
    parser.add_argument("--html-file")
    parser.add_argument("--target-domain", required=True)
    parser.add_argument("--db")
    parser.add_argument("--submission-id", type=int)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    if not args.url and not args.html_file:
        raise SystemExit("Provide --url or --html-file")

    live_url = args.url or str(Path(args.html_file).resolve())
    if args.html_file:
        html_text = Path(args.html_file).read_text(encoding="utf-8")
    else:
        html_text, live_url = fetch_html(args.url, args.timeout)

    result = verify(html_text, args.target_domain)
    print(result)
    if args.db and args.submission_id:
        update_db(args.db, args.submission_id, result, live_url)
        print(f"updated submission_id={args.submission_id}")
    return 0 if result["status"].startswith("live") else 2


if __name__ == "__main__":
    raise SystemExit(main())
