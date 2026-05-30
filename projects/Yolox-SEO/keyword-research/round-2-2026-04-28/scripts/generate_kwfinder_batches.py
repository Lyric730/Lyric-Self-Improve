"""
Split master v0 666 keywords into 27 KWFinder Free batch CSVs (25 each).

Strategy: priority order so that early batches contain highest-value
keywords (Tier 1/2 / Pool A) — small刀老师 can stop after first 8-10
batches if 时间紧 and still have Pillar-decision quality data.

Output: data/Data_Gotted/batch-3-keywords.csv ~ batch-29-keywords.csv
(continues from batch-1 + batch-2 already done = 30 keywords already)
"""

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
GOTTED_DIR = DATA_DIR / "Data_Gotted"

DIRECT = json.loads((DATA_DIR / "pool_v2_direct_keep.json").read_text())
VERDICTS = json.loads((DATA_DIR / "pool_v2_haiku_verdicts.json").read_text())
HAIKU_KEEPS = [v for v in VERDICTS["haiku_verdicts_all"] if v.get("verdict") == "keep"]

# Already done in batch-1 / batch-2 (Pool A 30 selected for Semrush KMT)
ALREADY_DONE_FILE = DATA_DIR / "Data_Gotted/kwfinder_import_export.csv"
already_done_keywords = set()
if ALREADY_DONE_FILE.exists():
    import csv
    for f in [DATA_DIR / "Data_Gotted/kwfinder_import_export.csv",
              DATA_DIR / "Data_Gotted/kwfinder_import_export (1).csv"]:
        if f.exists():
            with open(f, newline="", encoding="utf-8") as fp:
                for r in csv.DictReader(fp):
                    already_done_keywords.add(r["Keyword"].lower().strip())

print(f"Already done in earlier batches: {len(already_done_keywords)} keywords")

# Build priority-ordered keyword list
def normalize(kw):
    s = kw.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s)

# Priority 1: Direct keep (Pool A) — Tier 1/2/Pool-A精选
direct_kws = []
for r in DIRECT:
    kw = r.get("_kw_canonical") or r.get("keyword", "")
    direct_kws.append({
        "keyword": kw,
        "priority": 1,
        "tier_label": r.get("_priority", "?"),
        "icp": r.get("icp", "?"),
    })

# Priority 2-3: Haiku keep, sort by ICP coverage diversity
haiku_kws = []
for v in HAIKU_KEEPS:
    haiku_kws.append({
        "keyword": v.get("kw_extracted") or v.get("keyword"),
        "priority": 2,
        "tier_label": "haiku-4-yes",
        "icp": "?",
    })

# Combine + dedupe
all_kws = direct_kws + haiku_kws
seen = set()
unique_kws = []
for r in all_kws:
    norm = normalize(r["keyword"])
    if not norm or norm in seen:
        continue
    if norm in {normalize(k) for k in already_done_keywords}:
        continue  # skip already-done
    seen.add(norm)
    unique_kws.append(r)

print(f"Unique remaining keywords: {len(unique_kws)}")

# Sort by priority (asc) — priority 1 first
unique_kws.sort(key=lambda x: x["priority"])

# Split into batches of 25
BATCH_SIZE = 25
batches = [unique_kws[i:i+BATCH_SIZE] for i in range(0, len(unique_kws), BATCH_SIZE)]
print(f"Total batches: {len(batches)}")

# Write CSVs starting from batch-3 (batch-1+2 already in Data_Gotted)
batch_offset = 3
for i, batch in enumerate(batches):
    batch_num = i + batch_offset
    out = GOTTED_DIR / f"batch-{batch_num}-keywords.csv"
    out.write_text("\n".join(r["keyword"] for r in batch))
    if i < 5 or i == len(batches) - 1:  # show first 5 + last
        print(f"  batch-{batch_num}-keywords.csv: {len(batch)} keywords (priority {batch[0]['priority']})")

print(f"\nLast batch index: batch-{batch_offset + len(batches) - 1}-keywords.csv")
print(f"Total batches output: {len(batches)} ({sum(len(b) for b in batches)} keywords)")
