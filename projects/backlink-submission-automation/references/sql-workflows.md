# SQL Workflows

Use this reference for database setup, candidate import, submission recording, error escalation, and reporting. Prefer these SQL snippets over Python scripts unless the operation needs browser interaction or deterministic HTML parsing.

Replace placeholder values such as `<campaign-slug>`, `<csv-path>`, `<brand-name>`, and `<target-url>` before running.

## Run SQL

PowerShell:

```powershell
@'
-- paste SQL here
'@ | sqlite3 "campaigns\<campaign-slug>\data\backlinks.db"
```

If `sqlite3` CLI is unavailable, use Python's standard library:

```powershell
$env:BACKLINK_DB = "campaigns\<campaign-slug>\data\backlinks.db"
@'
-- paste SQL here
'@ | python -c "import os, sqlite3, sys; conn=sqlite3.connect(os.environ['BACKLINK_DB']); conn.executescript(sys.stdin.read()); conn.commit(); conn.close()"
```

Bash:

```bash
sqlite3 "campaigns/<campaign-slug>/data/backlinks.db" <<'SQL'
-- paste SQL here
SQL
```

Python fallback:

```bash
BACKLINK_DB="campaigns/<campaign-slug>/data/backlinks.db" python -c 'import os, sqlite3, sys; conn=sqlite3.connect(os.environ["BACKLINK_DB"]); conn.executescript(sys.stdin.read()); conn.commit(); conn.close()' <<'SQL'
-- paste SQL here
SQL
```

## Bootstrap Schema

Run once for every new campaign DB. It is safe to run again.

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS campaign_profile (
  key TEXT PRIMARY KEY,
  value TEXT,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS candidates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT,
  source_id TEXT,
  domain TEXT NOT NULL,
  url TEXT NOT NULL,
  dr INTEGER,
  traffic INTEGER,
  category TEXT,
  submission_type TEXT DEFAULT 'unknown',
  priority INTEGER DEFAULT 0,
  relevance_score INTEGER DEFAULT 0,
  evidence_score INTEGER DEFAULT 0,
  status TEXT DEFAULT 'new',
  notes TEXT,
  discovered_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(source, url)
);

CREATE TABLE IF NOT EXISTS submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_table TEXT,
  source_id INTEGER,
  platform_domain TEXT,
  submit_url TEXT,
  target_url TEXT,
  anchor_text TEXT,
  submit_method TEXT DEFAULT 'browser',
  submit_time TEXT DEFAULT CURRENT_TIMESTAMP,
  status TEXT DEFAULT 'pending',
  rel_actual TEXT DEFAULT 'unknown',
  live_url TEXT,
  verification_evidence TEXT,
  verified_at TEXT,
  attempt_count INTEGER DEFAULT 0,
  last_error_signature TEXT,
  priority_tag TEXT,
  error_log TEXT,
  notes TEXT,
  CHECK (
    status NOT IN ('live', 'live_plain_text')
    OR (
      live_url IS NOT NULL AND length(trim(live_url)) > 0
      AND verification_evidence IS NOT NULL AND length(trim(verification_evidence)) > 0
    )
  ),
  CHECK (
    status <> 'live'
    OR rel_actual NOT IN ('unknown', 'no_link_found', 'pending_expected_dofollow', 'live_plain_text')
  ),
  CHECK (status <> 'live_plain_text' OR rel_actual = 'live_plain_text')
);

