"""
Step 1: build the daily candidate pool for 三分钟未来.

Sources:
- AI HOT public API for fast AI-circle signals.
- Google News RSS queries for "AI changing reality" stories.

Output:
  daily/<date>/three-minute-future/work/candidates.json

Usage:
  python lines/three-minute-future/fetch_candidates.py 2026-05-23
  python lines/three-minute-future/fetch_candidates.py 2026-05-23 --content-date 2026-05-23
"""

from __future__ import annotations

import argparse
import email.utils
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = SCRIPT_DIR / "config" / "sources.json"

USER_AGENT = "self-media-three-minute-future/0.1"

AI_TERMS = [
    "ai",
    "人工智能",
    "大模型",
    "生成式",
    "智能体",
    "agent",
    "机器人",
    "自动驾驶",
    "openai",
    "anthropic",
    "deepmind",
    "nvidia",
    "英伟达",
    "microsoft",
    "微软",
    "meta",
]

REALITY_TAGS = {
    "law": ["法院", "裁员", "法律", "诉讼", "版权", "监管", "法案", "绿卡", "lawsuit", "court", "copyright", "regulation", "layoff"],
    "education": ["学校", "教育", "高中", "大学", "学生", "老师", "课堂", "school", "education", "student", "teacher"],
    "labor": ["员工", "工资", "招聘", "岗位", "工人", "工作", "labor", "worker", "hiring", "jobs", "wage"],
    "robotics": ["机器人", "人形机器人", "工厂", "机场", "搬运", "robot", "robotics", "factory", "airport"],
    "healthcare": ["医疗", "医院", "医生", "药", "healthcare", "hospital", "doctor", "medical"],
    "retail": ["零售", "库存", "门店", "星巴克", "retail", "inventory", "store", "starbucks"],
    "defense": ["国防", "五角大楼", "军方", "战争", "defense", "pentagon", "military"],
    "media": ["影视", "电影", "奥斯卡", "演员", "剧本", "music", "film", "oscars", "actor", "script"],
    "hardware": ["芯片", "算力", "硬件", "数据中心", "chip", "gpu", "hardware", "datacenter"],
    "policy": ["政府", "政策", "协议", "签署", "government", "policy", "agreement"],
    "society": ["伦理", "风险", "人性", "教皇", "宗教", "公共", "ethics", "risk", "humanity", "pope", "society"],
}

LOW_SIGNAL_TERMS = ["版本更新", "提示词", "框架", "教程", "测试", "release", "prompt", "benchmark"]


@dataclass
class Candidate:
    id: str
    title: str
    url: str
    source: str
    channel: str
    category: str
    published_at: str
    score: int
    tags: list[str]
    reason: str
    raw: dict[str, Any]

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "channel": self.channel,
            "category": self.category,
            "publishedAt": self.published_at,
            "score": self.score,
            "tags": self.tags,
            "reason": self.reason,
            "raw": self.raw,
        }


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def request_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def request_json(url: str, params: dict[str, Any]) -> dict[str, Any]:
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    return json.loads(request_text(full_url))


def safe_console(text: str) -> str:
    encoding = sys.stdout.encoding or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def stable_id(channel: str, title: str, url: str) -> str:
    payload = f"{channel}\n{normalize_title(title)}\n{canonical_url(url)}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", "", title).lower()


