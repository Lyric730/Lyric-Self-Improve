# 07 · 负向关键词清单（Day 3 产出）

**日期**：2026-04-23（Day 3）
**交付等级**：🟡 可用（给 Agent C 外链 + Agent D AEO 参考）
**对应 playbook**：§2.3.8 负向词 + §2.5 外链策略
**对应任务**：`docs/seo/tasks/week-2026-04-22/2.3-keyword-research.md` Day 3 + Day 4 合并

---

## 前言 · 负向词是什么、为什么要列

**负向词 ≠ 不允许出现的词**，而是 **YOLOX 本周/本月主动不追的词**。四个理由：

1. **搜这个词的人不是 YOLOX 客户**（品牌词：搜 "Lindy login" 的人要找 Lindy，不要 YOLOX）
2. **搜这个词的 SERP 新站排不上**（高 KD 大词：前 6 月 Google 不会让新站进 top 50）
3. **零流量期 SERP 结构对新站不友好**（商业调查词：SERP 全是 DR 70+ listicle 巨无霸）
4. **这个词对应的能力 YOLOX 不做**（AI 绘图：用户搜这个要找 Midjourney）

**这个清单的实际用途**：

| 使用方 | 怎么用 |
|---|---|
| **Agent B（我自己）** | Day 6 选博客标题时避开这些词 |
| **Agent C（外链/目录）** | 外链锚文本不用竞品品牌词、不在 Lindy 品牌搜索结果页投 |
| **Agent D（AEO/FAQPage）** | FAQPage schema 的 Q&A 不直接回答 "Lindy vs YOLOX"（那是商业调查 frame） |
| **下周 §2.4 博客产线** | 博客标题不碰"best AI X for Y" / "X vs Y"（引流弱 + SERP 排不上）|

---

## 统计

| 类别 | 词数 | 备注 |
|---|---|---|
| §1 竞品品牌词 | 25 | 包含 YOLOX 自己未来要做的"反向对比页"的原料（Day 7 Watch List）|
| §2 超高 KD 大词 | 12 | 6 个月内别碰，解锁后升级到 Map 头部词 |
| §3 零流量期商业调查词 | 43 | 从 Day 2 325 词里砍出，playbook §2.8 Watch List 重点 |
| §4 与 YOLOX 定位不符 | 18 | 永久负向（除非产品转向）|
| §5 弱 Claude 扩展 | 19 | Day 2 Claude 扩展里"无场景锚"被砍的 |
| **合计** | **117** | 对应 04 文档 "砍 ~125" 略少，差值 8 在 Day 5 Cluster 定稿时从 Tier 3 再砍 |

---

## §1 · 竞品品牌词（25）

**规则**：搜到包含竞品品牌名的词，**全部 defer**。搜的人是竞品潜在客户，不是 YOLOX。

**但保留战略价值**：这类词是**未来**反向对比页（§2.8.2 alternatives 页）的原料，**DR > 20 时**再做。

### 1.1 Lindy 相关（5）

- Lindy pricing
- Lindy login
- Lindy alternatives
- Lindy review
- is Lindy worth it

### 1.2 Zapier 相关（5）

- Zapier pricing
- Zapier login
- Zapier AI alternatives
- Zapier for AI agents
- Zapier agents review

### 1.3 Relevance AI / n8n / Make（8）

- Relevance AI pricing
- Relevance AI vs Lindy
- n8n pricing
- n8n self-hosted setup
- n8n alternatives
- Make.com pricing
- Make.com vs Zapier
- Make.com review

### 1.4 其他 AI agent 竞品（7）

- Gumloop pricing
- Gumloop alternatives
- Cassidy AI pricing
- Stack AI pricing
- Bardeen pricing
- AgentGPT review
- CrewAI commercial version

**Day 7 Watch List**（DR > 20 时做）：
- `Lindy alternatives` → 开页 `/compare/lindy-alternative`（含 YOLOX 作为首选推荐）
- `Zapier AI alternatives` → 同上
- `Make.com vs Zapier` → 横向对比加 YOLOX

