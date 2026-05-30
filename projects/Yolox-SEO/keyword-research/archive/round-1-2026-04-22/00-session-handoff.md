# Agent B · Session Handoff（本周中途 context 切换用）

**创建**：2026-04-23（Day 3 结束）
**用途**：Agent B session context 即将满，**下一个 session 用本文档作为 cold-start entry point** 继续 Day 4–7
**不要误用**：这 ≠ playbook Day 7 的"下周 handoff"（那是 `2.3-handoff.md`，本周任务全部做完后写给下周）。本文档是 session 切换用。

---

## 0 · 快速热身 checklist（新 session 启动第一件事）

1. Read 本文档全文
2. Read `docs/seo/keyword-research/04-keyword-map-v1.md` 的 **§Cluster 粗标汇总** + **Tier 1 表格**（只读这两部分足够做 Day 4–5）
3. Read `docs/seo/keyword-research/03-reddit-quora-questions.md` 末尾的 **30 个零量词预选表**（Day 4 原料）
4. 环境自检：`source ~/.nvm/nvm.sh && nvm use 22 && opencli doctor`（应显示全 OK）
5. Glob 看 `~/tools/opencli-raw/day*.json` 确认 15 份 Reddit/X 原始数据在
6. 向小刀老师汇报："Agent B cold-started，读完 handoff，准备开 Day X，按 Y 方式执行，确认？"

---

## 1 · 30 秒项目上下文

- **项目**：yolox-web（Next.js 16，AI agent 平台，零流量新站）
- **角色**：Agent B = §2.3 关键词研究
- **用户**：小刀老师（solo-op 全栈，沟通中文，CLAUDE.md 里"新手但决策力强"；见 `~/.claude/CLAUDE.md`）
- **本周周期**：2026-04-22（Day 1）→ 2026-04-28（Day 7）
- **本周目标**：从零建 200 词 Keyword Map（KD<10 + 零量词）+ 3 Pillar × 12-15 Cluster + 下周 6 篇博客选题

---

## 2 · 本周进度（截至 Day 3 结束）

| Day | 日期 | 产出 | 状态 |
|---|---|---|---|
| 1 | 04-22 周三 | `01-seed-keywords.md`（70 种子，4 源）| ✅ 🟢 merged in PR #8 |
| 2 | 04-23 周四上 | `02-expanded-keywords.md`（325 候选）+ `03-reddit-quora-questions.md`（74 问句）| ✅ 🟢 merged in PR #8 |
| 3 | 04-23 周四下 | `04-keyword-map-v1.md`（200 词主库）+ `07-negative-keywords.md`（117 负向）| ✅ 🟡 **未 commit**（Day 3 的产出不在 PR #8 里）|
| **4** | **04-25 周六** | **`05-zero-volume-strategy.md`（30 零量词策略）**| ⏳ **下一步** |
| 5 | 04-26 周日 | `06-pillar-cluster-map.md`（3 Pillar × 4-5 Cluster）| ⏳ |
| 6 | 04-27 周一 | `08-week2-blog-outlines.md`（下周 6 篇博客大纲）| ⏳ |
| 7 | 04-28 周二 | `keyword-map-v1.csv` + `09-feishu-import.md` + `2.3-handoff.md`（下周 handoff）| ⏳ |

**已创建的 PR**：#8（https://github.com/Infinite-Flow-Labs/yolox-web/pull/8）—— 包含 Day 1+2 产出 + 2.3 任务文档的 Day 1/2 进度。**Day 3 的 04 + 07 文档还未 commit**，下次 session 可以打包 commit（追加到现有 PR #8 或单独新 commit）。

---

## 3 · 已产出 5 个文档清单（按阅读优先级）

| # | 路径 | 一句话摘要 | 何时需读 |
|---|---|---|---|
| 1 | `docs/seo/keyword-research/04-keyword-map-v1.md` | **200 词主库**（Tier 1 × 40 + Tier 2 × 95 + Tier 3 × 65），按 12 个 Cluster 粗标 | Day 4/5/6 都要 |
| 2 | `docs/seo/keyword-research/03-reddit-quora-questions.md` | **74 真实问句**（15 OpenCLI + 25 Quora + Day 1 的 15），每条带 URL | Day 4（30 零量词清单在末尾）+ Day 6（博客证据）|
| 3 | `docs/seo/keyword-research/07-negative-keywords.md` | **117 负向词**（5 类）+ 给 Agent C/D 使用提醒 | Day 6 避坑 |
| 4 | `docs/seo/keyword-research/02-expanded-keywords.md` | 325 候选词（源头，已被 04 吸收）| **一般不用读**，除非 04 缺信息 |
| 5 | `docs/seo/keyword-research/01-seed-keywords.md` | 70 种子词（起点，已被 02/04 吸收）| **一般不用读** |

