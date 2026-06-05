# Phase 58 Review：云数据库控制台清单与集合文档护栏

日期：2026-06-05

## Findings

### P1：集合创建仍然不能由当前 CLI 自动完成

微信开发者工具 CLI 当前没有数据库建集合、建索引或云函数调用能力。本阶段不能把“数据库已完成”写入状态，只能把人工操作固化成清单，并用脚本防止代码集合名和文档脱节。

处理：新增 `docs/cloud-database-console-checklist.md`，并保持 `cloud-function-cutover-checklist` 中数据库和 owner 初始化为待确认。

### P2：未来新增集合时容易漏文档

云函数后续如果新增集合，开发者可能只改代码不改 schema/runbook，导致上线时控制台漏建集合。

处理：新增 `scripts/check-cloud-collection-docs.js`，从 `yunhanApi` 提取所有 `db.collection("...")` 集合名，并校验它们同时出现在 schema 和 runbook。

## 本阶段变更范围

- `docs/cloud-database-console-checklist.md`
  - 新增云开发面板集合、索引、环境变量、owner 初始化和后续验证清单。
- `scripts/check-cloud-collection-docs.js`
  - 新增集合文档一致性检查。
- `scripts/verify-launch-ready.ps1`
  - 将集合文档检查加入统一上线验证。
- `docs/cloud-init-runbook.md`
  - 链接控制台执行清单。
- `docs/cloud-function-cutover-checklist.md`
  - 指向 runbook 和控制台清单。

## 验证

- `git diff --check` 通过。
- `node --check scripts\check-cloud-collection-docs.js` 通过。
- `node scripts\check-cloud-collection-docs.js` 通过，输出 `Cloud collection docs check OK (10 collections checked)`。
- `node scripts\check-json-files.js` 通过，输出 `JSON check OK (36 files checked)`。
- `node scripts\check-production-copy.js` 通过，输出 `Production copy check OK (22 files checked)`。
- `node scripts\check-player-flow-routes.js` 通过，输出 `Player flow route check OK`。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`，包体 `852.0 KB / 872470 bytes`。

## 下一步

1. 用户在云开发面板按清单创建集合和索引。
2. 用户配置 `BOOTSTRAP_OWNER_SECRET`。
3. 使用 `/pages/setup-owner/setup-owner` 初始化 owner。
4. 再做真实写库链路验证。
