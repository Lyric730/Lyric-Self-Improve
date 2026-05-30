# yolox blog 链接 routing matrix v0.5

> **目的**：写 blog 时遇到"链到哪个 URL"不再卡——直接查表。
> **位置**：写作流程中段，brief 必填 6 内链清单 7+ 条要从本文档锁。
> **覆盖**：silo URL / 内链矩阵 / product 链 / 外链权威白名单 / 锚文本规则 / 决策 SOP
> **配套**：`brief-template.md`（写前填）/ `checklist-pre-publish.md` M10 内链检查

---

## 0 · 这份文档怎么用

3 步：

1. 拿到 brief 必填 6 的内链 7+ 条占位 → 来本文档查具体 URL
2. 写 markdown 遇到"这里要链一个 stat / quote / 文档" → 查 §4 外链白名单
3. 发布前 checklist M10 验证内链按 30/30/30/10 锚文本分布 → §5 校验

---

## 1 · 24 主词 + silo URL 总览

### 1.A AEO silo

| L6-XX | 主词 | URL | Type | 状态 |
|---|---|---|---|---|
| L6-00-pillar-aeo | `Answer Engine Optimization` | `/blog/aeo` | Pillar (type-4) | 🔴 待写（Pillar 主文 = silo entry）|
| L6-01 | `answer engine optimization services` | `/blog/aeo/answer-engine-optimization-services` | Cluster (type-7) | 🟡 Draft 已写（PR #21）|
| L6-07 | `Generative Engine Optimization` | `/blog/aeo/generative-engine-optimization` | Cluster (type-3) | 🔴 待写 |
| L6-08 | `aeo vs geo` | `/blog/aeo/aeo-vs-geo` | Cluster (type-5) | 🔴 待写 |
| L6-09 | `answer engine optimization tools` | `/blog/aeo/aeo-tools` | Cluster (type-1) | 🔴 待写 |
| L6-10 | `Google AI Overview optimization` | `/blog/aeo/google-ai-overview-optimization` | Cluster (type-2) | 🔴 待写 |

### 1.B α silo（AI 工具）

| L6-XX | 主词 | URL | Type | 状态 |
|---|---|---|---|---|
| L6-00-pillar-alpha | `AI infographic generator` | `/blog/ai-tools` | Pillar (type-4 hybrid) | 🔴 待写 |
| L6-03 | `AI proposal generator` | `/blog/ai-tools/ai-proposal-generator` | Cluster (type-1/7) | 🔴 |
| L6-11 | `AI ad creative generator` | `/blog/ai-tools/ai-ad-creative-generator` | Cluster (type-7) | 🔴 |
| L6-12 | `story writer AI` | `/blog/ai-tools/story-writer-ai` | Cluster (type-1) | 🔴 |
| L6-13 | `AI newsletter writer` | `/blog/ai-tools/ai-newsletter-writer` | Cluster (type-1) | 🔴 |
| L6-14 | `Marketing & Growth AI agents` | `/blog/ai-tools/marketing-growth-ai-agents` | Cluster (type-1) | 🔴 |

### 1.C β silo（B2B Sales/招聘）

| L6-XX | 主词 | URL | Type | 状态 |
|---|---|---|---|---|
| L6-00-pillar-beta | `ai tools for recruiting` | `/blog/b2b` | Pillar (type-4) | 🔴 |
| L6-04 | `cold email deliverability` | `/blog/b2b/cold-email-deliverability` | Cluster (type-2) | 🟡 候选第 2 篇 |
| L6-05 | `ai agents for project management` | `/blog/b2b/ai-agents-project-management` | Cluster (type-1) | 🔴 |
| L6-06 | `ai tools for recruiting` | `/blog/b2b/ai-tools-for-recruiting` | Cluster (双重身份与 Pillar) | 🔴 |
| L6-15 | `ai tools for recruiters` | `/blog/b2b/ai-tools-for-recruiters` | Cluster (type-1) | 🔴 |
| L6-16 | `cold calling AI` | `/blog/b2b/cold-calling-ai` | Cluster (type-2/3) | 🔴 |
| L6-17 | `best CRM for financial advisors` | `/blog/b2b/crm-financial-advisors` | Cluster (type-7+6) | 🔴 |

### 1.D γ silo（Creator/SMB）

