# digest 产线说明

`digest` 是 AI 日报 9 图图文产线，核心目标是把 AI 热点做成小红书可发布的图文包。

## 当前状态

🟡 可用：历史上已经跑通过抓取、撰写、渲染、截图、生成 post 和 README。当前主线已经转到《三分钟未来》，但 digest 仍保留为可参考产线。

## 关键文件

| 文件 | 用途 |
|---|---|
| `PLAN.md` | 产线规划和历史 sprint 拆解 |
| `REVIEW_CHECKLIST.md` | 发布前人工审核清单 |
| `.impeccable.md` | digest 专属视觉 brief |
| `run.py` | 机械步骤总控 |
| `scheduled_daily.sh` | Windows 任务到 WSL 的自动入口 |
| `templates/` | HTML / post 模板 |
| `schemas/enriched.py` | enriched 数据结构 |
| `archive/` | 历史定位和设计文档 |

## 常用命令

只重渲染已有 `final.json`：

```powershell
python lines\digest\run.py <YYYY-MM-DD> --only-render
```

完整跑链路前先确认当天输入、外部接口和通知配置，不要在没确认的情况下直接触发自动发布。

## 和其他目录的关系

- 源头脚本、模板、视觉 brief：`lines/digest/`
- 每日发布包：`daily/<date>/digest/publish/`
- 每日中间产物：`daily/<date>/digest/work/`
- 跨产线结构说明：`docs/PROJECT_STRUCTURE.md`
