"""
Build a Hyperframes sample project for Three-Minute Future.

The sample keeps the existing static card system as the visual source of truth:
- video canvas: 1080 x 1920
- cover card: 1080 x 1080
- inside card: 1080 x 1416

Usage:
  python lines/three-minute-future/build_hyperframes_sample.py 2026-05-26
  python lines/three-minute-future/build_hyperframes_sample.py 2026-05-26 --limit 2 --variant sample
  python lines/three-minute-future/build_hyperframes_sample.py 2026-05-26 --variant audio --audio-dir daily/2026-05-26/three-minute-future/work/tts
"""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import shutil
import subprocess
from pathlib import Path
from typing import Any


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LINE_ROOT = Path(__file__).resolve().parent
HYPERFRAMES_ROOT = LINE_ROOT / "hyperframes"
STYLE_PATH = LINE_ROOT / "styles" / "three-minute-future.css"

VIDEO_W = 1080
VIDEO_H = 1920
COVER_H = 1080
INSIDE_H = 1416
COVER_TOP = 420
INSIDE_TOP = 252
DEFAULT_COVER_SECONDS = 6.2
DEFAULT_REPORT_SECONDS = 10.4
DEFAULT_OUTRO_SECONDS = 0.8
DEFAULT_AUDIO_SPEED = 1.2
PLATFORM_SAFE_SCALE = 0.92
PLATFORM_SAFE_SIDE_MARGIN = round((VIDEO_W - VIDEO_W * PLATFORM_SAFE_SCALE) / 2)
COVER_TAIL_SECONDS = 0.45
REPORT_TAIL_SECONDS = 0.65
OUTRO_TAIL_SECONDS = 0.3


def ffmpeg_dir() -> Path:
    return (
        PROJECT_ROOT
        / "lines"
        / LINE_NAME
        / "remotion"
        / "node_modules"
        / "@remotion"
        / "compositor-win32-x64-msvc"
    )


def tool_path(name: str) -> Path:
    env_name = f"{name.upper()}_PATH"
    env_value = __import__("os").environ.get(env_name)
    if env_value and Path(env_value).exists():
        return Path(env_value)
    bundled = ffmpeg_dir() / f"{name}.exe"
    if bundled.exists():
        return bundled
    return Path(name)


