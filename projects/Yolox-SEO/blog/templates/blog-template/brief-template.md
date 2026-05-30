# 文章 brief 模板

> 拿到 L6-XX 大纲后，写之前必填。
> **必填 6 项**缺一不允许开 drafting。
> 预计时间：30min（熟练后 15-20min）。

---

## 怎么用

1. 复制下方"模板"块到新文件：`brief-L6-XX.md`
2. 逐项填写
3. 检查"必填 6 项"全 ✅ → 开始 drafting

---

## 模板（复制下方块）

```markdown
# Brief · L6-XX · {主关键词}

> **大纲来源**：`../keyword-research/round-2-2026-04-28/blog-outlines/L6-XX.md`
> **填写日期**：YYYY-MM-DD
> **预计开写日期**：YYYY-MM-DD

---

## 【必填 1】关键词三件套

| 类 | 内容 |
|---|---|
| **主词** | (1 个) — V=___ / KD=___ / Growth=___ |
| **副词**（5-8 个） | (从 outline 抄 / 或 keyword-rankings.md 取) |
| **LSI**（5-8 个） | (语义相关词，从 SERP top 5 + PAA 提取) |

---

## 【必填 2】ICP + 痛点（1 段，从 outline 抄）

主 ICP：___
次 ICP：___（如有）

痛点 hypothesis：
1. ___
2. ___
3. ___

---

## 【必填 3】文章 type（7 选 1）

☐ Type 1 · List Post（无序列表）
☐ Type 2 · Step-by-Step（有序流程）
☐ Type 3 · Expanded Definition（概念扩展）
☐ Type 4 · Beginner's Guide（全面教育，Pillar 主文）
☐ Type 5 · Comparison（对比）
☐ Type 6 · Contrarian（反共识）
☐ Type 7 · Buyer's Guide（yolox 专版）

→ 打开对应 [`type-X.md`](./type-X.md) 看骨架

---

## 【必填 4】角度声明（DUD Depth）

竞品 top 5 都在讲：___
我们和他们不同的点是：___（1 句话）

🔑 这一句决定文章能不能"言之有物" — 含糊的角度 = 注定水文。

---

## 【必填 5】引用素材池（写之前先攒）

### Case（≥2 个）

| # | case 描述 | 出处 / 链接（**URL 必填**）| 嵌入到哪个 H2 |
|---|---|---|---|
| 1 | (eg. "X 公司用 Aria 节省 70% 提案时间") | https://... | H2.X |
| 2 | | | |

### Data / Stat（≥3 个，2024-2026）

| # | 数据 | 出处 / 链接（**URL 必填**）| 权威性 🟢/🟡/🔴 | 嵌入到哪个 H2 |
|---|---|---|---|---|
| 1 | (eg. "Seer Sept 2025: AIO 让 organic CTR 跌 61%") | https://... | 🟢/🟡/🔴 | intro 或 H2.X |
| 2 | | | | |
| 3 | | | | |

🔑 **权威性铁律**（详见 [`routing-matrix-v0.5.md §4`](./routing-matrix-v0.5.md)）：
- 🟢 强 = 第一手研究 / 业界领袖个人 blog / 官方文档（每篇至少 2 条 🟢）
- 🟡 中 = 权威媒体转述 / agency blog（可引但 niche）
- 🔴 弱 = secondary 汇总站 / 来源不明（**不允许引用**，去找原 source）

### Quote（≥1 条原话）

| # | 引文 | 出处 / 链接（**URL 必填**）| 嵌入到哪个 H2 |
|---|---|---|---|
| 1 | (eg. "Aleyda Solis on chunk-level..." 原话 ≤30 词) | https://... | H2.X |

🔑 **素材池不齐 = 不开 drafting**。这是言之有物的唯一硬保障。
🔑 **每条 source URL 必填**——WebSearch 抓不到原文 → 改写为 "industry anecdotal estimate"（不能假装有 source）。

---

## 【必填 6】Frontmatter & 内链清单（上线必需）

### A · Frontmatter 字段（每篇 markdown 顶部必含）

完整字段定义见 `0-share/frontend-spec.md §3`。简版：

```yaml
---
# 核心 SEO
title: "..."                       # ⚠️ ≤60 chars（含 brand suffix 也算）+ 含主词 + buyer hook 词
slug: "..."                        # ⚠️ 必含主词全名或核心副词，不写 "services-guide" 这种泛词
silo: aeo / ai-tools / b2b / creator
type: cluster / pillar
pillar: "..."                      # cluster 必填
description: "..."                 # ⚠️ ≤155 chars + 含主词

