# Phase 56 Review：真实云环境绑定与云函数部署

日期：2026-06-05

## Findings

### P1：数据库集合、索引和首个 owner 尚未完成实证

本阶段已经确认云环境存在，并成功部署 `yunhanApi`；但还没有证明 `store_members`、`member_points`、`matches`、`admin_configs` 等集合和索引已经创建，也没有证明首个 owner 已初始化。

处理：不把集合和 owner 写成已完成。下一阶段必须按 `docs/cloud-init-runbook.md` 执行集合、索引、`BOOTSTRAP_OWNER_SECRET` 和 owner 初始化。

### P2：云函数默认超时时间为 3 秒

`cloud functions info` 显示 `yunhanApi` 当前 `timeout = 3`，运行时 `Nodejs16.13`。第一版接口大多是轻量读写，但 `member.getCode` 会生成二维码，后续真实调用时需要观察冷启动和生成耗时。

处理：先记录风险。真实调用如果出现超时，再在云开发控制台调整函数超时。

## 本阶段变更范围

- `miniprogram/app.js`
  - `wx.cloud.init()` 固定到 `cloudbase-d9gg155lc1ee1d72e`。
- `docs/cloud-init-runbook.md`
  - 写入真实云环境 ID。
  - 记录 2026-06-05 `yunhanApi` 部署结果。
- `docs/wechat-devtools-cli.md`
  - 写入真实云环境 ID、部署命令和函数状态。
- `docs/cloud-function-cutover-checklist.md`
  - 把云环境和云函数部署状态改为真实状态。
  - 集合、索引、owner 保持为待确认。

## 云端操作记录

只读检查：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh cloud env list --project 'F:\Making money\taiqiuxcx'
```

结果：

```text
* cloudbase-d9gg155lc1ee1d72e
```

首次部署：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh cloud functions deploy --project 'F:\Making money\taiqiuxcx' --env 'cloudbase-d9gg155lc1ee1d72e' --names 'yunhanApi' --remote-npm-install
```

结果：首次创建后云端处于 `Creating`，等待 35 秒后函数变为 `Active`。

最终部署：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh cloud functions deploy --project 'F:\Making money\taiqiuxcx' --env 'cloudbase-d9gg155lc1ee1d72e' --names 'yunhanApi' --remote-npm-install
```

结果：

```text
yunhanApi success: true
filesCount: 6
packSize: 17.8 KB
```

函数信息：

```text
status: Active
runtime: Nodejs16.13
timeout: 3
```

## 验证

- `cloud env list` 通过，返回 `cloudbase-d9gg155lc1ee1d72e`。
- `cloud functions deploy` 通过，`yunhanApi success = true`。
- `cloud functions info` 通过，`yunhanApi status = Active`。
- `powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId 'cloudbase-d9gg155lc1ee1d72e' -Port 30812` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`，包体 `841.4 KB / 861544 bytes`。

## 下一步

1. 创建云数据库集合和索引。
2. 配置 `BOOTSTRAP_OWNER_SECRET`。
3. 调用 `auth.whoami` 获取当前 OpenID。
4. 调用 `auth.bootstrapOwner` 初始化首个 owner。
5. 用真实云环境走一遍老板保存配置、员工设置到点时间、会员码生成、前台扫码核销。