**阅读预算**：每次 session 读 1 + 2 = 约 900 行，够用。3 按需看。

---

## 4 · 核心策略决策（已定，下次 session 不要重新质疑）

### 4.1 YOLOX 定位（数据反复印证）

**"AI marketing team for solopreneurs"**。这是 Lindy（个人助理）/ Relevance AI（Sales）/ Zapier AI（orchestration）/ n8n（dev 工具）4 个竞品都**没直接打**的空档。证据：
- en.json `home.heroActionCards` 15 个 Agent 里 **12 个是 marketing/growth 角色**（SEO Doctor / Ad Creative / Competitor Scout / Content Machine / Email Closer 等）
- 74 条 Reddit/Quora 问句 ~80% 能对应现成 Agent

### 4.2 零流量期关键词策略

- 只做 **KD < 10** 长尾 + **零量词**（playbook §2.3.4）
- **商业调查词**（`best X for Y`、`X vs Y`、`X alternative`）全部 defer 进 negative
- 品牌/导航词不进 Map
- 交易型（pricing）映射到 /pricing 页

### 4.3 Priority v0 临时打分公式（零流量期专用）

```
Priority_v0 = Info_intent_bonus (0/1) × 2
            + YOLOX_Match (0-3) × 1.5
            + Reddit_Evidence (0/1) × 2
            + Specificity (0-2) × 1
            = 最大 10 分
```

**Tier 分档**：Tier 1 ≥ 8 | Tier 2 5-7 | Tier 3 2-4 | ≤1 砍

**Day 7 升级路径**：拿到 Keywords Everywhere / Ahrefs 数据后，用 v1.1：
```
Priority_v1 = Priority_v0 × 0.5 + Volume_score × 0.25 + (10 - KD/10) × 0.25
```

### 4.4 12 个 Cluster 粗标（Day 5 精细化）

| Cluster | 主题 | Tier 1 数 | Day 5 Pillar 候选强度 |
|---|---|---|---|
| **C1** | AEO & llms.txt | 8 | ⭐⭐⭐ 强（+ YOLOX §2.6 同步 ship）|
| C2 | New-site SEO | 1 | ⭐ |
| **C3** | Shopify/ecommerce | 6 | ⭐⭐⭐ 强（ICP 聚焦）|
| C4 | SMB 获客 | 4 | ⭐⭐ |
| C5 | Content 产能 | 4 | ⭐ |
| C6 | Sales/Email | 1 | ⭐⭐ |
| **C7** | **Solopreneur AI** | 6 | ⭐⭐⭐⭐ **最强主 Pillar** |
| C8 | Competitor Intel | 2 | ⭐ |
| C9 | Social → Client | 1 | ⭐ |
| C10 | AI Agency | 0 | ⭐ 次要 Pillar |
| C11 | Connector × Agent | 2 | — |
| C12 | Launch/Referral | 2 | ⭐ |

### 4.5 3 个 Pillar 候选预测（Day 5 定稿，大概率是这 3 个）

| Pillar | Cluster 组合 | 主词候选 |
|---|---|---|
| **Pillar 1（主）** | C7 + 借 C1 + C3 + C4 | `AI agents for solopreneurs` |
| Pillar 2 | C1 + C2 | `AEO and llms.txt for new sites` |
| Pillar 3 | C3 + C6 + C9 + C12 | `AI marketing stack for Shopify/SaaS founders` |

### 4.6 下周 6 篇博客的选词方向（Day 6 正式挑）

**首选标准**（playbook §2.4）：
1. ≥ 2 条 Reddit/Quora 问句证据
2. YOLOX 有现成 Agent/Skill 能答
3. 1500–2500 字可控
4. KD < 10 或零量

**强候选 8 个**（Tier 1 有 Reddit 证据 10 条 + llms.txt 4 条变体）：
1. **Is llms.txt a scam? A 2026 reality check**（r/SEO 1srvco1 + §2.6 同步）🔥
2. How to close more sales faster with AI (for service businesses)（r/smallbusiness 1ss8ngr）
3. Why ChatGPT cites one page over another (AEO playbook)（r/SEO 1ss0drr）
4. How to get consistent clients for a cleaning business with AI（r/smallbusiness 1srl89h）
5. How to promote a Shopify store for sales（r/shopify 1srsdlw）
6. How to acquire customers for indie SaaS（r/SaaS 1srm4yl）
7. How to do distribution for indie SaaS（r/SaaS 1ss43uq）
8. How to get more genuine Google reviews（r/smallbusiness 1srnijf + r/ContentMarketing 1srx6uo）

