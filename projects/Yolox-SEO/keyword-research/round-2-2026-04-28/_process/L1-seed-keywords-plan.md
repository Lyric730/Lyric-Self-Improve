# Layer 1 · Day 1 种子词调研方案

**日期**：2026-04-28（v4 修订 2026-04-29）
**讨论方**：小刀老师 + Agent B
**状态**：草案 v4（讨论中）
**前置依赖**：L0 已对齐
**v4 主要变更（vs v3）**：
- 来源占比 50/40/10 → **60/20/10**（ICP 痛点 60% / 产品语义补缺 20% / 新兴 10%）
- Step 5 重定位：从"产品 × ICP 交集"→"产品语义补缺（compare/buy 词）"
- 新增**三层候选词池架构**：保留 99% 被筛掉的词作为 L2 扩词池
- 输出物从 1 文件 → **4 文件**（种子 + Pool B + Pool C + watchlist）
- 11 坑规避升级：6.2 Claude / 6.4 Reddit 1/1 用新机制根除

---

## 0 · 前置阻塞 · ✅ 已解决

- GITHUB_TOKEN 更新完成
- 3 个 manifest 全部拉到 `/tmp/agents.json` `/tmp/teams.json` `/tmp/skills.json`

**关键数据快照**：
```
agents  · 107 个 · 13 个 domain（最大：Business 17 / Growth 14 / Media 11 / Sales 10）
teams   · 35 个 · 7 个 category（最大：content 8 / service 7 / in-house 6）
skills  · 414 个 · 11 个 tag（最大：Developer Tools 217 / Design 54 / Productivity 47）
```

⚠️ Skills 一半是 Developer Tools → **YOLOX 是 AI 开发者 + 营销混合平台**，ICP 必须包含 dev/builder。

---

## 1 · 当天目标

| 维度 | 目标 |
|---|---|
| 种子精选（Pool A）| **~63 词**（质量优先，数量是经验值不是目标）|
| 候选词池（Pool B）| ~200 词（高质量，L2 扩词优先池）|
| 原始词池（Pool C）| ~750 词（粗筛过，L2 扩词备用池）|
| 新兴 watchlist | ~10-15 词（单源未验证）|
| 来源结构（Pool A）| ICP 真痛点 60% (42) / 产品语义补缺 20% (14) / 新兴探索 10% (7) |
| 质量标准 | 每词必须 4 条全过（详见 §1.1）|
| 人名陷阱 | 0 个含 YOLOX 人名 |

### 1.1 每个种子词的 4 条质量标准（仅 Pool A 强制）

每词必须 **4 条全过**：

1. **产品能答**：YOLOX 真有 agent/skill/team 能落地（不是空头支票）
2. **ICP 真在搜**：有 Reddit/Quora/IH URL 证据 OR Google suggest hit OR PAA 出现
3. **有扩展空间**：能扩 5+ 长尾
4. **可挂 Cluster**：周围有 4-5 个相邻词能撑一个 Cluster 候选

不全过 → 砍出 Pool A，留在 Pool B（如果过了 2-3 条）。

---

## 2 · 当天动作（7 步）

### Step 0 · 拉真实 manifest · ✅ 已完成

输出：`/tmp/agents.json` (440KB) · `/tmp/teams.json` (118KB) · `/tmp/skills.json` (1MB)

### Step 1 · 能力 → 应用领域映射 + 数据规范化（30 min）

**1.1 数据规范化**：
- `agents.domain` 合并 `E-commerce` (6) + `E-Commerce` (2) → 统一 `E-commerce` (8)
- 其他字段值过一遍，发现拼写不一致继续修正

**1.2 领域映射**：
- 直接用 manifest 自带分类字段（不用人工标）：agents.domain (13) + teams.category (7) + skills.tag (11)
- 跨 manifest 去重合并相邻领域

**1.3 输出**：
- 领域全集（去重后约 15-20 个）
- 每个领域挂多少能力（agent + team + skill 计数）
- 重点高频领域 top 6（Business / Growth / Media / Sales / Operations / Developer Tools）

### Step 2 · 领域 → ICP 反推（45 min）

每个领域映射到 **真实 ICP 群体**（含 dev/builder 主线）。

