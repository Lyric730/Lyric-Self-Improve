# Type 1 · List Post 骨架

> **Ahrefs 真实参考**：[23 Beginner Blogging Tips](https://ahrefs.com/blog/blogging-tips/)（实测 3500-4000 字 / 23 个 H2）

---

## 适用场景

- **非时间顺序信息**：任何项可重新排列仍有意义
- 工具评测 / tips 集合 / 方法清单 / idea 池
- yolox 适配：L6-13 newsletter writer / L6-09 AEO tools / L6-14 marketing agents / L6-19 amazon vine 等

❌ **不适用**：流程教学（用 Step-by-Step）/ 概念解释（用 Definition）/ 产品对比（用 Comparison）

---

## 字数 + 结构指标

| 指标 | 数值 |
|---|---|
| **字数** | 3500-4000 |
| **H2 数** | 15-25 |
| **H3 使用** | 可选，列表项内细分用 |
| **Intro 字数** | 150-180 |
| **平均 H2 内段落数** | 2-4 段 |
| **段落长度** | 50-150 字 |
| **视觉密度** | 每 H2 ≥1 视觉（截图 / 框架图 / 工具图） |
| **FAQ section** | ❌ 不需要（H2 已覆盖问题） |
| **CTA 处** | 3+：intro 末 / 结尾 / 工具推荐处 |

---

## Title 公式

| 公式 | 示例 |
|---|---|
| **"XX Ways to [Outcome]"** | "23 Ways to Get Better at Blogging Fast" |
| **"XX [Topic] Tips"** | "12 Cold Email Tips That Get Replies" |
| **"XX Best [Tools] for [Use Case]"** | "9 AI Newsletter Writers That Don't Sound Like AI" |

**钩子词**：数字（奇数 ≥ 偶数）+ 时间 / 速度 / 收益（"Fast" / "2026" / "That Actually Work"）

---

## Intro 公式（150-180 字，3 段）

```markdown
**段 1（背景，50-60 字）**：
设定读者的现状 — "你想要 X"。

**段 2（承诺，50-60 字）**：
告诉读者本文给什么 — "这是 N 个 proven 的 X tips"。
（可暗示来源权威：基于我们自己实测 / N 年经验 / N 篇研究）

**段 3（行动 + 目录，30-60 字）**：
鼓励行动 — "Try these tips" + 目录跳转（如有）。
```

**Ahrefs 原例**（L6-13 改编）：
> Want to write a newsletter people actually open? (背景)
> Here are 12 AI newsletter writers we've tested over 3 months, ranked by tone, speed, and zero-AI-tells. (承诺)
> Skim the list or jump straight to our top pick. (行动)

---

## H2 主体骨架

### H2 标题写法

**benefit-focused，不只是名词**：
- ❌ "Notion AI"
- ✅ "Notion AI — best for in-doc drafting if you live in Notion already"

### 每个 H2 内部结构（2-4 段）

```markdown
## [N]. [工具/tip 名] — [benefit 一句话]

**段 1（50-100 字）**：核心定义 / 是什么。
**段 2（80-150 字）**：怎么用 / 关键细节 / evidence。
（可选）**段 3（80-120 字）**：实例 / 截图 / quote。
（可选）**段 4（50 字）**：链接 / "try it free at..."。

[视觉：截图 or 框架图 or 数据图]
```

### 每个 H2 必含

- [ ] benefit-focused H2 标题（不只是名词）
- [ ] 至少 1 个具体细节（不是泛泛而谈）
- [ ] 1 个视觉元素（截图 / 图 / 列表）
- [ ] 在前 1/3 列表项嵌入 1-2 个 evidence（"X% of users..." / Brian Dean quote）

---

## Evidence 嵌入策略

| 位置 | 类型 | 例 |
|---|---|---|
| Intro | 行业 stat | "53.3% of all website traffic comes from organic search" |
| 前 1/3 列表项 | quote | "Dom Wells says ..." |
| 中段 | case | "X 公司用 Y 工具 N 周达到 Z" |
| 末段 | 数据图 / 截图 | 工具实际 UI |

---

## 结尾 + CTA

```markdown
## Final thoughts（或 Wrapping up / Now over to you）

[50-100 字总结]：
- 不要复述所有 H2
- 给一个 "choose 3-5 of these to start" 类的具体行动

**Try these blogging tips and let me know which one worked.** [CTA 行动句]
```

**CTA 3 处布点**：
1. **Intro 末**：软 — "Try these tips" / "Skim the list"
2. **工具推荐 H2 内**：product mention — "We use yolox Aria for this" + 链
3. **结尾**：硬 — 行动召唤 + 主 CTA（注册 / 试用 / 注册邮件）

---

## yolox 嵌入示范

```markdown
## 7. Aria — best for cold proposal drafting if you sell services

For service businesses (consulting / freelance / agency), the bottleneck is usually
not "writing" but "researching the client before writing". Aria pulls public data
(LinkedIn, company site, recent news) before generating, so the proposal feels
researched, not templated.

We use Aria for our own client proposals — average draft time dropped from 90min
to 18min.

[Aria 截图]

→ [Try Aria for free at yolox.ai/agents-store/aria](https://yolox.ai/agents-store/aria)
```

**注意**：
- ✅ 嵌入到正常列表项位置（不是单独"宣传段"）
- ✅ 含 yolox 自己的 case（"我们自己用，省了 80%"）
- ✅ benefit-focused（写"省时间"不是"yolox 最好"）

---

## SEO + AEO 嵌入要点

| 项 | 在 List Post 怎么落 |
|---|---|
| 主词 | title 数字开头 + 主词；首段第 1 句；至少 3 个 H2 含同义词 |
| 副词 | 散布在多个 H2 中 |
| 视觉 | 每 H2 1 个截图 / 图（已自然满足 §4 密度） |
| chunk 自包含 | 每个 H2 段开头 1 句自定义（"X is..."），不依赖上文 |
| citation 钩子 | 前 1/3 列表项嵌 1-2 个 stat + 末段嵌 1 个 quote |
| FAQ | 不强加；通过 H2 标题覆盖常见问题 |

---

## 适合的 yolox L6 大纲

| 大纲 | 备注 |
|---|---|
| **L6-09** AEO tools | 9-12 个工具评测 |
| **L6-13** AI newsletter writer | 10-12 个工具评测 |
| **L6-14** marketing agents | 8-10 个 agent 评测 |
| **L6-15** AI tools for recruiters | 8-10 个工具 |
| **L6-19** Amazon vine reviewer | tip list 风格 |

→ 写之前再回头看一下 L6 大纲，确认是否符合 "项可重排" 标准。
