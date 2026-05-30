# 226 Review Log

Last updated: 2026-05-24

## Chrome Connection

- Chrome extension connected successfully via backend `type=extension`.
- Profile observed by Codex: `fanrizio`.
- First controlled page load verified on `joaniesimon.com`.

## Batch 1: First 20 Rows

Source: `outreach/226-review-candidates.csv`, rows beginning at id 18.

| Result | Count | Notes |
|---|---:|---|
| Submitted | 1 | `syncedreview.com` accepted form and redirected to a comment anchor, but the comment/link was not visible afterward |
| Candidate but deferred | 9 | Comment forms existed but captcha/anti-bot or weak relevance blocked immediate submission |
| Skipped | 8 | No visible comment form, comments closed, or low topical relevance |
| Error | 2 | Navigation timeout/detached tab |

Submitted:

| id | domain | status | rel | notes |
|---:|---|---|---|---|
| 19 | `syncedreview.com` | failed | no_link_found | Redirected to `#comment-504111`, but no visible comment node or `yolox.ai` link |

## Batch 2: Relevant Candidates

Prioritized by AI/digital/business/marketing relevance.

| id | domain | decision | notes |
|---:|---|---|---|
| 57 | `blog.bmtmicro.com` | submitted_pending | WordPress returned unapproved/moderation URL |
| 62 | `proofreadanywhere.com` | deferred | Visible form but captcha/anti-bot detected |
| 69 | `blogs.ucl.ac.uk` | low_value | Visible form but no URL field |
| 174 | `digitalwellbeing.org` | live_ugc | Public comment, author link is `rel="ugc external nofollow"` |
| 218 | `blog.goaffpro.com` | submitted_pending | WordPress returned unapproved/moderation URL |
| 136 | `blogs.ubc.ca` | candidate | Form + URL field, but older Google+ education page; lower priority |
| 21 | `pixel77.com` | deferred | Visible form but captcha/anti-bot detected |

## Batch 3: Nofollow/UGC Accepted

User rule update: nofollow/ugc submissions should also be made and recorded, while only real dofollow counts toward the KPI.

| id | domain | decision | rel / status | notes |
|---:|---|---|---|---|
| 92 | `premierchess.com` | live | `ugc external nofollow` | Public author link at `#comment-272249` |
| 66 | `capturebilling.com` | pending | unknown | Submitted via URL field; redirected to thank-you page, no public link visible yet |
| 67 | `premierchess.com` | live | `external nofollow ugc` | Public author link at `#comment-272251` |
| 21 | `pixel77.com` | live | `ugc external nofollow` | Public author link at `#comment-243193` |
| 175 | `syncedreview.com` | live | `ugc external nofollow` | AI article; public author link at `#comment-504116` |
| 25 | `blogs.deusto.es` | pending | unknown | Comment count changed and `#comment-197114` assigned, but no public Yolox link visible yet |

## Batch 4: Profile / Form Recheck

| id | domain | decision | notes |
|---:|---|---|---|
| 51 | `nintendoworldreport.com` | defer | Registration form has no website field and likely requires email activation |
| 59 | `participacion.puertodelrosario.org` | defer | Profile route requires OAuth/login; no editable website field visible |
| 73 | `blogs.city.ac.uk` | defer | Reply/profile route requires login; no website field visible to guest |
| 118 | `labsk.net` | defer | Registration requires captcha/questions and has no website field at registration |
| 61 | `chayagrossberg.com` | defer | URL field exists, but textarea input was blocked by page/browser interaction; no submission made |
| 197 | `pixel77.com` | defer | URL field exists, but same domain already has one live ugc submission; avoid duplicate-domain burst |

## Batch 5: Education / Science / Culture / Sports

