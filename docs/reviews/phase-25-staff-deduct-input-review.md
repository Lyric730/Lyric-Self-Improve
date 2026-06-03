# Phase 25 Staff Deduct Input Review

日期：2026-06-02

## 范围

- `miniprogram/pages/staff-desk/staff-desk.wxml`
- `miniprogram/pages/staff-desk/staff-desk.js`
- `miniprogram/pages/staff-desk/staff-desk.wxss`
- 微信开发者工具 CLI 刷新流程

## 检查结论

通过。前台积分核销已改为填写扣除分数，符合员工端简单操作原则；模拟器启动失败经 CLI 刷新后，开发者工具服务、文件监听、项目打开和预览均已成功。

## 根因确认

- 固定扣分档位不是实际业务的最小操作单元，兑换品分值会变化，输入扣除分数更直接。
- 原固定按钮网格也会继续带来组件尺寸挤压风险。
- `Failed to fetch` 不是当前代码语法或 JSON 错误导致；本轮语法检查、JSON 检查、文案检查均通过，CLI 也能成功预览。

## 验证记录

- `node --check miniprogram\pages\staff-desk\staff-desk.js`
- `node scripts\check-json-files.js`
- `node scripts\check-production-copy.js`
- `git diff --check`
- `F:\微信web开发者工具\cli.bat --port 49663 --lang zh islogin`
- `F:\微信web开发者工具\cli.bat --port 49663 --lang zh reset-fileutils --project "F:\Making money\taiqiuxcx"`
- `F:\微信web开发者工具\cli.bat --port 49663 --lang zh open --project "F:\Making money\taiqiuxcx"`
- `F:\微信web开发者工具\cli.bat --port 49663 --lang zh preview --project "F:\Making money\taiqiuxcx"`

## 后续注意

- 如果模拟器界面仍停留在失败页，优先在开发者工具里点击“编译”，再重新打开项目；不要先改代码。
- 积分核销后续接云函数时，服务端必须再次校验扣分金额和会员余额，前端校验只用于减少误操作。