CREATE TABLE IF NOT EXISTS submission_attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  submission_id INTEGER,
  source_table TEXT,
  source_id INTEGER,
  platform_domain TEXT,
  attempt_no INTEGER,
  status TEXT,
  error_signature TEXT,
  error_message TEXT,
  notes TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS error_patterns (
  error_signature TEXT PRIMARY KEY,
  occurrence_count INTEGER DEFAULT 0,
  optimization_attempts INTEGER DEFAULT 0,
  status TEXT DEFAULT 'observed',
  priority_tag TEXT,
  first_seen TEXT DEFAULT CURRENT_TIMESTAMP,
  last_seen TEXT DEFAULT CURRENT_TIMESTAMP,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS account_credentials (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  platform_domain TEXT NOT NULL,
  account_email TEXT,
  username TEXT,
  password TEXT,
  auth_method TEXT,
  credential_status TEXT,
  source_submission_id INTEGER,
  live_url TEXT,
  notes TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(platform_domain, account_email, username)
);

CREATE TABLE IF NOT EXISTS target_pages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT UNIQUE,
  page_type TEXT,
  priority INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS anchor_texts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  anchor_text TEXT UNIQUE,
  type TEXT,
  use_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS spam_blacklist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain_pattern TEXT UNIQUE,
  reason TEXT,
  added_date TEXT DEFAULT CURRENT_DATE
);
```

## Migrate Existing DB

Run when a campaign DB was created by an older version of the skill.

```sql
ALTER TABLE candidates ADD COLUMN relevance_score INTEGER DEFAULT 0;
ALTER TABLE candidates ADD COLUMN evidence_score INTEGER DEFAULT 0;
ALTER TABLE submissions ADD COLUMN target_url TEXT;
ALTER TABLE submissions ADD COLUMN verification_evidence TEXT;
ALTER TABLE submissions ADD COLUMN verified_at TEXT;
ALTER TABLE submissions ADD COLUMN attempt_count INTEGER DEFAULT 0;
ALTER TABLE submissions ADD COLUMN last_error_signature TEXT;
ALTER TABLE submissions ADD COLUMN priority_tag TEXT;
```

If a column already exists, SQLite will print a duplicate-column error. That is not data loss; continue with the next statement.

## Live Write Guards

Use triggers so `live` cannot be written without public evidence.

```sql
CREATE TRIGGER IF NOT EXISTS guard_submissions_live_insert
BEFORE INSERT ON submissions
WHEN NEW.status IN ('live', 'live_plain_text')
  AND (
    NEW.live_url IS NULL OR length(trim(NEW.live_url)) = 0
    OR NEW.verification_evidence IS NULL OR length(trim(NEW.verification_evidence)) = 0
  )
BEGIN
  SELECT RAISE(ABORT, 'live status requires live_url and verification_evidence');
END;

CREATE TRIGGER IF NOT EXISTS guard_submissions_live_update
BEFORE UPDATE ON submissions
WHEN NEW.status IN ('live', 'live_plain_text')
  AND (
    NEW.live_url IS NULL OR length(trim(NEW.live_url)) = 0
    OR NEW.verification_evidence IS NULL OR length(trim(NEW.verification_evidence)) = 0
  )
BEGIN
  SELECT RAISE(ABORT, 'live status requires live_url and verification_evidence');
END;

CREATE TRIGGER IF NOT EXISTS guard_submissions_live_rel_insert
BEFORE INSERT ON submissions
WHEN NEW.status = 'live'
  AND NEW.rel_actual IN ('unknown', 'no_link_found', 'pending_expected_dofollow', 'live_plain_text')
BEGIN
  SELECT RAISE(ABORT, 'status=live requires a verified link rel');
END;

CREATE TRIGGER IF NOT EXISTS guard_submissions_live_rel_update
BEFORE UPDATE ON submissions
WHEN NEW.status = 'live'
  AND NEW.rel_actual IN ('unknown', 'no_link_found', 'pending_expected_dofollow', 'live_plain_text')
BEGIN
  SELECT RAISE(ABORT, 'status=live requires a verified link rel');
END;

CREATE TRIGGER IF NOT EXISTS guard_submissions_plain_text_insert
BEFORE INSERT ON submissions
WHEN NEW.status = 'live_plain_text' AND NEW.rel_actual <> 'live_plain_text'
BEGIN
  SELECT RAISE(ABORT, 'status=live_plain_text requires rel_actual=live_plain_text');
END;

