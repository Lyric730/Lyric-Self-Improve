# 云瀚台球俱乐部可编码设计系统规格 v0.1

状态：第一版，可用于前端拆组件
视觉方向：球房夜赛控制台
设计来源：`docs/design/imagegen-references/06-visual-foundation-board.png`、`07-component-ui-kit-board.png`、`08-rank-leaderboard-assets-board.png`、`09-motion-data-viz-spec-board.png`
适用端：微信小程序球友端优先，后续扩展员工端、老板端、电视大屏

## 1. 设计系统怎么用

这份文档不是设计赏析，而是给前端写代码用。

前端落地顺序：

```text
Design Tokens
-> Base Components
-> Business Components
-> Visual Assets
-> Page Assembly
-> Motion Polish
```

原则：

- 动态数据必须用代码渲染，不要把整张卡片切成图片。
- 图片资产只用于徽章、星星、宝箱、纹理、奖章这些高视觉成本部分。
- 按钮、卡片、列表、计分器、进度条、Tab、提示条都用 WXML/WXSS 实现。
- 页面只组合组件，不在页面里重复写视觉细节。
- 所有颜色、字号、间距、阴影、动效时间必须来自 token。

## 2. Design Tokens

建议先建：

```text
styles/tokens.wxss
styles/mixins.wxss
styles/motion.wxss
```

### 2.1 Color Tokens

第一版颜色先用可落地近似值。后续可以根据设计图二次取色校准。

```css
page {
  --yh-color-bg: #0d0a07;
  --yh-color-bg-2: #17100a;
  --yh-color-panel: #211810;
  --yh-color-panel-2: #2d2117;
  --yh-color-panel-raised: #3a2818;

  --yh-color-felt: #28180e;
  --yh-color-felt-2: #3d2616;
  --yh-color-rail-wood: #74401e;
  --yh-color-metal: #3a3832;

  --yh-color-orange: #ff7600;
  --yh-color-orange-deep: #b84a00;
  --yh-color-ember: #ff4b12;
  --yh-color-gold: #d9a441;
  --yh-color-gold-bright: #ffd36b;

  --yh-color-success: #f0bd58;
  --yh-color-warning: #f6b94a;
  --yh-color-danger: #ef4d32;
  --yh-color-info: #6a91c9;

  --yh-color-text: #f6efe6;
  --yh-color-text-muted: #b9a894;
  --yh-color-text-faint: #766a5d;
  --yh-color-disabled: #514942;
  --yh-color-line: rgba(255, 214, 145, 0.16);
  --yh-color-line-strong: rgba(255, 118, 0, 0.48);
}
```

使用约束：

- 主橙只用于主路径：开始挑战、选中、奖励、结算。
- 金色只用于段位、星级、排名、奖励。
- 红色只用于不服、扣分、时间不足、异常。
- 当前正式视觉不使用绿色成功态；可清算、已确认、成功统一使用金色 / 橙金反馈。
- 背景不使用纯黑，文字不使用纯白。

### 2.2 Spacing Tokens

微信小程序用 `rpx`。按 750 设计宽度，组件间距使用 4pt 体系。

```css
page {
  --yh-space-1: 8rpx;
  --yh-space-2: 16rpx;
  --yh-space-3: 24rpx;
  --yh-space-4: 32rpx;
  --yh-space-5: 48rpx;
  --yh-space-6: 64rpx;
  --yh-page-pad: 32rpx;
}
```

使用约束：

- 页面左右安全间距：`32rpx`。
- 组件内部紧凑组：`16rpx`。
- 页面主模块间距：`24rpx` 或 `32rpx`。
- 结算、奖励、段位这种仪式感区域可以使用 `48rpx`。

### 2.3 Radius And Shape Tokens

这套风格不要全部做成普通圆角卡片。

```css
page {
  --yh-radius-sm: 8rpx;
  --yh-radius-md: 16rpx;
  --yh-radius-lg: 24rpx;
  --yh-cut-sm: 12rpx;
  --yh-cut-md: 20rpx;
}
```

形状规则：

