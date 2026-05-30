# Backlinks And Technical SEO Reference

Use this reference for backlink operations and technical SEO audits.

## Backlink KPI

Count only links that are:

- Publicly visible.
- Verified from public HTML or a public page.
- `status = live`.
- `rel_actual = dofollow` or equivalent absence of nofollow-like attributes.

Record but do not count as dofollow KPI:

- `nofollow`
- `ugc`
- `sponsored`
- `rel="me"`
- Links visible only in dashboards, previews, or edit screens.

## Prospect Sources

Use:

- Competitor backlink exports.
- Sites shared by multiple competitors.
- GitHub awesome lists.
- Product directories.
- Showcases.
- Resource pages.
- Profile pages with public website fields.
- Partner or integration pages.
- Relevant blog/comment fields only when naturally allowed.

Avoid blind bulk submission. Run one clear path manually before scaling a source type.

## Prospect Screening

Ask:

1. Can the site accept self-service submission, PR, profile URL, or a clear request?
2. Is the link placement natural?
3. Will the link appear on a public page?
4. Can rel be verified from public HTML?
5. Is the human effort justified by link quality and likelihood?

Downgrade prospects with hidden links, high friction, unclear approval paths, or only nofollow/rel-me outcomes.

## Submission Types

Use consistent values:

- `directory`
- `showcase`
- `github_pr`
- `profile`
- `resource_page`
- `guest_post`
- `comment_url_field`
- `email_outreach`

Do not put raw promotional links into comment bodies when the site has no website field or relevant context.

## Backlink Tracker Schema

Minimum fields:

| Field | Meaning |
|---|---|
| `source_site` | Domain or platform |
| `target_url` | Page being linked to |
| `submission_type` | Directory, PR, profile, etc. |
| `submitted_url` | Form, PR, profile, or request URL |
| `status` | `candidate`, `submitted`, `pending`, `live`, `rejected`, `failed`, `skipped` |
| `rel_expected` | Expected rel before verification |
| `rel_actual` | Verified rel result |
| `evidence_url` | Public page proving the link |
| `notes` | Useful context |
| `created_at` | Created date |
| `updated_at` | Last checked date |

## Verification

Verify from public pages only:

- Open the public evidence URL.
- Inspect the rendered link or source HTML.
- Record destination URL.
- Record rel attribute.
- Record anchor text.
- Update status.

If a submission is awaiting moderation, leave it as `pending`. Do not resubmit the same row without evidence that the prior submission failed.

## Technical SEO Audit

Audit in this order:

1. Crawlability: sitemap, robots, indexable pages.
2. Index control: canonical, noindex, duplicate handling.
3. Metadata: title, description, title templates, per-page metadata.
4. Social previews: Open Graph and Twitter Card.
5. Structure: H1, headings, internal links.
6. Images: alt text, dimensions, load behavior.
7. Schema: JSON-LD, Article, Organization, WebSite, FAQPage, HowTo.
8. Internationalization: hreflang only when real alternate pages exist.
9. Private areas: auth, billing, dashboards, account pages excluded from indexing.

## Technical SEO Verification

Use the lightest reliable check:

- Inspect rendered HTML for metadata and schema.
- Fetch sitemap and robots output.
- Use Rich Results Test or Schema Markup Validator for structured data.
- Use a social preview debugger for OG/Twitter cards.
- Use GSC URL Inspection for important live pages.
- Use a crawler for site-wide issues.

## Completion Standard

For each technical issue, record:

- Page or template affected.
- What was wrong.
- What changed.
- How it was verified.
- Whether follow-up is needed.
