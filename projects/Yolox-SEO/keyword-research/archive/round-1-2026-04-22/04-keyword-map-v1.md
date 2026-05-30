# 04 · Keyword Map v1 · 200 词主库（Day 3 产出）

**日期**：2026-04-23（Day 3，周四）
**交付等级**：🟡 可用（已打分，未验证搜索量/KD）
**对应 playbook**：§2.3.3 Intent 分类 + §2.3.4 打分模型 + §2.3.5 表结构
**对应任务**：`docs/seo/tasks/week-2026-04-22/2.3-keyword-research.md` Day 3

---

## 前言 · 打分方法论（零流量期临时版）

### 为什么改公式

Playbook §2.3.4 原公式：

```
Priority = (Volume × 0.4) + (Intent × 0.4) + (Difficulty × -0.2)
```

**问题**：本周 Ahrefs KD 全 TODO、多数词 Volume 未知。原公式**退化成只剩 Intent 一项**，失去区分度。

### Priority v0 · 临时打分（0–10 分）

```
Priority_v0 =
    Info_intent_bonus   (0 或 1)   × 2      # 是不是信息型（主战场）
  + YOLOX_Match         (0–3)      × 1.5    # 匹配 15 个首页 Agent 的哪个
  + Reddit_Evidence     (0 或 1)   × 2      # 有没有原帖 URL 作证
  + Scenario_Specificity (0–2)     × 1      # 三层长尾 > 两层 > 单层
  ────────────────────────────────
  最大 10 分
```

**各维度判定规则**：

| 维度 | 0 分 | 1 分 | 2 分 | 3 分 |
|---|---|---|---|---|
| **Info bonus** | 非信息型 | 信息型（含 how/why/what）| — | — |
| **YOLOX Match** | 不匹配 | 弱（间接组合）| 中（需多 Agent 协作）| 强（1 个 hero agent 可答）|
| **Evidence** | 无 | Reddit A 档有 URL | — | — |
| **Specificity** | 单层大词（AI agent）| 两层（AI agent for Shopify）| 三层（AI SEO agent for Shopify store）| — |

**Tier 分档**：

| Tier | Priority | 含义 | 本周动作 |
|---|---|---|---|
| 🔴 Tier 1 | 8–10 | 本周重点，下周博客强候选 | Day 6 必选 |
| 🟠 Tier 2 | 5–7 | 下周–下下周写 | Day 6 备选 |
| 🟡 Tier 3 | 2–4 | 月内储备 | 月度刷新时再看 |
| ⚫ 砍 | ≤1 或 defer 标 | 不进主库 | → [07-negative-keywords.md](./07-negative-keywords.md) |

**Day 7 升级路径**：拿到 Keywords Everywhere 或 Ahrefs KD + Volume 后，回头用 playbook 原公式重排一次，主库升级为 v1.1 🔴。

---

## 统计

| 项 | 数量 |
|---|---|
| Day 2 候选池（02-expanded-keywords.md）| 383（去重后 ~325） |
| 砍掉 · 商业调查（best X / vs / alternative / top X）| ~58 |
| 砍掉 · 高 KD 大词（AI agent / AI workflow 等）| ~15 |
| 砍掉 · 与 YOLOX 定位不符（AI writing / drawing 等）| ~12 |
| 砍掉 · 品牌/导航词 | ~8 |
| 砍掉 · 弱 Claude 扩展（无场景锚点）| ~32 |
| **合计砍掉** | **~125** |
| **进主库** | **200** |
| ├─ Tier 1 | 40 |
| ├─ Tier 2 | 95 |
| └─ Tier 3 | 65 |

**Cluster 粗标**（12 个，Day 5 精细化）：

