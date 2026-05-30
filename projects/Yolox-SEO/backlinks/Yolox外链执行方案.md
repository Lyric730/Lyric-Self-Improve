# Yolox 外链执行方案 v3 — 深度小众 + 自动化拉满

> **定位**：攻坚手册。不立规矩，不分大众优先级。**所有能用的解法全列**——黑白灰不管，好用就用。
>
> **配套**：《深度长文.md》= 知识根据；本文 = 行动手册；`data/backlinks.db` = 数据武器库（已含 xlsx 226 条 + 后续衍生）。
>
> **驱动引擎**：Claude Code + Playwright MCP 是主力机器人。所有模块围绕"喂给机器人 + 让它自己跑"设计。

---

## 整体执行编排（把资源和方法串起来）

> 这一节是"指南的指南"。先读完它再去看后面 §1-§11 的细节。

### 0.1 核心思路：把 Yolox 当成一条 "外链生产线" 来跑

不是一个个手动发外链，**而是建一条流水线**：

```
原料端           →   引擎端           →   产出端          →   回流
─────────             ─────────              ─────────         ────
xlsx 226 条           Claude Code            submissions       data/
LXX.ai                + Playwright MCP       表 + 真实 URL     backlinks.db
EgoLinks                                                       (中央仓库)
Ahrefs API           （主力机器人）          rel 验证后回写
Serper.dev           ─────────              ─────────
8 套独家骚操作         CapSolver
Yolox 产品收割         BacklinkHelper
                      ─────────
```

**所有动作只服务一件事**：让 `data/backlinks.db` 里 `submissions` 表的 `dofollow` 行数每周增长。

### 0.2 编排原则（决定谁先做、谁并行、谁后做）

| 原则 | 含义 |
|---|---|
| **现成数据优先** | xlsx 226 条已经过验证，先把它跑完，不要先去搞新候选 |
| **基础设施先建一次** | DB schema / Skill 文件 / Chrome 插件 / Playwright MCP 装好后不再重做 |
| **代码改造与数据流并行** | Yolox 产品层的 Featured Embed 改造（§5）和数据流跑批（§3）**互不依赖**——同时做 |
| **候选池扩张永远晚于第一波跑通** | 先把 210 条跑通验证流水线，再去 §6 搞新数据源 |
| **半自动玩法靠脚本启动后基本不用管** | TG 频道、NPM 包、Hatena 书签都是"建好后自动跑"模式 |
| **监控/防御从 Day 1 就要开** | 不是后置任务，跟流水线一起上线 |

### 0.3 六阶段串联（A → F）

> 阶段间是"前置依赖"关系——A 没完成时不能跑 B。同一阶段内的子项可以并行。

```
┌──────────────────────────────────────────────────────────────┐
│ A. 基础设施搭建（一次性，~半天到 1 天）                         │
│    ├─ A1: Playwright MCP + Chrome 插件 + 3 个 Gmail            │
│    ├─ A2: data/backlinks.db 建好 7 张表 + 预灌锚文本/页面/黑名单 │
│    └─ A3: .claude/skills/backlinks/ 4 个 SKILL md 文件         │
└────────────────────────────┬─────────────────────────────────┘
                             │
        ┌────────────────────┼─────────────────────┐
        ▼                    ▼                     ▼
┌───────────────┐  ┌──────────────────┐  ┌────────────────────┐
│ B. 第一波速产  │  │ C. 产品层改造     │  │ G. 监控/防御启动    │
│ （5-7 天）     │  │ （与 B 并行）     │  │ （Day 1 就上）      │
│               │  │                  │  │                    │
│ B1: 226 全跑  │  │ C1: agents-store │  │ G1: GSC API 接入   │
│     (主力)    │  │     Featured     │  │     周报脚本       │
│ B2: whois     │  │     Embed 改造   │  │ G2: spam blacklist │
│     动态页    │  │ C2: GitHub       │  │     预灌完毕       │
│ B3: TG 频道   │  │     Awesome List │  │ G3: Disavow 预案  │
│ B4: Hatena    │  │     建仓库+推广  │  │     文件占位       │
└──────┬────────┘  └────────┬─────────┘  └──────────┬─────────┘
       │                    │                       │
       │                    │                       │
       └──────┬─────────────┴───────────────────────┘
              ▼ （B 验证流水线跑通后才进入 D）
┌──────────────────────────────────────────────────────────────┐
│ D. 候选池扩张（B 跑通后，1-2 周）                                │
│    ├─ D1: Ahrefs 未公开 API → 21 同行 Top 20（CapSolver 配合） │
│    ├─ D2: Serper.dev 1 万 AI 站点逆向 → Top 100 导航站         │
│    └─ D3: LXX.ai + EgoLinks + submitatool 三源导入             │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼ （喂回引擎）
┌──────────────────────────────────────────────────────────────┐
│ E. 第二波规模化（D 候选入库后，持续跑）                          │
│    ├─ E1: 新候选喂回 B1 流水线（同一 Claude Code Skill 直接复用）│
│    ├─ E2: nofollow→Dofollow bypass 升级 159 条 blog_comment    │
│    ├─ E3: NPM 包 + WP Plugin 发布（产出 30+ dofollow）          │
│    └─ E4: 列表诱饵 Blog × 3 + 8 平台分发                       │
└────────────────────────────┬─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│ F. 稳态运转（每周 cron 自动跑）                                  │
│    ├─ F1: 周一跑 run-batch.py 50 条                            │
│    ├─ F2: 周六刷新候选池（Ahrefs + Serper）                    │
│    ├─ F3: 周日交叉验证 + 周报                                  │
│    └─ F4: 异常告警自动 Disavow                                 │
└──────────────────────────────────────────────────────────────┘
```

### 0.4 数据怎么"穿"起来：以 1 条外链的全生命周期为例

```
  ┌────────────────────────────────────────────────────────┐
  │  以一条来自 "ageofwargame.io 外链池里的 phpBB Profile"   │
  │  的资源为例，跟踪它从原料到产出再到回流的完整生命周期    │
  └────────────────────────────────────────────────────────┘

[1] 原料入库
    xlsx → /外链/data/backlinks.db.gefei_226
    id=42, type='profile', url='https://example-forum.com/memberlist...',
    discovered_from='ahrefs:ageofwargame.io', has_captcha='No',
    link_strategy='url_field', submitted='no'

[2] 调度
    周一 9:00 cron 触发 scripts/run-batch.py 50
    SELECT 取出含 id=42 的批次
    生成 prompt 写入 .claude/queue/next.txt

[3] 执行
    Claude Code 用 backlinks Skill 读队列
    → profile.md SOP 执行
    → Playwright MCP 打开 URL，注册账号 (yolox.dev@gmail.com)
    → SELECT yolox_pages WHERE priority=1 ORDER BY RANDOM() → 拿到目标 URL
    → SELECT yolox_anchors WHERE type='lsi' → 拿到 bio 用语
    → Website 字段填 https://yolox.ai/agents-store
    → Bio 填 "Founder of [Yolox AI Agents Marketplace](...)"
    → 保存 Profile

[4] 验证
    → 跳转到 Profile 公开页
    → 跑 verify-rel.md 的 JS
    → 返回 {status: 'dofollow', rel: '', href: 'https://yolox.ai/...'}

[5] 回写
    UPDATE gefei_226 SET submitted='yes', rel_actual='dofollow',
        live_url='https://example-forum.com/profile/yolox-dev'
        WHERE id=42;
    INSERT INTO submissions (source_table, source_id, platform_domain,
        submit_url, target_yolox_url, anchor_text, submit_method, submit_time,
        status, rel_actual, live_url)
        VALUES ('gefei_226', 42, 'example-forum.com', '...', 'https://yolox.ai/...',
                'Yolox AI Agents Marketplace', 'MCP', NOW(), 'live', 'dofollow', '...');

[6] 监控（次周一 G1 触发）
    weekly-report.py 读 submissions
    周报输出："本周 dofollow +1, example-forum.com → /agents-store"

[7] 持续跟踪
    如果 4 周后 status 依然 = 'live' → 标记 'persistent'
    如果被删 → status='dead' + 加入个人 dead-sites 知识库
```

**这就是"串起来"的核心**：所有动作的最终目的都是往 `submissions` 表加一行 dofollow，并让 `gefei_226 / ahrefs_api / serper / lxx_ai` 这几个候选池**永远有比 submitted 数量多的 pending 行**。

### 0.5 模块之间的依赖关系一览

| 模块 | 依赖 | 阻塞谁 |
|---|---|---|
| A. 基础设施 | 无 | A 不完成，B/C/D/E 都不能开始 |
| B1. 226 全跑 | A | B 不跑通，D 没必要扩张 |
| B2. whois 动态页 | A2（DB blacklist） | 独立 |
| B3. TG 频道 | A1（Bot API） | 独立 |
| B4. Hatena | A1（账号） | 独立 |
| C1. Featured Embed | yolox-web 代码权限 | 不阻塞 B |
| C2. Awesome List | GitHub 个人账号 | 不阻塞 B |
| D1-D3. 候选池扩张 | **B1 跑通验证流水线** | 是 E 的前置 |
| E1. 新候选喂回 | D1-D3 | — |
| E2. nofollow bypass | B1 完成 + 159 条 blog_comment 列表 | — |
| E3. NPM/WP Plugin | A1（npm/wp 账号） | 不阻塞 |
| E4. 列表诱饵 Blog | C2 之后做更好（互推） | 不阻塞 |
| F. 稳态 cron | 所有上面跑通后启动 | — |
| G. 监控/防御 | **Day 1 上**，不能后置 | — |

### 0.6 如果只看这一段也能开始：4 步启动法

> 不想读 1788 行？只看这 4 步：

1. **跑 §0 → §2 装好基础设施**（半天）
   - Playwright MCP + Chrome 插件 + 3 个 Gmail + DB schema + Skill 文件
2. **同时启动 B1 + C2**（数据流 + 产品自媒体）
   - `python3 scripts/run-batch.py 10` 试跑 10 条
   - GitHub Awesome AI Agents 2026 repo 建好
