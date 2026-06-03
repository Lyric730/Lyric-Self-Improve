# Phase 55 Review：玩法与底分倍率配置服务化

日期：2026-06-03

## Findings

无阻塞问题。

## 已处理问题

- P1：云端 `getStoreModes()` 原先在读取 `admin_configs` 报错时会静默回默认玩法，这会把真实配置异常伪装成正常状态。本阶段已改为：没有配置文档时才使用默认玩法；数据库读取异常直接返回 `MODE_CONFIG_READ_FAILED`，前端展示正式失败状态。

## 本阶段变更范围

- `cloudfunctions/yunhanApi/index.js`
  - 新增 `match.getModes`。
  - 新增 `match.getSetup`。
  - `match.getModes` 读取老板端 `admin_configs.config.modes`。
  - `match.getSetup` 返回所选玩法、底分、倍率、风险积分和奖励范围。
- `miniprogram/services/match-service.js`
  - 新增 `getAvailableModes()`。
  - 新增 `getConfigurableMatchSetup()`。
  - 保留旧的同步 `getModes()` / `getMatchSetup()` 给其它页面和本地兜底。
  - DevTools 本地兜底优先读取老板端本地保存配置，再回默认玩法。
- `miniprogram/pages/mode-select/`
  - 进入页面异步读取玩法配置。
  - 增加加载、失败重试和无可用玩法状态。
- `miniprogram/pages/points-select/`
  - 进入页面异步读取底分、倍率和奖励规则。
  - 增加加载和失败重试状态。
- `scripts/test-ops-services.js`
  - 增加老板端配置联动回归：保存底分/倍率后，玩法读取和底分倍率读取必须返回同一份配置。

## 残余风险

- 真实云环境尚未创建，`match.getModes` / `match.getSetup` 还未在真实 `admin_configs` 集合、角色权限和索引下验证。
- `points-select` 当前只负责读取并传递参数；最终写入仍发生在 `match-confirm` 的 `match.configure`。
- `match-service.calculateSettlement()` 仍有本地展示计算入口，后续需要逐步减少正式页面对本地计算的依赖。

## 验证

- `git diff --check` 通过。
- `node --check cloudfunctions\yunhanApi\index.js` 通过。
- `node --check miniprogram\services\match-service.js` 通过。
- `node --check miniprogram\pages\mode-select\mode-select.js` 通过。
- `node --check miniprogram\pages\points-select\points-select.js` 通过。
- `node scripts\test-ops-services.js` 通过，输出 `Ops service fallback tests OK`。
- `node scripts\test-cloud-contracts.js` 通过，输出 `Cloud contract tests OK`。
- `node scripts\check-service-layer-boundary.js` 通过，输出 `Service layer boundary check OK`。
- `node scripts\check-production-copy.js` 通过，输出 `Production copy check OK (21 files checked)`。
- `node scripts\check-player-flow-routes.js` 通过，输出 `Player flow route check OK`。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`，包体 `841.3 KB / 861465 bytes`。
