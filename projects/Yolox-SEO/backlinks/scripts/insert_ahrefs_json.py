"""
insert_ahrefs_json.py — 从 browser_evaluate 输出的 JSON 文件 INSERT 到 ahrefs_api_results

用法：
  /usr/bin/python3 scripts/insert_ahrefs_json.py data/ahrefs-bolt.new.json
  /usr/bin/python3 scripts/insert_ahrefs_json.py data/ahrefs-*.json  # 批量
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB = ROOT / "data" / "backlinks.db"


def insert_one(conn, path: Path) -> tuple[str, int, int]:
    payload = json.loads(path.read_text())
    competitor = payload.get("competitor")
    if not competitor:
        # 兜底从文件名提取
        name = path.stem  # e.g. ahrefs-bolt.new
        if name.startswith("ahrefs-"):
            competitor = name[len("ahrefs-"):]
    rows = payload.get("data", [])
    cur = conn.cursor()
    inserted = 0
    for r in rows:
        try:
            cur.execute(
                """INSERT INTO ahrefs_api_results
                   (competitor, backlink_url, title, dr, anchor_text)
                   VALUES (?, ?, ?, ?, ?)""",
                (competitor, r["ref_url"], r["ref_title"], r["dr"], r["anchor"]),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    return competitor, len(rows), inserted


def main():
    if len(sys.argv) < 2:
        print("Usage: insert_ahrefs_json.py <file1.json> [file2.json ...]", file=sys.stderr)
        return 1
    conn = sqlite3.connect(DB)
    total_inserted = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"skip {arg}: not found")
            continue
        comp, count, inserted = insert_one(conn, path)
        print(f"{comp:<20} extracted={count:<3} inserted={inserted}")
        total_inserted += inserted
    print(f"\nTotal inserted: {total_inserted}")
    # 汇总
    cur = conn.cursor()
    print("\n=== ahrefs_api_results 汇总 ===")
    for r in cur.execute(
        "SELECT competitor, COUNT(*) FROM ahrefs_api_results GROUP BY competitor ORDER BY competitor"
    ):
        print(f"  {r[0]:<22} {r[1]}")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
