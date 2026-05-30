# Growth Engine Pipeline SOP

等级：🟡 可用

来源项目：[projects/growth-engine-pipeline/README.md](../../../projects/growth-engine-pipeline/README.md)

## 目标

把 AI 领域信号变成可发布文章：采集信号、聚类选题、路由泳道、生成文章、配图、分发到账号。

## 使用前判断

| 检查项 | 标准 |
| --- | --- |
| 输入源 | 有 X / Podcast / 外部 source item |
| API | `ANTHROPIC_API_KEY`、`KIE_API_KEY` 已可用 |
| 发布账号 | 目标账号 profile 和发布队列清楚 |
| 审核方式 | 默认保留人工选题审核，不直接自动发布 |

## 标准流程

1. L0 信号采集：抓取 X/Twitter、Podcast 或已有 source items。
2. L1 主题引擎：过滤噪声、聚类、泳道路由、排序。
3. 人工审核：只放行值得写的 topic。
4. L2 文章生成：痛点提取、正文生成、质量门禁、修复循环。
5. L3 配图：按泳道生成封面和 inline 图。
6. L4 分发：组装队列，进入发布工具。
7. 复盘：记录命中 topic、失败原因、成本、发布结果。

## 常用命令

```bash
./run_pipeline.sh --source-dirs "path/to/source_items"
```

```bash
./run_pipeline.sh --source-dirs "path/to/sources" --skip-review --dry-run
```

```bash
./run_pipeline.sh --source-dirs "" --run-ingest
```

## 关键边界

- `runtime/` 是运行产物，不进 Obsidian 主索引。
- `configs/frameworks/` 是内容框架源头，改风格先改这里。
- 发布前必须确认账号、队列、图片授权和最终正文。
- `--skip-review` 只能用于 dry-run 或明确测试，不作为日常默认。

## 升级到 🔴 结实还要补

- 每轮运行自动生成成本和质量报告。
- 每个账号单独有发布 SOP。
- 将失败样本沉淀为门禁规则。
- 对 `runtime/` 建立轻量索引，而不是让 Obsidian 扫全部产物。

