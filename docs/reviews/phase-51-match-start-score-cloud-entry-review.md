# Phase 51 开赛状态与计分事件接服务端入口审查
日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 已处理风险：计分页不再只靠本地变量开始比赛，进入页面会先通过 `match.start` 写入 `matches.status = playing`、`startedAt`、`startedAtMs` 和初始盘数。

P1 已处理风险：计分页加减盘不再只改页面状态，会通过 `match.recordScore` 写回 `matches.scoreA / scoreB`，并写入 `match_score_events`。

P1 已处理风险：`match.recordScore` 只允许本场发起方或挑战方操作，并且单次只允许 `+1 / -1`。

P1 已处理风险：盘数会被限制在 `0` 到 `targetWins` 之间，达到目标盘数后房间进入 `settlement_pending`。

P1 已处理风险：结算用时不再只信任页面 query。云函数结算 payload 会优先用 `matches.startedAtMs` 计算 `elapsedSeconds`。

P1 已处理风险：计分页在开赛同步失败时显示正式错误态和重试入口，不渲染内部说明或演示文案。

P2 残余风险：真实云环境尚未创建，`match.start`、`match.recordScore`、`match.previewSettlement`、`match.settle` 的连续链路还没有在真实集合权限和索引下验证。

P2 残余风险：当前 `match.recordScore` 不是事务写入。若 `matches` 分数更新成功但 `match_score_events` 写入失败，真实云环境需要补失败重试或一致性巡检。

P2 残余风险：双方同时快速点击加减盘时仍可能出现后写覆盖，真实上线前需要根据云数据库能力补条件更新或版本号。

## Scope Check

本阶段只处理开赛状态、计分事件和服务端计时入口，不改积分公式、不改段位规则、不改结算写入策略。

- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/README.md`
- `miniprogram/services/match-service.js`
- `miniprogram/pages/match-scoring/match-scoring.js`
- `miniprogram/pages/match-scoring/match-scoring.wxml`
- `miniprogram/pages/match-scoring/match-scoring.wxss`
- `docs/api-service-layer-contract.md`
- `docs/cloud-function-cutover-checklist.md`
- `docs/cloud-database-schema.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 云函数新增 `match.start`。
- `match.start` 要求房间已配置、双方到齐、玩法参数已确认。
- `match.start` 写入 `status = playing`、`startedAt`、`startedAtMs`、`scoreA`、`scoreB`。
- 云函数新增 `match.recordScore`。
- `match.recordScore` 只允许本场双方修改盘数。
- `match.recordScore` 将盘数限制在 `0` 到 `targetWins`。
- `match.recordScore` 写入 `match_score_events`。
- 达到目标盘数后状态变为 `settlement_pending`。
- 小程序新增 `match-service.startConfiguredMatch()` 和 `recordMatchScore()`。
- 计分页先通过服务层开赛，再允许点击计分按钮。
- 计分页加减盘通过服务层写入，不再本地自增自减。
- 计分页已用时间以服务端开赛时间为基准展示。
- DevTools 无云环境时保留本地兜底，正式环境失败会提示失败。

## Verification Evidence

最终验证命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

验证结果：

- `Ops service fallback tests OK`
- `Settlement engine tests OK`
- `Admin config validator tests OK`
- `Member profile tests OK`
- `Cloud contract tests OK`
- `Service layer boundary check OK`
- `JSON check OK (35 files checked)`
- `Production copy check OK (21 files checked)`
- `Player flow route check OK`
- `Edge check OK (32 PNG assets checked)`
- Mini-program JS syntax check 通过。
- Cloud function JS syntax check 通过。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`。
- 包体 `810.1 KB / 829564 bytes`。
- 最终输出 `Launch verification OK`。

## Decision

本阶段可提交。下一阶段建议继续处理真实后端闭环里的“结算后榜单 / 我的数据 / 积分账户读服务端”，把赛后展示从本地 `ladder-data.js` 迁出。
