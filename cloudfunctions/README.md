# 云瀚台球小程序云函数

当前云函数根目录已在 `project.config.json` 中配置为：

```json
"cloudfunctionRoot": "cloudfunctions/"
```

## yunhanApi

`cloudfunctions/yunhanApi` 是第一版统一云函数入口：

- `auth`：读取微信 OpenID。
- `auth.bootstrapOwner`：使用云函数环境变量完成首个 owner 初始化，仅允许无 owner 门店执行一次。
- `match`：处理比赛房间、比赛查询和服务端结算；`createRoom` 创建等待房间；`joinRoom` 写入挑战方并把房间状态改为 `joined`；`get` 读取房间状态；`previewSettlement` 只计算结算预览、不写库；`settle` 会计算积分、随机奖励、段位变化，写入 `settlements`、`points_ledger`、`member_points` 和 `matches.status`；`getSettlement` 读取已结算记录。
- `member`：生成球友端会员码，保存会员昵称、手机号、备注和头像。
- `staff`：处理员工写操作，写入 `table_sessions`、`member_points`、`points_ledger`、`matches`，并写入 `operation_logs`。
- `admin`：处理老板配置保存，先做服务端参数校验，再写入 `admin_configs`，并写入 `operation_logs`。
- `screen`：预留大屏数据和 `screenToken` 校验。

正式上线前必须补齐：

- `matches` 后续状态机：玩法配置、开赛、计分事件和服务端计时。
- 服务端计时。
- 前端结算链路切换到 `match.previewSettlement`、`match.settle`、`match.getSettlement`。
- `screen_tokens` 大屏凭证。

初始化步骤见：

```text
docs/cloud-init-runbook.md
```
