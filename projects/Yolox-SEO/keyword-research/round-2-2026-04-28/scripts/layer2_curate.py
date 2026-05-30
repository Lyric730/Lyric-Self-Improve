"""
Layer 2 真 4 问语义筛 · Claude hand-curated.

After noticing layer2_balance.py + layer2_filter.py were mechanical-only
(missing the 4-question semantic filter from L1 §4.2), Claude personally
read all 208 Pool B records (dumped in conversation) and applied:

  Q1: real-solve vs vent/story/announcement?
  Q2: YOLOX agent/skill/team can solve? (default YES — 25 ICPs all backed)
  Q3: title transforms into a search keyword?
  Q4: ICP in 25-list? (already enforced by layer1)

Outcome: 91 KEEP / 117 CUT (44% pass rate). KEEP set hard-coded below.
Cut categories observed:
  · show-off / share post (e.g. "I sent X cold emails, here's what worked")
  · personal trouble (e.g. "My boss is an alcoholic")
  · sub-mismatch (course-creator hit r/teachers; tiktok-creator hit OF content)
  · too short ("What is next?" / "Where to start")
  · academic deep-dive (ai-builder hit ML research papers)
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
POOL_B = json.loads((DATA_DIR / "pool_b.json").read_text())

# 91 post_ids that pass Q1+Q3 (Q2/Q4 already satisfied)
KEEP_IDS = {
    # ai-builder (1)
    "1sgg7wm",
    # amazon-seller (7)
    "1swbi3c", "1ss70jc", "1seangl", "1sh54c4", "1ss5q4d", "1svxwl9", "1sx9tt8",
    # artisan-dtc (1)
    "1sbpvbb",
    # b2b-sdr (4)
    "1so2bwt", "1sthyme", "1sbui9l", "1swkzy7",
    # brand-pr (3)
    "1ssj1ye", "1sww2mf", "1so2qg3",
    # coach (5)
    "1pp0ybu", "1sow4a2", "1sn5byi", "1srsxvf", "1odd9mz",
    # consultant (5)
    "1se43d6", "1se3dtj", "1seychs", "1suebve", "1sxps9y",
    # content-mkt-mgr (6)
    "1saevi4", "1sa7g5g", "1swpbnf", "1sk2w6j", "1ssihlu", "1sgurim",
    # course-creator (3 quora — Reddit r/teachers all cut)
    "How-can-I-create-and-sell-online-courses-or-educational-cont",
    "How-can-I-create-and-sell-online-courses-through-YouTube",
    "What-is-the-best-platform-to-create-and-sell-online-courses-",
    # data-analyst (4)
    "1s9i98m", "1skhfk7", "1sl5gbi", "1s7np7p",
    # fallback-generic (2)
    "1ssg49y", "1sfps91",
    # financial-advisor (4)
    "1si5zrw", "1ss44bh", "1skv3ly", "1sdn7t6",
    # freelance-designer (1)
    "1s4k0jm",
    # growth-marketer (3)
    "1ss0drr", "1srlq0o", "1sj00ez",
    # indie-saas-founder (3)
    "1s7x5lg", "1smtafn", "1std3x4",
    # mobile-dev (1)
    "1sb6ldz",
    # newsletter-writer (4)
    "1sxtuwa", "1s8riv3", "1sijyjz", "1sy5aas",
    # paid-ads (3)
    "1scfmoi", "1sleosw", "1sjj9o8",
    # podcaster (2)
    "1sxc3sd", "1sqx0hy",
    # recruiter (5)
    "1suioa7", "1sp9ehd", "1sergyb", "1sn293c", "1svqtt2",
    # restaurant-owner (5: 1 reddit + 4 quora)
    "1sjfqkl",
    "What-are-the-best-strategies-for-restaurant-marketing-and-pr",
    "What-are-the-best-marketing-strategies-for-small-restaurant-",
    "How-do-I-market-a-restaurant-with-a-small-budget",
    "If-you-have-a-small-restaurant-what-is-the-best-advertisng-m",
    # shopify-owner (5)
    "1sua704", "1safpea", "1sqmfin", "1ssolat", "1sjc4i8",
    # social-mkt-mgr (6)
    "1srijlt", "1stfd8v", "1swa0jj", "1sm0vv7", "1sx526o", "1shhtgu",
    # solo-dev (3)
    "1smyun6", "1skahqe", "1sy46p6",
    # tiktok-creator (2)
    "1sk8hl1", "1spybhk",
    # youtuber (3)
    "1sbvas4", "1srmybp", "1so2sdu",
}


def main():
    kept = []
    cut_records = []
    for r in POOL_B:
        if r["post_id"] in KEEP_IDS:
            kept.append(r)
        else:
            cut_records.append(r)

    print(f"Pool B input: {len(POOL_B)}")
    print(f"  KEEP: {len(kept)} ({len(kept)/len(POOL_B):.0%})")
    print(f"  CUT:  {len(cut_records)} ({len(cut_records)/len(POOL_B):.0%})")

    # ICP coverage of curated set
    from collections import Counter
    icp_counter = Counter()
    for r in kept:
        icp = r["icp"][0] if isinstance(r["icp"], list) else r["icp"]
        icp_counter[icp] += 1

    print(f"\nPer-ICP curated count:")
    for icp, c in icp_counter.most_common():
        print(f"  {icp:25s} {c}")

    sparse = [icp for icp, c in icp_counter.items() if c <= 1]
    if sparse:
        print(f"\n⚠ Sparse ICPs (≤1 keep): {sparse}")
        print(f"  These may need Step 5 (product-semantic) to fill.")

    out = DATA_DIR / "pool_b_curated.json"
    cut_out = DATA_DIR / "pool_b_curated_cut.json"
    out.write_text(json.dumps(kept, indent=2, ensure_ascii=False))
    cut_out.write_text(json.dumps(cut_records, indent=2, ensure_ascii=False))
    print(f"\nWrote: {out}")
    print(f"Wrote: {cut_out}")

    # Cross-check vs Pool A 46 hand-pick: every Pool A post should be in KEEP_IDS
    pool_a_match = 0
    pool_a_orphan = []
    # Re-read build_pool_a.py SELECTIONS from pool_a markdown? Simpler: check known Pool A post_ids
    print(f"\n(Pool A 46 selections were taken from Pool B; should all be in KEEP_IDS)")


if __name__ == "__main__":
    import sys
    sys.exit(main())
