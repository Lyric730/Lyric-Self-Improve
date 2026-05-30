# Submission SOP

Use this reference while operating the browser.

## Universal Preflight

Live submissions must use the runtime's approved interactive browser controller on the user's real browser/profile. Examples: Codex Chrome Extension, Claude Code browser MCP/plugin, or another approved browser controller with cookies, OAuth, file upload, and human-verification handoff. Do not click live third-party submit/save/publish buttons with headless Playwright. If no approved controller is available, record `blocked_browser_controller` or a browser-specific blocker and stop.

Before deciding "cannot submit":

1. Open the candidate URL.
2. Wait for the page to settle.
3. Scroll to the bottom.
4. Inspect footer, nav menus, account menus, dropdowns, modals, and embedded forms.
5. Click likely routes:
   - `Submit`
   - `Add tool`
   - `List your tool`
   - `List your product`
   - `Add startup`
   - `Vendor signup`
   - `Claim profile`
   - `Contribute`
6. Check if the submission form is inside an iframe or a third-party form builder.
7. Search page text for `submit`, `list`, `product`, `tool`, `startup`, `software`, `profile`, `website`, `url`.
8. If login is required and authorized accounts are available, use Google OAuth or create an email/password account.

Do not inspect only the first viewport or only visible DOM inputs.

## Field Mapping

| form field | preferred value |
|---|---|
| Product/Tool/Company name | product profile `brand_name` |
| Website/URL | product profile `canonical_url`, normalized lowercase when the brand allows it |
| Contact email | profile/directory email from product profile |
| Submitter name | product profile `submitter_name` or approved human name |
| Category | product profile `categories` |
| Tags | product profile `tags` |
| HQ/Country | product profile `hq_country` / `hq_city` |
| Description | use `references/templates.md`; include URL if no website field exists |
| Screenshot/logo | use product profile assets |
| Reciprocal badge | only add if the product owner approves; otherwise choose "No" or skip |

If a site forces Europe/HQ/company-size fields, fill them from the product profile. Do not stop on easy profile fields.

## Directory/Product Listing

1. Fill all required product facts.
2. If only one URL field exists, use canonical home URL.
3. If there are extra URL fields, add blog/docs only if relevant.
4. If no website field exists but public description supports links, put the target URL in the description naturally.
5. Upload screenshot/logo if required.
6. Submit free/basic path unless the user approved payment.
7. Record `pending_review` when the site says review/queue/approval.
8. Record exact public slug if shown, even if not live yet.

## Profile/Account Page

1. Check public samples first: do website links render and what rel do they use?
2. Create or log into account only if a website/profile/bio link can plausibly become public.
3. Fill website, bio, company name, social links, avatar/logo.
4. Visit the public profile while logged out or in raw fetch when possible.
5. If the profile has no website field but has a bio/description, include a natural naked URL and verify whether it becomes a link.

## Blog Comment

Use only when the article has a real comment form and an author URL/website field.

1. Use a comment-specific email if the campaign has one.
2. Name should look human, not the brand.
3. Website field gets the target URL.
4. Comment body should be topical and specific; do not paste generic praise.
5. Do not stuff links into comment body unless the campaign explicitly allows testing HTML comments.
6. Submit, capture moderation URL or comment anchor.
7. Verify author URL rel if visible.

## Classifieds

1. Choose the closest category, commonly Digital Items, Websites, Software, Business, or Services.
2. Put the target URL both in URL field and body if allowed.
3. Use plain URL in body if Markdown/HTML is rejected.
4. Upload an image when available.
5. Many classified sites show a success page but delay public publication. Mark `pending_review` until public page verifies.

## GitHub Awesome List PR

1. Check contribution guidelines and existing entry format.
2. Add one concise entry in the most accurate category.
3. Avoid promotional wording.
4. Open a PR with a small diff and direct title.
5. Record as `pending_review` until merged.
6. After merge, verify the live README link and rel.

## Document/Media Sharing

1. Use a PDF/one-pager with target URL visible inside the document.
2. Fill title, description, tags, category.
3. If profile website field exists, set it.
4. Publish public, not private/unlisted when SEO value matters.
5. Verify whether the external link is a real anchor, nofollow, plain text, or inside a viewer only.

## CAPTCHA And Human Verification

Do not fake completion. Record:

- `blocked_captcha` if registration/submit cannot proceed.
- `pending_human_verification` if the tab is ready and only a human check remains.
- `pending_email_confirmation` if email activation is required.

Keep only necessary handoff tabs open. Close all others.

## Account Recording

After account creation, immediately run:

```bash
python skills/backlink-submission-automation/scripts/record_submission.py account \
  --db data/backlinks.db \
  --platform example.com \
  --email submit@example.com \
  --username productname \
  --password 'vault:Backlink/example.com' \
  --auth-method email_password \
  --credential-status confirmed \
  --notes "Created during directory submission"
```

If the user wants direct password storage, put the password in `--password`. If a password manager is used, put the vault pointer there.

## Submission Recording

After each attempt:

```bash
python skills/backlink-submission-automation/scripts/record_submission.py submission \
  --db data/backlinks.db \
  --platform example.com \
  --submit-url https://example.com/submit \
  --target-url https://product.example/ \
  --status pending_review \
  --rel unknown \
  --live-url https://example.com/products/product-name \
  --notes "Submitted free listing; waiting approval"
```

## Retry Recording

Each submission/candidate may be attempted at most three times. After each failed attempt, record it:

```bash
python skills/backlink-submission-automation/scripts/record_submission.py error \
  --db data/backlinks.db \
  --platform example.com \
  --source-table candidates \
  --source-id 12 \
  --attempt-no 1 \
  --error-signature upload_button_timeout \
  --error-message "Image upload button timed out after file chooser opened" \
  --notes "Retry with smaller PNG"
```

If the same error signature reaches three occurrences, stop the batch and optimize once. If the same error occurs after that optimization, record it with `--after-optimization`; the script marks it `unresolved_high_priority` and the agent should route around it.
