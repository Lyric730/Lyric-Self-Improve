# Phase 4 比赛计分与时间规则审查

日期：2026-05-27
范围：`match-scoring`、`time-insufficient`、`match-confirm`、相关文档。

## Findings

### P2：计时与比分仍是单端页面状态

当前 `elapsedSeconds`、`scoreA`、`scoreB` 存在小程序页面内。页面表现已经符合正式规则，但正式上线必须由房间状态同步，避免双方手机不同步、退出页面丢状态、争议比分无法追溯。

处理：不阻塞 Phase 4。后端接入阶段必须引入房间状态、操作记录和服务端时间。

### P2：结算页暂未接收 Phase 4 参数

计分页在满足目标盘数和最低时间后会携带参数进入结算页，但结算页仍是后续旧实现。结算参数接收和服 / 不服链路属于 Phase 5。

处理：不阻塞 Phase 4。Phase 5 继续接上。

## Scope Check

通过。

本阶段只改了：

- `match-confirm` 开始比赛参数传递。
- `match-scoring` 计分、正向计时、最低有效时间检查。
- `time-insufficient` 时间不足提示。
- Phase 4 相关文档。

没有改动结算、排行榜、员工端、老板端。

## Requirement Check

通过。

- 计分页接收玩法、底分、倍率、风险积分。
- 正向计时从 `00:00:01` 开始。
- 双方都能加减盘数。
- 达到目标盘数后先检查最低有效时间。
- 未满最低有效时间进入时间不足页。
- 时间不足页没有结算按钮，只提供继续计分、先去续时。
- 页面没有出现 mock、模拟、演示、调试、临时、后台、服务器、模板等用户可见痕迹。

## Verification Evidence

已执行：

```powershell
Select-String -Path miniprogram\pages\match-scoring\match-scoring.wxml,miniprogram\pages\time-insufficient\time-insufficient.wxml -Pattern 'mock|模拟|演示|调试|临时|占位|PM|本页|负责|后台|服务器|模板' -SimpleMatch
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

结果：preview 通过，包体 `616.5 KB`。

## Decision

通过，进入 Phase 5。

后续必须处理：

- Phase 5：结算页接收并展示真实参数。
- 后端阶段：比分、计时、操作记录服务端同步。