**ICP 列举原则**：
- 谁会真的需要这种能力？
- 谁愿意付钱解决这种问题？
- 谁在 Reddit / Quora / IH 真实出现过 "as a X" 句式？

**预期 ICP 类目**（约 20-25 个）：

| 大类 | 细分 ICP 示例 |
|---|---|
| 营销 / 增长 | growth marketer · DTC brand · Shopify owner · Amazon seller · paid ads media buyer |
| 内容创作 | newsletter writer · blogger · YouTuber · TikTok creator · podcaster · course creator |
| 销售服务 | B2B SDR · agency owner · freelancer · coach |
| 实体业务 | local business owner · real estate agent · service biz |
| **开发者** | **indie SaaS founder · AI builder · solo developer · automation engineer · low-code maker** |
| 设计 / 创意 | designer · illustrator · video editor |
| 数据 / 运营 | data analyst · ops specialist |
| 财务 / 教育 | bookkeeper · online tutor |

**输出**：ICP 清单（20-25 个）+ 每 ICP 对应领域 + 第 1 轮是否覆盖（标 ✅/❌）

### Step 3 · ICP → 渠道映射（30 min · M 层覆盖面）

#### 3.1 Reddit（主战场，30-40 sub）
按 ICP 找 2-3 个高质量 sub。例：
- growth marketer → r/marketing · r/growthhacking · r/PPC
- DTC/Shopify → r/shopify · r/ecommerce · r/FacebookAds
- B2B SDR → r/sales · r/salestechniques · r/coldemail
- indie SaaS founder → r/SaaS · r/Entrepreneur · r/indiehackers
- AI builder / dev → r/LocalLLaMA · r/MachineLearning · r/aiprogramming · r/Anthropic

#### 3.2 Quora（补充：Reddit 少的 ICP）
主要扫：coach · 实体店主 · 律师 / 会计师 / 房产经纪 · online tutor · bookkeeper

#### 3.3 IndieHackers（补充：builder/founder 自述）
主要扫：indie SaaS founder · solo developer · AI builder

**输出**：30-40 sub + Quora ICP 列表 + IH 范围

### Step 4 · ICP 真痛点挖词 · 三层池架构（核心 · 1.5 hrs）

#### 4.1 抓取（M 层 · ~2500 帖）

每 sub **hot week 30 帖 + top month 30 帖**：
```bash
opencli reddit subreddit r/{sub} --sort hot --time week --limit 30
opencli reddit subreddit r/{sub} --sort top --time month --limit 30
opencli reddit search --query "as a {ICP} how do I" --sort top --time year --limit 20
```

Quora：每 ICP 5-10 高 view 问题
IndieHackers：近 1 月 votes 排序前 200 帖

输出 raw JSON：`~/tools/opencli-raw/round2-day1-{platform}-{sub|icp}.json`

#### 4.2 三层漏斗 + 三层池落盘（关键架构）

```
~2500 帖
  ↓ 第 1 层 · 机械筛（脚本批量）
  · score≥5 + 评论≥5（Reddit）/ views≥1000（Quora）/ votes≥3（IH）
  · 标题含信号词：how / why / what / any tool / struggling / need help / as a / ?
  · 标题不含展示词：I built / I launched / Show HN / AMA / results / hit $X
  ↓
~750 帖 → 转换为关键词 → 落盘 Pool C · 原始候选
  ↓ 第 2 层 · 语义筛（4 问 · 人工 + Claude 辅助）
  · 是真实求解，不是吐槽 / 故事 / 公告？
  · 痛点能被 YOLOX 某 agent / skill 解决？
  · 标题能直接或简单转换成搜索词？
  · ICP 是 Step 2 反推清单内的？
  ↓
~200 词 → 落盘 Pool B · 高质量候选
  ↓ 第 3 层 · 去重 + 选最高互动 + 4 标准全过
  ↓
~42 词 → Pool A · 种子精选（ICP 痛点部分，60%）
```

#### 4.3 Pool C 字段（与 Pool A 同精度，3a 决策）

