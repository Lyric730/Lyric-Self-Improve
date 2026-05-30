# Round-2 · L3 主库打分 v1 · 03-master-scored

**日期**：2026-05-07
**讨论方**：小刀老师 + Agent B
**状态**：v1 final · 6 维度 13 分公式打分完成
**前置依赖**：master v0 666 + KWFinder 570 词全数据 → L3 打分

---

## 0 · 概览

| 维度 | 数值 |
|---|---|
| 主库总词数（去重）| **570** |
| 有 KWFinder 数据 | 570 |
| **Tier 1（≥9 分）** | **6** |
| **Tier 1.5（ICP 长尾·KWFinder 不覆盖）** | **58** |
| Tier 2（6-8 分）| 88 |
| Tier 3（<6 分）| 418 |

## 1 · 打分公式

| 维度 | 满分 | 规则 |
|---|---|---|
| Volume | 3 | >1000=3 / 100-1000=2 / 10-100=1 / 0或空=0 |
| KD | 3 | <20=3 / 20-40=2 / 40-60=1 / >60=0 / 空=0 |
| Intent | 2 | commercial/transactional=2 / info=1 / navigational=0 |
| Growth | 2 | >50%=2 / 0-50%=1 / <0=0 |
| ICP | 2 | direct(Pool-A meta)=2 / related(step2/3 sugg)=1 / unknown=0 |
| 产品对接 | 1 | product 字段非空=1 / 否=0 |
| **总分** | **13** | Tier 1≥9 / Tier 2: 6-8 / Tier 3: <6 |

## 2 · Tier 1 · 高优先（Pillar/Cluster 候选）（6 词）

| # | 关键词 | 总分 | Vol | KD | Intent | Growth | ICP | 产品 | SERP |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Answer Engine Optimization | **10** | 2100 (3) | 50 (1) | informatio (1) | 200% (2) | direct-product (2) | L4 验证 (1) | AI Overview, People Also  |
| 2 | Model Context Protocol | **9** | 21500 (3) | 55 (1) | commercial (2) | -35% (0) | direct-product (2) | L4 验证 (1) | AI Overview |
| 3 | AI app builder | **9** | 9600 (3) | 47 (1) | navigation (0) | 305% (2) | direct-product (2) | team App Developer (1) | AI Overview |
| 4 | Generative Engine Optimization | **9** | 4800 (3) | 66 (0) | informatio (1) | 180% (2) | direct-product (2) | L4 验证 (1) | AI Overview, People Also  |
| 5 | AI infographic generator | **9** | 1700 (3) | 37 (2) | — (1) | -40% (0) | direct-product (2) | agent Logan (Infographic Designer); team Content Marketing (1) | — |
| 6 | answer engine optimization services | **9** | 350 (2) | 19 (3) | — (1) | 909% (2) | related (1) | — (0) | AI Overview |

## 2.5 · Tier 1.5 · ICP 长尾（KWFinder 不覆盖,博客大纲候选）（58 词）

