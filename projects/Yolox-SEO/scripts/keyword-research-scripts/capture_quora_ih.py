"""
Round-2 Day-1 Step 4.1 fallback · Quora & IndieHackers via google site: (D5=A).

opencli has no quora/indiehackers adapter, so we use `opencli google search`
with `site:quora.com` / `site:indiehackers.com` operators. Output is SERP
metadata (title + url + snippet) — no views/votes signal, so Pool C tags
these as `low-confidence`.

Output: ~/tools/opencli-raw/round2-day1-{quora|ih}-{icp}.json

Run AFTER capture_reddit.py completes (daemon contention).
"""

import json
import random
import subprocess
import sys
import time
from pathlib import Path

# Anti-ban pacing (Google CAPTCHA'd us last run after burst).
# Random per-query delay + long pause every 5 queries + early-stop on
# 2 consecutive failures (we'd rather salvage some data than burn IP).
INTER_QUERY_DELAY_RANGE = (15, 25)   # seconds
LONG_PAUSE_EVERY = 5                 # queries
LONG_PAUSE_RANGE = (60, 90)          # seconds
FAIL_STREAK_STOP = 2                 # consecutive failures triggers halt

OUT_DIR = Path.home() / "tools" / "opencli-raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FAIL_LOG = OUT_DIR / "round2-day1-quora-ih-FAILURES.json"

OPENCLI_PREFIX = "source ~/.nvm/nvm.sh && nvm use 22 >/dev/null 2>&1 && opencli"

# Quora: 8 ICP × 1 query (L1 §3.2 — coaches, service biz, finance/recruiter, course)
QUORA_QUERIES = {
    "coach": "career coach how to find clients",
    "consultant": "consultant how to land first client",
    "course-creator": "how to create and sell online course",
    "restaurant-owner": "restaurant marketing strategy small business",
    "recruiter": "recruiter how to source candidates linkedin",
    "financial-advisor": "financial advisor how to grow practice",
    "amazon-seller": "amazon FBA seller how to start",
    "shopify-owner": "shopify store conversion rate",
}

# IH: 5 ICP × 1 query (L1 §3.3 — builder/founder)
IH_QUERIES = {
    "indie-saas-founder": "saas marketing pricing first customers",
    "solo-dev": "solo developer indie hacker",
    "ai-builder": "AI agent wrapper builder",
    "newsletter-writer": "newsletter growth subscribers",
    "shopify-owner": "shopify store ecommerce growth",
}


def parse_opencli_json(stdout):
    s = stdout.strip()
    if not s:
        return None
    start = s.find("[")
    if start < 0:
        start = s.find("{")
    if start < 0:
        return None
    decoder = json.JSONDecoder()
    try:
        obj, _ = decoder.raw_decode(s[start:])
        return obj
    except Exception:
        return None


def run_opencli(args, retries=2, timeout=60):
    # Single-quote outer bash -c so inner double-quoted query survives
    cmd = f"bash -c '{OPENCLI_PREFIX} {args} -f json'"
    last_err = None
    for attempt in range(retries + 1):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            if r.returncode == 0:
                obj = parse_opencli_json(r.stdout)
                if obj is not None:
                    return {"ok": True, "data": obj}
                last_err = "no JSON parsed"
            else:
                last_err = f"exit {r.returncode}: {r.stderr.strip()[:200]}"
        except subprocess.TimeoutExpired:
            last_err = f"timeout after {timeout}s"
        except Exception as e:
            last_err = f"exception: {e}"
        if attempt < retries:
            time.sleep(2 ** attempt)
    return {"ok": False, "error": last_err}


def write_raw(platform, icp, payload):
    out = OUT_DIR / f"round2-day1-{platform}-{icp}.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return out


def main():
    failures = []
    success = 0
    total_results = 0
    runs = []

    for icp, q in QUORA_QUERIES.items():
        runs.append(("quora", icp, q, f'google search "site:quora.com {q}" --limit 30'))
    for icp, q in IH_QUERIES.items():
        runs.append(("ih", icp, q, f'google search "site:indiehackers.com {q}" --limit 30'))

    total = len(runs)
    t0 = time.time()
    fail_streak = 0
    print(f"[plan] total runs: {total} (Quora {len(QUORA_QUERIES)} + IH {len(IH_QUERIES)})", flush=True)
    print(f"[pacing] inter-query {INTER_QUERY_DELAY_RANGE}s · long pause every {LONG_PAUSE_EVERY} queries ({LONG_PAUSE_RANGE}s) · fail-streak stop at {FAIL_STREAK_STOP}", flush=True)

    for idx, (platform, icp, query, args) in enumerate(runs, 1):
        elapsed = time.time() - t0
        print(f"[{idx:>2}/{total}] {elapsed:>6.1f}s · {platform} · {icp} · {query[:50]}", flush=True)
        result = run_opencli(args)
        if result["ok"]:
            data = result["data"]
            n = len(data) if isinstance(data, list) else 1
            total_results += n
            success += 1
            fail_streak = 0
            payload = {
                "platform": platform,
                "icp": icp,
                "query": query,
                "args": args,
                "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "result_count": n,
                "low_confidence": True,  # SERP only, no engagement signals
                "data": data,
            }
            write_raw(platform, icp, payload)
            print(f"      ✓ {n} results", flush=True)
        else:
            fail_streak += 1
            failures.append({
                "platform": platform,
                "icp": icp,
                "query": query,
                "args": args,
                "error": result["error"],
            })
            print(f"      ✗ FAIL ({fail_streak} streak): {result['error']}", flush=True)
            if fail_streak >= FAIL_STREAK_STOP:
                print(f"\n!! Fail streak {fail_streak} ≥ {FAIL_STREAK_STOP}, halting to avoid IP ban.", flush=True)
                break

        # Anti-ban pacing
        if idx < total:
            if idx % LONG_PAUSE_EVERY == 0:
                pause = random.uniform(*LONG_PAUSE_RANGE)
                print(f"      ⏸  long pause {pause:.0f}s", flush=True)
            else:
                pause = random.uniform(*INTER_QUERY_DELAY_RANGE)
            time.sleep(pause)

    elapsed = time.time() - t0
    print(f"\n=== Summary ===")
    print(f"Runs: {success}/{total} OK · {len(failures)} failed")
    print(f"Results captured: {total_results}")
    print(f"Elapsed: {elapsed:.0f}s")

    if failures:
        FAIL_LOG.write_text(json.dumps(failures, indent=2, ensure_ascii=False))
        print(f"Failure log: {FAIL_LOG}")


if __name__ == "__main__":
    sys.exit(main())
