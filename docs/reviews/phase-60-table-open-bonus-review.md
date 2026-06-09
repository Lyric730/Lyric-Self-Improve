# Phase 60 开台赠分会员绑定审查

日期：2026-06-09

## 结论

本阶段可归档。员工端已支持在设置球桌到点时间时可选绑定开台会员；云函数会在绑定会员后发放老板端配置的开台赠分，并写入 `member_points` 和 `points_ledger(type = table_bonus)`。

## 已处理风险

### P1：开台赠分只有配置，没有真实发放

此前老板端可以配置开台赠分，球友端也能看到开台赠分，但员工设置开台到点时间不会实际发分。

处理：`staff.updateTableDueTime` 支持 `memberOpenid`，绑定会员后发放开台赠分，并返回 `tableBonus` 结果给员工端提示。

### P1：不能把积分核销会员误当成开台会员

积分核销场景和开台绑定场景不是同一件事。如果复用同一个 `selectedMember`，员工在核销时改到点时间可能错发开台赠分。

处理：新增独立的 `tableOpenMember` 状态和“扫码绑定开台会员”入口；积分核销仍使用 `selectedMember`。

### P1：重复保存到点时间不能刷开台赠分

员工可能重复点击保存到点时间，或者为了改分钟数多次保存。

处理：新增 `bonusKey`。没有开台软件订单 ID 时，默认按 `tableId + openid + date` 去重；以后如果接入开台软件订单，可传入 `openSessionId` 作为更准确的去重键。

## 残余风险

### P1：没有真实开台订单 ID

当前小程序仍不接开台软件 API，无法知道“本次真实开台订单”的唯一 ID。因此默认去重策略偏保守：同一会员同一天同一球桌只发一次。

处理：可上线前先接受这个策略；后续如果店内强烈要求“同一天同一会员多次开台都给赠分”，需要让员工新建开台周期或接入开台软件订单 ID。

### P2：真实云环境还没做重复点击验证

代码已做查询去重，但真实云数据库并发点击下仍可能出现极端重复写入。

处理：真实云环境测试时必须连续点击保存、断网重试、换会员保存，必要时再加唯一业务锁或事务。

## 验证

- `node --check cloudfunctions\yunhanApi\index.js`
- `node --check miniprogram\services\staff-service.js`
- `node --check miniprogram\pages\staff-desk\staff-desk.js`
- `node scripts\test-ops-services.js`
- `node scripts\check-cloud-collection-docs.js`
- `git diff --check`