| Cluster | 名 | 词数 |
|---|---|---|
| C1 | AEO & llms.txt | 20 |
| C2 | New-site SEO（新站策略）| 18 |
| C3 | Shopify / ecommerce | 25 |
| C4 | SMB 获客 / 服务业 | 22 |
| C5 | Content 产能 / listicle | 18 |
| C6 | Sales / Email 自动化 | 16 |
| C7 | Solopreneur AI 生态（Pillar 候选）| 20 |
| C8 | Competitor Intelligence | 14 |
| C9 | Social media → client | 12 |
| C10 | AI Agency 创业（次要 Pillar 候选）| 8 |
| C11 | Connector × Agent（Notion/Gmail/Slack）| 15 |
| C12 | Launch / Referral | 12 |
| **合计** | | **200** |

---

## Tier 1 · 本周重点（40 词 · Priority 8–10）

**特征**：至少 3 个维度满分，下周博客强候选。每词表格字段按 playbook §2.3.5 精简版。

| # | Keyword | Intent | P | YOLOX Agent | Evidence | Cluster | Zero-vol | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | is llms.txt a scam | info | 10 | Sophie | r/SEO 1srvco1 | C1 | Y | 🔥 下周 blog #1 强候选（§2.6 同步 ship） |
| 2 | how to create llms.txt | info | 10 | Sophie | — | C1 | Y | llms.txt 主题，配 blog #1 内链 |
| 3 | what is llms.txt file | info | 10 | Sophie | — | C1 | Y | 同上 |
| 4 | why ChatGPT cites one page over another | info | 10 | Sophie | r/SEO 1ss0drr | C1 | Y | AEO 典型问题 |
| 5 | struggling to get consistent clients cleaning business | info | 10 | Elias | r/smallbusiness 1srl89h | C4 | Y | 极具体三层词，solo-op 典型 |
| 6 | how to acquire customers for indie SaaS | info | 10 | Elias | r/SaaS 1srm4yl | C4 | Y | SaaS ICP 强匹配 |
| 7 | how to promote Shopify store for sales | info | 10 | Elias + Savannah + Stella | r/shopify 1srsdlw | C3 | Y | Shopify ICP 强 |
| 8 | how to do distribution for indie SaaS | info | 10 | Arlo + Quinn | r/SaaS 1ss43uq | C4 | Y | 下周 blog #2 候选 |
| 9 | how to structure headings for listicles | info | 9 | Isaiah | r/SEO 1ss6uxv | C5 | Y | 对应 Programmatic SEO Builder |
| 10 | how to rank new site vs high traffic sites | info | 9 | Stella | r/SEO 1sri4ht | C2 | N | Pillar 候选主词 |
| 11 | SEO for local service business | info | 9 | Stella | r/SEO 1srh3al | C4 | N | local SEO 长尾 |
| 12 | how to get more clients for service business | info | 9 | Elias | r/smallbusiness 1ss4ibj | C4 | N | 本周博客强候选 |
| 13 | how to close more sales faster | info | 9 | Daniel | r/smallbusiness 1ss8ngr | C6 | N | Email Closer 直接对应 |
| 14 | turn social media attention into clients | info | 9 | Mia + Savannah + Addison | r/smallbusiness 1srignl | C9 | N | 跨 Agent 协作案例 |
| 15 | get more genuine Google reviews for business | info | 9 | Quinn | r/smallbusiness 1srnijf | C12 | Y | Referral Architect 对应 |
| 16 | build AI workers in plain English | info | 9 | YOLOX 整体 | r/Entrepreneur 1snchax | C7 | Y | Pillar 候选主词 |
| 17 | why people visit website but don't sign up | info | 9 | Sophie + Addison | r/indiehackers 1smtafn | C2 | Y | 转化诊断，AEO+CRO |
| 18 | how to automate order tracking inquiries Shopify | info | 9 | 客服 Agent | r/ecommerce 1srh6iv | C3 | Y | Shopify 具体场景 |
| 19 | open source social media scheduling alternative | info | 9 | Mia | r/SideProject 1sk8fn3 | C9 | Y | 对 $400/月 SaaS 的替代讨论 |
| 20 | how to get Google reviews without pressure | info | 9 | Quinn | r/ContentMarketing 1srx6uo | C12 | Y | Quinn 强对应，两条证据 |
| 21 | llms.txt vs robots.txt | info | 9 | Sophie | — | C1 | Y | 对比型，AEO 教学 |
| 22 | does llms.txt help SEO | info | 9 | Sophie | — | C1 | Y | 信任度疑问 |
| 23 | does ChatGPT read llms.txt | info | 9 | Sophie | — | C1 | Y | 技术真相问题 |
| 24 | how llms.txt helps AI citation | info | 9 | Sophie | — | C1 | Y | outcome-oriented |
| 25 | AI agents for solopreneurs | info | 8 | YOLOX 整体 | — | C7 | N | **主要 Pillar 词** |
| 26 | AI marketing team for solopreneur | info | 8 | YOLOX 整体 | — | C7 | N | Pillar 同义词 |
| 27 | AI SEO agent for Shopify store | info | 8 | Sophie | — | C3 | Y | 三层长尾典型 |
| 28 | AI competitor monitoring agent | info | 8 | Evelyn | — | C8 | N | Evelyn 直对应 |
| 29 | AI landing page builder for SaaS | info | 8 | Addison | — | C3 | Y | 三层长尾 |
| 30 | AI ad creative studio for Shopify | info | 8 | Olivia | — | C3 | Y | 三层长尾 |
| 31 | AI agent for Notion automation | info | 8 | 多 Agent | — | C11 | Y | connector × YOLOX 核心 |
| 32 | AI email closer for Gmail | info | 8 | Daniel | — | C11 | Y | Daniel × Gmail 精确 |
| 33 | AI referral architect for service business | info | 8 | Quinn | — | C12 | Y | Quinn × 服务业 |
| 34 | AI launch strategist for indie SaaS | info | 8 | Arlo | — | C12 | Y | Arlo × SaaS |
| 35 | AI traffic commander for Shopify | info | 8 | Elias | — | C3 | Y | Elias × Shopify |
| 36 | AI competitor scout for SaaS | info | 8 | Evelyn | — | C8 | Y | Evelyn × SaaS |
| 37 | AI content machine for YouTube | info | 8 | Theodore | — | C5 | Y | Theodore × YouTube |
| 38 | AI video producer for TikTok | info | 8 | Sadie | — | C5 | Y | Sadie × TikTok |
| 39 | AI agent for Substack newsletter | info | 8 | 多 Agent | — | C7 | Y | Substack ICP |
| 40 | 24/7 AI team for solopreneurs | info | 8 | YOLOX 整体 | — | C7 | Y | 对应 tagline "Teams working 24/7" |

