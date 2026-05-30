# Verification And Reporting

Use this reference after any submission or during status refresh.

## Verification Order

1. Open the public URL in a browser.
2. Inspect rendered DOM for `a[href*="target-domain"]`.
3. Fetch raw public HTML when possible to confirm logged-out visibility.
4. Classify rel.
5. Update `submissions`.
6. Recompute KPI.

## Browser DOM Snippet

Run in browser evaluation when a page is JS-rendered:

```javascript
() => {
  const target = "product.example";
  const links = Array.from(document.querySelectorAll(`a[href*="${target}"]`));
  return links.map((a) => ({
    text: (a.textContent || "").trim().slice(0, 120),
    href: a.href,
    rel: (a.getAttribute("rel") || "").toLowerCase().trim(),
    visible: !!(a.offsetWidth || a.offsetHeight || a.getClientRects().length),
  }));
}
```

If no links are found, search body text for the naked URL to determine `live_plain_text`.

## Rel Classification

Classify the actual public link, not what was typed into a form.

```text
contains sponsored -> sponsored
contains nofollow and ugc -> nofollow_ugc
contains nofollow -> nofollow
contains ugc -> ugc
token "me" -> me_no_pagerank
otherwise actual anchor -> dofollow
no actual anchor but text exists -> live_plain_text
not public/approved -> unknown or pending_expected_dofollow
```

Important:

- `noopener`, `noreferrer`, `external`, and `author` are not nofollow by themselves.
- `rel="me"` is an identity relation and must not be counted as SEO dofollow.
- You cannot make a third-party page dofollow by manually editing DOM in your browser.

## Static HTML Verification

Use:

```bash
python skills/backlink-submission-automation/scripts/verify_rel.py \
  --db data/backlinks.db \
  --submission-id 123 \
  --url https://example.com/products/product-name \
  --target-domain product.example
```

If the site requires JS, use browser verification and then update manually:

Use `references/sql-workflows.md` → **Record Live After Verification** with `live_url`, `rel_actual`, and `verification_evidence`.

The DB live-write guards refuse `status=live` or `status=live_plain_text` without `live_url` and `verification_evidence`. Pending/submitted rows may be recorded immediately, but live value must be verified first.

## Recheck Cadence

| status | recheck |
|---|---|
| `pending_review` | 24h, 72h, 7d, then weekly |
| `pending_email_confirmation` | after email action |
| `pending_human_verification` | after human completes challenge |
| `pending_expected_dofollow` | daily until public or 7d expires |
| `live` nofollow/ugc | no need unless site later approves/changes |
| `failed` / skipped | do not retry unless new evidence appears |

## Reporting Format

Always separate:

- true live dofollow KPI
- live nofollow/ugc
- live plain text only
- pending review/approval
- blocked by CAPTCHA/auth
- failed/skipped
- accounts created and their credential status
- error signatures repeated 3+ times and any `unresolved_high_priority` items

Do not say "built X backlinks" when most are pending or nofollow. Say "submitted X, live Y, dofollow Z".

## Useful Queries

```sql
SELECT platform_domain, live_url
FROM submissions
WHERE status='live' AND rel_actual='dofollow'
ORDER BY submit_time DESC;
```

```sql
SELECT status, COUNT(*) count
FROM submissions
GROUP BY status
ORDER BY count DESC;
```

```sql
SELECT platform_domain, credential_status, account_email, username
FROM account_credentials
ORDER BY updated_at DESC;
```
