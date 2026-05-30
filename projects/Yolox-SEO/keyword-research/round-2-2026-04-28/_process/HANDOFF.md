# Round 2 关键词调研 · 任务交接

**起草**：2026-04-29
**面向**：冷启动的新 session Agent B（或接手的另一个 agent）
**状态**：8 层方案已 commit，0 层执行
**核心约束**：**每层任务必须先出方案 → 我们对齐 → 通过后才执行**（plan-first 工作流）

---

## 0 · 状态快照

| 维度 | 状态 |
|---|---|
| 8 层方案 (L0-L7) | ✅ 全部 commit（`1361f97`）|
| L1 manifest 拉取 | ✅ 已完成（agents 107 / teams 35 / skills 414 落 /tmp/）|
| L1-L7 实际执行 | ❌ 全部待执行 |
| 当前分支 | `feat/seo-keyword-research`（Agent B 专属，与 Agent A 隔离）|
| 当前 commit | `1361f97 docs(seo): ship round-2 keyword research 8-layer plans (L0-L7)` |
| GITHUB_TOKEN | ✅ 已更新到 `.env.local`（建议使用前查是否过期：试 manifest 拉取）|
| Ahrefs trial | ❌ 未激活（L2 Step 4 / L4 Step 3 / L7 Step 1 三处用）|
| 飞书 base | ❌ 未创建（L7 Step 4 用）|

---

## 1 · 文档索引（按读顺序）

### 必读（冷启动按此顺序）

| # | 文档 | 用途 | 长度 |
|---|---|---|---|
| 1 | `../METHODOLOGY.md` | 方法论 + 11 坑速查 + 工具栈 | 580 行 |
| 2 | `L0-overall-framework.md` | 顶层框架 + 8 层地图 + 验证粒度分层 | 180 行 |
| 3 | `HANDOFF.md`（本文）| 任务交接 + 启动指引 | — |
| 4 | 当前要执行的 LN-*.md | 当层细节方案 | 220-344 行 |

### 选读（按需）

| 文档 | 何时读 |
|---|---|
| `L1-seed-keywords-plan.md` | 执行 L1 / 看 ICP 反推链 |
| `L2-expansion-plan.md` | 执行 L2 / 8 渠道扩词 + 4 级筛选 |
| `L3-keyword-map-plan.md` | 执行 L3 / 6 维度打分 + 4 档 Tier |
| `L4-quantitative-validation-plan.md` | 执行 L4 / GAKP + Ahrefs 双源 |
| `L5-pillar-cluster-plan.md` | 执行 L5 / 5 标准选 3 Pillar |
| `L6-blog-outlines-plan.md` | 执行 L6 / 9 砍 6 + 1.5 页大纲 |
| `L7-final-precision-handoff-plan.md` | 执行 L7 / Ahrefs 精排 + 飞书 + 写作风格 |

### 引用资料（教材，不直接用）

| 文档 | 用途 |
|---|---|
| `../archive/round-1-2026-04-22/README.md` | 第 1 轮 11 个坑 + 复用矩阵 |
| `../archive/round-1-2026-04-22/raw-gakp-historical.csv` | 第 1 轮 217 词 GAKP 历史（参考）|

---

## 2 · 工作流约定（核心 · 不可破）

### 2.1 plan-first 流程

```
当前层 LN
  ↓
草案 v1（按 LN 文档结构）
  ↓
和小刀老师对齐（讨论关键决策点）
  ↓
草案 vN（修订到敲定）
  ↓
执行 → 交付 → 起草下一层
```

### 2.2 文档约定

- 头部用：`日期 / 讨论方 / 状态 草案 vN / 前置依赖`
- **不写**：审核 checklist / 签字栏 / "待老板填的字段" / "老板视角"
- 用语：草案 / 我们对齐 / 讨论敲定 / 待对齐
- 输入需求直接写在 Step 0，不另开"待填"章节

### 2.3 每层 plan 必含 6 字段

1. 当天目标（可量化）
2. 当天动作（具体步骤 + 命令模板）
3. 当天交付物（路径 + 字段）
4. 当天规避动作（11 坑映射）
5. 当天退出条件（什么情况叫停）
6. 对齐后下一步

### 2.4 汇报节奏

- 每个 Step 完成 → 简短汇报（密度优先 + 表格）→ 等下一步指令
- 遇决策点 → 列选项 + 推荐 → 等用户拍板再执行
- 工具失败 / 数据异常 → 立即停 + 列退出条件 → 等用户决定

---

## 3 · 8 层方案速查（执行参照）

| Layer | 主题 | 核心动作 | 交付 | 工期 |
|---|---|---|---|---|
| **L1** | 种子词 + 来源真实性 | manifest 反推 ICP / 8 渠道 / 3 池架构 | `01-seed-keywords.md` + 3 池 | ~5 hr |
| **L2** | 扩词 + 存在性验证 | 8 渠道扩词 / 4 级筛选漏斗 / Ahrefs 第 1 次用 | `02-expanded-keywords.md` + 4 文件 | ~9 hr |
| **L3** | 主库打分 | 6 维度 13 分 / 4 档 Tier + Tier-E / Cluster 雏形 | `04-keyword-map.md` | ~3 hr |
| **L4** | 量化验证 + 零量词 | GAKP + Ahrefs 双源 / 30 零量狙击词 / yoy 红利 | `04-v2.md` + 3 文件 | ~3 hr |
| **L5** | Pillar/Cluster | 5 标准选 3 Pillar / 5×3=15 / 5-3-1 发布 | `06-pillar-cluster-map.md` | ~3 hr |
| **L6** | 博客大纲 | 严格 4 纪律 9 砍 6 / 1.5 页 + Schema | `08-blog-outlines.md` | ~4 hr |
| **L7** | 落库 + 精排 + handoff | Ahrefs 第 2 次 / 17 分制 / 飞书 / 写作风格 | `04-v3.md` + 3 文件 | ~3 hr |

