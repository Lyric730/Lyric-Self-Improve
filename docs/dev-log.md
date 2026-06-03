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

## 2026-05-31 正式小程序 AppID 接入

本轮目的：把微信开发者工具项目身份从旧测试 AppID 切换到正式小程序 AppID，为云开发检查和云函数部署做前置准备。

变更：

- `project.config.json` 的 `appid` 更新为 `wxe30b469d64636a2b`。
- `scripts/check-wechat-cloud-readiness.ps1` 默认项目路径更新为 `F:\Making money\taiqiuxcx`。
- `AGENTS.md` 和 `docs/wechat-devtools-cli.md` 同步当前本地项目路径。
- `docs/cloud-init-runbook.md` 同步当前项目路径。

注意：

- 之前 `F:\Making money\Lyric-Self-Improve\projects\taiqiuxcx` 目录当前只剩少量私有配置，不是完整小程序目录。
- 当前完整小程序目录为 `F:\Making money\taiqiuxcx`。

下一步：

- 用微信开发者工具 CLI 打开当前项目，确认工具识别正式 AppID。
- 再运行云开发检查，判断是否已经可以创建或读取云环境。

验证结果：

- `node scripts\check-json-files.js` 通过，共 32 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 20 个正式页面文件。
- 小程序 JS 语法检查通过，共 39 个 JS 文件。
- 微信开发者工具 CLI preview 通过，包体 `667.9 KB` / `683963` bytes。
- preview 输出 `使用 AppID: wxe30b469d64636a2b`，说明项目身份已切换成功。
- 云开发检查不再返回“测试号不能使用云服务”，当前返回 `ret:1000 system error`。

新的阻塞：

- 需要在微信开发者工具 UI 中打开“云开发”，确认云环境是否已创建。
- 如果云开发入口提示无权限，需要小程序管理员把当前登录微信号加入项目成员，并授予开发 / 云开发相关权限。

## 2026-06-01 Phase 19 结算规则纯函数与本地测试

本轮目的：云环境暂时不能创建时，先把最核心的积分、随机奖励、最低时间和段位星级规则做成可测试纯函数，避免明天接云函数时还在页面里散算。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 19。
- 更新 `docs/api-service-layer-contract.md`，说明当前前端结算展示已接入规则引擎，后续云函数必须复用同一口径。
- 新增 `docs/reviews/phase-19-settlement-engine-review.md`，归档本阶段审查结论。

代码变更：

- 新增 `miniprogram/utils/settlement-engine.js`：
  - `calculateMatchSettlement`
  - `calculateRankChange`
  - `calculateRewardValue`
  - `getRewardPhase`
  - `normalizeMode`
  - `formatRankTitle`
- 新增 `scripts/test-settlement-engine.js`：
  - 覆盖抢 5 结算。
  - 覆盖抢 7 结算。
  - 覆盖最低有效时间不足。
  - 覆盖非法底分。
  - 覆盖第 4 大局续时冲刺奖励。
  - 覆盖黄金保护和铂金掉星。
  - 覆盖抢 7 加 2 星跨小段。
- 更新 `miniprogram/utils/ladder-data.js`：
  - `buildSettlement` 改为调用 `calculateMatchSettlement`。
  - 前端结算展示和本地测试规则同源。

验证结果：

- `node scripts\test-settlement-engine.js` 通过，输出 `Settlement engine tests OK`。
- `node --check miniprogram\utils\settlement-engine.js` 通过。
- `node --check miniprogram\utils\ladder-data.js` 通过。
- `node --check miniprogram\services\match-service.js` 通过。
- 抽样结算：抢 5、底分 100、倍率 3、比分 5:3、奖励 120，风险积分 300，胜方 +420，败方 -180。
- 微信开发者工具 CLI preview 通过，当前端口为 `49663`，包体 `679.1 KB` / `695420` bytes，AppID 为 `wxe30b469d64636a2b`。

阶段审查：

- P1：云函数 `match.settle` 仍未启用。
- P1：本地测试不能覆盖数据库并发、重复结算、重复加星。
- P2：前端和云函数暂未共享同一份物理规则文件，云端接入时要做一致性处理。

下一项任务：

- 云环境未创建前，可以继续做管理员参数校验、页面异常态、榜单数据结构和大屏 token 设计。
- 云环境创建后，优先把 `match.settle` 接到云函数，并写入 `settlements`、`points_ledger`、`rank_states`。

## 2026-06-01 Phase 20 老板端参数校验

本轮目的：云环境明天才能创建时，先补上线前的参数护栏。老板可以调整底分、倍率、随机奖励、积分补给、防刷分和大屏参数，但保存前必须先判断配置是否能被系统安全使用。

源头文档更新：

- 更新 `docs/backend-integration-readiness-plan.md`，新增 Phase 20。
- 更新 `docs/api-service-layer-contract.md`，记录 `admin-config-validator` 和云端后续复用要求。
- 新增 `docs/reviews/phase-20-admin-config-validation-review.md`，归档本阶段审查结论。

代码变更：

- 新增 `miniprogram/utils/admin-config-validator.js`：
  - 校验玩法模板、底分、倍率、随机奖励、胜方加星、最低有效时间。
  - 禁止抢 9 进入玩法模板。
  - 校验新用户积分、到店登录积分、开台赠分、兑换门槛。
  - 校验店内定位范围、大屏榜单和刷新间隔。
- 新增 `scripts/test-admin-config-validator.js`。
- `miniprogram/services/admin-service.js` 保存配置前执行 `assertValidAdminConfig`。
- `miniprogram/pages/boss-config/boss-config.js` 保存前执行 `validateAdminConfig`，失败时弹出正式用户提示。

验证结果：

- `node scripts\test-admin-config-validator.js` 通过，输出 `Admin config validator tests OK`。
- `node scripts\test-settlement-engine.js` 通过，输出 `Settlement engine tests OK`。
- 小程序 JS 语法检查通过，共 41 个 JS 文件。
- 云函数 JS 语法检查通过。
- JSON 解析检查通过，共 32 个 JSON 文件。
- 正式页面文案脚本检查通过，共 20 个文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，当前端口为 `49663`，包体 `686.4 KB` / `702871` bytes，AppID 为 `wxe30b469d64636a2b`。
- 云开发检查仍被微信侧阻塞：`cloud env list` 返回 `ret:1000 system error`。

阶段审查：

- P1：云函数 `admin.saveConfig` 仍未复用该校验，真实云环境可用后必须补。
- P2：老板端目前还是配置展示页，尚未做完整编辑表单。

下一项任务：

- 云环境未创建前，继续做页面异常态或大屏 `screenToken` 结构设计。

## 2026-06-01 Phase 21 开发者工具预览通道

本轮目的：解决当前没有云环境时，微信开发者工具里无法继续完整流程、无法进入员工端和老板端的问题，同时不把这些入口暴露给正式用户。

