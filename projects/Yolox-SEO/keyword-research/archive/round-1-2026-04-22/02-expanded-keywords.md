# 02 · 候选词池 300+（Day 2 产出）

**日期**：2026-04-23（Day 2）
**交付等级**：🟢 候选池（未去重、未打分、未分类 intent）
**对应 playbook**：§2.3.2 扩展方法论
**对应任务**：`docs/seo/tasks/week-2026-04-22/2.3-keyword-research.md` Day 2 任务 2.1 + 2.3

---

## 统计

| 来源 | 词数 | 方法 |
|---|---|---|
| Day 1 种子词（01-seed-keywords.md）| 70 | 4 源采集 |
| Claude 10 核心词语义扩展 | 173 | 每词 15–20 个同义/近义/场景变体 |
| ICP × Agent 角色交叉矩阵 | 60 | 精选组合（不硬凑）|
| Connector × Agent 角色交叉 | 40 | 精选组合 |
| Reddit/Quora 问句主干提取 | 40 | 从 03-reddit-quora-questions.md 去重后 |
| **合并去重后估计** | **~320** | 目标 300+ ✅ |

**降级说明**：
- AnswerThePublic 免费版：WebFetch 拿不到数据（SPA + 登录墙），**降级由 Claude 语义扩展代替**
- AlsoAsked 免费版：同上降级
- 下周 Day 8+ 小刀老师手动跑一次 AnswerThePublic 付费试用（1–2 天免费）查漏

---

## 1. Day 1 种子词（70，回顾）

完整清单见 [`01-seed-keywords.md`](./01-seed-keywords.md)。按来源分：
- 源 1 产品语义（20）：品类词 5 + ICP 场景 10 + Agent 角色 5
- 源 2 Reddit 真实（15）：带原 URL 证据
- 源 3 竞品反查（17）：Lindy/Relevance AI/Zapier/n8n
- 源 4 品类相邻（18）：自动化/AI Agent/Solo/内容营销

---

## 2. Claude 10 核心词 × 语义扩展（173 词）

**扩展原则**：
- 不是简单同义词替换（避免 AI agent → AI bot 这种表层）
- 覆盖 5 个 intent 变体：how-to / tool-find / scenario-specific / outcome-based / vs-compare
- 每词保留原词"场景指向"，不漂到 YOLOX 不支持的领域

---

### 2.1 核心词 #1 · `how to close more sales faster`（20 变体）

映射 Daniel · Email Closer。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | how to close sales faster with AI | how-to |
| 2 | AI tool to close deals faster | tool-find |
| 3 | AI assistant for sales closing | tool-find |
| 4 | automate sales follow-up with AI | how-to |
| 5 | AI email sequence for closing sales | scenario |
| 6 | AI for sales objection handling | scenario |
| 7 | close more deals with AI agent | how-to |
| 8 | AI sales closer for small business | scenario-ICP |
| 9 | how to speed up sales cycle with AI | how-to |
| 10 | AI agent for sales follow-up | tool-find |
| 11 | reduce sales cycle length with AI | outcome |
| 12 | AI lead qualification and closing | scenario |
| 13 | AI for cold email closing | scenario |
| 14 | automated sales pipeline AI | scenario |
| 15 | AI agent that closes sales while I sleep | outcome（对应 YOLOX "24/7" tagline） |
| 16 | AI sales bot for solopreneurs | scenario-ICP |
| 17 | AI closing script generator | scenario |
| 18 | how to automate deal closing | how-to |
| 19 | AI-powered sales follow-up sequence | scenario |
| 20 | one-person AI sales team | scenario-ICP |

---

### 2.2 核心词 #2 · `how to structure headings for listicles`（15 变体）

映射 Isaiah · SEO Content Factory + Stella · Programmatic SEO Builder。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | how to write SEO-optimized listicle headings | how-to |
| 2 | AI for listicle SEO | tool-find |
| 3 | listicle structure best practices | how-to |
| 4 | how many H2 should a listicle have | how-to |
| 5 | AI tool for listicle generation | tool-find |
| 6 | programmatic SEO listicle template | scenario |
| 7 | AI listicle writer for blog | tool-find |
| 8 | how to structure "best X for Y" article | how-to |
| 9 | listicle heading format for SERP | scenario |
| 10 | AI for top 10 article structure | scenario |
| 11 | best AI tool to write listicles | tool-find（defer 商业调查）|
| 12 | listicle H1 H2 H3 structure | how-to |
| 13 | automate listicle creation AI | how-to |
| 14 | how to rank listicle articles on Google | how-to |
| 15 | AI article outline for listicles | tool-find |

