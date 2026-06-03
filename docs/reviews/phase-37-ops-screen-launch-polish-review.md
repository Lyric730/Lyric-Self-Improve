# Phase 37 我的、员工端、老板端、大屏上线化审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

P2 残余风险：当前云环境尚未创建，会员码、前台扫码核销、到点时间保存、异常作废在微信开发者工具中使用本地兜底；正式上线前必须由云函数返回真实会员二维码并落库积分流水、球桌到点时间和异常处理记录。

## Scope Check

本阶段只处理运营入口与大屏链路：

- 我的页：保持个人资料编辑、会员工具、员工 / 老板 / 大屏入口。
- 前台页：只保留今日球桌到点时间、积分核销、异常比赛三类高频动作。
- 老板页：参数可输入、校验、保存，并增加本地持久化，刷新后不丢。
- 大屏页：读取老板端大屏配置，并加入横屏舞台层，避免继续按手机窄屏挤压榜单。
- 会员码页：云函数优先，DevTools 无云环境时显示本地视觉码，避免页面失败。

未修改比赛积分规则、段位规则和球友主流程。

## Requirement Check

- “我的”页已包含可编辑资料：昵称、手机号、备注、头像图片。
- 员工端未增加复杂后台功能，仍然只处理开台到点、积分核销、异常作废。
- 老板端玩法模板、积分补给、防刷分、大屏配置均可编辑，保存后写入本地缓存。
- 大屏主榜、副榜、刷新文案从老板端配置读取；电视宽屏下使用三栏横屏舞台。
- 正式页面未出现 PM、mock、演示、调试、内部校验等用户可见文案。

## Verification Evidence

```powershell
node --check miniprogram\services\admin-service.js
node --check miniprogram\services\staff-service.js
node --check miniprogram\services\member-service.js
node --check miniprogram\services\screen-service.js
node --check miniprogram\pages\staff-desk\staff-desk.js
node --check miniprogram\pages\tv-ranking\tv-ranking.js
node --check miniprogram\pages\member-code\member-code.js
```

结果：通过。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
node scripts\check-json-files.js
node scripts\check-production-copy.js
node scripts\check-player-flow-routes.js
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：全部通过。

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```

结果：通过，包体 `747.4 KB` / `765348` bytes。

## Decision

通过。Stage 7 已完成，可进入下一阶段：全流程手工走查、真实页面视觉问题记录、云函数接入前置清单。
