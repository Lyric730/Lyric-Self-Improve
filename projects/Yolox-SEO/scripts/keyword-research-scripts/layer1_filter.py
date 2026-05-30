"""
Round-2 Day-1 Step 4.2 Layer 1 · Mechanical filter → Pool C.

Reads ~/tools/opencli-raw/round2-day1-{reddit|quora|ih}-*.json,
applies engagement + title-pattern filters, outputs:
- pool_c.json (passed records, structured for L2 semantic filter)
- pool_c_rejected.json (rejected with reason, for audit)

Filter rules (L1 plan §4.2 Layer 1):
- Reddit: upvotes ≥ 5 AND comments ≥ 5
- Quora/IH (SERP fallback): accept all, low_confidence=True
- Title MUST contain question signal: how / why / what / any tool / struggling /
  need help / as a / ? / anyone / has anyone / is there / where / when
- Title MUST NOT contain show-off: I built / I launched / Show HN / AMA /
  results / hit $X / crossed $X / exited / milestone / etc.
"""

import json
import re
import sys
from pathlib import Path

RAW_DIR = Path.home() / "tools" / "opencli-raw"
OUT_DIR = Path(__file__).parent.parent / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUESTION_SIGNALS = [
    "how ", "why ", "what ", "any tool", "struggling", "need help",
    "as a ", "as an ", "?", "anyone ", "has anyone", "is there",
    "where ", "when ", "best ", "looking for", "advice on",
    "thoughts on", "should i", "tips for", "help with",
]

SHOWOFF_SIGNALS = [
    "i built", "i launched", "show hn", "ama", "i made",
    "i created", "i shipped", "i finished", "crossed $", "hit $",
    "reached $", "exited my", "sold my", "my first $", "i just",
    "just launched", "just shipped", "just released",
    "milestone", "we hit", "we crossed", "we reached",
    "announcement", "roadmap update", "i'm launching",
    "weekly update", "monthly update", "year in review",
    "i'd like to share", "i want to share", "sharing my",
    "after months of", "after years of", "from $0 to",
]


def is_question_title(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in QUESTION_SIGNALS)


def is_showoff_title(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in SHOWOFF_SIGNALS)


def post_id_from_url(url: str, platform: str) -> str:
    if platform == "reddit":
        m = re.search(r"/comments/([a-z0-9]+)/", url)
        if m:
            return m.group(1)
    if platform == "quora":
        m = re.search(r"quora\.com/([^/?#]+)", url)
        if m:
            return m.group(1)[:60]
    if platform == "ih":
        m = re.search(r"indiehackers\.com/(?:post|forum-post)/([^/?#]+)", url)
        if m:
            return m.group(1)[:60]
        # fall back to last path segment
        m = re.search(r"indiehackers\.com/([^/?#]+/[^/?#]+)", url)
        if m:
            return m.group(1)[:60]
    return url[-40:]


def load_all_raw():
    files = sorted(RAW_DIR.glob("round2-day1-*.json"))
    files = [f for f in files if "FAILURES" not in f.name]
    print(f"Found {len(files)} raw files in {RAW_DIR}")
    return files


def process_reddit_payload(payload):
    icp = payload.get("icp")
    kind = payload.get("kind", "")
    sub_or_q = payload.get("sub_or_query", "")
    posts = payload.get("data", []) or []
    out = []
    rejected = []
    for p in posts:
        title = p.get("title", "")
        upvotes = p.get("upvotes", 0) or 0
        comments = p.get("comments", 0) or 0
        url = p.get("url", "")
        author = p.get("author", "")

        rec_base = {
            "platform": "reddit",
            "post_id": post_id_from_url(url, "reddit"),
            "source": sub_or_q if "subreddit" in kind else f"search:{sub_or_q}",
            "kind": kind,
            "title": title,
            "score": upvotes,
            "num_comments": comments,
            "url": url,
            "author": author,
            "icp": icp,
            "low_confidence": False,
        }
        # Filter 1: engagement
        if upvotes < 5 or comments < 5:
            rejected.append({**rec_base, "reason": f"engagement-low(score={upvotes},c={comments})"})
            continue
        # Filter 2: showoff
        if is_showoff_title(title):
            rejected.append({**rec_base, "reason": "showoff-pattern"})
            continue
        # Filter 3: question signal required
        if not is_question_title(title):
            rejected.append({**rec_base, "reason": "not-question-shape"})
            continue
        out.append(rec_base)
    return out, rejected