| L6-XX | 主词 | URL | Type | 状态 |
|---|---|---|---|---|
| L6-00-pillar-gamma | `social media management tools` | `/blog/creator` | Pillar (type-4) | 🔴 |
| L6-02 | `podcast guest release form` | `/blog/creator/podcast-guest-release-form` | Cluster (type-3+template) | 🔴 |
| L6-18 | `podcast name generator` | `/blog/creator/podcast-name-generator` | Cluster (type-1) | 🔴 |
| L6-19 | `amazon vine reviewer` | `/blog/creator/amazon-vine-reviewer` | Cluster (type-3) | 🔴 |
| L6-20 | `ecommerce growth strategy` | `/blog/creator/ecommerce-growth-strategy` | Cluster (type-1) | 🔴 |
| L6-21 | `restaurant marketing strategies` | `/blog/creator/restaurant-marketing-strategies` | Cluster (type-1) | 🔴 |

🔑 **URL slug 规则**（来自主 SOP §5 S5）：
- 必含主词全名或核心副词
- 连字符分隔，≤5 词
- **不带年份**（避免每年改 URL）
- 长主词可缩到核心副词（如 `answer engine optimization tools` → `aeo-tools`）

---

## 2 · 内链矩阵（site-level）

### 2.A 上行链（cluster → Pillar，**每篇必含 ≥1 条**）

每个 cluster 文章**必须**至少 1 条链回本 silo 的 Pillar 主文。这是 silo 架构的核心——Pillar 接收 5+ 内链才能成为 hub。

| 当前 cluster | 链到 Pillar | 锚文本候选 |
|---|---|---|
| AEO silo 任意 cluster | `/blog/aeo` | "Answer Engine Optimization Pillar guide" / "AEO basics" / "AEO complete guide" |
| α silo 任意 cluster | `/blog/ai-tools` | "AI infographic generator Pillar" / "AI tools overview" |
| β silo 任意 cluster | `/blog/b2b` | "B2B AI tools Pillar" / "AI tools for recruiting overview" |
| γ silo 任意 cluster | `/blog/creator` | "social media management tools Pillar" / "creator toolkit overview" |

⚠️ **Pillar 主文未 ship 期间**：链 placeholder 保留 `/blog/{silo}` 即可（前端会渲染 silo entry 页 — 见 `frontend-spec.md §2.C.2`）。

### 2.B 横向链（同 silo cluster ↔ cluster，每篇 1-3 条）

#### AEO silo 内链推荐（完整）

| 当前文章 | 推荐 1 链 | 推荐 2 链 | 场景 |
|---|---|---|---|
| L6-01 services | L6-07 GEO | L6-09 tools | services 评估完 → DIY / tools 路径 |
| L6-07 GEO | L6-08 AEO vs GEO | L6-10 AI Overview | 概念入门 → 对比 / 实操 |
| L6-08 AEO vs GEO | L6-07 GEO | L6-01 services | 区分概念 → 服务购买 |
| L6-09 tools | L6-01 services | L6-10 AI Overview | tools 评测 → service 路径 / 实操 |
| L6-10 AI Overview | L6-07 GEO | L6-09 tools | 实操 → 概念 / 工具 |

#### α / β / γ silo 横向链（待具体写时 finalize）

🟡 v0.5 暂留占位——下个 session 写 L6-04 时把 β silo 横向链表补全。**通用规则**：

- 每 cluster 横向链 1-3 条，覆盖 silo 内相关主题
- 优先链 "用户读完这篇可能想读的下一篇"
- 不链同 silo 内**主题完全无关**的 cluster（如 podcast 不必链 amazon vine）

### 2.C 跨 silo 链（特殊场景，**默认不跨**）

跨 silo 链只在内容必要时加。**默认不跨**——影响 silo 权重集中。

允许跨 silo 的 3 种场景：

| 场景 | 例 | 锚文本规则 |
|---|---|---|
| 主题边界自然交叉 | β L6-04 cold email → α L6-13 newsletter（"outreach 后用 newsletter 维系"）| 通用锚 |
| 上游 Pillar 概念 | 任意 silo → AEO Pillar（讨论 AI search 时）| 通用锚 |
| 强相关 case | β L6-17 CRM → α L6-03 proposal（financial advisor 工作流）| 部分锚 |

🔑 **跨 silo 锚文本用通用锚**（"see also" / "related discussion"），不用主词——避免抢走自 silo 权重。

---

## 3 · Product 链路由

> ⚠️ **本节已迁移**——具体 URL 不再在此处维护，全部转入 [`url-inventory.md`](./url-inventory.md)（活数据，从 yolox manifest 直接拉取）。
> 本节只保留**规则 / 决策树 / 锚类型**，URL 必须从 url-inventory.md 复制。

### 3.A · URL 体系总览