CREATE TRIGGER IF NOT EXISTS guard_submissions_plain_text_update
BEFORE UPDATE ON submissions
WHEN NEW.status = 'live_plain_text' AND NEW.rel_actual <> 'live_plain_text'
BEGIN
  SELECT RAISE(ABORT, 'status=live_plain_text requires rel_actual=live_plain_text');
END;
```

## Seed Profile Basics

Insert the minimum profile values from `profile/profile.json` or the structured answers. Store JSON strings when the value is a list or object.

```sql
INSERT INTO campaign_profile(key, value) VALUES
  ('brand_name', '<brand-name>'),
  ('canonical_url', '<target-url>'),
  ('contact_email', '<contact-email>'),
  ('min_dr', '20')
ON CONFLICT(key) DO UPDATE SET
  value = excluded.value,
  updated_at = CURRENT_TIMESTAMP;

INSERT OR IGNORE INTO target_pages(url, page_type, priority)
VALUES ('<target-url>', 'home', 1);

INSERT OR IGNORE INTO anchor_texts(anchor_text, type)
VALUES
  ('<brand-name>', 'brand'),
  ('<target-url>', 'naked');

INSERT OR IGNORE INTO spam_blacklist(domain_pattern, reason)
VALUES
  ('*.lol', 'low-quality spam TLD pattern'),
  ('*casino*', 'spam niche'),
  ('*betting*', 'spam niche'),
  ('*loan*', 'spam niche'),
  ('*pharmacy*', 'spam niche'),
  ('*viagra*', 'spam niche'),
  ('backlink.*', 'backlink farm pattern'),
  ('*-backlinks.*', 'backlink farm pattern');
```

## Import Candidate CSV

The bundled packs use this normalized column order:

```text
id,source_id,source,domain,url,dr,traffic,category,submission_type,priority,notes
```

PowerShell example:

```powershell
@'
DROP TABLE IF EXISTS temp_candidate_import;
CREATE TABLE temp_candidate_import (
  id TEXT,
  source_id TEXT,
  source TEXT,
  domain TEXT,
  url TEXT,
  dr TEXT,
  traffic TEXT,
  category TEXT,
  submission_type TEXT,
  priority TEXT,
  notes TEXT
);
.mode csv
.import --skip 1 "skills/backlink-submission-automation/candidate-packs/lxx-ai.csv" temp_candidate_import

INSERT INTO candidates (
  source, source_id, domain, url, dr, traffic, category, submission_type,
  priority, relevance_score, evidence_score, status, notes
)
SELECT
  NULLIF(source, ''),
  NULLIF(source_id, ''),
  lower(replace(NULLIF(domain, ''), 'www.', '')),
  NULLIF(url, ''),
  CAST(NULLIF(dr, '') AS INTEGER),
  CAST(NULLIF(traffic, '') AS INTEGER),
  NULLIF(category, ''),
  COALESCE(NULLIF(submission_type, ''), 'unknown'),
  COALESCE(CAST(NULLIF(priority, '') AS INTEGER), 0),
  0,
  CASE
    WHEN lower(notes) LIKE '%dofollow%' THEN 15
    WHEN lower(notes) LIKE '%website field%' OR lower(notes) LIKE '%submit%' THEN 10
    ELSE 0
  END,
  'new',
  notes
FROM temp_candidate_import
WHERE NULLIF(domain, '') IS NOT NULL
  AND NULLIF(url, '') IS NOT NULL
ON CONFLICT(source, url) DO UPDATE SET
  dr = COALESCE(excluded.dr, candidates.dr),
  traffic = COALESCE(excluded.traffic, candidates.traffic),
  category = COALESCE(excluded.category, candidates.category),
  submission_type = COALESCE(excluded.submission_type, candidates.submission_type),
  priority = MAX(candidates.priority, excluded.priority),
  evidence_score = MAX(candidates.evidence_score, excluded.evidence_score),
  notes = CASE
    WHEN candidates.notes IS NULL OR candidates.notes = '' THEN excluded.notes
    WHEN excluded.notes IS NULL OR excluded.notes = '' THEN candidates.notes
    ELSE candidates.notes || char(10) || excluded.notes
  END,
  updated_at = CURRENT_TIMESTAMP;

