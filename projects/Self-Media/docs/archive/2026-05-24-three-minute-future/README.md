# Three-Minute Future Cleanup Archive

This archive keeps process notes from the 2026-05-24 cleanup pass.

## Kept As Production Source

- `lines/three-minute-future/`: reusable production line scripts, configs, runbook, visual brief, and task flow.
- `daily/2026-05-23/three-minute-future/`: first approved issue assets and publish package.
- `daily/_state/three-minute-future/published-ledger.json`: published-topic ledger seeded with the 2026-05-23 issue.

## Archived Here

- `date-dedup-design.md`: design notes for separating `publishDate` and `contentDate`.
- `date-dedup-plan.md`: implementation plan for date inference and published-content dedupe.

## Deleted During Cleanup

- `.superpowers/`: temporary brainstorm preview artifacts.
- `daily/2026-05-24/three-minute-future/`: abandoned same-day trial output. The mechanism remains in code, but the 2026-05-24 material should not be treated as a real issue.
- `daily/2026-05-23/three-minute-future/publish/images/.chrome-profile/`: temporary browser profile produced during PNG export.

## Current Direction

The next production-line pass should start from the reusable source under `lines/three-minute-future/`.
The 2026-05-23 issue is the visual/content baseline. The paused video track should use those approved images first, while TTS voice selection remains a separate user decision.
