"""
Build master v0 keyword library · 02-expanded-keywords.md.

Sources:
  · Direct keep (tier-1+2): 76 records (Pool A 76)
  · Haiku keep (4/4 yes from Layer 3): 590 records
  · Haiku keep_weak (3/4 yes): 175 records → Pool B reserve

Total master v0: 666 keywords (direct + haiku keep)
Pool B reserve: 175 keep_weak

Output:
  · 02-expanded-keywords.md (主库 v0 666 词)
  · 02.5-pool-b-reserve.md (175 keep_weak 备用)
"""

import json
import re
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ROUND_DIR = Path(__file__).parent.parent

DIRECT = json.loads((DATA_DIR / "pool_v2_direct_keep.json").read_text())
VERDICTS = json.loads((DATA_DIR / "pool_v2_haiku_verdicts.json").read_text())
HAIKU_VERDICTS = VERDICTS["haiku_verdicts_all"]

# Index direct keep by keyword for meta merge
direct_idx = {}
for r in DIRECT:
    norm = r.get("_norm") or r.get("_kw_canonical", r.get("keyword", "")).lower().strip()
    direct_idx[norm] = r


def normalize(kw):
    s = kw.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def md_escape(s):
    if s is None:
        return "—"
    return str(s).replace("|", "\\|").replace("\n", " ")[:200]


def determine_intent(record):
    """Best guess intent from KWFinder data or default by source."""
    intent = record.get("kwf_intent", "")
    if intent:
        return intent
    src = record.get("source", "")
    if "exploratory" in src or "emerging" in src:
        return "info"
    if "product" in src:
        return "compare"
    return "info"


def determine_tier(record):
    """Tier based on data signals."""
    if record.get("kwf_volume") is not None and (record.get("kwf_volume") or 0) > 0:
        if (record.get("kwf_kd") or 100) < 30:
            return "Tier 1 · 高优先"
        return "Tier 2 · 数据验证"
    if record.get("source", "").startswith("pool-a"):
        return "Tier 2 · Pool A 精选"
    if record.get("yes_count") == 4:
        return "Tier 3 · Haiku 4 yes"
    return "Tier 3 · 其他"


# Build unified master v0 list (direct + haiku keep)
master_v0 = []

# Add direct keep
for r in DIRECT:
    master_v0.append({
        "keyword": r.get("_kw_canonical") or r.get("keyword"),
        "source_layer": "Layer 1+2 direct keep (Pool A)",
        "icp": r.get("icp", "?"),
        "raw_source": r.get("source", "?"),
        "product": r.get("product", "—"),
        "intent": determine_intent(r),
        "tier": determine_tier(r),
        "kwf_volume": r.get("kwf_volume"),
        "kwf_kd": r.get("kwf_kd"),
        "kwf_growth": r.get("kwf_growth_pct"),
        "kwf_serp_features": r.get("kwf_serp_features", ""),
        "yes_count": "(direct)",
        "kw_extracted": r.get("_kw_canonical") or r.get("keyword"),
    })

# Add Haiku keep
for v in HAIKU_VERDICTS:
    if v.get("verdict") != "keep":
        continue
    master_v0.append({
        "keyword": v.get("keyword"),
        "source_layer": "Layer 3 Haiku keep (4/4 yes)",
        "icp": "(via Haiku)",
        "raw_source": "step2/3 sugg",
        "product": "—",
        "intent": "info",
        "tier": "Tier 3 · Haiku 4 yes",
        "kwf_volume": None,
        "kwf_kd": None,
        "kwf_growth": None,
        "kwf_serp_features": "",
        "yes_count": v.get("yes_count", 4),
        "kw_extracted": v.get("kw_extracted") or v.get("keyword"),
    })

# Pool B reserve (Haiku keep_weak 3/4)
pool_b_reserve = []
for v in HAIKU_VERDICTS:
    if v.get("verdict") != "keep_weak":
        continue
    pool_b_reserve.append({
        "keyword": v.get("keyword"),
        "yes_count": v.get("yes_count", 3),
        "kw_extracted": v.get("kw_extracted") or v.get("keyword"),
        "q1": v.get("q1"), "q2": v.get("q2"), "q3": v.get("q3"), "q4": v.get("q4"),
    })

print(f"Master v0: {len(master_v0)} records")
print(f"Pool B reserve: {len(pool_b_reserve)} records")

# Render master v0 markdown
out = []
out.append("# Round-2 Day-2 · L2 主库 v0 · 02-expanded-keywords\n")
out.append("**日期**：2026-05-04")
out.append("**讨论方**：小刀老师 + Agent B")
out.append("**状态**：v0 final（L2 Step 5 4 级筛漏斗完成）")
out.append("**前置依赖**：Pool A 76 + Step 2 1890 + Step 3 27 + KWFinder 30 → 4 级筛 → 主库 v0\n")
out.append("---\n")

