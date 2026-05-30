"""
audit_profiles_v2.py — 在 v1 has_website_field 基础上深入审计

# 为什么需要 V2
V1 只查"页面是否有 website 字样"。但 D2 实战发现：
- 80% has_website_field 死亡率（5 条跑下来只有 1 个 OK）
- 死因：rel=nofollow / 注册关闭

V2 一次性筛掉：
- 已有用户 Website 链是 rel=nofollow → 站点强制 nofollow → dead
- register 路径返回 "disabled" / "not possible" → dead

只剩 viable 候选才值得真去注册。

# 分类
- viable                 ← 用户 Website rel=dofollow + register 开放 → 起手优先级
- dead_nofollow          ← 强制 nofollow
- dead_register_closed   ← 注册关闭
- maybe_viable           ← rel OK 但 register 路径找不到（论坛非标准）→ 人工确认
- inconclusive           ← 没找到用户 Website 链示例

执行：
  /usr/bin/python3 scripts/audit_profiles_v2.py             # dry-run
  /usr/bin/python3 scripts/audit_profiles_v2.py --commit    # 写 DB

预计 13 条 × 15 秒 ≈ 3-5 分钟（每条要 navigate 2 个页面：profile + register）
"""
import argparse
import sqlite3
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

REGISTER_DISABLED_PATTERNS = [
    "registration is currently not possible",
    "registration is not possible",
    "registration is currently disabled",
    "cannot register at this time",
    "registrations are closed",
    "disabled new account registrations",
    "new registrations are disabled",
    "eine registrierung ist derzeit nicht möglich",
    "registrierungen sind geschlossen",
    "регистрация отключена",
    "регистрация невозможна",
]

REGISTER_OPEN_PATTERNS = [
    "create an account",
    "sign up",
    "register at",
    "create account",
    "join",
    "registrer",
    "регистрация",
]

# 常见 register 路径（按概率排序）
REGISTER_PATHS = [
    "/register.php",
    "/register/",
    "/register",
    "/ucp.php?mode=register",
    "/member.php?action=register",
    "/signup",
    "/signup/",
    "/wp-login.php?action=register",
    "/users/sign_up",
    "/account/create",
]


def check_user_website_rel(page) -> tuple[str, str | None]:
    """启发式：找 user 在 profile 里填的外部 Website 链 + rel."""
    try:
        result = page.evaluate(
            """
            () => {
              const host = location.hostname;
              const links = Array.from(document.querySelectorAll('a[href^="http"]'));
              // 过滤掉常见非用户链接
              const skip_patterns = [
                /twitter\\.com\\//, /facebook\\.com\\//, /instagram\\.com\\//,
                /youtube\\.com\\//, /google\\.com\\//, /github\\.com\\/(?!.+\\?)/,
                /phpbb\\.com/, /informer\\.com/, /mybb\\.com/, /discourse\\.org/,
                /punbb\\.org/, /vbulletin\\.com/, /xenforo\\.com/,
                /linkedin\\.com\\/company/, /apple\\.com/, /microsoft\\.com/,
                /wordpress\\.org/, /jquery\\.com/, /bootstrap/,
                /mozilla\\.org/, /w3\\.org/, /creativecommons\\.org/,
                /github\\.io\\//,
              ];
              const externals = links.filter(a => {
                try {
                  const u = new URL(a.href);
                  if (u.hostname === host) return false;
                  if (u.hostname.endsWith('.' + host)) return false;
                  for (const p of skip_patterns) if (p.test(a.href)) return false;
                  return true;
                } catch { return false; }
              });
              if (externals.length === 0) return null;
              // 取前 3 个作样本
              return externals.slice(0, 3).map(a => ({
                href: a.href,
                rel: (a.getAttribute('rel') || '').toLowerCase().trim()
              }));
            }
            """
        )
    except Exception as e:
        return ("eval_error", str(e)[:80])
    if not result:
        return ("no_user_link", None)
    # 看至少一个用户链的 rel
    for link in result:
        rel = link["rel"]
        if "nofollow" in rel or "sponsored" in rel or "ugc" in rel:
            return ("rel_nofollow", f"rel={rel or '(empty)'} | {link['href'][:60]}")
    # 所有 sample 都 dofollow
    sample = result[0]
    return (
        "rel_dofollow",
        f"rel={sample['rel'] or '(empty)'} | {sample['href'][:60]}",
    )


