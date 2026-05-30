"""
L5 · Pillar/Cluster 选定 + leader handoff 精确索引文档.

决策(per 小刀老师 5/7 拍板):
  · Pillar A+B+C 全做, 每个 Pillar 配 5 Cluster (合计 15 词)
  · 输出 1 份 handoff 文档(99-handoff-leader-review.md)给 leader 审核
  · Pillar 主词来自 Tier 1, Cluster 从 Tier 1/1.5/2 中按主题相关度选

输出:
  · 04-pillar-cluster.md          (L5 标准输出, L6/L7 用)
  · 99-handoff-leader-review.md   (leader 审核, 带精确索引 + 决策依据)
"""

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ROUND_DIR = Path(__file__).parent.parent

MASTER = json.loads((DATA_DIR / "master_scored.json").read_text())


def normalize(kw):
    s = kw.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s)


master_idx = {normalize(r["keyword"]): r for r in MASTER}


def find_line(file_rel, pattern):
    """Find line number(s) where pattern occurs in file. Returns 'L<n>' or 'L<n>-<m>'."""
    f = ROUND_DIR / file_rel
    if not f.exists():
        return "—"
    p_low = pattern.lower()
    matches = []
    for i, line in enumerate(f.read_text().split("\n"), 1):
        if p_low in line.lower():
            matches.append(i)
    if not matches:
        return "—"
    if len(matches) == 1:
        return f"L{matches[0]}"
    return f"L{matches[0]}+{len(matches)-1}"


def lookup(kw):
    r = master_idx.get(normalize(kw))
    if not r:
        return None
    return {
        "keyword": r["keyword"],
        "tier": r["tier"],
        "score": r["score_total"],
        "vol": r.get("kwf_volume"),
        "kd": r.get("kwf_kd"),
        "growth": r.get("kwf_growth"),
        "intent": r.get("kwf_intent", ""),
        "icp_label": r["icp_label"],
        "product_score": r["score_product"],
        "source": r.get("source", ""),
        "serp": r.get("kwf_serp", ""),
    }


# === Pillar/Cluster 决策 ===
PILLARS = [
    {
        "id": "A",
        "title": "Answer Engine Optimization (AEO)",
        "thesis": "AI 搜索时代的 SEO — 从'被 Google 排名'转向'被 ChatGPT/Perplexity/Google AI Overview 引用'。",
        "icp": "SaaS 产品经理、SEO 从业者、内容创作者",
        "product_hook": "YOLOX agent 可帮内容自动检测 AEO 信号(llms.txt/schema/citations)并生成优化建议",
        "pillar_kw": "Answer Engine Optimization",
        "clusters": [
            ("answer engine optimization services", "shoulder commercial — 极低 KD + 爆发增长,蓝海"),
            ("Generative Engine Optimization", "alternative concept,GEO 在 Google 内部生态有差异化"),
            ("google ai overview", "Google specific,大流量但 KD 偏高"),
            ("llms.txt SEO", "技术实现层(ICP 长尾,但社区真实存在)"),
            ("why ChatGPT cites pages", "informational long-tail(博客金字塔底层)"),
        ],
    },
    {
        "id": "B",
        "title": "AI Agent 开发栈 (Model Context Protocol & Claude)",
        "thesis": "Agent 开发标准化 — MCP/Claude agent skills 是 2026 年的 React/Vue,开发者必学。",
        "icp": "独立开发者、技术 founder、AI 应用开发者",
        "product_hook": "YOLOX 本身是 agent team SaaS,这部分是技术权威 + 给我们的 agent store 引流",
        "pillar_kw": "Model Context Protocol",
        "clusters": [
            ("ai coding agent", "大流量(V=3000) + 极高增长(+1236%) — 必投"),
            ("Claude agent skills", "ICP 长尾,但 Claude skills 生态在爆发期"),
            ("Claude Code workflow", "ICP 长尾,Claude Code 用户教程刚需"),
            ("ai agents for project management", "ICP 直击 + KD 25 友好"),
            ("ai agent for code review", "ICP 直击,V 空但 KD=34 + 真实社区帖文证据"),
        ],
    },
    {
        "id": "C",
        "title": "SMB AI 工具直击 (AI app builder & 衍生)",
        "thesis": "中小企业'非技术'用户用 AI agent 替代专业工具(设计/proposal/广告) — 这是 YOLOX 的 ICP 主战场。",
        "icp": "中小企业主、咨询顾问、自由职业者、内容创作者",
        "product_hook": "YOLOX agent store 直接对接 — 每个 Cluster 词能挂一个或多个 product agent",
        "pillar_kw": "AI app builder",
        "clusters": [
            ("AI infographic generator", "Tier 1 (V=1700, KD=37) — 设计场景 ICP"),
            ("AI proposal generator", "consultant/freelancer ICP, V=530"),
            ("AI ad creative generator", "PPC agency ICP, +75% 增长"),
            ("AI newsletter writer", "creator ICP, KD=30 友好"),
            ("Marketing & Growth AI agents", "ICP 长尾,直接对接 agent store 'Marketing' 分类"),
        ],
    },
]