3. **验证 B1 跑通后开 D**（扩张候选池）
   - 跑 Ahrefs API + Serper 两个候选池脚本
4. **稳定后进 F**（cron 自动化）
   - crontab 加 4 行（见 §7）

后续所有迭代都是"加新数据源 → 喂回 B1 流水线 → 更多 dofollow"。

---

## 0. 模块地图

```
                     ┌──────────────────────────────────┐
                     │  Claude Code + Playwright MCP    │
                     │     （主战引擎，单实例起步）       │
                     └────┬───────────┬───────────┬─────┘
                          │           │           │
        ┌─────────────────┘           │           └────────────────┐
        ▼                             ▼                            ▼
┌─────────────────┐         ┌──────────────────┐        ┌──────────────────┐
│ 模块 1          │         │ 模块 2           │        │ 模块 3           │
│ 226 条 xlsx     │         │ 哥飞独家骚操作    │        │ Yolox 产品收割   │
│ 全自动批量      │         │ 8 套打法         │        │ 反向被动外链     │
│                 │         │                  │        │                  │
│ 92.9% 无验证码   │         │ DR 90+ 平台      │        │ Featured 机制    │
│ 一键提交+验证    │         │ 高 DR / 灰白都做  │        │ Awesome List     │
└────────┬────────┘         └────────┬─────────┘        └────────┬─────────┘
         │                           │                           │
         └─────────────┬─────────────┴───────────────────────────┘
                       ▼
            ┌──────────────────────┐
            │ 模块 4               │
            │ 候选池持续供给        │
            │ LXX.ai + Ahrefs API  │
            │ + Serper 导航站逆向   │
            └──────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  data/backlinks.db   │
            │  本地 SQLite 武器库   │
            └──────────────────────┘
```

**资源池一览**（这些是子弹）：

| 资源 | 量 | 状态 |
|---|---|---|
| xlsx 226 条免登录免注册 | 226 | ✅ 已入 `data/backlinks.db` |
| LXX.ai 精选数据库 | 3000+ | 兑换码 `GEFEI` |
| EgoLinks 高权重清单 | 150 站 | egolinks.online/@backlinks |
| submitatool.com（oldcai 整理） | ~50 站 | 现成清单 |
| 哥飞独家骚操作 | 8 套 | 见 §4 |
| Yolox 自有 agents/skills/teams store | 全平台 | 见 §5 |

---

## 1. 资源池盘点（弹药库）

### 1.1 xlsx 226 条 ⭐⭐⭐ 已入 SQLite

哥飞用浏览器插件分析了 21 个小游戏种子站的 841 个外链，清洗出 **226 条免登录免注册即可发布**的资源。

**关键画像**：

| 维度 | 分布 |
|---|---|
| 总条数 | 226 |
| 无验证码 | **221**（97.8%）|
| url_field 策略 | **214**（94.7%）|
| **无验证码 + url_field（可完全自动化）** | **210**（92.9%）|
| Type: blog_comment | 159（无验证码 154）|
| Type: profile | 67（无验证码 67）|

**已入数据库**：`/外链/data/backlinks.db` → 表 `gefei_226`

字段：`id, type, url, discovered_from, has_captcha, link_strategy, link_format, has_url_field, root_domain, submitted, submit_time, rel_actual, live_url, notes`

**直接可跑的查询**：

```sql
-- 取本次要批量提交的 210 条
SELECT id, type, url, link_format, root_domain 
FROM gefei_226 
WHERE has_captcha='No' AND link_strategy='url_field' AND submitted='no'
ORDER BY type, root_domain;

-- 按种子站分批（21 个种子站）
SELECT discovered_from, COUNT(*) FROM gefei_226 GROUP BY discovered_from;
```

### 1.2 LXX.ai 3000+ 精选

