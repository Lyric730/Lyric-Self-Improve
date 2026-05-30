# Round-2 Day-2 · L2 主库 v0 · 02-expanded-keywords

**日期**：2026-05-04
**讨论方**：小刀老师 + Agent B
**状态**：v0 final（L2 Step 5 4 级筛漏斗完成）
**前置依赖**：Pool A 76 + Step 2 1890 + Step 3 27 + KWFinder 30 → 4 级筛 → 主库 v0

---

## 0 · 概览

| 维度 | 数值 |
|---|---|
| **主库 v0 总词数** | **666** |
| Pool A 直接 keep（tier-1+2）| 76 |
| Haiku Layer 3 keep（4/4 yes）| 590 |
| Pool B reserve（3/4 yes）| 175 |
| 总输入候选 | 1316（去重后）|
| Layer 3 通过率 | 48%（590/1240）|
| L2 §1 目标 | 300-500 词（实际 666，超 33%）|

## 1 · Tier 分布

| Tier | 数量 |
|---|---|
| Tier 2 · Pool A 精选 | 68 |
| Tier 2 · 数据验证 | 8 |
| Tier 3 · Haiku 4 yes | 590 |

## 2 · 11 坑规避自检

| 坑 | 状态 |
|---|---|
| 6.2 Claude 12.5% 命中率 | ✅ Layer 3 用 Haiku 4.5 不是 Opus 凭空扩，符合 spec |
| 6.5 内部 Agent 人名 | ✅ Layer 2 黑名单过滤通过 |
| 6.11 Handoff stale | ✅ worktree 隔离 + git status 干净 |
| 新 · Haiku 误判 | ⚠️ Pool B 175 keep_weak 备用，L4 量化时回查可升级 |

## 3 · 主库 v0 完整词表（666 词）

**字段**：# / 关键词 / Tier / 来源 / ICP / Intent / Volume / KD / Growth / SERP Features / 备注

