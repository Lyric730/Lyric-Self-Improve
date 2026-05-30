# 云瀚台球小程序开发记录

## 2026-05-27 Phase 0 上线级执行框架落地

本轮目的：把“逐阶段上线级打磨 + 阶段收尾审查”固定成项目执行规则，避免继续按临时演示版本推进。

已完成：

- 新增 `docs/launch-readiness-execution-plan.md`，拆分 Phase 0 ~ Phase 9。
- 在 `AGENTS.md` 中登记上线级执行规则。
- 新增 `scripts/check-json-files.js`，后续阶段统一用它检查 JSON 配置。

阶段要求：

- 每个阶段先落文档，再做代码。
- 每个阶段收尾必须运行验证命令。
- 每个阶段收尾必须用 Codex 代码审查姿态检查问题。
- 审查结果和遗留风险必须写回 `docs/dev-log.md`；必要时新增 `docs/reviews/` 详细审查记录。

下一项任务：

- Phase 1：挑战首页上线级打磨。

## 2026-05-27 Phase 1 挑战首页上线级打磨完成

本轮目的：把挑战首页从演示入口改成上线版开局检查页，只承担“判断能否发起有效挑战”和“进入等待房间”两件事。

已完成：

- 更新 `miniprogram/pages/challenge-home/`。
- 更新 `miniprogram/utils/ladder-data.js`，新增首页开局检查 mock。
- 更新 `docs/design/player-flow-page-spec.md`，补充“挑战首页上线级要求”。
- 新增 `docs/reviews/phase-1-challenge-home-review.md`。

页面变化：

- 首页展示门店、球桌、开台到点时间。
- 首页展示微信登录、店内 100 米定位、球桌开台有效 3 个检查项。
- 主按钮由检查项计算 `canStartChallenge`，条件不足时禁用。
- 首页保留当前段位卡，并说明全部游戏模式共用一个段位。
- 首页不展示底分、倍率、计分器、结算明细。

验证结果：

- JS 语法检查通过。
- `node scripts\check-json-files.js` 通过：`JSON check OK (28 files checked)`。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过：`Edge check OK (32 PNG assets checked)`。
- 微信开发者工具 CLI preview 通过，包体 `605.5 KB`。
- 微信开发者工具 auto 通过，WebSocket 当前页面为 `pages/challenge-home/challenge-home`。

阶段审查结果：

- P0 / P1：无。
- P2：开局检查仍是 mock 数据，正式上线前必须接真实登录、定位、球桌开台状态。
- P3：本机暂不能自动截取微信开发者工具模拟器画面，视觉验收仍需用户截图。

下一项任务：

- Phase 2：等待与接受挑战流程上线级打磨。

## 2026-05-27 Phase 1 首页演示痕迹纠偏

本轮目的：修正首页把内部校验和 PM 说明直接展示给顾客的问题。正式上线首页不能出现 `FLOW`、`本页只做入口`、`已完成`、`待处理` 这类演示痕迹。

已完成：

- 删除首页可见的微信登录 / 店内定位 / 球桌开台检查清单。
- 删除首页“本页只做入口”说明卡。
- 首页改为正式用户视角：排位状态、发起挑战按钮、当前段位、常用入口。
- 内部仍保留 `canStartChallenge` gate，用于控制是否能进入等待房间。
- 更新 `docs/launch-readiness-execution-plan.md` 和 `docs/design/player-flow-page-spec.md`，明确内部校验不能直接展示给顾客。
- 更新 `docs/reviews/phase-1-challenge-home-review.md`，记录原审查口径错误和修订结论。

验证结果：

- JS 语法检查通过。
- `node scripts\check-json-files.js` 通过：`JSON check OK (28 files checked)`。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过：`Edge check OK (32 PNG assets checked)`。
- 微信开发者工具 CLI preview 通过，包体 `604.9 KB`。
- 微信开发者工具 auto 通过，WebSocket 当前页面为 `pages/challenge-home/challenge-home`。

审查结果：

- P0 / P1：无。
- P2：开局 gate 仍是 mock 数据，正式上线前必须替换为真实微信登录、定位、开台状态。
- P3：当前仍无法自动获取微信开发者工具模拟器截图，视觉验收需要用户截图确认。

## 2026-05-27 Phase 2 等待与接受挑战流程完成

本轮目的：把等待房间和接受挑战页从演示态改成正式上线态，不能出现“模拟对手扫码”等演示按钮。

已完成：

- 更新 `miniprogram/pages/waiting-room/`。
- 更新 `miniprogram/pages/accept-challenge/`。
- 更新 `miniprogram/utils/ladder-data.js`，新增房间状态和邀请占位数据。
- 更新 `docs/launch-readiness-execution-plan.md` 和 `docs/design/player-flow-page-spec.md`，补充 Phase 2 上线要求。
- 新增 `docs/reviews/phase-2-waiting-accept-review.md`。

页面变化：

- 等待页展示房间码、球桌、发起人、等待状态。
- 等待页只保留刷新状态、取消挑战两个正式动作。
- 接受页展示发起方、挑战方、球桌、房间状态。
- 接受页只保留接受挑战、拒绝邀请。
- 页面不展示底分、倍率、积分公式、排行榜。
- 页面不出现 mock、模拟、演示、调试、临时、PM 说明等用户可见痕迹。

验证结果：

- WXML 演示痕迹扫描无匹配输出。
- JS 语法检查通过。
- `node scripts\check-json-files.js` 通过：`JSON check OK (28 files checked)`。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过：`Edge check OK (32 PNG assets checked)`。
- 微信开发者工具 CLI preview 通过，包体 `610.6 KB`。
- 微信开发者工具 auto 通过，但直接页面跳转协议未实现。

阶段审查结果：

- P0 / P1：无。
- P2：房间状态仍是占位数据，正式上线前必须接真实房间状态。
- P3：DevTools 自动化协议不能直接 `reLaunch` 指定页面，视觉验收仍需截图或补充工具链。

下一项任务：

- Phase 3：玩法与风险积分选择上线级打磨。

## 2026-05-27 Phase 3 玩法与风险积分选择完成

