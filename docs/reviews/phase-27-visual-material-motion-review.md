# Phase 27 Review: Visual Material And Motion Layer

## Scope

- Reduced the overall pure-black weight of the mini program UI.
- Added table-felt, wood rail, metal strip, score-light, and reward-plaque material language through shared tokens and components.
- Reconnected `star-track` to the extracted UI Kit PNG assets while keeping fixed alignment.
- Added the first shared motion layer for page entrance, reward floating, star lighting, and score flash.

## Checks

- `rg -n "rgba\([^)]*,\s*,|transparent [0-9]+r[^p]|[0-9]+r\)|NaN|undefined" miniprogram\styles miniprogram\components miniprogram\pages -g "*.wxss"`
- `Get-ChildItem -Path miniprogram -Recurse -Filter *.js | ForEach-Object { node --check $_.FullName }`
- `node scripts\check-json-files.js`
- `node scripts\check-production-copy.js`
- `powershell -ExecutionPolicy Bypass -File scripts\check-ui-kit-asset-edges.ps1 -RequireAssets`
- `git diff --check`
- `F:\微信web开发者工具\cli.bat --port 30812 --lang zh preview --project F:\Making money\taiqiuxcx`

## Results

- WXSS typo scan passed.
- JS syntax check passed.
- JSON check passed: 35 files checked.
- Production copy check passed: 21 formal page files checked.
- UI Kit edge check passed: 32 PNG assets checked.
- Diff whitespace check passed with CRLF warnings only.
- WeChat DevTools preview passed with AppID `wxe30b469d64636a2b`.

## Review Notes

- This phase intentionally changed shared sources first: `tokens.wxss`, `motion.wxss`, `player-flow.wxss`, `yh-panel`, `bottom-nav`, rank/reward/settlement components. This avoids page-by-page color drift.
- The star component now follows the asset-map rule again: star states use official PNG assets, not CSS or text glyphs. Alignment remains code-controlled through a fixed grid.
- Reward, rank, victory, accept, and settlement components now let extracted art assets carry the emotional value, while WXML/WXSS still renders dynamic copy and data.
- Motion is still conservative. It is meant to clarify state and add ceremony, not to turn staff or owner pages into an arcade UI.

## Remaining Risks

- Visual QA still requires manual simulator screenshots. CLI preview proves the project builds; it does not prove the new material balance looks right on every page.
- Staff pages may need a separate quieter material set if the shared panel treatment still feels too game-like for front-desk work.
- The page-level `prefers-reduced-motion` rule should be checked on target WeChat base library behavior during real-device QA.