- 普通按钮：小圆角。
- 模式卡、奖励卡、结算卡：切角面板。
- 排行榜行：轻圆角或斜切底板。
- 段位徽章、奖章、宝箱：图片资产。

切角可用 CSS 方案：

```css
.yh-cut-panel {
  clip-path: polygon(
    0 0,
    calc(100% - var(--yh-cut-md)) 0,
    100% var(--yh-cut-md),
    100% 100%,
    var(--yh-cut-md) 100%,
    0 calc(100% - var(--yh-cut-md))
  );
}
```

微信小程序兼容性要实测。若 `clip-path` 在目标基础库表现不稳，改用背景九宫格图或伪元素切角。

### 2.4 Typography Tokens

```css
page {
  --yh-font-cn: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  --yh-font-number: "DIN Alternate", "DIN Condensed", "Bahnschrift", "Arial Narrow", sans-serif;

  --yh-text-xs: 20rpx;
  --yh-text-sm: 24rpx;
  --yh-text-md: 28rpx;
  --yh-text-lg: 34rpx;
  --yh-text-xl: 44rpx;
  --yh-text-hero: 72rpx;
  --yh-text-score: 96rpx;
}
```

字号规则：

- 页面标题：`44rpx` 左右。
- 计分数字：`96rpx` 以上。
- 风险积分和随机奖励：`44rpx` 到 `64rpx`。
- 说明文字：`24rpx` 到 `28rpx`。
- 排行榜行：昵称 `28rpx`，积分 `24rpx`。

字体约束：

- 中文正文使用系统字体，保证微信端稳定。
- 大数字尽量使用数字字体，但要准备系统 fallback。
- 不用渐变文字。
- 不用大段全大写英文。

### 2.5 Shadow And Glow Tokens

```css
page {
  --yh-shadow-panel: 0 16rpx 42rpx rgba(0, 0, 0, 0.36);
  --yh-shadow-button: 0 12rpx 28rpx rgba(255, 118, 0, 0.28);
  --yh-shadow-reward: 0 18rpx 44rpx rgba(217, 164, 65, 0.24);
  --yh-glow-orange: 0 0 28rpx rgba(255, 118, 0, 0.42);
  --yh-glow-gold: 0 0 32rpx rgba(255, 211, 107, 0.36);
}
```

使用约束：

- Glow 只给主按钮、奖励、段位、选中态。
- 不给每张卡都加光。
- 员工端和老板端默认不用 glow。

### 2.6 Motion Tokens

```css
page {
  --yh-motion-fast: 120ms;
  --yh-motion-base: 220ms;
  --yh-motion-slow: 420ms;
  --yh-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --yh-ease-pop: cubic-bezier(0.22, 1.42, 0.36, 1);
}
```

MVP 必做动效：

- 按钮按下：`120ms`，轻微缩放。
- 计分 +1 / -1：`220ms`，数字弹跳。
- 随机奖励揭示：`420ms`，宝箱或奖励牌打开。
- 结算加星：`420ms`，星星飞入段位条。

## 3. Base Components

### 3.1 Button

组件名建议：

```text
YhButton
```

Props：

| Prop | 类型 | 说明 |
| --- | --- | --- |
| `variant` | `primary / secondary / success / danger / ghost` | 按钮类型 |
| `size` | `sm / md / lg` | 尺寸 |
| `disabled` | boolean | 禁用 |
| `loading` | boolean | 加载中 |
| `icon` | string | 可选图标 |

样式要求：

- `primary`：橙色切角按钮，用于开始挑战、确认下一步。
- `danger`：红色按钮，用于不服、退出本场。
- `success`：金色确认按钮，用于服了确认、可结算；这是代码语义名，不代表绿色。
- `secondary`：深色金属面板，用于返回、演示、次级操作。
- `ghost`：透明背景，用于取消、低优先级。

WXML 示例：

```xml
<button class="yh-btn yh-btn--primary yh-btn--lg">
  开始挑战
</button>
```

WXSS 示例：

