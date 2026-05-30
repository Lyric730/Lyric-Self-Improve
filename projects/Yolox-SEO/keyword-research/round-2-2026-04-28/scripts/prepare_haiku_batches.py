"""
Prepare Haiku batches for L2 Step 5 Layer 3 · 4-question semantic filter.

From pool_v1_passed.json (1316 candidates):
  · tier-1-validated (KWFinder Vol>0): direct keep, no batch
  · tier-2-pool-a / tier-2-kd-only (Pool A 76): direct keep, no batch
  · tier-3-multi-source (50): batch process
  · tier-4-single-source (1190): batch process

Output: /tmp/round2-haiku-batch-NN.json (13 batches × ~95 keywords)
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
TMP_DIR = Path("/tmp")
BATCH_SIZE = 100

POOL = json.loads((DATA_DIR / "pool_v1_passed.json").read_text())

# Split by tier
direct_keep = [r for r in POOL if r["_priority"] in ("tier-1-validated", "tier-2-pool-a", "tier-2-kd-only")]
to_batch = [r for r in POOL if r["_priority"] in ("tier-3-multi-source", "tier-4-single-source")]

print(f"Total: {len(POOL)}")
print(f"Direct keep (tier 1+2): {len(direct_keep)}")
print(f"To batch (tier 3+4): {len(to_batch)}")

# Write direct-keep set (skip Haiku, goes straight to Layer 4)
direct_file = DATA_DIR / "pool_v2_direct_keep.json"
direct_file.write_text(json.dumps(direct_keep, indent=2, ensure_ascii=False))
print(f"\nWrote: {direct_file} ({len(direct_keep)} records)")

# Slim down each candidate for batch (keep keyword + 1-2 line context, drop bulk fields)
def slim(r):
    out = {
        "keyword": r.get("_kw_canonical") or r.get("keyword"),
        "icp": r.get("icp", "?"),
        "source": r.get("source", "?"),
        "priority": r["_priority"],
    }
    if r.get("seed"):
        out["seed"] = r["seed"]
    if r.get("kwf_kd") is not None:
        out["kwf_kd"] = r["kwf_kd"]
    if r.get("kwf_volume") is not None:
        out["kwf_volume"] = r["kwf_volume"]
    if r.get("_overlap_sources"):
        out["overlap_count"] = len(r["_overlap_sources"])
    return out

slim_batch = [slim(r) for r in to_batch]

# Split into batches of BATCH_SIZE
batches = [slim_batch[i:i+BATCH_SIZE] for i in range(0, len(slim_batch), BATCH_SIZE)]
print(f"\nBatches: {len(batches)}")

for i, batch in enumerate(batches, 1):
    out_file = TMP_DIR / f"round2-haiku-batch-{i:02d}.json"
    out_file.write_text(json.dumps({"batch_id": i, "size": len(batch), "keywords": batch}, indent=2, ensure_ascii=False))
    print(f"  batch {i:02d}: {len(batch)} keywords → {out_file}")

print(f"\n=== Next ===")
print(f"Dispatch {len(batches)} Haiku agents in parallel (5 at a time × 3 rounds)")
print(f"Each agent: read batch JSON → apply 4 questions → output verdict to /tmp/round2-haiku-verdict-NN.json")
