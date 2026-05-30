# Layer 5 · Day 5 Pillar / Cluster 主题图方案

**日期**：2026-04-29
**讨论方**：小刀老师 + Agent B
**状态**：草案 v1（讨论中）
**前置依赖**：L4 v1 已交付（4 文件 · 主库 v2 + 零量词 + yoy 红利 + 死词）

---

## 0 · 你的决策（输入）

| # | 决策 | 选择 |
|---|---|---|
| 1 | Pillar 选择标准 | **1a** · 5 标准全过 |
| 2 | Pillar 数量 | **2a** · 3 个 |
| 3 | Cluster 数量 | **3a** · 每 Pillar 5 个 = 15 总 |
| 4 | 5-3-1 发布排序 | **4d** · 混合（红利 + 高分）|
| 5 | 内链网规则 | **5a** · 沿用第 1 轮（METHODOLOGY §5.6）|
| 6 | 零量狙击词归属 | **6b** · 归 Pillar Cluster |
| 7 | 输出文件 | **7a** · 单文件 06-pillar-cluster-map.md |

---

## 1 · L5 边界（不越界）

按 L0 §7 验证粒度分层：

| 越界 | 谁做 |
|---|---|
| ❌ 量化验证（Volume + yoy）| L4 已做 |
| ❌ 选博客大纲（H1 / TL;DR / H2-H3）| L6 |
| ❌ 写博客内容 | 下周 |
| ❌ 精确 KD | L7 |

**L5 只做 5 件事**：
1. 数据驱动决定 3 Pillar 主词
2. 每 Pillar 配 5 Cluster（共 15）
3. 5-3-1 发布顺序设计（哪 5 Cluster 先发）
4. 内链网规则
5. 零量狙击词的 Cluster 归属

---

## 2 · 当天目标

| 维度 | 目标 |
|---|---|
| Pillar 数 | 3 |
| Cluster 总数 | 15（3 × 5）|
| Cluster 词覆盖 | 主库 v2 Tier 0+1 词 ≥ 50% 入 Cluster |
| yoy 红利词覆盖 | 100% 入 Cluster（不能漏）|
| 零量狙击词归属 | 30 词全部归到 15 Cluster 中 |
| 5-3-1 首发 5 Cluster 选定 | 含 ≥ 2 yoy 红利 + ≥ 2 Tier 0 |
| 工期 | ~3 hr 净执行 |

---

## 3 · 当天动作（7 步）

### Step 1 · 候选 Pillar 主词识别（30 min）

#### 1.1 数据来源
- L3 Cluster 雏形（15-25 个粗分主题，按 ICP + Intent 双维度）
- L4 yoy 红利清单（5-15 词）
- L4 主库 v2 Tier 0/1 高分词

#### 1.2 候选 Pillar 主词清单（约 5-8 个）
从 L3 Cluster 雏形中，识别**能升级为 Pillar 候选**的主题（5-8 个）：
- 标题信息型 + 长尾扩展空间大
- 周围有 5+ Cluster 候选词

例（基于 archive/round-1/06 + v4 数据，**等 L4 实际跑出后调整**）：
- 候选 P-A: AI agents for solopreneurs
- 候选 P-B: llms.txt for new websites（红利）
- 候选 P-C: AI marketing stack for Shopify/SaaS founders
- 候选 P-D: AEO and AI Overview optimization（红利）
- 候选 P-E: AI agent builder / dev tools（Skills 217 个 Developer Tools）
- 候选 P-F: programmatic SEO for SaaS
- ...

#### 1.3 输出
- `/tmp/round2-day5-pillar-candidates.csv` 含每候选的 5 标准初评

### Step 2 · Pillar 选择（5 标准全过 · 45 min）

#### 2.1 5 标准（决策 1a · 全过）

每个 Pillar 候选必须通过：

| # | 标准 | 评分方式 |
|---|---|---|
| 1 | Intent 信息型 | 主词非 best/vs/pricing → ✅ |
| 2 | 5+ Cluster 候选 | 邻近词数 ≥ 5 → ✅ |
| 3 | Cluster 词 Volume>0 比例 ≥ 30% | 双源（GAKP + Ahrefs）任一有量 |
| 4 | 至少 1 个 yoy 红利词 | 在 05.5-yoy-rising.md 中 |
| 5 | Cluster 词 Tier 0+1 占比 ≥ 30% | L4 主库 v2 数据 |

**全过**才进 Pillar 入选名单。

