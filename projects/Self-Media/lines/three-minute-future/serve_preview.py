"""
Serve a rendered 三分钟未来 publish directory for Codex side-browser preview.

Usage:
  python lines/three-minute-future/serve_preview.py 2026-05-23 --port 58417
"""

from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
from pathlib import Path


LINE_NAME = "three-minute-future"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def publish_dir_for(date: str) -> Path:
    return PROJECT_ROOT / "daily" / date / LINE_NAME / "publish"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("date", help="publish date YYYY-MM-DD")
    parser.add_argument("--port", type=int, default=58417, help="local preview port")
    args = parser.parse_args()

    publish_dir = publish_dir_for(args.date)
    index_path = publish_dir / "index.html"
    if not index_path.exists():
        raise SystemExit(
            f"missing: {index_path}\n"
            f"run: python lines\\three-minute-future\\render_pages.py {args.date}"
        )

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(publish_dir))
    with ReusableTCPServer(("127.0.0.1", args.port), handler) as httpd:
        print(f"Preview: http://localhost:{args.port}/")
        print(f"Serving: {publish_dir}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
