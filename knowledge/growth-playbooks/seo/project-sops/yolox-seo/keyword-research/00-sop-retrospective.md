# Round-2 关键词研究 SOP 复盘

> **目的**：给小刀老师 round-3 起手用 — 5 分钟看完知道"上次怎么做、下次怎么压缩、哪些坑要避"。
>
> **取材**：本目录全部 markdown + `data/` 产物，读取于 2026-05-12。
>
> **方法**：subagent 通读 + 我手动 verify 4 个关键缺口。
>
> **未交叉验证**：subagent 报告的具体数字（如 "3702 帖"、"570 词"、"47.6%"）— 我未逐一回查源文件交叉验证，按 90% 可信度处理。

---

## 1 · 流程总览

| 层 | 主题 | 输入 → 输出 | 词数变化 |
|---|---|---|---|
| **L0** | 顶层框架 | 5 项决策 + 8 层地图 + 11 坑映射 | — |
| **L1** | 种子词（来源真实）| manifest → ICP 反推 → 3 渠道抓帖 → 三层池 | **抓 3702 帖 → Pool C 903 / Pool B 91 / Pool A 66** |
| **L2** | 扩词 + 存在性 | Pool A 76 词 × 8 渠道 Suggest → Haiku 批量 4 问筛 | **1316 unique → master v0 666** |
| **L3** | 主库打分 | 666 → 去重 570 → 6 维度 13 分公式 | **570 词分 Tier 1/1.5/2/3（6 / 58 / 88 / 418）** |
| **L4** | 量化验证 | 计划 GAKP + Ahrefs 双源 → **实际 pivot 到 KWFinder paid** | 570/570 全量化（V/KD/Growth/Intent/SERP）|
| **L5** | Pillar/Cluster | Tier 1+1.5+2 共 152 词 → 5 标准选 Pillar | **24 主词**（4 Pillar 主文 + 20 Cluster）|
| **L6** | 博客大纲 | 24 主词 → 1.5 页大纲 + Schema | **25 篇大纲**（v1 计划 6 → v2 补到 25）|
| **L7** | 落库 + handoff | 计划 Ahrefs 精排 + 飞书 → **实际仅 handoff + coverage 文档** | — |

净执行预估 30 hr，实际跨 2026-04-28 → 05-08 共 10 天（含审核回合）。

---

## 2 · 每层 SOP

### L1 · 种子词
- **做什么**：从产品 manifest 反推 ICP，再去 Reddit/Quora/IH 挖真痛点
- **工具**：opencli reddit/quora/hn · GitHub manifest（107 agents / 35 teams / 414 skills）· Google Suggest · 8 新兴渠道
- **决策点**：来源 60/20/10（ICP 60% / 产品语义补缺 20% / 新兴 10%）；4 条质量标准全过才进 Pool A
- **量化**：抓 3702 帖 → 机械筛 27% 通过 → Pool C 903 帖 → Layer 2 4 问筛 → Pool B 91 → Pool A 46+13+7=66 词
- **坑**：禁用 Claude 凭空扩（L0 坑 6.2）；hero 名 50 词黑名单（坑 6.5）
- **产物**：`_process/01-seed-keywords.md` · `_process/01.5-pool-{b,c}-*.md`

### L2 · 扩词 + 存在性
- **做什么**：Pool A 每词过 8 渠道 Suggest，候选爆炸到几千，4 级漏斗筛回 666
- **工具**：opencli Suggest（Google / YouTube / Bing / DDG）+ Reddit/Quora/IH/Twitter Suggest · **Haiku 4.5 批量 4 问筛**
- **决策点**：4 级漏斗 — 机械去重 → 自动质量信号 → Haiku 4 问语义（真问题/产品能解/搜索形/ICP 25-list）→ 4 标准
- **量化**：Pool A 76 + Step2 1890 sugg + Step3 27 sugg + KWFinder 30 = **1316 unique → 590 keep（47.6%）/ 175 keep_weak / 475 cut → 主库 v0 666 词**
- **产物**：`_process/02-expanded-keywords.md`（719 行）

### L3 · 主库打分
- **做什么**：6 维度 13 分公式给 570 词打分分档
- **工具**：Python `scripts/l3_score_master.py`
- **决策点**：公式 = Volume×3 + KD×3 + Intent×2 + Growth×2 + ICP×2 + 产品对接×1 = 13 满分；Tier 1 ≥9 / Tier 2: 6-8 / Tier 3 <6；**新增 Tier 1.5**（ICP 长尾，KWFinder 无 Volume 但 ICP 直击）单列
- **量化**：666 → 去重 570 → **Tier 1: 6 / Tier 1.5: 58 / Tier 2: 88 / Tier 3: 418**
- **产物**：`_process/03-master-scored.md` · `data/master_scored.json`

