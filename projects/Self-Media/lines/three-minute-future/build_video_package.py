"""
Build video handoff assets for Three-Minute Future.

Input:
  daily/<date>/three-minute-future/work/final.json
  daily/<date>/three-minute-future/publish/images/*.png

Output:
  daily/<date>/three-minute-future/work/video/episode.video.json
  daily/<date>/three-minute-future/work/video/voiceover-script.md
  daily/<date>/three-minute-future/work/video/tts-input.txt
  daily/<date>/three-minute-future/work/video/assets/*.png

Usage:
  python lines/three-minute-future/build_video_package.py 2026-05-26
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FPS = 30
CANVAS = {"width": 1080, "height": 1920, "fps": FPS}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def clean_text(value: Any) -> str:
    text = str(value or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def text_units(text: str) -> int:
    return len(re.sub(r"[\s，。！？、；：,.!?;:\"'“”‘’（）()《》<>-]", "", text))


def estimate_duration_seconds(text: str, scene_type: str) -> float:
    # Chinese TTS commonly lands around 4.0-5.0 chars/sec. Use a conservative
    # estimate for drafts; final timing should be driven by actual audio files.
    base = text_units(text) / 4.4
    if scene_type == "cover":
        return max(5.5, min(7.5, base + 1.0))
    if scene_type == "outro":
        return max(4.0, min(6.0, base + 1.0))
    return max(8.0, min(13.5, base + 1.4))


def final_path(date: str) -> Path:
    return PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "final.json"


def publish_images_dir(date: str) -> Path:
    return PROJECT_ROOT / "daily" / date / LINE_NAME / "publish" / "images"


def video_dir(date: str) -> Path:
    return PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "video"


def scene_image_name(index: int) -> str:
    return "00-cover.png" if index == 0 else f"{index:02d}.png"


def copy_scene_assets(date: str, count: int) -> None:
    source = publish_images_dir(date)
    target = video_dir(date) / "assets"
    target.mkdir(parents=True, exist_ok=True)
    expected = [scene_image_name(i) for i in range(count + 1)]
    for name in expected:
        src = source / name
        if not src.exists():
            raise SystemExit(f"missing image: {src}")
        shutil.copy2(src, target / name)


def cover_voiceover(final: dict[str, Any], count: int) -> str:
    return f"三分钟未来，带你用三分钟了解最近AI圈发生了什么，用{count}条报道，看 AI 怎么继续进入现实。"


def item_voiceover(item: dict[str, Any]) -> str:
    title = clean_text(item.get("title"))
    fact = clean_text(item.get("fact"))
    thought = clean_text(item.get("thought"))
    if thought:
        return f"{title}。{fact} {thought}"
    return f"{title}。{fact}"


def build_scenes(final: dict[str, Any]) -> list[dict[str, Any]]:
    items = list(final.get("items", []))
    scenes: list[dict[str, Any]] = []

    cover_text = cover_voiceover(final, len(items))
    scenes.append(
        {
            "id": "00-cover",
            "type": "cover",
            "title": clean_text(final.get("cover", {}).get("title") or final.get("name")),
            "image": "assets/00-cover.png",
            "voiceover": cover_text,
            "audio": None,
            "durationSeconds": estimate_duration_seconds(cover_text, "cover"),
            "tailPaddingSeconds": 0.5,
            "transitionSeconds": 0.4,
        }
    )

    for item in items:
        index = int(item.get("index") or len(scenes))
        voice = item_voiceover(item)
        scenes.append(
            {
                "id": f"{index:02d}",
                "type": "story",
                "index": index,
                "title": clean_text(item.get("title")),
                "source": clean_text(item.get("source")),
                "image": f"assets/{index:02d}.png",
                "voiceover": voice,
                "audio": None,
                "durationSeconds": estimate_duration_seconds(voice, "story"),
                "tailPaddingSeconds": 1.0,
                "transitionSeconds": 0.35,
            }
        )

    outro = "这就是本期三分钟未来，关注我，持续为你带来最新消息。"
    scenes.append(
        {
            "id": "outro",
            "type": "outro",
            "title": "三分钟未来",
            "image": "assets/00-cover.png",
            "voiceover": outro,
            "audio": None,
            "durationSeconds": estimate_duration_seconds(outro, "outro"),
            "tailPaddingSeconds": 0.5,
            "transitionSeconds": 0.0,
        }
    )
    return scenes


def total_duration(scenes: list[dict[str, Any]]) -> float:
    total = 0.0
    for scene in scenes:
        total += float(scene.get("durationSeconds") or 0)
        total += float(scene.get("transitionSeconds") or 0)
    return round(total, 2)


def write_voiceover_docs(out_dir: Path, final: dict[str, Any], scenes: list[dict[str, Any]]) -> None:
    lines = [
        f"# 三分钟未来 VOL. {int(final.get('vol') or 0):03d} 视频旁白脚本",
        "",
        f"发布日：{final.get('publishDate', '')}",
        f"内容区间：{final.get('coverageLabel') or final.get('contentStart', '')}",
        f"账号：{final.get('account', '')}",
        "",
        "说明：每个编号是一段独立 TTS 输入。导入 TTS 时保留段落分隔，导出时建议一段一个音频文件。",
        "",
    ]
    tts_blocks: list[str] = []
    for scene in scenes:
        sid = scene["id"]
        voice = scene["voiceover"]
        lines.extend(
            [
                f"## {sid} {scene.get('title', '')}",
                "",
                f"建议时长：{scene.get('durationSeconds')} 秒",
                "",
                voice,
                "",
            ]
        )
        tts_blocks.append(f"[{sid}]\n{voice}")

    (out_dir / "voiceover-script.md").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "tts-input.txt").write_text("\n\n".join(tts_blocks) + "\n", encoding="utf-8")


def build(date: str) -> Path:
    final = read_json(final_path(date))
    items = list(final.get("items", []))
    out_dir = video_dir(date)
    out_dir.mkdir(parents=True, exist_ok=True)
    copy_scene_assets(date, len(items))
    scenes = build_scenes(final)
    episode = {
        "line": LINE_NAME,
        "publishDate": final.get("publishDate", date),
        "contentStart": final.get("contentStart"),
        "contentEnd": final.get("contentEnd"),
        "coverageLabel": final.get("coverageLabel"),
        "vol": final.get("vol"),
        "account": final.get("account"),
        "canvas": CANVAS,
        "durationMode": "audio-driven-later",
        "draftDurationSeconds": total_duration(scenes),
        "audioRule": "When TTS files are ready, set scene.audio and replace durationSeconds with measured audio duration plus tailPaddingSeconds.",
        "scenes": scenes,
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    write_json(out_dir / "episode.video.json", episode)
    write_voiceover_docs(out_dir, final, scenes)
    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    args = parser.parse_args()

    out_dir = build(args.date)
    print(f"OK video package -> {out_dir}")


if __name__ == "__main__":
    main()
