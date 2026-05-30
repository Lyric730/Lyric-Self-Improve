"""
Step 5 retry · 13 shorter candidates after first round had 13/18 zero-hit.

Diagnosis: original keywords were too long (4-6 modifiers like "AI ASO
optimizer for indie iOS apps") — Google suggest is prefix autocomplete,
needs real users to have searched the prefix. Trimmed to 2-4 token
shape ("AI ASO tool" / "AI app builder") that real users do search.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from step5_suggest_validate import (  # noqa: E402
    OUT_DIR,
    parse_json,
    run_suggest,
    keyword_has_hero_name,
)

OUT_FILE = OUT_DIR / "round2-step5-suggest-results-retry.json"

RETRY_CANDIDATES = [
    # A-dev (2 originally 0-hit, shorter)
    ("A-dev", "AI ASO tool",
     "agent Oliver (ASO Optimizer); team App Developer"),
    ("A-dev", "programmatic SEO AI",
     "agent Stella (Programmatic SEO Builder); team SaaS Founder"),

    # B-sparse (4)
    ("B-sparse", "AI proposal generator",
     "agent Aria (Freelance Proposal Writer); team Freelance Designer"),
    ("B-sparse", "AI ad creative generator",
     "agent Olivia (Ad Creative Studio); team Artisan/DTC"),
    ("B-sparse", "AI app builder",
     "team App Developer"),
    ("B-sparse", "AI for ML research",
     "Skills · Data & Analytics; team AI App Builder"),

    # C-compare (5)
    ("C-compare", "AI cold email tool",
     "agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer)"),
    ("C-compare", "AI brand identity generator",
     "agent Elijah (Brand Identity Manager); team Brand & PR"),
    ("C-compare", "AI infographic generator",
     "agent Logan (Infographic Designer); team Content Marketing"),
    ("C-compare", "AI newsletter writer",
     "agent Aurora (Newsletter Curator); team Newsletter Creator"),
    ("C-compare", "Shopify AI product description",
     "agent Grayson (Product Listing Copywriter); team Shopify/DTC"),

    # D-tag (2)
    ("D-tag", "AI sales agent",
     "Skills · Sales & CRM"),
    ("D-tag", "AI design tool",
     "Skills · Design & Creative 54"),
]


def main():
    results = []
    t0 = time.time()
    print(f"[plan] {len(RETRY_CANDIDATES)} shorter candidates · interval 5s")

    for idx, (group, kw, product) in enumerate(RETRY_CANDIDATES, 1):
        elapsed = time.time() - t0
        print(f"[{idx:>2}/{len(RETRY_CANDIDATES)}] {elapsed:>5.1f}s · {group} · {kw}", flush=True)
        r = run_suggest(kw)
        if r["ok"]:
            data = r["data"] or []
            n = len(data)
            results.append({
                "group": group,
                "keyword": kw,
                "product": product,
                "suggest_count": n,
                "suggestions": [d.get("suggestion", "") for d in data][:10],
                "hero_name_flag": keyword_has_hero_name(kw),
            })
            print(f"      ✓ {n} suggestions" + (f" · sample: {data[0].get('suggestion','')[:50]}" if data else ""))
        else:
            results.append({
                "group": group,
                "keyword": kw,
                "product": product,
                "suggest_count": 0,
                "error": r["error"],
                "hero_name_flag": keyword_has_hero_name(kw),
            })
            print(f"      ✗ FAIL: {r['error']}")

        if idx < len(RETRY_CANDIDATES):
            time.sleep(5)

    results.sort(key=lambda x: -x.get("suggest_count", 0))
    OUT_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))

    pass_count = sum(1 for r in results if r.get("suggest_count", 0) >= 1)
    print(f"\n=== Retry Summary ===")
    print(f"Pass (≥1 hit): {pass_count} / {len(RETRY_CANDIDATES)}")
    print(f"\nWrote: {OUT_FILE}")
    print(f"\nResults preview:")
    for i, r in enumerate(results, 1):
        marker = "✓" if r.get("suggest_count", 0) >= 1 else "✗"
        flag = f" 🔴HERO:{r['hero_name_flag']}" if r["hero_name_flag"] else ""
        print(f"  {i:>2}. [{marker}] {r.get('suggest_count',0):>2} hits · {r['keyword']}{flag}")


if __name__ == "__main__":
    sys.exit(main())
