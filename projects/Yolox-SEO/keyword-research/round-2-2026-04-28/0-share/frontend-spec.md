# yolox blog 前端需求 · 必做清单

> **变更（2026-05-12）**：原 P0/P1/P2 分级取消。**所有项必须 ✅ 才允许 blog ship**。
> **覆盖**：技术 SEO + Schema + EEAT + 导航 + Meta/OG/Hreflang + UX/性能 + AEO/追踪
> **来源**：2 轮独立 SEO 审计（11 点 + 66 点）汇总修正

---

## 0 · 现状（2026-05-12）

| 已 ship | 在哪 |
|---|---|
| ✅ Organization JSON-LD（全局）| `src/app/layout.tsx` |
| ✅ 默认 Title / Meta description | `src/app/layout.tsx` |
| ✅ sitemap.ts（含 agents/skills/teams）| `src/app/sitemap.ts` |
| ✅ robots.ts | `src/app/robots.ts` |
| ✅ apple-touch-icon | `src/app/layout.tsx` |

| 未 ship（本文档要求）| 状态 |
|---|---|
| ❌ blog 路由 `/blog/{silo}/{slug}` | 路由未建 |
| ❌ Article / FAQPage / BreadcrumbList / Person / HowTo / Speakable JSON-LD | 全缺 |
| ❌ blog frontmatter parser + 渲染管线 | 未建 |
| ❌ 作者 bio block / Breadcrumb 导航 / TOC / Continue Reading 等 | 全缺 |

---

## 1 · markdown 原生支持（无需调整）

| 元素 | 状态 | 备注 |
|---|---|---|
| H1 / H2 / H3 / H4 标题层级 | ✅ | 25 篇全部使用 |
| 正文段落 / 列表 / 表格 | ✅ | 25 篇全部 |
| 引用框（blockquote）| ✅ | TL;DR / 警告 |
| 代码块（语言标注）| ✅ | DIY prompt / Schema 示例 |
| 内链 / 外链 | ✅ | 25 篇 |
| 图片 | ✅ | 由作者按需放（含 `[INSERT IMAGE: ...]` 占位 — 见 2.E.4）|

---

## 2 · 必做项（全部 ✅ 才允许 ship）

### 2.A · Schema / 结构化数据（最大缺口）

> Schema = 用 JSON-LD 格式注入 `<head>` 的"分类标签"。无 Schema = Google 把 blog 当普通 HTML = 富媒体卡片不显示 + AI Overview / PAA 不引 = CTR -30% + AEO 流量 -70%。

| # | Schema 类型 | 用在哪 | 实现要点 |
|---|---|---|---|
| **2.A.1** | **Article JSON-LD** | 每篇 blog 必含 | 从 frontmatter `title / author / date / last_updated / image / description` 自动生成。模板见 §7 |
| **2.A.2** | **FAQPage JSON-LD** | 含 FAQ 节的 blog（buyer's guide / pillar 必含）| 识别 H2 = "FAQ" 节下的 H3 + 紧跟段落 → `mainEntity` Q&A 数组。**实际渲染后用 [Google Rich Results Test](https://search.google.com/test/rich-results) 验证**。模板见 §9 |
| **2.A.3** | **BreadcrumbList JSON-LD** | 每篇 blog 必含 | 从 URL `/blog/{silo}/{slug}` 自动生成 3 层级（Home > Blog > {silo title} > {article title}）。模板见 §8 |
| **2.A.4** | **Person JSON-LD** | 每篇 blog 必含 | 从 frontmatter `author / author_linkedin / author_avatar` 生成。含 `name / url / image / sameAs:[linkedin]`。模板见 §10 |
| **2.A.5** | **Organization JSON-LD** | 已 ship 部分 | 补全 `sameAs:[LinkedIn / Twitter / GitHub]`。**LinkedIn Company Page 必须先建**（15min，免费） |
| **2.A.6** | **HowTo JSON-LD** | type-2 step-by-step 用 | 识别 H2 = "Step N: ..." 模式，生成 `step` 数组 |
| **2.A.7** | **Speakable JSON-LD** | FAQ 节 + TL;DR 节 | 仅标记可朗读节点的 cssSelector，为语音搜索 / Google Assistant 准备 |

