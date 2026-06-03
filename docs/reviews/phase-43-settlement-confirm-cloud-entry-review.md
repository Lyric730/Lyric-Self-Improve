# Phase 43 结算确认按钮接入云函数入口审查

日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 残余风险：结算页预览、拒绝页和结果页仍使用本地结算展示。当前阶段只把“服了，确认结算”动作接到 `match-service.settleCurrentMatch()`，还没有完成全链路云端结算单读取。

P2 残余风险：本地占位比赛数据没有真实云端 `matches` 文档和双方 OpenID。微信开发者工具里会走本地兜底；真实云环境创建后必须用真实房间数据复测。

## Scope Check

本阶段只修改结算确认入口，不重构整套结算页面状态。

- `miniprogram/services/match-service.js`
- `miniprogram/pages/match-scoring/match-scoring.js`
- `miniprogram/pages/settlement/settlement.js`
- `miniprogram/pages/settlement/settlement.wxml`
- `docs/api-service-layer-contract.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 新增 `match-service.settleCurrentMatch()`，优先调用云函数 `match.settle`。
- 微信开发者工具预览环境允许云失败后本地兜底。
- 非 DevTools 环境下，云函数失败会抛出错误并由页面提示，不会静默本地结算。
- 结算确认按钮增加 loading / disabled，避免重复点击。
- 计分页跳结算页时开始透传 `matchId`。
- 原 `calculateSettlement()` 保留给当前结算预览使用。

## Verification Evidence

```powershell
node --check miniprogram\services\match-service.js
node --check miniprogram\pages\settlement\settlement.js
node --check miniprogram\pages\match-scoring\match-scoring.js
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

结果：统一验证通过，输出 `Launch verification OK`；微信预览包体以最终验证输出为准。

## Decision

通过，可提交。下一阶段应继续把结算结果页改为读取服务端结算单，或等待云环境创建后先做真实云端结算闭环测试。
