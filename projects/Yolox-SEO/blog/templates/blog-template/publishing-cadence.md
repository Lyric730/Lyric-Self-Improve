# 发布节奏纪律

> **决定 25 篇 blog 用什么节奏发布**。
> **核心真相**：Google 看的是"首次发现日"，frontmatter 改不了。
> **配套**：`yolox-blog-template-v0.5.md` 主 SOP / `checklist-pre-publish.md` ship 前必读

---

## 0 · 一句话核心

> **frontmatter `date` 是给读者看的；Google 看的是 Googlebot 第一次 crawl 这个 URL 的真实时间戳**。无法作弊。

---

## 1 · 你能改的 vs Google 看的（对照）

| 你能改 ✅ | Google 实际看 ❌（不可作弊）|
|---|---|
| frontmatter `date: 2025-08-15`（显示给读者）| Googlebot 第一次 crawl 这个 URL 的时间戳（Google 内部数据库）|
| Schema `datePublished` / `dateModified` | sitemap.xml `<lastmod>`（每次 deploy 自动生成）|
| HTML 顶部"Published Aug 2025" | Server HTTP `Last-Modified` header（服务器返回的真实 build time）|
| markdown 里写"3 months ago" | Wayback Machine 快照（archive.org 第三方独立备份）|
| | 整站内链结构瞬间变化（anomaly detection）|

→ **5 重 detection 中你能控制 0 重**。"假装早写好" 骗读者不骗 Google。

---

## 2 · Google 5 重 detection 细节

### 2.A · Googlebot 首次抓取时间戳

你 deploy 新 URL → Googlebot 第一次访问 → Google 内部数据库写 "first seen: YYYY-MM-DD HH:mm:ss"。**永远改不了**。这是 Google 算法判断"freshness" / "stable rank"的根本。

### 2.B · sitemap.xml `<lastmod>` 字段

每次 build → `src/app/sitemap.ts` 自动生成新 entry。24 个 URL 同一天出现 → Google ping 通知 → **100% 检测到批量发布**。

### 2.C · HTTP `Last-Modified` Header

浏览器 / 爬虫每次 access 服务器都拿到这个 header。**值 = 服务器实际 deploy 时间**，不是你 frontmatter 写的 date。

### 2.D · Wayback Machine（archive.org）

全自动定期备份的第三方服务。你 2026-05-13 才发 → archive.org 上**永远不会有 2025-08-15 的 snapshot**。竞争对手 / Google 都能查。

### 2.E · 站内链接结构 anomaly

正常 blog 每周 1-2 篇 / 月 4-8 篇。一夜之间 24 篇 + Pillar 瞬间收 5+ 内链 = unnatural pattern → 可能触发 manipulation flag。

---

## 3 · 一次性全发的 3 重风险

| # | 风险 | 严重度 |
|---|---|---|
| 1 | **质量风险**：模板没经实战验证就批量产 = 同错误复制 24 次 | 🔴 **最严重**（dogfood 哲学根本反对）|
| 2 | **Google "新站翻转" flag**：突然 24 篇 = 可能判定为 mass-produced / AI 内容农场 / SEO spam | 🟡 中（不一定触发，看域名年龄 + 内容质量）|
| 3 | **内链结构 unnatural**：Pillar 瞬间收 5+ 内链 = manipulation pattern | 🟡 中 |

🔑 **现代 Google 已能区分合法 silo strategy 和 link manipulation**，但保守起见仍推荐逐步发表。

---

## 4 · 4 种发布节奏对比

| 节奏 | 时间表 | Google 风险 | 建议 |
|---|---|---|---|
| 一天 24 篇 | 1 天 | 🔴 高（mass-produced flag）| ❌ **不允许** |
| 每天 2 篇 | 2 周 | 🟡 中 | 🟡 工业化但激进 |
| **每周 2 篇** | **3 个月** | 🟢 低 | ⭐ **推荐（最佳 trade-off）** |
| 每周 1 篇 | 6 个月 | 🟢 最低 | 保守 / ship 速度过慢 |

### 为什么"每周 2 篇 / 3 个月"是 sweet spot

- ✅ ship 速度合理（3 个月 = 1 个 quarter，能跟季度 OKR 对齐）
- ✅ Google 看到"自然生长"的内容站，trust 信号持续上升
- ✅ 每周 2 篇 = 真实数据反馈快，能 dogfood 模板迭代到 v1
- ✅ 不阻塞 yolox 产品其他工作
- ✅ Pillar 主文逐步收到 cluster 内链 = 排名稳步上升（vs 一次性发后 Pillar 排名 stuck）

---

## 5 · 25 篇发布计划表（推荐）

> **总体节奏**：12 周 / 每周 2 篇 / 共 24 + 1 = 25 篇
>
> **顺序原则**：低 KD 优先（快速首页占位） + Pillar 主文最后发（接收 cluster 内链）

### 阶段 1（Week 1-3）：低 KD cluster 占位

KD ≤25 的 6 篇优先（Ben 锁定 + 之前的 cooling-off review 目标）：

