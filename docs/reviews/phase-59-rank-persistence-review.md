# Phase 59 结算段位持久化审查

日期：2026-06-09

## 结论

本阶段可归档。`match.settle` 已经从服务端会员档案读取双方当前段位，并在结算成功后把双方最新 `rankState / rankTitle` 写回 `store_members`。这补齐了个人端段位、同段位榜和下一场段位清算需要的持久化基础。

## 已处理风险

### P1：段位只算不存

此前 `match.settle` 会返回 `rankChanges`，但没有写回会员档案。用户下一次进入个人页或排行榜时，只能读到旧段位或默认段位。

处理：新增 `applyRankStateUpdates()`，在积分写账后更新双方 `store_members.rankState / rankTitle / lastRankUpdatedAt`，并把写回结果记录到 `settlements.rankResults`。

### P1：前端可影响当前段位输入

此前结算 payload 支持前端传入 `rankStateA / rankStateB`。正式上线时，段位属于比赛资产，不能相信前端。

处理：`buildCloudSettlementPayload()` 改为在云函数内读取 `store_members.rankState`，再传入结算规则引擎。前端传来的段位不会作为最终依据。

### P2：角色字段被段位更新覆盖

段位写回时不能把已有老板或员工账号改成普通球友。

处理：已有 `store_members` 记录只更新段位字段，不写 `role`；只有记录不存在时才新建 `role = player`。

## 残余风险

### P1：结算写入仍不是事务

当前顺序是：

1. 写入 `settlements.status = settling`。
2. 更新 `member_points` 和 `points_ledger`。
3. 更新 `store_members` 段位。
4. 更新 `settlements.status = settled` 和 `matches.status = settled`。

如果第 2 步之后失败，可能出现积分已改、结算单仍停留在 `settling` 的中间状态。

处理：不阻塞本阶段。真实云环境可用后，必须做重复点击、网络中断和中途失败测试；必要时升级为云数据库事务或补偿脚本。

### P2：开台赠分还未绑定会员归属

当前员工只设置球桌到点时间，没有选择本次开台的会员。系统还不能判断 +30 开台赠分应该发给谁。

处理：下一阶段需要设计“开台会员绑定”或“会员扫码开台确认”入口，再写 `points_ledger(type = table_bonus)`。

## 验证

- `node --check cloudfunctions\yunhanApi\index.js`
- `node scripts\test-cloud-contracts.js`
- `node scripts\test-settlement-engine.js`
- `git diff --check`