问题根因：

- 等待房间按正式上线逻辑只等待真实对手加入；没有房间状态接口时，页面会停在“等待对手加入”。
- 员工端、老板端按正式权限读取 `yunhanUserRole`；默认角色是 `player`，所以普通球友不能进入运营端。

代码变更：

- 新增 `miniprogram/utils/dev-preview.js`。
- `challenge-home` 在微信开发者工具里显示“预览通道”，可进入员工端、老板端和大屏榜单。
- 进入员工端 / 老板端 / 大屏时，只在微信开发者工具里写入对应预览角色。
- `waiting-room` 在微信开发者工具里显示“继续选玩法”，用于无后端时继续走球友流程。

边界：

- 入口由 `wx.getSystemInfoSync().platform === "devtools"` 控制。
- 真机、体验版、正式版不显示这些入口。
- 正式页面仍不出现 `mock`、`模拟`、`调试`、`演示` 等违规文案。

验证结果：

- `node --check miniprogram\utils\dev-preview.js` 通过。
- `node --check miniprogram\pages\challenge-home\challenge-home.js` 通过。
- `node --check miniprogram\pages\waiting-room\waiting-room.js` 通过。
- `node scripts\check-production-copy.js` 通过，共 20 个正式页面文件。
- `node scripts\check-json-files.js` 通过，共 33 个 JSON 文件。

## 2026-06-01 Phase 22 控件尺寸、老板端编辑和大屏响应式修复

本轮目的：修正实际预览中暴露的三个上线级问题：按钮/分段控件尺寸撑破页面、老板端只能看不能改、大屏榜单在手机模拟器里横向溢出。

问题根因：

- `yh-button` 最初按主按钮和大视觉组件设计，缺少在小容器里的收缩约束。
- `option-chip` 使用原生 button，但没有完整设置 `width / padding / line-height / overflow`，在分段选择中容易撑破。
- 老板端页面仍停留在配置展示，没有输入控件。
- 大屏页默认按横屏电视三栏布局写死，手机模拟器宽度下每列过窄，内部固定列宽继续溢出。

代码变更：

- 更新 `miniprogram/components/yh-button/yh-button.wxss`：
  - 增加 `max-width: 100%`、`min-width: 0`、文本省略。
  - icon-only 按钮允许在父容器中收缩。
- 更新 `miniprogram/styles/player-flow.wxss`：
  - 重做 `option-chip` 的尺寸和溢出约束。
  - 重做计分页 `stepper-grid` 和 `stepper-box`，让加减盘按钮按双列稳定排列。
- 更新 `miniprogram/pages/match-scoring/match-scoring.wxml`：
  - 给计分按钮增加 `custom-class="stepper-button"`。
- 更新 `miniprogram/pages/boss-config/`：
  - 玩法、底分、倍率、随机奖励、最低时间、胜方加星可编辑。
  - 新用户积分、到店登录、开台赠分、兑换门槛可编辑。
  - 防刷分和大屏榜单参数可编辑。
  - 保存前继续走 `validateAdminConfig`。
- 更新 `miniprogram/services/admin-service.js`：
  - 微信开发者工具里允许本地保存配置，方便云环境未创建前预览。
  - 真机和正式环境仍然走云函数，不做本地伪成功。
- 更新 `miniprogram/pages/tv-ranking/tv-ranking.wxss`：
  - 默认使用单列移动预览布局。
  - `@media (min-width: 900px)` 时切回三栏电视布局。

验证结果：

- `node scripts\test-admin-config-validator.js` 通过。
- `node scripts\test-settlement-engine.js` 通过。
- 小程序 JS 语法检查通过，共 42 个 JS 文件。
- 云函数 JS 语法检查通过。
- JSON 解析检查通过，共 33 个 JSON 文件。
- 正式页面文案脚本检查通过，共 20 个文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，端口 `49663`，包体 `697.3 KB` / `714068` bytes。

仍需人工复看：

- 微信开发者工具模拟器截图接口不可用，最终视觉是否足够规整仍需要在模拟器里逐页看。
- 真正电视横屏效果需要等小米电视或宽屏浏览环境测试。

## 2026-06-02 Phase 23 底分倍率页与前台工作台紧凑控件修复

本轮目的：解决实际预览中底分 / 倍率页、前台工作台仍然使用大按钮尺寸，导致分段选择器和操作按钮挤压、撑满、比例不对的问题。

问题根因：

- Phase 22 主要修的是全局 `yh-button` 和通用 `option-chip` 的溢出边界，但这两类页面需要的是页面级紧凑控件，不应该继续套主视觉按钮尺寸。
- 底分 / 倍率页的底分、倍率选择，本质是参数分段选择器，不是大按钮。
- 前台工作台是员工高频操作页，需要更低高度、更稳定的网格、更小的扫码/保存/核销按钮，减少上手成本。

代码变更：

- 更新 `miniprogram/pages/points-select/points-select.wxml` 与 `points-select.wxss`：
  - 底分、倍率选择器改为 `points-selector-grid` / `points-selector-chip`。
  - 选择器改为低高度内嵌分段控件，四角全部切角。
  - 确认按钮从 `lg` 改为 `md`，并限制最大宽度。
- 更新 `miniprogram/pages/staff-desk/staff-desk.wxml` 与 `staff-desk.wxss`：
  - 到点时间、扣分选择改为 `staff-option-grid` / `staff-option-chip`。
  - 四个时间选项按 4 列稳定排列，扣分选项按 3 列排列。
  - 扫码选择、保存到点时间、确认核销、作废异常按钮改为员工端紧凑尺寸。
  - 今日球桌、会员卡片的内边距和切角同步收紧。

验证结果：

