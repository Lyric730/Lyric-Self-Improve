"""
Run the reusable 三分钟未来 daily production pipeline.

Default full pipeline:
  fetch -> enrich -> select -> copy -> screenshots -> keywords -> render -> export

Usage:
  python lines/three-minute-future/run_daily.py 2026-05-24 --vol 2
  python lines/three-minute-future/run_daily.py 2026-05-24 --stop-after selection
  python lines/three-minute-future/run_daily.py 2026-05-24 --start-at render
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
STEPS = ["fetch", "enrich", "select", "copy", "screenshots", "keywords", "render", "export"]


def work_dir_for(publish_date: str) -> Path:
    return PROJECT_ROOT / "daily" / publish_date / LINE_NAME / "work"


def final_path_for(publish_date: str) -> Path:
    return work_dir_for(publish_date) / "final.json"


def publish_dir_for(publish_date: str) -> Path:
    return PROJECT_ROOT / "daily" / publish_date / LINE_NAME / "publish"


def infer_content_date(publish_date: str, explicit_content_date: str | None) -> str:
    if explicit_content_date:
        return explicit_content_date
    publish_day = date.fromisoformat(publish_date)
    return (publish_day - timedelta(days=1)).isoformat()


def infer_content_range(args: argparse.Namespace) -> tuple[str, str]:
    if args.content_start or args.content_end:
        start = args.content_start or args.content_end
        end = args.content_end or args.content_start
        if date.fromisoformat(end) < date.fromisoformat(start):
            raise SystemExit("--content-end must be the same as or later than --content-start")
        return start, end
    content_date = infer_content_date(args.date, args.content_date)
    return content_date, content_date


def format_cmd(command: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in command)


def run(command: list[str], dry_run: bool) -> None:
    print(f"\n$ {format_cmd(command)}")
    if dry_run:
        return
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    subprocess.run(command, cwd=PROJECT_ROOT, env=env, check=True)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def existing_cover_image(publish_date: str) -> str:
    final_path = final_path_for(publish_date)
    if not final_path.exists():
        return ""
    try:
        path = str(read_json(final_path).get("cover", {}).get("imagePath", ""))
    except Exception:
        return ""
    return path if path and Path(path).exists() else ""


def fixed_cover_image() -> str:
    config_path = SCRIPT_DIR / "config" / "visual_asset_policy.json"
    if not config_path.exists():
        return ""
    try:
        raw = str(read_json(config_path).get("coverComposition", {}).get("fixedBackgroundPath", ""))
    except Exception:
        return ""
    if not raw:
        return ""
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (PROJECT_ROOT / path).resolve()
    return str(path) if path.exists() else ""


def infer_vol(publish_date: str) -> int:
    final_path = final_path_for(publish_date)
    if final_path.exists():
        try:
            vol = int(read_json(final_path).get("vol") or 0)
            if vol > 0:
                return vol
        except Exception:
            pass

    publish_day = date.fromisoformat(publish_date)
    used_vols: list[int] = []
    for path in (PROJECT_ROOT / "daily").glob(f"*/{LINE_NAME}/work/final.json"):
        try:
            day = date.fromisoformat(path.parts[-4])
        except Exception:
            continue
        if day >= publish_day:
            continue
        try:
            vol = int(read_json(path).get("vol") or 0)
        except Exception:
            vol = 0
        if vol > 0:
            used_vols.append(vol)
    return (max(used_vols) + 1) if used_vols else 1


def apply_cover_image(publish_date: str, cover_image: str) -> None:
    if not cover_image:
        return
    final_path = final_path_for(publish_date)
    if not final_path.exists():
        raise SystemExit(f"missing: {final_path} (run copy step first)")
    image_path = Path(cover_image).expanduser()
    if not image_path.is_absolute():
        image_path = (PROJECT_ROOT / image_path).resolve()
    if not image_path.exists():
        raise SystemExit(f"missing cover image: {image_path}")

    data = read_json(final_path)
    data.setdefault("cover", {})
    data["cover"]["imagePath"] = str(image_path)
    fixed_path = fixed_cover_image()
    data["cover"]["imageMode"] = (
        "fixed-reuse-background"
        if fixed_path and image_path.resolve() == Path(fixed_path).resolve()
        else "approved-cover"
    )
    data["cover"]["updatedAt"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    write_json(final_path, data)
    print(f"OK cover image -> {image_path}")


def require_cover_if_needed(publish_date: str, require_cover: bool) -> None:
    final_path = final_path_for(publish_date)
    if not final_path.exists():
        return
    cover = read_json(final_path).get("cover", {})
    image_path = str(cover.get("imagePath", ""))
    if image_path and Path(image_path).exists():
        return
    message = (
        "cover image missing; render_pages.py will use a fallback background. "
        "The standard pipeline should reuse the fixed cover in config/visual_asset_policy.json; "
        "pass --cover-image only when manually overriding it."
    )
    if require_cover:
        raise SystemExit(message)
    print(f"WARN {message}")


def step_range(start_at: str, stop_after: str) -> list[str]:
    start = STEPS.index(start_at)
    stop = STEPS.index(stop_after)
    if stop < start:
        raise SystemExit("--stop-after must be the same as or later than --start-at")
    return STEPS[start : stop + 1]


def command_for_step(args: argparse.Namespace, step: str, vol: int) -> list[str]:
    python = sys.executable
    if step == "fetch":
        command = [python, str(SCRIPT_DIR / "fetch_candidates.py"), args.date]
        if args.content_start or args.content_end:
            command.extend(["--content-start", args.content_start, "--content-end", args.content_end])
        elif args.content_date:
            command.extend(["--content-date", args.content_date])
        return command
    if step == "enrich":
        return [
            python,
            str(SCRIPT_DIR / "enrich_assets.py"),
            args.date,
            "--limit",
            str(args.enrich_limit),
            "--min-score",
            str(args.min_score),
        ]
    if step == "select":
        return [python, str(SCRIPT_DIR / "select_items.py"), args.date, "--limit", str(args.item_limit)]
    if step == "copy":
        return [python, str(SCRIPT_DIR / "generate_final.py"), args.date, "--vol", str(vol)]
    if step == "screenshots":
        return [python, str(SCRIPT_DIR / "capture_source_screenshots.py"), args.date]
    if step == "keywords":
        command = [python, str(SCRIPT_DIR / "search_keyword_images.py"), args.date]
        if args.prefer_keyword:
            command.append("--prefer-keyword")
        return command
    if step == "render":
        return [python, str(SCRIPT_DIR / "render_pages.py"), args.date]
    if step == "export":
        return [python, str(SCRIPT_DIR / "screenshot_pages.py"), args.date]
    raise AssertionError(step)


def write_run_report(args: argparse.Namespace, steps: list[str], vol: int, dry_run: bool) -> None:
    if dry_run:
        return
    work_dir = work_dir_for(args.date)
    work_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "line": LINE_NAME,
        "publishDate": args.date,
        "contentDate": args.content_date,
        "contentStart": args.content_start,
        "contentEnd": args.content_end,
        "vol": vol,
        "steps": steps,
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "outputs": {
            "work": str(work_dir),
            "publish": str(publish_dir_for(args.date)),
            "preview": str(publish_dir_for(args.date) / "live-preview.html"),
        },
    }
    write_json(work_dir / "run-report.json", report)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--content-date", help="content date YYYY-MM-DD; default = publish date minus 1 day")
    parser.add_argument("--content-start", help="content range start YYYY-MM-DD")
    parser.add_argument("--content-end", help="content range end YYYY-MM-DD")
    parser.add_argument("--vol", type=int, help="issue number; default keeps existing vol or infers next")
    parser.add_argument("--item-limit", type=int, default=15)
    parser.add_argument("--enrich-limit", type=int, default=30)
    parser.add_argument("--min-score", type=int, default=3)
    parser.add_argument("--cover-image", help="approved 1080x1080 cover background image path")
    parser.add_argument("--prefer-keyword", action="store_true", help="prefer keyword images over screenshots when filling gaps")
    parser.add_argument("--require-cover", action="store_true", help="fail before rendering if cover image is missing")
    parser.add_argument("--start-at", choices=STEPS, default="fetch")
    parser.add_argument("--stop-after", choices=STEPS, default="export")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    args.content_start, args.content_end = infer_content_range(args)
    args.content_date = args.content_end
    vol = args.vol or infer_vol(args.date)
    steps = step_range(args.start_at, args.stop_after)
    preserved_cover = args.cover_image or existing_cover_image(args.date) or fixed_cover_image()

    print(
        f"三分钟未来 pipeline publishDate={args.date} "
        f"contentDate={args.content_date} contentRange={args.content_start}..{args.content_end} "
        f"vol={vol:03d} steps={','.join(steps)}"
    )
    for step in steps:
        if step == "render" and not args.dry_run:
            require_cover_if_needed(args.date, args.require_cover)
        run(command_for_step(args, step, vol), args.dry_run)
        if step == "copy" and not args.dry_run:
            apply_cover_image(args.date, preserved_cover)

    write_run_report(args, steps, vol, args.dry_run)
    if args.dry_run:
        print("\nDRY-RUN only; no files were changed.")
    else:
        print(f"\nOK pipeline -> {publish_dir_for(args.date)}")
        print(f"Preview command: python lines\\three-minute-future\\serve_preview.py {args.date} --port 58417")


if __name__ == "__main__":
    main()