本轮目的：把玩法选择、底分倍率、开局确认做成真实参数链，而不是后续页面固定读取演示参数。

已完成：

- 更新 `miniprogram/pages/mode-select/`。
- 更新 `miniprogram/pages/points-select/`。
- 更新 `miniprogram/pages/match-confirm/`。
- 更新 `miniprogram/components/mode-card/`，删除“预留 / 锁定”等内部化表达。
- 更新 `miniprogram/utils/ladder-data.js`，新增 `getModeById` 和 `buildMatchSetup`。
- 更新 `docs/launch-readiness-execution-plan.md` 和 `docs/design/player-flow-page-spec.md`，补充 Phase 3 上线要求。
- 新增 `docs/reviews/phase-3-mode-points-confirm-review.md`。

页面变化：

- 玩法页选择的 `modeId` 会传到底分页。
- 底分页选择的底分、倍率、风险积分会传到开局确认页。
- 开局确认页展示用户实际选择参数。
- 抢 10 展示为“暂未开放”，不再写内部后台预留说明。
- 页面不出现 mock、模拟、演示、调试、临时、PM、后台模板、服务器记录等用户可见痕迹。

验证结果：

- WXML 演示痕迹扫描无匹配输出。
- JS 语法检查通过。
- `node scripts\check-json-files.js` 通过：`JSON check OK (28 files checked)`。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过：`Edge check OK (32 PNG assets checked)`。
- 微信开发者工具 CLI preview 通过，包体 `612.9 KB`。

阶段审查结果：

- P0 / P1：无。
- P2：参数仍停留在页面 query 和占位数据层，后端阶段必须持久化到房间记录。
- P2：比赛计分页暂未接收 Phase 3 参数，进入 Phase 4 处理。

下一项任务：

- Phase 4：比赛计分与时间规则上线级打磨。

## 2026-05-27 Phase 4 比赛计分与时间规则完成

本轮目的：把计分页和时间不足页从演示跳转改成正式规则状态，未满最低有效时间不能进入结算。

已完成：

- 更新 `miniprogram/pages/match-confirm/match-confirm.js`，开始比赛时传递玩法、底分、倍率、风险积分。
- 更新 `miniprogram/pages/match-scoring/`，接收本场参数、正向计时、双方加减盘、目标盘数检查。
- 更新 `miniprogram/pages/time-insufficient/`，只提供继续计分、先去续时两个正式动作。
- 更新 `docs/launch-readiness-execution-plan.md` 和 `docs/design/player-flow-page-spec.md`，补充 Phase 4 上线要求。
- 新增 `docs/reviews/phase-4-scoring-time-review.md`。

页面变化：

- 计分页从 `00:00:01` 开始正向计时。
- 计分页展示本场玩法、目标盘数、风险积分。
- 任一方达到目标盘数后先检查最低有效时间。
- 未满最低有效时间进入时间不足页，不能结算。
- 时间不足页不再出现“演示进入结算”。

验证结果：

- WXML 演示痕迹扫描无匹配输出。
- JS 语法检查通过。
- `node scripts\check-json-files.js` 通过：`JSON check OK (28 files checked)`。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过：`Edge check OK (32 PNG assets checked)`。
- 微信开发者工具 CLI preview 通过，包体 `616.5 KB`。

阶段审查结果：

- P0 / P1：无。
- P2：计时与比分仍是单端页面状态，正式上线前必须接房间状态和服务端时间。
- P2：结算页暂未接收 Phase 4 参数，进入 Phase 5 处理。

下一项任务：

- Phase 5：结算、服 / 不服、结果页上线级打磨。

## 2026-05-27 UI Kit 资产流程约束固化

本轮目的：把“复杂美术资源不能用代码硬画、抠图必须干净、裁切过程必须可复查”写进源头约束，而不是只留在聊天里。

已完成：

- 新增项目级源头约束文档 `AGENTS.md`。
- 新增 `docs/design/ui-asset-map.md`，明确宝箱、段位徽章、胜利横幅、服了确认章等复杂资产必须走 PNG 资产。
- 在 `docs/design/yunhan-codable-design-system-spec.md` 中引用资产映射文档。
- 在 `docs/design/component-traceability-map.md` 中补充组件与图片资产的边界。
- 新增 `scripts/check-ui-kit-asset-edges.ps1`，用于检查 PNG 四条边是否存在非透明像素贴边。

后续要求：

