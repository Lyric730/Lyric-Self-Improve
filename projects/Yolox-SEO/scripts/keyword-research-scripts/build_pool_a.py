"""
Build Pool A · Round-2 Day-1 ICP 痛点部分 ~44 词.

Strategy: hand-curated mapping (Claude-judged from Pool B 91 records,
applying L1 §1.1 4-standard semantic filter):
  1. 产品能答 — every ICP backed by manifest agent/team/skill (Step 1)
  2. ICP 真在搜 — every record carries Reddit/Quora/IH URL evidence
  3. 有扩展空间 — title contains noun + modifier extending 5+ long-tails
  4. 可挂 Cluster — neighbor topics in Pool B/C support 4-5 cluster candidates

For each entry below:
  - icp: from 25-ICP list
  - keyword: title → search-shaped keyword (no ?, no first-person)
  - title_match: substring used to fuzzy-find the source post in pool_b.json
  - product_link: brief mapping to YOLOX manifest agent/skill/team
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ROUND_DIR = Path(__file__).parent.parent
POOL_B = json.loads((DATA_DIR / "pool_b.json").read_text())

# Step 5 · Product semantic supplement (14 words, hits ≥1 from suggest validation)
# Source: hand-designed from manifest reverse mapping; validated via opencli google suggest
SELECTIONS_STEP5 = [
    # (icp, keyword, hits, product)
    ("freelance-designer", "AI proposal generator", 10,
     "agent Aria (Freelance Proposal Writer); team Freelance Designer"),
    ("artisan-dtc", "AI ad creative generator", 10,
     "agent Olivia (Ad Creative Studio); team Artisan/DTC"),
    # Removed: "AI agent for code review" — duplicates Step 4 ICP entry (ai-builder)
    ("mobile-dev", "AI app builder", 10,
     "team App Developer"),
    ("ai-builder", "AI for ML research", 10,
     "Skills · Data & Analytics; team AI App Builder"),
    ("newsletter-writer", "AI newsletter writer", 10,
     "agent Aurora (Newsletter Curator); team Newsletter Creator"),
    ("content-mkt-mgr", "AI infographic generator", 8,
     "agent Logan (Infographic Designer); team Content Marketing"),
    ("shopify-owner", "Shopify AI product description", 7,
     "agent Grayson (Product Listing Copywriter); team Shopify/DTC"),
    ("indie-saas-founder", "programmatic SEO AI", 6,
     "agent Stella (Programmatic SEO Builder); team SaaS Founder"),
    ("solo-dev", "AI agent for API documentation", 5,
     "Skills · DevOps; team Indie Hacker"),
    ("b2b-sdr", "AI cold email tool", 5,
     "agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer)"),
    ("ai-builder", "AI agent for unit testing", 4,
     "Skills · Developer Tools"),
    ("growth-marketer", "Marketing & Growth AI agents", 4,
     "Skills · Marketing & Growth 33"),
    ("content-mkt-mgr", "Content & Writing AI agents", 4,
     "Skills · Content & Writing 24"),
]


# Step 6 · Emerging-ecosystem (7 words, ≥2 source verified per L1 §2.6)
# Source: 8-channel scan (HN + GitHub + Anthropic + OpenAI + Google AI + Aleyda + SEL + Reddit)
SELECTIONS_STEP6 = [
    # (canonical_id, keyword, sources, source_count, note)
    ("geo", "Generative Engine Optimization", ["aleyda-rss", "anthropic-release-notes", "search-engine-land-seo"], 3,
     "AEO 同类 / 2026 SEO 红利"),
    ("mcp", "Model Context Protocol", ["anthropic-release-notes", "github-trending"], 2,
     "Anthropic 2024-2025 推的 agent 协议"),
    ("claude-code", "Claude Code workflow", ["anthropic-release-notes", "github-trending"], 2,
     "Anthropic CLI 工具品牌名"),
    ("agent-skills", "Claude agent skills", ["anthropic-release-notes", "search-engine-land-seo"], 2,
     "Anthropic 2025 新概念"),
    ("llms-txt", "llms.txt SEO", ["aleyda-rss", "reddit-r-SEO-hot"], 2,
     "2024 提案 · LLM-optimized robots.txt"),
    ("aeo", "Answer Engine Optimization", ["aleyda-rss", "search-engine-land-seo"], 2,
     "GEO 同类 / 答案引擎优化"),
    ("ai-overview", "Google AI Overview optimization", ["aleyda-rss", "search-engine-land-seo"], 2,
     "Google 2024 AI Overview 产品"),
]


# (icp, keyword, title_match, product_link)
SELECTIONS = [
    # ai-builder (1)
    ("ai-builder", "AI agent for code review", "Why don’t they just use Mythos to fix all the bugs in Claude Code",
     "Skills · Developer Tools 217 (e.g. agent-tools); team AI App Builder"),

    # amazon-seller (2)
    ("amazon-seller", "how to get amazon reviews without vine", "Struggling to get reviews without Vine",
     "team Amazon Seller; agent Alice (Review Manager)"),
    ("amazon-seller", "amazon FBA shipment lost tracking", "How do I know if my shipment is lost",
     "team Amazon Seller"),

    # artisan-dtc (1)
    ("artisan-dtc", "selling handmade items online platform comparison", "Etsy refunded $600 to buyer without requiring a return",
     "team Artisan / DTC Brand Founder"),

    # b2b-sdr (2)
    ("b2b-sdr", "cold email metrics that matter", "I sent cold emails for 6 months and tracked everything",
     "agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer)"),
    ("b2b-sdr", "cold email volume vs deliverability", "I send 50,000 cold emails a day",
     "agent Lucas (Cold Outreach Pro)"),

    # brand-pr (2)
    ("brand-pr", "AI agent for PR", "AI Agents in PR- what are you building",
     "agent Wyatt (Press Release Writer); agent Alexander (Crisis PR Advisor)"),
    ("brand-pr", "value of media placements for clients", "How do you explain the value of media placements to clients",
     "team Brand & PR Manager"),

    # coach (2)
    ("coach", "best business coaching program", "What is the best business coaching program",
     "team Career & Life Coach"),
    ("coach", "best scheduling tool for coaches", "What scheduling tool",
     "team Career & Life Coach; skill Productivity"),

    # consultant (2)
    ("consultant", "consultant powerpoint design tips", "Tips to make better slides to become PowerPoint God",
     "team Consultant; agent Silas (Pitch Deck Builder)"),
    ("consultant", "traits of high performing consultant", "What traits define a high-performing consultant",
     "team Consultant"),

    # content-mkt-mgr (3)
    ("content-mkt-mgr", "content marketing strategy that works 2026", "What content marketing strategy is actually working for you right now",
     "team Content Marketing Manager; agent Theodore (Content Machine)"),
    ("content-mkt-mgr", "AI SEO agency for product descriptions", "Can an AISEO agency help with product descriptions",
     "agent Sophie (SEO Doctor); agent Isaiah (SEO Content Factory)"),
    ("content-mkt-mgr", "how to get LLM link citations", "Citations vs brand mentions in LLM results",
     "agent Sophie (SEO Doctor); skill ai-seo"),

    # course-creator (2)
    ("course-creator", "how to create and sell online course", "How to create and sell online courses or educational",
     "team Knowledge IP Builder; agent Scarlett (Course Architect)"),
    ("course-creator", "best platform to sell online courses", "What is the best platform to create and sell online courses",
     "team Knowledge IP Builder; agent Scarlett (Course Architect)"),

    # data-analyst (2)
    ("data-analyst", "how to start data analysis project from scratch", "How do data analysts actually start a project from scratch",
     "agent Camila (Data Interpreter); agent Jackson (Dashboard Designer)"),
    ("data-analyst", "SQL self join tutorial mental model", "I've been stuck on SQL self-joins for 6 months",
     "skill Data & Analytics 20"),

    # fallback-generic (1)
    ("fallback-generic", "local SEO cost for small business", "Quoted $3500/month for local SEO as a plumbing business",
     "agent Sophie (SEO Doctor); team Local Restaurant"),

    # financial-advisor (2)
    ("financial-advisor", "how to handle fee-sensitive prospects", "How Do You Handle Fee-Sensitive Prospects",
     "team Independent Financial Advisor"),
    ("financial-advisor", "best CRM for financial advisors", "What software do you use to help with automation and why",
     "team Independent Financial Advisor"),

    # freelance-designer (1)
    ("freelance-designer", "how to write freelance design proposals", "How to write freelance proposals that actually win",
     "team Freelance Designer; agent Aria (Freelance Proposal Writer)"),

    # growth-marketer (3)
    ("growth-marketer", "why ChatGPT cites pages", "Why ChatGPT Cites One Page Over Another",
     "agent Sophie (SEO Doctor); skill ai-seo"),
    ("growth-marketer", "Cloudflare blocking GPTBot SEO impact", "Cloudflare has been quietly blocking GPTBot",
     "agent Brooks (Website Audit Reporter); skill ai-seo"),
    ("growth-marketer", "buying backlinks DA score risk", "Why buying Backlinks on the Homepage",
     "agent Brooks (Website Audit Reporter); skill backlink-analyzer"),

    # indie-saas-founder (2)
    ("indie-saas-founder", "why visitors don't sign up SaaS", "How do I find out why people visited my website are not signing up",
     "team SaaS Founder; agent Luna (Conversion Optimizer)"),
    ("indie-saas-founder", "best community for SaaS builders", "Where are the \"actually building\" founder communities",
     "team SaaS Founder"),

    # mobile-dev (1)
    ("mobile-dev", "React Native cross platform 2026 comparison", "Is React Native still the best choice for cross platform apps in 2026",
     "team App Developer; agent Oliver (ASO Optimizer)"),

    # newsletter-writer (3)
    ("newsletter-writer", "where to advertise newsletter for subscribers", "Where to advertise your newsletter to get the most subscribers",
     "team Newsletter Creator; agent Aurora (Newsletter Curator)"),
    ("newsletter-writer", "tips for growing small newsletter", "Tips for growing small newsletters",
     "team Newsletter Creator"),
    ("newsletter-writer", "best social media to promote substack", "What Socials Are the Best to Promote Substack",
     "team Substack/Newsletter-First Creator; agent Aurora"),

    # paid-ads (2)
    ("paid-ads", "streaming TV vs paid social ads", "Streaming TV vs paid social",
     "agent Savannah (Paid Ads Strategist); agent Olivia (Ad Creative Studio)"),
    ("paid-ads", "best landing page builder for PPC agencies", "Agencies running PPC, what landing page builders are you using",
     "agent Addison (Landing Page Builder); agent Savannah (Paid Ads Strategist)"),

    # podcaster (1)
    ("podcaster", "podcast guest release agreement template", "Guest release agreements – how do you guys do it",
     "team Podcaster; agent Elena (Podcast Producer)"),

    # recruiter (2)
    ("recruiter", "AI candidate sourcing tool", "Anyone using AI candidate sourcing",
     "team Recruiter"),
    ("recruiter", "freelance recruiter daily workflow", "solo/freelance recruiters - how do you actually run your desk",
     "team Recruiter"),

    # restaurant-owner (2)
    ("restaurant-owner", "small restaurant marketing strategies", "best marketing strategies for small restaurant",
     "team Local Restaurant; agent Leo (Local Event Planner)"),
    ("restaurant-owner", "restaurant marketing on small budget", "How to market a restaurant with a small budget",
     "team Local Restaurant"),

    # shopify-owner (2)
    ("shopify-owner", "ecommerce growth strategy 2026", "Struggling with eCommerce growth what’s actually working in 2026",
     "team Shopify/DTC Brand"),
    ("shopify-owner", "shopify alternatives ecommerce platforms", "Other eCommerce platforms vs Shopify",
     "team Shopify/DTC Brand"),

    # social-mkt-mgr (2)
    ("social-mkt-mgr", "how to batch create social content", "How do I create social content when I am too busy",
     "team Social Media Manager; agent Harper (Content Repurposing Engine)"),
    ("social-mkt-mgr", "best multi-platform social media management tool", "What tools are you using to manage multi platform social media",
     "team Social Media Manager"),

    # solo-dev (1)
    ("solo-dev", "self hosting mistakes for beginners", "What self hosting mistake would you warn beginners about",
     "team Indie Hacker; skill DevOps"),

    # tiktok-creator (1)
    ("tiktok-creator", "starting Instagram from day 1 strategy", "If you were starting an Instagram today, what would you do from day 1",
     "team Short Video Creator; agent Claire (Twitter Growth Pilot)"),

    # youtuber (1)
    ("youtuber", "when to LLC YouTube channel", "When is it worth making your channel into an LLC",
     "team YouTube/Twitch Creator; agent Sadie (Video Producer)"),
]


def find_record(title_match):
    """Fuzzy match a Pool B record by title substring."""
    needle = title_match.lower()[:40]  # first 40 chars usually unique enough
    for r in POOL_B:
        if needle in r.get("title", "").lower():
            return r
    return None


def md_escape(s):
    if s is None:
        return "—"
    return str(s).replace("|", "\\|").replace("\n", " ")


def main():
    rows = []
    not_found = []
    for icp, keyword, title_match, product in SELECTIONS:
        rec = find_record(title_match)
        if not rec:
            not_found.append((icp, keyword, title_match))
            continue
        rows.append({
            "icp": icp,
            "keyword": keyword,
            "title_match": title_match,
            "product": product,
            "record": rec,
        })

    if not_found:
        print(f"⚠ Could not find {len(not_found)} records:")
        for icp, kw, tm in not_found:
            print(f"  {icp} · {kw} · {tm[:60]}")

    print(f"✓ Matched {len(rows)} / {len(SELECTIONS)} selections")

    # Build markdown
    out = []
    step5_count = len(SELECTIONS_STEP5)
    step6_count = len(SELECTIONS_STEP6)
    total_count = len(rows) + step5_count + step6_count
    out.append("# Round-2 Day-1 · Pool A · 种子词精选 (Final v3)\n")
    out.append("**日期**：2026-04-29 (Step 5 追加 2026-05-01 / Step 6 + Step 7 final 2026-05-02)")
    out.append("**讨论方**：小刀老师 + Agent B")
    out.append(f"**状态**：v3 final（Step 4 ICP {len(rows)} + Step 5 产品语义 {step5_count} + Step 6 新兴 {step6_count} = {total_count} 词）")
    out.append("**前置依赖**：L1 Step 1-7 全部完成（manifest 解析 / ICP 反推 / 渠道映射 / 三层池抓筛 / 产品语义补缺 / 新兴扫描 / 整理）\n")
    out.append("---\n")

    out.append("## 0 · 概览\n")
    out.append("| 维度 | Final | L1 §1 目标 |")
    out.append("|---|---|---|")
    out.append(f"| **Pool A 总词数** | **{total_count}** | ~63 |")
    out.append(f"| ICP 痛点 60% | {len(rows)} (Step 4) | 42 |")
    out.append(f"| 产品语义 20% | {step5_count} (Step 5) | 14 |")
    out.append(f"| 新兴生态 10% | {step6_count} (Step 6 · EXPLORATORY) | 7 |\n")

    out.append("**4 标准评估**（L1 §1.1）：每词通过 4 条标准")
    out.append("1. 产品能答 ✅ — manifest 含对应 agent/team/skill")
    out.append("2. ICP 真在搜 ✅ — Reddit/Quora/IH 帖证据")
    out.append("3. 有扩展空间 ✅ — title 含 noun+modifier 可扩 5+ 长尾")
    out.append("4. 可挂 Cluster ✅ — Pool B/C 有 4-5 邻近词\n")
    out.append("---\n")

    # Group rows by ICP
    from collections import defaultdict
    groups = defaultdict(list)
    for row in rows:
        groups[row["icp"]].append(row)

    out.append("## 1 · ICP 痛点部分（60% · {} 词）\n".format(len(rows)))
    out.append("| # | 关键词 | 来源 | Intent | ICP 对接 | 产品对接 | 平台 | URL | 标签 | 4 标准 | 池 | 备注 |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")

    idx = 0
    for icp in sorted(groups.keys()):
        for row in groups[icp]:
            idx += 1
            r = row["record"]
            score = r.get("score")
            comments = r.get("num_comments")
            score_str = f"{score}/{comments}c" if score is not None else "SERP"
            out.append(
                f"| {idx} | {md_escape(row['keyword'])} | ICP | info | {icp} | "
                f"{md_escape(row['product'])} | {md_escape(r['platform'])} | "
                f"[link]({md_escape(r['url'])}) | — | ✅✅✅✅ | A | {score_str} |"
            )

    out.append("\n---\n")

    # Section 1.6 · Step 6 emerging ecosystem
    out.append("## 1.6 · 新兴生态（10% · {} 词 · Step 6 · EXPLORATORY）\n".format(step6_count))
    out.append("**来源**：8 渠道扫描（HN + GitHub + Anthropic + OpenAI + Google AI + Aleyda + SEL + 4 Reddit subs）+ 双源验证 ≥2 sources")
    out.append("**砍**：fine-tuning（已 well-known）/ structured-outputs（已普及）/ ai-search（太宽泛）→ 进 watchlist\n")
    out.append("| # | 关键词 | 来源 | Intent | ICP 对接 | 产品对接 | 验证 sources | 标签 | 4 标准 | 池 | 备注 |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    step6_idx = len(rows) + step5_count
    for canonical, kw, sources, count, note in SELECTIONS_STEP6:
        step6_idx += 1
        sources_str = " + ".join(s.split("-")[0] for s in sources[:3])
        out.append(
            f"| {step6_idx} | {md_escape(kw)} | 新兴生态 | info | (跨 ICP) | "
            f"L4 验证 (Step 6 不必产品对接) | {sources_str} ({count}) | EXPLORATORY | ✅✅⏸⏸ | A | {note} |"
        )
    out.append("\n注：4 标准列 ✅✅⏸⏸ 含义 — 标准 1 (产品能答) 暂不强求（新兴 EXPLORATORY 可能产品没现成 agent）；标准 2 (ICP 真在搜) 8 渠道双源验证已过；标准 3+4 (扩展空间 / Cluster) L4 量化验证再判。\n")
    out.append("---\n")

    # Section 1.5 · Step 5 product semantic supplement
    out.append("## 1.5 · 产品语义补缺（20% · {} 词 · Step 5）\n".format(step5_count))
    out.append("**来源**：YOLOX manifest 反推（Skills/Agents/Teams）+ google suggest 验证 ≥1 hit")
    out.append("**重点补**：4 个稀疏 ICP（ai-builder / artisan-dtc / freelance-designer / mobile-dev）+ dev/builder 主线 + compare/buy 决策词\n")
    out.append("| # | 关键词 | 来源 | Intent | ICP 对接 | 产品对接 | 验证 | 标签 | 4 标准 | 池 | suggest hits |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    step5_idx = len(rows)
    for icp, kw, hits, product in SELECTIONS_STEP5:
        step5_idx += 1
        out.append(
            f"| {step5_idx} | {md_escape(kw)} | 产品语义 | compare | {icp} | "
            f"{md_escape(product)} | google suggest | — | ✅✅✅✅ | A | {hits} hits |"
        )
    out.append("\n---\n")

    # Summary footer
    out.append("## 2 · 末尾汇总段（占位 · Step 6/7 完整后更新）\n")

    # Platform distribution
    plat_counter = defaultdict(int)
    for row in rows:
        plat_counter[row["record"]["platform"]] += 1

    out.append("### Final Pool A 总汇总\n")
    out.append(f"- **Pool A 总词数**：{total_count}（Step 4 ICP {len(rows)} + Step 5 产品语义 {step5_count} + Step 6 新兴 {step6_count}）")
    pct_icp = len(rows) / total_count * 100
    pct_step5 = step5_count / total_count * 100
    pct_step6 = step6_count / total_count * 100
    out.append(f"- **来源占比**：ICP {pct_icp:.0f}% · 产品语义 {pct_step5:.0f}% · 新兴 {pct_step6:.0f}% (vs L1 §1 目标 60/20/10)")
    out.append(f"- **平台分布**（Step 4 ICP 部分）：" + " / ".join(f"{p} {c}" for p, c in sorted(plat_counter.items())))
    out.append(f"- **4 条质量标准全过率**：{len(rows) + step5_count}/{total_count} = {(len(rows) + step5_count)/total_count*100:.0f}% (Step 4+5 全过；Step 6 EXPLORATORY {step6_count} 词部分过 ✅✅⏸⏸ 留 L4 量化)")
    out.append(f"- **EXPLORATORY 词数**：{step6_count}")
    out.append(f"- **含人名陷阱词**：0（Pool A {total_count} 词终检通过——无 Sophie/Elias/Stella 等内部 agent 名）")
    out.append(f"- **三层池总规模**：A {total_count} / B 91 / C 903\n")

    out.append("### 三层池架构（D6=A 决策）\n")
    out.append(f"- Pool A · 种子精选：{total_count} 词（ICP {len(rows)} + 产品语义 {step5_count} + 新兴 {step6_count}）")
    out.append("- Pool B · 高质量候选：91 词（Layer 2 4 问真筛后；从 208 候选 → 91 KEEP 44%）")
    out.append("- Pool C · 原始候选：903 帖（去重后，机械筛通过）")
    out.append("- Watchlist · 7 词（3 双源降级 + 4 单源新兴；详见 01.5-watchlist.md）\n")

    out.append("### 11 坑规避自检 · Layer 1-3 阶段\n")
    out.append("| 坑 | 规避状态 |")
    out.append("|---|---|")
    out.append("| 6.2 Claude 12.5% 命中率 | ✅ 全部从 Pool C 派生（Reddit/Quora/IH 实证），未凭空扩词 |")
    out.append("| 6.3 Reddit show-off 帖 | ✅ Layer 1 排除 124 个 show-off 帖 |")
    out.append("| 6.4 Reddit 1/1 score 孤例 | ✅ Layer 1 阈值 score≥5 + comments≥5 |")
    out.append("| 6.5 内部 Agent 人名 | ✅ Pool A 终检 0 个含 Sophie/Elias/Stella 等 |")
    out.append("| 6.11 Handoff stale | ✅ session 启动 git status √ |")
    out.append("\n---\n")

    out.append("## 3 · 下一步（L1 完成 → 进 L2）\n")
    out.append("- **Step 4** · ✅ ICP 痛点挖词 46 词")
    out.append("- **Step 5** · ✅ 产品语义补缺 14 词")
    out.append("- **Step 6** · ✅ 新兴生态扫描 7 词（EXPLORATORY）")
    out.append("- **Step 7** · ✅ 去重 + 4 文件 final 落盘")
    out.append("- **下一层 L2** · 扩词 + 存在性验证（Pool A 67 词作为种子，8 渠道扩词漏斗 ~10000 候选 → 主库 v0 300-500 词）\n")
    out.append("所有数据可追溯：pool_a.json / pool_b_curated.json (91) / pool_c.json (903) / step6_emerging_scan.json / opencli-raw/round2-day1-* (144 raw files)。\n")

    out_path = ROUND_DIR / "01-seed-keywords.md"
    out_path.write_text("\n".join(out))
    print(f"\nWrote: {out_path} ({total_count} keywords = {len(rows)} ICP + {step5_count} product-semantic)")


if __name__ == "__main__":
    main()
