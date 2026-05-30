# Type 5 · Competitor Comparison 骨架

> **Ahrefs 参考**：Notion vs OneNote / Dropbox Sign vs DocuSign

---

## 适用场景

- **2 个产品/服务/概念被买家比较**
- 主词通常含 "vs" / "or" / "alternative to"
- yolox 适配：L6-08 AEO vs GEO / 未来 "yolox vs Lindy" / "Aria vs Apollo" 类

❌ **不适用**：多个工具评测（用 List）/ 概念解释（用 Definition）

---

## 字数 + 结构指标

| 指标 | 数值 |
|---|---|
| **字数** | 2000-3000 |
| **H2 数** | 5-8 |
| **Intro 字数** | 180-250 |
| **段落长度** | 50-150 字 |
| **视觉密度** | 每 400-500 字 ≥1 视觉，**必含 ≥1 对比表** |
| **FAQ section** | 可选 |
| **CTA 处** | 2+ |

---

## Title 公式

| 公式 | 示例 |
|---|---|
| **"[A] vs [B]: Which Is Better?"** | "AEO vs GEO: Which Should You Optimize For?" |
| **"[A] vs [B] (XXXX): Honest Comparison"** | "Notion vs OneNote (2026): Which Should You Use?" |
| **"[A] vs [B]: [Differentiator]"** | "Aria vs Apollo: Researched Proposals vs Templated Ones" |

---

## Intro 公式（180-250 字）

**中立介绍双方 + 暗示自家偏好**

```markdown
**段 1（介绍双方，80-100 字）**：
两方各自是什么、定位差异在哪。
不带偏见地概括（即使后面会偏向自家）。

**段 2（读者痛点，60-80 字）**：
为什么读者会纠结 — 通常是因为两方都有道理但场景不同。

**段 3（本文承诺 + 暗示，40-70 字）**：
"本文给你 N 个维度对比 + 1 个决策树"。
（可暗示倾向，但不卖关子）
```

**示例（L6-08 AEO vs GEO 改编）**：
> AEO (Answer Engine Optimization) and GEO (Generative Engine Optimization)
> are both about getting content cited by AI search. AEO focuses on answer
> engines like Google AI Overview / Bing Copilot; GEO is broader, covering
> all generative AI surfaces including ChatGPT, Perplexity, and Claude.
>
> If you're spinning up an AI search strategy in 2026, picking the wrong one
> means wasted 6-month bets — and both terms are often used interchangeably
> in vendor pitches.
>
> Below: 5-dimension comparison + a decision tree to pick the right one for
> your 2026 content roadmap.

---

## H2 主体骨架

### 必含 H2 顺序

```markdown
## At a glance（对比表 — 第 1 屏即看完整对比）
## [A] explained briefly
## [B] explained briefly
## [A] vs [B]: [Dimension 1, eg. Coverage]
## [A] vs [B]: [Dimension 2, eg. Tooling]
## [A] vs [B]: [Dimension 3, eg. Cost]
## When [A] wins / When [B] wins (场景化)
## Final verdict (含 yolox 嵌入)
```

### "At a glance" 对比表（第 1 屏必含）

```markdown
## At a glance

| Dimension | [A] | [B] |
|---|---|---|
| Best for | ___ | ___ |
| Cost | ___ | ___ |
| Learning curve | ___ | ___ |
| Coverage | ___ | ___ |
| Time to ROI | ___ | ___ |
| Limitations | ___ | ___ |

**TL;DR**: Choose **[A]** if [scenario]. Choose **[B]** if [scenario].
```

🔑 这个表是 Comparison type 的核心 — LLM 100% 会从这个表抓引用。

---

## 维度对比 H2 内部结构

```markdown
## [A] vs [B]: [Dimension]

**段 1（开场，50-80 字）**：
这个维度上两方差异在哪 — 1 句自包含。

**段 2（A 怎么样，80-120 字）**：
具体 — 含 evidence（截图 / 价格 / spec）。

**段 3（B 怎么样，80-120 字）**：
具体 — 含 evidence。

**段 4（差异总结，50-80 字）**：
这一维度上的 winner / takeaway。

[视觉：截图 or 表 or 价格图]
```

---

## "When A wins / When B wins" 场景表

```markdown
## When AEO wins

- ✅ 场景 1: ___
- ✅ 场景 2: ___
- ✅ 场景 3: ___

## When GEO wins

- ✅ 场景 1: ___
- ✅ 场景 2: ___
- ✅ 场景 3: ___
```

🔑 这一节是"中立平衡感"的核心 — 没有它，整篇会显得偏袒，AEO 引用率下降。

---

## Final verdict + CTA

```markdown
## Final verdict

[100-150 字]：
- 重申两方各自适用场景
- 给一个 "if you're forced to pick one" 的明确建议
- yolox 嵌入：how yolox handles both

**Try [A] free** [CTA 链] or **Try [B] free** [CTA 链]

Or [skip the choice — yolox handles both with one agent stack][yolox CTA].
```

---

## yolox 嵌入示范

**在 "Final verdict" 内自然嵌入**：

```markdown
## Final verdict

If you're an SMB content team in 2026:
- **Pick AEO** if your audience is on Google (still 80%+ of search volume).
- **Pick GEO** if you're targeting tech-savvy buyers researching on ChatGPT/Perplexity.

The reality: most teams need both. Manually managing both takes ~10h/week
across schema audit + chunk rewriting + citation tracking.

**yolox** runs both as a unified AEO/GEO team — Sophie + Brooks + Stella +
Isaiah cover schema, audit, chunks, and citation tracking. We use this stack
for yolox.ai itself.

→ [See the AEO/GEO agent team](https://yolox.ai/agents-store?category=aeo)
```

**注意**：
- ✅ 不在 dimension 对比中带 yolox（保持中立）
- ✅ 只在 verdict 段嵌入（读者已被说服中立后）
- ✅ "skip the choice" 的 framing — 不站队，给第三选择

---

## SEO + AEO 嵌入要点

| 项 | 在 Comparison 怎么落 |
|---|---|
| 主词 | title（vs 词）/ H1 / 首段 / URL / At-a-glance 表 |
| 副词 | 每个 dimension H2 |
| chunk 自包含 | 每个 dimension H2 开头 1 句差异总结 |
| 对比表（视觉关键）| **第 1 屏必含 ≥1 对比表** |
| citation 钩子 | At-a-glance 表 + dimension 数据 |
| 内链 | A / B 各 1-2 个 silo 内详细文章 |

🔑 **Comparison type 是 AEO 第二易引（仅次 Definition）** — LLM 在 "X vs Y" query 上几乎必引对比表。

---

## 适合的 yolox L6 大纲

| 大纲 | 备注 |
|---|---|
| **L6-08** AEO vs GEO | 主要 — Definition + Comparison 混合 |
| 未来：yolox vs Lindy / Aria vs Apollo / AEO vs traditional SEO | 都用此 type |