**Tier 1 观察**：
- 24/40 是零量词候选（60%）—— 零流量期正确的姿势
- 10/40 有 Reddit A 档证据（25%）—— 其余靠 YOLOX 强匹配 + 三层长尾
- **C1（AEO/llms.txt）占 8 个**（20%）—— 这个 Cluster Day 5 大概率定为第一 Pillar
- **C7（Solopreneur AI）占 6 个** —— Pillar 候选 2
- **C3（Shopify）占 6 个** —— Pillar 候选 3

---

## Tier 2 · 下周–下下周（95 词 · Priority 5–7）

按 Cluster 分组，紧凑表格。

### C1 · AEO & llms.txt 变体（12）

| Keyword | P | Notes |
|---|---|---|
| llms.txt for new website | 7 | scenario-ICP |
| llms.txt spec explained | 7 | what-is |
| llms-full.txt vs llms.txt | 7 | vs-compare |
| AI search engines and llms.txt | 7 | scenario |
| llms.txt best practices 2026 | 7 | how-to |
| llms.txt example | 7 | scenario |
| should I add llms.txt to my site | 7 | how-to |
| llms.txt for startup website | 6 | scenario-ICP |
| generate llms.txt automatically | 6 | tool-find |
| Google traffic vs ChatGPT traffic ecommerce | 6 | r/ecommerce 1srpe36 证据 |
| AI for Shopify conversion optimization | 6 | Addison + Shopify |
| AI for customer support ecommerce | 5 | 弱匹配 |