- 正式抠图时必须生成黑底预览和棋盘格透明预览。
- 正式接入前必须运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-ui-kit-asset-edges.ps1 -RequireAssets
```

- 当前项目已预留 `miniprogram/assets/ui-kit/`，但还没有正式批量落地的 PNG 资产；下一轮抠图必须从 `docs/design/imagegen-references/08-rank-leaderboard-assets-board.png` 开始。

## 2026-05-27 UI-01 正式抠图流水线完成

本轮目的：完成第一批 UI 美术资产的可复跑裁切流程，避免后续再靠手动截图和聊天记录找裁切参数。

已完成：

- 新增 `docs/design/ui-kit-task-tracker.md`，用于追踪 UI Kit 还原任务。
- 新增 `scripts/extract-ui-kit-assets.ps1`，从 `docs/design/imagegen-references/08-rank-leaderboard-assets-board.png` 批量裁切资产。
- 输出 32 个 PNG 到 `miniprogram/assets/ui-kit/`。
- 生成黑底预览：`docs/design/extracted-ui-assets-preview.png`。
- 生成棋盘格透明预览：`docs/design/extracted-ui-assets-checker-preview.png`。
- 运行 `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets`，结果为 `Edge check OK (32 PNG assets checked)`。
- 将 UI-01 从任务队列归档到 `docs/design/ui-kit-task-tracker.md`。

下一项任务：

- UI-02：制作第一批资产组件，包括 `RankBadge`、`StarTrack`、`RewardCrate`、`SettlementBadge`、`VictoryBanner`、`AcceptStamp`。

## 2026-05-27 UI-02 资产组件第一批完成

本轮目的：把第一批 PNG 美术资产封装成小程序可复用组件，避免后续页面直接散落 `<image>`。

已完成：

- 新增 `miniprogram/components/rank-badge/`，用于展示段位徽章、段位标题、积分进度。
- 新增 `miniprogram/components/star-track/`，用于展示空星、已获得、新获得、保护星、扣除星状态。
- 新增 `miniprogram/components/reward-crate/`，用于展示普通奖励和续时冲刺奖励。
- 新增 `miniprogram/components/settlement-badge/`，用于展示段位提升、加分、扣分、奖励结算卡。
- 新增 `miniprogram/components/victory-banner/`，用于展示胜利横幅。
- 新增 `miniprogram/components/accept-stamp/`，用于展示服了确认章。
- 更新 `miniprogram/pages/ui-kit/`，新增“美术资产组件”验收区。
- 将 UI-02 从任务队列归档到 `docs/design/ui-kit-task-tracker.md`。

验证结果：

- JS 语法检查通过。
- JSON 解析检查通过，共 13 个 JSON 文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `558.3 KB`。

下一项任务：

- UI-03：重做 UI Kit 组件验收台的信息架构和间距，把每个组件的状态分组展示，避免页面继续拥挤堆叠。

## 2026-05-27 UI-03 组件验收台完成

本轮目的：把 UI Kit 页面从“组件堆叠展示”改成真正可用于逐项扣细节的验收台。

已完成：

- 重构 `miniprogram/pages/ui-kit/ui-kit.wxml`。
- 重写 `miniprogram/pages/ui-kit/ui-kit.wxss`。
- 新增顶部阶段轨道，显示 UI-01 / UI-02 已完成、UI-03 当前验收阶段。
- 将按钮区改成状态矩阵：主按钮、次要/提示按钮、对局结果按钮、图标按钮分组展示。
- 将玩法卡片区改成“当前推荐 + 高收益/预留”的分层结构，避免三张卡片平铺拥挤。
- 将美术资产区改成段位星级、随机奖励、结算反馈、胜负确认四组。
- 将 UI-03 从任务队列归档到 `docs/design/ui-kit-task-tracker.md`。

验证结果：

- JS 语法检查通过。
- JSON 解析检查通过，共 13 个 JSON 文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 本轮触碰文件行尾检查通过。
- 微信开发者工具 CLI preview 通过，包体 `561.5 KB`。

下一项任务：

- UI-04：在微信开发者工具中逐组件对照设计图，记录按钮、模式卡、段位、星级、奖励、结算资产的视觉差异和需要继续扣的点。

## 2026-05-27 UI-04 对照验收启动

本轮目的：开始把微信开发者工具中的实际 UI Kit 页面和 07 / 08 号设计稿逐组件对照。

已完成：

- 新增 `docs/design/ui-kit-visual-review.md`。
- 记录当前机器验收结果：CLI preview 可打开、包体 `561.5 KB`、JS/JSON/资产边缘检测通过。
- 记录当前已知视觉差异：按钮、模式卡、段位、星级、奖励、结算、胜利横幅、确认章都列入后续精修点。
- 将 UI-04 标记为进行中。

阻塞点：

- 微信开发者工具 CLI 没有直接截图命令。
- 已尝试 `cli auto` 和临时 `miniprogram-automator`，但自动连接截图流程超时。
- UI-04 不能在没有模拟器截图的情况下归档完成。

下一步：

- 获取微信开发者工具模拟器截图后，继续逐组件记录“通过 / 待修 / 不适用”结论。

## 2026-05-27 UI-04 截图通道排查记录

本轮目的：确认 Codex 能否直接通过微信开发者工具 CLI 或自动化协议拿到模拟器截图。

已确认：

- `cli auto --project ... --port 55121 --auto-port 9434 --trust-project` 可以开启自动化端口。
- `ws://127.0.0.1:9434` 可以建立 WebSocket 连接。
- 自动化协议的 `Tool.getInfo` 返回微信开发者工具版本 `2.01.2510290`、SDKVersion `3.16.0`。
- `App.getCurrentPage` 和 `App.getPageStack` 可返回当前页面。
- `miniprogram-automator` 可以连接、跳转到 `pages/player/player`，并读取页面 data。

阻塞：

- `App.captureScreenshot` 超时不返回。
- `Tool.captureScreenshot` 返回 `unimplemented`。
- `Page.captureScreenshot` 返回 `appservice Page.captureScreenshot unimplemented`。
- Windows `PrintWindow` / `CopyFromScreen` 对 DevTools 主窗口只能得到灰屏或黑屏，不能作为视觉验收截图。

结论：

- UI-04 不能自动归档。真实视觉对照仍需要微信开发者工具模拟器截图。
- 这不是小程序构建失败，也不是端口没开，而是当前 DevTools 截图接口/窗口合成层不可自动抓取。

## 2026-05-27 UI-05 球友端页面组装完成

本轮目的：在 UI Kit 组件基础上，组装一个真实球友端页面骨架，用于后续继续扣视觉细节。

已完成：

- 新增 `miniprogram/pages/player/`。
- 将 `pages/player/player` 设置为小程序首屏，`pages/ui-kit/ui-kit` 保留为组件验收台。
- 页面覆盖：顶部门店和球桌信息、当前段位、玩法选择、底分倍率、风险积分、普通随机奖励、续时冲刺奖励、比赛计分、正向计时、结算确认、不服路径、个人端排行榜。
- 复用现有组件：`YhButton`、`YhPanel`、`ModeCard`、`RankBadge`、`StarTrack`、`RewardCrate`、`VictoryBanner`、`AcceptStamp`。
- 保持规则：不开放抢 9；底分、倍率、奖励按模式配置展示；全部游戏模式共用一个段位。

验证结果：

- JS 语法检查通过。
- JSON 解析检查通过，共 14 个 JSON 文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `584.5 KB`。
- 自动化协议可进入 `pages/player/player` 并读取页面 data：`selectedModeId=race5`、`riskPoints=300`、`rankingRows=4`。

下一项任务：

- UI-06：基于真实截图继续扣球友端细节，包括顶部视觉、模式卡拥挤度、底分倍率区、比赛计分区、结算仪式感和排行榜表现。

## 2026-05-27 UI-07 球友端多页面流程重构完成