#### 2.2 排序选 Top 3
若全过候选 > 3：
- 按"红利 + 高分混合"排：yoy 红利数 × 1.5 + Tier 0 词数 × 1.0
- 取 top 3

若全过候选 < 3（边界）：
- 放宽标准 4（红利可选不必选）
- 仍 < 3 → 收缩到 2 Pillar（E1 退出条件）

#### 2.3 输出
- 3 Pillar 主词锁定
- 每 Pillar 写 1 句话定位（"为什么选这个 Pillar"）
- 标 Pillar 优先级（按上述综合分）

### Step 3 · 每 Pillar 配 5 Cluster（决策 3a · 45 min）

#### 3.1 Cluster 选择标准

每 Cluster 必须：
- 子问题具体（"is X a scam" / "how to X for Y"）
- KD 估计 <10（基于 L7 trial，但 L5 可估算：长尾 + 社区证据 + 低 SERP 竞争）
- 至少 1 词 Reddit/Quora/IH 真问 OR yoy 红利

#### 3.2 配置流程

每 Pillar 操作：
1. 拉所有挂该 Pillar 主题的主库 v2 词（约 30-80 词）
2. 按子问题语义聚类（人工 + Haiku 4.5 辅助）
3. 选 top 5 子问题作为 Cluster
4. 每 Cluster 选 1 个**头词**（最高 Priority 那个）+ 4-8 个**长尾词**

#### 3.3 输出
- 3 Pillar × 5 Cluster = 15 Cluster
- 每 Cluster：头词 + 长尾词清单 + 对接 ICP + 对接产品 agent/skill

### Step 4 · 5-3-1 发布顺序设计（决策 4d 混合 · 30 min）

#### 4.1 混合排序逻辑

```
Cluster_publish_score =
    yoy_rising_count × 1.5    # 含 yoy 红利词加分
  + tier0_count × 1.0          # Tier 0 词数加分
  + tier1_count × 0.5          # Tier 1 词数加分
  + reddit_evidence × 0.5      # Reddit 真问加分
```

#### 4.2 排所有 15 Cluster
- 选 top 5 作"首发 5 Cluster"
- 限制：每 Pillar 至少 1 个首发（不集中在一个 Pillar）

#### 4.3 5-3-1 周期
```
Week 1: 首发 Cluster #1（混合 score 最高）
Week 2: 首发 Cluster #2
Week 3: 首发 Cluster #3
Week 4: 首发 Cluster #4
Week 5: 首发 Cluster #5（5 Cluster 完成）
        监控：3 Cluster 已被索引？
        ↓ 是 → 启动 Pillar 写作
Week 6: 第 1 个 Pillar 上线（对应 3 个已索引的 Cluster 中权重最高的 Pillar）
Week 7-9: 继续 Cluster #6-10（其他 Pillar 的首批）
Week 10-12: Pillar 2 + Pillar 3 上线 + Cluster 11-15
```

### Step 5 · 内链网规则（决策 5a · 沿用第 1 轮 · 15 min）

#### 5.1 链接类型 + 密度（METHODOLOGY §5.6）

| 类型 | 数量 | 锚文本规则 |
|---|---|---|
| Cluster → Pillar 主链 | 1 / Cluster 文末 | 完整语义短语（"AI agents for solopreneurs"，不要 "click here"）|
| Cluster ↔ Cluster 同 Pillar 邻近链 | 2-3 / Cluster 正文 | 子问题语义（"why ChatGPT cites some pages"）|
| Pillar → Cluster 锚点 | 5 / Pillar（每 Cluster 1 个）| 子问题完整短语 |
| 跨 Pillar | 1-2 / Cluster | 仅当真有相关性 |

#### 5.2 内链规则文档化
- 输出内链网图（Mermaid 或文字描述）
- 每 Cluster 的 outgoing links 清单
- 每 Pillar 的 incoming links 清单

### Step 6 · 零量狙击词归属（决策 6b · 30 min）

#### 6.1 归属流程
30 个零量狙击词（来自 L4 输出 05-zero-volume.md）：
- 每词按 ICP + 主题相关性匹配到 1 个 Cluster
- 进 Cluster 的"长尾词"部分（不作为 Cluster 头词）
- 标 `ZERO-VOL-SNIPER`

#### 6.2 边界
- 零量词不能升级 Cluster 头（头词必须有 Volume 信号）
- 同 Cluster 不能 > 30% 是零量词（避免 Cluster 整体无量）

#### 6.3 输出
- 30 零量词 → 15 Cluster 分布表
- 哪些 Cluster 因为零量词加成而升级
- 单独标"零量战略 Cluster"（如果某 Cluster 60%+ 是零量词）

