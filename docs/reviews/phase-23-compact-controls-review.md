# Phase 23 Compact Controls Review

日期：2026-06-02

## 范围

- `miniprogram/pages/points-select/points-select.wxml`
- `miniprogram/pages/points-select/points-select.wxss`
- `miniprogram/pages/staff-desk/staff-desk.wxml`
- `miniprogram/pages/staff-desk/staff-desk.wxss`

## 检查结论

通过，当前修改把底分 / 倍率页和前台工作台从“大按钮组件”改成了页面级紧凑分段选择器，避免继续用全局按钮尺寸硬套高密度页面。

## 主要风险

- 微信开发者工具 CLI 只能证明构建和预览包生成成功，不能替代逐页视觉复看。
- `custom-class` 依赖微信小程序外部样式类机制，后续如果调整 `yh-button` 的样式隔离策略，需要重新检查员工端和底分倍率页按钮尺寸。

## 验证记录

- `node scripts\check-json-files.js`
- `node scripts\check-production-copy.js`
- `Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }`
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets`
- `F:\微信web开发者工具\cli.bat preview --project "F:\Making money\taiqiuxcx" --port 49663 --lang zh`

## 下一步建议

- 在微信开发者工具中分别打开 `pages/points-select/points-select` 和 `pages/staff-desk/staff-desk`，确认分段控件高度、按钮宽度和四角切角是否符合当前设计方向。
- 如果仍觉得视觉密度不对，下一轮应以具体页面截图为准继续调页面级控件，而不是改全局按钮组件。