本轮目的：修正 `pages/player` 把所有功能堆成一个长页面的问题，按 PRD 的层层递进流程拆成多个页面。

源头文档更新：

- 新增 `docs/design/player-flow-page-spec.md`。
- 更新 `docs/prd-taiqiu-ladder-mvp.md`，明确球友端不能做一个长页面。
- 更新 `docs/ladder-plan/05-mvp-scope-and-decisions.md`，补充球友端页面顺序和主任务。
- 更新 `docs/design/yunhan-codable-design-system-spec.md`，把多页面流程作为实现约束。

代码变更：

- 将小程序首屏从 `pages/player/player` 改为 `pages/challenge-home/challenge-home`。
- 删除错误方向的 `pages/player` 长页面。
- 新增共享 mock 数据：`miniprogram/utils/ladder-data.js`。
- 新增共享页面样式：`miniprogram/styles/player-flow.wxss`。
- 新增球友端递进页面：
  - `challenge-home`
  - `waiting-room`
  - `accept-challenge`
  - `mode-select`
  - `points-select`
  - `match-confirm`
  - `match-scoring`
  - `time-insufficient`
  - `settlement`
  - `refusal`
  - `match-result`
  - `my-data`
  - `rankings`
  - `points-perks`

验证结果：

- JS 语法检查通过。
- JSON 解析检查通过，共 27 个 JSON 文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `599.8 KB`。
- 自动化协议逐页 `reLaunch` 验证通过，14 个业务页和 `ui-kit` 页都可打开。

结论：

- UI-07 归档完成。
- 下一步进入 UI-06：逐页截图，对照设计稿继续抠视觉细节，不再对错误长页做精修。

## 2026-05-27 Phase 5 结算 / 不服 / 结果页完成

本轮目的：把结算确认、不服处理和结算结果从旧静态数据改成正式流程状态，避免页面继续展示固定演示结算。

源头文档更新：

- 更新 `docs/design/player-flow-page-spec.md`，新增结算、服 / 不服、结果页上线级要求。
- 新增 `docs/reviews/phase-5-settlement-refusal-result-review.md`，归档本阶段审查结论和验证证据。

代码变更：

- 更新 `miniprogram/utils/ladder-data.js`：
  - 新增 `buildSettlement`。
  - 新增奖励范围解析、稳定奖励值生成、正负积分格式化。
  - 结算公式按当前规则：胜方 = 风险积分 + 随机奖励；败方 = 随机奖励 - 风险积分。
- 更新 `miniprogram/pages/match-scoring/match-scoring.js`：
  - 达到目标盘数后，把玩法、底分、倍率、风险积分、比分、赢家、已用时间传入结算页。
- 更新 `settlement`：
  - 展示胜方、比分、用时、风险积分、随机奖励、双方积分变化、胜方加星。
  - “服了，确认结算”进入结果页；“不服，暂不结算”进入不服页。
- 更新 `refusal`：
  - 只保留“双方同意退出”和“再战一场”两条正式路径。
  - 退出本场不计积分、不加星、不更新排行榜。
- 更新 `match-result`：
  - 展示结算已生效后的加分、净变化、随机奖励和加星反馈。
  - 败方净变化可能为非负数时，使用奖励反馈样式而不是固定扣分样式。

验证结果：

- JS 语法检查通过。
- JSON 解析检查通过，共 28 个 JSON 文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 结算相关页面可见文案黑名单扫描无匹配。
- 微信开发者工具 CLI preview 通过，包体 `623.4 KB`。
- 微信开发者工具 auto 服务启动通过。
- `buildSettlement` 抽样验证：抢 5、底分 100、倍率 3、比分 5:3、胜方 A，风险积分 300，随机奖励 12，胜方变化 312，败方变化 -288。

审查结论：

- P2：结算仍是前端本地状态，正式上线前必须由服务端结算并记录双方确认。
- P2：随机奖励当前为稳定占位算法，正式上线前必须由服务端按老板配置生成并落单。

下一项任务：

- Phase 6：个人数据、排行榜、积分礼遇页上线级打磨。

## 2026-05-27 Phase 6 数据 / 排行榜 / 积分礼遇完成

本轮目的：把个人数据、排行榜、积分礼遇从“产品说明口吻”改成正式顾客会看到的页面。

源头文档更新：

- 更新 `docs/design/player-flow-page-spec.md`，新增数据、排行榜、积分礼遇上线级要求。
- 新增 `docs/reviews/phase-6-data-ranking-perks-review.md`，归档本阶段审查结论和验证证据。

代码变更：

- 更新 `miniprogram/utils/ladder-data.js`：
  - 新增同段位榜、微信好友榜。
  - 新增个人赛季数据。
  - 新增积分礼遇配置数据。
- 更新 `my-data`：
  - 展示当前段位、星级、本赛季胜率、有效挑战、当前连胜。
  - 展示店内、同段位、好友排名摘要。
- 更新 `rankings`：
  - 支持店内总榜、同段位榜、微信好友榜切换。
  - 移除“后续切换”等开发说明。
- 更新 `points-perks`：
  - 展示当前积分、兑换门槛、开台赠分。
  - 兑换方式改为顾客可理解的前台核销说明。

验证结果：

- JS 语法检查通过。
- JSON 解析检查通过，共 28 个 JSON 文件。
- 数据、排行、积分礼遇页面可见文案黑名单扫描无匹配。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `625.7 KB`。

审查结论：

- P2：数据、榜单和积分余额仍是本地占位数据，正式上线前必须接会员、比赛记录、积分流水和好友关系数据源。
- P2：排行榜切换还没有远程分页和刷新，接口阶段需要补。

下一项任务：

- Phase 7：员工端、老板端和电视大屏上线级打磨。

## 2026-05-27 Phase 7 员工端 / 老板端 / 大屏完成

本轮目的：补齐员工端、老板端和电视大屏的上线级骨架，避免只有球友端页面，无法覆盖门店现场运营。

源头文档更新：

- 新增 `docs/design/ops-owner-screen-page-spec.md`，约束员工端、老板端和大屏页面职责。
- 新增 `docs/reviews/phase-7-ops-owner-screen-review.md`，归档本阶段审查结论和验证证据。

