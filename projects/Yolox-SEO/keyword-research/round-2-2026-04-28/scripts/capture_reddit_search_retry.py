"""
Retry the 25 failed `reddit search` runs from capture_reddit.py.
Root cause: outer `bash -c "..."` collided with inner `"query"` quotes.
Fix is in capture_reddit.py (single-quote outer bash -c). This script
re-runs only the search portion, leaving the 106 successful subreddit
files untouched.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from capture_reddit import (  # noqa: E402
    ICP_SEARCH_QUERIES,
    OUT_DIR,
    run_opencli,
    write_raw,
)

FAIL_LOG = OUT_DIR / "round2-day1-reddit-search-FAILURES.json"


def main():
    failures = []
    success = 0
    total_posts = 0
    runs = []
    for icp, query in ICP_SEARCH_QUERIES.items():
        # query already has no internal double quotes; just wrap once
        runs.append(("search-asa", icp, icp, f'reddit search "{query}" --sort top --time year --limit 20'))

    total = len(runs)
    t0 = time.time()
    print(f"[plan] retry runs: {total}")

    for idx, (kind, icp, sub_or_q, args) in enumerate(runs, 1):
        elapsed = time.time() - t0
        print(f"[{idx:>2}/{total}] {elapsed:>5.1f}s · {icp}", flush=True)
        result = run_opencli(args)
        if result["ok"]:
            data = result["data"]
            n = len(data) if isinstance(data, list) else 1
            total_posts += n
            success += 1
            key = f"{kind}-{icp}-{sub_or_q}".replace("/", "_").replace(" ", "_").lower()
            payload = {
                "kind": kind,
                "icp": icp,
                "sub_or_query": sub_or_q,
                "args": args,
                "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "post_count": n,
                "data": data,
            }
            write_raw(key, payload)
            print(f"      ✓ {n} posts", flush=True)
        else:
            failures.append({"icp": icp, "args": args, "error": result["error"]})
            print(f"      ✗ FAIL: {result['error']}", flush=True)
        time.sleep(1.5)

    elapsed = time.time() - t0
    print(f"\n=== Search-Retry Summary ===")
    print(f"Runs: {success}/{total} OK · {len(failures)} failed")
    print(f"Posts captured: {total_posts}")
    print(f"Elapsed: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    if failures:
        FAIL_LOG.write_text(json.dumps(failures, indent=2, ensure_ascii=False))
        print(f"Failure log: {FAIL_LOG}")


if __name__ == "__main__":
    sys.exit(main())
