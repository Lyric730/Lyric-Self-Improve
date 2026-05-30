# Three-Minute Future Date And Dedup Design

## Goal

Make `三分钟未来` support two production rhythms without repeated topics:

- Regular daily issue: publish on `publishDate`, cover `contentDate = publishDate - 1 day`.
- Same-day extra issue: publish on `publishDate`, cover `contentDate = publishDate`, excluding everything already published.

## Terms

- `publishDate`: the date shown on the page and used in the output folder.
- `contentDate`: the news window used for source collection.
- `published ledger`: a persistent record of items already used by the channel.

Example:

```text
2026-05-24 第 002 期
publishDate = 2026-05-24
contentDate = 2026-05-24
mode = same-day-incremental
```

```text
2026-05-25 第 003 期
publishDate = 2026-05-25
contentDate = 2026-05-24
mode = regular
```

## Default Schedule

The default production mode is `regular`.

When the user runs:

```powershell
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3
```

the pipeline should use:

```text
publishDate = 2026-05-25
contentDate = 2026-05-24
```

This gives a full 24-hour information window.

## Same-Day Incremental Mode

When the user wants an extra same-day issue:

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24
```

the pipeline should:

- only collect items dated `2026-05-24`;
- filter out items already in the published ledger;
- accept that the candidate pool may be smaller than a regular issue;
- prefer 5-6 strong items over padding to 8 weak ones.

## Dedup Rules

Before selection, each candidate is compared with the ledger.

Hard duplicate:

- same normalized URL;
- same source URL after redirects;
- same normalized title.

Topic duplicate:

- title tokens overlap with a published item strongly enough;
- same topic cluster, such as `starbucks-ai-inventory`, `ai-layoffs`, `robot-phone`, `deepseek-hardware`, `ai-healthcare`, `ai-oscar`;
- same image file or same image source URL.

Topic duplicates should be excluded by default and recorded in `filtered-published.json` so the user can audit what was removed.

## Ledger Location

Mutable production state should not live inside `lines/`.

Use:

```text
daily/_state/three-minute-future/published-ledger.json
```

Each entry should include:

```json
{
  "line": "three-minute-future",
  "publishDate": "2026-05-23",
  "contentDate": "2026-05-23",
  "vol": 1,
  "title": "AI 比人工更贵？",
  "sourceTitle": "微软称，使用人工智能的成本高于支付人工工资",
  "url": "https://example.com/source",
  "source": "Hacker News / Fortune",
  "topicKey": "ai-cost-labor",
  "imageKey": "asset-hash-or-source-url"
}
```

## Pipeline Behavior

Fetch stage:

- use `contentDate`, not `publishDate`, for source filtering;
- strict date filtering for Google News RSS;
- AIHot can include timezone-aware items whose local date equals `contentDate`.

Selection stage:

- read the ledger by default;
- remove duplicates before scoring;
- keep a debug output of removed candidates;
- do not fill missing slots with no-reality-tag items unless the user explicitly allows weak filler.

Publishing stage:

- do not automatically mark a draft as published during `--stop-after select`;
- after final PNG export and user approval, record selected items into the ledger with a dedicated command.

## Commands

Regular daily issue:

```powershell
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3
```

Same-day incremental issue:

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24
```

Mark approved issue as published:

```powershell
python lines\three-minute-future\mark_published.py 2026-05-24 --vol 2
```

Audit duplicates removed from a run:

```text
daily/<publishDate>/three-minute-future/work/filtered-published.json
```

## Acceptance Criteria

- Running a regular issue for `2026-05-25` defaults to `contentDate=2026-05-24`.
- Running a same-day issue can explicitly set `contentDate=2026-05-24`.
- Selection excludes items from prior published issues.
- The pipeline records excluded duplicates for review.
- The first `2026-05-23` issue can be imported into the ledger so `2026-05-24` same-day content does not repeat it.
