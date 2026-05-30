# Blog 内容生产流程

目标：把关键词机会变成可索引、可引用、可转化的页面。

## 输入

- 关键词研究交付的 L6 outline。
- 证据池：case、数据、quote、官方文档或一手研究链接。
- Blog 模板、frontmatter 规范和 manifest 规范。

## 执行

1. 写正文前先补齐 brief：关键词、读者、文章类型、SERP 差异化角度、证据池、链接、SEO 字段。
2. 按搜索意图选文章类型：list、step-by-step、expanded definition、beginner guide、comparison、contrarian、buyer guide。
3. 正文采用 answer-first：开头明确回答，TL;DR 可单独引用。
4. 每个 H2 至少有一个证据、判断或可执行步骤。
5. 做三类链接：同 silo 内链、产品链接、权威外链。
6. 产品露出保持自然：开头点场景，中段嵌入步骤，结尾给 CTA，不在每个 H2 硬塞产品。
7. 发布到 `posts/{slug}/index.md`，更新 `manifest.json`，运行校验脚本。

## 完成标准

- frontmatter 和 manifest 字段一致。
- title、description、slug、tags、schema 清晰且无 TBD。
- 外链和内链都是真实可访问 URL。
- 图片有合理 alt。
- 校验脚本通过。

## 常见坑

- 证据池没补齐就写正文，文章会空泛。
- 不要所有文章都写成“终极指南”。
- URL 不要凭空编。