---

### 2.3 核心词 #3 · `is llms.txt a scam`（15 变体）

映射 Sophie · SEO Doctor（AEO）。**高价值 —— YOLOX §2.6 本周正在 ship /llms.txt，博客可作为产品发布伴随内容**。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | what is llms.txt file | what-is |
| 2 | llms.txt vs robots.txt | vs-compare |
| 3 | how to create llms.txt | how-to |
| 4 | llms.txt for new website | scenario |
| 5 | does llms.txt help SEO | how-to |
| 6 | llms.txt spec explained | what-is |
| 7 | llms-full.txt vs llms.txt | vs-compare |
| 8 | AI search engines and llms.txt | scenario |
| 9 | llms.txt best practices 2026 | how-to |
| 10 | does ChatGPT read llms.txt | what-is |
| 11 | llms.txt example | scenario |
| 12 | should I add llms.txt to my site | how-to |
| 13 | llms.txt for startup website | scenario-ICP |
| 14 | how llms.txt helps AI citation | outcome |
| 15 | generate llms.txt automatically | tool-find |

---

### 2.4 核心词 #4 · `AI agents for solopreneurs`（20 变体）

**最可能的 Pillar 词**。映射 YOLOX 整体定位。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | best AI agents for solo founders | tool-find（defer 商业调查）|
| 2 | AI marketing agent for solo entrepreneur | scenario-ICP |
| 3 | one-person AI team | scenario |
| 4 | AI agent that replaces a team | outcome |
| 5 | AI co-founder for solopreneurs | scenario |
| 6 | how solopreneurs use AI agents | how-to |
| 7 | AI stack for solo business | scenario |
| 8 | 24/7 AI team for solopreneurs | outcome |
| 9 | AI for running a business alone | scenario |
| 10 | solo AI automation setup | how-to |
| 11 | AI agent for one-person startup | scenario |
| 12 | AI agents replace virtual assistants | vs-compare |
| 13 | AI for solopreneur marketing | scenario |
| 14 | AI for solopreneur sales | scenario |
| 15 | AI agent for indie business | scenario |
| 16 | AI for side hustle automation | scenario-ICP |
| 17 | no-code AI agents for non-technical founders | scenario-ICP |
| 18 | AI agents for creator business | scenario-ICP |
| 19 | AI for bootstrapped founders | scenario-ICP |
| 20 | lean AI stack solo | scenario |

---

### 2.5 核心词 #5 · `AI SEO agent`（18 变体）

映射 Sophie · SEO Doctor + Isaiah · SEO Content Factory + Stella · Programmatic SEO Builder。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | AI SEO automation tool | tool-find |
| 2 | AI agent for SEO optimization | tool-find |
| 3 | automate on-page SEO with AI | how-to |
| 4 | AI agent for keyword research | scenario |
| 5 | AI for technical SEO audit | scenario |
| 6 | AI SEO content writer agent | scenario |
| 7 | AI agent for backlink outreach | scenario |
| 8 | AI for meta title optimization | scenario |
| 9 | AI SEO for new website | scenario-ICP |
| 10 | AI agent for competitor SEO analysis | scenario |
| 11 | AI agent for GSC monitoring | scenario |
| 12 | AI for internal linking | scenario |
| 13 | AI agent for SERP analysis | scenario |
| 14 | AI SEO for Shopify store | scenario-ICP |
| 15 | AI SEO for SaaS blog | scenario-ICP |
| 16 | AI SEO for local business | scenario-ICP |
| 17 | AI agent for content gap analysis | scenario |
| 18 | AI for schema markup generation | scenario |

---

### 2.6 核心词 #6 · `AI competitor monitoring agent`（15 变体）

