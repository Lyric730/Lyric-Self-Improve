# L6-04 · `cold email deliverability` · 大纲(精简版)

> **状态**:v0 · 待复审
> **优先级**:Ben 锁定 #4(β Pillar cluster)

---

## 0 · 元数据

| 字段 | 值 |
|---|---|
| 关键词 | `cold email deliverability` |
| Volume | 40/月 |
| KD | **17**(低) |
| Growth | +50% |
| Search Intent | Informational(技术深度类) |
| Tier | Tier 2(7/13) |
| SERP Features | **AI Overview** ⚠️ |
| Pillar/Cluster | **β**(B2B Sales & 招聘 AI) |
| 发布 URL | **`/blog/b2b/cold-email-deliverability`** |
| 落地 CTA | → `/agents-store` |

---

## 1 · ICP + 痛点 hypothesis

### 主 ICP
**SDR / sales 自营 cold outreach 的 founder**,搜这词的人都已经发了 cold email 但**进 spam 不知道为啥**。技术层面有点摸不着头脑(SPF/DKIM/DMARC 是天书)。

### 次 ICP
**新建 sales team 的 SMB owner**,提前研究"如何不进 spam"。

### 痛点 hypothesis
1. 邮件全进 spam,open rate < 5%(行业平均 25-35%)
2. 不懂 SPF / DKIM / DMARC,自己配怕配错
3. 卖工具的(Lemlist, Smartlead, Instantly)$50-150/月,小团队用不起
4. inbox warmup 流程复杂(谁帮 warm?warm 多久?)
5. 不知道 deliverability 怎么测(发到 spam 自己看不到)

### 现有解决方案为什么不够
- 工具厂商 blog 都"自卖自夸"(用我们工具就行,不教原理)
- 技术博客太深(写给 ops engineer,不是 SDR)
- DIY 没 checklist,每次靠经验

---

## 2 · SERP 现状

| 信号 | 解读 |
|---|---|
| **AI Overview 占位** ⚠️ | Google 给 AI 摘要,organic CTR 腰斩 → 战略 = 被 AI 引用 |
| KD=17 | 极低,1-3 个月可上首页 |
| Volume 40 + Growth +50% | 词在崛起,词龄不长 |

### 内容空缺
- top 10 大多是 Lemlist / Smartlead / Mailchimp 自家文章(promotional)
- **缺**:vendor-neutral 完整指南 + 检查 checklist + 测试工具列表 + 真实 recovery case
- 我们的位置:**Complete neutral guide + tested tools + recovery playbook**(为 AI Overview 引用优化)

---

## 3 · 文章结构

### 标题候选
1. ⭐ **"Cold Email Deliverability: The 2026 Complete Guide (Setup, Testing, and Recovery)"**
2. "Cold Email Deliverability 2026: Why You're Hitting Spam (and How to Fix It)"
3. "The Cold Email Deliverability Stack: 5 Layers Every SDR Should Know"

### H2 / H3 结构

```
H1: Cold Email Deliverability: The 2026 Complete Guide
    (Setup, Testing, and Recovery)

[TL;DR · 80 字] Cold email 进 spam 的 5 层原因(DNS / IP / sender score
/ content / engagement),完整 setup checklist + 4 个免费测试工具 +
recovery playbook(已经掉进 spam 怎么救回来)。

H2.1 · What is cold email deliverability (一句话定义 + 3 因素)
  H3 · 一句话定义
  H3 · open rate vs deliverability(2 概念别混)
  H3 · 数据:行业平均 deliverability(SparkPost / Mailgun reports)

H2.2 · The 5-tier deliverability stack
  H3 · Tier 1 - DNS records(SPF / DKIM / DMARC)
  H3 · Tier 2 - IP reputation
  H3 · Tier 3 - sender score / domain age
  H3 · Tier 4 - content signals(spam triggers / link ratio / image ratio)
  H3 · Tier 5 - engagement(open / reply / forward = 正向信号)

H2.3 · Setup checklist(SPF / DKIM / DMARC 一步步)
  H3 · SPF setup(含 cloudflare / Google Workspace 真实截图)
  H3 · DKIM setup
  H3 · DMARC setup(p=none → p=quarantine 渐进策略)
  H3 · custom domain warmup(4-week schedule 表)

H2.4 · Testing tools(免费 vs 付费哪个值得)
  H3 · mail-tester.com(免费,基础)
  H3 · GlockApps(付费,best for serious)
  H3 · Lemwarm / Mailwarm(warmup 集成,有免费试)
  H3 · 自测脚本(给 dev:DKIM / SPF / DMARC 一键检查 bash + Python)

H2.5 · Recovery playbook — 已经掉到 spam 怎么救
  H3 · Phase 1 - 暂停 cold,只发 warm(1-2 周)
  H3 · Phase 2 - 修复 DNS + 内容
  H3 · Phase 3 - 渐进重启(从 100 封/天开始)
  H3 · 真实 case study(找一个公开 case 引用)

H2.6 · Content best practices(影响 deliverability 的 7 条)
  H3 · subject line 规则
  H3 · 正文 word count
  H3 · 链接 / 图片比例
  H3 · signature 设计
  H3 · CTAs / unsubscribe link

H2.7 · FAQ(5 条,AI Overview 优化重点)
  Q1: Why are my cold emails going to spam?
  Q2: How long does email warmup take?
  Q3: Can I send cold email from Gmail?
  Q4: What's a good open rate for cold email?
  Q5: Do I need a separate domain for cold email?

CTA:
"yolox 提供 AI agents 帮你做 cold outreach 的 personalization +
follow-up sequence — [浏览 agents store →](/agents-store)"
```

