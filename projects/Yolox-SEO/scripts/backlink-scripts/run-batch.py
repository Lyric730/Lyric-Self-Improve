"""
D1: 从 gefei_226 取 N 条 pending → 输出 JSON prompt 供 Claude Code 自动跑

执行：/usr/bin/python3 scripts/run-batch.py [N]
默认 N=3（DR 16 新站慢喂节奏）

输出：
  1. 控制台打印任务清单 + 复制粘贴用的 prompt
  2. 写入 .claude/queue/next.txt 供 Claude Code 读取

节奏纪律：
- 第 1-2 周：N=0（不走本脚本，手动跑 D2）
- 第 3-4 周：N=3
- 第 5-8 周：N=5-8
- 第 9 周+：评估 GSC 后定
"""
import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB = ROOT / "data" / "backlinks.db"
QUEUE_DIR = ROOT / ".claude" / "queue"
QUEUE_FILE = QUEUE_DIR / "next.txt"

DEFAULT_BATCH = 3
SAFETY_DAILY_MAX = 10  # 不管 argv 传啥，一天最多 10 条


def today_submitted_count(conn: sqlite3.Connection) -> int:
    today = date.today().isoformat()
    cur = conn.cursor()
    return cur.execute(
        "SELECT COUNT(*) FROM submissions WHERE date(submit_time) = ?",
        (today,),
    ).fetchone()[0]


def fetch_pending(conn: sqlite3.Connection, n: int) -> list[dict]:
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT id, type, url, root_domain, link_format
        FROM gefei_226
        WHERE submitted='no'
          AND has_captcha='No'
          AND link_strategy='url_field'
          AND root_domain NOT IN (
              SELECT domain_pattern FROM spam_blacklist
              WHERE domain_pattern NOT LIKE '%*%'
          )
        ORDER BY type, root_domain
        LIMIT ?
        """,
        (n,),
    ).fetchall()
    return [
        {"id": r[0], "type": r[1], "url": r[2], "domain": r[3], "format": r[4]}
        for r in rows
    ]


def build_prompt(tasks: list[dict]) -> str:
    return f"""请使用 Yolox Backlinks Skill 处理以下 {len(tasks)} 条候选：

```json
{json.dumps(tasks, ensure_ascii=False, indent=2)}
```

工作流：
1. 对每条按 type 选 SOP：
   - blog_comment → 跟 `.claude/skills/backlinks/comment.md`
   - profile / directory → 跟 `.claude/skills/backlinks/profile.md`
2. 提交完跑 verify-rel.md，INSERT 进 submissions 表
3. 更新 gefei_226.submitted='yes'（或 'failed' / 'dead'）
4. 单条失败不阻塞下一条
5. 全部完成后报告 markdown 表：
   | id | domain | type | rel_actual | live_url | notes |

数据库：`/外链/data/backlinks.db`
邮箱：
- profile/SaaS/注册 → liuyouxuan570@gmail.com
- WP 评论 / 论坛评论 → suppscanofficial@gmail.com
"""


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BATCH
    if n > SAFETY_DAILY_MAX:
        print(
            f"⚠️  请求 N={n} 超过单日安全上限 {SAFETY_DAILY_MAX}",
            file=sys.stderr,
        )
        return 1

    conn = sqlite3.connect(DB)

    today_count = today_submitted_count(conn)
    remaining = SAFETY_DAILY_MAX - today_count
    if remaining <= 0:
        print(
            f"⚠️  今天已经跑了 {today_count} 条，达到单日上限。明天再来。",
            file=sys.stderr,
        )
        return 1
    if n > remaining:
        print(f"⚠️  今天已跑 {today_count} 条，剩余配额 {remaining}。降到 N={remaining}")
        n = remaining

    tasks = fetch_pending(conn, n)
    if not tasks:
        print("✅ 没有 pending 候选了（或全被 spam_blacklist 过滤）")
        return 0

    prompt = build_prompt(tasks)

    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(prompt, encoding="utf-8")

    print(f"=== 今天已跑 {today_count} 条，本批 {len(tasks)} 条 ===\n")
    for t in tasks:
        print(f"  #{t['id']:<4} {t['type']:<14} {t['domain']:<35} {t['format']}")

    print(f"\n=== Prompt 已写入 {QUEUE_FILE} ===")
    print("把上面这段 prompt 复制到 Claude Code 即可")
    print()
    print(prompt)

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
