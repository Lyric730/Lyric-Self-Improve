# Phase 5 结算 / 不服 / 结果页审查

日期：2026-05-27

## Findings

### P2：结算仍是前端本地状态，正式上线前必须改为服务端结算

当前页面已经按流程参数计算胜负积分、随机奖励和加星，但这些数据仍来自前端状态和本地占位数据。正式上线前，结算必须由服务端完成，并带操作日志、幂等校验和双方确认记录。

处理：不阻塞当前页面打磨阶段。后端阶段必须把 `buildSettlement` 替换为接口返回结果。

### P2：随机奖励当前是确定性占位算法

当前为了让页面能跑通，使用奖励范围和本场参数生成一个稳定奖励值。正式上线前应由服务端按老板配置生成，并记录在比赛结算单里。

处理：不阻塞当前页面打磨阶段。页面文案不外显占位或模拟状态。

## Scope Check

本阶段只改动结算相关页面、比赛计分跳转参数、共享结算计算函数和页面流程文档：

- `miniprogram/pages/settlement/`
- `miniprogram/pages/refusal/`
- `miniprogram/pages/match-result/`
- `miniprogram/pages/match-scoring/match-scoring.js`
- `miniprogram/utils/ladder-data.js`
- `docs/design/player-flow-page-spec.md`

没有改动排行榜、员工端、老板端和大屏端。

## Requirement Check

- 结算页接收玩法、底分、倍率、风险积分、比分、赢家、已用时间。
- 赢家积分变化 = 风险积分 + 本场随机奖励。
- 输家积分变化 = 本场随机奖励 - 风险积分。
- 随机奖励统一一套标准，双方同享。
- 服了后进入结算结果页。
- 不服后进入退出本场 / 再战页。
- 结果页展示加分、扣分或净变化、随机奖励、加星。
- 页面没有出现 mock、模拟、演示、调试、临时、占位、PM、后台、服务器、模板等用户可见痕迹。

## Verification Evidence

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过。

```powershell
node scripts\check-json-files.js
```

结果：`JSON check OK (28 files checked)`。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：`Edge check OK (32 PNG assets checked)`。

```powershell
Select-String -Path miniprogram\pages\settlement\settlement.wxml,miniprogram\pages\refusal\refusal.wxml,miniprogram\pages\match-result\match-result.wxml -Pattern 'mock|模拟|演示|调试|临时|占位|PM|本页|负责|后台|服务器|模板' -SimpleMatch
```

结果：无匹配。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 `623.4 KB`。

```powershell
& 'F:\微信web开发者工具\cli.bat' auto --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121 --auto-port 9434 --trust-project
```

结果：通过，auto 服务可启动。

```powershell
node -e "const { buildSettlement } = require('./miniprogram/utils/ladder-data'); console.log(buildSettlement({ modeId: 'race5', base: 100, multiplier: 3, scoreA: 5, scoreB: 3, elapsed: 2520, elapsedText: '00:42:00', winner: 'a' }).winnerDelta)"
```

结果：`312`，对应风险积分 `300` + 本场随机奖励 `12`。

## Decision

修复后通过。可以进入 Phase 6：个人数据、排行榜、积分礼遇页上线级打磨。

