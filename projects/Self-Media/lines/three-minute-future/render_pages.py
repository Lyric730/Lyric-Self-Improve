"""
Render Three-Minute Future cover and inside pages from final.json.

Input:
  daily/<date>/three-minute-future/work/final.json

Output:
  daily/<date>/three-minute-future/<out-dir>/html/*.html
  daily/<date>/three-minute-future/<out-dir>/live-preview.html
  daily/<date>/three-minute-future/<out-dir>/index.html

Usage:
  python lines/three-minute-future/render_pages.py 2026-05-23
  python lines/three-minute-future/render_pages.py 2026-05-23 --out-dir publish-next
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path
from string import Template
from typing import Any


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LINE_ROOT = Path(__file__).resolve().parent
TEMPLATE_DIR = LINE_ROOT / "templates"
STYLE_PATH = LINE_ROOT / "styles" / "three-minute-future.css"
VISUAL_POLICY_PATH = LINE_ROOT / "config" / "visual_asset_policy.json"

COVER_WIDTH = 1080
COVER_HEIGHT = 1080
INSIDE_WIDTH = 1080
INSIDE_HEIGHT = 1416

TAG_THEME = {
    "labor": ("#cfff00", "#00e5ff", "WORK"),
    "law": ("#ff2c7a", "#cfff00", "RULE"),
    "retail": ("#cfff00", "#ff2c7a", "STORE"),
    "robotics": ("#00e5ff", "#cfff00", "ROBOT"),
    "hardware": ("#ff2c7a", "#00e5ff", "CHIP"),
    "defense": ("#cfff00", "#ff2c7a", "DEFENSE"),
    "healthcare": ("#00e5ff", "#cfff00", "HEALTH"),
}

HOT_TERMS = [
    "更贵",
    "裁员",
    "翻车",
    "机器人",
    "身份证",
    "绿卡",
    "硬件",
    "算力",
    "账单",
    "库存",
    "生死",
    "小区",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_final(date: str) -> dict[str, Any]:
    path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "final.json"
    if not path.exists():
        raise SystemExit(f"missing: {path} (run generate_final.py first)")
    return load_json(path)


def load_visual_policy() -> dict[str, Any]:
    if not VISUAL_POLICY_PATH.exists():
        return {}
    return load_json(VISUAL_POLICY_PATH)


def load_style() -> str:
    if not STYLE_PATH.exists():
        raise SystemExit(f"missing style: {STYLE_PATH}")
    return STYLE_PATH.read_text(encoding="utf-8")


def render_template(name: str, **context: Any) -> str:
    path = TEMPLATE_DIR / name
    if not path.exists():
        raise SystemExit(f"missing template: {path}")
    template = Template(path.read_text(encoding="utf-8"))
    return template.safe_substitute({k: str(v) for k, v in context.items()})


def data_uri(path: str) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.exists():
        return ""
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    encoded = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def css_url_data_uri(path: str) -> str:
    uri = data_uri(path)
    return uri or ""


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def html_text(value: Any) -> str:
    return esc(value).replace("\n", "<br>")


def theme_for(item: dict[str, Any]) -> tuple[str, str, str]:
    for tag in item.get("tags", []):
        if tag in TAG_THEME:
            return TAG_THEME[tag]
    return "#cfff00", "#00e5ff", "AI"


def inside_title_class(title: str) -> str:
    length = len(title.replace(" ", ""))
    if length >= 17:
        return "title-long"
    if length >= 13:
        return "title-mid"
    return ""


def highlight_hook(text: str) -> str:
    escaped = esc(text)
    for term in HOT_TERMS:
        escaped_term = esc(term)
        if escaped_term in escaped:
            return escaped.replace(escaped_term, f'<span class="hot">{escaped_term}</span>', 1)
    return escaped


def estimate_duration_text(item_count: int) -> str:
    seconds = 4 + item_count * 14 + max(item_count - 1, 0) * 0.4 + 3
    rounded = int(round(seconds / 5) * 5)
    minutes, secs = divmod(rounded, 60)
    return f"{minutes}'{secs:02d}\""


def coverage_label(final: dict[str, Any]) -> str:
    explicit = final.get("coverageLabel") or final.get("dateRange")
    if explicit:
        return esc(explicit)
    start = final.get("coverageStart") or final.get("contentStart")
    end = final.get("coverageEnd") or final.get("contentEnd")
    if start and end:
        return f"({esc(start)}-{esc(end)})"
    return esc(final.get("dateLabel", ""))


def cover_context(final: dict[str, Any], css: str) -> dict[str, Any]:
    items = list(final.get("items", []))
    first = items[0] if items else {}
    cover = final.get("cover", {})
    cover_bg = css_url_data_uri(cover.get("imagePath", "")) or css_url_data_uri(first.get("imagePath", ""))
    title = cover.get("title") or final.get("name") or "三分钟未来"
    subtitle = cover.get("tagline") or "AI 资讯 × 实时热点"
    lead = cover.get("subtitle") or cover.get("topic") or first.get("title", "")
    hooks = items[1:3]
    while len(hooks) < 2:
        hooks.append(first)

    return {
        "css": css,
        "page_title": f"{title} · 封面",
        "cover_bg": cover_bg,
        "cover_title": esc(title),
        "cover_subtitle": esc(subtitle),
        "vol": f"{int(final.get('vol') or 0):02d}" if str(final.get("vol", "")).isdigit() else esc(final.get("vol", "")),
        "date_range": coverage_label(final),
        "lead_hook": highlight_hook(str(lead)),
        "sub_hook_1": highlight_hook(str(hooks[0].get("title", ""))),
        "sub_hook_2": highlight_hook(str(hooks[1].get("title", ""))),
        "report_count": str(len(items)),
        "estimated_duration": estimate_duration_text(len(items)),
        "account": esc(final.get("account", "")),
    }


def item_context(final: dict[str, Any], item: dict[str, Any], css: str) -> dict[str, Any]:
    visual_path = item.get("imagePath") or item.get("keywordImagePath") or item.get("sourceScreenshotPath") or ""
    image = data_uri(visual_path)
    accent_a, accent_b, _ = theme_for(item)
    if image:
        visual = f'<img src="{image}" alt="">'
    else:
        visual = '<div class="fallback-art"></div>'

    title = str(item.get("title", ""))
    return {
        "css": css,
        "page_title": f"{final.get('name', '三分钟未来')} · {title}",
        "accent_a": accent_a,
        "accent_b": accent_b,
        "date_label": esc(final.get("dateLabel", "")),
        "visual": visual,
        "source": esc(item.get("source", "")),
        "title": esc(title),
        "title_class": inside_title_class(title),
        "fact": html_text(item.get("fact", "")),
        "thought": html_text(item.get("thought", "")),
        "account": esc(final.get("account", "")),
    }


def preview_nav_label(item: dict[str, Any]) -> str:
    title = str(item.get("title", "")).strip()
    short_title = title[:8] + ("..." if len(title) > 8 else "")
    return f"{int(item.get('index', 0)):02d} {short_title}"


def preview_pages(final: dict[str, Any]) -> list[dict[str, Any]]:
    pages = [
        {
            "label": "封面",
            "href": "html/00-cover.html",
            "width": COVER_WIDTH,
            "height": COVER_HEIGHT,
        }
    ]
    for item in final.get("items", []):
        index = int(item["index"])
        pages.append(
            {
                "label": preview_nav_label(item),
                "href": f"html/{index:02d}-{item['id']}.html",
                "width": INSIDE_WIDTH,
                "height": INSIDE_HEIGHT,
            }
        )
    return pages


def render(date: str, out_dir: str = "publish") -> Path:
    final = load_final(date)
    load_visual_policy()  # Kept as a future hook; current template is clarity-first by default.
    css = load_style()

    publish_dir = PROJECT_ROOT / "daily" / date / LINE_NAME / out_dir
    html_dir = publish_dir / "html"
    html_dir.mkdir(parents=True, exist_ok=True)

    (html_dir / "00-cover.html").write_text(
        render_template("cover.html.tmpl", **cover_context(final, css)),
        encoding="utf-8",
    )

    for item in final["items"]:
        path = html_dir / f"{int(item['index']):02d}-{item['id']}.html"
        path.write_text(
            render_template("item.html.tmpl", **item_context(final, item, css)),
            encoding="utf-8",
        )

    title = esc(final.get("cover", {}).get("title") or final.get("name", "三分钟未来"))
    pages_json = json.dumps(preview_pages(final), ensure_ascii=False, indent=6)
    (publish_dir / "live-preview.html").write_text(
        render_template("live-preview.html.tmpl", title=title, pages_json=pages_json),
        encoding="utf-8",
    )
    (publish_dir / "index.html").write_text(
        render_template("index.html.tmpl", title=title),
        encoding="utf-8",
    )
    return html_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--out-dir", default="publish", help="output directory under the daily line folder")
    args = parser.parse_args()

    html_dir = render(args.date, args.out_dir)
    print(f"OK html -> {html_dir}")


if __name__ == "__main__":
    main()
