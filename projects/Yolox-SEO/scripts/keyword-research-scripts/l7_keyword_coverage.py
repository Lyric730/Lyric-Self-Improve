"""
L7 · 关键词使用 Coverage 全景分析.

目的:回答小刀老师 5/8 的问题
  · 4 Pillar × 20 Cluster 实际使用多少关键词?(总不会只是 24 个吧)
  · 第一期已使用的词
  · 剩余词分类:有 yolox skill 直接对接 vs 需要新做 skill

逻辑:
  1. 24 主词 = 直接 target
  2. 每篇文章自然 cover ~5-15 个 secondary keyword(从 master 同 Pillar 主题词池里挑)
  3. 剩余词分成:
     · A 类:能挂到现有/规划中的 yolox agent → 后续新 cluster 候选
     · B 类:词主题没对应 yolox agent → 需要做新 skill/agent
     · C 类:Tier 3 弱信号 / 词义偏离 ICP → 跳过

输出:
  · 0-share/keyword-coverage.md
"""

import json
import re
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SHARE_DIR = Path(__file__).parent.parent / "0-share"
MASTER = json.loads((DATA_DIR / "master_scored.json").read_text())


def normalize(kw):
    s = kw.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s)


idx = {normalize(r["keyword"]): r for r in MASTER}

# 24 词主词矩阵(Round-2 本期使用)
PRIMARY_KEYWORDS = [
    # AEO Pillar
    ("AEO", "Pillar 主文", "Answer Engine Optimization"),
    ("AEO", "Cluster", "answer engine optimization services"),
    ("AEO", "Cluster", "Generative Engine Optimization"),
    ("AEO", "Cluster", "aeo vs geo"),
    ("AEO", "Cluster", "answer engine optimization tools"),
    ("AEO", "Cluster", "Google AI Overview optimization"),
    # α Pillar
    ("α", "Pillar 主文", "AI infographic generator"),
    ("α", "Cluster", "AI proposal generator"),
    ("α", "Cluster", "AI ad creative generator"),
    ("α", "Cluster", "story writer AI"),
    ("α", "Cluster", "AI newsletter writer"),
    ("α", "Cluster", "Marketing & Growth AI agents"),
    # β Pillar
    ("β", "Pillar 主文", "ai tools for recruiting"),
    ("β", "Cluster", "cold email deliverability"),
    ("β", "Cluster", "ai agents for project management"),
    ("β", "Cluster", "ai tools for recruiters"),
    ("β", "Cluster", "cold calling AI"),
    ("β", "Cluster", "best CRM for financial advisors"),
    # γ Pillar
    ("γ", "Pillar 主文", "social media management tools"),
    ("γ", "Cluster", "podcast guest release form"),
    ("γ", "Cluster", "podcast name generator"),
    ("γ", "Cluster", "amazon vine reviewer"),
    ("γ", "Cluster", "ecommerce growth strategy"),
    ("γ", "Cluster", "restaurant marketing strategies"),
]

primary_norms = {normalize(kw) for _, _, kw in PRIMARY_KEYWORDS}

# Pillar 主题关键词(用于自动归类剩余词)
PILLAR_THEMES = {
    "AEO": ["aeo", "answer engine", "generative engine", "geo opt", "ai overview", "ai search", "llm seo",
            "llms.txt", "chatgpt cit", "perplexity", "rich snippet", "schema markup"],
    "α": ["ai infographic", "infographic", "ai proposal", "proposal", "ai ad", "ad creative", "ad generator",
          "story writer", "story ai", "newsletter writer", "ai newsletter",
          "marketing ai", "growth ai", "ai design", "ai art", "ai writing", "ai writer", "ai creative",
          "content gen", "ai logo", "logo generator", "podcast cover", "ai poster", "infographic maker",
          "ai presentation"],
    "β": ["ai tools for recruit", "recruiting", "recruiter", "sourcing",
          "cold email", "cold call", "outreach", "deliverability", "spam",
          "ai agent", "project management", "pm ", "scrum",
          "crm", "salesforce", "hubspot", "sales", "sdr",
          "lead gen", "lead generation", "ai sales"],
    "γ": ["social media", "instagram", "tiktok", "facebook", "twitter", "x.com", "youtube",
          "podcast", "amazon", "shopify", "ecommerce", "restaurant",
          "creator", "content creation",
          "vine review", "amazon listing", "etsy", "pinterest"],
}


def classify_pillar(kw):
    """根据 keyword 字面归类到最匹配的 Pillar.返回 (pillar, score)."""
    kw_low = kw.lower()
    scores = {}
    for pillar, themes in PILLAR_THEMES.items():
        score = sum(1 for t in themes if t in kw_low)
        if score > 0:
            scores[pillar] = score
    if not scores:
        return ("UNCLASSIFIED", 0)
    best = max(scores.items(), key=lambda x: x[1])
    return best


# 已使用 vs 未使用
used = []
unused = []
for r in MASTER:
    norm = normalize(r["keyword"])
    if norm in primary_norms:
        used.append(r)
    else:
        unused.append(r)

