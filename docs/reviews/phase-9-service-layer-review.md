# Phase 9 接口层收口审查

日期：2026-05-27

## Findings

### P1：当前 service 层仍未连接真实后端

`miniprogram/services/` 已经把页面取数、运营动作、结算结果收口，但当前 service 内部仍读取 `ladder-data.js`。正式上线必须把 `api-client.js` 替换为真实请求，并让角色、房间、结算、积分流水、操作日志都由服务端负责。

处理：当前阶段目标是前端接口口子收口，不假装真实后端已完成；进入后端接入阶段时优先替换 service。

### P1：结算 service 仍调用本地计算函数

页面已经不再直接调用 `buildSettlement`，改为调用 `match-service.calculateSettlement`。但 `calculateSettlement` 当前内部仍调用本地函数。正式上线必须改成服务端结算接口，前端不能保留可篡改的结算权。

处理：已从页面层移除直接结算计算；服务端结算进入下一阶段 P0。

### P2：service 返回仍是同步结构

当前 service 返回 `{ ok, data }` 同步结果，便于现阶段不改大量页面。后续接 `wx.request` 或云函数时，可能需要改成 Promise 或 async 流程。

处理：记录到接口接入阶段；如果真实后端选型确定，再统一调整调用方式。

## Scope Check

本阶段新增或改动：

- `miniprogram/services/api-client.js`
- `miniprogram/services/player-service.js`
- `miniprogram/services/match-service.js`
- `miniprogram/services/staff-service.js`
- `miniprogram/services/admin-service.js`
- `miniprogram/services/screen-service.js`
- 全部正式业务页面 JS 的数据入口
- `docs/api-service-layer-contract.md`
- `docs/backend-integration-readiness-plan.md`
- `AGENTS.md`

没有改动 WXML 视觉结构，没有新增用户可见页面文案。

## Requirement Check

- 业务页面不再直接引用 `miniprogram/utils/ladder-data.js`。
- 业务页面不再直接引用 `miniprogram/utils/operation-log.js`。
- 员工端、老板端、小程序大屏页继续保留权限拦截。
- 员工端和老板端动作改为通过 service 写入操作日志入口。
- 玩法、底分倍率、结算结果改为通过 `match-service` 获取。
- 排行榜、我的数据、积分礼遇、等待房间、接受挑战改为通过 `player-service` 获取。
- 大屏榜单改为通过 `screen-service` 获取。
- 接口层契约已落文档。

## Verification Evidence

```powershell
rg -n "ladder-data|operation-log" miniprogram\pages --glob "*.js"
```

结果：无匹配。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过。

```powershell
node scripts\check-json-files.js
```

结果：`JSON check OK (31 files checked)`。

```powershell
node scripts\check-production-copy.js
```

结果：`Production copy check OK (19 files checked)`。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：`Edge check OK (32 PNG assets checked)`。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 `641.5 KB`。

## Decision

通过。Phase 9 作为接口层前置阶段归档；下一阶段进入真实后端选型与接入。
