# Layer 2 · Day 2 扩词 + 存在性验证方案

**日期**：2026-04-29（v2 修订 2026-04-29）
**讨论方**：小刀老师 + Agent B
**状态**：草案 v2（讨论中）
**前置依赖**：L1 v4 已交付（4 文件）+ Ahrefs trial 注册就绪
**v2 主要变更（vs v1）**：
- L2 重定位：扩词 + **存在性验证**（同步做，不分两个 Step）
- 渠道从仅 PAA → **全 8 个渠道**（D1+D2+D3+E1+E2+F+G+H）
- 扩词分级：**Pool A 深扩 + Pool B 广扫**（Pool C 仅升级路径）
- Step 5 重写为 **4 级筛选漏斗**（应对 ~10000 候选）
- 第 3 级筛选用 **Haiku 4.5 批量过 4 问**（性价比，plan 订阅）

---

## 0 · 你的决策（输入）

| # | 决策 | 选择 |
|---|---|---|
| L2 范围 | **1b** · 扩词 + 竞品反查（全 5 步）|
| Ahrefs trial 时机 | **2a** · L2 提前激活（同 trial 用 L2 + L7 两次）|
| 主库 v0 规模 | **3a** · 300-500 词 |
| 输出文件结构 | **4a** · 单文件 + intent 列 |
| 4 标准重审范围 | **5c** · 仅对 L2 新派生过 |
| 渠道覆盖 | **1b** · 全 8 个 |
| Layer 边界 | **2a** · L2=存在性 / L4=量化 / L7=精确 |
| 扩词分级 | **1b** · A 深 + B 广 |
| Pool B 走的渠道 | **2a** · D2 Related + D3 Suggest |
| 4 级筛选 | **1a** · 同意 |
| 第 3 级 Claude 辅助 | **2a** · Claude 批量过 4 问（具体用 **Haiku 4.5**，plan 订阅）|
| 第 4 级阈值 | **3a** · 4 条全过严格 |
| 渠道并行/串行 | **4a** · 全渠道并行抓后统一筛 |

---

## 1 · 当天目标

| 维度 | 目标 |
|---|---|
| 候选总量（筛前）| ~6000-10500 词 |
| 主库 v0（筛后）| 300-500 词 |
| 来源分布 | Pool A PAA 派生 ~30% / Pool A 其他 7 渠道 ~25% / Pool B 派生 ~15% / 竞品缺口 ~25% / Pool 升级 ~5% |
| Intent 分布（主库 v0）| info ≥ 60% / compare 20-30% / buy 10-15% |
| 工期 | ~9 hr 净执行（之前 v1 是 6 hr，全 8 渠道 + 4 级筛选 +3 hr）|

---

## 2 · 当天动作（5 大 Step）

### Step 1 · Pool 升级（30 min）

不变（同 v1）。
- Pool C → Pool B（约 50-100 词）
- Pool B → Pool A（约 10-20 词）
- 输出：`02.5-pool-updates.md`，新 Pool A 总规模 ~70-80 词

### Step 2 · Pool A 多渠道深扩（4 hr · 8 渠道全做）