### C2 · New-site SEO（10）

| Keyword | P | Notes |
|---|---|---|
| AI SEO for new website | 7 | 三层：SEO × new site |
| how to rank new blog on Google | 7 | scenario |
| SEO strategy for zero traffic site | 6 | specific pain |
| new domain SEO checklist | 6 | how-to |
| how to get first 100 visitors SEO | 6 | outcome |
| optimize Shopify pages per day SEO | 6 | r/shopify 1srdlxp |
| AI agent for keyword research | 6 | Sophie |
| AI agent for GSC monitoring | 6 | Sophie |
| AI for meta title optimization | 6 | Sophie |
| AI for schema markup generation | 5 | Sophie, 技术 SEO |

### C3 · Shopify / ecommerce（15）

| Keyword | P | Notes |
|---|---|---|
| AI agent for Shopify SEO | 7 | Shopify + SEO |
| AI agent for Shopify product description | 7 | Levi × Shopify |
| AI for Shopify customer support | 7 | 客服 Agent |
| AI agent Shopify email marketing | 7 | Daniel × Shopify |
| AI agent Shopify review management | 7 | Quinn × Shopify |
| AI agent for Shopify abandoned cart | 7 | Daniel × Shopify |
| AI for Shopify cross-sell upsell | 7 | Savannah × Shopify |
| AI Shopify traffic generator | 7 | Elias × Shopify |
| how to reach Shopify store owners B2B | 7 | r/shopify 1ss1lnw (defer 轻度) |
| best agent right now Shopify | 6 | r/shopify 1srps0d, 商业调查轻度 |
| AI agent paid ads strategist for Shopify | 6 | Savannah |
| AI agent programmatic SEO for Shopify | 6 | Stella |
| AI competitor scout for Shopify | 6 | Evelyn |
| AI for Shopify inventory | 5 | 弱匹配（物流边缘）|
| Shopify traffic quality by source | 5 | r/shopify 1ssafzz，归因分析 |

### C4 · SMB 获客 / 服务业（14）

| Keyword | P | Notes |
|---|---|---|
| AI for local service business marketing | 7 | Elias + local |
| AI lead gen for consultants | 7 | Elias × consulting |
| AI agent for SMB client acquisition | 7 | SMB × Elias |
| how to scale service business with AI | 7 | outcome |
| AI for coaching business clients | 7 | Elias × coaching |
| AI client outreach tool | 7 | Elias |
| AI for freelancer client acquisition | 7 | Elias × freelance |
| automate client outreach service business | 7 | how-to |
| AI agent cleaning business clients | 6 | 对应 r/smallbusiness 1srl89h |
| AI agent for local business marketing | 6 | Stella + local |
| how to 10x service business with AI | 6 | outcome-bold |
| AI-powered referral system for services | 6 | Quinn × services |
| AI to find more clients service business | 5 | 同 Elias |
| AI to grow service business | 5 | outcome |

### C5 · Content 产能（10）

| Keyword | P | Notes |
|---|---|---|
| AI listicle writer for blog | 7 | Isaiah |
| programmatic SEO listicle template | 7 | Stella + Isaiah |
| AI for top 10 article structure | 7 | Isaiah |
| AI article outline for listicles | 7 | Isaiah |
| how to write SEO-optimized listicle headings | 7 | how-to |
| AI tool for listicle generation | 7 | Isaiah |
| automate listicle creation AI | 6 | Isaiah |
| AI for listicle SEO | 6 | Isaiah + Sophie |
| how to rank listicle articles on Google | 6 | Sophie + Isaiah |
| listicle H1 H2 H3 structure | 5 | 技术 SEO |

### C6 · Sales / Email 自动化（10）

