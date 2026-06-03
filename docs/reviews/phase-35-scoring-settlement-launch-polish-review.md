# Phase 35 计分、时间不足、结算链路上线化审查

日期：2026-06-03

## Findings

P1 已修：计分页原先依赖页面 `setInterval` 累加时间。用户进入“时间不足”页再返回计分页时，停留在提示页的时间不会计入比赛用时，可能导致实际已满最低时间但页面仍显示未满足。本轮改为根据比赛开始时间 `matchStartedAt` 计算已用时。

P2 已修：快速连点盘数 `+` 可能重复触发结算 / 时间不足跳转。本轮增加 `settlementLocked`，防止重复跳页；从时间不足页返回后自动解锁。

## Scope Check

本阶段只修改 `match-scoring.js` 并更新计划、审查和开发日志。结算引擎、结算页展示、不服页、结果页未做无必要改动。

## Requirement Check

- 正向计时从 `00:00:01` 开始。
- 已用时间按比赛开始时间计算，离开计分页后返回仍会继续累计。
- 任一方达到目标盘数后，先检查最低有效时间。
- 未满最低有效时间时进入时间不足页，不进入结算。
- 结算页现有展示继续使用风险积分、随机奖励、加星和双方积分变化。
- 不服页继续只提供退出本场不结算、再战一场两条路径。

## Verification Evidence

```powershell
node scripts\test-settlement-engine.js
```

结果：`Settlement engine tests OK`

```powershell
node --check miniprogram\pages\match-scoring\match-scoring.js
node --check miniprogram\pages\time-insufficient\time-insufficient.js
node --check miniprogram\pages\settlement\settlement.js
node --check miniprogram\pages\refusal\refusal.js
node --check miniprogram\pages\match-result\match-result.js
```

结果：通过。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
node scripts\check-json-files.js
node scripts\check-production-copy.js
node scripts\check-player-flow-routes.js
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：全部通过。

```powershell
git diff --check -- miniprogram\pages\match-scoring\match-scoring.js
```

结果：通过，仅有既有 CRLF 提示，无阻断错误。

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```

结果：通过，包体 `740.3 KB` / `758050` bytes。

## Decision

通过。Stage 5 已完成，可进入 Stage 6：个人数据、排行榜、积分礼遇上线化。