### L4 · 量化验证（**最大 pivot 层**）
- **plan**：GAKP + Ahrefs Bulk lookup 双源（`L4-quantitative-validation-plan.md:38-44`）
- **实际**：**KWFinder paid $39**（`99-handoff-leader-review.md:14`）
- **GAKP 实际未跑**（verify 2026-05-12 by `ls data/Data_Gotted/`）— 只有 KWFinder + batch-*.csv，无 gakp-*.csv
- **Ahrefs trial 已过期**（`L7-final-precision-handoff-plan.md:220` 明写）
- **量化**：570/570 全覆盖；零量比例约 30%（远好于 round-1 的 94.5%）
- **坑**：48h 退款窗口必须 5/9 18:00 前退订（💸 已记入 handoff §5 风险表）
- **产物**：`data/master_scored.json` · `data/Data_Gotted/kwfinder_*.csv`

### L5 · Pillar/Cluster
- **做什么**：数据驱动选 Pillar，每 Pillar 配 5 Cluster
- **工具**：`scripts/l5_pillar_cluster_v2.py` + Ben PR #14 review
- **决策点**：5 标准（Intent info / 5+ Cluster 候选 / Vol>0 ≥30% / 至少 1 yoy 红利 / Tier 0+1 ≥30%）；最终选 **AEO + α(AI 工具) + β(B2B Sales/招聘) + γ(Creator/SMB)** 4 个，不是计划的 3 个
- **量化**：Tier 1+1.5+2 共 152 词 → 24 主词；URL silo `/blog/{aeo|ai-tools|b2b|creator}/{slug}`
- **坑**：α 主词 `AI infographic generator` 词义偏窄但 KD 低，用 Hybrid 主文（窄词 target + hub 5 cluster）兜底
- **产物**：`_process/04-pillar-cluster.md`（v2.1）

### L6 · 博客大纲
- **做什么**：每个主词写 1.5 页大纲（H1 + meta + TL;DR + H2-H3 + 5 FAQ + Schema + 内链）
- **工具**：Claude 手写
- **决策点**：4 选题纪律严格过；FAQPage + Article Schema 模板；每篇至少 2 Reddit 原帖证据
- **量化**：原 plan 9 砍 6；**实际 ship 25 篇大纲**；Ben 锁定 KD ≤25 的 6 篇优先写 markdown（L6-01~06）
- **产物**：`blog-outlines/L6-*.md` 25 个

### L7 · 落库 + handoff（**plan vs 实际严重不符**）
- **plan 4 步**：Ahrefs 精排 230 词 / 17 分制重打分 / 飞书 CSV 12-15 列 / 写作风格指南 3 段（`L7-final-precision-handoff-plan.md:14-17`）
- **实际**：
  - Ahrefs 精排 → **未做**（Ahrefs trial 已过期）
  - 17 分制重打分 → **未做**
  - 飞书 base + `09-feishu-import.md` → **未创建**（verify by `ls _process/`）
  - 写作风格指南 → **未创建**
- **改 ship 的**：`99-handoff-leader-review.md` + `0-share/keyword-coverage.md` + `0-share/frontend-spec.md`
- **task #18 L7 仍 in_progress** — 这是事实，不是疏漏

---

## 3 · 关键 Pivot 时间线

| 时间 | Pivot | 原因 |
|---|---|---|
| L1 v3→v4（04-29）| 来源占比 50/40/10 → 60/20/10；新增三层池 A/B/C | Pool B/C 不丢词，留 L2 升级路径 |
| L2 v1→v2（04-29）| 渠道从仅 PAA → 全 8 个；新增 Haiku 4 问筛 | 候选爆炸需 LLM 批量过 |
| L3 新增 Tier 1.5（05-07）| 6 维度公式对零 Volume 长尾不公允 | 58 词，否则全沉 Tier 3 被废 |
| **L4 工具 pivot**（约 05-04）| **Ahrefs $7 trial → KWFinder paid $39** | Ahrefs trial 已过期（已 verify）。**其他选型理由 ❓ 待小刀老师确认**（是否对比过 SEMrush / 仅找了一个 / 还是 KWFinder 有特定优势）|
| L5 3 Pillar → 4 Pillar（05-07）| 计划 3×5=15 → 实际 4×5=24 | Ben review 后认为覆盖应更广 |
| L6 6 篇 → 25 篇大纲（05-07→08）| 全 24 主词 ship 大纲，6 篇 markdown 优先 | Ben 锁 6 篇 KD≤25 先 ship，剩 19 篇大纲先占位 |
| L7 plan→实际 | 4 步全部未做，改 ship 3 个文档 | Ahrefs trial 过期 → 精排做不了 → 17 分制 / 飞书 / style guide 连锁未做 |

---

## 4 · Round-3 简化版

