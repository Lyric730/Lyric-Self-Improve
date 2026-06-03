# 云瀚台球小程序云函数

当前云函数根目录已在 `project.config.json` 中配置为：

```json
"cloudfunctionRoot": "cloudfunctions/"
```

## yunhanApi

`cloudfunctions/yunhanApi` 是第一版统一云函数入口：

- `auth`：读取微信 OpenID。
- `auth.bootstrapOwner`：使用云函数环境变量完成首个 owner 初始化，仅允许无 owner 门店执行一次。
- `player`：处理球友端只读数据；`getProfile` 返回会员积分、段位和赛季表现；`getRankings` 返回店内总榜、同段位榜和好友榜占位；`getPointsPerks` 返回积分礼遇和兑换门槛。
- `match`：处理比赛房间、比赛查询、开赛计分和服务端结算；`createRoom` 创建等待房间；`joinRoom` 写入挑战方并把房间状态改为 `joined`；`configure` 写入玩法、底分、倍率和风险积分；`start` 把房间状态改为 `playing` 并写入服务端开赛时间；`recordScore` 写入双方盘数和 `match_score_events`；`get` 读取房间状态；`previewSettlement` 只计算结算预览、不写库；`settle` 会计算积分、随机奖励、段位变化，写入 `settlements`、`points_ledger`、`member_points` 和 `matches.status`；`getSettlement` 读取已结算记录。
- `member`：生成球友端会员码，保存会员昵称、手机号、备注和头像。
- `staff`：处理员工写操作，写入 `table_sessions`、`member_points`、`points_ledger`、`matches`，并写入 `operation_logs`。
- `admin`：处理老板配置保存，先做服务端参数校验，再写入 `admin_configs`，并写入 `operation_logs`。
- `screen`：预留大屏数据和 `screenToken` 校验。

正式上线前必须补齐：

- 真实云环境验证 `match.start`、`match.recordScore`、`match.previewSettlement`、`match.settle` 的连续链路。
- 真实云环境验证 `player.getProfile`、`player.getRankings`、`player.getPointsPerks` 的只读链路和排行榜索引。
- 前端结算链路切换到 `match.previewSettlement`、`match.settle`、`match.getSettlement`。
- `screen_tokens` 大屏凭证。

初始化步骤见：

```text
docs/cloud-init-runbook.md
```
