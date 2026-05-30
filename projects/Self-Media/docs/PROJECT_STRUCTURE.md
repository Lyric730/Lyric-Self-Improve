# Self-Media 项目结构

更新时间：2026-05-28

## 总原则

这个项目按“内容生产线”组织。每条产线自己带代码、模板、视觉规则、运行手册和验收规则；每日输出只落在 `daily/`，不反向污染源头。

## 根目录

| 路径 | 职责 | 注意 |
|---|---|---|
| `README.md` | 项目入口，给人和 Agent 快速定位 | 新人先读 |
| `AGENTS.md` | Agent 工作规则 | Codex 优先识别 |
| `AGENT.md` | 兼容入口 | 只指向 `AGENTS.md` |
| `CLAUDE.md` | 项目宪法、定位、历史设计上下文 | 保留高层原则，不塞单期细节 |
| `.claude/commands/` | Claude 项目级 slash commands | 命令名应和产线名一致 |

## `lines/`

可复用生产线都放这里。

```text
lines/
├── README.md
├── digest/
└── three-minute-future/
```

| 产线 | 当前定位 | 关键入口 |
|---|---|---|
| `digest` | AI 日报 9 图图文，历史主线 | `lines/digest/README.md` |
| `three-minute-future` | 《三分钟未来》图文 + 视频，当前主线 | `lines/three-minute-future/README.md` |

规则：

- 新产线必须新建 `lines/<new-name>/`。
- 不复用旧产线的视觉 brief、模板、字体、色彩和口吻，除非用户明确要求。
- 可复用脚本、模板、样式、配置、文档必须改在 `lines/<line-name>/`，不要只改 `daily/`。

## `daily/`

每日运行结果都放这里。

```text
daily/
├── README.md
├── _state/
├── 2026-05-12/
├── 2026-05-14/
└── ...
```

典型结构：

```text
daily/<YYYY-MM-DD>/<line-name>/
├── work/       中间产物，例如 candidates、selection、final、video input
└── publish/    发布包，例如 HTML、PNG、post、video
```

规则：

- `publish/` 是能直接发布或验收的结果。
- `work/` 是中间文件，可以辅助排查，但不能当成长期文档入口。
- `_state/` 是跨日期运行状态，例如已发布账本，不能随手清空。

## `docs/`

跨产线文档放这里。

```text
docs/
├── README.md
├── PROJECT_STRUCTURE.md
├── handoffs/
├── proposals/
├── archive/
└── superpowers/
```

规则：

- 交接放 `docs/handoffs/`。
- 还没执行或只是设计建议的方案放 `docs/proposals/`。
- 已完成、废弃或只留历史原因的内容放 `docs/archive/`。
- 某条产线的常用操作不要放这里，放回该产线目录。

## `topics/`

未产线化选题素材放这里。

规则：

- 单篇深度、长图文草案、选题事实包放 `topics/`。
- 一旦某类选题开始重复生产，应升级成 `lines/<new-name>/`。
- 不要把完整生产脚本塞进 `topics/`。

## 判断一个文件该放哪

| 文件类型 | 应放位置 |
|---|---|
| 可复用脚本 | `lines/<line-name>/` |
| 可复用模板 / 样式 / 配置 | `lines/<line-name>/` |
| 单期 HTML / PNG / MP4 | `daily/<date>/<line-name>/publish/` |
| 单期 raw / enriched / final / TTS input | `daily/<date>/<line-name>/work/` |
| 阶段交接 | `docs/handoffs/` |
| 改版方案 | `docs/proposals/` |
| 过期方案 / 废弃设计 | `docs/archive/` |
| 单篇选题素材 | `topics/` |