#### 2a · D1 · Google PAA 链式 3 层（1.5 hr）
- Pool A 70-80 词 × 3 层
- 主：浏览器手工（最稳）
- 辅：`opencli google search "{词}"` 抓首层 PAA
- 备：[answerthepublic.com](https://answerthepublic.com)
- 输出：~600-1200 长尾候选 标 `PAA-L1/L2/L3`

#### 2b · D2 · Google Related Searches（30 min）
- Pool A 70-80 词，每词搜 Google → 取 SERP 底部"相关搜索"8 个
- 命令：`opencli google search "{词}" --include-related true`
- 输出：~500-600 词 标 `related`

#### 2c · D3 · Google Suggest（30 min）
- Pool A 70-80 词 × Suggest 补全
- 命令：`opencli google suggest "{词}"`
- 多前缀（"how to {词}" / "{词} for" / "{词} vs" 等）
- 输出：~350-700 词 标 `suggest`

#### 2d · E1 · Ahrefs Keywords Explorer · Matching Terms（含在 Step 4 trial）
- 70 词批量导入 KE → "Matching Terms"
- 导出 CSV `/tmp/ahrefs-matching.csv`
- 输出：~1500-2500 词（KE 通常给 30-50 词/种子）

#### 2e · E2 · Ahrefs Keywords Explorer · Questions（含在 Step 4 trial）
- 同样 KE 中筛 "Questions" 标签
- 导出 CSV `/tmp/ahrefs-questions.csv`
- 输出：~500-1000 词（how/what/why 开头）

#### 2f · F · Google Trends Related Queries（20 min）
- Pool A 重点词（top 30）批量进 Trends
- 看 Top + Rising related queries
- 红利信号：rising +900% / +∞
- 输出：~150-300 词 标 `trends-rising` / `trends-top`

#### 2g · G · YouTube Suggest（15 min）
- Pool A 70 词 × YouTube 搜索框 suggest
- 命令：`opencli youtube suggest "{词}"`（如支持）或浏览器
- 输出：~200-350 词 标 `youtube`

#### 2h · H · Bing/DDG Suggest（15 min）
- Pool A 70 词 × Bing/DDG 补全
- 输出：~200-350 词 标 `bing-ddg`

**Step 2 总输出**：~4000-6500 候选词，全部标"已通过存在性验证"

### Step 3 · Pool B 广扫（1 hr · D2 + D3 only）

#### 3a · D2 · Google Related（30 min）
- Pool B 200 词中**与 Pool A 语义邻近**的 100-150 词
- 每词 Related 8 个
- 输出：~800-1200 词

#### 3b · D3 · Google Suggest（30 min）
- 同上 100-150 词
- 多前缀
- 输出：~500-1500 词

**Step 3 总输出**：~1300-2700 词

**注意**：Pool C 不直接扩词——通过 Step 1 升级到 B 后才走 Step 3。

### Step 4 · 竞品反查（2 hr · Ahrefs trial 激活）

不变（同 v1），但**提前**确认 Step 2d/2e 也用同一 trial：

#### 4.1 激活 Ahrefs trial
- https://ahrefs.com/awt → 7-day trial $7
- 记录激活日期 → 计算 expiry = 激活 + 7 天
- ⚠️ 7 天内必须完成：Step 2d/2e Matching/Questions + Step 4 5 站反查 + L7 主库精排

#### 4.2 5 站批量导出 organic keywords
| # | 域名 | 导出 |
|---|---|---|
| 1 | lindy.ai | top 1000 |
| 2 | relevance.ai | top 1000 |
| 3 | zapier.com（filter `/ai/`）| top 1000 |
| 4 | n8n.io | top 1000 |
| 5 | make.com | top 1000 |

输出：`/tmp/ahrefs-{competitor}.csv` × 5

#### 4.3 Python 合并 + 去重 + 标 type
```python
# 5 CSV → 合并 → 标 duplicate / gap-overlap / gap-new / 不相关
```
预期：~3000-5000 unique 词

**Step 4 总输出**：竞品候选词 + 标记，进入 Step 5 筛选漏斗

### Step 5 · 4 级筛选漏斗（2 hr · 关键 Step）

总候选预估：
```
Step 2 Pool A 8 渠道：4000-6500
Step 3 Pool B 2 渠道：1300-2700
Step 4 竞品 5 站：3000-5000
合计：~8300-14200
```

#### 5.1 第 1 级 · 机械去重 + 字符清洗（5 min · Python 脚本）
**自动**：
- 跨来源去重（lower-case + 去标点 + 去多余空格）
- 长度过滤（3-100 字符）
- 停用词砍（仅 "the / a / and / or / of" 单词）
- 维护 Pool 标签（A 派生 / B 派生 / 竞品 / 升级）

预期：~10000 → ~5000 通过

#### 5.2 第 2 级 · 自动质量信号（10 min · 半自动脚本）
**自动**：
- **人名黑名单**：`messages/en.json` 15 hero 人名（Sophie/Elias/Stella/...）含一律砍 → 坑 6.5
- **负向词黑名单**：`archive/round-1/07-negative-keywords.md` 117 词 + Step 4 新增 duplicate
- **Ahrefs CSV** Volume=0 且 KD>30 → 标弱（不主库，留 watchlist）
- **SERP 巨头垄断**（前 10 全 Wikipedia/Forbes/Google/YouTube）→ 砍

预期：5000 → ~3000 通过

#### 5.3 第 3 级 · 4 问语义筛（1 hr · Haiku 4.5 批量）

**工具选择**：用 **Haiku 4.5**（性价比，plan 订阅），不用 Opus 4.7

**批量提示模板**：
```
对以下 50 个候选关键词逐个回答 4 个 yes/no 问题:

Q1. 是真实求解（不是吐槽 / 故事 / 公告）?
Q2. 痛点能被 YOLOX agent / skill 解决?（参考 manifest 类目）
Q3. 标题能直接或简单转换成搜索词?
Q4. ICP 是 L1 反推清单内的?

输入候选清单：
1. {词1} | 来源: {来源} | 上下文: {如有}
2. ...
50. ...

参考资料：
- YOLOX manifest 类目摘要：{Step 1 输出}
- ICP 清单：{L1 Step 2 输出}

输出 CSV: 词, Q1, Q2, Q3, Q4, 备注
```

**通过门**：
- 4 yes → 进 Pool A 候选（进入第 4 级）
- ≥3 yes → 进 Pool B
- <3 yes → 留 Pool C（不丢弃）

预期：3000 → ~1500 进 Pool A/B

#### 5.4 第 4 级 · 4 标准（30 min · 人工 + Haiku 辅助 · 仅进主库前）

仅对 1500 高质量 Pool A/B 词跑：

| 标准 | 检查 |
|---|---|
| 1. 产品能答 | manifest 双向验证（agent_id / skill_id 匹配）|
| 2. ICP 真在搜 | 来源链接 OR opencli suggest hit |
| 3. 能扩 5+ 长尾 | 看 Step 2/3 派生数 ≥ 5 |
| 4. 可挂 Cluster | 看主题接近词数 ≥ 4 |

**通过门**：4 条全过（决策 3a 严格）→ 主库 v0
**部分过**（≥2 条）→ 留 Pool B 备用
**全不过** → 砍

预期：1500 → ~500 主库 v0 ✅

#### 5.5 主库 v0 整理 + 落盘
- 跨来源去重
- Intent 标注（info / compare / buy）
- 字段完整性检查
- 输出 `02-expanded-keywords.md`

---

## 3 · 当天交付物（5 文件）

| 文件 | 内容 | 数量 |
|---|---|---|
| `02-expanded-keywords.md` | 主库 v0 · 单文件 + intent 列 | 300-500 |
| `02.5-pool-updates.md` | Step 1 升级清单 | 50-120 |
| `02.5-pool-b-updated.md` | Pool B 增量（第 3/4 级筛选不全过的）| ~1000 |
| `02.5-competitor-keywords.csv` | 5 站合并 + 标 type | ~3000-5000 |
| `07-negative-keywords-v2.md` | 含 Step 4 重复词 + 第 2 级 SERP 巨头垄断 | +50-100 |

**字段表结构**（02-expanded-keywords.md）：

| # | 关键词 | 来源 | 渠道 | Intent | 父种子 | ICP | 产品对接 | 4 标准 | 池 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | how to do programmatic SEO | Pool A | (L1 已过) | info | — | indie SaaS | Stella · pSEO Builder | (L1) | A | 沿用 L1 |
| 2 | what is programmatic SEO | A 深扩 | PAA-L1 | info | how to do programmatic SEO | indie SaaS | Stella | ✅✅✅✅ | A | PAA 派生 |
| 3 | programmatic SEO vs traditional | A 深扩 | PAA-L2 | compare | how to do programmatic SEO | indie SaaS | — | ✅✅✅❌ | B | 不能扩 5 长尾 |
| 4 | n8n alternative for AI agents | 竞品 gap-new | Ahrefs | compare | n8n.io | indie SaaS | Multi-agent team | ✅✅✅✅ | A | KD 18 / Vol 320 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**末尾汇总段**：
- 总词数（实际数）+ 各来源占比 + Intent 分布
- Pool A 净增（vs L1 63 词）
- 4 级漏斗各级通过率
- 竞品反查 type 分布
- Ahrefs trial 激活/失效日期 + L7 倒计时
- 含人名陷阱词：0
- 8 渠道实际数据量统计

---

## 4 · 当天规避动作（11 坑映射 · v2）

| 坑 | v2 规避 | 在哪 Step |
|---|---|---|
| **6.1 验证递归循环** | L2 只做存在性验证（PAA/KE 出现），不做量化（GAKP 是 L4）| 全 Step |
| **6.2 Claude 12.5%** | 全程禁用 Claude 凭空扩；用 8 渠道 + 4 级筛 | 全 Step |
| 6.3 Reddit show-off 陷阱 | （L1 已规避）| — |
| 6.4 Reddit 1/1 孤例 | Pool 升级时考虑互动 | Step 1 |
| **6.5 内部 Agent 人名** | **第 2 级自动黑名单 + Step 5.5 终检** | Step 5.2 + 5.5 |
| 6.6 GAKP Forecast/Historical | 不涉及（L4 才用）| — |
| **6.10 yoy +∞ 真信号** | F · Trends Rising 主动找 +∞ | Step 2f |
| **6.11 Handoff stale** | L2 启动前 `git status` + 验证 `feat/seo-keyword-research` | 启动前 |
| 新 · Ahrefs trial 倒计时 | S4 激活后立即标 expiry，覆盖 Step 2d/2e + Step 4 + L7 | Step 4.1 |
| 新 · PAA 抓取被 Google 频率限制 | 切人工 + AnswerThePublic | Step 2a |
| 新 · CSV 编码 | Ahrefs 通常 UTF-8，验证后必要时 iconv | Step 4 |
| 新 · 候选量爆炸（~10000）| 4 级筛选漏斗自动化前 2 级 | Step 5 |
| 新 · Haiku 批量误判 | 第 4 级人工复审 ≥3 yes 的边缘词 | Step 5.4 |

---

## 5 · 当天退出条件

| # | 触发 | 动作 |
|---|---|---|
| E1 | Ahrefs trial 注册失败 / paywall 卡死 | 跳过 S2d/2e + S4，剩余继续，L7 重启 |
| E2 | PAA 抓取被 Google 频率限制 | 切人工 + AnswerThePublic 补 |
| E3 | 候选总量 < 5000 | 抓取深度可能不够，回 Step 2 加抓 |
| E4 | 第 1 级机械筛通过率 < 30% | 异常重复，回 Step 2 检查渠道是否冗余 |
| E5 | 第 3 级 Haiku 4 问通过率 < 30% | 候选质量太差，可能 Pool A 选错，回 L1 重审 |
| E6 | 主库 v0 < 250 词 | 暂停回 L1 检查 Pool 是否需要扩 |
| E7 | 第 4 级 4 标准全过率 < 25% | 暂停 Step 5.5，回 Step 2/3 重新审来源 |
| E8 | 竞品反查 duplicate 比例 > 30% | 我们的种子被 4 站锁太多，提示 L1 ICP/领域选择需重审 |
| E9 | Ahrefs CSV 字段格式异常 | 跳过该域名，剩余 4 站继续 |

---

**对齐后下一步**：执行 Step 1（Pool 升级）→ Step 2 8 渠道 + Step 3 Pool B 广扫并行 → 中段对齐 → Step 4 竞品反查（同时跑 Step 2d/2e）→ Step 5 4 级筛选漏斗 → 交付 5 文件 → 起草 L3 主库打分方案
