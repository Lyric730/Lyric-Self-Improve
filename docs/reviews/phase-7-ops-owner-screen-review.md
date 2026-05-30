# Phase 7 员工端 / 老板端 / 大屏审查

日期：2026-05-27

## Findings

### P1：员工端和老板端还没有权限校验

当前已新增前台工作台和门店参数页，但任何可访问这些路由的人都能看到页面。正式上线前必须接入角色权限，员工只能进员工端，老板或管理员才能进老板端。

处理：当前阶段只完成页面骨架，不阻塞页面打磨；上线前必须修复。

### P1：员工操作和老板配置还没有服务端操作日志

员工核销积分、作废异常、老板保存配置都必须落服务端日志。当前页面只保留正式动作入口，没有真实写入。

处理：接口阶段必须补操作日志、确认弹窗、失败回滚提示。

### P2：电视网页大屏数据仍是静态内容

`screen/yunhan-tv-ranking.html` 已具备 16:9 大屏结构和 60 秒自动刷新，但数据仍是静态内容。正式上线前需要接大屏数据接口和 `screenToken`。

处理：不阻塞当前页面结构阶段。

### 已修复：`ui-kit` 不能进入正式页面列表

复查时发现 `pages/ui-kit/ui-kit` 仍在 `app.json` 中。该页面是开发验收台，不能作为正式小程序可访问路由打包。

处理：已从 `miniprogram/app.json` 移除，文件保留在仓库内用于开发验收。

## Scope Check

本阶段新增或改动：

- `miniprogram/pages/staff-desk/`
- `miniprogram/pages/boss-config/`
- `miniprogram/pages/tv-ranking/`
- `screen/yunhan-tv-ranking.html`
- `miniprogram/app.json`
- `miniprogram/utils/ladder-data.js`
- `docs/design/ops-owner-screen-page-spec.md`

没有改动球友端挑战主流程。

## Requirement Check

- 员工端只保留今日球桌、开台到点、积分核销、异常比赛。
- 员工端没有底分、倍率、随机奖励、段位规则配置。
- 老板端按玩法模板、积分补给、防刷分、大屏榜单分组。
- 大屏包含门店名、赛季、前三名、店内总榜、赏金猎人榜、活动位。
- 小程序大屏页和静态网页大屏都加入 60 秒刷新行为。
- `ui-kit` 已从正式页面列表移除。
- 页面没有出现 mock、模拟、演示、调试、临时、占位、PM、后台、服务器、模板、MVP、后续、可调、维护等用户可见痕迹。

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
Select-String -Path miniprogram\pages\staff-desk\staff-desk.wxml,miniprogram\pages\boss-config\boss-config.wxml,miniprogram\pages\tv-ranking\tv-ranking.wxml,screen\yunhan-tv-ranking.html -Pattern 'mock|模拟|演示|调试|临时|占位|PM|本页|负责|后台|服务器|模板|MVP|后续|可调|维护' -SimpleMatch
```

结果：无匹配。

```powershell
$app = Get-Content -Encoding UTF8 -Raw 'miniprogram/app.json' | ConvertFrom-Json
$files = @('miniprogram/app.json') + ($app.pages | ForEach-Object { "miniprogram/$_.wxml" })
Select-String -Path $files -Pattern 'mock|模拟|演示|调试|临时|占位|PM|本页|负责|后台|服务器|模板|MVP|后续|可调|维护|个人端说明' -SimpleMatch
```

结果：正式页面列表无匹配。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：`Edge check OK (32 PNG assets checked)`。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 `628.0 KB`。

## Decision

修复后通过页面骨架阶段。进入后端和权限阶段前，P1 权限校验、操作日志、接口写入必须补齐。

