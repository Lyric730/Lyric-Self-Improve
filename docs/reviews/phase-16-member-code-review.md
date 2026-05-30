# Phase 16 球友端会员码审查

日期：2026-05-27

## Findings

### P1：真实云函数部署时必须安装 `qrcode` 依赖

会员码由云函数 `member.getCode` 生成，依赖 `cloudfunctions/yunhanApi/package.json` 中的 `qrcode`。微信开发者工具部署时必须选择“上传并部署：云端安装依赖”。

处理：`docs/cloud-init-runbook.md` 已要求云端安装依赖；真实部署后需要在 `docs/dev-log.md` 记录部署结果。

### P1：会员积分账户创建链路仍未完成

会员码能生成，但积分核销仍要求 `member_points` 中存在账户。用户首次登录、首次开台或首次进入积分页时，应创建积分账户并发放可配置的新用户/开台积分。

处理：后续 Phase 补会员账户创建和积分发放。

### P2：二维码图像渲染需要真机确认

当前验证包含微信开发者工具 preview，但尚未在真机里确认 `<image>` 是否稳定显示云函数返回的 base64 data URL。

处理：云函数部署后做真机扫码闭环：球友端出示会员码，员工端扫码选择会员。

## Scope Check

本阶段新增或改动：

- `cloudfunctions/yunhanApi/package.json`
- `cloudfunctions/yunhanApi/index.js`
- `miniprogram/services/member-service.js`
- `miniprogram/pages/member-code/*`
- `miniprogram/app.json`
- `miniprogram/pages/points-perks/points-perks.js`
- `miniprogram/pages/points-perks/points-perks.wxml`
- `docs/dev-log.md`

## Requirement Check

- 球友端新增会员码页面。
- 积分页新增“出示会员码”入口。
- 会员码由云函数按当前微信 OpenID 生成。
- 二维码 payload 包含 `type`、`version`、`storeId`、`openid`。
- 员工端扫码解析已兼容该 JSON 格式。
- 页面没有展示内部校验、mock、调试、临时说明。

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

结果：通过，包体 667.6 KB。

## Decision

Phase 16 可作为球友端会员码第一版归档。下一阶段建议补会员积分账户创建、开台赠分和积分流水发放。
