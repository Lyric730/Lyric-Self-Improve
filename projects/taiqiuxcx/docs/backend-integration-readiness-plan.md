# 上线接入准备方案：权限、接口、状态机与真实数据

状态：v1.0
日期：2026-05-27

## 1. 目标

页面骨架已经覆盖球友端、员工端、老板端和大屏端。下一阶段目标不是继续补静态页面，而是把“能上线”的基础能力接起来：

- 角色权限。
- 真实房间状态。
- 服务端计时。
- 服务端结算。
- 积分流水。
- 员工 / 老板操作日志。
- 大屏接口和 screenToken。

## 2. 必须先做的上线阻断项

| 优先级 | 模块 | 不做的风险 |
| --- | --- | --- |
| P0 | 角色权限 | 普通顾客可访问员工端或老板端 |
| P0 | 服务端结算 | 前端可篡改比分、积分、随机奖励 |
| P0 | 积分流水 | 无法追踪积分来源、扣减、撤销 |
| P1 | 房间状态机 | 多端比分不同步，退出 / 不服 / 再战状态混乱 |
| P1 | 服务端时间 | 用户本地时间不可信，最低有效时间可被绕过 |
| P1 | 操作日志 | 员工作废、老板配置、前台核销无法追责 |
| P1 | 大屏 screenToken | 大屏接口可能被外部随意访问 |

## 3. 角色权限

第一版至少三类角色：

| 角色 | 可访问 |
| --- | --- |
| 球友 | 挑战流程、我的数据、排行榜、积分礼遇 |
| 员工 | 前台工作台 |
| 老板 / 管理员 | 门店参数、员工端、所有数据 |

前端路由进入前必须检查角色；后端接口也必须重复校验角色，不能只靠前端隐藏入口。

## 4. 房间状态机

建议先按以下状态实现：

| 状态 | 含义 |
| --- | --- |
| `waiting` | 发起方已开房，等待对手加入 |
| `accepted` | 对手已接受，准备选择玩法 |
| `configured` | 已确认玩法、底分、倍率 |
| `playing` | 比赛计分中 |
| `time_blocked` | 已达到胜利盘数但未满最低有效时间 |
| `settlement_pending` | 满足结算条件，等待败方服 / 不服 |
| `settled` | 结算生效 |
| `refused` | 败方不服，等待退出或再战 |
| `voided` | 员工作废 |

任何比分、状态、结算结果都由服务端写入，前端只负责展示和提交动作。

## 5. 服务端结算

服务端接收：

- `matchId`
- `winnerUserId`
- `scoreA`
- `scoreB`
- `finalAction`

服务端必须重新读取：

- 玩法模板。
- 底分和倍率。
- 开赛时间。
- 当前服务端时间。
- 球桌开台到点时间。
- 双方积分余额。
- 本场随机奖励。

服务端输出：

- 胜方积分变化。
- 败方积分变化。
- 随机奖励。
- 段位星级变化。
- 积分流水记录。
- 排行榜更新任务。

## 6. 接口清单

### 球友端

- `POST /matches` 创建挑战房间。
- `POST /matches/:id/join` 接受挑战。
- `POST /matches/:id/config` 确认玩法、底分、倍率。
- `POST /matches/:id/score` 提交加减盘操作。
- `GET /matches/:id` 获取房间状态。
- `POST /matches/:id/settle/accept` 服了确认。
- `POST /matches/:id/settle/refuse` 不服。
- `POST /matches/:id/rematch` 再战。
- `GET /me/stats` 我的数据。
- `GET /rankings` 排行榜。
- `GET /points/perks` 积分礼遇。

### 员工端

- `GET /staff/tables` 今日球桌。
- `POST /staff/tables/:id/due-time` 设置开台到点时间。
- `GET /staff/users/search` 搜索用户。
- `POST /staff/points/deduct` 前台扣积分。
- `GET /staff/abnormal-matches` 异常比赛。
- `POST /staff/matches/:id/void` 作废比赛。

### 老板端