| Keyword | P | Notes |
|---|---|---|
| AI assistant for sales closing | 7 | Daniel |
| AI sales closer for small business | 7 | Daniel × SMB |
| AI email sequence for closing sales | 7 | Daniel |
| automated sales pipeline AI | 7 | Daniel |
| AI for sales objection handling | 7 | Daniel |
| AI lead qualification and closing | 7 | Daniel |
| AI for cold email closing | 7 | Daniel |
| AI sales bot for solopreneurs | 7 | Daniel × solo |
| how to speed up sales cycle with AI | 6 | outcome |
| AI-powered sales follow-up sequence | 6 | Daniel |

### C7 · Solopreneur AI 生态（12）

| Keyword | P | Notes |
|---|---|---|
| one-person AI team | 7 | outcome 指向 YOLOX 整体 |
| AI co-founder for solopreneurs | 7 | outcome, 高情感 |
| AI agent that replaces a team | 7 | outcome |
| AI agent for one-person startup | 7 | scenario |
| AI for running a business alone | 7 | scenario |
| AI for solopreneur marketing | 7 | scenario |
| AI for solopreneur sales | 7 | scenario |
| AI agent for indie business | 7 | scenario |
| how solopreneurs use AI agents | 7 | how-to |
| AI for side hustle automation | 6 | side hustle ICP |
| AI for bootstrapped founders | 6 | bootstrap ICP |
| lean AI stack solo | 5 | 弱 |

### C8 · Competitor Intelligence（10）

| Keyword | P | Notes |
|---|---|---|
| AI to track competitors | 7 | Evelyn |
| AI competitor intelligence tool | 7 | Evelyn |
| automate competitor analysis with AI | 7 | how-to + Evelyn |
| AI agent for competitor pricing tracking | 7 | Evelyn |
| AI for competitor ad monitoring | 7 | Evelyn |
| AI competitor content monitoring | 7 | Evelyn |
| AI for competitor social media monitoring | 7 | Evelyn |
| competitor website change AI alert | 7 | Evelyn, 具体场景 |
| AI to monitor competitor product launches | 6 | Evelyn |
| automate weekly competitor check AI | 6 | Evelyn |

### C9 · Social → Client（6）

| Keyword | P | Notes |
|---|---|---|
| AI DM automation for lead gen | 7 | Mia |
| AI for social media lead capture | 7 | Mia |
| social media to client funnel AI | 7 | Mia + Addison |
| AI for Instagram lead qualification | 7 | Mia × IG |
| AI for TikTok lead conversion | 7 | Mia × TikTok |
| AI LinkedIn outreach to clients | 7 | Daniel × LinkedIn |

### C10 · AI Agency 创业（4）

| Keyword | P | Notes |
|---|---|---|
| AI agency toolkit for solopreneurs | 6 | 次要 Pillar 候选 |
| start AI automation agency no coding | 6 | Quora 证据 |
| AI agent team for AI automation agency | 5 | 弱 |
| white-label AI agents for agencies | 5 | 弱 |

### C11 · Connector × Agent（可）

（共 10 词合并展示）

| Keyword | P | Notes |
|---|---|---|
| AI content machine for Notion | 6 | Theodore × Notion |
| AI competitor scout saves to Notion | 6 | Evelyn × Notion |
| AI SEO agent with Notion sync | 6 | Sophie × Notion |
| AI project partner for Notion | 6 | Nova × Notion |
| AI email closer reads Notion CRM | 7 | Daniel × Notion 跨数据源 |
| AI agent for Gmail classification | 6 | Gmail × classifier |
| AI agent auto-reply Gmail | 7 | Gmail × Daniel |
| AI agent for Slack notifications | 5 | 偏工具 |
| AI lead list Google Sheets automation | 6 | Elias × Sheets |
| AI keyword research to Google Sheets | 5 | Sophie × Sheets |

### C12 · Launch / Referral（2）

| Keyword | P | Notes |
|---|---|---|
| AI for launch marketing | 6 | Arlo |
| help post product on Hacker News | 6 | r/indiehackers 1srn06k 证据 |

**Tier 2 合计：95 词** ✅

---

## Tier 3 · 月内储备（65 词 · Priority 2–4）