- 小程序 JS 语法检查通过。
- `node scripts\check-json-files.js` 通过，共 33 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 20 个正式页面文件。
- `scripts/check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，32 个 PNG 资产无贴边。
- 微信开发者工具 CLI preview 通过，端口 `49663`，包体 `701.1 KB` / `717931` bytes。

审查归档：

- `docs/reviews/phase-23-compact-controls-review.md`

## 2026-06-02 Phase 24 底分倍率控件结构重做与到点时间 Picker

本轮目的：继续处理实际预览反馈：底分 / 倍率页的组件尺寸仍像被挤坏的按钮条，前台工作台的到点时间不应使用固定预设按钮。

问题根因：

- 底分 / 倍率页仍使用小程序原生 `button` 作为网格选项。即使覆盖了样式，原生按钮在实际渲染中仍容易出现默认尺寸、文本对齐和宽度异常。
- 倍率选项有 5 个，继续用横向分段条会天然挤压第二行，不适合当前页面宽度。
- 到点时间不是固定的四个选项，员工需要能选择任意 `HH:mm`，并且保持 24 小时制。

代码变更：

- 更新 `miniprogram/pages/points-select/points-select.wxml` 与 `points-select.wxss`：
  - 底分 / 倍率选项从原生 `button` 改为普通 `view` 选项块。
  - 使用 `points-choice-grid` / `points-choice` 完全控制尺寸、切角、间距和选中态。
  - 底分 3 列，倍率 3 列自动换行，避免长条挤压。
- 更新 `miniprogram/pages/staff-desk/`：
  - 到点时间从预设按钮改为 `<picker mode="time">`。
  - 支持 `00:00` 到 `23:59`，实际选择几时几分。
  - 页面展示为一个紧凑的时间选择入口，保存逻辑继续沿用 `selectedTime`。

验证结果：

- `node --check miniprogram\pages\staff-desk\staff-desk.js` 通过。
- `node scripts\check-json-files.js` 通过，共 33 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 20 个正式页面文件。
- `git diff --check` 通过。
- 微信开发者工具 CLI preview 通过，端口 `49663`，包体 `701.9 KB` / `718755` bytes。

审查归档：

- `docs/reviews/phase-24-selector-picker-review.md`

## 2026-06-02 Phase 25 前台积分核销输入框与开发者工具刷新

本轮目的：根据实际预览反馈，将前台积分核销从固定扣分档位改为员工填写扣除分数，并处理微信开发者工具模拟器启动失败。

问题根因：

- 前台兑换场景不是固定 `100 / 200 / 500` 三档，员工需要按兑换品实际分值填写扣除多少分。
- 固定档位继续使用按钮网格，会再次出现尺寸挤压问题，也会增加员工理解成本。
- 模拟器报 `TypeError: Failed to fetch` 时，`127.0.0.1:49663` 服务仍可访问，但根路径返回 404；说明端口未完全断开，更像开发者工具内部文件服务或编译状态卡住。

代码变更：

- 更新 `miniprogram/pages/staff-desk/staff-desk.wxml`：
  - 移除 `100 / 200 / 500` 固定扣分按钮。
  - 新增数字输入框，员工填写本次扣除积分。
- 更新 `miniprogram/pages/staff-desk/staff-desk.js`：
  - 新增 `deductPointsInput` / `deductPoints`。
  - 输入值只保留数字。
  - 核销前校验：必须先选择会员、扣分必须为正整数、不能超过已知会员余额。
- 更新 `miniprogram/pages/staff-desk/staff-desk.wxss`：
  - 新增 `deduct-input-card` / `deduct-input-box` / `deduct-input`。
  - 删除旧固定扣分按钮样式。

开发者工具处理：

- 探测 `http://127.0.0.1:49663`：端口有响应，根路径返回 404。
- 执行 CLI：
  - `islogin`：通过。
  - `reset-fileutils`：通过。
  - `open --project`：通过。
  - `preview --project`：通过，包体 `703.7 KB` / `720579` bytes。

验证结果：

- `node --check miniprogram\pages\staff-desk\staff-desk.js` 通过。
- `node scripts\check-json-files.js` 通过，共 33 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 20 个正式页面文件。
- `git diff --check` 通过。

审查归档：

- `docs/reviews/phase-25-staff-deduct-input-review.md`

## 2026-06-02 Phase 26 段位星星重做与“我的”身份入口

本轮目的：处理实际预览反馈：段位星星抠图不干净、排列不齐；底部 Tab 需要新增“我的”，个人信息、会员工具、员工端、老板端和电视大屏入口统一收进“我的”。

问题根因：

- 旧星星依赖切图资源，图片边缘不干净时会在深色背景上露出杂边；不同状态的图片视觉边界不一致，也会导致排列看起来不齐。
- 员工 / 老板 / 大屏入口原先放在首页调试区，容易让首页变成演示入口集合，不符合正式上线的玩家首屏。
- 底部导航只有挑战 / 数据 / 排行 / 积分，缺少承载个人资料、会员码和身份切换的稳定入口。

代码变更：

- 更新 `miniprogram/components/star-track/`：
  - 不再使用星星 PNG 切图。
  - 改为统一的 5 列固定星位，使用文本星形绘制不同状态。
  - 每颗星使用固定宽高和居中对齐，保证当前段位卡片中的星星整齐排列。
- 新增 `miniprogram/components/bottom-nav/`：
  - 统一底部导航组件。
  - 新增第五项“我的”。
  - 统一处理挑战、数据、排行、积分、我的之间的跳转。
- 新增 `miniprogram/pages/my-hub/`：
  - 展示当前会员资料。
  - 集中会员码、积分礼遇、我的数据、排行榜等常用工具。
  - 将员工端、老板端、电视大屏入口统一放在“身份切换”区域。
- 更新 `miniprogram/app.json` 与相关页面：
  - 注册 `pages/my-hub/my-hub`。
  - 首页、我的数据、排行榜、积分礼遇、会员码页改用统一 `bottom-nav`。
  - 移除首页正式页面里的预览 / 内部入口区，避免上线页面继续出现演示内容。

验证结果：

- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `git diff --check` 通过，仅有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，端口 `49663`，AppID `wxe30b469d64636a2b`，包体 `710.1 KB` / `727139` bytes。

审查归档：

- `docs/reviews/phase-26-star-track-my-hub-review.md`

## 2026-06-03 Phase 27 全局视觉减黑与动效基础层

本轮目的：按最新视觉反馈优化第一轮 UI 源头组件。方向不改变“黑橙竞技”，但降低纯黑占比，增加台呢绿、木纹棕、金属压条和奖励牌匾的材质层次；同时把已抠图资产接回关键组件。

问题根因：

- 当前页面大量使用接近纯黑的背景和面板，导致整体视觉过暗，层次像“黑色后台套橙色按钮”。
- 通用面板、底部导航、选择控件都偏同质化，未充分体现设计稿里的台球桌边框、金属压条、记分灯板、奖励牌匾四类组件语言。
- 星星此前为快速解决脏边改成字符渲染，但设计系统要求复杂星级状态使用正式 PNG 资产。
- 动效只有按钮按压、数字弹动和 loading，没有页面进场、星星点亮、奖励浮动、比分闪烁这类基础动效层。

代码变更：

- 更新 `miniprogram/styles/tokens.wxss`：调整背景、面板、台呢绿、木纹棕、金属灰、金色和橙色 token，并新增材质 surface token。
- 更新 `miniprogram/styles/motion.wxss`：新增页面进场、奖励浮动、星星点亮、比分闪烁和 reduced motion 降级规则。
- 更新 `miniprogram/app.wxss` 与 `miniprogram/styles/player-flow.wxss`：页面背景从单一深黑改为台呢绿深层、木质球桌边、暖黑底纹组合。
- 更新 `miniprogram/components/yh-panel/`：通用面板改为设备面板质感，加入顶部金属压条和角落圆弧装饰。
- 更新 `miniprogram/components/star-track/`：固定五格布局保留，星星重新接入 `star-empty`、`star-earned`、`star-new`、`star-protected`、`star-lost` PNG 资产。
- 更新 `miniprogram/components/reward-crate/`：宝箱资产继续使用正式 PNG，背景改为奖励牌匾质感，宝箱加入轻微浮动。
- 更新 `miniprogram/components/rank-badge/`、`victory-banner/`、`accept-stamp/`、`settlement-badge/`：让段位、胜利、确认章、加减分卡更突出已有美术资产。
- 更新 `miniprogram/components/bottom-nav/`、`mode-card/`、`points-select/`：底部导航、模式卡和底分倍率控件未选态更接近金属压条，选中态保持橙色。

