# UI 美术资产映射表

## 原则

复杂美术资源不使用代码硬画，直接从设计资产图中抠出 PNG 后接入小程序。

- 宝箱、段位勋章、胜利徽章、积分币：使用图片资产。
- 面板、按钮、切角、状态框、排版、数值：使用 WXML + WXSS 实现。
- 图片资产统一放在 `miniprogram/assets/ui-kit/`。
- 抠图脚本：`scripts/extract-ui-kit-assets.ps1`。
- 资产来源图：`docs/design/imagegen-references/08-rank-leaderboard-assets-board.png`。
- 抠图预览：`docs/design/extracted-ui-assets-preview.png`。

## 当前已抠图资产

| 资产 | 文件 | 当前用途 |
| --- | --- | --- |
| 普通奖励宝箱 | `miniprogram/assets/ui-kit/reward-crate-normal.png` | 随机奖励组件普通阶段 |
| 冲刺奖励宝箱 | `miniprogram/assets/ui-kit/reward-crate-sprint.png` | 随机奖励组件冲刺阶段 |
| 结算奖励宝箱 | `miniprogram/assets/ui-kit/settlement-reward-crate.png` | 预留给结算弹层 |
| 青铜勋章 | `miniprogram/assets/ui-kit/rank-bronze.png` | 预留给段位组件 |
| 白银勋章 | `miniprogram/assets/ui-kit/rank-silver.png` | 预留给段位组件 |
| 黄金勋章 | `miniprogram/assets/ui-kit/rank-gold.png` | 预留给段位组件 |
| 黄金 III 大徽章 | `miniprogram/assets/ui-kit/rank-gold-iii-featured.png` | 预留给个人段位卡 |
| 铂金勋章 | `miniprogram/assets/ui-kit/rank-platinum.png` | 预留给段位组件 |
| 钻石勋章 | `miniprogram/assets/ui-kit/rank-diamond.png` | 预留给段位组件 |
| 星耀勋章 | `miniprogram/assets/ui-kit/rank-star.png` | 预留给段位组件 |
| 王者勋章 | `miniprogram/assets/ui-kit/rank-king.png` | 预留给段位组件 |
| 积分币 | `miniprogram/assets/ui-kit/reward-coin.png` | 预留给积分礼遇 |
| 胜利徽章 | `miniprogram/assets/ui-kit/settlement-victory.png` | 预留给结算成功态 |
| 服了确认章 | `miniprogram/assets/ui-kit/settlement-confirmed.png` | 预留给结算确认态 |

## 代码接入要求

1. 复杂图形优先用 `<image>`，不要再用 WXSS 拼箱子、徽章、奖杯。
2. 图片组件必须保留 `mode="aspectFit"`，避免拉伸变形。
3. 图片路径使用小程序根路径，例如 `/assets/ui-kit/reward-crate-sprint.png`。
4. 如果后续重新生成设计图，更新裁切坐标后重跑脚本，不手工覆盖单张图片。
