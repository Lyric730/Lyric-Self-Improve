# 微信开发者工具 CLI 使用记录

版本：v0.3

项目目录：`F:\Making money\taiqiuxcx`

工具路径：`F:\微信web开发者工具\cli.bat`
当前服务端口：`30812`
当前 AppID：`wxe30b469d64636a2b`
当前云环境：`cloudbase-d9gg155lc1ee1d72e`

## 1. 官方文档结论

官方文档说明：开发者工具提供命令行和 HTTP 服务两种接口，可用于登录、预览、上传等操作。使用命令行前，需要在开发者工具的设置 -> 安全设置中开启服务端口。

官方命令行工具路径：

```text
Windows: <安装路径>/cli.bat
```

本机实际路径：

```text
F:\微信web开发者工具\cli.bat
```

## 2. 当前本机状态

已确认：

```text
HTTP 服务地址：http://127.0.0.1:30812
当前项目目录：F:\Making money\taiqiuxcx
当前 AppID：wxe30b469d64636a2b
```

已执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh islogin
```

结果：

```json
{"login":true}
```

含义：开发者工具服务端口可用，当前工具已登录。

## 3. 常用命令

检查登录态：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh islogin
```

打开当前项目并触发编译刷新：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh open --project 'F:\Making money\taiqiuxcx'
```

重建文件监听：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh reset-fileutils --project 'F:\Making money\taiqiuxcx'
```

预览：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```

上传代码：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh upload --project 'F:\Making money\taiqiuxcx' -v 0.1.0 -d 'UI Kit scaffold'
```

上传命令只在明确要发体验版 / 提审前使用，日常扣组件不要随便上传。

## 4. 云开发 CLI

当前本机工具支持云开发命令：

```powershell
& 'F:\微信web开发者工具\cli.bat' cloud --help
& 'F:\微信web开发者工具\cli.bat' cloud env --help
& 'F:\微信web开发者工具\cli.bat' cloud functions --help
```

只读检查：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1
```

指定云环境后检查 `yunhanApi`：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId 'cloudbase-d9gg155lc1ee1d72e'
```

部署 `yunhanApi`，并让云端安装 npm 依赖：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId 'cloudbase-d9gg155lc1ee1d72e' -Deploy
```

注意：`-Deploy` 会写入云端，只有确认云环境 ID 正确时执行。

## 5. 当前云开发状态

2026-05-27 执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh cloud env list --project 'F:\Making money\taiqiuxcx'
```

返回：

```text
测试号不能使用云服务
```

历史含义：旧 AppID 被微信开发者工具识别为测试号，测试号不能使用云开发。

当前处理：`project.config.json` 已切换到正式 AppID `wxe30b469d64636a2b`。后续需要用 CLI 打开当前项目，并重新执行云开发检查。

2026-05-31 更新：

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\taiqiuxcx' --port 55121 --lang zh
```

结果：

```text
使用 AppID: wxe30b469d64636a2b
preview
```

说明：项目身份已切换到正式 AppID。

2026-06-03 更新：开发者工具当前实际监听端口变为 `30812`。继续用旧端口会提示需要重启工具，因此后续 CLI 命令默认使用 `30812`。

继续执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1
```

结果：

```text
ret:1000
errmsg:"system error."
```

说明：已经不是测试号阻塞。下一步需要在微信开发者工具 UI 里打开“云开发”，确认是否已创建云环境，以及当前登录微信号是否有云开发权限。

2026-06-05 更新：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh cloud env list --project 'F:\Making money\taiqiuxcx'
```

结果：

```text
* cloudbase-d9gg155lc1ee1d72e
```

部署 `yunhanApi`：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh cloud functions deploy --project 'F:\Making money\taiqiuxcx' --env 'cloudbase-d9gg155lc1ee1d72e' --names 'yunhanApi' --remote-npm-install
```

结果：部署成功，`filesCount = 6`，`packSize = 17.8 KB`。函数信息：

```text
yunhanApi status: Active
runtime: Nodejs16.13
timeout: 3
```

## 6. 后续使用纪律

- 改组件后先本地校验 JS / JSON。
- 再用 CLI `open --project` 或 `reset-fileutils` 刷新开发者工具。
- 如果需要真机看效果，再用 `preview`。
- 不在未确认版本号和说明时执行 `upload`。
