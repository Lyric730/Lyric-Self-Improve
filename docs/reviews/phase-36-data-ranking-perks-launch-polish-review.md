# Phase 36 数据、排行榜、积分礼遇上线化审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

P3 已修：排行榜第三个 Tab 原文为“好友榜”，不如“微信好友榜”准确。本轮已改为“微信好友榜”。

## Scope Check

本阶段只修改排行榜 Tab 数据标签，并更新计划、审查和开发日志。未修改页面结构或积分规则。

## Requirement Check

- 我的数据页展示当前段位、当前积分、星级进度、本赛季胜率、有效挑战数、连胜、店内/同段位/好友排名摘要。
- 排行榜页包含店内总榜、同段位榜、微信好友榜。
- 积分礼遇页展示当前积分、兑换门槛、开台赠分、前台兑换方式。
- 积分礼遇页不包含线上商城、抽奖或内部配置说明。

## Verification Evidence

```powershell
node --check miniprogram\services\player-service.js
node --check miniprogram\pages\my-data\my-data.js
node --check miniprogram\pages\rankings\rankings.js
node --check miniprogram\pages\points-perks\points-perks.js
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

结果：通过，包体 `740.3 KB` / `758056` bytes。

## Decision

通过。Stage 6 已完成，可进入 Stage 7：我的、员工端、老板端、大屏上线化。