out.append("## 0 · 概览\n")
out.append("| 维度 | 数值 |")
out.append("|---|---|")
out.append(f"| **主库 v0 总词数** | **{len(master_v0)}** |")
out.append(f"| Pool A 直接 keep（tier-1+2）| 76 |")
out.append(f"| Haiku Layer 3 keep（4/4 yes）| {len(master_v0) - 76} |")
out.append(f"| Pool B reserve（3/4 yes）| {len(pool_b_reserve)} |")
out.append(f"| 总输入候选 | 1316（去重后）|")
out.append(f"| Layer 3 通过率 | {(len(master_v0)-76)/1240:.0%}（590/1240）|")
out.append(f"| L2 §1 目标 | 300-500 词（实际 {len(master_v0)}，超 33%）|\n")

# Tier distribution
tier_dist = defaultdict(int)
for r in master_v0:
    tier_dist[r["tier"]] += 1
out.append("## 1 · Tier 分布\n")
out.append("| Tier | 数量 |")
out.append("|---|---|")
for tier in sorted(tier_dist.keys()):
    out.append(f"| {tier} | {tier_dist[tier]} |")
out.append("")

# 11 坑规避
out.append("## 2 · 11 坑规避自检\n")
out.append("| 坑 | 状态 |")
out.append("|---|---|")
out.append("| 6.2 Claude 12.5% 命中率 | ✅ Layer 3 用 Haiku 4.5 不是 Opus 凭空扩，符合 spec |")
out.append("| 6.5 内部 Agent 人名 | ✅ Layer 2 黑名单过滤通过 |")
out.append("| 6.11 Handoff stale | ✅ worktree 隔离 + git status 干净 |")
out.append("| 新 · Haiku 误判 | ⚠️ Pool B 175 keep_weak 备用，L4 量化时回查可升级 |\n")

# Master v0 table
out.append(f"## 3 · 主库 v0 完整词表（{len(master_v0)} 词）\n")
out.append("**字段**：# / 关键词 / Tier / 来源 / ICP / Intent / Volume / KD / Growth / SERP Features / 备注\n")
out.append("| # | 关键词 | Tier | 来源 | ICP | Intent | Vol | KD | Growth | SERP | 产品对接 |")
out.append("|---|---|---|---|---|---|---|---|---|---|---|")

# Sort: tier-1 first (KWFinder validated), then Pool A, then Haiku keep
def sort_key(r):
    if "Tier 1" in r["tier"]:
        return (0, -(r.get("kwf_volume") or 0))
    if "Pool A" in r["tier"]:
        return (1, 0)
    return (2, 0)

master_v0_sorted = sorted(master_v0, key=sort_key)
for i, r in enumerate(master_v0_sorted, 1):
    vol = r.get("kwf_volume") if r.get("kwf_volume") is not None else "—"
    kd = r.get("kwf_kd") if r.get("kwf_kd") is not None else "—"
    g = r.get("kwf_growth") if r.get("kwf_growth") is not None else "—"
    g_str = f"{g}%" if g != "—" else "—"
    serp = (r.get("kwf_serp_features", "") or "—")[:25]
    out.append(
        f"| {i} | {md_escape(r['keyword'])} | {r['tier']} | {r['source_layer'][:30]} | "
        f"{r['icp']} | {r['intent']} | {vol} | {kd} | {g_str} | {serp} | {md_escape(r['product'])} |"
    )

out.append("\n---\n")
out.append("## 4 · 下一步（L3+）\n")
out.append("- **L3 主库打分**：6 维度 13 分公式给 666 词打分 + Tier 1/2/3 分档")
out.append("- **L4 量化验证**：剩 ~620 词跑 KWFinder/GAKP（Mangools free 每天 25 词，需 25 天分批 / 或激活付费）")
out.append("- **L5 Pillar/Cluster**：从 Tier 1 选 3 Pillar × 5 Cluster")
out.append("- **L6 博客大纲**：6 篇\n")

out_path = ROUND_DIR / "02-expanded-keywords.md"
out_path.write_text("\n".join(out))
print(f"\nWrote: {out_path} ({len(master_v0)} keywords)")

# Render Pool B reserve
b_out = []
b_out.append("# Round-2 Day-2 · Pool B Reserve · keep_weak 3/4 yes\n")
b_out.append("**日期**：2026-05-04")
b_out.append("**状态**：v0（Haiku Layer 3 keep_weak 备用）\n")
b_out.append(f"## 0 · 概览\n")
b_out.append(f"- 总词数：**{len(pool_b_reserve)}**（Haiku 3/4 yes）")
b_out.append(f"- 升级路径：L4 量化验证后，符合 GAKP Vol > 0 + KD < 30 的可升 Pool A\n")
b_out.append("## 1 · 词表\n")
b_out.append("| # | 关键词 | Q1 | Q2 | Q3 | Q4 | yes | kw_extracted |")
b_out.append("|---|---|---|---|---|---|---|---|")
for i, r in enumerate(pool_b_reserve, 1):
    b_out.append(
        f"| {i} | {md_escape(r['keyword'])} | {r['q1']} | {r['q2']} | {r['q3']} | {r['q4']} | "
        f"{r['yes_count']} | {md_escape(r.get('kw_extracted') or '—')} |"
    )

b_path = ROUND_DIR / "02.5-pool-b-reserve.md"
b_path.write_text("\n".join(b_out))
print(f"Wrote: {b_path} ({len(pool_b_reserve)} keywords)")
