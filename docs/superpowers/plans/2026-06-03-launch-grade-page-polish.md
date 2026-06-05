# 云瀚台球上线级逐页打磨执行计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把当前小程序从可演示页面推进到可上线页面，先保证正式路由、页面职责、用户可见文案和主流程参数链稳定，再逐页打磨视觉与动画。

**Architecture:** 以 `miniprogram/app.json` 为正式页面入口清单，球友端按 `challenge-home -> waiting-room -> accept-challenge -> mode-select -> points-select -> match-confirm -> match-scoring -> time-insufficient/settlement -> refusal/match-result` 串联。页面数据暂时使用本地服务和占位数据，但所有用户可见内容必须按真实线上状态呈现，不显示 PM、mock、演示或内部校验说明。

**Tech Stack:** 微信小程序 WXML / WXSS / JS，Node.js 验证脚本，微信开发者工具 CLI。

---

## Execution Rules

- 一次只推进一个阶段，完成后写 `docs/dev-log.md` 和 `docs/reviews/phase-XX-*.md`。
- 每个阶段收尾必须跑验证脚本和微信开发者工具预览。
- 不回滚现有未提交改动，除非用户明确要求。
- 新增内部验证只放在 `scripts/` 和文档，不进入用户可见页面。
- UI Kit 只作为组件验收台，不进入正式 `app.json` 页面列表。

## Stage 1: 正式路由与页面职责护栏

**Files:**
- Create: `scripts/check-player-flow-routes.js`
- Modify: `docs/launch-readiness-execution-plan.md`
- Modify: `docs/dev-log.md`
- Create: `docs/reviews/phase-31-route-flow-guard-review.md`

- [x] **Step 1: Add route guard script**

Create a Node.js script that verifies:

- `miniprogram/app.json` first page is `pages/challenge-home/challenge-home`.
- `pages/ui-kit/ui-kit` is not listed in formal pages.
- every formal page listed in `app.json` has `.js`, `.json`, `.wxml`, `.wxss`.
- required player-flow pages are present in the expected order.
- pages that should show bottom tab include `<bottom-nav`.
- match-in-progress pages do not include `<bottom-nav`.

- [x] **Step 2: Run route guard**

Run:

```powershell
node scripts/check-player-flow-routes.js
```

Expected:

```text
Player flow route check OK
```

- [x] **Step 3: Add route guard to launch plan**

Add `node scripts/check-player-flow-routes.js` to the standard verification command list in `docs/launch-readiness-execution-plan.md`.

- [x] **Step 4: Review and archive Stage 1**

Write a review file under `docs/reviews/` with findings, scope check, requirement check, verification evidence, and decision.

## Stage 2: 球友端首页上线化

**Files:**
- Modify: `miniprogram/pages/challenge-home/challenge-home.wxml`
- Modify: `miniprogram/pages/challenge-home/challenge-home.wxss`
- Modify: `miniprogram/pages/challenge-home/challenge-home.js`
- Modify: `docs/design/player-flow-page-spec.md`
- Create: `docs/reviews/phase-32-challenge-home-launch-polish-review.md`

- [x] **Step 1: Confirm homepage only has one primary job**

Homepage must show:

- club name, table number, due time
- current rank and points
- ranked challenge availability
- primary action: start challenge
- secondary navigation via bottom tab or compact shortcuts only

Homepage must not show:

- base point selection
- multiplier selection
- scoring controls
- settlement details
- PM / mock / demo copy

- [x] **Step 2: Polish homepage layout**

Reduce black-heavy density and strengthen billiards-hall material language:

- table-rail hero
- rank board
- compact availability panel
- sparse orange/gold accents
- no card pile-up

- [x] **Step 3: Verify navigation**

Use DevTools preview and manually test:

- Start challenge enters waiting room when gate passes.
- Disabled state shows user-facing toast when gate fails.
- Bottom tabs navigate to data, rankings, points, mine.

## Stage 3: 等待与接受挑战上线化

**Files:**
- Modify: `miniprogram/pages/waiting-room/`
- Modify: `miniprogram/pages/accept-challenge/`
- Create: `docs/reviews/phase-33-waiting-accept-launch-polish-review.md`

- [x] Waiting page must only show room state, table, host, waiting state, cancel/refresh.
- [x] Accept page must only show invite state, host, player, accept/reject.
- [x] No demo opponent button or mock wording.

