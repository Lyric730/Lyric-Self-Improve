# Yolox 外链建设 — 会话交接文档

> 给下一会话 Claude / 任何接手者：读完这个就能继续干，不用回看历史对话。

---

## 1. 一句话项目状态

**F1 ahrefs 反推完成（380 候选 + 24 个跨 ≥3 同行高频站）。GitHub Awesome List PR #195 已提交，下一步转向可投稿/可提交站点 + 226 池子复核；邮件 outreach 降到最低优先级。**

```
[阶段] 方案+学习 → 环境就位 → 226 初筛（失败但保留复核）→ F1 反推（done）→ PR #195 submitted ← 你在这里
                                                          ↓
                                                    可投稿/可提交站点 + 226 复核
                                                          ↓
                                                    ⭐ 拿到第 1 条真 dofollow
```

**当前 KPI**：`submissions WHERE rel_actual='dofollow' AND status='live' = 0`（226 池子 #88 padowan 跑出 rel="me"，不算 dofollow；awesome-vibe-coding #195 处于 pending）

**⚠️ Ahrefs 数据警示**：yolox.ai 当前 DR=16 / RD=17（截图 2026-05-22）。是个**纯新站**，外链速度必须慢喂。详见 §14。

**接手者注意**：若你是 **Codex**（OpenAI），读完本文件 → `TODO.md` → `AGENTS.md` 即可直接干活。若是 **Claude Code**，额外读 `.claude/skills/backlinks/SKILL.md`。

---

## 2. 这个项目在干嘛（30 秒理解）

Yolox = **AI agent team platform**（为 indie hackers / creators / 小生意主搭建自己的领域专家 AI 团队，不是 marketplace）。这次任务是**为 yolox.ai 建一条自动化外链生产线**——让 Claude Code + Playwright MCP 替小刀老师全自动跑外链提交。

**唯一 KPI**：`data/backlinks.db.submissions` 表里 `rel_actual='dofollow'` 行数每周增长。

**原料**：35 篇社群学习材料里挖出的 8 套独家骚操作 + 哥飞 226 条免登录资源 xlsx + 24 个 Yolox 相关项目 + Ahrefs API/Serper 持续供给候选池。

---

## 3. 已完成的工作（不要重做）

### Session 1（2026-05-21）— 方案 + 学习
| 产出 | 路径 |
|---|---|
| 综合 35 篇社群材料 → 深度长文（1149 行） | `refs/深度长文.md` |
| 执行方案 v3（1969 行，4 模块 + 8 套骚操作） | `Yolox外链执行方案.md` |
| 226 条入 SQLite | `data/backlinks.db.gefei_226` |
| xlsx → CSV 双备份 | `data/gefei-226-resources.csv` |
| docx → md 转换器 | `scripts/docx2md.py` + `batch_convert.sh` |
| 版本控制 | 推 feat/backlink-workflow，PR #24 OPEN |

### Session 2（2026-05-23）— 环境就位 + 风险评估
| 产出 | 路径 / 备注 |
|---|---|
| 全局 yolox.com → yolox.ai（71 处） | 4 个 md 全替换 |
| Ahrefs 状态确认 | DR=16 / RD=17 — 纯新站，修订 D 节奏 |
| A1 Playwright MCP | `@playwright/mcp` 0.0.75 + Chromium 149.0 (114MB) |
| A2 邮箱 | `liuyouxuan570@gmail.com`（profile/SaaS）+ `suppscanofficial@gmail.com`（评论） |
| A3 Chrome 插件 | sitedata + BacklinkHelper（小刀老师装好） |
| B1 数据库 8 表 | `scripts/init_db.py` 幂等 |
| B2 预灌（16/5/13） | anchors / pages / spam_blacklist |
| B3 24 项目入库 | `scripts/import_projects.py` — xlsx 实际只有 24 个项目（非 219）且 URL 全已含 |
| C1 5 个 Skill | `.claude/skills/backlinks/{SKILL,comment,profile,verify-rel,anti-spam}.md` |
| C2 MCP 配置 | `yolox-web/.mcp.json` + `yolox-web/.claude/settings.local.json`（`enableAllProjectMcpServers: true`）— `settings.local.json` 的 schema **不接受 `mcpServers` 字段**，必须用 `.mcp.json` |
| D1 调度脚本 | `scripts/run-batch.py` — 单日上限 10 硬编码 |
| D 节奏调整 | TODO §D 改成"第 1-2 周手动 / 3-4 周日 2-3 / 5-8 周日 5-8" |

