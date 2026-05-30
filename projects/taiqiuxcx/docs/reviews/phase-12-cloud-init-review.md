# Phase 12 云开发初始化与首个 owner 入库审查

日期：2026-05-27

## Findings

### P1：真实云环境仍需在微信开发者工具里执行初始化

本阶段已补齐代码入口和运行手册，但没有替用户在微信云开发环境中实际创建集合、部署云函数、设置环境变量。上线前必须按 `docs/cloud-init-runbook.md` 执行。

处理：下一阶段进入真实云环境初始化或继续后端接口接入前，先确认云环境已开通、集合已创建、`yunhanApi` 已部署。

### P1：`BOOTSTRAP_OWNER_SECRET` 初始化后必须删除或轮换

`auth.bootstrapOwner` 依赖云函数环境变量 `BOOTSTRAP_OWNER_SECRET`。虽然它只允许无 owner 门店执行一次，但初始化完成后仍应删除或轮换密钥，减少误用入口。

处理：手册已写入该约束；真实执行时需要把密钥处理结果写回 `docs/dev-log.md`。

### P1：前端 service 尚未切到云函数

本阶段只补初始化链路。小程序页面当前仍通过 service 使用本地数据源，尚未让员工端、老板端写操作实际调用云函数。

处理：下一阶段优先把 `staff-service` 和 `admin-service` 的写操作替换为 `callCloud`。

## Scope Check

本阶段新增或改动：

- `cloudfunctions/yunhanApi/index.js`
- `docs/cloud-init-runbook.md`
- `cloudfunctions/README.md`
- `docs/api-service-layer-contract.md`
- `docs/backend-integration-readiness-plan.md`
- `docs/dev-log.md`

没有改动小程序可见页面。

## Requirement Check

- 已提供首个 owner 初始化方案。
- 初始化方案不依赖前端传入角色。
- 初始化方案不默认把无成员用户设为老板。
- 初始化方案不做成页面按钮。
- 已说明云数据库建集合、建索引、部署云函数、配置密钥、调用初始化和验证权限的步骤。
- 云函数错误响应保留 `PERMISSION_DENIED` 等错误码。

## Verification Evidence

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

结果：通过，包体 642.2 KB。

## Decision

Phase 12 可作为云开发初始化方案阶段归档。下一阶段应优先把员工端和老板端写操作接入 `callCloud`，让权限和操作日志真正经过云函数。