## Stage 4: 玩法、底分倍率、开局确认上线化

**Files:**
- Modify: `miniprogram/pages/mode-select/`
- Modify: `miniprogram/pages/points-select/`
- Modify: `miniprogram/pages/match-confirm/`
- Create: `docs/reviews/phase-34-mode-risk-confirm-launch-polish-review.md`

- [x] Mode selection passes `modeId`.
- [x] Points selection passes `base`, `multiplier`, `risk`.
- [x] Confirm page prominently shows normal random reward and rush reward.
- [x] Component sizes must fit current page width.

## Stage 5: 计分、时间不足、结算链路上线化

**Files:**
- Modify: `miniprogram/pages/match-scoring/`
- Modify: `miniprogram/pages/time-insufficient/`
- Modify: `miniprogram/pages/settlement/`
- Modify: `miniprogram/pages/refusal/`
- Modify: `miniprogram/pages/match-result/`
- Create: `docs/reviews/phase-35-scoring-settlement-launch-polish-review.md`

- [x] Positive timer from `00:00:01`.
- [x] No settlement before minimum effective time.
- [x] Settlement uses `risk + random reward` and shared rank.
- [x] Refusal has only exit-no-settlement or rematch.
- [x] Add point/star feedback animation states.

## Stage 6: 数据、排行榜、积分礼遇上线化

**Files:**
- Modify: `miniprogram/pages/my-data/`
- Modify: `miniprogram/pages/rankings/`
- Modify: `miniprogram/pages/points-perks/`
- Create: `docs/reviews/phase-36-data-ranking-perks-launch-polish-review.md`

- [x] Ranking page includes store total, same-rank ranking, WeChat friend ranking.
- [x] Rank leaderboard is visible and clear.
- [x] Points perks page only shows front-desk redemption, no online mall.

## Stage 7: 我的、员工端、老板端、大屏上线化

**Files:**
- Modify: `miniprogram/pages/my-hub/`
- Modify: `miniprogram/pages/staff-desk/`
- Modify: `miniprogram/pages/boss-config/`
- Modify: `miniprogram/pages/tv-ranking/`
- Create: `docs/reviews/phase-37-ops-screen-launch-polish-review.md`

- [x] My page contains editable profile and role entries.
- [x] Staff page keeps only high-frequency actions.
- [x] Boss page allows numeric parameters to be adjusted locally.
- [x] TV screen is 16:9 and not based on cramped mobile layout.

## Stage 8: 运营服务层兜底测试与云接入清单

**Files:**
- Create: `scripts/test-ops-services.js`
- Create: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/api-service-layer-contract.md`
- Create: `docs/reviews/phase-38-ops-service-fallback-review.md`

- [x] Add a repeatable Node test for DevTools local fallback.
- [x] Cover owner config, staff due time, member exchange lookup, points deduction, abnormal voiding, member code fallback, and screen config propagation.
- [x] Document cloud function cutover checklist for tomorrow's cloud environment work.
- [x] Add the new test to standard verification.

## Stage 9: 页面服务层依赖护栏

**Files:**
- Create: `scripts/check-service-layer-boundary.js`
- Modify: `docs/api-service-layer-contract.md`
- Create: `docs/reviews/phase-39-service-boundary-review.md`

- [x] Add a script that fails when formal pages directly import `ladder-data`, `operation-log`, or `settlement-engine`.
- [x] Run the script and confirm current pages only go through service modules.
- [x] Add the script to standard verification.

## Stage 10: 统一上线验证脚本

**Files:**
- Create: `scripts/verify-launch-ready.ps1`
- Create: `docs/reviews/phase-40-launch-verification-script-review.md`

- [x] Add a single PowerShell entrypoint for local launch verification.
- [x] Include service fallback tests, rule tests, JSON, production copy, route, asset, and full JS syntax checks.
- [x] Support optional WeChat DevTools preview with `-WithPreview`.
- [x] Avoid literal Chinese default path encoding issues in PowerShell 5.

## Stage 11: 云函数服务端校验与会员资料保存

**Files:**
- Create: `cloudfunctions/yunhanApi/admin-config-validator.js`
- Create: `cloudfunctions/yunhanApi/member-profile.js`
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `miniprogram/services/member-service.js`
- Create: `scripts/test-cloud-contracts.js`
- Create: `docs/reviews/phase-41-cloud-validation-profile-review.md`

- [x] Cloud `admin.saveConfig` validates config server-side before writing `admin_configs`.
- [x] Cloud `member.saveProfile` saves only editable member profile fields.
- [x] Saving profile must not overwrite existing owner/staff role.
- [x] Saving profile must not create a `member_points` document without balance.
- [x] Frontend member service calls cloud first and falls back locally only in DevTools.
- [x] Add parity tests for mini-program and cloud validation rules.

## Stage 12: 云函数比赛结算链路准备

**Files:**
- Create: `cloudfunctions/yunhanApi/settlement-engine.js`
- Create: `cloudfunctions/yunhanApi/match-settlement.js`
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `scripts/test-cloud-contracts.js`
- Create: `docs/reviews/phase-42-cloud-match-settle-review.md`

- [x] Copy settlement rule engine into the cloud function package.
- [x] Add a pure write-plan builder for cloud settlement.
- [x] `match.settle` rejects missing match, duplicate settlement, missing player accounts, and insufficient point balance.
- [x] `match.settle` writes `settlements`, `points_ledger`, `member_points`, and `matches.status`.
- [x] Keep frontend `match-service.calculateSettlement` unchanged until a separate async page-flow migration stage.
- [x] Add cloud contract tests for settlement parity and write-plan shape.

## Stage 13: 结算确认按钮接入服务端结算入口

**Files:**
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/match-scoring/match-scoring.js`
- Modify: `miniprogram/pages/settlement/settlement.js`
- Modify: `miniprogram/pages/settlement/settlement.wxml`
- Create: `docs/reviews/phase-43-settlement-confirm-cloud-entry-review.md`

