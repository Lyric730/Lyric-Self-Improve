# Phase 13 员工端与老板端写操作接入云函数审查

日期：2026-05-27

## Findings

### P1：真实云环境未初始化时，写操作会返回云端不可用或权限失败

员工端和老板端写操作已经切到 `callCloud`。如果还没有按 `docs/cloud-init-runbook.md` 初始化云环境、部署云函数、写入 owner，保存动作会失败并展示失败 toast。

处理：这是正确行为，不能回退到本地伪成功。真实联调前必须完成 Phase 12 手册。

### P1：员工积分核销仍缺少稳定用户 ID

当前核销 payload 仍使用 `userName`，这是因为第一版本地数据里还没有会员 OpenID 或 memberId。正式接积分流水前，员工核销必须改为传稳定用户 ID。

处理：后续接会员搜索和 `points_ledger` 时补 `openid` 或 `memberId`。

### P1：老板配置写操作已传完整配置，但云端尚未持久化

`admin-service` 已把完整 `config` 发给云函数；但 `yunhanApi` 目前只做权限校验和操作日志，没有写入 `admin_configs`。

处理：后续 Phase 补 `admin_configs` 集合和真实保存逻辑。

## Scope Check

本阶段新增或改动：

- `miniprogram/services/staff-service.js`
- `miniprogram/services/admin-service.js`
- `miniprogram/pages/staff-desk/staff-desk.js`
- `miniprogram/pages/staff-desk/staff-desk.wxml`
- `miniprogram/pages/boss-config/boss-config.js`
- `miniprogram/pages/boss-config/boss-config.wxml`
- `docs/api-service-layer-contract.md`
- `docs/backend-integration-readiness-plan.md`
- `docs/dev-log.md`

没有改动球友端挑战流程可见页面。

## Requirement Check

- 员工保存到点时间已通过 `callCloud("staff", "updateTableDueTime")`。
- 员工积分核销已通过 `callCloud("staff", "deductMemberPoints")`。
- 员工异常作废已通过 `callCloud("staff", "voidAbnormalMatch")`。
- 老板保存配置已通过 `callCloud("admin", "saveConfig")`。
- 页面按钮增加 loading，避免重复提交。
- 页面不展示内部校验、演示状态、mock、调试或临时说明。
- 页面仍不直接引用 `ladder-data` 或 `operation-log`。
- service 层不再使用本地 `operation-log` 伪造运营留痕。

## Verification Evidence

```powershell
rg -n "ladder-data|operation-log" miniprogram\pages --glob "*.js"
```

结果：无命中。

```powershell
rg -n "operation-log|recordOperation" miniprogram\services --glob "*.js"
```

结果：无命中。

```powershell
node --check cloudfunctions\yunhanApi\index.js
```

结果：通过。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过，共 37 个 JS 文件。

```powershell
node scripts\check-json-files.js
```

结果：通过，共 32 个 JSON 文件。

```powershell
node scripts\check-production-copy.js
```

结果：通过，共 19 个正式页面文件。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：通过，共 32 个 PNG 资产。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 656.1 KB。

## Decision

Phase 13 可作为运营端写操作接入云函数阶段归档。下一阶段建议补云端真实持久化：`admin_configs`、员工到点时间、积分核销流水和异常作废状态。
