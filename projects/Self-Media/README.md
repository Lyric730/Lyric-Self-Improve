# Self-Media 项目入口

小刀老师，这是自媒体内容生产项目，不是单一代码工程。核心结构是：`lines/` 放可复用生产线，`daily/` 放每日产物，`docs/` 放可交接文档，`topics/` 放还没变成产线的选题素材。

## 先看哪几个文件

| 场景 | 先读 |
|---|---|
| 第一次进入项目 | `README.md`、`AGENTS.md`、`CLAUDE.md` |
| 想看整体目录框架 | `docs/PROJECT_STRUCTURE.md` |
| 要做《三分钟未来》 | `lines/three-minute-future/README.md` |
| 要做 AI 日报 digest | `lines/digest/README.md` |
| 要找历史交接、方案、归档 | `docs/README.md` |
| 要找某天发布结果 | `daily/README.md` |
| 要找未产线化选题 | `topics/README.md` |

## 当前目录分层

```text
Self-Media/
├── README.md                     项目入口，给人和 Agent 快速定位
├── AGENTS.md                     Agent 工作规则，Codex 优先识别
├── AGENT.md                      兼容入口，指向 AGENTS.md
├── CLAUDE.md                     项目宪法，保留历史决策和设计上下文
├── docs/                         可交接文档：结构、方案、交接、归档
├── lines/                        可复用内容生产线
├── daily/                        按日期落盘的每日产物和中间文件
├── topics/                       单篇选题素材，未必可复用
└── .claude/commands/             Claude 项目级 slash commands
```

## 两条主产线

| 产线 | 目录 | 当前用途 | 状态 |
|---|---|---|---|
| digest | `lines/digest/` | AI 日报 9 图图文生产 | 历史可用产线 |
| three-minute-future | `lines/three-minute-future/` | 《三分钟未来》图文 + 视频生产 | 当前主线 |

## 目录边界

- 可复用脚本、模板、样式、规则：只放 `lines/<line-name>/`。
- 某一天的运行结果、发布包、视频、临时素材：只放 `daily/<YYYY-MM-DD>/<line-name>/`。
- 方案、交接、结构说明、归档：放 `docs/`。
- 单篇选题素材：放 `topics/`。
- 不要把 `daily/` 里的临时修补当成源头改动；下一期不会自动继承。

## 常用入口命令

《三分钟未来》常规图文流程：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL>
```

《三分钟未来》先停在选题审核：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL> --stop-after select
```

《三分钟未来》本地预览：

```powershell
python lines\three-minute-future\serve_preview.py <publishDate> --port 58419
```

digest 只重渲染已有内容：

```powershell
python lines\digest\run.py <YYYY-MM-DD> --only-render
```

## 当前交付等级

🟡 可用：这个整理停在“日常能看懂、能继续跑”的文档等级。还不是 🔴 生产级知识库，升级路径是给每条产线补自动化自检和每期发布后的固定复盘模板。