- [x] Add `match-service.settleCurrentMatch()` as the cloud-first settlement service.
- [x] Keep `calculateSettlement()` for current settlement preview rendering.
- [x] In DevTools preview, cloud failure falls back to local settlement.
- [x] In non-DevTools production, cloud settlement failure is surfaced to the user.
- [x] Settlement confirm button shows loading and blocks repeat taps.
- [x] Pass `matchId` through the scoring-to-settlement query when available.

## Stage 14: 结算结果页读取服务端结算单

**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/match-result/match-result.js`
- Create: `docs/reviews/phase-44-match-result-cloud-read-review.md`

- [x] Add cloud action `match.getSettlement`.
- [x] `match.getSettlement` requires `matchId` and returns `SETTLEMENT_NOT_FOUND` when absent.
- [x] Add `match-service.getSettlementResult()` as cloud-first read service.
- [x] Match result page keeps local preview first, then replaces with cloud settlement when available.
- [x] DevTools preview may fallback locally; production cloud read failure is surfaced.
- [x] Document that settlement preview page still needs a later server-read migration.

## Stage 15: 生产态结算结果页禁止本地伪成功
**Files:**
- Modify: `miniprogram/pages/match-result/match-result.js`
- Modify: `miniprogram/pages/match-result/match-result.wxml`
- Modify: `miniprogram/pages/match-result/match-result.wxss`
- Modify: `docs/api-service-layer-contract.md`
- Create: `docs/reviews/phase-45-match-result-production-state-review.md`

- [x] In production, match result page must not render local settlement success before cloud settlement is read.
- [x] Missing `matchId` shows a fixed error page, not a fake success result.
- [x] `SETTLEMENT_NOT_FOUND` shows a fixed error page with retry and home actions.
- [x] DevTools preview may still render local settlement for no-cloud demo.
- [x] Add loading state while reading server settlement.

## Stage 16: 结算确认页接入云端预览入口
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/yunhanApi/match-settlement.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/settlement/settlement.js`
- Modify: `miniprogram/pages/settlement/settlement.wxml`
- Modify: `miniprogram/pages/settlement/settlement.wxss`
- Modify: `scripts/test-cloud-contracts.js`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Create: `docs/reviews/phase-46-settlement-preview-cloud-entry-review.md`

- [x] Add cloud action `match.previewSettlement`.
- [x] Preview action computes settlement and account balance preview without writing settlement, ledger, points, or match status.
- [x] Add `match-service.previewSettlement()` as cloud-first preview service.
- [x] Settlement confirmation page only enables confirm/refuse after preview is ready.
- [x] Production preview failure shows a fixed error state with retry and home actions.
- [x] DevTools preview may fallback locally while cloud environment is unavailable.
- [x] Add contract test to ensure preview and write plan use the same settlement output.

