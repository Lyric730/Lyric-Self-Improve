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
| `miniprogram/services/member-service.js` | 会员码、会员资料读取与保存 | 云函数 + 本地缓存兜底 | `/member/code`、`/member/profile` |
| `miniprogram/services/match-service.js` | 玩法模板、开局参数、当前比赛、结算结果 | `ladder-data.js` | `/matches/:id`、`/matches/:id/config`、`/matches/:id/settle/*` |
| `miniprogram/services/staff-service.js` | 员工球桌、到点时间、积分核销、异常作废 | 云函数 + DevTools 本地缓存兜底 | `/staff/tables`、`/staff/points/deduct`、`/staff/matches/:id/void` |
| `miniprogram/services/admin-service.js` | 老板配置读取与保存 | 云函数 + 本地配置缓存 | `/admin/config/*` |
| `miniprogram/services/screen-service.js` | 小程序大屏榜单数据 | `ladder-data.js` + 老板端大屏配置 | `/screen/ranking`、`/screen/bounty` |

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
3. `admin-service` 保存配置前已通过 `miniprogram/utils/admin-config-validator.js` 校验门店参数，云函数 `admin.saveConfig` 也已通过 `cloudfunctions/yunhanApi/admin-config-validator.js` 复用同一口径。
4. 当前 `match-service.calculateSettlement` 仍通过 `miniprogram/utils/settlement-engine.js` 计算本地结算展示。
5. 云函数 `match.settle` 已接入 `cloudfunctions/yunhanApi/settlement-engine.js` 和 `match-settlement.js`，会服务端计算积分、随机奖励和段位变化，并写入 `settlements`、`points_ledger`、`member_points`、`matches.status`。
6. 下一步把 `match-service.calculateSettlement` 替换为 `callCloud("match", "settle", payload)`；前端切换前，正式页面仍不能绕过 `match-service`。
6. `member-service.saveMemberProfile` 已改为优先调用 `callCloud("member", "saveProfile", payload)`，云函数只允许保存昵称、手机号、备注、头像地址，不允许保存段位和积分；DevTools 无云环境时才使用本地缓存兜底。
7. 最后替换榜单、个人数据和大屏数据读取。

注意：`admin-config-validator` 和 `member-profile` 当前在小程序端与云函数包内各保留一份。每次修改校验规则后必须运行 `node scripts/test-cloud-contracts.js`，确认前端和云函数口径一致。

当前为了保证微信开发者工具在无云环境时可继续预览，`member-service`、`staff-service`、`admin-service` 保留 DevTools 本地兜底。生产环境不能依赖这些兜底；云函数可用后，必须按 `docs/cloud-function-cutover-checklist.md` 做真实落库验证。

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
- `match.settle` 已有云函数入口，但真实云环境尚未验证；上线前必须测试重复结算、余额不足、比赛不存在、最低时间不足、双方身份缺失。
- `screen-service.js` 接入 `screenToken`。
- `screen-service.js` 的榜单数据接真实排行榜集合。
- `member-service.js` 的会员资料保存已接云函数；真实云环境可用后要验证 `store_members` / `member_points` 写入。

## 7. 验收规则

后续每次新增页面或接口，必须满足：

```powershell
node scripts/test-ops-services.js
node scripts/test-cloud-contracts.js
node scripts/check-service-layer-boundary.js
```

结果应通过。若页面直接引用本地数据、操作日志或结算引擎，除非是明确的开发验收页，否则不能归档。