```css
.yh-btn {
  min-height: 88rpx;
  padding: 0 32rpx;
  border-radius: var(--yh-radius-md);
  font-size: var(--yh-text-md);
  font-weight: 800;
  transition: transform var(--yh-motion-fast) var(--yh-ease-out);
}

.yh-btn--primary {
  color: #1a0f08;
  background: linear-gradient(135deg, var(--yh-color-orange), var(--yh-color-orange-deep));
  box-shadow: var(--yh-shadow-button);
}

.yh-btn:active {
  transform: scale(0.98);
}
```

### 3.2 Cut Panel

组件名建议：

```text
YhPanel
```

用途：

- 模式卡容器。
- 计分面板。
- 奖励模块。
- 结算模块。

Props：

| Prop | 类型 | 说明 |
| --- | --- | --- |
| `tone` | `default / orange / gold / danger / success` | 视觉语义 |
| `cut` | boolean | 是否切角 |
| `raised` | boolean | 是否浮起 |

要求：

- 默认背景为深金属黑。
- 允许少量台呢纹理或金属纹理。
- 不允许所有页面堆一样的普通圆角卡。

## 4. Business Components

### 4.1 BrandHeader

用途：

- 门店名。
- 当前球桌。
- 开台到点时间。
- 当前段位或积分摘要。

字段：

| 字段 | 示例 |
| --- | --- |
| `clubName` | 云瀚台球俱乐部 |
| `tableNo` | T03 |
| `dueTime` | 22:30 |
| `rankTitle` | 走位黄金 III |
| `points` | 2860 |

布局：

- 顶部左侧是门店字标。
- 右侧是球桌和到点信息。
- 球友端需要强品牌感，员工端可以简化。

### 4.2 ModeCard

用途：选择抢 5 / 抢 7 / 抢 10 预留。

字段：

| 字段 | 示例 |
| --- | --- |
| `name` | 抢5 |
| `targetWins` | 5 |
| `minimumMinutes` | 40 |
| `baseOptions` | 20 / 50 / 100 |
| `starReward` | +1 星 |
| `enabled` | true |
| `selected` | true |

状态：

| 状态 | 表现 |
| --- | --- |
| default | 深色切角面板 |
| selected | 橙色描边、轻 glow、标题高亮 |
| disabled | 灰化、显示预留 |
| pressed | 轻微缩放 |

不要写：

- 不显示「赌注」。
- 不显示「赔率」。
- 不开放抢 9。

### 4.3 PointOptionGrid

用途：底分和倍率选择。

字段：

```ts
type PointOptionGridProps = {
  baseOptions: number[];
  multipliers: number[];
  selectedBase: number;
  selectedMultiplier: number;
}
```

规则：

- 底分只能从后台配置档位选择，不自由输入。
- 倍率只能从后台配置档位选择。
- 选项变化时，`RiskFormula` 必须实时更新。

### 4.4 RiskFormula

用途：展示风险积分。

公式：

```text
风险积分 = 底分 × 倍率
```

示例：

```text
100 × 3 = 300 分
```

实现要求：

- `100`、`3`、`300` 用大数字。
- 这不是奖励，是输赢双方积分清算的风险部分。
- 旁边可放说明：胜方 `+风险积分`，败方 `-风险积分`，双方另加随机奖励。

### 4.5 RandomRewardCard

用途：突出随机奖励。

字段：

| 字段 | 示例 |
| --- | --- |
| `type` | normal / sprint |
| `range` | 80-150 |
| `appliesTo` | both |
| `revealedValue` | 126 |

视觉：

- 可使用宝箱或奖励牌图片资产。
- 奖励范围要比说明文字大至少 2 个层级。
- 普通奖励和续时冲刺奖励要有区别。

文案：

```text
随机奖励
80 ~ 150 积分
双方同享，结算后发放
```

状态：

| 状态 | 表现 |
| --- | --- |
| preview | 显示区间 |
| revealing | 宝箱打开 / 数字翻牌 |
| revealed | 显示实际奖励 |
| sprint | 更强金色表现 |

### 4.6 ScoreBoard