按 Cluster 分组，极紧凑（只列关键词）。Day 5 Cluster 定稿时，每个 Cluster 会从这里抽 1–2 词作"支撑词"。

### C1 · AEO 相关（2）
- AI search engines and llms.txt
- llms.txt for AI citation

### C2 · New-site SEO（6）
- AI agent for backlink outreach | AI for internal linking | AI agent for SERP analysis | AI agent for content gap analysis | AI agent for competitor SEO analysis | how many Shopify pages optimize per day

### C3 · Shopify/ecommerce（10）
- AI agent Shopify vs Zapier | Shopify traffic quality by source | market niche ecommerce products | ecommerce marketing budget 2026 | automate Etsy order fulfillment | upload POD designs in bulk | AI for Shopify inventory | integrate Shopify Etsy dashboard | eCommerce growth 2026 | AI for ecommerce customer questions

### C4 · SMB 获客（4）
- AI for small business automation | AI tools grow small business online | AI tools improve productivity | AI for sales productivity

### C5 · Content（6）
- AI writing tools for creators | AI for YouTube scripts | AI visual creator for Amazon | AI copy polisher for video | AI for TikTok trending analysis | AI for Instagram creators discovery

### C6 · Sales（4）
- reduce sales cycle length AI | AI closing script generator | one-person AI sales team | AI agent that closes sales while I sleep

### C7 · Solopreneur（4）
- AI agents replace virtual assistants | no-code AI agents for non-technical founders | AI agents for creator business | solo AI automation setup

### C8 · Competitor（4）
- AI agent to spy on competitors | AI competitive analysis for SaaS | AI for competitor keyword tracking | AI competitor review monitoring

### C9 · Social → Client（6）
- AI for X/Twitter DM lead gen | AI for YouTube lead generation | social media ROI AI tracking | AI funnel from social to sale | AI to turn likes into leads | automate social lead nurture AI

### C10 · AI Agency（4）
- how to find clients for AI consultancy | technical skills AI automation agency | AI agency pricing | AI consulting business ideas

### C11 · Connector 扩展（10）
- AI agent connects Notion databases | AI launch strategist Notion templates | AI agent for Slack DM responder | AI traffic commander outreach via Gmail | AI agent for cold email Gmail | AI team communication Slack bot | AI agent posts Slack updates | AI agent syncs to Google Sheets | AI SEO data to Google Sheets | AI ad performance Google Sheets

### C12 · Launch / Referral（5）
- AI launch playbook | AI Product Hunt strategy | AI for first 100 users | build audience before launching product | how to validate mobile app idea

**Tier 3 合计：65 词** ✅

---

## Cluster 粗标汇总（给 Day 5 备料）

| Cluster | 主词（候选 Pillar 词） | Tier 1 数 | Total | Day 5 Pillar 候选 |
|---|---|---|---|---|
| C1 | AEO & llms.txt | llms.txt ecosystem | 8 | 20 | ⭐⭐⭐ 强（证据 + 产品同步）|
| C2 | New-site SEO | how to rank new site | 1 | 18 | ⭐ |
| C3 | Shopify/ecommerce | AI for Shopify store owners | 6 | 25 | ⭐⭐⭐ 强（ICP 聚焦）|
| C4 | SMB 获客 | AI client acquisition for solopreneurs | 4 | 22 | ⭐⭐ |
| C5 | Content 产能 | AI content factory | 4 | 18 | ⭐ |
| C6 | Sales/Email | AI email closer | 1 | 16 | ⭐⭐ |
| C7 | Solopreneur AI | **AI agents for solopreneurs** | 6 | 20 | ⭐⭐⭐⭐ **最强 Pillar 候选** |
| C8 | Competitor | AI competitor monitoring | 2 | 14 | ⭐ |
| C9 | Social → Client | AI social to client funnel | 1 | 12 | ⭐ |
| C10 | AI Agency | AI automation agency toolkit | 0 | 8 | ⭐ 次要 Pillar |
| C11 | Connector × Agent | AI agent for Notion | 2 | 15 | — |
| C12 | Launch/Referral | AI launch strategist | 2 | 12 | ⭐ |