def canonical_url(url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(url)
        return urllib.parse.urlunparse((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/"), "", "", ""))
    except Exception:
        return url


LOCAL_TZ = timezone(timedelta(hours=8))


def parse_rss_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except Exception:
        return None


def parse_rss_date(value: str) -> str:
    parsed = parse_rss_datetime(value)
    if parsed is None:
        return value or ""
    return parsed.isoformat().replace("+00:00", "Z")


def date_in_range(day: date, start: date, end: date) -> bool:
    return start <= day <= end


def iso_matches_content_range(value: str, start: date, end: date) -> bool:
    if not value:
        return True
    try:
        day = date.fromisoformat(value[:10])
    except Exception:
        return True
    return date_in_range(day, start, end)


def rss_matches_content_range(value: str, start: date, end: date) -> bool:
    parsed = parse_rss_datetime(value)
    if parsed is None:
        return True
    return date_in_range(parsed.astimezone(LOCAL_TZ).date(), start, end)


def score_candidate(title: str, source: str, category: str) -> tuple[int, list[str], str]:
    text = f"{title} {source} {category}".lower()
    score = 0
    tags: list[str] = []
    reasons: list[str] = []

    if any(term.lower() in text for term in AI_TERMS):
        score += 2
        reasons.append("AI 相关")

    for tag, terms in REALITY_TAGS.items():
        matched = [term for term in terms if term.lower() in text]
        if matched:
            score += 2
            tags.append(tag)
            reasons.append(f"{tag}: {matched[0]}")

    if category in {"industry", "ai-products"}:
        score += 1

    if any(term.lower() in text for term in LOW_SIGNAL_TERMS):
        score -= 1
        reasons.append("偏工具/教程/小更新")

    if not tags:
        reasons.append("暂未命中现实场景标签")

    return score, tags, "；".join(reasons)


def fetch_aihot(config: dict[str, Any], content_start: date, content_end: date) -> list[Candidate]:
    aihot = config["aihot"]
    payload = request_json(
        aihot["url"],
        {
            "mode": aihot.get("mode", "all"),
            "take": int(aihot.get("take", 100)),
        },
    )

    items = payload.get("items", [])
    out: list[Candidate] = []
    for item in items:
        published_at = item.get("publishedAt", "")
        if published_at and not iso_matches_content_range(published_at, content_start, content_end):
            continue
        title = item.get("title", "").strip()
        url = item.get("url", "").strip()
        if not title or not url:
            continue
        source = item.get("source", "AI HOT")
        category = item.get("category", "")
        score, tags, reason = score_candidate(title, source, category)
        out.append(
            Candidate(
                id=stable_id("aihot", title, url),
                title=title,
                url=url,
                source=source,
                channel="aihot",
                category=category,
                published_at=published_at,
                score=score,
                tags=tags,
                reason=reason,
                raw=item,
            )
        )
    return out


def google_news_url(query: str, gn: dict[str, Any]) -> str:
    q = f"{query} when:{int(gn.get('window_days', 2))}d"
    params = {
        "q": q,
        "hl": gn.get("hl", "zh-CN"),
        "gl": gn.get("gl", "CN"),
        "ceid": gn.get("ceid", "CN:zh-Hans"),
    }
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(params)


def fetch_google_news(config: dict[str, Any], content_start: date, content_end: date) -> list[Candidate]:
    gn = config["google_news"]
    out: list[Candidate] = []
    for query in gn.get("queries", []):
        try:
            rss = request_text(google_news_url(query, gn))
            root = ET.fromstring(rss)
        except Exception as exc:
            print(f"warning: google news query failed: {query} ({exc})", file=sys.stderr)
            continue

        for item in root.findall("./channel/item"):
            title = (item.findtext("title") or "").strip()
            url = (item.findtext("link") or "").strip()
            source_node = item.find("source")
            source = (source_node.text if source_node is not None and source_node.text else "Google News").strip()
            pub_date = item.findtext("pubDate") or ""
            if not rss_matches_content_range(pub_date, content_start, content_end):
                continue
            published_at = parse_rss_date(pub_date)
            if not title or not url:
                continue
            score, tags, reason = score_candidate(title, source, "news")
            out.append(
                Candidate(
                    id=stable_id("google-news", title, url),
                    title=title,
                    url=url,
                    source=source,
                    channel="google-news",
                    category="news",
                    published_at=published_at,
                    score=score,
                    tags=tags,
                    reason=f"query={query}；{reason}",
                    raw={
                        "query": query,
                        "googleNewsUrl": url,
                    },
                )
            )
    return out


def dedupe(candidates: list[Candidate]) -> list[Candidate]:
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[Candidate] = []
    for item in sorted(candidates, key=lambda x: x.score, reverse=True):
        cu = canonical_url(item.url)
        nt = normalize_title(item.title)
        if cu in seen_urls or nt in seen_titles:
            continue
        seen_urls.add(cu)
        seen_titles.add(nt)
        unique.append(item)
    return unique


def format_date_label(day: date) -> str:
    return day.isoformat().replace("-", ".")


def coverage_label(content_start: date, content_end: date) -> str:
    if content_start == content_end:
        return format_date_label(content_start)
    return f"{format_date_label(content_start)}-{format_date_label(content_end)}"


def write_output(publish_date: date, content_start: date, content_end: date, candidates: list[Candidate]) -> Path:
    out_dir = PROJECT_ROOT / "daily" / publish_date.isoformat() / LINE_NAME / "work"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "candidates.json"
    data = {
        "line": LINE_NAME,
        "publishDate": publish_date.isoformat(),
        "contentDate": content_end.isoformat(),
        "contentStart": content_start.isoformat(),
        "contentEnd": content_end.isoformat(),
        "coverageLabel": coverage_label(content_start, content_end),
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "count": len(candidates),
        "items": [item.to_json() for item in candidates],
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--content-date", default=None, help="content date YYYY-MM-DD; default = publish date")
    parser.add_argument("--content-start", default=None, help="content range start YYYY-MM-DD")
    parser.add_argument("--content-end", default=None, help="content range end YYYY-MM-DD")
    args = parser.parse_args()

    publish_date = date.fromisoformat(args.date)
    if args.content_start or args.content_end:
        content_start = date.fromisoformat(args.content_start or args.content_end)
        content_end = date.fromisoformat(args.content_end or args.content_start)
    else:
        content_start = content_end = date.fromisoformat(args.content_date or args.date)
    if content_end < content_start:
        raise SystemExit("--content-end must be the same as or later than --content-start")

    config = load_config()
    candidates = []
    candidates.extend(fetch_aihot(config, content_start, content_end))
    candidates.extend(fetch_google_news(config, content_start, content_end))
    candidates = dedupe(candidates)

    out_path = write_output(publish_date, content_start, content_end, candidates)

    tagged = sum(1 for item in candidates if item.tags)
    print(f"OK {len(candidates)} candidates ({tagged} tagged reality-impact) -> {out_path}")
    for idx, item in enumerate(candidates[:12], 1):
        tag_text = ",".join(item.tags) or "-"
        print(safe_console(f"{idx:02d}. [{item.score:>2}] {tag_text:28s} {item.title}  ({item.source})"))


if __name__ == "__main__":
    main()