---

### 2.B · EEAT 信号（Google 2024+ 严判 AI 编内容）

> EEAT = Experience / Expertise / Authoritativeness / Trustworthiness。无作者信息 → Google 判定为低信任内容 → 排名降。

| # | 项 | 实现 |
|---|---|---|
| **2.B.1** | 作者 bio block（文末）| frontmatter `author / author_avatar / author_linkedin / author_bio` → 渲染头像 + 名字 + 简介 + LinkedIn link |
| **2.B.2** | 顶部元信息条 | "作者头像 · 作者名 · 发布日期 · last updated · 预计阅读时间" 横排 |
| **2.B.3** | Last updated date 可见 | frontmatter `last_updated` 或从 git commit 自动取，每编辑 1 次同步改 |
| **2.B.4** | 发布日期可见 | frontmatter `date` |
| **2.B.5** | 作者简介页 `/authors/{slug}` | 含照片 + 简介 + 历史文章列表。**Person Schema 的 url 字段指向这里** |

---

### 2.C · 导航 / 内链

| # | 项 | 实现 |
|---|---|---|
| **2.C.1** | Breadcrumb 导航条 | URL 路径自动生成 + silo title mapping（aeo → "AEO" / ai-tools → "AI Tools" / b2b → "B2B Operations" / creator → "Creator Toolkit"）。**UI + BreadcrumbList Schema 同步** |
| **2.C.2** | silo entry page `/blog/{silo}` | 4 个 silo 索引页，自动列出本 silo 文章 + 简介 + 排序（Pillar 主文置顶 / cluster 按 date 排）。**Pillar 主文 ship 后充当 silo hero 内容** |
| **2.C.3** | Continue Reading（silo 内推荐 3 篇）| silo + tag 筛选 + 排除当前文章。文末渲染 |
| **2.C.4** | 自动 TOC（>1500 字默认开）| `remark-toc` 或 `rehype-toc` plugin。**frontmatter `toc: true` 信号开启**；侧边浮动 TOC（桌面端） + 折叠 TOC（移动端） |
| **2.C.5** | H2 自动 anchor id | slug 化 H2 文本作 id，TOC 可点击跳转。**作者写 markdown 时引用某 H2 的 anchor 必须用 slug 化后的 id** |

---

### 2.D · Meta / OG / Twitter / Canonical / Hreflang

| # | 项 | 实现 |
|---|---|---|
| **2.D.1** | **Canonical 标签** | 每篇自指 `<link rel="canonical" href="https://yolox.ai/blog/{silo}/{slug}">`。Next.js `generateMetadata` 自动 |
| **2.D.2** | **Hreflang** | 中文版上线时声明 `<link rel="alternate" hreflang="zh" href="...">` + `hreflang="en"`。**当前预留 frontmatter `lang_alternates` 字段** |
| **2.D.3** | **Open Graph 完整字段** | `og:title` / `og:description` / `og:image`（1200x630） / `og:url` / `og:type=article` / `og:site_name` / `article:author` / `article:published_time` / `article:modified_time` |
| **2.D.4** | **Twitter Card** | `twitter:card=summary_large_image` / `twitter:title` / `twitter:description` / `twitter:image` / `twitter:site=@yolox_ai` |
| **2.D.5** | **Meta description** | frontmatter `description` ≤155 chars。**超过会被截断** |
| **2.D.6** | **Title 标签** | frontmatter `title` ≤60 chars。可加 brand suffix " \| yolox" 但要算进 60 字内 |
| **2.D.7** | **Robots meta** | 默认 `index, follow`。`/login` `/register` `/billing` 已 disallow（robots.ts） |

---

### 2.E · UX / 性能

