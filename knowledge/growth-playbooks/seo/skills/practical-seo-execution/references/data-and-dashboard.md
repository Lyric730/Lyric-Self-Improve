# Data And Dashboard Reference

Use this reference when setting up SEO measurement for an early product site.

## GSC Setup

Check whether a Google Search Console property already exists before creating a new one.

If an owner exists, ask them to add the working account as Owner in `Settings > Users and permissions`. If no property exists, create a URL-prefix property and verify with the simplest available method, often HTML file verification.

Submit the sitemap from the property UI:

- Open `Sitemaps`.
- Enter only `sitemap.xml` when the site root is already selected.
- Confirm status is `Success`.
- Confirm discovered URLs is greater than zero when the site has public pages.

Capture these baseline screens or notes:

- Sitemap status.
- Pages / Coverage status.
- Performance / Search results baseline.

Zero clicks or zero impressions can be normal for a new site. The setup is still valid if verification, sitemap submission, and page coverage are visible.

## Bing Webmaster

Prefer importing from GSC:

- Use the same Google account.
- Let Bing create the site property.
- Reuse verification.
- Pull the sitemap automatically.

Bing matters beyond direct Bing traffic because some AI search surfaces can be influenced by Bing indexing.

## GA4 Events

Use snake_case event names and parameter names. Do not send PII such as email, name, phone, IP address, street address, or payment data.

Recommended event layers:

| Layer | Purpose | Example Events |
|---|---|---|
| Conversion | Business outcomes | `auth_register_complete`, `agent_instantiated`, `purchase` |
| Funnel | Key user actions | `pricing_view`, `store_card_click`, `product_view`, `cta_click` |
| Diagnostic | UX and engagement | `scroll_depth`, `message_sent`, `form_error` |

Mark core business events as conversions or key events. Validate new events in DebugView or Realtime before relying on reports.

## UTM Rules

Use UTM only on external links. Do not add UTM to internal navigation.

Format:

```text
https://example.com/path?utm_source=<site>&utm_medium=<channel>&utm_campaign=<content>
```

Rules:

- Use lowercase ASCII.
- Use hyphens between words.
- `utm_source` is the specific site or platform.
- `utm_medium` is the channel type.
- `utm_campaign` is the campaign, content, or submission name.

Suggested `utm_medium` values:

- `directory`
- `community`
- `guest-post`
- `ai-search`
- `email`
- `social`
- `podcast`
- `cpc`
- `display`

Before publishing a tracked link, open it in an incognito window and confirm GA4 Realtime sees the visit with the expected source/medium.

## Looker Studio Dashboard

Build six widgets.

### Organic Funnel

Purpose: show whether organic users move from page views to key pages and conversion.

Suggested funnel:

1. `page_view`
2. `page_view` filtered by key commercial or product pages.
3. Primary conversion event, such as `auth_register_complete`.

Filter:

- `Session default channel group` contains `Organic Search`.

### Acquisition By UTM Medium

Dimension:

- `Session medium`

Metrics:

- `Sessions`
- `Key events` filtered to the main conversion.

Sort by Sessions descending.

### Landing Page Performance

Dimension:

- `Landing page + query string`

Metrics:

- `Users` or `Active users`
- `Average engagement time per session`
- `Key events`

Sort by Users descending. Show Top 20 by default.

### Top Queries From GSC

Data source:

- Search Console

Dimension:

- `Query`

Metrics:

- `Impressions`
- `Clicks`
- `Average position`

Sort by Impressions descending. Empty early data is acceptable.

### Event Count Trend

Chart:

- Time series

Dimension:

- `Event name`

Metric:

- `Event count`

Filter to key events so noise does not overwhelm the chart.

### Purchase Revenue

Chart:

- Table

Dimension:

- `Item name`, plan, product, or equivalent.

Metrics:

- `Purchase revenue`
- `Ecommerce purchases`

Filter:

- `Event name` equals `purchase`.

## Measurement Done Criteria

- GSC property verified.
- Sitemap submitted successfully.
- Bing imported or verified.
- GA4 Realtime sees key events.
- UTM test click appears in analytics.
- Dashboard widgets have correct dimensions, metrics, filters, and data sources.
