# 外链建设流程

目标：用低成本、可验证的提交方式获取公开页面上的有效链接。外链 KPI 只统计 `status = live` 且 `rel_actual = dofollow` 的记录。

## 输入

- 候选站点清单。
- 外链数据库或表格。
- 提交材料：产品名、描述、官网 URL、分类、logo / 截图、联系人信息。
- 状态文档。

## 执行

1. 候选站点先问五个问题：能否自助提交、能否自然放官网链接、链接是否公开、能否从 HTML 验证 rel、单条处理成本是否足够低。
2. 优先处理 directory、showcase、GitHub awesome list、profile/signup 公开 website 字段、少量人工筛出的 blog comment / URL field 机会。
3. 提交前查数据库和状态文档，避免重复提交。
4. 根据入口类型准备材料：form、GitHub PR、profile field、showcase request、directory submit。
5. 提交后记录为 `submitted` 或 `pending`。
6. 等公开页面可访问后，只用 public HTML 验证链接和 rel。
7. 根据验证结果更新为 `live`、`rejected`、`failed`、`skipped` 或继续 `pending`。

## 状态字段

每条记录至少保留：source site、target URL、submission type、submitted URL、status、rel expected、rel actual、evidence URL、notes。

推荐状态值：`candidate`、`submitted`、`pending`、`live`、`rejected`、`failed`、`skipped`。

## 常见坑

- `nofollow`、`ugc`、`sponsored` 可以记录，但不算 dofollow KPI。
- `rel="me"` 记为 `me_no_pagerank`，不算 SEO dofollow。
- 后台预览、个人资料编辑页、提交成功提示都不能算 live。
- 不要在没有 URL 字段的评论正文里硬塞链接。

