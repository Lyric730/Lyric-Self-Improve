# Phase 8 权限与操作留痕审查

日期：2026-05-27

## Findings

### P1：服务端权限校验仍未接入

当前已新增前端角色拦截，员工端、老板端、小程序大屏页进入前会检查角色；但正式上线不能只依赖前端。后续接口层必须再次校验角色，防止普通用户直接调用员工或老板接口。

处理：前端已完成第一道拦截；服务端权限校验进入接口阶段 P0。

### P1：操作日志当前仍是本地记录

员工设置到点时间、积分核销、异常作废，老板保存配置已经统一写入 `operation-log` 入口；但当前记录仍在本地存储。正式上线必须写入服务端 `operation_logs`，并带操作者、门店、设备、接口结果和失败原因。

处理：前端入口已补齐；服务端落库进入接口阶段 P0。

### 已修复：未授权页面可能短暂渲染内容

首次实现只在 `onLoad` 做跳转，未授权用户可能在重定向前短暂看到员工端或老板端内容。已给员工端、老板端、小程序大屏页根节点增加 `accessReady` 条件，权限未通过前不渲染页面主体。

处理：已修复。

### P2：静态电视网页仍未接入 screenToken

小程序内大屏页已增加角色拦截；但 `screen/yunhan-tv-ranking.html` 是给小米电视浏览器打开的网页，仍需要后续接入 `screenToken` 和大屏接口。

处理：记录到接口阶段，不阻塞当前前端权限入口。

## Scope Check

本阶段新增或改动：

- `miniprogram/utils/access-control.js`
- `miniprogram/utils/operation-log.js`
- `miniprogram/utils/ladder-data.js`
- `miniprogram/pages/staff-desk/`
- `miniprogram/pages/boss-config/`
- `miniprogram/pages/tv-ranking/`
- `miniprogram/pages/points-perks/`
- `docs/backend-integration-readiness-plan.md`
- `docs/design/ops-owner-screen-page-spec.md`
- `docs/design/player-flow-page-spec.md`
- `docs/launch-readiness-execution-plan.md`
- `AGENTS.md`
- `scripts/check-production-copy.js`

没有改动球友端比赛主流程。

## Requirement Check

- 员工端进入前检查员工或老板角色。
- 老板端进入前检查老板角色。
- 小程序大屏页进入前检查员工、老板或大屏角色。
- 权限未通过前，受保护页面主体不渲染。
- 员工端关键动作进入统一操作日志入口。
- 老板端保存配置进入统一操作日志入口。
- 正式页面列表可见文案没有出现内部校验、PM 说明、演示状态、mock、模拟、调试、临时、占位等痕迹。
- 共享本地数据文件已从 `ladder-mock.js` 改名为 `ladder-data.js`。
- 正式页面文案检查已沉淀为固定脚本，后续阶段收尾必须运行。

## Verification Evidence

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过。

```powershell
node scripts\check-json-files.js
```

结果：`JSON check OK (31 files checked)`。

```powershell
node --check scripts\check-production-copy.js
```

结果：通过。

```powershell
node scripts\check-production-copy.js
```

结果：`Production copy check OK (19 files checked)`。

```powershell
$app = Get-Content -Encoding UTF8 -Raw 'miniprogram/app.json' | ConvertFrom-Json
$files = @('miniprogram/app.json') + ($app.pages | ForEach-Object { "miniprogram/$_.wxml" })
Select-String -Path $files -Pattern 'mock|模拟|演示|调试|临时|占位|PM|本页|负责|后台|服务器|模板|MVP|后续|可调|维护|个人端说明|内部校验|演示状态' -SimpleMatch
```

结果：正式页面列表无匹配。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：`Edge check OK (32 PNG assets checked)`。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 `634.4 KB`。

## Decision

前端权限拦截和操作日志入口修复后通过。下一阶段应进入接口层：服务端权限、服务端操作日志、房间状态机、服务端计时和服务端结算。