---

## §2 · 超高 KD 大词（12，6 个月内别碰）

**规则**：KD 预估 > 40，前 6 月碰了等于白写。

### 2.1 AI 行业大词（8）

| 词 | 估计 KD | 现 SERP 头部 |
|---|---|---|
| AI agent | 80+ | Zapier, Lindy, Relevance (DR 80+) |
| AI workflow | 70+ | Zapier, n8n, Make |
| AI automation | 75+ | Zapier 占半壁 |
| AI assistant | 80+ | Apple Siri, Google Assistant 信息页 |
| AI integration | 65+ | Zapier |
| AI agent builder | 60+ | n8n, Gumloop |
| AI copilot | 75+ | Github, Microsoft |
| AI orchestration | 60+ | Zapier AI, LangChain |

### 2.2 非 AI 大词（4）

| 词 | 估计 KD |
|---|---|
| workflow automation | 70+ |
| no-code automation | 60+ |
| business process automation | 75+ |
| RPA AI | 60+ |

**解锁路径**：
- 前 3 月：只做这些词下面的 KD < 10 长尾（例：`AI agent for Shopify store owner`，而不是 `AI agent`）
- 3–6 月：如果 Tier 1 博客有 20+ 进 top 20，开始攻 `AI agent for solopreneurs`（Pillar 发布）
- 6 月后：才考虑 `AI agent` 这种大词（通过 Pillar page 承接）

---

## §3 · 零流量期商业调查词（43）

**规则**：SERP 必然是 listicle / vs / alternative，新站排不上。**100% 进 Watch List，下周博客不做**。

**但保留价值**：这些问题**用作 FAQPage schema 的 Q&A**（AEO 友好，playbook §2.6）。Agent D 写 FAQPage schema 时可以直接抄这些 Q&A 形式。

### 3.1 "best X for Y" 型（20）

- best AI agents for solopreneurs
- best AI tools for small business automation
- best AI writing tool for content creators
- best AI tools to grow small business
- best AI content tools 2025
- best AI agent for Shopify store
- best free AI tool for content creators
- best AI tools for productivity
- best new AI tools 2026
- best AI tools for agencies
- best Claude setups for SEO
- best AI automation company
- best AI tool to write listicles
- best AI driven teams for packaging design
- best agent right now（r/shopify 原问，但 frame 为"best"→ defer）
- best AI SEO tool
- best AI for ecommerce
- best AI for Etsy sellers
- best AI for coaches
- best AI for consultants

### 3.2 "X vs Y" 型（10）

- Lindy vs Zapier
- n8n vs Make
- Zapier vs Relevance AI
- Jasper vs Copy.ai
- Notion AI vs ChatGPT
- Claude vs ChatGPT for agents
- AI agents vs chatbots
- AI agent vs automation
- AI assistant vs AI agent
- Gumloop vs Cassidy

### 3.3 "X alternatives" 型（8）

- Lindy alternatives
- Zapier AI alternatives
- Make alternatives
- Jasper alternatives
- Notion AI alternatives
- AgentGPT alternative
- open source Zapier alternative
- free AI agent alternatives

### 3.4 "which / what is the" 商业调查（5）

- which AI agent for work
- which AI tool is used for content creation
- what companies use Notion
- what is the best AI software for small business
- what are the top AI business ideas for beginners

---

## §4 · 与 YOLOX 定位不符（18）

**规则**：这些词对应的能力 YOLOX **不提供**，追了也是流量错位（搜这个词的人进站后秒退）。

### 4.1 纯 AI 写作市场（5）

- AI blog post generator（不是 YOLOX 强项，Jasper/Copy.ai 在打）
- AI novel writing
- AI story generator
- AI essay writer
- AI academic writing

### 4.2 AI 绘图 / 视频生成（6）

- AI image generation
- AI video generation
- AI art generator
- Midjourney alternative
- Stable Diffusion tutorials
- AI photo editing

