# Phase 49 接受挑战加入房间云端入口审查
日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 已处理风险：接受挑战不再直接前端跳转玩法页，而是先通过服务层调用 `match.joinRoom`，写入 `matches.guestOpenid` 后再继续。

P1 已处理风险：加入房间从普通 `get -> update` 改为条件更新，只有 `guestOpenid` 仍为空时才写入，降低两个对手同时扫码导致后写覆盖的风险。

P1 已处理风险：云函数 `formatRoomState()` 在对手未加入时不再返回空 `guest` 对象，避免接受页把空对象当挑战方显示。

P1 已处理风险：接受页读取真实房间失败时不再渲染空数据页面，改为正式错误态和返回首页动作。

P2 残余风险：真实云环境尚未创建，`match.joinRoom` 尚未在真实 `matches` 集合中验证权限、条件更新结果和重复扫码路径。

P2 残余风险：房间二维码 / 邀请链接生成链路尚未接入，本阶段只处理接受页拿到 `matchId` 后的加入动作。

## Scope Check

本阶段只处理接受挑战加入房间，不改玩法规则、计分规则、结算公式和大屏榜单。

- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/README.md`
- `miniprogram/services/match-service.js`
- `miniprogram/pages/accept-challenge/accept-challenge.js`
- `miniprogram/pages/accept-challenge/accept-challenge.wxml`
- `miniprogram/pages/accept-challenge/accept-challenge.wxss`
- `docs/api-service-layer-contract.md`
- `docs/cloud-function-cutover-checklist.md`
- `docs/cloud-database-schema.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 云函数新增 `match.joinRoom`。
- `match.joinRoom` 会写入挑战方 OpenID，并把房间状态改为 `joined`。
- `match.joinRoom` 拒绝房主加入自己发起的房间。
- `match.joinRoom` 拒绝第三人加入已占用房间。
- `match.joinRoom` 拒绝不存在或已关闭的房间。
- 小程序新增 `match-service.joinChallengeRoom()`。
- 接受挑战页按 `matchId` 读取房间，并在接受时通过服务层加入。
- 接受成功后带 `matchId` 进入玩法选择。
- DevTools 无云环境时保留本地预览兜底。

## Verification Evidence

最终验证命令：

```powershell
node --check cloudfunctions\yunhanApi\index.js
node --check miniprogram\services\match-service.js
node --check miniprogram\pages\accept-challenge\accept-challenge.js
node scripts\check-production-copy.js
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

验证结果：

- `node --check` 快速语法检查通过。
- `node scripts\check-production-copy.js` 通过，输出 `Production copy check OK (21 files checked)`。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`，包体 `792.0 KB / 811001 bytes`。

## Decision

本阶段可提交。下一阶段建议补房间配置状态机，把玩法、底分、倍率写回 `matches`，避免后续计分页仍主要依赖 query 参数。
