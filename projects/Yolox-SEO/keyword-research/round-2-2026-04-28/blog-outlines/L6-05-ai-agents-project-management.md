# L6-05 · `ai agents for project management` · 大纲(精简版)

> **状态**:v0 · 待复审
> **优先级**:Ben 锁定 #5(β Pillar cluster)

---

## 0 · 元数据

| 字段 | 值 |
|---|---|
| 关键词 | `ai agents for project management` |
| Volume | 120/月 |
| KD | **25**(中低) |
| Growth | **+158%** |
| Search Intent | Informational + Commercial(用户在 evaluate)|
| Tier | Tier 2(8/13) |
| SERP Features | 干净(无 AI Overview / 无 PAA) |
| Pillar/Cluster | **β**(B2B Sales & 招聘 AI) |
| 发布 URL | **`/blog/b2b/ai-agents-project-management`** |
| 落地 CTA | → `/agents-store`(直接挂 yolox PM agents) |

---

## 1 · ICP + 痛点 hypothesis

### 主 ICP
**PM / project lead / scrum master**,听说"AI agents"对 PM 工作有帮助,在 evaluate 是不是该用 / 选哪个工具。

### 次 ICP
**SMB owner 兼 PM**(没专职 PM),工具是 Asana/Notion 但效率低。

### 痛点 hypothesis
1. 每天 30-50% 时间在 status update / chase up / 跟进 — 重复劳动
2. Asana/Notion AI 太弱(只是 summarize / draft,不是真"agent")
3. Slack messages / email / Notion 数据散乱,看不到 project 全貌
4. 风险预警靠 PM 主观感觉(没数据驱动)
5. AI agent 听起来不错但**不知道实际能做啥** — vendor 都吹得天花乱坠

### 现有解决方案为什么不够
- Notion AI / Asana Intelligence:summarize / draft 级别,不是 multi-step agent
- Make / Zapier:无 AI,只是 trigger 链
- 通用 ChatGPT:没接 project context,每次重复 paste

---

## 2 · SERP 现状

| 信号 | 解读 |
|---|---|
| 干净 SERP | 标准 organic 玩法 |
| KD=25 | 中低,有机会快上 |
| Volume 120 + Growth +158% | 词在快速崛起,top 10 还没沉淀 → **早投早占位** |

### 内容空缺
- top 10 多是"Top 10 AI PM tools" listicle 或厂商 landing
- **缺**:"what AI agents *should* do for PM(vs 现有 AI features)" + 6 个 use case 拆解 + DIY low-code workflow
- 我们的位置:**vision-driven guide + 6 use cases + DIY alternative**

---

## 3 · 文章结构

### 标题候选
1. ⭐ **"AI Agents for Project Management: 6 Use Cases That Replace Manual Work (2026)"**
2. "Beyond Notion AI: What True AI Agents Can Do for Project Managers"
3. "AI Project Management Agents: A 2026 Buyer's Guide for Modern PMs"

### H2 / H3 结构

```
H1: AI Agents for Project Management: 6 Use Cases That Replace Manual Work (2026)

[TL;DR · 80 字] AI agents 不是 Notion AI 的"summarize"功能 —
是能跑多步任务的 autonomous workers。本文 6 个 PM 实际 use case +
工具评估 5 问 + DIY 用 Make + Claude API 低成本搭一个的方法。

H2.1 · Why current "AI PM features" aren't enough
  H3 · Notion AI / Asana Intelligence 的局限
  H3 · "AI feature" vs "AI agent" 的本质差别(autonomy / multi-step)

H2.2 · What is an AI agent (vs LLM features, vs RPA)
  H3 · 一句话定义
  H3 · 3 类对比:LLM feature / Agent / RPA
  H3 · 关键能力:tool use / planning / memory / multi-step

H2.3 · 6 use cases for PM
  H3 · UC1 - Daily standup synthesis(Slack/email → 日报)
  H3 · UC2 - Risk detection(project log + Slack → 早预警)
  H3 · UC3 - Task assignment optimization(load balance based on capacity)
  H3 · UC4 - Meeting → action items auto-extraction
  H3 · UC5 - Stakeholder update generation(每周自动 draft)
  H3 · UC6 - Resource forecast(基于 historical velocity 预测)

H2.4 · How to evaluate an AI agent for your team
  H3 · Q1 - 接哪些数据源?(Slack / Notion / Linear / GitHub)
  H3 · Q2 - 怎么 customize?
  H3 · Q3 - human-in-loop 还是 fully autonomous?
  H3 · Q4 - data privacy(你的 project 数据上 LLM 训练吗?)
  H3 · Q5 - pricing model(per agent / per seat / per task)

H2.5 · DIY:low-code AI agent with Make + Claude API + Slack
  H3 · 架构图(Make → Claude → Slack)
  H3 · 4 个 trigger
  H3 · 真实 prompt 模板(放正文)
  H3 · 月成本估算($10-30 取决于使用量)

H2.6 · What to expect in 12 months
  H3 · 主流 PM SaaS 都会出"AI agent" feature(竞争激化)
  H3 · 真正 differentiator = 你的数据 + customization
  H3 · 推荐 small team 先 DIY,等市场成熟再换 SaaS

H2.7 · FAQ(5 条)
  Q1: How is an AI agent different from Notion AI?
  Q2: Can AI agents replace project managers?
  Q3: How much do AI agents for PM cost?
  Q4: Are AI agents secure (project data privacy)?
  Q5: What's the best AI agent for small teams?

CTA:
"yolox 提供 PM AI agents:standup-synth / risk-detector /
stakeholder-update-drafter — [浏览 →](/agents-store)"
```

