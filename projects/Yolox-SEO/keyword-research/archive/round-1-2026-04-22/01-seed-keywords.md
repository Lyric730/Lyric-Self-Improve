# 01 · 种子词池（Day 1 产出）

**日期**：2026-04-22
**交付等级**：🟢 spike / 候选池（未打分、未分类意图、未映射落地页）
**对应任务**：`docs/seo/tasks/week-2026-04-22/2.3-keyword-research.md` Day 1
**对应 playbook**：§2.3.1 种子词的四条来源

---

## 前言 · 数据来源说明

按 playbook §2.3.1 的 4 条来源并行采集：

| 源 | 采集方法 | 状态 | 词数 |
|---|---|---|---|
| 1. 产品语义（内部） | 读 `messages/en.json`（manifest 拉不到，走文案降级）| ✅ 完成 | 20 |
| 2. 用户语言（Reddit）| OpenCLI `reddit subreddit` / `search` × 7 查询 | ✅ 完成 | 15 |
| 3. 竞品反查（4 站）| WebFetch Lindy / Relevance AI / Zapier AI / n8n 首页 | ✅ 完成 | 17 |
| 4. 品类相邻 | 手工列 + 领域常识 | ✅ 完成 | 18 |

**总计：70 词**（目标 60+ ✅）。Twitter/X 挖词推迟到 Day 2 扩展到 300+ 时并入。

**⚠️ 已知降级**：
- Agent/Skill manifest（`yolox-agent-store` / `yolox-skills-store` 两个私有仓库）jsDelivr 返回 404。已请小刀老师提供 `GITHUB_TOKEN`，Day 2 回头补挖；首页 `heroActionCards` 只曝光 15 个 agent，manifest 可能有更多。
- 所有 KD 字段留空 **TODO**，由小刀老师代查 Ahrefs 或 Day 7 批量补。

---

## 源 1 · 产品语义（20 词）

**采集思路**：从 YOLOX 自己的产品文案里抠，这些是产品团队已经认可的"我们卖什么"。文案源：`messages/en.json`。

### 1.1 核心品类词（5）

| 关键词 | 语义备注 | 文案出处 |
|---|---|---|
| AI agent team | 核心品类词，强调"团队"而不是"单个 agent" | `home.heroMeet/evolving/agent/team` 拼 |
| AI marketing team | YOLOX 15 个首页 Agent 里 12 个是 marketing/growth 角色，这是差异化定位 | `home.heroActionCards` |
| AI agents for solopreneurs | 对齐 `home.placeholder 1–10` 的 ICP 画像 | 平台定位 |
| AI agent store | 产品信息架构词（/agents-store 页面）| `nav.agentsStore` |
| AI skill store | 同上（/skills-store）| `nav.skillsStore` |

### 1.2 ICP 场景词（10，映射 home.placeholder1-10）

| 关键词 | 对应 ICP | 文案出处 |
|---|---|---|
| AI agent for Substack newsletter | paid newsletter writer | `home.placeholder1` |
| AI agent for Shopify store | Shopify 店主 | `home.placeholder2` |
| AI agent for SaaS founders | SaaS builder | `home.placeholder3` |
| AI agent for TikTok creators | short video creator | `home.placeholder5` |
| AI agent for Amazon sellers | Amazon 卖家 | `home.placeholder7` |
| AI agent for YouTube creators | YouTuber | `home.placeholder9` |
| AI agent for indie SaaS | 复合长尾 | placeholder3 + solopreneur 拼 |
| AI agent for course creators | 在线课讲师 | `home.placeholder10` |
| AI agent for growth marketers | growth 团队 | `home.placeholder6` |
| AI marketing agent for solo founders | 长尾组合 | placeholder3 + solo 合并 |

### 1.3 Agent 角色词（5，映射 15 个 heroActionCards 里最硬的 5 个）

| 关键词 | 对应 Agent | 文案出处 |
|---|---|---|
| AI SEO agent | Sophie · SEO Doctor + Isaiah · SEO Content Factory | `home.heroActionCards` |
| AI programmatic SEO builder | Stella · Programmatic SEO Builder | 同上 |
| AI competitor monitoring agent | Evelyn · Competitor Scout | 同上 |
| AI landing page builder | Addison · Landing Page Builder | 同上 |
| AI ad creative generator | Olivia · Ad Creative Studio + Savannah · Paid Ads Strategist | 同上 |

**待挖储备**（先不进 15 词但记下来）：Referral Architect、Launch Strategist、Copy Polisher、Video Producer、Visual Creator、Email Closer、Content Machine、Traffic Commander —— 每一个都能扩出 3–5 个长尾词。Day 2 扩展到 300 时再铺开。

---

