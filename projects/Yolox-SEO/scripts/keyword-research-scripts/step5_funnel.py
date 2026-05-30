"""
L2 Step 5 · 4 级筛选漏斗 · 第 1 + 2 级（机械 + 半自动）.

输入数据源:
  · Pool A 76 词（meta: ICP / 产品对接 / 来源）
  · KWFinder 30 词（Volume / KD / Intent / Growth / SERP Features）
  · Step 2 Safe 4 channels 1890 sugg（meta: ICP / channel）
  · Step 3 Pool B suggest 27 sugg

第 1 级机械去重:
  · lowercase + 去标点 + 去多余空格
  · 长度过滤 3-100 字符
  · 跨来源去重（保留 meta 最丰富的）

第 2 级自动质量信号:
  · 人名黑名单（YOLOX 内部 agent first-name 15 个）→ 砍（坑 6.5）
  · 负向词黑名单（archive/round-1/07-negative-keywords 117 个）→ 砍
  · KWFinder Vol=0 且 KD>30 → 标弱（不进 v0，留 watchlist）
  · 接受 Vol 空（KWFinder 数据库不覆盖长尾）→ 标 long-tail

输出:
  · pool_v1_passed.json — 通过第 1+2 级的候选词（含 meta）
  · pool_v1_rejected.json — 砍的 + 原因
  · 等待 Claude 第 3 级 4 问语义筛
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OPENCLI_RAW = Path.home() / "tools" / "opencli-raw"
SCRIPTS_DIR = Path(__file__).parent

# Internal agent first-names (per L1 §6.5) - block in keyword
HERO_NAMES = {
    "sophie", "elias", "stella", "olivia", "aria", "lucas", "daniel",
    "aurora", "elena", "logan", "elijah", "harper", "theodore",
    "isaiah", "savannah", "addison", "alexander", "wyatt", "audrey",
    "alice", "ava", "leo", "luna", "claire", "scarlett", "grayson",
    "sadie", "oliver", "brooks", "james", "mia", "kai", "finn",
    "ruby", "penelope", "levi", "noah", "ethan", "samuel", "jackson",
    "camila", "evelyn", "hazel", "hannah", "eva", "aaron", "miles",
    "mason", "quinn", "arlo", "madelyn",
}

# Negative keywords from round-1 (high-level patterns)
NEGATIVE_PATTERNS = [
    r"\bporn\b", r"\bnsfw\b", r"\bxxx\b",
    r"\bcrypto\b", r"\bnft\b", r"\bbitcoin\b",
    r"\bdating\b", r"\bromance\b",
    r"\bgambling\b", r"\bcasino\b",
    r"\bweed\b", r"\bcannabis\b", r"\bmarijuana\b",
    r"\bdiet pill\b", r"\bweight loss\b",
    r"\bget rich\b", r"\bpyramid\b",
]
NEG_RE = [re.compile(p, re.IGNORECASE) for p in NEGATIVE_PATTERNS]


def normalize_kw(kw: str) -> str:
    """lowercase + remove punct except space + collapse whitespace."""
    s = kw.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_pool_a():
    """Pool A 76 keywords from build_pool_a + step1_promote_apply."""
    import sys
    sys.path.insert(0, str(SCRIPTS_DIR))
    from build_pool_a import SELECTIONS, SELECTIONS_STEP5, SELECTIONS_STEP6
    from step1_promote_apply import B_TO_A

    rows = []
    for icp, kw, _tm, product in SELECTIONS:
        rows.append({"keyword": kw, "icp": icp, "source": "pool-a-step4-icp", "product": product})
    for icp, kw, hits, product in SELECTIONS_STEP5:
        rows.append({"keyword": kw, "icp": icp, "source": "pool-a-step5-product", "product": product, "suggest_hits": hits})
    for canonical, kw, sources, count, note in SELECTIONS_STEP6:
        rows.append({"keyword": kw, "icp": "(cross-icp)", "source": "pool-a-step6-emerging",
                     "product": "L4 验证", "exploratory_sources": count, "note": note})
    for post_id, icp, kw, reason, product in B_TO_A:
        rows.append({"keyword": kw, "icp": icp, "source": "pool-a-step1-promoted", "product": product, "reason": reason})
    return rows


def load_step2_sugg():
    """Step 2 Safe 4 channels (Google/YouTube/Bing/DDG suggest)."""
    f = OPENCLI_RAW / "round2-step2-suggest-all.json"
    if not f.exists():
        return []
    data = json.loads(f.read_text())
    rows = []
    for seed_kw, payload in data.items():
        meta = payload.get("_meta", {})
        for ch_name, sugs in payload.get("channels", {}).items():
            for sug in sugs:
                rows.append({
                    "keyword": sug,
                    "icp": meta.get("icp", "?"),
                    "source": f"step2-{ch_name}",
                    "seed": seed_kw,
                })
    return rows


def load_step3_sugg():
    """Step 3 Pool B Suggest."""
    f = OPENCLI_RAW / "round2-step3-poolb-suggest.json"
    if not f.exists():
        return []
    data = json.loads(f.read_text())
    rows = []
    for kw, payload in data.items():
        for sug in payload.get("suggestions", []):
            rows.append({
                "keyword": sug,
                "icp": payload.get("icp", "?"),
                "source": "step3-pool-b-google-suggest",
                "seed": kw,
            })
    return rows


def load_kwfinder():
    """KWFinder 30 keywords with Volume / KD / Intent / Growth."""
    folder = DATA_DIR / "Data_Gotted"
    rows = []
    for f in sorted(folder.glob("*.csv")):
        if "Zone.Identifier" in f.name:
            continue
        with open(f, newline="", encoding="utf-8") as fp:
            for r in csv.DictReader(fp):
                rows.append({
                    "keyword": r["Keyword"],
                    "kwf_volume": parse_int(r.get("Avg. Search Volume (Last Known Values)")),
                    "kwf_kd": parse_int(r.get("Keyword Difficulty")),
                    "kwf_intent": r.get("Search Intent", "").strip(),
                    "kwf_growth_pct": parse_int(r.get("Keyword interest growth (%)")),
                    "kwf_serp_features": r.get("Serp Features", "").strip(),
                    "kwf_cpc": r.get("CPC/USD", "").strip(),
                    "kwf_content_type": r.get("Content Type", "").strip(),
                })
    return rows


def parse_int(s):
    try:
        return int(s) if s else None
    except:
        return None


def has_hero_name(kw_norm):
    """Check if normalized keyword contains an internal agent first-name."""
    tokens = set(kw_norm.split())
    return tokens & HERO_NAMES


def has_negative(kw):
    """Check negative keyword patterns."""
    for r in NEG_RE:
        if r.search(kw):
            return True
    return False


def main():
    pool_a = load_pool_a()
    step2 = load_step2_sugg()
    step3 = load_step3_sugg()
    kwf = load_kwfinder()

    print(f"=== Inputs ===")
    print(f"Pool A: {len(pool_a)}")
    print(f"Step 2 sugg: {len(step2)}")
    print(f"Step 3 sugg: {len(step3)}")
    print(f"KWFinder: {len(kwf)}")
    total_input = len(pool_a) + len(step2) + len(step3)
    print(f"Total candidates (before merge): {total_input}")

    # Index KWFinder by normalized keyword
    kwf_idx = {}
    for r in kwf:
        norm = normalize_kw(r["keyword"])
        kwf_idx[norm] = r

    # Merge all candidates by normalized keyword (Pool A wins meta, then step2/3)
    merged = {}
    for batch_name, rows in [("pool-a", pool_a), ("step2", step2), ("step3", step3)]:
        for r in rows:
            kw = r["keyword"].strip()
            norm = normalize_kw(kw)
            if not norm or len(norm) < 3 or len(norm) > 100:
                continue
            if norm in merged:
                # If existing record has weaker source, upgrade
                existing = merged[norm]
                if "pool-a" in r["source"] and "pool-a" not in existing["source"]:
                    merged[norm] = r
                    merged[norm]["_norm"] = norm
                else:
                    # Append source as overlap signal
                    existing.setdefault("_overlap_sources", []).append(r["source"])
            else:
                merged[norm] = dict(r)
                merged[norm]["_norm"] = norm
                merged[norm]["_kw_canonical"] = kw

    # Attach KWFinder data where exists
    for norm, rec in merged.items():
        kwf_rec = kwf_idx.get(norm)
        if kwf_rec:
            for k, v in kwf_rec.items():
                if k.startswith("kwf_"):
                    rec[k] = v

    print(f"\n=== Layer 1: Mechanical Dedup ===")
    print(f"Unique normalized keywords: {len(merged)}")

    # Layer 2: filter
    passed = {}
    rejected = []
    for norm, rec in merged.items():
        kw = rec.get("_kw_canonical", norm)
        # Hero name check
        hero = has_hero_name(norm)
        if hero:
            rejected.append({**rec, "_reject_reason": f"hero-name:{','.join(hero)}"})
            continue
        # Negative pattern check
        if has_negative(kw):
            rejected.append({**rec, "_reject_reason": "negative-pattern"})
            continue
        # KWFinder data: Vol=0 & KD>30 → 砍
        vol = rec.get("kwf_volume")
        kd = rec.get("kwf_kd")
        if vol is not None and vol == 0 and kd is not None and kd > 30:
            rejected.append({**rec, "_reject_reason": f"vol=0+kd={kd}>30"})
            continue
        passed[norm] = rec

    print(f"\n=== Layer 2: Quality Filter ===")
    print(f"Passed: {len(passed)}")
    print(f"Rejected: {len(rejected)}")

    # Reject reason distribution
    from collections import Counter
    reasons = Counter(r["_reject_reason"].split(":")[0] for r in rejected)
    print(f"Reject reason distribution:")
    for reason, c in reasons.most_common():
        print(f"  {reason}: {c}")

    # Tag for Layer 3 priority
    for rec in passed.values():
        # Priority tier based on data signals
        if rec.get("kwf_volume") is not None and rec["kwf_volume"] > 0:
            rec["_priority"] = "tier-1-validated"
        elif rec.get("kwf_kd") is not None:
            rec["_priority"] = "tier-2-kd-only"
        elif "pool-a" in rec.get("source", ""):
            rec["_priority"] = "tier-2-pool-a"
        elif len(rec.get("_overlap_sources", [])) >= 2:
            rec["_priority"] = "tier-3-multi-source"
        else:
            rec["_priority"] = "tier-4-single-source"

    # Distribution
    tier_counts = Counter(r["_priority"] for r in passed.values())
    print(f"\n=== Priority Distribution ===")
    for tier, c in sorted(tier_counts.items()):
        print(f"  {tier}: {c}")

    # Source distribution
    source_counts = Counter(r["source"] for r in passed.values())
    print(f"\n=== Source Distribution ===")
    for src, c in sorted(source_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {src}: {c}")

    # Output
    out_passed = DATA_DIR / "pool_v1_passed.json"
    out_rejected = DATA_DIR / "pool_v1_rejected.json"
    out_passed.write_text(json.dumps(list(passed.values()), indent=2, ensure_ascii=False))
    out_rejected.write_text(json.dumps(rejected, indent=2, ensure_ascii=False))
    print(f"\nWrote: {out_passed}")
    print(f"Wrote: {out_rejected}")
    print(f"\n=== Next ===")
    print(f"Layer 3 · 4 问语义筛 (Claude · 处理 {len(passed)} 词)")
    print(f"Layer 4 · 4 标准 (Claude · 处理 ~Layer 3 通过的)")


if __name__ == "__main__":
    import sys
    sys.exit(main())
