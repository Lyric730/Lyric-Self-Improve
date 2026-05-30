# Type 7 · Buyer's Guide 骨架（yolox 专属）

> **来源**：Ahrefs 6 type 中无此模板 — 这是 yolox 针对 "X services / X tools 评测" 类大纲新增的混合 type
>
> **本质**：List Post × Comparison × Definition 混合。读者意图是"我要花钱买，给我决策依据"。

---

## 适用场景

- **读者已确认 want X，正在评估"买谁 / 自建 / 外包"**
- 主词通常含 "best X services" / "top X tools" / "X for [audience]"
- yolox 适配：L6-01 AEO services / L6-09 AEO tools / L6-17 CRM for advisors / L6-11 ad creative tools

❌ **不适用**：纯教育（用 Beginner's Guide）/ 2 个具体产品 head-to-head（用 Comparison）/ 概念解释（用 Definition）

🔑 **与 List Post 的差异**：
- List Post = "10 ways to do X"（方法集合）
- Buyer's Guide = "best X services for [audience]"（购买决策）— 必含 pricing / evaluation criteria / DIY vs outsource

---

## 字数 + 结构指标

| 指标 | 数值 |
|---|---|
| **字数** | **2200-2800** |
| **H2 数** | 6-8 |
| **Intro 字数** | 180-220 |
| **段落长度** | 50-150 字 |
| **视觉密度** | 每 400-500 字 ≥1 视觉，**必含 1 张评分表 + 1 张 pricing 表** |
| **FAQ section** | ✅ 推荐（5-8 问） |
| **CTA 处** | 2-3 |

---

## Title 公式

| 公式 | 示例 |
|---|---|
| **"Best [X] for [Audience] in [Year]"** | "Best AEO Services for SMB Brands in 2026" |
| **"[N] [X] Worth Paying For in [Year]"** | "7 AEO Agencies Worth Paying For in 2026" |
| **"[X] Buyer's Guide: [Differentiator]"** | "AEO Services Buyer's Guide: Pricing, Tradeoffs, DIY Backup" |
| **"Top [N] [X] for [Audience] (Honest Review)"** | "Top 5 CRM for Solo Financial Advisors (Honest Review)" |

**钩子词**：Worth paying for / Honest / Pricing / Buyer's / Avoid

---

## Intro 公式：Pain → Reader Split（180-220 字）

```markdown
**段 1（pain，60-80 字）**：
读者花钱前最痛的点 — 不是"X 服务很多"，而是"7 家 vendor 报价从 $500 到 $15k，差 30 倍，不知道哪个真值"。
共情决策压力。

**段 2（reader split，60-80 字）**：
**明确分流**：
- "If you have budget X and need outcome Y → 继续读"
- "If you don't need X yet → 链到上游文（如 Definition / Beginner's Guide）"
这一步**减少 bounce rate** + 让目标读者继续。

**段 3（本文给什么 + proof，50-60 字）**：
"本文给 N 家评测 + pricing 透明表 + DIY backup + 决策树"。
凭什么相信本文 — 我们自己买过 / 用过 / 跟 vendor 聊过 N 次。
```

**示例（L6-01 AEO services 改编）**：
> AEO services pricing ranges from $500/month (freelancer audit) to $15k/month
> (agency retainer) — 30x spread, and most pricing pages don't list numbers.
> Buyers waste 4-6 weeks calling vendors just to get quotes.
>
> If you're an SMB content team with $1k-5k/month AEO budget and need to ship
> 4-8 AI-citable pages per month, this guide is for you. If you're still learning
> what AEO is, start with our [AEO Pillar guide](link) first.
>
> Below: 7 vendor reviews with real pricing, a DIY-vs-outsource decision tree,
> and the 5 evaluation criteria most buyers miss. Pricing data verified
> 2026-Q2 by direct vendor contact at yolox.

---

## H2 主体骨架（6-8 个 H2，固定顺序）