DROP TABLE temp_candidate_import;
'@ | sqlite3 "campaigns\<campaign-slug>\data\backlinks.db"
```

If the machine does not have `sqlite3` CLI, use this inline Python importer instead of adding a package script:

```powershell
$env:BACKLINK_DB = "campaigns\<campaign-slug>\data\backlinks.db"
$env:CANDIDATE_CSV = "skills/backlink-submission-automation/candidate-packs/lxx-ai.csv"
@'
import csv, os, sqlite3

db = os.environ["BACKLINK_DB"]
csv_path = os.environ["CANDIDATE_CSV"]
conn = sqlite3.connect(db)
cur = conn.cursor()
with open(csv_path, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        domain = (row.get("domain") or "").lower().replace("www.", "").strip()
        url = (row.get("url") or "").strip()
        if not domain or not url:
            continue
        notes = row.get("notes") or ""
        notes_l = notes.lower()
        evidence = 15 if "dofollow" in notes_l else 10 if ("website field" in notes_l or "submit" in notes_l) else 0
        cur.execute(
            """
            INSERT INTO candidates (
              source, source_id, domain, url, dr, traffic, category, submission_type,
              priority, relevance_score, evidence_score, status, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, 'new', ?)
            ON CONFLICT(source, url) DO UPDATE SET
              dr = COALESCE(excluded.dr, candidates.dr),
              traffic = COALESCE(excluded.traffic, candidates.traffic),
              category = COALESCE(excluded.category, candidates.category),
              submission_type = COALESCE(excluded.submission_type, candidates.submission_type),
              priority = MAX(candidates.priority, excluded.priority),
              evidence_score = MAX(candidates.evidence_score, excluded.evidence_score),
              notes = CASE
                WHEN candidates.notes IS NULL OR candidates.notes = '' THEN excluded.notes
                WHEN excluded.notes IS NULL OR excluded.notes = '' THEN candidates.notes
                ELSE candidates.notes || char(10) || excluded.notes
              END,
              updated_at = CURRENT_TIMESTAMP
            """,
            (
                row.get("source") or None,
                row.get("source_id") or None,
                domain,
                url,
                int(row["dr"]) if row.get("dr") else None,
                int(row["traffic"]) if row.get("traffic") else None,
                row.get("category") or None,
                row.get("submission_type") or "unknown",
                int(row["priority"]) if row.get("priority") else 0,
                evidence,
                notes,
            ),
        )
conn.commit()
print("imported_or_updated_rows", conn.total_changes)
conn.close()
'@ | python -
```

## Select Next Candidates

Set `profile_terms` from the campaign profile. This query ranks by DR, stored priority, product relevance, public-link evidence, and friction/risk.

```sql
WITH profile_terms(term) AS (
  VALUES
    ('ai'),
    ('automation'),
    ('agent')
),
base AS (
  SELECT
    c.*,
    CASE
      WHEN c.dr >= 90 THEN 50
      WHEN c.dr >= 70 THEN 35
      WHEN c.dr >= 40 THEN 20
      WHEN c.dr >= CAST((SELECT COALESCE(value, '20') FROM campaign_profile WHERE key='min_dr') AS INTEGER) THEN 10
      ELSE -100
    END AS dr_score,
    CASE
      WHEN c.submission_type IN ('github_pr', 'directory', 'showcase') THEN 25
      WHEN c.submission_type IN ('profile', 'document', 'media') THEN 12
      WHEN c.submission_type = 'blog_comment' THEN 5
      ELSE -5
    END AS path_score,
    (
      SELECT MIN(COUNT(*) * 4, 24)
      FROM profile_terms pt
      WHERE lower(c.domain || ' ' || c.url || ' ' || COALESCE(c.category, '') || ' ' || COALESCE(c.notes, '')) LIKE '%' || lower(pt.term) || '%'
    ) AS dynamic_relevance,
    CASE
      WHEN lower(COALESCE(c.notes, '')) LIKE '%captcha%' THEN -15
      WHEN lower(COALESCE(c.notes, '')) LIKE '%manual_hold=true%' THEN -50
      WHEN lower(COALESCE(c.notes, '')) LIKE '%paid=true%' THEN -30
      ELSE 0
    END AS friction_score
  FROM candidates c
  WHERE c.status IN ('new', 'queued')
)
SELECT
  id,
  (COALESCE(priority, 0) + dr_score + path_score + COALESCE(relevance_score, 0)
   + COALESCE(evidence_score, 0) + dynamic_relevance + friction_score) AS score,
  COALESCE(dr, '') AS dr,
  domain,
  submission_type,
  url,
  notes
FROM base
WHERE dr_score > -100
ORDER BY score DESC, COALESCE(dr, 0) DESC, id ASC
LIMIT 10;
```

## Record Submitted Or Pending

Use this immediately after a form/PR/profile action is accepted but before public verification.

```sql
INSERT INTO submissions (
  source_table, source_id, platform_domain, submit_url, target_url,
  anchor_text, submit_method, status, rel_actual, live_url, notes
) VALUES (
  'candidates',
  123,
  'example.com',
  'https://example.com/submit',
  '<target-url>',
  '<anchor-text>',
  'browser',
  'pending_review',
  'unknown',
  'https://example.com/products/example-product',
  'Submitted free listing; waiting approval'
);

UPDATE candidates
SET status = 'submitted', updated_at = CURRENT_TIMESTAMP
WHERE id = 123;
```

## Record Live After Verification

Before writing `live`, the evidence must come from logged-out public HTML or rendered public DOM. The trigger guards above reject missing evidence.

```sql
UPDATE submissions
SET
  status = 'live',
  rel_actual = 'dofollow',
  live_url = 'https://example.com/products/example-product',
  verification_evidence = 'logged-out public HTML showed a[href*="<target-domain>"] with empty rel',
  verified_at = CURRENT_TIMESTAMP,
  notes = CASE
    WHEN notes IS NULL OR notes = '' THEN 'Verified dofollow public link'
    ELSE notes || char(10) || 'Verified dofollow public link'
  END
WHERE id = 123;

SELECT changes() AS updated_rows;
```

If the public page shows only plain text, use:

```sql
UPDATE submissions
SET
  status = 'live_plain_text',
  rel_actual = 'live_plain_text',
  live_url = 'https://example.com/products/example-product',
  verification_evidence = 'logged-out public DOM showed target URL text but no outbound anchor',
  verified_at = CURRENT_TIMESTAMP
WHERE id = 123;
```

## Record Account Credentials

Use a vault pointer in `password` unless local password storage was approved.

```sql
INSERT INTO account_credentials (
  platform_domain, account_email, username, password, auth_method,
  credential_status, source_submission_id, live_url, notes, updated_at
) VALUES (
  'example.com',
  'submit@example.com',
  'productname',
  'vault:Backlink/example.com',
  'email_password',
  'confirmed',
  123,
  'https://example.com/u/productname',
  'Created during directory submission',
  CURRENT_TIMESTAMP
)
ON CONFLICT(platform_domain, account_email, username) DO UPDATE SET
  password = excluded.password,
  auth_method = excluded.auth_method,
  credential_status = excluded.credential_status,
  source_submission_id = excluded.source_submission_id,
  live_url = excluded.live_url,
  notes = excluded.notes,
  updated_at = CURRENT_TIMESTAMP;
```

## Record Failed Attempt And Escalation

Each candidate gets at most 3 attempts. After every failed/blocked attempt, write the attempt and update the aggregate error pattern.

```sql
INSERT INTO submission_attempts (
  submission_id, source_table, source_id, platform_domain, attempt_no,
  status, error_signature, error_message, notes
) VALUES (
  123,
  'candidates',
  456,
  'example.com',
  1,
  'failed',
  'upload_button_timeout',
  'Image upload button timed out after file chooser opened',
  'Retry with smaller PNG'
);

INSERT INTO error_patterns (
  error_signature, occurrence_count, optimization_attempts, status,
  priority_tag, notes, last_seen
) VALUES (
  'upload_button_timeout',
  1,
  0,
  'observed',
  NULL,
  'Retry with smaller PNG',
  CURRENT_TIMESTAMP
)
ON CONFLICT(error_signature) DO UPDATE SET
  occurrence_count = occurrence_count + 1,
  last_seen = CURRENT_TIMESTAMP,
  notes = CASE
    WHEN excluded.notes IS NULL OR excluded.notes = '' THEN error_patterns.notes
    WHEN error_patterns.notes IS NULL OR error_patterns.notes = '' THEN excluded.notes
    ELSE error_patterns.notes || char(10) || excluded.notes
  END;

UPDATE error_patterns
SET
  status = CASE
    WHEN occurrence_count >= 3 AND optimization_attempts >= 1 THEN 'unresolved_high_priority'
    WHEN occurrence_count >= 3 THEN 'needs_optimization'
    ELSE status
  END,
  priority_tag = CASE
    WHEN occurrence_count >= 3 THEN 'HIGH_PRIORITY_FIX'
    ELSE priority_tag
  END
WHERE error_signature = 'upload_button_timeout';

UPDATE submissions
SET
  attempt_count = MAX(COALESCE(attempt_count, 0), 1),
  last_error_signature = 'upload_button_timeout',
  status = CASE WHEN 1 >= 3 THEN 'failed_after_3_attempts' ELSE 'failed' END,
  error_log = 'Image upload button timed out after file chooser opened'
WHERE id = 123;
```

After the same error reaches 3 occurrences, stop the batch and make one workflow fix. Record that one optimization:

```sql
UPDATE error_patterns
SET
  optimization_attempts = optimization_attempts + 1,
  status = 'optimization_attempted',
  priority_tag = 'HIGH_PRIORITY_FIX',
  notes = CASE
    WHEN notes IS NULL OR notes = '' THEN 'Tried smaller image upload path'
    ELSE notes || char(10) || 'Tried smaller image upload path'
  END,
  last_seen = CURRENT_TIMESTAMP
WHERE error_signature = 'upload_button_timeout';
```

If the error appears again after that fix, mark it and route around it:

```sql
UPDATE error_patterns
SET status = 'unresolved_high_priority',
    priority_tag = 'HIGH_PRIORITY_FIX',
    last_seen = CURRENT_TIMESTAMP
WHERE error_signature = 'upload_button_timeout';
```

## Reports

KPI:

```sql
SELECT COUNT(*) AS live_dofollow
FROM submissions
WHERE status = 'live' AND rel_actual = 'dofollow';
```

Status breakdown:

```sql
SELECT status, rel_actual, COUNT(*) AS count
FROM submissions
GROUP BY status, rel_actual
ORDER BY count DESC;
```

Pending public checks:

```sql
SELECT id, platform_domain, live_url, submit_time, notes
FROM submissions
WHERE status IN ('submitted', 'pending', 'pending_review', 'pending_email_confirmation')
ORDER BY submit_time DESC;
```

Created accounts:

```sql
SELECT platform_domain, account_email, username, credential_status, auth_method, notes
FROM account_credentials
ORDER BY updated_at DESC;
```

High-priority unresolved errors:

```sql
SELECT error_signature, occurrence_count, optimization_attempts, status, priority_tag, notes
FROM error_patterns
WHERE occurrence_count >= 3 OR status = 'unresolved_high_priority'
ORDER BY occurrence_count DESC;
```
