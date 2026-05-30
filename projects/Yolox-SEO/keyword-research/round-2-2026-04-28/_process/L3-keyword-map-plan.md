# Layer 3 · Day 3 主库打分 + Tier 分档方案

**日期**：2026-04-29
**讨论方**：小刀老师 + Agent B
**状态**：草案 v1（讨论中）
**前置依赖**：L2 v2 已交付（5 文件）

---

## 0 · 你的决策（输入）

| # | 决策 | 选择 |
|---|---|---|
| 1 | L3 范围 | **1b** · 仅打分 + 分档 + Cluster 雏形粗分 |
| 2 | Priority 公式 | **2b** · v4 中（6 维度，13 分制）|
| 3 | Tier 切法 | **3b** · 4 档（Tier 0+1+2+3）+ 单独 Tier-E |
| 4 | EXPLORATORY 处理 | **4a** · 单独 Tier-E |
| 5 | 输出文件 | **5a** · 单文件 04-keyword-map.md |

---

## 1 · L3 边界（不越界）

按 L0 §7 验证粒度分层：

| 越界 | 谁做 |
|---|---|
| ❌ 重新做存在性验证 | L2 已做 |
| ❌ 量化验证（Volume + yoy）| L4 |
| ❌ 精确 KD | L7 |
| ❌ Pillar 主题聚类（精细）| L5 |
| ❌ 选博客大纲 | L6 |

**L3 只做 5 件事**：
1. 跨来源最终去重 + 元数据完整化
2. 应用 6 维度 Priority 公式打分
3. Tier 0/1/2/3 分档 + Tier-E 单独
4. EXPLORATORY 词分类处理（暂入 Tier-E，等 L4）
5. **Cluster 雏形粗分**（L5 正式做，L3 做粗骨架）

---

## 2 · 当天目标

| 维度 | 目标 |
|---|---|
| 输入词数 | ~500（L2 主库 v0）+ ~10-15（EXPLORATORY）|
| 输出 Tier 0 | 5-10 词（博客必选）|
| 输出 Tier 1 | 30-50 词 |
| 输出 Tier 2 | 100-150 词 |
| 输出 Tier 3 | 100-200 词 |
| 输出 Tier-E | 10-15 词（EXPLORATORY 单独）|
| 砍 | 50-100 词（进负向词库）|
| 工期 | ~3 hr 净执行 |

---

## 3 · 当天动作（5 步）

### Step 1 · 元数据完整化 + 跨来源最终去重（30 min）

#### 1.1 跨文件合并
- `02-expanded-keywords.md` 主库 v0（500 词）
- `02.5-pool-b-updated.md` 不进主库的（如果 L4 后回头补）—— 不参与 L3 打分
- 仅以 02 的 500 词 + L1 EXPLORATORY 的 7-15 词 = ~510-515 词为 L3 输入

#### 1.2 元数据补全
每词必有：
- 关键词
- 来源（L1 Pool / Pool 升级 / L2 派生渠道 / 竞品反查）
- Intent（info / compare / buy）
- ICP 对接（L1 Step 2 反推 ICP 之一）
- 产品对接（agent / team / skill ID）
- 渠道签证清单（哪些 L2 渠道出现：PAA / Related / Suggest / KE / Trends / YouTube / Bing-DDG）
- 竞品状态（gap-new / gap-overlap / duplicate / 未知）
- EXPLORATORY 标记（是 / 否）
- Reddit_Evidence URL（如有）

#### 1.3 终极去重
- lower-case + 去标点 + 去多余空格后比对
- 同一词跨来源出现 → 合并所有来源信号
- 输出去重后清单（约 500-510 词）

### Step 2 · 应用 6 维度 Priority 公式打分（1 hr）

#### 2.1 Priority 公式

```
Priority_v4_中 (0-13) =
    Info_intent_bonus      (0|1)  × 2.0
  + Product_Match          (0-3)  × 1.5
  + Reddit_Evidence        (0|1)  × 2.0
  + Specificity            (0-2)  × 1.0
  + Existence_strength     (0-3)  × 0.5
  + Competitor_signal      (-2~1) × 1.0
```

#### 2.2 打分实施

**自动打分**（4 个维度，脚本可计算）：
| 维度 | 自动规则 |
|---|---|
| Info_intent | 标题正则匹配 how/why/what/when/which/? → 1，否则 0 |
| Specificity | 词数：≤2 → 0；3-5 → 1；6+ → 2 |
| Existence_strength | 数渠道签证清单长度 → 0/1/2/3 |
| Competitor_signal | 取 02.5-competitor-keywords.csv 的 type 字段 |

**人工 + Haiku 4.5 辅助**（2 个维度，需语义判断）：
| 维度 | Haiku 提示模板 |
|---|---|
| Product_Match | "对每词判断 YOLOX 产品对接强度（0-3）。参考 manifest agents/skills 类目..." |
| Reddit_Evidence | 检查 Reddit_Evidence URL 字段是否非空 → 1/0（脚本即可）|

注：Reddit_Evidence 实际可全自动（看字段是否有 URL）；Product_Match 才需 Haiku。

#### 2.3 输出
- 每词的 6 维度分 + 总分 Priority（保留 1 位小数）
- 落 `/tmp/round2-day3-priority-scores.csv`

### Step 3 · Tier 分档（30 min）

#### 3.1 Tier 阈值（13 分制）

| Tier | 分数 | 含义 | 预期数量 |
|---|---|---|---|
| **Tier 0** | 10-13 | 顶 5-10 词，下周博客必选 | 5-10 |
| Tier 1 | 7.5-9.9 | 博客强候选 | 30-50 |
| Tier 2 | 4.5-7.4 | 下周-下下周 | 100-150 |
| Tier 3 | 1-4.4 | 月度储备 | 100-200 |
| 砍 | <1 | 进 07-negative-keywords v3 | 50-100 |