## 源 2 · 用户语言 / Reddit（15 词）

**采集方法**：OpenCLI v1.7.6（Node 22 / 路径 `/home/lyric/tools/`），复用 Chrome 登录 session 跑 7 次查询 ≈ 150 条帖子，原始 JSON 存 `~/tools/opencli-raw/day1-*.json`（7 文件）。
**筛词规则**：(1) 是真实求解帖（非新闻/吐槽/AMA），(2) 场景对齐 YOLOX ICP（solopreneur / SMB / creator / marketer），(3) 选 title 可直接当长尾词的。

### 2.1 查询策略迭代（过程记录，反省给小刀老师）

**第一轮失败**：`r/Entrepreneur top-month` / `r/SideProject top-month` / `r/marketing top-month` / `search "how do I automate" top-month` → top posts 都是热门故事/AMA/吐槽，**不是求解帖**。
**反省**：Reddit 的"top"排序由社区 upvote 驱动，排名高的几乎都是叙事帖；**求解帖藏在 `--sort new` 或垂直子版的 `hot`**。
**第二轮修正**：改用 `r/SEO hot-week` / `r/smallbusiness hot-week` / `search "any tool to" new-month` → 前两个命中，第 3 个仍然太泛（污染严重，跨 dataeng/guns/Scanlation）。
**结论**：子版精准度 > 搜索 query 精准度。Day 2 挖 50+ 问句主要吃 `hot` 排序的垂直子版。

### 2.2 挖到的 15 个种子词（每词附原 Reddit thread URL 作证据）

**来自 r/SEO**（5）

