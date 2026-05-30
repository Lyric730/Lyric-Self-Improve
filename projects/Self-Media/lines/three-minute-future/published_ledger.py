from __future__ import annotations

import hashlib
import json
import re
import urllib.parse
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = PROJECT_ROOT / "daily" / "_state" / LINE_NAME / "published-ledger.json"

TOPIC_PATTERNS = [
    ("ai-cost-labor", ["微软", "人工", "成本"]),
    ("ai-cost-labor", ["AI", "人工", "贵"]),
    ("meta-layoffs", ["Meta", "裁员"]),
    ("starbucks-ai-inventory", ["星巴克", "库存"]),
    ("robot-delivery-busan", ["高尔夫球包", "机器人"]),
    ("humanoid-robot-id", ["机器人", "身份证"]),
    ("openai-green-card", ["OpenAI", "绿卡"]),
    ("entry-level-hiring", ["初级", "招聘"]),
    ("robot-phone", ["机器人手机"]),
    ("robot-phone", ["Robot Phone"]),
    ("open-harmony-robots", ["鸿蒙", "机器人操作系统"]),
    ("open-harmony-robots", ["M-Robots"]),
    ("deepseek-hardware", ["DeepSeek", "硬件"]),
    ("ai-workflow-labor", ["AI选题", "工作流"]),
    ("ai-workplace-product", ["MARVIS"]),
    ("ai-healthcare", ["医疗", "医院"]),
    ("ai-healthcare", ["患者数据"]),
    ("ai-oscar-media", ["奥斯卡", "AI"]),
]


def normalize_text(value: str) -> str:
    text = (value or "").lower()
    text = re.sub(r"https?://\S+", "", text)
    return re.sub(r"[\s\W_]+", "", text, flags=re.UNICODE)


def normalize_url(value: str) -> str:
    if not value:
        return ""
    parsed = urllib.parse.urlparse(value)
    host = parsed.netloc.lower().replace("www.", "")
    path = parsed.path.rstrip("/")
    return urllib.parse.urlunparse((parsed.scheme.lower(), host, path, "", "", ""))


def searchable_text(item: dict[str, Any]) -> str:
    fields = (
        "title",
        "sourceTitle",
        "rawTitle",
        "displayTitle",
        "fact",
        "thought",
        "summary",
    )
    return " ".join(str(item.get(field, "")) for field in fields)


def topic_key(item: dict[str, Any]) -> str:
    text = searchable_text(item)
    lowered = text.lower()
    for key, terms in TOPIC_PATTERNS:
        if all(term.lower() in lowered for term in terms):
            return key
    normalized = normalize_text(text)
    return hashlib.sha1(normalized[:120].encode("utf-8")).hexdigest()[:12] if normalized else ""


def image_key(item: dict[str, Any]) -> str:
    image = item.get("image") or item.get("enrichment", {}).get("image", {})
    values = [
        item.get("imagePath", ""),
        item.get("keywordImagePath", ""),
        image.get("sourceUrl", ""),
        image.get("url", ""),
        image.get("path", ""),
    ]
    for value in values:
        if value:
            return normalize_url(str(value)) or normalize_text(str(value))
    return ""


def load_ledger(path: Path = LEDGER_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"line": LINE_NAME, "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(data: dict[str, Any], path: Path = LEDGER_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fingerprint(item: dict[str, Any]) -> dict[str, str]:
    final_url = item.get("enrichment", {}).get("finalUrl") or item.get("url", "")
    return {
        "url": normalize_url(str(final_url)),
        "title": normalize_text(str(item.get("title", ""))),
        "sourceTitle": normalize_text(str(item.get("rawTitle") or item.get("sourceTitle") or "")),
        "topicKey": topic_key(item),
        "imageKey": image_key(item),
    }


def duplicate_reason(item: dict[str, Any], ledger: dict[str, Any]) -> str | None:
    current = fingerprint(item)
    for prior in ledger.get("items", []):
        prior_url = normalize_url(str(prior.get("url", "")))
        prior_title = normalize_text(str(prior.get("title", "")))
        prior_source_title = normalize_text(str(prior.get("sourceTitle", "")))
        prior_topic = str(prior.get("topicKey", ""))
        prior_image = str(prior.get("imageKey", ""))

        if current["url"] and current["url"] == prior_url:
            return "same-url"
        if current["title"] and current["title"] in {prior_title, prior_source_title}:
            return "same-title"
        if current["sourceTitle"] and current["sourceTitle"] in {prior_title, prior_source_title}:
            return "same-source-title"
        if current["topicKey"] and current["topicKey"] == prior_topic:
            return f"same-topic:{current['topicKey']}"
        if current["imageKey"] and current["imageKey"] == prior_image:
            return "same-image"
    return None


def ledger_entry(
    item: dict[str, Any],
    publish_date: str,
    content_date: str,
    vol: int,
) -> dict[str, Any]:
    final_url = item.get("enrichment", {}).get("finalUrl") or item.get("url", "")
    source_title = item.get("rawTitle") or item.get("sourceTitle") or item.get("title", "")
    return {
        "line": LINE_NAME,
        "publishDate": publish_date,
        "contentDate": content_date,
        "vol": vol,
        "title": item.get("title", ""),
        "sourceTitle": source_title,
        "url": final_url,
        "source": item.get("source", ""),
        "topicKey": topic_key(item),
        "imageKey": image_key(item),
    }