验证结果：

- WXSS 笔误扫描通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- `git diff --check` 通过，仅有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `719.3 KB` / `736572` bytes。

仍需人工复看：

- 本轮是源头组件和视觉材质第一轮，不等于逐页最终打磨。
- 需要在微信开发者工具模拟器里重点复看：首页、底分倍率、计分页、结算页、我的页、员工端、大屏页的实际观感。
- 员工端如果仍显得太游戏化，下一轮应单独降低员工端装饰强度。

审查归档：

- `docs/reviews/phase-27-visual-material-motion-review.md`

## 2026-06-03 Phase 28 字符星回退、去绿色成功态与视觉二轮修正

本轮目的：按实际预览反馈继续做上线级视觉修正。用户确认星星 PNG 资产没扣干净，正式页面先用字符星；同时当前视觉不接受绿色成功态，确认、可结算、已完成统一改为金色 / 橙金反馈。

问题根因：

- 星星 PNG 虽然通过边缘脚本，但实际深色页面上仍有脏边和观感不齐，说明自动边缘检查不能替代真实设备视觉验收。
- 旧文档仍把“成功 / 可结算”写成绿色，后续前端容易按旧口径做回绿色。
- `wx.showToast({ icon: "success" })` 会触发微信原生成功图标，视觉上可能出现绿色反馈。
- 多个组件引用了共享动效名，但组件 WXSS 没有显式导入 `motion.wxss`，在组件样式隔离下存在动画不生效风险。

代码变更：

- 更新 `miniprogram/components/star-track/`：
  - 移除星星 PNG 引用。
  - 使用字符星 `★ / ☆` 渲染空星、亮星、新增星、保护星和掉星。
  - 保留 5 列固定网格、固定宽高和居中对齐，解决排列不齐。
- 更新 `miniprogram/styles/tokens.wxss`、`miniprogram/app.wxss`、`miniprogram/styles/player-flow.wxss`：
  - 移除此前引入的绿色 / 台呢绿视觉倾向。
  - 背景和面板改为暖黑、木纹棕、橙金光。
- 更新 `miniprogram/components/yh-button/`、`yh-panel/`、`staff-desk/`：
  - `success` 视觉从绿色改为金色确认态。
  - 禁用态不参与确认按钮呼吸动效。
  - 前台已选会员状态从绿色发光改为金色 / 橙金选中态。
- 更新 `miniprogram/pages/boss-config/boss-config.js`、`miniprogram/pages/staff-desk/staff-desk.js`：
  - 原生成功 toast 全部改为 `icon: "none"`，避免微信绿色成功图标。
- 更新 `miniprogram/components/star-track/`、`yh-panel/`、`reward-crate/`、`rank-badge/`、`settlement-badge/`、`victory-banner/`：
  - 补充导入 `motion.wxss`，保证共享动效在组件内可用。
- 更新源头文档：
  - `AGENTS.md`
  - `docs/prd-taiqiu-ladder-mvp.md`
  - `docs/ladder-plan/02-core-rules.md`
  - `docs/ui-design-style-guide-yunhan.md`
  - `docs/design/component-traceability-map.md`
  - `docs/design/ui-asset-map.md`
  - `docs/design/yunhan-codable-design-system-spec.md`
  - `docs/design/ui-kit-task-tracker.md`

验证结果：

- 绿色残留扫描通过：旧绿色十六进制、绿色 rgba、`green` 关键字在 `miniprogram` 可见代码中无命中。
- 原生绿色 toast 扫描通过：正式页面内无 `icon: "success"`。
- WXSS 笔误扫描通过。
- 全量 `miniprogram` JS `node --check` 通过，共 44 个 JS 文件。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- `git diff --check` 通过，仅有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `721.1 KB` / `738384` bytes。

审查结论：

- P1 已修：共享动效组件缺少 `motion.wxss` 导入，可能导致动画不生效。
- P2 已修：文档和代码对“成功态是否绿色”的口径不一致。
- P2 已修：星星 PNG 资产实际观感不达标，当前正式实现改回字符星。

仍需人工复看：

- 微信开发者工具模拟器里重点复看段位星星、确认按钮、结算页、前台工作台和计分页实际观感。
- 本轮仍是源头视觉二轮修正，不等于所有页面逐页最终完成。

审查归档：

- `docs/reviews/phase-28-char-stars-no-green-visual-review.md`

## 2026-06-03 Phase 29 我的页个人资料编辑

本轮目的：把“我的”页里的个人信息从静态展示改成正式可编辑资料，同时明确用户只能改会员资料，不能改段位和积分。

边界判断：

- 可编辑：昵称、手机号、备注。
- 不可编辑：段位、积分、星级、排名。这些是比赛和结算系统资产，只能由系统计算。
- 当前云环境还没完成创建，保存先走 `member-service` 的本地缓存兜底，后续接云函数时只替换服务层。

测试先行：

- 新增 `scripts/test-member-profile.js`。
- 先跑测试，确认红灯：缺少 `miniprogram/utils/member-profile`。
- 再新增工具层和页面实现，让测试转绿。

代码变更：

- 新增 `miniprogram/utils/member-profile.js`：
  - `buildProfileDraft`
  - `normalizeMemberProfile`
  - `validateMemberProfile`
  - 只保留 `name / phone / note`，主动剔除 `points / rankTitle` 等不可编辑字段。
- 更新 `miniprogram/services/member-service.js`：
  - 新增 `getMemberProfile`。
  - 新增 `saveMemberProfile`。
  - 当前用 `wx.setStorageSync` 做本地缓存兜底，刷新后保留开发阶段编辑结果。
- 更新 `miniprogram/pages/my-hub/`：
  - 个人信息卡新增“编辑”按钮。
  - 编辑态支持昵称、手机号、备注输入。
  - 保存后更新头像文字、昵称和资料展示。
  - 段位和积分继续展示，但不进入编辑表单。
- 更新接口和后端计划文档：
  - `docs/api-service-layer-contract.md`
  - `docs/backend-integration-readiness-plan.md`

验证结果：

- `node scripts\test-member-profile.js` 通过。
- `node --check miniprogram\utils\member-profile.js` 通过。
- `node --check miniprogram\services\member-service.js` 通过。
- `node --check miniprogram\pages\my-hub\my-hub.js` 通过。
- `node scripts\test-admin-config-validator.js` 通过。
- `node scripts\test-settlement-engine.js` 通过。

