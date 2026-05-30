# Type 2 · Step-by-Step Guide 骨架

> **Ahrefs 参考**：[How to Write a Blog Post in 9 Steps](https://ahrefs.com/blog/how-to-write-a-blog-post/) / "How to Get on First Page of Google"

---

## 适用场景

- **教人完成某事，需按特定顺序执行**
- 关键判断：调换 step 顺序后失败 = 适用 Step-by-Step
- yolox 适配：L6-04 cold email deliverability / L6-10 AI Overview opt / L6-07 GEO 实操部分

❌ **不适用**：tip 集合（用 List）/ 概念解释（用 Definition）

---

## 字数 + 结构指标

| 指标 | 数值 |
|---|---|
| **字数** | 2000-3000 |
| **H2 数** | 5-10（= step 数 + intro/conclusion） |
| **Intro 字数** | 200-250 |
| **平均 H2 内段落数** | 3-6 |
| **段落长度** | 50-150 字 |
| **视觉密度** | 每 step ≥1 截图 / 流程图 |
| **FAQ section** | 可选（常见错误 H2 可替代） |
| **CTA 处** | 3+ |

---

## Title 公式

| 公式 | 示例 |
|---|---|
| **"How to [Outcome]"** | "How to Pass Cold Email Deliverability Checks" |
| **"How to [Outcome] (in XX Steps)"** | "How to Optimize for AI Overview in 7 Steps" |
| **"How to [Outcome] (Without [Pain])"** | "How to Send Cold Email Without Hitting Spam" |

---

## Intro 公式：PSP（Problem → Solution → Proof）

```markdown
**P · Problem（80-100 字）**：
读者的具体痛点 — 不是泛泛"很难"，而是"75% 的 cold email 进 spam"具体数。
共情读者的失败/痛苦。

**S · Solution（60-80 字）**：
本文给的解法 — "这是一个 7 步的 deliverability checklist"。
告诉读者跟着做能拿到什么结果。

**P · Proof（40-60 字）**：
凭什么相信本文 — 数据 / case / 经验。
"基于我们对 X 个 cold email campaign 的复盘 / 行业老兵 Y 的方法"。
```

**示例（L6-04 改编）**：
> 75% of cold emails get filtered into spam. You spend hours writing them — nobody sees them. (Problem)
>
> This 7-step deliverability checklist takes 30 minutes to run before any campaign. It moves your inbox rate from <30% to 85%+ in our tests. (Solution)
>
> Below steps come from auditing 200+ cold email campaigns at yolox and 3 years of running outbound at scale. (Proof)

---

## H2 主体骨架（按 step 编号）

### H2 标题写法

**Present tense verbs + 编号**：
- ✅ "Step 1: Find your dream prospects"
- ✅ "Step 2: Choose your email tool"
- ❌ "Finding prospects"（不强 actionable）
- ❌ "Step 1: How to find prospects"（多余）

### 每个 step（H2）内部结构

```markdown
## Step N: [Present tense action]

**段 1（开场，60-80 字）**：
这一步要达到什么 — 1 句答案优先句。
"In this step, you'll [outcome]."

**段 2-3（怎么做，100-200 字）**：
具体步骤 — 子步骤可用编号或 H3。
带具体工具 / 截图 / 命令。

**段 4（warning / tip，50-100 字）**：
常见错误 / pro tip / 备选方案。

**段 5（结果验证，50 字）**：
怎么知道这一步做对了。

[视觉：截图 / 流程图 / 命令行]
```

### 每个 step 必含

- [ ] 答案优先开头句
- [ ] 至少 1 个具体工具 / 命令 / 例子
- [ ] 1 个视觉（截图 / 流程图）
- [ ] 1 个 "如何验证这步成功"

---

## 钩子段落

### 在 step 之前加 H2: "Before you start"（可选）

```markdown
## Before you start

You'll need:
- Tool / account 1: [link]
- Tool / account 2: [link]
- Estimated time: [N min]

Skip this if you already have [...].
```

### 在最后 step 后加 H2: "Common errors and troubleshooting"

```markdown
## Common errors and troubleshooting

**Error 1: [常见错误]**
- 原因：___
- 修法：___

**Error 2: [常见错误]**
- 原因：___
- 修法：___
```

---

## 结尾 + CTA

```markdown
## Quick recap

[80-120 字]：
- 列出 N 个 step 名（不是再讲细节）
- 一个"如果你只有 5 分钟，做这 1 件"

**Now go [action verb]** — [行动召唤] [CTA 链]
```

---

## yolox 嵌入示范

**自然嵌入到对应 step 内**：

```markdown
## Step 4: Personalize each email (the part everyone skips)

Manually researching every prospect is the bottleneck — that's why most people
skip personalization and tank deliverability.

[Daniel](https://yolox.ai/agents-store/daniel) (yolox's Email Closer agent) does
the research → draft loop in 90 seconds per prospect. We use it for our own
cold campaigns — reply rate jumped from 4% to 11% in 6 weeks.

If you'd rather DIY: open LinkedIn → check last 30 days of activity → pull 1
specific detail to reference.

[Daniel 截图]
```

**注意**：
- ✅ 嵌入到对应 step（personalization → Daniel）
- ✅ 给 DIY 备选（不强推 yolox）
- ✅ 含 yolox 自家 case

---

## SEO + AEO 嵌入要点

| 项 | 在 Step-by-Step 怎么落 |
|---|---|
| 主词 | title + 首段（PSP 的 Problem 段）+ Step 1 H2 |
| 副词 | 散布在 step H2 / Common errors |
| chunk 自包含 | 每个 step 开头 "In this step, you'll..." |
| citation 钩子 | PSP Proof 段 + Step 内 stat |
| 视觉 | 每 step 1 截图（自然满足） |
| FAQ | 可用 "Common errors" 替代 |
| HowTo Schema | frontmatter 加 `schema_type: HowTo` 让前端注入 JSON-LD |

🔑 **HowTo Schema 是 Step-by-Step type 的 SEO 杀器** — 让 step 在 SERP 中以列表形式出现，CTR 翻倍。

---

## 适合的 yolox L6 大纲

| 大纲 | 备注 |
|---|---|
| **L6-04** cold email deliverability | 7 step checklist |
| **L6-10** Google AI Overview optimization | 5-7 step 优化流程 |
| **L6-07** GEO（部分）| Pillar 主文中嵌 step section |

→ 写之前确认 outline 的 "is X step order necessary?" 问题。
