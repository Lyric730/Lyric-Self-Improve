# Risk Policy

Use this reference when deciding whether to submit, skip, slow down, or reserve a site for manual launch.

## Authority Thresholds

Default:

- DR below 20: skip as `skipped_low_dr`.
- DR 20-39: submit only if highly relevant and low friction.
- DR 40-69: normal queue.
- DR 70-89: high priority if self-serve.
- DR 90+: high priority, but check manual-hold rules.

If the user gives a different threshold, record it in `campaign_profile`.

## Manual-Hold Sites

Do not automate these unless explicitly requested:

- Product Hunt.
- Hacker News launch posts.
- G2/Capterra/TrustRadius/review sites.
- paid advertorial/sponsored placements.
- anything requiring a real customer review.

These are not failures. Mark `skipped_manual_hold`.

## Velocity

For a young domain, avoid concentrated spikes. Prefer steady manual/assisted batches:

| stage | guidance |
|---|---|
| calibration | 5-10 fully verified manual submissions |
| early automation | 2-3 submissions/day |
| scaled automation | 5-8 submissions/day after quality is proven |
| review | weekly KPI and GSC/Ahrefs check |

Slow down when:

- many recent links are low-quality nofollow/ugc/comment spam.
- public pages are not getting indexed.
- search console/manual action risk appears.
- acceptance rate drops sharply.

## Quality Rules

Submit when:

- the site is relevant to AI tools, startups, software, productivity, small business, directories, or developer resources.
- there is a self-serve submission/profile/listing path.
- existing public examples show real outbound links.
- the product facts can be represented honestly.

Skip when:

- no public link can render.
- only private dashboards or internal bookmarks are available.
- the site is parked, hacked, spammy, or unrelated.
- CAPTCHA blocks all progress and no human handoff is planned.
- the only route is deceptive review/testimonial behavior.

## Low-DR And Toxic Sites

Low DR is not automatically toxic, but it usually has poor ROI. Combine DR with:

- topical relevance
- public page quality
- outbound link pattern
- spam niche
- whether many unrelated submissions appear recent

For DR under threshold, skip unless the user explicitly says to include nofollow/low-DR for breadth.

## CAPTCHA Policy

Do not pretend a CAPTCHA was solved. Use:

- `blocked_captcha` when blocked at form/signup.
- `pending_human_verification` when the form is filled and a human action remains.
- `pending_email_confirmation` when email activation is the next step.

If using a CAPTCHA-solving service, the user must approve it and the campaign must record the integration.

## Retry And Optimization Limits

Per candidate/submission:

- attempt 1 fails -> record and retry if a different low-risk action is available.
- attempt 2 fails -> record and make one small adjustment.
- attempt 3 fails -> mark `failed_after_3_attempts`; do not keep retrying.

Across the campaign:

- if the same `error_signature` appears 3 times or more, stop the current batch.
- perform one optimization change only: update SOP, adjust script, change upload asset, or alter field strategy.
- if the error occurs again after that optimization, mark the pattern `unresolved_high_priority` with priority tag `HIGH_PRIORITY_FIX`.
- after that, route around this error class; do not spend the run repeatedly debugging it.

## Stop Signals

Pause automation and report when:

- credentials repeatedly fail or accounts are locked.
- submissions require payment.
- a site asks for misleading claims, fake reviews, or personal identity.
- external pages start publishing incorrect product descriptions at scale.
- the browser session is unstable or many tabs are left open.
