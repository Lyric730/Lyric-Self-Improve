# yolox blog 写作模板 v0.5 · 主 SOP

> **角色定位**：本文档 = blog 写作的"工艺标准"。
> 拿到 L6-XX 大纲 → 按本文 + 对应 type 骨架 → 写出可发布 markdown。
> **不要跳步骤** — 跳了等于回退到"凭感觉写"。

---

## 0 · 怎么用这份模板

| 项 | 内容 |
|---|---|
| **谁用** | 小刀老师 / AI agent / 未来外包写手 |
| **何时用** | 拿到 L6-XX 大纲后、开始 drafting 之前 |
| **输入** | 一份 L6-XX 大纲 + 主词数据（V/KD/Growth） + 知道这篇属于 7 type 中哪种 |
| **输出** | 1 份可发布 markdown + 通过 checklist-pre-publish 必须 15 项 |
| **预计工时** | brief 30min + drafting 4-6h + 24h 冷却 + 编辑 2h = 总 ~8h/篇 |
| **核心纪律** | drafting 写完必须**隔 24h** 才能编辑（Ahrefs editing magic） |

---

## 1 · 文章 brief（开写前必填，30min）

完整字段 + 示例见 [`brief-template.md`](./brief-template.md)。

**必填 6 项**（缺一不开始 drafting）：
1. **关键词三件套**：主词 / 5-8 副词 / 5-8 LSI
2. **ICP + 痛点**（1 段，从 outline 抄）
3. **文章 type**（7 种选 1）→ 决定用哪个 type 骨架
4. **角度声明**（1 句话，"我们和竞品 top 5 不一样的点在哪"）— DUD Depth 的核心
5. **引用素材池**：≥2 个 case + ≥3 个 2025-2026 数据 + ≥1 个 quote，**每条 source URL 必填**（找不到原文 → 写为 "industry anecdotal estimate"）
6. **Frontmatter & 内链清单**：frontmatter 字段齐（slug 含主词 / author / linkedin / toc / schema_type）+ 内链 ≥7（silo 内 ≥3 + product ≥1 + 外链权威 ≥3）。**URL 来源** = [`routing-matrix-v0.5.md`](./routing-matrix-v0.5.md)，不要现想

**可选 2 项**：
7. SERP top 5 截图（如果时间紧可跳，但 buyer's guide 类强烈建议做）
8. 关键词出现位置预规划（title / H2 选词）

🔑 **核心：素材池不收集 + 内链不预选，不允许开始 drafting**。这是把"言之有物 + 站内权重内循环"前置到结构里的唯一办法。

---

## 2 · 结构骨架（总论）

每篇文章 = **Intro + TL;DR/Answer-first（可选）+ H2 主体 + 结尾 + CTA**

| 元素 | 规则 |
|---|---|
| **Title** | **≤60 chars**（含 brand suffix 也算）+ 含主词 + 1 个 buyer-stage hook 词（cost / 2026 / DIY / vs / best 等）。超 60 移动端会截断 |
| **Intro** | 字数 + 公式按 type 不同（详见各 type-X.md） |
| **TL;DR / Answer-first** | Pillar / Buyer's / How-to / Definition 必含；List / Contrarian 可省 |
| **H2 主体** | 数量按 type 不同；每个 H2 必含 1 evidence + 1 actionable |
| **FAQ** | Pillar / Buyer's 必含；其他 type 可选 |
| **结尾** | 含金句或行动召唤 |
| **CTA** | ≥3 处：intro 末（软）+ 结尾（硬）+ product 嵌入处 |

---

## 3 · 7 种文章 type 骨架库

完整骨架在各 type-X.md。摘要：