| # | 项 | 实现 |
|---|---|---|
| **2.E.1** | 预计阅读时间显示 | 自动计算（中文字数 / 300 wpm 或英文 / 200 wpm），渲染在顶部元信息条 |
| **2.E.2** | 宽表响应式 | markdown 渲染时 `<table>` 自动包裹 `<div style="overflow-x: auto">`，或全局 CSS `table { display: block; overflow-x: auto; }` |
| **2.E.3** | Image lazy loading | `<img loading="lazy">` 默认 |
| **2.E.4** | `[INSERT IMAGE: ...]` 占位识别 | markdown 渲染识别 `\[INSERT IMAGE: <prompt>\]` → 渲染成虚线灰色占位框 + 显示 prompt 文本。**上线前必须替换为真实图（hero 图必须双重用途：alt text + og:image）** |
| **2.E.5** | 决策树 / 信息图 SVG 升级 | 当前文章用 ASCII 决策树 — 设计师后期升级为 SVG（更好的图片搜索 + 移动端可读性）|

---

### 2.F · 追踪 / AEO

| # | 项 | 实现 |
|---|---|---|
| **2.F.1** | GA4 events | `blog_view`（页面 load）/ `pillar_view`（type=pillar 时）/ `scroll_75`（滚到 75%）/ `internal_link_click_{target}`（点击内链）/ `clipboard_copy_template`（复制 code block）。frontmatter `tracking_type` 区分 blog/pillar |
| **2.F.2** | **llms.txt 文件** | `public/llms.txt` 静态文件。LLM crawler 优先读，决定抓哪些页。模板见 §5 |
| **2.F.3** | sitemap.xml 自动收录 blog | `src/app/sitemap.ts` 加 blog 路由动态读取（按 silo + slug） |

---

## 3 · frontmatter 完整字段定义（每篇 markdown 顶部必含）

```yaml
---
# 必填字段
title: "Best Answer Engine Optimization Services for SMB Brands (2026)"  # ≤60 chars
slug: "answer-engine-optimization-services"                              # 必含主词
silo: "aeo"                                                              # aeo / ai-tools / b2b / creator
type: "cluster"                                                          # cluster / pillar
pillar: "AEO"                                                            # cluster 必填，pillar 类型可空

# 作者字段（Person schema 用）
author: "yolox team"                                                     # 默认；特殊场景标真名
author_avatar: "/images/authors/yolox-team.jpg"                          # 200x200 webp / png
author_linkedin: "https://www.linkedin.com/company/yolox-ai"
author_bio: "AI agent team SaaS for SMB and non-technical users"         # 1-2 句 EEAT 信号

# 日期
date: 2026-05-12                                                         # 发布日
last_updated: 2026-05-12                                                 # 每次编辑同步改

# Meta / SEO
description: "AEO services pricing $1.5k–$60k/month. Buyer's guide..."   # ≤155 chars
tags: ["AEO", "buyer's guide", "answer engine optimization"]

# Schema 控制
schema_type: "FAQPage"                                                   # FAQPage / HowTo / Article（默认 Article）
toc: true                                                                # >1500 字默认 true
tracking_type: "cluster"                                                 # blog / pillar — GA4 event 区分

# OG 字段（前端从 frontmatter 取）
og_image: "/images/blog/aeo/services-guide-hero.png"                     # 1200x630，与 hero 图同源
og_image_alt: "AEO services pricing tiers 2026"                          # alt text 必含主词

# 国际化（中文版上线时）
lang: "en"                                                               # 当前语言
lang_alternates:                                                         # 其他语言版本（可空）
  - { lang: "zh", url: "/zh/blog/aeo/answer-engine-optimization-services" }
---
```

---

## 4 · 实施依赖图（取代原 P0/P1/P2 节奏）

