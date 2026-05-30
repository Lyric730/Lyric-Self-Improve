# 云瀚台球小程序云函数

当前云函数根目录已在 `project.config.json` 中配置为：

```json
"cloudfunctionRoot": "cloudfunctions/"
```

## yunhanApi

`cloudfunctions/yunhanApi` 是第一版统一云函数入口：

- `auth`：读取微信 OpenID。
- `auth.bootstrapOwner`：使用云函数环境变量完成首个 owner 初始化，仅允许无 owner 门店执行一次。
- `match`：预留房间状态和服务端结算。
- `member`：生成球友端会员码。
- `staff`：处理员工写操作，写入 `table_sessions`、`member_points`、`points_ledger`、`matches`，并写入 `operation_logs`。
- `admin`：处理老板配置保存，写入 `admin_configs`，并写入 `operation_logs`。
- `screen`：预留大屏数据和 `screenToken` 校验。

正式上线前必须补齐：

- `matches` 房间状态机。
- 服务端计时。
- 服务端结算。
- `screen_tokens` 大屏凭证。

初始化步骤见：

```text
docs/cloud-init-runbook.md
```