---

## 5 · 未决策点（等小刀老师）

| # | 未决策 | 影响 | 阻塞? |
|---|---|---|---|
| 1 | Keywords Everywhere $10 买不买 | Day 7 回头重排 Priority 精度 | 否（Day 7 才真需要）|
| 2 | GITHUB_TOKEN | Day 6 想扫完整 agent/skill manifest 时会用 | 否 |
| 3 | Ahrefs 7 天试用 | 一次性跑 325 词 KD，Day 3 就能精准打分 | 否 |
| 4 | Review 04/07 的意见 | 可能要回头修 | 否（不 block Day 4）|
| 5 | Day 3 的 04 + 07 要不要 commit 进 PR #8 | 两个文件还未 commit | 下次 session 问一下 |

**默认行为**（如果小刀老师没回）：继续 Day 4 推进，Keywords Everywhere 没买就 KD 全保持 TODO。

---

## 6 · Day 4 具体怎么开

### 6.1 任务（来自 `2.3-keyword-research.md` Day 4）

产出 `docs/seo/keyword-research/05-zero-volume-strategy.md` 🟡：

1. **通俗解释什么是零量词**（对小刀老师学习模式友好）
2. 从 `03-reddit-quora-questions.md` 末尾"30 个零量词预选表"里**精选 30 个**（已预选好，可直接用）
3. 对每个词讲：
   - 原始出处（Reddit/Quora URL）
   - 用户真实痛点（引原帖内容）
   - YOLOX 的解决路径（具体到 Agent 名）
   - 预期写博客 / doc / agent 详情页
4. **学习目标**（小刀老师要求）：她读完能独立判断哪些 Reddit 问句值得做博客

### 6.2 省时提醒

- **30 个零量词清单 03 文档末尾已做好**，**不用重挖**，直接从 03 §"为 Day 4（05-zero-volume-strategy.md）预选的 30 个零量词种子"复制
- 原始 Reddit 数据在 `~/tools/opencli-raw/day1-*.json` + `day2-*.json`，如果要引用原帖内容可以 jq 拉
- 负向词清单 Day 3 已顺手做完（原计划 Day 4），Day 4 只剩 05 一份文档，3h 可 ship

### 6.3 Day 4 交付等级目标

🟡 可用（给 Day 6 博客选题用）

---

## 7 · 技术环境（下次 session 复用）

### 7.1 Node / OpenCLI

```bash
# 每次开新 session 先跑（shell state 不跨 Bash 调用持久化）
source ~/.nvm/nvm.sh
nvm use 22               # Node 22.22.2, OpenCLI 只在这里装
opencli doctor           # 应全 OK（如果不是，说明 Chrome 扩展断连）
```

**OpenCLI 版本**：CLI v1.7.6 + Chrome extension v1.0.2 + daemon on port 19825
**OpenCLI 路径**：`/home/lyric/tools/OpenCLI/`（clone 源码）
**原始数据**：`/home/lyric/tools/opencli-raw/*.json`（15 份，Day 1+2 跑的）

### 7.2 常用 OpenCLI 命令（Day 4-7 可能复用）

```bash
# Reddit 子版 hot（Day 1-2 经验：hot 比 top 更多求解帖）
opencli reddit subreddit <name> --sort hot --time week --limit 30 -f json > <file>.json

# Reddit 跨子版搜
opencli reddit search "<query>" --sort new --time month --limit 30 -f json > <file>.json

# Reddit 单帖详情（Day 4 可能用来引原帖内容作证据）
opencli reddit read <post-id> -f json > <file>.json
```

### 7.3 jq 常用筛（扫 title）

```bash
cd /home/lyric/tools/opencli-raw && \
jq -r '.[] | "[\(.comments // 0)c/\(.upvotes // .score // 0)] \(.title)  \(.url)"' <file>.json | head -20
```

### 7.4 Git 状态

- 当前分支：`feature/seo-geo-phase-2`
- 已 push 到 remote，PR #8 已开
- PR #8 里只有 Day 1+2 的 4 个文档（不含 Day 3 的 04/07，不含 Agent A 的代码改动）
- Agent A 的代码 + 其他 task docs 还在 working tree 未 commit（**留给 Agent A 自己 commit**，Agent B 不碰）

---

## 8 · 关键数据速查（避免下次 session 读 02/03 才能工作）

### 8.1 15 个 heroActionCards Agent（en.json `home.heroActionCards`）

