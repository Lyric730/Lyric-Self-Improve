# Phase 17 会员积分账户创建与初始积分发放审查

日期：2026-05-27

## Findings

### P1：真实云环境尚未执行闭环验证

`member.getCode` 已经会确保 `member_points` 账户存在，并在首次创建时写入 `points_ledger`。但目前尚未在真实云数据库中验证账户创建、流水写入和二维码显示。

处理：完成云初始化后，用真机访问会员码页，确认 `member_points` 和 `points_ledger` 同时写入。

### P1：开台赠分尚未接入

本阶段只处理新用户初始积分。开台赠分需要知道用户与开台记录的关系，当前还没有真实开台会员绑定。

处理：后续补开台赠分时，必须写 `points_ledger(type=table_bonus)`，并避免同一开台重复发放。

### P1：初始积分发放暂未事务化

如果极端情况下同一用户同时触发两次会员码生成，理论上存在重复创建或重复发放风险。

处理：真实上线前可通过唯一索引、事务或幂等锁强化。

## Scope Check

本阶段新增或改动：

- `cloudfunctions/yunhanApi/index.js`
- `miniprogram/pages/member-code/member-code.js`
- `miniprogram/pages/member-code/member-code.wxml`
- `miniprogram/pages/member-code/member-code.wxss`
- `docs/dev-log.md`

## Requirement Check

- `member.getCode` 会查询 `member_points`。
- 没有积分账户时，会按 `admin_configs.config.points.newUser` 发放初始积分。
- 没有老板配置时，使用默认新用户初始积分 300。
- 初始积分发放写入 `points_ledger(type=initial)`。
- 会员码页面展示当前积分。
- 开台赠分没有被错误地提前发放。

## Verification Evidence

```powershell
node --check cloudfunctions\yunhanApi\index.js
```

结果：通过。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过，共 39 个 JS 文件。

```powershell
node scripts\check-json-files.js
```

结果：通过，共 33 个 JSON 文件。

```powershell
node scripts\check-production-copy.js
```

结果：通过，共 20 个正式页面文件。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：通过，共 32 个 PNG 资产。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 667.9 KB。

## Decision

Phase 17 可作为会员积分账户创建与初始积分发放阶段归档。下一阶段建议补真实云环境部署和真机扫码闭环验证，再继续做服务端结算。
