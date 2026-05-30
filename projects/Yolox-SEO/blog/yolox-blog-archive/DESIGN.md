# yolox-blog 数据源设计文档

## 1. 概述

`yolox-blog` 作为独立的博客内容仓库，为前端应用提供结构化的 Markdown 博客数据。采用**文件系统即数据库**的模式，每篇文章以目录为单位，co-locate 正文、封面和引用图片。

### 设计目标

- 前端应用通过 raw 文件 URL 直接消费内容，无需后端服务
- `manifest.json` 提供轻量列表索引，避免前端逐一解析 Markdown
- 目录结构即 slug，减少配置冗余
- 对 Git 友好，支持版本追踪和协作

## 2. 目录结构

```
yolox-blog/
  DESIGN.md
  manifest.json                          # 文章列表索引
  posts/
    skill-distillation-guide/            # slug = 目录名
      index.md                           # frontmatter + 正文
      cover.jpg                          # 封面图（可选）
      diagram1.png                       # 文章内引用图片
    future-of-user-experience/
      index.md
      cover.jpg
```

### 命名规范

| 项目 | 规则 | 示例 |
|------|------|------|
| 文章目录名 | kebab-case，即 slug | `skill-distillation-guide` |
| 正文文件 | 固定 `index.md` | - |
| 封面图 | 固定 `cover.jpg`、`cover.png` 或 `cover.svg` | - |
| 引用图片 | kebab-case，描述性命名 | `training-pipeline.png` |

## 3. manifest.json

只存元数据，不存正文。前端加载列表页时只需请求此文件。

### Schema

```jsonc
{
  "version": 1,
  "posts": [
    {
      "slug": "skill-distillation-guide",
      "title": "Skill Distillation Guide: ...",
      "description": "A hands-on guide...",
      "date": "2026-05-10",
      "author": "YOLOX Team",
      "tags": ["ai", "skills"],
      "draft": false,
      "order": 1,
      "coverImage": "posts/skill-distillation-guide/cover.jpg"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `slug` | string | 是 | 与目录名一致，用作路由标识 |
| `title` | string | 是 | 文章标题 |
| `description` | string | 是 | 摘要，用于列表卡片和 SEO |
| `date` | string | 是 | 发布日期，ISO 8601 格式 `YYYY-MM-DD` |
| `author` | string | 是 | 作者名 |
| `tags` | string[] | 是 | 标签数组，全小写 kebab-case |
| `draft` | boolean | 否 | 默认 `false`，`true` 时前端应过滤 |
| `order` | number | 否 | 自定义排序权重，数值越小越靠前。省略时按 `date` 降序排列 |
| `coverImage` | string | 否 | 封面图相对路径，无封面则省略 |

### 排序规则

前端排序优先级：`order`（升序） > `date`（降序）。

- 有 `order` 的文章始终排在无 `order` 的文章前面
- 多篇文章都有 `order` 时，按 `order` 值升序排列
- 无 `order` 的文章之间按 `date` 降序排列

`manifest.json` 中的 `posts` 数组也应遵循此排序规则。

## 4. index.md Frontmatter

```yaml
---
title: "Skill Distillation Guide: ..."
description: "A hands-on guide..."
date: "2026-05-10"
author: "YOLOX Team"
tags: ["ai", "skills"]
draft: false
---
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 与 manifest 保持一致 |
| `description` | string | 是 | 与 manifest 保持一致 |
| `date` | string | 是 | ISO 8601 `YYYY-MM-DD` |
| `author` | string | 是 | 作者名 |
| `tags` | string[] | 是 | 与 manifest 保持一致 |
| `draft` | boolean | 否 | 默认 `false` |

### 一致性约束

Frontmatter 与 `manifest.json` 中对应条目的 `title`、`description`、`date`、`author`、`tags`、`draft` 字段必须一致。`manifest.json` 是索引的唯一数据源，frontmatter 作为单篇文章的自描述备份。

## 5. Markdown 正文规范

### 图片引用

使用相对路径引用同目录下的图片：

```markdown
![Training pipeline](./training-pipeline.png)
```

前端渲染时需将相对路径转换为完整 URL（基于仓库 raw 地址）。

### 内容约定

- 标题从 `##` 开始（`#` 留给页面渲染的文章标题）
- 代码块标注语言以启用语法高亮
- 外部链接使用完整 URL

## 6. 前端消费方式

### 列表页

```
GET {raw-base}/manifest.json
```

解析 JSON，过滤 `draft !== true`，按 `order` 升序（优先）/ `date` 降序排列渲染卡片列表。封面图 URL 拼接：`{raw-base}/{coverImage}`。

### 详情页

```
GET {raw-base}/posts/{slug}/index.md
```

解析 frontmatter 获取元数据，渲染 Markdown 正文。正文中的相对图片路径转换为：`{raw-base}/posts/{slug}/{filename}`。

### URL 拼接示例

以 GitHub 为例，`raw-base` 为：

```
https://raw.githubusercontent.com/{owner}/yolox-blog/main
```

## 7. 维护流程

### 新增文章

1. 在 `posts/` 下创建 kebab-case 目录
2. 编写 `index.md`（含 frontmatter）
3. 放入封面图和引用图片
4. 在 `manifest.json` 的 `posts` 数组头部添加对应条目
5. 提交并推送

### 修改文章

1. 编辑 `index.md` 正文或图片
2. 若元数据变更，同步更新 `manifest.json`
3. 提交并推送

### 删除文章

1. 删除 `posts/` 下对应目录
2. 从 `manifest.json` 移除对应条目
3. 提交并推送