映射 Evelyn · Competitor Scout。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | AI to track competitors | scenario |
| 2 | AI competitor intelligence tool | tool-find |
| 3 | automate competitor analysis with AI | how-to |
| 4 | AI agent for competitor pricing tracking | scenario |
| 5 | AI for competitor ad monitoring | scenario |
| 6 | AI competitor content monitoring | scenario |
| 7 | AI agent to spy on competitors | scenario |
| 8 | competitor website change AI alert | scenario |
| 9 | AI for competitor social media monitoring | scenario |
| 10 | AI agent for competitor SEO tracking | scenario |
| 11 | AI competitive analysis for SaaS | scenario-ICP |
| 12 | AI to monitor competitor product launches | scenario |
| 13 | AI competitor review monitoring | scenario |
| 14 | automate weekly competitor check AI | how-to |
| 15 | AI for competitor keyword tracking | scenario |

---

### 2.7 核心词 #7 · `AI agent for Shopify store`（15 变体）

映射多 Agent（Sophie/Elias/Savannah/Addison/Olivia 等）。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | AI agent for Shopify SEO | scenario |
| 2 | AI agent for Shopify product description | scenario |
| 3 | AI for Shopify customer support | scenario |
| 4 | AI agent Shopify ads | scenario |
| 5 | AI for Shopify conversion optimization | scenario |
| 6 | AI agent Shopify email marketing | scenario |
| 7 | automate Shopify store with AI agent | how-to |
| 8 | AI agent for Shopify inventory | scenario（间接）|
| 9 | AI for Shopify order tracking | scenario |
| 10 | AI agent Shopify review management | scenario |
| 11 | AI Shopify traffic generator | scenario |
| 12 | best AI agent for Shopify store | tool-find（defer）|
| 13 | AI agent Shopify vs Zapier | vs-compare |
| 14 | AI agent for Shopify abandoned cart | scenario |
| 15 | AI for Shopify cross-sell upsell | scenario |

---

### 2.8 核心词 #8 · `how to get more clients for service business`（15 变体）

映射 Elias · Traffic Commander + Daniel · Email Closer。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | AI to find more clients service business | scenario |
| 2 | AI for service business lead generation | scenario |
| 3 | automate client outreach service business | how-to |
| 4 | AI agent for SMB client acquisition | scenario |
| 5 | how to scale service business with AI | how-to |
| 6 | AI lead gen for consultants | scenario-ICP |
| 7 | AI for local service business marketing | scenario-ICP |
| 8 | AI agent cleaning business clients | scenario-ICP |
| 9 | AI to grow service business | scenario |
| 10 | AI for coaching business clients | scenario-ICP |
| 11 | AI-powered referral system for services | scenario |
| 12 | AI agent for local business marketing | scenario-ICP |
| 13 | how to 10x service business with AI | outcome |
| 14 | AI client outreach tool | tool-find |
| 15 | AI for freelancer client acquisition | scenario-ICP |

---

### 2.9 核心词 #9 · `turn social media attention into clients`（15 变体）

映射 Mia · Traffic + Savannah · Paid Ads + Addison · Landing Page。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | AI to convert social followers to clients | outcome |
| 2 | AI DM automation for lead gen | scenario |
| 3 | AI for social media lead capture | scenario |
| 4 | social media to client funnel AI | scenario |
| 5 | AI for Instagram lead qualification | scenario-ICP |
| 6 | AI for TikTok lead conversion | scenario-ICP |
| 7 | AI LinkedIn outreach to clients | scenario-ICP |
| 8 | AI for X/Twitter DM lead gen | scenario-ICP |
| 9 | social media attention monetization AI | outcome |
| 10 | AI to turn likes into leads | outcome |
| 11 | AI bot convert comments to clients | scenario |
| 12 | social media ROI AI tracking | scenario |
| 13 | AI funnel from social to sale | scenario |
| 14 | automate social lead nurture AI | how-to |
| 15 | AI for YouTube lead generation | scenario-ICP |

---

### 2.10 核心词 #10 · `AI marketing agent for solo founders`（15 变体）

**另一个 Pillar 候选**。