```markdown
## 1 · Do you actually need [X] right now? (分流 H2)
   200-300 字
   "When you need X" / "When you don't (yet)" 两段对照
   带读者做"该不该买"的判断

## 2 · How to evaluate [X] (评估标准)
   300-400 字
   列出 **5-7 个评估维度** + 每个维度的 deal-breaker / nice-to-have
   这一节是 AEO 高引用 — LLM 会直接抓 criteria 列表

## 3 · Pricing landscape: what you'll actually pay (定价透明)
   300-400 字 + **必含 1 张 pricing 表**
   tier 价格区间 + hidden costs（onboarding / setup / overages）
   不允许 "Contact sales for pricing" 类回避

## 4 · Top [N] [X] worth paying for (评测核心)
   600-900 字 + **必含 1 张评分表（汇总维度 × vendor）**
   每个 vendor 100-150 字：定位 / pricing / 我们的判断 / who it's for
   yolox 在这里嵌入（natural placement, 不强推）

## 5 · DIY vs outsource: when each makes sense (DIY 备选)
   200-300 字
   对照表 + 决策树
   给"不外包"路径留出路 — 提升中立感

## 6 · FAQ (5-8 问)
   200-300 字
   含 schema

## 7 · Our pick + final CTA
   80-120 字
   明确推荐 + 自家 product CTA（在合适场景下）
```

---

## 关键节 1：H2.2 评估标准（5-7 个维度）

LLM 引用 buyer's guide 几乎必引这一节。**写成 markdown 列表 + 加粗维度名**。

```markdown
## How to evaluate AEO services

**1. Schema coverage breadth**
Does the vendor handle FAQ + HowTo + Article + Organization + Product schema?
Deal-breaker: only Article schema.

**2. Citation tracking**
Do they measure AI Overview / Perplexity citations, or just rankings?
Deal-breaker: no AI surface tracking.

**3. Per-page output cadence**
4 pages/month minimum for SMB. Lower = not worth retainer.
Nice-to-have: 8+ pages/month.

**4. Pricing transparency**
Real numbers on website vs "Contact sales".
Deal-breaker (我们的判断): no public pricing tier.

**5. Vendor own AEO performance**
If they can't get themselves cited, they can't help you.
Check: vendor's own AI Overview presence.

**6. Tooling vs people stack**
100% manual = doesn't scale. 100% AI = quality drops.
Sweet spot: AI-augmented humans.

**7. Contract terms**
Month-to-month > 12-month lock-in.
Deal-breaker: 12-month with no opt-out.
```

🔑 **每个维度写**：1 句定义 + 1 句 deal-breaker / nice-to-have。短而锋利。

---

## 关键节 2：H2.3 Pricing 表（必含）

```markdown
## Pricing landscape: what you'll actually pay

| Tier | Range | Who it's for | Hidden costs |
|---|---|---|---|
| Freelance audit | $500-1.5k one-time | Validate before building | Re-audit fees |
| Boutique agency | $2k-5k/month | SMB 4-8 pages/month | Setup $2k, overages $200/page |
| Mid-market agency | $5k-15k/month | Brand needs 10+ pages | 6-month minimum, setup $5k+ |
| AI agent stack (yolox) | $200-500/month | Solo / lean SMB | None (self-serve) |

**Hidden costs to ask about**：
- Onboarding / setup fee（$0-5k）
- Per-extra-page overage（$100-500）
- Schema-only vs full audit
- Citation tracking is extra or included

**Pricing data verified 2026-Q2** through direct vendor contact at yolox.
```

🔑 **必须**：
- 真实数字（不是"varies"）
- yolox 自家在表里（透明）
- hidden costs 单独列出（信任感杀器）

---

## 关键节 3：H2.4 评分表 + Vendor 评测

