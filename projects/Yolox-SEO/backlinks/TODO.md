# Yolox 外链建设 TODO

> **当前状态**：环境就位、Skill 就位、数据就位。下一步 D2 手动校准（10 条人工跑）。
>
> **唯一 KPI**：`data/backlinks.db.submissions` 表里 `rel_actual='dofollow'` 的行数每周增长。
>
> **标记说明**：🛠 = 你手动 / 🤖 = Claude Code 自动 / 🌐 = 要外部账号 / ⏱ = 单条预计耗时

依赖链：**A 基础设施 → (B 数据预处理 ∥ C Skill ∥ E 产品改造 ∥ I 监控) → D 跑流水线 → (F 候选池 ∥ G 骚操作 ∥ H 自媒体) → J 稳态**

---

## ⚡ 执行进度（2026-05-23 更新，Session 3 结束）

| 阶段 | 状态 | 备注 |
|---|---|---|
| A1 Playwright MCP | ✅ | @playwright/mcp 0.0.75 + Chromium 149 |
| A2 邮箱 × 2 | ✅ | liuyouxuan570@gmail.com（profile）+ suppscanofficial@gmail.com（评论） |
| A3 Chrome 插件 | ✅ | sitedata + BacklinkHelper |
| A4 CapSolver | ⏳ | 不再必需（MCP 浏览器路径绕过了 Turnstile） |
| A5/A6/A7 | ⏳ | 不阻塞当前阶段 |
| B1 数据库 9 表 | ✅ | `scripts/init_db.py` 幂等 |
| B2 预灌（22/5/13） | ✅ | anchors / pages / spam_blacklist（anchors 改 22 — 删 6 marketplace 加 12 team-platform）|
| B3 24 项目入库 | ✅ | `scripts/import_projects.py` |
| C1 5 Skill 文件 | ✅ | `.claude/skills/backlinks/`，verify-rel.md 已修正 rel="me" |
| C2 MCP 配置 | ✅ | `yolox-web/.mcp.json` |
| D1 run-batch.py | ✅ | 写好；暂不批量跑，先做人工复核 |
| D2 手动校准 | 🔁 复核 | #88 padowan 注册成功但 rel="me"（非 dofollow）。226 不整体废弃，改为只筛可投稿/可提交站点 |
| **F1 ahrefs 反推** | ✅ ⭐ | 19 同行 × 20 = 380 候选入 `ahrefs_api_results`。Skip tabnine/anthropic（免费版返回 0）|
| **F5 Cross-validation** | ✅ | 24 个跨 ≥3 同行的高频站。详见 HANDOFF §17 |
| **O1 GitHub PR** | ⏳ | awesome-vibe-coding [PR #195](https://github.com/filipecalegario/awesome-vibe-coding/pull/195) 已提交，等 merge |
| **下一步** | ⏳ | 可投稿/可提交站点 + 226 池子复核；邮件 outreach 降到最低 |

**Codex 接手第一句建议**：
> 看完 AGENTS.md + HANDOFF.md。当前 KPI=0；awesome-vibe-coding PR #195 已提交等待 merge。准备优先做可投稿/可提交站点和 226 池子复核，邮件 outreach 放最低。

---

## 🎯 当前下一步任务（可提交/投稿优先）

### O1. GitHub Awesome List PR（已提交，等审核）🛠
- [x] Fork `github.com/filipecalegario/awesome-vibe-coding`
- [x] 看现有 entries 格式（v0 / bolt / lovable / windsurf 等已收录）
- [x] 加入 Yolox entry 到 Browser-based Tools
- [x] 提 PR：[`filipecalegario/awesome-vibe-coding#195`](https://github.com/filipecalegario/awesome-vibe-coding/pull/195)
- [ ] PR merged 后验证 live README 链接
- [ ] 更新 `submissions.status='live'` + `rel_actual='dofollow'`
- [ ] **预期产出**：DR 97 dofollow（PR merged 后立刻 live）

### O2. 可投稿/可提交站点（当前主线）🛠
- [ ] 从 F1 24 个跨同行高频站里优先筛：showcase / awesome list / directory submission / profile signup / community listing
- [ ] 每个候选先判断：是否可自助提交、是否需要审核、是否能放 `https://yolox.ai/`、是否能验证 rel
- [ ] 只提交低摩擦、自然资产型站点；单条人工耗时超过 10 分钟就降级
- [ ] 每条提交后写入 `submissions`：`pending/submitted/live/rejected`

### O3. 226 池子复核（不是重跑批量）🛠
- [x] 导出 `gefei_226 WHERE submitted='no' AND type='blog_comment' AND has_url_field='Yes'` → `outreach/226-review-candidates.csv`（155 条，含 `link_strategy='both'`）
- [ ] 抽样 20 条人工打开，判断是否仍可访问、是否可提交、是否明显 nofollow/ugc、是否需要注册/验证码
- [ ] 对可提交项做 1 条 happy path，验证 rel；只有有希望的子类继续扩展
- [ ] Profile 类暂只做小样本复核，不再按旧 audit 结论一刀切
- [ ] 仍然不把 `rel="me"` 算 dofollow

### O4. Tailwind Showcase 申请 🛠
- [ ] `tailwindcss.com/showcase` 申请表单
- [ ] 确认 yolox.ai 是否适合作为 Tailwind 案例
- [ ] 准备截图 + 一句话描述
- [ ] **预期产出**：DR 90 dofollow（如被收录）

### O5. 更多 GitHub Awesome List 🛠
- [ ] 搜 `awesome-ai-agents` / `awesome-ai-tools` / `awesome-llm-apps` / `awesome-vibe-coding`
- [ ] 只挑维护活跃、收录标准匹配、已有同类 agent/app builder 的列表
- [ ] 每个列表单独 PR，单独记录 pending

### O-low. 邮件 outreach（最低优先级）🧊
- [ ] Prismic：`prismic.io/blog/ai-code-generators`
- [ ] n8n：`blog.n8n.io/best-ai-for-coding/`
- [ ] `zapier.com/blog/best-ai-productivity-tools/`
- [ ] 只在可提交站点消化后处理

### O6. 找更多可提交站点 🤖
- [ ] 搜 `awesome-ai-agents` / `awesome-ai-tools` / `awesome-llm-apps` 等 GitHub 列表
- [ ] 每个评估收录标准 + PR Yolox
- [ ] **预期**：再发现 5-10 个候选，每个 DR 80+

---

## 🔁 重新复核的阶段

### D 阶段 — 226 池子流水线（人工复核，不批量硬跑）
**背景**：D2 实战发现 profile 子类 viable 率很低，但 226 池子仍有 155 条 `blog_comment + url_field`，值得重新筛“可投稿/可提交”机会。详见 HANDOFF §16。
- gefei_226 25 dead / 200 no（200 没 audit 但预期 viable 率仍低）
- 1 个 yes（#88 padowan，rel="me" 不算 dofollow）
- **不要按旧 D3 批量跑**；先抽样复核、分类、只做低摩擦可验证站点

---

## A. 环境就位（一次性基础设施，~半天）

### A1. Playwright MCP 装好 🛠
- [ ] `cd /外链 && npm init -y && npm install @playwright/mcp playwright`
- [ ] `npx playwright install chromium`
- [ ] 项目级 `.claude/settings.local.json` 加 mcpServers.playwright 配置
- [ ] **产出**：Claude Code 启动时能看到 playwright MCP 工具

### A2. 邮箱配置 ✅ 已就位
- [x] **`liuyouxuan570@gmail.com`** — profile / SaaS 目录 / GitHub / dev.to / 注册类全部
- [x] **`suppscanofficial@gmail.com`** — WP 评论 / 论坛评论（Akismet 隔离）
- ⚠️ 仅 2 邮箱（非原方案 3 个）—— 一旦某邮箱被某站拉黑，**不要换另一个邮箱重试同一站**，避免双邮箱被关联拉黑

### A3. 装 2 个 Chrome 插件 🛠
- [ ] **sitedata** — 一键看页面外链 + 域名年龄 + 流量，人工 debug 必备
- [ ] **BacklinkHelper** — 复杂站手动兜底 + 看 rel 状态（不开飞书同步，Local-First 模式）

### A4. CapSolver 账号 + API key 🛠🌐
- [ ] 注册 [capsolver.com](https://capsolver.com)
- [ ] 用折扣码 `brightdata` 充值 $5（5% off）
- [ ] 拿 API key 存到 `~/.config/yolox/credentials`（不进 git）
- [ ] **产出**：能解 Cloudflare Turnstile

### A5. Serper.dev 免费账号 🛠🌐
- [ ] 注册 [serper.dev](https://serper.dev)（免费 2500 queries）
- [ ] 拿 API key

### A6. LXX.ai 兑换码 🛠🌐
- [ ] 注册 [lxx.ai](https://www.lxx.ai/)
- [ ] 兑换码 `GEFEI` → 1 年免费
- [ ] 筛选 "AI Tools" + "Startup" 分类 → 导出 CSV → `data/lxx-export.csv`

### A7. JS Bookmarklet 加书签 🛠
- [ ] 把 v3 §2.3 的 javascript 代码加到 Chrome 书签栏，命名 `EXT-LINKS`
- [ ] **产出**：访问竞品页面一键提外链 CSV

---

## B. 数据库扩容 + 原料预处理（与 A 部分并行）

### B1. backlinks.db 加缺失表 🤖
- [ ] 执行 v3 §2.4 所有 `CREATE TABLE` 语句（submissions / yolox_anchors / yolox_pages / lxx_ai / spam_blacklist / serper_candidates / ahrefs_api_results）
- [ ] **产出**：`sqlite3 data/backlinks.db ".tables"` 看到 8 张表

### B2. 预灌固定数据 🤖
- [ ] 灌 16 条 yolox_anchors（品牌词 / LSI / 描述句 / 裸 URL / 中文锚）
- [ ] 灌 5 条 yolox_pages（home / agents / skills / teams / blog）
- [ ] 灌 13 条 spam_blacklist（weknow / backlink.* / *.lol / *casino* 等）

### B3. 处理 yolox-related-projects.xlsx ✅
- [x] 24 条入 SQLite `yolox_related_projects` 表（`scripts/import_projects.py`）
- ⚠️ xlsx 名义 219 行但**实际只有 24 个项目有数据**（其余 195 行空白）—— HANDOFF 之前写错了
- ✅ URL 字段全部已含（HYPERLINK 公式提取），**无需 Serper 补 URL**
- [ ] 9 个项目缺 category，14 个缺 description — 后期 F2 时再补

### B4. LXX.ai 导入 🤖
- [ ] `scripts/import-lxx-csv.py` 写好
- [ ] 跑导入 → `lxx_ai` 表
- [ ] **产出**：3000+ 候选入库

---

## C. Claude Code Skill 知识库就位（与 A/B 并行）

### C1. 4 个 Skill markdown 文件 🤖
- [ ] `.claude/skills/backlinks/SKILL.md` — 入口（v3 §3.2 内容）
- [ ] `.claude/skills/backlinks/comment.md` — WP 评论 SOP
- [ ] `.claude/skills/backlinks/profile.md` — profile 字段 SOP
- [ ] `.claude/skills/backlinks/verify-rel.md` — rel 验证脚本
- [ ] `.claude/skills/backlinks/anti-spam.md` — 6 种反垃圾系统对策（Akismet/Antispam Bee/CleanTalk/hCaptcha/Jetpack/WPantispam）

### C2. MCP 配置 ✅
- [x] **不要**配在 `.claude/settings.local.json`（schema 不接受 `mcpServers`）
- [x] 在 `yolox-web/.mcp.json` 定义 playwright server（指向 `/外链/node_modules/@playwright/mcp/cli.js`）
- [x] 在 `yolox-web/.claude/settings.local.json` 加 `enableAllProjectMcpServers: true`

---

## D. 第一波速产 — 跑通流水线（依赖 A+B+C）⭐⭐ 核心

> ⚠️ **节奏说明（DR 16 新站约束）**：当前 yolox.ai Ahrefs DR=16 / RD=17。**任何"集中爆破"都会被 Google 算法识别为人工操纵**。
>
> | 阶段 | 速度 | 累计上限 |
> |---|---|---|
> | 第 1-2 周 | 手动 5-10 条全人工跑（SOP 校准期） | 累计 ≤ 20 |
> | 第 3-4 周 | 自动化每天 2-3 条 | 累计 ≤ 60 |
> | 第 5-8 周 | 自动化每天 5-8 条 | 累计 ≤ 280 |
> | 第 9 周 + | 评估 GSC + Ahrefs，决定是否提速 | — |
>
> **不要一天跑 50 条然后停一周** — Google 看的是增长曲线自然度，不是日均量。

### D1. 写调度脚本 ✅
- [x] `scripts/run-batch.py` 已写
- [x] 默认 N=3，单日上限硬编码 10，超额自动 cap
- 用法：`/usr/bin/python3 scripts/run-batch.py [N]`

### D2. 手动校准期：头 10 条全人工跑 🛠（第 1 周）
- [ ] 不走 run-batch.py，直接打开 Chrome + sitedata + BacklinkHelper 人工跑
- [ ] 每条记录到 `submissions` 表：哪个字段卡了 / rel 实际是 dofollow/nofollow/ugc/sponsored / 单条耗时 / 验证码遇到没
- [ ] **产出**：SOP 校准数据 → 反哺 C 阶段 Skill 文件
- [ ] **决策点**：dofollow 率 ≥ 30% → 进 D3；< 30% → 回 C 调整 SOP

### D3. 自动化慢喂期 🤖（第 3-4 周）
- [ ] `python3 scripts/run-batch.py 3`（每天 2-3 条）
- [ ] **累计上限**：第 4 周末 submissions 表 ≤ 60 条
- [ ] 每条都看 rel_actual，每周看 GSC Manual Actions
- [ ] **不要一次跑 20 条然后停** — 每天都跑，每天少量

### D4. 提速期 🤖（第 5-8 周）
- [ ] `python3 scripts/run-batch.py 5`（每天 5-8 条）
- [ ] **累计上限**：第 8 周末 submissions 表 ≤ 280 条
- [ ] **预期**：210 条无验证码 + url_field 中，~150-180 条 dofollow
- [ ] **退场信号**：GSC 出现 Manual Action / Ahrefs DR 反降 / 自然流量负相关 → 立刻停 + 走 I5 Disavow

### D5. 5 条带验证码的 → CapSolver 集成 🤖
- [ ] `scripts/solve-turnstile.py` 写好
- [ ] 跑 5 条 has_captcha='Yes' 的

---

## E. 产品层改造（agents-store Featured Embed，与 D 并行）

### E1. 新分支 🛠
- [ ] `git checkout -b feat/agents-featured-badge`

### E2. 写组件代码 🤖
- [ ] `src/features/agents-store/components/FeaturedBadgeEmbed.tsx`（v3 §5.1 文件 1）
- [ ] `src/app/api/featured-badge/[agentId]/route.ts`（v3 §5.1 文件 2）
- [ ] 在 `AgentDetailLayout.tsx` 引用 `<FeaturedBadgeEmbed>`

### E3. skills-store / teams-store 复制改造 🤖
- [ ] `SkillDetailLayout.tsx` 加 embed
- [ ] `TeamDetailLayout.tsx` 加 embed

### E4. detail 页底部加邮箱入口 🤖
- [ ] "Want your AI agent featured here? Email featured@yolox.ai"

### E5. 本地预览 + PR 🛠
- [ ] `npm run dev` 浏览器看效果
- [ ] commit + PR 到 main

### E6. 冷启动 5-10 个 agent 作者 🛠
- [ ] 从 Yolox 已收录 agents 里挑 10 个最活跃的
- [ ] Twitter / GitHub 私信发 Featured badge URL
- [ ] **预期**：80% 会自传播

---

## F. 候选池持续供给（D 跑通后启动）

### F1. Ahrefs 未公开 API — 21 个同行种子 🤖
- [ ] `scripts/ahrefs-best-links.py` 跑（CapSolver $0.025）
- [ ] **产出**：~400 条候选入 `ahrefs_api_results` 表

### F2. 24 个 yolox_related_projects 衍生 🤖（B3 完成后）
- [ ] 同一脚本，输入换成 24 个项目域名
- [ ] **产出**：~4000 条候选（去重后 1500-2000 新平台）⭐
- [ ] 这一步是 v3 之外的扩展，杠杆最大

### F3. Serper.dev 1 万 AI 站点逆向 🤖
- [ ] `scripts/serper-nav-reverse.py` 跑（先用 LXX.ai 拿到的 3000 个 AI 站点）
- [ ] **产出**：~100 个"经过谷歌检验"的导航站

### F4. 多国家扩展 🤖
- [ ] 同脚本 `gl='jp'` `gl='kr'` `gl='de'` 各跑一次
- [ ] **产出**：本地化导航站清单

### F5. 交叉验证 🤖
- [ ] `scripts/cross-validate.py` 写好
- [ ] SQL 找跨数据源 ≥ 2 出现的候选 → 高信噪比清单
- [ ] **产出**：Top 100 黄金候选喂回 D 流水线

---

## G. 哥飞独家骚操作 8 套（按"设置成本"由低到高）

### G1. 套 5：Telegram 频道（最快）🤖
- [ ] @BotFather 注册 `@YoloxAgentsBot` 拿 token
- [ ] 创建频道 `@YoloxAgents`，描述含 `https://yolox.ai`（**后端渲染 dofollow**）
- [ ] `scripts/tg-auto-poster.py` 写好 — 每天抓 HN AI 类 → 发频道
- [ ] crontab 加 `0 9 * * * python3 scripts/tg-auto-poster.py`
- [ ] **衍生**：建 `@YoloxCodeAgents` `@YoloxResearchAgents` 垂类
- [ ] **产出**：4 条 t.me dofollow 描述链 + 每日发帖 mention

### G2. 套 6：Hatena Bookmark 🤖
- [ ] 注册 hatena.ne.jp（Google OAuth）
- [ ] 申请 Hatena Bookmark API OAuth 凭证
- [ ] `scripts/hatena-bulk-bookmark.py` 写好
- [ ] 批量收藏 yolox.ai 所有重要页（agents detail / skills / blog）
- [ ] 在 yolox.ai/about 加 Hatena profile 链接引导 Google 收录
- [ ] **产出**：20-50 条 b.hatena.ne.jp 外链

### G3. 套 1：WP whois 动态页 🤖
- [ ] 在 yolox-web `public/seo-resources/` 部署隐藏页（noindex,follow）
- [ ] 页面里放 5-10 个已知动态页 URL（link.zhihu.com / qiuyumi / nslookup.io / similarweb）
- [ ] Bing Webmaster API 推送（IndexNow）
- [ ] GSC URL Inspection API 推送
- [ ] **产出**：5-10 条子域名 DR 90+ 反向链

### G4. 套 3：NPM 包发布 🤖
- [ ] `packages/yolox-agents-sdk/package.json` 写好（v3 §4.3）
- [ ] `index.js` + `README.md`
- [ ] `npm login` + `npm publish --access public`
- [ ] **再发 5 个微包**：`@yolox/cli` / `@yolox/embed` / `@yolox/types` / `@yolox/utils` / `@yolox/sdk-react`
- [ ] **产出**：6 × 4 = 24 条 npmjs.com DR 92 dofollow

### G5. 套 4：WP Plugin 官方目录 🤖🛠
- [ ] 写第一个插件 `yolox-agents-embed`（PHP，v3 §4.4 骨架）
- [ ] zip 后提交 [wordpress.org/plugins/developers/add](https://wordpress.org/plugins/developers/add)
- [ ] 审核 5-30 天
- [ ] **再做 4 个微插件**：Yolox Agent Sidebar / Skills Embed / Search Widget / Featured Badge
- [ ] **产出**：5 × 3 = 15 条 wordpress.org dofollow

### G6. 套 2：nofollow→Dofollow bypass 🤖
- [ ] `scripts/wp-nofollow-bypass.py` 写好（v3 §4.2 完整代码）
- [ ] 用 gefei_226 里 type='blog_comment' AND link_format='html' 的 159 条做实验
- [ ] **预期**：38-60% 成功率 → 60-95 条原 nofollow 评论升级成 dofollow

### G7. 套 7 + G8. 套 8（已在 F1 + F3）
- [x] 套 7（Serper 导航站逆向）= F3
- [x] 套 8（Ahrefs 链轮挖掘）= F1

---

## H. Yolox 产品自媒体（与 E 并行，长期资产）

### H1. GitHub Awesome AI Agents 2026 🛠🤖
- [ ] 个人账号建 repo `awesome-ai-agents-2026`（**不是 Yolox org**）
- [ ] README 按 v3 §5.2 模板写
- [ ] **收录 50+ AI agent 工具**（数据源：B3 的 24 项目 + B4 的 LXX.ai）
- [ ] Yolox 列在 "AI Agent Team Platforms" 类第 1
- [ ] 加 `awesome.re` badge

### H2. 推广 repo 🛠
- [ ] 提交 `sindresorhus/awesome` PR
- [ ] 发 HN "Show HN: Awesome AI Agents 2026"
- [ ] 发 Reddit r/MachineLearning / r/programming
- [ ] X / Twitter 长推
- [ ] 发 dev.to 配套介绍文章
- [ ] **目标**：100+ stars → 拿到 GitHub DR 92 backlink

### H3. 列表诱饵 Blog 3 篇 🤖
- [ ] 写 "20 Best AI Coding Agents in 2026 (Tested for Real)"
- [ ] 写 "AI Agent Team Platforms: A Complete Comparison"
- [ ] 写 "I Tested 15 AI Agents as a Solo Founder — Here's My Stack"
- [ ] 每篇底部加 `featured@yolox.ai` 邮箱入口
- [ ] 每篇 Yolox 列前 3 + "Why it stands out"

### H4. 多平台分发 🤖
- [ ] `scripts/blog-distribute.py` 写好（dev.to API / Hashnode GraphQL / Medium API）
- [ ] 每篇文章发 8 个平台（5 英文 + 3 中文）
- [ ] 全部 canonical 回 yolox.ai/blog
- [ ] **产出**：3 × 8 = 24 条文章内链 + 持续被动外链入口

---

## I. 监控 + 防御（Day 1 启动，与所有阶段并行）

### I1. GSC 配置 🛠🌐
- [ ] 加 yolox.ai **网址前缀资源**（不是网域资源——后者不支持 Disavow）
- [ ] 链接 GSC API（OAuth）

### I2. spam_blacklist 预灌 🤖
- [ ] 已在 B2 完成

### I3. 周报脚本 🤖
- [ ] `scripts/weekly-report.py` 写好（v3 §8.1 完整骨架）
- [ ] 测试输出到终端
- [ ] 可选：发到 TG `@YoloxAgentsBot` 私聊

### I4. 异常告警 🤖
- [ ] `scripts/anomaly-check.py` 写好
- [ ] 触发条件：周新增 Referring Domains > 50 且非主动发的 / 流量 vs 外链负相关

### I5. Disavow 预案 🤖
- [ ] 创建 `data/disavow-pending.txt` 空文件占位
- [ ] `scripts/auto-disavow.py` 写好（v3 §9.1）

---

## J. 稳态自动化（D + F + G 跑通后启动）

### J1. crontab 配置 🛠
- [ ] `0 9 * * 1 cd /外链 && python3 scripts/run-batch.py 50` — 周一跑批
- [ ] `0 10 * * 6 cd /外链 && python3 scripts/ahrefs-best-links.py` — 周六候选池
- [ ] `0 11 * * 6 cd /外链 && python3 scripts/serper-nav-reverse.py`
- [ ] `0 9 * * 0 cd /外链 && python3 scripts/cross-validate.py` — 周日交叉验证
- [ ] `0 8 * * 1 cd /外链 && python3 scripts/weekly-report.py` — 周一早报

### J2. 进入正循环
- [ ] 每周一看周报 + 决策本周是否加新数据源
- [ ] 每月最后一周做月度复盘（v3 §6.1）
- [ ] 季度看流量曲线判断是否调整策略

---

## 最快启动路径（如果只挑核心做）

**当前最短路径：先让已提交 PR 进入 live，再用可提交站点补第二批 pending**：

| Day | 任务 |
|---|---|
| **Day 1** | 跟踪 awesome-vibe-coding #195；把 PR 写入 submissions pending；筛 226 的 155 条 blog_comment/url_field |
| **Day 2** | 人工打开 20 条 226 样本，标可提交/不可提交/需注册/明显 nofollow |
| **Day 3** | 对 1-3 条可提交站点做 happy path，验证 rel 后决定是否扩大 |

**之后**：D4 跑完 226 + E（产品改造并行）+ F1（候选池扩张）→ 进入循环。

---

## 优先级判断（如果时间紧只挑一个）

| 排名 | 任务 | 理由 |
|---|---|---|
| 🥇 | **已提交 PR 跟踪 + live 验证** | 最接近第一条真 dofollow |
| 🥈 | **可投稿/可提交站点** | 比邮件快，且审核路径更明确 |
| 🥉 | **226 池子复核** | 还有 155 条 blog_comment/url_field，值得重新筛 |
| 4 | 更多 GitHub Awesome List | 可复制 #195 路径 |
| 5 | Tailwind Showcase | 表单提交，质量高但审核不可控 |
| 6 | 邮件 outreach | 周期长、成功率低，放最低 |

---

## 已完成的（不用再做）

- ✅ 35 篇社群学习材料综合（`refs/深度长文.md`）
- ✅ v3 执行方案（`Yolox外链执行方案.md`）
- ✅ 226 条 xlsx 入 SQLite（`data/backlinks.db.gefei_226`）
- ✅ 24 条竞品入文件（`data/yolox-related-projects.xlsx`）
- ✅ 目录结构整理
- ✅ docx→md 转换脚本（`scripts/docx2md.py`）

---

**下一步动作**：跟踪 #195 + 建立 226 复核清单，不再按旧 D3 批量跑。
