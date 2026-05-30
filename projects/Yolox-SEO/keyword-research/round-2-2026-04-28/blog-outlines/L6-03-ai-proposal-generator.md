# L6-03 · `AI proposal generator` · 大纲(精简版)

> **状态**:v0 · 待复审
> **优先级**:Ben 锁定 #3(α Pillar cluster)
> **替换说明**:替换原 `proposal generator`(KD=15 但 -44% 衰退),改用 `AI proposal generator`(KD=34 但"AI"前缀挂上行赛道)

---

## 0 · 元数据

| 字段 | 值 |
|---|---|
| 关键词 | `AI proposal generator` |
| Volume | 530/月 |
| KD | 34 |
| Growth | -50%(注意:词在衰退,但 Ben 选这条因为"AI"前缀挂上行赛道,流量长期看会回升) |
| Search Intent | Commercial / TOOLS(KWFinder Content Type) |
| Tier | Tier 2(8/13) |
| SERP Features | **People Also Ask** ⚠️(必加 FAQ schema) |
| Pillar/Cluster | **α**(AI 工具替代专业岗位) |
| 发布 URL | **`/blog/ai-tools/ai-proposal-generator`** |
| 落地 CTA | → `/agents-store` |

---

## 1 · ICP + 痛点 hypothesis

### 主 ICP
**consultant / freelancer / agency owner** 每周写 3-5 个 proposal,平均 4-8h/份,核心痛点是"重复劳动 + 不个性化 → 客户不读 → 转化率低"。

### 次 ICP
**SMB sales team** 评估 AI proposal 工具替代 PandaDoc / DocuSign。

### 痛点 hypothesis
1. 写 proposal 4-8h/份,大部分时间在调样式 / 找历史模板
2. 不知道哪种结构 conversion 高(没法 A/B test)
3. 客户问"有没有做过类似的"时,翻历史 proposal 找 case study 累
4. PandaDoc / Proposify 太贵 ($25-65/月) 且非 AI-native
5. 用 ChatGPT 自己写,但不知道 prompt 怎么写

### 现有解决方案为什么不够
- PandaDoc:贵 + 不是 AI-first(只是 template + e-sign)
- Notion AI:通用,不专 proposal
- 自己 ChatGPT:prompt 不专,output 套话多

---

## 2 · SERP 现状

| 信号 | 解读 |
|---|---|
| KD=34 | 中等竞争,top 10 是产品页 + listicle |
| Content Type: TOOLS | top 10 多是"产品页"(toolfinder ranking pages) |
| **People Also Ask** | Google 显示 PAA 框 → **FAQ schema 必加,争夺 PAA 位置** |
| Growth -50% | 词流量下滑,但绝对值仍 530/月 + AI 大势,长期会回升 |

### 内容空缺
- top 10 是 affiliate listicle 或厂商 SEO landing
- **缺**:中立 buyer's guide + DIY prompt 模板 + 真实 use case 拆解
- 我们的位置:**vendor-neutral guide + free DIY prompt template + consultant case study**

---

## 3 · 文章结构

### 标题候选
1. ⭐ **"AI Proposal Generator: 7 Tools Compared (Plus a Free DIY Prompt Template, 2026)"**
2. "Best AI Proposal Generators 2026: Buyer's Guide for Consultants & Freelancers"
3. "7 AI Proposal Generators Tested: Pricing, Quality, and a Free Alternative"

### H2 / H3 结构

