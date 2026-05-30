# 看板与数据接入流程

目标：先把 SEO 执行信号接住，再谈优化。完成后应能回答索引是否建立、自然搜索是否产生曝光、外部分发是否带来 session、自然流量是否进入关键转化。

## 输入

- 网站域名和可验证权限。
- GA4 property 权限。
- sitemap 地址。
- 需要追踪的关键事件清单。
- 外部分发链接和渠道清单。

## 执行

1. 在 Google Search Console 建立或接入 property，优先复用已有 owner 权限，不重复验证。
2. 提交 sitemap，并确认状态为成功、发现 URL 大于 0。
3. 在 Bing Webmaster 通过 GSC import 建站点、复用验证并同步 sitemap。
4. 统一 GA4 事件命名，使用 snake_case，不传邮箱、姓名、电话、IP、地址、信用卡等 PII。
5. 把注册、agent 创建、购买等核心事件标记为 key event / conversion。
6. 所有站外分发链接使用 UTM，格式为 `utm_source`、`utm_medium`、`utm_campaign`，全部小写、短横线分隔。
7. 在 Looker Studio 固定搭 6 个模块：Organic Funnel、Acquisition by UTM Medium、Landing Page Performance、Top Queries from GSC、Event Count Trend、Purchase Revenue。

## 完成标准

- GSC property 和 sitemap 可截图证明。
- Bing import 成功。
- GA4 DebugView 或 Realtime 能看到关键事件。
- UTM 点击能在 GA4 Realtime 里看到来源。
- Looker 6 个模块都有正确数据源、维度、指标和过滤条件。

## 常见坑

- 新站 GSC 初始为空是正常现象，不要因为空就删看板。
- 站内链接不要加 UTM，否则会污染真实来源。
- 事件参数不要带 PII。

