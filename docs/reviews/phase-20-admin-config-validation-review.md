# Phase 20 审查：老板端参数校验

日期：2026-06-01

## 范围

本阶段只处理老板端配置保存前的参数校验，不做完整编辑表单，不接真实云环境。

涉及文件：

- `miniprogram/utils/admin-config-validator.js`
- `miniprogram/services/admin-service.js`
- `miniprogram/pages/boss-config/boss-config.js`
- `scripts/test-admin-config-validator.js`

## 审查结论

P0 / P1：未发现会直接导致当前小程序无法启动的问题。

P1：云函数 `admin.saveConfig` 还没有复用同一套校验。当前校验已经覆盖前端和 service，但正式上线不能只依赖前端，云环境可用后必须把相同规则接进云函数。

P2：老板端页面目前仍是配置展示页，不是完整编辑表单。后续做编辑器时，需要确保每个输入控件的保存逻辑仍然走 `validateAdminConfig`。

P2：校验规则当前偏向“结构和数值安全”，没有做业务成本上限。例如抢 10 底分最高能否超过 300、续时奖励最高能否超过 300，需要老板确认后再加上限。

## 已验证

```powershell
node scripts\test-admin-config-validator.js
node scripts\test-settlement-engine.js
node --check miniprogram\utils\admin-config-validator.js
node --check miniprogram\services\admin-service.js
node --check miniprogram\pages\boss-config\boss-config.js
node scripts\check-json-files.js
node scripts\check-production-copy.js
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\taiqiuxcx' --port 49663 --lang zh
```

补充结果：

- 小程序 JS 语法检查通过，共 41 个 JS 文件。
- 微信开发者工具 CLI preview 通过，包体 `686.4 KB` / `702871` bytes。
- 云开发检查仍被微信侧阻塞，`cloud env list` 返回 `ret:1000 system error`。

## 后续要求

- 云函数 `admin.saveConfig` 必须复用该校验。
- 真实云环境可用后，要用非法配置直接请求云函数，确认服务端拒绝。
- 做老板端编辑表单时，每个输入控件只负责修改值，最终保存统一走 `validateAdminConfig`。
