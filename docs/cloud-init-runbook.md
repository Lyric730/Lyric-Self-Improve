# 云开发初始化运行手册

状态：v1.0
日期：2026-05-27

## 1. 目标

本手册用于第一次把小程序接入微信云开发环境。目标不是继续做页面，而是让后端权限链路能跑起来：

- 云函数能部署。
- 云数据库集合存在。
- 老板 OpenID 能写入 `store_members`。
- `staff` / `admin` 模块能按服务端角色判断权限。

## 2. 前置条件

- 微信开发者工具已经打开本项目。
- 项目目录：`F:\Making money\taiqiuxcx`
- 云函数根目录：`cloudfunctions/`
- 统一云函数：`cloudfunctions/yunhanApi`

## 3. 创建云开发环境

在微信开发者工具中执行：

1. 打开“云开发”。
2. 创建一个环境。
3. 记录环境 ID。
4. 确认 `project.config.json` 中已经有：

```json
{
  "cloudfunctionRoot": "cloudfunctions/"
}
```

第一版代码使用：

```js
cloud.init({
  env: cloud.DYNAMIC_CURRENT_ENV
});
```

这表示云函数会使用当前部署环境，不在代码里写死环境 ID。

## 4. 创建第一批集合

按顺序创建以下集合：

| 集合 | 必须性 | 用途 |
| --- | --- | --- |
| `store_members` | P0 | 门店角色与权限 |
| `operation_logs` | P0 | 员工和老板操作留痕 |
| `matches` | P0 | 房间和比赛状态 |
| `settlements` | P0 | 比赛结算结果 |
| `points_ledger` | P0 | 积分流水 |
| `member_points` | P0 | 会员积分账户余额 |
| `table_sessions` | P0 | 球桌当前开台到点时间 |
| `admin_configs` | P0 | 老板端门店参数配置 |
| `match_score_events` | P1 | 加减盘事件 |
| `screen_tokens` | P1 | 电视大屏访问凭证 |

字段说明见 `docs/cloud-database-schema.md`。

## 5. 建议索引

第一批至少创建：

```js
// store_members
{ storeId: 1, openid: 1, status: 1 }

// operation_logs
{ storeId: 1, module: 1, createdAt: -1 }

// matches
{ storeId: 1, status: 1, updatedAt: -1 }

// points_ledger
{ storeId: 1, openid: 1, createdAt: -1 }

// member_points
{ storeId: 1, openid: 1 }

// table_sessions
{ storeId: 1, tableId: 1, status: 1 }

// admin_configs
{ storeId: 1 }
```

## 6. 部署 `yunhanApi`

在微信开发者工具中：

1. 右键 `cloudfunctions/yunhanApi`。
2. 选择“上传并部署：云端安装依赖”。
3. 部署完成后，在云函数测试面板确认能调用。

如果工具提示依赖未安装，进入云函数目录安装：

```powershell
cd "F:\Making money\taiqiuxcx\cloudfunctions\yunhanApi"
npm install
```

也可以使用 CLI 部署。先检查云开发是否可用：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1
```

如果已经创建云环境，指定环境 ID 检查云函数：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID'
```

部署 `yunhanApi`，并让云端安装 `qrcode` 和 `wx-server-sdk` 依赖：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID' -Deploy
```

当前已验证的阻塞：如果 CLI 返回 `测试号不能使用云服务`，说明当前 AppID 是测试号。测试号不能做云开发部署，必须先切换到已注册小程序 AppID，再创建云环境。

## 7. 配置一次性初始化密钥

在云函数环境变量中配置：

```text
BOOTSTRAP_OWNER_SECRET=一串只用于初始化的长随机字符串
```

要求：

- 只用于第一次初始化老板账号。
- 不写入前端代码。
- 不写入公开文档。
- owner 初始化完成后，可以删除这个环境变量。

## 8. 获取当前微信 OpenID

在小程序调试器 Console 执行：

```js
wx.cloud.callFunction({
  name: "yunhanApi",
  data: {
    module: "auth",
    action: "whoami",
    payload: {
      storeId: "default"
    }
  }
}).then(console.log);
```

没有 `store_members` 记录时，返回角色应为：

```json
{
  "role": "player",
  "storeId": "default"
}
```

## 9. 初始化首个 owner

在小程序调试器 Console 执行一次：

```js
wx.cloud.callFunction({
  name: "yunhanApi",
  data: {
    module: "auth",
    action: "bootstrapOwner",
    payload: {
      storeId: "default",
      nickname: "云瀚老板",
      bootstrapSecret: "这里填 BOOTSTRAP_OWNER_SECRET"
    }
  }
}).then(console.log);
```

成功结果应包含：

```json
{
  "ok": true,
  "data": {
    "role": "owner",
    "storeId": "default"
  }
}
```

执行后会写入：

```json
{
  "storeId": "default",
  "openid": "当前微信 OpenID",
  "role": "owner",
  "status": "active",
  "nickname": "云瀚老板"
}
```

注意：

- 同一个门店已有 `active owner` 后，再执行会返回 `OWNER_ALREADY_EXISTS`。
- 这不是顾客端功能，不能做成页面按钮。
- 如果 `operationLogged` 为 `false`，说明 `operation_logs` 集合或写入权限需要补查，但 owner 记录已经写入。

## 10. 验证权限链路

### 10.1 验证 auth

```js
wx.cloud.callFunction({
  name: "yunhanApi",
  data: {
    module: "auth",
    action: "whoami",
    payload: {
      storeId: "default"
    }
  }
}).then(console.log);
```

期望：当前用户 `role` 为 `owner`。

### 10.2 验证 staff

```js
wx.cloud.callFunction({
  name: "yunhanApi",
  data: {
    module: "staff",
    action: "ping",
    payload: {
      storeId: "default"
    }
  }
}).then(console.log);
```

期望：`ok: true`。

### 10.3 验证 admin

```js
wx.cloud.callFunction({
  name: "yunhanApi",
  data: {
    module: "admin",
    action: "ping",
    payload: {
      storeId: "default"
    }
  }
}).then(console.log);
```

期望：`ok: true`。

## 11. 失败处理

| 错误码 | 含义 | 处理 |
| --- | --- | --- |
| `BOOTSTRAP_SECRET_NOT_CONFIGURED` | 云函数环境变量没配置 | 配置 `BOOTSTRAP_OWNER_SECRET` 后重新部署 |
| `BOOTSTRAP_SECRET_INVALID` | 初始化密钥错误 | 检查 Console 传入值 |
| `OWNER_ALREADY_EXISTS` | 当前门店已有老板 | 不需要重复初始化 |
| `PERMISSION_DENIED` | 当前 OpenID 不是允许角色 | 检查 `store_members` |

## 12. 不做的事

- 不把 owner 初始化做成小程序页面。
- 不把前端传入的 `role` 当成权限依据。
- 不把没有成员记录的用户默认设为老板。
- 不在代码中写死老板 OpenID。
