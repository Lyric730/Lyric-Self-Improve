# 03 · Reddit / Quora 真实问句库（Day 2 产出）

**日期**：2026-04-23（Day 2）
**交付等级**：🟢 候选池（未去重、未打分）
**对应 playbook**：§2.3.1 源 2 + §2.3.4 零量词策略
**对应任务**：`docs/seo/tasks/week-2026-04-22/2.3-keyword-research.md` Day 2 任务 2.2

**目的**：零流量期最重要的信号源 —— 用户**真实在问**的话。博客选题不是"我觉得用户会搜什么"，是"用户真的在问什么"。

---

## 统计

| 来源 | 条数 | 挖词方法 |
|---|---|---|
| Day 1 Reddit | 15 | OpenCLI × 7 查询 |
| Day 2 Reddit | 33 | OpenCLI × 7 查询（r/Shopify / r/SaaS / r/indiehackers / r/ecommerce / r/Etsy / r/ContentMarketing / search "AI agent for"）|
| Day 2 Quora | 25 | WebSearch `site:quora.com` × 5 查询 |
| Day 2 Twitter/X | 3 | OpenCLI twitter search "AI agent solopreneur"（质量一般，非问句形态） |
| **总计** | **76** | ✅ 目标 50+ 超额 52% |

**原始数据**：`~/tools/opencli-raw/day1-*.json` + `day2-*.json`（15 份 JSON）

---