用途：比赛中计分。

字段：

| 字段 | 示例 |
| --- | --- |
| `playerA` | 云瀚-阿杰 |
| `playerB` | 台球小宇 |
| `scoreA` | 5 |
| `scoreB` | 3 |
| `targetWins` | 5 |
| `currentRack` | 8 |
| `elapsedSeconds` | 1715 |

组件组成：

- 双方头像和昵称。
- LED 风格比分。
- 当前玩法。
- 当前局数。
- 到点提醒。
- 加减分按钮。

### 4.7 ScoreStepper

用途：双方都能操作 `+` / `-`。

要求：

- 按钮必须大，适合球桌旁单手点。
- `+` 是主视觉，`-` 是弱视觉。
- 每次点击给数字反馈。
- 不能出现负数。
- 达到抢 5 / 抢 7 目标后提醒是否可结算。

### 4.8 ForwardTimer

用途：正向计时和最低有效时间。

规则：

- 从 `00:00:01` 正向计时。
- 最低有效时间不是倒计时。
- 未满最低有效时间不能计积分段位。
- 到开台到点时间时提醒续时。

显示：

```text
已进行 00:28:35
最低有效 40:00
还差 11:25 可清算
```

状态：

| 状态 | 条件 | 表现 |
| --- | --- | --- |
| running | 比赛中 | 橙色进度 |
| belowMinimum | 已达胜盘但时间不足 | 红色提醒 |
| canSettle | 胜盘 + 时间满足 | 金色可结算 |
| dueTimeReached | 到点 | 续时提醒 |

### 4.9 SettlementPanel

用途：结算确认。

必须展示：

- 胜方。
- 比分。
- 风险积分。
- 双方随机奖励。
- 双方最终积分变化。
- 加星结果。
- 服 / 不服。

数据计算：

```text
胜方积分变化 = 风险积分 + 随机奖励
败方积分变化 = -风险积分 + 随机奖励
```

示例：

```text
风险积分 300
随机奖励 +126
胜方 +426
败方 -174
```

按钮：

- `服了，确认结算`：金色确认态。
- `不服`：红色。

不服路径：

- 对方同意退出本场：双方不结算。
- 双方选择再战：当前场作废，重新开一局。

### 4.10 RankBadge

用途：展示段位。

段位：

```text
青铜 / 白银 / 黄金 / 铂金 / 钻石 / 星耀 / 王者
```

字段：

| 字段 | 示例 |
| --- | --- |
| `tier` | gold |
| `division` | III |
| `stars` | 3 |
| `protected` | true |

实现：

- 段位主体用图片资产。
- 星星当前使用字符星 `★ / ☆` + 固定五格布局；已生成 PNG 因脏边不达标，重新验收前不得接入正式页面。
- 文字和积分进度用代码渲染。

### 4.11 StarTrack

用途：加星、掉星、保护星。

状态：

| 状态 | 表现 |
| --- | --- |
| empty | 暗星 |
| filled | 金星 |
| gained | 新增星动效 |
| lost | 掉星红色反馈 |
| protected | 保护星带盾牌或锁形标记 |

规则：

- 青铜到黄金只加星不掉星。
- 黄金以后允许掉星，具体细分待补。
- 所有玩法共用一个段位。

### 4.12 Leaderboard

排行榜类型：

| 类型 | 说明 |
| --- | --- |
| storeOverall | 店内总榜 |
| sameRank | 同段位榜 |
| wechatFriends | 微信好友榜 |
| bountyHunter | 赏金猎人 |

组件：

- `LeaderboardTabs`
- `TopThreePodium`
- `LeaderboardRow`
- `RankChangeBadge`

行字段：

| 字段 | 示例 |
| --- | --- |
| `rankNo` | 4 |
| `nickname` | 孙总 |
| `rankTitle` | 推杆白银 II |
| `points` | 2860 |
| `winRate` | 62% |
| `change` | +2 |

### 4.13 BottomTabBar

Tabs：

```text
挑战 / 数据 / 排行 / 积分
```

要求：