补充验证结果：

- 全量 `miniprogram` JS `node --check` 通过，共 45 个 JS 文件。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- 页面层直接引用检查通过：`miniprogram/pages` 内无 `ladder-data` / `operation-log` 直接引用。
- `git diff --check` 通过，仅有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `730.8 KB` / `748332` bytes。

仍需后端补齐：

- 云环境可用后，需要把 `member.saveProfile` 接入云函数，并在云端重复校验不可编辑字段。

审查归档：

- `docs/reviews/phase-29-member-profile-edit-review.md`

## 2026-06-03 Phase 30 我的页资料卡编辑入口与头像编辑

本轮目的：修正个人信息卡编辑按钮过长、位置不合理的问题，并补齐头像图片编辑能力。

设计修正：

- 取消个人信息 panel 顶部的大号 `yh-button` 编辑入口。
- 编辑入口改成资料卡右侧的小切角按钮，避免在正式页面里形成一条突兀横条。
- 资料卡左侧支持真实头像图片；没有头像时继续显示昵称首字。
- 编辑态顶部新增头像图片更换区域，使用微信小程序 `chooseAvatar` 能力。

功能边界：

- 可编辑字段扩展为：昵称、手机号、备注、头像图片。
- 不可编辑字段不变：段位、积分、星级、排名。
- 当前云环境未可用，头像路径和资料仍先进入 `member-service` 本地缓存兜底。
- 云环境可用后，头像图片应先上传到云存储，再保存云文件地址。

代码变更：

- 更新 `miniprogram/utils/member-profile.js`：
  - `buildProfileDraft`、`normalizeMemberProfile`、`validateMemberProfile` 增加 `avatarUrl`。
  - 继续剔除 `points / rankTitle` 等比赛资产字段。
- 更新 `miniprogram/services/member-service.js`：
  - 会员资料本地缓存包含 `avatarUrl`。
- 更新 `miniprogram/pages/my-hub/`：
  - 右侧小编辑按钮。
  - 头像预览。
  - 头像更换入口。

验证结果：

- TDD 红灯：`node scripts\test-member-profile.js` 先失败，证明头像字段尚未纳入资料模型。
- TDD 绿灯：补实现后 `node scripts\test-member-profile.js` 通过。

审查归档：

- `docs/reviews/phase-30-profile-avatar-edit-review.md`

## 2026-06-03 Phase 31 正式路由与页面职责护栏

本轮目的：把后续上线级逐页打磨先落成任务计划，并新增自动检查脚本，避免 UI Kit、调试页、错误首页或比赛中底部 Tab 混进正式页面结构。

计划落地：

- 新增 `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`。
- 将上线打磨拆成 7 个 Stage：正式路由护栏、挑战首页、等待接受、玩法参数、计分结算、数据排行积分、我的/员工/老板/大屏。
- Stage 1 已在计划中标记完成，后续从 Stage 2 开始逐页执行。

代码变更：

- 新增 `scripts/check-player-flow-routes.js`：
  - 检查正式首页是否为 `pages/challenge-home/challenge-home`。
  - 检查 `pages/ui-kit/ui-kit` 是否误入正式 `app.json`。
  - 检查正式页面是否都具备 `.js / .json / .wxml / .wxss`。
  - 检查球友端主流程页面是否按顺序存在。
  - 检查非比赛中页面是否有底部 Tab，比赛中页面是否没有底部 Tab。
- 更新 `docs/launch-readiness-execution-plan.md`：
  - 标准验证命令新增 `node scripts/check-player-flow-routes.js`。

验证结果：

- `node scripts\check-player-flow-routes.js` 通过，输出 `Player flow route check OK`。
- `node --check scripts\check-player-flow-routes.js` 通过。
- `git diff --check -- docs\superpowers\plans\2026-06-03-launch-grade-page-polish.md scripts\check-player-flow-routes.js docs\launch-readiness-execution-plan.md` 通过，仅有既有 CRLF 提示，无阻断错误。

审查归档：

- `docs/reviews/phase-31-route-flow-guard-review.md`

## 2026-06-03 Phase 32 挑战首页上线级首轮打磨

本轮目的：把挑战首页从“功能入口集合”收束成正式上线首页，只承担当前球桌状态、当前会员段位和发起挑战入口，不再在内容区重复堆数据、排行榜、积分礼遇等快捷卡。

代码变更：

- 更新 `miniprogram/pages/challenge-home/challenge-home.wxml`：
  - 首页主模块改为排位状态板。
  - 展示当前会员、球桌、开台、到点和发起挑战按钮。
  - 删除内容区三个快捷卡，避免和底部 Tab 重复。
  - 新增轻量规则条：当前开放玩法、开台赠分、最低有效时间。
- 更新 `miniprogram/pages/challenge-home/challenge-home.wxss`：
  - 强化台球厅设备面板感：切角、轨道线、口袋弧线、暖黑木纹底。
  - 减少页面卡片堆叠感。
  - 保持按钮为唯一主动作。

验证结果：

- `Get-ChildItem miniprogram\pages\challenge-home -Filter *.js | ForEach-Object { node --check $_.FullName }` 通过。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `git diff --check -- miniprogram\pages\challenge-home\challenge-home.wxml miniprogram\pages\challenge-home\challenge-home.wxss` 通过，仅有既有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `736.6 KB` / `754230` bytes。

仍需人工复看：

- 首页视觉需要在模拟器里人工确认：首屏是否仍偏黑、状态板是否过重、底部规则条是否会挤压段位卡。

审查归档：

- `docs/reviews/phase-32-challenge-home-launch-polish-review.md`

## 2026-06-03 Phase 33 等待与接受挑战流程上线化

本轮目的：修正等待房间中的开发预览口和视觉口径问题，把等待/接受流程收束成正式房间状态页。

问题根因：

- 等待页保留了 `devtoolsPreview` 条件按钮“继续选玩法”，容易在微信开发者工具里变成用户看到的开发入口。
- 等待页对手加入状态使用绿色点，和当前“不要绿色”的视觉规范冲突。

代码变更：

- 更新 `miniprogram/pages/waiting-room/waiting-room.wxml`：
  - 移除开发预览专用按钮。
  - 对手加入后才展示正式按钮“选择玩法”。
  - 状态说明根据是否已加入动态变化。
- 更新 `miniprogram/pages/waiting-room/waiting-room.js`：
  - 移除 `dev-preview` 依赖。
  - `refreshRoom` 改为正式刷新房间状态：首次刷新进入“对手已加入”，再次刷新提示状态已更新。
  - 新增 `continueMatch`，只在对手已加入时进入玩法选择。
- 更新 `miniprogram/pages/waiting-room/waiting-room.wxss`：
  - 已加入状态点从绿色改为金色。