代码变更：

- 更新 `miniprogram/app.json`，新增员工端、老板端、小程序大屏路由。
- 更新 `miniprogram/utils/ladder-data.js`：
  - 新增员工端球桌、积分核销用户、异常比赛数据。
  - 新增老板端配置数据。
  - 新增赏金猎人榜数据。
- 新增 `miniprogram/pages/staff-desk/`：
  - 今日球桌。
  - 设置开台到点时间。
  - 前台积分核销。
  - 异常比赛作废入口。
- 新增 `miniprogram/pages/boss-config/`：
  - 玩法模板。
  - 积分补给。
  - 防刷分门槛。
  - 大屏榜单。
- 新增 `miniprogram/pages/tv-ranking/`：
  - 店内总榜。
  - 赏金猎人榜。
  - 前三名领奖台。
  - 60 秒刷新行为。
- 新增 `screen/yunhan-tv-ranking.html`：
  - 小米电视浏览器可打开的 16:9 静态大屏页。
  - 60 秒自动刷新。
- 从 `miniprogram/app.json` 移除 `pages/ui-kit/ui-kit`，该页面只保留在仓库中做组件验收，不进入正式页面列表。

验证结果：

- JS 语法检查通过。
- JSON 解析检查通过，共 31 个 JSON 文件。
- 员工端、老板端、大屏端可见文案黑名单扫描无匹配。
- 按 `app.json` 正式页面列表做全局可见文案扫描，无匹配；`ui-kit` 不在正式页面列表。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `628.0 KB`。

审查结论：

- P1：员工端和老板端还没有权限校验，正式上线前必须接角色权限。
- P1：员工操作和老板配置还没有服务端操作日志，接口阶段必须补。
- P2：电视网页大屏数据仍是静态内容，正式上线前需要接大屏数据接口和 `screenToken`。
- 已修复：`ui-kit` 开发验收页不再进入正式 `app.json` 页面列表。

下一项任务：

- 进入接口、权限、状态机和真实数据阶段；页面骨架阶段已覆盖球友端、员工端、老板端和大屏端。

## 2026-05-27 Phase 8 权限与操作留痕前置

本轮目的：修掉员工端、老板端、小程序大屏页裸露的问题，并把员工/老板关键动作接入统一操作日志入口。正式上线不能让普通球友直接看到运营页面，也不能让核销、作废、保存配置这些动作没有留痕。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，补充前端权限与操作日志入口，并明确服务端仍必须重复校验权限。
- 更新 `docs/design/ops-owner-screen-page-spec.md`，补充员工端、老板端、大屏页的权限与操作留痕要求。
- 更新 `docs/design/player-flow-page-spec.md` 和 `docs/launch-readiness-execution-plan.md`，把共享本地数据入口统一改为 `miniprogram/utils/ladder-data.js`。
- 更新 `AGENTS.md` 和 `docs/launch-readiness-execution-plan.md`，把正式页面文案检查脚本纳入固定阶段验证。
- 新增 `docs/reviews/phase-8-access-operation-log-review.md`，归档本阶段审查结论和验证证据。

代码变更：

- 将共享本地数据文件从 `miniprogram/utils/ladder-data.js` 统一作为页面数据入口使用，清理旧 `ladder-mock` 引用。
- 新增 `miniprogram/utils/access-control.js`：
  - 员工端允许员工和老板进入。
  - 老板端仅允许老板进入。
  - 小程序大屏页允许员工、老板和大屏角色进入。
  - 权限未通过时返回球友首页，并提示当前账号暂无权限。
- 新增 `miniprogram/utils/operation-log.js`：
  - 员工设置开台到点时间写入日志入口。
  - 员工积分核销写入日志入口。
  - 员工作废异常比赛写入日志入口。
  - 老板保存门店配置写入日志入口。
- 受保护页面根节点增加 `accessReady` 条件，权限未通过前不渲染页面主体，避免重定向前短暂露出内容。
- 积分礼遇页把“出示本页”改成“出示会员码”，避免页面文案像内部说明。
- 新增 `scripts/check-production-copy.js`，自动扫描正式页面和电视大屏 HTML 的可见文案，命中内部校验、PM 说明、演示状态、mock、模拟、调试、临时、占位等痕迹时直接失败。

验证结果：

- JS 语法检查通过。
- `scripts/check-production-copy.js` 语法检查通过。
- JSON 解析检查通过，共 31 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- 正式页面列表可见文案黑名单扫描无匹配。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `634.4 KB`。

审查结论：

- 已修复：员工端、老板端、小程序大屏页裸露给普通角色的问题。
- 已修复：未授权页面可能在跳转前短暂渲染内容的问题。
- P1：前端权限不能替代服务端权限，接口阶段必须补服务端角色校验。
- P1：操作日志当前仍是本地记录，接口阶段必须写入服务端 `operation_logs`。
- P2：静态电视网页仍未接入 `screenToken`。

下一项任务：

- 进入接口层设计与落地：服务端权限、服务端操作日志、房间状态机、服务端计时和服务端结算。

## 2026-05-27 Phase 9 接口层收口

本轮目的：把页面对本地数据、操作日志和结算函数的直接依赖收口到 `miniprogram/services/`。这一步不是做假后端，而是为真实后端接入做接口口子，后续优先替换 service，不再到每个页面里散改。

源头文档更新：

- 新增 `docs/api-service-layer-contract.md`，定义 service 分层、页面调用规则、返回结构和验收命令。
- 更新 `docs/backend-integration-readiness-plan.md`，记录 Phase 9 接口层收口结果。
- 更新 `AGENTS.md`，新增接口层硬约束：业务页面不能直接引用本地数据和操作日志。
- 新增 `docs/reviews/phase-9-service-layer-review.md`，归档本阶段审查结论。

代码变更：

