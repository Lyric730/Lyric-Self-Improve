# Phase 31 正式路由与页面职责护栏审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

## Scope Check

本阶段只新增正式路由检查脚本、上线级逐页计划，并把新脚本加入标准验证命令。未修改用户可见页面。

## Requirement Check

- 已确认正式首页必须是 `pages/challenge-home/challenge-home`。
- 已确认 `pages/ui-kit/ui-kit` 不得进入正式 `app.json` 页面列表。
- 已确认 `app.json` 内所有正式页面必须具备 `.js / .json / .wxml / .wxss`。
- 已确认球友端主流程页面按递进顺序存在。
- 已确认底部 Tab 只允许出现在挑战首页、数据、排行榜、积分、我的等非比赛中页面。
- 已确认等待、接受、玩法选择、底分倍率、开局确认、计分、时间不足、结算、不服、结果页不放底部 Tab。

## Verification Evidence

```powershell
node scripts\check-player-flow-routes.js
```

结果：`Player flow route check OK`

```powershell
node --check scripts\check-player-flow-routes.js
```

结果：通过。

```powershell
git diff --check -- docs\superpowers\plans\2026-06-03-launch-grade-page-polish.md scripts\check-player-flow-routes.js docs\launch-readiness-execution-plan.md
```

结果：通过，仅有既有 CRLF 提示，无阻断错误。

## Decision

通过。Stage 1 已完成，可进入 Stage 2：挑战首页上线级打磨。
