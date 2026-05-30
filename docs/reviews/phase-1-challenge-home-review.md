# Phase 1 挑战首页上线级打磨审查

日期：2026-05-27
范围：`miniprogram/pages/challenge-home/`、`miniprogram/utils/ladder-data.js`、相关文档和验证脚本。

## 2026-05-27 修订说明

本审查最初允许首页展示“微信登录 / 店内定位 / 球桌开台”三项检查清单，这是错误口径。

正式上线首页不能展示内部检查清单，也不能出现 `FLOW`、`本页只做入口`、`已完成`、`待处理` 这类演示痕迹。修订后，检查逻辑只作为内部 gate，顾客只看到排位状态、发起挑战按钮和必要的失败提示。

## Findings

### P2：开局门槛仍是 mock 数据，不能作为正式防刷依据

当前 `challengeGate` 只在 `miniprogram/utils/ladder-data.js` 中模拟微信登录、100 米定位和球桌开台状态。它可以支撑页面结构和交互验收，但不能支撑正式上线的防刷、防店外开局。

处理：不阻塞 Phase 1。正式接入放到 Phase 8 / Phase 9 前的后端与权限阶段，必须替换为真实微信登录态、位置授权、门店地理围栏、球桌开台状态。

### P3：本机暂不能自动截取微信开发者工具模拟器画面

本阶段可通过 CLI preview 和自动化 WebSocket 确认页面路径，但当前 DevTools 截图接口不可用，无法自动完成像素级视觉验收。

处理：不阻塞 Phase 1。视觉细节仍需要用户提供模拟器截图，或后续单独补可用截图链路。

## Scope Check

通过。

本阶段只改了：

- 上线级执行文档与阶段规则。
- JSON 验证脚本。
- 挑战首页开局检查、入口状态和页面规格。
- 共享 mock 中的首页开局状态。

没有改动玩法选择、计分、结算、员工端、老板端。

## Requirement Check

通过。

- 首页展示门店、球桌、开台到点时间。
- 首页展示当前段位，并保留“全部游戏模式共用一个段位”的说明。
- 首页不展示内部检查清单，只展示排位状态和发起挑战按钮。
- 主按钮由内部 gate 计算 `canStartChallenge`，条件不足时禁用。
- 首页没有展示底分、倍率、比赛计分器、结算明细。
- 页面流程规格已补充“挑战首页上线级要求”。

## Verification Evidence

2026-05-27 修订后重新执行：

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过，无语法错误输出。

```powershell
node scripts\check-json-files.js
```

结果：`JSON check OK (28 files checked)`。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：`Edge check OK (32 PNG assets checked)`。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：preview 通过，包体 `604.9 KB`。

```powershell
& 'F:\微信web开发者工具\cli.bat' auto --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121 --auto-port 9434 --trust-project
```

结果：auto 通过。

自动化 WebSocket 检查：

```text
currentPage.path = pages/challenge-home/challenge-home
```

修订前执行记录：

已执行：

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过，无语法错误输出。

```powershell
node scripts\check-json-files.js
```

结果：`JSON check OK (28 files checked)`。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：`Edge check OK (32 PNG assets checked)`。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：preview 通过，包体 `605.5 KB`。

```powershell
& 'F:\微信web开发者工具\cli.bat' auto --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121 --auto-port 9434 --trust-project
```

结果：auto 通过。

自动化 WebSocket 检查：

```text
currentPage.path = pages/challenge-home/challenge-home
```

补充：尝试使用 `miniprogram-automator` 读取页面 data 时，本项目未安装该依赖，命令失败于 `Cannot find module 'miniprogram-automator'`。本阶段改用 DevTools WebSocket 协议确认当前页面路径。

## Decision

通过，进入 Phase 2 前无需返工。

后续必须处理：

- Phase 2：等待 / 接受挑战流程上线级打磨。
- 后端集成阶段：把首页 mock 检查替换成真实登录、定位、开台状态。
- 视觉验收阶段：继续依赖用户提供微信开发者工具截图，直到找到稳定截图链路。

