# 云瀚台球俱乐部前端设计交接说明

状态：视觉方向已选定为「球房夜赛控制台」  
用途：把 image-2 设计图转成后续小程序前端组件和视觉资产  

## 1. 已保存的设计图

图片已保存到：

```text
docs/design/imagegen-references/
```

| 文件 | 用途 |
| --- | --- |
| `style finding/01-style-comparison-2x2.png` | 早期 4 方向对比，作为历史记录 |
| `style finding/02-night-match-console-style.png` | 已选方向：球房夜赛控制台 |
| `style finding/03-premium-club-style.png` | 备选方向：高端会员俱乐部 |
| `style finding/04-street-ranked-style.png` | 备选方向：街头排位竞技 |
| `style finding/05-urban-neon-billiards-style.png` | 备选方向：新中式霓虹球房 |
| `06-visual-foundation-board.png` | 视觉基础：色彩、材质、字体、几何规则 |
| `07-component-ui-kit-board.png` | 组件库：按钮、玩法卡、计分、奖励、榜单 |
| `08-rank-leaderboard-assets-board.png` | 段位、星级、排行榜、奖励资产 |
| `09-motion-data-viz-spec-board.png` | 动效、状态、图表和数据可视化规范 |

## 2. 前端能否按 UI Kit 实现

可以实现，但不能只让前端照着 image-2 图片凭感觉还原。

正确路径是把图片拆成可执行规格：

```text
image-2 设计图
-> Design Tokens
-> Component Library
-> Visual Assets
-> Motion Spec
-> Page Assembly
```

如果只有图片，前端通常只能还原 70%-80% 的视觉方向，因为颜色、状态、尺寸、动效都需要猜。

如果继续补齐 token、组件状态、资产切图和动效规范，可以做到 90% 以上接近，并且后续页面不会越写越散。

当前已经开始落地的可编码规格见：

```text
docs/design/yunhan-codable-design-system-spec.md
```

## 3. 这些图不直接变成代码

这些图的作用不是「截图还原」，而是给前端建立设计系统。

前端真正要做的是：

1. 从 `06-visual-foundation-board.png` 提取设计 token。
2. 从 `07-component-ui-kit-board.png` 拆出可复用组件。
3. 从 `08-rank-leaderboard-assets-board.png` 生成段位、星星、奖章、宝箱等视觉资产。
4. 从 `09-motion-data-viz-spec-board.png` 定义加星、加分、开奖励、警告反馈等动效。
5. 再把这些规则应用到真实页面：扫码首页、玩法选择、底分倍率、比赛计分、结算、排行榜。

## 4. 前端需要实现的设计系统

### 4.1 Design Tokens

这些是全局变量，先落到 `styles/tokens.wxss` 或同等文件。

必须包含：

- 颜色：炭黑、台呢黑绿、主橙、暗橙、段位金、暖白、成功绿、风险红、禁用灰。
- 字体层级：品牌标题、页面标题、计分数字、按钮文字、辅助说明。
- 间距：4 / 8 / 12 / 16 / 24 / 32。
- 圆角和切角：普通按钮可以小圆角，比赛面板和模式卡优先切角。
- 阴影和发光：只用于主按钮、奖励、段位，不做全页面乱发光。
- 边框：细金属线、橙色选中线、暗面板分割线。
- 动效时间：按钮反馈、数字跳动、奖励揭示、加星。

### 4.2 Component Library

前端组件建议拆成：

| 组件 | 作用 |
| --- | --- |
| `BrandHeader` | 门店字标、球桌状态、到点时间 |
| `PrimaryButton` / `SecondaryButton` / `DangerButton` | 开始挑战、返回、服/不服 |
| `ModeCard` | 抢 5 / 抢 7 / 抢 10 预留 |
| `PointOptionGrid` | 底分和倍率选择 |
| `RiskFormula` | `底分 × 倍率 = 风险积分` |
| `RandomRewardCard` | 普通随机奖励、续时冲刺奖励 |
| `ScoreBoard` | 双方比分、头像、当前盘数 |
| `ScoreStepper` | `+` / `-` 记分按钮 |
| `ForwardTimer` | 正向计时、最低有效时间进度 |
| `SettlementPanel` | 胜负、积分变化、随机奖励、服/不服 |
| `RankBadge` | 青铜到王者段位徽章 |
| `StarTrack` | 加星、掉星、保护星 |
| `LeaderboardRow` | 店内榜、同段位榜、好友榜 |
| `TopThreePodium` | 排行榜前三名 |
| `StatusNotice` | 时间不足、可结算、娱乐局、异常 |
| `BottomTabBar` | 挑战、数据、排行、积分 |

### 4.3 Visual Assets

不是所有东西都应该用 CSS 画。

建议用图片资产的部分：

- 段位徽章：青铜、白银、黄金、铂金、钻石、星耀、王者。
- 星星状态：空星、亮星、新增星、保护星、掉星。
- 随机奖励宝箱 / 奖励牌。
- 赛季徽章。
- 大屏前三名奖章。
- 台呢纹理、木质球桌边框纹理。

建议用代码实现的部分：

- 按钮。
- 选项卡。
- 玩法卡结构。
- 排行榜列表。
- 比分布局。
- 进度条。
- 弹窗 / toast / notice。
- 大部分面板边框和切角。

## 5. 小程序前端如何落地

无论最后用原生小程序、Taro、uni-app，落地顺序都一样。

### 第一步：先建 token

把颜色、字号、间距、阴影、圆角、动效时间先写成统一变量。

不要每个页面单独写颜色。否则后面风格会散。

### 第二步：先做基础组件

先做按钮、模式卡、底分倍率、奖励卡、计分器、排行榜行。

这些组件做完后，页面只是组合它们。

### 第三步：再做页面

球友端页面顺序：

1. 扫码首页。
2. 玩法选择。
3. 底分倍率。
4. 比赛计分。
5. 结算确认。
6. 我的数据。
7. 排行榜。
8. 积分礼遇。

### 第四步：补视觉资产

段位徽章、奖励宝箱、星星、奖章这些要单独生图或矢量化。

建议流程：

```text
image-2 出资产方向
-> 选定版本
-> 统一尺寸和透明背景
-> 前端放入 assets/rank、assets/reward、assets/season
-> 组件通过 props 切换图片
```

### 第五步：补动效

动效不要一开始全做。

MVP 先做 4 个：

- 按钮按下反馈。
- 加减分数字跳动。
- 随机奖励揭示。
- 结算加星。

## 6. 关键原则

- image-2 负责「视觉表达」。
- HTML 原型负责「页面布局和业务流程」。
- 前端代码负责「组件化复用和状态变化」。
- 不要拿单张设计图逐像素硬抄。
- 要把设计图拆成 token、组件、资产、动效四层。

## 7. 下一步建议

下一步应该基于 `yunhan-codable-design-system-spec.md` 做「球友端 UI Kit v1」：

1. 固定颜色和字体规范。
2. 固定按钮、玩法卡、底分倍率、奖励卡、计分器、榜单行。
3. 生成段位徽章和奖励宝箱透明资产。
4. 再把 HTML 原型改成真正接近小程序组件库的版本。