**步骤**：
1. 注册 [lxx.ai](https://www.lxx.ai/)
2. 用户中心 → 兑换码 `GEFEI` → 1 年免费
3. 筛选 "AI Tools" + "Startup" → 导出 CSV
4. `import_lxx_to_db.py`（见 §6.1）→ 入 SQLite 同表

### 1.3 EgoLinks /@backlinks 150 个高权重清单

**入口**：[egolinks.online/@backlinks](https://egolinks.online/@backlinks)

**用法**（不止是被动看）：
1. 注册 egolinks.online 自己账号
2. 创建你的聚合页：`egolinks.online/@yolox`
3. 把 yolox.ai 重要页面（agents-store / skills-store / blog 主文章）全部加进去
4. 顺便引用 `@backlinks` 那 150 站的链接到你的聚合页 → 你的聚合页会被这些站收录到 ego linker
5. 自己的聚合页 URL 加到 yolox.ai footer → 让 Google 抓你聚合页时把那 150 个 outbound 一起看到

### 1.4 submitatool.com（oldcai 整理）

[submitatool.com](https://submitatool.com/) 是 [#26] 作者 oldcai 整理的"实测可成功提交的导航站清单"。

**接入方法**：
1. 爬取该站列表（站本身鼓励爬取）
2. 入 SQLite 表 `submitatool_dirs`（schema 见 §6）
3. 加入模块 1 批量队列

```python
# 一次性爬取脚本骨架
import requests, sqlite3
from bs4 import BeautifulSoup

resp = requests.get('https://submitatool.com/')
soup = BeautifulSoup(resp.text, 'html.parser')
# 解析站点清单 → 入库
```

### 1.5 哥飞独家骚操作（8 套）

详见 §4。预览：

| 套 | 渠道 | DR | 自动化等级 |
|---|---|---|---|
| 1 | WP whois 动态页（薅 link.zhihu.com 等） | 子域名 95+ | 🤖🤖🤖 完全自动 |
| 2 | WP 评论 nofollow → Dofollow 正则 bypass | 各 | 🤖🤖 半自动 |
| 3 | NPM 包发布薅 npmjs.com | 92 | 🤖🤖🤖 完全自动 |
| 4 | WP Plugin 官方目录 wordpress.org/plugins | 高 | 🤖 半手动 |
| 5 | Telegram 频道（后端渲染 dofollow） | t.me 高 | 🤖🤖🤖 完全自动 |
| 6 | Hatena Bookmark 日本高权重 | 88 | 🤖🤖 半自动 |
| 7 | 阳光杉木 Serper.dev 导航站逆向 | 各 | 🤖🤖🤖 完全自动 |
| 8 | 226 衍生：链轮挖掘自动化（Ahrefs 未公开 API） | 各 | 🤖🤖🤖 完全自动 |

### 1.6 Yolox 产品自身（被动收割）

详见 §5。Yolox 已经是收录平台 → 反过来让被收录方给我们外链：

- agents-store Featured Embed
- GitHub Awesome AI Agents 自建
- 列表诱饵 Blog

---

## 2. 自动化武器库

### 2.1 Claude Code + Playwright MCP（主力）

**装配清单**：

```bash
# 1. Playwright MCP（Anthropic 官方）
cd /home/lyric/Infinite\ Flow\ Project/SEO/yolox-web/外链
npm init -y
npm install @playwright/mcp playwright
npx playwright install chromium

# 2. 项目级 settings.json（让 Claude Code 知道 MCP 在哪）
cat > .claude/settings.local.json <<'EOF'
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp", "--headless=false"]
    }
  }
}
EOF

# 3. SKILL 知识库（4 个精简文件）
mkdir -p .claude/skills/backlinks
# 内容见 §3.2
```

**单实例 vs 多实例**：先单实例。稳定后再用 tmux 起 4 个 Profile 并发（[长文§5.3]）。

### 2.2 CF Turnstile 绕过工具栈

| 工具 | 类型 | 用途 | 成本 |
|---|---|---|---|
| **CapSolver** [capsolver.com/products/cloudflare](https://www.capsolver.com/products/cloudflare) | 付费 | Turnstile 解，3s 出 token | $1.2/1000 |
| 折扣码 | — | `brightdata` | 5% off |
| **2Captcha** [2captcha.com/p/cloudflare-turnstile](https://2captcha.com/p/cloudflare-turnstile) | 付费 | 备用 | 类似 |
| **DrissionPage** [drissionpage.cn](https://drissionpage.cn/) | 开源 | Python 自带 CF 绕过 | 免费 |
| **CloudflareBypassForScraping** [github.com/sarperavci/CloudflareBypassForScraping](https://github.com/sarperavci/CloudflareBypassForScraping) | 开源 | undetected-chrome 系 | 免费 |
| **Turnstile-Solver** [github.com/Theyka/Turnstile-Solver](https://github.com/Theyka/Turnstile-Solver) | 开源 | 纯 Python | 免费 |

**优先**：DrissionPage（中文友好+免费）→ CapSolver（兜底）。

### 2.3 浏览器辅助插件（人工介入时用）

| 插件 | 商店 | 用途 |
|---|---|---|
| sitedata | [Chrome 商店](https://chromewebstore.google.com/detail/emeakbgdecgmdjgegnejpppcnkcnoaen) | 一键看页面外链 + 域名年龄 + 流量 |
| BacklinkHelper | [Chrome 商店](https://chromewebstore.google.com/detail/backlinkhelper-–-智能外链提交助手/njplbneiegbjpmaiemjogaeilmbjnkij) | 复杂站手动兜底 + 看 rel 状态（Local-First 模式，不开飞书同步） |

### 2.4 数据流：SQLite + Python

**统一仓库**：`/外链/data/backlinks.db`

**当前已有表**：

```sql
-- 已建好
CREATE TABLE gefei_226 (...); -- 226 条原始资源
```

**v3 需要新增表**：

```sql
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY,
    source_table TEXT,        -- gefei_226 / lxx_ai / serper_found / ahrefs_api
    source_id INTEGER,        -- 关联源表
    platform_domain TEXT,
    submit_url TEXT,
    target_yolox_url TEXT,
    anchor_text TEXT,
    submit_method TEXT,       -- MCP / 人工 / BacklinkHelper / npm-cli / WP-cli
    submit_time TEXT,
    status TEXT,              -- pending / submitted / live / dead / failed
    rel_actual TEXT,          -- empty / nofollow / ugc / dofollow
    live_url TEXT,
    error_log TEXT,
    notes TEXT
);

CREATE TABLE lxx_ai (...);          -- §6.1
CREATE TABLE serper_candidates (...); -- §6.3
CREATE TABLE ahrefs_api_results (...); -- §6.2
CREATE TABLE submitatool_dirs (...);  -- §1.4

CREATE TABLE yolox_anchors (
    id INTEGER PRIMARY KEY,
    anchor_text TEXT,
    type TEXT,  -- brand / lsi / descriptive / naked / chinese
    use_count INTEGER DEFAULT 0
);

CREATE TABLE yolox_pages (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    page_type TEXT,  -- home / agent_detail / skill_detail / blog
    priority INTEGER -- 1=highest
);
```

**Yolox 锚文本预灌**（直接插入 `yolox_anchors`）：

```sql
INSERT INTO yolox_anchors (anchor_text, type) VALUES
  ('Yolox', 'brand'),
  ('Yolox AI Agents', 'brand'),
  ('Yolox AI Agents Marketplace', 'brand'),
  ('AI agents marketplace', 'lsi'),
  ('agent marketplace platform', 'lsi'),
  ('AI agents for solo founders', 'lsi'),
  ('marketplace for AI agents and skills', 'lsi'),
  ('agentic workflow platform', 'lsi'),
  ('multi-agent collaboration platform', 'lsi'),
  ('AI skills marketplace', 'lsi'),
  ('a platform called Yolox that lets you...', 'descriptive'),
  ('tools like Yolox', 'descriptive'),
  ('marketplaces such as Yolox', 'descriptive'),
  ('yolox.ai', 'naked'),
  ('Yolox AI 智能体平台', 'chinese'),
  ('AI Agent 平台 Yolox', 'chinese');
```

**目标页面预灌**：

```sql
INSERT INTO yolox_pages (url, page_type, priority) VALUES
  ('https://yolox.ai/', 'home', 1),
  ('https://yolox.ai/agents-store', 'agents_list', 2),
  ('https://yolox.ai/skills-store', 'skills_list', 2),
  ('https://yolox.ai/teams-store', 'teams_list', 2),
  ('https://yolox.ai/blog', 'blog_index', 3);
```

---

## 3. 模块 1：226 条全自动批量

> 目标：把 `gefei_226` 表里 210 条 "无验证码 + url_field" 的资源喂给 Playwright MCP，一周跑完。

### 3.1 数据流水线

```
gefei_226 (DB)
   │
   │  SELECT WHERE has_captcha='No' AND link_strategy='url_field' AND submitted='no'
   ▼
Claude Code Agent Loop:
   │ ① 取下一条
   │ ② 读 platform_type 决定走 §3.3 (comment) 或 §3.4 (profile)
   │ ③ Playwright MCP 打开 URL
   │ ④ 注册账号 (如果需要) / 找表单
   │ ⑤ 填字段 (锚文本从 yolox_anchors 随机选)
   │ ⑥ 提交
   │ ⑦ rel 验证脚本
   │ ⑧ 写回 submissions 表
   │ ⑨ 失败则记 error_log, status=failed
   │ ⑩ goto ①
```

### 3.2 Claude Code Skill 文件（4 个精简）

`/外链/.claude/skills/backlinks/SKILL.md`：

```markdown
# Yolox Backlinks Skill

When asked to "submit backlinks" or "run batch":
1. Connect to SQLite: /外链/data/backlinks.db
2. Query: SELECT * FROM gefei_226 WHERE submitted='no' AND has_captcha='No' AND link_strategy='url_field' ORDER BY type LIMIT N
3. For each row:
   - If type='blog_comment': follow comment.md SOP
   - If type='profile': follow profile.md SOP
4. After each submission, verify rel using verify-rel.md
5. UPDATE gefei_226 SET submitted='yes', submit_time=NOW(), and INSERT into submissions

Reference files:
- comment.md - WP/forum comment submission SOP
- profile.md - profile field submission SOP
- verify-rel.md - rel attribute verification scripts
- anti-spam.md - 6 anti-spam systems bypass methods
```

`comment.md`：

```markdown
# Blog Comment Submission SOP

For each URL:
1. browser_navigate to URL
2. browser_snapshot — find the comment form
3. Locate fields:
   - Name field → use random English name (avoid "Yolox")
   - Email field → yolox.outreach@gmail.com
   - **URL/Website field** → pick from yolox_pages weighted by priority
   - Comment textarea → AI-generate 50-80 word contextually relevant comment
4. For comment text, use browser_fill_form to fill name/email/URL fields
5. For textarea, use pressSequentially (one char at a time) to bypass Antispam Bee
6. If textarea has rel bypass opportunity (see anti-spam.md bypass-1):
   - In comment textarea, embed: <a href="https://yolox.ai/\n">anchor</a> with real newline char
7. browser_evaluate to check captcha presence
   - If present and not in has_captcha=Yes: skip (data is stale)
8. Submit (use HTMLFormElement.prototype.submit.call if form.submit() shadowed)
9. Wait for redirect to #comment-XXX or ?unapproved=XXX
10. Run verify-rel.md
```

`profile.md`：

```markdown
# Profile Field Submission SOP

For each URL (URL is profile edit page or member page):
1. browser_navigate to URL
2. Check if requires login:
   - Yes: Try register flow with yolox.outreach@gmail.com
   - No (xlsx URLs are pre-filtered): proceed
3. Find "Website" / "URL" / "Homepage" / "Personal Site" field
4. Pick yolox_pages.url weighted by priority for THIS profile
5. Fill bio/description if exists:
   - Use anchor from yolox_anchors weighted by type=descriptive 60%, lsi 40%
   - "Founder of [Yolox](https://yolox.ai) — an AI Agents marketplace"
6. Save profile
7. browser_navigate to profile page URL (the one with Website field visible)
8. Run verify-rel.md against the website link
```

`verify-rel.md`：

```markdown
# Rel Attribute Verification

After submission, run in browser console:

```js
const yoloxLinks = document.querySelectorAll('a[href*="yolox.ai"]');
if (yoloxLinks.length === 0) {
  return { status: 'failed', reason: 'no_link_found' };
}
const link = yoloxLinks[0];
const rel = (link.rel || '').trim();
let status;
if (rel === '' || rel === 'noopener' || rel === 'noopener noreferrer') {
  status = 'dofollow';
} else if (rel.includes('ugc')) {
  status = 'ugc';  // counts as nofollow
} else if (rel.includes('nofollow')) {
  status = 'nofollow';
} else {
  status = 'unknown:' + rel;
}
return { status, rel, href: link.href };
```

UPDATE submissions SET rel_actual=<status>, live_url=<window.location.href> WHERE id=<current_id>
```

`anti-spam.md` (核心反垃圾绕过)：

```markdown
# Anti-Spam Bypass Cookbook

## Akismet (most common)
- Symptoms: Comment submitted but never appears
- Bypass: clean Gmail (yolox.outreach@gmail.com) + random REAL name + link only in author URL field (not in body)

## Antispam Bee (German blogs)
- Symptoms: 403 on submit
- Bypass: Use pressSequentially() for ALL text fields, NOT element.value=''
  ```js
  await page.locator('textarea[name="comment"]').pressSequentially(text, { delay: 50 })
  ```

## CleanTalk
- Symptoms: 403 with "CleanTalk" string in response
- Bypass: NONE. Skip this URL. UPDATE gefei_226 SET notes='CleanTalk', submitted='dead'

## hCaptcha Enterprise
- Symptoms: hCaptcha appears with "enterprise" in script src
- Bypass: NONE. Skip.

## Jetpack Highlander
- Symptoms: Comment form is in cross-origin iframe
- Bypass: NONE. Skip.

## WPantispam Protect (random honeypot textareas)
- Symptoms: Random-named fields like ak_hp_textarea, alt_s, wantispam_e_*
- Bypass: LEAVE THESE BLANK. They're honeypots. Only fill the real comment field.

## form.submit() shadowed
- Symptoms: form.submit() throws "submit is not a function"
- Bypass: HTMLFormElement.prototype.submit.call(formElement)

## nofollow → Dofollow Bypass (special opportunity)
WP core wp_rel_nofollow() uses regex /<a (.+?)>/i WITHOUT /s flag
.+? doesn't match \n by default
So inject \n inside href:
  In comment body: <a href="https://yolox.ai/<REAL NEWLINE HERE>">anchor</a>
  Real \n = charCode 10 (not literal \n two chars)
  Playwright: when using pressSequentially, JS string '\n' becomes charCode 10 automatically
Verify: Check rel must be empty or only noopener/noreferrer.
  rel="ugc" or "nofollow ugc" = FAILED (don't get fooled)
Success rate: 38-60% (other 40-62% has wp_kses strip, extra sanitize, etc.)
```

### 3.3 一键启动脚本

`/外链/scripts/run-batch.py`：

```python
#!/usr/bin/env python3
"""一键启动 Claude Code 处理 N 条 gefei_226 记录"""
import sqlite3, sys, subprocess, json
from pathlib import Path

ROOT = Path(__file__).parent.parent
db = sqlite3.connect(ROOT / 'data/backlinks.db')
batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10

rows = db.execute("""
    SELECT id, type, url, root_domain 
    FROM gefei_226 
    WHERE submitted='no' AND has_captcha='No' AND link_strategy='url_field'
    ORDER BY type, root_domain
    LIMIT ?
""", (batch_size,)).fetchall()

print(f"Pending: {len(rows)} URLs")
task_json = json.dumps([{'id': r[0], 'type': r[1], 'url': r[2], 'domain': r[3]} for r in rows])

# 让 Claude Code 跑这批
prompt = f"""
Use the Yolox Backlinks Skill. Process these {len(rows)} URLs:

{task_json}

For each: follow comment.md or profile.md SOP based on type.
After each submission, run verify-rel.md and INSERT into submissions table.
Update gefei_226 SET submitted='yes' after each row.

Report a summary table at the end.
"""

# 写入 prompt 文件，让 Claude Code 读
(ROOT / '.claude/queue/next.txt').write_text(prompt)
print(f"Queued {len(rows)} tasks. Run `claude` in this dir to start.")
```

### 3.4 单实例 vs 多实例

**单实例**（推荐起步）：

```bash
cd /外链
claude  # 启动 Claude Code
# 然后：跑 batch
> python3 scripts/run-batch.py 10
> 用 Yolox Backlinks Skill 跑队列里的任务
```

**多实例**（稳定后，参考 [长文§5.3]）：

```bash
tmux new-session -d -s yolox-A
tmux new-session -d -s yolox-B
tmux send-keys -t yolox-A "cd /外链/instance-A && claude" Enter
tmux send-keys -t yolox-B "cd /外链/instance-B && claude" Enter
# 每个 instance 用不同 Chrome Profile + 不同 Gmail
```

### 3.5 5 条带 captcha 的处理

```sql
SELECT id, url FROM gefei_226 WHERE has_captcha='Yes';
```

加 CapSolver 集成（`anti-spam.md` 追加）：

```python
import requests, time

def solve_turnstile(site_key, url, api_key='YOUR_CAPSOLVER_KEY'):
    """Returns token usable as captcha response"""
    r = requests.post('https://api.capsolver.com/createTask', json={
        'clientKey': api_key,
        'task': {
            'type': 'AntiTurnstileTaskProxyLess',
            'websiteKey': site_key,
            'websiteURL': url,
        }
    })
    task_id = r.json()['taskId']
    while True:
        time.sleep(1)
        rr = requests.post('https://api.capsolver.com/getTaskResult', json={
            'clientKey': api_key, 'taskId': task_id
        }).json()
        if rr.get('status') == 'ready':
            return rr['solution']['token']
```

让 Claude Code 在遇到 Turnstile 时调用这个函数，把 token 注入 `cf-turnstile-response` 隐藏字段。

---

## 4. 模块 2：哥飞独家骚操作 8 套

### 4.1 套 1：WP whois 动态页（薅子域名权重）

**原理**（[长文§4.6]）：高 DR 站的动态参数页面，会动态生成包含你域名的链接。如果该页面无 nofollow，搜索引擎收录后给你加一条 backlink。

**已知可利用的动态页**：

```
https://link.zhihu.com/?target=https%3A%2F%2Fyolox.ai
https://www.qiuyumi.com/whois/?domain=yolox.ai
https://tool.chinaz.com/tools/urlencode.aspx?... (待验证)
https://nslookup.io/lookup/?host=yolox.ai
https://similarweb.com/website/yolox.ai (生成)
```

**自动化构造 + 自动让搜索引擎抓的脚本**：

```python
# scripts/dynamic-page-backlink.py
"""
1. 列出已知可利用的动态页 URL 模板
2. 在 Yolox 自家页面（比如 yolox.ai/seo-resources/ 隐藏页）放这些链接
3. 用 IndexNow / Bing Webmaster API 推送 yolox.ai/seo-resources 让 Bing 抓
4. 用 GSC URL Inspection API 推送 Google
5. 等抓取 → 顺着链接抓动态页 → 给 yolox.ai 加 backlink
"""

YOLOX_DOMAIN = 'yolox.ai'
DYNAMIC_PAGES = [
    f"https://link.zhihu.com/?target=https%3A%2F%2F{YOLOX_DOMAIN}",
    f"https://www.qiuyumi.com/whois/?domain={YOLOX_DOMAIN}",
    f"https://nslookup.io/lookup/?host={YOLOX_DOMAIN}",
    f"https://similarweb.com/website/{YOLOX_DOMAIN}",
    f"https://www.alexa.com/siteinfo/{YOLOX_DOMAIN}",  # 死站但可能历史保留
    # 持续追加发现的
]

# 写一个 yolox.ai/seo-resources/ 静态页（不放主菜单）
html = """<!DOCTYPE html>
<html><head><title>SEO Resources</title>
<meta name="robots" content="noindex,follow">  <!-- 不让自己被搜，但允许爬虫 follow 链接 -->
</head><body>
<h1>SEO Resources</h1>
""" + "\n".join(f'<p><a href="{url}">link {i}</a></p>' for i, url in enumerate(DYNAMIC_PAGES)) + """
</body></html>"""

# 部署到 yolox.ai/seo-resources/index.html（next.js public/ 目录）
Path('public/seo-resources/index.html').write_text(html)
```

**关键**：
- 自己页面 `noindex,follow` — 自己不被收，但爬虫跟着跳到动态页
- 动态页被 Google 抓到后，**前提是动态页本身要 dofollow**——人工或脚本检测一次每个候选

**子站补充**：知乎子域名 link.zhihu.com 是哥飞实测的 [长文§3.1#15 评论区]，DR 95+。

### 4.2 套 2：WP 评论 nofollow → Dofollow 正则 bypass [#8]

**原理**：WP 核心 `wp_rel_nofollow()` 正则 `|<a (.+?)>|i` 没加 `/s` flag，`.+?` 默认不匹配 `\n`。

**Playwright 完整代码**：

```python
# scripts/wp-nofollow-bypass.py
"""
对所有 type=blog_comment 且 link_format=html 的目标
在评论正文塞 <a href="url\n">anchor</a>
"""
from playwright.sync_api import sync_playwright
import sqlite3, random, time

YOLOX_URL = 'https://yolox.ai/'
ANCHORS = ['Yolox AI Agents', 'Yolox', 'AI agents marketplace', 'tools like Yolox']

NAMES = ['John Smith', 'Sarah Johnson', 'Michael Brown', 'Emma Wilson', 'David Chen']
EMAIL = 'yolox.outreach@gmail.com'

def submit_with_bypass(page, target_url, comment_body):
    page.goto(target_url)
    page.wait_for_load_state('domcontentloaded')
    
    # 找标准 WP 评论字段
    page.locator('input[name="author"]').first.fill(random.choice(NAMES))
    page.locator('input[name="email"]').first.fill(EMAIL)
    # author URL 字段也填上 - 不一定有效但提交标准做法
    try:
        page.locator('input[name="url"]').first.fill(YOLOX_URL)
    except: pass
    
    # 核心：评论正文用 pressSequentially（绕 Antispam Bee）
    # 且 href 里塞真换行符（绕 WP wp_rel_nofollow）
    anchor = random.choice(ANCHORS)
    # 注意：'\n' 在 Python 字符串里是 charCode 10 字符
    comment_with_link = f'{comment_body} <a href="{YOLOX_URL}\n">{anchor}</a> Just my 2 cents.'
    page.locator('textarea[name="comment"]').first.press_sequentially(comment_with_link, delay=30)
    
    # 提交（用原型链绕过 name="submit" shadow）
    page.evaluate("""() => {
        const form = document.querySelector('form#commentform') || document.querySelector('form');
        HTMLFormElement.prototype.submit.call(form);
    }""")
    
    page.wait_for_load_state('networkidle', timeout=15000)
    return page.url

def verify_rel(page):
    """检查 yolox.ai 链接的 rel"""
    return page.evaluate("""() => {
        const ya = document.querySelectorAll('a[href*="yolox.ai"]');
        if (ya.length === 0) return {status: 'no_link'};
        const rel = (ya[0].rel || '').trim();
        if (rel === '' || rel === 'noopener' || rel === 'noopener noreferrer') return {status: 'dofollow', rel};
        if (rel.includes('ugc')) return {status: 'ugc_fail', rel};
        if (rel.includes('nofollow')) return {status: 'nofollow', rel};
        return {status: 'unknown', rel};
    }""")

# 主循环
db = sqlite3.connect('data/backlinks.db')
rows = db.execute("""
    SELECT id, url FROM gefei_226 
    WHERE type='blog_comment' AND link_format='html' AND submitted='no'
    LIMIT 30
""").fetchall()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context()
    
    for row_id, url in rows:
        page = ctx.new_page()
        try:
            # 生成切题评论（让 Claude Code 调用 OpenAI/Gemini API 生成；这里占位）
            body = f"Great post! I've been exploring similar tools and"
            submit_with_bypass(page, url, body)
            result = verify_rel(page)
            print(f"[{row_id}] {url} → {result}")
            
            db.execute("UPDATE gefei_226 SET submitted='yes', rel_actual=? WHERE id=?",
                       (result.get('status'), row_id))
            db.commit()
        except Exception as e:
            db.execute("UPDATE gefei_226 SET submitted='failed', notes=? WHERE id=?",
                       (str(e)[:200], row_id))
            db.commit()
        finally:
            page.close()
            time.sleep(random.randint(15, 45))  # 间隔，避免被风控
    
    browser.close()
```

**实测期望**：38-60% 成功率（[#8] 实测）。

### 4.3 套 3：NPM 包薅 npmjs.com DR 92

**两条玩法**：

#### 玩法 A（推荐）：发 Yolox 官方 NPM 包

```bash
# 在 yolox-web 项目下
mkdir -p packages/yolox-agents-sdk
cd packages/yolox-agents-sdk

cat > package.json <<'EOF'
{
  "name": "@yolox/agents-sdk",
  "version": "0.1.0",
  "description": "Official Yolox AI Agents SDK - Deploy and interact with AI agents",
  "main": "index.js",
  "homepage": "https://yolox.ai",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/yolox/agents-sdk.git"
  },
  "bugs": {
    "url": "https://github.com/yolox/agents-sdk/issues",
    "email": "support@yolox.ai"
  },
  "keywords": ["ai", "agents", "yolox", "ai-marketplace", "agentic-workflow"],
  "author": {
    "name": "Yolox Team",
    "url": "https://yolox.ai"
  },
  "license": "MIT"
}
EOF

cat > index.js <<'EOF'
// Yolox Agents SDK
const YOLOX_API = process.env.YOLOX_API || 'https://api.yolox.ai/v1';
module.exports = {
  agents: { list: async () => fetch(`${YOLOX_API}/agents`).then(r => r.json()) },
  skills: { list: async () => fetch(`${YOLOX_API}/skills`).then(r => r.json()) },
};
EOF

cat > README.md <<'EOF'
# @yolox/agents-sdk

Official SDK for [Yolox](https://yolox.ai) — AI Agents Marketplace.

## Install

```bash
npm install @yolox/agents-sdk
```

[Documentation](https://yolox.ai) · [GitHub](https://github.com/yolox/agents-sdk)
EOF

npm login  # 注册/登录
npm publish --access public
```

**结果**：`npmjs.com/package/@yolox/agents-sdk` 页面有 4 个 dofollow 链接指向 yolox.ai（homepage / author URL / repository / bugs）。

#### 玩法 B：薅老旧无人维护包

```bash
# 找老包：下载量大但 >1 年未更新
npm search --json mime-types | jq '.[]| select(.date < "2023-01-01") | .name'

# 或用 npms.io API：
curl 'https://api.npms.io/v2/search?q=ai+keywords:ai+is:not-deprecated&size=50' \
  | jq '.results[] | select(.score.detail.maintenance < 0.5) | .package.name'
```

找到候选 → fork 一份 → 让 Claude Code 写个升级版（如添 TypeScript 类型）→ 发新版本（注意 name 不能冲突，要换 scope 或新 name）→ package.json homepage 字段填 yolox.ai。

**风险**：npm 有 spam 检测。一周发 ≤ 3 个新包。

### 4.4 套 4：WP Plugin 官方目录 wordpress.org/plugins

**做一个 Yolox AI Agents Embed plugin**：让 WordPress 站长能在文章里嵌入 Yolox agent。

```php
// yolox-agents-embed/yolox-agents-embed.php
<?php
/*
Plugin Name: Yolox AI Agents Embed
Plugin URI: https://yolox.ai/wordpress-plugin
Description: Embed AI agents from Yolox marketplace into your WordPress posts. Visit https://yolox.ai to discover agents.
Version: 1.0.0
Author: Yolox Team
Author URI: https://yolox.ai
License: MIT
*/

function yolox_agent_shortcode($atts) {
    $atts = shortcode_atts(['id' => ''], $atts);
    $agent_id = esc_attr($atts['id']);
    return '<iframe src="https://yolox.ai/embed/agent/' . $agent_id . '" 
            width="100%" height="500" frameborder="0"></iframe>
            <p><small>Powered by <a href="https://yolox.ai">Yolox</a></small></p>';
}
add_shortcode('yolox_agent', 'yolox_agent_shortcode');
```

**提交流程**：
1. zip 整个目录
2. 提交到 [wordpress.org/plugins/developers/add/](https://wordpress.org/plugins/developers/add/)
3. 审核（5-30 天）通过后插件页面有：
   - Plugin Homepage → yolox.ai/wordpress-plugin（dofollow）
   - Author URI → yolox.ai（dofollow）
   - readme.txt 里允许多个外链

**衍生**：写 5-10 个微插件（Yolox Agent Sidebar / Yolox Skills Embed / Yolox Search Widget），每个都是一条 wordpress.org 外链。

### 4.5 套 5：Telegram 频道自建（后端渲染 dofollow）

**目标**：自建 `@YoloxAgents` 频道，每天发"AI Agent 行业动态"，每次顺手 mention yolox.ai。频道描述区放 yolox.ai（后端渲染 dofollow）。

**全自动发帖管线**：

```python
# scripts/tg-auto-poster.py
import requests, sqlite3
from datetime import datetime

TG_BOT_TOKEN = 'YOUR_BOT_TOKEN'  # @BotFather 获取
TG_CHANNEL = '@YoloxAgents'

def fetch_hn_top():
    """HN 热门 AI 话题"""
    ids = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()[:30]
    items = []
    for i in ids[:5]:
        s = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{i}.json').json()
        if s and any(k in (s.get('title','').lower()) for k in ['ai', 'agent', 'llm', 'gpt', 'claude']):
            items.append(s)
    return items

def post_to_tg(text, link=None):
    requests.post(
        f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage',
        json={
            'chat_id': TG_CHANNEL,
            'text': text + f"\n\n📌 Powered by Yolox — https://yolox.ai",
            'parse_mode': 'HTML',
            'disable_web_page_preview': False,
        }
    )

# 每天跑一次
items = fetch_hn_top()
text = "📰 <b>Today's AI Agent News</b>\n\n"
for it in items[:5]:
    text += f"• <a href='{it.get('url')}'>{it['title']}</a>\n"
post_to_tg(text)
```

**频道描述**（一次性设置）：
```
Daily AI Agent news & insights. Curated by https://yolox.ai — the marketplace for AI agents and skills.
```

**Cron**：
```cron
0 9 * * * cd /外链 && python3 scripts/tg-auto-poster.py
```

**dofollow 验证**：TG 频道的 t.me 链接是后端渲染 — 查看源码确认 `<a href="https://yolox.ai">` 无 rel="nofollow"。

**衍生**：建多个垂类频道：`@YoloxCodeAgents` `@YoloxResearchAgents` `@YoloxAgentJobs` 等，每个都是一条 t.me dofollow + 描述区 yolox.ai 链接。

### 4.6 套 6：Hatena Bookmark（日本 DR 88）

**操作**：

1. 注册 hatena.ne.jp（用 Google OAuth）
2. 装 Hatena Bookmark Chrome 插件 ([商店搜索](https://chromewebstore.google.com/search/hatena%20bookmark))
3. 用插件**收藏 yolox.ai 主要页面**（每个 agent detail 都可以收藏）
4. 收藏即生成 `b.hatena.ne.jp/<username>/<bookmark-id>` 页面，含 yolox.ai 链接

**让收藏页被 Google 收录**：
- yolox.ai/about 加 "Bookmarked us: [hatena profile URL]"
- 在 Twitter 发一次"我们的 Hatena 书签收藏"

**自动化收藏脚本**（如果手动嫌慢）：

```python
# Hatena Bookmark API
# https://developer.hatena.ne.jp/ja/documents/bookmark/apis/atom
import requests
from requests_oauthlib import OAuth1Session

# OAuth 凭证（hatena 开发者中心申请）
hatena = OAuth1Session(
    client_key='YOUR_KEY',
    client_secret='YOUR_SECRET',
    resource_owner_key='YOUR_TOKEN',
    resource_owner_secret='YOUR_TOKEN_SECRET'
)

def bookmark_url(url, comment):
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://purl.org/atom/ns#">
  <link rel="related" type="text/html" href="{url}" />
  <summary type="text/plain">{comment}</summary>
</entry>"""
    return hatena.post(
        'https://bookmark.hatenaapis.com/rest/1/my/bookmark',
        data=xml.encode('utf-8'),
        headers={'Content-Type': 'application/xml'}
    )

# 批量收藏 Yolox 所有重要页
URLS = [
    ('https://yolox.ai/', 'AI Agents Marketplace'),
    ('https://yolox.ai/agents-store', 'AI Agents Catalog'),
    ('https://yolox.ai/skills-store', 'AI Skills Marketplace'),
    # ... 加更多
]
for url, comment in URLS:
    bookmark_url(url, comment)
```

### 4.7 套 7：阳光杉木导航站逆向（Serper.dev 批量）

**思路**（[长文§4.2]）：用 TAAFT / Toolify.ai 的 1 万 AI 站点名搜 Google，前 30 结果汇总 → 找出"经过谷歌检验的能拿流量的导航站"清单。

**完整脚本**：

```python
# scripts/serper-nav-reverse.py
"""
找经过谷歌检验、能拿流量的导航站
1. 拉 TAAFT / Toolify.ai 的 AI 站点列表（开源/爬取）
2. 每个站点名 + " review" 或 " alternative" → Serper.dev
3. 前 30 结果聚合 → 频次排序
4. Top 100 自动入 serper_candidates 表
"""
import requests, sqlite3, time
from collections import Counter
from urllib.parse import urlparse

SERPER_KEY = 'YOUR_SERPER_KEY'  # serper.dev 免费 2500 queries

def google_search(query, n=30):
    r = requests.post('https://google.serper.dev/search',
        headers={'X-API-KEY': SERPER_KEY},
        json={'q': query, 'num': n, 'gl': 'us'})
    return r.json().get('organic', [])

# 1. 拿 1000 个 AI 工具名（这里假设已从 TAAFT 爬取）
ai_tool_names = open('data/ai_tool_names.txt').read().split('\n')[:1000]

# 2. 对每个工具搜 "<name> review"
hosts = Counter()
for i, name in enumerate(ai_tool_names):
    if i % 50 == 0: print(f"Progress: {i}/{len(ai_tool_names)}")
    results = google_search(f'{name} review')
    for r in results:
        try:
            h = urlparse(r['link']).netloc.lower().replace('www.', '')
            hosts[h] += 1
        except: pass
    time.sleep(1)  # 别打太快

# 3. Top 100 入库
db = sqlite3.connect('data/backlinks.db')
db.execute("""CREATE TABLE IF NOT EXISTS serper_candidates (
    id INTEGER PRIMARY KEY,
    domain TEXT UNIQUE,
    appearance_count INTEGER,
    discovered_at TEXT DEFAULT CURRENT_TIMESTAMP
)""")
for host, count in hosts.most_common(100):
    db.execute("INSERT OR IGNORE INTO serper_candidates (domain, appearance_count) VALUES (?, ?)",
               (host, count))
db.commit()

print(f"Stored {len(hosts)} candidate directories.")
print("Top 20:", hosts.most_common(20))
```

**多国家扩展**（[长文§4.2]）：

```python
# 同样脚本，gl 参数换成 'jp' / 'kr' / 'de' / 'br'
results_jp = google_search(f'{name} レビュー', n=30)  # 日本
results_kr = google_search(f'{name} 리뷰', n=30)  # 韩国
```

**结果**：得到 100-300 个"在 AI 工具搜索结果里反复出现"的导航站 → 这些 100% 是 Google 认可的、能拿流量的、值得提交的。

### 4.8 套 8：226 衍生——链轮挖掘自动化（Ahrefs 未公开 API）

**思路**：xlsx 226 条来自 21 个游戏种子站。同样思路应用到 AI Agent 平台 → 取 21 个 AI 同行 → 每个用 Ahrefs API 拉 Top 20 best links → 衍生出 N00 条新候选。

**Ahrefs 未公开 API 完整脚本**（来自 [#7]）：

```python
# scripts/ahrefs-best-links.py
import requests, time, sqlite3

API_KEY = 'CAP-XXXX'  # CapSolver API key
SITE_KEY = '0x4AAAAAAAAzi9ITzSN9xKMi'  # Ahrefs Turnstile site key (固定)

def get_token(domain):
    r = requests.post('https://api.capsolver.com/createTask', json={
        'clientKey': API_KEY,
        'task': {
            'type': 'AntiTurnstileTaskProxyLess',
            'websiteKey': SITE_KEY,
            'websiteURL': f'https://ahrefs.com/backlink-checker/?input={domain}&mode=subdomains',
        }
    })
    task_id = r.json()['taskId']
    while True:
        time.sleep(2)
        rr = requests.post('https://api.capsolver.com/getTaskResult', json={
            'clientKey': API_KEY, 'taskId': task_id
        }).json()
        if rr.get('status') == 'ready':
            return rr['solution']['token']

def get_signature(token, domain):
    r = requests.post('https://ahrefs.com/v4/stGetFreeBacklinksOverview', json={
        'captcha': token, 'mode': 'subdomains', 'url': domain
    })
    data = r.json()
    return data[1]['signedInput']['signature'], data[1]['signedInput']['input']['validUntil']

def get_top_backlinks(signature, valid_until, domain):
    r = requests.post('https://ahrefs.com/v4/stGetFreeBacklinksList', json={
        'reportType': 'TopBacklinks',
        'signedInput': {
            'signature': signature,
            'input': {'validUntil': valid_until, 'mode': 'subdomains', 'url': f'{domain}/'}
        }
    })
    return r.json()[1]['topBacklinks']['backlinks']

# 21 个 AI Agent 同行（精选）
AI_COMPETITORS = [
    'v0.dev', 'bolt.new', 'cursor.com', 'lovable.dev', 'continue.dev',
    'replit.com', 'claude.ai', 'gemini.google.com', 'perplexity.ai', 'codeium.com',
    'sourcegraph.com', 'tabnine.com', 'jetbrains.com', 'windsurf.com', 'openrouter.ai',
    'anthropic.com', 'openai.com', 'cohere.com', 'mistral.ai', 'huggingface.co',
    'crewai.com',  # 第 21 个
]

db = sqlite3.connect('data/backlinks.db')
db.execute("""CREATE TABLE IF NOT EXISTS ahrefs_api_results (
    id INTEGER PRIMARY KEY,
    competitor TEXT,
    backlink_url TEXT,
    title TEXT,
    UNIQUE(competitor, backlink_url)
)""")

for comp in AI_COMPETITORS:
    print(f"=== {comp} ===")
    try:
        token = get_token(comp)
        sig, valid_until = get_signature(token, comp)
        backlinks = get_top_backlinks(sig, valid_until, comp)
        for bl in backlinks:
            db.execute("INSERT OR IGNORE INTO ahrefs_api_results (competitor, backlink_url, title) VALUES (?,?,?)",
                       (comp, bl.get('urlFrom'), bl.get('title')))
        db.commit()
        print(f"  +{len(backlinks)} backlinks")
    except Exception as e:
        print(f"  FAILED: {e}")
    time.sleep(5)

# 跨竞品聚合（交叉验证法）
top_domains = db.execute("""
    SELECT 
        substr(backlink_url, instr(backlink_url, '://')+3, 
               instr(substr(backlink_url, instr(backlink_url, '://')+3) || '/', '/')-1) as domain,
        COUNT(DISTINCT competitor) as competitor_count
    FROM ahrefs_api_results
    GROUP BY domain
    HAVING competitor_count >= 3
    ORDER BY competitor_count DESC
    LIMIT 100
""").fetchall()

print("\n=== 出现在 >=3 个 AI 同行外链里的域名（高价值候选）===")
for d, c in top_domains:
    print(f"  {c} 个同行 → {d}")
```

**成本**：21 个 competitor × 1 次 CapSolver = $0.025 + Ahrefs API 免费 = **2.5 美分跑完**。

**衍生子玩法**：拿到 Top 100 候选后再做 Serper.dev 验证 traffic（§4.7）→ 双重过滤 → 入 `submissions` 表跑模块 1 流水线。

---

## 5. 模块 3：Yolox 产品被动收割

### 5.1 agents-store Featured Embed（代码改造）

**改造 3 个文件**：

#### 文件 1：新组件

`src/features/agents-store/components/FeaturedBadgeEmbed.tsx`

```tsx
'use client';

interface Props {
  agentId: string;
  agentName: string;
}

export function FeaturedBadgeEmbed({ agentId, agentName }: Props) {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://yolox.ai';
  const embedHtml = `<a href="${baseUrl}/agents-store/${agentId}?ref=featured" target="_blank" rel="noopener">
  <img src="${baseUrl}/api/featured-badge/${agentId}.svg" alt="Featured on Yolox" width="200" height="40" />
</a>`;
  
  const markdownEmbed = `[![Featured on Yolox](${baseUrl}/api/featured-badge/${agentId}.svg)](${baseUrl}/agents-store/${agentId}?ref=featured)`;

  return (
    <details className="mt-6 rounded-lg border border-zinc-200 p-4 dark:border-zinc-700">
      <summary className="cursor-pointer text-sm font-medium">
        Building {agentName}? Embed this Featured badge on your site
      </summary>
      <div className="mt-4 space-y-3">
        <div>
          <div className="text-xs text-zinc-500 mb-1">HTML</div>
          <pre className="overflow-x-auto rounded bg-zinc-100 dark:bg-zinc-800 p-3 text-xs">
            <code>{embedHtml}</code>
          </pre>
          <button 
            className="mt-1 text-xs underline"
            onClick={() => navigator.clipboard.writeText(embedHtml)}
          >Copy HTML</button>
        </div>
        <div>
          <div className="text-xs text-zinc-500 mb-1">Markdown (for README)</div>
          <pre className="overflow-x-auto rounded bg-zinc-100 dark:bg-zinc-800 p-3 text-xs">
            <code>{markdownEmbed}</code>
          </pre>
          <button 
            className="mt-1 text-xs underline"
            onClick={() => navigator.clipboard.writeText(markdownEmbed)}
          >Copy Markdown</button>
        </div>
      </div>
    </details>
  );
}
```

#### 文件 2：动态 SVG badge

`src/app/api/featured-badge/[agentId]/route.ts`

```ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ agentId: string }> }
) {
  const { agentId } = await params;
  // 极简 SVG，可以根据 agent name 动态变长度
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="40" viewBox="0 0 200 40">
    <rect width="200" height="40" rx="6" fill="#000"/>
    <text x="100" y="25" text-anchor="middle" fill="#fff" font-family="Inter,sans-serif" font-size="13" font-weight="600">
      ⭐ Featured on Yolox
    </text>
  </svg>`;
  
  return new NextResponse(svg, {
    headers: {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'public, max-age=86400, immutable',
    },
  });
}
```

#### 文件 3：在 detail 页接入

`src/features/agents-store/components/AgentDetailLayout.tsx` 加：

```tsx
import { FeaturedBadgeEmbed } from './FeaturedBadgeEmbed';

// 在 JSX 底部加
<FeaturedBadgeEmbed agentId={agent.id} agentName={agent.name} />
```

**skills-store / teams-store 复制相同改造**。

#### 邮箱入口（detail 页底部）

```tsx
<section className="mt-12 border-t pt-6">
  <h3 className="text-lg font-medium">Want your AI agent featured here?</h3>
  <p className="mt-2 text-sm text-zinc-600">
    Email us at <a href="mailto:featured@yolox.ai" className="underline">featured@yolox.ai</a> with a link to your agent. 
    We'll review and feature qualifying agents weekly.
  </p>
</section>
```

#### 冷启动 SOP

```python
# scripts/cold-outreach-featured.py
"""主动通知已收录的 agent 作者，告诉他们 Featured badge"""
import sqlite3, requests

# 1. 拉 Yolox 已收录的 agents（从 GitHub manifest）
agents = requests.get('https://api.github.com/repos/Infinite-Flow-Labs/agents/contents/manifest.json').json()
# Decode + 解析...

# 2. 找作者 Twitter/GitHub
# 3. 自动起草 DM 草稿（人工发送）
draft = """
Hey [name],

Saw you built [agent_name]. We've featured it on Yolox 
(https://yolox.ai/agents-store/[agent_id]).

Here's a Featured badge you can embed:
[Featured badge URL]

Free promotion for you — if you embed it, you'll get more eyeballs on your work.
"""
```

### 5.2 GitHub Awesome AI Agents 自建（DR 92 长期资产）

**Repo 名**：`awesome-ai-agents-2026`（你个人账号下，**不是 Yolox org**——显得是 curated 项目）

**README 模板**：

```markdown
# Awesome AI Agents 2026

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of AI agents, agent frameworks, marketplaces, and tools for building intelligent autonomous systems in 2026.

> Maintained by [@yourname](https://github.com/yourname). If helpful, ⭐ star this repo.

## Contents
- [Agent Marketplaces](#agent-marketplaces) ← Yolox 在这里
- [Code Agents](#code-agents)
- [Chat Agents](#chat-agents)
- [Multi-Agent Frameworks](#multi-agent-frameworks)
- [Agent Infrastructure](#agent-infrastructure)
- [Browser Automation](#browser-automation)
- [Research & Papers](#research--papers)

## Agent Marketplaces
- **[Yolox](https://yolox.ai)** — Marketplace for AI agents and skills with built-in team collaboration. Solo founder friendly.
- [Lindy](https://lindy.ai) — Business workflow agents.
- [Relevance AI](https://relevanceai.com) — Multi-agent platform.
- [CrewAI Hub](https://crewai.com) — Agent crew marketplace.

## Code Agents
- [Cursor](https://cursor.com)
- [v0.dev](https://v0.dev)
- [Bolt.new](https://bolt.new)
- [Lovable](https://lovable.dev)
- [Continue.dev](https://continue.dev)
- [Replit Agent](https://replit.com/agent)
- [Windsurf](https://windsurf.com)

（每类列 10-15 个，加 Yolox 自己 1-2 处）

## Contributing
PRs welcome! Send a PR adding your tool with:
- Name, URL, 1-line description
- Category (one of above)

## License
[CC0](LICENSE) — Free to use, copy, modify.
```

**推广脚本**（让 Claude Code 跑）：

```bash
# 1. 提交到主 awesome 收录站
# github.com/sindresorhus/awesome PR
gh repo fork sindresorhus/awesome
# 编辑 readme.md 加你的 awesome-ai-agents-2026 到 "Computer Science" → "Artificial Intelligence" 区
gh pr create --title "Add awesome-ai-agents-2026"

# 2. 提交到 awesomelists.top
curl -X POST 'https://awesomelists.top/submit' -d 'url=https://github.com/yourname/awesome-ai-agents-2026'

# 3. 发 Hacker News
# 4. 发 Reddit r/MachineLearning, r/programming
# 5. 发 X / Twitter / 长推
# 6. 发 dev.to 配套文章
```

**自我扩展**：每周让 Claude Code 跑：

```python
# scripts/awesome-list-update.py
"""每周更新 Awesome AI Agents：从 ProductHunt / HN / Reddit 收集新工具，自动 PR 给自己 repo"""
# 1. 抓 ProductHunt 本周 AI 类
# 2. 抓 HN best of week
# 3. 自动写 PR 加入
```

### 5.3 列表诱饵 Blog + 多平台分发

**3 篇主题**（[长文§6.1]）：

```
Article 1: "20 Best AI Coding Agents in 2026 (Tested for Real)"
  Yolox 位置: 第 1 名 + "Why Yolox stands out" 副标题段
  目标 KW: best ai coding agent 2026

Article 2: "AI Agent Marketplaces: A Complete Comparison"
  Yolox 位置: 在 marketplace 类列第 1
  目标 KW: ai agent marketplace

Article 3: "I Tested 15 AI Agents as a Solo Founder — Here's My Stack"
  Yolox 位置: 在 Stack 配图里
  目标 KW: ai agent for solo founder
```

**多平台分发管线**：

```python
# scripts/blog-distribute.py
"""一篇文章自动分发到 8 个平台 + canonical 回主站"""

ARTICLE_URL = 'https://yolox.ai/blog/20-best-ai-coding-agents-2026'
ARTICLE_MD = open('blog-content/20-best-ai-coding-agents.md').read()

PLATFORMS = [
    ('dev.to', 'https://dev.to/api/articles', 'POST', 'API_KEY_DEV_TO'),
    ('hashnode', 'https://api.hashnode.com', 'GraphQL', 'HASHNODE_TOKEN'),
    ('medium', 'https://api.medium.com/v1/users/.../posts', 'POST', 'MEDIUM_TOKEN'),
    # ...
]

# dev.to 例子
def post_dev_to(title, body_md, canonical_url):
    return requests.post('https://dev.to/api/articles', 
        headers={'api-key': DEV_TO_KEY},
        json={
            'article': {
                'title': title,
                'body_markdown': body_md,
                'published': True,
                'canonical_url': canonical_url,
                'tags': ['ai', 'agents', 'productivity', 'saas'],
            }
        })

# hashnode（GraphQL）
def post_hashnode(title, body_md, canonical_url):
    query = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) { post { url } }
    }
    """
    return requests.post('https://gql.hashnode.com', 
        headers={'Authorization': HASHNODE_TOKEN},
        json={'query': query, 'variables': {'input': {
            'title': title,
            'contentMarkdown': body_md,
            'originalArticleURL': canonical_url,
            'tags': [{'slug': 'ai'}, {'slug': 'agents'}],
        }}})

for name, _, _, _ in PLATFORMS:
    print(f"Posting to {name}...")
    # 调用对应函数
```

---

## 6. 模块 4：候选池持续供给

### 6.1 LXX.ai 数据导入

```python
# scripts/import-lxx-csv.py
import sqlite3, csv

db = sqlite3.connect('data/backlinks.db')
db.execute("""CREATE TABLE IF NOT EXISTS lxx_ai (
    id INTEGER PRIMARY KEY,
    domain TEXT, url TEXT, category TEXT, dr INTEGER, traffic INTEGER,
    submitted TEXT DEFAULT 'no'
)""")

with open('data/lxx_export.csv') as f:
    for row in csv.DictReader(f):
        db.execute("INSERT INTO lxx_ai (domain, url, category, dr, traffic) VALUES (?,?,?,?,?)",
                   (row.get('domain'), row.get('url'), row.get('category'),
                    int(row.get('dr', 0)), int(row.get('traffic', 0))))
db.commit()
```

### 6.2 Ahrefs 未公开 API 自动化

见 §4.8。每月跑一次刷新候选池。

### 6.3 阳光杉木 Serper 批量

见 §4.7。

### 6.4 交叉验证脚本

跑完模块 4 的 3 个数据源后做交叉过滤：

```sql
-- 出现在 >=2 个数据源里的候选 = 高信噪比
SELECT domain, 'gefei_226' as src FROM gefei_226 GROUP BY root_domain
UNION ALL
SELECT domain, 'lxx_ai' FROM lxx_ai
UNION ALL  
SELECT domain, 'ahrefs_api' FROM ahrefs_api_results
UNION ALL
SELECT domain, 'serper' FROM serper_candidates;

-- Top 100 by appearance
SELECT domain, COUNT(DISTINCT src) as src_count, GROUP_CONCAT(src) 
FROM (...above...) 
GROUP BY domain 
HAVING src_count >= 2
ORDER BY src_count DESC LIMIT 100;
```

---

## 7. 流水线接线图

```
┌──────────────────────────────────────────────────────────────┐
│ 周一早晨：一键启动                                              │
└──────────────────┬───────────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────┐
│ python3 scripts/run-batch.py 20     │ ← 取 20 条 pending
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Claude Code reads queue/next.txt    │
│ Uses Backlinks Skill                │
│ Plays Playwright MCP                │
└──────┬──────────────────────────────┘
       │
       ├──→ 每提交一条
       │    ├─ verify-rel.md
       │    ├─ UPDATE gefei_226 SET submitted='yes'
       │    └─ INSERT into submissions
       │
       ▼
┌─────────────────────────────────────┐
│ 周末：跑模块 4 候选池刷新             │
│ ├ ahrefs-best-links.py (5 min)      │
│ ├ serper-nav-reverse.py (30 min)    │
│ └ Cross-validation SQL              │
└──────┬──────────────────────────────┘
       │
       ▼
新候选入 gefei_226 / ahrefs_api_results / serper_candidates → 下周再跑模块 1
```

**每周 cron**（让 Claude Code 帮你写 systemd timer 或 cron）：

```cron
# crontab -e
0 9 * * 1   cd /外链 && python3 scripts/run-batch.py 50    # 周一 9 点跑模块 1 批 50
0 10 * * 6  cd /外链 && python3 scripts/ahrefs-best-links.py # 周六 10 点刷新候选池
0 11 * * 6  cd /外链 && python3 scripts/serper-nav-reverse.py
0 9 * * 0   cd /外链 && python3 scripts/cross-validate.py    # 周日 9 点交叉验证
```

---

## 8. 监控自动化

### 8.1 周报脚本（让 Claude Code 周一跑）

```python
# scripts/weekly-report.py
import sqlite3
from datetime import datetime, timedelta

db = sqlite3.connect('data/backlinks.db')

# 本周新增
week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
weekly = db.execute("""
    SELECT 
        COUNT(*) as total_submitted,
        SUM(CASE WHEN rel_actual='dofollow' THEN 1 ELSE 0 END) as dofollow,
        SUM(CASE WHEN status='live' THEN 1 ELSE 0 END) as live,
        SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) as failed,
        COUNT(DISTINCT platform_domain) as unique_domains
    FROM submissions 
    WHERE submit_time >= ?
""", (week_ago,)).fetchone()

# 平台类型分布
by_type = db.execute("""
    SELECT submit_method, COUNT(*) FROM submissions 
    WHERE submit_time >= ? GROUP BY submit_method
""", (week_ago,)).fetchall()

report = f"""
## Yolox 外链周报 — {datetime.now().strftime('%Y-W%V')}

### 本周战果
- 提交总数: {weekly[0]}
- Dofollow 数: {weekly[1]} ({weekly[1]/max(weekly[0],1)*100:.0f}%)
- 已上线: {weekly[2]}
- 失败: {weekly[3]}
- 独立域名数: {weekly[4]}

### 按提交方式
""" + '\n'.join(f"- {m}: {c}" for m, c in by_type)

print(report)
# 可选：发到 Telegram / Email
```

### 8.2 GSC + Ahrefs 异常告警

```python
# scripts/anomaly-check.py
"""检测外链/流量异常 - 接 GSC API + Ahrefs API"""
# 1. GSC API 拉 Referring Domains 周环比
# 2. 如果单周 +50% 且不是你主动发的 → 告警
# 3. 流量与外链曲线对比 - 负相关 = 攻击信号
```

---

## 9. 防御自动化

### 9.1 自动 Disavow

```python
# scripts/auto-disavow.py
"""扫 spam_blacklist 模式 → 自动生成 disavow.txt"""
import sqlite3, re

db = sqlite3.connect('data/backlinks.db')

# blacklist 模式（已预灌）
patterns = db.execute("SELECT domain_pattern FROM spam_blacklist").fetchall()

# 拉最近 30 天 backlinks（GSC API or Ahrefs API)
recent_backlinks = []  # GSC.links.list() 等

flagged = []
for bl in recent_backlinks:
    for (p,) in patterns:
        if p.startswith('*') and p.endswith('*'):
            if p.strip('*') in bl: flagged.append(bl)
        elif p.startswith('*'):
            if bl.endswith(p.strip('*')): flagged.append(bl)
        elif p.endswith('*'):
            if bl.startswith(p.strip('*')): flagged.append(bl)
        else:
            if p == bl: flagged.append(bl)

# 生成 disavow.txt
with open('data/disavow-pending.txt', 'w') as f:
    f.write(f"# Auto-generated {datetime.now()}\n")
    for d in set(flagged):
        f.write(f"domain:{d}\n")

print(f"Flagged {len(set(flagged))} domains. Review data/disavow-pending.txt")
```

**人工 review 后提交**：[google.com/webmasters/tools/disavow-links-main](https://www.google.com/webmasters/tools/disavow-links-main)

### 9.2 spam_blacklist 预灌

```sql
CREATE TABLE IF NOT EXISTS spam_blacklist (
    id INTEGER PRIMARY KEY,
    domain_pattern TEXT UNIQUE,
    added_date TEXT DEFAULT CURRENT_DATE,
    reason TEXT
);

INSERT OR IGNORE INTO spam_blacklist (domain_pattern, reason) VALUES
('weknow.website', '案例垃圾站 #25'),
('backlink.wiki', '案例垃圾站 #25'),
('zhanhao.online', '案例垃圾站 #25'),
('pranksfl.lol', '案例垃圾站 #25'),
('vickys.design', '案例垃圾站 #25'),
('*.lol', '高风险后缀'),
('*casino*', '关键词模式'),
('*betting*', '关键词模式'),
('*loan*', '关键词模式'),
('*pharmacy*', '关键词模式'),
('*viagra*', '关键词模式'),
('backlink.*', 'backlink 前缀'),
('*-backlinks.*', 'backlinks 后缀');
```

---

## 10. 一图速查：每个模块的预期产出

| 模块 | 输入 | 自动化等级 | 预期外链数 | 时间 |
|---|---|---|---|---|
| 1 — 226 条全跑 | xlsx 226 | 92.9% 全自动 | **150-180 dofollow**（约 70% rel 验证通过） | 5-7 天 |
| 2.1 — WP whois 动态页 | 5-10 个动态页 | 全自动 | **5-10 条子域名 dofollow**（DR 90+） | 1 天 |
| 2.2 — nofollow→Dofollow bypass | 模块 1 中的 159 条 blog_comment | 半自动 | **60-95 条 dofollow 升级**（38-60% 成功率） | 与模块 1 同步 |
| 2.3 — NPM 包 | 1 个官方包 + 5 个微包 | 半自动 | **6 个包 × 4 链 = 24 条 dofollow** | 2 天 |
| 2.4 — WP Plugin | 5 个微插件 | 半自动 | **5 × 3 = 15 条 dofollow**（含 plugin home + author URL） | 1-2 周（审核） |
| 2.5 — TG 频道 | 1 主 + 3 垂类 | 全自动 | **4 条 t.me dofollow + 描述链** | 2 天 |
| 2.6 — Hatena Bookmark | 全 yolox.ai 重要页 | 全自动 | **20-50 条**（看收录率） | 1 天 |
| 2.7 — Serper 导航站逆向 | Top 100 候选 | 全自动 | **30-50 条 dofollow**（高信噪比） | 1 周 |
| 2.8 — Ahrefs 链轮 | 21 个同行 → Top 200 候选 | 全自动 | 衍生供给，融入模块 1 | 持续 |
| 3.1 — Featured Embed | 100 个 agents 收录方 | 半自动 | **30-50 条**（6 个月内被动） | 持续 |
| 3.2 — Awesome List | 1 个 repo | 半自动 | **1 条 GitHub DR 96 + 持续 fork/star 信号** | 持续 |
| 3.3 — 列表诱饵 Blog | 3 篇 + 8 平台分发 | 半自动 | **24 条文章内链 + 持续被动** | 1 周 |

**单月预期总产出**：**300+ 条独立域名 backlinks**，其中 dofollow 占比 50-60%。

---

## 11. 立刻可执行的第一批动作（按"可立刻干"排）

> 不分时间。按"今天能装/能跑/能改"排。

### 🚀 可在 1 小时内启动

- [ ] `pip3 install --user --break-system-packages playwright openpyxl requests` （顺手）
- [ ] `npm install -g @playwright/mcp` + `npx playwright install chromium`
- [ ] 在 `/外链/.claude/skills/backlinks/` 建 4 个 skill md 文件（§3.2 全部内容粘贴）
- [ ] `data/backlinks.db` 加 §2.4 所有表 + 预灌 anchors + pages + blacklist
- [ ] 注册 3 个 Gmail：`yolox.team` / `yolox.outreach` / `yolox.dev`
- [ ] 装 5 个 Chrome 插件（§2.3）

### 🚀 可在 1 天内启动

- [ ] 跑 `scripts/run-batch.py 10` 试跑模块 1 第一批 10 条
- [ ] 验证 rel 检测脚本工作
- [ ] CapSolver 充值 $5 + 拿 API key
- [ ] Serper.dev 注册（免费 2500 queries）

### 🚀 可在 1 周内启动

- [ ] 把模块 1 跑完一遍（226 条 → 全部入 submissions）
- [ ] 模块 2 套 1-2-5 启动（whois 动态页 + nofollow bypass + TG 频道）
- [ ] Yolox 代码改造 §5.1（agents-store Featured Embed）→ PR 等 review
- [ ] GitHub Awesome AI Agents 2026 repo 建好 + 推到 awesome 元站

### 🚀 可在 2-4 周内启动

- [ ] WP Plugin × 5 提交 wordpress.org（等审核 5-30 天）
- [ ] NPM `@yolox/agents-sdk` 发布
- [ ] 模块 4 候选池流水线全跑通
- [ ] 3 篇列表诱饵 Blog 写完 + 8 平台分发

---

## 附录 A：完整数据库 Schema 一览

```sql
-- 已建（§1.1）
gefei_226           -- 226 条原始资源（含字段：submitted, rel_actual, live_url, notes）

-- §2.4 待建
submissions         -- 所有提交记录（跨数据源）
yolox_anchors       -- 16 条预灌锚文本
yolox_pages         -- 5 条预灌目标页

-- §6 候选池表（按需建）
lxx_ai              -- LXX.ai 导出
ahrefs_api_results  -- Ahrefs API 抓取（21 同行 × Top 20）
serper_candidates   -- Serper 导航站逆向
submitatool_dirs    -- oldcai 整理的清单
spam_blacklist      -- 黑名单（§9.2 已预灌）
```

## 附录 B：核心 URL 速查

| 用途 | URL |
|---|---|
| LXX.ai | https://www.lxx.ai/ （兑换码 `GEFEI`） |
| EgoLinks | https://egolinks.online/@backlinks |
| submitatool.com | https://submitatool.com/ |
| Ahrefs free checker | https://ahrefs.com/backlink-checker |
| Google Disavow | https://www.google.com/webmasters/tools/disavow-links-main |
| CapSolver | https://www.capsolver.com/products/cloudflare （折扣码 `brightdata`）|
| Serper.dev | https://serper.dev |
| WP Plugin 提交 | https://wordpress.org/plugins/developers/add/ |
| NPM 注册 | https://www.npmjs.com/signup |
| Hatena 注册 | https://www.hatena.ne.jp/ |
| Hatena API 文档 | https://developer.hatena.ne.jp/ja/documents/bookmark/apis/atom |
| TG BotFather | https://t.me/BotFather |
| Telegraph | https://telegra.ph |
| dev.to API | https://docs.dev.to/api/ |
| Hashnode API | https://gql.hashnode.com |
| Medium API | https://github.com/Medium/medium-api-docs |

## 附录 C：Yolox 提交内容预先准备

`data/yolox-submission-templates.json`：

```json
{
  "name": "Yolox",
  "tagline": "An AI Agents Marketplace for Solo Founders and Teams",
  "short_description": "Yolox is an AI agents marketplace where you can deploy, share, and monetize intelligent agents and skills with built-in team collaboration.",
  "long_description": "Yolox is a marketplace platform for AI agents and skills, designed for solo founders, developers, and small teams. Browse hundreds of pre-built agents, deploy them to your workspace, compose them into custom teams, and ship faster. Built with first-class support for multi-agent collaboration, real-time messaging, and a skills marketplace where developers can monetize their agent components.",
  "categories": ["AI Tools", "Productivity", "Developer Tools", "SaaS", "AI Agents"],
  "pricing_model": "Freemium",
  "website": "https://yolox.ai",
  "tags": ["ai", "agents", "marketplace", "productivity", "agentic-workflow", "ai-skills"],
  "founder_email": "yolox.team@gmail.com",
  "support_email": "support@yolox.ai",
  "logo_512": "/外链/assets/yolox-logo-512.png",
  "logo_256": "/外链/assets/yolox-logo-256.png",
  "screenshots": [
    "/外链/assets/screenshot-landing.png",
    "/外链/assets/screenshot-agents-store.png",
    "/外链/assets/screenshot-client-home.png"
  ]
}
```

## 附录 D：常见反垃圾系统快速识别表

| 系统 | 识别 | 处理 |
|---|---|---|
| Akismet | WP 站，提交后等审核 | ✅ 干净 Gmail + 链接放 author URL |
| Antispam Bee | 德语圈，403 错误 | ✅ pressSequentially 而非 element.value |
| CleanTalk | 403 含 "CleanTalk" 字 | ❌ 跳过 |
| hCaptcha Enterprise | hCaptcha + "enterprise" in script src | ❌ 跳过 |
| Jetpack Highlander | 评论区是 cross-origin iframe | ❌ 跳过 |
| WPantispam Protect | random honeypot textareas | ✅ 留空 honeypot 字段 |

---

## 结语

**这份方案不是阅读材料，是配方表 + 弹药库 + 流水线设计图。**

打开 Claude Code 在 `/外链/` 目录下，照着 §11 一条一条点击启动。

每条都对应：
- ✅ 一个已有的 SQL 表（武器）
- ✅ 一个 Python / Shell 脚本（操作）
- ✅ 一个验证 / rel 检测机制（质量门）
- ✅ 一份回写数据库的事务（资产沉淀）

**3 个月预期**：突破 500-1000 条独立域名 backlinks，50%+ dofollow。

干就完了。
