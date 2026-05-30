"""
IH-only retry · 5 query · ultra-slow pacing.

Last attempt: site:indiehackers.com triggered Google CAPTCHA after only 1 query
(coming on the heels of 8 quora queries). This run:
  · interval 100-130s per query
  · fail-streak halt = 1 (save IP, don't burn it)
  · 5 queries → ~10 min
"""

import json
import random
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from capture_quora_ih import run_opencli, write_raw  # noqa: E402

OUT_DIR = Path.home() / "tools" / "opencli-raw"
FAIL_LOG = OUT_DIR / "round2-day1-ih-retry-FAILURES.json"

IH_QUERIES = {
    "indie-saas-founder": "saas marketing pricing first customers",
    "solo-dev": "solo developer indie hacker",
    "ai-builder": "AI agent wrapper builder",
    "newsletter-writer": "newsletter growth subscribers",
    "shopify-owner": "shopify store ecommerce growth",
}

INTERVAL_RANGE = (100, 130)


def main():
    failures = []
    success = 0
    total_results = 0
    runs = []
    for icp, q in IH_QUERIES.items():
        runs.append(("ih", icp, q, f'google search "site:indiehackers.com {q}" --limit 30'))

    total = len(runs)
    t0 = time.time()
    print(f"[plan] {total} IH queries · interval {INTERVAL_RANGE}s · fail-streak halt = 1", flush=True)

    for idx, (platform, icp, query, args) in enumerate(runs, 1):
        elapsed = time.time() - t0
        print(f"[{idx}/{total}] {elapsed:>6.1f}s · {icp} · {query[:60]}", flush=True)
        result = run_opencli(args)
        if result["ok"]:
            data = result["data"]
            n = len(data) if isinstance(data, list) else 1
            total_results += n
            success += 1
            payload = {
                "platform": platform,
                "icp": icp,
                "query": query,
                "args": args,
                "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "result_count": n,
                "low_confidence": True,
                "data": data,
            }
            write_raw(platform, icp, payload)
            print(f"      ✓ {n} results", flush=True)
        else:
            failures.append({"icp": icp, "query": query, "args": args, "error": result["error"]})
            print(f"      ✗ FAIL: {result['error']}", flush=True)
            print(f"\n!! Halting on first failure to save IP. Got {success}/{total}.", flush=True)
            break

        if idx < total:
            pause = random.uniform(*INTERVAL_RANGE)
            print(f"      ⏸  pause {pause:.0f}s", flush=True)
            time.sleep(pause)

    elapsed = time.time() - t0
    print(f"\n=== IH-Retry Summary ===", flush=True)
    print(f"Runs: {success}/{total} OK · {len(failures)} failed", flush=True)
    print(f"Results captured: {total_results}", flush=True)
    print(f"Elapsed: {elapsed:.0f}s ({elapsed/60:.1f} min)", flush=True)
    if failures:
        FAIL_LOG.write_text(json.dumps(failures, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
