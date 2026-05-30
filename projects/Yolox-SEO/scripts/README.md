# SEO 脚本说明

这个目录只集中归档 SEO 相关脚本，方便从项目包里直接找到自动化工具。

## `keyword-research-scripts/`

关键词研究脚本，主要用于：

- 从 seed keyword 构建候选池。
- 对候选词做过滤、分层、平衡和评分。
- 生成 KWFinder / GAKP 批量导入文件。
- 从 Reddit、Quora、Indie Hackers 等来源采集需求信号。
- 生成 pillar / cluster 和 keyword coverage。
- 渲染 Markdown 交付文档。

典型输入是 seed keyword、候选池 JSON、工具导出的 CSV、人工审核结果。典型输出是 scored master JSON、候选池 JSON、批量导入 CSV、Markdown 报告。

## `backlink-scripts/`

外链建设脚本，主要用于：

- 初始化和维护外链 SQLite 数据库。
- 导入项目候选表。
- 抓取或导入 Ahrefs 反链数据。
- 审计 profile / blog comment 机会。
- 批量跑候选站点检查。
- 汇总 226 资源池状态。

典型输入是候选站 CSV / XLSX、Ahrefs JSON、数据库文件。典型输出是更新后的数据库、review candidates CSV、状态报告和外链报告数据。

