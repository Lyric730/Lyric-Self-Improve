# Phase 14 云端真实持久化审查

日期：2026-05-27

## Findings

### P1：真实云环境尚未部署验证

云函数已经补真实写库逻辑，但本阶段验证仍是本地语法、正式文案、资产和微信开发者工具 preview。没有在真实云数据库中执行写入验证。

处理：完成 `docs/cloud-init-runbook.md` 后，用真实 owner 账号逐项调用 `saveConfig`、`updateTableDueTime`、`deductMemberPoints`、`voidAbnormalMatch`。

### P1：积分扣减暂未使用数据库事务

`deductMemberPoints` 会先查 `member_points`，再更新余额，再写 `points_ledger`。在同一会员被并发核销时，存在余额竞争风险。

处理：正式上线高并发前升级为云数据库事务；单店前台低频核销可先进入联调，但不能忽视。

### P1：员工端核销缺少会员 OpenID

服务端已经要求 `openid`，没有 OpenID 时返回 `MEMBER_OPENID_REQUIRED`。当前页面本地展示数据还没有真实会员 ID，因此默认核销会失败。

处理：后续必须补员工端会员搜索/扫码识别，传入真实 OpenID 后才能核销积分。

### P1：异常作废依赖真实 `matches` 文档

服务端现在按 `storeId + matchId` 查找比赛，找不到会返回 `MATCH_NOT_FOUND`。这符合上线要求，但当前本地异常列表的样例 ID 不会自动对应云数据库。

处理：后续异常列表读数据必须接云端 `matches`，不要继续用本地异常样例触发作废。

## Scope Check

本阶段新增或改动：

- `cloudfunctions/yunhanApi/index.js`
- `miniprogram/services/staff-service.js`
- `miniprogram/pages/staff-desk/staff-desk.js`
- `docs/cloud-database-schema.md`
- `docs/cloud-init-runbook.md`
- `docs/backend-integration-readiness-plan.md`
- `docs/dev-log.md`

没有改动球友端挑战流程可见页面。

## Requirement Check

- `admin.saveConfig` 写入 `admin_configs`。
- `staff.updateTableDueTime` 写入 `table_sessions`。
- `staff.deductMemberPoints` 扣减 `member_points`，并写入 `points_ledger`。
- `staff.voidAbnormalMatch` 按 `storeId + matchId` 校验后写入 `matches.status = voided`。
- `voidAbnormalMatch` 不再只按 `matchId` 直接更新，避免误改其他门店比赛。
- 云数据库 schema 已补 `member_points`、`table_sessions`、`admin_configs`。
- 初始化手册已补对应集合和索引。

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

结果：通过，包体 656.2 KB。

## Decision

Phase 14 可作为云端写库逻辑第一版归档。下一阶段建议补员工端真实会员搜索/扫码识别，解决积分核销缺少 OpenID 的问题。
