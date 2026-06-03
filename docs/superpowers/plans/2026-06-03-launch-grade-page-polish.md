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

- [ ] Positive timer from `00:00:01`.
- [ ] No settlement before minimum effective time.
- [ ] Settlement uses `risk + random reward` and shared rank.
- [ ] Refusal has only exit-no-settlement or rematch.
- [ ] Add point/star feedback animation states.

## Stage 6: 数据、排行榜、积分礼遇上线化

**Files:**
- Modify: `miniprogram/pages/my-data/`
- Modify: `miniprogram/pages/rankings/`
- Modify: `miniprogram/pages/points-perks/`
- Create: `docs/reviews/phase-36-data-ranking-perks-launch-polish-review.md`

- [ ] Ranking page includes store total, same-rank ranking, WeChat friend ranking.
- [ ] Rank leaderboard is visible and clear.
- [ ] Points perks page only shows front-desk redemption, no online mall.

## Stage 7: 我的、员工端、老板端、大屏上线化

**Files:**
- Modify: `miniprogram/pages/my-hub/`
- Modify: `miniprogram/pages/staff-desk/`
- Modify: `miniprogram/pages/boss-config/`
- Modify: `miniprogram/pages/tv-ranking/`
- Create: `docs/reviews/phase-37-ops-screen-launch-polish-review.md`

- [ ] My page contains editable profile and role entries.
- [ ] Staff page keeps only high-frequency actions.
- [ ] Boss page allows numeric parameters to be adjusted locally.
- [ ] TV screen is 16:9 and not based on cramped mobile layout.

## Standard Verification

Run after each stage:

```powershell
Get-ChildItem miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }
node scripts/check-json-files.js
node scripts/check-production-copy.js
node scripts/check-player-flow-routes.js
powershell -ExecutionPolicy Bypass -File scripts/check-ui-kit-asset-edges.ps1 -RequireAssets
& 'F:\微信web开发者工具\cli.bat' --port 30812 --lang zh preview --project 'F:\Making money\taiqiuxcx'
```