| 字段 | 内容 |
|---|---|
| post_id | Reddit base36 / Quora url slug / IH post id |
| 平台 | Reddit / Quora / IH |
| subreddit / source | r/SEO 等 / Quora 主题 / IH 板块 |
| title | 原帖标题（截 80 字符）|
| score / num_comments / views | 互动指标 |
| url | 完整 url |
| 提取的种子词 | 转换后的搜索意图词 |
| 对接 ICP | Step 2 反推清单中的 ICP（可能多对一）|
| 对接产品能力 | Step 1 manifest 中的 agent/skill/team（如适用）|
| 池标签 | A / B / C |
| 排除原因 | （仅 B/C）哪一条 4 标准未过 |

#### 4.4 落盘文件

| 文件 | 内容 |
|---|---|
| `01-seed-keywords.md` | Pool A · 42 词 ICP 痛点部分（先占位，Step 5/6 后追加）|
| `01.5-pool-b-candidates.md` | Pool B · ~200 词高质量候选 |
| `01.5-pool-c-raw.md` | Pool C · ~750 词原始候选 |

### Step 5 · 产品语义补缺（compare/buy 词）（45 min · 14 词 · 20%）

**重新定位（v4）**：不是"产品 × ICP 交集"，是 **Step 4 ICP 痛点未覆盖的产品能力补词**。

**重点补两类**：
- **dev/builder 类**：Skills 中 Developer Tools 217 个，Reddit 痛点反推不出"AI agent for code review"，需从产品端拼
- **compare/buy 词**：用户已知工具时搜的词，info 痛点词覆盖不到

**模板**：
```
{Agent role_title} for {ICP}                  # compare 意图
how to {Skill name} as a {ICP}                # buy 意图
{Skill tag} AI agent for {ICP}                # 产品类目
best AI agent for {场景}                      # 决策类
```

例：
- `AI agent for code review`（Skills · Developer Tools 类）
- `AI agent for invoice automation`（Skills · Finance & Legal 类）
- `programmatic SEO agent for SaaS founders`（compare）
- `AI ad creative tool for DTC brands`（buy 意图）

**质量门**（每词必过）：
- 产品对接：能指向至少 1 个真实 agent / skill / team（manifest 验证）
- 真实搜索证据：opencli google suggest 至少 1 hit OR PAA 出现
- **禁用人名**（坑 6.5）：终检每词无 Sophie / Elias / Stella 等
- **去重 Step 4**：与 Pool A/B 已有词不重复

**输出**：14 词，追加到 `01-seed-keywords.md`

### Step 6 · 新兴生态主动扫描（45 min · 7 词 · 10% · `EXPLORATORY`）

8 渠道全扫：

| # | 渠道 | URL / 命令 |
|---|---|---|
| 1 | HN top week | `opencli hn search --sort top --time week` 50 帖 |
| 2 | GitHub trending weekly | https://github.com/trending?since=weekly · top 25 repo |
| 3 | Anthropic docs release notes | https://docs.anthropic.com/en/release-notes/overview · 近 1 月 |
| 4 | OpenAI blog | https://openai.com/blog · 近 5 篇 |
| 5 | Google AI blog | https://blog.google/technology/ai/ · 近 5 篇 |
| 6 | Aleyda Solis newsletter | https://www.aleydasolis.com/en/newsletter/ · 最新一期 |
| 7 | Search Engine Land | https://searchengineland.com/library/seo · 近 1 周 |
| 8 | r/SEO + r/MachineLearning + r/LocalLLaMA hot week | 同 §4.1 |

**双源验证**：每候选词 ≥ 2 个独立渠道出现 → 进种子标 `EXPLORATORY`
单源词存 `01.5-watchlist.md` 不进种子。

**保留**：新概念 / 协议 / spec（mcp · a2a · agent2agent · structured outputs · AEO · GEO · LLMO）
**砍**：广泛已知（GPT-4 / Claude 3）/ 公司动态（融资 / 雇人）/ 太小众（only 1 source）

**输出**：
- 7 词追加到 `01-seed-keywords.md`（标 `EXPLORATORY`）
- 单源词落盘 `01.5-watchlist.md`

### Step 7 · 去重 + 4 标准 + 整理（30 min）

- 跨 Step 去重（4/5/6 之间）
- **Pool A 4 条质量标准过一遍**：每词显式打 ✅/❌
- 不全过 → 降级到 Pool B
- 4 个文件最终落盘 + 末尾汇总段

---

## 3 · 当天交付物（4 文件）

