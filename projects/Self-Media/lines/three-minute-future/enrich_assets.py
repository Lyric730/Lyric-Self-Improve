"""
Step 2: enrich candidates and collect image assets for 三分钟未来.

Input:
  daily/<date>/three-minute-future/work/candidates.json

Output:
  daily/<date>/three-minute-future/work/enriched.json
  daily/<date>/three-minute-future/work/assets/

Usage:
  python lines/three-minute-future/enrich_assets.py 2026-05-23 --limit 30
"""

from __future__ import annotations

import argparse
import html
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
USER_AGENT = "Mozilla/5.0 (compatible; self-media-three-minute-future/0.1)"
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MIN_IMAGE_WIDTH = 500
MIN_IMAGE_HEIGHT = 300


def fetch_bytes(url: str, timeout: int = 25) -> tuple[bytes, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        content_type = resp.headers.get("content-type", "")
        final_url = resp.geturl()
    return data, content_type, final_url


def fetch_html(url: str) -> tuple[str, str]:
    data, content_type, final_url = fetch_bytes(url)
    charset = "utf-8"
    m = re.search(r"charset=([^;\s]+)", content_type, re.I)
    if m:
        charset = m.group(1)
    return data.decode(charset, errors="replace"), final_url


def meta_content(page: str, key: str) -> str:
    patterns = [
        rf'<meta\s+[^>]*(?:property|name)=["\']{re.escape(key)}["\'][^>]*content=["\']([^"\']+)["\'][^>]*>',
        rf'<meta\s+[^>]*content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']{re.escape(key)}["\'][^>]*>',
    ]
    for pattern in patterns:
        m = re.search(pattern, page, re.I)
        if m:
            return html.unescape(m.group(1)).strip()
    return ""


def page_title(page: str) -> str:
    og = meta_content(page, "og:title")
    if og:
        return og
    m = re.search(r"<title[^>]*>(.*?)</title>", page, re.I | re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()


def page_description(page: str) -> str:
    for key in ("og:description", "description", "twitter:description"):
        value = meta_content(page, key)
        if value:
            return value
    return ""


def attr_value(tag: str, name: str) -> str:
    m = re.search(rf'\s{name}=["\']([^"\']+)["\']', tag, re.I)
    return html.unescape(m.group(1)).strip() if m else ""


def parse_int(value: str) -> int | None:
    m = re.search(r"\d+", value or "")
    return int(m.group(0)) if m else None


def page_image_candidates(page: str, base_url: str) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for key in ("og:image", "twitter:image", "twitter:image:src"):
        value = meta_content(page, key)
        if value:
            candidates.append(
                {
                    "url": urllib.parse.urljoin(base_url, value),
                    "source": key,
                    "width": None,
                    "height": None,
                    "score": 10_000,
                }
            )

    for tag in re.findall(r"<img\b[^>]*>", page, flags=re.I):
        raw_url = ""
        for name in ("data-original", "data-src", "data-lazy-src", "src"):
            raw_url = attr_value(tag, name)
            if raw_url:
                break
        if not raw_url or raw_url.startswith("data:"):
            continue
        if raw_url.lower().endswith(".svg"):
            continue
        width = parse_int(attr_value(tag, "width")) or parse_int(attr_value(tag, "w"))
        height = parse_int(attr_value(tag, "height")) or parse_int(attr_value(tag, "h"))
        if width and height and (width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT):
            continue
        area = (width or 0) * (height or 0)
        candidates.append(
            {
                "url": urllib.parse.urljoin(base_url, raw_url),
                "source": "img",
                "width": width,
                "height": height,
                "score": area,
            }
        )

    unique: dict[str, dict[str, Any]] = {}
    for item in sorted(candidates, key=lambda x: x.get("score", 0), reverse=True):
        unique.setdefault(item["url"], item)
    return list(unique.values())


def body_excerpt(page: str) -> str:
    page = re.sub(r"<script[\s\S]*?</script>", " ", page, flags=re.I)
    page = re.sub(r"<style[\s\S]*?</style>", " ", page, flags=re.I)
    paras = re.findall(r"<p[^>]*>([\s\S]*?)</p>", page, flags=re.I)
    cleaned: list[str] = []
    for para in paras:
        text = re.sub(r"<[^>]+>", " ", para)
        text = re.sub(r"\s+", " ", html.unescape(text)).strip()
        if len(text) >= 40:
            cleaned.append(text)
    return cleaned[0][:500] if cleaned else ""


def image_ext(url: str, content_type: str) -> str:
    lower = urllib.parse.urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if lower.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    if "gif" in content_type:
        return ".gif"
    return ".jpg"


def image_size(data: bytes) -> tuple[int, int] | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        width = int.from_bytes(data[16:20], "big")
        height = int.from_bytes(data[20:24], "big")
        return width, height

    if data.startswith(b"\xff\xd8"):
        idx = 2
        while idx + 9 < len(data):
            if data[idx] != 0xFF:
                idx += 1
                continue
            marker = data[idx + 1]
            idx += 2
            if marker in (0xD8, 0xD9):
                continue
            if idx + 2 > len(data):
                break
            length = int.from_bytes(data[idx:idx + 2], "big")
            if length < 2 or idx + length > len(data):
                break
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                height = int.from_bytes(data[idx + 3:idx + 5], "big")
                width = int.from_bytes(data[idx + 5:idx + 7], "big")
                return width, height
            idx += length

    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        # Minimal support for VP8X WebP dimensions.
        vp8x = data.find(b"VP8X")
        if vp8x != -1 and vp8x + 30 <= len(data):
            width = 1 + int.from_bytes(data[vp8x + 12:vp8x + 15], "little")
            height = 1 + int.from_bytes(data[vp8x + 15:vp8x + 18], "little")
            return width, height

    return None


def download_image(url: str, dest_base: Path) -> dict[str, Any]:
    if not url:
        return {"status": "missing"}
    try:
        data, content_type, final_url = fetch_bytes(url, timeout=25)
        if len(data) < 1000:
            return {"status": "too-small", "url": url}
        if len(data) > MAX_IMAGE_BYTES:
            return {"status": "too-large", "url": url, "bytes": len(data)}
        size = image_size(data)
        if size:
            width, height = size
            if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
                return {
                    "status": "too-small-dimensions",
                    "url": url,
                    "width": width,
                    "height": height,
                    "bytes": len(data),
                }
        ext = image_ext(final_url or url, content_type)
        dest = dest_base.with_suffix(ext)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return {
            "status": "downloaded",
            "url": url,
            "finalUrl": final_url,
            "path": str(dest),
            "bytes": len(data),
            "contentType": content_type,
            "width": size[0] if size else None,
            "height": size[1] if size else None,
        }
    except Exception as exc:
        return {"status": "error", "url": url, "error": str(exc)}


def download_best_image(candidates: list[dict[str, Any]], dest_base: Path) -> dict[str, Any]:
    if not candidates:
        return {"status": "missing"}
    attempts: list[dict[str, Any]] = []
    for candidate in candidates[:8]:
        info = download_image(candidate["url"], dest_base)
        info["candidateSource"] = candidate.get("source")
        attempts.append(dict(info))
        if info.get("status") == "downloaded":
            result = dict(info)
            result["attempts"] = attempts
            return result
    return {"status": "no-valid-image", "attempts": attempts}


def load_candidates(date: str) -> dict[str, Any]:
    path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "candidates.json"
    if not path.exists():
        raise SystemExit(f"missing: {path} (run fetch_candidates.py first)")
    return json.loads(path.read_text(encoding="utf-8"))


def enrich_item(item: dict[str, Any], assets_dir: Path) -> dict[str, Any]:
    out = dict(item)
    url = item.get("url", "")
    out["enrichment"] = {
        "status": "pending",
        "finalUrl": "",
        "ogTitle": "",
        "ogDescription": "",
        "ogImage": "",
        "bodyExcerpt": "",
        "image": {"status": "missing"},
    }

    try:
        page, final_url = fetch_html(url)
        title = page_title(page)
        description = page_description(page)
        image_candidates = page_image_candidates(page, final_url)
        excerpt = body_excerpt(page)
        image_info = download_best_image(image_candidates, assets_dir / item["id"])
        out["enrichment"] = {
            "status": "ok",
            "finalUrl": final_url,
            "ogTitle": title,
            "ogDescription": description,
            "ogImage": image_candidates[0]["url"] if image_candidates else "",
            "imageCandidates": image_candidates[:8],
            "bodyExcerpt": excerpt,
            "image": image_info,
        }
    except Exception as exc:
        out["enrichment"] = {
            "status": "error",
            "finalUrl": "",
            "ogTitle": "",
            "ogDescription": "",
            "ogImage": "",
            "bodyExcerpt": "",
            "image": {"status": "missing"},
            "error": str(exc),
        }
    return out


def write_output(date: str, source: dict[str, Any], items: list[dict[str, Any]]) -> Path:
    work_dir = PROJECT_ROOT / "daily" / date / LINE_NAME / "work"
    out_path = work_dir / "enriched.json"
    data = {
        "line": LINE_NAME,
        "publishDate": date,
        "contentDate": source.get("contentDate", date),
        "contentStart": source.get("contentStart", source.get("contentDate", date)),
        "contentEnd": source.get("contentEnd", source.get("contentDate", date)),
        "coverageLabel": source.get("coverageLabel", ""),
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "count": len(items),
        "items": items,
    }
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--min-score", type=int, default=3)
    args = parser.parse_args()

    data = load_candidates(args.date)
    items = [item for item in data.get("items", []) if int(item.get("score", 0)) >= args.min_score]
    items = items[: args.limit]

    work_dir = PROJECT_ROOT / "daily" / args.date / LINE_NAME / "work"
    assets_dir = work_dir / "assets"
    enriched = []
    for idx, item in enumerate(items, 1):
        result = enrich_item(item, assets_dir)
        enriched.append(result)
        status = result["enrichment"]["status"]
        image_status = result["enrichment"]["image"]["status"]
        print(f"{idx:02d}/{len(items):02d} {status:5s} image={image_status:10s} {item.get('title', '')[:56]}")

    out_path = write_output(args.date, data, enriched)
    image_count = sum(1 for item in enriched if item["enrichment"]["image"]["status"] == "downloaded")
    ok_count = sum(1 for item in enriched if item["enrichment"]["status"] == "ok")
    print(f"OK enriched={ok_count}/{len(enriched)} images={image_count}/{len(enriched)} -> {out_path}")


if __name__ == "__main__":
    main()
