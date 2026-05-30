# Phase 10 微信云开发骨架审查

日期：2026-05-27

## Findings

### P1：云函数只是骨架，不能作为已上线后端

`cloudfunctions/yunhanApi` 已建立统一入口，但角色、房间、结算、积分流水都还没有真实数据库规则。当前云函数只能作为后端接入起点，不能支撑正式业务。

处理：不阻塞骨架阶段。下一阶段必须创建云数据库集合并实现角色读取。

### P1：员工和老板云端权限还未读 `store_members`

当前 `assertRole` 还没有从云数据库读取门店成员角色。正式上线必须根据 OpenID + storeId 查询角色，不能用前端传参决定身份。

处理：下一阶段 P0。

### P1：服务端结算还未实现

云函数 `match.settle` 当前返回未启用，前端 `match-service.calculateSettlement` 仍使用本地计算。正式上线前必须把结算公式、最低有效时间、随机奖励、积分流水全部迁移到云函数。

处理：下一阶段 P0。

### P2：云环境 ID 尚未固定

`wx.cloud.init({ traceUser: true })` 未指定 `env`，适合本阶段不阻塞预览；正式部署前需要在项目配置或运行配置中明确云环境。

处理：云开发开通后补。

## Scope Check

本阶段新增或改动：

- `project.config.json`
- `miniprogram/app.js`
- `miniprogram/services/api-client.js`
- `cloudfunctions/README.md`
- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/yunhanApi/package.json`
- `docs/backend-integration-readiness-plan.md`
- `docs/api-service-layer-contract.md`

没有切换正式页面到云函数调用，因此不会影响当前小程序预览流程。

## Requirement Check

- 项目已配置 `cloudfunctionRoot`。
- 小程序启动时安全初始化云能力。
- 已建立统一云函数入口。
- 云函数包含 `auth`、`match`、`staff`、`admin`、`screen` 模块入口。
- `api-client` 已预留 `callCloud`。
- 文档明确当前只是骨架，不冒充真实后端。

## Verification Evidence

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过。

```powershell
node --check cloudfunctions\yunhanApi\index.js
```

结果：通过。

```powershell
node scripts\check-json-files.js
```

结果：`JSON check OK (32 files checked)`。

```powershell
node scripts\check-production-copy.js
```

结果：`Production copy check OK (19 files checked)`。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 `642.2 KB`。

## Decision

通过。Phase 10 作为云开发骨架阶段归档；下一阶段进入云数据库集合和服务端权限。
