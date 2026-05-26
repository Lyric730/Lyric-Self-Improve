# 微信开发者工具 CLI 使用记录

版本：v0.1  
项目目录：`F:\Making money\taiqiuxcx-wechat`  
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
当前项目目录：F:\Making money\taiqiuxcx-wechat
当前 Git 分支：codex/taiqiuxcx-wechat
```

已执行：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh islogin
```

结果：

```json
{"login":false}
```

含义：开发者工具服务端口可用，但当前工具登录态失效，需要在微信开发者工具里重新登录。

## 3. 常用命令

检查登录态：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh islogin
```

打开当前项目并触发编译刷新：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh open --project 'F:\Making money\taiqiuxcx-wechat'
```

重建文件监听：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh reset-fileutils --project 'F:\Making money\taiqiuxcx-wechat'
```

预览：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh preview --project 'F:\Making money\taiqiuxcx-wechat'
```

上传代码：

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 55121 --lang zh upload --project 'F:\Making money\taiqiuxcx-wechat' -v 0.1.0 -d 'UI Kit scaffold'
```

上传命令只在明确要发体验版 / 提审前使用，日常扣组件不要随便上传。

## 4. 当前阻塞

现在 CLI 已连通，但 `open --project` 返回：

```text
需要重新登录 (code 10)
```

小刀老师需要在微信开发者工具里重新登录。登录后我可以继续用 CLI 打开项目、刷新编译、重建文件监听、生成预览码。

## 5. 后续使用纪律

- 改组件后先本地校验 JS / JSON。
- 再用 CLI `open --project` 或 `reset-fileutils` 刷新开发者工具。
- 如果需要真机看效果，再用 `preview`。
- 不在未确认版本号和说明时执行 `upload`。
