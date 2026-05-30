# Environment And Handoff Setup

This is a bundled internal reference. The user does not need to read it before starting; `SKILL.md` contains the startup flow. Use this file when a new teammate, machine, or autonomous growth agent needs setup details.

## Required Tools

- SQLite database file for campaign state. Use SQLite CLI when available; otherwise run the inline SQL through Python's standard `sqlite3` module as shown in `references/sql-workflows.md`.
- Python 3.10+ only for the bundled helper scripts: profile folder creation/import, screenshot fallback, and static rel verification.
- A real browser automation path:
  - Required for live submissions: an approved interactive browser controller connected to a real user browser/profile.
  - Examples: Codex Chrome Extension, Claude Code browser MCP/plugin, or another runtime-approved browser controller with cookies, OAuth, file upload, and human-verification handoff.
  - Fallback for unauthenticated/static checks: Playwright Chromium.
- Spreadsheet editor only for review exports; do not make spreadsheets the source of truth.
- Email inboxes or team login vault access for account verification.
- Product assets: logo, screenshot, PDF/one-pager, short and long descriptions.

## Recommended Directory Layout

```text
campaign/
  data/
    backlinks.db
    candidates.csv
  assets/
    logo.png
    screenshot.png
    product-one-pager.pdf
  skills/
    backlink-submission-automation/
```

The skill can live inside a repo for handoff. For auto-discovery by Codex, copy or symlink the skill folder into `$CODEX_HOME/skills` or `~/.codex/skills`.

## Bootstrap

Before collecting product fields, detect the current agent runtime's intake capability:

1. If a native structured-input UI/tool is available, use it and save `intake.mode=native_structured`.
2. If only structured choices are available, use them for decisions and collect free-text fields as JSON; save `intake.mode=hybrid_structured`.
3. If no structured UI/tool exists, use the Markdown fallback form in `SKILL.md`; save `intake.mode=markdown_fallback`.
4. If running unattended, read an answers JSON or existing profile path; save `intake.mode=file_import`.

Use `assets/intake-schema.json` as the portable schema for runtimes that can render a form from JSON schema. Do not present plain chat text as native structured intake.

Create/import a campaign profile from structured answers:

```bash
python skills/backlink-submission-automation/scripts/init_campaign_profile.py \
  --campaign-root campaigns \
  --answers-json skills/backlink-submission-automation/assets/structured-answers.example.json
```

Or import an existing profile repo/folder/file:

```bash
python skills/backlink-submission-automation/scripts/init_campaign_profile.py \
  --campaign-root campaigns \
  --import-path /path/to/existing/profile-or-repo
```

Initialize `campaigns/<campaign-slug>/data/backlinks.db` with `references/sql-workflows.md`:

1. Run **Bootstrap Schema**.
2. Run **Live Write Guards**.
3. Run **Seed Profile Basics** from the saved `profile/profile.json`.

Run these on every new database. They are idempotent except the migration block, where duplicate-column errors mean the column already exists.

## Candidate Import

Prepare CSV with at least:

```csv
domain,url,dr,category,source,notes
example.com,https://example.com/submit,72,AI directory,lxx_ai,page 1
```

Then import it with `references/sql-workflows.md` → **Import Candidate CSV**.

Use prepared candidate packs the same way by replacing the CSV path with a file under `candidate-packs/`.

After the team exports the full LXX list, store it as `candidate-packs/lxx-ai.csv` and import it the same way. New users without LXX access should use the prepared pack instead of trying to log in.

## Missing Images

If the user did not provide screenshots/logos, capture a homepage screenshot:

```bash
python skills/backlink-submission-automation/scripts/capture_homepage_screenshot.py \
  --url <canonical-url> \
  --out campaigns/<campaign-slug>/assets/homepage-screenshot.png
```

If Playwright is unavailable, use the active browser screenshot tool and save the resulting file under the campaign `assets/` folder.

## Browser Setup

For real submissions, require an approved interactive browser controller attached to a real user browser/profile. Many sites rely on cookies, Google OAuth, Cloudflare, browser uploads, or user-installed extensions; headless Playwright is not an acceptable primary executor for live submissions.

Runtime mapping:

- Codex: Codex Chrome Extension controlling the user's Chrome profile.
- Claude Code: approved browser MCP/plugin/Chrome control path connected to the user's authenticated browser profile.
- Gemini/custom agents: approved interactive browser controller that supports the user's browser profile, cookies, OAuth, file upload, and human-verification handoff.

Definition of a real submission:

- clicking a third-party submit/publish/save button
- creating or editing a live account/profile/listing
- using Google OAuth or email/password registration
- uploading logo, screenshot, PDF, or other files
- interacting with CAPTCHA, Cloudflare, or human-verification screens
- changing any live third-party page

Checklist:

- Confirm the runtime's approved interactive browser controller is connected.
- Confirm the authorized Google account is visible before clicking OAuth.
- If the controller is unavailable, stop and record `blocked_browser_controller`, `blocked_auth`, or a browser-specific blocker; do not substitute headless Playwright for the live action.
- Keep only active work tabs open; close finished pages.
- When using Playwright, avoid claiming a page has no form until you have checked scroll bottom, modals, dropdowns, iframes, and route links.

Allowed Playwright/headless uses:

- local smoke tests of this skill package
- static public HTML rel verification
- unauthenticated page inspection when no live action is taken
- screenshot fallback when Chrome screenshot tooling is unavailable

File uploads should go through the approved interactive browser controller. If upload fails because extension/controller file access is disabled, tell the user to enable file access for that controller, record the attempt, then retry within the 3-attempt limit.

## Credential Handling

Use `account_credentials` in the campaign DB as the operational handoff table:

- `platform_domain`
- `account_email`
- `username`
- `password` or vault pointer
- `auth_method`
- `credential_status`
- `source_submission_id`
- `notes`

The database also stores retry/error state:

- `submission_attempts`: every failed/blocked attempt.
- `error_patterns`: repeated error signatures and whether one optimization was already attempted.

If the organization has a password manager, store the real password there and write a stable vault pointer in `password`. If the user explicitly wants local DB storage, record the password directly.

Never commit a real campaign database with passwords to a public repo.

## Product Assets

Store product assets in a campaign `assets/` folder and reference them from the product profile JSON:

- square logo for avatars/icons
- wide logo or hero screenshot
- product screenshot
- PDF/one-pager for document sharing sites
- optional launched/thumbnail variants

If a submission form asks for a "Screenshot URL", use a stable public asset URL from the product site when available; otherwise upload the local file if the site supports upload.

## Health Check

Use `references/sql-workflows.md`:

1. **Reports** → KPI and status breakdown.
2. **Select Next Candidates** → next batch queue.

The report should show KPI counts. Candidate selection should return rows or make the queue/filter reason obvious.
