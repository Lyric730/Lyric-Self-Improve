# Phase 42 云函数比赛结算链路审查

日期：2026-06-03

## Findings

未发现 P0 / P1 代码语法问题。

P1 残余风险：`match.settle` 目前不是事务级写入。已先写 `settlements.status = settling` 作为结算锁，再写积分和流水，最后改为 `settled`；但真实并发、云函数中途失败、重复点击仍必须在云环境创建后实测。

P2 残余风险：前端 `match-service.calculateSettlement` 尚未切换为云函数异步接口。当前阶段只准备云函数结算能力，不改结算页 / 不服页 / 结果页的同步页面流程。

## Scope Check

本阶段只处理云函数侧结算能力和本地契约测试，不改球友端页面流程。

- 新增 `cloudfunctions/yunhanApi/settlement-engine.js`
- 新增 `cloudfunctions/yunhanApi/match-settlement.js`
- 更新 `cloudfunctions/yunhanApi/index.js`
- 更新 `scripts/test-cloud-contracts.js`
- 更新云函数、接口契约、切换清单和执行计划文档

## Requirement Check

- 云函数包内已有结算规则引擎，不依赖 `miniprogram` 外部目录。
- `match.settle` 会拒绝缺少 `matchId`、比赛不存在、重复结算、双方身份缺失、积分账户缺失、余额不足。
- 结算写入 `settlements`，并用 `settling -> settled` 表示写入阶段。
- 积分变化写入 `member_points` 和 `points_ledger`，胜方类型为 `match_win`，败方类型为 `match_loss`。
- 比赛状态更新为 `matches.status = settled`。
- 小程序侧和云函数侧结算公式通过 `scripts/test-cloud-contracts.js` 做一致性验证。

## Verification Evidence

```powershell
node scripts\test-cloud-contracts.js
node --check cloudfunctions\yunhanApi\index.js
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

结果：统一验证通过，输出 `Launch verification OK`；微信预览包体 `748.8 KB` / `766759` bytes。

## Decision

通过，可提交。下一阶段建议做前端结算链路异步化，或等云环境创建后优先部署 `yunhanApi` 并做真实云数据库重复结算测试。