```
H1: AI Proposal Generator: 7 Tools Compared
    (Plus a Free DIY Prompt Template, 2026)

[TL;DR · 80 字] 7 个 AI proposal generator 对比表 + 真实 consultant
case study(从 6h/份压到 45min)+ 一份能直接用的 ChatGPT/Claude
prompt 模板。无 affiliate,纯实用。

H2.1 · Why proposals are killing your billable hours
  H3 · 真数据:6 个 consultant 平均花在 proposal 的时间(我们做小调研)
  H3 · proposal time → bill rate dilution 的数学

H2.2 · What an AI proposal generator actually does
  H3 · 5 项核心 capability
  H3 · vs 通用 ChatGPT(为什么"专门工具"有时反而比 ChatGPT 差)

H2.3 · 7 best AI proposal generators(对比表)
  H3 · 完整对比表(Tool / Pricing / Best for / Cons / Score)
  H3 · 1) PandaDoc AI
  H3 · 2) Indy
  H3 · 3) Better Proposals
  H3 · 4) Bonsai
  H3 · 5) Proposify
  H3 · 6) Notion AI(general)
  H3 · 7) yolox AI proposal agent(诚实标"我们自家 product",放在中位)

H2.4 · DIY prompt template — free, paste into ChatGPT/Claude
  H3 · 完整 prompt(700 字版)放正文
  H3 · 8 个 input fields 拆解
  H3 · 如何 iterate(prompt engineering 小技巧)

H2.5 · How to evaluate which tool fits your business
  H3 · solo / SMB / agency 不同选择
  H3 · 5 个 evaluation 问题

H2.6 · Common AI proposal mistakes (5 traps)
  H3 · 套话过多 / 不个性化 / 价格写错 / 法律措辞缺失 / 没 follow-up

H2.7 · FAQ(5 条 PAA 优化)
  Q1: Can ChatGPT write proposals?
  Q2: How much does an AI proposal generator cost?
  Q3: Are AI-generated proposals legal?
  Q4: Will clients know I used AI?
  Q5: What's the ROI of AI proposal tools?

CTA:
"yolox 提供 AI proposal agent + 其他 consultant 工具 — [浏览 →](/agents-store)"
```

### 字数预估
- 7 H2 = 2,200 字
- 对比表 + DIY prompt(700 字)= 800 字
- FAQ 5 条 = 250 字
- **总:2,500-3,000 字**

---

## 4 · 内链规划(锚文本配比)

### 上行
- → `/blog/ai-tools` Pillar 主文 · 占位
  - anchor: `the AI tools for solos overview`(branded · 30%)

### 横向(同 α Pillar)
- → `/blog/ai-tools/ai-ad-creative`(α cluster · 占位 / Round-3 做)
  - anchor: `AI ad creative tools`(partial · 30%)
- → `/blog/aeo/services-guide`(L6-01 · 跨 Pillar 弱链,只在"如何让 proposal 在 AI 搜索中被找到"提一下)
  - anchor: `getting found in AI search`(generic · 10%)

### 下行
- → `/agents-store`
  - anchor: `yolox AI proposal agent`(exact match · 30%)

### 外链(EEAT)
- McKinsey 2024 · State of AI in Sales
- HBR · AI in Professional Services
- Hubspot · Sales Proposal Statistics

---

## 5 · CTA 详解

### 主 CTA(文末)
```markdown
> yolox 提供 AI proposal agent + 其他 consultant 工具(invoice / contract /
> follow-up sequence)— [浏览 agents store →](/agents-store)
```

### 次 CTA(中段 2 处)
- H2.3 对比表下方(yolox 那行):"试用 yolox AI proposal agent →"
- H2.4 prompt 模板末:"懒得调 prompt?[直接用 yolox 一键生成 →](/agents-store)"

---

## 6 · 成功指标

### Search Console
| 时间窗 | 目标 |
|---|---|
| 4 周 | 首次 impression |
| 8 周 | impressions > 300/月 + clicks > 50/月 |
| 12 周 | top 5 + clicks > 100/月 |
| 16 周 | top 3 + clicks > 200/月 + PAA 出现 |

### GA4 events
| Event | trigger |
|---|---|
| `blog_view` | 文章页浏览 |
| `blog_scroll_75` | 滚动到 75% |
| `internal_link_click_agent_store` | 点击 CTA |
| `external_link_click_competitor` | 点击 PandaDoc/Proposify 等外链(竞品研究指标)|

---

## 7 · 风险

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 🐛 listicle 包含自家产品被 Google 判 promotional | 中 | yolox 放在第 7 位(中位偏后)+ 客观打分,劣势写明 |
| 🐛 PAA 优化不到位,被竞品占 | 中 | FAQ 5 条精准答 PAA 高频问题,加 FAQ schema |
| 🔑 数据(consultant 6h/份)需要 own research | 中 | Round-3 做小型 survey(10-15 个 consultant)。本文先用 secondary source(Hubspot 数据)|

---

## 8 · 复审 checklist

- [ ] listicle 包含 yolox 自家产品 OK?(还是只对比外部 6 个)
- [ ] DIY prompt 模板放正文(不锁邮箱)OK?
- [ ] consultant 6h/份的数据,Round-3 做 own survey vs 本轮先用 Hubspot secondary?
- [ ] FAQ 5 条直接 target Google PAA 当前的 5 个问题 — 我会写文章前去 google 确认 PAA 实际显示什么