#### 3.2 EXPLORATORY 单独 Tier-E
- 不进 Priority 打分（Reddit_Evidence 通常 0，分不公允）
- 列入 Tier-E（10-15 个）
- 标"等 L4 GAKP 验证"
- L4 后回头：有量 → 重新打分入正常 Tier；无量 → 砍或 watchlist

#### 3.3 边界检查
- Tier 0 词数过多（>10）→ 提高阈值到 11
- Tier 0 词数过少（<3）→ 降阈值到 9
- 极端分布异常 → 暂停回 Step 2 检查打分逻辑

### Step 4 · Cluster 雏形粗分（45 min · L5 正式做，L3 做骨架）

#### 4.1 自动聚类（脚本）
- 按 ICP + Intent 双维度分组
- 同 ICP 同 Intent 的词归一组
- 每组词数统计

例：`indie SaaS founder + info` 一组、`Shopify owner + compare` 另一组...

#### 4.2 人工调整
- 跨 ICP 但语义高相关的词合并
- 单 ICP 词数 <3 的归"杂项"
- 输出粗 Cluster 列表（预计 15-25 个 Cluster 雏形）

#### 4.3 标注每词所属 Cluster
- 每词标 Cluster 编号（C1 / C2 / ... / C25）
- L5 正式做时基于这粗骨架细化

### Step 5 · 主库 v1 整理 + 落盘（30 min）

#### 5.1 字段表结构

| # | 关键词 | Tier | Priority | Info | Product | Reddit | Spec | Exist | Comp | Intent | ICP | 产品对接 | Cluster | 渠道签证 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | how to do pSEO as SaaS founder | 0 | 12.0 | 1×2 | 3×1.5 | 1×2 | 2 | 3×0.5 | 1 | info | indie SaaS | Stella · pSEO | C2 | PAA+KE+Reddit | 顶级词 |
| 2 | what is programmatic SEO | 1 | 9.0 | 1×2 | 3×1.5 | 0 | 1 | 2×0.5 | 1 | info | indie SaaS | Stella | C2 | PAA+KE | — |
| 3 | n8n alternative for AI agents | 1 | 7.5 | 0 | 3×1.5 | 0 | 2 | 2×0.5 | 1 | compare | indie SaaS | Multi-team | C7 | KE | — |
| 4 | Zapier alternative | 砍 | 0.0 | 0 | 1×1.5 | 0 | 0 | 1×0.5 | -2 | compare | — | — | — | KE | duplicate |
| 5 | agent2agent protocol | E | — | — | — | — | — | — | — | info | growth marketer | — | C-E1 | HN+Anthropic | EXPLORATORY |

#### 5.2 末尾汇总段
- 总词数 + 各 Tier 分布（实际 vs 预期）
- 6 维度分均值 / 中位数 / 最高 / 最低
- Cluster 雏形数 + 每 Cluster 词数分布
- EXPLORATORY 词 → Tier-E 数量
- 砍词 → 07 增量数量
- L4 倒计时（Ahrefs trial expiry）

---

## 4 · 当天交付物

| 文件 | 内容 |
|---|---|
| `04-keyword-map.md` | 主库 v1 · 单文件 · 含 Tier 0/1/2/3/E + Cluster 雏形 |
| `07-negative-keywords-v3.md` | 含 L3 砍词增量（duplicate 类 + Priority<1）|
| `/tmp/round2-day3-priority-scores.csv` | 中间产物 · Priority 计算明细 |

---

## 5 · 当天规避动作（11 坑映射）

| 坑 | 规避 | 在哪 Step |
|---|---|---|
| **6.1 验证递归循环** | L3 不重做 L2 存在性验证；不抢 L4 量化；不抢 L5 Pillar | 全 Step |
| 6.5 内部 Agent 人名 | （L2 已规避，L3 抽样复查 5%）| Step 1 抽查 |
| **6.9 Pillar 拍脑袋** | Cluster 雏形仅"按 ICP+Intent 自动 + 调整"，不锁 Pillar（L5 才做）| Step 4 |
| 6.11 Handoff stale | L3 启动前 `git status` | 启动前 |
| 新 · Tier 阈值僵化 | Step 3.3 边界检查 + 必要时调阈值 | Step 3.3 |
| 新 · EXPLORATORY 误打分 | 单独 Tier-E，不进 6 维度公式（Reddit_Evidence 不公允）| Step 3.2 |
| 新 · 元数据缺失 | Step 1.2 强制 9 字段补全，缺失即落 Pool B 不进 L3 打分 | Step 1.2 |

---

## 6 · 当天退出条件

| # | 触发 | 动作 |
|---|---|---|
| E1 | L2 主库 v0 < 250 词 | 暂停回 L2 检查筛选漏斗 |
| E2 | Step 2 打分异常分布（>50% 词分数 <2 或 >10）| 暂停回 Step 2.2 检查公式 |
| E3 | Tier 0 词数 = 0（无顶级词）| 警示但继续；可能需要 L4 后重审 |
| E4 | Tier 1+0 总数 < 30 | 主库可用度低，回 L2 检查 4 标准过严 |
| E5 | Cluster 雏形 < 8 个 | 主题分散度过低，可能需要 L1 ICP 反推 |
| E6 | 元数据缺失 > 10% | 暂停回 Step 1.2 强制补全 |

---

**对齐后下一步**：执行 Step 1（合并 + 元数据）→ Step 2（打分）→ Step 3（Tier 分档）→ 中段对齐 → Step 4（Cluster 雏形）→ Step 5（落盘 04-keyword-map.md）→ 起草 L4 量化验证方案
