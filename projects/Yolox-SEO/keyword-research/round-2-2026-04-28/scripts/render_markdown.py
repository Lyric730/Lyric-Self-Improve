"""
Render Pool C + Pool B as markdown tables grouped by ICP.

Output:
  · 01.5-pool-c-raw.md   — full 903 records (per L1 §4.3, 11 fields)
  · 01.5-pool-b-candidates.md — 208 selected (per L1 §3 12 fields)

Pool A (01-seed-keywords.md) is hand-curated by Claude in a follow-up turn.
"""

import json
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ROUND_DIR = Path(__file__).parent.parent
POOL_C = json.loads((DATA_DIR / "pool_c.json").read_text())
POOL_B = json.loads((DATA_DIR / "pool_b_curated.json").read_text())


def primary_icp(rec):
    icp = rec.get("icp")
    return icp[0] if isinstance(icp, list) else icp


def icp_label(rec):
    icp = rec.get("icp")
    if isinstance(icp, list):
        return "+".join(icp)
    return icp or "?"


def md_escape(s):
    if s is None:
        return "—"
    return str(s).replace("|", "\\|").replace("\n", " ")


def render_pool_c():
    """Pool C raw — per L1 §4.3 fields."""
    out = []
    out.append("# Pool C · Round-2 Day-1 原始候选词池\n")
    out.append("**日期**：2026-04-29\n**讨论方**：小刀老师 + Agent B\n**状态**：草案 v1\n**前置依赖**：L1 Step 4.1 抓取完成 / Layer 1 机械筛通过\n\n---\n")
    out.append(f"## 概览\n")
    out.append(f"- Pool C 总规模：**{len(POOL_C)}** 帖（去重后）")
    out.append(f"- 原始抓取：3702 帖（Reddit 3572 + Quora 80 + IH 50）→ 机械筛通过率 27%")
    out.append(f"- 三层池架构（D6=A 决策）：每帖与 Pool A 同字段精度\n")
    out.append("**字段说明（11 列）**：post_id / 平台 / source（sub or query）/ title / score / num_comments / url / icp / 池标签 / 排除原因（仅 B/C）/ low_confidence\n")
    out.append("---\n")

    # Group by ICP
    groups = defaultdict(list)
    for r in POOL_C:
        groups[primary_icp(r)].append(r)

    for icp in sorted(groups.keys()):
        out.append(f"\n## ICP · {icp} ({len(groups[icp])} 帖)\n")
        out.append("| # | 平台 | source | title | score | comments | url | icp | 池 | low_conf |")
        out.append("|---|---|---|---|---|---|---|---|---|---|")
        # Sort by score desc within group (None last)
        sorted_g = sorted(groups[icp], key=lambda x: (x.get("score") is None, -(x.get("score") or 0)))
        for i, r in enumerate(sorted_g, 1):
            out.append(
                f"| {i} | {md_escape(r['platform'])} | {md_escape(r.get('source','—'))[:30]} | "
                f"{md_escape(r['title'])[:120]} | {md_escape(r.get('score','—'))} | "
                f"{md_escape(r.get('num_comments','—'))} | "
                f"[link]({md_escape(r['url'])}) | {icp_label(r)} | C | "
                f"{'✅' if r.get('low_confidence') else '—'} |"
            )

    return "\n".join(out)


def render_pool_b():
    """Pool B 208 selected — per L1 §3 fields."""
    out = []
    out.append("# Pool B · Round-2 Day-1 高质量候选词池（Layer 2 真筛后）\n")
    out.append("**日期**：2026-04-29 (curated 2026-05-01)\n**讨论方**：小刀老师 + Agent B\n**状态**：草案 v2 · Layer 2 真 4 问筛选完成\n**前置依赖**：Pool C / Layer 2 ICP 平衡 → Claude 4 问语义筛\n\n---\n")
    out.append(f"## 概览\n")
    out.append(f"- Pool B 总规模：**{len(POOL_B)}** 帖（Layer 2 4 问筛选后 · KEEP 率 44%）")
    out.append(f"- 来源：从 ICP 平衡的 208 候选 → Claude 逐帖判 4 问 → 91 keep / 117 cut")
    out.append(f"- 25 ICP 全覆盖（4 个稀疏 ICP=1：ai-builder / artisan-dtc / freelance-designer / mobile-dev → Step 5 重点填）\n")
    out.append("**Layer 2 4 问**（L1 §4.2）：")
    out.append("1. 真实求解 vs 吐槽 / 故事 / 公告？")
    out.append("2. YOLOX agent/skill/team 能解？（默认 yes · 25 ICP 都有 manifest 支持）")
    out.append("3. 标题转得了搜索词？")
    out.append("4. ICP 在 25 清单内？（机械筛已确保）\n")
    out.append("**主要 CUT 类型**：show-off/share post · 个人议题 · sub 跑偏（r/teachers / OF 内容）· 标题太短 · 学术深度文\n")
    out.append("**字段（与 Pool A 同精度）**：关键词候选 / 来源 / Intent / ICP 对接 / 产品对接 / 平台 / URL / 标签 / 4 标准 / 池 / 备注\n")
    out.append("说明：本表的『关键词候选』列是 title 的简化，最终 Pool A 由 Claude 做 4 标准评估 + 二次精炼。\n")
    out.append("---\n")

    groups = defaultdict(list)
    for r in POOL_B:
        groups[primary_icp(r)].append(r)

    for icp in sorted(groups.keys()):
        out.append(f"\n## ICP · {icp} ({len(groups[icp])})\n")
        out.append("| # | 关键词候选 (title 简化) | 来源 | Intent | ICP | 平台 | URL | score/c | 池 | 备注 |")
        out.append("|---|---|---|---|---|---|---|---|---|---|")
        sorted_g = sorted(groups[icp], key=lambda x: (x.get("score") is None, -(x.get("score") or 0)))
        for i, r in enumerate(sorted_g, 1):
            kw = md_escape(r["title"])[:120]
            score_str = f"{r.get('score','—')}/{r.get('num_comments','—')}c"
            out.append(
                f"| {i} | {kw} | ICP | info | {icp_label(r)} | {md_escape(r['platform'])} | "
                f"[link]({md_escape(r['url'])}) | {score_str} | B | — |"
            )

    return "\n".join(out)


def main():
    pool_c_md = render_pool_c()
    pool_b_md = render_pool_b()

    (ROUND_DIR / "01.5-pool-c-raw.md").write_text(pool_c_md)
    (ROUND_DIR / "01.5-pool-b-candidates.md").write_text(pool_b_md)
    print(f"Wrote: 01.5-pool-c-raw.md ({len(POOL_C)} records)")
    print(f"Wrote: 01.5-pool-b-candidates.md ({len(POOL_B)} records)")


if __name__ == "__main__":
    main()
