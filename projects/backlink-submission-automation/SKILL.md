---
name: backlink-submission-automation
description: "Generic end-to-end backlink growth operations for any product: campaign setup, candidate sourcing, DR/risk filtering, browser-based directory/profile/comment/product submissions, account and password tracking, retry/error escalation, public rel verification, SQLite reporting, and handoff to an autonomous growth agent. Use when the user asks to build or run an external backlink campaign, submit a product/tool/site to backlink sources, process LXX/Ahrefs/GitHub/CSV candidates, verify dofollow/nofollow/ugc links, or turn backlink work into repeatable automation."
---

# Backlink Submission Automation

## Core Objective

Grow verified backlinks for any product without losing auditability. Treat the database as the source of truth: every candidate, account, submission attempt, failure, pending review, public URL, and rel result must be recorded.

The KPI is strict:

```sql
SELECT COUNT(*)
FROM submissions
WHERE status='live' AND rel_actual='dofollow';
```

Never hardcode a product's positioning, URL, country, assets, or forbidden wording in the skill. Load those facts from the campaign product profile.

## Skill Folder Contract

This skill must be usable from the folder alone. `SKILL.md` is the complete operating entrypoint. Files under `references/` are bundled internal manuals for deeper steps; they are not external prerequisites for the user to read before starting. Files under `scripts/` are the executable helpers.

Files under `candidate-packs/` are also bundled skill resources. When a user installs the skill from Git, a ZIP archive, or by copying the whole `backlink-submission-automation/` folder into `CODEX_HOME/skills`, the candidate CSVs and `candidate-packs/manifest.json` travel with the skill. Do not require a new user to have the original local SQLite database, LXX invite, or Ahrefs account if a prepared pack is already bundled.

## Real Submission Browser Requirement

For any real third-party submission, the agent must use an approved interactive browser controller attached to a real user browser/profile. "Real submission" includes clicking a third-party submit button, creating or editing an account/profile, using Google OAuth, uploading logo/screenshots/files, passing through Cloudflare or CAPTCHA screens, or changing any live third-party page.

The controller is runtime-specific:

- Codex: Codex Chrome Extension controlling the user's Chrome profile.
- Claude Code: an approved browser MCP/plugin/Chrome control path connected to the user's authenticated browser profile.
- Gemini or custom growth agents: their approved interactive browser controller, if it supports the user's browser profile, cookies, OAuth, file upload, and human-verification handoff.

Do not use headless Playwright as the primary executor for real submissions. Playwright is allowed for local smoke tests, static public HTML checks, screenshot fallback, and unauthenticated read-only inspection only. If no approved interactive browser controller is available, stop the live submission, record the blocker in the campaign DB, and ask the user to connect the appropriate browser controller instead of switching to headless automation.

Before starting a live submission:

1. Confirm the runtime's approved interactive browser controller is connected.
2. Confirm it is using the authorized browser profile and existing login state when available.
3. If login is required, use approved Google OAuth or approved email/password registration.
4. If file upload fails, tell the user to enable file access for the active browser controller/extension, then retry within the 3-attempt policy.
5. Close finished Chrome tabs before ending the batch, keeping only explicit handoff tabs for CAPTCHA, email verification, or user approval.

## Invocation Startup: Cross-Agent Intake

When the skill is invoked and no campaign profile is already selected, collect intake with this capability order:

1. **Native structured input first.** If the current runtime exposes a structured-input UI or tool, use it. Examples include Codex Asked / `request_user_input` when available, a Claude/Gemini form adapter, a JSON-schema form renderer, or a CLI prompt wizard.
2. **Hybrid structured input second.** If native structured input only supports choices, use it for decisions such as profile source, credential policy, and candidate source, then collect free-text fields as a structured JSON block.
3. **Markdown fallback third.** If no structured-input capability exists, use the fallback form below in a normal message.
4. **File import for unattended agents.** If the agent runs without a user, read `--answers-json`, `--import-path`, or an existing profile folder/repo and continue.

Do not claim that native structured input was triggered unless an actual runtime UI/tool/schema adapter was used. Record the chosen path in the answers JSON as `intake.mode` with one of: `native_structured`, `hybrid_structured`, `markdown_fallback`, `file_import`.

Use `assets/intake-schema.json` as the canonical field contract for any runtime that can render JSON-schema-style forms. Required fields are deliberately minimal:

- `profile_mode`: `new` or `import`.
- If importing: `import_path`.
- If creating: `brand_name`, `canonical_url`, `contact_email`, `allow_account_creation`, and `password_storage`.

Optional fields may be `"none"` or blank. The agent must complete missing optional facts from the product website, public docs, screenshots, or user-provided assets before the first live submission.

### Markdown Fallback Intake Form

Use this only when native structured input is unavailable:

```text
Please provide the minimum backlink automation startup information.
Required fields must be filled. Optional fields may be "none"; the agent will complete them from the website and product materials.

[A. Profile source, choose one]
1. Create a new profile.
2. Import an existing profile: provide a profile repo/folder/JSON path or Git URL.

[B. Required for a new profile]
- Product/brand name:
- Official website URL:
- Contact/registration email:
- May the agent create third-party submission accounts and store credentials: yes/no
- Password storage mode: local_sqlite / team_vault_pointer / current_session_only

[C. Optional for a new profile]
- One-line positioning:
- Target users:
- Short product description:
- Categories/tags:
- HQ country/city:
- Forbidden phrases:
- Logo/screenshot/PDF paths:
- Minimum DR threshold:
- Manual-hold platforms:

[D. Candidate source, choose after profile creation]
1. Import your own backlink source file/folder/database.
2. Use bundled/team-prepared candidate packs and execute candidates one by one.
```

If the user selects an existing profile repository/folder/file, load it with `scripts/init_campaign_profile.py --import-path ...` and do not ask for fields already present. If the user selects "new profile", create a dedicated campaign profile folder before submitting anything.

## First-Run Setup

After the intake answer is available, normalize it into an answers JSON file and create/import the profile:

```bash
python skills/backlink-submission-automation/scripts/init_campaign_profile.py \
  --campaign-root campaigns \
  --answers-json path/to/structured-answers.json
```

Then initialize the DB from the saved profile:

```bash
python skills/backlink-submission-automation/scripts/bootstrap_backlink_db.py \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --profile campaigns/<campaign-slug>/profile/profile.json
```

If images are missing, create screenshots automatically before first submissions:

```bash
python skills/backlink-submission-automation/scripts/capture_homepage_screenshot.py \
  --url <canonical-url> \
  --out campaigns/<campaign-slug>/assets/homepage-screenshot.png
```

If Playwright is unavailable, use the active browser screenshot tool and save the image into the campaign `assets/` folder.

Keep real passwords in the campaign database or an approved team vault, not in the skill package.

## Operating Loop

1. **Load campaign context**
   - Load `campaigns/<slug>/profile/profile.json` or import an existing profile folder/repo.
   - Confirm target domain, brand wording, assets, emails, manual-hold sites, DR threshold, daily velocity, and forbidden phrases.
   - Use the product's own positioning in every submission.

2. **Choose candidate source after profile completion**
   - Ask the user to choose:
     1. import their own candidate source file/folder/database, or
     2. use bundled/team-prepared candidate packs and execute one by one.
   - For imported sources, use `scripts/import_candidates.py`.
   - For prepared packs, read `candidate-packs/manifest.json`, then import one or more CSVs from `candidate-packs/`.
   - LXX is optional: users without an LXX invite/code cannot see the full list, so treat LXX as a prepared candidate pack once the team exports it.
   - Ahrefs-derived packs are research packs unless the row is clearly actionable, such as an awesome-list repository. Inspect the route in the browser before submitting.
   - Legacy 226 packs are review packs. Re-open every URL; do not trust old audit labels.

Prepared-pack import example:

```bash
python skills/backlink-submission-automation/scripts/import_candidates.py \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --csv skills/backlink-submission-automation/candidate-packs/lxx-ai.csv \
  --source lxx_ai
```

3. **Ingest and score candidates**
   - Read `references/source-to-candidate.md` when importing LXX, Ahrefs, GitHub, Serper, legacy pools, or arbitrary CSVs.
   - Import CSV candidates with `scripts/import_candidates.py`.
   - Select the next batch with `scripts/next_candidates.py`; it combines DR, stored priority, product relevance, public-link evidence, friction, and manual-hold filters.
   - Hold high-effort flagship platforms for manual launch unless the user explicitly assigns them.

4. **Preflight each site in the browser**
   - For real submissions, use the runtime's approved interactive browser controller on the user's authenticated browser profile. Do not run real submissions through headless Playwright.
   - Scroll to the bottom, inspect embedded forms/iframes, open menus/dropdowns, click "List your product/tool/software", and check account/profile settings.
   - Do not judge a page only from visible inputs in the first viewport.
   - If there is no website field but a public description/bio field exists, include the target URL naturally there and later verify whether it renders as a link.

5. **Submit with bounded retries**
   - Read `references/submission-sop.md` for field mapping and site-type playbooks.
   - Each candidate/submission gets at most **3 attempts**.
   - After each failed attempt, record an attempt row with `scripts/record_submission.py error`.
   - If the same submission still fails after attempt 3, stop retrying that submission, record `failed`, and move to the next candidate.
   - If the same error signature occurs **3 times across the batch/campaign**, stop the task and optimize the workflow once.
   - If that one optimization does not fix the error, stop solving that error class; record it as `unresolved_high_priority` in `error_patterns` and continue around it.

6. **Record immediately**
   - Use `scripts/record_submission.py` for submissions, attempts, errors, and accounts.
   - Record failed, skipped, blocked, and pending items too. This prevents repeated dead-end work.
   - Do not record `status=live` or `status=live_plain_text` until public evidence has been checked; the script requires `--verified`, `--evidence`, and `--live-url` for those states.

7. **Verify public value**
   - Read `references/verification-and-reporting.md`.
   - Use `scripts/verify_rel.py` for static public HTML and browser inspection for JS-rendered pages.
   - Count a link as dofollow only when public HTML/DOM contains an actual `<a href>` to the target and rel does not include `nofollow`, `ugc`, or `sponsored`.
   - `rel="me"` is `me_no_pagerank`; it is not KPI dofollow.
   - You cannot force dofollow by editing a third-party `href` in the browser; the public site controls rel.