验证结果：

- `node --check miniprogram\pages\waiting-room\waiting-room.js` 通过。
- `node --check miniprogram\pages\accept-challenge\accept-challenge.js` 通过。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `git diff --check` 通过，仅有既有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `736.8 KB` / `754528` bytes。

审查归档：

- `docs/reviews/phase-33-waiting-accept-launch-polish-review.md`

## 2026-06-03 Phase 34 玩法、底分倍率、开局确认上线化

本轮目的：继续执行上线级逐页计划，把 `玩法选择 -> 底分倍率 -> 开局确认` 三页补齐为真实开局参数链，重点突出风险积分和随机奖励机制。

代码变更：

- 更新 `miniprogram/pages/points-select/points-select.wxml`：
  - 在“本场风险积分”模块中展示普通随机奖励和续时冲刺奖励。
- 更新 `miniprogram/pages/points-select/points-select.wxss`：
  - 风险积分公式改为固定网格，避免窄屏挤压。
  - 新增随机奖励预览卡片样式。
- 更新 `miniprogram/pages/match-confirm/match-confirm.wxml`：
  - 开局确认页补充发起方和挑战方信息。
- 更新 `miniprogram/pages/match-confirm/match-confirm.wxss`：
  - 补充三项参数指标的固定网格样式。

验证结果：

- `node --check miniprogram\pages\mode-select\mode-select.js` 通过。
- `node --check miniprogram\pages\points-select\points-select.js` 通过。
- `node --check miniprogram\pages\match-confirm\match-confirm.js` 通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- `git diff --check` 通过，仅有既有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `739.6 KB` / `757339` bytes。

审查归档：

- `docs/reviews/phase-34-mode-risk-confirm-launch-polish-review.md`

## 2026-06-03 Phase 35 计分、时间不足、结算链路上线化

本轮目的：修正比赛计分页的时间累计方式，确保最低有效时间判断更接近正式上线逻辑，并避免快速连点导致重复跳转。

问题根因：

- 旧计时逻辑靠页面 `setInterval` 每秒加 1。进入“时间不足”页后计分页 `onHide` 会停止计时，返回后无法把停留在提示页的时间算进去。
- 达到目标盘数后如果快速连点 `+`，可能重复触发时间不足或结算跳转。

代码变更：

- 更新 `miniprogram/pages/match-scoring/match-scoring.js`：
  - 新增 `matchStartedAt`，用比赛开始时间计算 `elapsedSeconds`。
  - 新增 `syncElapsedTime()`，页面显示时间从开始时间推导，不再只依赖累加器。
  - 新增 `settlementLocked`，达到目标盘数后锁定跳转，避免重复进入结算链路。
  - 从时间不足页返回后 `onShow` 自动解锁，允许继续计分。

验证结果：

- `node scripts\test-settlement-engine.js` 通过。
- `node --check miniprogram\pages\match-scoring\match-scoring.js` 通过。
- `node --check miniprogram\pages\time-insufficient\time-insufficient.js` 通过。
- `node --check miniprogram\pages\settlement\settlement.js` 通过。
- `node --check miniprogram\pages\refusal\refusal.js` 通过。
- `node --check miniprogram\pages\match-result\match-result.js` 通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- `git diff --check` 通过，仅有既有 CRLF 提示，无阻断错误。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `740.3 KB` / `758050` bytes。

审查归档：

- `docs/reviews/phase-35-scoring-settlement-launch-polish-review.md`

## 2026-06-03 Phase 36 数据、排行榜、积分礼遇上线化

本轮目的：检查个人数据、排行榜、积分礼遇是否符合上线级页面口径，并修正排行榜 Tab 文案。

代码变更：

- 更新 `miniprogram/services/player-service.js`：
  - 排行榜第三个 Tab 从“好友榜”改为“微信好友榜”，与需求口径一致。

验收结果：

- 我的数据页已包含：当前段位、当前积分、星级进度、本赛季胜率、有效挑战数、连胜、店内/同段位/好友排名摘要。
- 排行榜页已包含：店内总榜、同段位榜、微信好友榜。
- 积分礼遇页仅展示前台兑换、当前积分、兑换门槛、开台赠分和会员码入口，没有线上商城或抽奖。

验证结果：

- `node --check miniprogram\services\player-service.js` 通过。
- `node --check miniprogram\pages\my-data\my-data.js` 通过。
- `node --check miniprogram\pages\rankings\rankings.js` 通过。
- `node --check miniprogram\pages\points-perks\points-perks.js` 通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `740.3 KB` / `758056` bytes。

审查归档：

- `docs/reviews/phase-36-data-ranking-perks-launch-polish-review.md`

## 2026-06-03 Phase 37 我的、员工端、老板端、大屏上线化

本轮目的：把“我的 / 前台 / 老板 / 大屏”从可看页面推进到能支撑上线流程的运营入口，并在云环境未创建时保留本地预览兜底。

代码变更：

- 更新 `miniprogram/services/admin-service.js`：
  - 老板端配置保存后写入本地缓存。
  - 重新进入老板端时优先读取本地缓存，避免刷新后配置丢失。
- 更新 `miniprogram/services/staff-service.js`：
  - 前台球桌到点时间、异常比赛列表支持本地缓存。
  - DevTools 无云环境时，本地兜底允许保存到点、核销积分、作废异常，生产环境仍要求云函数成功。
- 更新 `miniprogram/pages/staff-desk/staff-desk.js`：
  - 积分核销后即时扣减当前会员显示分，并清空扣分输入。
  - 异常作废后从当前列表移除，减少员工误判。
- 更新 `miniprogram/services/member-service.js` 与 `miniprogram/pages/member-code/`：
  - 会员码优先使用云函数结果。
  - DevTools 无云环境时显示本地视觉码和码值，避免会员码页面失败。
- 更新 `miniprogram/services/screen-service.js` 与 `miniprogram/pages/tv-ranking/`：
  - 大屏主榜、副榜、刷新文案读取老板端配置。
  - 增加 `tv-stage` 横屏舞台层，电视宽屏使用三栏布局，手机模拟器仍可纵向查看。

验收结果：

- 我的页保留个人资料编辑、会员工具、员工 / 老板 / 大屏入口。
- 前台页只保留三类高频动作：到点时间、积分核销、异常处理。
- 老板页参数可编辑、可校验、可本地保存。
- 大屏页不再只依赖窄屏手机布局，配置项能进入榜单标题和刷新文案。

验证结果：

- `node --check miniprogram\services\admin-service.js` 通过。
- `node --check miniprogram\services\staff-service.js` 通过。
- `node --check miniprogram\services\member-service.js` 通过。
- `node --check miniprogram\services\screen-service.js` 通过。
- `node --check miniprogram\pages\staff-desk\staff-desk.js` 通过。
- `node --check miniprogram\pages\tv-ranking\tv-ranking.js` 通过。
- `node --check miniprogram\pages\member-code\member-code.js` 通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `747.4 KB` / `765348` bytes。

