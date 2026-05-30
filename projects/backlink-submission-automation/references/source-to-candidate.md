# Source To Candidate Pipeline

Use this reference when building or refreshing the candidate pool.

## Candidate Sources

| source | use for | notes |
|---|---|---|
| `lxx_ai` | bulk directory/profile/classified candidates | Requires access/invite on LXX; for new users, use the team's exported `candidate-packs/lxx-ai.csv` once available. |
| `ahrefs` | competitor backlink reverse engineering | Best for discovering repeatable platforms and high-authority lists. |
| `github` | awesome lists and PR-based directories | High DR, often real dofollow after merge. |
| `serper` | Google result mining | Useful for "submit AI tool", "list your startup", country-specific directories. |
| `legacy_226` | old blog comment/profile pool | Re-audit; do not blindly bulk-run. |
| `manual` | user-supplied URL | Inspect immediately and record decision. |

## Minimum Candidate CSV

```csv
domain,url,dr,category,source,submission_type,priority,relevance_score,evidence_score,notes
aiai.tools,https://aiai.tools/submit-ai-tool,31,AI directory,lxx_ai,directory,40,20,10,has form
github.com,https://github.com/org/repo,97,awesome list,manual,github_pr,80,25,15,needs PR
```

`relevance_score` and `evidence_score` are optional. If missing, `import_candidates.py` defaults them to 0 and `next_candidates.py` computes additional relevance from the campaign profile.

## After Profile Completion

Ask the user to choose one path:

1. **Import their own source**: CSV, folder, existing DB, Ahrefs export, GitHub list, or legacy pool.
2. **Use prepared packs**: import `candidate-packs/starter-pack.csv` or the team's exported packs such as `candidate-packs/lxx-ai.csv`.

Do not require new users to have an LXX invite/code. If they do not have access, use the bundled/team-exported candidate pack.

## Candidate Pack Distribution

Candidate packs live inside the skill folder:

```text
backlink-submission-automation/
  candidate-packs/
    manifest.json
    starter-pack.csv
    lxx-ai.csv
    ahrefs-competitor-backlinks.csv
    legacy-226-review.csv
```

This means users get the packs when they install the skill by Git clone, ZIP download, or copying the full folder into `CODEX_HOME/skills`. The pack is not tied to the original operator's machine.

Read `candidate-packs/manifest.json` before importing. It records row counts, source notes, and the exact import command for each CSV.

Current bundled pack roles:

| pack | use | execution rule |
|---|---|---|
| `starter-pack.csv` | smoke test and small first run | safe to import first; selection filters still apply |
| `lxx-ai.csv` | self-serve directories/profiles/classified candidates | highest practical execution pack; still inspect every form |
| `ahrefs-competitor-backlinks.csv` | competitor backlink research | submit only if the route is clearly allowed/actionable |
| `legacy-226-review.csv` | old blog-comment URLs with prior URL-field signal | browser re-audit is mandatory; many rows may still be skipped |

Refresh packs manually. Do not run a normal campaign flow that writes back into bundled candidate packs. The bundled CSVs are source assets, not runtime output.

If the team later exports a larger LXX/source file, replace the target CSV intentionally and keep the same columns. Never overwrite a bundled CSV with a zero-row export.

Useful SQL for exporting from a canonical campaign DB:

```sql
SELECT source_id, source, domain, url, dr, traffic, category,
       submission_type, priority, relevance_score, evidence_score, notes
FROM candidates
WHERE status IN ('new', 'queued')
  AND (dr IS NULL OR dr >= 20)
ORDER BY priority DESC, relevance_score DESC, evidence_score DESC, COALESCE(dr, 0) DESC;
```

Import:

```bash
python skills/backlink-submission-automation/scripts/import_candidates.py \
  --db data/backlinks.db \
  --csv data/candidates.csv \
  --source lxx_ai
```

## Filtering Rules

Default filters:

1. Skip DR below the campaign minimum from the product profile unless the user overrides it.
2. Skip obvious spam niches: casino, betting, loan, pharma, adult, hacked pages, parked domains.
3. Hold flagship manual-launch sites such as Product Hunt, Hacker News launch posts, G2/Capterra-style review platforms, and any site the user explicitly reserves.
4. Skip direct competitors' owned blogs unless the route is clearly allowed and useful.
5. Prioritize self-serve, low-friction, public pages over email outreach.
6. Prefer pages that can render a real public `<a href>` to the target URL.
7. Prefer topical/category relevance over raw DR when DR is close.

## Scoring Heuristic

Assign priority using this rough model:

```text
priority =
  DR bucket
  + submission path confidence
  + relevance
  + evidence of existing outbound dofollow samples
  - friction
  - risk
```

Suggested buckets:

- DR 90+: `+50`
- DR 70-89: `+35`
- DR 40-69: `+20`
- DR 20-39: `+10`
- DR below threshold: skip

Path confidence:

- visible "submit/list your tool/product/startup": `+25`
- GitHub list with matching category: `+25`
- public profile website field: `+15`
- public description/bio with rendered links: `+10`
- email-only outreach: `-20`
- CAPTCHA/account approval required: `-15`

## Legacy 226 Pool

Do not assume previous audit labels are final. For each legacy URL:

1. Open the page yourself.
2. Scroll to comments/profile/footer.
3. Check form availability and URL/website field.
4. Check existing author/profile links for rel samples.
5. Submit only if the page still has a real form or profile route.
6. Record closed comments, missing URL fields, login limits, 403/409/500, and no-form pages as skipped/failed with evidence.

## Ahrefs Reverse Engineering

Group competitor backlinks by domain. High-value domains are those appearing across multiple competitors.

Good outcomes:

- GitHub awesome list PRs.
- Showcase forms.
- Tool directories with self-serve submission.
- Documentation/tutorial pages where a product reference is natural.

Weak outcomes:

- competitor-owned blogs.
- generic review articles that require email only.
- Wikipedia or app stores where the product is not eligible yet.

## Manual Hold List

Keep these out of automation unless explicitly approved:

- Product Hunt launch.
- Hacker News Show HN.
- G2, Capterra, Trustpilot, review platforms requiring real customer review flow.
- Paid advertorials.
- Any site requiring misleading identity or fake review claims.

Record as `skipped_manual_hold`, not `failed`.