**总执行工期** ≈ 30 hr 净（不含审核回合）。

---

## 4 · 立即第 1 步动作（冷启动跑这个）

```bash
# 1. 验证环境
cd "/home/lyric/Infinite Flow Project/SEO/yolox-web"
git status
git branch --show-current  # 必须 = feat/seo-keyword-research

# 2. 验证 manifest 数据是否仍可读
ls -la /tmp/agents.json /tmp/teams.json /tmp/skills.json
# 如果文件不存在 → 重跑拉取（见 L1 Step 0）

# 3. 验证 GITHUB_TOKEN（可选）
( set -a; source .env.local; set +a
  curl -sL -H "Authorization: Bearer $GITHUB_TOKEN" \
    "https://api.github.com/repos/Infinite-Flow-Labs/yolox-agent-store" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('full_name', d.get('message','?')))"
)
# 期望: Infinite-Flow-Labs/yolox-agent-store
# 如果 Bad credentials → 找小刀老师重生 token
```

执行完上面验证后：

→ 进入 L1 执行：起草 **L1 Step 1+2+3 一次性产出**（领域映射 + ICP 反推 + 渠道清单），交给小刀老师对齐 → 通过后启动 Step 4 抓词

---

## 5 · 红线（不能碰）

1. **不擅自改 8 层方案**——要改回讨论后修订 LN 文档
2. **不写 Pool B/C 的词进主库**（L3 仅打分主库 v0；L2 4 级筛选过的才进主库）
3. **不删 EXPLORATORY 词**（标 `EXPLORATORY` 等 L4 验证后再分流）
4. **不破 4 选题纪律**（show-off / 1/1 孤例 / 产品答不上 / 内部人名 → 砍）
5. **不用 Claude 凭空扩词**（命中率 12.5%，第 1 轮坑 6.2）
6. **Ahrefs trial 7 天倒计时**（激活后立即标 expiry，覆盖 L2/L4/L7 三次使用）
7. **GAKP 必选 Historical metrics**（不要 Forecast，第 1 轮坑 6.6）
8. **CSV 立即 iconv 转码**（GAKP UTF-16 LE，第 1 轮坑 6.7）

---

## 6 · 资源 / 工具

| 类型 | 资源 | 状态 |
|---|---|---|
| 代码仓库 | `Infinite-Flow-Labs/yolox-web` | 当前分支 `feat/seo-keyword-research` |
| Manifest | `yolox-agent-store` + `yolox-skills-store` | 私有，需 GITHUB_TOKEN |
| opencli | `~/tools/opencli` | reddit/google/hn/so 搜索 |
| GAKP | Google Ads Keyword Planner | 不绑卡账户已注册 |
| Ahrefs trial | $7 / 7 天 | **未激活**（L2 Step 4 启动）|
| Haiku 4.5 | Claude plan 订阅 | L2 第 3 级筛 + L3/L4 辅助 |
| 飞书 base | — | **未创建**（L7 Step 4 用）|

---

## 7 · 决策已锁清单（不要再讨论）

| 项 | 选定 | 来源 |
|---|---|---|
| 范围 | 完整重做 | L0 §6 |
| 复用 | 仅复用 GAKP raw csv + 踩坑教材 | L0 §6 |
| 工具 | Ahrefs $7 trial | L0 §6 |
| Pillar 时机 | 数据驱动重选（5 标准全过）| L0 §6 / L5 |
| 调研 vs 写作 | 全调研完再写 | L0 §6 |
| L1 来源结构 | ICP 50% / 产品 40% / 探索 10% | L1 §1 |
| L2 渠道 | 全 8 个 | L2 §2 |
| L2 扩词分级 | A 深 + B 广 | L2 §2 |
| L2 筛选 | 4 级漏斗 | L2 §5 |
| L3 公式 | 6 维度 13 分 | L3 §2.1 |
| L3 Tier | 4 档 + Tier-E | L3 §3.1 |
| L4 Volume 公式 | 加分项不扣分 | L4 §4 |
| L4 撒网 | Pool B+C 也跑 | L4 §3.2 |
| L5 Pillar | 5 标准全过 / 3 个 / 5×3 | L5 §3 |
| L5 发布 | 5-3-1 混合排序 | L5 §4 |
| L6 大纲 | 1.5 页 + 5 FAQ + FAQPage+Article | L6 §3.2 |
| L7 精排 | Tier 0+1+2 / 17 分制 / 飞书 12-15 列 | L7 §3 |

---

## 8 · 给领导的高层 5 行版

> 第 2 轮关键词调研采用 **plan-first 工作流**（每层方案先对齐再执行）。已锁 8 层方案：从真实 manifest（107 agents / 35 teams / 414 skills）反推 ICP，8 渠道扩词后用 4 级漏斗筛 ~10000 候选 → 500 主库，6 维度→17 维度递进打分（v4_最终），数据驱动选 3 Pillar × 5 Cluster，5-3-1 发布，最终交付飞书 base + 6 篇博客大纲 + 写作风格指南。预计 30 小时净执行。第 1 轮 11 个坑全部规避。

---

## 9 · 启动提示词（复制粘贴用 · 给新 session）

见同目录 `BOOT-PROMPT.md`。