| 文件 | 内容 | 数量 | 字段精度 |
|---|---|---|---|
| `01-seed-keywords.md` | **Pool A · 种子精选** | ~63 | 完整 |
| `01.5-pool-b-candidates.md` | Pool B · 高质量候选 | ~200 | 完整（同 A）|
| `01.5-pool-c-raw.md` | Pool C · 原始候选 | ~750 | 完整（同 A，3a 决策）|
| `01.5-watchlist.md` | 新兴生态单源词 | ~10-15 | 简略（词 + 单源 url + 类别）|

**字段表结构**（Pool A/B/C 共用）：

| # | 关键词 | 来源 | Intent | ICP 对接 | 产品对接 | 平台 | URL | 标签 | 4 标准 | 池 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | how to do pSEO as a SaaS founder | ICP | info | indie SaaS founder | Stella · Programmatic SEO Builder | Reddit | reddit.com/r/SaaS/... | — | ✅✅✅✅ | A | score 28/12 |
| 2 | AI agent for code review | 产品语义 | compare | AI builder | Skills · Developer Tools | suggest | google suggest | — | ✅✅✅✅ | A | — |
| 3 | A2A protocol for marketers | 新兴 | info | growth marketer | — | HN+Anthropic | 双源 url | EXPLORATORY | ✅✅?? | A | 等 L4 |
| 4 | how to grow newsletter | ICP | info | newsletter writer | Theodore · Content Machine | Reddit | reddit.com/r/Substack/... | — | ✅✅❌✅ | B | 不能扩 5 长尾 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**`01-seed-keywords.md` 末尾汇总段**：
- Pool A 总词数 + 各来源占比
- 平台分布（Reddit / Quora / IH / suggest / 多源）
- 4 条质量标准全过率
- `EXPLORATORY` 词数
- 含人名陷阱词：0
- ICP 类附 URL 比例
- 三层池总规模（A 63 / B 200 / C 750）

---

## 4 · 当天规避动作（11 坑映射 · v4 升级）

| 坑 | v4 规避 | 在哪 Step |
|---|---|---|
| **6.2 Claude 12.5%** | **L2 从 Pool B/C 派生，不再凭空扩** | Step 4 三层池架构 |
| 6.3 Reddit show-off 陷阱 | 第 1 层机械筛排除展示词 | Step 4.2 |
| **6.4 Reddit 1/1 孤例** | 第 1 层互动阈值 + Pool C 保留低互动作 watchlist | Step 4.2 |
| 6.5 内部 Agent 人名 ≠ 搜索词 | Step 5 + Step 7 终检 | Step 5 + Step 7 |
| 6.11 Handoff stale | L1 启动前 `git status` + `git branch --show-current` | 启动前 |
| 新 · ICP 营销门面陷阱 | manifest 反推 ICP，不只 placeholder | Step 0-2 |
| 新 · 数据脏点 | Step 1 显式规范化（如 E-commerce 大小写）| Step 1 |
| 新 · 单平台偏差 | M 层 3 平台覆盖（Reddit + Quora + IH）| Step 4.1 |
| **新 · 抓取浪费** | **三层池保留 99% 被筛词** | Step 4.2 |

---

## 5 · 当天退出条件

| # | 触发 | 动作 |
|---|---|---|
| E1 | manifest 解析出错（JSON 损坏 / 字段缺失）| L1 暂停，修复后继续 |
| E2 | Pool A 总词数 < 50 | 暂停回 L0 对齐 |
| E3 | Step 2 反推不出 ≥ 15 个真实 ICP | 调整领域定义重做 |
| E4 | Pool A 任意来源 < 50% 目标（ICP < 25 / 产品 < 7 / 新兴 < 4）| 调整后重做该来源 |
| E5 | Pool A 4 条质量标准通过率 < 70% | 暂停回 Step 1 重审来源 |
| E6 | 某 ICP Pool A 种子 < 1 词 | 4.5 针对性补抓（不暂停）|
| E7 | Pool C 总规模 < 400 词 | 抓取深度可能不够，回 Step 4.1 加抓 |

---

**对齐后下一步**：执行 Step 1（manifest 解析 + 规范化）→ Step 2（ICP 反推）→ Step 3（渠道清单）→ 中段对齐一次后继续 Step 4-7
