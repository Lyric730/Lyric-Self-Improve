# YOLOX 网站 SEO 审计报告

**日期**: 2026-04-16
**审计工具**: Claude Code
**审计 Skill**: [SEO Audit by Marketing Skills](https://skills.sh/coreyhaines31/marketingskills/seo-audit)
**站点**: YOLOX Web (Next.js 16)
**范围**: 全站审计 — 技术 SEO、页面 SEO、国际化、结构化数据

> **复审**: 修复完成后，可再次使用 `/marketing-skills:seo-audit` 技能对站点进行复审，验证修复效果。

---

## 复审记录（2026-04-20）

核对 17 项修复：**7 项已完成**、**1 项部分完成**、**9 项未完成**。下方"修复清单"表已用 `[x]` / `[ ]` 标注状态，已完成项加删除线。

### 快速状态

| 状态 | 数量 | 项次 |
|------|------|------|
| ✅ 已完成 | 7 | #1 sitemap、#2 robots、#4 metadataBase、#5 H1、#6 根 description、#7 title template、#3 OG/Twitter 字段 |
| ⚠️ 部分完成 | 1 | #3 OG 字段已配，但图片引用 `.svg`（Twitter/LinkedIn/微信多不渲染 SVG，等同于没有 OG 图） |
| ❌ 未完成 | 9 | #8 图片 alt、#9 详情页 OG、#10 hreflang、#11 OG 图 PNG、#12–13 JSON-LD、#14 i18n URL 前缀、#15 noindex、#16 manifest、#17 多尺寸 favicon |

### 下一步建议

1. **最紧急**：生成 `public/og-image.png`（1200×630），替换 `src/app/layout.tsx` 中 `openGraph.images` 和 `twitter.images` 的路径 — 让 #3 真正生效
2. 动态详情页在 `generateMetadata()` 补 `openGraph: { title, description, images }`（#9）
3. 根 layout 加 `alternates.languages: { en, zh }`（#10）
4. 首页图片 alt 逐个补（#8），装饰性加 `role="presentation"`

---

## 概要

YOLOX 网站基于 Next.js 16 构建，具备基础的页面级 metadata，但在搜索引擎可发现性方面存在多个关键缺失。当前站点所有页面均配置了 title 和 description，动态详情页（Agent/Skill/Team）也实现了 `generateMetadata()`，这是好的基础。但缺少 robots.txt、sitemap、Open Graph 标签等核心 SEO 基础设施，严重影响搜索引擎收录和社交分享效果。

### 问题总览

| 优先级 | 问题 | 影响 |
|--------|------|------|
| **P0 Critical** | 无 robots.txt | 搜索引擎无爬取指令 |
| **P0 Critical** | 无 sitemap.xml | 搜索引擎无法发现页面 |
| **P0 Critical** | 无 Open Graph / Twitter Card 元数据 | 社交分享无预览 |
| **P1 High** | 首页缺少 H1 标签 | 搜索引擎无法识别页面主题 |
| **P1 High** | 大量图片 alt="" 为空 | 可访问性和图片搜索流量损失 |
| **P1 High** | 无 hreflang 多语言标签 | 中英文页面无法正确关联 |
| **P2 Medium** | 无 JSON-LD 结构化数据 | 搜索结果无富文本片段 |
| **P2 Medium** | 根 metadata 描述过于笼统 | "YOLOX homepage" 不够描述性 |
| **P3 Low** | 无 canonical 标签 | 潜在重复内容风险 |
| **P3 Low** | 无 web manifest | PWA 支持缺失 |

---

## 1. 可爬取性与索引

### 1.1 robots.txt — 缺失 (Critical)

**问题**: 项目中无 `robots.txt`（`public/robots.txt` 和 `src/app/robots.ts` 均不存在）。

**影响**: 搜索引擎缺少爬取指令，无法知道哪些路径应该/不应该被索引。

**修复建议**: 创建 `src/app/robots.ts`：

```ts
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/client-home/', '/billing/', '/auth/'],
      },
    ],
    sitemap: 'https://yolox.ai/sitemap.xml',
  };
}
```

### 1.2 Sitemap — 缺失 (Critical)

**问题**: 无 `sitemap.ts` 或 `sitemap.xml`。

**影响**: 搜索引擎无法自动发现所有公开页面，尤其是动态的 agent/skill/team 详情页。

**修复建议**: 创建 `src/app/sitemap.ts`：

```ts
import type { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const staticPages = [
    '/', '/home', '/agents-store', '/skills-store',
    '/teams-store', '/privacy', '/terms',
  ];

  // TODO: 从 GitHub manifest 获取动态 agent/skill/team ID
  // const agents = await fetchAgentsList();

  return staticPages.map((path) => ({
    url: `https://yolox.ai${path}`,
    lastModified: new Date(),
    changeFrequency: 'weekly',
    priority: path === '/home' ? 1.0 : 0.8,
  }));
}
```

### 1.3 需要屏蔽的路径

以下路径应在 robots.txt 中设置 disallow：

- `/api/*` — API 路由
- `/client-home/` — 认证后工作区
- `/billing/*` — 账单页面
- `/auth/*` — OAuth 回调
- `/login`、`/register` — 登录注册（可选）
- `/invite-code/`、`/waitlist/` — 重定向页面

---

## 2. 页面 SEO

### 2.1 首页缺少 H1 标签 — High

**问题**: `HomeLayout.tsx` 只有两个 `<h2>` 标签（第 733 行和第 944 行），没有 `<h1>`。

**影响**: 搜索引擎无法准确判断页面主题。H1 是页面最重要的标题信号。

**证据**:
- 第 733 行: `<h2 className="font-zpix ...">` (Hero 区域)
- 第 944 行: `<h2 className="font-zpix ...">` (第二板块)

**修复建议**: 将主标题改为 `<h1>`：

```tsx
<h1 className="...">YOLOX — Your AI Agent Platform</h1>
```

### 2.2 图片 alt 属性大量为空 — High

**问题**: `HomeLayout.tsx` 中 25+ 个 `<Image>` 组件中，约 20 个使用 `alt=""`。

**证据**（部分空 alt 行号）:
- 第 52, 549, 567, 598, 626, 663, 671, 765, 818, 833, 846, 863, 878, 891, 915, 955, 963, 971, 1033, 1041, 1049 行

仅少数图片有有意义的 alt 文本：
- 第 467 行: `alt={t("agentDeviceAlt")}` (国际化)
- 第 701 行: `alt={`${item.label} icon`}` (动态)
- 第 746 行: `alt={t("codeSnippetBackgroundAlt")}` (国际化)
- 第 986, 1011 行: `alt="YOLOX"` (品牌 Logo)

**影响**: 搜索引擎无法理解图片内容，失去图片搜索流量；可访问性也会降低。

**修复建议**: 为每个有意义的图片添加描述性 alt 文本。纯装饰性图片可保留 `alt=""`，但应加 `role="presentation"`。

### 2.3 Meta Description 质量

| 页面 | 当前 Description | 评价 |
|------|------------------|------|
| 根 Layout | "YOLOX homepage" | 过于笼统，需改进 |
| Home | "Explore YOLOX AI agents, teams, and workflows in one place." | 可接受 |
| Agent Store | "Browse curated AI agents from the YOLOX agent store." | 可接受 |
| Skills Store | "Browse YOLOX skills calibrated for new workflows and templates." | 可接受 |
| Teams Store | "Discover team templates and collaboration-ready agent bundles." | 可接受 |
| App Store | "Install ready-made YOLOX agents and templates from the app store." | 可接受 |
| Login | "Sign in to your YOLOX workspace to access agents and projects." | 可接受 |
| Register | "Create a YOLOX account to start building with AI agents." | 可接受 |
| Workspace | "Jump back into your personalized YOLOX workspace with agents and conversations." | 可接受 |
| Privacy | "Read the YOLOX Privacy Policy." | 可接受 |
| Terms | "Read the YOLOX Terms of Service." | 可接受 |

**修复建议**: 更新根 layout 的 description：

```ts
description: "YOLOX is an AI agent platform for building, deploying, and collaborating with intelligent agents."
```

### 2.4 Title 标签结构

当前模式: `"YOLOX | Page Name"` — 品牌名在前。

**修复建议**: 将品牌名移到末尾以提升关键词可见度：`"Page Name | YOLOX"`。使用 Next.js 的 title template：

```ts
title: {
  default: "YOLOX",
  template: "%s | YOLOX",
},
```

这样子页面只需设置 `title: "Agent Store"` 即可自动生成 `"Agent Store | YOLOX"`。

---

## 3. 社交分享（Open Graph 与 Twitter Card）

### 3.1 无 Open Graph / Twitter Card 元数据 — Critical

**问题**: 全站没有任何 Open Graph 或 Twitter Card meta 标签，也没有 `opengraph-image` 文件。

**影响**: 链接在 Twitter、LinkedIn、微信、Slack 等平台分享时没有预览图和描述。

**证据**: 在整个 `src/` 目录中搜索 `openGraph|twitter|og:` 返回零结果。

**修复建议**: 在根 `layout.tsx` 的 metadata 中添加：

```ts
export const metadata: Metadata = {
  metadataBase: new URL('https://yolox.ai'),
  title: {
    default: "YOLOX",
    template: "%s | YOLOX",
  },
  description: "YOLOX is an AI agent platform for building, deploying, and collaborating with intelligent agents.",
  openGraph: {
    type: "website",
    siteName: "YOLOX",
    images: [{ url: "/og-image.png", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    images: ["/og-image.png"],
  },
};
```

同时设计一张 1200x630 的 OG 图片放在 `public/og-image.png`。

对于动态页面（agent/skill/team 详情），在 `generateMetadata()` 中补充 OG 数据：

```ts
openGraph: {
  title: agentName,
  description: agentDescription,
  images: [agentImageUrl || "/og-image.png"],
},
```

---

## 4. 国际化 (i18n) SEO

### 4.1 缺少 hreflang 标签 — High

**问题**: 网站支持 en/zh 两种语言，但没有配置 `alternates` metadata。

**影响**: 搜索引擎无法将中英文版本关联，可能导致重复内容惩罚或在搜索结果中显示错误的语言版本。

**证据**: 在 `src/` 中搜索 `canonical|alternate|hreflang` 返回零结果。

**修复建议**: 在 metadata 中添加：

```ts
alternates: {
  languages: {
    en: "https://yolox.ai/en",
    zh: "https://yolox.ai/zh",
  },
},
```

### 4.2 URL 结构不含语言前缀

**问题**: i18n 通过 cookie 检测语言（`NEXT_LOCALE`），URL 中不包含 `/en/` 或 `/zh/` 前缀。

**影响**: 搜索引擎无法区分同一页面的不同语言版本。同一 URL 根据 cookie 返回不同内容是 SEO 的反面模式。

**修复建议**: 考虑使用 next-intl 的 URL 前缀模式（`/en/home`、`/zh/home`）。这是多语言站点的 SEO 最佳实践。注意：这涉及较大的架构改动，需谨慎评估。

---

## 5. 结构化数据（Schema Markup）

### 5.1 无 JSON-LD — Medium

**问题**: 全站没有任何 JSON-LD 结构化数据。

**影响**: 搜索结果中不会显示富文本片段（产品评分、FAQ 折叠、面包屑等）。

**证据**: 搜索 `json-ld|JsonLd|structured.?data|schema.org` 返回零结果。

**修复建议**:

**首页** — `WebSite` + `Organization` schema：

```tsx
<script type="application/ld+json">
{JSON.stringify({
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "YOLOX",
  "url": "https://yolox.ai",
  "description": "AI agent platform for building and collaborating with intelligent agents",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://yolox.ai/agents-store?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
})}
</script>
```

**Agent 详情页** — `SoftwareApplication` schema：

```tsx
<script type="application/ld+json">
{JSON.stringify({
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": agentName,
  "description": agentDescription,
  "applicationCategory": "AI Agent",
  "operatingSystem": "Web"
})}
</script>
```

---

## 6. 技术 SEO

### 6.1 Canonical 标签 — Low

**问题**: 未显式配置 canonical 标签。没有设置 `metadataBase` 时 Next.js 不会自动生成。

**修复建议**: 在根 layout metadata 中设置 `metadataBase`：

```ts
metadataBase: new URL('https://yolox.ai'),
```

设置后 Next.js 会自动为每个页面生成 canonical URL。

### 6.2 Web Manifest — Low

**问题**: public 目录中没有 `manifest.json` 或 `manifest.webmanifest`。

**影响**: 浏览器无法识别 PWA 能力，"添加到主屏幕"体验缺失。

**修复建议**: 创建 `public/manifest.json` 配置基本 PWA 元数据。

### 6.3 Favicon

**当前状态**: 使用 `/yolox_logo.svg` 作为 favicon。`public/` 中已有 `favicon.ico`（25.9KB）。

**修复建议**: 补充多尺寸 PNG 以支持 `apple-touch-icon` 等设备图标：

```ts
icons: {
  icon: "/favicon.ico",
  apple: "/apple-touch-icon.png",
},
```

### 6.4 安全与 HTTPS

- `/login` 和 `/register` 路由已配置 CORS 头（Cross-Origin-Opener-Policy）
- API 代理重写配置正确
- `/api/preview-delivery` 路由有 SSRF 防护

**状态**: 正常。

### 6.5 Next.js 配置

- React Compiler 已启用（`reactCompiler: true`）— 有利于性能
- Webpack 内存优化已启用
- 图片优化已配置远程和本地模式

**状态**: 正常。

---

## 7. 内容与页面结构

### 7.1 页面审计

| 页面 | Title | Description | H1 | OG | Canonical | 状态 |
|------|-------|-------------|----|----|-----------|------|
| / (首页) | YOLOX \| Home | 有 | 缺失 | 无 | 无 | 需修复 |
| /agents-store | YOLOX \| Agent Store | 有 | 未检查 | 无 | 无 | 需修复 |
| /agents-store/[id] | 动态生成 | 动态生成 | 未检查 | 无 | 无 | 需修复 |
| /skills-store | YOLOX \| Skill Store | 有 | 未检查 | 无 | 无 | 需修复 |
| /skills-store/[id] | 动态生成 | 动态生成 | 未检查 | 无 | 无 | 需修复 |
| /teams-store | YOLOX \| Team Store | 有 | 未检查 | 无 | 无 | 需修复 |
| /teams-store/[id] | 动态生成 | 动态生成 | 未检查 | 无 | 无 | 需修复 |
| /appstore | 308 → /agents-store | 不适用 | 不适用 | 不适用 | 不适用 | 已改为永久重定向 |
| /login | YOLOX \| Sign In | 有 | 不适用 | 无 | 无 | 低优先 |
| /register | YOLOX \| Register | 有 | 不适用 | 无 | 无 | 低优先 |
| /privacy | YOLOX \| Privacy Policy | 有 | 未检查 | 无 | 无 | 正常 |
| /terms | YOLOX \| Terms of Service | 有 | 未检查 | 无 | 无 | 正常 |
| /client-home | YOLOX \| Workspace | 有 | 不适用 | 无 | 无 | 应设 noindex |
| /billing/* | 有 | 有 | 不适用 | 无 | 无 | 应设 noindex |

### 7.2 现有优势

- 所有页面均配置了 metadata（title 和 description）
- 动态详情页使用 `generateMetadata()` 生成元数据
- 支持多语言（en/zh），locale 处理正确
- `<html>` 标签动态设置 `lang` 属性
- 已集成 Google Analytics
- 首页使用了语义化的 `<section>` 元素
- 法律页面（privacy、terms）结构合理，配置了 revalidation

---

## 8. 修复 Todo List

> 修复完成后，使用 [SEO Audit Skill](https://skills.sh/coreyhaines31/marketingskills/seo-audit) 再次审计以验证修复效果。

### 重要程度说明

| 标签 | 含义 |
|------|------|
| **BLOCKER** | 不修复则搜索引擎基本无法正常收录，必须最先处理 |
| **CRITICAL** | 严重影响搜索排名或社交传播，应尽快修复 |
| **IMPORTANT** | 对 SEO 有明显提升，建议本周内完成 |
| **NICE-TO-HAVE** | 锦上添花，有余力时处理 |

### 修复清单

| # | 状态 | 任务 | 涉及文件 | 重要程度 | 优先级 | 说明 |
|---|------|------|----------|----------|--------|------|
| 1 | [x] | ~~**创建 sitemap.ts** — 生成 XML Sitemap，包含所有公开页面和动态详情页~~ | `src/app/sitemap.ts` | **BLOCKER** | P0 | ✅ 2026-04-20 核对：已实现，含 static + 动态 agents/skills/teams，用 `Promise.allSettled` 容错 |
| 2 | [x] | ~~**创建 robots.ts** — 配置爬虫规则，屏蔽 /api/、/client-home/、/billing/ 等路径~~ | `src/app/robots.ts` | **BLOCKER** | P0 | ✅ 2026-04-20 核对：已实现，额外加了 `/login`、`/register`、`/invite-code/`、`/waitlist/` |
| 3 | [~] | **添加 Open Graph / Twitter Card 元数据** — 根 layout 配置全局 OG 标签 | `src/app/layout.tsx` | **CRITICAL** | P0 | ⚠️ 2026-04-20 核对：字段已配（`layout.tsx:20-33`），但 `images` 指向 `/yolox_logo.svg`，Twitter/LinkedIn/微信多不渲染 SVG。需配合 #11 生成 PNG 才能真正生效 |
| 4 | [x] | ~~**设置 metadataBase** — 启用自动 canonical URL 生成~~ | `src/app/layout.tsx` | **CRITICAL** | P0 | ✅ 2026-04-20 核对：已实现，新建 `lib/site-url.ts` 工具，支持 `NEXT_PUBLIC_SITE_URL` 环境变量 |
| 5 | [x] | ~~**首页添加 H1 标签** — 将主标题从 `<h2>` 改为 `<h1>`~~ | `src/features/home/components/HomeLayout.tsx` | **CRITICAL** | P1 | ✅ 2026-04-20 核对：`HomeLayout.tsx:733` 已从 `<h2>` 改为 `<h1>`；944 行第二板块保持 `<h2>`（合理）|
| 6 | [x] | ~~**改进根 metadata description** — 将 "YOLOX homepage" 改为有意义的描述~~ | `src/app/layout.tsx` | **CRITICAL** | P1 | ✅ 2026-04-20 核对：`layout.tsx:10-11` 已换成完整描述 |
| 7 | [x] | ~~**使用 title template 模式** — 品牌名放到后面 `"%s \| YOLOX"`~~ | `src/app/layout.tsx` + 子页面 | **IMPORTANT** | P1 | ✅ 2026-04-20 核对：`layout.tsx:15-18` 已配置 `template: "%s \| YOLOX"` |
| 8 | [ ] | **修复首页图片 alt 属性** — 约 20 个 `<Image>` 的 alt 为空 | `src/features/home/components/HomeLayout.tsx` | **IMPORTANT** | P2 | ❌ 2026-04-20 核对：仍有 ~20 处 `alt=""`（52, 549, 567, 598, 626, 663, 671, 765, 818, 833, 846, 863, 878, 891, 915, 955, 963, 971, 1033, 1041, 1049 行）|
| 9 | [ ] | **为动态详情页添加 OG 元数据** — Agent/Skill/Team 详情页在 generateMetadata 中补充 OG | Agent/Skill/Team `[id]/page.tsx` | **IMPORTANT** | P2 | ❌ 2026-04-20 核对：`agents-store/[agentId]`、`skills-store/[skillId]`、`teams-store/[teamId]` 的 `generateMetadata()` 仍只有 title + description |
| 10 | [ ] | **添加 hreflang alternates 配置** — 关联 en/zh 页面 | `src/app/layout.tsx` | **IMPORTANT** | P2 | ❌ 2026-04-20 核对：全站 `alternates` / `hreflang` / `languages:` 零匹配 |
| 11 | [ ] | **设计并放置 OG 图片** — 1200x630 品牌图 | `public/og-image.png` | **IMPORTANT** | P2 | ❌ 2026-04-20 核对：`public/` 下无任何 PNG 文件，阻塞 #3 的真实效果 |
| 12 | [ ] | **添加 JSON-LD 结构化数据（首页）** — WebSite + Organization schema | `src/app/(pages)/home/page.tsx` 或 layout | **NICE-TO-HAVE** | P3 | ❌ 2026-04-20 核对：全站 `application/ld+json` 零匹配 |
| 13 | [ ] | **添加 JSON-LD 结构化数据（详情页）** — SoftwareApplication schema | Agent/Skill/Team `[id]/page.tsx` | **NICE-TO-HAVE** | P3 | ❌ 2026-04-20 核对：同上，零匹配 |
| 14 | [ ] | **评估 i18n URL 前缀方案** — 从 cookie 模式迁移到 `/en/`、`/zh/` 前缀 | 全站架构调整 | **NICE-TO-HAVE** | P3 | ❌ 2026-04-20 核对：仍是 cookie 模式（预期，大改动需评估）|
| 15 | [ ] | **为认证/账单页面添加 noindex** — /client-home、/billing/* | 对应 `page.tsx` | **NICE-TO-HAVE** | P3 | ❌ 2026-04-20 核对：`client-home/page.tsx`、`billing/success`、`billing/cancel` 的 metadata 未设置 `robots: { index: false }`；robots.txt 有 disallow，但缺少双保险 |
| 16 | [ ] | **创建 Web Manifest** — PWA 基础配置 | `public/manifest.json` | **NICE-TO-HAVE** | P3 | ❌ 2026-04-20 核对：不存在 |
| 17 | [ ] | **补充多尺寸 Favicon** — apple-touch-icon 等 | `public/` + `src/app/layout.tsx` | **NICE-TO-HAVE** | P3 | ❌ 2026-04-20 核对：`layout.tsx:34-36` 的 `icons.icon` 仍指向 `yolox_logo.svg`，无 apple 字段；`public/` 无 PNG |

### 建议修复顺序

```
第 1 周 (BLOCKER + CRITICAL):
  #1 sitemap.ts  →  #2 robots.ts  →  #4 metadataBase  →  #3 OG 标签
  →  #6 根 description  →  #5 H1 标签  →  #7 title template

第 2 周 (IMPORTANT):
  #8 图片 alt  →  #9 详情页 OG  →  #10 hreflang  →  #11 OG 图片

第 3 周+ (NICE-TO-HAVE):
  #12-17 按时间余量逐步推进
```

---

## 附录：涉及文件清单

| 文件 | 用途 |
|------|------|
| `src/app/layout.tsx` | 根 layout，全局 metadata 配置 |
| `src/app/(pages)/home/page.tsx` | 首页 metadata |
| `src/features/home/components/HomeLayout.tsx` | 首页内容和结构 |
| `src/app/(pages)/agents-store/page.tsx` | Agent 商店 metadata |
| `src/app/(pages)/agents-store/[agentId]/page.tsx` | Agent 详情页动态 metadata |
| `src/app/(pages)/skills-store/page.tsx` | Skills 商店 metadata |
| `src/app/(pages)/skills-store/[skillId]/page.tsx` | Skill 详情页动态 metadata |
| `src/app/(pages)/teams-store/page.tsx` | Teams 商店 metadata |
| `src/app/(pages)/teams-store/[teamId]/page.tsx` | Team 详情页动态 metadata |
| `next.config.mjs` | Next.js 配置 |
| `src/i18n/config.ts` | 国际化语言配置 |
| `messages/en.json` | 英文翻译文件 |
| `messages/zh.json` | 中文翻译文件 |
