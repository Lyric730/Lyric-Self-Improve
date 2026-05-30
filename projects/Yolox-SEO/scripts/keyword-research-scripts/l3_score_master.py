"""
L3 · 主库 6 维度 13 分打分公式 → Tier 1/2/3 分档.

输入:
  · master v0 666 词（已有 76 direct + 590 Haiku keep）
  · KWFinder 5 个 export（旧 2 个 30 词 + 新 3 个 540 词 = 570 词数据）
  · step2_sugg / step3_sugg 用于回溯 Haiku 的 ICP

公式:
  · Volume   0-3   >1000=3 / 100-1000=2 / 10-100=1 / 0或空=0
  · KD       0-3   <20=3 / 20-40=2 / 40-60=1 / >60=0 / 空=0
  · Intent   0-2   commercial|transactional=2 / info=1 / navigational=0
  · Growth   0-2   >50%=2 / 0-50%=1 / <0=0
  · ICP      0-2   direct(pool-a-step4-icp/step1-promoted)=2 /
                   related(step2/step5/step6/step3)=1 / unknown=0
  · 产品对接  0-1   product 字段非空=1 / 否=0
  Total 0-13

Tier:
  · Tier 1: ≥9
  · Tier 2: 6-8
  · Tier 3: <6

输出:
  · 03-master-scored.md
  · master_scored.json
"""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ROUND_DIR = Path(__file__).parent.parent
OPENCLI_RAW = Path.home() / "tools" / "opencli-raw"
GOTTED = DATA_DIR / "Data_Gotted"


def normalize(kw: str) -> str:
    s = kw.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s)


def parse_int(s):
    try:
        if s is None or str(s).strip() == "":
            return None
        return int(float(s))
    except Exception:
        return None


# === 1. Load all KWFinder exports (5 files: 2 old + 3 new) ===
kwf_idx = {}
for f in sorted(GOTTED.glob("kwfinder_import_export*.csv")):
    if "Zone.Identifier" in f.name:
        continue
    with open(f, newline="", encoding="utf-8") as fp:
        for r in csv.DictReader(fp):
            kw = r.get("Keyword", "").strip()
            if not kw:
                continue
            norm = normalize(kw)
            kwf_idx[norm] = {
                "kwf_volume": parse_int(r.get("Avg. Search Volume (Last Known Values)")),
                "kwf_kd": parse_int(r.get("Keyword Difficulty")),
                "kwf_intent": (r.get("Search Intent", "") or "").strip().lower(),
                "kwf_growth": parse_int(r.get("Keyword interest growth (%)")),
                "kwf_serp": (r.get("Serp Features", "") or "").strip(),
                "kwf_cpc": (r.get("CPC/USD", "") or "").strip(),
            }
print(f"KWFinder data loaded: {len(kwf_idx)} unique keywords")


# === 2. Build seed → ICP map from step2/step3 sugg (for Haiku ICP backfill) ===
sugg_icp = {}  # normalized sugg → icp


def add_sugg(sugg, icp, source):
    n = normalize(sugg)
    if n and n not in sugg_icp:
        sugg_icp[n] = (icp, source)


step2_file = OPENCLI_RAW / "round2-step2-suggest-all.json"
if step2_file.exists():
    data = json.loads(step2_file.read_text())
    for seed_kw, payload in data.items():
        meta = payload.get("_meta", {})
        icp = meta.get("icp", "?")
        for ch_name, sugs in payload.get("channels", {}).items():
            for sug in sugs:
                add_sugg(sug, icp, f"step2-{ch_name}")
        # Also map seed itself
        add_sugg(seed_kw, icp, "step2-seed")

step3_file = OPENCLI_RAW / "round2-step3-poolb-suggest.json"
if step3_file.exists():
    data = json.loads(step3_file.read_text())
    for kw, payload in data.items():
        icp = payload.get("icp", "?")
        for sug in payload.get("suggestions", []):
            add_sugg(sug, icp, "step3-pool-b")
        add_sugg(kw, icp, "step3-seed")

print(f"Sugg → ICP map: {len(sugg_icp)} entries")


# === 3. Load master v0 ===
DIRECT = json.loads((DATA_DIR / "pool_v2_direct_keep.json").read_text())
VERDICTS = json.loads((DATA_DIR / "pool_v2_haiku_verdicts.json").read_text())
HAIKU_KEEPS = [v for v in VERDICTS["haiku_verdicts_all"] if v.get("verdict") == "keep"]


def determine_icp_score(record):
    """0-2 分 based on source label."""
    src = record.get("source", "")
    icp = record.get("icp", "")
    origin = record.get("origin", "")
    if "pool-a-step4-icp" in src or "step1-promoted" in src:
        return 2, "direct-icp"
    if "pool-a-step5-product" in src or "pool-a-step6-emerging" in src:
        return 2, "direct-product"
    if any(k in src for k in ["step2-", "step3-"]):
        return 1, "related"
    if icp and icp not in ("?", "(via Haiku)", "(cross-icp)"):
        return 2, "direct-meta"
    # Haiku keep 来自 step2/3 broadcast,即便没回填 sugg_icp,逻辑上是 related
    if origin == "haiku-keep":
        return 1, "haiku-related"
    return 0, "unknown"