### Session 3（2026-05-23 下午）— 226 失败 + F1 反推完成

| 产出 | 路径 / 备注 |
|---|---|
| D2 手动校准 #88 padowan 注册成功 | rel="me" — **Google 不当 SEO 信号**（John Mueller 公开声明），实际 0 dofollow |
| 发现 PunBB 表单坑 | PHP 8 Deprecated warning 串入空 input value → POST 验证 silent reject。修复：清空 `value.includes('Deprecated:')` 字段 |
| Profile 池子 audit v1 + v2 | 67 条 profile → 1.5% 实际 viable（25 dead / 1 live but rel=me / 35 灰色 / 6 重分类成 blog_comment） |
| 226 池子初筛失败 | profile 子类 viable 率太低 + 多数 rel=nofollow / 注册关闭；但 155 条 blog_comment/url_field 需要重新复核 |
| F1 ahrefs 反推 — 19 同行 × 20 backlinks | `ahrefs_api_results` 表：380 条（skip tabnine / anthropic，免费版返回 0）|
| Cross-validation 出 24 个跨 ≥3 同行 | TOP：github.com (12×, DR97) / zapier.com (11×, DR91) / wikipedia (8×, DR97) — 详见 §17 |
| Audit 脚本 V1/V2 | `scripts/audit_profiles*.py` |
| Ahrefs scraper | `scripts/scrape_ahrefs.py`（headless 被 Cloudflare 拦——MCP 浏览器路径 OK） |
| Insert helper | `scripts/insert_ahrefs_json.py` 把 ahrefs JSON 入库 |
| SOP 修正 | `verify-rel.md` 加 rel="me" → me_no_pagerank（不算 dofollow）|
| 文档同步 | 创建 `AGENTS.md`（Codex 接手主入口）|
| 临时文件归档 | 21 个 `data/ahrefs-*.json` → `data/archive/ahrefs-raw/` |

**v1 / v2 执行方案已废删——不要从 git 历史里复活**。

---

## 4. 关键决策档案（小刀老师明确选过的）

| # | 决策 | 不要违反 |
|---|---|---|
| 1 | **不分黑白灰，所有解法都做** | 不要把 nofollow bypass / 过期域名 301 / Ahrefs API 这些标 "灰帽不做" |
| 2 | **不要立"铁律"** | 不要写 "5 条铁律 / 单日 ≤ 5 条" 这种规矩条款 |
| 3 | **不分时间，按任务/依赖组织** | 不要 "第 1 周做 X / 第 2 周做 Y" |
| 4 | **批量自助 > 半自动 > 邮件** | SaaS Testimonial / Best X List 等邮件类只能 P2，不能上 P0 |
| 5 | **小众 + 自动化 + 资源堆叠** | 不要列 "30 个 SaaS 目录"这种大众清单——失败过，被砍 |
| 6 | **飞书 Base 暂搁** | API 月配额已撞（lark-cli 99991403）。用本地 CSV + SQLite |
| 7 | **数据库本地** | `data/backlinks.db`（SQLite）+ CSV 双备份 |
| 8 | **Chrome 插件砍到 2 个** | 只装 sitedata + BacklinkHelper。其他（AutoCommentAI / External Link Extractor / AIPex 等）不要 |
| 9 | **废弃版本直接删** | 不归档 `.v1-已废.md`、不在文档里留"废案"段落 |
| 10 | **"模块"代替"战场"** | 22 处替换完毕，不要写回去 |
| 11 | **重要命令前置说明** | CLAUDE.md 全局规则；改 DB / push / 删文件前必须说明 |
| 12 | **直白不绕弯，密度优先** | 表格 / 列表 / 代码块 > 散文；emoji 仅作结构标识 |

---

## 5. 关键约束（踩过的坑）

