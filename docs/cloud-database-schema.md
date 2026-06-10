# 云数据库集合设计

状态：v1.0
日期：2026-05-27

## 1. 第一批必须创建

第一批先创建服务端权限和操作留痕需要的集合：

| 集合 | 用途 | 优先级 |
| --- | --- | --- |
| `store_members` | 门店成员角色，决定谁是球友、员工、老板 | P0 |
| `operation_logs` | 员工和老板操作日志 | P0 |
| `matches` | 挑战房间和比赛状态机 | P0 |
| `match_score_events` | 加减盘事件 | P1 |
| `settlements` | 结算结果 | P0 |
| `points_ledger` | 积分流水 | P0 |
| `member_points` | 会员积分账户余额 | P0 |
| `table_sessions` | 球桌当前开台到点时间 | P0 |
| `admin_configs` | 老板端门店参数配置 | P0 |
| `screen_tokens` | 电视大屏访问凭证 | P1 |

## 2. `store_members`

用于服务端权限判断。不能只靠前端角色。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID，单店第一版可用 `default` |
| `openid` | string | 是 | 微信 OpenID |
| `role` | string | 是 | `player` / `staff` / `owner` / `screen` |
| `status` | string | 是 | `active` / `disabled` |
| `nickname` | string | 否 | 昵称 |
| `phone` | string | 否 | 会员手机号 |
| `note` | string | 否 | 前台备注 |
| `avatarUrl` | string | 否 | 会员头像地址 |
| `rankState` | object | 否 | 当前段位状态，全部玩法共用一个段位 |
| `rankTitle` | string | 否 | 当前段位展示文案，例如 `走位黄金 III` |
| `lastRankUpdatedAt` | date | 否 | 最近一次段位结算写回时间 |
| `createdAt` | date | 是 | 创建时间 |
| `updatedAt` | date | 是 | 更新时间 |

建议索引：

```js
{ storeId: 1, openid: 1, status: 1 }
{ storeId: 1, role: 1, status: 1 }
```

第一版角色规则：

- `owner`：可访问老板端、员工端、大屏端。
- `staff`：可访问员工端、大屏端。
- `screen`：只用于大屏访问。
- `player`：只访问球友端。

老板端人员权限规则：

- 首个 `owner` 通过 `/pages/setup-owner/setup-owner` 初始化。
- 后续员工和大屏账号由老板端“人员权限”扫码会员码设置。
- `admin.setMemberRole` 只能设置 `player` / `staff` / `screen`。
- 不能通过人员权限入口修改已有 `owner`。
- 不能把当前老板自己的账号降权。

## 3. `operation_logs`

用于追踪员工和老板动作。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `module` | string | 是 | `staff` / `admin` / `match` |
| `action` | string | 是 | 操作动作 |
| `payload` | object | 是 | 操作参数 |
| `role` | string | 是 | 操作者角色 |
| `operatorOpenid` | string | 是 | 操作者 OpenID |
| `createdAt` | date | 是 | 操作时间 |

建议索引：

```js
{ storeId: 1, module: 1, createdAt: -1 }
```

## 4. `matches`

用于房间状态机。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 比赛 ID |
| `storeId` | string | 是 | 门店 ID |
| `roomNo` | string | 是 | 房间码，展示给对手加入 |
| `tableNo` | string | 是 | 球桌号 |
| `dueTime` | string | 否 | 球桌到点时间，例：`22:30` |
| `openedAt` | string | 否 | 员工设置的开台时间 |
| `status` | string | 是 | `waiting` / `joined` / `configured` / `playing` / `time_blocked` / `settlement_pending` / `settled` / `refused` / `voided` |
| `hostOpenid` | string | 是 | 发起方 |
| `guestOpenid` | string | 否 | 挑战方 |
| `source` | string | 否 | 创建来源，第一版为 `miniapp` |
| `modeId` | string | 否 | 玩法 |
| `base` | number | 否 | 底分 |
| `multiplier` | number | 否 | 倍率 |
| `riskPoints` | number | 否 | 风险积分，`base * multiplier` |
| `targetWins` | number | 否 | 当前玩法胜利盘数 |
| `minimumMinutes` | number | 否 | 当前玩法最低有效分钟数 |
| `scoreA` | number | 否 | 发起方盘数，开赛后写入 |
| `scoreB` | number | 否 | 挑战方盘数，开赛后写入 |
| `winnerSide` | string | 否 | 达到目标盘数后写入，`a` / `b` |
| `configuredAt` | date | 否 | 玩法和风险参数确认时间 |
| `startedAt` | date | 否 | 开赛时间 |
| `startedAtMs` | number | 否 | 开赛时间毫秒数，用于小程序端按服务端开始点计算已用时间 |
| `tableDueAt` | date | 否 | 开台到点时间 |
| `createdAt` | date | 是 | 创建时间 |
| `updatedAt` | date | 是 | 更新时间 |

建议索引：

```js
{ storeId: 1, status: 1, updatedAt: -1 }
{ storeId: 1, roomNo: 1 }
```

## 5. `match_score_events`

用于保存比赛计分过程中的每一次加减盘事件。它不是结算结果，只用于回溯“谁在什么时候改了哪一方盘数”。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `matchId` | string | 是 | 比赛 ID |
| `operatorOpenid` | string | 是 | 操作人 OpenID |
| `side` | string | 是 | 被调整的一方，`a` / `b` |
| `delta` | number | 是 | 本次变化，通常为 `1` / `-1` |
| `scoreA` | number | 是 | 调整后的发起方盘数 |
| `scoreB` | number | 是 | 调整后的挑战方盘数 |
| `createdAt` | date | 是 | 创建时间 |

建议索引：

