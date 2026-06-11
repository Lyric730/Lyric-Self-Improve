# 云瀚台球小程序项目源头约束

本文件是本项目的源头约束文档。之后任何 agent 或开发者接手，都先按这里执行，再看具体任务。

## 接手第一读物

如果你是新接手的 agent，先读：

```text
docs/agent-handoff.md
```

这份文档记录当前状态、真实项目路径、云端阻塞、已完成能力和下一步任务。不要只依赖聊天上下文或 `docs/dev-log.md`，`dev-log.md` 太长，只适合查历史细节。

## 协作原则

- 对话用中文；代码注释和技术变量用英文。
- 先判断方案风险，再执行实现。
- 重要阶段产出必须落到文档，不只留在聊天窗口。
- 修改前说明要改什么、为什么；破坏性操作必须先确认。
- 员工端交互默认追求最少步骤、最少学习成本。

## 过程文档规则

重要开发节点必须同步到文档：

- 产品规则变更：更新 `docs/prd-taiqiu-ladder-mvp.md` 和 `docs/ladder-plan/`。
- 设计系统变更：更新 `docs/design/yunhan-codable-design-system-spec.md`。
- 组件对应关系变更：更新 `docs/design/component-traceability-map.md`。
- 美术资产裁切、接入、验收变更：更新 `docs/design/ui-asset-map.md`。
- UI Kit 还原任务进度：更新 `docs/design/ui-kit-task-tracker.md`。
- 阶段性开发记录：更新 `docs/dev-log.md`。
- 上线级阶段执行：更新 `docs/launch-readiness-execution-plan.md`。
- 接口层、权限、状态机、服务端结算接入：更新 `docs/backend-integration-readiness-plan.md` 和 `docs/api-service-layer-contract.md`。

不要让“临时决定”只存在于聊天里。凡是会影响后续前端实现、设计还原、验收标准的内容，都要写进上面的文档。

## 上线级执行规则

小程序进入上线级打磨后，按 `docs/launch-readiness-execution-plan.md` 分阶段执行。

正式上线页面硬约束：

- 页面上不能出现内部校验、PM 说明、演示状态、mock、模拟、调试、临时、占位说明等痕迹。
- 后端、会员、房间状态未接入时，可以先用占位数据驱动页面，但用户可见表现必须像正式线上状态。
- 内部 gate、权限判断、接口 fallback 只能影响按钮、toast、状态，不直接拆成技术清单展示给顾客。
- 页面文案只说用户当下要做什么，不解释“这个页面负责什么”。

每个阶段必须完成：

1. 先确认阶段范围和验收标准。
2. 再改文档和代码。
3. 运行本阶段验证命令。
4. 用 Codex 代码审查姿态检查问题。
5. 把验证结果、审查结论、遗留风险写回 `docs/dev-log.md`。

不允许在一个阶段里把多个页面组混在一起大改。阶段审查中发现 P0 / P1 问题时，必须先修复再进入下一阶段。

正式页面文案必须运行：

```powershell
node scripts/check-production-copy.js
```

该脚本扫描正式 `app.json` 页面和电视大屏 HTML。命中内部校验、PM 说明、演示状态、mock、模拟、调试、临时、占位等可见痕迹时，本阶段不能归档。

接口层硬约束：

- 业务页面只能通过 `miniprogram/services/` 取数和提交动作。
- 业务页面不能直接引用 `miniprogram/utils/ladder-data.js`。
- 业务页面不能直接引用 `miniprogram/utils/operation-log.js`。
- 结算结果必须通过 `match-service` 获取；后续替换为服务端结算接口。

## UI Kit 还原原则

- 当前视觉方向：黑橙竞技、球房夜赛控制台、游戏感 60% + 工具感 40%。
- HTML 原型只代表业务流程和组件布局，不等于最终设计稿。
- image-2 设计图负责视觉表达；小程序代码负责组件化、状态和动态数据。
- 组件实现必须能明确对应设计稿区域，不能凭感觉写“差不多像”的黑橙 UI。
- 页面不能拥挤堆叠；组件之间必须保留清晰间距和呼吸感。
- 切角、金属边、暗面板、橙色高光、段位仪式感是核心视觉特征。

## 美术资产硬约束

复杂美术资源原则上用图片资产，不用 WXML/WXSS 硬画：

- 段位徽章
- 奖励宝箱
- 胜利横幅
- 服了确认章
- 积分币
- 赛季徽章
- 大屏榜单装饰资产

星级状态当前是明确例外：星星 PNG 资产边缘不够干净，正式实现先使用字符星 `★ / ☆` + 固定五格布局。只有重新生成并通过透明边、脏边、完整性验收后，才允许把星星切回 PNG。

当前视觉也不使用绿色成功态。确认、可结算、已完成统一使用金色 / 橙金反馈；`success` 只能作为代码语义名，不代表绿色。

仍然用 WXML/WXSS 实现的部分：

- 按钮结构
- 面板结构
- 玩法卡片
- 底分/倍率选项
- 排行榜行
- 比分布局
- 进度条
- 提示条
- 弹窗和 toast

美术资产默认源图：

```text
docs/design/imagegen-references/08-rank-leaderboard-assets-board.png
```

正式资产默认输出目录：

```text
miniprogram/assets/ui-kit/
```

小程序中引用时使用根路径：

```xml
<image src="/assets/ui-kit/reward-crate-sprint.png" mode="aspectFit" />
```

## 抠图流程硬约束

抠图不能手工覆盖单张 PNG。正式接入时必须脚本化，让裁切坐标、输出尺寸、透明边距都能复查。

每次调整抠图后必须做四件事：

1. 生成或更新正式 PNG 资产。
2. 生成黑底预览图，用来检查视觉质感。
3. 生成棋盘格透明预览图，用来检查透明边和脏边。
4. 运行边缘检测脚本，确认 PNG 四条边没有非透明像素贴边。

验收命令：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-ui-kit-asset-edges.ps1 -RequireAssets
```

通过标准：

```text
Edge check OK
```

不通过时不能提交。典型问题：

- 左边或右边没截完整。
- 素材贴到画布边缘。
- 带入了相邻素材、分割线、标题文字。
- 黑底预览看不出问题，但棋盘格预览能看到脏边。

修裁切框时优先只向缺失方向补，不要盲目整体放大。比如左边缺，就优先向左扩；右边已经干净，就尽量保持右边界不变。

## 微信开发者工具

本地项目目录：

```text
F:\Making money\taiqiuxcx
```

微信开发者工具 CLI 当前约定：

```powershell
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\taiqiuxcx'
```

如果端口或工具路径变化，更新 `docs/wechat-devtools-cli.md`。
