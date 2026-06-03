# Phase 40 统一上线验证脚本审查

日期：2026-06-03

## Findings

未发现 P0 / P1 问题。

P3 已修：第一版脚本把微信开发者工具 CLI 中文路径写成默认字符串，在 PowerShell 5 中会被错误解码。已改为用字符码组装默认路径，避免编码导致 CLI 找不到。

## Scope Check

本阶段只新增验证脚本和文档，不修改小程序页面和业务规则。

- 新增 `scripts/verify-launch-ready.ps1`。
- 更新执行计划和开发日志。

## Requirement Check

- 统一脚本默认运行本地上线检查。
- `-WithPreview` 会调用微信开发者工具 CLI 预览。
- 脚本包含运营服务层兜底、结算规则、老板配置校验、会员资料、服务层边界、JSON、正式文案、路由、资产和 JS 语法检查。

## Verification Evidence

```powershell
powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812
```

结果：通过，输出 `Launch verification OK`，微信预览包体 `747.4 KB` / `765348` bytes。

## Decision

通过。后续阶段可优先使用该脚本做本地完整验证。
