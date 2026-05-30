"""
audit_blog_comments.py — 审计 type='blog_comment' 候选

# 为什么需要
profile 阶段实测真 viable 率 ~1.5%。blog_comment 不用注册，但流程也有摩擦：
- 评论被 Akismet 吞（commit 但不显示）
- 评论 form 强制 rel=nofollow
- comments closed（老文章关闭评论）
- login required（必须登录才能评论）
- CleanTalk 等强反垃圾

V3 策略：先 audit 149 条候选，筛出可跑的，再去真提交。

# 检测维度
1. 页面有 comment form 吗？（找 textarea + name/url 字段）
2. 已有评论里的链接 rel？（取一两条样本，看是否被自动 nofollow）
3. 评论 form 是否需要登录？
4. 是否有 disabled / closed 字样？

# 分类
- comment_form_dofollow   ← 已有评论链接是 dofollow → 起手优先级
- comment_form_nofollow   ← 已有评论链接是 nofollow → dead
- comments_closed         ← 评论关闭 → dead
- login_required          ← 必须登录 → dead（这一波不做注册）
- no_comment_form         ← 找不到表单 → dead
- no_existing_comment     ← 有 form 但没已有评论可参考 → maybe_viable

执行：
  /usr/bin/python3 scripts/audit_blog_comments.py --commit
预计 149 × 8 秒 ≈ 20 分钟
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


def audit_comment_page(page) -> tuple[str, str | None]:
    try:
        result = page.evaluate(
            """
            () => {
              const body_text = (document.body.innerText || '').toLowerCase();

              // closed signal
              const closed_patterns = [
                'comments are closed', 'comments closed',
                'commenting is closed', 'comments are off',
                'no longer accepting comments',
                'leaving comments has been disabled',
                'commentaires sont fermés', // FR
                'kommentare sind geschlossen', // DE
              ];
              for (const p of closed_patterns) {
                if (body_text.includes(p)) return {status: 'comments_closed', marker: p};
              }

              // login required signal (textarea 不可见 + 提示登录)
              if (/(?:log\\s?in|sign\\s?in|please log).{0,40}(?:to comment|to post|to reply)/i.test(body_text)) {
                return {status: 'login_required', marker: 'login phrase found'};
              }

              // find comment form
              const forms = Array.from(document.querySelectorAll('form'));
              const commentForm = forms.find(f => {
                const html = (f.outerHTML || '').toLowerCase();
                const action = (f.getAttribute('action') || '').toLowerCase();
                if (action.includes('comment') || action.includes('comments')) return true;
                if (html.includes('comment') && f.querySelector('textarea')) return true;
                return false;
              });
              if (!commentForm) {
                // fallback: any textarea with name/email/url inputs
                const hasTextarea = !!document.querySelector('textarea');
                const hasUrlField = !!document.querySelector('input[name*="url" i], input[name*="website" i], input[name*="homepage" i]');
                if (!hasTextarea || !hasUrlField) {
                  return {status: 'no_comment_form', marker: `textarea=${hasTextarea} url=${hasUrlField}`};
                }
              }

              // check existing comments' link rel
              // 找已有评论容器：常见 class/id 含 comment
              const commentContainers = Array.from(document.querySelectorAll(
                '.comment, .comments li, [id^=comment-], [class^=comment-], [class*=comment_], #comments li, .comment-body, .commentlist li'
              ));
              const sample_links = [];
              for (const c of commentContainers.slice(0, 5)) {
                const links = c.querySelectorAll('a[href^=http]');
                for (const a of links) {
                  try {
                    const u = new URL(a.href);
                    if (u.hostname === location.hostname) continue;
                    if (/twitter|facebook|youtube|instagram|google\\.com|gravatar/.test(u.hostname)) continue;
                    sample_links.push({
                      href: a.href.substring(0, 80),
                      rel: (a.getAttribute('rel') || '').toLowerCase()
                    });
                    if (sample_links.length >= 3) break;
                  } catch {}
                }
                if (sample_links.length >= 3) break;
              }

              if (sample_links.length === 0) {
                return {status: 'no_existing_comment', marker: 'comment form present but no commenter link samples'};
              }

              // 看 sample links 的 rel
              const noFollowCount = sample_links.filter(l => /nofollow|sponsored|ugc/.test(l.rel)).length;
              const dofollowCount = sample_links.length - noFollowCount;
              if (dofollowCount >= 1) {
                const sample = sample_links.find(l => !/nofollow|sponsored|ugc/.test(l.rel));
                return {status: 'comment_form_dofollow', marker: `rel=${sample.rel || '(empty)'} | ${sample.href}`};
              }
              return {status: 'comment_form_nofollow', marker: `${noFollowCount}/${sample_links.length} samples nofollow; e.g. rel=${sample_links[0].rel}`};
            }
            """
        )
        return (result["status"], result.get("marker"))
    except Exception as e:
        return ("eval_error", str(e)[:100])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    query = """
        SELECT id, url, root_domain FROM gefei_226
        WHERE submitted='no' AND type='blog_comment'
        ORDER BY id
    """
    if args.limit:
        query += f" LIMIT {args.limit}"
    rows = cur.execute(query).fetchall()
    if not rows:
        print("No pending blog_comment candidates.")
        return 0
    print(f"Auditing {len(rows)} blog_comment candidates (commit={args.commit})")
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
                status, marker = audit_comment_page(page)
            except Exception as e:
                status = "navigation_error"
                marker = str(e)[:80]
            dt = time.time() - t0
            print(
                f"[{i:>3}/{len(rows)}] #{rid:<4} {root:<28} {dt:>5.1f}s → {status}"
                + (f" | {marker[:80]}" if marker else "")
            )
            results.append((rid, status, marker))
            time.sleep(1.0)
        browser.close()

    print("-" * 80)
    print("=== AUDIT 汇总 ===")
    for status, count in Counter(r[1] for r in results).most_common():
        print(f"  {status:<28} {count:>3}")

    if args.commit:
        for rid, status, marker in results:
            new_notes = f"audit_bc:{status}"
            if marker:
                new_notes += f" | {marker[:180]}"
            if status in (
                "comments_closed",
                "login_required",
                "no_comment_form",
                "comment_form_nofollow",
                "navigation_error",
            ):
                cur.execute(
                    "UPDATE gefei_226 SET submitted='dead', notes=? WHERE id=?",
                    (new_notes, rid),
                )
            else:
                cur.execute(
                    "UPDATE gefei_226 SET notes = COALESCE(notes,'') || ' | ' || ? WHERE id=?",
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
