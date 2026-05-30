"""
Round-2 Day-1 Step 4.2 Layer 2 finalize · Pool B ~200 keywords.

Strategy: per-ICP quota (8 each × 25 ICPs ≈ 200), prioritized by:
  1. Auto-keep candidates first (rule-strong question shape)
  2. Within each ICP, sort by Reddit score (proxy for community resonance)
     Quora/IH (no score) ranked AFTER reddit (low_confidence, but unique signal)
  3. If an ICP has fewer than quota in auto-keep, top up from manual_review by score
  4. Skip duplicates (post_id seen)

Output: pool_b.json (~200 records, balanced) + Pool C unchanged
"""

import json
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).parent.parent / "data"
KEEP = json.loads((DATA_DIR / "pool_b_auto_keep.json").read_text())
REVIEW = json.loads((DATA_DIR / "pool_b_manual_review.json").read_text())

QUOTA_PER_ICP = 8  # 25 × 8 = 200


def primary_icp(rec):
    icp = rec.get("icp")
    return icp[0] if isinstance(icp, list) else icp


def score_key(rec):
    """Higher score = better. Quora/IH (None) sorted last."""
    s = rec.get("score")
    if s is None:
        return -1  # SERP fallback ranks below any reddit score
    return s


def main():
    seen = set()
    icp_groups_keep = defaultdict(list)
    icp_groups_review = defaultdict(list)

    for r in KEEP:
        icp = primary_icp(r)
        key = (r["platform"], r["post_id"])
        if key in seen:
            continue
        seen.add(key)
        icp_groups_keep[icp].append(r)

    for r in REVIEW:
        icp = primary_icp(r)
        key = (r["platform"], r["post_id"])
        if key in seen:
            continue
        seen.add(key)
        icp_groups_review[icp].append(r)

    # Sort each group by score desc
    for g in icp_groups_keep.values():
        g.sort(key=score_key, reverse=True)
    for g in icp_groups_review.values():
        g.sort(key=score_key, reverse=True)

    pool_b = []
    icp_counts = {}
    icp_filled_from_review = {}

    all_icps = sorted(set(list(icp_groups_keep.keys()) + list(icp_groups_review.keys())))
    for icp in all_icps:
        from_keep = icp_groups_keep[icp][:QUOTA_PER_ICP]
        remaining = QUOTA_PER_ICP - len(from_keep)
        from_review = icp_groups_review[icp][:remaining] if remaining > 0 else []
        pool_b.extend(from_keep + from_review)
        icp_counts[icp] = len(from_keep) + len(from_review)
        icp_filled_from_review[icp] = len(from_review)

    # Stats
    print(f"=== Pool B Balanced Selection ===")
    print(f"Total: {len(pool_b)} (target ~200)\n")
    print(f"Per-ICP breakdown:")
    for icp in all_icps:
        marker = f" (+{icp_filled_from_review[icp]} from review)" if icp_filled_from_review[icp] > 0 else ""
        avail_keep = len(icp_groups_keep[icp])
        print(f"  {icp:25s} {icp_counts[icp]} (auto_keep had {avail_keep}){marker}")

    out = DATA_DIR / "pool_b.json"
    out.write_text(json.dumps(pool_b, indent=2, ensure_ascii=False))
    print(f"\nWrote: {out}")


if __name__ == "__main__":
    import sys
    sys.exit(main())