- `GET /admin/config` 获取门店配置。
- `POST /admin/config/modes` 保存玩法配置。
- `POST /admin/config/points` 保存积分配置。
- `POST /admin/config/anti-cheat` 保存防刷分配置。
- `POST /admin/config/screen` 保存大屏配置。

### 大屏

- `GET /screen/ranking?storeId=&screenToken=`
- `GET /screen/bounty?storeId=&screenToken=`

## 7. 数据表建议

第一版至少需要：

- `users`
- `store_members`
- `roles`
- `tables`
- `table_sessions`
- `game_templates`
- `matches`
- `match_score_events`
- `settlements`
- `points_ledger`
- `rank_states`
- `rank_snapshots`
- `admin_configs`
- `operation_logs`
- `screen_tokens`

## 8. 前端替换顺序

1. 接角色权限，先挡住员工端和老板端。
2. 接员工端球桌到点时间。
3. 接创建房间、加入房间、房间状态轮询。
4. 接比赛计分事件。
5. 接服务端结算。
6. 接我的数据、排行榜、积分礼遇。
7. 接老板配置。
8. 接大屏接口和 screenToken。

## 9. 仍然保留本地占位的范围

在接口接入前，允许本地数据只用于页面开发和联调，但必须满足：

- 页面不出现 mock、模拟、演示、占位等可见文案。
- 所有本地数据模块集中在 `miniprogram/utils/ladder-data.js`，不能散落到页面里。
- 每替换一个接口，就删除对应本地数据入口。

## 10. 当前前端已落地的接入准备

本轮已经先把权限和操作留痕的前端入口补上，避免员工端、老板端继续以裸页面方式存在。

- 新增 `miniprogram/utils/access-control.js`：统一读取当前角色，并在员工端、老板端、小程序大屏页进入前做权限拦截。
- 新增 `miniprogram/utils/operation-log.js`：统一记录员工和老板动作，为后续替换成服务端日志接口预留结构。
- 员工端已接入权限拦截：员工和老板可进入，普通球友进入时返回球友首页。
- 老板端已接入权限拦截：仅老板角色可进入。
- 小程序大屏页已接入权限拦截：员工、老板或大屏角色可进入。
- 员工端已记录：设置开台到点时间、积分核销、异常比赛作废。
- 老板端已记录：保存门店配置。

注意：前端权限和本地操作记录不能替代服务端权限与服务端日志。正式上线时，接口层必须重复校验角色，并将操作日志写入 `operation_logs`。

## 11. Phase 9：前端接口层收口

本轮新增 `miniprogram/services/`，把页面取数、运营动作和结算计算先收口到 service 层：

- `api-client.js`：统一 `ok/data` 返回结构和错误处理。
- `player-service.js`：球友端首页、房间、邀请、我的数据、排行榜、积分礼遇。
- `match-service.js`：玩法模板、开局参数、当前比赛、结算结果。
- `staff-service.js`：员工球桌、到点时间、积分核销、异常作废。
- `admin-service.js`：老板配置读取和保存。
- `screen-service.js`：小程序大屏榜单。

阶段目标不是制造一个假后端，而是让页面不再直接依赖本地数据和本地结算函数。后续接真实接口时，优先替换 `services/`，不要回到每个页面里散改。

详细契约见：`docs/api-service-layer-contract.md`。

## 12. Phase 10：微信云开发骨架

基于 solo-op 维护成本优先，第一版后端默认按微信云开发推进：

- 不额外维护独立服务器。
- 登录态、OpenID、云函数和云数据库都在微信开发链路内。
- 适合先做单店 MVP，再逐步扩展多店。

当前已落地：

- `project.config.json` 增加 `cloudfunctionRoot: "cloudfunctions/"`。
- `miniprogram/app.js` 增加安全的 `wx.cloud.init({ traceUser: true })`。
- 新增 `cloudfunctions/yunhanApi` 统一云函数入口。
- `api-client.js` 预留 `callCloud(moduleName, action, payload)`，后续 service 可逐步替换到云函数调用。

`yunhanApi` 当前只做后端骨架，不代表真实业务已上线：

