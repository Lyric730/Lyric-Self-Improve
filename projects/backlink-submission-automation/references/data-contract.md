# Data Contract

Use this reference when creating a new DB, mapping an existing project DB, writing queries, or explaining status/rel fields.

## Canonical Tables

### `campaign_profile`

One row per campaign/product.

| column | meaning |
|---|---|
| `key` | stable setting name |
| `value` | JSON/text value |

### `candidates`

Normalized candidate pool from LXX, Ahrefs, GitHub search, Serper, legacy pools, or manual URLs.

| column | meaning |
|---|---|
| `id` | candidate id |
| `source` | `lxx_ai`, `ahrefs`, `github`, `serper`, `legacy_226`, `manual` |
| `source_id` | id from source table/file when available |
| `domain` | normalized root/platform domain |
| `url` | best submission or inspection URL |
| `dr` | domain rating/inferred authority; integer when known |
| `category` | directory/profile/comment/classified/github/showcase/etc. |
| `submission_type` | `directory`, `profile`, `blog_comment`, `classified`, `github_pr`, `document`, `media`, `community`, `unknown` |
| `priority` | higher = sooner |
| `relevance_score` | product/profile relevance boost; can be stored or computed by selection SQL |
| `evidence_score` | route/evidence boost, such as known dofollow samples or visible submit route |
| `status` | `new`, `queued`, `submitted`, `skipped`, `blocked`, `failed`, `live` |
| `notes` | inspection notes |

### `submissions`

Every actual attempt or verified result.

| column | meaning |
|---|---|
| `source_table` / `source_id` | candidate source pointer |
| `platform_domain` | site/domain submitted to |
| `submit_url` | form/profile/PR URL used |
| `target_url` | target URL submitted |
| `anchor_text` | anchor or visible text used |
| `submit_method` | `browser`, `github_pr`, `csv_import`, `manual`, etc. |
| `status` | current execution status |
| `rel_actual` | verified rel classification |
| `live_url` | public page URL if known |
| `verification_evidence` | public proof used before writing `live` or `live_plain_text` |
| `verified_at` | timestamp for public verification |
| `error_log` | exact failure or traceback |
| `notes` | human-readable audit trail |

New databases should use `target_url`. Do not keep product-specific target columns in reusable skill databases.

### `submission_attempts`

One row per attempt. This table enforces "try at most three times, then stop".

| column | meaning |
|---|---|
| `id` | attempt id |
| `submission_id` | related `submissions.id`, when known |
| `source_table` / `source_id` | candidate pointer, when no submission row exists yet |
| `platform_domain` | site/domain attempted |
| `attempt_no` | 1, 2, or 3 |
| `status` | `failed`, `blocked`, `retrying`, `resolved`, etc. |
| `error_signature` | short stable error key |
| `error_message` | exact error text or observed blocker |
| `notes` | additional audit notes |

### `error_patterns`

Aggregated error signatures across the campaign.

| column | meaning |
|---|---|
| `error_signature` | primary key, short stable key |
| `occurrence_count` | how many times this error occurred |
| `optimization_attempts` | how many workflow/code fixes have been attempted |
| `status` | `observed`, `needs_optimization`, `optimization_attempted`, `unresolved_high_priority`, `resolved` |
| `priority_tag` | use `HIGH_PRIORITY_FIX` when unresolved after escalation |
| `first_seen` / `last_seen` | timestamps |
| `notes` | optimization notes |

### `account_credentials`

Operational account handoff. Store real passwords only if approved.

| column | meaning |
|---|---|
| `platform_domain` | site account belongs to |
| `account_email` | login email |
| `username` | username/display name |
| `password` | password or vault pointer |
| `auth_method` | `email_password`, `google_oauth`, `github_oauth`, `vault_pointer` |
| `credential_status` | `confirmed`, `pending_email_confirmation`, `missing_password`, `oauth`, etc. |
| `source_submission_id` | related `submissions.id` |
| `notes` | activation, verification, reset notes |

## Status Values

| value | use when |
|---|---|
| `live` | public page exists and rel was verified |
| `live_plain_text` | URL appears as text but no outbound `<a href>` |
| `submitted` | form/action was accepted, but no public approval state is known yet |
| `pending` | submitted or partially submitted, final public state unknown |
| `pending_review` | explicit admin/moderation review |
| `pending_email_confirmation` | email verification blocks completion |
| `pending_human_verification` | human CAPTCHA or identity check blocks completion |
| `blocked_captcha` / `blocked_recaptcha` / `blocked_turnstile` | CAPTCHA blocks automation |
| `blocked_auth` | login, permission, or paid wall blocks progress |
| `blocked_browser_controller` | no approved interactive browser controller is available for live submission |
| `failed` | attempted but not accepted or not recoverable without new info |
| `failed_after_3_attempts` | same candidate failed three times; do not retry without new evidence |
| `skipped` | intentionally skipped with a recorded reason |
| `skipped_low_dr` | DR below campaign threshold |
| `skipped_manual_hold` | high-stakes site reserved for manual launch |
| `skipped_no_submission_form` | no usable submit/list/profile path found after full inspection |
| `skipped_no_public_link` | accepts content but cannot render a public external link |

## Rel Values

| value | KPI? | meaning |
|---|---:|---|
| `dofollow` | yes | actual outbound link and rel does not include `nofollow`, `ugc`, `sponsored`, or `me` |
| `nofollow` | no | link exists but rel includes `nofollow` |
| `ugc` | no | user-generated-content signal; not KPI |
| `nofollow_ugc` | no | both nofollow and ugc |
| `sponsored` | no | sponsored/paid signal |
| `me_no_pagerank` | no | `rel="me"` identity relation; not SEO KPI |
| `live_plain_text` | no | URL text exists but no outbound anchor |
| `none` | review | rel attribute empty or unavailable; inspect notes before counting |
| `unknown` | no | cannot verify yet |
| `pending_expected_dofollow` | no | samples suggest dofollow if approved, but not live yet |

## KPI Queries

```sql
SELECT COUNT(*) AS live_dofollow
FROM submissions
WHERE status='live' AND rel_actual='dofollow';
```

```sql
SELECT status, rel_actual, COUNT(*) AS count
FROM submissions
GROUP BY status, rel_actual
ORDER BY count DESC;
```

```sql
SELECT platform_domain, live_url
FROM submissions
WHERE status='pending_review'
ORDER BY submit_time DESC;
```

## Existing Project Mapping

If a project already has source-specific tables, keep them and map into canonical fields:

- `lxx_ai.domain/url/dr/category/submitted` -> `candidates`.
- `gefei_226.root_domain/url/type/has_url_field/link_strategy/submitted` -> `candidates`.
- `ahrefs_api_results.backlink_url/dr/competitor/title` -> candidates for manual inspection or GitHub/showcase outreach.

Do not delete source tables. They are evidence.

## Retry/Error Queries

```sql
SELECT error_signature, occurrence_count, optimization_attempts, status, priority_tag
FROM error_patterns
WHERE occurrence_count >= 3 OR status='unresolved_high_priority'
ORDER BY occurrence_count DESC;
```

```sql
SELECT platform_domain, attempt_no, error_signature, error_message, created_at
FROM submission_attempts
WHERE status IN ('failed', 'blocked')
ORDER BY created_at DESC
LIMIT 50;
```
