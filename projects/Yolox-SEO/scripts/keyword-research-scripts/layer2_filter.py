"""
Round-2 Day-1 Step 4.2 Layer 2 · Semantic filter (rule pre-pass).

Reads pool_c.json (903 unique posts). Applies enhanced rules to split into:
  · pool_b_auto_keep      — high-confidence semantic-OK (clear question + tool-shape)
  · pool_b_manual_review  — borderline, Claude reads + decides 4-questions
  · pool_b_auto_cut       — high-confidence story/rant/journey (extends layer1 rules)

The 4 questions (L1 §4.2):
  Q1: real solve vs vent/story/announcement?
  Q2: YOLOX agent/skill/team can solve?  (default YES — 25 ICPs all backed by manifest)
  Q3: title transforms into a search keyword?
  Q4: ICP in the 25-list?  (already enforced by layer1)

Auto-keep criteria (Q1 + Q3 strong signal):
  · Title contains "tool" OR "best X for" OR "how to X"
  · Title ends with "?" AND length ≤ 100 chars
  · Title contains "anyone using" / "alternative to" / "vs"
Auto-cut (Q1 fail — story/rant/lesson):
  · "my journey" / "lessons learned" / "year in review" / "what I learned"
  · "rant" / "vent" / "frustrated" without question
  · "advice for" + author share-mode (no question mark)
"""

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
POOL_C = DATA_DIR / "pool_c.json"
POOL_B_KEEP = DATA_DIR / "pool_b_auto_keep.json"
POOL_B_REVIEW = DATA_DIR / "pool_b_manual_review.json"
POOL_B_CUT = DATA_DIR / "pool_b_auto_cut.json"

# Strong keep signals (title shape implies info-intent search query)
KEEP_PATTERNS = [
    r"\bbest\s+\w+\s+(for|to)\b",          # best X for Y / best X to do Y
    r"\bany\s+(tool|tools)\b",              # any tool / any tools
    r"\banyone\s+(using|tried|know)\b",     # anyone using/tried
    r"\bhow\s+(to|do|can|should|would)\b",  # how to / how do
    r"\b(what|which|where|when|why)\s",     # info-intent question word
    r"\balternative(s)?\s+to\b",            # alternative to X
    r"\bvs\b|\bversus\b",                   # X vs Y comparison
    r"\bis\s+\w+\s+(worth|good|better)\b", # is X worth/good
    r"\btips?\s+(for|on|to)\b",             # tips for/on/to
    r"\bguide\s+(for|to|on)\b",             # guide for/to/on
    r"\bhelp\s+(with|me)\b",                # help with / help me
    r"\bstruggling\s+(with|to)\b",          # struggling with/to
    r"\bcan't\s+(figure|find|get)\b",       # can't figure out / find / get
    r"\bshould\s+I\b",                      # should I
    r"\b(recommend|recommendation|suggestion)s?\b",
]

# Strong cut signals (story / rant / share / not-search-shaped)
CUT_PATTERNS = [
    r"\bmy\s+(journey|story|experience|path|year)\b",
    r"\b(year|month|week)\s+in\s+review\b",
    r"\blessons?\s+(learned|i'?ve|i\s+learned)\b",
    r"\bwhat\s+i\s+(learned|wish|did|tried)\b",
    r"\b(i'?m|i\s+am)\s+(quitting|leaving|done|tired|exhausted|burned)\b",
    r"^(rant|vent|venting|opinion|hot\s+take|unpopular)\b",
    r"\b(rant|venting):\s",
    r"\badvice\s+for\s+\w+\s+(starting|new|wannabe)",  # "advice for new X"
    r"\bcase\s+study\b.*\b(how\s+i|how\s+we)\b",       # case study from author
    r"^my\s+\w+\s+(reached|hit|crossed|exceeded)",
    r"\b\d+\s+(years?|months?)\s+(in|of|after)\b.*\b(here'?s|here\s+is)\b",  # "5 years in, here's..."
]

# Compile
KEEP_RE = [re.compile(p, re.IGNORECASE) for p in KEEP_PATTERNS]
CUT_RE = [re.compile(p, re.IGNORECASE) for p in CUT_PATTERNS]


def classify(record):
    title = record.get("title", "")
    snippet = record.get("snippet", "")
    text = (title + " " + snippet).lower()

    keep_hits = [p.pattern for p in KEEP_RE if p.search(text)]
    cut_hits = [p.pattern for p in CUT_RE if p.search(text)]

    # Cut signals win over keep (story-shaped)
    if cut_hits and not keep_hits:
        return "cut", cut_hits, []
    # Strong keep + no cut → auto keep
    if keep_hits and not cut_hits:
        return "keep", keep_hits, []
    # Both → manual (likely "what I learned how to X")
    if keep_hits and cut_hits:
        return "review", keep_hits, cut_hits
    # Neither → manual review (could be valid topic without standard signal)
    return "review", [], []


def main():
    pool_c = json.loads(POOL_C.read_text())
    print(f"Loaded {len(pool_c)} Pool C records")

    keep, review, cut = [], [], []
    for r in pool_c:
        verdict, kh, ch = classify(r)
        annotated = dict(r)
        annotated["_l2_keep_hits"] = kh
        annotated["_l2_cut_hits"] = ch
        if verdict == "keep":
            keep.append(annotated)
        elif verdict == "cut":
            cut.append(annotated)
        else:
            review.append(annotated)

    print(f"\n=== Layer 2 Pre-Pass Summary ===")
    print(f"Auto-keep:     {len(keep):>4}  ({len(keep)/len(pool_c):.0%})")
    print(f"Manual review: {len(review):>4}  ({len(review)/len(pool_c):.0%})")
    print(f"Auto-cut:      {len(cut):>4}  ({len(cut)/len(pool_c):.0%})")

    POOL_B_KEEP.write_text(json.dumps(keep, indent=2, ensure_ascii=False))
    POOL_B_REVIEW.write_text(json.dumps(review, indent=2, ensure_ascii=False))
    POOL_B_CUT.write_text(json.dumps(cut, indent=2, ensure_ascii=False))
    print(f"\nWrote: {POOL_B_KEEP.name} / {POOL_B_REVIEW.name} / {POOL_B_CUT.name}")


if __name__ == "__main__":
    sys.exit(main())