残余风险：

- 当前没有 Git remote，阶段提交只能本地完成，无法推送远端。
- 云环境尚未创建，本地兜底不能替代正式云函数；上线前必须补会员码、积分流水、球桌到点时间、异常比赛处理的真实落库。

审查归档：

- `docs/reviews/phase-37-ops-screen-launch-polish-review.md`

## 2026-06-03 Phase 38 运营服务层兜底测试与云接入清单

本轮目的：把阶段 37 新增的 DevTools 本地兜底写成可复跑测试，并补一份云环境创建后的切换清单，避免明天接云函数时漏接口。

代码变更：

- 新增 `scripts/test-ops-services.js`：
  - 模拟微信开发者工具环境、无 `wx.cloud`、有本地 storage。
  - 验证老板配置保存 / 读取。
  - 验证大屏读取老板端配置。
  - 验证前台球桌到点时间保存。
  - 验证会员扫码查询、积分核销、异常作废。
  - 验证会员码本地视觉码兜底。

文档变更：

- 新增 `docs/cloud-function-cutover-checklist.md`，记录云函数切换前置条件、必测接口、本地兜底替换点、上线前命令、人工走查顺序和不能上线红线。
- 更新 `docs/api-service-layer-contract.md`，同步运营服务层当前状态。
- 更新 `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`，新增 Stage 8，并把 `node scripts/test-ops-services.js` 加入标准验证。

验证结果：

- `node scripts\test-ops-services.js` 通过，输出 `Ops service fallback tests OK`。
- `node scripts\test-settlement-engine.js` 通过。
- `node scripts\test-admin-config-validator.js` 通过。
- `node scripts\test-member-profile.js` 通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `747.4 KB` / `765348` bytes。

审查归档：

- `docs/reviews/phase-38-ops-service-fallback-review.md`

## 2026-06-03 Phase 39 页面服务层依赖护栏

本轮目的：把“页面只能调用 service，不能直接读本地数据或写操作日志”的规则变成脚本，避免后续新增页面绕过接口层。

代码变更：

- 新增 `scripts/check-service-layer-boundary.js`：
  - 扫描 `miniprogram/pages/**/*.js`。
  - 禁止页面直接 `require` `ladder-data`。
  - 禁止页面直接 `require` `operation-log`。
  - 禁止页面直接 `require` `settlement-engine`。

文档变更：

- 更新 `docs/api-service-layer-contract.md`，把手动 `rg` 检查替换为脚本检查。
- 更新 `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`，新增 Stage 9，并加入标准验证。

验证结果：

- `node scripts\check-service-layer-boundary.js` 通过，输出 `Service layer boundary check OK`。
- `node scripts\test-ops-services.js` 通过。
- `node scripts\test-settlement-engine.js` 通过。
- `node scripts\test-admin-config-validator.js` 通过。
- `node scripts\test-member-profile.js` 通过。
- 全量 `miniprogram` JS `node --check` 通过。
- `node scripts\check-json-files.js` 通过，共 35 个 JSON 文件。
- `node scripts\check-production-copy.js` 通过，共 21 个正式页面文件。
- `node scripts\check-player-flow-routes.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets` 通过，共 32 个 PNG 资产。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `747.4 KB` / `765348` bytes。

审查归档：

- `docs/reviews/phase-39-service-boundary-review.md`

## 2026-06-03 Phase 40 统一上线验证脚本

本轮目的：把本地上线检查从多条散命令收口成一个统一入口，降低后续每次阶段提交前漏跑检查的概率。

代码变更：

- 新增 `scripts/verify-launch-ready.ps1`：
  - 默认运行运营服务层兜底测试、结算规则测试、老板配置校验测试、会员资料测试。
  - 运行服务层边界检查、JSON 检查、正式文案检查、球友流程路由检查、UI 资产边缘检查。
  - 运行全量 `miniprogram` JS 语法检查。
  - 传入 `-WithPreview` 后调用微信开发者工具 CLI 预览。
  - 使用字符码组装默认微信 CLI 路径，避免 PowerShell 5 中文路径解码错误。

验证结果：

- 第一轮 `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 因中文默认路径乱码失败。
- 修正后重跑通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `747.4 KB` / `765348` bytes。

审查归档：

- `docs/reviews/phase-40-launch-verification-script-review.md`

## 2026-06-03 Phase 41 云函数服务端校验与会员资料保存

本轮目的：把老板参数保存和球友个人资料保存从“前端本地可用”推进到“云函数可接入”，先把服务端校验、白名单写入和前后端校验一致性补齐。

代码变更：

- 新增 `cloudfunctions/yunhanApi/admin-config-validator.js`：
  - 云函数侧复用老板配置校验规则。
  - `admin.saveConfig` 写入 `admin_configs` 前先调用服务端校验。
- 新增 `cloudfunctions/yunhanApi/member-profile.js`：
  - 云函数侧复用会员资料校验规则。
  - 只允许保存昵称、手机号、备注、头像。
- 更新 `cloudfunctions/yunhanApi/index.js`：
  - 新增 `member.saveProfile`。
  - 已有 `store_members` 只更新资料字段，不改 `role` / `status`。
  - 新会员资料保存只创建 `store_members` 球友身份。
  - 已有 `member_points` 只同步资料字段，不创建缺少余额的积分账户。
- 更新 `miniprogram/services/member-service.js`：
  - 保存个人资料时优先调用云函数。
  - 只有微信开发者工具预览环境允许本地 storage 兜底。
- 新增 `scripts/test-cloud-contracts.js`：
  - 校验小程序侧和云函数侧老板配置规则一致。
  - 校验小程序侧和云函数侧会员资料规则一致。
- 更新 `scripts/verify-launch-ready.ps1`：
  - 加入云函数契约测试。
  - 加入云函数 JS 语法检查。

文档变更：

- 更新 `docs/api-service-layer-contract.md`，记录云函数校验、会员资料云端保存和 DevTools 兜底边界。
- 更新 `docs/cloud-database-schema.md`，补充 `store_members` / `member_points` 的会员资料字段。
- 更新 `docs/cloud-function-cutover-checklist.md`，加入云函数契约测试。
- 更新 `cloudfunctions/README.md`，同步 `member.saveProfile` 和 `admin.saveConfig` 当前职责。
- 更新执行计划，新增 Stage 11。

验证结果：

- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- `node scripts\test-cloud-contracts.js` 已纳入统一脚本，输出 `Cloud contract tests OK`。
- 云函数 JS 语法检查通过。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `748.8 KB` / `766759` bytes。

残余风险：

- 云环境尚未创建，真实云数据库权限、集合索引、云函数部署和线上调用还没有实测。
- 云函数侧校验文件与小程序侧校验文件目前是复制保持一致，后续若改规则，必须同步跑 `node scripts/test-cloud-contracts.js`。

审查归档：

- `docs/reviews/phase-41-cloud-validation-profile-review.md`

## 2026-06-03 Phase 42 云函数比赛结算链路准备

本轮目的：在云环境还没创建前，先把核心结算能力放进云函数包，避免上线前仍由前端单独决定积分和段位。

代码变更：

- 新增 `cloudfunctions/yunhanApi/settlement-engine.js`：
  - 从小程序侧结算规则引擎机械复制到云函数包内。
  - 云函数部署包不依赖 `miniprogram` 目录。
- 新增 `cloudfunctions/yunhanApi/match-settlement.js`：
  - 生成结算写库计划。
  - 校验 `matchId`、双方 OpenID、同一用户不能同时作为双方。
  - 拆出胜方 `match_win`、败方 `match_loss` 两条积分流水。
  - 生成胜负双方段位变化。
- 更新 `cloudfunctions/yunhanApi/index.js`：
  - `match.settle` 不再返回 `SETTLEMENT_NOT_READY`。
  - 读取真实 `matches` 文档，不存在则拒绝。
  - 已结算或已有 `settlements` 记录时拒绝重复结算。
  - 双方 `member_points` 账户必须存在。
  - 败方扣分后不能出现负余额。
  - 先写 `settlements.status = settling` 作为结算锁，再写积分和流水，最后改为 `settled`。
  - 更新 `matches.status = settled`。
- 更新 `scripts/test-cloud-contracts.js`：
  - 增加小程序 / 云函数结算公式一致性检查。
  - 增加结算写库计划检查。
  - 增加缺少对手身份的拒绝检查。

文档变更：

- 更新 `cloudfunctions/README.md`，说明 `match.settle` 当前职责。
- 更新 `docs/api-service-layer-contract.md`，说明云函数结算已准备，但前端尚未切换。
- 更新 `docs/cloud-function-cutover-checklist.md`，补充 `match.settle` 真云验证要点。
- 更新执行计划，新增 Stage 12。

验证结果：

- `node scripts\test-cloud-contracts.js` 通过，输出 `Cloud contract tests OK`。
- `node --check cloudfunctions\yunhanApi\index.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。
- 微信开发者工具 CLI preview 通过，当前端口 `30812`，AppID `wxe30b469d64636a2b`，包体 `748.8 KB` / `766759` bytes。

