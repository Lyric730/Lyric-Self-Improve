# Semrush Pro 7-day Free Trial · 操作 SOP

**日期**：2026-05-02
**面向**：小刀老师（Semrush 操作）
**目的**：用 Pro 7-day Free Trial 完成 L2 Step 2d/2e + L2 Step 4 + L4 + L7 共 5 个使用点
**前提**：trial 是 free（绑卡需 cancel），数据量大于 Ahrefs $7 trial

---

## 0 · 激活前 checklist

- [ ] 准备 1 张可绑定的 credit card（trial 期不收费但需预授权）
- [ ] 用一个**无 Semrush 历史**的邮箱（trial 限 1 次/邮箱）
- [ ] 浏览器开 Cookie + JS

⏰ **激活后立即记录日期** + 设置 calendar 第 6 天提醒 cancel（避免被扣 $139.95/月）

---

## 1 · 激活步骤

```
1. https://www.semrush.com/free-trial/ → "Start free trial"
2. 选 Pro plan 7-day free trial
3. 注册账号 + 绑定 credit card（不会立即扣，预授权 $1-10 trial 期满退）
4. 验证邮箱 → 进 dashboard
5. 验证：能进 Keyword Magic Tool + Organic Research + Domain Overview
```

---

## 2 · L2 Step 2d/2e · Keyword Magic Tool（KMT）

### 路径 A · 完整 76 词（彻底但慢，~1.5 hr）

每词单独跑 KMT，每词导出 1 份 broad match CSV + 1 份 questions CSV。

### 路径 B · 精华 30 词（推荐，~45 min）

精华清单：覆盖 25 ICP 重点词 + 7 EXPLORATORY 全保留 + Step 5 高 hits 词。完整 30 词清单见 §6。

### KMT 操作（每词重复）

```
1. https://www.semrush.com/analytics/keywordmagic/
2. Database 选 "United States" (或 "Worldwide")
3. 输入框输入 1 个 seed keyword（如 "AI agent for code review"）→ Search
4. 默认 Broad match tab，看到该 seed 扩展的关键词列表
5. 顶部 Filter 设：
   - Volume: > 0（去掉无搜索量）
   - KD: 不限（先全拿）
   - Word Count: 不限
6. 顶部 Export → CSV → 选 "Top 1000" 或 "All filtered"
7. 保存到 /tmp/semrush-kmt-broad-{seed-slug}.csv

8. 切换 tab 到 "Questions"
9. 同样 Filter + Export → /tmp/semrush-kmt-questions-{seed-slug}.csv
```

**slug 命名约定**：seed keyword 转 lowercase + replace spaces with hyphens
- `AI agent for code review` → `ai-agent-for-code-review`
- 文件名：`/tmp/semrush-kmt-broad-ai-agent-for-code-review.csv`

**预期产出**：
- 30 seeds × 200-500 broad match rows = 6000-15000 词
- 30 seeds × 50-100 questions rows = 1500-3000 词
- **总 ~7500-18000 候选词**（远超 L2 §1 目标 6000-10500）

---

## 3 · L2 Step 4 · Organic Research（Site Explorer 等价）

5 个域名分别跑：

| # | 域名 | filter | 导出文件 |
|---|---|---|---|
| 1 | lindy.ai | Country = US | `/tmp/semrush-organic-lindy.csv` |
| 2 | relevance.ai | Country = US | `/tmp/semrush-organic-relevance.csv` |
| 3 | zapier.com | URL contains `/ai/` | `/tmp/semrush-organic-zapier.csv` |
| 4 | n8n.io | Country = US | `/tmp/semrush-organic-n8n.csv` |
| 5 | make.com | Country = US | `/tmp/semrush-organic-make.csv` |

### 操作（每域名重复）

```
1. https://www.semrush.com/analytics/organic/
2. 输入域名（如 lindy.ai）→ Search
3. 左导航 "Positions"（即域名的 organic keywords）
4. Country 选 United States
5. 顶部 Filter:
   - Position: 1-100
   - Volume: > 0
   - 仅 zapier: URL contains "/ai/"
6. 排序 by Traffic % desc 或 Volume desc
7. 顶部 Export → CSV → "Top 1000" (Pro plan limit)
8. 保存到对应 /tmp/semrush-organic-{domain}.csv
```

**预期**：每站 1000 行 × 5 = 5000 行（合并去重后 ~3000-4500 unique）

---

## 4 · trial 倒计时管理

