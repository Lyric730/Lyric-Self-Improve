"""
L2 Step 2 · Safe channels (no CAPTCHA risk) · public suggest APIs.

Channels covered:
  · D3 · Google Suggest (suggestqueries.google.com)
  · G  · YouTube Suggest (same endpoint, client=youtube, JSONP wrapped)
  · H1 · Bing Suggest (api.bing.com/osjson.aspx)
  · H2 · DuckDuckGo Suggest (duckduckgo.com/ac/)

Input: Pool A 76 keywords (Step 4 ICP 46 + Step 5 product 13 + Step 6
EXPLORATORY 7 + L2 Step 1 promoted 10)

Output: ~/tools/opencli-raw/round2-step2-suggest-all.json
  schema: {keyword: {channel: [suggestions...]}}
"""

import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

OUT_DIR = Path.home() / "tools" / "opencli-raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "round2-step2-suggest-all.json"
SCRIPTS_DIR = Path(__file__).parent

sys.path.insert(0, str(SCRIPTS_DIR))
from build_pool_a import SELECTIONS, SELECTIONS_STEP5, SELECTIONS_STEP6  # noqa: E402
from step1_promote_apply import B_TO_A  # noqa: E402


def collect_keywords():
    kws = []
    # Step 4 ICP 46
    for icp, keyword, _tm, _product in SELECTIONS:
        kws.append({"keyword": keyword, "icp": icp, "source": "step4-icp"})
    # Step 5 product semantic 13
    for icp, keyword, _hits, _product in SELECTIONS_STEP5:
        kws.append({"keyword": keyword, "icp": icp, "source": "step5-product"})
    # Step 6 emerging 7
    for canonical, keyword, _sources, _count, _note in SELECTIONS_STEP6:
        kws.append({"keyword": keyword, "icp": "(cross-icp)", "source": "step6-exploratory"})
    # L2 Step 1 promoted 10
    for post_id, icp, keyword, _reason, _product in B_TO_A:
        kws.append({"keyword": keyword, "icp": icp, "source": "step1-promoted"})
    return kws


def fetch_url(url, timeout=10):
    cmd = ["curl", "-sL", "--max-time", str(timeout), url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def google_suggest(kw):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={urllib.parse.quote(kw)}"
    data = fetch_url(url)
    if data:
        try:
            return json.loads(data)[1]
        except Exception:
            return None
    return None


def youtube_suggest(kw):
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={urllib.parse.quote(kw)}"
    data = fetch_url(url)
    if data:
        # JSONP wrapper: window.google.ac.h([query, [[s,...], ...]])
        m = re.search(r"\[(.*)\]", data, re.DOTALL)
        if m:
            try:
                arr = json.loads("[" + m.group(1) + "]")
                # arr = [query, [[s, 0, [...]], ...]]
                if len(arr) >= 2 and isinstance(arr[1], list):
                    return [item[0] for item in arr[1] if isinstance(item, list)]
            except Exception:
                return None
    return None


def bing_suggest(kw):
    url = f"https://api.bing.com/osjson.aspx?query={urllib.parse.quote(kw)}"
    data = fetch_url(url)
    if data:
        try:
            return json.loads(data)[1]
        except Exception:
            return None
    return None


def ddg_suggest(kw):
    url = f"https://duckduckgo.com/ac/?q={urllib.parse.quote(kw)}&type=list"
    data = fetch_url(url)
    if data:
        try:
            return json.loads(data)[1]
        except Exception:
            return None
    return None


CHANNELS = {
    "D3-google": google_suggest,
    "G-youtube": youtube_suggest,
    "H1-bing": bing_suggest,
    "H2-ddg": ddg_suggest,
}


def main():
    keywords = collect_keywords()
    print(f"[plan] {len(keywords)} keywords × {len(CHANNELS)} channels = {len(keywords)*len(CHANNELS)} API calls")
    t0 = time.time()
    results = {}
    fail_count = {ch: 0 for ch in CHANNELS}

    for idx, kw_info in enumerate(keywords, 1):
        kw = kw_info["keyword"]
        results[kw] = {"_meta": kw_info, "channels": {}}
        for ch_name, fn in CHANNELS.items():
            sugs = fn(kw)
            if sugs is None or not sugs:
                fail_count[ch_name] += 1
                results[kw]["channels"][ch_name] = []
            else:
                results[kw]["channels"][ch_name] = sugs[:15]
        elapsed = time.time() - t0
        n_total = sum(len(c) for c in results[kw]["channels"].values())
        print(f"[{idx:>2}/{len(keywords)}] {elapsed:>5.1f}s · {kw[:50]:50s} · {n_total} sugg",
              flush=True)
        time.sleep(1)  # public APIs, 1s pacing safe

    # Stats
    total_sugg = 0
    by_channel = {ch: 0 for ch in CHANNELS}
    for kw, payload in results.items():
        for ch, sugs in payload["channels"].items():
            by_channel[ch] += len(sugs)
            total_sugg += len(sugs)

    elapsed = time.time() - t0
    print(f"\n=== Step 2 Safe Channels Summary ===")
    print(f"Keywords: {len(keywords)}")
    print(f"Total suggestions: {total_sugg}")
    print(f"By channel:")
    for ch, n in by_channel.items():
        fails = fail_count[ch]
        print(f"  {ch:12s} {n:>5} sugg · {fails} kw with 0 hits")
    print(f"Elapsed: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    OUT_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nWrote: {OUT_FILE}")


if __name__ == "__main__":
    sys.exit(main())
