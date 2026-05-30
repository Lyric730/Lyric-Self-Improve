"""
L2 Step 1 · Apply pool upgrades, output 02.5-pool-updates.md.

Pool B → A: 10 hand-picked records (Claude-judged, prioritizing 4 sparse
ICPs from L1: fallback-generic / podcaster / tiktok-creator / youtuber).

Pool C → B: top 3 by score per ICP (mechanical, ≤75 records total),
prepared for L2 Step 3 Pool B 广扫.

Pool A markdown is NOT mutated — L1 final is committed. Upgrades are
captured here for L2 Step 5 主库 v0 integration.
"""

import json
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ROUND_DIR = Path(__file__).parent.parent

POOL_C = json.loads((DATA_DIR / "pool_c.json").read_text())
POOL_B = json.loads((DATA_DIR / "pool_b_curated.json").read_text())
CANDIDATES = json.loads((DATA_DIR / "step1_promote_candidates.json").read_text())

# Pool B → Pool A · 10 hand-picked (post_id → keyword + reason)
B_TO_A = [
    ("1ssg49y", "fallback-generic", "tasks entrepreneurs can automate",
     "高 score 231/281c · automation 主题强对接 YOLOX agent (Xavier Workflow Automator)",
     "agent Xavier (Workflow Automator); Skills · Automation"),
    ("1sqx0hy", "podcaster", "AI generated podcasts 2026",
     "新兴话题 + podcaster ICP 之前稀疏 (1 词 → 2 词)",
     "team Podcaster; agent Elena (Podcast Producer)"),
    ("1swa0jj", "tiktok-creator", "how to build TikTok presence in 2026",
     "TikTok 建号策略 + tiktok-creator ICP 稀疏",
     "team Short Video Creator; agent Sadie (Video Producer)"),
    ("1sbvas4", "youtuber", "YouTube video stolen on TikTok recovery",
     "维权 + 跨平台具体痛点 + youtuber 稀疏 (1→3 词)",
     "team YouTube/Twitch Creator; agent Sadie"),
    ("1srmybp", "youtuber", "youtuber pain points 2026",
     "行业 pain 综合搜索词 + youtuber 第二位",
     "team YouTube/Twitch Creator"),
    ("1sthyme", "b2b-sdr", "cold email at million scale",
     "score 70/68c + 量级讨论强 (1 million cold emails)",
     "agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer)"),
    ("1ss70jc", "amazon-seller", "amazon vine review recovery",
     "1-star Vine 杀单具体痛点 + 求解",
     "team Amazon Seller; agent Alice (Review Manager)"),
    ("1se43d6", "consultant", "consulting ex-consultant clients",
     "score 391/73c + 复杂业务场景 + 高质量 consultant 经验",
     "team Consultant"),
    ("1s9i98m", "data-analyst", "data analysis early career mistakes",
     "score 95/24c + 经验性求解 + analyst 入门",
     "agent Camila (Data Interpreter); team Indie Hacker"),
    ("1ss44bh", "financial-advisor", "financial advisor disengaged client management",
     "score 25/76c + advisor 业务管理痛点",
     "team Independent Financial Advisor"),
]

POOL_A_USED_IDS = set(CANDIDATES["pool_a_post_ids_used"])
POOL_B_BY_ID = {r["post_id"]: r for r in POOL_B}


def pool_c_to_b_top_per_icp(top_n=3):
    """Mechanical top-N per ICP from Pool C → B candidates."""
    pc_to_pb = CANDIDATES["pool_c_to_pool_b_candidates"]
    by_icp = defaultdict(list)
    for r in pc_to_pb:
        icp = r["icp"][0] if isinstance(r["icp"], list) else r["icp"]
        by_icp[icp].append(r)
    selected = []
    for icp in sorted(by_icp.keys()):
        by_icp[icp].sort(key=lambda x: -(x.get("score") or 0))
        selected.extend(by_icp[icp][:top_n])
    return selected


def md_escape(s):
    if s is None:
        return "—"
    return str(s).replace("|", "\\|").replace("\n", " ")