| # | 种子词 | 原帖标题（截断）| URL |
|---|---|---|---|
| 1 | why ChatGPT cites one page over another | "Why ChatGPT Cites One Page Over Another (Study of 1.4M Prompts)" | [1ss0drr](https://www.reddit.com/r/SEO/comments/1ss0drr/) |
| 2 | is llms.txt a scam | "Is llms.txt file a scam?" | [1srvco1](https://www.reddit.com/r/SEO/comments/1srvco1/) |
| 3 | how to rank new site vs high traffic sites | "Is it possible for a new site to compete with older high-traffic websites?" | [1sri4ht](https://www.reddit.com/r/SEO/comments/1sri4ht/) |
| 4 | how to structure headings for listicles | 同标题 | [1ss6uxv](https://www.reddit.com/r/SEO/comments/1ss6uxv/) |
| 5 | SEO for local service business | "How to do SEO for a local service business (cleaning company)?" | [1srh3al](https://www.reddit.com/r/SEO/comments/1srh3al/) |

**来自 r/smallbusiness**（5）

| # | 种子词 | 原帖标题（截断）| URL |
|---|---|---|---|
| 6 | how to get more clients for service business | "Need Help With Getting More Clients (lashes, brows etc…)" | [1ss4ibj](https://www.reddit.com/r/smallbusiness/comments/1ss4ibj/) |
| 7 | how to get consistent clients cleaning business | "Struggling to get consistent clients for my cleaning business — what worked for you?" | [1srl89h](https://www.reddit.com/r/smallbusiness/comments/1srl89h/) |
| 8 | how to close more sales faster | "How do I close more sales, and that too faster?" | [1ss8ngr](https://www.reddit.com/r/smallbusiness/comments/1ss8ngr/) |
| 9 | turn social media attention into clients | "How are you turning social media attention into actual clients?" | [1srignl](https://www.reddit.com/r/smallbusiness/comments/1srignl/) |
| 10 | get more genuine Google reviews for business | "What actually helped you get more genuine Google reviews for your business?" | [1srnijf](https://www.reddit.com/r/smallbusiness/comments/1srnijf/) |

**来自 r/Entrepreneur**（3）

| # | 种子词 | 原帖标题（截断）| URL |
|---|---|---|---|
| 11 | build AI workers in plain English | "anthropic just made it possible to build AI workers in plain english" | [1snchax](https://www.reddit.com/r/Entrepreneur/comments/1snchax/) |
| 12 | business held together with duct tape operationally | "Anyone else making good money but feel like their business is held together with duct tape operationally" | [1sd545v](https://www.reddit.com/r/Entrepreneur/comments/1sd545v/) |
| 13 | automate work responsibilities with AI | "Facing disciplinary investigation / sack for automating most of my responsibilities at work" | [1s23k0o](https://www.reddit.com/r/BestofRedditorUpdates/comments/1s23k0o/) |

**来自 r/SideProject**（2）

| # | 种子词 | 原帖标题（截断）| URL |
|---|---|---|---|
| 14 | open source social media scheduling tool | "My girlfriend runs a small social media agency. I got sick of watching her pay 400 bucks a month for scheduling tools, so I built an open-source alternative." | [1sk8fn3](https://www.reddit.com/r/SideProject/comments/1sk8fn3/) |
| 15 | local floating AI assistant for creators | "I built a free, fully local floating AI assistant for macOS. No API keys, no subscriptions, no cloud." | [1sl0rjq](https://www.reddit.com/r/SideProject/comments/1sl0rjq/) |

### 2.3 映射到 YOLOX Agent 角色（策略信号）

这 15 个 Reddit 种子词里，**10/15 能直接对应 en.json `heroActionCards` 的 Agent 角色**：

| Reddit 需求 | YOLOX 现成 Agent |
|---|---|
| 为什么 ChatGPT 引 X 不引 Y | Sophie · SEO Doctor（AEO 维度） |
| llms.txt 是骗局吗 | Sophie · SEO Doctor（AEO 解释器） |
| 新站怎么斗高权重站 | Stella · Programmatic SEO Builder |
| listicle 怎么结构 | Isaiah · SEO Content Factory |
| local SEO for cleaning biz | Stella · Programmatic SEO Builder（local pages 变体） |
| 获客 × 3 条 | Elias · Traffic Commander + Daniel · Email Closer |
| social → client 转化 | Savannah · Paid Ads Strategist + Addison · Landing Page Builder |
| Google review 获取 | Quinn · Referral Architect |
| AI workers in plain English | YOLOX 本身的定位（"one sentence → full business"）|
| 自动化工作职责 | 通用 agentic 定位 |

**战略洞察**：**YOLOX 的 15 个 Agent 和真实 Reddit 求解帖的 mapping 度 ≥ 67%**，说明产品定位和用户痛点高度对齐。Day 5 选 Pillar 时，这 10 条 mapping 就是最好的"Pillar 候选证据"。

### 2.4 原始数据留存

```
~/tools/opencli-raw/
├── day1-entrepreneur-top.json     (r/Entrepreneur top-month, 25 帖)
├── day1-sideproject-top.json      (r/SideProject top-month, 25 帖)
├── day1-marketing-top.json        (r/marketing top-month, 25 帖)
├── day1-search-automate.json      (search "how do I automate", 25 帖)
├── day1-search-anytool.json       (search "any tool to", 30 帖, 噪声大)
├── day1-seo-hot.json              (r/SEO hot-week, 30 帖, 金矿)
└── day1-smallbiz-hot.json         (r/smallbusiness hot-week, 30 帖, 金矿)
```

Day 2 扩展到 50+ 问句时复用这些数据 + 新增 2–3 条 `hot` 查询（r/Shopify / r/SaaS / r/indiehackers）。

---

## 源 3 · 竞品反查（17 词）

**采集方法**：WebFetch 4 个竞品首页，抠"产品自述词"和"use case 标签"。
**降级说明**：无 Ahrefs，本周不做"竞品 top 100 外的长尾词反查"，只做**首页级词汇提取**。下周拿到 Ahrefs 后补完整反查。
**标记**：所有词 `KD: TODO`。

### 3.1 共用高频词（跨 4 站出现，5 词）

| 关键词 | 来源站 | 备注 |
|---|---|---|
| AI agent | lindy / relevance / zapier / n8n | 行业通用词，KD 必然高，进 `deferred` 但留作 pillar 潜在候选 |
| AI workflow automation | zapier / n8n | 赛道中间词 |
| AI agent builder | n8n / zapier | |
| AI assistant | lindy / zapier | 偏日常助手语境 |
| AI integration | zapier (9000+ apps) / n8n (500+) | |

### 3.2 Lindy 独有（3 词）

| 关键词 | 原文案 |
|---|---|
| AI email automation | "Drafts your email, preps your meetings" |
| AI meeting scheduling | "Meeting scheduling, prep and follow-up" |
| AI inbox management | "Manages your inbox automatically" |

### 3.3 Relevance AI 独有（4 词）

| 关键词 | 原文案 |
|---|---|
| AI BDR agent | "BDR Agent" |
| AI SDR agent | "Outbound SDR" |
| AI workforce | "Build AI workforces" / "The home of the AI Workforce" |
| AI GTM automation | "Scale GTM results, without scaling headcount" |

### 3.4 Zapier AI 独有（3 词）

| 关键词 | 原文案 |
|---|---|
| AI lead qualification | "AI Lead Qualification" |
| AI social publishing agent | "AI Social Publishing" |
| AI orchestration | "Your home for AI orchestration" |

### 3.5 n8n 独有（2 词）

| 关键词 | 原文案 |
|---|---|
| visual AI agent builder | "AI agents and workflows you can see and control" |
| RAG workflow | "Handle multi-agent setups and RAG systems" |

### 3.6 YOLOX vs 竞品定位差异观察（不是关键词，是策略笔记）

4 个竞品对比：
- **Lindy** → 个人助理（日历/邮件/会议）
- **Relevance AI** → Sales/GTM（BDR/SDR）
- **Zapier AI** → 企业自动化 orchestration
- **n8n** → 开发者可视化工作流

**YOLOX 的空档**：**AI marketing team for solopreneurs/creators/indie founders** — 4 个竞品都没直接打。
→ 这个定位 = 源 1 的"AI marketing team" / "AI agents for solopreneurs"正好对上，**不是偶然**。

→ Day 5 选 Pillar 时，"AI agents for solopreneurs" 和 "AI marketing team for creators" 是两个强候选。

---

## 源 4 · 品类相邻赛道（18 词）

**采集方法**：列 AI/自动化赛道的相邻品类词，作为 YOLOX 可能出现在用户"平行考虑"里的词。
**标记**：所有词 `KD: TODO`。

### 4.1 自动化赛道（5）

| 关键词 | 备注 |
|---|---|
| no-code automation | 相邻赛道，Zapier/Make 也在打 |
| workflow automation | 同上 |
| business process automation | 偏企业 |
| RPA AI | RPA + AI 融合词 |
| task automation AI | 通用 |

### 4.2 AI Agent 类（5）

| 关键词 | 备注 |
|---|---|
| agentic AI | 2024–2026 新兴词，值得跟 |
| autonomous AI agent | 学术/产品双语境都在用 |
| multi-agent system | RAG + 多 agent 融合 |
| AI copilot | Github Copilot 带火的泛化词 |
| LLM orchestration | Langchain 语境 |

### 4.3 Solo/Indie 场景（4）

| 关键词 | 备注 |
|---|---|
| AI tools for solopreneurs | 正好对上 YOLOX ICP |
| AI for indie hackers | Hacker News 社区常用 |
| AI stack for startups | startup 语境 |
| AI productivity tools | 泛化但高频 |

### 4.4 内容/营销相邻（4）

| 关键词 | 备注 |
|---|---|
| AI content factory | 对应 Isaiah · SEO Content Factory |
| AI marketing automation | 对应 YOLOX 营销 team 定位 |
| AI for content creators | 对应 TikTok/YouTube placeholder |
| AI workflow builder | 偏产品形态词 |

---

## 初步观察 / 给小刀老师的学习笔记

1. **YOLOX 产品定位意外地清晰**：从 `heroActionCards` 15 个 agent 看，YOLOX 是**"AI marketing team"**，不是通用 AI 助手。这意味着：
   - 别和 Lindy/Zapier 争"AI assistant"大词
   - 要抓的是 "AI [具体营销角色] for [具体 ICP]"的超长尾组合，例如：
     - `AI SEO agent for Shopify store` (KD 极可能 < 5)
     - `AI ad creative generator for solopreneurs`
     - `AI competitor scout for SaaS founders`

2. **Skill 和 Agent 可能是两条种子词线**：产品文案区分了 "Agent"（执行者）和 "Skill"（能力芯片）。源 1 目前主要抠了 agent 词。Day 2 manifest 拿到后，skill 词可能能铺出另一批"AI skill for X"的长尾。

3. **Connector 是免费的长尾 × N 生成器**：YOLOX 已集成 Feishu/Gmail/Google Sheets/Notion/Slack/TikTok。每个 connector × 每个 agent 角色 = 一个长尾词（例：`AI agent for Notion automation`、`AI email closer for Gmail`）。这批 Day 2 扩展到 300 时重点铺。

4. **YOLOX 自己的产品文案就指向零量词战场**：`skillDetail.workflowFallback` 直接写了 "Monitor relevant subreddits → auto-reply"。产品团队自己在想 Reddit 场景，这和 §2.3.4 的"零搜索量关键词"策略完美对齐 —— Day 4 的零量词示范，这条直接是第一个样本。

---

## Day 1 交付物清单

- [x] 源 1：20 词（产品语义，从 en.json）
- [x] 源 2：15 词（Reddit，OpenCLI 抓取，每词带原 URL 证据）
- [x] 源 3：17 词（4 竞品反查，WebFetch 降级版）
- [x] 源 4：18 词（品类相邻）
- [x] 目录创建 `docs/seo/keyword-research/`
- [x] 文档 `01-seed-keywords.md` 完整版 🟢

**当前词数**：**70 词**（目标 60+ ✅）

**下周债（Day 2 处理）**：
- Ahrefs KD 统一标 TODO（等小刀老师代查）
- `yolox-agent-store` / `yolox-skills-store` 私有 manifest（等 GITHUB_TOKEN）
- Twitter/X 挖词合并到 Day 2 扩展 300 词里