### 字数预估
- 7 H2 = 2,200 字
- DNS setup 截图 + 测试脚本 = 400 字
- FAQ 5 条 = 250 字
- **总:2,500-3,000 字**

> 技术深度文章 + AI Overview 引用优化 → 中长篇(2500+)

---

## 4 · 内链规划(锚文本配比)

### 上行
- → `/blog/b2b` Pillar 主文 · 占位
  - anchor: `B2B sales operations overview`(branded · 30%)

### 横向(同 β Pillar)
- → `/blog/b2b/ai-tools-for-recruiting`(L6-06)
  - anchor: `AI in recruiting outreach`(partial · 30%)
- → `/blog/b2b/ai-agents-project-management`(L6-05)
  - anchor: `automating sales workflows with AI agents`(partial · 30%)

### 跨 Pillar(弱链,谨慎)
- → `/blog/aeo/services-guide`(L6-01)— 在"如何被 AI 引用"小节提
  - anchor: `getting cited by AI Overview`(exact AEO partial · 10%)

### 下行
- → `/agents-store`
  - anchor: `yolox cold outreach agent`(branded · 30%)

### 外链(EEAT + AI Overview 引用)
- Google Postmaster Tools docs
- SparkPost 2025 deliverability report
- Mailgun · email authentication guide

---

## 5 · CTA 详解

### 主 CTA(文末)
```markdown
> yolox 提供 AI agents 帮 cold outreach personalization +
> follow-up sequence + reply 分类 — [浏览 →](/agents-store)
```

### 次 CTA(中段 2 处)
- H2.3 setup checklist 末:"配置完想要自动监控 deliverability?yolox 的
  cold-email-monitor agent → /agents-store"
- H2.5 recovery 末:"想自动跑 recovery playbook?yolox AI agents 列表 →"

---

## 6 · 成功指标

### Search Console
| 时间窗 | 目标 |
|---|---|
| 4 周 | 首次 impression(KD=17 易 index)|
| 8 周 | impressions > 100/月 + clicks > 30/月 |
| 12 周 | top 5 + clicks > 80/月 + AI Overview 开始引用我们 |

### GA4 events
| Event | trigger |
|---|---|
| `blog_view` | 文章页浏览 |
| `blog_scroll_75` | 滚动到 75% |
| `blog_code_copy` | 复制 DNS 配置脚本(JS clipboard 监听) |
| `internal_link_click_agent_store` | 点击 CTA |

### LLM 引用监测
| 检查 | 目标 |
|---|---|
| ChatGPT "cold email deliverability" | 12 周内被引用至少 1 次 |
| Google AI Overview | 12 周后被引用 |

---

## 7 · 风险

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 🐛 AI Overview 抢流量(40/月词,组件被 AI 摘要后 organic 流量更小) | 高 | 战略 = 被引用,不是 organic 排名(转化靠 CTA + agent store) |
| 🐛 技术深度文章受众窄 | 中 | 文章顶部加"too technical?跳到 H2.5 recovery playbook" 锚链接 |
| 💸 真实 DNS setup 截图需要后端 ops 资源 | 低 | 用通用 cloudflare / Google Workspace 公开文档截图,不暴露 yolox 真实配置 |

---

## 8 · 复审 checklist

- [ ] 5-tier 模型是否过技术?要不要加 layperson 版?
- [ ] DNS 截图(SPF/DKIM/DMARC 配置过程)能找资源做吗?
- [ ] AI Overview 引用监测可执行?(目前需要手工 check)
- [ ] cold-email-monitor agent 是 Round-3 计划中?
