# yolox URL 主清单（路径式）

> **用途**：blog 内链时**唯一权威 URL 源**。所有 agent / skill / team / category 链接从此处取，不允许现编。
> **日期**：2026-05-15
> **数据来源**：直接从 yolox 生产 manifest 拉取
> - agents: `Infinite-Flow-Labs/yolox-agent-store/manifests/agents.json` · 110 个（隐藏 3 个，可见 **107**）
> - skills: `Infinite-Flow-Labs/yolox-skills-store/manifests/skills.json` · **414** 个
> - teams: `Infinite-Flow-Labs/yolox-agent-store/manifests/teams.json` · **36** 个

---

## 目录

1. [§1 顶级 catalog URL](#1--catalog-url3-)
2. [§2 分类 URL（待 Path B 路由实现）](#2--url-path-b-)
3. [§3 SEO 相关 shortlist（L6-01 优先用）](#3--seo--shortlist)
4. [§4 Agent 详情页 URL（107 个）](#4--agent--url107-)
5. [§5 Skill 详情页 URL（414 个）](#5--skill--url414-)
6. [§6 Team 详情页 URL（36 个）](#6--team--url36-)
7. [§7 URL 格式规则 & 隐忧](#7--url---)

---

## §1 · 顶级 catalog URL（3 个）

✅ **已有**，可立即使用：

| 资产类型 | URL | 说明 |
|---|---|---|
| Agents 总列表 | https://yolox.ai/agents-store | 110 个 agent 网格 + 12 类 filter |
| Skills 总列表 | https://yolox.ai/skills-store | 414 个 skill |
| Teams 总列表 | https://yolox.ai/teams-store | 36 个团队 |

**SEO 建议**：blog 文中 "see all yolox agents" 这种**笼统锚文本**才链顶级页。**具体功能**链具体 agent/skill 详情。

---

## §2 · 分类 URL（待 Path B 路由实现）

⚠️ **现在不存在**——需要新增 1 个动态路由文件 `/agents-store/category/[category]/page.tsx`（约 30min dev）。Blog 可先把这些 URL **写进 markdown**，dev 完成后激活。

### Agents 分类（12 个）

| 分类 | 内含 agent 数 | URL（path-style）|
|---|---|---|
| Brand | 8 | https://yolox.ai/agents-store/category/brand |
| Business | 17 | https://yolox.ai/agents-store/category/business |
| E-Commerce | 11 | https://yolox.ai/agents-store/category/e-commerce |
| Education | 2 | https://yolox.ai/agents-store/category/education |
| Finance | 4 | https://yolox.ai/agents-store/category/finance |
| Growth | 14 | https://yolox.ai/agents-store/category/growth |
| Media | 11 | https://yolox.ai/agents-store/category/media |
| Operations | 9 | https://yolox.ai/agents-store/category/operations |
| Research | 8 | https://yolox.ai/agents-store/category/research |
| Sales | 10 | https://yolox.ai/agents-store/category/sales |
| Social | 7 | https://yolox.ai/agents-store/category/social |
| Writing | 9 | https://yolox.ai/agents-store/category/writing |

### Skills 分类（11 个）

| 分类 | 内含 skill 数 | URL（path-style）|
|---|---|---|
| Automation | 3 | https://yolox.ai/skills-store/category/automation |
| Content & Writing | 24 | https://yolox.ai/skills-store/category/content-writing |
| Data & Analytics | 20 | https://yolox.ai/skills-store/category/data-analytics |
| Design & Creative | 54 | https://yolox.ai/skills-store/category/design-creative |
| DevOps & Infrastructure | 13 | https://yolox.ai/skills-store/category/devops-infrastructure |
| Developer Tools | 217 | https://yolox.ai/skills-store/category/developer-tools |
| Finance & Legal | 2 | https://yolox.ai/skills-store/category/finance-legal |
| Marketing | 3 | https://yolox.ai/skills-store/category/marketing |
| Marketing & Growth | 30 | https://yolox.ai/skills-store/category/marketing-growth |
| Productivity | 47 | https://yolox.ai/skills-store/category/productivity |
| Sales & CRM | 1 | https://yolox.ai/skills-store/category/sales-crm |

### Teams 分类（7 个）

| 分类 | 内含 team 数 | URL（path-style）|
|---|---|---|
| Content | 8 | https://yolox.ai/teams-store/category/content |
| Developer | 5 | https://yolox.ai/teams-store/category/developer |
| E-Commerce | 4 | https://yolox.ai/teams-store/category/ecommerce |
| Finance | 1 | https://yolox.ai/teams-store/category/finance |
| In-House | 6 | https://yolox.ai/teams-store/category/in-house |
| Service | 7 | https://yolox.ai/teams-store/category/service |
| Vertical | 5 | https://yolox.ai/teams-store/category/vertical |

---

## §3 · SEO 相关 shortlist（L6-01 / 4 AEO Pillar 优先用）

⭐ **AEO / SEO 主题 blog 内链时优先选这些**。它们的 URL slug 直接含 "seo"，关键词匹配度最高。

### Skills（5 个，全在 Marketing & Growth 分类）

| Skill | URL | 用在 |
|---|---|---|
| **ai-seo** | https://yolox.ai/skills-store/marketing-growth__ai-seo | AEO / GEO 主题（最匹配）|
| **seo-audit** | https://yolox.ai/skills-store/marketing-growth__seo-audit | "audit existing content" 段落 |
| **seo-geo** | https://yolox.ai/skills-store/marketing-growth__seo-geo | GEO 概念解释段 |
| **programmatic-seo** | https://yolox.ai/skills-store/marketing-growth__programmatic-seo | scale 内容生产段 |
| **content-strategy** | https://yolox.ai/skills-store/marketing-growth__content-strategy | content planning 段 |
| **schema-markup** | https://yolox.ai/skills-store/marketing-growth__schema-markup | JSON-LD / Schema 段 |

### Agents（4 个，全在 Growth 分类）

| Agent | URL | 用在 |
|---|---|---|
| **SEO Doctor** | https://yolox.ai/agents-store/seo-doctor | "diagnose SEO issues" 段 |
| **SEO Content Factory** | https://yolox.ai/agents-store/seo-content-factory | "scale content production" 段 |
| **Programmatic SEO Builder** | https://yolox.ai/agents-store/programmatic-seo-builder | programmatic SEO 落地段 |
| **AI Content Pipeline Manager** | https://yolox.ai/agents-store/ai-content-pipeline-manager | content ops 段（Operations 分类）|
| **Website Audit Reporter** | https://yolox.ai/agents-store/website-audit-reporter | "audit your site" 段 |

### 锚文本建议

| 锚文本类型 | 例 | 链到 |
|---|---|---|
| 精准锚 | "AI SEO skill" | https://yolox.ai/skills-store/marketing-growth__ai-seo |
| 部分锚 | "yolox SEO Doctor agent" | https://yolox.ai/agents-store/seo-doctor |
| 品牌锚 | "yolox" | https://yolox.ai/agents-store |
| 通用锚 | "see yolox marketing agents" | https://yolox.ai/agents-store/category/growth（待路由）|

---

## §4 · Agent 详情页 URL（107 个）

> **URL 模式**：`/agents-store/{role-slug}`
> **数据来源**：manifest `.agents[].id`，去除 `__info` 后缀
> **route 验证**：`getAgentById` 会自动 split `__` 取前缀匹配，所以**两种写法都通**（推荐 clean 形）：
> - ✅ https://yolox.ai/agents-store/crisis-pr-advisor ← blog 用这个
> - ⚠️ https://yolox.ai/agents-store/crisis-pr-advisor__info ← 内部代码用的，blog 不用（含 `__` 不利 SEO）

### Brand (8)

| Role Title | URL |
|---|---|
| Brand Guidelines Builder | https://yolox.ai/agents-store/brand-guidelines-builder |
| Brand Identity Manager | https://yolox.ai/agents-store/brand-identity-manager |
| Crisis Pr Advisor | https://yolox.ai/agents-store/crisis-pr-advisor |
| Infographic Designer | https://yolox.ai/agents-store/infographic-designer |
| Personal Brand Advisor | https://yolox.ai/agents-store/personal-brand-advisor |
| Portfolio Curator | https://yolox.ai/agents-store/portfolio-curator |
| Press Release Writer | https://yolox.ai/agents-store/press-release-writer |
| Social Share Card Designer | https://yolox.ai/agents-store/social-share-card-designer |

### Business (17)

| Role Title | URL |
|---|---|
| A/B Test Strategist | https://yolox.ai/agents-store/ab-test-strategist |
| Budget Planner | https://yolox.ai/agents-store/budget-planner |
| Contract Drafter | https://yolox.ai/agents-store/contract-drafter |
| Cross Border Ecom Copywriter | https://yolox.ai/agents-store/cross-border-ecom-copywriter |
| Financial Report Builder | https://yolox.ai/agents-store/financial-report-builder |
| Freelance Proposal Writer | https://yolox.ai/agents-store/freelance-proposal-writer |
| Hello World | https://yolox.ai/agents-store/hello-world |
| Investor Pitch Builder | https://yolox.ai/agents-store/investor-pitch-builder |
| Job Posting Writer | https://yolox.ai/agents-store/job-posting-writer |
| Multilingual Translator | https://yolox.ai/agents-store/multilingual-translator |
| Onboarding Guide Builder | https://yolox.ai/agents-store/onboarding-guide-builder |
| Pitch Deck Builder | https://yolox.ai/agents-store/pitch-deck-builder |
| Pricing Advisor | https://yolox.ai/agents-store/pricing-advisor |
| Privacy Policy Generator | https://yolox.ai/agents-store/privacy-policy-generator |
| Product Hunt Commander | https://yolox.ai/agents-store/product-hunt-commander |
| Quiz Exam Builder | https://yolox.ai/agents-store/quiz-exam-builder |
| Reply Copilot | https://yolox.ai/agents-store/reply-copilot |

### E-Commerce (11)

| Role Title | URL |
|---|---|
| TikTok Content Creator | https://yolox.ai/agents-store/tiktok-content-creator |
| Local Event Planner | https://yolox.ai/agents-store/local-event-planner |
| Product Listing Copywriter | https://yolox.ai/agents-store/product-listing-copywriter |
| Product Photo Director | https://yolox.ai/agents-store/product-photo-director |
| TikTok Product Selector | https://yolox.ai/agents-store/tiktok-product-selector |
| Promo Campaign Planner | https://yolox.ai/agents-store/promo-campaign-planner |
| Property Listing Writer | https://yolox.ai/agents-store/property-listing-writer |
| Review Manager | https://yolox.ai/agents-store/review-manager |
| TikTok Ads Operator | https://yolox.ai/agents-store/tiktok-ads-operator |
| TikTok Affiliate Manager | https://yolox.ai/agents-store/tiktok-affiliate-manager |
| TikTok Data Analyst | https://yolox.ai/agents-store/tiktok-data-analyst |

### Education (2)

| Role Title | URL |
|---|---|
| Course Architect | https://yolox.ai/agents-store/course-architect |
| Student Feedback Analyst | https://yolox.ai/agents-store/student-feedback-analyst |

### Finance (1 可见)

| Role Title | URL |
|---|---|
| Industry Researcher | https://yolox.ai/agents-store/industry-researcher |

> 注：原 Finance 类 4 个 agent，3 个已在 `HIDDEN_AGENT_IDS` 隐藏（quant-analysis-assistant / financial-content-editor / financial-social-media）。

### Growth (14) ⭐ SEO 相关聚集地

| Role Title | URL |
|---|---|
| ASO Optimizer | https://yolox.ai/agents-store/aso-optimizer |
| Ad Creative Studio | https://yolox.ai/agents-store/ad-creative-studio |
| Brand Collab Planner | https://yolox.ai/agents-store/brand-collab-planner |
| Free Tool Lead Gen Planner | https://yolox.ai/agents-store/free-tool-lead-gen-planner |
| Holiday Campaign Planner | https://yolox.ai/agents-store/holiday-campaign-planner |
| Landing Page Builder | https://yolox.ai/agents-store/landing-page-builder |
| Launch Strategist | https://yolox.ai/agents-store/launch-strategist |
| Paid Ads Strategist | https://yolox.ai/agents-store/paid-ads-strategist |
| **Programmatic SEO Builder** | https://yolox.ai/agents-store/programmatic-seo-builder |
| Referral Architect | https://yolox.ai/agents-store/referral-architect |
| **SEO Content Factory** | https://yolox.ai/agents-store/seo-content-factory |
| **SEO Doctor** | https://yolox.ai/agents-store/seo-doctor |
| Traffic Commander | https://yolox.ai/agents-store/traffic-commander |
| Website Audit Reporter | https://yolox.ai/agents-store/website-audit-reporter |

### Media (11)

| Role Title | URL |
|---|---|
| Article Illustrator | https://yolox.ai/agents-store/article-illustrator |
| Bgm Curator | https://yolox.ai/agents-store/bgm-curator |
| Carousel Designer | https://yolox.ai/agents-store/carousel-designer |
| Comic Strip Creator | https://yolox.ai/agents-store/comic-strip-creator |
| Explainer Video Director | https://yolox.ai/agents-store/explainer-video-director |
| Podcast Producer | https://yolox.ai/agents-store/podcast-producer |
| Talking Head Video Coach | https://yolox.ai/agents-store/talking-head-video-coach |
| Video Producer | https://yolox.ai/agents-store/video-producer |
| Visual Creator | https://yolox.ai/agents-store/visual-creator |
| Voiceover Workshop | https://yolox.ai/agents-store/voiceover-workshop |
| Youtube Thumbnail Studio | https://yolox.ai/agents-store/youtube-thumbnail-studio |

### Operations (9)

| Role Title | URL |
|---|---|
| **AI Content Pipeline Manager** | https://yolox.ai/agents-store/ai-content-pipeline-manager |
| Doc Assistant | https://yolox.ai/agents-store/doc-assistant |
| Feature Announcement Writer | https://yolox.ai/agents-store/feature-announcement-writer |
| In App Copy Writer | https://yolox.ai/agents-store/in-app-copy-writer |
| Internal Comms Writer | https://yolox.ai/agents-store/internal-comms-writer |
| Knowledge Librarian | https://yolox.ai/agents-store/knowledge-librarian |
| Meeting Scribe | https://yolox.ai/agents-store/meeting-scribe |
| Weekly Report Writer | https://yolox.ai/agents-store/weekly-report-writer |
| Workflow Automator | https://yolox.ai/agents-store/workflow-automator |

### Research (8)

| Role Title | URL |
|---|---|
| Competitor Scout | https://yolox.ai/agents-store/competitor-scout |
| Dashboard Designer | https://yolox.ai/agents-store/dashboard-designer |
| Data Interpreter | https://yolox.ai/agents-store/data-interpreter |
| Info Radar | https://yolox.ai/agents-store/info-radar |
| Market Researcher | https://yolox.ai/agents-store/market-researcher |
| Revops Analyst | https://yolox.ai/agents-store/revops-analyst |
| Survey Designer | https://yolox.ai/agents-store/survey-designer |
| User Interview Coach | https://yolox.ai/agents-store/user-interview-coach |

### Sales (10)

| Role Title | URL |
|---|---|
| Churn Prevention Guard | https://yolox.ai/agents-store/churn-prevention-guard |
| Cold Outreach Pro | https://yolox.ai/agents-store/cold-outreach-pro |
| Community Script Library | https://yolox.ai/agents-store/community-script-library |
| Conversion Optimizer | https://yolox.ai/agents-store/conversion-optimizer |
| Email Closer | https://yolox.ai/agents-store/email-closer |
| Membership System Designer | https://yolox.ai/agents-store/membership-system-designer |
| Onboarding Designer | https://yolox.ai/agents-store/onboarding-designer |
| Paywall Tuner | https://yolox.ai/agents-store/paywall-tuner |
| Popup Strategist | https://yolox.ai/agents-store/popup-strategist |
| Sales Enablement Kit | https://yolox.ai/agents-store/sales-enablement-kit |

### Social (7)

| Role Title | URL |
|---|---|
| Cn Social Syndicator | https://yolox.ai/agents-store/cn-social-syndicator |
| LinkedIn B2B Builder | https://yolox.ai/agents-store/linkedin-b2b-builder |
| Twitter Growth Pilot | https://yolox.ai/agents-store/twitter-growth-pilot |
| Twitter Thread Writer | https://yolox.ai/agents-store/twitter-thread-writer |
| Wechat Publisher | https://yolox.ai/agents-store/wechat-publisher |
| Weibo Rapid Poster | https://yolox.ai/agents-store/weibo-rapid-poster |
| Xiaohongshu Creator | https://yolox.ai/agents-store/xiaohongshu-creator |

### Writing (9)

| Role Title | URL |
|---|---|
| Case Study Writer | https://yolox.ai/agents-store/case-study-writer |
| Content Machine | https://yolox.ai/agents-store/content-machine |
| Content Repurposing Engine | https://yolox.ai/agents-store/content-repurposing-engine |
| Copy Polisher | https://yolox.ai/agents-store/copy-polisher |
| E Book Producer | https://yolox.ai/agents-store/e-book-producer |
| Newsletter Curator | https://yolox.ai/agents-store/newsletter-curator |
| Product Review Writer | https://yolox.ai/agents-store/product-review-writer |
| Speech Writer | https://yolox.ai/agents-store/speech-writer |
| Whitepaper Writer | https://yolox.ai/agents-store/whitepaper-writer |

---

## §5 · Skill 详情页 URL（414 个）

> **URL 模式**：`/skills-store/{category-slug}__{skill-name}`
> ⚠️ **重要**：skill 路由**只接受完整 `category__name` 格式**（不像 agent 能容忍短形）。`__` 必须保留。
> **数据来源**：manifest `.skills[].name`，category 来自 `.skills[].tag` 经 slugify

### Automation (3)

| Skill | URL |
|---|---|
| omc | https://yolox.ai/skills-store/automation__omc |
| parallel-task | https://yolox.ai/skills-store/automation__parallel-task |
| parallel-task-spark | https://yolox.ai/skills-store/automation__parallel-task-spark |

### Content & Writing (24)

| Skill | URL |
|---|---|
| baoyu-format-markdown | https://yolox.ai/skills-store/content-writing__baoyu-format-markdown |
| comment-code-generate-a-tutorial | https://yolox.ai/skills-store/content-writing__comment-code-generate-a-tutorial |
| convert-plaintext-to-md | https://yolox.ai/skills-store/content-writing__convert-plaintext-to-md |
| copy-editing | https://yolox.ai/skills-store/content-writing__copy-editing |
| copywriting | https://yolox.ai/skills-store/content-writing__copywriting |
| create-tldr-page | https://yolox.ai/skills-store/content-writing__create-tldr-page |
| csharp-docs | https://yolox.ai/skills-store/content-writing__csharp-docs |
| doc-coauthoring | https://yolox.ai/skills-store/content-writing__doc-coauthoring |
| documentation-writer | https://yolox.ai/skills-store/content-writing__documentation-writer |
| docx | https://yolox.ai/skills-store/content-writing__docx |
| finnish-humanizer | https://yolox.ai/skills-store/content-writing__finnish-humanizer |
| humanizer-zh | https://yolox.ai/skills-store/content-writing__humanizer-zh |
| internal-comms | https://yolox.ai/skills-store/content-writing__internal-comms |
| markdown-to-html | https://yolox.ai/skills-store/content-writing__markdown-to-html |
| markdown-url | https://yolox.ai/skills-store/content-writing__markdown-url |
| mkdocs-translations | https://yolox.ai/skills-store/content-writing__mkdocs-translations |
| next-intl-add-language | https://yolox.ai/skills-store/content-writing__next-intl-add-language |
| prd | https://yolox.ai/skills-store/content-writing__prd |
| readme-blueprint-generator | https://yolox.ai/skills-store/content-writing__readme-blueprint-generator |
| technical-writing | https://yolox.ai/skills-store/content-writing__technical-writing |
| tldr-prompt | https://yolox.ai/skills-store/content-writing__tldr-prompt |
| update-oo-component-documentation | https://yolox.ai/skills-store/content-writing__update-oo-component-documentation |
| update-specification | https://yolox.ai/skills-store/content-writing__update-specification |
| user-guide-writing | https://yolox.ai/skills-store/content-writing__user-guide-writing |

### Data & Analytics (20)

| Skill | URL |
|---|---|
| analytics-tracking | https://yolox.ai/skills-store/data-analytics__analytics-tracking |
| bigquery-pipeline-audit | https://yolox.ai/skills-store/data-analytics__bigquery-pipeline-audit |
| copilot-usage-metrics | https://yolox.ai/skills-store/data-analytics__copilot-usage-metrics |
| create-spring-boot-kotlin-project | https://yolox.ai/skills-store/data-analytics__create-spring-boot-kotlin-project |
| create-web-form | https://yolox.ai/skills-store/data-analytics__create-web-form |
| data-analysis | https://yolox.ai/skills-store/data-analytics__data-analysis |
| fabric-lakehouse | https://yolox.ai/skills-store/data-analytics__fabric-lakehouse |
| log-analysis | https://yolox.ai/skills-store/data-analytics__log-analysis |
| looker-studio-bigquery | https://yolox.ai/skills-store/data-analytics__looker-studio-bigquery |
| neon-postgres | https://yolox.ai/skills-store/data-analytics__neon-postgres |
| postgresql-table-design | https://yolox.ai/skills-store/data-analytics__postgresql-table-design |
| power-bi-dax-optimization | https://yolox.ai/skills-store/data-analytics__power-bi-dax-optimization |
| power-bi-model-design-review | https://yolox.ai/skills-store/data-analytics__power-bi-model-design-review |
| power-bi-performance-troubleshooting | https://yolox.ai/skills-store/data-analytics__power-bi-performance-troubleshooting |
| powerbi-modeling | https://yolox.ai/skills-store/data-analytics__powerbi-modeling |
| shuffle-json-data | https://yolox.ai/skills-store/data-analytics__shuffle-json-data |
| snowflake-semanticview | https://yolox.ai/skills-store/data-analytics__snowflake-semanticview |
| supabase-postgres-best-practices | https://yolox.ai/skills-store/data-analytics__supabase-postgres-best-practices |
| web-search | https://yolox.ai/skills-store/data-analytics__web-search |
| xlsx | https://yolox.ai/skills-store/data-analytics__xlsx |

### Design & Creative (54)

| Skill | URL |
|---|---|
| agent-ui | https://yolox.ai/skills-store/design-creative__agent-ui |
| ai-image-generation | https://yolox.ai/skills-store/design-creative__ai-image-generation |
| ai-video-generation | https://yolox.ai/skills-store/design-creative__ai-video-generation |
| algorithmic-art | https://yolox.ai/skills-store/design-creative__algorithmic-art |
| baoyu-article-illustrator | https://yolox.ai/skills-store/design-creative__baoyu-article-illustrator |
| baoyu-comic | https://yolox.ai/skills-store/design-creative__baoyu-comic |
| baoyu-cover-image | https://yolox.ai/skills-store/design-creative__baoyu-cover-image |
| baoyu-image-gen | https://yolox.ai/skills-store/design-creative__baoyu-image-gen |
| baoyu-infographic | https://yolox.ai/skills-store/design-creative__baoyu-infographic |
| baoyu-slide-deck | https://yolox.ai/skills-store/design-creative__baoyu-slide-deck |
| brand-guidelines | https://yolox.ai/skills-store/design-creative__brand-guidelines |
| building-native-ui | https://yolox.ai/skills-store/design-creative__building-native-ui |
| canvas-design | https://yolox.ai/skills-store/design-creative__canvas-design |
| database-schema-design | https://yolox.ai/skills-store/design-creative__database-schema-design |
| dataverse-python-quickstart | https://yolox.ai/skills-store/design-creative__dataverse-python-quickstart |
| dataverse-python-usecase-builder | https://yolox.ai/skills-store/design-creative__dataverse-python-usecase-builder |
| debian-linux-triage | https://yolox.ai/skills-store/design-creative__debian-linux-triage |
| design-md | https://yolox.ai/skills-store/design-creative__design-md |
| enhance-prompt | https://yolox.ai/skills-store/design-creative__enhance-prompt |
| excalidraw-diagram-generator | https://yolox.ai/skills-store/design-creative__excalidraw-diagram-generator |
| expo-tailwind-setup | https://yolox.ai/skills-store/design-creative__expo-tailwind-setup |
| flutter-animations | https://yolox.ai/skills-store/design-creative__flutter-animations |
| frontend-design | https://yolox.ai/skills-store/design-creative__frontend-design |
| frontend-design-system | https://yolox.ai/skills-store/design-creative__frontend-design-system |
| image-manipulation-image-magick | https://yolox.ai/skills-store/design-creative__image-manipulation-image-magick |
| interface-design | https://yolox.ai/skills-store/design-creative__interface-design |
| legacy-circuit-mockups | https://yolox.ai/skills-store/design-creative__legacy-circuit-mockups |
| make-repo-contribution | https://yolox.ai/skills-store/design-creative__make-repo-contribution |
| make-skill-template | https://yolox.ai/skills-store/design-creative__make-skill-template |
| mcp-create-adaptive-cards | https://yolox.ai/skills-store/design-creative__mcp-create-adaptive-cards |
| mobile-ios-design | https://yolox.ai/skills-store/design-creative__mobile-ios-design |
| nano-banana | https://yolox.ai/skills-store/design-creative__nano-banana |
| nano-banana-2 | https://yolox.ai/skills-store/design-creative__nano-banana-2 |
| nano-banana-pro-openrouter | https://yolox.ai/skills-store/design-creative__nano-banana-pro-openrouter |
| penpot-uiux-design | https://yolox.ai/skills-store/design-creative__penpot-uiux-design |
| plantuml-ascii | https://yolox.ai/skills-store/design-creative__plantuml-ascii |
| power-bi-report-design-consultation | https://yolox.ai/skills-store/design-creative__power-bi-report-design-consultation |
| pptx | https://yolox.ai/skills-store/design-creative__pptx |
| pptx-presentation-builder | https://yolox.ai/skills-store/design-creative__pptx-presentation-builder |
| qwen-image-2 | https://yolox.ai/skills-store/design-creative__qwen-image-2 |
| qwen-image-2-pro | https://yolox.ai/skills-store/design-creative__qwen-image-2-pro |
| remotion | https://yolox.ai/skills-store/design-creative__remotion |
| remotion-video-production | https://yolox.ai/skills-store/design-creative__remotion-video-production |
| responsive-design | https://yolox.ai/skills-store/design-creative__responsive-design |
| slack-gif-creator | https://yolox.ai/skills-store/design-creative__slack-gif-creator |
| sleek-design-mobile-apps | https://yolox.ai/skills-store/design-creative__sleek-design-mobile-apps |
| stitch-loop | https://yolox.ai/skills-store/design-creative__stitch-loop |
| swiftui-expert-skill | https://yolox.ai/skills-store/design-creative__swiftui-expert-skill |
| tailwind-design-system | https://yolox.ai/skills-store/design-creative__tailwind-design-system |
| theme-factory | https://yolox.ai/skills-store/design-creative__theme-factory |
| ui-ux-pro-max | https://yolox.ai/skills-store/design-creative__ui-ux-pro-max |
| videoagent-video-studio | https://yolox.ai/skills-store/design-creative__videoagent-video-studio |
| web-design-guidelines | https://yolox.ai/skills-store/design-creative__web-design-guidelines |
| web-design-reviewer | https://yolox.ai/skills-store/design-creative__web-design-reviewer |

### DevOps & Infrastructure (13)

| Skill | URL |
|---|---|
| agent-governance | https://yolox.ai/skills-store/devops-infrastructure__agent-governance |
| arch-linux-triage | https://yolox.ai/skills-store/devops-infrastructure__arch-linux-triage |
| aspire | https://yolox.ai/skills-store/devops-infrastructure__aspire |
| azure-resource-health-diagnose | https://yolox.ai/skills-store/devops-infrastructure__azure-resource-health-diagnose |
| centos-linux-triage | https://yolox.ai/skills-store/devops-infrastructure__centos-linux-triage |
| entra-agent-user | https://yolox.ai/skills-store/devops-infrastructure__entra-agent-user |
| environment-setup | https://yolox.ai/skills-store/devops-infrastructure__environment-setup |
| fedora-linux-triage | https://yolox.ai/skills-store/devops-infrastructure__fedora-linux-triage |
| llm-council | https://yolox.ai/skills-store/devops-infrastructure__llm-council |
| mcp-deploy-manage-agents | https://yolox.ai/skills-store/devops-infrastructure__mcp-deploy-manage-agents |
| msstore-cli | https://yolox.ai/skills-store/devops-infrastructure__msstore-cli |
| release-skills | https://yolox.ai/skills-store/devops-infrastructure__release-skills |
| security-best-practices | https://yolox.ai/skills-store/devops-infrastructure__security-best-practices |

### Developer Tools (217)

> ⚠️ 该类 217 个，文件过长——本文档保留**完整列表**作为权威来源。其中常用于 blog 引用的少数（如 `code-review`, `git-workflow`, `playwright-*` 等）会在具体 blog brief 中按需 cite。

完整列表见 [appendix-skills-developer-tools.md](./appendix-skills-developer-tools.md) ← 因长度独立文件保存。

### Finance & Legal (2)

| Skill | URL |
|---|---|
| ai-tool-compliance | https://yolox.ai/skills-store/finance-legal__ai-tool-compliance |
| sponsor-finder | https://yolox.ai/skills-store/finance-legal__sponsor-finder |

### Marketing (3)

| Skill | URL |
|---|---|
| onboarding-cro | https://yolox.ai/skills-store/marketing__onboarding-cro |
| page-cro | https://yolox.ai/skills-store/marketing__page-cro |
| paid-ads | https://yolox.ai/skills-store/marketing__paid-ads |

### Marketing & Growth (30) ⭐ SEO 相关聚集地

| Skill | URL |
|---|---|
| ab-test-setup | https://yolox.ai/skills-store/marketing-growth__ab-test-setup |
| ad-creative | https://yolox.ai/skills-store/marketing-growth__ad-creative |
| **ai-seo** | https://yolox.ai/skills-store/marketing-growth__ai-seo |
| audit-website | https://yolox.ai/skills-store/marketing-growth__audit-website |
| backlink-analyzer | https://yolox.ai/skills-store/marketing-growth__backlink-analyzer |
| baoyu-post-to-wechat | https://yolox.ai/skills-store/marketing-growth__baoyu-post-to-wechat |
| baoyu-post-to-x | https://yolox.ai/skills-store/marketing-growth__baoyu-post-to-x |
| baoyu-xhs-images | https://yolox.ai/skills-store/marketing-growth__baoyu-xhs-images |
| churn-prevention | https://yolox.ai/skills-store/marketing-growth__churn-prevention |
| competitor-alternatives | https://yolox.ai/skills-store/marketing-growth__competitor-alternatives |
| **content-strategy** | https://yolox.ai/skills-store/marketing-growth__content-strategy |
| email-sequence | https://yolox.ai/skills-store/marketing-growth__email-sequence |
| form-cro | https://yolox.ai/skills-store/marketing-growth__form-cro |
| free-tool-strategy | https://yolox.ai/skills-store/marketing-growth__free-tool-strategy |
| launch-strategy | https://yolox.ai/skills-store/marketing-growth__launch-strategy |
| marketing-ideas | https://yolox.ai/skills-store/marketing-growth__marketing-ideas |
| marketing-psychology | https://yolox.ai/skills-store/marketing-growth__marketing-psychology |
| marketing-skills-collection | https://yolox.ai/skills-store/marketing-growth__marketing-skills-collection |
| paywall-upgrade-cro | https://yolox.ai/skills-store/marketing-growth__paywall-upgrade-cro |
| popup-cro | https://yolox.ai/skills-store/marketing-growth__popup-cro |
| pricing-strategy | https://yolox.ai/skills-store/marketing-growth__pricing-strategy |
| product-marketing-context | https://yolox.ai/skills-store/marketing-growth__product-marketing-context |
| **programmatic-seo** | https://yolox.ai/skills-store/marketing-growth__programmatic-seo |
| referral-program | https://yolox.ai/skills-store/marketing-growth__referral-program |
| **schema-markup** | https://yolox.ai/skills-store/marketing-growth__schema-markup |
| **seo-audit** | https://yolox.ai/skills-store/marketing-growth__seo-audit |
| **seo-geo** | https://yolox.ai/skills-store/marketing-growth__seo-geo |
| signup-flow-cro | https://yolox.ai/skills-store/marketing-growth__signup-flow-cro |
| social-content | https://yolox.ai/skills-store/marketing-growth__social-content |
| twitter-automation | https://yolox.ai/skills-store/marketing-growth__twitter-automation |

### Productivity (47)

| Skill | URL |
|---|---|
| baoyu-compress-image | https://yolox.ai/skills-store/productivity__baoyu-compress-image |
| baoyu-danger-x-to-markdown | https://yolox.ai/skills-store/productivity__baoyu-danger-x-to-markdown |
| bmad-idea | https://yolox.ai/skills-store/productivity__bmad-idea |
| bmad-orchestrator | https://yolox.ai/skills-store/productivity__bmad-orchestrator |
| boost-prompt | https://yolox.ai/skills-store/productivity__boost-prompt |
| brainstorming | https://yolox.ai/skills-store/productivity__brainstorming |
| breakdown-epic-pm | https://yolox.ai/skills-store/productivity__breakdown-epic-pm |
| breakdown-feature-prd | https://yolox.ai/skills-store/productivity__breakdown-feature-prd |
| breakdown-plan | https://yolox.ai/skills-store/productivity__breakdown-plan |
| breakdown-test | https://yolox.ai/skills-store/productivity__breakdown-test |
| executing-plans | https://yolox.ai/skills-store/productivity__executing-plans |
| finalize-agent-prompt | https://yolox.ai/skills-store/productivity__finalize-agent-prompt |
| find-skills | https://yolox.ai/skills-store/productivity__find-skills |
| first-ask | https://yolox.ai/skills-store/productivity__first-ask |
| fun-brainstorming | https://yolox.ai/skills-store/productivity__fun-brainstorming |
| gen-specs-as-issues | https://yolox.ai/skills-store/productivity__gen-specs-as-issues |
| github-issues | https://yolox.ai/skills-store/productivity__github-issues |
| meeting-minutes | https://yolox.ai/skills-store/productivity__meeting-minutes |
| memory-merger | https://yolox.ai/skills-store/productivity__memory-merger |
| my-issues | https://yolox.ai/skills-store/productivity__my-issues |
| obsidian-bases | https://yolox.ai/skills-store/productivity__obsidian-bases |
| opencontext | https://yolox.ai/skills-store/productivity__opencontext |
| pdf | https://yolox.ai/skills-store/productivity__pdf |
| pdftk-server | https://yolox.ai/skills-store/productivity__pdftk-server |
| plan-harder | https://yolox.ai/skills-store/productivity__plan-harder |
| planner | https://yolox.ai/skills-store/productivity__planner |
| planning-with-files | https://yolox.ai/skills-store/productivity__planning-with-files |
| proactive-agent | https://yolox.ai/skills-store/productivity__proactive-agent |
| project-workflow-analysis-blueprint-generator | https://yolox.ai/skills-store/productivity__project-workflow-analysis-blueprint-generator |
| remembering-conversations | https://yolox.ai/skills-store/productivity__remembering-conversations |
| repo-story-time | https://yolox.ai/skills-store/productivity__repo-story-time |
| self-improving-agent | https://yolox.ai/skills-store/productivity__self-improving-agent |
| simple | https://yolox.ai/skills-store/productivity__simple |
| standup-meeting | https://yolox.ai/skills-store/productivity__standup-meeting |
| subagent-driven-development | https://yolox.ai/skills-store/productivity__subagent-driven-development |
| super-swarm-spark | https://yolox.ai/skills-store/productivity__super-swarm-spark |
| swarm-planner | https://yolox.ai/skills-store/productivity__swarm-planner |
| task-estimation | https://yolox.ai/skills-store/productivity__task-estimation |
| task-planning | https://yolox.ai/skills-store/productivity__task-planning |
| update-implementation-plan | https://yolox.ai/skills-store/productivity__update-implementation-plan |
| update-markdown-file-index | https://yolox.ai/skills-store/productivity__update-markdown-file-index |
| using-superpowers | https://yolox.ai/skills-store/productivity__using-superpowers |
| vibe-kanban | https://yolox.ai/skills-store/productivity__vibe-kanban |
| what-context-needed | https://yolox.ai/skills-store/productivity__what-context-needed |
| workflow-automation | https://yolox.ai/skills-store/productivity__workflow-automation |
| workiq-copilot | https://yolox.ai/skills-store/productivity__workiq-copilot |
| writing-plans | https://yolox.ai/skills-store/productivity__writing-plans |

### Sales & CRM (1)

| Skill | URL |
|---|---|
| cold-email | https://yolox.ai/skills-store/sales-crm__cold-email |

---

## §6 · Team 详情页 URL（36 个）

> **URL 模式**：`/teams-store/{team-id}`

### Content (8)

| Team | URL |
|---|---|
| Content Creator | https://yolox.ai/teams-store/content-creator |
| Knowledge IP Builder | https://yolox.ai/teams-store/knowledge-ip |
| Newsletter Creator | https://yolox.ai/teams-store/newsletter-creator |
| Podcaster | https://yolox.ai/teams-store/podcaster |
| Short Video Creator | https://yolox.ai/teams-store/short-video-creator |
| Substack / Newsletter-First Creator | https://yolox.ai/teams-store/substack-creator |
| Xiaohongshu Creator | https://yolox.ai/teams-store/xiaohongshu-creator |
| YouTube/Twitch Creator | https://yolox.ai/teams-store/youtube-creator |

### Developer (5)

| Team | URL |
|---|---|
| AI App Builder | https://yolox.ai/teams-store/ai-app-builder |
| App Developer | https://yolox.ai/teams-store/app-developer |
| Indie Game Developer | https://yolox.ai/teams-store/indie-game-dev |
| Indie Hacker | https://yolox.ai/teams-store/indie-hacker |
| SaaS Founder | https://yolox.ai/teams-store/saas-founder |

### E-Commerce (4)

| Team | URL |
|---|---|
| Amazon Seller | https://yolox.ai/teams-store/amazon-seller |
| Artisan / DTC Brand Founder | https://yolox.ai/teams-store/artisan-dtc |
| Shopify / DTC Brand | https://yolox.ai/teams-store/shopify-dtc |
| TikTok Shop | https://yolox.ai/teams-store/tiktok-shop |

### Finance (1)

| Team | URL |
|---|---|
| Independent Financial Advisor | https://yolox.ai/teams-store/financial-advisor |

### In-House (6)

| Team | URL |
|---|---|
| Brand & PR Manager | https://yolox.ai/teams-store/brand-pr |
| Content Marketing Manager | https://yolox.ai/teams-store/content-marketing |
| Growth Lead | https://yolox.ai/teams-store/growth-lead |
| Marketing Lead | https://yolox.ai/teams-store/marketing-lead |
| Sales & BD | https://yolox.ai/teams-store/sales-bd |
| Social Media Manager | https://yolox.ai/teams-store/social-media-manager |

### Service (7)

| Team | URL |
|---|---|
| Career & Life Coach | https://yolox.ai/teams-store/career-coach |
| Consultant | https://yolox.ai/teams-store/consultant |
| Event Planner | https://yolox.ai/teams-store/event-planner |
| Freelance Designer | https://yolox.ai/teams-store/freelance-designer |
| Independent Travel Advisor | https://yolox.ai/teams-store/travel-advisor |
| Photographer / Wedding Planner | https://yolox.ai/teams-store/photographer |
| Training Business | https://yolox.ai/teams-store/training-business |

### Vertical (5)

| Team | URL |
|---|---|
| Go-Global Business | https://yolox.ai/teams-store/go-global |
| Local Restaurant | https://yolox.ai/teams-store/local-restaurant |
| MCN Agency | https://yolox.ai/teams-store/mcn-agency |
| Pet Services | https://yolox.ai/teams-store/pet-services |
| Recruiter | https://yolox.ai/teams-store/recruiter |

---

## §7 · URL 格式规则 & 隐忧

### URL 格式速查

| 类型 | 格式 | 例 | 现状 |
|---|---|---|---|
| Agent 列表 | https://yolox.ai/agents-store | https://yolox.ai/agents-store | ✅ 已有 |
| Agent 详情 | `/agents-store/{slug}` | https://yolox.ai/agents-store/seo-doctor | ✅ 已有 |
| Agent 分类 | `/agents-store/category/{cat}` | https://yolox.ai/agents-store/category/growth | ❌ 待 Path B |
| Skill 列表 | https://yolox.ai/skills-store | https://yolox.ai/skills-store | ✅ 已有 |
| Skill 详情 | `/skills-store/{cat}__{name}` | https://yolox.ai/skills-store/marketing-growth__ai-seo | ✅ 已有 |
| Skill 分类 | `/skills-store/category/{cat}` | https://yolox.ai/skills-store/category/marketing-growth | ❌ 待 Path B |
| Team 列表 | https://yolox.ai/teams-store | https://yolox.ai/teams-store | ✅ 已有 |
| Team 详情 | `/teams-store/{slug}` | https://yolox.ai/teams-store/content-creator | ✅ 已有 |
| Team 分类 | `/teams-store/category/{cat}` | https://yolox.ai/teams-store/category/content | ❌ 待 Path B |

### 隐忧 / 待解决

#### 🟡 隐忧 1：Skill URL 的 `__` 不利 SEO

Skill URL 形如 https://yolox.ai/skills-store/marketing-growth__ai-seo——含 `__`（双下划线），Google 不友好。

**未来 v0.6 升级方向**：
- 改 `getSkillById` 支持 base ID 查找（参考 `getAgentById` 的 split 逻辑）
- 用 canonical 把 `marketing-growth__ai-seo` 指向 `ai-seo`
- 升级后 blog 改用 https://yolox.ai/skills-store/ai-seo

**当前**：仍按 `__` 全形写，因为路由只认这个。

#### 🟡 隐忧 2：Agent URL 双形态需 canonical

Agent route 同时接受 https://yolox.ai/agents-store/seo-doctor 和 https://yolox.ai/agents-store/seo-doctor__info，2 URL 渲染同页 = 重复内容。

**应对**：前端在详情页 `<head>` 加 canonical 锁定 clean 形：
```tsx
<link rel="canonical" href={`https://yolox.ai/agents-store/${id.split("__")[0]}`} />
```

**当前 blog 行动**：blog 只链 clean 形（无 `__info`），不引发重复。

#### 🔴 隐忧 3：分类 URL 全部待 Path B 实现

§2 列的 30 个分类 URL **现在都返 404**。需要：
- 加 3 个动态路由文件：`/agents-store/category/[category]/page.tsx` / `/skills-store/category/[category]/page.tsx` / `/teams-store/category/[category]/page.tsx`
- 每个 route 读 `[category]` 参数 → 复用现有 list 组件 + 预筛选
- 加 metadata（title/description/canonical）+ sitemap

**估时**：3 个文件 × 30min = 1.5h。

**blog ship 顺序建议**：blog markdown 里**先写 URL**（path-style，未来不会变），dev 完成后激活。short term 如果 dev 没好，**临时 fallback 改链 list 总页** https://yolox.ai/agents-store。

---

## §8 · 数据刷新流程

manifest 是活的，新 agent / skill 会持续加。**每月 1 号**重跑：

```bash
# 在 yolox-web 项目根目录
source .env.local
curl -sL -H "Authorization: Bearer $GITHUB_TOKEN" -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/Infinite-Flow-Labs/yolox-agent-store/contents/manifests/agents.json?ref=main" \
  -o /tmp/yolox-agents.json

# 然后用 jq 重生成本文档对应 section
jq -r '.agents | map(select((.id // "" | split("__")[0]) as $base | $base != "quant-analysis-assistant" and $base != "financial-content-editor" and $base != "financial-social-media")) | group_by(.domain) | .[] | ...' /tmp/yolox-agents.json
```

→ 后续做成 `npm run blog:url-inventory:refresh` script（v0.6 计划）。

---

## §9 · 与其他文档的关系

| 本文档 | 其他文档 |
|---|---|
| §3 SEO shortlist | `routing-matrix-v0.5.md §3` 替代旧的"占位 agent 名" |
| §4-6 详细 URL | `brief-template.md` 内链清单填写时查这里 |
| §7 隐忧 | `frontend-spec.md` 需补 canonical 实现 |
| Path B 路由 | 待开 PR：`feat/agents-store-category-route` |
