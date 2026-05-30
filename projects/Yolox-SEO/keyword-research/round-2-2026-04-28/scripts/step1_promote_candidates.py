"""
L2 Step 1 · 升级候选列表生成.

Two pools to evaluate:
  · Pool B → Pool A: 45 records (Pool B 91 KEEP minus 46 already in Pool A)
  · Pool C → Pool B: ~812 records (Pool C 903 minus 91 already in Pool B)

Output candidates ranked by score for Claude semantic review.
"""

import json
import re
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
SCRIPTS_DIR = Path(__file__).parent

POOL_C = json.loads((DATA_DIR / "pool_c.json").read_text())
POOL_B = json.loads((DATA_DIR / "pool_b_curated.json").read_text())

# Extract Pool A post_ids from build_pool_a.py SELECTIONS.title_match
# (parse the .py file to get title_match strings, then look them up)
build_py = (SCRIPTS_DIR / "build_pool_a.py").read_text()
selection_titles = re.findall(r'SELECTIONS = \[(.*?)\n\]\n', build_py, re.DOTALL)
title_matches = []
if selection_titles:
    for m in re.finditer(r'\(\s*"[^"]+",\s*"[^"]+",\s*"([^"]+)"', selection_titles[0]):
        title_matches.append(m.group(1).lower()[:40])

pool_a_post_ids = set()
for r in POOL_B:
    title_low = r.get("title", "").lower()
    for tm in title_matches:
        if tm in title_low:
            pool_a_post_ids.add(r["post_id"])
            break

print(f"Pool A used post_ids: {len(pool_a_post_ids)} (expected 46)")

pool_b_ids = {r["post_id"] for r in POOL_B}
print(f"Pool B post_ids: {len(pool_b_ids)} (expected 91)")

# Pool B → Pool A candidates: in Pool B but NOT in Pool A
pb_to_pa = [r for r in POOL_B if r["post_id"] not in pool_a_post_ids]
pb_to_pa.sort(key=lambda x: -(x.get("score") or 0))
print(f"\nPool B → Pool A candidates: {len(pb_to_pa)} (expected ~45)")

# Group by ICP for balance
by_icp = defaultdict(list)
for r in pb_to_pa:
    icp = r["icp"][0] if isinstance(r["icp"], list) else r["icp"]
    by_icp[icp].append(r)

print("\n=== Pool B → A candidates (by ICP, score desc) ===")
for icp in sorted(by_icp.keys()):
    print(f"\n[{icp}] ({len(by_icp[icp])})")
    for r in by_icp[icp][:5]:  # top 5 per ICP
        score = r.get("score", "—") or "SERP"
        nc = r.get("num_comments", "—") or "—"
        title = r["title"][:80]
        print(f"  {r['post_id']:55s} [{score}/{nc}c] {title}")

# Pool C → Pool B candidates: in Pool C but NOT in Pool B, with high score + question signal
question_signals = ["how ", "why ", "what ", "any tool", "anyone ", "best ", "?",
                    "where ", "when ", "should i", "tips for", "looking for"]
pc_to_pb = []
for r in POOL_C:
    if r["post_id"] in pool_b_ids:
        continue
    if r.get("platform") != "reddit":
        continue
    score = r.get("score") or 0
    if score < 10:  # higher bar than Layer 1's 5
        continue
    title_low = r.get("title", "").lower()
    if not any(s in title_low for s in question_signals):
        continue
    pc_to_pb.append(r)

pc_to_pb.sort(key=lambda x: -(x.get("score") or 0))
print(f"\n\nPool C → Pool B candidates (score≥10 + question signal): {len(pc_to_pb)}")

# Group by ICP for top picks
pc_by_icp = defaultdict(list)
for r in pc_to_pb:
    icp = r["icp"][0] if isinstance(r["icp"], list) else r["icp"]
    pc_by_icp[icp].append(r)

print("\n=== Pool C → B candidates (top 4 per ICP) ===")
for icp in sorted(pc_by_icp.keys()):
    print(f"\n[{icp}] ({len(pc_by_icp[icp])})")
    for r in pc_by_icp[icp][:4]:
        score = r.get("score", "—")
        nc = r.get("num_comments", "—")
        title = r["title"][:90]
        print(f"  {r['post_id']:55s} [{score}/{nc}c] {title}")

# Save candidates JSON
out = {
    "pool_a_post_ids_used": sorted(pool_a_post_ids),
    "pool_b_to_pool_a_candidates": pb_to_pa,
    "pool_c_to_pool_b_candidates": pc_to_pb,
}
out_file = DATA_DIR / "step1_promote_candidates.json"
out_file.write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(f"\nWrote: {out_file}")
print(f"  Pool B→A: {len(pb_to_pa)} records")
print(f"  Pool C→B: {len(pc_to_pb)} records")
