# Submission Templates

Use these templates by substituting values from the product profile. Do not hardcode the example product or reuse wording that conflicts with `forbidden_phrases`.

## Product Profile Fields

| profile key | used for |
|---|---|
| `brand_name` | product/tool/company name |
| `canonical_url` | website field and naked URL mentions |
| `target_domain` | verification target |
| `positioning` | concise category, e.g. "AI writing assistant" |
| `audience` | who the product serves |
| `one_liner` | tight directory tagline |
| `short_description` | most product forms |
| `long_description` | long directory/classified forms |
| `categories` | category dropdowns |
| `tags` | tag fields |
| `submitter_name` | submitter/contact name |
| `contact_email` | account/listing email |
| `hq_country` / `hq_city` | forced HQ fields |
| `assets` | screenshots, logos, PDF, public screenshot URL |
| `forbidden_phrases` | phrases to avoid |

## Short Description

```text
[brand_name] is a [positioning] for [audience]. It helps users [primary outcome].
```

If the product profile has `short_description`, prefer that exact value.

## Description With URL

Use when no website field exists but a public description/bio field supports text:

```text
[brand_name] is a [positioning] for [audience]. [short_description]

Website: [canonical_url]
```

## GitHub Awesome List Entry

Adapt to the list's style:

```markdown
- [brand_name](canonical_url) - [one_liner]
```

## Blog Comment Style

Use the website field for the URL. Do not paste generic praise.

Pattern:

```text
The section about [specific point] is useful because [specific reason]. I have seen the same issue when [audience] try to [related workflow]. The practical takeaway for me is [specific takeaway].
```

## Profile Bio

```text
Building [brand_name], a [positioning] for [audience].
```

```text
Working on [brand_name]: [one_liner]
```

## Classified Body

```text
[brand_name] is a [positioning] for [audience].

[long_description]

Website: [canonical_url]
```

## Email Outreach Low-Priority Template

Use only after self-serve submissions are exhausted.

```text
Subject: Possible fit for your [topic] list

Hi [Name],

I found your article on [topic] and thought [brand_name] might be a useful addition if you update the list.

[brand_name] is a [positioning] for [audience]. [short_description]

URL: [canonical_url]

No pressure either way. I just wanted to send it over in case it fits your next refresh.

Best,
[submitter_name]
```
