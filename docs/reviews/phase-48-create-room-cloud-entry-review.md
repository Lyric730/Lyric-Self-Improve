# Phase 48 发起挑战房间云端入口审查
日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 已处理风险：发起挑战不再只是前端跳转等待页，而是先通过服务层创建比赛房间，并把 `matchId` 透传到后续玩法、底分、确认、计分和结算链路。

P1 残余风险：对手加入动作仍未接云函数。本阶段只解决“开房”和“等待页读取”，还不能作为完整真实双人匹配闭环上线。

P2 残余风险：真实云环境尚未创建，`match.createRoom` / `match.get` 尚未在真实 `matches` 集合中验证权限、字段和索引。

## Scope Check

本阶段只处理发起挑战房间和 `matchId` 透传，不改玩法选择规则、不改计分规则、不改结算公式。

- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/README.md`
- `miniprogram/services/match-service.js`
- `miniprogram/pages/challenge-home/challenge-home.js`
- `miniprogram/pages/challenge-home/challenge-home.wxml`
- `miniprogram/pages/waiting-room/waiting-room.js`
- `miniprogram/pages/waiting-room/waiting-room.wxml`
- `miniprogram/pages/waiting-room/waiting-room.wxss`
- `miniprogram/pages/mode-select/mode-select.js`
- `miniprogram/pages/points-select/points-select.js`
- `miniprogram/pages/match-confirm/match-confirm.js`
- `miniprogram/pages/match-scoring/match-scoring.js`
- `docs/api-service-layer-contract.md`
- `docs/cloud-function-cutover-checklist.md`
- `docs/cloud-database-schema.md`
- `docs/cloud-init-runbook.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 云函数新增 `match.createRoom`。
- 云函数 `match.get` 可按 `matchId` 读取房间状态。
- 小程序新增 `match-service.createChallengeRoom()` 和 `getWaitingRoomState()`。
- 首页发起挑战按钮有 loading / disabled 防重复点击。
- 等待页支持读取中状态。
- `matchId` 透传到后续关键页面。
- DevTools 无云环境时保留本地房间预览。

## Verification Evidence

最终验证命令：

```powershell
node --check cloudfunctions\yunhanApi\index.js
node --check miniprogram\services\match-service.js
node --check miniprogram\pages\challenge-home\challenge-home.js
node --check miniprogram\pages\waiting-room\waiting-room.js
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

验证结果：

- `node --check` 快速语法检查通过。
- `node scripts\check-service-layer-boundary.js` 通过，输出 `Service layer boundary check OK`。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`，包体 `783.7 KB / 802497 bytes`。

## Decision

本阶段可提交。下一阶段建议补 `match.joinRoom`，让对手加入不再依赖本地演示刷新。