def determine_intent_score(intent_str):
    """0-2 分. KWFinder paid 大量空,空默认给 1(info)."""
    if not intent_str:
        return 1  # 空默认 info
    s = intent_str.lower()
    if "commercial" in s or "transactional" in s:
        return 2
    if "info" in s:
        return 1
    return 0


def determine_volume_score(vol):
    if vol is None:
        return 0
    if vol > 1000:
        return 3
    if vol >= 100:
        return 2
    if vol >= 10:
        return 1
    return 0


def determine_kd_score(kd):
    if kd is None:
        return 0
    if kd < 20:
        return 3
    if kd < 40:
        return 2
    if kd < 60:
        return 1
    return 0


def determine_growth_score(g):
    if g is None:
        return 0
    if g > 50:
        return 2
    if g >= 0:
        return 1
    return 0


def determine_product_score(record):
    p = record.get("product", "")
    if p and p not in ("—", "?", ""):
        return 1
    return 0


def score_record(rec):
    norm = normalize(rec.get("keyword", ""))
    kwf = kwf_idx.get(norm, {})
    # Fallback to record's own kwf fields (恢复已跑 30 词 in pool_v2_direct_keep)
    vol = kwf.get("kwf_volume") if kwf.get("kwf_volume") is not None else rec.get("kwf_volume")
    kd = kwf.get("kwf_kd") if kwf.get("kwf_kd") is not None else rec.get("kwf_kd")
    intent = kwf.get("kwf_intent") or rec.get("kwf_intent", "") or ""
    growth = kwf.get("kwf_growth") if kwf.get("kwf_growth") is not None else rec.get("kwf_growth_pct")

    # Backfill ICP for Haiku-only records via sugg map
    if rec.get("source") == "haiku-keep":
        if norm in sugg_icp:
            icp, src = sugg_icp[norm]
            rec["icp"] = icp
            rec["source"] = src

    s_vol = determine_volume_score(vol)
    s_kd = determine_kd_score(kd)
    s_intent = determine_intent_score(intent)
    s_growth = determine_growth_score(growth)
    s_icp, icp_label = determine_icp_score(rec)
    s_product = determine_product_score(rec)
    total = s_vol + s_kd + s_intent + s_growth + s_icp + s_product

    # Tier 1.5: ICP 长尾(Vol+KD 双空但来自 Pool A 直击 + product 对接)
    is_icp_longtail = (
        vol is None and kd is None
        and s_icp == 2  # direct-icp / direct-product / direct-meta
        and s_product == 1
    )
    if total >= 9:
        tier = "Tier 1"
    elif is_icp_longtail:
        tier = "Tier 1.5"  # ICP 长尾候选(KWFinder 不覆盖,但社区真实存在)
    elif total >= 6:
        tier = "Tier 2"
    else:
        tier = "Tier 3"

    return {
        **rec,
        "kwf_volume": vol,
        "kwf_kd": kd,
        "kwf_intent": intent,
        "kwf_growth": growth,
        "kwf_serp": kwf.get("kwf_serp", ""),
        "kwf_cpc": kwf.get("kwf_cpc", ""),
        "score_vol": s_vol,
        "score_kd": s_kd,
        "score_intent": s_intent,
        "score_growth": s_growth,
        "score_icp": s_icp,
        "score_product": s_product,
        "score_total": total,
        "tier": tier,
        "icp_label": icp_label,
        "has_kwf": norm in kwf_idx,
    }


# Build master records
master = []

# Direct keep (76) — spread all fields so kwf_* fallback works
for r in DIRECT:
    kw = r.get("_kw_canonical") or r.get("keyword", "")
    master.append(score_record({
        **r,
        "keyword": kw,
        "origin": "direct-keep",
    }))

# Haiku keep (590)
for v in HAIKU_KEEPS:
    kw = v.get("kw_extracted") or v.get("keyword", "")
    master.append(score_record({
        "keyword": kw,
        "source": "haiku-keep",
        "icp": "(via Haiku)",
        "product": "—",
        "origin": "haiku-keep",
        "yes_count": v.get("yes_count", 4),
    }))

# Dedupe by normalized keyword (keep highest score)
seen = {}
for r in master:
    n = normalize(r["keyword"])
    if not n:
        continue
    if n in seen:
        if r["score_total"] > seen[n]["score_total"]:
            seen[n] = r
    else:
        seen[n] = r

master = list(seen.values())
master.sort(key=lambda r: (-r["score_total"], -(r.get("kwf_volume") or 0)))

# Distribution
tier_dist = Counter(r["tier"] for r in master)
has_kwf = sum(1 for r in master if r["has_kwf"])
print(f"\nMaster scored: {len(master)} records (deduped)")
print(f"  has KWFinder data: {has_kwf}")
print(f"  Tier 1 (≥9): {tier_dist['Tier 1']}")
print(f"  Tier 2 (6-8): {tier_dist['Tier 2']}")
print(f"  Tier 3 (<6): {tier_dist['Tier 3']}")