- 新增 `miniprogram/services/api-client.js`：统一 `ok/data` 返回结构和 `ensureOk` 错误处理。
- 新增 `miniprogram/services/player-service.js`：收口首页、房间、邀请、我的数据、排行榜、积分礼遇。
- 新增 `miniprogram/services/match-service.js`：收口玩法、开局参数、当前比赛、结算结果。
- 新增 `miniprogram/services/staff-service.js`：收口员工球桌、到点时间、积分核销、异常作废。
- 新增 `miniprogram/services/admin-service.js`：收口老板配置读取和保存。
- 新增 `miniprogram/services/screen-service.js`：收口小程序大屏榜单数据。
- 全部正式业务页面 JS 改为通过 service 获取数据和提交动作。
- 小程序大屏页刷新前先清理旧计时器，避免重复进入页面时创建多个刷新定时器。

阶段审查：

- P1：service 层仍未连接真实后端，下一阶段必须替换 `api-client`。
- P1：结算 service 当前内部仍调用本地计算函数，正式上线必须替换为服务端结算。
- P2：service 当前是同步返回结构，后续接 `wx.request` 或云函数时可能需要统一调整为异步调用。

验证结果：

- 页面结构检查通过：`miniprogram/pages` 无直接引用 `ladder-data` 或 `operation-log`。
- JS 语法检查通过。
- JSON 解析检查通过，共 31 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `641.5 KB`。

下一项任务：

- 进入真实后端选型与接入。必须先决定使用微信云开发、自建 Node 服务，还是先用云函数最小闭环；然后按 `docs/backend-integration-readiness-plan.md` 的优先级接服务端权限、房间状态机、服务端结算和积分流水。

## 2026-05-27 Phase 10 微信云开发骨架

本轮目的：先按微信云开发搭后端骨架。选择原因是 solo-op 维护成本最低，小程序登录态、OpenID、云函数、云数据库在一条链路里，暂时不需要额外租服务器和维护部署链路。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 10 云开发骨架说明。
- 更新 `docs/api-service-layer-contract.md`，记录 `callCloud` 替换顺序。
- 新增 `cloudfunctions/README.md`，说明云函数模块职责和未完成项。

代码变更：

- `project.config.json` 新增 `cloudfunctionRoot: "cloudfunctions/"`。
- `miniprogram/app.js` 增加安全的 `wx.cloud.init({ traceUser: true })`。
- `miniprogram/services/api-client.js` 预留 `callCloud(moduleName, action, payload)`。
- 新增 `cloudfunctions/yunhanApi/`：
  - `auth`：读取微信 OpenID。
  - `match`：预留房间状态和服务端结算。
  - `staff`：预留员工操作日志入口。
  - `admin`：预留老板操作日志入口。
  - `screen`：预留大屏 `screenToken` 校验。

阶段审查：

- P1：云函数当前只是骨架，角色读取仍未接 `store_members`。
- P1：`match.settle` 当前返回未启用，服务端结算公式还没落地。
- P1：云数据库集合尚未创建，`operation_logs`、`points_ledger`、`matches` 等必须在下一阶段建表。

验证结果：

- 小程序 JS 语法检查通过。
- 云函数 JS 语法检查通过。
- JSON 解析检查通过，共 32 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `642.2 KB`。

下一项任务：

- Phase 11：云数据库集合设计与服务端权限实现。优先建 `store_members`、`operation_logs`，让员工端/老板端云函数能真正按 OpenID + 角色判断权限。

## 2026-05-27 Phase 11 云数据库集合与服务端权限

本轮目的：把云函数权限从固定 TODO 推进到正式角色规则：按 `store_members` 查询 OpenID 在门店内的角色；员工/老板操作按服务端角色拦截。

源头文档更新：

- 新增 `docs/cloud-database-schema.md`，定义第一批云数据库集合、字段、索引建议和服务端权限规则。
- 更新 `docs/backend-integration-readiness-plan.md`，记录 Phase 11 云数据库集合和角色权限进展。
- 新增 `docs/reviews/phase-11-cloud-db-role-review.md`，归档本阶段审查结论。

代码变更：

- 更新 `cloudfunctions/yunhanApi/index.js`：
  - 新增 `getStoreId`。
  - 新增 `getMemberRole`，按 `store_members` 查询角色。
  - 新增 `roleAllowed` 和异步 `assertRole`。
  - 新增 `writeOperationLog`。
  - `auth` 返回 OpenID、storeId 和角色。
  - `staff` 模块要求 `staff` 或 `owner`。
  - `admin` 模块要求 `owner`。
  - 无成员记录时按普通 `player` 处理。

阶段审查：

- P1：云数据库集合尚未在微信云开发环境中创建。
- P1：缺少首个 owner 账号初始化流程。
- P1：服务端结算仍未实现。

验证结果：

- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过。
- JSON 解析检查通过，共 32 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `642.2 KB`。

下一项任务：

- Phase 12：补云开发初始化流程。重点是建集合、建索引、录入首个 `owner`，否则老板端云函数权限会因为缺少 `store_members` 记录被拒绝。

## 2026-05-27 Phase 12 云开发初始化与首个 owner 入库

本轮目的：补齐第一次上线接云开发时最容易卡住的初始化链路，尤其是首个老板账号。没有 owner 记录时，云函数会把当前用户视为普通球友，这是安全默认值；但也意味着必须有明确的初始化办法。

源头文档更新：

- 新增 `docs/cloud-init-runbook.md`，写清建集合、建索引、部署云函数、设置 `BOOTSTRAP_OWNER_SECRET`、获取 OpenID、初始化 owner、验证权限的步骤。
- 更新 `docs/backend-integration-readiness-plan.md`，记录 Phase 12 初始化方案。
- 更新 `docs/api-service-layer-contract.md`，记录 `auth.bootstrapOwner` 不做成前端页面。
- 更新 `cloudfunctions/README.md`，同步当前云函数职责。
- 新增 `docs/reviews/phase-12-cloud-init-review.md`，归档本阶段审查结论。

代码变更：

- 更新 `cloudfunctions/yunhanApi/index.js`：
  - 新增 `getExistingOwner`。
  - 新增 `auth.bootstrapOwner`。
  - `bootstrapOwner` 需要云函数环境变量 `BOOTSTRAP_OWNER_SECRET`。
  - 同一门店已有 `active owner` 后不能重复初始化。
  - 初始化成功后写入 `store_members`，并尽量写入 `operation_logs`。
  - 云函数 catch 现在会保留 `PERMISSION_DENIED` 等错误码。

