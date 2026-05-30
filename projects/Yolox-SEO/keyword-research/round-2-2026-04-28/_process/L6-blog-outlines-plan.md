# Layer 6 · Day 6 博客大纲方案

**日期**：2026-04-29
**讨论方**：小刀老师 + Agent B
**状态**：草案 v1（讨论中）
**前置依赖**：L5 v1 已交付（06-pillar-cluster-map.md · 3 Pillar × 5 Cluster + 9 候选博客）

---

## 0 · 你的决策（输入）

| # | 决策 | 选择 |
|---|---|---|
| L6.1 | 9 砍 6 标准 | **a** · 严格 4 纪律全过 |
| L6.2 | 大纲深度 | **b** · 1.5 页（含 meta + slug + reading time）|
| L6.3 | FAQ 数量 | **b** · 5 FAQ |
| L6.4 | Schema 标注 | **b** · FAQPage + Article schema |

---

## 1 · L6 边界（不越界）

按 L0 §7：

| 越界 | 谁做 |
|---|---|
| ❌ Pillar/Cluster 决策 | L5 已做 |
| ❌ 精确 KD（Ahrefs trial 第 2 次）| L7 做 |
| ❌ 写博客内容 | 下周 |
| ❌ 落库飞书 | L7 做 |

**L6 只做**：
1. 9 候选博客严格 4 纪律过滤 → 砍 3 留 6
2. 6 篇 1.5 页大纲撰写
3. Schema 标注（FAQPage + Article）
4. 整理 → `08-blog-outlines.md`

---

## 2 · 当天目标

| 维度 | 目标 |
|---|---|
| 候选博客 | 9（来自 L5 §6）|
| 过滤后保留 | 6 篇（4 纪律全过 + 综合分排序）|
| 大纲深度 | 1.5 页（H1+TL;DR+H2-H3+meta+slug+reading time+5 FAQ+CTA+Schema）|
| Pillar 平衡 | 6 篇覆盖 3 Pillar 各 ≥ 1（Cluster 1.x / 2.x / 3.x 至少各 1）|
| 5-3-1 对接 | 6 篇含 L5 §3 首发 5 Cluster 中 ≥ 4 个 |
| 工期 | ~4 hr 净执行 |

---

## 3 · 当天动作（4 步）

### Step 1 · 9 候选过 4 纪律（30 min · 决策 L6.1a 严格）

#### 1.1 4 选题纪律（继承 archive/round-1/05 §6）

每候选过 4 问 yes/no：

| # | 问题 | 不通过 |
|---|---|---|
| 1 | 原帖是"提问"还是"公告/show-off"？ | 后者砍 |
| 2 | 原帖 + Cluster 邻近证据累计够吗？ | 孤例砍 |
| 3 | 你的产品有现成能力答这题吗？ | 答不了不写 |
| 4 | 关键词是用户会 Google 的吗？ | 内部人名 / 黑话不行 |

#### 1.2 严格过滤（决策 L6.1a）
- 4 yes 全过 → 入选
- 任一 no → 砍出（进 watchlist）

#### 1.3 边界
- 全过候选 < 6 → 放宽某项（比如纪律 #2 评估"邻近证据累计"宽松些）
- 全过候选 > 6 → 按 L5 §3 混合分（yoy 红利 ×1.5 + Tier 0 ×1.0 + Tier 1 ×0.5）排前 6

#### 1.4 Pillar 平衡
- 6 篇必须覆盖 3 Pillar 各 ≥ 1
- 若集中在某 Pillar > 3 篇 → 调整：从其他 Pillar 候选中提拔

#### 1.5 输出
- 6 选定博客 + 各自所属 Pillar/Cluster + 4 纪律评分
- 3 砍掉 → watchlist

### Step 2 · 6 篇大纲撰写（3 hr · 每篇 30 min · 决策 L6.2b 1.5 页）

#### 2.1 大纲模板（每篇必含）

```markdown
# [博客 N]: {H1 标题}

## 元信息
- **slug**: /blog/{slug-kebab-case}
- **meta title**: {≤60 字符}
- **meta description**: {≤155 字符 · 含核心词 + CTA 暗示}
- **reading time**: {分钟数 · 1500 字 ≈ 7 min}
- **Pillar**: P{N} - {Pillar 主词}
- **Cluster**: C{N.M} - {Cluster 主题}
- **目标关键词**: {Cluster 头词}
- **辅助关键词**: {2-3 长尾词 · 来自 Cluster 长尾池}
- **目标 ICP**: {1-2 个 ICP 名}
- **对接产品**: {agent / skill / team 名}
- **5-3-1 顺序**: {首发 第 N 周 / 后续 等}

## TL;DR（3-5 行 · AEO-friendly）
{3-5 行精简回答，每行一个要点。AEO 优化——LLM 抓取友好。}

## H2-H3 结构

### H2-1: {子主题 1}
- H3-1.1: {要点}
- H3-1.2: {要点}

### H2-2: {子主题 2}
- H3-2.1
- H3-2.2

### H2-3: {子主题 3}
- H3-3.1

### H2-4: {子主题 4}
- H3-4.1

### H2-5: {子主题 5 · 通常是"How YOLOX helps" 或对接产品段落}

## Reddit/Quora 证据（来自 L1 Step 4）
- {URL 1}: {标题截断 60 字符 · score/评论数}
- {URL 2}: ...
- 至少 2 个原帖（坑 6.4 规避：不孤例）

## 5 FAQ（决策 L6.3b · FAQPage schema 用）
1. **Q**: {问题 · 来自 PAA 或 Reddit 真问}
   **A**: {答案 50-80 字 · AEO-friendly}
2. ...
（5 条）

## CTA
- 位置：文末 + 中段（H2-3 后软插入）
- 文案：{定制 CTA · 指向 agent / team 落地页}
- 链接：/agents-store/{agent-id} 或 /teams-store/{team-id}

## 内链网（来自 L5 §5）
- 主链 → Pillar：{Pillar URL}
- 同 Pillar 邻近：{Cluster A URL} · {Cluster B URL}
- 跨 Pillar（可选）：{Cluster X URL}

## Schema（决策 L6.4b）
- **FAQPage**: 5 个 Q&A
- **Article**: headline / datePublished / author / image
- 落地实施在 L8 Day 8（不在 L6 范围）
```

