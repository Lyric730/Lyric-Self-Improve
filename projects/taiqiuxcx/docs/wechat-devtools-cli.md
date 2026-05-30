# 微信开发者工具 CLI 使用记录

版本：v0.2  
项目目录：`F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx`  
工具路径：`F:\微信web开发者工具\cli.bat`  
当前服务端口：`55121`

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
HTTP 服务地址：http://127.0.0.1:55121
当前项目目录：F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx
```

已执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh islogin
```

结果：

```json
{"login":true}
```

含义：开发者工具服务端口可用，当前工具已登录。

## 3. 常用命令

检查登录态：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh islogin
```

打开当前项目并触发编译刷新：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh open --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx'
```

重建文件监听：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh reset-fileutils --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx'
```

预览：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx'
```

上传代码：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh upload --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' -v 0.1.0 -d 'UI Kit scaffold'
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
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID'
```

部署 `yunhanApi`，并让云端安装 npm 依赖：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID' -Deploy
```

注意：`-Deploy` 会写入云端，只有确认云环境 ID 正确时执行。

## 5. 当前阻塞

2026-05-27 执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh cloud env list --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx'
```

返回：

```text
测试号不能使用云服务
```

含义：当前导入的 AppID 仍被微信开发者工具识别为测试号，测试号不能使用云开发。要做真实云函数部署、数据库集合、会员码扫码闭环，必须先把项目切到已注册的小程序 AppID，并在开发者工具里开通云开发环境。

## 6. 后续使用纪律

- 改组件后先本地校验 JS / JSON。
- 再用 CLI `open --project` 或 `reset-fileutils` 刷新开发者工具。
- 如果需要真机看效果，再用 `preview`。
- 不在未确认版本号和说明时执行 `upload`。