def probe_duration(media_path: Path) -> float:
    ffprobe = tool_path("ffprobe")
    result = subprocess.run(
        [
            str(ffprobe),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(media_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def atempo_filter(speed: float) -> str:
    parts: list[float] = []
    remaining = speed
    while remaining > 2.0:
        parts.append(2.0)
        remaining /= 2.0
    while remaining < 0.5:
        parts.append(0.5)
        remaining /= 0.5
    parts.append(remaining)
    return ",".join(f"atempo={part:.6g}" for part in parts)


def prepare_audio(source: Path, target: Path, speed: float) -> tuple[str, float]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if abs(speed - 1.0) < 0.001:
        shutil.copy2(source, target)
    else:
        ffmpeg = tool_path("ffmpeg")
        subprocess.run(
            [
                str(ffmpeg),
                "-y",
                "-i",
                str(source),
                "-filter:a",
                atempo_filter(speed),
                "-vn",
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "3",
                str(target),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    return f"assets/audio/{target.name}", probe_duration(target)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def escape(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def final_path(date: str) -> Path:
    return PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "final.json"


def publish_dir(date: str) -> Path:
    return PROJECT_ROOT / "daily" / date / LINE_NAME / "publish"


def project_dir(final: dict[str, Any], variant: str) -> Path:
    vol = int(final.get("vol") or 0)
    return HYPERFRAMES_ROOT / f"vol-{vol:03d}-{variant}"


def local_asset_name(prefix: str, source: Path) -> str:
    ext = source.suffix.lower()
    if ext not in {".png", ".jpg", ".jpeg", ".webp"}:
        guessed = mimetypes.guess_extension(mimetypes.guess_type(source.name)[0] or "")
        ext = guessed or ".png"
    return f"{prefix}{ext}"


def copy_asset(source: Path, target: Path) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return f"assets/{target.name}"


def asset_source_for_item(item: dict[str, Any]) -> Path | None:
    for key in ("imagePath", "keywordImagePath", "sourceScreenshotPath"):
        value = item.get(key)
        if value and Path(value).exists():
            return Path(value)
    return None


def title_class(title: str) -> str:
    length = len(title)
    if length >= 15:
        return "title-long"
    if length >= 11:
        return "title-mid"
    return ""


def date_label(value: str) -> str:
    return value.replace("-", ".")


def copy_fonts(assets_dir: Path) -> None:
    fonts_dir = assets_dir / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    font_sources = {
        "msyh.ttc": Path("C:/Windows/Fonts/msyh.ttc"),
        "msyhbd.ttc": Path("C:/Windows/Fonts/msyhbd.ttc"),
        "simhei.ttf": Path("C:/Windows/Fonts/simhei.ttf"),
        "consolab.ttf": Path("C:/Windows/Fonts/consolab.ttf"),
    }
    for target_name, source in font_sources.items():
        if source.exists():
            shutil.copy2(source, fonts_dir / target_name)


def copy_vendor(assets_dir: Path) -> None:
    vendor_dir = assets_dir / "vendor"
    vendor_dir.mkdir(parents=True, exist_ok=True)
    gsap_source = HYPERFRAMES_ROOT / "vendor" / "gsap.min.js"
    if gsap_source.exists():
        shutil.copy2(gsap_source, vendor_dir / "gsap.min.js")


def video_duration(data: dict[str, Any]) -> float:
    report_seconds = sum(float(report.get("seconds") or DEFAULT_REPORT_SECONDS) for report in data["reports"])
    return round(
        float(data.get("coverSeconds") or DEFAULT_COVER_SECONDS)
        + report_seconds
        + float(data.get("outroSeconds") or DEFAULT_OUTRO_SECONDS),
        2,
    )


def build_sample_data(
    final: dict[str, Any],
    out_dir: Path,
    limit: int | None = None,
    audio_dir: Path | None = None,
    audio_speed: float = DEFAULT_AUDIO_SPEED,
) -> dict[str, Any]:
    items = list(final.get("items", []))
    if limit is not None:
        items = items[:limit]
    if not items:
        raise ValueError("final.json has no report items")
    assets_dir = out_dir / "assets"
    copy_fonts(assets_dir)
    copy_vendor(assets_dir)

    cover_path = Path(final.get("cover", {}).get("imagePath") or "")
    if not cover_path.exists():
        fallback = publish_dir(str(final.get("publishDate"))) / "images" / "00-cover.png"
        cover_path = fallback
    cover_asset = copy_asset(cover_path, assets_dir / local_asset_name("cover-bg", cover_path))

    audio_assets_dir = assets_dir / "audio"
    cover_audio = None
    cover_seconds = DEFAULT_COVER_SECONDS
    outro_audio = None
    outro_seconds = DEFAULT_OUTRO_SECONDS
    if audio_dir is not None:
        cover_source = audio_dir / "00.mp3"
        outro_source = audio_dir / f"{len(items) + 1:02d}.mp3"
        if cover_source.exists():
            cover_audio, cover_audio_seconds = prepare_audio(
                cover_source, audio_assets_dir / "00-cover.mp3", audio_speed
            )
            cover_seconds = round(cover_audio_seconds + COVER_TAIL_SECONDS, 2)
        if outro_source.exists():
            outro_audio, outro_audio_seconds = prepare_audio(
                outro_source, audio_assets_dir / "outro.mp3", audio_speed
            )
            outro_seconds = round(outro_audio_seconds + OUTRO_TAIL_SECONDS, 2)

    reports: list[dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        source = asset_source_for_item(item)
        if source is None:
            source = publish_dir(str(final.get("publishDate"))) / "images" / f"{idx:02d}.png"
        image_asset = copy_asset(source, assets_dir / local_asset_name(f"report-{idx:02d}", source))
        report_audio = None
        report_seconds = DEFAULT_REPORT_SECONDS
        if audio_dir is not None:
            audio_source = audio_dir / f"{idx:02d}.mp3"
            if audio_source.exists():
                report_audio, report_audio_seconds = prepare_audio(
                    audio_source, audio_assets_dir / f"{idx:02d}.mp3", audio_speed
                )
                report_seconds = round(report_audio_seconds + REPORT_TAIL_SECONDS, 2)
        reports.append(
            {
                "index": idx,
                "title": clean(item.get("title")),
                "source": clean(item.get("source")),
                "fact": clean(item.get("fact")),
                "thought": clean(item.get("thought")),
                "image": image_asset,
                "audio": report_audio,
                "audioSeconds": round(report_seconds - REPORT_TAIL_SECONDS, 2)
                if report_audio
                else 0,
                "seconds": report_seconds,
                "accentA": item.get("accentA") or "#cfff00",
                "accentB": item.get("accentB") or "#00e5ff",
            }
        )

    hooks = [clean(item.get("title")) for item in list(final.get("items", []))[:3]]
    hooks += ["", "", ""]

    data = {
        "title": clean(final.get("cover", {}).get("title") or "三分钟未来"),
        "subtitle": clean(final.get("cover", {}).get("tagline") or "AI 资讯 × 实时热点"),
        "coverageLabel": clean(final.get("coverageLabel")),
        "publishDate": clean(final.get("publishDate")),
        "dateText": date_label(clean(final.get("publishDate"))),
        "vol": int(final.get("vol") or 0),
        "account": clean(final.get("account")),
        "reportCount": len(final.get("items", [])),
        "estimatedDuration": clean(final.get("estimatedDuration") or "2'40\""),
        "coverAudio": cover_audio,
        "coverAudioSeconds": round(cover_seconds - COVER_TAIL_SECONDS, 2) if cover_audio else 0,
        "coverSeconds": cover_seconds,
        "outroAudio": outro_audio,
        "outroAudioSeconds": round(outro_seconds - OUTRO_TAIL_SECONDS, 2) if outro_audio else 0,
        "outroSeconds": outro_seconds,
        "audioSpeed": audio_speed if audio_dir is not None else 1,
        "coverBackground": cover_asset,
        "leadHook": hooks[0],
        "subHook1": hooks[1],
        "subHook2": hooks[2],
        "reports": reports,
    }
    data["duration"] = video_duration(data)
    return data


def data_js(data: dict[str, Any]) -> str:
    return "window.TMF_SAMPLE_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"


def design_md() -> str:
    return f"""# Three-Minute Future Hyperframes Design

## Visual Source Of Truth
The video composition reuses the static card system:
- video canvas: {VIDEO_W} x {VIDEO_H}
- cover card: 1080 x {COVER_H}, centered vertically at top {COVER_TOP}px
- inside card: 1080 x {INSIDE_H}, centered vertically at top {INSIDE_TOP}px
- video safe wrapper: scale {PLATFORM_SAFE_SCALE}, centered, leaving about {PLATFORM_SAFE_SIDE_MARGIN}px horizontal margin per side for Douyin/player crop

## Style Prompt
Industrial constructivist AI news video. The HTML cards keep the approved Three-Minute Future graphic system: black/off-white base, acid-lime information ribbons, cyan/magenta registration accents, heavy Chinese display type, hard editorial collage.

## Motion
Animate components inside the cards. Do not animate flattened exported PNGs as the whole video.

## TTS Readiness
Each report scene keeps source, title, brief, and thought as separately addressable elements for later audio timing.
"""


def base_css() -> str:
    css = STYLE_PATH.read_text(encoding="utf-8")
    css = css.replace(
        '"HarmonyOS Sans SC", "MiSans", "Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans SC", sans-serif',
        '"Microsoft YaHei UI", "Microsoft YaHei", sans-serif',
    ).replace(
        '"SimHei", "Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans SC", sans-serif',
        '"SimHei", "Microsoft YaHei UI", "Microsoft YaHei", sans-serif',
    )
    return (
        css.replace(
            "var(--font-ui)",
            '"Microsoft YaHei UI", "Microsoft YaHei", sans-serif',
        )
        .replace(
            "var(--font-display)",
            '"SimHei", "Microsoft YaHei UI", "Microsoft YaHei", sans-serif',
        )
    )


def hyperframes_css() -> str:
    return f"""
    @font-face {{
      font-family: "Microsoft YaHei UI";
      src: url("./assets/fonts/msyhbd.ttc") format("truetype");
      font-weight: 700 950;
    }}
    @font-face {{
      font-family: "Microsoft YaHei";
      src: url("./assets/fonts/msyh.ttc") format("truetype");
      font-weight: 400 950;
    }}
    @font-face {{
      font-family: "SimHei";
      src: url("./assets/fonts/simhei.ttf") format("truetype");
      font-weight: 900 950;
    }}
    @font-face {{
      font-family: "TMFHei";
      src: url("./assets/fonts/msyhbd.ttc") format("truetype");
      font-weight: 700 950;
    }}
    @font-face {{
      font-family: "TMFDisplay";
      src: url("./assets/fonts/simhei.ttf") format("truetype");
      font-weight: 900 950;
    }}
    @font-face {{
      font-family: "TMFMono";
      src: url("./assets/fonts/consolab.ttf") format("truetype");
      font-weight: 700 950;
    }}
    html, body {{
      width: 100%;
      height: 100%;
      margin: 0;
      overflow: hidden;
      background: #050706;
    }}
    #tmf-vol-sample {{
      position: relative;
      width: {VIDEO_W}px;
      height: {VIDEO_H}px;
      overflow: hidden;
      background:
        linear-gradient(rgba(217,255,22,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(217,255,22,.025) 1px, transparent 1px),
        #050706;
      background-size: 54px 54px;
      font-family: "TMFHei", "Microsoft YaHei UI", "Microsoft YaHei", sans-serif;
    }}
    #tmf-vol-sample .safe-frame {{
      position: absolute;
      left: 50%;
      width: 1080px;
      transform: translateX(-50%) scale({PLATFORM_SAFE_SCALE});
      transform-origin: top center;
      will-change: transform;
    }}
    #tmf-vol-sample .cover-frame {{
      top: {COVER_TOP}px;
      height: {COVER_H}px;
    }}
    #tmf-vol-sample .inside-frame {{
      top: {INSIDE_TOP}px;
      height: {INSIDE_H}px;
    }}
    #tmf-vol-sample .page {{
      position: relative;
      left: 0;
      top: 0;
      transform-origin: center center;
    }}
    #tmf-vol-sample .cover {{
      width: 1080px;
      height: {COVER_H}px;
    }}
    #tmf-vol-sample .inside {{
      width: 1080px;
      height: {INSIDE_H}px;
    }}
    #tmf-vol-sample .scene {{
      position: absolute;
      inset: 0;
      overflow: hidden;
      background: #050706;
    }}
    #tmf-vol-sample .scene::before {{
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      background:
        radial-gradient(circle at 30% 20%, rgba(217,255,22,.08), transparent 24%),
        radial-gradient(circle at 76% 70%, rgba(229,24,68,.10), transparent 22%);
      opacity: .9;
    }}
    #tmf-vol-sample .cover .title,
    #tmf-vol-sample .inside-title {{
      font-family: "TMFDisplay", "SimHei", "Microsoft YaHei UI", sans-serif;
      font-weight: 950;
    }}
    #tmf-vol-sample .inside-top,
    #tmf-vol-sample .cover-banner,
    #tmf-vol-sample .inside-account-ribbon {{
      font-family: "TMFHei", "Microsoft YaHei UI", sans-serif;
      font-weight: 950;
    }}
    #tmf-vol-sample .title-card,
    #tmf-vol-sample .brief-card,
    #tmf-vol-sample .think-card,
    #tmf-vol-sample .content-card {{
      will-change: transform, opacity;
    }}
    #tmf-vol-sample .content-card {{
      padding-bottom: 42px;
    }}
    #tmf-vol-sample .transition-slice {{
      position: absolute;
      z-index: 80;
      top: 0;
      bottom: 0;
      left: -180px;
      width: 1440px;
      pointer-events: none;
      background: #d9ff16;
      opacity: 0;
      transform: skewX(-18deg);
      transform-origin: center;
    }}
    #tmf-vol-sample .magenta-slice {{
      background: #e51844;
      z-index: 79;
    }}
    [data-layout-ignore] {{
      pointer-events: none;
    }}
"""


def cover_markup(data: dict[str, Any]) -> str:
    return f"""
      <div class="safe-frame cover-frame" data-layout-allow-overflow>
        <article class="page cover" data-layout-allow-overflow style="--cover-bg: url('{escape(data['coverBackground'])}');">
        <div class="bg" data-layout-allow-overflow></div>
        <div class="wash"></div>
        <div class="quiet-slab" data-layout-allow-overflow></div>

        <div class="brand">AI HOT / REALITY SIGNAL</div>
        <div class="title">《{escape(data['title'])}》</div>
        <div class="subtitle">{escape(data['subtitle'])}</div>

        <div class="issue">
          第 <span class="num">{int(data['vol']):02d}</span> 期
          <span class="range">{escape(data['coverageLabel'])}</span>
        </div>

        <div class="lead-hook">{escape(data['leadHook'])}</div>

        <div class="sub-hooks">
          <div>{escape(data['subHook1'])}</div>
          <div>{escape(data['subHook2'])}</div>
        </div>

        <div class="metrics">
          <div class="metric">本期报道<strong>{escape(data['reportCount'])} 篇</strong></div>
          <div class="metric">预计时长<strong>{escape(data['estimatedDuration'])}</strong></div>
        </div>

        <div class="cover-banner">
          <span>THREE-MINUTE FUTURE</span>
          <span>{escape(data['account'])}</span>
        </div>
        </article>
      </div>
    """


def report_markup(report: dict[str, Any], data: dict[str, Any]) -> str:
    cls = title_class(report["title"])
    return f"""
      <div class="safe-frame inside-frame" data-layout-allow-overflow>
        <article class="page inside" style="--accent-a: {escape(report['accentA'])}; --accent-b: {escape(report['accentB'])};">
        <div class="inside-top">
          <div>三分钟未来 / AI HOT</div>
          <div>{escape(data['dateText'])}</div>
        </div>

        <div class="photo" data-layout-allow-overflow>
          <img src="{escape(report['image'])}" crossorigin="anonymous" alt="">
        </div>

        <div class="source">{escape(report['source'])}</div>

        <div class="title-card">
          <h2 class="inside-title {escape(cls)}">{escape(report['title'])}</h2>
        </div>

        <div class="story content-card">
          <section class="brief-card">
            <span class="module-label">短讯</span>
            <p>{escape(report['fact'])}</p>
          </section>
          <section class="think-card">
            <span class="module-label">思考</span>
            <div class="think">{escape(report['thought'])}</div>
          </section>
        </div>

        <div class="inside-account-ribbon" data-layout-allow-overflow>
          <span>THREE-MINUTE FUTURE</span>
          <span>{escape(data['account'])}</span>
        </div>
        </article>
      </div>
    """


def report_scenes_markup(data: dict[str, Any]) -> str:
    return "\n".join(
        f"""    <section id="scene-report-{report['index']}" class="scene">
{report_markup(report, data)}
    </section>"""
        for report in data["reports"]
    )


def report_ids_js(data: dict[str, Any]) -> str:
    return json.dumps([report["index"] for report in data["reports"]], ensure_ascii=False)


def report_seconds_js(data: dict[str, Any]) -> str:
    return json.dumps(
        {str(report["index"]): float(report.get("seconds") or DEFAULT_REPORT_SECONDS) for report in data["reports"]},
        ensure_ascii=False,
    )


def audio_clips_markup(data: dict[str, Any]) -> str:
    clips: list[str] = []
    cursor = 0.0

    def add_clip(clip_id: str, audio: str | None, start: float, duration: float, track: int) -> None:
        if not audio or duration <= 0:
            return
        clips.append(
            f'    <audio id="{escape(clip_id)}" data-start="{start:.2f}" data-duration="{duration:.2f}" '
            f'data-track-index="{track}" src="{escape(audio)}" data-volume="1"></audio>'
        )

    add_clip("audio-cover", data.get("coverAudio"), cursor, float(data.get("coverAudioSeconds") or 0), 50)
    cursor += float(data.get("coverSeconds") or DEFAULT_COVER_SECONDS)
    for report in data["reports"]:
        add_clip(
            f"audio-report-{int(report['index']):02d}",
            report.get("audio"),
            cursor,
            float(report.get("audioSeconds") or 0),
            50,
        )
        cursor += float(report.get("seconds") or DEFAULT_REPORT_SECONDS)
    add_clip("audio-outro", data.get("outroAudio"), cursor, float(data.get("outroAudioSeconds") or 0), 50)
    return "\n".join(clips)


def index_html(data: dict[str, Any]) -> str:
    reports_js = report_ids_js(data)
    report_seconds = report_seconds_js(data)
    last_report_id = data["reports"][-1]["index"]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(data['title'])} Hyperframes Sample</title>
  <script src="./assets/vendor/gsap.min.js"></script>
  <script src="./data.js"></script>
  <style>
{base_css()}
{hyperframes_css()}
  </style>
</head>
<body>
  <div id="tmf-vol-sample" data-composition-id="tmf-vol-sample" data-start="0" data-duration="{data['duration']}" data-width="{VIDEO_W}" data-height="{VIDEO_H}">
    <section id="scene-cover" class="scene">
{cover_markup(data)}
    </section>

{report_scenes_markup(data)}

    <section id="scene-outro" class="scene">
{cover_markup(data)}
    </section>

{audio_clips_markup(data)}

    <div class="transition-slice magenta-slice"></div>
    <div class="transition-slice lime-slice"></div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const transition = (at) => {{
        tl.set(".magenta-slice", {{ x: -1550, opacity: 0.72 }}, at);
        tl.set(".lime-slice", {{ x: -1600, opacity: 1 }}, at + 0.02);
        tl.to(".magenta-slice", {{ x: 1550, duration: 0.54, ease: "power4.inOut" }}, at);
        tl.to(".lime-slice", {{ x: 1600, duration: 0.44, ease: "expo.inOut" }}, at + 0.04);
        tl.set(".transition-slice", {{ opacity: 0 }}, at + 0.62);
      }};
      const showScene = (selector, at) => tl.set(selector, {{ autoAlpha: 1 }}, at);
      const hideScene = (selector, at) => tl.set(selector, {{ autoAlpha: 0 }}, at);
      const reports = {reports_js};
      const reportSeconds = {report_seconds};
      const coverSeconds = {float(data.get('coverSeconds') or DEFAULT_COVER_SECONDS)};
      const outroSeconds = {float(data.get('outroSeconds') or DEFAULT_OUTRO_SECONDS)};
      const totalDuration = {data['duration']};

      tl.set([...reports.map((i) => "#scene-report-" + i), "#scene-outro"], {{ autoAlpha: 0 }}, 0);
      tl.set("#scene-cover", {{ autoAlpha: 1 }}, 0);

      tl.from("#scene-cover .cover", {{ y: 70, scale: 0.985, opacity: 0, duration: 0.62, ease: "expo.out" }}, 0.14);
      tl.from("#scene-cover .bg", {{ scale: 1.05, x: -20, duration: 5.8, ease: "none" }}, 0.18);
      tl.from("#scene-cover .metrics .metric", {{ y: -20, opacity: 0, stagger: 0.1, duration: 0.34, ease: "sine.out" }}, 0.45);
      tl.from("#scene-cover .brand", {{ y: -28, opacity: 0, duration: 0.36, ease: "back.out(1.5)" }}, 0.55);
      tl.from("#scene-cover .title", {{ x: -64, opacity: 0, duration: 0.7, ease: "power4.out" }}, 0.72);
      tl.from("#scene-cover .subtitle", {{ scaleX: 0, opacity: 0, duration: 0.42, ease: "circ.out", transformOrigin: "left center" }}, 1.02);
      tl.from("#scene-cover .issue", {{ x: 56, opacity: 0, duration: 0.44, ease: "expo.out" }}, 1.25);
      tl.from("#scene-cover .lead-hook", {{ x: 50, opacity: 0, duration: 0.48, ease: "power3.out" }}, 1.46);
      tl.from("#scene-cover .sub-hooks div", {{ x: -42, opacity: 0, stagger: 0.16, duration: 0.4, ease: "power3.out" }}, 1.82);
      tl.from("#scene-cover .cover-banner", {{ y: 54, opacity: 0, duration: 0.36, ease: "power2.out" }}, 2.2);

      const animateReport = (index, at) => {{
        const s = "#scene-report-" + index;
        const dir = index % 2 === 0 ? 1 : -1;
        tl.from(s + " .inside", {{ x: 68 * dir, scale: 0.985, opacity: 0, duration: 0.56, ease: "expo.out" }}, at + 0.12);
        tl.from(s + " .inside-top div", {{ y: -24, opacity: 0, stagger: 0.08, duration: 0.34, ease: "power3.out" }}, at + 0.3);
        tl.from(s + " .photo", {{ x: 62 * dir, opacity: 0, duration: 0.54, ease: "power4.out" }}, at + 0.48);
        tl.from(s + " .photo img", {{ scale: 1.08, x: -24 * dir, duration: 8.3, ease: "none" }}, at + 0.48);
        tl.from(s + " .source", {{ opacity: 0, x: 26 * dir, duration: 0.32, ease: "sine.out" }}, at + 0.84);
        tl.from(s + " .title-card", {{ x: 76 * dir, opacity: 0, duration: 0.5, ease: "expo.out" }}, at + 1.0);
        tl.from(s + " .brief-card", {{ y: 52, opacity: 0, duration: 0.48, ease: "power3.out" }}, at + 1.42);
        tl.from(s + " .think-card", {{ y: 42, opacity: 0, duration: 0.42, ease: "circ.out" }}, at + 1.76);
        tl.from(s + " .module-label", {{ scale: 0.65, opacity: 0, stagger: 0.07, duration: 0.26, ease: "back.out(2)" }}, at + 1.96);
        tl.from(s + " .inside-account-ribbon", {{ y: 54, opacity: 0, duration: 0.34, ease: "power2.out" }}, at + 2.12);
      }};

      transition(coverSeconds - 0.55);
      let cursor = coverSeconds;
      reports.forEach((index, order) => {{
        const start = cursor;
        const seconds = reportSeconds[String(index)] || {DEFAULT_REPORT_SECONDS};
        const current = "#scene-report-" + index;
        const previous = order === 0 ? "#scene-cover" : "#scene-report-" + reports[order - 1];
        showScene(current, start);
        hideScene(previous, start + 0.06);
        animateReport(index, start + 0.08);
        transition(start + seconds - 0.7);
        cursor += seconds;
      }});

      showScene("#scene-outro", cursor);
      hideScene("#scene-report-{last_report_id}", cursor + 0.06);
      tl.from("#scene-outro .cover", {{ y: 60, scale: 0.985, opacity: 0, duration: 0.58, ease: "expo.out" }}, cursor + 0.1);
      tl.from("#scene-outro .bg", {{ scale: 1.04, x: -18, duration: Math.max(2.2, outroSeconds), ease: "none" }}, cursor + 0.12);
      tl.from("#scene-outro .title", {{ x: -54, opacity: 0, duration: 0.52, ease: "power4.out" }}, cursor + 0.28);
      tl.from("#scene-outro .subtitle", {{ scaleX: 0, opacity: 0, duration: 0.34, ease: "circ.out", transformOrigin: "left center" }}, cursor + 0.58);
      tl.from("#scene-outro .cover-banner", {{ y: 48, opacity: 0, duration: 0.34, ease: "power2.out" }}, cursor + 0.84);
      tl.to("#scene-outro", {{ opacity: 0, duration: 0.55, ease: "sine.inOut" }}, totalDuration - 0.65);
      window.__timelines["tmf-vol-sample"] = tl;
    </script>
  </div>
</body>
</html>
"""


def build(date: str, variant: str, limit: int | None = None, audio_dir: Path | None = None, audio_speed: float = DEFAULT_AUDIO_SPEED) -> Path:
    final = read_json(final_path(date))
    out_dir = project_dir(final, variant)
    data = build_sample_data(final, out_dir, limit=limit, audio_dir=audio_dir, audio_speed=audio_speed)
    write_text(out_dir / "DESIGN.md", design_md())
    write_text(out_dir / "data.js", data_js(data))
    write_text(out_dir / "index.html", index_html(data))
    return out_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--variant", default="full", help="output project suffix, e.g. full or sample")
    parser.add_argument("--limit", type=int, default=None, help="optional report limit for quick samples")
    parser.add_argument("--audio-dir", type=Path, default=None, help="optional directory with 00.mp3, 01.mp3 ... outro mp3")
    parser.add_argument("--audio-speed", type=float, default=DEFAULT_AUDIO_SPEED, help="audio speed multiplier when --audio-dir is set")
    args = parser.parse_args()
    out_dir = build(args.date, variant=args.variant, limit=args.limit, audio_dir=args.audio_dir, audio_speed=args.audio_speed)
    print(f"OK hyperframes sample -> {out_dir}")


if __name__ == "__main__":
    main()
