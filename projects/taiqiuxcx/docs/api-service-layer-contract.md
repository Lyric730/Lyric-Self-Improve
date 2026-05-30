# 小程序接口层契约

状态：v1.0
日期：2026-05-27

## 1. 目标

本文件约束小程序前端的接口层。后续接真实后端时，只改 `miniprogram/services/`，业务页面不再直接读取本地数据、不直接写日志、不直接计算结算。

## 2. 当前 service 分层

| 文件 | 职责 | 当前数据来源 | 未来替换接口 |
| --- | --- | --- | --- |
| `miniprogram/services/api-client.js` | 统一返回结构和错误处理 | 本地同步结果 | `wx.request` 或云函数调用 |
| `miniprogram/services/player-service.js` | 球友首页、房间、邀请、我的数据、排行榜、积分礼遇 | `ladder-data.js` | `/matches`、`/me/stats`、`/rankings`、`/points/perks` |
| `miniprogram/services/match-service.js` | 玩法模板、开局参数、当前比赛、结算结果 | `ladder-data.js` | `/matches/:id`、`/matches/:id/config`、`/matches/:id/settle/*` |
| `miniprogram/services/staff-service.js` | 员工球桌、到点时间、积分核销、异常作废 | `ladder-data.js` + 本地操作日志入口 | `/staff/tables`、`/staff/points/deduct`、`/staff/matches/:id/void` |
| `miniprogram/services/admin-service.js` | 老板配置读取与保存 | `ladder-data.js` + 本地操作日志入口 | `/admin/config/*` |
| `miniprogram/services/screen-service.js` | 小程序大屏榜单数据 | `ladder-data.js` | `/screen/ranking`、`/screen/bounty` |

## 3. 页面调用规则

- 页面只能调用 `miniprogram/services/`。
- 页面不能直接调用 `miniprogram/utils/ladder-data.js`。
- 页面不能直接调用 `miniprogram/utils/operation-log.js`。
- 页面不能直接计算积分结算。
- 页面可以继续调用 `access-control.js` 做前端路由拦截，但正式接口仍必须做服务端权限校验。

## 4. 返回结构

当前所有 service 返回：

```js
{
  ok: true,
  data: {}
}
```

失败时返回：

```js
{
  ok: false,
  code: "REQUEST_FAILED",
  message: "操作失败，请稍后再试"
}
```

页面用 `ensureOk(result)` 读取数据。后续换成真实接口时，仍保持这个返回结构，减少页面改动。

## 4.1 云函数预留

`api-client.js` 已预留：

```js
callCloud(moduleName, action, payload)
```

当前运营端写操作已开始调用云函数。后续替换顺序：

1. `staff-service` 的写操作已替换为 `callCloud("staff", action, payload)`。
2. `admin-service` 的保存配置已替换为 `callCloud("admin", action, payload)`。
3. 下一步把 `match-service.calculateSettlement` 替换为 `callCloud("match", "settle", payload)`。
4. 最后替换榜单、个人数据和大屏数据读取。

云函数入口：`cloudfunctions/yunhanApi/index.js`。

首个老板账号初始化见：`docs/cloud-init-runbook.md`。该流程通过 `auth.bootstrapOwner` 执行一次，不做成前端页面。

## 5. 当前已收口页面

球友端：

- `challenge-home`
- `waiting-room`
- `accept-challenge`
- `mode-select`
- `points-select`
- `match-confirm`
- `match-scoring`
- `time-insufficient`
- `settlement`
- `refusal`
- `match-result`
- `my-data`
- `rankings`
- `points-perks`

运营端：

- `staff-desk`
- `boss-config`
- `tv-ranking`

## 6. 仍需真实后端补齐

- `api-client.js` 替换为真实 `wx.request` 或云函数调用。
- `access-control.js` 的角色来源替换为登录态接口。
- `operation-log.js` 仅保留历史开发背景；运营端写操作已改为服务端 `operation_logs` 入口。
- `match-service.js` 的 `calculateSettlement` 替换为服务端结算接口，前端不再拥有结算公式。
- `screen-service.js` 接入 `screenToken`。

## 7. 验收规则

后续每次新增页面或接口，必须满足：

```powershell
rg -n "ladder-data|operation-log" miniprogram/pages --glob "*.js"
```

结果应无页面直接引用。若有命中，除非是明确的开发验收页，否则不能归档。