| 约束 | 详情 |
|---|---|
| 🔑 **飞书 API 月配额已撞** | lark-cli `99991403` 错误，等月初（约 6 月初）重置。本会话最后状态：可读个别文档但批量调用挂掉 |
| 🔑 **公开仓库代码污染风险** | `Infinite-Flow-Labs/yolox-web` 是组织级代码仓。**只推 dev 产出**（深度长文 / 执行方案 / 脚本 / 数据库），原始 docx / 27MB 图片 / 中间产物全部 gitignore |
| 🔑 **版权风险** | `refs/学习文章/` 是哥飞社群的原创 docx，**绝对不要 commit / push** — .gitignore 已排除 |
| ⚙️ | 当前 shell 默认 Python 在 `hermes-agent` venv 里——`openpyxl` 装在系统 Python。用 `/usr/bin/python3` 跑 xlsx 解析 |
| ⚙️ | sudo 在 Claude Code shell 里要密码——`apt install` 类命令让用户用 `! ` 自己跑 |

---

## 6. 文件结构（必须知道的）

```
/外链/
├── README.md                          ← 目录索引（永远先看这个）
├── TODO.md                            ← 当前待办清单（A-J 十阶段）
├── HANDOFF.md                         ← 你正在看的这个
├── Yolox外链执行方案.md                ← 主行动手册 v3（1969 行）
├── .gitignore
│
├── data/
│   ├── backlinks.db                   ← SQLite（当前只有 gefei_226 表，226 行）
│   ├── gefei-226-resources.csv        
│   └── yolox-related-projects.xlsx    ← 24 行，绝大多数 链接+类别 待补
│
├── scripts/
│   ├── docx2md.py                     ← python-docx 实现的 docx → md
│   └── batch_convert.sh               ← 批量壳
│
└── refs/                              ← 学习参考（不参与执行）
    ├── 深度长文.md                     ← 跨 35 篇综合 1149 行
    ├── _md/                           ← 35 篇转换后 markdown（gitignore）
    ├── _assets/                       ← 27MB 学习图片（gitignore）
    └── 学习文章/                       ← 35 个原始 docx（gitignore）
```

---

## 7. 数据库当前状态

9 张表全部就位：

```
gefei_226                  226 rows    25 dead / 1 yes (rel=me 不算) / 200 no — profile 初筛失败，blog_comment/url_field 子集复核中
ahrefs_api_results         380 rows    ⭐ Session 3 F1 反推 — 当前主候选池
yolox_anchors               22 rows    ✅ 预灌（Session 3 删 6 marketplace + 加 12 新）
spam_blacklist              13 rows    ✅ 预灌
yolox_pages                  5 rows    ✅ 预灌
yolox_related_projects      24 rows    24 条同行项目（F2 备用）
submissions                  1 row     status='live_no_seo_value' rel=me — KPI 实际 0
serper_candidates            0 rows    等 Serper API
lxx_ai                       0 rows    等 LXX.ai 账号
```

**重新初始化**：`/usr/bin/python3 scripts/init_db.py`（幂等，可重跑）
**导入 24 项目**：`/usr/bin/python3 scripts/import_projects.py`（OR IGNORE 防重）

字段结构 / 预灌内容详见 `Yolox外链执行方案.md` §2.4 + `scripts/init_db.py`。

---

## 8. git / PR 状态

| 项 | 值 |
|---|---|
| 当前分支 | `feat/backlink-workflow` |
| Upstream | `origin/feat/backlink-workflow`（已 tracking）|
| 最新 commit | `6b9771d`（Chrome 插件砍到 2 个） |
| 本分支 commits | 3 个：`cead5b6` 初始 → `3cba18c` 整理 → `6b9771d` 砍插件 |
| PR | **#24 OPEN**：feat/backlink-workflow → main，author Lyric730 |
| PR URL | https://github.com/Infinite-Flow-Labs/yolox-web/pull/24 |

**不要 merge PR 到 main**（小刀老师之前确认：方案还在执行验证中，4-6 周后有结果再决定）。

---

## 9. 下一步行动

**当前主线：先等 GitHub PR merge，再优先做可投稿/可提交站点；邮件 outreach 放最低。目标拿第 1 条真 dofollow**（详细清单见 §17）：

