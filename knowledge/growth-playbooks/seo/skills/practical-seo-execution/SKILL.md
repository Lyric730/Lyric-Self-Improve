---
name: practical-seo-execution
description: Practical SEO execution for early product sites. Use when Codex needs to set up search/analytics dashboards, mine keywords, create SEO blog briefs or articles, build backlink workflows, manage backlink status data, or run technical SEO audits without relying on project-specific local files.
---

# Practical SEO Execution

## Overview

Use this skill to turn SEO work into concrete execution artifacts: dashboards, keyword maps, blog briefs, backlink trackers, and technical SEO fixes. Keep the work practical. Do not invent publishing calendars, retrospective rituals, or strategy decks unless the user explicitly asks.

## Operating Rules

- Start from the user's site, product, ICP, current analytics access, and existing content.
- Prefer observable evidence: GSC data, SERP results, community questions, backlink pages, code output, and public HTML.
- Keep outputs actionable: tables, checklists, briefs, database fields, and specific next actions.
- Do not require local source files. If the user provides project-specific docs, extract reusable rules and rewrite paths as placeholders.
- Avoid vague SEO advice. Tie every recommendation to a task, input, output, or validation step.

## Workflow

### 1. Scope The SEO Task

Identify which lane the user is asking for:

- Measurement setup: GSC, Bing Webmaster, GA4, UTM, Looker Studio.
- Keyword research: seed terms, expansion, scoring, pillar/cluster, outlines.
- Blog production: brief, evidence pool, draft, links, publish checks.
- Backlinks: prospect pool, submission, rel verification, tracker/reporting.
- Technical SEO: sitemap, robots, metadata, OG, schema, alt, hreflang.

If multiple lanes are requested, execute in this order: measurement, keyword, blog, backlinks, technical SEO. For bug-like technical tasks, fix the technical blocker first.

### 2. Build Measurement First

Use measurement work to catch signals before content or backlink work scales.

Read `references/data-and-dashboard.md` when you need exact setup details for:

- GSC and Bing Webmaster.
- GA4 event naming and conversion events.
- UTM conventions.
- A 6-widget Looker Studio dashboard.

Core deliverables:

- Search Console property and sitemap checklist.
- GA4 event map.
- UTM naming table.
- Dashboard spec or implementation notes.

### 3. Mine Keywords From Evidence

Do not rely on model-generated keyword lists alone. Build from product functions, ICP pain, competitor/comparison intent, emerging search topics, communities, PAA, and keyword tools.

Read `references/keyword-and-blog.md` when doing keyword work. Use `assets/keyword-research-brief.md` as the handoff format.

Core deliverables:

- Seed keyword list.
- Expanded keyword pool.
- Scored keyword map with Tier 1, Tier 1.5, Tier 2, Tier 3, Negative.
- Pillar/cluster map.
- Blog-ready outline candidates.

### 4. Turn Keywords Into Blog Assets

Every article needs a brief before drafting. The brief must include keywords, ICP, search intent, article type, angle, evidence, internal links, product links, authority links, and SEO metadata.

Read `references/keyword-and-blog.md` for article type selection, evidence standards, AEO writing, and publish checks. Use `assets/blog-brief-template.md` for reusable briefs.

Core deliverables:

- Blog brief.
- Draft or outline.
- Internal/external link plan.
- Publish checklist result.

### 5. Build Backlinks As A Pipeline

Treat backlinks as tracked submissions, not ad hoc outreach. Count only public, verified `live` + `dofollow` links as the hard SEO KPI.

Read `references/backlinks-and-technical.md` for prospect sources, submission types, rel verification, and tracker schemas. Use `assets/backlink-tracker.csv` as a portable tracker.

Core deliverables:

- Prospect list.
- Submission status table.
- Public evidence URL for each live link.
- Summary of dofollow, nofollow/ugc, pending, rejected, failed, skipped.

### 6. Fix Technical SEO With Verification

Audit before changing. For each issue, identify the page/template/code owner, make a focused fix, and verify page output or search-tool validation.

Read `references/backlinks-and-technical.md` for the technical checklist. Use `assets/technical-seo-audit-checklist.md` as the working audit file.

Core deliverables:

- Technical SEO issue list.
- Fix notes tied to files/pages.
- Verification evidence: rendered HTML, sitemap/robots output, rich result/schema validation, social preview check, or GSC URL inspection.

## Resource Routing

- `references/data-and-dashboard.md`: load for analytics, events, UTM, and dashboard tasks.
- `references/keyword-and-blog.md`: load for keyword research, topic selection, SEO/AEO writing, blog briefs, and publishing checks.
- `references/backlinks-and-technical.md`: load for backlink systems, status fields, rel verification, and technical SEO audits.
- `assets/keyword-research-brief.md`: copy when handing off keyword research.
- `assets/blog-brief-template.md`: copy when preparing an article.
- `assets/backlink-tracker.csv`: copy when starting backlink tracking in a spreadsheet or database.
- `assets/technical-seo-audit-checklist.md`: copy when auditing a site.

## Completion Check

Before claiming done, verify:

- The output does not depend on hidden local files or absolute local paths.
- Every recommendation maps to a concrete SEO action.
- Keyword and blog outputs include evidence sources or clear placeholders for sources.
- Backlink outputs distinguish dofollow from nofollow, ugc, sponsored, and rel-me links.
- Technical SEO outputs include a validation method, not just a fix suggestion.