| 环节 | 决策 | 理由 |
|---|---|---|
| L0 顶层框架 | **保留**——缩到 1 页 | 5 决策 + 11 坑速查够用 |
| L1 manifest 反推 ICP | **省**——复用 round-2 | ICP 25-list 已 stable |
| L1 Reddit 三层池抓帖 | **保留 + 自动化** | 脚本成熟，跑增量 |
| L2 8 渠道 Suggest 全做 | **缩**——仅 Google + Reddit/Quora 关键 sub | YouTube/Bing/DDG 边际收益低 |
| L2 Haiku 4 问筛 | **保留** | 47.6% 通过率说明 prompt 已调好 |
| L3 6 维度公式 | **保留** | 含 Tier 1.5 单列 |
| L4 量化工具 | **决策点**——要么再 KWFinder $39 / 要么只跑增量 | 看 round-3 候选词数 |
| L5 4 Pillar 架构 | **保留** | silo URL 已锁，不要再动 |
| L6 大纲 → markdown | **核心**——把 19 篇剩余大纲写成 markdown | round-3 主线 |
| L7 飞书 | **省** | markdown + git 够用 |

**最小可跑流程**：L1 增量 → L2 仅 Google Suggest → L3 复用脚本 → L5 不重选 Pillar → L6 写 markdown。预估 8-12 hr。

---

## 5 · 缺口清单（verify 修正版）

| # | 项 | 状态 | 备注 |
|---|---|---|---|
| 1 | L4 从 Ahrefs/GAKP → KWFinder 的选型理由 | 🟡 部分缺 | Ahrefs trial 已过期 = 确定；**为何选 KWFinder 而非 SEMrush 等** = ❓ 待小刀老师确认 |
| 2 | L3 Tier 1.5 档位引入的临界讨论 | 🟡 部分缺 | `03-master-scored.md` §2.5 表头出现，未说决策时点 / 阈值 |
| 3 | L5 从 3 Pillar → 4 Pillar 的决策记录 | 🟡 部分缺 | `04-pillar-cluster.md` §5 列了 5 条 Ben 决策，未说"为何 4 不是 3" |
| 4 | L6 从 6 篇 → 25 篇大纲的扩张决策 | 🟡 部分缺 | 提了"Ben 锁 6 篇先写 markdown"，未说"为何另 19 篇也要先写大纲" |
| 5 | **GAKP 实际未跑** | 🟢 已 verify | `ls data/Data_Gotted/` 无 gakp-*.csv |
| 6 | opencli 工具版本/调用细节 | 🟡 缺 | 脚本里 import 了但无 versioning |
| 7 | **Ahrefs trial 已过期** | 🟢 已 verify | `L7-final-precision-handoff-plan.md:220` 明写 |
| 8 | **L7 飞书 + style guide 未 ship** | 🟢 已 verify | task #18 仍 in_progress；`_process/` 无 `09-feishu-import.md` |
| 9 | Haiku 4 问 prompt 全文 + verdicts JSON schema | 🟡 部分缺 | prompt 模板在 plan 里，实际 13 batch 跑的 prompt + verdicts schema 未单独文档化 |
| 10 | `scripts/` 28 个脚本依赖关系图 | 🟡 缺 | handoff §8 列了清单，无 DAG 图 |

**真 🔴 缺**：0 项（全部已 verify 修正）。
**🟡 部分缺**：6 项（不影响 round-3 起手，但写新人 onboarding 时要补）。
**❓ 待你确认**：1 项（L4 选型理由）。

---

## 6 · 一句话总结

Round-2 真正跑通的是 **L1（reddit 三层池）+ L2（8 渠道 + Haiku 漏斗）+ L3（6 维度打分）+ L4（KWFinder paid 全量化）+ L5（4 Pillar 数据驱动）+ L6（25 大纲）**；**L4 工具从 Ahrefs trial pivot 到 KWFinder 是关键单点改动**（直接连锁导致 L7 plan 4 步全部未做）；**L7 仍 in_progress**，飞书 / 精排 / 写作风格指南改成 `0-share/` 三文档兜底。Round-3 主线是**把 19 篇剩余大纲写成 markdown**，调研环节可大幅压缩到 8-12 hr。

---

## 7 · 给 round-3 / 新人的"5 分钟入门"

打开顺序：
1. **本文档** — 知道全貌
2. `_process/L0-overall-framework.md` — 顶层决策 + 11 坑
3. `_process/99-handoff-leader-review.md` — 数据漏斗证据链
4. `_process/04-pillar-cluster.md` — Pillar/Cluster 决策
5. `blog-outlines/` — 25 篇大纲
6. `0-share/keyword-coverage.md` — 团队对外入口
7. `../../blog-template/` — 写作时打开

跑下一轮起手：
```bash
# 从复用 round-2 ICP 开始
cat _process/01-seed-keywords.md | grep -A20 "ICP 25-list"
# 跑 L1 增量
python scripts/capture_reddit.py --incremental
# 跑 L2 仅 Google Suggest
python scripts/expand_via_suggest.py --channels google
# 复用 L3 打分脚本
python scripts/l3_score_master.py
```
