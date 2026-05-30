"""
B3: 把 yolox-related-projects.xlsx 入库到 yolox_related_projects 表

注意：xlsx 名义 219 行，但实际只有 24 个项目有数据，其余空白。
URL 是 =HYPERLINK("...", "...") 公式格式，需要正则提取。

执行：/usr/bin/python3 scripts/import_projects.py
"""
import openpyxl
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
XLSX = ROOT / "data" / "yolox-related-projects.xlsx"
DB = ROOT / "data" / "backlinks.db"


def extract_url(cell_value) -> str | None:
    if not cell_value:
        return None
    s = str(cell_value)
    if s.startswith("http"):
        return s
    match = re.search(r'"(https?://[^"]+)"', s)
    return match.group(1) if match else None


def main() -> int:
    if not XLSX.exists():
        print(f"ERROR: {XLSX} not found", file=sys.stderr)
        return 1

    wb = openpyxl.load_workbook(XLSX)
    ws = wb.active

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        name, link_cell, desc, cat, _guide = row
        if not name:
            skipped += 1
            continue
        url = extract_url(link_cell)
        cur.execute(
            """
            INSERT INTO yolox_related_projects (name, description, url, category, source)
            VALUES (?, ?, ?, ?, 'yolox-related-projects.xlsx')
            """,
            (name.strip() if name else None, desc, url, cat),
        )
        inserted += 1

    conn.commit()

    print(f"Inserted: {inserted}")
    print(f"Skipped (empty rows): {skipped}")
    print()
    print("=== sample 5 ===")
    for r in cur.execute(
        "SELECT name, category, url FROM yolox_related_projects LIMIT 5"
    ):
        print(f"  {r[0]:<25} | {r[1] or '-':<15} | {r[2] or '-'}")

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