阶段审查：

- P1：真实云环境仍需在微信开发者工具中创建集合、部署云函数、设置环境变量。
- P1：`BOOTSTRAP_OWNER_SECRET` 初始化后必须删除或轮换。
- P1：前端 service 尚未切到云函数。

验证结果：

- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过，共 37 个 JS 文件。
- JSON 解析检查通过，共 32 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `642.2 KB`。

下一项任务：

- Phase 13：把 `staff-service` 和 `admin-service` 的写操作接入 `callCloud`，让员工端/老板端操作真正走云函数权限和 `operation_logs`。

## 2026-05-27 Phase 13 员工端与老板端写操作接入云函数

本轮目的：先把运营端写操作接到云函数，避免员工/老板操作继续本地伪成功。读数据暂时保留本地服务层，降低一次性迁移风险。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 13 写操作接入范围。
- 更新 `docs/api-service-layer-contract.md`，标记 `staff-service` 和 `admin-service` 写操作已接入 `callCloud`。
- 新增 `docs/reviews/phase-13-cloud-write-ops-review.md`，归档本阶段审查结论。

代码变更：

- `miniprogram/services/staff-service.js`：
  - `updateTableDueTime` 改为先调用 `callCloud("staff", "updateTableDueTime")`。
  - `deductMemberPoints` 改为先调用 `callCloud("staff", "deductMemberPoints")`。
  - `voidAbnormalMatch` 改为先调用 `callCloud("staff", "voidAbnormalMatch")`。
  - 移除本地 `operation-log` 依赖。
- `miniprogram/services/admin-service.js`：
  - `saveAdminConfig` 改为先调用 `callCloud("admin", "saveConfig")`。
  - 保存配置 payload 改为传完整 `config`。
  - 移除本地 `operation-log` 依赖。
- `miniprogram/pages/staff-desk/staff-desk.js` 和 WXML：
  - 写操作改为 async。
  - 保存到点时间、积分核销、异常作废按钮增加 loading。
  - 云函数失败时展示失败 toast。
- `miniprogram/pages/boss-config/boss-config.js` 和 WXML：
  - 保存配置改为 async。
  - 保存按钮增加 loading。
  - 云函数失败时展示失败 toast。

阶段审查：

- P1：真实云环境未初始化时，写操作会返回云端不可用或权限失败，不能回退到本地伪成功。
- P1：员工积分核销仍缺少稳定用户 ID。
- P1：老板配置写操作已传完整配置，但云端尚未持久化。

验证结果：

- 页面直接引用本地数据/本地日志检查无命中。
- service 本地 `operation-log` 检查无命中。
- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过，共 37 个 JS 文件。
- JSON 解析检查通过，共 32 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `656.1 KB`。

下一项任务：

- Phase 14：补云端真实持久化。优先顺序：`admin_configs` 保存、员工到点时间写入、积分核销写入 `points_ledger`、异常比赛写入 `matches.status = voided`。

## 2026-05-27 Phase 14 云端真实持久化第一版

本轮目的：让云函数不再只记操作日志，而是开始写正式业务集合。

源头文档更新：

- 更新 `docs/cloud-database-schema.md`，新增 `member_points`、`table_sessions`、`admin_configs`。
- 更新 `docs/cloud-init-runbook.md`，补充新增集合和索引。
- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 14 云端持久化范围。
- 更新 `cloudfunctions/README.md`，同步云函数当前写库职责。
- 新增 `docs/reviews/phase-14-cloud-persistence-review.md`，归档本阶段审查结论。

代码变更：

- `cloudfunctions/yunhanApi/index.js`：
  - 新增 `requirePayloadValue`、`isFailureResult`、`upsertOne`。
  - `admin.saveConfig` 写入或更新 `admin_configs`。
  - `staff.updateTableDueTime` 写入或更新 `table_sessions`。
  - `staff.deductMemberPoints` 要求会员 OpenID，读取并扣减 `member_points`，写入 `points_ledger`。
  - `staff.voidAbnormalMatch` 先按 `storeId + matchId` 校验，再更新 `matches.status = voided`。
  - `voidAbnormalMatch` 不再只按 `matchId` 更新，避免跨门店误改。
- `miniprogram/services/staff-service.js` 和 `staff-desk.js`：
  - 核销 payload 预留并传递 `openid`。

阶段审查：

- P1：真实云环境尚未部署验证。
- P1：积分扣减暂未使用数据库事务。
- P1：员工端核销缺少会员 OpenID。
- P1：异常作废依赖真实 `matches` 文档。

验证结果：

- 页面直接引用本地数据/本地日志检查无命中。
- service 本地 `operation-log` 检查无命中。
- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过，共 37 个 JS 文件。
- JSON 解析检查通过，共 32 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `656.2 KB`。

下一项任务：

- Phase 15：员工端真实会员搜索/扫码识别。目标是让前台核销拿到真实 `openid` 或 `memberId`，并移除当前默认会员样例对核销流程的影响。

## 2026-05-27 Phase 15 员工端会员扫码识别

本轮目的：把员工端核销从“默认样例会员”改成“扫码选择真实会员”。没有会员 OpenID 时，不允许核销。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 15 员工端会员扫码识别。
- 更新 `docs/cloud-database-schema.md`，给 `member_points` 增加会员昵称和备注名字段。
- 新增 `docs/reviews/phase-15-staff-member-scan-review.md`，归档本阶段审查结论。

代码变更：

- `cloudfunctions/yunhanApi/index.js`：
  - 新增 `staff.getMemberForExchange`。
  - 服务端按 `member_points` 查询会员积分账户。
- `miniprogram/services/staff-service.js`：
  - 新增 `getMemberForExchange`。
  - `getStaffDeskData` 不再返回默认核销会员。
- `miniprogram/pages/staff-desk/staff-desk.js`：
  - 新增 `scanCode` Promise 包装。
  - 新增 `parseMemberOpenid`，兼容 JSON、URL query、`openid:` 文本和纯 OpenID。
  - 新增 `scanMember`。
  - 核销前必须存在 `selectedMember`。