## Stage 17: 远端同步链路恢复
**Files:**
- Modify: `docs/dev-log.md`
- Modify: `docs/superpowers/plans/2026-06-03-launch-grade-page-polish.md`

- [x] Confirm active project repository is `F:\Making money\taiqiuxcx`.
- [x] Confirm previous push failures were caused by missing `remote.origin`.
- [x] Reuse sibling project remote `https://github.com/Lyric730/Lyric-Self-Improve.git`.
- [x] Push `codex/launch-page-polish` without touching `main`.
- [x] Set upstream to `origin/codex/launch-page-polish`.

## Stage 18: 发起挑战房间接服务端入口
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/challenge-home/challenge-home.js`
- Modify: `miniprogram/pages/challenge-home/challenge-home.wxml`
- Modify: `miniprogram/pages/waiting-room/waiting-room.js`
- Modify: `miniprogram/pages/waiting-room/waiting-room.wxml`
- Modify: `miniprogram/pages/waiting-room/waiting-room.wxss`
- Modify: `miniprogram/pages/mode-select/mode-select.js`
- Modify: `miniprogram/pages/points-select/points-select.js`
- Modify: `miniprogram/pages/match-confirm/match-confirm.js`
- Modify: `miniprogram/pages/match-scoring/match-scoring.js`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/cloud-database-schema.md`
- Modify: `docs/cloud-init-runbook.md`
- Create: `docs/reviews/phase-48-create-room-cloud-entry-review.md`

- [x] Add cloud action `match.createRoom`.
- [x] Enhance cloud action `match.get` to read a room by `matchId`.
- [x] Add `match-service.createChallengeRoom()` and `getWaitingRoomState()`.
- [x] Challenge home creates a room before navigating to waiting room.
- [x] Waiting room reads room state through service layer.
- [x] Propagate `matchId` through mode, points, confirm, scoring, and settlement query.
- [x] Keep DevTools local fallback while cloud environment is unavailable.
- [x] Document that opponent join is still a separate required stage.

## Stage 19: 接受挑战加入房间接服务端入口
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/accept-challenge/accept-challenge.js`
- Modify: `miniprogram/pages/accept-challenge/accept-challenge.wxml`
- Modify: `miniprogram/pages/accept-challenge/accept-challenge.wxss`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/cloud-database-schema.md`
- Create: `docs/reviews/phase-49-join-room-cloud-entry-review.md`

- [x] Add cloud action `match.joinRoom`.
- [x] Join action writes `guestOpenid` and changes room status to `joined`.
- [x] Join action rejects host self-join, occupied rooms, missing rooms, and closed rooms.
- [x] Add `match-service.joinChallengeRoom()`.
- [x] Accept challenge page reads room state by `matchId`.
- [x] Accept challenge page joins through service layer before navigating to mode selection.
- [x] Keep DevTools local fallback while cloud environment is unavailable.
- [x] Document that room scoring state machine is still a separate required stage.

## Stage 20: 开局参数写回比赛房间
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/match-confirm/match-confirm.js`
- Modify: `miniprogram/pages/match-confirm/match-confirm.wxml`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/cloud-database-schema.md`
- Create: `docs/reviews/phase-50-configure-match-cloud-entry-review.md`

- [x] Add cloud action `match.configure`.
- [x] Configure action validates mode enabled state.
- [x] Configure action validates base points and multiplier against mode options.
- [x] Configure action requires both host and guest to be present.
- [x] Configure action writes `modeId`, `base`, `multiplier`, `riskPoints`, `targetWins`, and `minimumMinutes` into `matches`.
- [x] Add `match-service.configureMatchSetup()`.
- [x] Match confirm page saves setup before navigating to scoring.
- [x] Keep DevTools local fallback while cloud environment is unavailable.
- [x] Document that scoring events and service-side timer are still separate required stages.

## Stage 21: 开赛状态与计分事件接服务端入口
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/match-scoring/match-scoring.js`
- Modify: `miniprogram/pages/match-scoring/match-scoring.wxml`
- Modify: `miniprogram/pages/match-scoring/match-scoring.wxss`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/cloud-database-schema.md`
- Create: `docs/reviews/phase-51-match-start-score-cloud-entry-review.md`