| URL 类型 | 模式 | 现状 | 在 url-inventory.md 哪一节 |
|---|---|---|---|
| 顶级 catalog | `https://yolox.ai/{agents,skills,teams}-store` | ✅ 已有 | §1 |
| 分类页 | `https://yolox.ai/{store}/category/{cat}` | ❌ 待 Path B 路由 | §2 |
| Agent 详情 | `https://yolox.ai/agents-store/{slug}` | ✅ 已有 | §4 |
| Skill 详情 | `https://yolox.ai/skills-store/{cat}__{name}` | ✅ 已有 | §5 |
| Team 详情 | `https://yolox.ai/teams-store/{slug}` | ✅ 已有 | §6 |

### 3.B · 选 URL 的 3 步法

```
Step 1：blog 主题 → 找 silo（aeo / α / β / γ）
Step 2：打开 url-inventory.md §3 看该主题的 SEO shortlist
Step 3：按 §3.C 决策表选 URL 类型 → 复制 url-inventory.md 对应 URL
```

🔑 **铁律**：blog 内链**必须**来自 url-inventory.md 当前版。不允许"凭记忆"或"猜"slug。

### 3.C CTA 决策表（什么时候用哪条 URL 类型）

| 场景 | URL 类型 | url-inventory.md 节 |
|---|---|---|
| 通用 CTA（intro 末软 / 结尾硬，"see all agents"）| 分类页 或 顶级 catalog | §1 / §2 |
| 具体功能 mention（"chunk-level AI SEO skill"）| Skill 详情 | §5 + §3 shortlist |
| 具体 agent mention（"SEO Doctor agent"）| Agent 详情 | §4 + §3 shortlist |
| Pillar 主文末（多 agent stack）| 多个 Agent 详情 + Team | §4 + §6 |
| 中立场景（不推 product）| silo Pillar guide（不链 product）| brief §B silo 表 |

### 3.D · L6-01 已用资产示例（dogfood）

| 链接 | URL（从 url-inventory.md §3 取）|
|---|---|
| Schema Markup skill | https://yolox.ai/skills-store/marketing-growth__schema-markup |
| SEO Doctor agent | https://yolox.ai/agents-store/seo-doctor |
| AI SEO skill | https://yolox.ai/skills-store/marketing-growth__ai-seo |
| Website Audit Reporter agent | https://yolox.ai/agents-store/website-audit-reporter |
| AEO 类别 CTA | https://yolox.ai/agents-store/category/growth（待 Path B）|

🔑 **每个新 blog 写之前**，先去 url-inventory.md §3 找该主题的 shortlist。如果没有 shortlist，brief 阶段查 §4-6 详情表挑出 ≥4 个匹配的 yolox 真实资产。

---

## 4 · 外链权威白名单（按主题）

🔑 **优先级铁律**：**🥇 引第一手 > 🥈 引权威媒体报道 > 🥉 引 secondary 汇总站**。
不要因为第一手 URL 难找就默认引 secondary——花 5 min WebSearch 找原研究 URL，是 EEAT trust 信号的 10x。

### 4.A SEO/AEO 数据源

| 源 | URL | 权威性 | 推荐引用领域 |
|---|---|---|---|
| Search Engine Land | https://searchengineland.com/ | 🟢 **强** | 业界新闻 / algorithm 更新 / Seer 等研究报道 |
| Seer Interactive（**第一手**）| https://www.seerinteractive.com/insights/ | 🟢 **强** | CTR / AI Overview 自家研究 — **优于引 SEL 转述** |
| SparkToro（Rand Fishkin）| https://sparktoro.com/blog/ | 🟢 **强** | zero-click / 搜索行为研究 |
| First Page Sage | https://firstpagesage.com/reports/ | 🟢 **强** | CTR by position / AI Overview impact 自家研究 |
| Conductor（**第一手**）| https://www.conductor.com/blog/ | 🟢 **强** | AI Overview prevalence 自家 benchmark |
| Search Engine Journal | https://www.searchenginejournal.com/ | 🟢 **强** | 业界教程 / case study |
| ALM Corp | https://almcorp.com/blog/ | 🟡 **中** | AI Overview industry surge — agency blog，引时确认数据原 source |
| Position Digital | https://www.position.digital/blog/ | 🟡 **中** | AI SEO statistics 汇总站 — **优先去找原 source（Conductor 等）|
| Digital Strategy Force | https://digitalstrategyforce.com/ | 🟡 **中** | AEO agency 自家 blog — pricing data 用，但**niche source** |
| GrackerAI（via NatLawReview）| https://natlawreview.com/.../grackerai | 🟡 **中** | 73% cybersecurity benchmark — **优先去 GrackerAI 原 blog 找** |