trial 7 天内完成：
- ✅ Step 2d/2e（本周）→ KMT × 30 seeds × 2 tab = 60 CSV
- ✅ Step 4（本周）→ Organic Research × 5 站 = 5 CSV
- ⏳ L4 主库 v0 KD + Volume 精排（约 1 周后，主库做完 L3 后跑）
- ⏳ L7 主库 v1 最终精排（trial 期内最后 1-2 天用完）

**风险提示**：
- 🔑 trial 自动续约 → **第 6 天**进 settings 手动 cancel 避免被扣 $139.95/月
- 🔑 CSV 数据**离线下载**保留——trial 结束后 Semrush 进不去，但 CSV 永久可用

---

## 5 · 激活后告诉 Agent B 什么

回到 conversation 告诉我：
1. ✅ trial 已激活（具体日期 + 时间 → 我标 expiry = +7 天）
2. CSV 文件路径（按 §2 §3 命名约定，我直接读 `/tmp/semrush-*.csv`）
3. 选了路径 A（76 词）还是路径 B（30 词）

我会立刻开始：
- 解析 35-65 个 CSV（30/76 KMT seeds × 2 tab + 5 organic）
- 跨源合并去重（同关键词出现多次只算 1 次）
- 进 L2 Step 5 4 级筛选漏斗
- 输出 `02-expanded-keywords.md` 主库 v0 300-500 词

---

## 6 · 路径 B · 精华 30 词清单（推荐）

### Step 4 ICP top 18（每 ICP 1 词，按 score / 产品对接强度选）

| # | 关键词 | ICP | 备注 |
|---|---|---|---|
| 1 | AI agent for code review | ai-builder | 高 score 1038/122c · 核心 dev 词 |
| 2 | how to get amazon reviews without vine | amazon-seller | Vine 痛点具体 |
| 3 | cold email metrics that matter | b2b-sdr | 73/45c · cold email 主线 |
| 4 | AI agent for PR | brand-pr | PR + 产品语义 |
| 5 | best business coaching program | coach | 推荐求解 |
| 6 | consultant powerpoint design tips | consultant | 高 score 101/51c |
| 7 | content marketing strategy that works 2026 | content-mkt-mgr | 趋势 + 策略 |
| 8 | how to create and sell online course | course-creator | Quora 强 |
| 9 | how to start data analysis project from scratch | data-analyst | 入门求解 |
| 10 | local SEO cost for small business | fallback-generic | 高 score 149/263c |
| 11 | how to handle fee-sensitive prospects | financial-advisor | advisor 业务 |
| 12 | how to write freelance design proposals | freelance-designer | 唯一 freelance 主线 |
| 13 | why ChatGPT cites pages | growth-marketer | 新兴红利 100/49c |
| 14 | why visitors don't sign up SaaS | indie-saas-founder | 转化主题 |
| 15 | React Native cross platform 2026 comparison | mobile-dev | 主流技术对比 |
| 16 | where to advertise newsletter for subscribers | newsletter-writer | 业务策略 |
| 17 | best landing page builder for PPC agencies | paid-ads | 工具求解 17/43c |
| 18 | AI candidate sourcing tool | recruiter | 工具问 18/109c |

### Step 5 产品语义 top 5（按 hits 排，覆盖未填 ICP）

| # | 关键词 | hits | ICP |
|---|---|---|---|
| 19 | AI proposal generator | 10 | freelance-designer |
| 20 | AI ad creative generator | 10 | artisan-dtc |
| 21 | AI app builder | 10 | mobile-dev |
| 22 | AI newsletter writer | 10 | newsletter-writer |
| 23 | Marketing & Growth AI agents | 4 | growth-marketer |

### Step 6 EXPLORATORY 全 7（新兴红利不能砍）

| # | 关键词 | 双源 |
|---|---|---|
| 24 | Generative Engine Optimization | aleyda + anthropic + SEL (3) |
| 25 | Model Context Protocol | anthropic + github (2) |
| 26 | Claude Code workflow | anthropic + github (2) |
| 27 | Claude agent skills | anthropic + SEL (2) |
| 28 | llms.txt SEO | aleyda + reddit-r-SEO (2) |
| 29 | Answer Engine Optimization | aleyda + SEL (2) |
| 30 | Google AI Overview optimization | aleyda + SEL (2) |

**总 30 词。**

---

## 7 · 完整 76 词清单（路径 A 用）

完整列表已落 `/tmp/pool-a-76-keywords.txt`，直接 cat 看。