| 优先 | 目标 | DR | 路径 | 工作量 |
|---|---|---|---|---|
| 🥇 | `github.com/filipecalegario/awesome-vibe-coding#195` | 97 | PR 已提交，等 merge | 跟踪 |
| 🥈 | 226 池子 `blog_comment + url_field` 子集 | 混合 | 抽样复核、只做可提交/可验证站点 | 先 20 条 |
| 🥉 | 更多 GitHub awesome list | 80+ | PR 加 Yolox | 单个 15-30 min |
| 4 | `tailwindcss.com/showcase` | 90 | 表单申请 | 20 min |
| 5 | `prismic.io` / `n8n.io` / `zapier.com` | 88-91 | 邮件作者 | 最低优先级 |

**🥇 GitHub Awesome List PR 当前状态**：

```bash
# PR: https://github.com/filipecalegario/awesome-vibe-coding/pull/195
# Title: Add Yolox
# Status: open / waiting for maintainer review
# Merge 后：验证 README live link → submissions.status='live' rel_actual='dofollow'
```

**等结果同时可并行做的**：
- 🥈 复核 226 池子中 `blog_comment + url_field` 子集，先跑 20 条人工样本
- 🥉 找更多 GitHub awesome list / showcase / directory submission
- 🧊 邮件稿保留，但 prismic / n8n / zapier 放最低优先级

**不要做的**：
- ❌ 按旧 D3 批量跑 226
- ❌ 把 rel="me" 算 dofollow
- ❌ 在明显 nofollow/ugc 或注册关闭站点上花长时间

---

## 10. 用户偏好补充（本会话学到的，CLAUDE.md 之外）

| 偏好 | 行动指引 |
|---|---|
| 小刀老师是 solo-op 全栈，主力工具 Claude Code | 所有方案不依赖团队协作 / 不用"找工程师" |
| 飞书 wiki 是他的学习材料归档地，但 API 配额紧 | 不要让他每次跑 lark-cli；要用先确认配额 |
| 倾向"看见结果再决策"——4-6 周才合 PR | 不要催 merge / 不要催 review |
| 偏好密集表格 / 不要散文 / emoji 仅作结构 | 写文档严格遵守 |
| 中文沟通 + 英文术语 | 保留这种混合风格 |

---

## 11. 我（上个 Claude）做了哪些"判断"，你可以推翻

| 判断 | 来源 | 可不可以改 |
|---|---|---|
| 把 35 篇分 Tier 0-7 学习路径 | 我设计的，小刀老师认可"OK 按这个走" | 可改但要先跟用户确认 |
| 数据库 schema（10 张表） | 我设计的，未跟用户逐字确认 | 可改 — 字段不够时直接 ALTER |
| TODO 阶段 A-J 分类 | 我设计的，按依赖链 | 可改但要保持"按任务/依赖，不分时间" |
| Chrome 插件砍到 2 个 | 用户拍板了 | 不要再加 |
| 不用飞书 Base | 用户拍板（API 限额）| 月初配额重置后可重启讨论 |

---

## 12. 如果用户问"上次做到哪了"

**标准回答**：

> 3 个 Session 进展：
> - **Session 1**：方案 v3 + 226 池子入库 + 24 同行项目入库
> - **Session 2**：环境就位（Playwright MCP / 2 Gmail / 数据库 9 表 / 5 Skill 文件 / MCP 配置 / run-batch 脚本）
> - **Session 3**（最新）：D2 试跑 226 池子失败（rel="me" 不算 dofollow + audit 80% dead）→ 转向 F1 ahrefs 反推 → 19 同行 380 条 backlinks 入库 → cross-validation 出 24 个跨同行高频站
>
> 当前阶段：**F1 反推完成，0 真 dofollow，下一步 outreach（GitHub PR 起手）**
> 完整状态见 `HANDOFF.md`，下一步详情 §9 + §17。

---

## 13. 上下文清完后的第一句对话建议

**Codex 接手**建议说：

> 看完 AGENTS.md + HANDOFF.md。当前 KPI=0；awesome-vibe-coding PR #195 已提交等待 merge。下一步优先做可投稿/可提交站点和 226 池子复核，邮件 outreach 放最低。

**Claude Code 接手**建议说：

> 看完 HANDOFF / TODO / .claude/skills/backlinks/SKILL.md。MCP 已加载。准备从 awesome-vibe-coding GitHub PR 起手。

---

## 14. Ahrefs 数据 + 风险评估（Session 2 关键决策）

截图于 2026-05-22 拿到的 yolox.ai 实际数据：