def check_register_status(page, root_domain: str) -> tuple[str, str | None]:
    base = f"https://{root_domain}"
    last_path_tried = None
    for path in REGISTER_PATHS:
        url = base + path
        last_path_tried = path
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=12000)
            if response is None:
                continue
            if response.status >= 400:
                continue
            time.sleep(0.5)
            body = page.locator("body").inner_text(timeout=4000).lower()
            for p in REGISTER_DISABLED_PATTERNS:
                if p in body:
                    return ("register_closed", f"{path}: {p[:50]}")
            for p in REGISTER_OPEN_PATTERNS:
                if p in body:
                    return ("register_open", path)
        except Exception:
            continue
    return ("register_no_path", f"last tried: {last_path_tried}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    query = """
        SELECT id, url, root_domain FROM gefei_226
        WHERE submitted='no' AND type='profile'
          AND notes LIKE 'audit:has_website_field%'
        ORDER BY id
    """
    if args.limit:
        query += f" LIMIT {args.limit}"
    rows = cur.execute(query).fetchall()
    if not rows:
        print("No pending has_website_field candidates.")
        return 0
    print(f"V2 auditing {len(rows)} candidates (commit={args.commit})")
    print("-" * 80)

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA)
        page = context.new_page()
        for i, (rid, url, root) in enumerate(rows, 1):
            t0 = time.time()
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(1)
                rel_status, rel_marker = check_user_website_rel(page)
            except Exception as e:
                rel_status = "navigation_error"
                rel_marker = str(e)[:80]

            if rel_status == "rel_nofollow":
                final = "dead_nofollow"
                marker = rel_marker
            elif rel_status == "rel_dofollow":
                reg_status, reg_marker = check_register_status(page, root)
                if reg_status == "register_closed":
                    final = "dead_register_closed"
                    marker = reg_marker
                elif reg_status == "register_open":
                    final = "viable"
                    marker = f"{rel_marker} | reg={reg_marker}"
                else:
                    final = "maybe_viable"
                    marker = f"{rel_marker} | reg={reg_status}"
            elif rel_status == "no_user_link":
                final = "inconclusive"
                marker = "no user-filled external links on profile"
            else:
                final = rel_status
                marker = rel_marker
            dt = time.time() - t0
            print(
                f"[{i:>3}/{len(rows)}] #{rid:<4} {root:<28} {dt:>5.1f}s → {final}"
                + (f" | {marker}" if marker else "")
            )
            results.append((rid, final, marker))
            time.sleep(1.5)
        browser.close()

    print("-" * 80)
    print("=== V2 AUDIT 汇总 ===")
    for status, count in Counter(r[1] for r in results).most_common():
        print(f"  {status:<25} {count:>3}")

    if args.commit:
        for rid, final, marker in results:
            new_notes = f"audit_v2:{final}"
            if marker:
                new_notes += f" | {marker[:200]}"
            if final in ("dead_nofollow", "dead_register_closed"):
                cur.execute(
                    "UPDATE gefei_226 SET submitted='dead', notes=? WHERE id=?",
                    (new_notes, rid),
                )
            else:
                cur.execute(
                    "UPDATE gefei_226 SET notes = notes || ' | ' || ? WHERE id=?",
                    (new_notes, rid),
                )
        conn.commit()
        print("\n✓ Committed")
    else:
        print("\n(dry-run — use --commit to write)")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
