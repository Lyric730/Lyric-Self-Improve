# Phase 6 数据 / 排行榜 / 积分礼遇审查

日期：2026-05-27

## Findings

### P2：数据、榜单和积分余额仍是本地占位数据

当前页面已经按正式线上内容呈现，但数据仍来自 `ladder-data.js`。正式上线前必须接会员、比赛记录、积分流水和好友关系数据源。

处理：不阻塞当前页面打磨阶段。后端阶段必须替换为接口数据，并处理加载中、空状态和失败重试。

### P2：排行榜切换还没有远程分页和刷新

当前店内总榜、同段位榜、好友榜在前端本地切换。正式上线后，榜单需要按门店、赛季、段位、好友关系查询，并补分页或下拉刷新。

处理：不阻塞当前阶段，进入接口接入阶段处理。

## Scope Check

本阶段只改动：

- `miniprogram/pages/my-data/`
- `miniprogram/pages/rankings/`
- `miniprogram/pages/points-perks/`
- `miniprogram/utils/ladder-data.js`
- `docs/design/player-flow-page-spec.md`

没有改动比赛流程、员工端、老板端和大屏端。

## Requirement Check

- 我的数据页展示当前段位、星级、赛季胜率、有效挑战、连胜和三类排名摘要。
- 排行榜页包含店内总榜、同段位榜、微信好友榜，并可切换。
- 积分礼遇页展示当前积分、兑换门槛、开台赠分和前台兑换方式。
- 页面没有出现 mock、模拟、演示、调试、临时、占位、PM、后台、服务器、模板、MVP、后续、可调、维护等用户可见痕迹。

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
Select-String -Path miniprogram\pages\my-data\my-data.wxml,miniprogram\pages\rankings\rankings.wxml,miniprogram\pages\points-perks\points-perks.wxml -Pattern 'mock|模拟|演示|调试|临时|占位|PM|本页|负责|后台|服务器|模板|MVP|后续|可调|维护|个人端说明' -SimpleMatch
```

结果：无匹配。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：`Edge check OK (32 PNG assets checked)`。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 `625.7 KB`。

## Decision

通过。可以进入 Phase 7：员工端、老板端和电视大屏上线级打磨。

