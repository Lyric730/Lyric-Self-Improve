# Phase 41 云函数服务端校验与会员资料保存审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

P2 残余风险：当前云环境尚未创建，本阶段只能验证云函数代码契约、语法和本地校验一致性；尚未在真实云数据库中验证集合权限、索引、写入规则和线上 `wx.cloud.callFunction` 行为。

## Scope Check

本阶段只处理云函数服务端校验和会员资料保存链路，不改变页面交互和积分结算规则。

- 新增云函数侧老板配置校验器：`cloudfunctions/yunhanApi/admin-config-validator.js`
- 新增云函数侧会员资料校验器：`cloudfunctions/yunhanApi/member-profile.js`
- 更新云函数入口：`cloudfunctions/yunhanApi/index.js`
- 更新球友端会员服务：`miniprogram/services/member-service.js`
- 新增小程序与云函数校验一致性测试：`scripts/test-cloud-contracts.js`
- 更新统一上线验证脚本：`scripts/verify-launch-ready.ps1`

## Requirement Check

- `admin.saveConfig` 写入 `admin_configs` 前会先做服务端参数校验。
- `member.saveProfile` 只保存昵称、手机号、备注、头像这些可编辑资料。
- 已存在的老板 / 员工会员不会因为保存个人资料被改成球友角色。
- 会员资料保存不会创建没有余额字段的 `member_points` 脏账户。
- 前端会员资料保存优先调用云函数，只有微信开发者工具预览环境才允许本地兜底。
- 小程序侧与云函数侧校验规则通过 `node scripts/test-cloud-contracts.js` 做一致性验证。

## Verification Evidence

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

结果：通过，输出 `Launch verification OK`；微信预览包体 `748.8 KB` / `766759` bytes。

## Decision

通过。本阶段可以提交。下一阶段优先继续做真实云环境创建后的部署验证，或提前准备 `match.settle` 云函数结算链路。
