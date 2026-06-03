# Phase 24 Selector Picker Review

日期：2026-06-02

## 范围

- `miniprogram/pages/points-select/points-select.wxml`
- `miniprogram/pages/points-select/points-select.wxss`
- `miniprogram/pages/staff-desk/staff-desk.wxml`
- `miniprogram/pages/staff-desk/staff-desk.js`
- `miniprogram/pages/staff-desk/staff-desk.wxss`

## 检查结论

通过。底分 / 倍率页已经移除原生按钮选项，改成可控的 `view` 选项块；前台到点时间改用微信小程序原生时间选择器，满足 24 小时制时分选择。

## 根因确认

- 原生 `button` 适合明确动作，不适合在当前设计里承担高密度参数选项。
- 对底分 / 倍率这类参数选择，用普通 `view + bindtap` 可以稳定控制宽度、切角、换行和选中态。
- 到点时间的真实业务不是四个预设值，而是员工按开台软件同步具体到点时刻，所以应该使用时间选择器。

## 验证记录

- `node --check miniprogram\pages\staff-desk\staff-desk.js`
- `node scripts\check-json-files.js`
- `node scripts\check-production-copy.js`
- `git diff --check`
- `F:\微信web开发者工具\cli.bat preview --project "F:\Making money\taiqiuxcx" --port 49663 --lang zh`

## 后续注意

- 底分 / 倍率页后续不要再回退到原生 `button` 网格。
- 员工端到点时间如果需要限制营业时段，应在 `picker` 的 `start` / `end` 或保存校验里做，而不是恢复固定按钮。
