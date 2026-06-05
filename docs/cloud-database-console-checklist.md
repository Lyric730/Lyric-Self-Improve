# 云数据库控制台执行清单

日期：2026-06-05

适用环境：`cloudbase-d9gg155lc1ee1d72e`

## 1. 创建集合

在微信开发者工具打开“云开发” -> “数据库”，逐个创建：

权限类型统一选择：**所有用户不可读写**。

原因：正式版不让小程序前端直接读写云数据库，全部通过 `yunhanApi` 云函数访问；角色、员工、老板权限都在云函数里判断。

| 顺序 | 集合 | 优先级 | 权限类型 | 创建后勾选 |
| --- | --- | --- | --- | --- |
| 1 | `store_members` | P0 | 所有用户不可读写 | [ ] |
| 2 | `operation_logs` | P0 | 所有用户不可读写 | [ ] |
| 3 | `matches` | P0 | 所有用户不可读写 | [ ] |
| 4 | `settlements` | P0 | 所有用户不可读写 | [ ] |
| 5 | `points_ledger` | P0 | 所有用户不可读写 | [ ] |
| 6 | `member_points` | P0 | 所有用户不可读写 | [ ] |
| 7 | `table_sessions` | P0 | 所有用户不可读写 | [ ] |
| 8 | `admin_configs` | P0 | 所有用户不可读写 | [ ] |
| 9 | `match_score_events` | P1 | 所有用户不可读写 | [ ] |
| 10 | `screen_tokens` | P1 | 所有用户不可读写 | [ ] |

## 2. 创建索引

在每个集合的“索引管理”中创建：

| 集合 | 索引字段 | 用途 | 勾选 |
| --- | --- | --- | --- |
| `store_members` | `storeId: 1, openid: 1, status: 1` | 角色查询 | [ ] |
| `operation_logs` | `storeId: 1, module: 1, createdAt: -1` | 操作日志 | [ ] |
| `matches` | `storeId: 1, status: 1, updatedAt: -1` | 异常列表 / 状态筛选 | [ ] |
| `matches` | `storeId: 1, roomNo: 1` | 房间码查询 | [ ] |
| `points_ledger` | `storeId: 1, openid: 1, createdAt: -1` | 积分流水 | [ ] |
| `member_points` | `storeId: 1, openid: 1` | 会员积分账户 | [ ] |
| `member_points` | `storeId: 1, balance: -1` | 店内总榜 | [ ] |
| `table_sessions` | `storeId: 1, tableId: 1, status: 1` | 球桌到点时间 | [ ] |
| `table_sessions` | `storeId: 1, status: 1` | 挑战首页开台检查 | [ ] |
| `admin_configs` | `storeId: 1` | 老板配置读取 | [ ] |
| `screen_tokens` | `storeId: 1, token: 1, status: 1` | 浏览器大屏凭证 | [ ] |

## 3. 配置云函数环境变量

在 `yunhanApi` 的环境变量中新增：

```text
BOOTSTRAP_OWNER_SECRET=<只用于初始化的一次性长随机字符串>
```

要求：

- 不写进代码。
- 不写进公开文档。
- owner 初始化完成后，可以删除或更换。

## 4. 初始化首个老板账号

1. 在开发者工具中切到小程序页面：`/pages/setup-owner/setup-owner`。
2. 确认页面显示当前 OpenID。
3. 输入 `BOOTSTRAP_OWNER_SECRET`。
4. 点击“初始化老板账号”。
5. 成功后确认页面显示“老板账号已绑定”。

## 5. 初始化后验证

| 验证项 | 期望 |
| --- | --- |
| `/pages/setup-owner/setup-owner` 刷新状态 | 当前角色为 `owner` |
| `store_members` | 有一条 `role = owner`、`status = active` 的记录 |
| 老板端保存配置 | `admin_configs` 写入或更新 |
| 员工端设置到点时间 | `table_sessions` 写入或更新 |
| 会员码页 | `member_points` 创建积分账户 |
| 前台积分核销 | `member_points` 扣分，`points_ledger` 写流水 |

## 6. 当前不能由 CLI 自动完成的事

微信开发者工具 CLI 当前只能管理云环境和云函数，不能直接创建集合、创建索引或调用云函数。以上集合、索引、环境变量和首次 owner 初始化，需要通过云开发面板和小程序页面完成。
