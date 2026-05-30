"""
Step 5 · Product semantic seed validation via google suggest.

18 candidate keywords (Claude hand-designed from manifest reverse mapping)
→ opencli google suggest (public API, no browser, no CAPTCHA risk)
→ keep entries with ≥1 suggestion → top 14 progress to Pool A.

L1 §2.5 quality gate per keyword:
  · product mapping (already pre-filled in CANDIDATES tuple)
  · google suggest ≥1 hit OR PAA appearance (we use suggest only)
  · no internal agent first-name (Sophie/Elias/Stella/...)
  · dedupe vs Pool A 46 / Pool B 91 (post-validation script step)
"""

import json
import subprocess
import sys
import time
from pathlib import Path

OUT_DIR = Path.home() / "tools" / "opencli-raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "round2-step5-suggest-results.json"

OPENCLI_PREFIX = "source ~/.nvm/nvm.sh && nvm use 22 >/dev/null 2>&1 && opencli"

# (group, keyword, product_link)
CANDIDATES = [
    # A · dev/builder main line (5)
    ("A-dev", "AI agent for code review",
     "Skills · Developer Tools (agent-tools); team AI App Builder"),
    ("A-dev", "AI agent for unit testing",
     "Skills · Developer Tools"),
    ("A-dev", "AI agent for API documentation",
     "Skills · DevOps; team Indie Hacker"),
    ("A-dev", "AI ASO optimizer for indie iOS apps",
     "agent Oliver (ASO Optimizer); team App Developer"),
    ("A-dev", "programmatic SEO agent for SaaS founders",
     "agent Stella (Programmatic SEO Builder); team SaaS Founder"),

    # B · sparse ICP refill (4)
    ("B-sparse", "AI proposal writer for freelance designers",
     "agent Aria (Freelance Proposal Writer); team Freelance Designer"),
    ("B-sparse", "AI ad creative generator for DTC brands",
     "agent Olivia (Ad Creative Studio); team Artisan/DTC"),
    ("B-sparse", "AI agent for cross-platform mobile apps",
     "team App Developer"),
    ("B-sparse", "AI agent for indie ML researchers",
     "Skills · Data & Analytics; team AI App Builder"),

    # C · compare/buy decision (5)
    ("C-compare", "best AI agent for cold email outreach",
     "agent Lucas (Cold Outreach Pro); agent Daniel (Email Closer)"),
    ("C-compare", "AI brand identity manager for solo founders",
     "agent Elijah (Brand Identity Manager); team Brand & PR"),
    ("C-compare", "AI infographic designer for content marketers",
     "agent Logan (Infographic Designer); team Content Marketing"),
    ("C-compare", "best AI tool for newsletter growth",
     "agent Aurora (Newsletter Curator); team Newsletter Creator"),
    ("C-compare", "AI agent for shopify product descriptions",
     "agent Grayson (Product Listing Copywriter); team Shopify/DTC"),

    # D · skill category (4)
    ("D-tag", "Marketing & Growth AI agents",
     "Skills · Marketing & Growth 33"),
    ("D-tag", "Content & Writing AI agents",
     "Skills · Content & Writing 24"),
    ("D-tag", "Sales & CRM AI agents",
     "Skills · Sales & CRM"),
    ("D-tag", "Design & Creative AI agents",
     "Skills · Design & Creative 54"),
]

# Internal agent first-names (per L1 §6.5) — for dedupe check
HERO_NAMES = {
    "sophie", "elias", "stella", "olivia", "aria", "lucas", "daniel",
    "aurora", "elena", "logan", "elijah", "harper", "theodore",
    "isaiah", "savannah", "addison", "alexander", "wyatt", "audrey",
    # (Selectively block; we allow them in product_link but flag in keyword)
}


def parse_json(stdout):
    s = stdout.strip()
    start = s.find("[")
    if start < 0:
        return None
    decoder = json.JSONDecoder()
    try:
        obj, _ = decoder.raw_decode(s[start:])
        return obj
    except Exception:
        return None


def run_suggest(keyword, timeout=30):
    cmd = f"bash -c '{OPENCLI_PREFIX} google suggest \"{keyword}\" --lang en -f json'"
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0:
            data = parse_json(r.stdout)
            if data is not None:
                return {"ok": True, "data": data}
        return {"ok": False, "error": (r.stdout + r.stderr).strip()[:200]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timeout {timeout}s"}


def keyword_has_hero_name(kw):
    """Flag if the keyword string contains an internal agent first-name."""
    low = kw.lower()
    return [n for n in HERO_NAMES if f" {n} " in f" {low} " or low.startswith(n + " ")]


def main():
    results = []
    t0 = time.time()
    print(f"[plan] {len(CANDIDATES)} candidates · interval 5s · public API")

    for idx, (group, kw, product) in enumerate(CANDIDATES, 1):
        elapsed = time.time() - t0
        print(f"[{idx:>2}/{len(CANDIDATES)}] {elapsed:>5.1f}s · {group} · {kw}", flush=True)
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
            print(f"      ✓ {n} suggestions" + (f" · sample: {data[0].get('suggestion','')[:50]}" if data else " · NO HITS"))
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

        if idx < len(CANDIDATES):
            time.sleep(5)

    # Sort by suggest_count desc
    results.sort(key=lambda x: -x.get("suggest_count", 0))

    OUT_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n=== Step 5 Suggest Validation ===")
    pass_count = sum(1 for r in results if r.get("suggest_count", 0) >= 1)
    print(f"Pass (≥1 hit): {pass_count} / {len(CANDIDATES)}")
    print(f"Top 14 by hit count → Pool A (产品语义部分)")
    print(f"\nWrote: {OUT_FILE}")
    print(f"\nResults preview (top 18):")
    for i, r in enumerate(results, 1):
        marker = "✓" if r.get("suggest_count", 0) >= 1 else "✗"
        flag = f" 🔴HERO:{r['hero_name_flag']}" if r["hero_name_flag"] else ""
        print(f"  {i:>2}. [{marker}] {r.get('suggest_count',0):>2} hits · {r['keyword']}{flag}")


if __name__ == "__main__":
    sys.exit(main())