```js
{ storeId: 1, matchId: 1, createdAt: -1 }
```

## 6. `settlements`

用于保存比赛结算结果。`match.previewSettlement` 只计算预览，不写入本集合；`match.settle` 确认后才写入。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `matchId` | string | 是 | 比赛 ID |
| `status` | string | 是 | `settling` / `settled` |
| `winnerSide` | string | 是 | 胜方，`a` / `b` |
| `loserSide` | string | 是 | 败方，`a` / `b` |
| `riskPoints` | number | 是 | 底分乘倍率 |
| `rewardValue` | number | 是 | 本场随机奖励分 |
| `rewardPhase` | string | 是 | `normal` / `sprint` |
| `winnerDelta` | number | 是 | 胜方积分变化 |
| `loserDelta` | number | 是 | 败方积分变化 |
| `scoreA` | number | 是 | 发起方最终盘数 |
| `scoreB` | number | 是 | 挑战方最终盘数 |
| `elapsedSeconds` | number | 是 | 实际比赛用时秒数 |
| `pointChanges` | array | 是 | 双方积分变化明细 |
| `rankChanges` | object | 是 | 双方段位变化明细 |
| `balances` | array | 否 | 结算写入后的双方余额 |
| `rankResults` | array | 否 | 结算写回 `store_members` 后的双方最新段位 |
| `settledBy` | string | 是 | 点击确认结算的 OpenID |
| `createdAt` | date | 是 | 创建时间 |
| `updatedAt` | date | 是 | 更新时间 |

建议索引：

```js
{ storeId: 1, matchId: 1 }
{ storeId: 1, status: 1, createdAt: -1 }
```

## 7. `points_ledger`

用于积分流水。所有积分变化都必须写流水。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `openid` | string | 是 | 用户 OpenID |
| `matchId` | string | 否 | 来源比赛 |
| `type` | string | 是 | `initial` / `table_bonus` / `match_win` / `match_loss` / `reward` / `exchange` / `adjust` |
| `delta` | number | 是 | 积分变化 |
| `balanceAfter` | number | 是 | 变化后余额 |
| `tableId` | string | 否 | 开台赠分来源球桌 |
| `dueTime` | string | 否 | 开台赠分对应的到点时间 |
| `bonusKey` | string | 否 | 开台赠分去重键 |
| `operatorOpenid` | string | 否 | 员工或老板操作人 OpenID |
| `createdAt` | date | 是 | 创建时间 |

## 8. `member_points`

用于保存会员当前积分余额。积分核销不能只写流水，必须先读取余额、扣减余额，再写流水。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `openid` | string | 是 | 用户 OpenID |
| `nickname` | string | 否 | 会员昵称 |
| `name` | string | 否 | 会员备注名 |
| `phone` | string | 否 | 会员手机号 |
| `note` | string | 否 | 前台备注 |
| `avatarUrl` | string | 否 | 会员头像地址 |
| `balance` | number | 是 | 当前积分余额 |
| `createdAt` | date | 是 | 创建时间 |
| `updatedAt` | date | 是 | 更新时间 |

建议索引：

```js
{ storeId: 1, openid: 1 }
{ storeId: 1, balance: -1 }
```

## 9. `table_sessions`

用于保存当前球桌开台到点时间。第一版只要求员工设置开台到点时间，不接开台软件 API。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `tableId` | string | 是 | 球桌 ID |
| `status` | string | 是 | `active` / `closed` |
| `dueTime` | string | 是 | 到点时间，例：`22:30` |
| `memberOpenid` | string | 否 | 本次开台绑定会员，绑定后可发开台赠分 |
| `updatedBy` | string | 是 | 最后更新员工 OpenID |
| `createdAt` | date | 是 | 创建时间 |
| `updatedAt` | date | 是 | 更新时间 |

建议索引：

```js
{ storeId: 1, tableId: 1, status: 1 }
{ storeId: 1, status: 1 }
```

## 10. `admin_configs`

用于保存老板端门店参数。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `config` | object | 是 | 完整门店配置 |
| `updatedBy` | string | 是 | 最后更新老板 OpenID |
| `createdAt` | date | 是 | 创建时间 |
| `updatedAt` | date | 是 | 更新时间 |

`config.antiCheat` 至少包含：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `geoFence` | string | 是 | 店内定位范围，例如 `100 米` |
| `storeLatitude` | string | 否 | 门店纬度；填写后用于挑战首页店内定位 |
| `storeLongitude` | string | 否 | 门店经度；填写后用于挑战首页店内定位 |

建议索引：

```js
{ storeId: 1 }
```

## 11. `screen_tokens`

用于电视浏览器访问大屏网页时校验凭证。小程序内大屏可以通过 `store_members.role = screen / staff / owner` 访问；浏览器静态网页不能依赖微信登录，必须走 token。

字段：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `_id` | string | 是 | 云数据库自动生成 |
| `storeId` | string | 是 | 门店 ID |
| `token` | string | 是 | 大屏访问凭证 |
| `status` | string | 是 | `active` / `disabled` |
| `label` | string | 否 | 电视或门店备注 |
| `createdAt` | date | 是 | 创建时间 |
| `updatedAt` | date | 是 | 更新时间 |

建议索引：

```js
{ storeId: 1, token: 1, status: 1 }
```

## 12. 服务端权限规则

云函数必须按以下顺序判断：

1. 读取微信 OpenID。
2. 按 `storeId + openid + status=active` 查询 `store_members`。
3. 没有记录时视为 `player`。
4. `owner` 拥有老板端、员工端、大屏端权限。
5. `staff` 只能访问员工端和大屏端。
6. 服务端禁止相信前端传入的角色。
7. 老板端人员权限变更必须写 `operation_logs`。