- [x] Add cloud action `match.start`.
- [x] `match.start` requires configured room, both players, and confirmed setup.
- [x] `match.start` writes `status = playing`, `startedAt`, `startedAtMs`, `scoreA`, and `scoreB`.
- [x] Add cloud action `match.recordScore`.
- [x] `match.recordScore` only allows host or guest to change the score.
- [x] `match.recordScore` clamps score between `0` and `targetWins`.
- [x] `match.recordScore` writes `match_score_events`.
- [x] Reaching target wins changes room status to `settlement_pending`.
- [x] Add `match-service.startConfiguredMatch()` and `recordMatchScore()`.
- [x] Match scoring page starts the match through service layer before enabling score buttons.
- [x] Match scoring page changes score through service layer instead of local-only state.
- [x] Match scoring page derives elapsed display from service-side start time.
- [x] Keep DevTools local fallback while cloud environment is unavailable.
- [x] Document that final settlement still needs real cloud environment verification.

## Stage 22: 球友赛后展示数据服务化
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/player-service.js`
- Modify: `miniprogram/pages/my-data/my-data.js`
- Modify: `miniprogram/pages/my-data/my-data.wxml`
- Modify: `miniprogram/pages/rankings/rankings.js`
- Modify: `miniprogram/pages/rankings/rankings.wxml`
- Modify: `miniprogram/pages/points-perks/points-perks.js`
- Modify: `miniprogram/pages/points-perks/points-perks.wxml`
- Modify: `miniprogram/pages/my-hub/my-hub.js`
- Modify: `miniprogram/styles/player-flow.wxss`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/cloud-database-schema.md`
- Modify: `docs/cloud-init-runbook.md`
- Create: `docs/reviews/phase-52-player-data-cloud-entry-review.md`

- [x] Add cloud module `player`.
- [x] Add `player.getProfile` for current member points, rank title, and season stats shell.
- [x] Add `player.getRankings` for store ranking, same-rank ranking, and empty friends ranking when friend relation is unavailable.
- [x] Add `player.getPointsPerks` for current points, table-open bonus, and exchange threshold.
- [x] Add `member_points` balance index requirement for leaderboard sorting.
- [x] Make `player-service` cloud-first with DevTools local fallback.
- [x] Make `my-data` load asynchronously with loading and retryable error states.
- [x] Make `rankings` load asynchronously with loading, retryable error, and empty ranking states.
- [x] Make `points-perks` load asynchronously with loading and retryable error states.
- [x] Remove unused synchronous `getPlayerProfile()` dependency from `my-hub`.
- [x] Keep formal UI copy only; no mock/demo/internal wording in pages.

## Stage 23: 小程序大屏榜单数据服务化
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/screen-service.js`
- Modify: `miniprogram/pages/tv-ranking/tv-ranking.js`
- Modify: `miniprogram/pages/tv-ranking/tv-ranking.wxml`
- Modify: `miniprogram/pages/tv-ranking/tv-ranking.wxss`
- Modify: `scripts/test-ops-services.js`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/cloud-database-schema.md`
- Modify: `docs/cloud-init-runbook.md`
- Create: `docs/reviews/phase-53-screen-board-cloud-entry-review.md`

- [x] Add cloud action `screen.getBoard`.
- [x] `screen.getBoard` returns store ranking from `member_points`.
- [x] `screen.getBoard` returns bounty hunter rows by aggregating settled match win point changes.
- [x] `screen.getBoard` reads owner screen config from `admin_configs`.
- [x] Allow small-program screen page access by `staff` / `owner` / `screen` role.
- [x] Keep `screenToken` validation path for future browser TV page.
- [x] Make `screen-service` cloud-first with DevTools local fallback.
- [x] Make `tv-ranking` load asynchronously with loading, retryable error, and empty board states.
- [x] Document `screen_tokens` token index.
- [x] Keep formal UI copy only; no mock/demo/internal wording in pages.