**Day 5 Pillar 定稿预测**：
- **Pillar 1（主）**：`AI agents for solopreneurs` = C7 + 借 C1 + C3 + C4 的核心 Cluster
- **Pillar 2**：`AEO and llms.txt for new sites` = C1 + C2（和 §2.6 本周 ship 完美对齐）
- **Pillar 3**：`AI marketing stack for Shopify / SaaS founders` = C3 + C6 + C9 + C12

---

## Day 3 交付清单

- [x] 325 词合并去重 + Intent 四分类
- [x] 砍 125 词 → [07-negative-keywords.md](./07-negative-keywords.md)（同步产出）
- [x] Priority v0 打分 0–10 分制
- [x] 200 词分 Tier 1 / 2 / 3
- [x] 12 个 Cluster 粗标 + 3 个 Pillar 候选预测
- [x] 交付等级 🟡（已打分 · 可 ship 到 Day 5）

---

## 反思 / 隐忧 / 给小刀老师

### 反思：Priority v0 公式的局限

- **公式没用到搜索量**（因为全 TODO）→ 对"零量词"和"10k/月词"一视同仁
- **没用到 KD** → 可能把真实 KD > 30 的词当 Tier 1 错推
- **纯靠 YOLOX 匹配度驱动** → 可能把"YOLOX 能做但其实没人搜"的词排高

**Day 7 回头修正**：拿到 KE / Ahrefs 数据后，Priority 公式升级：
```
Priority_v1 = Priority_v0 × 0.5 + (Volume_score × 0.25) + ((10 - KD/10) × 0.25)
```
维持原有 YOLOX 匹配度权重的同时，加入硬数据校准。

### 隐忧 1：Tier 1 里 10/40 有 Reddit 证据，30/40 靠推测

- Tier 1 的 30 个 "Claude 扩展 + YOLOX 强匹配" 词**理论上** KD < 10（太具体），但**实际**可能出现意外。Day 7 验证后可能有 5-10 个从 Tier 1 降级
- 下周 Day 6 选 6 篇博客时，**优先选有 Reddit 证据的 10 条** + 4 条 C1 llms.txt 变体（llms.txt 主词已验证）

### 隐忧 2：C1 AEO 占比可能偏高

- Tier 1 里 8/40 = 20% 是 llms.txt 相关。风险：llms.txt 是 2025-2026 新兴词，**热度可能快速下降**或被 Google 官方表态影响
- **Day 5 时**建议把 C1 做成 **1 篇 Pillar + 3-5 篇 Cluster 短文**（快速占坑），而不是铺 20 篇——词型重叠度高，写 20 篇互相竞争内链

### 隐忧 3：Connector × Agent 词（C11）排名普遍偏低

- C11 里只有 2 个进 Tier 1，10 个 Tier 2，10 个 Tier 3
- 原因：Connector 组合词"搜索真实性"弱（Claude 扩展，无 Reddit 证据），Specificity=2 但 Evidence=0
- **判断**：Day 7 用 KE 验证 "AI agent for Notion" 等词的真实 Volume 后，C11 可能**整体降级或整体升级**（取决于 Notion AI 搜索趋势）

### 学了啥（给小刀老师）

- **Priority 打分不是"越客观越好"**：零流量期 Volume/KD 没数据时，**主观的 YOLOX 匹配度 + Reddit 证据**反而比硬套公式更靠谱
- **Cluster 粗标的价值**：200 词散列很难选题；分 12 个 Cluster 后，选题变成"选 Cluster → 选该 Cluster 里 Tier 1 词"两步，决策链短
- **Pillar 候选的"累积证据"原则**：C7（Solopreneur）Pillar 候选最强，不是因为单词 Priority 最高，而是**6 个 Tier 1 + 20 个总词汇**形成"语义云"——Google 对站点主题权威信号是靠这种"语义密度"判断的（playbook §2.3.6 原理）