```
┌─────────────────────────────────────────────────────────┐
│  Foundation（必须先做）                                  │
│  ├─ blog 路由 /blog/{silo}/{slug}                       │
│  ├─ frontmatter parser（解析 §3 全字段）                 │
│  └─ markdown 渲染管线（remark + rehype 插件链）          │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ 2.A Schema   │ │ 2.B EEAT     │ │ 2.C 导航    │ │ 2.D Meta/OG │
│ 6 类 JSON-LD │ │ 作者 / 日期  │ │ Breadcrumb  │ │ Canonical   │
│              │ │              │ │ silo entry  │ │ Hreflang    │
│              │ │              │ │ TOC / 内链   │ │ OG / Twitter│
└──────────────┘ └──────────────┘ └─────────────┘ └──────────────┘
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌──────────────┐               ┌──────────────┐
│ 2.E UX/性能  │               │ 2.F 追踪/AEO │
│ 阅读时间 / 宽表│              │ GA4 / llms.txt│
│ lazy / 占位识别│              │ sitemap.xml  │
└──────────────┘               └──────────────┘
```

→ Foundation 是阻塞节点。其他 5 个组（2.A-2.F）并行实施。**任一组未完成 = blog 不允许 ship**。

---

## 5 · llms.txt 模板

文件位置：`public/llms.txt`（访问 `yolox.ai/llms.txt`）

```markdown
# yolox

> AI agent team SaaS for SMB and non-technical white-collar users.
> Helps consultants / creators / sales / SMB owners use AI agents
> to replace specialized tools and workflows.

## Blog

- [Blog homepage](/blog) - Articles on AI agents, AEO, and SMB tools

### Topics

- [AEO Guide](/blog/aeo) - Answer Engine Optimization for SMB and marketers
- [AI Tools](/blog/ai-tools) - AI tools by SMB use case (proposal / ad / newsletter / story / infographic)
- [B2B Operations](/blog/b2b) - Sales / recruiting / project management AI agents
- [Creator Toolkit](/blog/creator) - Podcast / amazon / shopify / restaurant tools

## Product

- [Agents Store](/agents-store) - AI agents catalog
- [Skills Store](/skills-store) - Skills catalog
- [Teams Store](/teams-store) - Teams catalog
- [About](/about) - What yolox is and who it's for

## Optional

- [Login](/login)
- [Register](/register)
```

> 静态文件，无需 build。LLM crawler 优先读 llms.txt 决定抓哪些页。

---

## 6 · Organization schema 模板（全局 `<head>` 注入）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "yolox",
  "url": "https://yolox.ai",
  "logo": "https://yolox.ai/images/logo.png",
  "description": "AI agent team SaaS for SMB and non-technical white-collar users",
  "sameAs": [
    "https://www.linkedin.com/company/yolox-ai",
    "https://twitter.com/yolox_ai",
    "https://github.com/Infinite-Flow-Labs"
  ]
}
</script>
```

🔑 `sameAs` 数组帮 LLM 关联 entity 到外部权威源。**LinkedIn / Twitter 账号没建 = entity 信号弱**——先建（免费 15min）。

---

## 7 · Article schema 模板（每篇 blog `<head>` 注入）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ frontmatter.title }}",
  "description": "{{ frontmatter.description }}",
  "image": "https://yolox.ai{{ frontmatter.og_image }}",
  "datePublished": "{{ frontmatter.date }}",
  "dateModified": "{{ frontmatter.last_updated }}",
  "author": {
    "@type": "Person",
    "name": "{{ frontmatter.author }}",
    "url": "https://yolox.ai/authors/{{ author_slug }}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "yolox",
    "logo": {
      "@type": "ImageObject",
      "url": "https://yolox.ai/images/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://yolox.ai/blog/{{ silo }}/{{ slug }}"
  }
}
</script>
```

---

