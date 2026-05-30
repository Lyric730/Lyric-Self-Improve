# Phase 18 云开发部署前检查审查

日期：2026-05-27

## Findings

### P0：当前 AppID 是测试号，不能使用微信云开发

CLI 执行 `cloud env list` 返回：

```text
测试号不能使用云服务
```

这会阻塞真实云函数部署、云数据库集合创建、首个 owner 初始化、会员码真机扫码闭环。

处理：不能继续假设云端可用。必须先把项目切换到已注册小程序 AppID，并创建云开发环境。

### P1：后续部署必须使用云端安装依赖

`yunhanApi` 依赖 `qrcode`。云函数部署必须使用 `--remote-npm-install`，否则会员码生成可能在云端缺依赖。

处理：已把部署命令固化到 `scripts/check-wechat-cloud-readiness.ps1`。

## Scope Check

本阶段只处理云开发部署检查、CLI 文档、部署脚本和过程文档，没有继续改比赛结算或页面业务。

## Requirement Check

- 已确认微信开发者工具 CLI 登录态。
- 检查脚本会在 `{"login":false}` 时阻断，避免未登录状态下继续判断云环境。
- 已确认 `cloud` 子命令能力。
- 已新增可复用检查脚本。
- 已把测试号阻塞写入过程文档。

## Verification Evidence

已执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1
```

结果：脚本能完成登录态检查，并在云环境列表阶段返回阻塞提示：

```text
Cloud readiness blocked.
测试号不能使用云服务
```

已执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh islogin
```

结果：`{"login":true}`。

已执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' cloud functions deploy --help
```

结果：确认支持 `--env`、`--names`、`--remote-npm-install`。

已执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh cloud env list --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx'
```

结果：返回 `测试号不能使用云服务`。

阶段标准检查：

```powershell
node --check cloudfunctions\yunhanApi\index.js
```

结果：通过。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过，共 39 个 JS 文件。

```powershell
node scripts\check-json-files.js
```

结果：通过，共 33 个 JSON 文件。

```powershell
node scripts\check-production-copy.js
```

结果：通过，共 20 个文件。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：通过，共 32 个 PNG 资产。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 `667.9 KB` / `683961` bytes。

## Decision

Phase 18 作为部署前检查阶段归档，但真实云端闭环被 P0 阻塞。下一阶段不能继续做服务端结算，必须先切换正式 AppID 并创建云开发环境。
