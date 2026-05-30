"""
B1 + B2: backlinks.db schema 扩容 + 固定数据预灌

执行：/usr/bin/python3 scripts/init_db.py
幂等：所有 CREATE 都用 IF NOT EXISTS / INSERT 都用 OR IGNORE
"""
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "backlinks.db"

SCHEMA = [
    # 跨源统一提交记录表
    """
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY,
        source_table TEXT,
        source_id INTEGER,
        platform_domain TEXT,
        submit_url TEXT,
        target_yolox_url TEXT,
        anchor_text TEXT,
        submit_method TEXT,
        submit_time TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending',
        rel_actual TEXT,
        live_url TEXT,
        error_log TEXT,
        notes TEXT
    )
    """,
    # Yolox 锚文本池
    """
    CREATE TABLE IF NOT EXISTS yolox_anchors (
        id INTEGER PRIMARY KEY,
        anchor_text TEXT UNIQUE,
        type TEXT,
        use_count INTEGER DEFAULT 0
    )
    """,
    # 目标页面池
    """
    CREATE TABLE IF NOT EXISTS yolox_pages (
        id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        page_type TEXT,
        priority INTEGER
    )
    """,
    # 219 竞品池（待 Serper 补 URL）
    """
    CREATE TABLE IF NOT EXISTS yolox_related_projects (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        url TEXT,
        category TEXT,
        source TEXT,
        added_date TEXT DEFAULT CURRENT_DATE
    )
    """,
    # LXX.ai 3000+ 候选
    """
    CREATE TABLE IF NOT EXISTS lxx_ai (
        id INTEGER PRIMARY KEY,
        domain TEXT,
        url TEXT,
        category TEXT,
        dr INTEGER,
        traffic INTEGER,
        submitted TEXT DEFAULT 'no'
    )
    """,
    # Ahrefs 未公开 API 同行链
    """
    CREATE TABLE IF NOT EXISTS ahrefs_api_results (
        id INTEGER PRIMARY KEY,
        competitor TEXT,
        backlink_url TEXT,
        title TEXT,
        UNIQUE(competitor, backlink_url)
    )
    """,
    # Serper 导航站逆向
    """
    CREATE TABLE IF NOT EXISTS serper_candidates (
        id INTEGER PRIMARY KEY,
        domain TEXT UNIQUE,
        appearance_count INTEGER,
        discovered_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """,
    # 黑名单（不能提交的垃圾站）
    """
    CREATE TABLE IF NOT EXISTS spam_blacklist (
        id INTEGER PRIMARY KEY,
        domain_pattern TEXT UNIQUE,
        added_date TEXT DEFAULT CURRENT_DATE,
        reason TEXT
    )
    """,
]

# B2 预灌数据
ANCHORS = [
    ("Yolox", "brand"),
    ("Yolox AI Agents", "brand"),
    ("Yolox AI Agents Marketplace", "brand"),
    ("AI agents marketplace", "lsi"),
    ("agent marketplace platform", "lsi"),
    ("AI agents for solo founders", "lsi"),
    ("marketplace for AI agents and skills", "lsi"),
    ("agentic workflow platform", "lsi"),
    ("multi-agent collaboration platform", "lsi"),
    ("AI skills marketplace", "lsi"),
    ("a platform called Yolox that lets you...", "descriptive"),
    ("tools like Yolox", "descriptive"),
    ("marketplaces such as Yolox", "descriptive"),
    ("yolox.ai", "naked"),
    ("Yolox AI 智能体平台", "chinese"),
    ("AI Agent 平台 Yolox", "chinese"),
]

PAGES = [
    ("https://yolox.ai/", "home", 1),
    ("https://yolox.ai/agents-store", "agents_list", 2),
    ("https://yolox.ai/skills-store", "skills_list", 2),
    ("https://yolox.ai/teams-store", "teams_list", 2),
    ("https://yolox.ai/blog", "blog_index", 3),
]

SPAM = [
    ("weknow.website", "案例垃圾站 #25"),
    ("backlink.wiki", "案例垃圾站 #25"),
    ("zhanhao.online", "案例垃圾站 #25"),
    ("pranksfl.lol", "案例垃圾站 #25"),
    ("vickys.design", "案例垃圾站 #25"),
    ("*.lol", "高风险后缀"),
    ("*casino*", "关键词模式"),
    ("*betting*", "关键词模式"),
    ("*loan*", "关键词模式"),
    ("*pharmacy*", "关键词模式"),
    ("*viagra*", "关键词模式"),
    ("backlink.*", "backlink 前缀"),
    ("*-backlinks.*", "backlinks 后缀"),
]


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for stmt in SCHEMA:
        cur.execute(stmt)

    cur.executemany(
        "INSERT OR IGNORE INTO yolox_anchors (anchor_text, type) VALUES (?, ?)",
        ANCHORS,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO yolox_pages (url, page_type, priority) VALUES (?, ?, ?)",
        PAGES,
    )
    cur.executemany(
        "INSERT OR IGNORE INTO spam_blacklist (domain_pattern, reason) VALUES (?, ?)",
        SPAM,
    )

    conn.commit()

    print("=== TABLES ===")
    for row in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ):
        count = cur.execute(f"SELECT COUNT(*) FROM {row[0]}").fetchone()[0]
        print(f"  {row[0]:<28} {count:>5} rows")

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
