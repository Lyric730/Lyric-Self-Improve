# Phase 53 小程序大屏榜单数据服务化审查
日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 已处理风险：`screen-service` 不再只从本地 `ladder-data.js` 读取电视榜单，已改为优先调用云函数 `screen.getBoard`。

P1 已处理风险：`screen.getBoard` 返回店内总榜、前三名、赏金猎人和老板端大屏配置，正式环境不再需要用本地样例榜单撑大屏页面。

P1 已处理风险：小程序内大屏支持 `staff` / `owner` / `screen` 角色访问；浏览器静态大屏保留 `screenToken` 校验路径。

P1 已处理风险：赏金猎人不再是固定样例，云函数会从已结算比赛的胜方积分变化中聚合赢分榜。

P1 已处理风险：`tv-ranking` 页面改为异步读取，增加加载、失败、重试和空榜状态，云读取失败时不会继续静默展示旧榜单。

P2 残余风险：真实云环境尚未创建，`screen.getBoard` 还没有在真实 `member_points`、`settlements`、`admin_configs`、`screen_tokens` 权限和索引下验证。

P2 残余风险：赏金猎人当前扫描最近 120 条已结算记录后聚合，适合第一版大屏；正式运营后建议增加按周期的榜单快照集合，避免数据量变大后实时聚合拖慢大屏刷新。

P2 残余风险：`screen/yunhan-tv-ranking.html` 这类电视浏览器静态网页还没有 HTTP 化接口，本阶段只处理小程序内大屏页和云函数读入口。

## Scope Check

本阶段只处理小程序内电视大屏页的数据读取链路，不改大屏视觉主布局、不改老板端配置表单、不引入新的 HTTP 服务。

- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/README.md`
- `miniprogram/services/screen-service.js`
- `miniprogram/pages/tv-ranking/tv-ranking.js`
- `miniprogram/pages/tv-ranking/tv-ranking.wxml`
- `miniprogram/pages/tv-ranking/tv-ranking.wxss`
- `scripts/test-ops-services.js`
- `docs/api-service-layer-contract.md`
- `docs/cloud-function-cutover-checklist.md`
- `docs/cloud-database-schema.md`
- `docs/cloud-init-runbook.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 新增云函数 `screen.getBoard`。
- `screen.getBoard` 支持小程序内角色访问。
- `screen.getBoard` 支持 `screenToken` 访问路径。
- 店内总榜从 `member_points.balance` 降序读取。
- 赏金猎人从 `settlements.pointChanges` 聚合胜方赢分。
- 大屏标题、刷新文案从 `admin_configs.config.screen` 读取。
- `screen-service.getScreenBoard()` 改为异步云函数优先。
- `tv-ranking` 增加正式加载、失败、重试和空榜状态。
- 文档补充 `screen_tokens` token 索引要求。

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
- 包体 `827.1 KB / 846943 bytes`。
- 最终输出 `Launch verification OK`。

## Decision

本阶段可提交。下一阶段建议处理首页非比赛入口数据，尤其是 `challenge-home` 的开局检查和球桌状态读取。
