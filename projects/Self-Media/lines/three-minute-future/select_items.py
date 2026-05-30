"""
Step 3: select publishable items for 三分钟未来.

Policy:
- Prefer foreign / overseas sources.
- De-prioritize domestic media aggregation.
- Down-rank healthcare and cap it by default.
- Reward usable images, but do not let image availability override topic quality.

Input:
  daily/<date>/three-minute-future/work/enriched.json

Output:
  daily/<date>/three-minute-future/work/selection.json

Usage:
  python lines/three-minute-future/select_items.py 2026-05-23 --limit 8
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from published_ledger import duplicate_reason, load_ledger


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = Path(__file__).resolve().parent / "config" / "selection_policy.json"

HEALTHCARE_CAP = 1

DOMESTIC_SOURCE_TERMS = [
    "IT之家",
    "搜狐",
    "新浪",
    "凤凰",
    "中国网",
    "中华网",
    "同花顺",
    "新华",
    "智源社区",
    "大健康派",
    "福州大学",
    "乌有之乡",
]

DOMESTIC_DOMAINS = [
    "ithome.com",
    "sohu.com",
    "sina.com.cn",
    "finance.sina.com.cn",
    "ifeng.com",
    "china.com",
    "10jqka.com.cn",
    "xinhuanet.com",
    "baidu.com",
]

FOREIGN_SOURCE_TERMS = [
    "Fortune",
    "Hacker News",
    "DataGuidance",
    "MarkTechPost",
    "The Verge",
    "CTIMES",
    "ByDrug",
    "Digital Today",
    "디지털투데이",
    "Samsung magazín",
    "orientaldaily.com.my",
    "Investing.com",
    "매일경제",
    "AASTOCKS",
    "Moomoo",
    "Bitget",
]

FOREIGN_DOMAINS = [
    "fortune.com",
    "dataguidance.com",
    "marktechpost.com",
    "theverge.com",
    "ctimes.com",
    "bydrug.pharmcube.com",
    "digitaltoday.co.kr",
    "news.ycombinator.com",
    "orientaldaily.com.my",
    "investing.com",
    "mk.co.kr",
    "aastocks.com",
    "moomoo.com",
    "bitget.com",
    "samsungmagazine.eu",
]

LOW_VALUE_TERMS = [
    "项目累计规模",
    "中标多个",
    "亮相",
    "大会",
    "授牌",
    "战略合作",
    "生态",
    "商业化落地",
    "创新实践",
    "医疗美容",
    "健康城",
]

STRONG_REALITY_TERMS = [
    "裁员",
    "叫停",
    "抗议",
    "法院",
    "库存",
    "工资",
    "工人",
    "员工",
    "机器人",
    "五角大楼",
    "国防",
    "学校",
    "奥斯卡",
    "成本",
    "替代",
    "翻车",
]


def load_enriched(date: str) -> dict[str, Any]:
    path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "enriched.json"
    if not path.exists():
        raise SystemExit(f"missing: {path} (run enrich_assets.py first)")
    return json.loads(path.read_text(encoding="utf-8"))


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def write_filtered(date: str, content_date: str, removed: list[dict[str, Any]]) -> Path:
    out_path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "filtered-published.json"
    data = {
        "line": LINE_NAME,
        "publishDate": date,
        "contentDate": content_date,
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "count": len(removed),
        "items": removed,
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def filter_published_duplicates(
    date: str,
    content_date: str,
    items: list[dict[str, Any]],
    allow_duplicates: bool,
) -> list[dict[str, Any]]:
    if allow_duplicates:
        write_filtered(date, content_date, [])
        return items

    ledger = load_ledger()
    kept: list[dict[str, Any]] = []
    removed: list[dict[str, Any]] = []
    for item in items:
        reason = duplicate_reason(item, ledger)
        if reason:
            removed.append({"reason": reason, "item": item})
        else:
            kept.append(item)
    write_filtered(date, content_date, removed)
    return kept


def host_of(url: str) -> str:
    try:
        return urllib.parse.urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def safe_console(text: str) -> str:
    encoding = sys.stdout.encoding or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def source_region(item: dict[str, Any]) -> str:
    source = item.get("source", "")
    final_url = item.get("enrichment", {}).get("finalUrl") or item.get("url", "")
    host = host_of(final_url)

    if contains_any(source, FOREIGN_SOURCE_TERMS) or any(domain in host for domain in FOREIGN_DOMAINS):
        return "foreign"
    if contains_any(source, DOMESTIC_SOURCE_TERMS) or any(domain in host for domain in DOMESTIC_DOMAINS):
        return "domestic"
    if re.search(r"[\u4e00-\u9fff]", source):
        return "domestic"
    return "unknown"


def image_bonus(item: dict[str, Any], policy: dict[str, Any]) -> tuple[int, str]:
    quality = policy.get("qualityWeights", {})
    image = item.get("enrichment", {}).get("image", {})
    if image.get("status") != "downloaded":
        return 0, "无有效图"
    width = image.get("width") or 0
    height = image.get("height") or 0
    if height >= width:
        return int(quality.get("verticalImage", 2)), "有竖向可用图"
    return int(quality.get("horizontalImage", 1)), "有横向可用图"


def score_item(item: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    title = item.get("title", "")
    tags = item.get("tags", [])
    base = int(item.get("score", 0))
    score = base
    reasons = [f"基础分 {base}"]

    region = source_region(item)
    region_weights = policy.get("regionWeights", {})
    if region == "foreign":
        bonus = int(region_weights.get("foreign", 3))
        score += bonus
        reasons.append(f"海外/国外来源 +{bonus}")
    elif region == "domestic":
        penalty = int(region_weights.get("domestic", -2))
        score += penalty
        reasons.append(f"国内媒体来源 {penalty}")
    else:
        bonus = int(region_weights.get("unknown", 0))
        score += bonus
        reasons.append(f"来源区域未知 {bonus:+d}")

    quality = policy.get("qualityWeights", {})
    tag_weights = policy.get("tagWeights", {})
    for tag in tags:
        if tag in tag_weights:
            weight = int(tag_weights[tag])
            score += weight
            reasons.append(f"{tag} 标签权重 {weight:+d}")

    if not tags:
        weight = int(quality.get("noRealityTag", -4))
        score += weight
        reasons.append(f"未命中现实影响标签 {weight:+d}")

    if contains_any(title, LOW_VALUE_TERMS):
        weight = int(quality.get("lowValuePressRelease", -2))
        score += weight
        reasons.append(f"偏通稿/行业稿 {weight:+d}")

    if contains_any(title, STRONG_REALITY_TERMS):
        weight = int(quality.get("strongRealityConflict", 2))
        score += weight
        reasons.append(f"现实冲突/场景强 +{weight}")

    bonus, image_reason = image_bonus(item, policy)
    score += bonus
    reasons.append(f"{image_reason} {'+' + str(bonus) if bonus else '+0'}")

    channel = item.get("channel", "")
    source_weights = policy.get("sourceWeights", {})
    if channel in source_weights:
        weight = int(source_weights[channel].get("bonus", 0))
        score += weight
        reasons.append(f"{channel} 来源权重 {weight:+d}")

    return {
        "selectionScore": score,
        "sourceRegion": region,
        "selectionReasons": reasons,
    }


def selection_sort_key(item: dict[str, Any]) -> tuple[int, int, int]:
    region_rank = {"foreign": 2, "unknown": 1, "domestic": 0}.get(item.get("sourceRegion"), 0)
    channel_rank = {"aihot": 1, "google-news": 0}.get(item.get("channel"), 0)
    return int(item.get("selectionScore", 0)), region_rank, channel_rank


def dedupe_topic(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen_clusters: set[str] = set()
    seen_source_tags: set[tuple[str, str]] = set()
    unique: list[dict[str, Any]] = []
    cluster_terms = [
        ("starbucks-ai-inventory", ["星巴克"]),
        ("ai-layoffs", ["裁员"]),
        ("ai-healthcare", ["医疗", "医院", "医助"]),
        ("humanoid-robot-id", ["机器人", "身份证"]),
        ("deepseek-hardware", ["DeepSeek", "硬件"]),
        ("pope-ai-ethics", ["教皇"]),
        ("pope-ai-ethics", ["Anthropic", "教皇"]),
    ]
    for item in items:
        title = item.get("title", "")
        cluster = ""
        for name, terms in cluster_terms:
            if all(term in title for term in terms):
                cluster = name
                break
        if cluster and cluster in seen_clusters:
            continue
        if cluster:
            seen_clusters.add(cluster)

        source = item.get("source", "")
        if source.startswith("X") or "@" in source:
            for tag in item.get("tags", []):
                if tag in {"hardware", "robotics", "labor"}:
                    source_tag = (source, tag)
                    if source_tag in seen_source_tags:
                        cluster = f"same-source-{tag}"
                        break
                    seen_source_tags.add(source_tag)
            if cluster.startswith("same-source-"):
                continue
        unique.append(item)
    return unique


def mix_bucket(item: dict[str, Any]) -> str:
    if item.get("channel") == "aihot":
        return "aihot"
    if item.get("sourceRegion") == "domestic":
        return "domesticMedia"
    return "externalNews"


def target_mix(limit: int, policy: dict[str, Any]) -> dict[str, int]:
    if limit == 15:
        mix = policy.get("sourceMixForFifteenItems", {})
        return {
            "aihot": int(mix.get("aihot", 8)),
            "externalNews": int(mix.get("externalNews", 5)),
            "domesticMedia": int(mix.get("domesticMedia", 2)),
        }
    if limit != 8:
        return {}
    mix = policy.get("sourceMixForEightItems", {})
    return {
        "aihot": int(mix.get("aihot", 4)),
        "externalNews": int(mix.get("externalNews", 3)),
        "domesticMedia": int(mix.get("domesticMedia", 1)),
    }


def can_select(
    item: dict[str, Any],
    tag_counts: dict[str, int],
    region_counts: dict[str, int],
    channel_counts: dict[str, int],
    policy: dict[str, Any],
) -> bool:
    tags = item.get("tags", [])
    tag_caps = policy.get("tagCaps", {"healthcare": HEALTHCARE_CAP})
    source_caps = policy.get("sourceCaps", {})
    channel_policy = policy.get("sourceWeights", {})

    if not tags and not policy.get("allowNoRealityTagFallback", False):
        item.setdefault("selectionReasons", []).append("未命中现实影响标签，跳过")
        return False

    for tag in tags:
        cap = tag_caps.get(tag)
        if cap is not None and tag_counts.get(tag, 0) >= int(cap):
            item.setdefault("selectionReasons", []).append(f"{tag} 已达本期上限，跳过")
            return False

    bucket = item.get("mixBucket")
    bucket_cap = source_caps.get(bucket)
    if bucket_cap is not None and channel_counts.get(f"bucket:{bucket}", 0) >= int(bucket_cap):
        item.setdefault("selectionReasons", []).append(f"{bucket} 来源已达本期上限，跳过")
        return False

    region = item.get("sourceRegion")
    region_cap = source_caps.get(region)
    if region_cap is not None and region_counts.get(region, 0) >= int(region_cap):
        item.setdefault("selectionReasons", []).append(f"{region} 来源已达本期上限，跳过")
        return False

    channel = item.get("channel", "")
    channel_cap = channel_policy.get(channel, {}).get("maxSelected")
    if channel_cap is not None and channel_counts.get(channel, 0) >= int(channel_cap):
        item.setdefault("selectionReasons", []).append(f"{channel} 已达本期上限，跳过")
        return False

    return True


def record_selection(
    item: dict[str, Any],
    tag_counts: dict[str, int],
    region_counts: dict[str, int],
    channel_counts: dict[str, int],
) -> None:
    for tag in item.get("tags", []):
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    region = item.get("sourceRegion")
    region_counts[region] = region_counts.get(region, 0) + 1
    channel = item.get("channel", "")
    if channel:
        channel_counts[channel] = channel_counts.get(channel, 0) + 1
    bucket = item.get("mixBucket")
    if bucket:
        key = f"bucket:{bucket}"
        channel_counts[key] = channel_counts.get(key, 0) + 1


def select_items(items: list[dict[str, Any]], limit: int, policy: dict[str, Any]) -> list[dict[str, Any]]:
    scored = []
    for item in items:
        enriched = dict(item)
        enriched.update(score_item(item, policy))
        scored.append(enriched)

    scored.sort(key=selection_sort_key, reverse=True)
    scored = dedupe_topic(scored)

    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    tag_counts: dict[str, int] = {}
    region_counts: dict[str, int] = {}
    channel_counts: dict[str, int] = {}
    mix = target_mix(limit, policy)

    for bucket in ("aihot", "externalNews", "domesticMedia"):
        target = mix.get(bucket, 0)
        while sum(1 for item in selected if item.get("mixBucket") == bucket) < target:
            candidate = None
            for item in scored:
                item_id = item.get("id") or item.get("url") or item.get("title")
                if item_id in selected_ids:
                    continue
                item["mixBucket"] = mix_bucket(item)
                if item["mixBucket"] != bucket:
                    continue
                if can_select(item, tag_counts, region_counts, channel_counts, policy):
                    candidate = item
                    break
            if candidate is None:
                break
            selected.append(candidate)
            selected_ids.add(candidate.get("id") or candidate.get("url") or candidate.get("title"))
            candidate.setdefault("selectionReasons", []).append(f"命中默认配比桶：{bucket}")
            record_selection(candidate, tag_counts, region_counts, channel_counts)

    for item in scored:
        if len(selected) >= limit:
            break
        item_id = item.get("id") or item.get("url") or item.get("title")
        if item_id in selected_ids:
            continue
        item["mixBucket"] = mix_bucket(item)
        if not can_select(item, tag_counts, region_counts, channel_counts, policy):
            continue
        selected.append(item)
        selected_ids.add(item_id)
        item.setdefault("selectionReasons", []).append("配额不足后的高分回填")
        record_selection(item, tag_counts, region_counts, channel_counts)

    selected.sort(key=selection_sort_key, reverse=True)

    if selected:
        selected[0]["role"] = "cover"
        for item in selected[1:]:
            item["role"] = "inside"
    return selected


def write_output(
    date: str,
    content_date: str,
    content_start: str,
    content_end: str,
    coverage_label: str,
    selected: list[dict[str, Any]],
    all_scored: list[dict[str, Any]],
    policy: dict[str, Any],
) -> Path:
    out_path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "selection.json"
    data = {
        "line": LINE_NAME,
        "publishDate": date,
        "contentDate": content_date,
        "contentStart": content_start,
        "contentEnd": content_end,
        "coverageLabel": coverage_label,
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "policy": policy,
        "count": len(selected),
        "items": selected,
        "topCandidates": all_scored[:30],
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--allow-published-duplicates", action="store_true")
    args = parser.parse_args()

    data = load_enriched(args.date)
    policy = load_policy()
    all_items = data.get("items", [])
    content_date = data.get("contentDate", args.date)
    content_start = data.get("contentStart", content_date)
    content_end = data.get("contentEnd", content_date)
    coverage_label = data.get("coverageLabel", "")
    all_items = filter_published_duplicates(args.date, content_date, all_items, args.allow_published_duplicates)
    scored = []
    for item in all_items:
        enriched = dict(item)
        enriched.update(score_item(item, policy))
        scored.append(enriched)
    scored.sort(key=selection_sort_key, reverse=True)

    selected = select_items(all_items, args.limit, policy)
    out_path = write_output(args.date, content_date, content_start, content_end, coverage_label, selected, scored, policy)

    print(f"OK selected={len(selected)} -> {out_path}")
    for idx, item in enumerate(selected, 1):
        tags = ",".join(item.get("tags", [])) or "-"
        region = item.get("sourceRegion", "?")
        line = f"{idx:02d}. [{item['selectionScore']:>2}] {region:8s} {tags:20s} {item['title']}"
        print(safe_console(line))


if __name__ == "__main__":
    main()