- 当前 tab 用橙色和轻 glow。
- 非当前 tab 保持低亮。
- 不使用复杂图标，MVP 可以用简单线性图标。

## 5. Visual Assets Spec

资产裁切、透明边缘验收、图片接入规则以 `docs/design/ui-asset-map.md` 为准。宝箱、段位徽章、胜利横幅、服了确认章这类复杂美术资源必须先通过资产映射文档的流程验收，再进入组件实现。

建议目录：

```text
assets/
  rank/
  reward/
  season/
  texture/
  leaderboard/
```

第一批资产：

| 资产 | 建议格式 | 建议尺寸 | 说明 |
| --- | --- | --- | --- |
| rank-bronze | PNG | 256x256 | 青铜徽章 |
| rank-silver | PNG | 256x256 | 白银徽章 |
| rank-gold | PNG | 256x256 | 黄金徽章 |
| rank-platinum | PNG | 256x256 | 铂金徽章 |
| rank-diamond | PNG | 256x256 | 钻石徽章 |
| rank-star | 暂缓 | 64x64 | 当前不用 PNG，待干净透明资产重新验收 |
| rank-star-empty | 暂缓 | 64x64 | 当前不用 PNG，待干净透明资产重新验收 |
| reward-chest-normal | PNG | 320x240 | 普通随机奖励 |
| reward-chest-sprint | PNG | 320x240 | 续时冲刺奖励 |
| season-badge-s1 | PNG | 180x180 | 第一赛季 |
| texture-felt | PNG/JPG | 512x512 | 台呢纹理 |
| texture-wood-rail | PNG/JPG | 512x256 | 木质球桌边 |

格式建议：

- MVP 优先 PNG，兼容更稳。
- WebP 可作为优化项，但要先确认目标微信基础库和机型表现。
- 不要把动态文字做进图片里。
- 所有需要叠在 UI 上的资产都要透明背景。

## 6. Motion Spec

### 6.1 Button Press

```text
duration: 120ms
scale: 0.98
feedback: brightness + slight shadow reduction
```

### 6.2 Score Change

```text
duration: 220ms
effect: score number pops up then settles
direction:
  +1: gold/orange flash
  -1: muted red flash
```

### 6.3 Random Reward Reveal

```text
duration: 420ms
steps:
  1. reward card brightens
  2. chest / reward plate opens
  3. reward number flips or counts up
  4. final number locks
```

### 6.4 Star Gain

```text
duration: 420ms
steps:
  1. new star appears near settlement number
  2. star flies into StarTrack
  3. rank badge flashes once
  4. final state remains gold
```

### 6.5 Time Insufficient Warning

```text
duration: 240ms
effect: red warning panel shake once
copy: 未满最低有效时间，暂不能清算
```

## 7. Page Assembly

球友端必须按递进流程拆页，一页只做一个主任务。详细路由和页面边界见 `docs/design/player-flow-page-spec.md`。

禁止把玩法选择、底分倍率、比赛计分、结算和排行榜堆成一个长页面；这种页面只能作为临时草稿，不能作为真实首屏。

### 7.1 扫码首页

组件：

- `BrandHeader`
- `RankBadge`
- `RandomRewardCard`
- `YhButton`
- `BottomTabBar`

核心信息：

- 球桌。
- 到点时间。
- 当前段位。
- 当前积分。
- 开始挑战。

### 7.2 玩法选择

组件：

- `ModeCard`
- `StatusNotice`
- `YhButton`

核心信息：

- 抢 5。
- 抢 7。
- 抢 10 预留。
- 最低有效时间。
- 加星收益。

### 7.3 底分倍率

组件：

- `PointOptionGrid`
- `RiskFormula`
- `RandomRewardCard`
- `YhButton`

核心信息：

- 底分。
- 倍率。
- 风险积分。
- 随机奖励。
- 是否满足开台剩余时间。

### 7.4 比赛计分

组件：

- `ScoreBoard`
- `ScoreStepper`
- `ForwardTimer`
- `StatusNotice`
- `YhButton`

