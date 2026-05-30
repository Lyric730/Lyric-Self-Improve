"""
Step 1: 从 aihot.virxact.com 抓取昨日 AI 圈热点 → raw.json

API:  https://aihot.virxact.com/api/public/items?mode=all&since=<ISO>&take=<N>

Output schema (per item):
  - id, title, title_en, url, source, publishedAt, summary, category

Usage:
    python lines/digest/fetch_aihot.py <PUBLISH_DATE> [--content-date YYYY-MM-DD] [--take 50]

参数:
    PUBLISH_DATE      产物目录日期（daily/<date>/digest/work/raw.json 中 <date>）
    --content-date    实际过滤事件的日期（fetch 哪天的内容）；不传默认 = PUBLISH_DATE

设计原则（5/22 后定）:「<触发日> 跑 <触发日-1> 的事件」
  scheduled_daily.sh 5/22 7:30 跑：
    --content-date 2026-05-21  → 拿 5/21 整天发布的事件（数据完整）
    PUBLISH_DATE   2026-05-22  → 产物落 daily/2026-05-22/digest/

Example:
    python lines/digest/fetch_aihot.py 2026-05-22 --content-date 2026-05-21
    → daily/2026-05-22/digest/work/raw.json  (内容是 5/21 的事件)
"""
import argparse
import json
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

import requests

API_BASE = "https://aihot.virxact.com/api/public/items"


def fetch_for_date(target_date: date, take: int = 100) -> dict:
    """
    API 经实测忽略 since/until — 总是返回最新 take 条 desc by publishedAt。
    所以策略：take 取大（默认 100，够覆盖 1-2 天），client-side 过滤到 target_date。
    """
    params = {"mode": "all", "take": take}
    resp = requests.get(
        API_BASE,
        params=params,
        headers={"User-Agent": "self-media-daily/1.0"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="发布日期 YYYY-MM-DD（产物目录名）")
    parser.add_argument("--content-date", default=None, help="内容日期（fetch 哪天的事件）；不传默认 = date")
    parser.add_argument("--take", type=int, default=100, help="API 抓取候选数（client filter 前）")
    parser.add_argument("--root", default=".", help="项目根目录")
    args = parser.parse_args()

    content_date_str = args.content_date or args.date
    target = date.fromisoformat(content_date_str)  # 实际过滤事件用的日期
    out_dir = Path(args.root) / "daily" / args.date / "digest" / "work"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "raw.json"

    print(f"→ fetch_aihot publish={args.date} content={target.isoformat()} (take={args.take})")
    data = fetch_for_date(target, take=args.take)
    raw_items = data.get("items", [])

    # Client-side strict filter: only items whose publishedAt date matches target (content date).
    # API since/until is best-effort; some items leak across UTC boundaries.
    target_prefix = target.isoformat()
    items = [i for i in raw_items if i.get("publishedAt", "").startswith(target_prefix)]
    dropped = len(raw_items) - len(items)
    data["items"] = items
    data["count"] = len(items)

    out_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"✓ {len(items)} items → {out_path}" + (f" ({dropped} cross-day dropped)" if dropped else ""))
    if items:
        print(f"  first: {items[0].get('title', '')[:60]}")
        print(f"  last:  {items[-1].get('title', '')[:60]}")


if __name__ == "__main__":
    main()