| Week | 篇 | 主词 | KD | type |
|---|---|---|---|---|
| 1 | L6-01 ✅ | answer engine optimization services | 19 | type-7 buyer's guide |
| 1 | L6-04 | cold email deliverability | 17 | type-2 step-by-step |
| 2 | L6-02 | podcast guest release form | 8 | type-3 definition |
| 2 | L6-05 | ai agents for project management | 25 | type-1 list |
| 3 | L6-08 | aeo vs geo | (KD low) | type-5 comparison |
| 3 | L6-06 | ai tools for recruiting | 25 | type-1 list |

### 阶段 2（Week 4-7）：剩余 cluster

每周 2 篇，14 篇分 7 周。按 silo 平衡分布（不集中在同一 silo）：

| Week | AEO silo | α silo | β silo | γ silo |
|---|---|---|---|---|
| 4 | L6-07 GEO | L6-03 proposal | | |
| 5 | L6-09 tools | | L6-15 recruiters | |
| 6 | L6-10 AI Overview | L6-11 ad creative | | |
| 7 | | L6-12 story writer | L6-16 cold calling | |
| 8 | | L6-13 newsletter | L6-17 CRM | |
| 9 | | L6-14 marketing agents | | L6-18 podcast name |
| 10 | | | | L6-19 amazon vine, L6-20 ecommerce |

### 阶段 3（Week 11-12）：Pillar 主文 + 收尾

| Week | 篇 |
|---|---|
| 11 | L6-00-pillar-aeo + L6-00-pillar-alpha |
| 12 | L6-00-pillar-beta + L6-00-pillar-gamma + L6-21 restaurant |

🔑 **Pillar 主文为什么最后**：等 5+ cluster 都发了 + 全链回 Pillar → Pillar 收到 ≥5 内链 → 上线即"自然高权重" → 排名 ramp 更快。

---

## 6 · 实际操作 SOP（每发 1 篇要做的）

```
Day 1 (写完 markdown)
  ↓
Day 2 (24h cooling-off)
  ↓
Day 3 (cooling-off 后 review + 跑 checklist 18 必须项)
  ↓
Day 3 (ship 到 GitHub PR)
  ↓ 等评审 / 合并
Day 5-7 deploy 到 production
  ↓
Day 7 验证：
  ├─ Google Rich Results Test 验 schema
  ├─ Search Console 提交 URL 加速 indexing
  ├─ GA4 verify event 触发
  └─ archive.org 主动 snapshot（curl https://web.archive.org/save/{URL}）
  ↓
Day 14-21（2-3 周后）
  └─ 检查首次 impression（Search Console）
  ↓
Day 30+
  └─ 评估首次排名 / AEO 引用情况 → 决定是否需要 update
```

每周 2 篇 = 2 个并行 pipeline，错开 3 天，互不阻塞。

---

## 7 · 紧急情况：加速 / 减速

### 7.A · 需要加速（如：竞争对手抢词 / 紧急行业事件）

可以从"每周 2 篇" → "每周 3-4 篇" **短期冲刺 2 周**。但：
- 超 2 周不允许（恢复 manipulation flag 风险）
- 必须**有真实事件触发**（不是为了加速而加速）
- 同 silo 内不允许同一周发 ≥3 篇（内链 anomaly）

### 7.B · 需要减速（如：质量问题 / 团队事故）

- 减到每周 1 篇 OK
- 减到每月 1 篇 = 接近"放弃 blog 策略"，慎用
- **不允许停 1 周以上不发**（Google 看 freshness，长期不发 = 整站信任分降）

---

## 8 · 给 leader / Ben 对接的"为什么不一次性发"

3 句话：

1. **Google "首次发现日"不可作弊** — frontmatter 改日期只骗读者，Googlebot 内部记录真实 crawl 时间
2. **一次性发 24 篇 = AI 内容农场 flag** — 现代 Google 区分得出合法 silo strategy 和 link manipulation，但保守仍推荐逐步
3. **逐步发让 Pillar 内链自然增长** — Pillar 最后发，前面 cluster 都内链回它，上线即高权重

---

## 9 · 与其他文档的接口

| 本文档涉及 | 对应位置 |
|---|---|
| Pillar / cluster URL 架构 | `routing-matrix-v0.5.md §1` |
| 内链最少数（silo ≥3 等）| `brief-template.md` 必填 6 |
| 每篇 checklist | `checklist-pre-publish.md` 18 必须 |
| 前端 sitemap 实施 | `0-share/frontend-spec.md §2.F.3` |
| 24 主词 + L6 大纲 | `keyword-research/round-2-2026-04-28/blog-outlines/` |
| Round-3 整体 plan | `00-sop-retrospective.md §4 简化版` |

---

## 10 · 版本

- **v0.5**（当前 2026-05-13）：3 个月 / 12 周 / 25 篇推荐表
- **v0.6**（触发：第 6 篇 ship 后）：根据真实排名数据校准节奏
- **v1**（触发：12 周满）：基于完整 dataset 的发布节奏 SOP

🔑 **核心**：不要看一时进度，看 12 周后整站状态。"慢即是快"在 SEO 里成立——Google 信任分是积分制，逐步累积 > 一次性轰炸。
