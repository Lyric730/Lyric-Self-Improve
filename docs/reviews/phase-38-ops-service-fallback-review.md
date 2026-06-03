# Phase 38 运营服务层兜底测试与云接入清单审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

P2 残余风险：`scripts/test-ops-services.js` 验证的是微信开发者工具无云环境时的本地兜底，不等于真实云函数已经可用。明天云环境创建后，必须按 `docs/cloud-function-cutover-checklist.md` 做真云函数验证。

## Scope Check

本阶段新增测试和文档，不改页面结构：

- 新增 `scripts/test-ops-services.js`，覆盖运营服务层 DevTools 本地兜底。
- 新增 `docs/cloud-function-cutover-checklist.md`，固定云函数切换前置条件、必测接口、不能上线红线。
- 更新 `docs/api-service-layer-contract.md`，同步当前服务层真实状态。
- 更新执行计划和开发日志。

## Requirement Check

- 老板配置保存和读取有可复跑测试。
- 前台到点时间、积分核销、异常作废有可复跑测试。
- 会员码无云环境兜底有可复跑测试。
- 大屏读取老板端大屏配置有可复跑测试。
- 明天云环境工作有明确入口和验证清单。

## Verification Evidence

```powershell
node scripts\test-ops-services.js
```

结果：通过，输出 `Ops service fallback tests OK`。

```powershell
node scripts\test-settlement-engine.js
node scripts\test-admin-config-validator.js
node scripts\test-member-profile.js
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
node scripts\check-json-files.js
node scripts\check-production-copy.js
node scripts\check-player-flow-routes.js
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：全部通过。

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```

结果：通过，包体 `747.4 KB` / `765348` bytes。

## Decision

通过。Stage 8 已完成，下一阶段应进入云环境创建后的真实云函数部署和真机/扫码闭环验证。