## 8 · BreadcrumbList schema 模板（每篇 blog `<head>` 注入）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://yolox.ai/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://yolox.ai/blog"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{ silo_title }}",
      "item": "https://yolox.ai/blog/{{ silo }}"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "{{ frontmatter.title }}"
    }
  ]
}
</script>
```

---

## 9 · FAQPage schema 模板（含 FAQ 节的 blog 注入）

自动从 markdown 抽取：识别 `## FAQ` 节，把每个 `### Q?` + 紧跟段落作 mainEntity 数组。

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much do AEO services cost in 2026?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "AEO services range from $1.5k for a one-time audit to $60k+/month for embedded enterprise retainers..."
      }
    }
    // 5-10 个 FAQ 自动循环
  ]
}
</script>
```

🔑 **渲染后用 [Google Rich Results Test](https://search.google.com/test/rich-results) 验证 JSON-LD 合法**。FAQPage 是 PAA box + AI Overview 的核心信号——做错了等于白做。

---

## 10 · Person schema 模板（每篇 blog 作者注入）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{{ frontmatter.author }}",
  "url": "https://yolox.ai/authors/{{ author_slug }}",
  "image": "https://yolox.ai{{ frontmatter.author_avatar }}",
  "description": "{{ frontmatter.author_bio }}",
  "sameAs": [
    "{{ frontmatter.author_linkedin }}"
  ],
  "worksFor": {
    "@type": "Organization",
    "name": "yolox",
    "url": "https://yolox.ai"
  }
}
</script>
```

---

## 11 · HowTo schema 模板（type-2 step-by-step 用）

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "{{ frontmatter.title }}",
  "description": "{{ frontmatter.description }}",
  "totalTime": "PT30M",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1: Find your prospects",
      "text": "Open LinkedIn Sales Navigator...",
      "url": "https://yolox.ai/blog/b2b/cold-email-deliverability#step-1"
    }
    // 5-10 个 step 自动循环
  ]
}
</script>
```

---

## 12 · 验证流程（上线前必跑）

每篇 blog ship 前 3 项 Schema 验证：

1. **Google Rich Results Test**（https://search.google.com/test/rich-results）— 粘 URL 或 HTML，验证 Article / FAQPage / BreadcrumbList / Person / HowTo 是否合法
2. **Schema.org Validator**（https://validator.schema.org/）— 验证 JSON-LD 语法
3. **手动验证 OG**：粘 URL 到 [opengraph.xyz](https://www.opengraph.xyz/) 看 OG 预览

任一不过 → 修复后再 ship。

---

## 13 · sameAs 外部 entity 清单（Organization + Person schema 用）

| Entity | URL | 状态 |
|---|---|---|
| **LinkedIn Company Page** | https://www.linkedin.com/company/yolox-ai | ⚠️ 未确认是否建好 |
| **Twitter Company Account** | https://twitter.com/yolox_ai | ⚠️ 未确认 |
| **GitHub Org** | https://github.com/Infinite-Flow-Labs | ✅ 已建 |
| **Crunchbase**（如有）| TBD | ❌ 推荐建（免费）|
| 作者 LinkedIn | 见 frontmatter `author_linkedin` | ⚠️ 当前用 yolox team 占位 |

🔑 **LinkedIn Company Page 是 entity 信号的关键**——15min 免费建。没有 = LLM 不知道 yolox 是真公司 = 引用率 -30%。

---

## 附录 · 与 markdown 写作模板的接口

本文档 = 前端实现层。  
写作层模板 = `docs/seo/blog-template/`：

| 写作模板规则 | 前端对应 |
|---|---|
| brief 必填 6 项 frontmatter | §3 完整字段定义 |
| 主 SOP §5 SEO 落地（slug 含主词等）| §2.D.5/6 Title/Meta 长度 + §2.A.1 Article schema |
| checklist M14（frontmatter 字段齐）| §3 字段定义 |
| checklist M16（CTA ≥3 处）| 渲染层不参与 — 作者保证 |
| checklist M18（≥1 图占位）| §2.E.4 `[INSERT IMAGE]` 渲染 |
| type-7 buyer's guide CTA / 图占位规范 | §2.E.4 + §2.A.1 image 字段 |

→ 任一写作模板字段添加 → 同步本文档 §3 字段定义。