| # | 关键词 | 总分 | Vol | KD | Intent | Growth | ICP | 产品 | SERP |
|---|---|---|---|---|---|---|---|---|---|
| 1 | how to get amazon reviews without vine | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Amazon Seller; agent Alice (Review Manager) (1) | — |
| 2 | selling handmade items online platform comparison | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Artisan / DTC Brand Founder (1) | — |
| 3 | cold email metrics that matter | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer) (1) | — |
| 4 | cold email volume vs deliverability | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Lucas (Cold Outreach Pro) (1) | — |
| 5 | AI agent for PR | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Wyatt (Press Release Writer); agent Alexander (Crisis  (1) | — |
| 6 | value of media placements for clients | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Brand & PR Manager (1) | — |
| 7 | best scheduling tool for coaches | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Career & Life Coach; skill Productivity (1) | — |
| 8 | consultant powerpoint design tips | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Consultant; agent Silas (Pitch Deck Builder) (1) | — |
| 9 | traits of high performing consultant | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Consultant (1) | — |
| 10 | content marketing strategy that works 2026 | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Content Marketing Manager; agent Theodore (Content Mach (1) | — |
| 11 | AI SEO agency for product descriptions | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Sophie (SEO Doctor); agent Isaiah (SEO Content Factory (1) | — |
| 12 | how to get LLM link citations | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Sophie (SEO Doctor); skill ai-seo (1) | — |
| 13 | how to start data analysis project from scratch | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Camila (Data Interpreter); agent Jackson (Dashboard De (1) | — |
| 14 | SQL self join tutorial mental model | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | skill Data & Analytics 20 (1) | — |
| 15 | local SEO cost for small business | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Sophie (SEO Doctor); team Local Restaurant (1) | — |
| 16 | how to handle fee-sensitive prospects | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Independent Financial Advisor (1) | — |
| 17 | how to write freelance design proposals | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Freelance Designer; agent Aria (Freelance Proposal Writ (1) | — |
| 18 | why ChatGPT cites pages | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Sophie (SEO Doctor); skill ai-seo (1) | — |
| 19 | Cloudflare blocking GPTBot SEO impact | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Brooks (Website Audit Reporter); skill ai-seo (1) | — |
| 20 | buying backlinks DA score risk | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Brooks (Website Audit Reporter); skill backlink-analyz (1) | — |
| 21 | why visitors don't sign up SaaS | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team SaaS Founder; agent Luna (Conversion Optimizer) (1) | — |
| 22 | best community for SaaS builders | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team SaaS Founder (1) | — |
| 23 | React Native cross platform 2026 comparison | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team App Developer; agent Oliver (ASO Optimizer) (1) | — |
| 24 | where to advertise newsletter for subscribers | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Newsletter Creator; agent Aurora (Newsletter Curator) (1) | — |
| 25 | tips for growing small newsletter | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Newsletter Creator (1) | — |
| 26 | best social media to promote substack | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Substack/Newsletter-First Creator; agent Aurora (1) | — |
| 27 | streaming TV vs paid social ads | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Savannah (Paid Ads Strategist); agent Olivia (Ad Creat (1) | — |
| 28 | best landing page builder for PPC agencies | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Addison (Landing Page Builder); agent Savannah (Paid A (1) | — |
| 29 | podcast guest release agreement template | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Podcaster; agent Elena (Podcast Producer) (1) | — |
| 30 | AI candidate sourcing tool | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Recruiter (1) | — |
| 31 | freelance recruiter daily workflow | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Recruiter (1) | — |
| 32 | restaurant marketing on small budget | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Local Restaurant (1) | — |
| 33 | ecommerce growth strategy 2026 | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Shopify/DTC Brand (1) | — |
| 34 | shopify alternatives ecommerce platforms | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Shopify/DTC Brand (1) | — |
| 35 | how to batch create social content | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Social Media Manager; agent Harper (Content Repurposing (1) | — |
| 36 | best multi-platform social media management tool | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Social Media Manager (1) | — |
| 37 | self hosting mistakes for beginners | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Indie Hacker; skill DevOps (1) | — |
| 38 | starting Instagram from day 1 strategy | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Short Video Creator; agent Claire (Twitter Growth Pilot (1) | — |
| 39 | when to LLC YouTube channel | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team YouTube/Twitch Creator; agent Sadie (Video Producer) (1) | — |
| 40 | AI for ML research | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | Skills · Data & Analytics; team AI App Builder (1) | — |
| 41 | AI agent for API documentation | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | Skills · DevOps; team Indie Hacker (1) | — |
| 42 | AI agent for unit testing | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | Skills · Developer Tools (1) | — |
| 43 | Marketing & Growth AI agents | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | Skills · Marketing & Growth 33 (1) | — |
| 44 | Content & Writing AI agents | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | Skills · Content & Writing 24 (1) | — |
| 45 | Claude Code workflow | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | L4 验证 (1) | — |
| 46 | Claude agent skills | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | L4 验证 (1) | — |
| 47 | llms.txt SEO | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | L4 验证 (1) | — |
| 48 | Google AI Overview optimization | **4** | — (0) | — (0) | — (1) | —% (0) | direct-product (2) | L4 验证 (1) | — |
| 49 | tasks entrepreneurs can automate | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Xavier (Workflow Automator); Skills · Automation (1) | — |
| 50 | AI generated podcasts 2026 | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Podcaster; agent Elena (Podcast Producer) (1) | — |
| 51 | how to build TikTok presence in 2026 | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Short Video Creator; agent Sadie (Video Producer) (1) | — |
| 52 | YouTube video stolen on TikTok recovery | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team YouTube/Twitch Creator; agent Sadie (1) | — |
| 53 | youtuber pain points 2026 | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team YouTube/Twitch Creator (1) | — |
| 54 | cold email at million scale | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer) (1) | — |
| 55 | amazon vine review recovery | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Amazon Seller; agent Alice (Review Manager) (1) | — |
| 56 | consulting ex-consultant clients | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Consultant (1) | — |
| 57 | data analysis early career mistakes | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | agent Camila (Data Interpreter); team Indie Hacker (1) | — |
| 58 | financial advisor disengaged client management | **4** | — (0) | — (0) | — (1) | —% (0) | direct-icp (2) | team Independent Financial Advisor (1) | — |

## 3 · Tier 2 · 数据验证（Cluster 补充）（88 词）

| # | 关键词 | 总分 | Vol | KD | Intent | Growth | ICP | 产品 | SERP |
|---|---|---|---|---|---|---|---|---|---|
| 1 | online courses platforms | **8** | 86400 (3) | 46 (1) | — (1) | 1046% (2) | haiku-related (1) | — (0) | — |
| 2 | online courses platform | **8** | 86400 (3) | 43 (1) | — (1) | 1046% (2) | haiku-related (1) | — (0) | — |
| 3 | AI testing | **8** | 42800 (3) | 46 (1) | — (1) | 64% (2) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 4 | self hosting | **8** | 3600 (3) | 45 (1) | — (1) | 70% (2) | haiku-related (1) | — (0) | — |
| 5 | ai coding agent | **8** | 3000 (3) | 45 (1) | — (1) | 1236% (2) | related (1) | — (0) | AI Overview |
| 6 | amazon vine review program | **8** | 630 (2) | 31 (2) | — (1) | 160% (2) | related (1) | — (0) | — |
| 7 | AI proposal generator | **8** | 530 (2) | 34 (2) | — (1) | -50% (0) | direct-product (2) | agent Aria (Freelance Proposal Writer); team Freelance Desig (1) | People Also Ask |
| 8 | best CRM for financial advisors | **8** | 300 (2) | 33 (2) | — (1) | -43% (0) | direct-icp (2) | team Independent Financial Advisor (1) | AI Overview, People Also  |
| 9 | best platform to sell online courses | **8** | 130 (2) | 39 (2) | — (1) | -31% (0) | direct-icp (2) | team Knowledge IP Builder; agent Scarlett (Course Architect) (1) | AI Overview, People Also  |
| 10 | ai agents for project management | **8** | 120 (2) | 25 (2) | — (1) | 158% (2) | related (1) | — (0) | — |
| 11 | AI ad creative generator | **8** | 60 (1) | 45 (1) | — (1) | 75% (2) | direct-product (2) | agent Olivia (Ad Creative Studio); team Artisan/DTC (1) | People Also Ask |
| 12 | best business coaching program | **8** | 30 (1) | 36 (2) | commercial (2) | -81% (0) | direct-icp (2) | team Career & Life Coach (1) | AI Overview, People Also  |
| 13 | google ai overview | **7** | 22500 (3) | 68 (0) | — (1) | 100% (2) | related (1) | — (0) | AI Overview, People Also  |
| 14 | social media management tools | **7** | 12800 (3) | 43 (1) | — (1) | 20% (1) | haiku-related (1) | — (0) | — |
| 15 | podcast name generator | **7** | 5000 (3) | 31 (2) | — (1) | -40% (0) | haiku-related (1) | — (0) | People Also Ask |
| 16 | app builder | **7** | 4800 (3) | 59 (1) | — (1) | 20% (1) | haiku-related (1) | — (0) | People Also Ask |
| 17 | content marketing strategy | **7** | 4200 (3) | 48 (1) | informatio (1) | 32% (1) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 18 | story writer AI | **7** | 2700 (3) | 31 (2) | — (1) | -19% (0) | haiku-related (1) | — (0) | — |
| 19 | amazon vine reviewer | **7** | 1800 (3) | 31 (2) | — (1) | -58% (0) | haiku-related (1) | — (0) | — |
| 20 | ai optimization | **7** | 1600 (3) | 40 (1) | informatio (1) | 39% (1) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 21 | ai code review | **7** | 1200 (3) | 42 (1) | — (1) | 23% (1) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 22 | code review ai | **7** | 1200 (3) | 41 (1) | — (1) | 23% (1) | haiku-related (1) | — (0) | AI Overview |
| 23 | product description | **7** | 1200 (3) | 48 (1) | — (1) | 26% (1) | haiku-related (1) | — (0) | Featured Snippet |
| 24 | product placement definition | **7** | 980 (2) | 36 (2) | — (1) | 10% (1) | haiku-related (1) | — (0) | — |
| 25 | ai agent for marketing | **7** | 420 (2) | 41 (1) | — (1) | 107% (2) | related (1) | — (0) | — |
| 26 | proposal generator | **7** | 310 (2) | 15 (3) | — (1) | -44% (0) | haiku-related (1) | — (0) | — |
| 27 | media placements | **7** | 280 (2) | 15 (3) | — (1) | -31% (0) | haiku-related (1) | — (0) | Featured Snippet |
| 28 | Shopify AI tools | **7** | 140 (2) | 36 (2) | — (1) | 40% (1) | haiku-related (1) | — (0) | — |
| 29 | cold calling AI | **7** | 140 (2) | 34 (2) | — (1) | 0% (1) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 30 | cold email deliverability | **7** | 40 (1) | 17 (3) | — (1) | 50% (1) | related (1) | — (0) | AI Overview |
| 31 | AI newsletter writer | **7** | 10 (1) | 30 (2) | — (1) | -67% (0) | direct-product (2) | agent Aurora (Newsletter Curator); team Newsletter Creator (1) | — |
| 32 | programmatic SEO AI | **7** | 10 (1) | 28 (2) | — (1) | -50% (0) | direct-product (2) | agent Stella (Programmatic SEO Builder); team SaaS Founder (1) | AI Overview |
| 33 | best scheduling app for coaches | **7** | 10 (1) | 14 (3) | — (1) | 0% (1) | related (1) | — (0) | AI Overview, People Also  |
| 34 | AI agent for code review | **7** | — (0) | 34 (2) | commercial (2) | —% (0) | direct-icp (2) | Skills · Developer Tools 217 (e.g. agent-tools); team AI App (1) | AI Overview |
| 35 | AI agents | **6** | 57600 (3) | 57 (1) | navigation (0) | 22% (1) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 36 | tiktok trends | **6** | 15500 (3) | 43 (1) | — (1) | -20% (0) | haiku-related (1) | — (0) | — |
| 37 | social media management | **6** | 9000 (3) | 42 (1) | — (1) | -60% (0) | haiku-related (1) | — (0) | — |
| 38 | instagram marketing strategy | **6** | 5600 (3) | 44 (1) | informatio (1) | -66% (0) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 39 | social media strategies | **6** | 3500 (3) | 41 (1) | — (1) | -61% (0) | haiku-related (1) | — (0) | — |
| 40 | powerpoint design | **6** | 2700 (3) | 44 (1) | — (1) | -34% (0) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 41 | social media content creation | **6** | 2300 (3) | 51 (1) | — (1) | -34% (0) | haiku-related (1) | — (0) | — |
| 42 | tiktok live streaming | **6** | 2100 (3) | 40 (1) | — (1) | -9% (0) | haiku-related (1) | — (0) | — |
| 43 | social media content | **6** | 1400 (3) | 51 (1) | — (1) | -46% (0) | haiku-related (1) | — (0) | — |
| 44 | create online courses | **6** | 1200 (3) | 46 (1) | — (1) | -63% (0) | haiku-related (1) | — (0) | — |
| 45 | email writing AI | **6** | 1200 (3) | 48 (1) | — (1) | -45% (0) | haiku-related (1) | — (0) | People Also Ask |
| 46 | infographic generator free | **6** | 1100 (3) | 52 (1) | — (1) | -26% (0) | haiku-related (1) | — (0) | — |
| 47 | paid ads social media | **6** | 770 (2) | 39 (2) | — (1) | -60% (0) | related (1) | — (0) | — |
| 48 | social media paid advertising | **6** | 770 (2) | 37 (2) | — (1) | -60% (0) | related (1) | — (0) | — |
| 49 | sell online courses | **6** | 710 (2) | 38 (2) | — (1) | -41% (0) | haiku-related (1) | — (0) | — |
| 50 | sell course online | **6** | 710 (2) | 34 (2) | — (1) | -41% (0) | haiku-related (1) | — (0) | — |
| 51 | aeo vs geo | **6** | 710 (2) | — (0) | — (1) | 7150% (2) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 52 | AI agent development | **6** | 650 (2) | 51 (1) | — (1) | 37% (1) | haiku-related (1) | — (0) | AI Overview |
| 53 | amazon vine program reviews | **6** | 630 (2) | — (0) | — (1) | 160% (2) | related (1) | — (0) | — |
| 54 | product description examples | **6** | 530 (2) | 40 (1) | — (1) | 47% (1) | haiku-related (1) | — (0) | — |
| 55 | restaurant marketing strategies | **6** | 520 (2) | 31 (2) | — (1) | -47% (0) | haiku-related (1) | — (0) | — |
| 56 | marketing strategies for restaurants | **6** | 520 (2) | 39 (2) | — (1) | -47% (0) | related (1) | — (0) | — |
| 57 | marketing strategies for a restaurant | **6** | 520 (2) | 39 (2) | — (1) | -47% (0) | related (1) | — (0) | — |
| 58 | consultant skills | **6** | 350 (2) | 20 (2) | — (1) | -51% (0) | haiku-related (1) | — (0) | Featured Snippet |
| 59 | ai powered recruitment tools | **6** | 350 (2) | — (0) | — (1) | 167% (2) | related (1) | — (0) | — |
| 60 | CRM for financial advisors | **6** | 340 (2) | 39 (2) | — (1) | -32% (0) | related (1) | — (0) | — |
| 61 | ai tools for recruiting | **6** | 340 (2) | 25 (2) | — (1) | -14% (0) | related (1) | — (0) | — |
| 62 | business coaching programs | **6** | 320 (2) | 37 (2) | — (1) | -39% (0) | haiku-related (1) | — (0) | Map Pack, People Also Ask |
| 63 | shipping amazon fba | **6** | 300 (2) | 26 (2) | — (1) | -92% (0) | haiku-related (1) | — (0) | — |
| 64 | ecommerce growth strategy | **6** | 300 (2) | 27 (2) | — (1) | -70% (0) | related (1) | — (0) | — |
| 65 | cold email tool | **6** | 270 (2) | 45 (1) | — (1) | 13% (1) | haiku-related (1) | — (0) | — |
| 66 | get amazon reviews | **6** | 230 (2) | 33 (2) | — (1) | -48% (0) | haiku-related (1) | — (0) | Knowledge Graph, AI Overv |
| 67 | restaurant marketing plan | **6** | 230 (2) | 20 (2) | — (1) | -54% (0) | haiku-related (1) | — (0) | — |
| 68 | answer engine optimization tools | **6** | 230 (2) | — (0) | — (1) | 5100% (2) | related (1) | — (0) | AI Overview |
| 69 | ecommerce content strategy | **6** | 200 (2) | 31 (2) | — (1) | -46% (0) | haiku-related (1) | — (0) | — |
| 70 | amazon fba shipping cost | **6** | 190 (2) | 31 (2) | — (1) | -48% (0) | related (1) | — (0) | — |
| 71 | infographic generator AI | **6** | 190 (2) | 38 (2) | — (1) | -64% (0) | haiku-related (1) | — (0) | — |
| 72 | best ai recruiting tools | **6** | 150 (2) | 39 (2) | — (1) | -21% (0) | related (1) | — (0) | — |
| 73 | content writer ai | **6** | 140 (2) | 36 (2) | — (1) | -51% (0) | haiku-related (1) | — (0) | — |
| 74 | ai agent coding | **6** | 130 (2) | 31 (2) | — (1) | -10% (0) | haiku-related (1) | — (0) | AI Overview |
| 75 | ecommerce insights | **6** | 130 (2) | 28 (2) | — (1) | -18% (0) | related (1) | — (0) | — |
| 76 | seo description generator | **6** | 120 (2) | 38 (2) | — (1) | -62% (0) | haiku-related (1) | — (0) | — |
| 77 | use AI agent | **6** | 120 (2) | — (0) | — (1) | 100% (2) | haiku-related (1) | — (0) | — |
| 78 | best coding ai agent | **6** | 100 (2) | — (0) | — (1) | 210% (2) | related (1) | — (0) | — |
| 79 | email AI tool | **6** | 100 (2) | 31 (2) | — (1) | -44% (0) | haiku-related (1) | — (0) | Featured Snippet |
| 80 | powerpoint presentation design tips | **6** | 90 (1) | 33 (2) | — (1) | 43% (1) | related (1) | — (0) | — |
| 81 | cold email marketing services | **6** | 70 (1) | 37 (2) | — (1) | 17% (1) | related (1) | — (0) | — |
| 82 | podcast guest release form | **6** | 70 (1) | 8 (3) | — (1) | -43% (0) | related (1) | — (0) | — |
| 83 | ad video generator | **6** | 30 (1) | 49 (1) | — (1) | 100% (2) | haiku-related (1) | — (0) | — |
| 84 | answer engine optimization examples | **6** | 30 (1) | 49 (1) | — (1) | 400% (2) | related (1) | — (0) | AI Overview, People Also  |
| 85 | cold email marketing strategy | **6** | 10 (1) | 33 (2) | — (1) | 50% (1) | related (1) | — (0) | — |
| 86 | best scheduling software for coaches | **6** | 10 (1) | 33 (2) | — (1) | 0% (1) | related (1) | — (0) | AI Overview, People Also  |
| 87 | product description generator Shopify | **6** | 10 (1) | 24 (2) | — (1) | 0% (1) | haiku-related (1) | — (0) | — |
| 88 | AI cold email tool | **6** | — (0) | 36 (2) | — (1) | —% (0) | direct-product (2) | agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer) (1) | — |

## 4 · Tier 3 · 长尾（前 50 词预览，完整见 JSON）（50 词）

| # | 关键词 | 总分 | Vol | KD | Intent | Growth | ICP | 产品 | SERP |
|---|---|---|---|---|---|---|---|---|---|
| 1 | seo website | **5** | 11300 (3) | 65 (0) | — (1) | -70% (0) | haiku-related (1) | — (0) | — |
| 2 | create AI agent | **5** | 860 (2) | — (0) | — (1) | 31% (1) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 3 | sell courses online | **5** | 710 (2) | 41 (1) | — (1) | -41% (0) | haiku-related (1) | — (0) | — |
| 4 | online course website | **5** | 700 (2) | 48 (1) | — (1) | -74% (0) | haiku-related (1) | — (0) | — |
| 5 | ad generator | **5** | 600 (2) | 48 (1) | — (1) | -31% (0) | haiku-related (1) | — (0) | — |
| 6 | best landing page builder | **5** | 520 (2) | 55 (1) | — (1) | -31% (0) | haiku-related (1) | — (0) | — |
| 7 | marketing for restaurants strategies | **5** | 520 (2) | 40 (1) | — (1) | -47% (0) | related (1) | — (0) | — |
| 8 | restaurant marketing strategy | **5** | 520 (2) | 40 (1) | — (1) | -47% (0) | haiku-related (1) | — (0) | — |
| 9 | google ads optimization | **5** | 500 (2) | 41 (1) | — (1) | -33% (0) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 10 | professional powerpoint | **5** | 470 (2) | 54 (1) | — (1) | -40% (0) | haiku-related (1) | — (0) | — |
| 11 | tiktok viral videos | **5** | 440 (2) | 44 (1) | — (1) | -26% (0) | haiku-related (1) | — (0) | — |
| 12 | ecommerce marketing strategy | **5** | 380 (2) | 43 (1) | — (1) | -51% (0) | haiku-related (1) | — (0) | — |
| 13 | vine reviews amazon | **5** | 250 (2) | — (0) | — (1) | 24% (1) | haiku-related (1) | — (0) | — |
| 14 | content marketing trends | **5** | 240 (2) | 50 (1) | — (1) | -62% (0) | haiku-related (1) | — (0) | — |
| 15 | online courses wordpress | **5** | 200 (2) | 56 (1) | — (1) | -11% (0) | haiku-related (1) | — (0) | — |
| 16 | code ai agents | **5** | 150 (2) | — (0) | — (1) | 10% (1) | haiku-related (1) | — (0) | — |
| 17 | grow tiktok | **5** | 140 (2) | 59 (1) | — (1) | -39% (0) | haiku-related (1) | — (0) | People Also Ask |
| 18 | tiktok video editing | **5** | 120 (2) | 41 (1) | — (1) | -35% (0) | haiku-related (1) | — (0) | — |
| 19 | AI agent creation | **5** | 100 (2) | — (0) | — (1) | 28% (1) | haiku-related (1) | — (0) | — |
| 20 | email AI tools | **5** | 100 (2) | 41 (1) | — (1) | -44% (0) | haiku-related (1) | — (0) | — |
| 21 | powerpoint design tips | **5** | 90 (1) | 33 (2) | — (1) | -25% (0) | haiku-related (1) | — (0) | — |
| 22 | cold email AI | **5** | 90 (1) | 33 (2) | — (1) | -58% (0) | haiku-related (1) | — (0) | — |
| 23 | ai agent for productivity | **5** | 80 (1) | — (0) | — (1) | 540% (2) | related (1) | — (0) | — |
| 24 | seo product descriptions | **5** | 80 (1) | 36 (2) | — (1) | -89% (0) | haiku-related (1) | — (0) | — |
| 25 | ai sourcing tools for recruiting | **5** | 70 (1) | — (0) | — (1) | 257% (2) | related (1) | — (0) | — |
| 26 | paid social media advertising services | **5** | 60 (1) | 33 (2) | — (1) | -75% (0) | related (1) | — (0) | — |
| 27 | ai tools for recruiters | **5** | 60 (1) | 23 (2) | — (1) | -33% (0) | related (1) | — (0) | — |
| 28 | restaurant local marketing | **5** | 60 (1) | 25 (2) | — (1) | -44% (0) | haiku-related (1) | — (0) | — |
| 29 | restaurant marketing budget | **5** | 60 (1) | 24 (2) | — (1) | -76% (0) | haiku-related (1) | — (0) | — |
| 30 | best executive coaching programs | **5** | 50 (1) | 45 (1) | — (1) | 0% (1) | related (1) | — (0) | — |
| 31 | best CRM software for financial advisors | **5** | 50 (1) | 26 (2) | — (1) | -46% (0) | related (1) | — (0) | — |
| 32 | best financial advisor CRM software | **5** | 50 (1) | 35 (2) | — (1) | -46% (0) | related (1) | — (0) | — |
| 33 | podcast guest release form template | **5** | 50 (1) | — (0) | — (1) | 78% (2) | related (1) | — (0) | — |
| 34 | cold email marketing tools | **5** | 40 (1) | 45 (1) | — (1) | 11% (1) | related (1) | — (0) | — |
| 35 | ppc landing pages | **5** | 40 (1) | 25 (2) | — (1) | -54% (0) | haiku-related (1) | — (0) | — |
| 36 | Shopify AI apps | **5** | 40 (1) | 21 (2) | — (1) | -11% (0) | haiku-related (1) | — (0) | — |
| 37 | gen ai marketing | **5** | 40 (1) | — (0) | — (1) | 63% (2) | haiku-related (1) | — (0) | — |
| 38 | best business coaching programs | **5** | 30 (1) | 25 (2) | — (1) | -81% (0) | related (1) | — (0) | — |
| 39 | grow newsletter | **5** | 30 (1) | 29 (2) | — (1) | -25% (0) | haiku-related (1) | — (0) | — |
| 40 | ad creative generator | **5** | 30 (1) | 39 (2) | — (1) | -33% (0) | haiku-related (1) | — (0) | — |
| 41 | answer engine optimization course | **5** | 30 (1) | — (0) | — (1) | 100% (2) | related (1) | — (0) | — |
| 42 | bito ai code review agent | **5** | 20 (1) | — (0) | — (1) | 150% (2) | related (1) | — (0) | — |
| 43 | dropshipping amazon fba | **5** | 20 (1) | 39 (2) | — (1) | -87% (0) | haiku-related (1) | — (0) | — |
| 44 | ai agent for programming | **5** | 20 (1) | — (0) | — (1) | 133% (2) | related (1) | — (0) | — |
| 45 | ai agents for programming | **5** | 20 (1) | — (0) | — (1) | 133% (2) | related (1) | — (0) | — |
| 46 | consulting powerpoint templates free | **5** | 20 (1) | 28 (2) | — (1) | -43% (0) | related (1) | — (0) | — |
| 47 | paid social media advertising strategy | **5** | 20 (1) | 39 (2) | — (1) | -64% (0) | related (1) | — (0) | — |
| 48 | unit testing AI | **5** | 20 (1) | 27 (2) | — (1) | -60% (0) | haiku-related (1) | — (0) | — |
| 49 | ai growth marketing | **5** | 20 (1) | — (0) | — (1) | 67% (2) | haiku-related (1) | — (0) | AI Overview, People Also  |
| 50 | small restaurant marketing strategies | **5** | 10 (1) | — (0) | — (1) | -82% (0) | direct-icp (2) | team Local Restaurant; agent Leo (Local Event Planner) (1) | — |

_Tier 3 完整 418 词见 `data/master_scored.json`_

---

## 5 · 下一步（L4-L7）

- **L4 量化验证**：Tier 1 词全部跑 KWFinder/SERP 二次检（找 SERP 上的真竞品 + AI Overview 占用情况）
- **L5 Pillar/Cluster**：从 Tier 1 选 3 Pillar × 5 Cluster
- **L6 博客大纲**：6 篇
- **L7 精排 + handoff**：final 输出 + 下一轮研究方向
