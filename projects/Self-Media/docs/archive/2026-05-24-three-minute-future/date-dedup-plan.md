# Three-Minute Future Date And Dedup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `三分钟未来` default to `contentDate = publishDate - 1 day` while supporting same-day incremental issues that exclude already-published topics.

**Architecture:** Add a small published-ledger module under `lines/three-minute-future/`, keep mutable ledger data under `daily/_state/three-minute-future/`, and wire filtering into selection. `run_daily.py` owns date defaults; `fetch_candidates.py` continues to receive an explicit `contentDate`.

**Tech Stack:** Python 3.13 standard library, existing JSON work files, existing PowerShell pipeline commands.

---

## File Structure

- Modify `lines/three-minute-future/run_daily.py`: infer default `contentDate = publishDate - 1 day`, pass it to fetch, and record it in `run-report.json`.
- Create `lines/three-minute-future/published_ledger.py`: ledger loading, normalization, topic-key extraction, duplicate checks, and ledger append helpers.
- Modify `lines/three-minute-future/select_items.py`: filter candidates through the ledger before scoring, write `filtered-published.json`, and allow opt-out for debugging.
- Create `lines/three-minute-future/mark_published.py`: append an approved issue's selected/final items to the ledger.
- Update `lines/three-minute-future/RUNBOOK.md` and `lines/three-minute-future/TASK_FLOW.md`: document regular and same-day incremental modes.
- Seed `daily/_state/three-minute-future/published-ledger.json` from `daily/2026-05-23/three-minute-future/work/final.json` or `selection.json`.

---

### Task 1: Date Defaults

**Files:**
- Modify: `lines/three-minute-future/run_daily.py`

- [ ] **Step 1: Add date parsing helper**

Add this near the existing date imports:

```python
from datetime import date, datetime, timedelta, timezone
```

Add:

```python
def infer_content_date(publish_date: str, explicit_content_date: str | None) -> str:
    if explicit_content_date:
        return explicit_content_date
    parsed = date.fromisoformat(publish_date)
    return (parsed - timedelta(days=1)).isoformat()
```

- [ ] **Step 2: Use inferred content date in `main`**

After argument parsing:

```python
    content_date = infer_content_date(args.date, args.content_date)
    args.content_date = content_date
```

Expected behavior:

```powershell
python lines\three-minute-future\run_daily.py 2026-05-25 --dry-run
```

prints a fetch command containing:

```text
fetch_candidates.py 2026-05-25 --content-date 2026-05-24
```

- [ ] **Step 3: Record content date in run report**

In `write_run_report`, include:

```python
        "contentDate": args.content_date,
```

- [ ] **Step 4: Verify**

Run:

```powershell
python -m py_compile lines\three-minute-future\run_daily.py
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3 --dry-run
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24 --dry-run
```

Expected:

- first dry run uses `--content-date 2026-05-24`;
- second dry run keeps `--content-date 2026-05-24`.

---

### Task 2: Published Ledger Module

**Files:**
- Create: `lines/three-minute-future/published_ledger.py`

- [ ] **Step 1: Add module**

Create:

```python
from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = PROJECT_ROOT / "daily" / "_state" / LINE_NAME / "published-ledger.json"


TOPIC_PATTERNS = [
    ("robot-phone", ["机器人手机", "Robot Phone"]),
    ("open-harmony-robots", ["鸿蒙", "机器人操作系统", "M-Robots"]),
    ("deepseek-hardware", ["DeepSeek", "硬件"]),
    ("ai-workflow-labor", ["AI选题", "工作流"]),
    ("ai-workplace-product", ["MARVIS", "生产关系"]),
    ("ai-healthcare", ["医疗", "医院", "医助", "患者数据"]),
    ("ai-oscar-media", ["奥斯卡", "短片", "AI"]),
    ("ai-layoffs", ["裁员"]),
    ("ai-cost-labor", ["人工", "成本", "工资"]),
    ("starbucks-ai-inventory", ["星巴克", "库存"]),
]


def normalize_text(value: str) -> str:
    text = value.lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[\\s\\W_]+", "", text, flags=re.UNICODE)
    return text


def normalize_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value or "")
    host = parsed.netloc.lower().replace("www.", "")
    path = parsed.path.rstrip("/")
    return urllib.parse.urlunparse((parsed.scheme.lower(), host, path, "", "", ""))


def topic_key(item: dict[str, Any]) -> str:
    text = " ".join(
        str(item.get(key, ""))
        for key in ("title", "sourceTitle", "displayTitle", "fact", "summary")
    )
    for key, terms in TOPIC_PATTERNS:
        if all(term.lower() in text.lower() for term in terms):
            return key
    normalized = normalize_text(text)
    return hashlib.sha1(normalized[:80].encode("utf-8")).hexdigest()[:12]


def image_key(item: dict[str, Any]) -> str:
    image = item.get("image") or item.get("enrichment", {}).get("image", {})
    value = image.get("sourceUrl") or image.get("url") or image.get("path") or ""
    return normalize_url(value) if value else ""


def load_ledger(path: Path = LEDGER_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"line": LINE_NAME, "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(data: dict[str, Any], path: Path = LEDGER_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fingerprint(item: dict[str, Any]) -> dict[str, str]:
    return {
        "url": normalize_url(item.get("url", "")),
        "title": normalize_text(item.get("title", "")),
        "topicKey": topic_key(item),
        "imageKey": image_key(item),
    }


def duplicate_reason(item: dict[str, Any], ledger: dict[str, Any]) -> str | None:
    current = fingerprint(item)
    for prior in ledger.get("items", []):
        prior_url = normalize_url(prior.get("url", ""))
        prior_title = normalize_text(prior.get("title") or prior.get("sourceTitle", ""))
        if current["url"] and current["url"] == prior_url:
            return "same-url"
        if current["title"] and current["title"] == prior_title:
            return "same-title"
        if current["topicKey"] and current["topicKey"] == prior.get("topicKey"):
            return f"same-topic:{current['topicKey']}"
        if current["imageKey"] and current["imageKey"] == prior.get("imageKey"):
            return "same-image"
    return None
```

