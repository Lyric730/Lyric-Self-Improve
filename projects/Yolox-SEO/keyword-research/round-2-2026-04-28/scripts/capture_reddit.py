"""
Round-2 Day-1 Step 4.1 · Reddit raw capture via opencli.

Loops 25 ICP × 1-4 sub each (53 sub total, deduped) × 2 sort modes
(hot/week + top/month) + 25 ICP search ("as a {ICP} how do I").

Output: ~/tools/opencli-raw/round2-day1-reddit-{key}.json
Failure log: ~/tools/opencli-raw/round2-day1-reddit-FAILURES.json

Run: nvm use 22 && python3 capture_reddit.py
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

OUT_DIR = Path.home() / "tools" / "opencli-raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FAIL_LOG = OUT_DIR / "round2-day1-reddit-FAILURES.json"

OPENCLI_PREFIX = (
    "source ~/.nvm/nvm.sh && nvm use 22 >/dev/null 2>&1 && opencli"
)

# 25 ICP × subs (from L1 plan §3.1, deduped)
ICP_SUBS = {
    "growth-marketer": ["marketing", "growthhacking", "SEO"],
    "content-mkt-mgr": ["contentmarketing", "blogging"],
    "brand-pr": ["PublicRelations", "branding"],
    "social-mkt-mgr": ["socialmedia", "SocialMediaMarketing"],
    "paid-ads": ["PPC", "FacebookAds", "GoogleAds"],
    "b2b-sdr": ["sales", "salestechniques", "coldemail"],
    "consultant": ["consulting"],
    "coach": ["Coaching", "lifecoaching"],
    "freelance-designer": ["freelance", "graphic_design"],
    "newsletter-writer": ["Substack", "Newsletters"],
    "podcaster": ["podcasting"],
    "youtuber": ["NewTubers", "PartneredYoutube"],
    "tiktok-creator": ["CreatorsAdvice"],
    "course-creator": ["teachers", "onlinecourse"],
    "indie-saas-founder": ["SaaS", "indiehackers"],
    "ai-builder": ["LocalLLaMA", "MachineLearning", "aiprogramming", "Anthropic"],
    "mobile-dev": ["iOSProgramming", "androiddev", "reactnative"],
    "solo-dev": ["programming", "selfhosted"],
    "amazon-seller": ["AmazonSeller", "FulfillmentByAmazon"],
    "shopify-owner": ["shopify", "ecommerce"],
    "artisan-dtc": ["Etsy"],
    "restaurant-owner": ["restaurateur", "KitchenConfidential"],
    "recruiter": ["recruiting"],
    "financial-advisor": ["CFP", "FinancialPlanning"],
    "data-analyst": ["dataanalysis", "SQL"],
    "fallback-generic": ["Entrepreneur", "smallbusiness"],
}

# ICP search queries (Reddit search "as a {ICP} how do I")
ICP_SEARCH_QUERIES = {
    "growth-marketer": "as a growth marketer how do I",
    "content-mkt-mgr": "as a content marketer how do I",
    "brand-pr": "as a brand manager how do I",
    "social-mkt-mgr": "as a social media manager how do I",
    "paid-ads": "as a media buyer how do I",
    "b2b-sdr": "as an SDR how do I",
    "consultant": "as a consultant how do I",
    "coach": "as a coach how do I",
    "freelance-designer": "as a freelance designer how do I",
    "newsletter-writer": "as a newsletter writer how do I",
    "podcaster": "as a podcaster how do I",
    "youtuber": "as a youtuber how do I",
    "tiktok-creator": "as a tiktok creator how do I",
    "course-creator": "as a course creator how do I",
    "indie-saas-founder": "as a SaaS founder how do I",
    "ai-builder": "as an AI builder how do I",
    "mobile-dev": "as a mobile dev how do I",
    "solo-dev": "as a solo developer how do I",
    "amazon-seller": "as an Amazon seller how do I",
    "shopify-owner": "as a Shopify owner how do I",
    "artisan-dtc": "as an Etsy seller how do I",
    "restaurant-owner": "as a restaurant owner how do I",
    "recruiter": "as a recruiter how do I",
    "financial-advisor": "as a financial advisor how do I",
    "data-analyst": "as a data analyst how do I",
}


def parse_opencli_json(stdout: str):
    """Strip trailing 'Update available' notice; return first JSON value."""
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


def run_opencli(args: str, retries: int = 2, timeout: int = 90):
    """Invoke opencli through bash + nvm v22; parse JSON; retry on failure.
    NOTE: outer bash -c uses SINGLE quotes so inner double-quoted args
    (like search queries) survive shell parsing intact.
    """
    cmd = f"bash -c '{OPENCLI_PREFIX} {args} -f json'"
    last_err = None
    for attempt in range(retries + 1):
        try:
            r = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            if r.returncode == 0:
                obj = parse_opencli_json(r.stdout)
                if obj is not None:
                    return {"ok": True, "data": obj, "raw_stdout_len": len(r.stdout)}
                last_err = "no JSON parsed from stdout"
            else:
                last_err = f"exit {r.returncode}: {r.stderr.strip()[:200]}"
        except subprocess.TimeoutExpired:
            last_err = f"timeout after {timeout}s"
        except Exception as e:
            last_err = f"exception: {e}"
        if attempt < retries:
            time.sleep(2 ** attempt)
    return {"ok": False, "error": last_err}


def write_raw(key: str, payload: dict):
    out = OUT_DIR / f"round2-day1-reddit-{key}.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return out


def main():
    failures = []
    success = 0
    total_runs = 0
    total_posts = 0

    # Plan: build full run list
    runs = []
    for icp, subs in ICP_SUBS.items():
        for sub in subs:
            runs.append(("subreddit-hot-week", icp, sub, f"reddit subreddit {sub} --sort hot --time week --limit 30"))
            runs.append(("subreddit-top-month", icp, sub, f"reddit subreddit {sub} --sort top --time month --limit 30"))
    for icp, query in ICP_SEARCH_QUERIES.items():
        # Quote query for shell
        q = query.replace('"', '\\"')
        runs.append(("search-asa", icp, icp, f'reddit search "{q}" --sort top --time year --limit 20'))

    total_runs = len(runs)
    t0 = time.time()
    print(f"[plan] total runs: {total_runs}")

    for idx, (kind, icp, sub_or_q, args) in enumerate(runs, 1):
        elapsed = time.time() - t0
        print(f"[{idx:>3}/{total_runs}] {elapsed:>5.1f}s · {kind} · {icp} · {sub_or_q}")
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
            print(f"      ✓ {n} posts")
        else:
            failures.append({
                "idx": idx,
                "kind": kind,
                "icp": icp,
                "sub_or_query": sub_or_q,
                "args": args,
                "error": result["error"],
            })
            print(f"      ✗ FAIL: {result['error']}")

        # Throttle: pause between runs to avoid Reddit rate limit
        time.sleep(1.5)

        # E1 exit condition: failure rate > 20%
        if idx >= 10:
            fail_rate = len(failures) / idx
            if fail_rate > 0.20:
                print(f"\n!! E1 trigger: failure rate {fail_rate:.1%} after {idx} runs. Pausing.")
                break

    elapsed = time.time() - t0
    print(f"\n=== Summary ===")
    print(f"Runs: {success}/{total_runs} OK · {len(failures)} failed")
    print(f"Posts captured: {total_posts}")
    print(f"Elapsed: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"Out dir: {OUT_DIR}")

    if failures:
        FAIL_LOG.write_text(json.dumps(failures, indent=2, ensure_ascii=False))
        print(f"Failure log: {FAIL_LOG}")

    return 0 if not failures or len(failures) / total_runs <= 0.2 else 1


if __name__ == "__main__":
    sys.exit(main())