核心信息：

- 双方比分。
- 已进行时间。
- 最低有效时间。
- 可否结算。
- 到点续时提醒。

### 7.5 结算确认

组件：

- `SettlementPanel`
- `RankBadge`
- `StarTrack`
- `RandomRewardCard`
- `YhButton`

核心信息：

- 胜负。
- 风险积分。
- 随机奖励。
- 双方积分变化。
- 段位加星。
- 服 / 不服。

### 7.6 排行榜

组件：

- `LeaderboardTabs`
- `TopThreePodium`
- `LeaderboardRow`
- `BottomTabBar`

核心信息：

- 店内总榜。
- 同段位榜。
- 微信好友榜。
- 赏金猎人榜后续可加。

## 8. Implementation Acceptance Criteria

前端实现完成后，用这张表验收。

| 项目 | 通过标准 |
| --- | --- |
| token | 页面没有散乱颜色和字号 |
| 组件 | 按钮、模式卡、奖励卡、计分器、榜单行可复用 |
| 资产 | 段位、星星、宝箱不是临时占位 |
| 数据 | 所有动态数据由 props / state 渲染 |
| 状态 | 默认、选中、禁用、成功、危险状态完整 |
| 动效 | 至少有按钮、计分、随机奖励、加星动效 |
| 可读性 | 球桌旁单手操作能看清、点准 |
| 简单性 | 用户不需要理解复杂规则才能开局 |
| 一致性 | 页面风格接近 `07-component-ui-kit-board.png`，但不是死抄整图 |

## 9. 当前实现进度

2026-05-26 已开始制作原生微信小程序 UI Kit 骨架。

当前新增：

```text
project.config.json
miniprogram/app.js
miniprogram/app.json
miniprogram/app.wxss
miniprogram/sitemap.json
miniprogram/styles/tokens.wxss
miniprogram/styles/mixins.wxss
miniprogram/styles/motion.wxss
miniprogram/components/yh-button/
miniprogram/components/yh-panel/
miniprogram/components/mode-card/
miniprogram/pages/ui-kit/
miniprogram/pages/challenge-home/
miniprogram/pages/waiting-room/
miniprogram/pages/accept-challenge/
miniprogram/pages/mode-select/
miniprogram/pages/points-select/
miniprogram/pages/match-confirm/
miniprogram/pages/match-scoring/
miniprogram/pages/time-insufficient/
miniprogram/pages/settlement/
miniprogram/pages/refusal/
miniprogram/pages/match-result/
miniprogram/pages/my-data/
miniprogram/pages/rankings/
miniprogram/pages/points-perks/
```

当前组件：

| 组件 | 状态 | 说明 |
| --- | --- | --- |
| `YhButton` | 已建 v0.1 | 支持 `primary / secondary / success / danger / ghost`、`sm / md / lg`、禁用、加载、块级 |
| `YhPanel` | 已建 v0.1 | 支持 `default / orange / gold / success / danger`、切角、标题、说明、右侧插槽 |
| `ModeCard` | 已建 v0.1 | 支持抢 5 / 抢 7 / 抢 10 预留、选中、禁用、底分、最低时间、加星 |
| `pages/ui-kit` | 已建 v0.1 | 用于在微信开发者工具里预览按钮、面板、玩法卡和奖励模块 |

当前验证：

- JS 语法检查通过。
- JSON 格式检查通过。
- `miniprogram/` 内未出现「赌注」「赔率」「抢 9」等不应出现的业务文案。
- `miniprogram/` 内未出现渐变文字、粗侧边条、`backdrop-filter` 等高风险 AI 味样式。

## 10. 下一步工作

下一批真实前端工作包：

1. `PointOptionGrid`、`RiskFormula`、`RandomRewardCard`。
2. `ScoreBoard`、`ScoreStepper`、`ForwardTimer`。
3. `RankBadge`、`StarTrack`、`SettlementPanel`。
4. `LeaderboardTabs`、`TopThreePodium`、`LeaderboardRow`。
5. 段位徽章和奖励宝箱透明资产生成。
