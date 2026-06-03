# Phase 54 挑战首页开局检查服务化审查
日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 已处理风险：`challenge-home` 不再在模块加载时同步读取本地 `challengeGate`，页面进入后通过 `player-service.getChallengeHome()` 异步读取首页状态。

P1 已处理风险：`player-service.getChallengeHome()` 已改为云函数优先，正式环境云函数失败时会显示错误态；只有 DevTools 云不可用时才回落到本地视觉数据。

P1 已处理风险：云函数新增 `player.getChallengeHome`，返回当前会员身份、积分、段位和球桌开局检查。

P1 已处理风险：首页能否发起挑战不再依赖固定本地样例，而是以 `table_sessions` 中 active 球桌的到点时间作为第一版简单开台门槛。

P1 已处理风险：首页增加加载、失败和重试状态，云读取失败不会直接展示默认会员和默认球桌。

P2 残余风险：真实云环境尚未创建，`player.getChallengeHome` 还没有在真实 `store_members`、`member_points`、`table_sessions` 权限和索引下验证。

P2 残余风险：当前只使用“存在 active 球桌到点时间”作为简单开局门槛；地理位置 100 米校验还需要真机授权、定位误差和云端校验方案，不能在模拟器里假装已完成。

P2 残余风险：当前首页没有完整球桌选择器。若未来球桌二维码携带 `tableId`，页面已经预留 `tableId/tableNo` 参数读取路径，但仍需和真实二维码生成链路联调。

## Scope Check

本阶段只处理挑战首页的开局检查读取，不改比赛房间创建逻辑、不改员工端开台表单、不引入定位权限弹窗。

- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/README.md`
- `miniprogram/services/player-service.js`
- `miniprogram/pages/challenge-home/challenge-home.js`
- `miniprogram/pages/challenge-home/challenge-home.wxml`
- `docs/api-service-layer-contract.md`
- `docs/cloud-function-cutover-checklist.md`
- `docs/cloud-database-schema.md`
- `docs/cloud-init-runbook.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 新增云函数 `player.getChallengeHome`。
- `player.getChallengeHome` 返回当前会员身份、积分和段位。
- `player.getChallengeHome` 读取 active `table_sessions` 作为可开局门槛。
- 没有 active 球桌到点时间时，首页显示正式不可用状态。
- `player-service.getChallengeHome()` 改为云函数优先。
- `challenge-home` 增加加载、失败和重试状态。
- 文档补充 `table_sessions` active status 查询索引。

## Verification Evidence

最终验证命令：

```powershell
git diff --check
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
- 包体 `831.1 KB / 851002 bytes`。
- 最终输出 `Launch verification OK`。

## Decision

本阶段可提交。下一阶段建议处理 `mode-select` / `points-select` 的玩法配置读取，让玩法、底分和倍率选择也从云端老板配置读取。
