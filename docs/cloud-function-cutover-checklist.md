# 云函数切换上线清单

日期：2026-06-03

## 1. 前置条件

- 微信开发者工具已使用正式小程序 AppID：`wxe30b469d64636a2b`。
- 已创建云开发环境，并拿到环境 ID。
- 已按 `docs/cloud-init-runbook.md` 创建集合、索引、云函数环境变量和首个 owner。
- 已部署 `cloudfunctions/yunhanApi`，并选择云端安装依赖。

## 2. 必测接口

| 模块 | action | 前端入口 | 必须验证 |
| --- | --- | --- | --- |
| `player` | `getProfile` | 我的数据 / 我的 | 读取当前会员积分、段位和赛季表现 |
| `player` | `getChallengeHome` | 挑战首页 | 读取当前会员身份、积分、段位和可用球桌到点时间 |
| `player` | `getRankings` | 排行榜 | 读取店内总榜、同段位榜和微信好友榜；好友关系未接入时返回空榜 |
| `player` | `getPointsPerks` | 积分礼遇 | 读取当前积分、开台赠分和兑换门槛 |
| `member` | `getCode` | 会员码页 | 返回真实可扫码二维码、当前积分、当前用户 OpenID 绑定账户 |
| `member` | `saveProfile` | 我的页个人信息 | 只保存昵称、手机号、备注、头像，不允许前端改积分和段位 |
| `staff` | `getMemberForExchange` | 前台扫码选择 | 扫码后能查到会员积分账户 |
| `staff` | `deductMemberPoints` | 前台积分核销 | 扣减余额、写 `points_ledger`、余额不足时拒绝 |
| `staff` | `updateTableDueTime` | 前台到点时间 | 写 `table_sessions`，再次进入前台能读回 |
| `staff` | `voidAbnormalMatch` | 异常比赛 | 更新比赛状态，写操作日志 |
| `admin` | `saveConfig` | 老板端参数 | 复用前端同一套校验，写 `admin_configs` |
| `screen` | `getBoard` | 电视大屏 | 读取店内总榜、赏金猎人和老板端大屏配置 |
| `match` | `getModes` | 玩法选择 | 读取老板端当前玩法配置，抢 10 关闭时仍展示为不可选 |
| `match` | `getSetup` | 底分倍率 | 按所选玩法读取底分、倍率、普通随机奖励和续时冲刺奖励 |
| `match` | `createRoom` | 发起挑战 | 创建 `matches` 等待房间，返回 `matchId` 和房间状态 |
| `match` | `joinRoom` | 接受挑战 | 写入挑战方 OpenID，房间状态改为 `joined`，防止加入自己的房间和第三人抢占 |
| `match` | `configure` | 确认开局 | 按老板端玩法配置校验底分和倍率，写入玩法、底分、倍率和风险积分，房间状态改为 `configured` |
| `match` | `start` | 进入计分页 | 校验房间已配置且双方到齐，把状态改为 `playing`，写入 `startedAt / startedAtMs` 和初始盘数 |
| `match` | `recordScore` | 比赛计分 | 校验本场双方身份，按单次 `+1 / -1` 写入当前盘数和 `match_score_events`，达到目标盘数后进入 `settlement_pending` |
| `match` | `get` | 等待对手页 | 按 `matchId` 读取房间状态 |
| `match` | `previewSettlement` | 结算确认页 | 服务端计算结算预览，不写结算单和积分流水 |
| `match` | `settle` | 结算链路 | 服务端计算积分、随机奖励、星级，写结算和积分流水 |
| `match` | `getSettlement` | 结果页 | 按 `matchId` 读取已结算记录，结果页显示云端结算单 |

`match.settle` 当前已有云函数代码入口，但还没在真实云环境验证。上线前必须确认：