# Save JSON
out_json = DATA_DIR / "master_scored.json"
out_json.write_text(json.dumps(master, indent=2, ensure_ascii=False))
print(f"\nWrote: {out_json}")


# === 4. Render markdown ===
def md(s):
    if s is None or s == "":
        return "—"
    return str(s).replace("|", "\\|").replace("\n", " ")[:60]


lines = []
lines.append("# Round-2 · L3 主库打分 v1 · 03-master-scored\n")
lines.append("**日期**：2026-05-07")
lines.append("**讨论方**：小刀老师 + Agent B")
lines.append("**状态**：v1 final · 6 维度 13 分公式打分完成")
lines.append("**前置依赖**：master v0 666 + KWFinder 570 词全数据 → L3 打分\n")
lines.append("---\n")

lines.append("## 0 · 概览\n")
lines.append("| 维度 | 数值 |")
lines.append("|---|---|")
lines.append(f"| 主库总词数（去重）| **{len(master)}** |")
lines.append(f"| 有 KWFinder 数据 | {has_kwf} |")
lines.append(f"| **Tier 1（≥9 分）** | **{tier_dist['Tier 1']}** |")
lines.append(f"| **Tier 1.5（ICP 长尾·KWFinder 不覆盖）** | **{tier_dist['Tier 1.5']}** |")
lines.append(f"| Tier 2（6-8 分）| {tier_dist['Tier 2']} |")
lines.append(f"| Tier 3（<6 分）| {tier_dist['Tier 3']} |\n")

lines.append("## 1 · 打分公式\n")
lines.append("| 维度 | 满分 | 规则 |")
lines.append("|---|---|---|")
lines.append("| Volume | 3 | >1000=3 / 100-1000=2 / 10-100=1 / 0或空=0 |")
lines.append("| KD | 3 | <20=3 / 20-40=2 / 40-60=1 / >60=0 / 空=0 |")
lines.append("| Intent | 2 | commercial/transactional=2 / info=1 / navigational=0 |")
lines.append("| Growth | 2 | >50%=2 / 0-50%=1 / <0=0 |")
lines.append("| ICP | 2 | direct(Pool-A meta)=2 / related(step2/3 sugg)=1 / unknown=0 |")
lines.append("| 产品对接 | 1 | product 字段非空=1 / 否=0 |")
lines.append("| **总分** | **13** | Tier 1≥9 / Tier 2: 6-8 / Tier 3: <6 |\n")


def render_table(records, title):
    lines.append(f"## {title}（{len(records)} 词）\n")
    if not records:
        lines.append("（无）\n")
        return
    lines.append("| # | 关键词 | 总分 | Vol | KD | Intent | Growth | ICP | 产品 | SERP |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(records, 1):
        lines.append(
            f"| {i} | {md(r['keyword'])} | "
            f"**{r['score_total']}** | "
            f"{r.get('kwf_volume') if r.get('kwf_volume') is not None else '—'} "
            f"({r['score_vol']}) | "
            f"{r.get('kwf_kd') if r.get('kwf_kd') is not None else '—'} "
            f"({r['score_kd']}) | "
            f"{md(r.get('kwf_intent', ''))[:10]} ({r['score_intent']}) | "
            f"{r.get('kwf_growth') if r.get('kwf_growth') is not None else '—'}% "
            f"({r['score_growth']}) | "
            f"{r['icp_label']} ({r['score_icp']}) | "
            f"{md(r.get('product', ''))} ({r['score_product']}) | "
            f"{md(r.get('kwf_serp', ''))[:25]} |"
        )
    lines.append("")


tier1 = [r for r in master if r["tier"] == "Tier 1"]
tier15 = [r for r in master if r["tier"] == "Tier 1.5"]
tier2 = [r for r in master if r["tier"] == "Tier 2"]
tier3 = [r for r in master if r["tier"] == "Tier 3"]

render_table(tier1, "2 · Tier 1 · 高优先（Pillar/Cluster 候选）")
render_table(tier15, "2.5 · Tier 1.5 · ICP 长尾（KWFinder 不覆盖,博客大纲候选）")
render_table(tier2, "3 · Tier 2 · 数据验证（Cluster 补充）")
# Tier 3 太长了，只显示前 50
render_table(tier3[:50], "4 · Tier 3 · 长尾（前 50 词预览，完整见 JSON）")
lines.append(f"_Tier 3 完整 {len(tier3)} 词见 `data/master_scored.json`_\n")

lines.append("---\n")
lines.append("## 5 · 下一步（L4-L7）\n")
lines.append("- **L4 量化验证**：Tier 1 词全部跑 KWFinder/SERP 二次检（找 SERP 上的真竞品 + AI Overview 占用情况）")
lines.append("- **L5 Pillar/Cluster**：从 Tier 1 选 3 Pillar × 5 Cluster")
lines.append("- **L6 博客大纲**：6 篇")
lines.append("- **L7 精排 + handoff**：final 输出 + 下一轮研究方向\n")

out_md = ROUND_DIR / "_process" / "03-master-scored.md"
out_md.write_text("\n".join(lines))
print(f"Wrote: {out_md}")