- `miniprogram/pages/staff-desk/staff-desk.wxml` 和 WXSS：
  - 核销区改为未选择会员状态。
  - 增加扫码选择按钮。
  - 选中会员后只展示“积分账户已匹配”，不展示 OpenID。
  - 未选择会员时禁用“确认核销”。

阶段审查：

- P1：球友端会员码生成入口尚未实现。
- P1：扫码后仍依赖云端 `member_points`。
- P2：员工端暂无手动搜索兜底。

验证结果：

- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过，共 37 个 JS 文件。
- JSON 解析检查通过，共 32 个 JSON 文件。
- 正式页面文案脚本检查通过，19 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `661.8 KB`。

下一项任务：

- Phase 16：补球友端会员码页面或入口，固定二维码内容格式，让员工扫码有正式来源。

## 2026-05-27 Phase 16 球友端会员码

本轮目的：给员工端扫码核销补正式来源。球友在积分页进入会员码页面，前台扫码后拿到当前用户 OpenID，再去 `member_points` 查询积分账户。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 16 球友端会员码。
- 更新 `cloudfunctions/README.md`，同步 `member` 模块职责。
- 新增 `docs/reviews/phase-16-member-code-review.md`，归档本阶段审查结论。

代码变更：

- `cloudfunctions/yunhanApi/package.json`：
  - 新增 `qrcode` 依赖。
- `cloudfunctions/yunhanApi/index.js`：
  - 新增 `member.getCode`。
  - 使用当前微信 OpenID 生成会员码二维码。
- 新增 `miniprogram/services/member-service.js`。
- 新增 `miniprogram/pages/member-code/`：
  - 生成中状态。
  - 会员码展示。
  - 失败状态。
  - 刷新会员码。
- `miniprogram/app.json` 新增会员码页面路由。
- `points-perks` 新增“出示会员码”入口。

阶段审查：

- P1：真实云函数部署时必须安装 `qrcode` 依赖。
- P1：会员积分账户创建链路仍未完成。
- P2：二维码图像渲染需要真机确认。

验证结果：

- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过，共 39 个 JS 文件。
- JSON 解析检查通过，共 33 个 JSON 文件。
- 正式页面文案脚本检查通过，20 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `667.6 KB`。

下一项任务：

- Phase 17：补会员积分账户创建与积分发放。至少要覆盖新用户初始积分、开台赠分、积分流水写入，以及老板端参数读取。

## 2026-05-27 Phase 17 会员积分账户创建与初始积分发放

本轮目的：让会员码页面不只是出示二维码，还能确保当前用户有积分账户。第一次生成会员码时创建 `member_points`，并按老板配置发放新用户初始积分。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 17 会员积分账户创建与初始积分发放。
- 新增 `docs/reviews/phase-17-member-points-account-review.md`，归档本阶段审查结论。

代码变更：

- `cloudfunctions/yunhanApi/index.js`：
  - 新增 `DEFAULT_POINTS_CONFIG`。
  - 新增 `getStorePointsConfig`。
  - 新增 `ensureMemberPointAccount`。
  - `member.getCode` 生成二维码前会确保积分账户存在。
  - 首次创建账户时写入 `points_ledger(type=initial)`。
- `miniprogram/pages/member-code/`：
  - 会员码页面展示当前积分。

阶段审查：

- P1：真实云环境尚未执行闭环验证。
- P1：开台赠分尚未接入。
- P1：初始积分发放暂未事务化。

验证结果：

- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过，共 39 个 JS 文件。
- JSON 解析检查通过，共 33 个 JSON 文件。
- 正式页面文案脚本检查通过，20 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `667.9 KB`。

下一项任务：

- 先做真实云环境部署和真机扫码闭环验证，再继续服务端结算。没有真云闭环前，继续写更多后端逻辑会让风险叠高。

## 2026-05-27 Phase 18 云开发部署前检查

本轮目的：不继续堆比赛结算逻辑，先确认微信云开发链路能不能跑。

源头文档更新：

- 更新 `docs/wechat-devtools-cli.md`，修正项目路径、当前登录态、云开发 CLI 命令和部署纪律。
- 更新 `docs/cloud-init-runbook.md`，补充 CLI 部署方式。
- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 18 云开发部署前检查。
- 新增 `docs/reviews/phase-18-cloud-readiness-review.md`，归档本阶段审查结论。

代码 / 脚本变更：

- 新增 `scripts/check-wechat-cloud-readiness.ps1`：
  - 检查微信开发者工具 CLI 路径和项目路径。
  - 检查登录态，`{"login":false}` 时直接阻断。
  - 检查云环境列表。
  - 支持传入 `-EnvId` 检查云函数列表和 `yunhanApi` 信息。
  - 支持传入 `-Deploy`，使用 `--remote-npm-install` 部署 `yunhanApi`。
  - 源码保持 ASCII，避免 Windows PowerShell 5 解析 UTF-8 无 BOM 脚本时把中文字符串解析坏。

阶段审查：

- P0：当前 AppID 被微信开发者工具识别为测试号，`cloud env list` 返回“测试号不能使用云服务”。
- P1：`yunhanApi` 依赖 `qrcode`，正式部署必须使用云端安装依赖。

验证结果：

- `scripts/check-wechat-cloud-readiness.ps1` 可执行，能完成登录态检查，并在云环境列表阶段稳定识别当前阻塞。
- `islogin` 通过，当前微信开发者工具已登录。
- `cloud functions deploy --help` 通过，确认支持 `--remote-npm-install`。
- `cloud env list` 未通过，返回“测试号不能使用云服务”。
- 云函数 JS 语法检查通过。
- 小程序 JS 语法检查通过，共 39 个 JS 文件。
- JSON 解析检查通过，共 33 个 JSON 文件。
- 正式页面文案脚本检查通过，20 个文件无违规文案。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，包体 `667.9 KB` / `683961` bytes。

下一项任务：

- 必须先切换到已注册小程序 AppID，并创建微信云开发环境。拿到云环境 ID 后运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID'
```

- 检查通过后再执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check-wechat-cloud-readiness.ps1 -EnvId '你的云环境ID' -Deploy
```

