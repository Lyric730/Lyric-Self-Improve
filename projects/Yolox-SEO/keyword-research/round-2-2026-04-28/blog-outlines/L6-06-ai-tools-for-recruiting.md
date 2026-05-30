# L6-06 · `ai tools for recruiting` · 大纲(精简版)

> **状态**:v0 · 待复审
> **优先级**:Ben 锁定 #6(β Pillar 主词,临时作为 cluster 文章)
> **特殊说明**:这是 β Pillar 的**主词**。Round-3 做 Pillar 主文时,这篇可保留为 cluster + 旁列出 β 主词文章,或者把这篇升级为 β 主文(Round-3 决定)。本轮先按 cluster 处理。

---

## 0 · 元数据

| 字段 | 值 |
|---|---|
| 关键词 | `ai tools for recruiting` |
| Volume | 340/月 |
| KD | **25**(中低) |
| Growth | -14%(轻微衰退,但 absolute 流量仍可观)|
| Search Intent | Commercial(buyer's guide 找工具)|
| Tier | Tier 2(6/13) |
| SERP Features | 干净 |
| Pillar/Cluster | **β**(B2B Sales & 招聘 AI · 主词) |
| 发布 URL | **`/blog/b2b/ai-tools-for-recruiting`**(Round-3 决定是否改为 `/blog/b2b/recruiting`) |
| 落地 CTA | → `/agents-store` |

---

## 1 · ICP + 痛点 hypothesis

### 主 ICP
**in-house recruiter / talent partner**,在 evaluate 是否引入 AI tools 进 recruiting 流程,需要 stage-by-stage 的对比。

### 次 ICP
**recruiting agency owner / 招聘 SaaS 评估的 HR 头**。

### 痛点 hypothesis
1. **sourcing 占 60%+ 时间**(LinkedIn 翻找 / Indeed 投递 / 主动联系)
2. screening 是枯燥重复劳动(看 resume / 第一轮电话)
3. candidate experience 差(回复慢 / 流程不透明)
4. 工具碎片(LinkedIn Recruiter / Indeed / iCIMS / Greenhouse)— **数据不通**
5. 主流 ATS "AI" 大多只是 keyword match(不是真 AI)

### 现有解决方案为什么不够
- 列表型博文都是"Top 15 AI recruiting tools",只罗列产品没拆解流程
- 厂商 landing 都自卖自夸
- LinkedIn / Indeed 自家 AI 弱 + 锁在他们生态

---

## 2 · SERP 现状

| 信号 | 解读 |
|---|---|
| 干净 SERP | 标准 organic |
| KD=25 | 中低,有机会 |
| Volume 340 + Growth -14% | 老 evergreen 词,搜的人 stable |

### 内容空缺
- top 10 都是"Top 15 AI recruiting tools" 大乱炖
- **缺**:**stage-by-stage 流程分解**(sourcing / screening / engagement / assessment / offer)+ 各 stage 最值得用的 + 综合 stack 推荐
- 我们的位置:**Stage-by-stage breakdown + recommended stack(small / mid / enterprise)**

---

## 3 · 文章结构

### 标题候选
1. ⭐ **"AI Tools for Recruiting: A Stage-by-Stage Breakdown (Sourcing → Offer, 2026)"**
2. "The 2026 AI Recruiting Stack: 5 Stages, 25 Tools, and What to Pick"
3. "Beyond 'Top 15 Lists': How to Build Your AI Recruiting Stack in 2026"

### H2 / H3 结构

```
H1: AI Tools for Recruiting: A Stage-by-Stage Breakdown (Sourcing → Offer, 2026)

[TL;DR · 80 字] 不再是"Top 15 AI recruiting tools" 大乱炖,本文按
招聘 5 个 stage(sourcing / screening / engagement / assessment / offer)
拆解每 stage 最值得用的 AI 工具 + 给 3 个 stack 推荐
(small team / mid / enterprise)。

H2.1 · Why most "Top X AI recruiting tools" lists miss the point
  H3 · 招聘是 5 阶段流程,不是 1 个工具能搞定
  H3 · 工具碎片化 + 数据孤岛是真问题

H2.2 · The recruiting funnel(5 stages overview)
  H3 · 5 stages 各占多少时间(Recruiter survey 数据 — secondary source)
  H3 · 每 stage AI 能省的时间 %

H2.3 · Stage 1 - Sourcing AI tools
  H3 · Hiretual(全网搜索 + Boolean AI)
  H3 · SeekOut(diversity 招聘强项)
  H3 · LinkedIn Recruiter AI(LinkedIn 内生态)
  H3 · 哪个 best for solo recruiter / agency / in-house

H2.4 · Stage 2 - Screening AI
  H3 · HireVue(video interview 自动评分)
  H3 · Pymetrics(behavioral assessment AI)
  H3 · Sapia(chat-based assessment)
  H3 · Bias 风险(EEOC 合规警告)

H2.5 · Stage 3 - Engagement AI
  H3 · Paradox(Olivia chatbot,large enterprise)
  H3 · Sense / Smashfly(text-based engagement)
  H3 · 对 candidate experience 的实测影响数据

H2.6 · Stage 4 - Assessment AI
  H3 · Codility AI(技术岗,代码评测)
  H3 · TestGorilla(general skills AI)
  H3 · 能否替代第一轮人工 screening

H2.7 · Stage 5 - Offer & Onboarding AI
  H3 · Eightfold(internal mobility + onboarding)
  H3 · ChartHop(comp / equity 自动 model)
  H3 · 这 stage AI 影响最小,但增长快

H2.8 · Recommended workflow stack(3 推荐)
  H3 · Solo recruiter / 小 agency:Hiretual + Paradox(基础组合)
  H3 · Mid in-house team(20-100 hires/year):+ HireVue + Codility
  H3 · Enterprise:Eightfold + LinkedIn Recruiter AI + 多 stages 集成

H2.9 · FAQ(5 条)
  Q1: Are AI recruiting tools EEOC compliant?
  Q2: How much do AI recruiting tools cost?
  Q3: Can AI replace recruiters entirely?
  Q4: What's the best AI tool for small recruiting teams?
  Q5: How long to implement an AI recruiting stack?

CTA:
"yolox 提供 recruiting AI agents — sourcing / screening / engagement
全 stage 覆盖 — [浏览 →](/agents-store)"
```

### 字数预估
- 9 H2 = 2,800 字(更长因为按 stage 拆 5 个)
- stage 工具对比表 = 400 字
- recommended stacks 3 个 = 300 字
- FAQ 5 条 = 250 字
- **总:3,000-3,500 字**

> Stage-by-stage 长文,β 主词候选,需要权威 length 占住主词排名

---

## 4 · 内链规划(锚文本配比)

### 上行
- → `/blog/b2b` Pillar 主文 · 占位 — Round-3 ship 后这篇文章作为 cluster,本身退一步
  - anchor: `B2B operations overview`(branded · 30%)

### 横向(同 β Pillar)
- → `/blog/b2b/cold-email-deliverability`(L6-04)
  - anchor: `cold outreach deliverability`(partial · 30%)
- → `/blog/b2b/ai-agents-project-management`(L6-05)
  - anchor: `AI agents in PM workflows`(partial · 30%)

### 下行
- → `/agents-store`(主 CTA)
  - anchor: `yolox recruiting agents`(exact · 30%)
  - anchor: `try our sourcing AI`(branded · 30%)
  - anchor: `more AI agents`(generic · 10%)

### 外链(EEAT)
- LinkedIn 2025 Talent Trends Report
- SHRM · AI in HR survey
- EEOC · AI bias guidance(合规权威)

---

## 5 · CTA 详解

### 主 CTA(文末)
```markdown
> yolox 提供 recruiting AI agents:
> · sourcing-agent(LinkedIn / GitHub / X 全网 sourcing)
> · screening-agent(resume + JD match + 第一轮 outreach)
> · engagement-agent(text-based candidate engagement)
> [浏览 →](/agents-store)
```

### 次 CTA(中段 2 处)
- H2.3 sourcing 末:"想 unified sourcing across 平台?yolox sourcing-agent → /agents-store"
- H2.8 recommended stacks 末:"yolox 是 stack 的核心 layer 之一 →"

---

## 6 · 成功指标

### Search Console
| 时间窗 | 目标 |
|---|---|
| 4 周 | 首次 impression |
| 8 周 | impressions > 500/月 + clicks > 80/月 |
| 12 周 | top 5 + clicks > 200/月 |
| 16 周 | top 3 + clicks > 400/月 |

### GA4 events
| Event | trigger |
|---|---|
| `blog_view` | 文章页浏览 |
| `blog_scroll_75` | 滚动到 75% |
| `internal_link_click_agent_store` | 点击 CTA |
| `blog_table_view` | stage 工具对比表查看(可选 scroll-into-view 监听)|

---

## 7 · 风险

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 🐛 涉及 25 个工具,**写错事实**风险高(pricing / features 容易过时)| 高 | 文章顶部加"Last reviewed 2026-05-XX,工具 features/pricing 可能变更",每 6 月 review |
| 🐛 EEOC bias 合规警告写不到位 = 法律风险 | 高 | H2.4 专门一节,引 EEOC 官方 + 加 disclaimer |
| 🟡 yolox recruiting agents 当前实际状态? | 中 | ship 前核对 yolox agents-store 实际 ship 的 recruiting agents,CTA 只标真实可用的 |

---

## 8 · 复审 checklist

- [ ] β Pillar 主词文章本轮处理为 cluster — Round-3 是否升级为 Pillar 主文?
- [ ] 25 个工具事实 — Round-3 做 quarterly review 制度吗?
- [ ] yolox 当前 recruiting agents 列表能拿到吗?(L7 ship 前核对)
- [ ] EEOC bias 合规警告由谁 sign-off?(法律 review)

---

# 6 篇 L6 大纲全部完成

| # | 文件 | 关键词 | URL | KD | Growth | 字数 |
|---|---|---|---|---|---|---|
| 1 | `L6-01-aeo-services.md` | answer engine optimization services | `/blog/aeo/services-guide` | 19 | +909% | 2500-2800 |
| 2 | `L6-02-podcast-guest-release-form.md` | podcast guest release form | `/blog/creator/podcast-guest-release-form` | 8 | -43% | 1800-2200 |
| 3 | `L6-03-ai-proposal-generator.md` | AI proposal generator | `/blog/ai-tools/ai-proposal-generator` | 34 | -50% | 2500-3000 |
| 4 | `L6-04-cold-email-deliverability.md` | cold email deliverability | `/blog/b2b/cold-email-deliverability` | 17 | +50% | 2500-3000 |
| 5 | `L6-05-ai-agents-project-management.md` | ai agents for project management | `/blog/b2b/ai-agents-project-management` | 25 | +158% | 2800-3200 |
| 6 | `L6-06-ai-tools-for-recruiting.md` | ai tools for recruiting | `/blog/b2b/ai-tools-for-recruiting` | 25 | -14% | 3000-3500 |

**总字数预估:14,800-17,700 字**(6 篇)
