# Phase 11 云数据库集合与服务端权限审查

日期：2026-05-27

## Findings

### P1：云数据库集合尚未在微信云开发环境中创建

已新增 `docs/cloud-database-schema.md`，但集合和索引还没有在微信开发者工具云开发面板中实际创建。正式启用云函数前，必须创建 `store_members`、`operation_logs`、`matches`、`points_ledger` 等集合。

处理：下一阶段需要在微信开发者工具中开通云环境并建集合。

### P1：服务端权限已按 `store_members` 设计，但缺少首个 owner 账号初始化

云函数现在会按 `storeId + openid + status=active` 查角色；没有记录时按 `player`。这符合安全默认值，但也意味着必须先给老板 OpenID 写入 `owner` 记录，否则老板端云函数会被拒绝。

处理：下一阶段补初始化脚本或后台录入流程。

### P1：服务端结算仍未实现

本阶段只处理云数据库 schema 和服务端角色判断；`match.settle` 仍未启用。

处理：后续 Phase 继续做服务端结算。

## Scope Check

本阶段新增或改动：

- `cloudfunctions/yunhanApi/index.js`
- `docs/cloud-database-schema.md`
- `docs/backend-integration-readiness-plan.md`

没有改动小程序可见页面。

## Requirement Check

- 已定义第一批云数据库集合。
- 已定义 `store_members` 字段和角色规则。
- 已定义 `operation_logs` 字段。
- 已定义 `matches` 状态字段。
- 已定义 `points_ledger` 字段。
- 云函数权限不再使用固定 TODO 角色。
- `staff` 模块要求员工或老板。
- `admin` 模块要求老板。
- 无成员记录时按普通球友处理。

## Verification Evidence

```powershell
node --check cloudfunctions\yunhanApi\index.js
```

结果：通过。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过。

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

结果：通过，包体 642.2 KB。

## Decision

Phase 11 可作为云数据库 schema 与服务端权限设计阶段归档。下一阶段进入云开发初始化和首个 owner 账号入库流程。