| # | 扩展词 | 意图类型 |
|---|---|---|
| 1 | AI marketing team for solopreneur | scenario |
| 2 | one-person AI marketing stack | scenario |
| 3 | AI agent for founder-led marketing | scenario |
| 4 | AI for bootstrapped marketing | scenario-ICP |
| 5 | AI marketing automation for solo | how-to |
| 6 | AI for indie SaaS marketing | scenario-ICP |
| 7 | AI marketing agency in a box | scenario |
| 8 | AI CMO for solo founder | scenario |
| 9 | AI marketing stack for creator business | scenario-ICP |
| 10 | full-stack AI marketing team | scenario |
| 11 | AI marketing for zero budget startup | scenario-ICP |
| 12 | AI agent for launch marketing | scenario |
| 13 | AI marketing agent for Shopify founder | scenario-ICP |
| 14 | AI marketing for Substack newsletter | scenario-ICP |
| 15 | AI marketing agent for YouTube creator | scenario-ICP |

**2 节合计：173 词**

---

## 3. ICP × Agent 角色交叉（60 精选）

**扩展思路**：10 个 ICP（home.placeholder 1–10）× 15 个 Agent 角色（home.heroActionCards）= 150 理论组合。**去掉明显不合理的**（例："Shopify 卖家 × Referral Architect" 合理；"Substack 作者 × Programmatic SEO Builder" 牵强），精选 60 组。

---

### 3.1 Shopify 店主 × 角色（8）

1. AI traffic commander for Shopify
2. AI SEO doctor for Shopify
3. AI programmatic SEO for Shopify
4. AI paid ads strategist for Shopify
5. AI referral architect for Shopify
6. AI landing page builder for Shopify
7. AI ad creative studio for Shopify
8. AI competitor scout for Shopify

### 3.2 Substack 作者 × 角色（5）

9. AI SEO content factory for Substack
10. AI copy polisher for Substack newsletter
11. AI referral architect for Substack
12. AI launch strategist for Substack newsletter
13. AI email closer for Substack paid subscribers

### 3.3 TikTok/YouTube 创作者 × 角色（7）

14. AI ad creative studio for TikTok
15. AI video producer for creators
16. AI content machine for YouTube
17. AI visual creator for TikTok creators
18. AI traffic commander for YouTube
19. AI launch strategist for new creator
20. AI copy polisher for video descriptions

### 3.4 SaaS 创始人 × 角色（8）

21. AI launch strategist for indie SaaS
22. AI SEO content factory for SaaS blog
23. AI programmatic SEO for SaaS
24. AI landing page builder for SaaS
25. AI paid ads strategist for SaaS
26. AI competitor scout for SaaS
27. AI referral architect for SaaS
28. AI email closer for SaaS trial users

### 3.5 Amazon 卖家 × 角色（5）

29. AI copy polisher for Amazon listing
30. AI ad creative studio for Amazon PPC
31. AI competitor scout for Amazon
32. AI visual creator for Amazon product images
33. AI programmatic SEO for Amazon listings

### 3.6 Course creator × 角色（5）

34. AI launch strategist for online course
35. AI traffic commander for course creators
36. AI email closer for course sales
37. AI content machine for course marketing
38. AI landing page builder for course launch

### 3.7 Growth marketer × 角色（4）

39. AI paid ads strategist for growth team
40. AI programmatic SEO builder for growth
41. AI ad creative studio for growth experiments
42. AI referral architect for viral loops

### 3.8 Etsy / POD 卖家 × 角色（5）

43. AI copy polisher for Etsy listings
44. AI visual creator for Etsy product photos
45. AI traffic commander for Etsy shop
46. AI competitor scout for Etsy
47. AI ad creative studio for Etsy ads

### 3.9 AI Automation Agency（Quora 新发现 ICP）× 角色（4）

48. AI agency toolkit for solopreneurs
49. white-label AI agents for agencies
50. AI agent team for AI automation agency
51. AI agency pricing calculator（defer）

### 3.10 coaching / consulting 服务业 × 角色（4）

52. AI email closer for coaches
53. AI landing page builder for consultants
54. AI referral architect for service business
55. AI traffic commander for local business

### 3.11 通用 ICP（"one-person business"）× 角色（5）

56. AI agent for $100k one-person business
57. AI team for 1-person SaaS
58. AI co-founder for solo builder
59. AI marketing agency in a box
60. 24/7 AI worker for solopreneur

**合计：60 词**

---

## 4. Connector × Agent 角色交叉（40 精选）

**扩展思路**：6 个 connector（Notion / Gmail / Google Sheets / Slack / TikTok / Feishu）× 15 个 Agent 角色 = 90 理论组合。精选 40 高质量。

