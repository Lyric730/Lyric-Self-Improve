"""
Export rendered HTML pages to PNG files.

Cover pages export as 1080x1080.
Inside pages export as 1080x1416.

Usage:
  python lines/three-minute-future/screenshot_pages.py 2026-05-23
  python lines/three-minute-future/screenshot_pages.py 2026-05-23 --out-dir publish-next
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
COVER_WIDTH = 1080
COVER_HEIGHT = 1080
INSIDE_WIDTH = 1080
INSIDE_HEIGHT = 1416
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


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return 0, 0
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def page_size(html_path: Path) -> tuple[int, int]:
    if html_path.name.startswith("00-cover"):
        return COVER_WIDTH, COVER_HEIGHT
    return INSIDE_WIDTH, INSIDE_HEIGHT


def screenshot_one(browser: Path, html_path: Path, out_path: Path, width: int, height: int) -> None:
    url = html_path.resolve().as_uri()
    profile_dir = out_path.parent / ".chrome-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-first-run",
            "--disable-extensions",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--user-data-dir={profile_dir}",
            f"--screenshot={out_path}",
            url,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    actual_width, actual_height = png_size(out_path)
    if (actual_width, actual_height) != (width, height):
        raise RuntimeError(f"unexpected screenshot size {actual_width}x{actual_height}: {out_path}")


def export(date: str, out_dir: str = "publish") -> Path:
    publish_dir = PROJECT_ROOT / "daily" / date / LINE_NAME / out_dir
    html_dir = publish_dir / "html"
    if not html_dir.exists():
        raise SystemExit(f"missing: {html_dir} (run render_pages.py first)")
    image_dir = publish_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    browser = browser_path()

    html_files = sorted(html_dir.glob("*.html"))
    for index, html_path in enumerate(html_files, 1):
        name = "00-cover.png" if index == 1 else f"{index - 1:02d}.png"
        out_path = image_dir / name
        width, height = page_size(html_path)
        screenshot_one(browser, html_path, out_path, width, height)
        print(f"OK {out_path.name} {width}x{height}")
    return image_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--out-dir", default="publish", help="output directory under the daily line folder")
    args = parser.parse_args()

    image_dir = export(args.date, args.out_dir)
    print(f"OK images -> {image_dir}")


if __name__ == "__main__":
    main()
