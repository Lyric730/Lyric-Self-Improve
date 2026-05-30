"""
Mark an approved 三分钟未来 issue as published.

This writes selected items into the channel ledger so later runs can avoid
repeating the same URL, title, topic, or image.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from published_ledger import LEDGER_PATH, LINE_NAME, PROJECT_ROOT, ledger_entry, load_ledger, save_ledger


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def work_dir_for(publish_date: str) -> Path:
    return PROJECT_ROOT / "daily" / publish_date / LINE_NAME / "work"


def load_issue(publish_date: str) -> tuple[dict[str, Any], str]:
    work_dir = work_dir_for(publish_date)
    final_path = work_dir / "final.json"
    selection_path = work_dir / "selection.json"
    if final_path.exists():
        return load_json(final_path), "final"
    if selection_path.exists():
        return load_json(selection_path), "selection"
    raise SystemExit(f"missing final.json or selection.json under {work_dir}")


def append_entries(ledger: dict[str, Any], entries: list[dict[str, Any]]) -> tuple[int, int]:
    existing = {
        (
            str(item.get("publishDate", "")),
            str(item.get("url", "")),
            str(item.get("topicKey", "")),
        )
        for item in ledger.get("items", [])
    }
    added = 0
    skipped = 0
    for entry in entries:
        key = (
            str(entry.get("publishDate", "")),
            str(entry.get("url", "")),
            str(entry.get("topicKey", "")),
        )
        if key in existing:
            skipped += 1
            continue
        ledger.setdefault("items", []).append(entry)
        existing.add(key)
        added += 1
    return added, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--vol", type=int, help="issue number; defaults to issue file vol")
    parser.add_argument("--content-date", help="override content date")
    args = parser.parse_args()

    issue, source = load_issue(args.date)
    content_date = args.content_date or issue.get("contentDate") or args.date
    vol = args.vol or int(issue.get("vol") or 0)
    if vol <= 0:
        raise SystemExit("missing vol; pass --vol")

    entries = [
        ledger_entry(item, args.date, content_date, vol)
        for item in issue.get("items", [])
    ]
    ledger = load_ledger()
    ledger["line"] = LINE_NAME
    ledger["updatedAt"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    added, skipped = append_entries(ledger, entries)
    save_ledger(ledger)
    print(f"OK ledger source={source} added={added} skipped={skipped} -> {LEDGER_PATH}")


if __name__ == "__main__":
    main()