- `auth`：读取微信 OpenID。
- `match`：预留房间状态和服务端结算。
- `staff`：预留员工操作日志入口。
- `admin`：预留老板操作日志入口。
- `screen`：预留大屏 `screenToken` 校验。

正式启用前必须先建表并补规则：

- `store_members`：角色与门店关系。
- `matches`：房间状态机。
- `match_score_events`：比分事件。
- `settlements`：结算结果。
- `points_ledger`：积分流水。
- `member_points`：会员积分账户余额。
- `table_sessions`：球桌当前开台到点时间。
- `admin_configs`：老板端门店参数配置。
- `operation_logs`：员工/老板操作日志。
- `screen_tokens`：大屏访问凭证。

## 13. Phase 11：云数据库集合与服务端权限

已新增 `docs/cloud-database-schema.md`，先定义第一批必须创建的集合和字段：

- `store_members`
- `operation_logs`
- `matches`
- `match_score_events`
- `settlements`
- `points_ledger`
- `screen_tokens`

云函数已从 TODO 权限推进到按 `store_members` 查询角色：

- `auth` 会返回当前 OpenID、storeId 和角色。
- `staff` 模块要求 `staff` 或 `owner`。
- `admin` 模块要求 `owner`。
- `owner` 默认拥有员工端、大屏端权限。
- 没有成员记录时按普通 `player` 处理。

注意：云数据库集合尚未在微信云开发环境中实际创建。下一步需要在微信开发者工具里开通云开发环境，并按 `docs/cloud-database-schema.md` 建集合和索引。

## 14. Phase 12：云开发初始化与首个 owner 入库

下一阶段不继续堆页面，而是补上线前必须完成的初始化链路：

- 在微信开发者工具中开通云开发环境。
- 上传并部署 `yunhanApi` 云函数。
- 按 `docs/cloud-database-schema.md` 创建第一批集合。
- 按集合用途创建建议索引。
- 获取老板 OpenID。
- 在 `store_members` 写入首个 `owner` 记录。
- 用 `auth`、`staff`、`admin` 三个模块验证服务端角色判断。

关键约束：

- 不做“前端临时角色开关”作为正式权限方案。
- 首个 owner 初始化必须有清晰操作手册，避免上线时老板端无法进入。
- 没有 owner 记录时，云函数按普通 `player` 处理，这是安全默认值，不应改成默认老板。

本阶段落地方式：

- 新增 `docs/cloud-init-runbook.md`。
- `auth.bootstrapOwner` 使用 `BOOTSTRAP_OWNER_SECRET` 做一次性初始化。
- `bootstrapOwner` 只在当前门店没有 `active owner` 时可执行。
- 初始化成功后写入 `store_members`，并尽量写入 `operation_logs`。

## 15. Phase 13：员工端与老板端写操作接入云函数

本阶段先接写操作，不一次性替换全部读数据：

- 员工保存球桌到点时间：`callCloud("staff", "updateTableDueTime")`
- 员工积分核销：`callCloud("staff", "deductMemberPoints")`
- 员工异常作废：`callCloud("staff", "voidAbnormalMatch")`
- 老板保存配置：`callCloud("admin", "saveConfig")`

已调整页面：

- 员工端写按钮增加 loading，避免重复提交。
- 老板端保存按钮增加 loading，避免重复提交。
- 云函数失败时只展示面向用户的失败 toast，不展示内部技术清单。

仍未完成：

- `admin_configs` 已有云函数写入逻辑，但尚未在真实云环境验证。
- 员工到点时间已有 `table_sessions` 写入逻辑，但尚未在真实云环境验证。
- 积分核销已有 `member_points` 扣减与 `points_ledger` 写入逻辑，但尚未在真实云环境验证。
- 异常作废已有 `matches.status = voided` 写入逻辑，但尚未在真实云环境验证。
- 员工核销还缺少稳定用户 ID，后续必须补 `openid` 或 `memberId`。

## 16. Phase 14：云端真实持久化第一版

本阶段把云函数从“只做权限和操作日志”推进到“真实写库”：

- `admin.saveConfig`
  - 写入或更新 `admin_configs`。
  - 保存完整 `config`。