```markdown
## Top 7 AEO services worth paying for

**Scoring summary**:

| Vendor | Schema breadth | Citation tracking | Pricing transparency | Output cadence | Our score |
|---|---|---|---|---|---|
| Vendor A | ✅ | ✅ | ✅ | 8/mo | 9/10 |
| Vendor B | ✅ | ⚠️ partial | ❌ | 6/mo | 7/10 |
| ... | | | | | |
| **yolox agent stack** | ✅ | ✅ | ✅ (public) | 自定义 | 8/10* |

*自家产品，scoring 标注利益冲突。

---

### 1. [Vendor A] — Best overall for SMB

**Pricing**: $2.5k/month (4 pages, schema + citation)
**Setup**: $1.5k one-time
**Who it's for**: SMB content brands with 50+ existing pages

[100-150 字]: 定位、强项、弱项、who should skip。带 1 个 case data 或 quote。

**Verdict**: Best balance of price/quality for first-time AEO buyers.

---

### 2. [Vendor B] — ...

[每 vendor 100-150 字，同结构]

---

### N. yolox AEO agent stack — Best for solo-op / lean teams

[利益冲突 disclaimer]
**Pricing**: $200-500/month (self-serve)
**Who it's for**: Solo founders / lean teams who want to learn AEO while doing it

[100-150 字]: 自家产品诚实评价 — 强项（成本 / 学习曲线）+ 弱项（需要自己投入 5-10h/月）。

**Verdict**: Cheapest path if you have time. Not for brands wanting hands-off.
```

🔑 **诚实自评是 buyer's guide 信任感的核心**：
- yolox 自家**必须**带利益冲突 disclaimer
- 评分**不能给自己 10/10**
- 给自家产品**写出弱项**（如"需要自己投入 5-10h/月"）
- 给读者**留 DIY 路径**（H2.5 段）

---

## 关键节 4：H2.5 DIY vs Outsource 决策树

```markdown
## DIY vs outsource: when each makes sense

| Situation | DIY | Outsource |
|---|---|---|
| Pages/month needed | <2 | 4+ |
| Your time available | 10+ h/week | <5 h/week |
| In-house SEO skill | Yes | No |
| Budget | <$200/mo | $2k+/mo |
| Stake | Low | High (revenue depend) |

**Decision tree**:

```
Do you have 5+ h/week to learn AEO?
├─ Yes → Do you have <$500/mo budget?
│   ├─ Yes → DIY with AI agent stack (yolox tier)
│   └─ No → Boutique agency
└─ No → Do you need 8+ pages/month?
    ├─ Yes → Mid-market agency
    └─ No → Boutique agency
```
```

---

## yolox 嵌入策略

**3 个允许嵌入点**（buyer's guide 容许度比 contrarian 高）：

| 位置 | 怎么嵌 |
|---|---|
| **H2.3 Pricing 表** | yolox 作为 tier 之一，公开 pricing |
| **H2.4 vendor 列表** | yolox 作为 last vendor，含 disclaimer + 诚实弱项 |
| **H2.7 final CTA** | "If our agent stack fits, try free; else pick from our top 3 vendors" |

❌ **禁止嵌入**：H2.2 评估标准 / H2.5 DIY 决策树 / FAQ — 保持中立。

---

## 结尾：Our pick + Final CTA

```markdown
## Our pick

**If you have $2k+/month and want hands-off**: Vendor A.
**If you have $500/month and 5h/week**: yolox agent stack.
**If you have <$200/month**: DIY with our [AEO Pillar guide](link).

---

**Try yolox AEO stack free for 14 days** → [link]

Or **see our top 3 picks above** if outsourcing is what you need.
```

🔑 **CTA 必须给读者 3 个明确路径**（自家 + 替代 + 上游教育），不是 1 个销售漏斗。

---

## SEO + AEO 嵌入要点