- [ ] **Step 2: Verify module imports**

Run:

```powershell
python -m py_compile lines\three-minute-future\published_ledger.py
```

Expected: no output and exit code 0.

---

### Task 3: Selection Filtering

**Files:**
- Modify: `lines/three-minute-future/select_items.py`

- [ ] **Step 1: Add CLI switch**

Add:

```python
    parser.add_argument("--allow-published-duplicates", action="store_true")
```

- [ ] **Step 2: Import ledger helpers**

Add near imports:

```python
from published_ledger import duplicate_reason, load_ledger
```

- [ ] **Step 3: Filter before scoring**

Add:

```python
def filter_published_duplicates(
    date: str,
    items: list[dict[str, Any]],
    allow_duplicates: bool,
) -> list[dict[str, Any]]:
    if allow_duplicates:
        return items
    ledger = load_ledger()
    kept = []
    removed = []
    for item in items:
        reason = duplicate_reason(item, ledger)
        if reason:
            removed.append({"reason": reason, "item": item})
        else:
            kept.append(item)
    out_path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "filtered-published.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"count": len(removed), "items": removed}, ensure_ascii=False, indent=2), encoding="utf-8")
    return kept
```

In `main`, before scoring:

```python
    all_items = filter_published_duplicates(args.date, all_items, args.allow_published_duplicates)
```

- [ ] **Step 4: Verify**

Run:

```powershell
python -m py_compile lines\three-minute-future\select_items.py
python lines\three-minute-future\select_items.py 2026-05-24 --limit 8
```

Expected:

- `daily/2026-05-24/three-minute-future/work/filtered-published.json` is written;
- selection still writes `selection.json`.

---

### Task 4: Mark Published Command

**Files:**
- Create: `lines/three-minute-future/mark_published.py`

- [ ] **Step 1: Add command**

Create a script that reads `work/final.json` if present, otherwise `work/selection.json`, and appends selected items to the ledger.

Use this shape for each appended entry:

```python
{
    "line": LINE_NAME,
    "publishDate": args.date,
    "contentDate": final.get("contentDate") or args.content_date or args.date,
    "vol": args.vol,
    "title": item.get("title") or item.get("displayTitle"),
    "sourceTitle": item.get("sourceTitle") or item.get("title"),
    "url": item.get("url", ""),
    "source": item.get("source", ""),
    "topicKey": topic_key(item),
    "imageKey": image_key(item),
}
```

- [ ] **Step 2: Verify with 2026-05-23**

Run:

```powershell
python lines\three-minute-future\mark_published.py 2026-05-23 --vol 1
```

Expected:

- `daily/_state/three-minute-future/published-ledger.json` exists;
- it contains entries from the first issue.

---

### Task 5: End-To-End Same-Day Incremental Check

**Files:**
- No new files unless bugs are found.

- [ ] **Step 1: Run same-day fetch and selection**

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24 --stop-after select --min-score 2
```

Expected:

- `candidates.json` has `publishDate=2026-05-24` and `contentDate=2026-05-24`;
- `selection.json` excludes topics from 2026-05-23;
- `filtered-published.json` lists removed overlaps.

- [ ] **Step 2: Review selection count**

If there are fewer than 8 strong items, keep the lower count. Do not pad with no-reality-tag filler unless the user asks for filler.

---

### Task 6: Documentation

**Files:**
- Modify: `lines/three-minute-future/RUNBOOK.md`
- Modify: `lines/three-minute-future/TASK_FLOW.md`

- [ ] **Step 1: Add production modes**

Document:

```powershell
# regular: publishDate with contentDate = publishDate - 1 day
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3

# same-day incremental
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24

# mark approved issue as published
python lines\three-minute-future\mark_published.py 2026-05-24 --vol 2
```

- [ ] **Step 2: Verify docs mention both dates**

Run:

```powershell
rg -n "publishDate|contentDate|same-day|增量|mark_published" lines\three-minute-future\RUNBOOK.md lines\three-minute-future\TASK_FLOW.md
```

Expected: both docs explain the difference between publish date and content date.

---

### Task 7: Final Verification

**Files:**
- All modified files.

- [ ] **Step 1: Compile all changed Python**

```powershell
python -m py_compile lines\three-minute-future\run_daily.py lines\three-minute-future\published_ledger.py lines\three-minute-future\select_items.py lines\three-minute-future\mark_published.py
```

- [ ] **Step 2: Run dry runs**

```powershell
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3 --dry-run
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24 --dry-run
```

- [ ] **Step 3: Run real selection checkpoint**

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24 --stop-after select --min-score 2
```

Expected: fresh same-day incremental selection without first-issue repeats.