# 未使用词归类
unused_by_pillar = defaultdict(list)
for r in unused:
    pillar, score = classify_pillar(r["keyword"])
    r["_classified_pillar"] = pillar
    r["_classify_score"] = score
    unused_by_pillar[pillar].append(r)

print(f"=== 总览 ===")
print(f"主库 master: {len(MASTER)}")
print(f"已使用(24 主词):{len(used)}")
print(f"未使用:{len(unused)}")
print()
print(f"未使用按 Pillar 主题归类:")
for pillar, words in sorted(unused_by_pillar.items()):
    print(f"  {pillar}: {len(words)}")


# Estimate "secondary" coverage
# 每篇 Pillar 主文 cover ~15 secondary, 每篇 cluster cover ~7 secondary
# Total secondary covered = 4 × 15 + 20 × 7 = 60 + 140 = 200
# 24 + 200 = 224 直接使用
# 剩 570 - 224 = 346 词需要分类

# Render markdown
lines = []
lines.append("# Round-2 关键词使用 Coverage · 全景梳理\n")
lines.append("**日期**:2026-05-08")
lines.append("**目的**:回答 4 Pillar × 20 Cluster 实际使用多少关键词 / 剩余词怎么分类\n")
lines.append("---\n")

lines.append("## 0 · TL;DR\n")
lines.append(f"主库 **{len(MASTER)} 词**,本期 24 主词只是冰山一角。完整使用估算:\n")
lines.append("| 类别 | 数量 | 说明 |")
lines.append("|---|---|---|")
lines.append(f"| **直接 target**(24 主词)| 24 | 4 Pillar 主文 + 20 cluster 文章主词 |")
lines.append(f"| **Secondary keyword**(每篇文章主动写 5-15 词)| ~200 | 主词 + LSI + synonyms + long-tail variants |")
lines.append(f"| **自然 rank**(文章发布后被动 rank)| ~150-300 | 文章发布后 Search Console 显示的『意外』 |")
lines.append(f"| **本期 cover 总计** | **~370-500** | 24 主词 + secondary + 自然 rank 估算 |")
lines.append(f"| **剩余未 cover** | **~70-200** | Round-3+ 候选 |\n")
lines.append(f"实际『明确目标』的关键词 = **~224 词**(24 + 200 secondary)\n")

# Section 1: 24 词清单
lines.append("## 1 · 第一期已使用 24 主词清单\n")
lines.append("| # | Pillar | 角色 | 关键词 | V | KD | Growth | Tier |")
lines.append("|---|---|---|---|---|---|---|---|")
for i, (pillar, role, kw) in enumerate(PRIMARY_KEYWORDS, 1):
    r = idx.get(normalize(kw))
    if r:
        v = r.get("kwf_volume")
        kd = r.get("kwf_kd")
        g = r.get("kwf_growth")
        lines.append(f"| {i} | {pillar} | {role} | `{kw}` | "
                     f"{v if v is not None else '—'} | "
                     f"{kd if kd is not None else '—'} | "
                     f"{g}% | {r['tier']} |"
                     .replace(f"{g}%", f"{g}%" if g is not None else "—"))
lines.append("")

# Section 2: 未使用词按 Pillar 归类
lines.append("## 2 · 未使用 ~546 词 · 按 Pillar 主题归类\n")
lines.append("| Pillar 归属 | 词数 | 说明 |")
lines.append("|---|---|---|")
total_unused = sum(len(w) for w in unused_by_pillar.values())
for pillar in ["AEO", "α", "β", "γ", "UNCLASSIFIED"]:
    count = len(unused_by_pillar.get(pillar, []))
    pct = count * 100 // total_unused if total_unused else 0
    name = {"AEO": "AEO Pillar 主题", "α": "α(AI 工具)主题", "β": "β(B2B Sales/招聘)主题",
            "γ": "γ(Creator/SMB)主题", "UNCLASSIFIED": "未归类(主题模糊)"}[pillar]
    lines.append(f"| {name} | {count}({pct}%) | — |")
lines.append("")

# Section 3: 每个 Pillar 内未使用词 — 按 Tier + Volume 排序前 30
lines.append("## 3 · 各 Pillar 未使用词 top 候选(待小刀老师标分类)\n")
lines.append("**说明**:每个 Pillar 内,从未使用词中挑 Tier 高 + Volume 大的 top 30 列出。请小刀老师为每个词标:\n")
lines.append("- **🟢 A 类**:有 yolox 已 ship / 即将 ship 的 agent 对接 → 可直接出 cluster 文章")
lines.append("- **🟡 B 类**:词热度好,但 yolox 暂无对应 agent → 需要做新 Skill / Agent")
lines.append("- **⚪ C 类**:跳过(主题偏离 ICP / 词义不合适)\n")