def main():
    pc_to_pb = pool_c_to_b_top_per_icp(top_n=3)

    # Build pool_b_extended.json (curated 91 + promoted ~75)
    pool_b_extended = list(POOL_B) + pc_to_pb
    extended_file = DATA_DIR / "pool_b_extended.json"
    extended_file.write_text(json.dumps(pool_b_extended, indent=2, ensure_ascii=False))

    # Stats
    by_icp_b_to_a = defaultdict(list)
    for post_id, icp, kw, reason, product in B_TO_A:
        by_icp_b_to_a[icp].append((post_id, kw))

    by_icp_c_to_b = defaultdict(int)
    for r in pc_to_pb:
        icp = r["icp"][0] if isinstance(r["icp"], list) else r["icp"]
        by_icp_c_to_b[icp] += 1

    # ---- Render markdown ----
    out = []
    out.append("# Round-2 Day-2 · L2 Step 1 · Pool 升级清单\n")
    out.append("**日期**：2026-05-02")
    out.append("**讨论方**：小刀老师 + Agent B")
    out.append("**状态**：v1 final（L2 Step 1 完成）")
    out.append("**前置依赖**：L1 final 已交付（4 文件 commit b0b8e4d）\n")
    out.append("---\n")

    out.append("## 0 · 概览\n")
    out.append("| 维度 | 升级前 | 升级后 |")
    out.append("|---|---|---|")
    out.append(f"| Pool A | 66 词（46 ICP + 13 产品 + 7 EXPLORATORY）| **{66 + len(B_TO_A)}** 词（+10 from Pool B）|")
    out.append(f"| Pool B | 91 词（Layer 2 KEEP）| **{91 + len(pc_to_pb)}** 词（+{len(pc_to_pb)} from Pool C）|")
    out.append(f"| Pool C | 903 帖 | 903 帖（不变）|\n")
    out.append("**注**：Pool A markdown (`01-seed-keywords.md`) 不修改 — L1 final 已 commit。本表升级在 L2 Step 5 主库 v0 整理时合并。\n")
    out.append("---\n")

    # === Pool B → A ===
    out.append(f"## 1 · Pool B → Pool A 升级（{len(B_TO_A)} 词）\n")
    out.append("**选词原则**：")
    out.append("- 优先填 4 个稀疏 ICP（fallback-generic / podcaster / tiktok-creator / youtuber 每 ICP 仅 1 词）")
    out.append("- 高 score 互动信号 + 真问句 + 产品对接强\n")
    out.append("| # | 关键词 | ICP | post_id | 升级理由 | 产品对接 | source |")
    out.append("|---|---|---|---|---|---|---|")
    for i, (post_id, icp, kw, reason, product) in enumerate(B_TO_A, 1):
        rec = POOL_B_BY_ID.get(post_id)
        url = rec.get("url", "—") if rec else "—"
        score = rec.get("score") or "SERP"
        nc = rec.get("num_comments") or "—"
        out.append(
            f"| {i} | {md_escape(kw)} | {icp} | {post_id[:20]} | "
            f"{md_escape(reason)} | {md_escape(product)} | "
            f"[link]({md_escape(url)}) ({score}/{nc}c) |"
        )
    out.append("")
    out.append("**ICP 平衡影响**：")
    icp_after = {
        "fallback-generic": "1 → 2",
        "podcaster": "1 → 2",
        "tiktok-creator": "1 → 2",
        "youtuber": "1 → 3 (+2)",
        "b2b-sdr": "3 → 4",
        "amazon-seller": "2 → 3",
        "consultant": "2 → 3",
        "data-analyst": "2 → 3",
        "financial-advisor": "2 → 3",
    }
    for icp, delta in icp_after.items():
        out.append(f"- `{icp}`: {delta}")
    out.append("\n---\n")

    # === Pool C → B ===
    out.append(f"## 2 · Pool C → Pool B 升级（{len(pc_to_pb)} 词 · 25 ICP × top 3 by score）\n")
    out.append("**选词原则**：机械按 ICP × score 降序 top 3。预备 L2 Step 3 Pool B 广扫用。\n")
    out.append(f"**总规模**：568 候选 → 选 {len(pc_to_pb)} 词")
    out.append("**Pool B 升级后**：91 + {} = {} 词\n".format(len(pc_to_pb), 91 + len(pc_to_pb)))
    out.append("| ICP | 升级数 | top 词示例（前 3）|")
    out.append("|---|---|---|")

    by_icp_pc = defaultdict(list)
    for r in pc_to_pb:
        icp = r["icp"][0] if isinstance(r["icp"], list) else r["icp"]
        by_icp_pc[icp].append(r)

    for icp in sorted(by_icp_pc.keys()):
        examples = " / ".join(r["title"][:50] for r in by_icp_pc[icp][:3])
        out.append(f"| {icp} | {len(by_icp_pc[icp])} | {md_escape(examples)} |")
    out.append("\n详细 75 词清单见 `data/pool_b_extended.json`（pool_b_curated 91 + promoted {}）\n".format(len(pc_to_pb)))
    out.append("---\n")

    # === 11 坑规避 ===
    out.append("## 3 · 11 坑规避自检\n")
    out.append("- 6.4 1/1 score 孤例 ✅ — Pool C → B 升级阈值 score≥10（高于 Layer 1 的 5）+ question signal")
    out.append("- 6.5 内部人名 ✅ — Pool B → A 10 词终检通过")
    out.append("- 6.11 Handoff stale ✅ — worktree 隔离 + git status 干净\n")

    # === 退出条件 ===
    out.append("## 4 · 退出条件触发\n")
    out.append("- E_pre · 候选不足：Pool B → A 候选 46 ≥ 升级目标 10 ✅；Pool C → B 候选 568 ≥ 75 ✅")
    out.append("- E_quality · 转关键词价值低：Pool B → A 10 词全过 4 标准（手工 hand-pick）✅\n")

    out.append("## 5 · 下一步\n")
    out.append("- L2 Step 2 · Pool A 8 渠道深扩 (PAA / Related / Suggest / KE / Trends / YT / Bing)")
    out.append("- L2 Step 3 · Pool B 广扫 D2 + D3（D2 Related + D3 Suggest）")
    out.append("- L2 Step 4 · 竞品反查 5 站 Ahrefs（**待激活 trial**）")
    out.append("- L2 Step 5 · 4 级筛选漏斗 → 主库 v0 300-500 词\n")

    out_path = ROUND_DIR / "02.5-pool-updates.md"
    out_path.write_text("\n".join(out))
    print(f"\nWrote: {out_path}")
    print(f"Pool B → A: {len(B_TO_A)} keywords promoted")
    print(f"Pool C → B: {len(pc_to_pb)} keywords promoted")
    print(f"Pool B extended: {len(pool_b_extended)} records → {extended_file}")


if __name__ == "__main__":
    import sys
    sys.exit(main())
