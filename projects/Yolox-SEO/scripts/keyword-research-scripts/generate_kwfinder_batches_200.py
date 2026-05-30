"""
Regroup remaining 540 keywords into 200-keyword batches for paid KWFinder.

Output: data/Data_Gotted/batch-200-1.csv ~ batch-200-3.csv (3 files)
  · batch-200-1.csv: 200 keywords (priority 1 first — Pool A direct keep剩余)
  · batch-200-2.csv: 200 keywords (priority 2 — Haiku 4-yes)
  · batch-200-3.csv: ~140 keywords (priority 2 tail)
"""

import json
import re
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
GOTTED_DIR = DATA_DIR / "Data_Gotted"

DIRECT = json.loads((DATA_DIR / "pool_v2_direct_keep.json").read_text())
VERDICTS = json.loads((DATA_DIR / "pool_v2_haiku_verdicts.json").read_text())
HAIKU_KEEPS = [v for v in VERDICTS["haiku_verdicts_all"] if v.get("verdict") == "keep"]

# Already done in batch-1 / batch-2
already_done_keywords = set()
for f in [GOTTED_DIR / "kwfinder_import_export.csv",
          GOTTED_DIR / "kwfinder_import_export (1).csv"]:
    if f.exists():
        with open(f, newline="", encoding="utf-8") as fp:
            for r in csv.DictReader(fp):
                already_done_keywords.add(r["Keyword"].lower().strip())

print(f"Already done in earlier batches: {len(already_done_keywords)} keywords")


def normalize(kw):
    s = kw.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s)


# Priority 1: Direct keep (Pool A)
direct_kws = []
for r in DIRECT:
    kw = r.get("_kw_canonical") or r.get("keyword", "")
    direct_kws.append({"keyword": kw, "priority": 1})

# Priority 2: Haiku keep
haiku_kws = []
for v in HAIKU_KEEPS:
    haiku_kws.append({
        "keyword": v.get("kw_extracted") or v.get("keyword"),
        "priority": 2,
    })

# Combine + dedupe
all_kws = direct_kws + haiku_kws
seen = set()
already_done_norm = {normalize(k) for k in already_done_keywords}
unique_kws = []
for r in all_kws:
    norm = normalize(r["keyword"])
    if not norm or norm in seen or norm in already_done_norm:
        continue
    seen.add(norm)
    unique_kws.append(r)

print(f"Unique remaining keywords: {len(unique_kws)}")

# Sort by priority (asc)
unique_kws.sort(key=lambda x: x["priority"])

# Split into batches of 200
BATCH_SIZE = 200
batches = [unique_kws[i:i+BATCH_SIZE] for i in range(0, len(unique_kws), BATCH_SIZE)]
print(f"Total batches: {len(batches)}")

for i, batch in enumerate(batches, 1):
    out = GOTTED_DIR / f"batch-200-{i}.csv"
    out.write_text("\n".join(r["keyword"] for r in batch))
    p1_count = sum(1 for r in batch if r["priority"] == 1)
    p2_count = sum(1 for r in batch if r["priority"] == 2)
    print(f"  batch-200-{i}.csv: {len(batch)} keywords (P1={p1_count}, P2={p2_count})")

print(f"\nTotal output: {sum(len(b) for b in batches)} keywords in {len(batches)} CSVs")
