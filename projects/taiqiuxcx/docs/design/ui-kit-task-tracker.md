# 云瀚 UI Kit 还原任务台账

状态：执行中
更新规则：每完成一项，就把该项从“当前任务队列”移动到“已完成归档”，并同步 `docs/dev-log.md`。

## 当前任务队列

| ID | 任务 | 状态 | 验收标准 |
| --- | --- | --- | --- |
| UI-04 | 微信开发者工具对照验收 | 进行中 | CLI 预览可打开；逐个组件对照设计图记录问题 |
| UI-06 | 球友端视觉二轮精修 | 待做 | 基于 UI-04 截图结论，继续扣按钮、玩法卡、奖励、结算、排行榜细节 |

## 已完成归档

| ID | 任务 | 完成时间 | 归档说明 |
| --- | --- | --- | --- |
| UI-01 | 建立正式抠图流水线 | 2026-05-27 | 新增 `scripts/extract-ui-kit-assets.ps1`，从第 08 张资产板生成 32 个 PNG、黑底预览、棋盘格预览；`scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过 |
| UI-02 | 资产组件第一批 | 2026-05-27 | 新增 `RankBadge`、`StarTrack`、`RewardCrate`、`SettlementBadge`、`VictoryBanner`、`AcceptStamp`；接入 `pages/ui-kit`；微信 CLI preview 通过 |
| UI-03 | UI Kit 组件验收台 | 2026-05-27 | 重构 `pages/ui-kit` 为验收台结构：顶部阶段轨道、按钮状态矩阵、玩法卡片分层、美术资产状态区；微信 CLI preview 通过 |
| UI-05 | 球友端页面组装 | 2026-05-27 | 新增 `pages/player`，把玩法选择、底分倍率、比赛计分、结算确认、排行榜串成球友端首屏；微信 CLI preview 通过，包体 `584.5 KB`。后续已判定该方向不符合 PRD 的多页面递进流程，只保留为错误记录，不再作为业务入口 |
| UI-07 | 球友端多页面流程重构 | 2026-05-27 | 新增 `challenge-home`、`waiting-room`、`accept-challenge`、`mode-select`、`points-select`、`match-confirm`、`match-scoring`、`time-insufficient`、`settlement`、`refusal`、`match-result`、`my-data`、`rankings`、`points-perks`；`challenge-home` 作为首屏；微信 CLI preview 和自动化路由验证通过 |

## 执行原则

- 不先做完整页面，先把 UI Kit 组件和美术资产扣准。
- 每个组件必须说明对应哪张设计图、哪个区域。
- 复杂美术资源必须来自 `miniprogram/assets/ui-kit/`，不使用 CSS 临时硬画。
- 完成一项后必须归档，不让任务状态只停留在聊天记录里。