| Type | 字数 | H2 数 | Intro 字数 | Intro 公式 | 适用 yolox 大纲 |
|---|---|---|---|---|---|
| [1 · List Post](./type-1-list-post.md) | 3500-4000 | 15-25 | 150-180 | 背景→承诺→行动 | L6-13 newsletter / L6-09 AEO tools / L6-14 marketing agents |
| [2 · Step-by-Step](./type-2-step-by-step.md) | 2000-3000 | 5-10 | 200-250 | **PSP**（Problem→Solution→Proof） | L6-04 cold email / L6-10 AI Overview opt |
| [3 · Expanded Definition](./type-3-expanded-definition.md) | 1500-2500 | 4-6 | 150-200 | 定义优先 + 加粗 featured snippet 词 | L6-07 GEO / L6-08 AEO vs GEO |
| [4 · Beginner's Guide](./type-4-beginners-guide.md) | 3800-4200 | 6-8（含 H3/H4） | 250-300 | 重点强调 stat→澄清误区→学习点 map | **4 个 Pillar 主文（L6-00-×4）** |
| [5 · Comparison](./type-5-comparison.md) | 2000-3000 | 5-8 | 180-250 | 中立介绍双方+暗示自家 | L6-08 AEO vs GEO（双标签策略） |
| [6 · Contrarian](./type-6-contrarian.md) | 2000-2200 | 6 | 100-150 | **承认共识→反对立场**（双层） | L6-17 CRM advisor / 未来反 AI 工具堆砌文 |
| [7 · Buyer's Guide](./type-7-buyers-guide.md) | 2200-2800 | 6-8 | 180-220 | 痛点→分流（需要 X？不需要 X？） | L6-01 AEO services / L6-17 CRM / L6-11 ad creative |

🔑 **不在 7 type 内的文章**：先回头检查 outline，多数情况能归入其中 1 种。实在不行，先按最近 type 写并标记为 "v0.6 候选新 type"。

---

## 4 · 段落写作规则（落到具体数字）

| 规则 | 具体值 | 来源 |
|---|---|---|
| **段落长度** | 50-150 字 / 3-5 句，允许 1-2 个长段 ~300-400 字承载复杂论证 | Ahrefs 实测 |
| **每个 H2 必含** | 至少 1 个 evidence（case / data / quote）+ 至少 1 个 actionable step | DUD Depth |
| **chunk-level 写法** | 每段开头 1 句自包含答案，不依赖上文；段内不用 "如前所述 / 上面说过" | Aleyda AEO 1 |
| **主词位置** | title / H1 / 首段（前 100 字）/ URL / meta / 至少 1 个 H2 | SEO 标准 |
| **主词密度** | 0.5%-1.5%（2500 字 → 13-38 次） | SEO 标准 |
| **二级词** | 5-8 个，每个 ≥1 次自然嵌入 | SEO 标准 |
| **LSI** | 5-8 个，散布全文 | SEO 标准 |
| **citation 钩子密度** | 每千字 ≥1 个可引用 stat 或 quote | Aleyda AEO 3 |
| **视觉元素密度** | **每 400-500 字 ≥1 个表 / 图 / 列表**（表 > 列表 > 图） | Ahrefs 实测 |
| **图片占位 default** | **每篇 ≥1 hero 图占位**（即使设计未交付，留 `[INSERT IMAGE: <prompt>]`）。Buyer's Guide / Pillar 推荐 ≥2，Definition / Contrarian / Step-by-Step 至少 1 个 hero。**0 张图占位 = checklist M18 不过 = 不允许 ship** | 图片 SEO + LLM multimodal |
| **数据时效** | 只用 2024-2026 数据，2023 之前的必带 "（XX 年数据，可能已变）" | DUD Update |
| **日期粒度** | "verified YYYY-MM"（精确到月）— 不用 "YYYY-Q" 季度模糊表述。每改一次内容同步改 `last_updated` | freshness 信号 |

---

## 5 · SEO + AEO 落地清单（嵌入式，不分开）

### SEO 落地（Ahrefs 步骤 8-9）

| # | 项 | 规则 |
|---|---|---|
| S1 | 主词位置 | title / H1 / 首段 / URL / meta / 至少 1 个 H2 |
| S2 | meta description | ≤155 chars，含主词 + buyer hook |
| S3 | 内链 | 5-8 个，**silo 内 ≥3 个**，30/30/30/10 锚文本分布（30% 精准主词 / 30% 部分匹配 / 30% 品牌或 URL / 10% 通用） |
| S4 | 外链 | 2-3 个权威源（data / stat 来源） |
| S5 | URL | `/blog/{silo}/{slug}` 嵌套。slug **必含主词全名或核心副词**（不写 "services-guide" / "buyers-guide" / "tools-list" 这种泛词），连字符分隔，≤5 词，**不带年份**（年份硬编码每年要改 URL）|
| S6 | 图片 alt | 含主词或同义词，描述图内容（不是 "image1.png"） |

### AEO 落地（Aleyda 8 点）

| # | 项 | 规则 |
|---|---|---|
| A1 | chunk 自包含 | 每段独立可引（见 §4） |
| A2 | answer-first | TL;DR / Answer box 在第 1 屏（Pillar / Buyer's / How-to / Definition 必含） |
| A3 | citation 钩子 | 每千字 ≥1 stat 或 quote，必带原文链 |
| A4 | topic breadth | silo 内链 ≥3 个 |
| A5 | multimodal | 每 400-500 字 ≥1 视觉（见 §4） |
| A6 | EEAT | frontmatter 含 author + author_avatar + author_linkedin + last_updated |
| A7 | personalization resilience | 不依赖 cookie / 设备 / 时间的纯文本（已自然满足，无需特殊处理） |
| A8 | crawlability | yolox 已 ship llms.txt + Organization schema（前端层已满足） |

---

## 6 · 自然嵌入 yolox 产品（Ahrefs 步骤 6）

| 规则 | 内容 |
|---|---|
| **频次** | 一篇 1-3 处 product mention，**不超过 3** |
| **嵌入方式** | ✅ case study（"X 用 yolox Aria 节省 70% 时间"）<br>✅ 工具栈对比（在 listicle 里把 yolox agent 列入对比表）<br>✅ "speed up with X"（在 step 中提示 "可以用 X 代替手工"）<br>❌ 销售口吻 / 强插 / 价格炫耀 |
| **CTA 落点** | 主 CTA → `/agents-store`（或具体 agent 页）<br>secondary CTA → 注册 / 邮件订阅 |
| **CTA 写法** | 行动动词短句："Try Aria for free" / "See the full agent list" |

🔑 **底线**：读者读完不知道我们是 yolox（没主动 mention 也行）≠ 失败；读者读到一半觉得"这是软文"= 失败。

---

## 7 · 发布前 checklist

完整 30 项见 [`checklist-pre-publish.md`](./checklist-pre-publish.md)。

**必须 18 项**（必过）：
1. brief 6 项全填 + 素材池齐全（含 source URL 100% 覆盖）
2. 字数在 type 规定区间
3. 主词出现位置全 ✅（title/H1/首段/URL/meta/H2）
4. 段落长度合规（无超 400 字段）
5. 每个 H2 ≥1 evidence + ≥1 actionable
6. citation 钩子密度 ≥1/千字
7. 视觉元素密度 ≥1/400-500 字
8. 内链 ≥7（silo 内 ≥3 + product ≥1 + 外链 ≥3）
9. 外链 ≥3 个权威源
10. meta description ≤155 chars + 含主词
11. frontmatter 字段齐（author / author_avatar / linkedin / toc / schema_type）+ slug 含主词 + linkedin 不是 TBD
12. 数据全部 2024-2026
13. yolox product mention ≤3 处
14. **drafting 完已隔 24h** 才编辑
15. **CTA ≥3 处布点**（intro 末 / 中段 / 结尾，不只结尾）
16. **`last_updated` 改到今天 + 日期写 YYYY-MM 不写 YYYY-Q**
17. **≥1 图片占位**（`[INSERT IMAGE: 描述]` 即使设计未完成也要留位）
18. **所有 stat 有 source URL**（找不到的写 "industry anecdotal estimate"）

**建议 13 项**（应过，不强卡）：见 checklist 文档。

---

## 8 · solo-op 改造（我不是 Ahrefs 团队）

| Ahrefs 角色 | yolox solo-op 替代 |
|---|---|
| SEO 顾问 | brief §1 必填 + checklist S1-S6 |
| 领域 expert | brief §5 引用素材池 + checklist 必含 ≥1 case |
| Writer | 你自己 / AI agent / 外包 |
| Editor | **24h 冷却 + 30 项 checklist** |

**24h 冷却纪律**：
- drafting 完成 → 关闭文档 → 24h 后回头编辑
- 编辑期不写新内容，只删 / 改 / 校
- 这是 Ahrefs "editing magic" 的唯一替代方案

---

## 9 · 使用流程图

```
┌─────────────────────────────────────────┐
│ 拿到 L6-XX 大纲（已有 25 篇）            │
└─────────────────────┬───────────────────┘
                      ↓
        ┌─────────────────────────┐
        │ 判断 type（7 选 1）       │
        │ → 打开 type-X.md         │
        └─────────────┬───────────┘
                      ↓
        ┌─────────────────────────┐
        │ 填 brief-template.md     │
        │ ~30min, 必填 5 项        │
        │ 素材池 ≥2 case + ≥3 data │
        └─────────────┬───────────┘
                      ↓
        ┌─────────────────────────┐
        │ 按 type 骨架 drafting    │
        │ + 主模板 §4 段落规则     │
        │ + §5 SEO/AEO 嵌入        │
        │ ~4-6h                   │
        └─────────────┬───────────┘
                      ↓
              ⏸ 关掉文档 24h
                      ↓
        ┌─────────────────────────┐
        │ 用 checklist 编辑        │
        │ 必须 15 项全 ✅          │
        │ ~2h                     │
        └─────────────┬───────────┘
                      ↓
                  ✅ Ship
```

---

## 10 · 已知缺陷 + 迭代计划

### v0.5 已知缺陷

| 缺陷 | 缓解 |
|---|---|
| 🟡 字数 / 段落 / 密度 default 基于 Ahrefs，未必适合 yolox 实际 | dogfood 1 节后校准 v0.6 |
| 🟡 7 type 可能不够覆盖（case study / opinion piece / interview 没列） | R3 ship 时如有不适配，加 v0.6 |
| 🟡 brief 30min 在 solo-op 是真负担 | 用模板压缩，可选项可跳，但素材池硬卡 |
| 🟠 24h 冷却纪律可能被现实打破 | 至少做到 4-8h 间隔，不要 0 间隔 |
| 🟠 AEO chunk-level 在 LLM 实际引用效果不可短期验 | Aleyda 框架 = 当前最佳假说，做了好过没做 |

### 迭代触发点

- **v0.6**：R3 第一批 1-2 篇 ship 后（基于真稿校准）
- **v1**：R3 全 8 篇 ship 后（定稿，可给外包 / agent 用）
- **v2**：R4 ship 完（加入 listicle 变种 / multimodal 升级 / 等）

---

## 11 · 发布节奏纪律

**核心**：写完 ≠ 发完。25 篇按 **每周 2 篇 / 12 周** 节奏 ship — 详见 [`publishing-cadence.md`](./publishing-cadence.md)。

🔑 **为什么不一次性 24 篇全发**：
- frontmatter `date` 改不了 Google 看到的"首次发现日"（Googlebot 抓取时间戳）
- 一夜 24 篇 = mass-produced flag 风险
- Pillar 主文最后发 = 自然收 5+ 内链 = 上线即高权重

→ Ship 前查 publishing-cadence.md §5 25 篇计划表确认本篇排期。

---

## 附录 · 标杆速查

| 来源 | 用在哪 |
|---|---|
| Ahrefs 6 模板 + 9 步流程 | §3 type 库 + §0-§9 流程 |
| Aleyda 8 点 AEO checklist | §5 AEO 部分 |
| Backlinko DUD 框架 | §4 数据时效 + §5 内链 + brief 角度声明 |
| Semrush content brief | brief-template.md 字段设计 |
| 3 篇 Ahrefs 真实文章实测 | §4 段落数字 default |