⚠️ **注意**：🟡 中级 source **不阻塞引用**，但**同主题数据时优先 🟢 强 source**。每篇 blog 至少 2 条外链应该是 🟢。

### 4.B Schema / 技术文档

| 源 | URL | 用途 |
|---|---|---|
| Schema.org | https://schema.org/{Type}（如 /FAQPage）| Schema 类型 spec |
| Google Search Central | https://developers.google.com/search/ | 结构化数据指南 |
| Google Rich Results Test | https://search.google.com/test/rich-results | 验证工具（外链 + 内部 verify）|
| Schema.org Validator | https://validator.schema.org/ | JSON-LD 语法验证 |

### 4.C 业界领袖（quote 优先源）

| 人 | 第一手主页 / Twitter | 权威性 | 推荐引用领域 |
|---|---|---|---|
| **Aleyda Solis** | https://www.aleydasolis.com/ / https://www.orainti.com/ | 🟢 **强** | AEO/GEO / topic clusters（**首选**）|
| Britney Muller | https://twitter.com/BritneyMuller | 🟢 **强** | LLM SEO / AI search |
| Marie Haynes | https://www.mariehaynes.com/blog | 🟢 **强** | EEAT / algorithm updates |
| Lily Ray | https://twitter.com/lilyraynyc | 🟢 **强** | EEAT / quality updates |
| TryProfound expert list | https://www.tryprofound.com/resources/articles/top-experts-in-generative-engine-optimization | 🟡 **中** | **secondary host**，找原作者 blog 取代 |

⚠️ **quote 引用纪律**：找到引语原话后**优先链作者个人 blog / Twitter**（🟢），不是聚合站（🟡）。
例：Aleyda quote → 链 aleydasolis.com 而不是 tryprofound.com/blog/aeo-vs-geo。

### 4.D 工具 vendor（pricing / 评测时引用）

| 类别 | 工具 | 何时引用 |
|---|---|---|
| 关键词 | Ahrefs / SEMrush / KWFinder | volume / KD 数据 |
| Schema | Schema.org / Google RR Test / Yoast | schema validation |
| AEO 监测 | Profound / Otterly.AI / Search Atlas / Surfer AEO | AEO 工具评测时（buyer's guide）|
| 内容 | Frase / Surfer / Jasper / Clearscope | content optimization |
| 分析 | GA4 / Search Console / Mixpanel | tracking |

🔑 **法律 / 商誉**：引用竞品 vendor 时**避免直接否定**。用 "X tool 提供 Y feature" 中立表述，不写 "X is bad" 类断言。否定要有公开 source 支撑。

### 4.E 社区证据（quote / pain point）

| 平台 | URL pattern | 用法 |
|---|---|---|
| Reddit r/SEO | https://www.reddit.com/r/SEO/ | 真实痛点 quote |
| Reddit r/bigseo | https://www.reddit.com/r/bigseo/ | 进阶 SEO 讨论 |
| Reddit r/marketing | https://www.reddit.com/r/marketing/ | SMB / B2B 视角 |
| Twitter SEO 圈 | https://twitter.com/search?q=AEO | 实时讨论 |
| HackerNews | https://news.ycombinator.com/ | tech SaaS 视角 |
| IndieHackers | https://www.indiehackers.com/ | solo / SMB founder 视角 |
| Quora SEO topic | https://www.quora.com/topic/Search-Engine-Optimization-SEO | "如何 X" 类查询 |

🔑 **引用 Reddit / Twitter** 时**贴 URL 而不是截图**——前端层防 dead link 用 archive.org snapshot 作 fallback（frontend P1-9 待加，**v0.5 暂不强卡**）。

---

## 5 · 锚文本规则（30/30/30/10 分布）

每篇 blog 5-8 个内链按这个分布：

| 类型 | 占比 | 例 |
|---|---|---|
| **精准锚**（完全匹配主词）| 30% | "answer engine optimization services" |
| **部分锚**（部分匹配 + 修饰）| 30% | "AEO services pricing guide" / "AEO buyer's guide" |
| **品牌锚 / URL 锚** | 30% | "yolox" / "yolox.ai/blog" / "Sophie AEO doctor" |
| **通用锚**（read more / this guide）| 10% | "this DIY path" / "see related" |

🔑 **避免过度精准锚**——Google 会判定 unnatural linking → 降权。**5 个内链中**：1 精准 + 2 部分 + 1-2 品牌 + 0-1 通用。

---

## 6 · 链接策略 SOP

### 6.A 强制规则（checklist M10 强卡）