（注：YOLOX 有 Eli · Visual Creator + Sadie · Video Producer，但**不是**从 prompt 生 raw 图/视频——它们是"调度 + 编辑"，不是内容生成。搜 `AI image generation` 的人要的是 Midjourney。）

### 4.3 AI 开发者工具（4）

- AI coding assistant
- AI code review
- AI debugging
- GitHub Copilot alternative

（纯 dev 用户不是 YOLOX ICP，详见 Day 1 §1 ICP 反例）

### 4.4 AI 教育 / B2B 企业（3）

- AI for education
- AI for classrooms
- enterprise AI solutions

---

## §5 · 弱 Claude 扩展（19）

**规则**：Claude 扩展 173 词里，**无场景锚点 + 纯泛词**的部分。直接砍，不 defer（没战略价值）。

### 5.1 无场景锚的泛词（10）

- AI agent that closes sales while I sleep（太情绪化，实际搜索少）
- AI for sales objection handling（场景太窄 + 无 ICP）
- social media attention monetization AI（词型生硬）
- AI funnel from social to sale（不自然）
- AI bot convert comments to clients（bot ≠ agent，语义冲突 YOLOX）
- reduce sales cycle length AI（学术化表达）
- AI closing script generator（竞品词 more than YOLOX）
- AI to 10x service business（夸张词 SEO 不友好）
- AI client outreach tool（太泛）
- AI to turn likes into leads（不自然）

### 5.2 ICP 错位（5）

- AI for enterprise marketing（YOLOX 不打企业）
- AI for Fortune 500（同上）
- AI for marketing agencies at scale（大代理商不是 ICP）
- AI for CMO at large company（同上）
- AI stack for seed-stage VC（ICP 太窄）

### 5.3 技术深度超出 YOLOX（4）

- multi-agent system architecture（dev 向）
- LLM orchestration framework（dev 向）
- RAG workflow for enterprise（dev 向）
- visual AI agent builder SDK（dev 向）

---

## 给 Agent C 的外链策略提醒（用这份清单）

1. **外链锚文本不用竞品品牌词**：不要为了"蹭 Lindy SEO"就在 Guest post 里用 Lindy alternative 做锚（Lindy 反链监测会警觉）
2. **目录提交分类不选"Zapier alternative"**：选"AI agents for creators" / "AI marketing tools" 这种 YOLOX 站位的分类
3. **Reddit 回答不主动提"Lindy vs YOLOX"**：让读者自己问，我们回答"为什么我们做这个"而不是"为什么 Lindy 不行"（playbook §2.5 反自我宣传原则）

---

## 给 Agent D 的 FAQPage schema 提醒

FAQPage schema 可以**引用** §3 的商业调查词作为 Q，但 A 里绝对不能说"best AI agent is YOLOX"（自夸，Google 对 FAQPage 的评分会扣）。

好范式：
- Q: "What are the main AI agents for solopreneurs?"
- A: "Solopreneurs typically evaluate three categories: [category 1], [category 2], [category 3]. The right choice depends on [criterion]."（中立，带出 YOLOX 所在类别）

---

## 升档信号 · 什么时候把词从负向拿回来

| 信号 | 动作 |
|---|---|
| DR > 20 | 把 §1 竞品品牌词的 `Lindy alternatives` 等 3–5 个词**拿回 Watch List**，写反向对比页（§2.8.2）|
| 前 3 Cluster 已索引 + 有 Impressions | §2 大词里的 "AI agent for solopreneurs" 开 Pillar |
| 6 个月后 | §2 超高 KD 大词可以开始攻（通过 Pillar 承接）|
| 产品方向调整 | §4 定位不符词重新评估（如 YOLOX 加 AI 绘图能力则解锁相关词）|

---

## Day 3 交付清单

- [x] §1–5 五类 117 词分类归档
- [x] 每类带规则 + YOLOX 战略含义
- [x] 给 Agent C / D 的使用提醒
- [x] 升档信号条件

**和 04-keyword-map-v1.md 合并后**：
- 200 进主库 + 117 进负向 = 317（接近 Day 2 的 325 去重后数字，差值 8 在 Day 5 会进一步精调）
