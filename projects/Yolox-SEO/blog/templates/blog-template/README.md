# yolox blog 写作模板 v0.5

> **用途**：把 25 篇 L6 大纲落地为可发布 markdown 的"工艺标准"。
> **日期**：2026-05-09
> **版本**：v0.5（🟡 可用级，dogfood 验证后迭代到 v1）
> **作者**：小刀老师 + Claude（基于 Ahrefs 6 模板 + Aleyda AEO 8 点 + Backlinko DUD 框架合成）

---

## 这是什么

一份**写 blog 的 SOP + 7 种文章 type 骨架库**。覆盖从「拿到 outline」到「ship 可发布 markdown」之间的全流程。

**解决的核心问题**：
- ❌ 大纲 → 4000 字 markdown 之间的桥
- ❌ "言之有物" 怎么变成可测量的规则
- ❌ SEO/AEO 怎么自然嵌入而不是事后补
- ❌ solo-op 一人扮 4 角色（writer / editor / SEO / expert）

---

## 文件清单

| 文件 | 用途 | 谁用 |
|---|---|---|
| [`yolox-blog-template-v0.5.md`](./yolox-blog-template-v0.5.md) | **主模板（SOP 主文，10 个 section）** | 所有人，先读 |
| [`brief-template.md`](./brief-template.md) | 写前 brief 表（**必填 6** + 可选 2 字段） | 写之前必填 |
| [`url-inventory.md`](./url-inventory.md) ⭐ | **yolox 内部 product URL 主清单**（107 agents + 414 skills + 36 teams 全收录 · path-style · 可点击）| 所有 product 内链**唯一权威源** |
| [`appendix-skills-developer-tools.md`](./appendix-skills-developer-tools.md) | Developer Tools 类 217 skills 独立附录 | url-inventory §5 引用 |
| [`routing-matrix-v0.5.md`](./routing-matrix-v0.5.md) | silo 内链矩阵 / 外链权威白名单 / 锚文本规则（**product URL 已迁移到 url-inventory.md**）| brief 填内链时查 |
| [`publishing-cadence.md`](./publishing-cadence.md) | 发布节奏纪律（25 篇 / 12 周 / Google 不可作弊的 5 重 detection）| ship 前 / 排期决策时 |
| [`checklist-pre-publish.md`](./checklist-pre-publish.md) | 发布前 checklist（**必须 18** + 建议 13） | ship 前必过 |
| [`type-1-list-post.md`](./type-1-list-post.md) | 无序列表文章骨架 | 按 type 选 |
| [`type-2-step-by-step.md`](./type-2-step-by-step.md) | 有序流程教学骨架 | 按 type 选 |
| [`type-3-expanded-definition.md`](./type-3-expanded-definition.md) | 概念扩展骨架 | 按 type 选 |
| [`type-4-beginners-guide.md`](./type-4-beginners-guide.md) | 全面教育骨架（Pillar 主文用） | 按 type 选 |
| [`type-5-comparison.md`](./type-5-comparison.md) | 对比文章骨架 | 按 type 选 |
| [`type-6-contrarian.md`](./type-6-contrarian.md) | 反共识观点骨架 | 按 type 选 |
| [`type-7-buyers-guide.md`](./type-7-buyers-guide.md) | yolox 专版买家指南骨架 | 按 type 选 |
| [`dogfood/L6-01-H2.1-sample.md`](./dogfood/L6-01-H2.1-sample.md) | dogfood 试跑：L6-01 第 1 节真稿 | 学规则的具体落地 |

---

## 怎么用（最简流程）

```
1. 拿到 outline（L6-XX.md）
   ↓
2. 判断 type → 打开对应 type-X.md
   ↓
3. 填 brief-template.md（30min，必填 6 项）
   ↓ product 链来自 url-inventory.md ⭐ / silo+外链来自 routing-matrix-v0.5.md
4. 按 type 骨架 + 主模板 §4 段落规则 drafting
   ↓
5. drafting 完 → **隔 24h** → 用 checklist 编辑
   ↓
6. checklist 必须 18 项全 ✅ → ship
   ↓ 按 publishing-cadence.md 排期（每周 2 篇 / 12 周完成 25 篇）
```