### Step 7 · 主题图整理 + 落盘 06-pillar-cluster-map.md（30 min）

#### 7.1 文件结构

```markdown
# 06 · Pillar / Cluster 主题图

## 1 · 3 Pillar 锁定 + 选择依据
（含每 Pillar 的 5 标准评分 + 综合分）

## 2 · 15 Cluster 配置（3 × 5）

### Pillar 1: {主词}
- 定位：1 句话
- 头词清单：5 个 Cluster 头词（含 Priority + Volume + yoy）
- 长尾词清单：每 Cluster 4-8 个

### Cluster 1.1: {子问题}
- 头词 / 长尾词清单
- 对接 ICP / 产品 agent/skill
- 零量狙击词分布

（重复 Cluster 1.2 - 1.5 + Pillar 2/3 同结构）

## 3 · 5-3-1 发布顺序

### 首发 5 Cluster（Week 1-5）
1. {Cluster}: {混合分} - 选定理由
...

### Pillar 上线触发条件
- Week 5 监控点：3 Cluster 被索引（GSC 验证）
- 索引到位 → Week 6 启动 Pillar 写作

### Cluster 6-15 排期（Week 7-12）

## 4 · 内链网规则
- 链接类型 + 数量 + 锚文本规则
- 内链网图（Mermaid）

## 5 · 零量狙击词分布
- 30 词 → 15 Cluster 分布表
- 零量战略 Cluster（如有）

## 6 · L6 衔接
- 9 候选博客（覆盖首发 5 Cluster + 4 备选）
- L6 任务：4 选题纪律砍 6 留 + 出大纲
```

#### 7.2 末尾汇总
- 3 Pillar 锁定 + 综合分
- 15 Cluster + 词覆盖率
- 30 零量狙击词分布
- 5 首发 Cluster + 排期
- L6 衔接：9 → 6 候选博客

---

## 4 · 当天交付物

| 文件 | 内容 |
|---|---|
| `06-pillar-cluster-map.md` | 3 Pillar × 5 Cluster 完整 + 5-3-1 发布顺序 + 内链网 + 零量狙击词分布 |

仅 1 个文件（决策 7a · 单文件）。

---

## 5 · 当天规避动作（11 坑映射）

| 坑 | 规避 | 在哪 Step |
|---|---|---|
| **6.1 验证递归循环** | L5 不重做 L4 量化；不抢 L6 大纲 | 全 Step |
| **6.9 Pillar 拍脑袋** | **Step 2 严格 5 标准全过 + 数据评分**（不是直觉）| Step 2 |
| **6.10 yoy +∞ 真信号** | Step 2 标准 4 必含 yoy 红利；Step 4 红利加权 | Step 2/4 |
| 6.11 Handoff stale | L5 启动前 `git status` | 启动前 |
| 新 · Pillar 数量僵化 | 边界检查（候选 < 3 → 退到 2 Pillar）| Step 2.2 |
| 新 · Cluster 头词零量 | Step 6.2 强制头词必有 Volume 信号 | Step 6 |
| 新 · 内链锚文本"click here" | Step 5.1 显式禁用，必须语义短语 | Step 5 |

---

## 6 · 当天退出条件

| # | 触发 | 动作 |
|---|---|---|
| E1 | 5 标准全过候选 < 3 | 放宽标准 4 → 仍 < 3 → 收缩到 2 Pillar |
| E2 | 任一 Pillar 凑不出 5 Cluster | 该 Pillar 降到 4 Cluster；如 < 3 → 重选 Pillar |
| E3 | 5 首发 Cluster 集中在 1 个 Pillar | 调整：每 Pillar 至少 1 首发 |
| E4 | yoy 红利词数 = 0（L4 输出空）| 标准 4 改为"≥1 词 Volume>100" |
| E5 | 主库 v2 Tier 0+1 词数 < 30 | 警示——Pillar 候选可能基础不够，回 L4 重审 |
| E6 | 零量狙击词无法归属（>5 词找不到 Cluster）| 这些词放 watchlist，不强塞 |
| E7 | 内链网超载（某 Cluster outgoing > 8）| 砍至 5 以内 |

---

**对齐后下一步**：执行 Step 1（识别候选）→ Step 2（5 标准选 3 Pillar）→ Step 3（配 5 Cluster × 3）→ 中段对齐（Pillar/Cluster 锁定）→ Step 4-7（发布顺序 + 内链 + 零量分布 + 落盘）→ 起草 L6 博客大纲方案