残余风险：

- `match.settle` 仍未在真实云环境验证。
- 当前不是事务级写入。虽然已有 `settling` 结算锁，但云函数并发、网络中断、数据库写入中途失败仍要真云压测。
- 前端结算页仍使用同步本地展示链路；切换到云函数需要单独改 `match-service` 和相关页面生命周期。

审查归档：

- `docs/reviews/phase-42-cloud-match-settle-review.md`

## 2026-06-03 Phase 43 结算确认按钮接入云函数入口

本轮目的：在不一次性重构结算三页的前提下，先让“服了，确认结算”动作进入服务端结算入口，减少正式上线时前端单独决定结算结果的风险。

代码变更：

- 更新 `miniprogram/services/match-service.js`：
  - 新增 `settleCurrentMatch(params)`。
  - 优先调用 `callCloud("match", "settle", payload)`。
  - DevTools 预览环境云不可用时，兜底返回本地 `calculateSettlement`。
  - 非 DevTools 环境云结算失败时抛出错误，不静默本地结算。
- 更新 `miniprogram/pages/match-scoring/match-scoring.js`：
  - 跳转结算页时透传 `matchId`，正式数据可用后用于云端结算定位比赛。
- 更新 `miniprogram/pages/settlement/settlement.js`：
  - 确认按钮改为异步调用 `settleCurrentMatch`。
  - 云函数返回 `{ matchId, settlement }` 时保留 `matchId` 并再跳结果页。
  - 失败时 `wx.showToast` 提示，不进入结果页。
- 更新 `miniprogram/pages/settlement/settlement.wxml`：
  - “服了，确认结算”按钮增加 loading / disabled，避免重复点击。

文档变更：

- 更新 `docs/api-service-layer-contract.md`，说明确认动作已接云函数入口，但预览和结果页仍待继续迁移。
- 更新执行计划，新增 Stage 13。

验证结果：

- `node --check miniprogram\services\match-service.js` 通过。
- `node --check miniprogram\pages\settlement\settlement.js` 通过。
- `node --check miniprogram\pages\match-scoring\match-scoring.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。

残余风险：

- 结算预览仍是本地公式展示，结果页仍通过 query 复算展示。
- 本地占位比赛数据不是正式云端 `matches` 文档；真实云环境创建后必须用真实 matchId 和双方 OpenID 复测。

审查归档：

- `docs/reviews/phase-43-settlement-confirm-cloud-entry-review.md`

## 2026-06-03 Phase 44 结算结果页读取服务端结算单

本轮目的：让结果页不再只能依赖 URL 参数复算展示，而是优先读取服务端已写入的结算单。

代码变更：

- 更新 `cloudfunctions/yunhanApi/index.js`：
  - 新增 `getSettlement(payload, storeId)`。
  - 新增 `match.getSettlement` action。
  - 必须传 `matchId`。
  - 查不到 `settlements` 时返回 `SETTLEMENT_NOT_FOUND`。
- 更新 `miniprogram/services/match-service.js`：
  - 新增 `getSettlementResult(params)`。
  - 有 `matchId` 时优先调用 `callCloud("match", "getSettlement", { matchId })`。
  - 把云端结算单核心字段合并为结果页现有展示结构。
  - DevTools 预览环境云失败时使用本地结算展示兜底。
- 更新 `miniprogram/pages/match-result/match-result.js`：
  - 先展示本地预览结果，避免白屏。
  - 再异步读取服务端结算单并替换展示。
  - 读取失败时提示，不强行进入“已同步”状态。

文档变更：

- 更新 `cloudfunctions/README.md`，补充 `match.getSettlement`。
- 更新 `docs/api-service-layer-contract.md`，说明结果页已接云端读取，结算预览页仍待迁移。
- 更新 `docs/cloud-function-cutover-checklist.md`，加入 `match.getSettlement` 必测项。
- 更新执行计划，新增 Stage 14。

验证结果：

- `node --check cloudfunctions\yunhanApi\index.js` 通过。
- `node --check miniprogram\services\match-service.js` 通过。
- `node --check miniprogram\pages\match-result\match-result.js` 通过。
- `powershell -ExecutionPolicy Bypass -File scripts\verify-launch-ready.ps1 -WithPreview -Port 30812` 通过，输出 `Launch verification OK`。

残余风险：

- 未在真实云环境验证 `settlements` 读取、集合权限和真实字段。
- 结算确认页仍是本地预览，后续要继续切服务端结算单。

审查归档：

- `docs/reviews/phase-44-match-result-cloud-read-review.md`