### 4.1 Notion × 角色（8）

1. AI agent for Notion automation
2. AI agent connects to Notion databases
3. AI content machine for Notion
4. AI email closer reads Notion CRM
5. AI competitor scout saves to Notion
6. AI SEO agent with Notion sync
7. AI project partner for Notion
8. AI launch strategist using Notion templates

### 4.2 Gmail × 角色（7）

9. AI email closer for Gmail
10. AI agent for Gmail automation
11. AI referral architect via Gmail
12. AI agent auto-reply Gmail
13. AI traffic commander outreach via Gmail
14. AI agent for Gmail classification
15. AI agent for cold email Gmail

### 4.3 Slack × 角色（6）

16. AI agent for Slack notifications
17. AI team communication Slack bot
18. AI agent posts Slack updates
19. AI competitor scout alerts in Slack
20. AI project partner Slack integration
21. AI agent Slack DM responder

### 4.4 Google Sheets × 角色（6）

22. AI agent syncs to Google Sheets
23. AI SEO data to Google Sheets
24. AI competitor tracking Google Sheets
25. AI lead list Google Sheets automation
26. AI keyword research to Google Sheets
27. AI ad performance Google Sheets

### 4.5 TikTok × 角色（6）

28. AI video producer for TikTok
29. AI content machine TikTok scripts
30. AI ad creative for TikTok ads
31. AI traffic commander TikTok
32. AI agent for TikTok trending analysis
33. AI agent TikTok lead capture

### 4.6 Feishu（中国市场，零量词）× 角色（4）

34. AI agent for Feishu docs
35. AI content machine for Feishu
36. AI project partner for Feishu
37. AI agent Feishu 飞书自动化

### 4.7 跨 connector（3）

38. AI agent reads Notion writes Slack
39. AI agent Gmail to Google Sheets CRM
40. AI agent for Notion + Gmail + Slack team

**合计：40 词**

---

## 5. Reddit/Quora 问句主干提取（40 词）

从 `03-reddit-quora-questions.md` 的 74 条问句，提取**还没出现在上面**的新词（去重）：

| # | 词 | 原问句 URL（简写）|
|---|---|---|
| 1 | how to promote Shopify store | r/shopify 1srsdlw |
| 2 | made-to-order workflow across Shopify Etsy | r/shopify 1srd6gf |
| 3 | optimize Shopify pages per day SEO | r/shopify 1srdlxp |
| 4 | reach Shopify store owners B2B | r/shopify 1ss1lnw |
| 5 | best AI agent for Shopify store owner | r/shopify 1srps0d |
| 6 | Shopify traffic quality by source | r/shopify 1ssafzz |
| 7 | validate mobile app idea before building | r/SaaS 1ss82kj |
| 8 | how to acquire customers for indie SaaS | r/SaaS 1srm4yl |
| 9 | how to do distribution for SaaS | r/SaaS 1ss43uq |
| 10 | why visitors don't sign up on my website | r/indiehackers 1smtafn |
| 11 | help post product on Hacker News | r/indiehackers 1srn06k |
| 12 | AI vs human marketing tired of hype | r/indiehackers 1sk90yl |
| 13 | market niche ecommerce products | r/ecommerce 1ss81mp |
| 14 | ecommerce marketing budget 2026 | r/ecommerce 1srj5ct |
| 15 | Google traffic vs ChatGPT traffic ecommerce | r/ecommerce 1srpe36 |
| 16 | automate Shopify order tracking inquiries | r/ecommerce 1srh6iv |
| 17 | AI driven team luxury packaging design | r/ecommerce 1srlppd |
| 18 | eCommerce growth 2026 what works | r/ecommerce 1sqmfin |
| 19 | improve conversion rate on landing page | r/ecommerce 1sqt733 |
| 20 | AI for e-commerce customer questions | r/ecommerce 1sr1zk5 |
| 21 | avoid scams on Etsy seller | r/Etsy 1sqnbwd |
| 22 | get Google reviews without pressure | r/ContentMarketing 1srx6uo |
| 23 | Claude setup SEO content ad copy free | r/ContentMarketing 1sldf7d |
| 24 | build audience before product launch | r/ContentMarketing 1sl4rqe |
| 25 | find reference ads examples | r/ContentMarketing 1sjwb65 |
| 26 | discover new Instagram creators | r/ContentMarketing 1shv026 |
| 27 | features AI agent for small business | r/AI_Agents 1ssa9zx |
| 28 | start AI automation agency no coding | Quora |
| 29 | find clients for AI consultancy | Quora |
| 30 | AI business ideas for beginners | Quora |
| 31 | automate Etsy Shopify with Printful Printify | Quora |
| 32 | upload POD designs in bulk | Quora |
| 33 | AI tools grow small business online 2025 | Quora |
| 34 | best AI automation company | Quora（defer 商业调查）|
| 35 | AI tools improve small business productivity | Quora |
| 36 | AI for customer support Tidio Freshchat Intercom | Quora |
| 37 | Webflow AI Site Builder for small business | Quora |
| 38 | AI content writing easy content | Quora |
| 39 | AI for sales productivity | Quora |
| 40 | duct tape operations business automation | r/Entrepreneur 1sd545v |