| 指标 | 当前 | 含义 |
|---|---|---|
| Domain Rating | **16** (+13) | 纯新站特征 |
| Referring Domains | **17** (+15) | 历史基线只有 2 个 RD |
| Health Score | 41 (+22) | 不健康（但用户明确说不归我管） |
| Broken | 25 (+23) | 同上不归我管 |
| Blocked | 4.5K (+3.1K) | 同上不归我管 |

**风险判断**：

| 策略 | 风险等级 | 原因 |
|---|---|---|
| 226 免登录目录批量 | 🔴 高 | RD 基线 17，加 226 条占比 13× 跳跃 |
| WP 评论 bypass（G6） | ☠️ 自杀级 | DR 16 站玩 bypass = 主动撞算法。**推迟到 DR 30+ 再做** |
| NPM / WP Plugin / GitHub Awesome | 🟢 极低 | 自然资产型，新站急需 |
| Telegram / Hatena | 🟢 低 | Google 当社交信号 |

**Google 当前机制**（2022 SpamBrain 之后）：
- 发现垃圾链 → 优先 **nullify**（贬值），而非惩罚目标站
- 仅在"极端明显的所有者操纵"时升级到手动 action
- 所以大部分风险是"做了等于白做"，不是"做了等于被罚"
- 但 DR 16 新站基线低，外链曲线异常更容易触发审查

**D 节奏调整结果**（已写入 TODO §D）：

| 阶段 | 速度 |
|---|---|
| 第 1-2 周 | 手动 5-10 条全人工跑 |
| 第 3-4 周 | 自动每天 2-3 条（累计 ≤ 60） |
| 第 5-8 周 | 自动每天 5-8 条（累计 ≤ 280） |
| 第 9 周 + | 评估 GSC + Ahrefs |

**社群"其他人没事"不是有效 anchor**：算法滞后 3-6 月 / 失败案例不公开 / 老站基础不同。

---

## 15. Session 2 + 3 学到的用户偏好

| 偏好 | 行动指引 |
|---|---|
| 用现有 2 个 Gmail（不愿额外注册） | 不要再建议注册新 Gmail；接受隔离不全的代价 |
| 邮箱单点风险用户接受 | 但 SOP 里要写"不要换邮箱重试同一站" |
| Health/Broken/Blocked 不归 Claude 管 | 站点工程问题用户自己处理；Claude 只负责外链 |
| 直接拍板，不喜欢被反复 confirm | 给计划 + 立刻动手，少问"要继续吗" |
| 看到失败直说"什么失败了？" | 不要快速下结论"是 X 问题"——先 debug 验证再说 |
| Pair 模式：你做一遍 / 我做一遍 | 关键流程上小刀老师会自己验，发现 Claude audit 误杀就提出来 |
| 「先一个一个来」 | 拿 0→1 比批量 audit 优先；先把一条 happy path 跑通 |

---

## 16. Session 3 D2 校准失败根因（不要再重做）

**226 池子复核原则**：

| 信号 | 数据 | 含义 |
|---|---|---|
| Profile 类 audit | 67 条 → 25 dead / 6 重分类 / 1 唯一注册成功 | viable 率 < 2% |
| 唯一注册成功（#88 padowan） | rel="me" | 不算 dofollow（John Mueller 公开声明） |
| Audit V2 加深检查（rel + register） | 18 个 has_website_field → 1 个 viable | 真"有效 profile"率 1.5% |
| Profile 多数挂点 | 注册关闭 / rel=nofollow / 不可访问 / URL 类型错误 | 哥飞 226 数据质量低，type 字段也有误判 |

**新的执行判断**：
- 不再把 226 整体废弃；先从 155 条 `blog_comment + has_url_field='Yes'`（含 `link_strategy='both'`）抽样 20 条复核。
- 复核目标不是“证明 226 有用”，而是找出其中仍可投稿/可提交、可验证 rel、低摩擦的站点。
- Profile 类不批量跑，只抽样看是否之前 audit 误杀。
- 任何 `rel="me"` 仍标 `me_no_pagerank`，不计入 KPI。

**PunBB 表单填写隐藏坑**（已修复，但 Codex 要注意）：
- PHP 8.x Deprecated warning 渲染到空 `<input value="...">` 里
- `fill_form` 只填指定字段 → 其他字段保留 warning string
- POST 时 `form[jabber]` type=email 验证 "Deprecated:..." 失败 → silent reject 整个 update
- **修复**：提交前 `evaluate` 清空所有 `value.includes('Deprecated:')` 的字段