- 发起挑战必须先创建真实 `matches` 文档，并把 `matchId` 透传到后续玩法、底分、计分、结算页面。
- 真实 `matches` 文档存在时才能结算。
- 对手加入必须通过 `match.joinRoom` 写入真实 `matches.guestOpenid`，不能只靠前端刷新状态。
- 玩法、底分、倍率必须通过 `match.configure` 写入真实 `matches` 文档，不能只依赖页面 query 参数。
- 开赛必须通过 `match.start` 写入 `matches.status = playing` 和服务端开赛时间，不能只靠页面本地计时。
- 加减盘必须通过 `match.recordScore` 写入真实 `matches.scoreA / scoreB` 和 `match_score_events`，不能只改页面变量。
- 结算用时必须优先由 `matches.startedAtMs` 计算，不能信任页面 query 里的 `elapsed`。
- 球友端个人数据、排行榜和积分礼遇必须通过 `player` 云函数读取，正式环境不能直接展示本地 `ladder-data.js` 样例数据。
- 挑战首页必须通过 `player.getChallengeHome` 读取会员身份和球桌开局检查，不能用本地固定 `challengeGate` 判断能否开局。
- 玩法选择和底分倍率必须通过 `match.getModes` / `match.getSetup` 读取老板端配置，不能只展示本地写死参数。
- `match.previewSettlement` 只能读取和计算，不得写入 `settlements`、`points_ledger` 或修改 `member_points`。
- 同一 `matchId` 不能重复写 `settlements` 或重复改积分。
- 双方 `member_points` 账户必须存在。
- 败方扣分后不能出现负余额。
- `points_ledger` 中胜方为 `match_win`，败方为 `match_loss`。
- 当前实现不是事务级写入，只是先写 `settlements.status = settling` 作为结算锁；云环境可用后必须做中途失败和重复点击测试。

## 3. 本地兜底必须替换的点

- `member-service.getMemberCode` 当前 DevTools 无云环境时显示本地视觉码；上线必须显示云函数真实二维码。
- `staff-service` 当前 DevTools 无云环境时允许本地保存到点时间、核销积分、作废异常；上线必须由云函数真实落库。
- `admin-service` 当前保存后写本地缓存；上线必须确认 `admin_configs` 云端写入和读取都成功。
- 小程序内大屏页必须通过 `screen.getBoard` 读取店内总榜、赏金猎人和老板端大屏配置；浏览器静态大屏后续还需要接 HTTP 化 `screenToken`。

## 4. 上线前验证命令

```powershell
node scripts/test-ops-services.js
node scripts/test-cloud-contracts.js
node scripts/test-settlement-engine.js
node scripts/test-admin-config-validator.js
node scripts/test-member-profile.js
node scripts/check-json-files.js
node scripts/check-production-copy.js
node scripts/check-player-flow-routes.js
powershell -ExecutionPolicy Bypass -File scripts/check-ui-kit-asset-edges.ps1 -RequireAssets
powershell -ExecutionPolicy Bypass -File scripts/check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID' -Deploy
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```

## 5. 人工走查顺序

1. 我的页编辑昵称、手机号、备注、头像，保存后退出重进仍保留。
2. 会员码页生成二维码，前台扫码能选择同一个会员。
3. 前台扣除积分，会员积分减少，积分流水有记录。
4. 前台设置球桌到点时间，退出重进后时间保持。
5. 老板端修改底分、倍率、随机奖励、大屏标题，保存后退出重进仍保留。
6. 玩法选择和底分倍率页显示老板端配置的玩法、底分、倍率和随机奖励。
7. 大屏页显示老板端配置的主榜、副榜、刷新文案。
8. 球友端完整走一场挑战，结算由云函数完成，重复点击不能重复结算。

## 6. 不能上线的红线

- 会员码不能被员工端扫码识别。
- 前台核销只改页面、不写积分流水。
- 老板端保存只在本地缓存成功、云端没有记录。
- 结算仍由前端单独决定积分和段位。
- 老板 / 员工权限只靠前端角色切换，不经过云函数角色校验。