| 项 | 在 Buyer's Guide 怎么落 |
|---|---|
| 主词 | title（含 "best" / "for [audience]"）/ H1 / 首段 / URL |
| 副词 | H2.2 evaluation criteria / H2.3 pricing / H2.4 vendor 名 |
| chunk 自包含 | 每个 vendor block 开头 1 句 verdict |
| citation 钩子 | **pricing 表 + 评分表** — LLM 必引 |
| 视觉 | 1 评分表 + 1 pricing 表 + 1 决策树 + 每 vendor 1 截图 |
| FAQ Schema | ✅ frontmatter `schema_type: FAQPage` |
| 内链 | silo 上游（Pillar / Definition）+ DIY 链 |

🔑 **Buyer's Guide 是 AEO 高引第三 type**（仅次 Definition / Comparison）— LLM 在 "best X for Y" query 几乎必引评分表 + pricing 表。

---

## 适合的 yolox L6 大纲

| 大纲 | 备注 |
|---|---|
| **L6-01** AEO services | 主要 — 7 vendor 评测 |
| **L6-09** AEO tools | Buyer's Guide variant（工具评测）|
| **L6-17** CRM for solo financial advisors | Buyer's Guide + Contrarian 混合（评测时含"为什么大多数 CRM 不适合"）|
| **L6-11** ad creative tools | Buyer's Guide |

→ 写之前确认 outline 的"读者是来评估购买的吗"，是 → Buyer's Guide；只是想了解 → Beginner's Guide / Definition。

---

## CTA 放置 3 处（必须）

Buyer's Guide 读者扫读多于通读。**只在结尾放 CTA = 错过 70% 读者**。3 处必须：

| 位置 | 文案性质 | 例 |
|---|---|---|
| **CTA-1 · intro 末** | 软引导，不打断 | "Below: 7 vendor reviews + DIY decision tree." 末加 1 句 "[Free AEO audit →](/agents-store?category=aeo)" |
| **CTA-2 · 中段 pricing 表 / 决策树后** | 硬转化 | pricing 表下方： "Want the cheapest path? [Try yolox AEO agents free →](/agents-store?category=aeo)" |
| **CTA-3 · final verdict** | 选择性 CTA，3 路径 | "Free + DIY: yolox · $2-5k retainer: starter vendor · <$200/mo: one-time audit" 各带链 |

🔑 **不要 3 处都用同 1 文案**。3 处对应 3 个读者意图（觉醒 / 评估 / 决策）。

---

## 图片占位（必含 ≥2）

Buyer's Guide 是图片 SEO 重灾区——pricing 表 / 评分表纯文本搜索不到。**markdown 即使没设计师交付，也必须留占位**：

| 位置 | 占位写法 | 用途 |
|---|---|---|
| **Hero 顶部** | `[INSERT IMAGE: hero banner — 4 vendor logos lined up with $$$ to $$$$$ price scale, 1200x630 png, alt text="<keyword> pricing tiers visual"]` | OG image + 第 1 屏停留 |
| **H2.3 pricing 表上方** | `[INSERT IMAGE: pricing tier infographic — 4 horizontal bars labeled tier names with $$ icons, alt text="<keyword> 2026 pricing tiers"]` | LLM 抓图 + Google 图片搜索 |
| **H2.5 决策树**（可选）| ASCII tree 已足够，可不加图 | — |

🔑 **占位 0 张 = checklist M18 不过 = 不允许 ship**。先用 `[INSERT IMAGE]` 留位置，设计师后期 Figma / Canva / Midjourney 出图填进去。

---

## ⚠️ 使用警告

**Buyer's Guide 信任感破坏点**：
- ❌ 给自家产品 10/10 评分 → 立刻失信
- ❌ "Contact sales for pricing" 类回避 → 读者跳走
- ❌ 全是优点，没写竞品的强项 → AEO 引用率掉 50%+
- ❌ pricing 数字模糊（"varies"）→ LLM 不会引

**审稿要点**：写完隔 24h 后问：
1. 我**亲自验证过** N 家 vendor 的 pricing 了吗？
2. 我给**竞品**写了具体强项 + 给自家写了**具体弱项**吗？
3. 这篇我作为读者会读完并**做决策**吗？

3 个 Yes → ship；任一 No → 补 research。