**rel="me" 不算 dofollow**：
- Google 文档只列 `nofollow/sponsored/ugc` 三个 hint
- 但 rel="me" 是 XFN 身份验证标准（Mastodon/IndieAuth 用），John Mueller 公开说 "not helpful to Google's algorithms"
- **`verify-rel.md` 已修正**：rel="me" 单独标 `me_no_pagerank`，不算 dofollow

---

## 17. F1 ahrefs 反推完整候选清单（24 个跨 ≥3 同行高频站）

`ahrefs_api_results` 表 380 条 → 跨同行去重 → 24 个出现在 ≥3 同行外链里的高价值站：

| 跨同行数 | DR | Domain | Yolox outreach 路径 |
|---|---|---|---|
| **12** | 97 | **github.com** | 找合适 Awesome List（vibe-coding / ai-agents 等）PR 加 Yolox ⭐⭐ |
| **11** | 91 | **zapier.com** | "Best AI Productivity Tools" 邮件作者请求加 Yolox |
| 8 | 97 | en.wikipedia.org | 需要 notability，新站不合格 |
| 7 | 92 | ibm.com | 大企业 blog 不接 outreach |
| 6 | 97 | apps.apple.com | App Store 评论，不直接 |
| 6 | 94 | medium.com | Yolox 自己写文章 + 多次引用 |
| 6 | 84 | datacamp.com | 教程站，找作者 outreach |
| **6** | 54 | **justdeleteme.xyz** | "删账号流程"站，6 同行收录，Yolox 提交流程 ⭐ |
| 5 | 99 | play.google.com | Google Play 评论，不直接 |
| 5 | 84 | codimd.apps.education.fr | 教育平台 markdown 笔记 — 可写笔记引用 |
| 5 | 41 | aubergine.co | "Top AI Coding Tools 2026" 评测，邮件作者 |
| **4** | 90 | **tailwindcss.com showcase** | 申请上 Tailwind Showcase（用 Tailwind 建的 yolox.ai）⭐ |
| 4 | 72 | gumloop.com | competitor blog（跳过） |
| 4 | 71 | voicemod.net | 语音工具，不对口 |
| **3** | 89 | **blog.n8n.io/best-ai-for-coding** | 评测文邮件 outreach ⭐ |
| **3** | 88 | **prismic.io/blog/ai-code-generators** | "12 AI Code Generators Tested"，邮件 ⭐⭐ |
| 3 | 76 | lindy.ai | competitor blog（跳过） |
| 3 | 74 | augmentcode.com | competitor blog（跳过） |
| 3 | 71 | bdor.fr | 法语站，需法语内容 |
| 3 | 64 | uibakery.io | competitor（跳过） |
| 3 | 57 | callbell.eu | WhatsApp 工具，不对口 |
| 3 | 56 | igmguru.com | 培训站 |
| 3 | 54 | axify.io | 工具站 |
| 3 | 11 | chatgptgratuit.app | 低 DR，可 skip |

**实际可投目标（按 ROI）**：

| ROI 评级 | 站 | 为啥 |
|---|---|---|
| 🥇 高 | github.com（找 Awesome list）| #195 已提交；可复制路径到更多列表 |
| 🥇 高 | 可投稿/可提交站点 | 比邮件链路更短，可直接进入 pending |
| 🥈 中 | tailwindcss showcase | 表单提交，等审批 |
| 🥈 中 | 226 池子可提交子集 | 需重新筛，先小样本 |
| 🧊 低 | prismic / n8n / zapier 邮件 | 周期长、不可控，放最低 |
| 🥉 低 | justdeleteme.xyz / codimd | DR 中等但路径不直接 |
| ❌ skip | wikipedia / ibm / apple / play | 大企业 / 严标准 |
| ❌ skip | gumloop / lindy / augmentcode / uibakery | competitor |

**SQL 查询任意候选详情**：

```sql
SELECT competitor, backlink_url, dr, title
FROM ahrefs_api_results
WHERE backlink_url LIKE '%github.com%'
ORDER BY CAST(dr AS INTEGER) DESC;
```