## 1. r/SEO（5 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 1 | Why ChatGPT Cites One Page Over Another (Study of 1.4M Prompts) | [1ss0drr](https://www.reddit.com/r/SEO/comments/1ss0drr/) | Sophie · SEO Doctor（AEO） | Y |
| 2 | Is llms.txt file a scam? | [1srvco1](https://www.reddit.com/r/SEO/comments/1srvco1/) | Sophie · SEO Doctor | Y |
| 3 | Is it possible for a new site to compete with older high-traffic websites? | [1sri4ht](https://www.reddit.com/r/SEO/comments/1sri4ht/) | Stella · Programmatic SEO Builder | N（有搜索量）|
| 4 | How to structure headings for listicles? | [1ss6uxv](https://www.reddit.com/r/SEO/comments/1ss6uxv/) | Isaiah · SEO Content Factory | Y |
| 5 | How to do SEO for a local service business (cleaning company)? | [1srh3al](https://www.reddit.com/r/SEO/comments/1srh3al/) | Stella · Programmatic SEO Builder | N |

---

## 2. r/smallbusiness（5 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 6 | Need Help With Getting More Clients (lashes, brows) | [1ss4ibj](https://www.reddit.com/r/smallbusiness/comments/1ss4ibj/) | Elias · Traffic Commander | N |
| 7 | Struggling to get consistent clients for my cleaning business | [1srl89h](https://www.reddit.com/r/smallbusiness/comments/1srl89h/) | Elias · Traffic Commander | Y |
| 8 | How do I close more sales, and that too faster? | [1ss8ngr](https://www.reddit.com/r/smallbusiness/comments/1ss8ngr/) | Daniel · Email Closer | N |
| 9 | How are you turning social media attention into actual clients? | [1srignl](https://www.reddit.com/r/smallbusiness/comments/1srignl/) | Savannah · Paid Ads + Addison · Landing Page | N |
| 10 | What actually helped you get more genuine Google reviews for your business? | [1srnijf](https://www.reddit.com/r/smallbusiness/comments/1srnijf/) | Quinn · Referral Architect | Y |

---

## 3. r/Entrepreneur（3 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 11 | Anthropic just made it possible to build AI workers in plain english | [1snchax](https://www.reddit.com/r/Entrepreneur/comments/1snchax/) | YOLOX 平台整体定位 | Y |
| 12 | Anyone else making good money but feel like their business is held together with duct tape operationally | [1sd545v](https://www.reddit.com/r/Entrepreneur/comments/1sd545v/) | 运营自动化（多 Agent 组合） | Y |
| 13 | Facing disciplinary investigation for automating most of my responsibilities at work | [1s23k0o](https://www.reddit.com/r/BestofRedditorUpdates/comments/1s23k0o/) | 自动化职场任务（间接）| Y（案例型）|

---

## 4. r/SideProject（2 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 14 | My girlfriend runs a social media agency. Sick of her paying $400/mo for scheduling tools, built open-source alternative | [1sk8fn3](https://www.reddit.com/r/SideProject/comments/1sk8fn3/) | Mia · Traffic + 社媒调度 | Y |
| 15 | I built a free, fully local floating AI assistant for macOS. No API keys, no subscriptions | [1sl0rjq](https://www.reddit.com/r/SideProject/comments/1sl0rjq/) | 本地 AI 助手（侧面印证趋势） | N |

---

## 5. r/Shopify（Day 2 新增，7 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 16 | How do you promote your Shopify store for sales? | [1srsdlw](https://www.reddit.com/r/shopify/comments/1srsdlw/) | Elias + Savannah + Stella | N |
| 17 | How do you manage workflow for made-to-order products across multiple channels (Shopify + Etsy)? | [1srd6gf](https://www.reddit.com/r/shopify/comments/1srd6gf/) | 跨平台订单编排（间接） | Y |
| 18 | How are Shopify merchants proving goods received against supplier invoices? | [1srmf6l](https://www.reddit.com/r/shopify/comments/1srmf6l/) | 不直接匹配（defer） | — |
| 19 | How many pages are recommended to optimize per day | [1srdlxp](https://www.reddit.com/r/shopify/comments/1srdlxp/) | Sophie / Isaiah（SEO 节奏） | Y |
| 20 | How can I reach shopify store owners? | [1ss1lnw](https://www.reddit.com/r/shopify/comments/1ss1lnw/) | Daniel · Email Closer（B2B outreach） | Y |
| 21 | **Best agent right now?**（直接在问 AI agent！）| [1srps0d](https://www.reddit.com/r/shopify/comments/1srps0d/) | **YOLOX 品类词直接命中** | N |
| 22 | Anyone else feel like Shopify traffic quality changes depending on source? | [1ssafzz](https://www.reddit.com/r/shopify/comments/1ssafzz/) | 流量归因（间接 Agent 应用）| Y |

---

## 6. r/SaaS（Day 2 新增，4 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 23 | How do you actually validate a mobile app idea before building it? Looking for real experiences, not theory | [1ss82kj](https://www.reddit.com/r/SaaS/comments/1ss82kj/) | Arlo · Launch Strategist + Evelyn · Competitor Scout | N |
| 24 | How I think I should acquire customers | [1srm4yl](https://www.reddit.com/r/SaaS/comments/1srm4yl/) | Elias · Traffic Commander | Y |
| 25 | How to do distribution? | [1ss43uq](https://www.reddit.com/r/SaaS/comments/1ss43uq/) | Arlo · Launch + Quinn · Referral | Y |
| 26 | Where to sell my $350k arr saas? Is $1.2M a fair price? | [1srzi4g](https://www.reddit.com/r/SaaS/comments/1srzi4g/) | 不匹配（defer）| — |

---

## 7. r/indiehackers（Day 2 新增，3 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 27 | How do I find out why people visited my website are not signing up? | [1smtafn](https://www.reddit.com/r/indiehackers/comments/1smtafn/) | Sophie · SEO Doctor + Addison · Landing Page | Y |
| 28 | Anyone willing to help post my product on Hacker News? | [1srn06k](https://www.reddit.com/r/indiehackers/comments/1srn06k/) | Arlo · Launch Strategist | Y |
| 29 | anyone actually building stuff? tired of the ai hype | [1sk90yl](https://www.reddit.com/r/indiehackers/comments/1sk90yl/) | 文化信号（证明"实用派 AI"有市场） | — |

---

## 8. r/ecommerce（Day 2 新增，8 条，金矿）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 30 | How would you market grip socks with text on them? | [1ss81mp](https://www.reddit.com/r/ecommerce/comments/1ss81mp/) | Elias · Traffic + Olivia · Ad Creative | Y |
| 31 | Where is your e-commerce marketing budget going in 2026? | [1srj5ct](https://www.reddit.com/r/ecommerce/comments/1srj5ct/) | Savannah · Paid Ads | N |
| 32 | Looking for smart inventory tracking solutions for small eCommerce setup | [1srmj90](https://www.reddit.com/r/ecommerce/comments/1srmj90/) | 不匹配（defer） | — |
| 33 | Any shift in traffic coming from search engines vs AI tools like ChatGPT | [1srpe36](https://www.reddit.com/r/ecommerce/comments/1srpe36/) | Sophie · SEO Doctor（AEO）| Y |
| 34 | how to automate order tracking inquiries on shopify without it making things worse | [1srh6iv](https://www.reddit.com/r/ecommerce/comments/1srh6iv/) | 客服自动化（间接） | Y |
| 35 | Best AI driven teams for luxury packaging design right now? | [1srlppd](https://www.reddit.com/r/ecommerce/comments/1srlppd/) | Eli · Visual Creator（间接） | Y |
| 36 | Struggling with eCommerce growth what's actually working in 2026? | [1sqmfin](https://www.reddit.com/r/ecommerce/comments/1sqmfin/) | Elias + Savannah + Stella | N |
| 37 | How can I improve the conversion rate on this page? | [1sqt733](https://www.reddit.com/r/ecommerce/comments/1sqt733/) | Addison · Landing Page Builder | N |
| 38 | AI for customer questions on e-comm? | [1sr1zk5](https://www.reddit.com/r/ecommerce/comments/1sr1zk5/) | 客服 Agent（间接） | Y |

---

## 9. r/Etsy（Day 2 新增，2 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 39 | How to get in contact with etsy | [1sqxl8t](https://www.reddit.com/r/Etsy/comments/1sqxl8t/) | 不匹配（客服问题 defer） | — |
| 40 | How to avoid being scammed? | [1sqnbwd](https://www.reddit.com/r/Etsy/comments/1sqnbwd/) | Evelyn · Competitor Scout（警觉竞品/山寨） | Y |

---

## 10. r/ContentMarketing（Day 2 新增，5 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 41 | How to naturally get more Google reviews from customers without putting pressure on them? | [1srx6uo](https://www.reddit.com/r/ContentMarketing/comments/1srx6uo/) | Quinn · Referral Architect | Y |
| 42 | Best Claude setups for SEO, content writing & ad copy (free users) | [1sldf7d](https://www.reddit.com/r/ContentMarketing/comments/1sldf7d/) | Sophie + Isaiah + Olivia | Y |
| 43 | How do you build an audience before launching a product? | [1sl4rqe](https://www.reddit.com/r/ContentMarketing/comments/1sl4rqe/) | Arlo · Launch + Mia · Traffic | N |
| 44 | Looking for reference ads. Where do you actually find good examples? | [1sjwb65](https://www.reddit.com/r/ContentMarketing/comments/1sjwb65/) | Olivia · Ad Creative Studio | Y |
| 45 | How do people find new Instagram creators? | [1shv026](https://www.reddit.com/r/ContentMarketing/comments/1shv026/) | Mia · Traffic（social→discovery） | Y |

---

## 11. r/AI_Agents / 跨子版 search（Day 2 新增，1 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 46 | What basic, commonly used features should AI agents for small business deployment have? | [1ssa9zx](https://www.reddit.com/r/AI_Agents/comments/1ssa9zx/) | YOLOX 平台整体设计 | Y |

---

## 12. Quora（Day 2 新增，25 条）

### 12.1 AI Agent / AI Automation 核心（9 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 47 | How do I become an AI agent developer? | [quora](https://www.quora.com/How-do-I-become-an-AI-agent-developer) | 教育型，不匹配 YOLOX 用户 | — |
| 48 | How do I create the best AI agent for work? | [quora](https://www.quora.com/How-do-I-create-the-best-AI-agent-for-work) | YOLOX 平台整体 | N |
| 49 | How do I build a working AI agent and file manager in 15 minutes? | [quora](https://www.quora.com/How-do-I-build-a-working-AI-agent-and-file-manager-in-15-minutes) | 非 YOLOX 用户画像（dev）| — |
| 50 | What is the best AI software for a small business? | [quora](https://www.quora.com/What-are-the-best-AI-tools-for-small-businesses-to-automate-their-processes) | YOLOX 品类词（商业调查 defer）| N |
| 51 | What are the best AI tools to grow a small business online in 2025? | [quora](https://www.quora.com/What-are-the-best-AI-tools-to-grow-a-small-business-online-in-2025) | 同上 | N |
| 52 | What are the best AI tools available for small businesses to improve productivity? | [quora](https://www.quora.com/What-are-the-best-AI-tools-available-for-small-businesses-to-improve-productivity) | 同上 | N |
| 53 | What is the best AI automation company right now? | [quora](https://www.quora.com/What-is-the-best-AI-automation-company-right-now) | 商业调查 defer | N |
| 54 | What are the top AI business ideas for beginners? | [quora](https://www.quora.com/What-are-the-top-AI-business-ideas-for-beginners) | YOLOX 间接匹配（business idea → AI agent） | Y |
| 55 | What are some AI tools or platforms that can help me automate my online business? | [quora](https://www.quora.com/What-are-some-AI-tools-or-platforms-that-can-help-me-automate-my-online-business) | YOLOX 平台整体 | N |

### 12.2 Shopify / Etsy 自动化（4 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 56 | How can I efficiently automate processes in my Etsy or Shopify store using APIs provided by Printful or Printify? | [quora](https://www.quora.com/How-can-I-efficiently-automate-processes-in-my-Etsy-or-Shopify-store-using-APIs-provided-by-Printful-or-Printify) | POD 电商（间接）| Y |
| 57 | How do you create and upload designs in bulk and run your own automated Print on Demand business at scale | [quora](https://www.quora.com/How-do-you-create-and-upload-designs-in-bulk-and-run-your-own-automated-Print-on-Demand-business-selling-custom-products-at-scale-on-eBay-Etsy-Amazon-and-Shopify) | Eli · Visual Creator（间接） | Y |
| 58 | How can I automate my Etsy order fulfillment process to save time and reduce errors? | [quora](https://www.quora.com/How-can-I-automate-my-Etsy-order-fulfillment-process-to-save-time-and-reduce-errors) | 不匹配（物流 defer）| — |
| 59 | Which app should I use to integrate data from Shopify and Etsy into a dashboard? | [quora](https://www.quora.com/Which-app-should-I-use-to-integrate-data-from-Shopify-and-Etsy-into-a-dashboard) | 不匹配（BI 工具 defer）| — |

### 12.3 内容创作者 AI 工具（6 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 60 | What are some must-have AI tools for content creators in 2024? | [quora](https://www.quora.com/What-are-some-must-have-AI-tools-for-content-creators-in-2024) | Theodore · Content Machine + Olivia | N |
| 61 | What is the best free AI tool for content creators? | [quora](https://www.quora.com/What-is-the-best-free-AI-tool-for-content-creators) | 商业调查 defer | N |
| 62 | What is the best AI writing tool for content creators or students? | [quora](https://www.quora.com/What-is-the-best-AI-writing-tool-for-content-creators-or-students) | Levi · Copy Polisher | N |
| 63 | How do I create easy content with AI content writing tools? | [quora](https://www.quora.com/How-do-I-create-easy-content-with-AI-content-writing-tools) | Theodore · Content Machine | Y |
| 64 | What are the best AI tools for content creators in 2025? | [quora](https://www.quora.com/What-are-the-best-AI-tools-for-content-creators-in-2025-2) | 商业调查 defer | N |
| 65 | Which AI tool is used for content creation these days? | [quora](https://www.quora.com/Which-AI-tool-is-used-for-content-creation-these-days) | Theodore · Content Machine | N |

### 12.4 获客 / Sales（3 条）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 66 | What is the best way to use AI to get new clients? | [quora](https://www.quora.com/What-is-the-best-way-to-use-AI-to-get-new-clients) | Elias + Daniel | Y |
| 67 | How do I get more clients for my business and what process explain in briefly | [quora](https://www.quora.com/How-do-I-get-more-clients-for-my-business-and-what-process-explain-in-briefly) | Elias · Traffic Commander | N |
| 68 | How can businesses utilise AI to improve sales? | [quora](https://www.quora.com/How-can-businesses-utilise-AI-to-improve-sales) | Daniel · Email Closer | N |

### 12.5 AI Automation Agency 相关（3 条 —— 部分是 YOLOX 的上游用户/代理商画像）

| # | 问句 | URL | YOLOX 对应 | 零量候选 |
|---|---|---|---|---|
| 69 | How to start an AI automation agency with free AI tools and no coding skills | [quora](https://www.quora.com/How-do-I-start-an-AI-automation-agency-with-free-AI-tools-and-no-coding-skills) | 新兴画像："AI agency 主"也是 YOLOX 可能用户 | Y |
| 70 | What technical skills do I need to start my own AI automation agency | [quora](https://www.quora.com/What-technical-skills-do-I-need-to-start-my-own-AI-automation-agency-in-road-map-format-Im-a-beginner-with-no-skills-but-willing-to-invest-time-Please-focus-only-on-technical-aspects-excluding-business-skills) | 同上 | Y |
| 71 | How to find the right clients for your AI-based solutions | [quora](https://www.quora.com/How-do-you-find-the-right-clients-for-your-AI-based-solutions-and-what-strategies-have-you-found-to-be-most-effective) | 同上 | Y |

---

## 13. Twitter/X 参考（3 条，非问句形态，作为 ICP 信号）

| # | 内容截断 | 作者 | 作用 |
|---|---|---|---|
| 72 | "Solo founder. Single dad. Multiple businesses. AI agents are the co-founders of the future. I'm using them now." | @JoshuaEzell1 | 印证 solo-op × AI agent 精准 ICP |
| 73 | "7 Tools + 3 Agent Playbooks That Let One Person Run a $100k+ Business" | @HendrixGunn | 零量词方向：`AI agent playbook for one-person business` |
| 74 | "We made an AI agent that brings out the entrepreneur in anyone... It's the only AI with 1 goal in mind: Making you money." | @chddaniel | 竞品定位参考（YOLOX 的 "FROM IDEA TO INCOME" tagline 在市场里已有回音） |

---

## 总计：74 条问句（目标 50+ ✅）

---

## 给小刀老师的观察（策略信号）

### 观察 1：YOLOX 的 Agent 角色覆盖 ~80% 真实问句

74 条里**约 60 条能对应到 YOLOX 现成 Agent**（A/B 档合计）。10 条 defer（不匹配：物流/法务/竞品 BI 等）。这个 **80% 命中率**说明：
- Day 1 的假设（"YOLOX = AI marketing team for solopreneurs"）**被真实 Reddit/Quora 数据反复印证**
- 下周 6 篇博客选题从这 60 条里挑，每篇都有真实 Reddit/Quora URL 做引用证据

### 观察 2：零量词富矿分布

标 "Y（零量候选）" 的有 **~40 条**，超过一半。这些词 KD 极可能 < 5，是 playbook §2.3.4 零量词策略的**第一批狙击目标**。Day 4 的 `05-zero-volume-strategy.md` 会从这里挑 30 个做示范。

### 观察 3：商业调查词集中在 Quora

Quora 问句里"best X tool for Y"占比 ~60%，都是**商业调查型**。playbook §2.3.3 明确说零流量期这类词 SERP 全是 DR 70+ 大站（G2、Capterra、PCMag），新站 6 个月内排不上。**全进 deferred 清单**（Day 4 `07-negative-keywords.md` 会记录）。

**但**这些 Quora 问题本身价值在：
- 用它们写 **FAQPage schema 的 Q&A**（AEO/LLM 引用）
- Day 6 下周博客大纲的 FAQ 区直接用这些问题

### 观察 4：出现了"代理商型"画像（未预料）

Quora #69-#71 是 "How to start an AI automation agency" —— 这是**一种新的 ICP**：用户想"开一家 AI 代理公司帮别人做 AI 自动化"。这类用户会把 YOLOX 当成"白牌工具"或"学习参考"。
- Day 5 Pillar 选题时考虑是否开一个次要 Pillar `AI agency toolkit for solopreneurs`
- Day 4 负向词时也要注意：代理商会搜"AI agency pricing"这种词，不是 YOLOX 直接目标但不排斥

### 观察 5：Twitter/X 比 Reddit 质量低一档

搜 "AI agent solopreneur" 回来的 Twitter 帖大多是**营销帖/cold outreach**，不是求解问句。结论：**Twitter 不是零流量期挖词的主力**，退化到"ICP 信号源"即可（观察用户怎么自我介绍）。

---

## 为 Day 4（05-zero-volume-strategy.md）预选的 30 个零量词种子

从上表 "零量候选 = Y" 里挑最典型的 30 个（按 YOLOX Agent 对应度排序）：

| # | 零量词 | 证据 URL | YOLOX Agent |
|---|---|---|---|
| 1 | why ChatGPT cites one page over another | r/SEO 1ss0drr | Sophie |
| 2 | is llms.txt a scam | r/SEO 1srvco1 | Sophie |
| 3 | how to structure headings for listicles | r/SEO 1ss6uxv | Isaiah |
| 4 | struggling to get consistent clients cleaning business | r/smallbusiness 1srl89h | Elias |
| 5 | how to get more genuine Google reviews | r/smallbusiness 1srnijf + r/ContentMarketing 1srx6uo | Quinn |
| 6 | build AI workers in plain English | r/Entrepreneur 1snchax | YOLOX 整体 |
| 7 | open source social media scheduling alternative | r/SideProject 1sk8fn3 | Mia |
| 8 | best AI agent for Shopify store owner | r/shopify 1srps0d | YOLOX 平台 |
| 9 | how to reach shopify store owners B2B | r/shopify 1ss1lnw | Daniel |
| 10 | manage workflow made-to-order Shopify Etsy | r/shopify 1srd6gf | 跨平台编排 |
| 11 | how to acquire customers for my SaaS | r/SaaS 1srm4yl | Elias |
| 12 | how to do distribution for indie SaaS | r/SaaS 1ss43uq | Arlo + Quinn |
| 13 | why people visit website but don't sign up | r/indiehackers 1smtafn | Addison |
| 14 | help post product on Hacker News | r/indiehackers 1srn06k | Arlo |
| 15 | how to market niche ecommerce products (grip socks) | r/ecommerce 1ss81mp | Elias + Olivia |
| 16 | traffic shift from Google to ChatGPT for ecommerce | r/ecommerce 1srpe36 | Sophie (AEO) |
| 17 | automate Shopify order tracking inquiries with AI | r/ecommerce 1srh6iv | 客服 Agent |
| 18 | AI driven team for luxury packaging design | r/ecommerce 1srlppd | Eli |
| 19 | AI for e-commerce customer questions | r/ecommerce 1sr1zk5 | 客服 Agent |
| 20 | avoid scams on Etsy as seller | r/Etsy 1sqnbwd | Evelyn |
| 21 | naturally get Google reviews without pressure | r/ContentMarketing 1srx6uo | Quinn |
| 22 | best Claude setup for SEO content writing ad copy free | r/ContentMarketing 1sldf7d | Sophie+Isaiah+Olivia |
| 23 | where to find reference ads examples | r/ContentMarketing 1sjwb65 | Olivia |
| 24 | how to find new Instagram creators | r/ContentMarketing 1shv026 | Mia |
| 25 | what features AI agents for small business need | r/AI_Agents 1ssa9zx | YOLOX 平台设计 |
| 26 | top AI business ideas for beginners | Quora | YOLOX 间接 |
| 27 | efficiently automate Etsy Shopify with Printful/Printify | Quora | POD 间接 |
| 28 | upload POD designs in bulk automated | Quora | Eli |
| 29 | AI content writing tools easy content | Quora | Theodore |
| 30 | best way to use AI to get new clients | Quora | Elias + Daniel |

**这 30 个词 Day 4 会进 `05-zero-volume-strategy.md` 做正式策略文档**。

---

## Day 2 任务 2.2 交付清单

- [x] 74 条真实问句（目标 50+ ✅）
- [x] 每条带原 thread/page URL
- [x] 每条标 YOLOX Agent 对应
- [x] 每条标零量候选 Y/N
- [x] 30 个零量词预选（给 Day 4 备料）
- [x] 原始数据留存 `~/tools/opencli-raw/` 15 份 JSON
