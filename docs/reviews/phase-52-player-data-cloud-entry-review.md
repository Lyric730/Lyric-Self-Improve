# Phase 52 球友赛后展示数据服务化审查
日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 已处理风险：`my-data`、`rankings`、`points-perks` 不再在页面模块加载时直接从本地样例数据同步取值，页面进入后通过异步服务层读取正式数据，并展示加载、失败、重试和空榜状态。

P1 已处理风险：`player-service` 已改为云函数优先读取。DevTools 云环境不可用时才使用本地视觉兜底；正式环境云函数失败会返回错误态，不静默展示样例数据。

P1 已处理风险：云函数新增 `player` 模块，提供 `getProfile`、`getRankings`、`getPointsPerks` 三个球友端读取入口。

P1 已处理风险：排行榜读取由 `member_points` 积分账户生成店内总榜和同段位榜；微信好友榜在好友关系模型未接入前返回正式空状态，不展示假的好友数据。

P1 已处理风险：个人数据页的赛季胜率、有效局数、店内排名、同段位排名从服务端读取和计算壳层输出，不再依赖纯前端静态样例。

P1 已处理风险：积分礼遇页从店铺积分配置读取开台赠分和兑换门槛，前台兑换说明保留为正式业务文案。

P2 残余风险：真实云环境尚未创建，`member_points` 的 `{ storeId: 1, balance: -1 }` 排行榜索引需要明天在真实云数据库中创建并验证。

P2 残余风险：当前赛季数据用最近结算记录扫描后本地过滤计算，只适合第一版壳层。正式运营后需要增加按 `openid + storeId + seasonId` 查询的统计表或聚合任务。

P2 残余风险：当前 `getPlayerIdentity()` 会在账户不存在时通过 `ensureMemberPointAccount()` 创建初始积分账户。这个行为符合“新会员首次进入即建档”的方向，但真实云环境上线前仍需确认是否要把建档动作限定到登录或开台节点。

## Scope Check

本阶段只处理球友赛后展示数据读取链路，不改积分公式、不改结算写入、不改段位规则、不新增好友关系模型。

- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/README.md`
- `miniprogram/services/player-service.js`
- `miniprogram/pages/my-data/my-data.js`
- `miniprogram/pages/my-data/my-data.wxml`
- `miniprogram/pages/rankings/rankings.js`
- `miniprogram/pages/rankings/rankings.wxml`
- `miniprogram/pages/points-perks/points-perks.js`
- `miniprogram/pages/points-perks/points-perks.wxml`
- `miniprogram/pages/my-hub/my-hub.js`
- `miniprogram/styles/player-flow.wxss`
- `docs/api-service-layer-contract.md`
- `docs/cloud-function-cutover-checklist.md`
- `docs/cloud-database-schema.md`
- `docs/cloud-init-runbook.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 新增云函数 `player.getProfile`。
- 新增云函数 `player.getRankings`。
- 新增云函数 `player.getPointsPerks`。
- 球友个人数据页通过 `player-service.getPlayerProfile()` 读取。
- 排行榜页通过 `player-service.getRankingTabs()` 读取。
- 积分礼遇页通过 `player-service.getPointsPerks()` 读取。
- DevTools 无云环境时保留本地视觉兜底。
- 正式环境云函数失败时展示失败态和重试入口。
- 微信好友榜在好友关系未接入前展示空状态，不制造假数据。
- 文档补充 `member_points` 排行榜索引要求。

## Verification Evidence

最终验证命令：

```powershell
git diff --check
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

验证结果：

- `Ops service fallback tests OK`
- `Settlement engine tests OK`
- `Admin config validator tests OK`
- `Member profile tests OK`
- `Cloud contract tests OK`
- `Service layer boundary check OK`
- `JSON check OK (35 files checked)`
- `Production copy check OK (21 files checked)`
- `Player flow route check OK`
- `Edge check OK (32 PNG assets checked)`
- Mini-program JS syntax check 通过。
- Cloud function JS syntax check 通过。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`。
- 包体 `821.0 KB / 840711 bytes`。
- 最终输出 `Launch verification OK`。

## Decision

本阶段可提交。下一阶段建议继续迁移电视大屏和首页非比赛入口数据，减少正式页面对本地静态样例的依赖。
