"""
audit_profiles.py — 批量审计 gefei_226 中 type='profile' 候选的数据质量。

# 为什么需要这个脚本
D2 起手第 1 条（#39 blend4web.com）发现哥飞 226 的 type='profile' 数据有质量问题：
- profile 页没有 Website 字段（公开端显示极简）
- URL 实际是 404 / group / bug detail 页（不是用户 profile）
所以在真正注册之前，先批量探测 67 条 profile 候选的实际页面情况。

# audit 分类
- has_website_field  ← 公开 profile 页有 Website 字样 → 有价值，保留
- no_website_field   ← 页面没找到 → 可能没用，但保留以防多语言漏判
- error_page         ← HTTP 4xx/5xx / 含 404 字样 / 含 inexistant → dead
- non_profile        ← URL 含 show_bug.cgi / /groups/ / /topic/ → dead
- navigation_error   ← 超时 / DNS 失败 → dead

# 使用
  /usr/bin/python3 scripts/audit_profiles.py --dry-run --limit 5   # 测试 5 条不写 DB
  /usr/bin/python3 scripts/audit_profiles.py --commit              # 全量 + 写 DB

预计 67 条耗时 8-15 分钟（headless + 1.5s 间隔）。
"""
import argparse
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
DB = ROOT / "data" / "backlinks.db"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)

WEBSITE_FIELD_PATTERNS = [
    # English
    "website", "web site", "homepage", "home page",
    "personal site", "personal page", "personal url",
    # Russian
    "веб-сайт", "сайт пользователя", "персональный сайт", "домашняя страница",
    # Spanish
    "sitio web", "página web",
    # French
    "site web", "site internet", "page d'accueil",
    # German
    "webseite", "webpräsenz",
    # Italian
    "sito web",
    # Portuguese
    "site da web", "sítio web",
    # Japanese
    "ホームページ", "ウェブサイト",
    # Chinese
    "网站", "主页", "个人主页",
    # Polish
    "strona internetowa", "strona www",
    # Dutch
    "persoonlijke website",
]

ERROR_PATTERNS = [
    "404", "page not found", "not found",
    "inexistant", "inexistent", "inexistente",
    "не существует", "не найдено",
    "doesn't exist", "does not exist",
    "access denied", "forbidden",
]

NON_PROFILE_URL_PATTERNS = [
    "show_bug.cgi",       # bugzilla
    "/groups/",           # group page, not user profile
    "/society-stampers/", # stampstampede group
    "/topic/",            # forum topic
    "/posts/",            # post list, not profile
]


def classify_url(url: str) -> str | None:
    url_lower = url.lower()
    for p in NON_PROFILE_URL_PATTERNS:
        if p in url_lower:
            return p
    return None


def audit_page(page, url: str) -> tuple[str, str | None]:
    pre = classify_url(url)
    if pre:
        return ("non_profile", f"URL pattern: {pre}")
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=20000)
        if response is None:
            return ("navigation_error", "no response")
        if response.status >= 400:
            return ("error_page", f"HTTP {response.status}")
        time.sleep(1)
        title = page.title().lower()
        try:
            body = page.locator("body").inner_text(timeout=5000).lower()
        except Exception:
            body = ""
        text = (title + " " + body)[:8000]
        for p in ERROR_PATTERNS:
            if p in text:
                return ("error_page", f"pattern: {p}")
        for p in WEBSITE_FIELD_PATTERNS:
            if p in text:
                return ("has_website_field", f"pattern: {p}")
        return ("no_website_field", None)
    except Exception as e:
        msg = str(e)[:120].replace("\n", " ")
        return ("navigation_error", msg)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    query = """
        SELECT id, url FROM gefei_226
        WHERE submitted='no' AND type='profile' AND link_strategy='url_field'
        ORDER BY id
    """
    if args.limit:
        query += f" LIMIT {args.limit}"
    rows = cur.execute(query).fetchall()
    if not rows:
        print("No pending profile candidates.")
        return 0

    print(f"Auditing {len(rows)} profile candidates (commit={args.commit})")
    print("-" * 70)

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA)
        page = context.new_page()
        for i, (rid, url) in enumerate(rows, 1):
            t0 = time.time()
            status, marker = audit_page(page, url)
            dt = time.time() - t0
            print(
                f"[{i:>3}/{len(rows)}] #{rid:<4} {dt:>5.1f}s → {status}"
                f"{' | ' + marker if marker else ''}"
            )
            results.append((rid, status, marker, url))
            time.sleep(1.5)
        browser.close()

    print("-" * 70)
    print("=== AUDIT 汇总 ===")
    counts = Counter(r[1] for r in results)
    for status, count in counts.most_common():
        print(f"  {status:<22} {count:>3}")

    if args.commit:
        for rid, status, marker, _url in results:
            notes = f"audit:{status}"
            if marker:
                notes += f" | {marker}"
            if status in ("error_page", "navigation_error", "non_profile"):
                cur.execute(
                    "UPDATE gefei_226 SET submitted='dead', notes=? WHERE id=?",
                    (notes, rid),
                )
            else:
                cur.execute(
                    "UPDATE gefei_226 SET notes=? WHERE id=?", (notes, rid)
                )
        conn.commit()
        print("\n✓ Committed to DB")
    else:
        print("\n(dry-run — not committed. Use --commit to write.)")

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
