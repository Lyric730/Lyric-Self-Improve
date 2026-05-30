"""
scrape_ahrefs.py — 批量跑 Ahrefs 免费 backlink checker，无需 CapSolver

# 方法
不走方案 §4.8 的"反 API 逆向 + CapSolver"路径，改走更便宜的：
直接用 Playwright 真浏览器访问 https://ahrefs.com/backlink-checker
让 Turnstile 在真浏览器里自动通过，抓 Top 20 backlinks。

D2 实测：v0.dev MCP 浏览器跑成功，20 条入库（GitHub Awesome / ProductHunt / Vercel blog 等高 DR）。

# 输入
21 个 AI 同行（方案 §4.8 固定清单 - 第 1 个 v0.dev 已跑，跑剩 20 个）

# 输出
ahrefs_api_results 表：competitor / backlink_url / title / dr / anchor_text

# 用法
  /usr/bin/python3 scripts/scrape_ahrefs.py             # 跑所有未跑过的同行
  /usr/bin/python3 scripts/scrape_ahrefs.py --only bolt.new  # 只跑 1 个

预计耗时 20 同行 × 25s ≈ 8-10 分钟（其中每个 navigate 5s + Turnstile 7s + extract 1s + 间隔 10s）
"""
import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
DB = ROOT / "data" / "backlinks.db"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)

# 21 个 AI 同行（方案 §4.8 固定）
AI_COMPETITORS = [
    "v0.dev", "bolt.new", "cursor.com", "lovable.dev", "continue.dev",
    "replit.com", "claude.ai", "gemini.google.com", "perplexity.ai", "codeium.com",
    "sourcegraph.com", "tabnine.com", "jetbrains.com", "windsurf.com", "openrouter.ai",
    "anthropic.com", "openai.com", "cohere.com", "mistral.ai", "huggingface.co",
    "crewai.com",
]


def extract_backlinks(page) -> list[dict]:
    return page.evaluate(
        """
        () => {
          const table = document.querySelector('table');
          if (!table) return [];
          const rows = Array.from(table.rows).slice(1, 21);
          return rows.map(row => {
            const cells = row.cells;
            if (cells.length < 3) return null;
            const refLinks = Array.from(cells[1].querySelectorAll('a[href^="http"]')).filter(a => {
              try { return !new URL(a.href).hostname.includes('ahrefs.com'); } catch { return false; }
            });
            return {
              dr: cells[0].textContent.trim(),
              ref_url: refLinks[0]?.href || '',
              ref_title: (cells[1].textContent || '').trim().substring(0, 200),
              anchor: (cells[2].textContent || '').trim().substring(0, 300)
            };
          }).filter(x => x && x.ref_url);
        }
        """
    )


def click_in_page(page, predicate_js: str):
    page.evaluate(
        f"""
        () => {{
          const btn = Array.from(document.querySelectorAll('button')).find(b => {predicate_js});
          if (btn) btn.click();
        }}
        """
    )


def scrape_one(page, competitor: str) -> list[dict]:
    url = f"https://ahrefs.com/backlink-checker/?input={competitor}&mode=subdomains"
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    # accept cookies
    try:
        click_in_page(page, "/accept all/i.test(b.textContent)")
        time.sleep(1.5)
    except Exception:
        pass
    # click Check backlinks
    click_in_page(page, "/check\\\\s*backlinks/i.test(b.textContent)")
    # wait for Turnstile + table render
    time.sleep(8)
    return extract_backlinks(page)


def insert_results(conn, competitor: str, rows: list[dict]) -> int:
    cur = conn.cursor()
    inserted = 0
    for r in rows:
        try:
            cur.execute(
                """INSERT INTO ahrefs_api_results
                   (competitor, backlink_url, title, dr, anchor_text)
                   VALUES (?, ?, ?, ?, ?)""",
                (competitor, r["ref_url"], r["ref_title"], r["dr"], r["anchor"]),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    return inserted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", help="只跑这一个 competitor", default=None)
    parser.add_argument(
        "--headless", action="store_true",
        help="headless 模式（Turnstile 大概率会拦，默认 headed）"
    )
    args = parser.parse_args()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    already_done = set(
        r[0] for r in cur.execute(
            "SELECT DISTINCT competitor FROM ahrefs_api_results"
        )
    )
    print(f"Already in DB: {sorted(already_done)}")

    if args.only:
        todo = [args.only]
    else:
        todo = [c for c in AI_COMPETITORS if c not in already_done]
    print(f"To scrape: {todo}\n")

    if not todo:
        print("Nothing to do.")
        return 0

    with sync_playwright() as p:
        # 关键修复（2026-05-23 D2 校准）：scripted Playwright 默认带
        #   --enable-automation flag，让 navigator.webdriver=true，被
        #   Cloudflare Turnstile 识别为 bot。MCP 浏览器默认禁用此 flag。
        # 修复：launch flag 关闭 automation + init script 改 webdriver=undefined。
        browser = p.chromium.launch(
            headless=args.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = browser.new_context(
            user_agent=UA,
            viewport={"width": 1366, "height": 768},
        )
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )
        page = context.new_page()

        for i, comp in enumerate(todo, 1):
            print(f"[{i:>2}/{len(todo)}] {comp} ...", end=" ", flush=True)
            t0 = time.time()
            try:
                rows = scrape_one(page, comp)
                inserted = insert_results(conn, comp, rows)
                dt = time.time() - t0
                print(f"{dt:.1f}s | extracted={len(rows)} inserted={inserted}")
            except Exception as e:
                print(f"FAILED: {str(e)[:120]}")
            # 间隔避免被限速
            time.sleep(8)
        browser.close()

    # 汇总
    print("\n=== ahrefs_api_results 汇总 ===")
    for r in cur.execute(
        "SELECT competitor, COUNT(*) FROM ahrefs_api_results GROUP BY competitor ORDER BY competitor"
    ):
        print(f"  {r[0]:<20} {r[1]}")
    total = cur.execute("SELECT COUNT(*) FROM ahrefs_api_results").fetchone()[0]
    print(f"\nTotal: {total}")

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
