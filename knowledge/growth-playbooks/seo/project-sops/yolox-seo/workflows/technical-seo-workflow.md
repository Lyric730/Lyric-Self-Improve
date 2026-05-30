# 技术 SEO 修补流程

目标：让页面能被抓取、理解、展示和分享。不要堆工具分数，一次只修一个明确问题。

## 输入

- 技术 SEO audit 报告。
- 网站代码仓库。
- sitemap、robots、metadata、schema、页面 HTML 的当前输出。

## 执行

1. 从 audit report 选择一个具体问题，定位到代码文件。
2. 检查抓取和索引：sitemap 是否包含公开页面，robots 是否误挡核心页面，auth / billing / account 类页面是否避免索引，canonical 是否明确。
3. 检查 metadata：首页 title / description、title template、动态详情页 `generateMetadata`、唯一 H1。
4. 检查 OG / Twitter Card：主图用 1200 x 630 PNG，不用 SVG 当主要 OG image。
5. 检查图片 alt：装饰图可空，传递信息的图必须有描述，不堆关键词。
6. 检查 JSON-LD：主页 Organization / WebSite，Blog Article / BlogPosting，FAQ 用 FAQPage，How-to 用 HowTo。
7. 如果有多语言版本，再检查 hreflang；没有多语言内容不要硬加。
8. 修完后用页面 HTML、搜索引擎工具或 schema validator 验证，并同步 audit 状态。

## 完成标准

- 代码里能定位到改动。
- 本地或线上页面能看到输出结果。
- sitemap / robots / metadata / schema 符合预期。
- 对应验证工具无明显错误。
- audit 文档状态已同步。