def process_serp_payload(payload, platform):
    """Quora / IH via google site: SERP — no score/comments, accept loosely."""
    icp = payload.get("icp")
    query = payload.get("query", "")
    results = payload.get("data", []) or []
    out = []
    rejected = []
    for p in results:
        title = p.get("title", "")
        url = p.get("url", "")
        snippet = p.get("snippet", "")
        rtype = p.get("type", "")
        # skip non-organic results (ads, knowledge panels)
        if rtype and rtype not in ("organic", "result", ""):
            rejected.append({"platform": platform, "icp": icp, "title": title, "url": url, "reason": f"non-organic({rtype})"})
            continue
        # skip non-quora/IH urls (google sometimes inserts side panels)
        domain = "quora.com" if platform == "quora" else "indiehackers.com"
        if domain not in url:
            rejected.append({"platform": platform, "icp": icp, "title": title, "url": url, "reason": "off-domain"})
            continue

        rec = {
            "platform": platform,
            "post_id": post_id_from_url(url, platform),
            "source": query,
            "kind": "serp-fallback",
            "title": title,
            "snippet": snippet[:200],
            "score": None,
            "num_comments": None,
            "url": url,
            "icp": icp,
            "low_confidence": True,
        }
        # Apply showoff filter (still applicable for Quora/IH titles)
        if is_showoff_title(title):
            rejected.append({**rec, "reason": "showoff-pattern"})
            continue
        # Question signal: relax for Quora (most Quora pages are questions); apply for IH
        if platform == "ih" and not is_question_title(title):
            rejected.append({**rec, "reason": "not-question-shape"})
            continue
        out.append(rec)
    return out, rejected


def main():
    files = load_all_raw()
    pool_c = []
    rejected = []

    for f in files:
        try:
            payload = json.loads(f.read_text())
        except Exception as e:
            print(f"  ⚠ skip {f.name}: {e}")
            continue
        platform = payload.get("platform")
        if not platform:
            # Reddit files don't carry platform key — infer from kind
            if "kind" in payload:
                platform = "reddit"
            else:
                platform = "reddit"  # default

        if platform == "reddit":
            kept, rej = process_reddit_payload(payload)
        elif platform in ("quora", "ih"):
            kept, rej = process_serp_payload(payload, platform)
        else:
            continue
        pool_c.extend(kept)
        rejected.extend(rej)

    # Dedupe pool_c by (platform, post_id) — multi-ICP overlap (e.g., r/SaaS)
    seen = {}
    for r in pool_c:
        key = (r["platform"], r["post_id"])
        if key in seen:
            # merge ICP into list
            existing = seen[key]
            if isinstance(existing.get("icp"), str):
                existing["icp"] = [existing["icp"]]
            if r["icp"] not in existing["icp"]:
                existing["icp"].append(r["icp"])
        else:
            seen[key] = dict(r)
    pool_c_dedup = list(seen.values())

    # Stats
    print(f"\n=== Filter Summary ===")
    print(f"Pool C (passed): {len(pool_c_dedup)} unique posts (from {len(pool_c)} hits)")
    print(f"Rejected: {len(rejected)}")
    by_platform = {}
    for r in pool_c_dedup:
        by_platform[r["platform"]] = by_platform.get(r["platform"], 0) + 1
    print(f"By platform: {by_platform}")

    by_reason = {}
    for r in rejected:
        by_reason[r["reason"]] = by_reason.get(r["reason"], 0) + 1
    print(f"Reject reasons (top 10):")
    for k, v in sorted(by_reason.items(), key=lambda x: -x[1])[:10]:
        print(f"  {k}: {v}")

    pool_c_path = OUT_DIR / "pool_c.json"
    rejected_path = OUT_DIR / "pool_c_rejected.json"
    pool_c_path.write_text(json.dumps(pool_c_dedup, indent=2, ensure_ascii=False))
    rejected_path.write_text(json.dumps(rejected, indent=2, ensure_ascii=False))
    print(f"\nWrote: {pool_c_path}")
    print(f"Wrote: {rejected_path}")


if __name__ == "__main__":
    sys.exit(main())
