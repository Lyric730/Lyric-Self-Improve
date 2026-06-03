# Phase 34 玩法、底分倍率、开局确认上线化审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

P2 已修：底分倍率页虽已使用卡片式选择，但随机奖励机制不够突出。本轮已在风险积分模块下方增加普通随机奖励和续时冲刺奖励预览。

P2 已修：开局确认页缺少双方玩家信息。本轮已补充发起方和挑战方卡片，避免确认页只剩参数。

## Scope Check

本阶段只修改 `points-select` 和 `match-confirm` 页面，没有改动规则计算、模式配置或结算引擎。

## Requirement Check

- 玩法选择页继续传递 `modeId`。
- 底分倍率页继续传递 `base / multiplier / risk`。
- 底分倍率页展示 `底分 × 倍率 = 风险积分`。
- 底分倍率页展示普通随机奖励和续时冲刺奖励范围。
- 开局确认页展示双方、玩法、底分、倍率、风险积分、最低有效时间、胜方加星。
- 页面可见文案未出现 PM、mock、演示、内部校验等上线禁用表达。

## Verification Evidence

```powershell
node --check miniprogram\pages\mode-select\mode-select.js
node --check miniprogram\pages\points-select\points-select.js
node --check miniprogram\pages\match-confirm\match-confirm.js
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
git diff --check -- miniprogram\pages\points-select\points-select.wxml miniprogram\pages\points-select\points-select.wxss miniprogram\pages\match-confirm\match-confirm.wxml miniprogram\pages\match-confirm\match-confirm.wxss
```

结果：通过，仅有既有 CRLF 提示，无阻断错误。

```powershell
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```

结果：通过，包体 `739.6 KB` / `757339` bytes。

## Decision

通过。Stage 4 已完成，可进入 Stage 5：计分、时间不足、结算链路上线化。
