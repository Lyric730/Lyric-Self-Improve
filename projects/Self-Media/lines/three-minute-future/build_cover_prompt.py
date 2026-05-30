"""
Build a compressed cover image prompt for 三分钟未来.

Input:
  daily/<date>/three-minute-future/work/final.json

Output:
  daily/<date>/three-minute-future/work/cover-prompt.txt

Usage:
  python lines/three-minute-future/build_cover_prompt.py 2026-05-26 --write-final
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = Path(__file__).resolve().parent / "config" / "visual_asset_policy.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def item_text(item: dict[str, Any]) -> str:
    return " ".join(
        str(item.get(key, ""))
        for key in ("title", "fact", "thought", "rawTitle", "source")
    )


def all_tags(items: list[dict[str, Any]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for item in items:
        counter.update(str(tag) for tag in item.get("tags", []))
    return counter


def has_text(items: list[dict[str, Any]], *terms: str) -> bool:
    joined = "\n".join(item_text(item) for item in items)
    return any(term in joined for term in terms)


def derive_plan(items: list[dict[str, Any]]) -> dict[str, Any]:
    tags = all_tags(items)

    if tags["robotics"] >= 4:
        core = "AI is moving from software into physical labor, logistics, public service, and institutional responsibility."
        primary = (
            "a harsh industrial logistics corridor with conveyor belts, floor markings, "
            "empty worker zones, equipment shadows, and public-space control gates"
        )
    elif tags["labor"] or tags["policy"] or tags["law"]:
        core = "AI pressure is becoming a labor, policy, and institutional responsibility problem."
        primary = (
            "a severe public administration workspace with blank folders, hard desk edges, "
            "worker shadows, access gates, and cold machine light"
        )
    elif tags["healthcare"]:
        core = "AI is entering medical workflows where efficiency and responsibility collide."
        primary = (
            "a cropped clinical operations room with instrument trays, diagnostic glow, "
            "machine arms as shadows, and blank patient files"
        )
    elif tags["retail"]:
        core = "AI is entering retail operations and exposing the limits of automation."
        primary = (
            "a dark retail stockroom with shelves, inventory boxes, scanning light, "
            "back-office desk fragments, and hard diagonal shadows"
        )
    else:
        core = "AI is leaving the screen and pressing into real institutions."
        primary = (
            "a severe industrial control room with machine panels, access doors, "
            "blank institutional papers, and empty workstations"
        )

    fragments: list[str] = []
    if tags["policy"] or tags["labor"] or tags["law"] or has_text(items, "加州", "裁员", "工人", "高管"):
        fragments.append("public administration desk, stamped blank folders, and worker silhouettes")
    if has_text(items, "WorkOS", "auth.md", "身份", "权限"):
        fragments.append("blank access cards, permission gates, and locked server doors")
    if tags["retail"] or has_text(items, "星巴克", "库存", "门店"):
        fragments.append("dark retail stockroom shelves and barcode-like blank strips")
    if tags["healthcare"] or has_text(items, "医疗"):
        fragments.append("cropped hospital instrument tray and diagnostic glow")
    if tags["hardware"] or has_text(items, "算力", "硬件"):
        fragments.append("server racks, cable shadows, and machine-room ventilation")

    # Keep only three secondary fragments. More than that has repeatedly pushed
    # the model toward generic information boards instead of a poster.
    fragments = fragments[:3]
    if len(fragments) < 2:
        fragments.extend(
            [
                "blank access cards and locked server doors",
                "hard-cropped machine-room panels and cold industrial light",
            ][: 2 - len(fragments)]
        )

    return {
        "coreIdea": core,
        "primaryVisualAnchor": primary,
        "secondaryFragments": fragments,
    }


def build_prompt(plan: dict[str, Any]) -> str:
    fragments = "; ".join(plan["secondaryFragments"])
    return "\n".join(
        [
            "Asset / size: 1080x1080 square cover background only. No embedded typography; all Chinese title, date, VOL, and account text will be added later.",
            f"Core idea: {plan['coreIdea']}",
            f"Primary visual anchor: {plan['primaryVisualAnchor']}. It dominates the composition but must not become a single-event illustration.",
            f"Secondary fragments: {fragments}. These appear only as cut panels, shadows, cropped evidence, or background fragments.",
            "Style: early Soviet Constructivist industrial news poster, avant-garde photomontage, severe editorial warning mood, aggressive diagonal asymmetry, sharp triangular planes, hard black shadows, dirty off-white paper slabs, acid-lime and warning-red accents, rough screenprint texture, halftone grain, slight cyan-magenta print misregistration, matte paper.",
            "Composition: main force from upper-left to lower-right; engineered and tense; leave a dark title-safe zone in the upper-middle, a clean right-middle zone for date and VOL, and darker lower zones for short hooks.",
            "Avoid: readable words, letters, logos, brand marks, smiling people, cute neon cyberpunk, glossy 3D render, glowing AI face, futuristic skyline, classroom poster, office slideshow, equal small icons, clean corporate deck.",
        ]
    )


def forbidden_hits(prompt: str, policy: dict[str, Any]) -> list[str]:
    terms = (
        policy.get("coverComposition", {})
        .get("promptGuardrails", {})
        .get("avoidTermsInPrompt", [])
    )
    hits = []
    for term in terms:
        text = str(term)
        pattern = re.escape(text)
        if re.fullmatch(r"[A-Za-z]+(?:\s+[A-Za-z]+)*", text):
            pattern = r"\b" + re.sub(r"\\\s+", r"\\s+", pattern) + r"\b"
        if re.search(pattern, prompt, flags=re.IGNORECASE):
            hits.append(text)
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--write-final", action="store_true", help="store prompt path and plan into final.json")
    args = parser.parse_args()

    final_path = PROJECT_ROOT / "daily" / args.date / LINE_NAME / "work" / "final.json"
    final = load_json(final_path)
    policy = load_json(POLICY_PATH)

    plan = derive_plan(final.get("items", []))
    prompt = build_prompt(plan)
    hits = forbidden_hits(prompt, policy)
    if hits:
        raise SystemExit(f"cover prompt contains forbidden trigger terms: {', '.join(hits)}")

    out_path = final_path.parent / "cover-prompt.txt"
    out_path.write_text(prompt + "\n", encoding="utf-8")

    if args.write_final:
        cover = final.setdefault("cover", {})
        cover["promptPath"] = str(out_path)
        cover["promptPlan"] = plan
        cover["promptBrief"] = (
            "封面实际生图 prompt 已压缩并写入 cover-prompt.txt；"
            "固定构成主义工业新闻海报语言，动态使用当期主视觉锚点和 2-3 个辅助碎片。"
        )
        final_path.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK cover prompt -> {out_path}")


if __name__ == "__main__":
    main()