| # | 关键词 | Tier | 来源 | ICP | Intent | Vol | KD | Growth | SERP | 产品对接 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AI agent for code review | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | ai-builder | commercial, transactional | — | 34 | — | AI Overview | Skills · Developer Tools 217 (e.g. agent-tools); team AI App Builder |
| 2 | how to get amazon reviews without vine | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | amazon-seller | info | — | — | — | — | team Amazon Seller; agent Alice (Review Manager) |
| 3 | amazon FBA shipment lost tracking | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | amazon-seller | info | — | — | — | — | team Amazon Seller |
| 4 | selling handmade items online platform comparison | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | artisan-dtc | info | — | — | — | — | team Artisan / DTC Brand Founder |
| 5 | cold email metrics that matter | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | b2b-sdr | info | — | — | — | — | agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer) |
| 6 | cold email volume vs deliverability | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | b2b-sdr | info | — | — | — | — | agent Lucas (Cold Outreach Pro) |
| 7 | AI agent for PR | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | brand-pr | info | — | — | — | — | agent Wyatt (Press Release Writer); agent Alexander (Crisis PR Advisor) |
| 8 | value of media placements for clients | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | brand-pr | info | — | — | — | — | team Brand & PR Manager |
| 9 | best scheduling tool for coaches | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | coach | info | — | — | — | — | team Career & Life Coach; skill Productivity |
| 10 | consultant powerpoint design tips | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | consultant | info | — | — | — | — | team Consultant; agent Silas (Pitch Deck Builder) |
| 11 | traits of high performing consultant | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | consultant | info | — | — | — | — | team Consultant |
| 12 | content marketing strategy that works 2026 | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | content-mkt-mgr | info | — | — | — | — | team Content Marketing Manager; agent Theodore (Content Machine) |
| 13 | AI SEO agency for product descriptions | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | content-mkt-mgr | info | — | — | — | — | agent Sophie (SEO Doctor); agent Isaiah (SEO Content Factory) |
| 14 | how to get LLM link citations | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | content-mkt-mgr | info | — | — | — | — | agent Sophie (SEO Doctor); skill ai-seo |
| 15 | how to create and sell online course | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | course-creator | info | — | 46 | — | — | team Knowledge IP Builder; agent Scarlett (Course Architect) |
| 16 | best platform to sell online courses | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | course-creator | info | — | — | — | — | team Knowledge IP Builder; agent Scarlett (Course Architect) |
| 17 | how to start data analysis project from scratch | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | data-analyst | info | — | — | — | — | agent Camila (Data Interpreter); agent Jackson (Dashboard Designer) |
| 18 | SQL self join tutorial mental model | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | data-analyst | info | — | — | — | — | skill Data & Analytics 20 |
| 19 | local SEO cost for small business | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | fallback-generic | info | — | — | — | — | agent Sophie (SEO Doctor); team Local Restaurant |
| 20 | how to handle fee-sensitive prospects | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | financial-advisor | info | — | — | — | — | team Independent Financial Advisor |
| 21 | best CRM for financial advisors | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | financial-advisor | info | — | — | — | — | team Independent Financial Advisor |
| 22 | how to write freelance design proposals | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | freelance-designer | info | — | — | — | — | team Freelance Designer; agent Aria (Freelance Proposal Writer) |
| 23 | why ChatGPT cites pages | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | growth-marketer | info | — | — | — | — | agent Sophie (SEO Doctor); skill ai-seo |
| 24 | Cloudflare blocking GPTBot SEO impact | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | growth-marketer | info | — | — | — | — | agent Brooks (Website Audit Reporter); skill ai-seo |
| 25 | buying backlinks DA score risk | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | growth-marketer | info | — | — | — | — | agent Brooks (Website Audit Reporter); skill backlink-analyzer |
| 26 | why visitors don't sign up SaaS | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | indie-saas-founder | info | — | — | — | — | team SaaS Founder; agent Luna (Conversion Optimizer) |
| 27 | best community for SaaS builders | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | indie-saas-founder | info | — | — | — | — | team SaaS Founder |
| 28 | React Native cross platform 2026 comparison | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | mobile-dev | info | — | — | — | — | team App Developer; agent Oliver (ASO Optimizer) |
| 29 | where to advertise newsletter for subscribers | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | newsletter-writer | info | — | — | — | — | team Newsletter Creator; agent Aurora (Newsletter Curator) |
| 30 | tips for growing small newsletter | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | newsletter-writer | info | — | — | — | — | team Newsletter Creator |
| 31 | best social media to promote substack | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | newsletter-writer | info | — | — | — | — | team Substack/Newsletter-First Creator; agent Aurora |
| 32 | streaming TV vs paid social ads | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | paid-ads | info | — | — | — | — | agent Savannah (Paid Ads Strategist); agent Olivia (Ad Creative Studio) |
| 33 | best landing page builder for PPC agencies | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | paid-ads | info | — | — | — | — | agent Addison (Landing Page Builder); agent Savannah (Paid Ads Strategist) |
| 34 | podcast guest release agreement template | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | podcaster | info | — | — | — | — | team Podcaster; agent Elena (Podcast Producer) |
| 35 | AI candidate sourcing tool | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | recruiter | info | — | — | — | — | team Recruiter |
| 36 | freelance recruiter daily workflow | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | recruiter | info | — | — | — | — | team Recruiter |
| 37 | small restaurant marketing strategies | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | restaurant-owner | info | — | — | — | — | team Local Restaurant; agent Leo (Local Event Planner) |
| 38 | restaurant marketing on small budget | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | restaurant-owner | info | — | — | — | — | team Local Restaurant |
| 39 | ecommerce growth strategy 2026 | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | shopify-owner | info | — | — | — | — | team Shopify/DTC Brand |
| 40 | shopify alternatives ecommerce platforms | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | shopify-owner | info | — | — | — | — | team Shopify/DTC Brand |
| 41 | how to batch create social content | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | social-mkt-mgr | info | — | — | — | — | team Social Media Manager; agent Harper (Content Repurposing Engine) |
| 42 | best multi-platform social media management tool | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | social-mkt-mgr | info | — | — | — | — | team Social Media Manager |
| 43 | self hosting mistakes for beginners | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | solo-dev | info | — | — | — | — | team Indie Hacker; skill DevOps |
| 44 | starting Instagram from day 1 strategy | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | tiktok-creator | info | — | — | — | — | team Short Video Creator; agent Claire (Twitter Growth Pilot) |
| 45 | when to LLC YouTube channel | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | youtuber | info | — | — | — | — | team YouTube/Twitch Creator; agent Sadie (Video Producer) |
| 46 | AI for ML research | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | ai-builder | compare | — | — | — | — | Skills · Data & Analytics; team AI App Builder |
| 47 | AI infographic generator | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | content-mkt-mgr | compare | — | — | — | — | agent Logan (Infographic Designer); team Content Marketing |
| 48 | Shopify AI product description | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | shopify-owner | compare | — | — | — | — | agent Grayson (Product Listing Copywriter); team Shopify/DTC |
| 49 | programmatic SEO AI | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | indie-saas-founder | compare | — | — | — | — | agent Stella (Programmatic SEO Builder); team SaaS Founder |
| 50 | AI agent for API documentation | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | solo-dev | compare | — | — | — | — | Skills · DevOps; team Indie Hacker |
| 51 | AI cold email tool | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | b2b-sdr | compare | — | — | — | — | agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer) |
| 52 | AI agent for unit testing | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | ai-builder | compare | — | — | — | — | Skills · Developer Tools |
| 53 | Marketing & Growth AI agents | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | growth-marketer | compare | — | — | — | — | Skills · Marketing & Growth 33 |
| 54 | Content & Writing AI agents | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | content-mkt-mgr | compare | — | — | — | — | Skills · Content & Writing 24 |
| 55 | Claude Code workflow | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | (cross-icp) | info | — | — | — | — | L4 验证 |
| 56 | Claude agent skills | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | (cross-icp) | info | — | — | — | — | L4 验证 |
| 57 | llms.txt SEO | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | (cross-icp) | info | — | — | — | — | L4 验证 |
| 58 | Google AI Overview optimization | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | (cross-icp) | info | — | — | — | — | L4 验证 |
| 59 | tasks entrepreneurs can automate | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | fallback-generic | info | — | — | — | — | agent Xavier (Workflow Automator); Skills · Automation |
| 60 | AI generated podcasts 2026 | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | podcaster | info | — | — | — | — | team Podcaster; agent Elena (Podcast Producer) |
| 61 | how to build TikTok presence in 2026 | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | tiktok-creator | info | — | — | — | — | team Short Video Creator; agent Sadie (Video Producer) |
| 62 | YouTube video stolen on TikTok recovery | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | youtuber | info | — | — | — | — | team YouTube/Twitch Creator; agent Sadie |
| 63 | youtuber pain points 2026 | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | youtuber | info | — | — | — | — | team YouTube/Twitch Creator |
| 64 | cold email at million scale | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | b2b-sdr | info | — | — | — | — | agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer) |
| 65 | amazon vine review recovery | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | amazon-seller | info | — | — | — | — | team Amazon Seller; agent Alice (Review Manager) |
| 66 | consulting ex-consultant clients | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | consultant | info | — | — | — | — | team Consultant |
| 67 | data analysis early career mistakes | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | data-analyst | info | — | — | — | — | agent Camila (Data Interpreter); team Indie Hacker |
| 68 | financial advisor disengaged client management | Tier 2 · Pool A 精选 | Layer 1+2 direct keep (Pool A) | financial-advisor | info | — | — | — | — | team Independent Financial Advisor |
| 69 | best business coaching program | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | coach | commercial | 30 | 36 | -81% | AI Overview, People Also  | team Career & Life Coach |
| 70 | AI proposal generator | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | freelance-designer | compare | 530 | 34 | -50% | People Also Ask | agent Aria (Freelance Proposal Writer); team Freelance Designer |
| 71 | AI ad creative generator | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | artisan-dtc | compare | 60 | 45 | 75% | People Also Ask | agent Olivia (Ad Creative Studio); team Artisan/DTC |
| 72 | AI app builder | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | mobile-dev | navigational | 9600 | 47 | 305% | — | team App Developer |
| 73 | AI newsletter writer | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | newsletter-writer | compare | 10 | 30 | -67% | — | agent Aurora (Newsletter Curator); team Newsletter Creator |
| 74 | Generative Engine Optimization | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | (cross-icp) | info | 4800 | 63 | 180% | AI Overview | L4 验证 |
| 75 | Model Context Protocol | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | (cross-icp) | commercial, informational, transactional | 21500 | 55 | -35% | AI Overview | L4 验证 |
| 76 | Answer Engine Optimization | Tier 2 · 数据验证 | Layer 1+2 direct keep (Pool A) | (cross-icp) | info | 2100 | 49 | 200% | AI Overview, People Also  | L4 验证 |
| 77 | ai agent for code analysis | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 78 | best ai agent for code review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 79 | build ai agent for code review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 80 | github ai agent for code review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 81 | ai agent code review gitlab | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 82 | ai agent code review prompt | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 83 | ai agent code review skill | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 84 | best ai agent for code analysis | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 85 | bitbucket ai agent code review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 86 | ai for code review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 87 | ai coding agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 88 | code review using ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 89 | bito ai code review agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 90 | bito's ai code review agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 91 | azure devops ai code review agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 92 | ai agent for embedded code reviewer | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 93 | ai agent for coding | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 94 | best coding ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 95 | how to code ai agents | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 96 | ai code review products | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 97 | ai code review online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 98 | ai agent no code | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 99 | code review ai free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 100 | ai code writer review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 101 | free no code ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 102 | how to get reviews on amazon products | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 103 | how to get amazon reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 104 | how to get amazon products free for review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 105 | how to get vine amazon review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 106 | how to be an amazon vine reviewer | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 107 | how many reviews to become amazon vine | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 108 | how to get into amazon vine reddit | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 109 | amazon vine program reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 110 | apply to be amazon vine reviewer | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 111 | what are vine reviews on amazon | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 112 | amazon vine customer review of free product | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 113 | amazon vine product reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 114 | amazon vine customer review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 115 | amazon vine review of free product | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 116 | amazon vine review program | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 117 | amazon fba shipment lost tracking number | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 118 | amazon fba shipment lost tracking process | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 119 | amazon fba shipment lost tracking inventory | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 120 | amazon tracking tba3 lost package | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 121 | amazon fba incorrect shipment | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 122 | amazon tracking id tba4 lost package | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 123 | amazon shipping tracking tba | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 124 | drop shipping in amazon fba | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 125 | how to cancel amazon fba shipment | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 126 | how to drop ship amazon fba | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 127 | amazon logistics tba tracking | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 128 | amazon fba container tracking | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 129 | amazon delivery tba tracking | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 130 | shipping to amazon fba | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 131 | how to ship fba items to amazon | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 132 | amazon fba shipping to warehouse | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 133 | amazon shipping costs fba | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 134 | amazon fba shipping cost | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 135 | selling handmade items online platform comparisons | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 136 | selling handmade items online platform comparison 2023 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 137 | cold email metrics that matters | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 138 | best cold email follow up metrics | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 139 | cold email marketing tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 140 | cold email marketing strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 141 | intelligent email marketing metrics | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 142 | cold email marketing services | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 143 | cold email deliverability | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 144 | cold emails that get responses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 145 | email deliverability system comparison | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 146 | email deliverability system review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 147 | email deliverability companies comparison | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 148 | email deliverability programs comparison | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 149 | email deliverability software comparison | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 150 | email deliverability system overview | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 151 | email deliverability software reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 152 | how to improve email deliverability rates | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 153 | best email deliverability guide | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 154 | email deliverability programs reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 155 | email deliverability companies reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 156 | ai agent for project management | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 157 | ai agent for presentation | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 158 | ai agent for procurement | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 159 | ai agent for programming | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 160 | ai agent for productivity | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 161 | ai agent for product owner | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 162 | ai agent for pr review | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 163 | ai agent for product manager | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 164 | ai agent for product research | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 165 | ai agent for programmers | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 166 | ai agents for prospecting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 167 | how do pr professionals use ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 168 | ai agent for marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 169 | ai agent for network | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 170 | ai agents for project management | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 171 | ai agents for programming | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 172 | value of media placements for clients on facebook | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 173 | what are media placements | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 174 | reasons for choosing placement media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 175 | product placement in media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 176 | local media placement for businesses cost | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 177 | what is media placement in advertising | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 178 | local media placement for business reputation | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 179 | local media placement for businesses reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 180 | local media placement for businesses examples | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 181 | main role of product placement in media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 182 | local media placement for businesses benefits | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 183 | product placement definition media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 184 | local media placement for business branding | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 185 | social media marketing placement | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 186 | social media product placement | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 187 | best business coaching programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 188 | best executive coaching programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 189 | best executive coaching programs in the us | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 190 | best business coaching software | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 191 | best business coaching certification programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 192 | best online business coaching programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 193 | best executive coaching training | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 194 | best executive coaching certification programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 195 | best executive coaching certification programs uk | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 196 | best executive coaching certification programs canada | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 197 | best business coaching programs 2023 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 198 | best business coaching programs for small businesses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 199 | business coaching program reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 200 | business coaching programs online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 201 | business coaching programs for managers | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 202 | business coaching programs near me | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 203 | business coaching programs for leaders | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 204 | the best coaching programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 205 | business coaching program examples | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 206 | schools with business coaching | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 207 | business coach program online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 208 | certified business coaching programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 209 | business coaching programs for executives | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 210 | small business coaching programs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 211 | business coaching programs certification | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 212 | best scheduling app for coaches | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 213 | best scheduling software for coaches | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 214 | best scheduling app for trainers | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 215 | best scheduling app for life coaches | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 216 | best scheduling tool for coaches on linkedin | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 217 | free scheduling software for coaches | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 218 | best team scheduling tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 219 | consultant powerpoint design tips and tricks | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 220 | powerpoint template for consulting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 221 | power point templates for consulting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 222 | consulting powerpoint templates free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 223 | best powerpoint add-ins for consultants | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 224 | ppt for consultancy services | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 225 | ppt templates for consulting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 226 | powerpoint presentation design tips | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 227 | management consulting powerpoint templates | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 228 | free consulting ppt template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 229 | consulting ppt templates free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 230 | powerpoint designer firms tips | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 231 | help with powerpoint design | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 232 | tips for making a professional powerpoint | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 233 | traits of high performing consultants | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 234 | traits of a great consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 235 | characteristics of a good consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 236 | qualities of a consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 237 | qualities of a good consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 238 | five key traits of successful consultants | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 239 | skills of a great consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 240 | skills of a consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 241 | top skills for a consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 242 | popular consultant job skills | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 243 | key skills for a consultant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 244 | content marketing strategy 2026 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 245 | what is content marketing strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 246 | content marketing trends 2023 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 247 | content marketing trends 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 248 | content marketing strategy development | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 249 | media marketing content strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 250 | content marketing management strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 251 | fall 2023 content marketing trends | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 252 | ai seo agency for product descriptions free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 253 | ai seo description generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 254 | seo for product descriptions | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 255 | ai seo software for local seo | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 256 | ai marketing solutions for seo | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 257 | ai seo tool for local seo | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 258 | seo ai for website | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 259 | seo for ai search | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 260 | seo product description generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 261 | ai tool to generate content for seo | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 262 | how to create and sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 263 | how to create and sell online courses with wordpress | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 264 | how to create and market an online course | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 265 | how to make money selling online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 266 | how to create a website to sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 267 | platforms to create and sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 268 | create and sell online courses free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 269 | create and sell online courses for profit | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 270 | best platform to create and sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 271 | how to make an online course to sell | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 272 | how to make and sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 273 | how to create online course selling website | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 274 | how to create and sell courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 275 | create online courses to sell | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 276 | how to create a course online and sell it | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 277 | create an online course to sell | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 278 | how to create and sell an online course | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 279 | how to create a course to sell | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 280 | how to sell a course online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 281 | how to make a course to sell | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 282 | how to sell courses online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 283 | selling a course online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 284 | best platform to sell online courses in india | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 285 | platforms to sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 286 | best platforms to sell online courses in america | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 287 | best platforms to sell online courses in us | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 288 | best platform for selling courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 289 | best site to sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 290 | best place to sell online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 291 | online courses selling platform | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 292 | best online courses to sell | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 293 | best online services to sell courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 294 | the best platform to sell online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 295 | online course selling platform | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 296 | best website to sell courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 297 | best course selling platform | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 298 | free course selling platform | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 299 | software for selling online courses | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 300 | sql self join tutorial mental models | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 301 | self join sql tutorial | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 302 | sql self join explained | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 303 | self join sql example | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 304 | self join sql questions | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 305 | self join in sql with examples | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 306 | example in self join sql server | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 307 | self join in ms sql server | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 308 | self join in sql diagram | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 309 | best crm for financial advisors in india | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 310 | best crm for financial advisors canada | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 311 | top crm for financial advisors | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 312 | best crm for investment advisors | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 313 | best crm for financial planners | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 314 | best crm software for financial advisors | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 315 | best free crm for financial advisors | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 316 | crm for financial advisors | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 317 | best crms for financial advisors | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 318 | crm for financial advisors comparison | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 319 | best financial advisor crm software | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 320 | financial crm software for advisors | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 321 | how to write a freelance job proposal | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 322 | freelance graphic design proposal | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 323 | how to make a freelance contract proposal | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 324 | sample business proposal freelance | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 325 | freelance work proposal template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 326 | how to write bid proposal for freelancing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 327 | software freelance project proposal | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 328 | proposal letter for freelancer | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 329 | graphic design freelance job proposal | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 330 | template freelancing work proposal | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 331 | best platform to build a community | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 332 | build a community online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 333 | best no code saas builder | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 334 | where to advertise newsletter for subscribers on youtube | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 335 | how to grow my newsletter subscriber list | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 336 | how to grow my email newsletter subscribers | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 337 | tips for growing small newsletters | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 338 | how to grow a newsletter | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 339 | how to grow newsletter subscribers | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 340 | grow a newsletter audience | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 341 | best social media to promote substack 2023 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 342 | how to promote your substack | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 343 | how to get popular on substack | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 344 | top social media strategies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 345 | streaming tv vs paid social ads facebook | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 346 | google ads vs paid social advertising | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 347 | paid ads social media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 348 | social media paid advertising | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 349 | paid social media advertising services | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 350 | paid social media advertising strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 351 | paid social media advertising benefits | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 352 | top landing page builders for agencies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 353 | landing page builder solution for agencies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 354 | ppc landing page software | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 355 | landing page builder software for agencies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 356 | landing page builder studio for agencies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 357 | the best landing page builder | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 358 | top landing page builder services for 2021 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 359 | top landing page builder websites | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 360 | top landing page builder solution | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 361 | top landing page builder services comparison | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 362 | ppc together with landing pages | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 363 | ppc competitor tool for landing page analysis | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 364 | top landing page builder services reviews | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 365 | top 10 landing page builder | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 366 | landing page builder professional | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 367 | podcast guest release form template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 368 | podcast guest agreement template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 369 | podcast guest release form template free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 370 | podcast guest release agreement template free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 371 | podcast guest release form | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 372 | free podcast guest release form | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 373 | podcast release form for guests | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 374 | podcast host agreement contract template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 375 | recording agreement template for podcasts | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 376 | podcast agreement contract template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 377 | podcast release form template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 378 | how to release a podcast with guests | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 379 | podcast co host agreement | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 380 | podcast guest consent form | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 381 | producer agreement template for podcast | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 382 | podcast partnership agreement sample | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 383 | hosting agreements for podcasts | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 384 | podcast partnership agreement examples | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 385 | ai candidate sourcing tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 386 | ai recruitment sourcing tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 387 | ai talent sourcing tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 388 | best ai candidate sourcing tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 389 | free ai candidate sourcing tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 390 | candidate sourcing methods | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 391 | ai sourcing tools for recruiting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 392 | free ai sourcing tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 393 | ai talent acquisition sourcing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 394 | ai tool for recruitment | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 395 | ai interview software for candidates | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 396 | ai tools for recruiting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 397 | ai powered recruitment tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 398 | generative ai tools for recruiting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 399 | best ai recruiting tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 400 | ai tools for recruiters | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 401 | best ai recruiting software tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 402 | free ai recruiting tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 403 | freelance recruiter daily workflows | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 404 | recruiting software workflow design | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 405 | recruiting software workflow steps | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 406 | recruiting software workflow best practices | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 407 | recruiting software workflow comparison | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 408 | recruiting software workflow template | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 409 | recruiting software workflow diagram | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 410 | recruiting software workflow automation | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 411 | recruiting software workflow integration | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 412 | recruiting software workflow optimization | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 413 | small restaurant marketing ideas and trends | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 414 | small restaurant marketing ideas | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 415 | small business restaurant marketing strategies for sustainability | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 416 | marketing strategies for restaurants | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 417 | marketing strategies for small restaurants | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 418 | restaurant business marketing strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 419 | marketing strategies for a restaurant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 420 | marketing for restaurants strategies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 421 | marketing ideas for small business restaurant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 422 | marketing ideas for small restaurants | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 423 | good marketing strategies for restaurants | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 424 | restaurant marketing near me strategies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 425 | business strategy for restaurant marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 426 | restaurant marketing and strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 427 | how to make restaurant marketing strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 428 | restaurant local marketing strategies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 429 | marketing strategy for small food business | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 430 | strategies for restaurant business | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 431 | restaurant marketing on small budgets | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 432 | budgeting for restaurant marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 433 | how to make restaurant marketing budget | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 434 | restaurant marketing proposal budget | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 435 | restaurant catering advertising budget | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 436 | marketing strategy for restaurant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 437 | marketing plan for a restaurant | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 438 | ecommerce growth strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 439 | ecommerce growth | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 440 | ecommerce insights | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 441 | ecommerce marketing strategy 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 442 | midsized ecommerce growth strategies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 443 | ultimate guide to ecommerce growth | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 444 | fall 2023 content strategy for e-commerce | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 445 | midsized ecommerce business growth | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 446 | how to bulk create social media posts in canva | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 447 | how to bulk create social media posts | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 448 | creating content for social media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 449 | how to batch create social content for instagram | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 450 | batching content for social media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 451 | how to create content for social media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 452 | how to generate content for social media | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 453 | best multi-platform social media management tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 454 | best multi-platform social media management tools and techniques | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 455 | avoid these common web hosting mistakes | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 456 | biggest web hosting mistakes | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 457 | self hosting for beginners | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 458 | worst web hosting mistakes | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 459 | avoid these common web hosting cost mistakes | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 460 | self hosting for dummies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 461 | how to start self hosting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 462 | avoid these common web host mistakes | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 463 | getting started self hosting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 464 | how to self host | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 465 | problems with hosting your own website | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 466 | start blog recommended hosting | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 467 | starting instagram from day 1 strategy 2023 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 468 | instagram strategies for beginners | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 469 | starting a new instagram | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 470 | how to start on instagram | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 471 | how to create a business instagram strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 472 | how to make a business instagram strategy | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 473 | marketing strategy for instagram | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 474 | starting a instagram page | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 475 | how to get started with instagram | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 476 | how to get started on instagram beginner | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 477 | how to start a successful instagram page | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 478 | best instagram planning strategies | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 479 | how to start your instagram page | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 480 | ai proposal generator free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 481 | ai proposal generator free online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 482 | ai proposal generator for freelancers | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 483 | ai proposal generator for upwork | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 484 | ai proposal generator online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 485 | ai proposal generator app | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 486 | ai proposal generator pdf | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 487 | ai proposal generator free download | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 488 | ai business proposal generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 489 | ai upwork proposal generator bot | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 490 | ai proposal generator online free of cost | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 491 | ai project proposal generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 492 | ai business proposal generator free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 493 | ai ad creative generator free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 494 | ai ad creative maker | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 495 | ai ad creative creator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 496 | best ai ad creative generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 497 | ai facebook ad creative generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 498 | best ai ad creative generator free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 499 | ad creative ai video generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 500 | free ai ad creative generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 501 | ai ad generator free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 502 | generate ad creatives using ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 503 | best ai ad generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 504 | ai product ad generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 505 | ai ad generator for video | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 506 | ai generator for ads | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 507 | ai generator for advertisement | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 508 | ai advertisement generator for free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 509 | ai app builder free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 510 | ai app builder free unlimited | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 511 | ai app builder no code free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 512 | ai app builder for android | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 513 | ai app builder no-code | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 514 | ai app builder for ios | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 515 | ai app builder ios | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 516 | ai app builder website | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 517 | ai app builder tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 518 | ai app builder software | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 519 | ai app builder free no code | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 520 | ai app builder online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 521 | ai app builder free domains | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 522 | ai app builder free no sign up | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 523 | ai app builder free with prompt | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 524 | ai newsletter writer free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 525 | ai news writer | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 526 | ai news writer free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 527 | ai newsletter writing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 528 | ai newsletter editor | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 529 | ai news writing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 530 | ai news writing tool | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 531 | ai news article writer | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 532 | ai news story writer | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 533 | ai infographic generator free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 534 | ai infographic generator from text | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 535 | ai infographic generator from text free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 536 | ai infographic generator free online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 537 | ai infographic generator no sign up | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 538 | ai infographic video generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 539 | ai infographic creator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 540 | free ai infographic generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 541 | best ai infographic generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 542 | shopify ai product description generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 543 | ai product description shopify app | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 544 | shopify product description builder ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 545 | chatgpt ai product description shopify | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 546 | shopify product description | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 547 | shopify product description examples | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 548 | ai product description generator shopify | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 549 | ai for shopify store | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 550 | ai shopify store design | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 551 | ai tools for shopify | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 552 | ai apps for shopify | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 553 | free shopify ai store | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 554 | ai ads for shopify | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 555 | ai ads for shopify store | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 556 | ai marketing for shopify | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 557 | shopify ai for images | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 558 | programmatic seo ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 559 | programmatic seo using ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 560 | ai agents examples | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 561 | how to create an ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 562 | ai agent for api documentation using postman | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 563 | ai agent for api documentation using python | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 564 | how to use agent ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 565 | how to create ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 566 | ai agent for data analysis | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 567 | creating an ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 568 | ai agent example code | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 569 | how to make ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 570 | ai agent to generate code | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 571 | ai agent development tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 572 | ai agent web ui | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 573 | application of ai agents | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 574 | ai sales email tool | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 575 | ai cold email software | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 576 | cold email ai tool free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 577 | ai cold email outreach | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 578 | cold email ai tool | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 579 | ai for cold emails | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 580 | cold email ai generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 581 | best cold email tool | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 582 | ai tool for email | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 583 | email ai tool free | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 584 | ai tool for mail | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 585 | ai tools for cold outreach | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 586 | ai cold calling software | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 587 | ai tools for email management | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 588 | best email ai tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 589 | ai software for email | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 590 | ai tool to write emails | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 591 | ai tool for writing emails | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 592 | how to use ai in testing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 593 | what are agent in ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 594 | ai agent for unit testing python | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 595 | ai agent for unit testing react | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 596 | ai agent for unit testing c# | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 597 | ai agent for unit testing java | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 598 | ai for unit testing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 599 | growth marketing ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 600 | how can ai help in marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 601 | ai agents for marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 602 | ai enhanced growth marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 603 | ai growth tool for marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 604 | gen ai for marketing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 605 | ai generated marketing content | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 606 | content writing ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 607 | content writer ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 608 | content writing chatgpt prompts | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 609 | ai for content writing | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 610 | email writing ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 611 | blog writing ai agent | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 612 | content writer ai free online | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 613 | answer engine optimization (aeo) | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 614 | answer engine optimization certification | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 615 | answer engine optimization vs generative engine optimization | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 616 | answer engine optimization examples | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 617 | answer engine optimization tools | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 618 | answer engine optimization course | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 619 | answer engine optimization vs geo | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 620 | answer engine optimization jobs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 621 | answer engine optimization services | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 622 | answer engine optimization tutorial | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 623 | answer engine optimization full course | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 624 | answer engine optimization hindi | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 625 | answer engine optimization malayalam | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 626 | answer engine optimization for law firms | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 627 | answer engine optimization los angeles | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 628 | answer engine optimization que es | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 629 | answer engine optimization sverige | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 630 | answer engine optimization definition | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 631 | answer engine optimization books | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 632 | answer engine optimization techniques | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 633 | google ai overview optimization services | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 634 | what is ai optimization | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 635 | google ai generative course | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 636 | google ai overview | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 637 | ai google ads optimization | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 638 | tasks entrepreneurs can automated | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 639 | daily tasks of an entrepreneur | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 640 | ai generated podcasts | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 641 | ai generated podcast intro | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 642 | ai generated podcast names | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 643 | ai that creates podcasts | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 644 | ai podcast generator notes | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 645 | ai podcast generator video | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 646 | ai podcast generator book | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 647 | generate podcast with ai | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 648 | ai summary generator podcast | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 649 | ai podcast generator for studying | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 650 | ai podcast content generator | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 651 | how to grow on tiktok 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 652 | how to go live on tiktok 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 653 | tiktok audience profile 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 654 | how to edit on tiktok 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 655 | trending on tiktok 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 656 | what's trending on tiktok 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 657 | trending videos on tiktok 2024 | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 658 | cold email at million scales | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 659 | cold email conversion rate | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 660 | cold email response rate | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 661 | cold email success rate | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 662 | data analysis early career mistakes interview | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 663 | data analysis early career mistakes interview questions | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 664 | early career data analyst | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 665 | career in data analysis | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |
| 666 | early career data analyst jobs | Tier 3 · Haiku 4 yes | Layer 3 Haiku keep (4/4 yes) | (via Haiku) | info | — | — | — | — | — |

---

## 4 · 下一步（L3+）

- **L3 主库打分**：6 维度 13 分公式给 666 词打分 + Tier 1/2/3 分档
- **L4 量化验证**：剩 ~620 词跑 KWFinder/GAKP（Mangools free 每天 25 词，需 25 天分批 / 或激活付费）
- **L5 Pillar/Cluster**：从 Tier 1 选 3 Pillar × 5 Cluster
- **L6 博客大纲**：6 篇