```
Elias    · Traffic Commander
Sophie   · SEO Doctor
Stella   · Programmatic SEO Builder
Savannah · Paid Ads Strategist
Quinn    · Referral Architect
Arlo     · Launch Strategist
Addison  · Landing Page Builder
Olivia   · Ad Creative Studio
Isaiah   · SEO Content Factory
Theodore · Content Machine
Levi     · Copy Polisher
Sadie    · Video Producer
Eli      · Visual Creator
Daniel   · Email Closer
Evelyn   · Competitor Scout
```

额外 Agent（en.json 其他位置）：Nova（project partner）/ Kit（delivery）/ Mia（traffic/social）/ Alex（overseas sales，teamsStore fallback）

### 8.2 10 个 ICP placeholder（en.json `home.placeholder 1-10`）

```
1.  paid newsletter on Substack (作者)
2.  Shopify store (店主)
3.  SaaS product builder
4.  global product taker
5.  TikTok short video creator
6.  growth marketing team lead
7.  Amazon seller
8.  AI-powered tools builder
9.  YouTube creator
10. course creator
```

### 8.3 6 个 Connector（en.json `connectorsPage.providerNames`）

`Feishu / Gmail / Google Sheets / Notion / Slack / TikTok`

### 8.4 Reddit A 档 15 词（有 URL 证据）

Day 1 挖的 15 条，详见 03 文档 §1-4 / §10-11。这 15 条是下周博客选题的**最强候选池**。

---

## 9 · 红线（下次 session 绝对不要做）

1. **不改代码**（Agent B 纪律：启动提示词第一条）
2. **不 amend commit**（CLAUDE.md 显式禁止，pre-commit hook 失败时尤其不能）
3. **不瞎猜 Ahrefs KD 数字**（小刀老师明确说"我会人工代查"）
4. **不跳过前置说明**（破坏性操作前先说"要做什么 / 为什么 / 失败怎么回滚"）
5. **不擅自 push 到 main**（feature 分支 push OK，main 永远禁止）
6. **不用 `git add -A` / `git add .`**（CLAUDE.md 说可能误加敏感文件）
7. **不碰 Agent A 的代码**（src/* 改动 + analytics.ts + ReferralSourceSelect.tsx 全留给 Agent A）
8. **不碰其他 agent 的任务文档**（2.2 / 2.5 / 2.6 + README 不是 Agent B 职责）
9. **不提 context 切换事件**（这次 clear 是 solo-op 日常操作，不用小刀老师提醒我一次我提一次）
10. **不编造 Reddit URL**（每个 URL 必须真存在于 `~/tools/opencli-raw/` 的原始数据里；不确定时用 Grep 查）

---

## 10 · 小刀老师的沟通偏好（from `~/.claude/CLAUDE.md`）

- **对话中文**，代码注释/内部技术表达英文
- 称谓"小刀老师"（仅中文），英文文本省略
- **直白不绕弯**，剔空洞赞美和"你问得好"式开场
- **Emoji 仅结构用**（🟢🟡🔴 交付等级 / 🔑💸🗑🐛 大坑标红），不装饰
- **立场反自嗨**：面对她的想法先审可行性 / 指风险 / 再给改进方向（纯执行任务跳过批判）
- **学习模式**：新概念直接讲"是什么 + 具体例子"，不做多层类比；同一概念一会话内不重复解释
- **建造纪律**：重要命令前置说明、交付等级标注、大坑标红
- **复杂任务收尾三段式**：ship 了啥 / 学了啥 / 隐忧（跨 3+ 文件或 30min+ 任务触发）
- **不说"找工程师/eng"**（她是 solo-op，没有团队可找）

---

## 11 · 下次 session 的开工提示词（小刀老师直接粘贴给新窗口）

```
你是 YOLOX SEO 执行的 Agent B（§2.3 关键词研究）cold-start session。

本周 Day 3 已完成，现在开 Day 4。

第一步：Read docs/seo/keyword-research/00-session-handoff.md 全文。
第二步：按 §0 快速热身 checklist 执行。
第三步：跑 opencli doctor 确认环境 OK。
第四步：汇报 Day 4 执行计划，等我确认。

你的职责、工作纪律、技术环境、前 3 天已做的策略决策都在 handoff 里，不要重读 01/02/03 全文浪费 context。
```

---

## 12 · session 切换自检（小刀老师 /clear 前核对）

- [x] 04 + 07 两个文档已写入磁盘
- [x] 任务文档 Day 3 进度已 append
- [x] 本 handoff 已产出
- [ ] **小刀老师 review handoff 无误**（尤其 §4 策略决策部分）
- [ ] 小刀老师决定 04 + 07 要不要 commit（如果要，在 clear 前 commit）
- [ ] 小刀老师 /clear
- [ ] 新 session 粘 §11 开工提示词

---

**handoff 结束。**
