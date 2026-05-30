#!/usr/bin/env python3
"""Capture a homepage screenshot for campaigns missing product imagery."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=1000)
    parser.add_argument("--full-page", action="store_true")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise SystemExit(
            "Playwright Python is not installed. Install it or use the active browser screenshot tool. "
            f"Original error: {exc}"
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(args.url, wait_until="networkidle", timeout=60000)
        page.screenshot(path=str(out), full_page=args.full_page)
        browser.close()
    print(out.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