### 字数预估
- 7 H2 = 2,400 字
- 6 use cases 拆解 = 800 字
- DIY 架构 + prompt = 400 字
- **总:2,800-3,200 字**

> Vision-driven 长文,KD=25 + 词新崛起,需要权威长度

---

## 4 · 内链规划(锚文本配比)

### 上行
- → `/blog/b2b` Pillar 主文 · 占位
  - anchor: `B2B operations toolkit overview`(branded · 30%)

### 横向(同 β Pillar)
- → `/blog/b2b/cold-email-deliverability`(L6-04)
  - anchor: `automating sales outreach`(partial · 30%)
- → `/blog/b2b/ai-tools-for-recruiting`(L6-06)
  - anchor: `AI in recruiting workflow`(partial · 30%)

### 下行
- → `/agents-store`
  - anchor: `yolox PM agents`(exact match · 30%)
  - anchor: `try our project management agents`(partial · 30%)
  - anchor: `learn more`(generic · 10%)

### 外链(EEAT)
- Anthropic · Claude tool use docs(权威 LLM agent 文档)
- LangChain · agent architecture guide
- Asana · State of Work 2025 report

---

## 5 · CTA 详解

### 主 CTA(文末)
```markdown
> yolox 提供 PM AI agents:
> · standup-synth(每日 standup 自动汇总)
> · risk-detector(从 project log 提取风险信号)
> · stakeholder-update-drafter(stakeholder 周报 draft)
> [浏览 →](/agents-store)
```

### 次 CTA(中段 2 处)
- H2.3 6 use cases 末:"想直接用?yolox 已实现 UC1/UC2/UC5 的 agent → /agents-store"
- H2.5 DIY 末:"懒得自己搭?yolox 一键启动 →"

---

## 6 · 成功指标

### Search Console
| 时间窗 | 目标 |
|---|---|
| 4 周 | 首次 impression |
| 8 周 | impressions > 200/月 + clicks > 40/月 |
| 12 周 | top 5 + clicks > 80/月 |
| 16 周 | top 3 + clicks > 150/月 |

### GA4 events
| Event | trigger |
|---|---|
| `blog_view` | 文章页浏览 |
| `blog_scroll_75` | 滚动到 75% |
| `internal_link_click_agent_store` | 点击 CTA |
| `external_link_click_anthropic` | 引用外链点击(权威信号验证)|

---

## 7 · 风险

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 🐛 主流 PM SaaS 12 月内会跟进出 AI agent feature → 词 KD 飙升 | 中 | 12 周内拿到 top 3 排名(KD 现在还低)|
| 🐛 use case 6 个写得不深 → 看起来"vendor pitch" | 中 | 每个 use case 配真实 workflow 截图 / 数据 |
| 🟡 Risk detector / forecast 是高级 agent,yolox 现在有吗? | 中 | 文章 ship 时,具体 agent CTA 改为 yolox 已 ship 的;未 ship 的标"alpha 阶段" |

---

## 8 · 复审 checklist

- [ ] 6 个 use case 全部能挂到 yolox agents 吗?
- [ ] DIY low-code 教程会不会"教竞品"?(我认为 OK,因为 DIY 还是麻烦,大多数人最后会选 SaaS)
- [ ] yolox 当前的 PM agents 列表 — 我能拿到吗?(写文章前要核对真实可用)