8. **Report**
   - Run `scripts/report.py --db data/backlinks.db`.
   - Report true dofollow separately from live nofollow, live plain text, pending review, blocked CAPTCHA, failed, skipped, and high-priority unresolved errors.

## Retry And Error Escalation

Use this exact policy:

| condition | action |
|---|---|
| one attempt fails | record `submission_attempts` and retry if attempts `< 3` |
| same candidate fails 3 times | mark submission/candidate failed and record exact reason |
| same error signature appears 3+ times | stop batch and perform one optimization change |
| error persists after one optimization | do not keep debugging; mark `unresolved_high_priority` and route around it |
| error is payment/manual-identity/fake-review | skip immediately; do not retry |

Good error signatures are stable and short, for example:

- `secureimg_captcha_register`
- `cloudflare_turnstile_submit`
- `form_submit_403_cleantalk`
- `upload_button_timeout`
- `oauth_account_not_allowed`
- `public_page_404_after_success`

## Status Discipline

Use these status values consistently:

- `live`: public page exists and rel was verified.
- `live_plain_text`: public page contains the URL as text but not a real outbound link.
- `submitted`: form/action was accepted, but no public review state is known yet.
- `pending_review`: submission accepted but not public/approved yet.
- `pending_email_confirmation`: account or listing waits for email verification.
- `pending_human_verification`: human CAPTCHA or identity check is the only blocker.
- `blocked_captcha`, `blocked_recaptcha`, `blocked_turnstile`: CAPTCHA prevents progress.
- `blocked_browser_controller`: no approved interactive browser controller is available.
- `blocked_auth`: login/account permission prevents progress.
- `failed`, `failed_after_3_attempts`: attempted but did not submit or cannot verify after allowed retries.
- `skipped_low_dr`, `skipped_manual_hold`, `skipped_no_submission_form`, `skipped_no_public_link`: intentionally skipped after inspection.

Use these rel values consistently:

- `dofollow`: actual outbound link and no `nofollow/ugc/sponsored/me`.
- `nofollow`, `ugc`, `sponsored`, `nofollow_ugc`: not KPI.
- `me_no_pagerank`: identity relation, not KPI.
- `live_plain_text`: visible text URL but no actual outbound anchor.
- `no_link_found`: public page checked and no target link/text was found.
- `none`: page inspected but no rel attribute or no useful link context; read notes.
- `unknown`: not enough public evidence yet.
- `pending_expected_dofollow`: samples suggest dofollow if approved, but the target is not live yet.

## Resource Map

- `references/environment.md`: portable setup, browser, credentials, assets, handoff.
- `references/data-contract.md`: canonical schema, rel/status taxonomy, account and error storage.
- `references/source-to-candidate.md`: candidate sourcing, CSV formats, DR/risk filters.
- `references/submission-sop.md`: browser submission SOP by site type.
- `references/verification-and-reporting.md`: rel verification, reporting, recheck cadence.
- `references/risk-policy.md`: velocity, manual-hold sites, low-DR policy, stop signals.
- `references/templates.md`: product-profile-driven form copy templates.
- `assets/intake-schema.json`: canonical cross-agent intake schema and UI hints.
- `candidate-packs/starter-pack.csv`: starter candidate pack for users without their own source.
- `candidate-packs/manifest.json`: bundled pack index with row counts, source notes, and import commands.
- `candidate-packs/lxx-ai.csv`: team-exported LXX-style directory/profile/classified candidate pack.
- `candidate-packs/ahrefs-competitor-backlinks.csv`: competitor-backlink research pack; only clearly actionable rows should be submitted.
- `candidate-packs/legacy-226-review.csv`: old 226 blog-comment review pack; browser re-audit is mandatory.
- `scripts/init_campaign_profile.py`: create/import a campaign profile folder from structured answers.
- `scripts/capture_homepage_screenshot.py`: capture homepage screenshot when the user did not provide images.
- `scripts/bootstrap_backlink_db.py`: initialize/extend SQLite campaign database.
- `scripts/import_candidates.py`: import candidates from CSV.
- `scripts/next_candidates.py`: select prioritized candidates.
- `scripts/record_submission.py`: insert/update submissions, attempts, errors, and credentials.
- `scripts/verify_rel.py`: classify public backlink rel from HTML.
- `scripts/report.py`: summarize KPI, pending work, accounts, failures, and high-priority errors.

## Completion Checklist

Before saying a batch is done:

1. Each attempted site has a `submissions` row.
2. Each failed attempt has a `submission_attempts` row.
3. Any repeated error signature with 3+ occurrences has an `error_patterns` row and either one optimization attempt or `unresolved_high_priority`.
4. Each created account has an `account_credentials` row or an explicit vault pointer.
5. Public pages were verified from a logged-out or raw-HTML perspective where possible.
6. KPI dofollow count was recomputed from the database.
7. Pending/human-verification items are clearly separated from live links.
8. Used browser tabs are closed except deliberate handoff tabs.