## Stage 24: 挑战首页开局检查服务化
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/player-service.js`
- Modify: `miniprogram/pages/challenge-home/challenge-home.js`
- Modify: `miniprogram/pages/challenge-home/challenge-home.wxml`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Modify: `docs/cloud-database-schema.md`
- Modify: `docs/cloud-init-runbook.md`
- Create: `docs/reviews/phase-54-challenge-home-cloud-entry-review.md`

- [x] Add cloud action `player.getChallengeHome`.
- [x] `player.getChallengeHome` returns current member identity, points, and rank.
- [x] `player.getChallengeHome` reads active `table_sessions` as the simple open-table gate.
- [x] If no active table due time exists, challenge home shows a formal unavailable state.
- [x] Make `player-service.getChallengeHome()` cloud-first with DevTools local fallback.
- [x] Make `challenge-home` load asynchronously with loading and retryable error states.
- [x] Document `table_sessions` active status index.
- [x] Keep formal UI copy only; no mock/demo/internal wording in pages.

## Stage 25: 玩法与底分倍率配置服务化
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Modify: `miniprogram/services/match-service.js`
- Modify: `miniprogram/pages/mode-select/mode-select.js`
- Modify: `miniprogram/pages/mode-select/mode-select.wxml`
- Modify: `miniprogram/pages/points-select/points-select.js`
- Modify: `miniprogram/pages/points-select/points-select.wxml`
- Modify: `docs/api-service-layer-contract.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Create: `docs/reviews/phase-55-mode-points-cloud-config-review.md`

- [x] Add cloud action `match.getModes`.
- [x] `match.getModes` reads `admin_configs.config.modes` and falls back to default modes only on server-side config absence.
- [x] Add cloud action `match.getSetup`.
- [x] `match.getSetup` returns selected mode, base, multiplier, risk points, and reward ranges.
- [x] Make `match-service.getAvailableModes()` cloud-first with DevTools local fallback.
- [x] Make `match-service.getConfigurableMatchSetup()` cloud-first with DevTools local fallback.
- [x] DevTools fallback reads locally saved boss config before default modes.
- [x] Make `mode-select` load asynchronously with loading, retryable error, and empty states.
- [x] Make `points-select` load asynchronously with loading and retryable error states.
- [x] Keep formal UI copy only; no mock/demo/internal wording in pages.

## Stage 26: 真实云环境绑定与云函数部署
**Files:**
- Modify: `miniprogram/app.js`
- Modify: `docs/cloud-init-runbook.md`
- Modify: `docs/wechat-devtools-cli.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Create: `docs/reviews/phase-56-cloud-env-deploy-review.md`

- [x] Confirm cloud environment `cloudbase-d9gg155lc1ee1d72e` is visible from WeChat DevTools CLI.
- [x] Deploy `cloudfunctions/yunhanApi` to `cloudbase-d9gg155lc1ee1d72e`.
- [x] Confirm `yunhanApi` status is `Active`.
- [x] Bind mini-program `wx.cloud.init()` to `cloudbase-d9gg155lc1ee1d72e`.
- [x] Document deployment command and function status.
- [x] Keep database collection/index/owner initialization as explicit next-step verification because it was not proven by deployment alone.

## Stage 27: 首个老板账号初始化入口
**Files:**
- Modify: `cloudfunctions/yunhanApi/index.js`
- Modify: `cloudfunctions/README.md`
- Create: `miniprogram/services/auth-service.js`
- Create: `miniprogram/pages/setup-owner/`
- Modify: `miniprogram/app.json`
- Modify: `miniprogram/pages/my-hub/`
- Modify: `docs/cloud-init-runbook.md`
- Modify: `docs/cloud-function-cutover-checklist.md`
- Create: `docs/reviews/phase-57-owner-bootstrap-entry-review.md`

- [x] `auth.whoami` returns current OpenID, role, store ID, and `ownerReady`.
- [x] `auth.bootstrapOwner` returns a clear error when `store_members` collection is missing.
- [x] Add `auth-service` for `whoami` and `bootstrapOwner`.
- [x] Add a formal setup page for first owner initialization with secret input.
- [x] Show the setup entry from My page only when `ownerReady === false`.
- [x] Keep the setup entry out of player challenge, ranking, and points flows.
- [x] Document that WeChat DevTools CLI can deploy functions but cannot create database collections or call functions directly.

## Standard Verification

Run after each stage:

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
node scripts/test-ops-services.js
node scripts/test-cloud-contracts.js
node scripts/check-service-layer-boundary.js
node scripts/check-json-files.js
node scripts/check-production-copy.js
node scripts/check-player-flow-routes.js
powershell -ExecutionPolicy Bypass -File scripts/check-ui-kit-asset-edges.ps1 -RequireAssets
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```

Or run the unified wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/verify-launch-ready.ps1 -WithPreview -Port 30812
```
