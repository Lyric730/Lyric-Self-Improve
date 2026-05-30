"""
L2 Step 3 · Pool B 广扫 · D3 Google Suggest only.

Spec L2 §3 says D2 Related + D3 Suggest, but opencli google search returns
no related-search type, so we limit to D3 Suggest (public API, no CAPTCHA).

Input: Pool B 169 records (extended) minus 46 already in Pool A → ~123 records.
Title is simplified to keyword form (strip ?, first-person pronouns, etc.)

Output: ~/tools/opencli-raw/round2-step3-poolb-suggest.json
  schema: {keyword: {original_title, post_id, suggestions: [...]}}
"""

import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUT_DIR = Path.home() / "tools" / "opencli-raw"
OUT_FILE = OUT_DIR / "round2-step3-poolb-suggest.json"

POOL_B_EXTENDED = json.loads((DATA_DIR / "pool_b_extended.json").read_text())
CANDIDATES = json.loads((DATA_DIR / "step1_promote_candidates.json").read_text())
POOL_A_USED = set(CANDIDATES["pool_a_post_ids_used"])


def title_to_keyword(title):
    """Strip first-person pronouns, ?, brackets etc. for clean suggest query."""
    s = title.strip()
    # Remove leading hashtag tags or [D] / [Question] etc.
    s = re.sub(r"^\[[^\]]+\]\s*", "", s)
    # Remove trailing ?
    s = s.rstrip("?!.")
    # Strip first-person leading clauses
    s = re.sub(r"^(my\s+|i'?m\s+|i\s+am\s+|i\s+|we\s+)", "", s, flags=re.IGNORECASE)
    # Truncate to 80 chars (Google suggest works best with short prefix)
    if len(s) > 80:
        s = s[:80]
    return s.strip()


def fetch_suggest(kw, timeout=10):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(kw)}"
    cmd = ["curl", "-sL", "--max-time", str(timeout), url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and r.stdout:
        try:
            return json.loads(r.stdout)[1]
        except Exception:
            return None
    return None


def main():
    # Filter Pool B excluding Pool A used post_ids
    candidates = []
    for r in POOL_B_EXTENDED:
        if r["post_id"] in POOL_A_USED:
            continue
        kw = title_to_keyword(r["title"])
        if len(kw) < 5:
            continue
        candidates.append({
            "post_id": r["post_id"],
            "icp": r["icp"][0] if isinstance(r["icp"], list) else r["icp"],
            "platform": r.get("platform", "?"),
            "score": r.get("score"),
            "original_title": r["title"][:100],
            "keyword": kw,
        })

    print(f"[plan] {len(candidates)} Pool B words × Google Suggest")
    t0 = time.time()
    results = {}
    fail = 0

    for idx, c in enumerate(candidates, 1):
        kw = c["keyword"]
        if kw in results:
            # Dedupe by simplified keyword
            continue
        sugs = fetch_suggest(kw)
        if sugs is None or not sugs:
            fail += 1
            results[kw] = {**c, "suggestions": []}
        else:
            results[kw] = {**c, "suggestions": sugs[:15]}
        elapsed = time.time() - t0
        n = len(results[kw]["suggestions"])
        print(f"[{idx:>3}/{len(candidates)}] {elapsed:>5.1f}s · {kw[:60]:60s} · {n}", flush=True)
        time.sleep(1)

    total_sugg = sum(len(v["suggestions"]) for v in results.values())
    elapsed = time.time() - t0
    print(f"\n=== Step 3 Pool B Suggest Summary ===")
    print(f"Pool B candidates: {len(results)} unique keywords")
    print(f"Total suggestions: {total_sugg}")
    print(f"0-hit keywords: {fail}")
    print(f"Elapsed: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    OUT_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nWrote: {OUT_FILE}")


if __name__ == "__main__":
    sys.exit(main())
