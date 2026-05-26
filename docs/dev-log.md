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