**合计：40 词**

---

## 6. 合并 + 预计去重

| 块 | 词数 |
|---|---|
| Day 1 种子 | 70 |
| 2. Claude 扩展 10 核心词 | 173 |
| 3. ICP × Agent 精选 | 60 |
| 4. Connector × Agent 精选 | 40 |
| 5. 问句主干提取 | 40 |
| **合计（含重叠）** | **383** |

估计重叠 ~15%（例：`AI SEO agent for Shopify` 在 2.5 和 3.1 都出现过）。
**去重后预计 ~325 词**（Day 3 实际去重时精确数）。✅ 目标 300+ 达成。

---

## 7. Day 3 准备 · 意图预分类（粗扫）

按 playbook §2.3.3 四意图（导航 / 信息 / 商业调查 / 交易），粗估分布：

| 意图 | 大致占比 | 本周策略 |
|---|---|---|
| 信息型（how-to / what-is） | ~60% | **主战场**，对应 §2.4 博客 |
| 商业调查（best X / vs） | ~20% | **defer** 进 Watch List |
| 交易型（pricing / demo） | ~5% | 映射到 /pricing / 注册页 |
| 导航型（品牌词） | ~5% | 不进 Keyword Map |
| 场景无法判定 | ~10% | Day 3 看 SERP 再定 |

**Day 3 要做的**：
1. 每词标一个 intent（1–5 分）
2. 砍掉商业调查 + 导航 = ~75 词
3. 剩 ~250 词进主库，按 Priority Score 筛到 200

---

## 8. Day 2 任务交付清单

- [x] 300+ 候选词（实际 ~325 去重后）🟢
- [x] 50+ 真实问句 → [`03-reddit-quora-questions.md`](./03-reddit-quora-questions.md)（74 条）🟢
- [x] 原始数据留存 `~/tools/opencli-raw/` 15 份 JSON
- [ ] AnswerThePublic / AlsoAsked 数据：**降级**（工具 SPA 拿不到，Claude 语义扩展代替）
- [x] Claude 10 核心词 × 15-20 变体 ≈ 173 扩展词
- [x] ICP × 角色 60
- [x] Connector × 角色 40

---

## 9. 隐忧 / 给小刀老师的提醒

- 🐛 **Claude 扩展词的"搜索真实性"没验证**：173 个 Claude 扩展词里只有映射到 Reddit 问句的那部分有真实证据。下周 Day 8+ 用 AnswerThePublic 付费试用或 Keywords Everywhere $10 跑一次全量校验
- 🐛 **商业调查词比例偏高**：Quora 几乎全是"best X"型，Day 3 打分后会砍掉很多，实际进主库的"有用词"估计 180–220 个（200 词主库目标仍能达）
- 💡 **"AI automation agency" 是新发现 ICP**：Quora 有 3 条相关问题，可能代表一小类**把 YOLOX 当白牌工具转卖**的用户群。Day 5 选 Pillar 时考虑要不要加一个次要 Pillar 覆盖
- 💡 **llms.txt 话题和 YOLOX 本周 §2.6 完美对齐**：`is llms.txt a scam` 是 A 档 Reddit 证据词 + 我们自己正在 ship /llms.txt + 15 个变体等着填。**这可能是下周第一篇 cluster 博客**