- `staff.updateTableDueTime`
  - 写入或更新 `table_sessions`。
  - 以 `storeId + tableId + status=active` 作为当前开台记录。
- `staff.deductMemberPoints`
  - 要求传入会员 `openid`。
  - 读取 `member_points` 当前余额。
  - 余额足够时扣减余额。
  - 写入 `points_ledger`。
- `staff.voidAbnormalMatch`
  - 先按 `storeId + matchId` 查比赛。
  - 找到后才更新 `matches.status = voided`。

仍未完成：

- 真实云环境部署验证。
- 积分扣减事务化。
- 员工端会员搜索/扫码识别。
- 异常列表从云端 `matches` 读取。
- 球友端比赛状态机和服务端结算。

## 17. Phase 15：员工端会员扫码识别

本阶段解决积分核销缺少会员 ID 的问题：

- 员工端不再默认挂一个样例会员。
- 核销区初始状态为“未选择会员”。
- 员工点击“扫码选择”后调用 `wx.scanCode`。
- 扫码结果可解析：
  - JSON：`{"openid":"..."}`
  - URL query：`?openid=...`
  - 标签文本：`openid:...`
  - 纯 OpenID
- 扫码后调用 `staff.getMemberForExchange`。
- 服务端从 `member_points` 查询积分账户。
- 只有选中会员后才能点击“确认核销”。

仍未完成：

- 球友端会员码页面。
- 统一二维码内容格式。
- 手机号/昵称手动搜索兜底。

## 18. Phase 16：球友端会员码

本阶段给员工端扫码核销补正式来源：

- 新增球友端会员码页面：`pages/member-code/member-code`。
- 积分礼遇页新增“出示会员码”入口。
- 新增 `member-service.js`。
- 云函数新增 `member.getCode`。
- 云函数用当前微信 OpenID 生成二维码。
- 二维码内容格式：

```json
{
  "type": "yunhan-member",
  "version": 1,
  "storeId": "default",
  "openid": "当前微信 OpenID"
}
```

注意：

- 会员码云函数依赖 `qrcode` npm 包。
- 部署 `yunhanApi` 时必须选择云端安装依赖。
- 后续需要补会员积分账户创建，否则员工扫码后仍可能找不到 `member_points`。

## 19. Phase 17：会员积分账户创建与初始积分发放

本阶段让会员码和积分账户打通：

- `member.getCode` 会先查 `member_points`。
- 如果当前用户没有积分账户：
  - 读取 `admin_configs.config.points.newUser`。
  - 没有老板配置时，使用默认 300 分。
  - 创建 `member_points`。
  - 写入 `points_ledger(type=initial)`。
- 如果已有积分账户：
  - 不重复发放初始积分。
  - 返回当前余额。
- 会员码页面展示当前积分。

仍未完成：

- 开台赠分。
- 积分账户创建幂等强化。
- 真实云环境和真机扫码闭环验证。

## 20. Phase 18：真实云环境部署前检查

本阶段不继续堆比赛结算逻辑，先确认云开发链路能不能跑。

已完成：

- 确认微信开发者工具 CLI 已登录。
- 确认 CLI 支持 `cloud env list`、`cloud functions deploy`、`cloud functions info`。
- 新增 `scripts/check-wechat-cloud-readiness.ps1`，用于统一检查登录态、云环境、云函数列表和 `yunhanApi` 信息。
- CLI 部署命令已固定为 `--remote-npm-install`，避免本地 `node_modules` 进入包体，并确保云端安装 `qrcode` 依赖。

当前阻塞：

- `cloud env list` 返回 `测试号不能使用云服务`。
- 这说明当前导入项目的 AppID 无法使用微信云开发。
- 在这个状态下，不能完成真实云函数部署、数据库集合创建、owner 初始化、会员码真机扫码闭环。

下一步必须先处理：

1. 把微信开发者工具项目切换到已注册的小程序 AppID。
2. 在开发者工具里创建云开发环境。
3. 记录云环境 ID。
4. 运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID'
```

5. 确认无误后部署：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID' -Deploy
```
