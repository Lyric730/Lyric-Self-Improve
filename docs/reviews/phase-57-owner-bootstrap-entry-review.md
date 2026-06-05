# Phase 57 Review：首个老板账号初始化入口

日期：2026-06-05

## Findings

### P1：云数据库集合和索引仍需人工创建

微信开发者工具 CLI 当前只提供 `cloud env` 和 `cloud functions`，没有创建集合、创建索引或调用云函数的命令。本阶段新增初始化页面后，仍然要求先在云开发面板创建 `store_members` 等集合。

处理：文档已写明 CLI 能力边界；`auth.bootstrapOwner` 在 `store_members` 不存在时返回 `STORE_MEMBERS_COLLECTION_REQUIRED`。

### P2：初始化入口必须保持运维性质

首个 owner 初始化页可以解决“必须手敲 Console”的上手成本问题，但不能进入顾客挑战、排行榜、积分等主流程，也不能把初始化密钥写进前端代码。

处理：入口只在“我的”页身份区域且 `ownerReady === false` 时显示；云函数仍要求 `BOOTSTRAP_OWNER_SECRET`，且已有 owner 后会拒绝重复初始化。

## 本阶段变更范围

- `cloudfunctions/yunhanApi/index.js`
  - `auth.whoami` 返回 `ownerReady`。
  - `auth.bootstrapOwner` 对缺失 `store_members` 集合返回明确错误。
- `miniprogram/services/auth-service.js`
  - 新增 `getAuthInfo()` 和 `bootstrapOwner()`。
- `miniprogram/pages/setup-owner/`
  - 新增门店初始化页面。
  - 支持读取当前身份、输入初始化密钥、绑定首个老板账号。
- `miniprogram/pages/my-hub/`
  - 读取 `ownerReady`。
  - 仅未初始化时展示“门店初始化”入口。
- `miniprogram/app.json`
  - 注册 `pages/setup-owner/setup-owner`。
- 文档
  - 更新云开发 runbook、切换清单、CLI 使用记录和执行计划。

## 验证

- `git diff --check` 通过。
- `node --check cloudfunctions\yunhanApi\index.js` 通过。
- `node --check miniprogram\services\auth-service.js` 通过。
- `node --check miniprogram\pages\setup-owner\setup-owner.js` 通过。
- `node --check miniprogram\pages\my-hub\my-hub.js` 通过。
- `node scripts\check-json-files.js` 通过，输出 `JSON check OK (36 files checked)`。
- `node scripts\check-player-flow-routes.js` 通过，输出 `Player flow route check OK`。
- `node scripts\check-production-copy.js` 通过，输出 `Production copy check OK (22 files checked)`。
- `node scripts\test-cloud-contracts.js` 通过，输出 `Cloud contract tests OK`。
- `node scripts\check-service-layer-boundary.js` 通过，输出 `Service layer boundary check OK`。
- 部署 `yunhanApi` 到 `cloudbase-d9gg155lc1ee1d72e` 通过：
  - `success = true`
  - `filesCount = 6`
  - `packSize = 17.9 KB`
- `scripts\check-wechat-cloud-readiness.ps1 -EnvId cloudbase-d9gg155lc1ee1d72e -Port 30812` 通过，`yunhanApi status = Active`。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，AppID `wxe30b469d64636a2b`，包体 `852.0 KB / 872470 bytes`。

## 下一步

1. 在微信开发者工具云开发面板创建集合和索引。
2. 配置 `BOOTSTRAP_OWNER_SECRET`。
3. 打开 `/pages/setup-owner/setup-owner` 初始化首个老板账号。
4. 重新验证老板端保存配置、员工端到点时间和会员积分核销。
