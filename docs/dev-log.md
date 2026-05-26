# 云瀚台球小程序开发留存

## 2026-05-26

### 微信小程序工程接入

- 当前开发目录：`F:\Making money\taiqiuxcx-wechat`
- 当前分支：`codex/taiqiuxcx-wechat`
- 微信开发者工具 CLI 路径：`F:\微信web开发者工具\cli.bat`
- IDE 服务端口：`55121`
- 已确认 CLI 可执行 `open`、`reset-fileutils`、`preview`。

### UI Kit 组件还原策略

- 设计参考图：`docs/design/imagegen-references/07-component-ui-kit-board.png`
- 还原方式：按编号区域逐组件实现，不把整张设计图切成静态图片。
- 已开始实现：
  - `01 按钮` -> `miniprogram/components/yh-button/`
  - `02 模式卡片` -> `miniprogram/components/mode-card/`
- 当前反馈：
  - 颜色和质感仍需继续贴近设计图。
  - 页面展示太拥挤，需要拉开板块间距。
  - 面板和组件形状需要改成四角内收切角。

### 文档留存规则

用户明确要求：之后每次有重要产出、重要 research 或重要开发节点，都需要自动同步更新文档留存。该规则已写入 `AGENTS.md`。

### UI Kit 第二轮细节还原

- 新增 `03 底分/倍率选择` 组件：`miniprogram/components/point-selector/`
- 新增内容：
  - 底分档位选择：50 / 100 / 200
  - 倍率档位选择：x1 / x2 / x3 / x5
  - 风险积分公式：底分 × 倍率 = 风险积分
  - 普通随机奖励与续时冲刺奖励展示
- 视觉修正：
  - 按钮、模式卡、面板、底分倍率组件统一改成四角内收切角。
  - UI Kit 页面拉大板块间距，避免组件堆叠拥挤。
  - 调整黑橙金属质感：降低泛光，增加内描边、暗金属底、斜向纹理。
- 验证：
  - JS 语法检查通过。
  - JSON 格式检查通过。
  - 禁用样式扫描通过。
  - 微信开发者工具 CLI `preview` 通过，包大小约 `39.7 KB`。

### UI Kit 模拟器只显示文字的问题修复

现象：

- 微信开发者工具里页面没有正常显示按钮、模式卡、选择器，只剩大段默认文字。
- 这说明问题不只是视觉不像，而是组件/WXSS 在模拟器里没有按预期生效。

处理：

- 自定义组件调用从自闭合写法改成显式闭合写法，例如 `<yh-button></yh-button>`。
- 事件绑定从 `bind:tap / bind:select / bind:change` 改为更稳的 `bindtap / bindselect / bindchange`。
- `usingComponents` 路径改成小程序根路径写法，例如 `/components/yh-button/yh-button`。
- 模式卡选中态从 WXML 的 `selectedMode === item.modeId` 表达式挪到 JS 数据字段 `item.selected`。
- `PointSelector` 的选中态从 WXML 表达式挪到组件 JS 生成的 `baseItems / multiplierItems`。
- 页面和底分倍率组件的主体布局从 `display: grid` 改为更稳的 flex 布局。

验证：

- JS 语法检查通过。
- JSON 格式检查通过。
- 高风险语法扫描通过，不再出现 `bind:`、`display: grid`、`wx:elif`、`selectedMode ===`。
- 微信开发者工具 CLI 清缓存、重置文件索引、重新预览通过，包大小约 `43.9 KB`。

### UI Kit 第三轮：04 计分与比分控件

- 新增 `04 计分与比分控件` 组件：`miniprogram/components/score-control/`
- 新增内容：
  - 比分大屏：双方头像占位、昵称、比分 `5 : 3`、玩法说明、到点时间。
  - 计分操作区：我方 `+ / -`、对手 `+ / -`、当前局卡片。
  - 正向计时区：已用时间、最低有效时间、剩余可清算时间提示。
- 设计约束：
  - 继续使用四角内收切角。
  - 使用 flex 布局，避免小程序模拟器里 `display: grid` 渲染不稳定。
  - 操作按钮保持大触控面积，符合球桌旁单手操作场景。

### UI Kit 第四轮：05 随机奖励宝箱

- 新增 `05 随机奖励宝箱` 组件：`miniprogram/components/reward-crate/`
- 对应设计稿右中区域，单独承载“普通随机奖励 / 续时冲刺奖励 / 当前奖励周期”。
- 新增内容：
  - 宝箱视觉：不用静态切图，使用 WXML 结构 + WXSS 分层实现箱盖、锁扣、箱体、发光底座。
  - 奖励数值：普通奖励 `80 ~ 150`、续时冲刺 `200 ~ 300`，作为老板后台可配置数据的展示样式。
  - 奖励进度：第 1 / 第 2 / 第 3 / 冲刺局四段进度，支持点击切换演示状态。
  - 续时提示：到点前冲刺、奖励提升比例，强调“续时继续打”的激励循环。
- 设计约束：
  - 继续使用四角内收切角、暗金属底、稀缺橙金高亮。
  - 首版曾用代码绘制宝箱；第五轮已按用户反馈替换为正式抠图资产。
  - 仍然禁用 `display: grid`、`bind:`、`wx:elif`、`background-clip`、粗侧边框等高风险写法。

### UI Kit 第五轮：美术资源接入策略修正

- 用户明确反馈：宝箱、段位勋章等现成美术资源不应继续用代码硬画。
- 调整原则：
  - 宝箱、段位勋章、结算徽章、积分币走 PNG 图片资源。
  - 代码只负责容器、布局、状态、数值、点击交互。
- 新增资产目录：`miniprogram/assets/ui-kit/`
- 新增抠图脚本：`scripts/extract-ui-kit-assets.ps1`
- 新增资产映射文档：`docs/design/ui-asset-map.md`
- 新增抠图预览：`docs/design/extracted-ui-assets-preview.png`
- 已改造 `reward-crate`：
  - 删除代码绘制的箱盖、锁扣、箱体结构。
  - 使用 `/assets/ui-kit/reward-crate-normal.png` 与 `/assets/ui-kit/reward-crate-sprint.png`。
  - 根据当前奖励阶段自动切换普通宝箱 / 冲刺宝箱。
