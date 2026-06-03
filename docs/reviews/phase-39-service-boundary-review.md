# Phase 39 页面服务层依赖护栏审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

## Scope Check

本阶段只新增自动检查脚本和文档，不修改小程序页面行为。

- 新增 `scripts/check-service-layer-boundary.js`。
- 更新执行计划和接口层契约。

## Requirement Check

- 正式页面不能直接读取 `miniprogram/utils/ladder-data.js`。
- 正式页面不能直接写 `operation-log`。
- 正式页面不能直接引用 `settlement-engine` 计算结算。
- 当前 `miniprogram/pages/**/*.js` 全部通过该检查。

## Verification Evidence

```powershell
node scripts\check-service-layer-boundary.js
```

结果：通过，输出 `Service layer boundary check OK`。

```powershell
node scripts\test-ops-services.js
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

通过。后续新增页面或接口时，标准验证必须包含该脚本。