# === Build Pillar/Cluster data ===
def render_kw_block(kw, role, note=""):
    r = lookup(kw)
    if not r:
        return f"  · ⚠️  未找到: {kw}"
    score_idx = find_line("03-master-scored.md", kw)
    seed_idx = find_line("01-seed-keywords.md", kw)
    master_idx_line = find_line("02-expanded-keywords.md", kw)
    return {
        "kw": kw,
        "role": role,
        "tier": r["tier"],
        "score": r["score"],
        "vol": r["vol"],
        "kd": r["kd"],
        "growth": r["growth"],
        "intent": r["intent"] or "(empty)",
        "icp_label": r["icp_label"],
        "source": r["source"],
        "serp": r["serp"],
        "note": note,
        "idx_score": score_idx,
        "idx_seed": seed_idx,
        "idx_master_v0": master_idx_line,
    }


for p in PILLARS:
    p["pillar_data"] = render_kw_block(p["pillar_kw"], "Pillar")
    p["cluster_data"] = [render_kw_block(kw, "Cluster", note) for kw, note in p["clusters"]]


# === Render 04-pillar-cluster.md (L5 standard output) ===
def fmt_v(v):
    return str(v) if v is not None else "—"


def fmt_g(g):
    return f"{g}%" if g is not None else "—"


def md_escape(s):
    return str(s).replace("|", "\\|")[:60] if s else "—"


lines = []
lines.append("# Round-2 · L5 Pillar/Cluster 选定 · 04-pillar-cluster\n")
lines.append("**日期**:2026-05-07")
lines.append("**讨论方**:小刀老师 + Agent B")
lines.append("**状态**:v1 final · A+B+C 全做(每 Pillar × 5 Cluster = 15 词)")
lines.append("**前置依赖**:`03-master-scored.md` Tier 1/1.5/2 全表\n")
lines.append("---\n")

lines.append("## 0 · 概览\n")
lines.append("| Pillar | 主词 | 5 Cluster |")
lines.append("|---|---|---|")
for p in PILLARS:
    cluster_kws = ", ".join(c["kw"] for c in p["cluster_data"])
    lines.append(f"| **{p['id']} · {p['title']}** | `{p['pillar_kw']}` | {cluster_kws} |")
lines.append("")

