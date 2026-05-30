---
name: future-career-job-search
description: Use when helping a user choose a career direction, research real job-market requirements, extract atomic abilities from resumes/projects, compare gaps, and produce both a learning/project补强 plan and a resume/project rewrite plan. Especially useful for AI PM, product, growth, and solo-op career planning.
---

# Future Career Job Search

## Core Rule

Do not start by rewriting the resume. Follow this order:

1. Direction diagnosis, or accept a user-specified direction.
2. Market and JD research for that direction.
3. User atomic ability extraction from resume and project files.
4. Gap planning with learning resources and补强 projects.
5. Resume/project rewrite plan based on the same JD evidence.

Steps 4 and 5 must be produced together as two parallel plans.

## Step 1: Direction

If the user already names a direction, record it and continue to JD research.

If the user is unsure, run a diagnostic with these dimensions:

- interest
- existing transferable ability
- learning cost
- portfolio feasibility in 4-8 weeks
- job-market opportunity
- risk from degree, years, or hard technical requirements

Output: `career-direction-diagnosis.md`

Include:

- recommended main line
- secondary line
- directions to pause or avoid
- reasons and risks

## Step 2: Market And JD Research

Use real current job information. Prefer official company hiring pages. Use Boss, Liepin, Maimai, LinkedIn, Anysearch, or search engines only as supplement/fallback.

Must output:

- `target-company-role-map.md`
- `jd-corpus.md`
- `role-coverage-index.md`
- `jd-requirement-frequency.md`
- `project-requirement-index.md`

Rules:

- Cite source links and fetch dates.
- Count only explicit JD requirement lines, not job titles.
- Mark source confidence.
- Say "没查到" when not found.
- Do not fabricate URLs, course links, or company openings.

Cluster requirements into:

- industry / user / scenario understanding
- product planning / requirement analysis / UX
- data analysis / metrics / experiments
- AI / LLM / Agent / RAG / Prompt
- engineering understanding / API / data structure / SQL / Python
- evaluation / quality / safety / risk
- growth / content / commercialization
- communication / project execution
- degree / years / internship limits

## Step 3: Atomic Ability Extraction

Inputs:

- resume
- user-specified project folders
- README / SOP / docs
- run artifacts, screenshots, logs, demos, publish results
- user clarification on personal contribution and confidentiality

Atomic ability format:

```text
ability = action + scenario + method/tool + result/evidence
```

Output: `user-atomic-ability-map.md`

Include:

- project list
- atomic abilities per project
- evidence path or source
- evidence strength: strong / medium / weak
- whether it belongs in resume
- what proof is missing

Rules:

- Prioritize recent real projects.
- Treat old experiences as raw ability material, not automatic main selling points.
- Do not overstate AI involvement.
- Do not present AI/Codex-assisted implementation as fully independent engineering.
- Do not copy private contact information.

## Step 4A: Learning And Ability Gap Plan

Compare JD requirements with user atomic abilities.

Output: `ability-gap-learning-roadmap.md`

Include:

- core gaps
- what to learn
- direct course/resource links
- project补强 tasks
- expected evidence after completion
- 4-8 week priority

Resource rules:

- Browse current resources when recommending courses.
- Prefer official docs, university open courses, high-quality platform courses, and open-source tutorials.
- Explain each resource's purpose.
- Avoid generic advice like "learn machine learning".

Project补强 rules:

Every project must define:

- target role capability
- user task
- data source
- core features
- tools/tech
- evaluation method
- portfolio output

## Step 4B: Resume And Project Rewrite Plan

Output: `resume-project-rewrite-plan.md`

Include:

- resume positioning line
- target role labels
- project ordering
- which projects to expand, compress, or omit
- rewritten bullets
- project evidence to补
- 30-second and 2-minute interview story
- risky claims and likely follow-up questions

## Step 5: Final Action Plan

Output: `career-action-plan.md`

Include:

1. target direction
2. target role range
3. target companies
4. core JD requirements
5. user atomic ability profile
6. gaps
7. learning/project补强 plan
8. resume/project rewrite plan
9. application priority
10. next review checkpoint

## Boundaries

Do not:

- rewrite resumes before JD evidence
- give learning plans before direction and market research
- use generic personality tests as the decision basis
- force old projects into the current main narrative
- fabricate job, company, or course links
- treat a small JD sample as the whole market

Always:

- decide direction first
- collect real JD evidence second
- extract user atomic abilities third
- then output both ability补强 and material rewrite plans
- keep reusable outputs in files
