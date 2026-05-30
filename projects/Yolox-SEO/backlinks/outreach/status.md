# Outreach Status

Last updated: 2026-05-24

## Active

| Target | Type | Status | Next action |
|---|---|---|---|
| `filipecalegario/awesome-vibe-coding#195` | GitHub awesome list PR | Open, waiting for maintainer merge | Verify after merge, then mark live dofollow if merged page exposes a normal link |
| `gefei_226` pool | Blog/profile review | Full sweep complete, `remaining_no=0` | Recheck pending URLs later and update from public HTML only |
| WP comment submissions | Blog comments | 16 live nofollow/ugc, 59 pending, 25 failed | Do not resubmit same rows; only verify pending status later |

## Current Counts

| Metric | Count |
|---|---:|
| Live dofollow KPI | 0 |
| Live nofollow/ugc/sponsored submissions | 16 |
| Pending submissions | 59 |
| Failed submissions | 25 |
| `rel="me"` no SEO value | 1 |
| `gefei_226` remaining `submitted='no'` | 0 |

## Gefei 226 Pool

Full sweep completed on 2026-05-24. Final `gefei_226.submitted` distribution:

Important: this was an automated public HTML sweep, not a Chrome visual review
of all 226 rows. Treat `skipped` / `failed` rows as auto-checked outcomes.
Chrome spot-check notes were added for representative rows after the audit
question.

| submitted | Count |
|---|---:|
| `dead` | 25 |
| `failed` | 25 |
| `pending` | 58 |
| `skipped` | 101 |
| `yes` | 17 |

## Priority Queue

1. Recheck pending moderation/unverified URLs after a delay and update `rel_actual` from the public page only.
2. Continue submission-friendly targets: showcase, awesome list, directory submission, profile/signup with visible website field.
3. Find more GitHub awesome lists related to agents, vibe coding, AI builders, small business automation.
4. Email outreach such as Prismic / n8n / Zapier remains lowest priority.

## Rules

- `nofollow` / `ugc` submissions are allowed and recorded as successful live submissions when visible.
- Only `status='live' AND rel_actual='dofollow'` counts toward the dofollow KPI.
- `rel="me"` is recorded as `me_no_pagerank`, not dofollow.
- Do not use `marketplace` as Yolox positioning or anchor text.
- Do not place raw Yolox links inside comment bodies when there is no URL/profile field.