for pillar in ["AEO", "α", "β", "γ"]:
    words = unused_by_pillar.get(pillar, [])
    if not words:
        continue
    # Sort by score_total desc, kwf_volume desc
    words_sorted = sorted(words, key=lambda r: (-r["score_total"], -(r.get("kwf_volume") or 0)))[:30]
    pillar_name = {"AEO": "AEO", "α": "α(AI 工具)", "β": "β(B2B Sales/招聘)",
                   "γ": "γ(Creator/SMB)"}[pillar]
    lines.append(f"### Pillar {pillar_name} · top {len(words_sorted)} 待分类\n")
    lines.append("| # | 关键词 | V | KD | Growth | Tier | 分类 [小刀老师 fill] |")
    lines.append("|---|---|---|---|---|---|---|")
    for i, r in enumerate(words_sorted, 1):
        v = r.get("kwf_volume")
        kd = r.get("kwf_kd")
        g = r.get("kwf_growth")
        lines.append(f"| {i} | `{r['keyword']}` | "
                     f"{v if v is not None else '—'} | "
                     f"{kd if kd is not None else '—'} | "
                     f"{g}% | {r['tier']} | __ |"
                     .replace(f"{g}%", f"{g}%" if g is not None else "—"))
    lines.append("")

# Section 4: UNCLASSIFIED
unc = unused_by_pillar.get("UNCLASSIFIED", [])
if unc:
    lines.append(f"## 4 · 未归类词(主题模糊,需要小刀老师手工 review)· 共 {len(unc)} 词\n")
    unc_sorted = sorted(unc, key=lambda r: (-r["score_total"], -(r.get("kwf_volume") or 0)))[:50]
    lines.append("| # | 关键词 | V | KD | Tier | 备注 |")
    lines.append("|---|---|---|---|---|---|")
    for i, r in enumerate(unc_sorted, 1):
        v = r.get("kwf_volume")
        kd = r.get("kwf_kd")
        lines.append(f"| {i} | `{r['keyword']}` | "
                     f"{v if v is not None else '—'} | "
                     f"{kd if kd is not None else '—'} | "
                     f"{r['tier']} | — |")
    lines.append(f"\n_完整 {len(unc)} 词见 `data/master_scored.json` 中 _classified_pillar=UNCLASSIFIED_\n")

# Section 5: 关键洞察
lines.append("## 5 · 关键洞察 · 给小刀老师的解释\n")
lines.append("### Q1:为什么 24 主词不等于『使用的全部词』?\n")
lines.append("SEO 写作中,一篇 cluster 文章 target **1 个主词**,但文章正文会自然提到 5-15 个相关词(synonyms / variants / LSI),这些都会被 Google 索引并 rank。例子:")
lines.append("- 主词:`AI proposal generator`")
lines.append("- 文章会自然包含:`AI proposal writer`、`automated proposal software`、`AI for sales proposals`、`proposal automation tool` 等 8-15 个 variants")
lines.append("- → 1 篇文章实际『覆盖』 10-15 个搜索意图\n")

lines.append("### Q2:24 主词 + 200 secondary = 224 词,剩 ~346 词怎么处理?\n")
lines.append("3 个去向:")
lines.append("1. **🟢 A 类(有 yolox agent)→ Round-3 直接出 cluster 文章**(无需做新 product)")
lines.append("2. **🟡 B 类(无 agent 但热度好)→ 排期做 Skill/Agent + 配套 cluster**(产品 + 内容协同)")
lines.append("3. **⚪ C 类(跳过)→ 词义偏离 / Tier 3 弱信号 / 不写文章**\n")

lines.append("### Q3:整个矩阵规划完成后,Round-3+ 还需要多少篇 blog?\n")
lines.append("假设 A 类 ~40 词,每篇 cluster cover 1 主词,Round-3 + Round-4 合计可写 ~40 篇 cluster。再加 4 Pillar 主文(本轮已设计)+ 14 cluster(本轮已设计)= **总规划 ~80 篇**。\n")
lines.append("ship 节奏(solo-op 估算):")
lines.append("- Round-2(本期):24 篇大纲 ✅")
lines.append("- Round-3:写 6 篇 markdown(Ben 锁定快赢)+ 设计另 20-30 篇大纲")
lines.append("- Round-4+:全量 ship\n")

lines.append("---\n")
lines.append("## 6 · 待小刀老师 / Ben 标的 4 件事\n")
lines.append("- [ ] 给上面每个 Pillar top 30 词标 🟢 A / 🟡 B / ⚪ C")
lines.append("- [ ] UNCLASSIFIED 50 词中挑出真正有意义的归类")
lines.append("- [ ] 标完成后,A 类词排 Round-3 cluster sequencing")
lines.append("- [ ] B 类词同步给 product 团队(yolox 新 Skill 排期)\n")

# Output
SHARE_DIR.mkdir(exist_ok=True)
out = SHARE_DIR / "keyword-coverage.md"
out.write_text("\n".join(lines))
print(f"\nWrote: {out} ({len(lines)} lines)")
print(f"Used keywords: {len(used)}")
print(f"Unused (by Pillar): {dict((p, len(w)) for p, w in unused_by_pillar.items())}")
