"""
L5 v2 · 4 Pillar × 5 Cluster 最终架构(Ben 第二轮反馈 + 小刀老师 5/7 拍板).

变化 vs v1(scripts/l5_pillar_cluster.py):
  · v1: 3 Pillar(A/B/C),已 commit
  · v2: 4 Pillar(AEO/α/β/γ),其中 AEO 是小刀老师在 Ben 3 Pillar 基础上加的
  · v2: AEO services 从原 v1 的 A2 cluster 升为 AEO Pillar 的 cluster
  · v2: 4 Pillar 主词 + 20 cluster = 24 keyword 矩阵

输出:
  · 04-pillar-cluster.md(覆盖 v1)
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


idx = {normalize(r["keyword"]): r for r in MASTER}


def lookup(kw):
    return idx.get(normalize(kw))


def fmt_v(v):
    return str(v) if v is not None else "—"


def fmt_g(g):
    return f"{g}%" if g is not None else "—"


# === 4 Pillar × 5 Cluster 架构 ===
PILLARS = [
    {
        "id": "AEO",
        "title": "Answer Engine Optimization",
        "thesis": "AI 搜索时代的 SEO — 内容被 ChatGPT/Perplexity/Google AI Overview 引用,而不是被 Google 排第一。",
        "icp": "marketer / 内容运营 / SMB owner(评估外包)/ in-house SEO 经理",
        "product_hook": "yolox AEO audit agent(Round-3 ship)",
        "blog_silo": "/blog/aeo/",
        "pillar_kw": "Answer Engine Optimization",
        "pillar_status": "✅ 大纲 ship · `blog-outlines/L6-00-pillar-aeo.md`",
        "cluster_status": [
            ("answer engine optimization services", "AEO-1", "✅ 大纲 ship · L6-01", "/blog/aeo/services-guide", "AEO audit agent"),
            ("Generative Engine Optimization", "AEO-2", "✅ 大纲 ship · L6-07", "/blog/aeo/generative-engine-optimization", "/agents-store"),
            ("aeo vs geo", "AEO-3", "✅ 大纲 ship · L6-08", "/blog/aeo/aeo-vs-geo", "/agents-store"),
            ("answer engine optimization tools", "AEO-4", "✅ 大纲 ship · L6-09", "/blog/aeo/tools-comparison", "/agents-store"),
            ("Google AI Overview optimization", "AEO-5", "✅ 大纲 ship · L6-10(Tier 1.5 ICP 长尾)", "/blog/aeo/google-ai-overview-optimization", "/agents-store"),
        ],
    },
    {
        "id": "α",
        "title": "AI 工具替代专业岗位",
        "thesis": "中小企业'非技术'白领用 AI agent 替代专业工具(设计/proposal/广告/newsletter) — yolox ICP 主战场。",
        "icp": "consultant / freelancer / 创意从业者 / SMB owner",
        "product_hook": "yolox agent store 'AI Tools' 分类(直接对接 6+ 具体 product agent)",
        "blog_silo": "/blog/ai-tools/",
        "pillar_kw": "AI infographic generator",
        "pillar_status": "✅ 大纲 ship(Hybrid 主文)· `blog-outlines/L6-00-pillar-alpha.md`(主词锁定保留)",
        "cluster_status": [
            ("AI proposal generator", "α-1", "✅ 大纲 ship · L6-03", "/blog/ai-tools/ai-proposal-generator", "/agents-store"),
            ("AI ad creative generator", "α-2", "✅ 大纲 ship · L6-11", "/blog/ai-tools/ai-ad-creative-generator", "/agents-store"),
            ("story writer AI", "α-3", "✅ 大纲 ship · L6-12", "/blog/ai-tools/ai-story-writer", "/agents-store"),
            ("AI newsletter writer", "α-4", "✅ 大纲 ship · L6-13", "/blog/ai-tools/ai-newsletter-writer", "/agents-store"),
            ("Marketing & Growth AI agents", "α-5", "✅ 大纲 ship · L6-14(Tier 1.5 ICP 长尾)", "/blog/ai-tools/marketing-growth-ai-agents", "/agents-store"),
        ],
    },
    {
        "id": "β",
        "title": "B2B Sales & 招聘 AI 工具",
        "thesis": "B2B 销售/招聘/PM 是 yolox agent store '销售/招聘/客服 agent' 分类的内容引流入口,比 MCP/Claude 路线短得多。",
        "icp": "SDR / sales 自营 founder / recruiter / PM / financial advisor",
        "product_hook": "yolox agent store 'Sales & Recruiting' 分类",
        "blog_silo": "/blog/b2b/",
        "pillar_kw": "ai tools for recruiting",
        "pillar_status": "✅ 大纲 ship · `blog-outlines/L6-00-pillar-beta.md`(主文聚焦招聘 stack 全景,L6-06 cluster 化聚焦 stage 详情)",
        "cluster_status": [
            ("cold email deliverability", "β-1", "✅ 大纲 ship · L6-04", "/blog/b2b/cold-email-deliverability", "/agents-store"),
            ("ai agents for project management", "β-2", "✅ 大纲 ship · L6-05", "/blog/b2b/ai-agents-project-management", "/agents-store"),
            ("ai tools for recruiters", "β-3", "✅ 大纲 ship · L6-15(单复数差异 vs Pillar 主词)", "/blog/b2b/ai-tools-for-recruiters", "/agents-store"),
            ("cold calling AI", "β-4", "✅ 大纲 ship · L6-16", "/blog/b2b/cold-calling-ai", "/agents-store"),
            ("best CRM for financial advisors", "β-5", "✅ 大纲 ship · L6-17", "/blog/b2b/crm-financial-advisors", "/agents-store"),
        ],
    },
    {
        "id": "γ",
        "title": "Creator & SMB Owner Toolkit",
        "thesis": "覆盖 4 个最常见 SMB 业主类型(podcaster / amazon seller / shopify owner / restaurant owner)+ 一个高流量 head。",
        "icp": "podcaster / amazon seller / shopify owner / restaurant owner / creator",
        "product_hook": "yolox agent store 'Creator Tools' 分类",
        "blog_silo": "/blog/creator/",
        "pillar_kw": "social media management tools",
        "pillar_status": "✅ 大纲 ship · `blog-outlines/L6-00-pillar-gamma.md`",
        "cluster_status": [
            ("podcast guest release form", "γ-1", "✅ 大纲 ship · L6-02", "/blog/creator/podcast-guest-release-form", "/agents-store(留引子:AI 模板生成 agent alpha)"),
            ("podcast name generator", "γ-2", "✅ 大纲 ship · L6-18", "/blog/creator/podcast-name-generator", "/agents-store"),
            ("amazon vine reviewer", "γ-3", "✅ 大纲 ship · L6-19", "/blog/creator/amazon-vine-reviewer", "/agents-store"),
            ("ecommerce growth strategy", "γ-4", "✅ 大纲 ship · L6-20", "/blog/creator/ecommerce-growth-strategy", "/agents-store"),
            ("restaurant marketing strategies", "γ-5", "✅ 大纲 ship · L6-21", "/blog/creator/restaurant-marketing-strategies", "/agents-store"),
        ],
    },
]


# Validate all keywords exist in master
print("=== 验证 24 keyword 全部在 master_scored.json 内 ===")
miss = []
for p in PILLARS:
    if not lookup(p["pillar_kw"]):
        miss.append(p["pillar_kw"])
    for kw, *_ in p["cluster_status"]:
        if not lookup(kw):
            miss.append(kw)

if miss:
    print(f"❌ 缺失 {len(miss)} 词:")
    for m in miss:
        print(f"  · {m}")
else:
    print("✅ 24 词全部命中 master")


# === Render 04-pillar-cluster.md (v2) ===
lines = []
lines.append("# Round-2 · L5 v2 · 4 Pillar × 5 Cluster 最终架构 · 04-pillar-cluster\n")
lines.append("**日期**:2026-05-08(更新版)")
lines.append("**版本**:v2.1 · 25 大纲全 ship 后的进度 update")
lines.append("**讨论方**:小刀老师 + Agent B + Ben(leader review)")
lines.append("**状态**:✅ **大纲全 ship** · 4 Pillar 主文 + 21 cluster(L6-06 双重身份)= 25 大纲文档,对应 24 词矩阵")
lines.append("**前置依赖**:Ben PR #14 反馈 (4395391661 + 4395487693) + 小刀老师 5/7 + 5/8 拍板\n")
lines.append("---\n")

lines.append("## 0 · 概览\n")
lines.append("| Pillar | 主词 | Pillar 主文 | 5 Cluster |")
lines.append("|---|---|---|---|")
for p in PILLARS:
    cluster_kws = ", ".join(c[0] for c in p["cluster_status"])
    lines.append(f"| **{p['id']} · {p['title']}** | `{p['pillar_kw']}` | {p['pillar_status'][:40]} | {cluster_kws} |")
lines.append("")

lines.append("## 1 · ship 进度(本轮 vs Round-3+)\n")
total_done = sum(1 for p in PILLARS for c in p["cluster_status"] if "✅" in c[2])
total_pending = sum(1 for p in PILLARS for c in p["cluster_status"] if "🔴" in c[2] or "🟡" in c[2])
total_pillar_done = sum(1 for p in PILLARS if "✅" in p["pillar_status"])
total_pillar_pending = len(PILLARS) - total_pillar_done

lines.append(f"| 类别 | 数量 | 状态 |")
lines.append(f"|---|---|---|")
lines.append(f"| Pillar 主文 | {len(PILLARS)} | {total_pillar_done} ✅ / {total_pillar_pending} 🔴 待 Round-3 |")
lines.append(f"| Cluster 文章 | 20 | {total_done} ✅ L6 大纲已 ship / {total_pending} 🔴 L6-2 批或 Round-3 |")
lines.append(f"| **总规划** | **24** | **{total_done}/24 ({total_done*100//24}%) 完成大纲** |")
lines.append("")

lines.append("## 2 · 全矩阵详细数据\n")

for p in PILLARS:
    lines.append(f"### Pillar {p['id']} · {p['title']}\n")
    lines.append(f"**Thesis**:{p['thesis']}\n")
    lines.append(f"**ICP**:{p['icp']}\n")
    lines.append(f"**产品对接**:{p['product_hook']}\n")
    lines.append(f"**Blog silo**:`{p['blog_silo']}`\n")

    # Pillar 主词
    pdata = lookup(p["pillar_kw"])
    if pdata:
        lines.append(f"#### 🏛️ Pillar 主词:`{pdata['keyword']}`")
        lines.append(f"- **状态**:{p['pillar_status']}")
        lines.append(f"- **数据**:V={fmt_v(pdata.get('kwf_volume'))}, KD={fmt_v(pdata.get('kwf_kd'))}, Growth={fmt_g(pdata.get('kwf_growth'))}")
        lines.append(f"- **Tier**:{pdata['tier']} ({pdata['score_total']}/13)")
        lines.append(f"- **Intent**:{pdata.get('kwf_intent') or '(KWFinder 未填)'}")
        lines.append(f"- **预期 URL**:`{p['blog_silo']}` (目录入口)")
        lines.append(f"- **索引**:`data/master_scored.json` + `03-master-scored.md`")
        lines.append("")

    # 5 Cluster
    lines.append(f"#### 📚 5 Cluster\n")
    lines.append("| # | 关键词 | V | KD | Growth | Tier | 状态 | URL | CTA |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for kw, cid, status, url, cta in p["cluster_status"]:
        cdata = lookup(kw)
        if not cdata:
            lines.append(f"| {cid} | `{kw}` | ❌ 未找到 | — | — | — | — | — | — |")
            continue
        lines.append(
            f"| {cid} | `{cdata['keyword']}` | "
            f"{fmt_v(cdata.get('kwf_volume'))} | "
            f"{fmt_v(cdata.get('kwf_kd'))} | "
            f"{fmt_g(cdata.get('kwf_growth'))} | "
            f"{cdata['tier']} | {status} | `{url}` | {cta} |"
        )
    lines.append("")

# === Section 3: Ben 锁定的 6 篇优先 markdown ===
lines.append("## 3 · Ben 锁定 · 6 篇优先写 markdown(Round-3 实施)\n")
lines.append("**说明**:25 篇大纲全部 ship,但 Ben 锁定 6 篇 KD ≤ 25 的快赢词优先写成 markdown 实际发布,先拿 ranking 反馈。\n")
lines.append("| L6 # | Pillar | 关键词 | KD | Growth | URL |")
lines.append("|---|---|---|---|---|---|")
ben_locked = [
    ("L6-01", "AEO", "answer engine optimization services", "/blog/aeo/services-guide"),
    ("L6-02", "γ", "podcast guest release form", "/blog/creator/podcast-guest-release-form"),
    ("L6-03", "α", "AI proposal generator", "/blog/ai-tools/ai-proposal-generator"),
    ("L6-04", "β", "cold email deliverability", "/blog/b2b/cold-email-deliverability"),
    ("L6-05", "β", "ai agents for project management", "/blog/b2b/ai-agents-project-management"),
    ("L6-06", "β", "ai tools for recruiting (β 主词)", "/blog/b2b/ai-tools-for-recruiting"),
]
for l6id, pid, kw, url in ben_locked:
    cdata = lookup(kw.replace(" (β 主词)", ""))
    if cdata:
        lines.append(
            f"| **{l6id}** | {pid} | `{cdata['keyword']}` | "
            f"{fmt_v(cdata.get('kwf_kd'))} | {fmt_g(cdata.get('kwf_growth'))} | `{url}` |"
        )
lines.append("")
lines.append("**6 篇 Pillar 分布**:AEO=1 / α=1 / β=3 / γ=1(Ben 按 KD ≤ 25 选,β 偏多因为 β 内 KD 低词多)\n")

# === Section 4: Round-3+ 实施清单 ===
lines.append("## 4 · Round-3+ 实施清单(剩 19 大纲 → markdown)\n")
lines.append("**说明**:25 大纲已 ship,Ben 锁定 6 篇优先 markdown(本轮 Phase),剩 19 篇大纲(4 Pillar 主文 + 15 cluster)在 Round-3+ 写 markdown。\n")

lines.append("### Pillar 主文(4 篇)— Round-3 ship,给 cluster 提供 inbound 链 target\n")
for p in PILLARS:
    lines.append(f"- **{p['id']} 主文** · `{p['pillar_kw']}` · 大纲已 ship · 路径 `{p['blog_silo']}`")
lines.append("")

ben_locked_kws = {kw.replace(" (β 主词)", "") for _, _, kw, _ in ben_locked}
lines.append("### Cluster 文章(剩 15 篇 — 除 Ben 6 篇外)\n")
for p in PILLARS:
    pending = [(kw, cid, url) for kw, cid, _, url, _ in p["cluster_status"] if kw not in ben_locked_kws]
    if pending:
        lines.append(f"**Pillar {p['id']}**({len(pending)} 篇):")
        for kw, cid, url in pending:
            lines.append(f"  - `{kw}` ({cid}) · `{url}`")
lines.append("")

# === Section 5: 已决策记录 ===
lines.append("## 5 · 已决策记录(Ben + 小刀老师 5/7-5/8)\n")
lines.append("| # | 决策 | 决策方 | 日期 |")
lines.append("|---|---|---|---|")
lines.append("| 1 | 4 Pillar × 5 Cluster = 24 词架构 final | 小刀老师 + Ben | 2026-05-07 |")
lines.append("| 2 | α Pillar 主词保留 `AI infographic generator`(KD 低优先,放弃 `AI app builder`)| 小刀老师 | 2026-05-08 |")
lines.append("| 3 | Pillar α 主文用 Hybrid 方式(target 窄词 + hub 5 cluster)| 小刀老师 | 2026-05-08 |")
lines.append("| 4 | 25 篇大纲全 ship,Ben 6 篇优先写 markdown,剩 19 篇 Round-3+ | Ben + 小刀老师 | 2026-05-08 |")
lines.append("| 5 | KWFinder paid 5/9 18:00 前退订(已用全 570 词数据)| Ben + 小刀老师 | 2026-05-08 |")
lines.append("")

# === Section 6: 已识别风险 ===
lines.append("## 6 · 已识别风险(Round-3 关注)\n")
lines.append("| # | 风险 | 严重度 | 缓解 |")
lines.append("|---|---|---|---|")
lines.append("| 1 | **α Pillar 主词词义偏窄** — `AI infographic generator` 只 cover infographic 一类,但 cluster 涵盖 5 种工具 | 🟡 中 | Hybrid 主文设计(target 窄词 + 文末 hub 到其他 cluster)— L6-00-pillar-alpha 大纲已实现 |")
lines.append("| 2 | β Pillar 主词与 β-3 单复数差异(`ai tools for recruiting` vs `ai tools for recruiters`)| 🟢 低 | 主词聚焦『招聘 stack 全景』(Pillar 主文)/ cluster 聚焦『recruiter 个体工具栈』(L6-15)|")
lines.append("| 3 | Pillar 主文 Round-3 才写 markdown,cluster ship 时内链上行 anchor 占位 | 🟡 中 | 大纲已埋 anchor 占位,Round-3 ship Pillar 主文后 anchor 自动 live |")
lines.append("")

# === Section 7: Footnote ===
lines.append("---")
lines.append("")
lines.append("## 附录 · 数据可信度\n")
lines.append("- 24 词全部在 `data/master_scored.json` 570 词 KWFinder paid 全量化覆盖内 ✅")
lines.append("- V/KD/Growth 数据来自 KWFinder paid(2026-05-07 export)")
lines.append("- Tier 来自 6 维度 13 分公式(`scripts/l3_score_master.py`)")
lines.append("- Pillar 选择基于 Ben PR #14 反馈 + 小刀老师 5/7 拍板")
lines.append("")

(ROUND_DIR / "_process" / "04-pillar-cluster.md").write_text("\n".join(lines))
print(f"\nWrote: 04-pillar-cluster.md ({len(lines)} lines)")
print(f"Total keywords in matrix: 4 Pillar + 20 Cluster = 24")
print(f"L6 outlines done: {total_done}/20 cluster")
print(f"Pillar main posts: {total_pillar_done}/4")