#### 2.2 撰写顺序
按 L5 §3 5-3-1 首发 5 Cluster 排序——首发的 Cluster 优先撰写大纲（避免 Day 7 落库时缺）。

#### 2.3 6 篇分布预期（基于 L5 推断）
- 2 篇 from Pillar 1（含 1 yoy 红利）
- 2 篇 from Pillar 2
- 2 篇 from Pillar 3

### Step 3 · Schema 标注 + 校验（30 min · 决策 L6.4b）

#### 3.1 FAQPage schema JSON-LD 模板

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{Q1}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{A1}"
      }
    }
    // × 5
  ]
}
```

#### 3.2 Article schema JSON-LD 模板

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{H1}",
  "description": "{meta description}",
  "datePublished": "{ISO 日期}",
  "dateModified": "{ISO 日期}",
  "author": {
    "@type": "Organization",
    "name": "YOLOX"
  },
  "image": "{封面图 URL}"
}
```

#### 3.3 校验
- Google Rich Results Test (https://search.google.com/test/rich-results) 验证 schema（在 L8 实施时再做）
- L6 阶段只输出 schema 模板和字段值，不上线

### Step 4 · 整理 + 落盘 08-blog-outlines.md（30 min）

#### 4.1 文件结构
```markdown
# 08 · 下周 6 篇博客大纲

## 0 · 概览
- 6 篇分布: P1 × 2 / P2 × 2 / P3 × 2
- 5-3-1 顺序: ...
- 总字数预估: ~9000 字（6 篇 × 1500 字 avg）

## 1 · 博客 1: {H1}
（完整大纲）

## 2 · 博客 2: {H1}
...

## 6 · 博客 6: {H1}

## 7 · 砍掉 3 候选 + 理由
（4 纪律未过的）

## 8 · 内链网总览
（6 篇之间 + 跨 Pillar 链接图）

## 9 · L7 衔接
- L7 飞书 CSV 字段需含 Cluster + 6 篇博客 ID
- L7 Ahrefs 精排重点：6 篇博客的目标词 + 长尾词
```

#### 4.2 末尾汇总
- 6 篇 × 1.5 页 = 9 页大纲
- Pillar 平衡: 各 2 篇
- 4 纪律全过率: 100%
- yoy 红利覆盖: 1-2 篇
- 5-3-1 首发 4 个 + 后续 2 个

---

## 4 · 当天交付物

| 文件 | 内容 |
|---|---|
| `08-blog-outlines.md` | 6 篇 1.5 页大纲 + Schema 模板 + 内链网 |

---

## 5 · 当天规避动作（11 坑映射）

| 坑 | 规避 | 在哪 Step |
|---|---|---|
| **6.3 Reddit show-off 陷阱** | 4 纪律 #1 严格过 | Step 1.1 |
| **6.4 Reddit 1/1 孤例** | 每篇至少 2 原帖证据；4 纪律 #2 严格过 | Step 2.1 |
| 6.5 内部 Agent 人名 | 4 纪律 #4 严格过 | Step 1.1 |
| 6.11 Handoff stale | L6 启动前 `git status` | 启动前 |
| 新 · Pillar 不平衡 | Step 1.4 强制每 Pillar ≥ 1 | Step 1.4 |
| 新 · meta description 超长 | Step 2.1 校验 ≤155 字符 | Step 2.1 |
| 新 · 5 FAQ 重复 | Step 2.1 跨 FAQ 语义去重 | Step 2.1 |

---

## 6 · 当天退出条件

| # | 触发 | 动作 |
|---|---|---|
| E1 | 4 纪律全过候选 < 6 | 放宽纪律 #2（邻近证据宽松）/ 仍 <6 → 收缩到 5 篇 |
| E2 | 任一 Pillar 候选 < 1 | 提拔该 Pillar 的次优 Cluster 进入 |
| E3 | 某博客找不到 ≥ 2 原帖证据 | 该篇降级到 watchlist，从其他候选提拔 |
| E4 | 5 FAQ 凑不齐 | 用 PAA L2/L3 数据补；仍不够 → 降到 3 FAQ |
| E5 | 大纲撰写超时（> 4 hr）| 简化到 1 页（去掉 reading time + slug）|

---

**对齐后下一步**：执行 Step 1（9 砍 6）→ Step 2（6 篇大纲）→ Step 3（Schema）→ Step 4（落盘）→ 起草 L7 落库 + Ahrefs 精排方案
