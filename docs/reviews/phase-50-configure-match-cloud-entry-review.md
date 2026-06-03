# Phase 50 开局参数写回比赛房间审查
日期：2026-06-03

## Findings

未发现 P0 / P1 语法问题。

P1 已处理风险：确认开局不再只靠页面 query 传递玩法、底分和倍率，而是通过 `match.configure` 写回 `matches`。

P1 已处理风险：`match.configure` 不使用固定默认模式直接校验，已改为优先读取 `admin_configs.modes`，避免老板端改过参数后云端仍按默认参数拒绝。

P1 已处理风险：`match.configure` 要求房间双方都已到齐，并且操作者必须是本场发起方或挑战方。

P1 已处理风险：确认页“开始比赛”增加保存中状态，防止重复点击造成重复写配置。

P2 残余风险：真实云环境尚未创建，`match.configure` 尚未在真实 `admin_configs` 和 `matches` 集合中验证权限、字段和老板配置读取。

P2 残余风险：开赛状态、计分事件和服务端计时还没有接云端。本阶段只把开局参数写入房间，计分页仍通过 query 保留展示兜底。

P2 残余风险：在进入正式 `playing` 状态前，本场双方仍可能再次确认参数并覆盖配置；需要下一阶段用开赛状态锁住参数。

## Scope Check

本阶段只处理开局参数写回，不改积分公式、不改计分页交互、不改结算写入逻辑。

- `cloudfunctions/yunhanApi/index.js`
- `cloudfunctions/README.md`
- `miniprogram/services/match-service.js`
- `miniprogram/pages/match-confirm/match-confirm.js`
- `miniprogram/pages/match-confirm/match-confirm.wxml`
- `docs/api-service-layer-contract.md`
- `docs/cloud-function-cutover-checklist.md`
- `docs/cloud-database-schema.md`
- `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

## Requirement Check

- 云函数新增 `match.configure`。
- `match.configure` 校验玩法是否开放。
- `match.configure` 按老板端玩法配置校验底分和倍率。
- `match.configure` 要求房间状态为 `joined` 或 `configured`。
- `match.configure` 要求双方都已到齐。
- `match.configure` 写入 `modeId`、`base`、`multiplier`、`riskPoints`、`targetWins`、`minimumMinutes` 和 `configuredAt`。
- 小程序新增 `match-service.configureMatchSetup()`。
- 确认开局页点击开始比赛前先保存参数。
- DevTools 无云环境时保留本地预览兜底。

## Verification Evidence

最终验证命令：

```powershell
node --check cloudfunctions\yunhanApi\index.js
node --check miniprogram\services\match-service.js
node --check miniprogram\pages\match-confirm\match-confirm.js
node scripts\test-cloud-contracts.js
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

验证结果：

- `node --check` 快速语法检查通过。
- `node scripts\test-cloud-contracts.js` 通过，输出 `Cloud contract tests OK`。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`，包体 `796.3 KB / 815426 bytes`。

## Decision

本阶段可提交。下一阶段建议补开赛状态、计分事件和服务端计时，把比赛过程从页面状态继续迁移到云端房间状态机。
