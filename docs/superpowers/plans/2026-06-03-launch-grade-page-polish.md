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