| 规则 | 来源 |
|---|---|
| ✅ 每篇 cluster **必含 ≥1 上行链**回 Pillar | silo 架构 |
| ✅ 每篇文章**必含 ≥3 silo 内链**（含上行 + 横向）| brief 必填 6 + checklist M10 |
| ✅ 每篇文章**必含 ≥1 product 链** | 主 SOP §6 |
| ✅ 每篇文章**必含 ≥3 外链权威源** | 主 SOP M11 |
| ❌ 不允许跨 silo 链作主链 | 见 §2.C 例外 |
| ❌ 不允许同一锚文本指多个 URL | confusion 信号 |

### 6.B 决策树（写到一个点要不要加链）

```
写到一个点要加链 →
├─ 这是 stat / data？ → §4.A 数据源
├─ 这是 quote？ → §4.C 业界领袖
├─ 这是 schema / 技术概念？ → §4.B
├─ 这是 silo 内相关概念？ → §2.B 横向链
├─ 这是 Pillar 上游概念？ → §2.A 上行链
├─ 这是推荐 yolox 产品？ → §3 product 链
├─ 这是 vendor / 工具评测？ → §4.D
├─ 这是真实痛点引用？ → §4.E 社区
└─ 都不是 → 不加链
```

🔑 **链不是越多越好**。每个链都消耗读者注意力 + 分散 PageRank。**每 400-500 字 ≤1 个外链**（过密会被判 unnatural）。

---

## 7 · 使用流程（写新 blog 时）

写 brief 必填 6 时：

```
Step 1: 拿到 L6-XX 大纲 + 确认 type 选定
Step 2: 查 §1 silo URL 表确定自己的 URL（slug 含主词）
Step 3: 查 §2.A 上行链 → 锁 1 条（Pillar）
Step 4: 查 §2.B 横向链 → 锁 1-2 条（silo 内 cluster）
Step 5: 查 §3.B-C product 链 → 锁 1 条 CTA（具体 agent or 通用 category）
Step 6: 查 §4 外链白名单 → 锁 3-5 条（根据素材池每条 stat/quote/case 的 source）
Step 7: 7+ 个内链清单填进 brief 必填 6 的内链表
Step 8: 验证锚文本 30/30/30/10 分布
Step 9: 开 drafting
```

写 markdown 中段：
- 每加 1 个链都回查决策树 §6.B
- 不确定时**默认不加链**（少胜过多）

---

## 8 · v0.5 已知缺口

| 缺口 | 影响 | 何时补 |
|---|---|---|
| α / β / γ silo cluster 横向链推荐表 | 不影响 AEO 第 1 篇 | 写 L6-04（β 第 1 篇）时补 β |
| 具体 agent 名（除 AEO 4 个）| Product 链 specifics | 每写 1 篇新 silo cluster 时 grep agents-store / GitHub manifest 补 |
| `/agents-store?category={silo}` 是否真实支持 | CTA URL 准确性 | 等前端实施 frontend-spec.md 时同步 verify |
| Pillar 主文 4 篇全部"待写" | 上行链占位 ship 时 = 死链 | 写每个 Pillar 时 finalize |
| 跨 silo 链白名单 | 边缘 case 不影响主线 | v1 时补 |
| 锚文本 30/30/30/10 自动检查工具 | 现在靠手动数 | v1 / 工具化阶段 |

---

## 9 · 迭代触发点

| 版本 | 触发条件 |
|---|---|
| **v0.5**（当前）| AEO silo 第 1 篇 L6-01 完成 |
| **v0.6** | 写完 L6-04（β silo 第 1 篇）后扩展 β silo |
| **v0.7** | 4 silo 各 1 篇 cluster ship 后定稿 |
| **v1** | Pillar 主文全 ship（routing 全部 verified）|
| **v2** | 工具化（脚本自动检查 30/30/30/10 + 死链 + Pillar 内链数）|

---

## 附录 · 与其他文档的接口

| 本文档涉及 | 对应文档 |
|---|---|
| 内链 ≥3 silo 内 / ≥1 product / ≥3 外链 | `brief-template.md` 必填 6 + `checklist-pre-publish.md` M10/M11 |
| URL slug 规则 | `yolox-blog-template-v0.5.md` §5 S5 |
| Schema / JSON-LD 注入 | `0-share/frontend-spec.md` §2.A |
| Agent / Skill / Team manifest 来源 | 项目根 `CLAUDE.md` "Data Fetching for Catalogs" |
| 24 主词列表完整表 | `keyword-research/round-2-2026-04-28/0-share/keyword-coverage.md` |
