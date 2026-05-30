"""
Screenshot source pages for final items that do not have a usable image.

This is a fallback for inside pages only. It does not capture Google News proxy
pages because those are not the original reports.

Input:
  daily/<date>/three-minute-future/work/final.json

Output:
  daily/<date>/three-minute-future/work/source-shots/*.png
  final.json updated with sourceScreenshotPath / visualFallbackStatus

Usage:
  python lines/three-minute-future/capture_source_screenshots.py 2026-05-23
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]


def browser_path() -> Path:
    for path in CHROME_CANDIDATES:
        if path.exists():
            return path
    raise SystemExit("missing Chrome/Edge executable")


def load_final(date: str) -> tuple[Path, dict]:
    path = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "final.json"
    if not path.exists():
        raise SystemExit(f"missing: {path} (run generate_final.py first)")
    return path, json.loads(path.read_text(encoding="utf-8"))


def host_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return 0, 0
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def screenshot_url(browser: Path, url: str, out_path: Path) -> bool:
    profile_dir = out_path.parent / ".chrome-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    host = host_of(url)
    window_size = "820,1100" if host in {"x.com", "twitter.com"} else "1200,900"
    try:
        subprocess.run(
            [
                str(browser),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--no-first-run",
                "--disable-extensions",
                "--force-device-scale-factor=1",
                f"--window-size={window_size}",
                f"--user-data-dir={profile_dir}",
                f"--screenshot={out_path}",
                url,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=45,
        )
        width, height = png_size(out_path)
        if host in {"x.com", "twitter.com"}:
            if out_path.stat().st_size < 50_000:
                return False
            return width >= 760 and height >= 900
        return width >= 1000 and height >= 700
    except Exception:
        if out_path.exists():
            out_path.unlink()
        return False


def capture(date: str) -> Path:
    final_path, data = load_final(date)
    shot_dir = PROJECT_ROOT / "daily" / date / LINE_NAME / "work" / "source-shots"
    shot_dir.mkdir(parents=True, exist_ok=True)
    browser = browser_path()

    for item in data.get("items", []):
        if item.get("imagePath"):
            item["visualFallbackStatus"] = "has-image"
            continue
        if item.get("keywordImagePath"):
            item["visualFallbackStatus"] = "keyword-image"
            continue
        url = item.get("url", "")
        host = host_of(url)
        if not url:
            item["visualFallbackStatus"] = "missing-url"
            continue
        if "news.google.com" in host:
            item["visualFallbackStatus"] = "skipped-google-news-proxy"
            continue

        out_path = shot_dir / f"{item['id']}.png"
        ok = screenshot_url(browser, url, out_path)
        if ok:
            item["sourceScreenshotPath"] = str(out_path)
            item["visualFallbackStatus"] = "source-screenshot"
            print(f"OK screenshot {item['id']} {host}")
        else:
            item["sourceScreenshotPath"] = ""
            item["visualFallbackStatus"] = "screenshot-failed"
            if out_path.exists():
                out_path.unlink()
            print(f"MISS screenshot {item['id']} {host}")

    final_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return shot_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    args = parser.parse_args()

    shot_dir = capture(args.date)
    print(f"OK source shots -> {shot_dir}")


if __name__ == "__main__":
    main()