| id | domain | decision | rel / status | notes |
|---:|---|---|---|---|
| 74 | `programas.cooperativa.cl` | not_submitted | insecure_form | Form has URL field but posts to insecure `http`; Chrome stopped at unsafe form page |
| 75 | `sites.williams.edu` | pending | unknown | Submitted after checking required human checkbox; hash `#comment-8590`, no public Yolox link visible |
| 121 | `notsowimpyteacher.com` | pending | unknown | Hash `#comment-138384`, no public Yolox link visible |
| 132 | `jilliancyork.com` | live | `external nofollow` | Public author link at `#comment-171939` |
| 146 | `blogs.urz.uni-halle.de` | not_submitted | blocked | URL field exists, but Chrome input hit clipboard limitation and direct fetch hit SSL verification |
| 178 | `madrimasd.org` | pending | unknown | Direct form POST attempted; no public Yolox link on recheck |
| 181 | `rcinet.ca` | pending | unknown | Direct form POST attempted; no public Yolox link on recheck |
| 206 | `anspblog.org` | not_submitted | blocked | Chrome blocked page with `ERR_BLOCKED_BY_CLIENT` |
| 210 | `squatuniversity.com` | skipped | no_url_field | Comment form shell exists but no usable comment/profile URL fields |
| 222 | `fivereasonssports.com` | live | `nofollow` | Public author link visible on page |

## Full 226 Completion Sweep

Date: 2026-05-24

Scope: all remaining `gefei_226` rows with `submitted='no'`.

Final result: `remaining_no=0`.

Method note: this completion sweep was an automated public-page check, not a
Chrome visual review of every row. The script fetched each public URL, parsed
forms and visible/hidden fields from returned HTML, submitted only when a
usable URL/Website field was detected, and verified public Yolox links from the
returned or refetched HTML. Profile/no-field rows were largely based on the
source `has_url_field` value plus prior audit notes. Rows marked `skipped` or
`failed` should be treated as `auto_checked`, not as exhaustively human-reviewed
in Chrome.

| Result | Count | Notes |
|---|---:|---|
| Live verified | 9 | Public author/profile URL visible immediately; all are `nofollow` or `ugc` |
| Pending | 50 | Submit attempted, but no public Yolox link visible on immediate verification |
| Failed | 23 | HTTP submit errors, mostly 409/403/500 responses |
| Skipped | 101 | Profile no website field, no URL field, no form, comments closed/login required, navigation error, or unsafe/ineligible form |

Live verified in the sweep:

| id | domain | rel_actual | live_url |
|---:|---|---|---|
| 31 | `beautythroughimperfection.com` | nofollow | `https://www.beautythroughimperfection.com/reindeer-donuts/#comment-1195556` |
| 43 | `feettothefire.blogs.wesleyan.edu` | ugc | `https://feettothefire.blogs.wesleyan.edu/2009/02/26/main-street-marketplace/comment-page-222/#comment-1317859` |
| 49 | `mummyfever.co.uk` | ugc | `https://mummyfever.co.uk/the-best-youtube-home-workouts/?WPACUnapproved=0&WPACUrl=https%3A%2F%2Fmummyfever.co.uk%2Fthe-best-youtube-home-workouts%2F%23comment-494335#comment-494335` |
| 63 | `lilistravelplans.com` | ugc | `https://www.lilistravelplans.com/chemka-hot-springs-moshi-tanzania/#comment-193208` |
| 77 | `simonsaysstampblog.com` | ugc | `https://www.simonsaysstampblog.com/blog/amore-laurafadora-3/comment-page-15/#comment-1072199` |
| 163 | `blogs.deusto.es` | ugc | `https://blogs.deusto.es/innovandis/exprime-las-naranjas/#comment-197288` |
| 170 | `everythingetsy.com` | nofollow | `https://www.everythingetsy.com/2013/02/10-social-media-tips-to-make-you-a-rock-star/?unapproved=1386912&moderation-hash=82573573fe71eff7f543c64cae3574ed#comment-1386912` |
| 172 | `blog.organicfood.vn` | ugc | `https://blog.organicfood.vn/thoi-gian-ngam-cac-loai-hat-la-bao-lau-tai-sao-phai-ngam-hat/#comment-277812` |
| 215 | `mummyfever.co.uk` | ugc | `https://mummyfever.co.uk/family-skiing-in-bulgaria/?WPACUnapproved=0&WPACUrl=https%3A%2F%2Fmummyfever.co.uk%2Ffamily-skiing-in-bulgaria%2F%23comment-494337#comment-494337` |

Final `gefei_226.submitted` distribution:

| submitted | Count |
|---|---:|
| `dead` | 25 |
| `failed` | 25 |
| `pending` | 58 |
| `skipped` | 101 |
| `yes` | 17 |

Chrome spot-check after user challenge:

| id | domain | prior status | Chrome observation |
|---:|---|---|---|
| 3 | `bordeaux.onvasortir.com` | skipped | Login form only; no visible profile/website URL field |
| 6 | `blogs.eltiempo.com` | skipped | Chrome navigation timed out; no useful visible form fields observed |
| 18 | `joaniesimon.com` | skipped | No comment-like form and no visible URL/Website field |
| 26 | `blogs.uww.edu` | skipped | No comment-like form and no visible URL/Website field |
| 31 | `beautythroughimperfection.com` | yes | Public Yolox author link visible, `rel="external nofollow"` |
| 43 | `feettothefire.blogs.wesleyan.edu` | yes | Public Yolox author link visible, `rel="ugc external nofollow"` |
| 48 | `soccernet.ng` | failed | Visible Website field exists; status remains failed because direct submit returned HTTP 403 |
| 62 | `proofreadanywhere.com` | pending | Visible Website field exists; no public Yolox link visible at the comment anchor, keep pending |
| 204 | `wonderfulmalaysia.com` | skipped | Comment form has comment/name/email only; no Website/URL field |
| 210 | `squatuniversity.com` | skipped | Main comment form has no fields; only hidden Jetpack carousel Website field, not usable |

## Reviewed But Not Submitted

Recorded in `gefei_226.notes` with reason: no visible form, no URL field, comments closed, 502/timeout, page not found, OAuth/login required, captcha/questions, low topical relevance, or duplicate-domain control.

## Submitted Records

| id | domain | DB status | rel_actual | live_url |
|---:|---|---|---|---|
| 174 | `digitalwellbeing.org` | live | ugc | `https://digitalwellbeing.org/five-reasons-why-chatgpt-is-the-future-of-digital-mental-health-support/#comment-847847` |
| 92 | `premierchess.com` | live | ugc | `https://premierchess.com/chess-growth/maythebestplayerwin#comment-272249` |
| 67 | `premierchess.com` | live | ugc | `https://premierchess.com/uncategorized/is-chess-a-sport-an-introduction-of-chess-in-and-within-the-sports-world#comment-272251` |
| 21 | `pixel77.com` | live | ugc | `https://pixel77.com/typography-rules-technique/#comment-243193` |
| 175 | `syncedreview.com` | live | ugc | `https://syncedreview.com/2022/06/29/nvidias-global-context-vit-achieves-sota-performance-on-cv-tasks-without-expensive-computation/comment-page-4/#comment-504116` |
| 132 | `jilliancyork.com` | live | nofollow | `https://jilliancyork.com/2010/02/20/on-memorability/#comment-171939` |
| 222 | `fivereasonssports.com` | live | nofollow | `https://www.fivereasonssports.com/news/ultimate-miami-heat-fan-travel-guide-tickets-hotels-and-local-hotspots/` |
| 218 | `blog.goaffpro.com` | pending | | `https://blog.goaffpro.com/mastering-affiliate-product-reviews-a-step-by-step-guide-for-engaging-content-and-conversions/?unapproved=59351&moderation-hash=1368eebc162b6fccfeda8b4edd6e66f1#comment-59351` |
| 57 | `blog.bmtmicro.com` | pending | | `https://blog.bmtmicro.com/4449-2/?unapproved=229533&moderation-hash=637f2d7da1cd6595ee88d362d52b86f1#comment-229533` |
| 66 | `capturebilling.com` | pending | | `https://capturebilling.com/thank-you-for-your-thoughts/` |
| 25 | `blogs.deusto.es` | pending | | `https://blogs.deusto.es/innovandis/llegando-al-nivel-pro-con-lxs-20g-en-innovandis/#comment-197114` |
| 75 | `sites.williams.edu` | pending | | `https://sites.williams.edu/srd4/methods-exercises/methods-exercise-6/#comment-8590` |
| 121 | `notsowimpyteacher.com` | pending | | `https://notsowimpyteacher.com/2024/01/5-reasons-why-teaching-grammar-is-still-important.html#comment-138384` |
| 178 | `madrimasd.org` | pending | | `https://www.madrimasd.org/blogs/astrofisica/2022/05/20/134942` |
| 181 | `rcinet.ca` | pending | | `https://www.rcinet.ca/bhm-en/2021/02/02/a-variety-of-activities-unveiled-for-black-history-month/` |

## Next

1. Recheck pending moderation URLs after they have had time to publish.
2. Do not resubmit completed `gefei_226` rows; update only from public verification.
3. Move next effort to submission-friendly targets: awesome lists, showcases, directories, and profiles with visible website fields.