---

## 术语速查（SEO / AEO 行话）

写 / 读 blog 时高频出现的术语：

| 术语 | 全称 / 意思 | 用在哪 |
|---|---|---|
| **SEO** | Search Engine Optimization | 优化 Google 自然排名 |
| **AEO** | Answer Engine Optimization | 优化被 ChatGPT / Perplexity / AI Overview 引用 |
| **GEO** | Generative Engine Optimization | AEO 同义词的另一说法 |
| **CTA** | Call To Action（行动召唤）| Blog 里引导读者下一步动作的链接 / 按钮（如"Try yolox free →"），布点：顶 / 中 / 底各 1 |
| **EEAT** | Experience / Expertise / Authoritativeness / Trustworthiness | Google 2024+ 算法判断"作者真人 + 内容可信"的 4 大信号 |
| **Schema / JSON-LD** | 结构化数据 | 注入 `<head>` 的 JSON 代码，告诉 Google "这页是文章 / FAQ / 产品"，触发富媒体卡片 |
| **PAA** | People Also Ask | Google 搜索结果里的 FAQ 折叠 box，靠 FAQPage Schema 触发 |
| **AI Overview / AIO** | Google 在 SERP 顶部生成的 AI 答案 | 抢走 30-60% 流量的零点击罪魁 |
| **CTR** | Click-Through Rate | 点击率（impressions → clicks 的转化）|
| **silo** | 主题筒仓 | Pillar 主文 + 5 cluster 围绕同主题，URL 嵌套 `/blog/{silo}/{slug}` |
| **Pillar / Cluster** | 中枢 / 簇 | 1 篇全面 Pillar 主文 + N 篇专题 cluster 文章互链 |
| **slug** | URL 路径末段 | `/blog/aeo/answer-engine-optimization-services` 最后那段 |
| **chunk** | 文章的最小自包含段 | 50-150 字独立可读，LLM 抓取单元 |
| **anchor text** | 链接的可点文字 | 锚文本，影响 Google 理解链接含义 |
| **dogfood** | 自己用自己做的产品 / 模板 | 写完模板自己跑一篇验证 |

→ 不熟悉的术语 / 概念可问 AI 或查 [`routing-matrix-v0.5.md §4`](./routing-matrix-v0.5.md)（外链权威源含解释链）。

---

## 标杆来源

- **Ahrefs 6 模板**：[blog-post-templates](https://ahrefs.com/blog/blog-post-templates/)
- **Ahrefs 9 步写作流程**：[how-to-write-a-blog-post](https://ahrefs.com/blog/how-to-write-a-blog-post/)
- **Aleyda Solis 8 点 AI Search Checklist**：[learningseo.io](https://learningseo.io/seo_roadmap/optimize-ai-search/)
- **Backlinko Skyscraper DUD 框架**：[backlinko.com](https://backlinko.com/skyscraper-technique)
- **Ahrefs 3 篇真实文章实测**（字数/段落/视觉密度数据来源）：
  - List Post：[blogging-tips](https://ahrefs.com/blog/blogging-tips/)
  - Contrarian：[ai-content-is-short-term-arbitrage](https://ahrefs.com/blog/ai-content-is-short-term-arbitrage/)
  - Beginner's Guide：[duplicate-content](https://ahrefs.com/blog/duplicate-content/)

---

## 迭代计划

- **v0.5**（当前）：基于标杆合成，dogfood 1 节验证可跑
- **v0.6**：R3 第一批 1-2 篇 ship 后基于真稿校准（字数/密度/checklist 删减）
- **v1**：R3 全部 8 篇 ship 后定稿
