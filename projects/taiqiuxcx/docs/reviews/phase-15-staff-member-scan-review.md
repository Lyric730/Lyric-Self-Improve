# Phase 15 员工端会员扫码识别审查

日期：2026-05-27

## Findings

### P1：会员码生成入口尚未实现

员工端已经支持扫码识别会员，但球友端还没有正式“会员码/核销码”页面。当前解析兼容 JSON、URL query 和纯 OpenID，真实上线前需要统一会员码格式。

处理：后续补球友端会员码页面，并固定二维码内容格式。

### P1：扫码后仍依赖云端 `member_points`

扫码只能拿到会员标识，积分余额必须从云端 `member_points` 查。真实云环境没初始化或会员积分账户不存在时，会返回失败。

处理：完成云初始化后，会员首次开台或注册时必须创建 `member_points`。

### P2：员工端暂无手动搜索兜底

当前优先做最简单路径：扫码选择会员。若顾客手机不在身边，前台暂时没有手机号/昵称搜索兜底。

处理：后续视门店实际需要补搜索，不在本阶段扩复杂度。

## Scope Check

本阶段新增或改动：

- `cloudfunctions/yunhanApi/index.js`
- `miniprogram/services/staff-service.js`
- `miniprogram/pages/staff-desk/staff-desk.js`
- `miniprogram/pages/staff-desk/staff-desk.wxml`
- `miniprogram/pages/staff-desk/staff-desk.wxss`
- `docs/cloud-database-schema.md`
- `docs/dev-log.md`

没有改动球友端挑战流程。

## Requirement Check

- 员工端前台核销不再默认展示样例会员。
- 员工端必须先扫码选择会员，再核销积分。
- 扫码后调用 `callCloud("staff", "getMemberForExchange")` 查询真实积分账户。
- 核销按钮在未选择会员时禁用。
- 员工端不向前台展示 OpenID。
- 服务端按 `member_points` 返回会员昵称和积分余额。

## Verification Evidence

```powershell
node --check cloudfunctions\yunhanApi\index.js
```

结果：通过。

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
```

结果：通过，共 37 个 JS 文件。

```powershell
node scripts\check-json-files.js
```

结果：通过，共 32 个 JSON 文件。

```powershell
node scripts\check-production-copy.js
```

结果：通过，共 19 个正式页面文件。

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets
```

结果：通过，共 32 个 PNG 资产。

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx' --port 55121
```

结果：通过，包体 661.8 KB。

## Decision

Phase 15 可作为员工端会员扫码识别第一版归档。下一阶段建议补球友端会员码页面，让前台扫码有正式来源。
