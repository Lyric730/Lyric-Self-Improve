# yolox-blog

YOLOX 项目的博客内容仓库。作为前端应用的数据源，提供结构化的 Markdown 博客文章。

## 结构

```
manifest.json                  # 文章列表索引（元数据）
posts/
  {slug}/
    index.md                   # frontmatter + 正文
    cover.jpg                  # 封面图（可选）
    *.png                      # 文章引用图片
```

## 使用方式

前端通过 GitHub raw URL 直接消费：

```
# 获取文章列表
GET https://raw.githubusercontent.com/{owner}/yolox-blog/main/manifest.json

# 获取文章正文
GET https://raw.githubusercontent.com/{owner}/yolox-blog/main/posts/{slug}/index.md
```

## manifest.json 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `slug` | string | 是 | 文章目录名，用作路由 |
| `title` | string | 是 | 标题 |
| `description` | string | 是 | 摘要 |
| `date` | string | 是 | 发布日期 `YYYY-MM-DD` |
| `author` | string | 是 | 作者 |
| `tags` | string[] | 是 | 标签，小写 kebab-case |
| `draft` | boolean | 否 | 草稿标记，默认 `false` |
| `order` | number | 否 | 排序权重，越小越靠前 |
| `coverImage` | string | 否 | 封面图相对路径 |

### 排序规则

有 `order` 的文章按 `order` 升序排在前面，其余按 `date` 降序。

## 新增文章

1. 创建 `posts/{slug}/index.md`，填写 frontmatter：

```yaml
---
title: "文章标题"
description: "一句话摘要"
date: "2026-05-14"
author: "YOLOX Team"
tags: ["tag1", "tag2"]
---
```

2. 在 `manifest.json` 的 `posts` 数组中添加对应条目
3. 确保 frontmatter 与 manifest 中的元数据一致

## 验证

```bash
node scripts/validate.js
```

CI 会在 push 到 main 和 PR 修改 `manifest.json` 或 `posts/**` 时自动运行验证。

检查项包括：JSON 格式、必填字段、日期格式、slug 命名、标签格式、排序顺序、frontmatter 与 manifest 一致性、图片引用完整性。

## 详细设计

见 [DESIGN.md](./DESIGN.md)。
