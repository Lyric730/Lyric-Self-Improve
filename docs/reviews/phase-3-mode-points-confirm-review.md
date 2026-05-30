# Phase 3 玩法与风险积分选择审查

日期：2026-05-27
范围：`mode-select`、`points-select`、`match-confirm`、`mode-card`、`ladder-data.js`、相关文档。

## Findings

### P2：参数仍停留在页面 query 和占位数据层

玩法、底分、倍率已经能从页面 A 传到页面 B / C，但还没有真实房间状态保存。用户刷新页面或多端同步时，参数不会从后端恢复。

处理：不阻塞 Phase 3。房间状态和后端接入阶段必须把 `modeId/base/multiplier/risk` 持久化到房间记录。

### P2：比赛计分页暂未接收 Phase 3 参数

`match-confirm` 已展示真实选择参数，但点击开始比赛后仍进入后续既有计分页。计分页参数接收、最低有效时间和风险积分联动属于 Phase 4 范围。

处理：不阻塞 Phase 3。Phase 4 必须继续接上。

## Scope Check

通过。

本阶段只改了：

- `mode-select`
- `points-select`
- `match-confirm`
- `mode-card`
- `ladder-data.js` 中的参数构造 helper
- Phase 3 相关文档

没有改动计分、结算、员工端、老板端。

## Requirement Check

通过。

- 抢 5、抢 7 当前开放，抢 10 展示为暂未开放。
- 玩法选择会把 `modeId` 传入底分页。
- 底分页会把底分、倍率、风险积分传入开局确认页。
- 开局确认页展示用户实际选择参数。
- 页面突出底分 × 倍率 = 风险积分。
- 页面突出普通随机奖励和续时冲刺奖励。
- 页面没有出现 mock、模拟、演示、调试、临时、PM、后台模板、服务器记录等用户可见痕迹。

## Verification Evidence

已执行：

```powershell
Select-String -Path miniprogram\pages\mode-select\mode-select.wxml,miniprogram\pages\points-select\points-select.wxml,miniprogram\pages\match-confirm\match-confirm.wxml,miniprogram\components\mode-card\mode-card.wxml -Pattern 'mock|模拟|演示|调试|临时|占位|PM|本页|负责|后台|服务器|模板|预留 / 锁定|未选中' -SimpleMatch
```

结果：无匹配输出。

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

结果：preview 通过，包体 `612.9 KB`。

## Decision

通过，进入 Phase 4。

后续必须处理：

- Phase 4：计分页接收并展示本场参数。
- 后端阶段：房间参数持久化和多端同步。