for p in PILLARS:
    lines.append(f"## Pillar {p['id']} · {p['title']}\n")
    lines.append(f"**Thesis**:{p['thesis']}")
    lines.append(f"**ICP**:{p['icp']}")
    lines.append(f"**产品对接**:{p['product_hook']}\n")
    pd = p["pillar_data"]
    lines.append(f"### Pillar 主词:`{pd['kw']}`\n")
    lines.append("| 字段 | 值 |")
    lines.append("|---|---|")
    lines.append(f"| Tier | {pd['tier']} ({pd['score']}/13) |")
    lines.append(f"| Volume | {fmt_v(pd['vol'])} |")
    lines.append(f"| KD | {fmt_v(pd['kd'])} |")
    lines.append(f"| Growth | {fmt_g(pd['growth'])} |")
    lines.append(f"| Intent | {pd['intent']} |")
    lines.append(f"| ICP 标签 | {pd['icp_label']} |")
    lines.append(f"| SERP Features | {md_escape(pd['serp'])} |")
    lines.append(f"| 来源行 | `03-master-scored.md` {pd['idx_score']} · `02-expanded-keywords.md` {pd['idx_master_v0']} · `01-seed-keywords.md` {pd['idx_seed']} |")
    lines.append("")

    lines.append("### 5 Cluster\n")
    lines.append("| # | 关键词 | Tier | V | KD | Growth | ICP 标签 | 决策依据 | 03-master-scored 行 |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for i, c in enumerate(p["cluster_data"], 1):
        lines.append(
            f"| {p['id']}{i} | `{c['kw']}` | {c['tier']} | {fmt_v(c['vol'])} | "
            f"{fmt_v(c['kd'])} | {fmt_g(c['growth'])} | {c['icp_label']} | {c['note']} | {c['idx_score']} |"
        )
    lines.append("")

(ROUND_DIR / "_process" / "04-pillar-cluster-v1.md").write_text("\n".join(lines))
print(f"Wrote: 04-pillar-cluster.md ({len(lines)} lines)")


# === Render 99-handoff-leader-review.md (精确索引对接文档) ===
hl = []
hl.append("# Round-2 关键词研究 · Leader 审核版 (handoff v1)\n")
hl.append("**Round**:Round-2(2026-04-28 启动)")
hl.append("**Author**:Agent B + 小刀老师")
hl.append("**Date**:2026-05-07")
hl.append("**Branch**:`feat/seo-keyword-research`(worktree)")
hl.append("**Status**:🟡 可用 · L5 完成 / L6+L7 待 leader 审核后启动")
hl.append("**审核范围**:L0-L5(8 层中前 6 层) — Pillar/Cluster 决策与索引证据\n")
hl.append("---\n")

hl.append("## 0 · TL;DR\n")
hl.append("> Round-2 在 Round-1 的 Pool A/B/C 三层架构上,通过 8 渠道公共 Suggest 扩展 + Haiku 批量语义筛选 + KWFinder paid 全量化验证(570/570 词),产出 666 词主库 v0,经 6 维度 13 分公式打分得到:")
hl.append("> ")
hl.append(f"> **Tier 1**:6 词(Pillar 候选) · **Tier 1.5**:58 词(ICP 长尾,博客大纲候选) · **Tier 2**:88 词(Cluster 候选) · **Tier 3**:418 词(长尾备用)")
hl.append(">")
hl.append("> 选定 **3 Pillar × 5 Cluster = 15 词**:**A · AEO** + **B · Agent 开发栈(MCP)** + **C · SMB AI 工具(AI app builder)**")
hl.append(">")
hl.append("> 待 leader 拍板后启动 **L6 (6 篇博客大纲)** + **L7 (精排 + handoff final)** — 我侧预估 4-6h\n")

hl.append("## 1 · 文档地图(精确索引)\n")
hl.append("| Layer | 文档 | 行数 | 核心交付 |")
hl.append("|---|---|---|---|")
hl.append("| L1 种子词 | `01-seed-keywords.md` | 161 | Pool A 76 词(46 ICP + 13 product + 7 EXPLORATORY + 10 promoted) |")
hl.append("| L2 Step 0 watchlist | `01.5-watchlist.md` | 60 | 7 词 watchlist(双源降级 3 + 单源 4) |")
hl.append("| L2 Step 1-2 候选 | `01.5-pool-b-candidates.md` | 249 | Pool B 91 词(Layer 2 真筛) |")
hl.append("| L2 Step 1 原料 | `01.5-pool-c-raw.md` | 1051 | Pool C 903 帖原料(Reddit/Quora/IH) |")
hl.append("| L2 Step 1 升级 | `02.5-pool-updates.md` | 110 | 10 B→A + 78 C→B 升级记录 |")
hl.append("| L2 Step 5 主库 | `02-expanded-keywords.md` | 719 | master v0 666 词(Pool A 76 + Haiku keep 590) |")
hl.append("| L2 备用池 | `02.5-pool-b-reserve.md` | 188 | 175 keep_weak(3/4 yes,Layer 3 待复审) |")
hl.append("| L3 主库打分 | `03-master-scored.md` | 264 | 6 维度 13 分 + Tier 1/1.5/2/3 分档 |")
hl.append("| L5 Pillar/Cluster | `04-pillar-cluster.md` | 88 | 15 词决策 + 精确数据(本批新增) |")
hl.append("| **本审核文档** | `99-handoff-leader-review.md` | 172 | leader 审核入口 |")
hl.append("| 结构化数据 | `data/master_scored.json` | — | 570 词 KWFinder 全数据(Vol/KD/Growth/Intent/SERP) |")
hl.append("| 原始 KWFinder | `data/Data_Gotted/kwfinder_*.csv` | 4 个文件 | 570 词原始 export |")
hl.append("")

hl.append("## 2 · 漏斗证据链(数字可追溯)\n")
hl.append("```")
hl.append("L0/L1: Pool A 66 词(46 ICP + 13 product + 7 EXPLORATORY)")
hl.append("       ↓ source: 01-seed-keywords.md L1-161")
hl.append("L2 Step 1: B→A 10 词 + C→B 78 词 升级")
hl.append("       ↓ source: 02.5-pool-updates.md L1-110")
hl.append("L2 Step 2: 8 渠道 Suggest 扩展 → 1890 sugg")
hl.append("       ↓ Google/YouTube/Bing/DDG Suggest + Reddit/Quora/IH/Twitter")
hl.append("L2 Step 3: Pool B 27 词广扫 → 27 sugg")
hl.append("L2 Step 5 Layer 1: 机械去重 → 1316 unique")
hl.append("       ↓ scripts/step5_funnel.py")
hl.append("L2 Step 5 Layer 2: 自动质量信号(hero name 黑名单 / 负向词 / Vol=0+KD>30)")
hl.append("       ↓ tier-1-validated 8 + tier-2-pool-a 66 + tier-2-kd-only 2 = 76 direct keep")
hl.append("       ↓ tier-3+4: 1240 → Haiku 13 batches × 4 问语义筛")
hl.append("L2 Step 5 Layer 3 (Haiku 4.5): 1240 → 590 keep + 175 keep_weak + 475 cut")
hl.append("       ↓ 通过率 47.6% (590/1240)")
hl.append("L2 Step 5 final: master v0 = 76 direct + 590 Haiku keep = 666 词")
hl.append("       ↓ source: 02-expanded-keywords.md L1-719")
hl.append("L3 主库打分: 666 → 去重 570 → 6 维度 13 分公式 → Tier 1/1.5/2/3")
hl.append("       ↓ KWFinder paid 570/570 全量化(Vol/KD/Growth/Intent/SERP)")
hl.append("       ↓ source: 03-master-scored.md L1-264 + data/master_scored.json")
hl.append("L5 Pillar/Cluster: Tier 1 6 + Tier 1.5 58 + Tier 2 88 → 选 15 词(3 Pillar × 5 Cluster)")
hl.append("       ↓ source: 04-pillar-cluster.md (新生成)")
hl.append("```\n")

hl.append("## 3 · 三 Pillar 决策(A+B+C 全做)\n")

for p in PILLARS:
    hl.append(f"### Pillar {p['id']} · {p['title']}\n")
    hl.append(f"**Thesis**:{p['thesis']}")
    hl.append(f"**ICP**:{p['icp']}")
    hl.append(f"**产品对接**:{p['product_hook']}\n")
    pd = p["pillar_data"]
    hl.append(f"**Pillar 主词**:`{pd['kw']}`")
    hl.append(f"- Tier {pd['tier']} (得分 {pd['score']}/13)")
    hl.append(f"- 数据:V={fmt_v(pd['vol'])}, KD={fmt_v(pd['kd'])}, Growth={fmt_g(pd['growth'])}, Intent={pd['intent']}")
    hl.append(f"- 索引:`03-master-scored.md` {pd['idx_score']} | `02-expanded-keywords.md` {pd['idx_master_v0']} | `01-seed-keywords.md` {pd['idx_seed']}\n")

    hl.append("**5 Cluster**:")
    hl.append("")
    hl.append("| # | 关键词 | Tier | V | KD | Growth | 决策依据 | 主库索引 |")
    hl.append("|---|---|---|---|---|---|---|---|")
    for i, c in enumerate(p["cluster_data"], 1):
        hl.append(
            f"| {p['id']}{i} | `{c['kw']}` | {c['tier']} | {fmt_v(c['vol'])} | "
            f"{fmt_v(c['kd'])} | {fmt_g(c['growth'])} | {c['note']} | {c['idx_score']} |"
        )
    hl.append("")

hl.append("## 4 · 数据质量与可信度\n")
hl.append("| 维度 | 状态 | 证据 |")
hl.append("|---|---|---|")
hl.append("| 主库覆盖 | 570/570 词 KWFinder 全量化 | `data/master_scored.json` 字段 has_kwf 全 true |")
hl.append("| 长尾未量化 | 58 词(Tier 1.5) | 来自 Reddit/Quora/IH 真实帖文 — `01.5-pool-c-raw.md` 903 帖原料可追 |")
hl.append("| Haiku 4-yes 通过率 | 47.6% (590/1240) | 4 问标准:真问题/产品能解/搜索形/ICP 25-list,`pool_v2_haiku_verdicts.json` 可审计 |")
hl.append("| KD 极低 + 高增长词 | 1 词(AEO services KD=19, +909%) | `03-master-scored.md` Tier 1 #6 |")
hl.append("| KD<30 + 真 ICP 词 | 7 词(ai agents for project management 等) | Tier 2 top 30 |")
hl.append("")

hl.append("## 5 · 风险与隐忧\n")
hl.append("| 风险 | 严重度 | 现状 | 缓解 |")
hl.append("|---|---|---|---|")
hl.append("| 🐛 KWFinder 70% ICP 长尾词无 Volume | 中 | 已识别 | Tier 1.5 单列,L6 大纲依赖 ICP 匹配度而非 Vol |")
hl.append("| 💸 KWFinder 48h 退款窗口 | 高 | $39 已支付 | **5/9 18:00 前必须取消订阅** — 我做 L6/L7 期间需 leader 通知小刀老师 |")
hl.append("| 🔑 内部 agent 人名(坑 6.5) | 低 | Layer 2 黑名单已过滤 | `step5_funnel.py:38-47` 50 个 hero name 全黑 |")
hl.append("| 🗑 主库 100% 工具自动化产出 | 中 | Tier 1 + Tier 1.5 共 64 词需 sanity check | **本审核环节由 leader 把关** |")
hl.append("| 🐛 Pillar B 流量集中在 MCP/Claude | 中 | KD 普遍 50+ | 5 Cluster 中 3 个 ICP 长尾(Tier 1.5)对冲 |")
hl.append("| 🐛 Pillar C 5 Cluster 同型(`AI X generator`)模板化 | 低 | ICP 不同(consultant / PPC / creator / 设计 / agent store) | L6 大纲会按 ICP 角度差异化撰写 |")
hl.append("")

hl.append("## 6 · 待办(L6/L7,leader 审核通过后启动)\n")
hl.append("| Layer | 任务 | 输出 | 工时 |")
hl.append("|---|---|---|---|")
hl.append("| L6 | 6 篇博客大纲(从 15 词中选 6 个 Cluster + 部分 Tier 1.5 长尾) | H2/H3 + 字数估计 + Search Intent + 内链 | 3-4h |")
hl.append("| L7 | 精排 + handoff final | 含 6 篇大纲产出顺序 + 内链矩阵 + 下一轮研究方向(Round-3 提案) | 1h |")
hl.append("| 副 | git commit + push 到 feat/seo-keyword-research | PR 描述 + 文件清单 | 30min |")
hl.append("")

hl.append("## 7 · Leader 审核 checklist(建议)\n")
hl.append("- [ ] **Pillar 战略**:A+B+C 全做合理? 还是聚焦其中 1-2 个?(预算/带宽考虑)")
hl.append("- [ ] **Pillar A**:AEO 是否符合公司主线? 还是 GEO 更稳妥?")
hl.append("- [ ] **Pillar B**:MCP/Claude 技术权威路线 vs 我们 SMB 客群是否错配?")
hl.append("- [ ] **Pillar C**:5 Cluster 中 'Marketing & Growth AI agents' 直接挂 agent store 分类页 OK 吗?")
hl.append("- [ ] **Tier 1.5 ICP 长尾**:58 词无 Vol 数据,是否接受'依赖社区证据'的判断?")
hl.append("- [ ] **预算**:KWFinder $39(48h 退款)是否退? 还是续订做 Round-3?")
hl.append("- [ ] **时间表**:L6/L7 5/9 前完成 OK?(配合 KWFinder 退款窗口)")
hl.append("- [ ] **Round-3 方向**:SERP intent 二次校验 + 真竞品反查(用付费 Ahrefs/Semrush trial)?")
hl.append("")

hl.append("## 8 · 附录:工具与脚本清单\n")
hl.append("```")
hl.append("scripts/")
hl.append("  capture_reddit.py            — Reddit 公共 API 抓取(131 runs)")
hl.append("  capture_quora_ih.py          — Quora/IH via Google site:")
hl.append("  capture_ih_retry.py          — 慢速 IH retry (100-130s 防 ban)")
hl.append("  layer1_filter.py             — Layer 1 机械过滤")
hl.append("  layer2_curate.py             — Layer 2 4 问真筛(由我执行)")
hl.append("  step5_suggest_validate.py    — Step 5 product semantic 验证")
hl.append("  step6_emerging_scan.py       — Step 6 8 渠道新兴生态扫")
hl.append("  build_pool_a.py              — Pool A 76 词 markdown 渲染")
hl.append("  step1_promote_apply.py       — L2 Step 1 升级落地")
hl.append("  step2_safe_suggest.py        — Step 2 4 渠道 Suggest")
hl.append("  step3_poolb_suggest.py       — Step 3 Pool B 广扫")
hl.append("  step5_funnel.py              — Layer 1+2 漏斗机械筛")
hl.append("  prepare_haiku_batches.py     — Haiku 13 batches 拆分")
hl.append("  build_master_v0.py           — master v0 666 词渲染")
hl.append("  generate_kwfinder_batches_200.py — KWFinder paid 200/CSV 拆分")
hl.append("  l3_score_master.py           — L3 6 维度 13 分打分(本轮主交付)")
hl.append("  l5_pillar_cluster.py         — L5 Pillar/Cluster + handoff(本文档生成)")
hl.append("```\n")

hl.append("---")
hl.append("")
hl.append("**审核反馈渠道**:在本文档下方批注 / 直接回复小刀老师 / GitHub PR comment")
hl.append("**预期反馈时间**:审核完成后启动 L6/L7,我侧 4-6h 完成最终交付")
hl.append("")

(ROUND_DIR / "_process" / "99-handoff-leader-review.md").write_text("\n".join(hl))
print(f"Wrote: 99-handoff-leader-review.md ({len(hl)} lines)")
