# Phase 19 结算规则纯函数与本地测试审查

日期：2026-06-01

## Findings

### P1：云函数结算仍未启用

本阶段只完成本地规则引擎和前端展示接入，`cloudfunctions/yunhanApi` 的 `match.settle` 仍然返回 `SETTLEMENT_NOT_READY`。

处理：等待云环境创建后，把同一套规则接入云函数，并写入 `settlements`、`points_ledger`、`rank_states`。

### P1：当前规则测试不能覆盖数据库并发

本地测试能证明公式正确，但不能证明同一场比赛不会重复结算、不会并发扣分、不会重复加星。

处理：云环境可用后必须增加服务端幂等键和结算状态校验。

### P2：小程序端和云函数端暂未共享同一份物理文件

当前规则引擎位于 `miniprogram/utils/settlement-engine.js`，前端展示已接入。云函数部署包不能直接引用 `miniprogram` 目录外的文件。

处理：云端接入时要么复制规则引擎并加一致性测试，要么建立构建脚本同步规则文件。

## Scope Check

本阶段只处理结算公式、段位星级规则、本地测试和前端展示接入，没有继续推进云数据库写入。

## Requirement Check

- 抢 5 / 抢 7 / 抢 10 模板规则可计算。
- 底分、倍率、随机奖励公式可测试。
- 最低有效时间不足会阻断结算。
- 第 4 大局可进入续时冲刺奖励。
- 青铜到黄金保护，铂金以上掉星。
- 前端现有 `buildSettlement` 已改为调用规则引擎。

## Verification Evidence

```powershell
node scripts\test-settlement-engine.js
```

结果：`Settlement engine tests OK`。

```powershell
node --check miniprogram\utils\settlement-engine.js
node --check miniprogram\utils\ladder-data.js
node --check miniprogram\services\match-service.js
```

结果：通过。

```powershell
node -e "const { buildSettlement } = require('./miniprogram/utils/ladder-data'); const result = buildSettlement({ modeId: 'race5', base: 100, multiplier: 3, scoreA: 5, scoreB: 3, winner: 'a', reward: 120, elapsed: 2530 }); console.log(JSON.stringify({ riskPoints: result.riskPoints, winnerDelta: result.winnerDelta, loserDelta: result.loserDelta, rewardValue: result.rewardValue, rewardPhase: result.rewardPhase }, null, 2));"
```

结果：

```json
{
  "riskPoints": 300,
  "winnerDelta": 420,
  "loserDelta": -180,
  "rewardValue": 120,
  "rewardPhase": "normal"
}
```

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\taiqiuxcx' --port 49663 --lang zh
```

结果：通过，包体 `679.1 KB` / `695420` bytes，使用 AppID `wxe30b469d64636a2b`。

## Decision

Phase 19 可归档。本阶段提升了规则可验证性，但不能替代云端结算。下一阶段在云环境可用前，可继续做页面异常态、管理员参数校验、榜单数据结构；云环境可用后优先接 `match.settle` 写库。