# 作者（Person schema 用）
author: "yolox team"               # 默认值，特殊情况标作者真名
author_avatar: "/images/authors/yolox-team.jpg"
author_linkedin: "https://www.linkedin.com/company/yolox-ai"  # ⚠️ 不能是 TBD
author_bio: "AI agent team SaaS for SMB..."  # 1-2 句 EEAT 信号

# 日期
date: YYYY-MM-DD
last_updated: YYYY-MM-DD           # ⚠️ 编辑日同步改

# Schema / 渲染控制
tags: ["...", "..."]
schema_type: FAQPage / HowTo / Article
toc: true                          # >1500 字默认 true
tracking_type: cluster / pillar    # GA4 event 区分

# OG / 社交
og_image: "/images/blog/{silo}/{slug}-hero.png"   # 1200x630，hero 同源
og_image_alt: "..."                # 含主词

# 国际化（中文版上线时）
lang: "en"
lang_alternates: []                # [{ lang: "zh", url: "..." }]
---
```

### B · 内链清单（**silo 内 ≥3 + product 链 ≥1 + 外链权威 ≥3**）

🔗 **URL 来源**（v0.6 起严格分工）：
- **yolox 内部 product 链**（agent / skill / team / category）→ [`url-inventory.md`](./url-inventory.md)（活数据 · 从 manifest 拉取 · 107+414+36 全收录）
- **silo 内 blog 间内链**（pillar / cluster）→ [`routing-matrix-v0.5.md §1-2`](./routing-matrix-v0.5.md)
- **外链权威源**（数据 / quote / pricing）→ [`routing-matrix-v0.5.md §4`](./routing-matrix-v0.5.md)
- **锚文本分布规则** → [`routing-matrix-v0.5.md §5`](./routing-matrix-v0.5.md)

🔑 **铁律**：**不允许现想 URL**——所有内链**完整 URL 形** `https://yolox.ai/...` 复制自上述文档。URL 在 brief 填写时验证存在，draft 阶段不再改。

| # | 锚文本 | 链接到（完整 URL）| 锚类型（精准/部分/品牌/通用）|
|---|---|---|---|
| 1 (silo 内) | | https://yolox.ai/blog/{silo}/{pillar-slug} | |
| 2 (silo 内) | | https://yolox.ai/blog/{silo}/{cluster-slug} | |
| 3 (silo 内) | | https://yolox.ai/blog/{silo}/{cluster-slug} | |
| 4 (product) | | https://yolox.ai/agents-store/{agent} 或 /skills-store/{cat}__{name} | |
| 5 (外链) | | https://... | |
| 6 (外链) | | https://... | |
| 7 (外链) | | https://... | |

🔑 分布：30% 精准锚 / 30% 部分 / 30% 品牌或 URL / 10% 通用（详见 routing-matrix §5）。
🔑 silo 内 <3 = AEO entity 关联弱 / Pillar 接不到内链 = 整 silo 排名集中度差。

---

## 【可选 7】SERP top 5 截图

跑一次 `google.com/search?q={主词}`，截 top 5 标题 + URL：

1. ___ — ___
2. ___ — ___
3. ___ — ___
4. ___ — ___
5. ___ — ___

**content gap**（top 5 缺什么，我们补什么）：___

> Buyer's Guide / Comparison 类强烈建议做；List / Definition 时间紧可跳。

---

## 【可选 8】关键词出现位置预规划

| 位置 | 关键词 | 备注 |
|---|---|---|
| Title | 主词 | + 1 个 hook 词（cost / 2026 / vs / best） |
| H1 | 主词 | 通常 = title |
| 首段（前 100 字） | 主词 | 自然第 1 次出现 |
| URL slug | 主词去停用词 + 连字符 | ≤5 词 |
| Meta description | 主词 | ≤155 chars |
| H2.X | 主词或副词 | 至少 1 个 H2 含 |

---

## 自检（开 drafting 前）

- [ ] 必填 1：关键词三件套齐
- [ ] 必填 2：ICP + 痛点写完
- [ ] 必填 3：type 选定
- [ ] 必填 4：角度声明 1 句话
- [ ] 必填 5：素材池齐（≥2 case + ≥3 data + ≥1 quote）+ **每条 source URL 必填**
- [ ] 必填 6：frontmatter 字段齐（slug 含主词 / author_linkedin 不是 TBD / toc / schema_type）+ 内链 ≥7（silo 内 ≥3 + product ≥1 + 外链 ≥3）

6 项全 ✅ → 开 drafting。任一缺 → 回去补，不允许"先写再补"。
```

---

## 示例 brief（参考）

> 暂用 `dogfood/L6-01-H2.1-sample.md` 的开头部分作示例。后续 R3 第一篇 ship 后，把那篇真 brief 移到此处作正式 reference。
