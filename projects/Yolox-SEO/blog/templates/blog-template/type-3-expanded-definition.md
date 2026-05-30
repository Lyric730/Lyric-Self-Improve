# Type 3 · Expanded Definition 骨架

> **Ahrefs 参考**：[What is HTTPS?](https://ahrefs.com/blog/what-is-https/) / [What are SERPs?](https://ahrefs.com/blog/serps/)

---

## 适用场景

- **读者要先理解概念才能用**
- 核心读者意图：搜 "what is X" / "X meaning" / "X definition"
- yolox 适配：L6-07 GEO / L6-08 AEO vs GEO 的定义部分 / 未来 "what is X agent" 类

❌ **不适用**：流程教学（用 Step-by-Step）/ 全面教育（用 Beginner's Guide）/ tip 集合（用 List）

---

## 字数 + 结构指标

| 指标 | 数值 |
|---|---|
| **字数** | 1500-2500 |
| **H2 数** | 4-6 |
| **Intro 字数** | 150-200 |
| **段落长度** | 50-150 字 |
| **视觉密度** | 每 400-500 字 ≥1 视觉 |
| **FAQ section** | 可选 |
| **CTA 处** | 2+ |

---

## Title 公式

| 公式 | 示例 |
|---|---|
| **"What is [X]?"** | "What is GEO?" |
| **"What is [X]? [Tagline]"** | "What is AEO? Everything You Need to Know in 2026" |
| **"[X] Explained"** | "GEO Explained: Generative Engine Optimization Beyond the Hype" |

---

## Intro 公式（150-200 字）

**定义优先 + featured snippet 加粗词**

```markdown
**段 1（30-50 字）**：
**核心定义 1 句话**（必须用 markdown **加粗**）。
这一句是 Google featured snippet 抢的目标。

**段 2（80-120 字）**：
扩展解释 — 为什么这个概念现在重要 / 行业现状。

**段 3（30-50 字）**：
本文给什么 — 列出几个 follow-up 问题（"In this guide, you'll learn..."）。
```

**示例（L6-07 GEO 改编）**：
> **GEO (Generative Engine Optimization) is the practice of optimizing content
> so it gets cited by AI search engines like ChatGPT, Perplexity, and Google's
> AI Overview.** (加粗 = featured snippet 候选句)
>
> Unlike traditional SEO (rank a page), GEO aims to get your content quoted inside
> AI-generated answers. With AI Overview now appearing on 40%+ of US searches
> (SparkToro 2025), GEO is no longer optional for content brands.
>
> In this guide, you'll learn what GEO is, how it differs from SEO/AEO, and the
> 5 levers that move citation rate. (内容地图)

---

## H2 主体骨架

### 必含 H2 顺序

```markdown
## What is [X]? (定义详细展开)
## Why does [X] matter? (重要性论证)
## How does [X] work? (机制 / 原理)
## [X] vs [related concept] (对比，区分概念)
## How to do [X] (实操简化版，深度交给 Beginner's Guide)
## Common myths about [X] (可选)
## FAQ (可选)
```

### 每个 H2 内部结构

```markdown
## [H2 title]

**段 1（开头 1 句，自包含答案，50-80 字）**：
直接回答 H2 的问题，不绕。

**段 2-3（细节展开，100-150 字/段）**：
- 用 H3 / 列表 / 表分层
- 至少 1 个例子

**段 4（视觉或表，可选）**：

[视觉]
```

---

## 关键钩子：Featured Snippet 写法

Google 的 featured snippet 抢的是"定义型"段落。Expanded Definition type 必做：

1. **每个 H2 第 1 句 = 自包含答案**（不超 50 字）
2. **核心定义句用 markdown 加粗**
3. **避免代词开头**（用 "GEO is..." 不是 "It is..."）

**示例**：
- ❌ "It works by analyzing your content..."
- ✅ "**GEO works by structuring content so AI can extract self-contained chunks.**"

---

## 结尾 + CTA

```markdown
## Wrapping up（or Now you know）

[50-100 字]：
- 重申 1 句话定义
- 给一个"下一步"链接（指向 Beginner's Guide 或 How-to）

**Ready to apply [X]?** → [Continue to: How to do X](link)
```

---

## yolox 嵌入示范

**在 "How to do X" 段内嵌入产品**：

```markdown
## How to do GEO (in 5 levers)

The 5 levers that move citation rate:

1. Chunk-level content structure
2. Citation hooks (data + quotes)
3. ...

For brands that don't have a content team, **yolox Sophie + Brooks** (our SEO
Doctor + Site Auditor) automate levers 1-3 in about 20 minutes per page.
We use them for yolox.ai itself — 4 pages went from 0 to 12 AI Overview
citations in 8 weeks.

→ [Try Sophie at yolox.ai/agents-store/sophie](https://yolox.ai/...)
```

---

## SEO + AEO 嵌入要点

| 项 | 在 Definition 怎么落 |
|---|---|
| 主词 | title / H1 / **加粗的核心定义句** / 首段 / URL |
| AEO 加粗钩子 | 核心定义 + 关键术语 markdown 加粗（LLM 优先抓） |
| chunk 自包含 | 每个 H2 第 1 句必自包含 |
| FAQ Schema | 如果加 FAQ section，frontmatter 加 `schema_type: FAQPage` |
| 内链 | silo 内的 Pillar 主文（Beginner's Guide）+ How-to + Comparison 类 |

🔑 **Expanded Definition 是 AEO 最易被引的 type** — 因为 LLM 在 "what is X" 类 query 上几乎必引定义页。

---

## 适合的 yolox L6 大纲

| 大纲 | 备注 |
|---|---|
| **L6-07** GEO | 部分 — Pillar 内 "What is GEO" 段 |
| **L6-08** AEO vs GEO | 主要 — Definition + Comparison 混合 |
| 未来：what is AI agent / what is agent team / what is AEO Suite | 都用此 type |
