"""
Step 6 · 8-channel emerging-ecosystem scan.

Scans 4 web sources + 4 Reddit subs (already captured in opencli-raw)
for emerging 2026 concepts. Cross-source verified terms (≥2 sources)
graduate to Pool A as EXPLORATORY. Single-source terms go to watchlist.

Channels (per L1 §2.6) — all 8 covered:
  1. HN top — Algolia API JSON (hn.algolia.com/api/v1/search?tags=story)
  2. GitHub trending weekly — curl HTML
  3. Anthropic docs release notes — curl HTML
  4. OpenAI blog — RSS feed (openai.com/blog/rss.xml)
  5. Google AI blog — curl HTML
  6. Aleyda Solis — RSS feed (aleydasolis.com/en/feed/), SEOFOMO is paid-wall
  7. Search Engine Land SEO — curl HTML
  8. r/SEO + r/MachineLearning + r/LocalLLaMA + r/Anthropic — already in raw JSON

Cuts (per spec):
  - widely-known terms (GPT-4, Claude 3) — excluded from search list
  - corporate news (funding, hires) — N/A
  - only 1 source — → watchlist not Pool A
"""

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OPENCLI_RAW = Path.home() / "tools" / "opencli-raw"
WEB_CACHE_DIR = OPENCLI_RAW / "round2-step6-web-cache"
WEB_CACHE_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

WEB_SOURCES = {
    "hn-algolia": "https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage=100",
    "github-trending": "https://github.com/trending?since=weekly",
    "anthropic-release-notes": "https://docs.anthropic.com/en/release-notes/overview",
    "openai-rss": "https://openai.com/blog/rss.xml",
    "google-ai-blog": "https://blog.google/technology/ai/",
    "aleyda-rss": "https://www.aleydasolis.com/en/feed/",
    "search-engine-land-seo": "https://searchengineland.com/library/seo",
}

# Reddit raw files — sources already captured in Step 4
REDDIT_SOURCES = {
    "reddit-r-SEO-hot": "round2-day1-reddit-subreddit-hot-week-growth-marketer-seo.json",
    "reddit-r-MachineLearning-hot": "round2-day1-reddit-subreddit-hot-week-ai-builder-machinelearning.json",
    "reddit-r-LocalLLaMA-hot": "round2-day1-reddit-subreddit-hot-week-ai-builder-localllama.json",
    "reddit-r-Anthropic-hot": "round2-day1-reddit-subreddit-hot-week-ai-builder-anthropic.json",
}

# Emerging concepts to scan for (case-insensitive substring match)
# Each tuple: (canonical-term, [aliases])
EMERGING_TERMS = [
    ("mcp", ["mcp ", " mcp,", " mcp.", "model context protocol"]),
    ("a2a", ["a2a ", "agent2agent", "agent-to-agent", "agent to agent"]),
    ("structured-outputs", ["structured outputs", "structured output"]),
    ("aeo", ["aeo ", " aeo,", " aeo.", "answer engine optimization"]),
    ("geo", [" geo ", "generative engine optimization"]),
    ("llmo", ["llmo ", "llm optimization", "llm seo"]),
    ("llms-txt", ["llms.txt"]),
    ("ai-overview", ["ai overview", "ai overviews", "ai mode"]),
    ("chatgpt-search", ["chatgpt search", "chatgpt browse"]),
    ("perplexity-citation", ["perplexity citation", "perplexity citations"]),
    ("computer-use", ["computer use", "computer-use"]),
    ("agent-skills", ["agent skills", "claude skills"]),
    ("claude-code", ["claude code", "claude-code"]),
    ("agent-sdk", ["agent sdk", "agents sdk", "agent builder"]),
    ("ai-citations", ["ai citation", "ai citations", "llm citation", "llm citations"]),
    ("vibe-coding", ["vibe coding", "vibe-coding"]),
    ("rag-eval", ["rag eval", "rag evaluation"]),
    ("agentic-rag", ["agentic rag"]),
    ("ai-search", ["ai search", "ai-powered search"]),
    ("prompt-caching", ["prompt caching"]),
    ("fine-tuning-2026", ["fine-tuning", "fine tuning"]),  # heavily-used, may need filter
    ("voice-mode", ["voice mode", "advanced voice"]),
    ("realtime-api", ["realtime api"]),
    ("o1-reasoning", ["o1 ", "reasoning model"]),
]


def fetch_html(name, url):
    cache_file = WEB_CACHE_DIR / f"{name}.html"
    cmd = ["curl", "-sL", "--max-time", "20", "-A", UA, "-o", str(cache_file), url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0 and cache_file.exists() and cache_file.stat().st_size > 100:
        return cache_file.read_text(errors="replace")
    return None


def load_reddit(filename):
    path = OPENCLI_RAW / filename
    if not path.exists():
        return None
    try:
        d = json.loads(path.read_text())
        # Concatenate all titles
        return " ".join(p.get("title", "") for p in d.get("data", []))
    except Exception:
        return None


def scan_text(text, terms):
    if not text:
        return set()
    low = text.lower()
    hits = set()
    for canonical, aliases in terms:
        for a in aliases:
            if a.lower() in low:
                hits.add(canonical)
                break
    return hits


def main():
    source_hits = defaultdict(set)  # source -> set of canonical terms

    print("=== Web sources ===")
    for name, url in WEB_SOURCES.items():
        text = fetch_html(name, url)
        if text is None:
            print(f"  ✗ {name}: fetch failed")
            continue
        # Strip HTML tags for cleaner matching
        clean = re.sub(r"<[^>]+>", " ", text)
        hits = scan_text(clean, EMERGING_TERMS)
        source_hits[name] = hits
        print(f"  ✓ {name}: {len(hits)} terms · {sorted(hits)[:8]}")

    print("\n=== Reddit sources ===")
    for name, filename in REDDIT_SOURCES.items():
        text = load_reddit(filename)
        if text is None:
            print(f"  ✗ {name}: load failed (file: {filename})")
            continue
        hits = scan_text(text, EMERGING_TERMS)
        source_hits[name] = hits
        print(f"  ✓ {name}: {len(hits)} terms · {sorted(hits)[:8]}")

    # Cross-tally: term -> set of sources where it appeared
    term_sources = defaultdict(set)
    for source, hits in source_hits.items():
        for term in hits:
            term_sources[term].add(source)

    # Classify
    multi = {t: srcs for t, srcs in term_sources.items() if len(srcs) >= 2}
    single = {t: srcs for t, srcs in term_sources.items() if len(srcs) == 1}

    print(f"\n=== Cross-source classification ===")
    print(f"≥2 sources (→ Pool A EXPLORATORY): {len(multi)}")
    for term, srcs in sorted(multi.items(), key=lambda x: -len(x[1])):
        print(f"  · {term}: {len(srcs)} sources · {sorted(srcs)}")

    print(f"\n=1 source (→ watchlist): {len(single)}")
    for term, srcs in sorted(single.items()):
        print(f"  · {term}: {list(srcs)[0]}")

    out = {
        "channels_scanned": len(WEB_SOURCES) + len(REDDIT_SOURCES),
        "channels_succeeded": sum(1 for h in source_hits.values() if h or h == set()),
        "multi_source": {t: sorted(s) for t, s in multi.items()},
        "single_source": {t: sorted(s) for t, s in single.items()},
        "source_hits": {s: sorted(h) for s, h in source_hits.items()},
    }
    out_file = DATA_DIR / "step6_emerging_scan.json"
    out_file.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote: {out_file}")


if __name__ == "__main__":
    sys.exit(main())
