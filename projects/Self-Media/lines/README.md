# lines 目录说明

`lines/` 是可复用内容生产线层。每条产线是一个独立目录，自己管理脚本、模板、样式、配置、视觉 brief、运行手册和验收规则。

## 当前产线

| 产线 | 目录 | 状态 | 入口 |
|---|---|---|---|
| AI 日报 digest | `lines/digest/` | 历史可用 | `lines/digest/README.md` |
| 三分钟未来 | `lines/three-minute-future/` | 当前主线 | `lines/three-minute-future/README.md` |

## 放置规则

- 能被下一期复用的东西放 `lines/<line-name>/`。
- 只属于某一天的输出放 `daily/<date>/<line-name>/`。
- 新产线不要继承旧产线视觉和口吻，除非小刀老师明确要求。
- 产线文档先在本目录内闭环，再把跨产线结论同步到根 `README.md` 或 `docs/PROJECT_STRUCTURE.md`。
