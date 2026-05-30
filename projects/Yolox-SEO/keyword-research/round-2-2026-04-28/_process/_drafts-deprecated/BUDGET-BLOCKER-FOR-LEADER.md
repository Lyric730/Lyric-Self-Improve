# YOLOX SEO Round-2 · 付费工具卡点决策请示

**日期**：2026-05-04
**讨论方**：小刀老师 + Agent B → 提交 Leader
**状态**：决策请示 v1（待 Leader 拍板）
**前置依赖**：L1 已完成（4 文件 final · commit `19c300c`）/ L2 Step 1-3 完成

---

## 0 · TL;DR（30 秒读完）

**目标**：本周完成 L2 关键词扩词 + 验证 → 300-500 词主库 v0 → 驱动 6 篇博客大纲。

**卡点**：扩词 + 验证 KD/Volume 必须用专业 SEO 工具，但当前所有"低价 trial"选项都失败——
- Ahrefs **$7 / 7-day trial 在 2026 年已废止**（plan 文档引用了过时信息，需修正）
- Ahrefs Starter $29/月 **无 export 功能**（致命 dealbreaker）
- Semrush Pro Trial 已激活但 **export 月限 3 次**（不够任何工作量）

**4 个可行选项**（详见 §3）：
- **A · DataForSEO API ~$25-40 一次性**（推荐 · 达原目标）
- B · Mangools KWFinder $29.9 + 10-day money-back（中等 · 退款风险）
- C · Ahrefs Lite $129/月（贵但稳）
- D · 缩水目标用免费数据 · 0 成本（主库 v0 100-200 词，原目标 300-500）

**需 Leader 拍板**：批 $25-130 budget 或接受目标缩水。

---

## 1 · 项目背景（已完成的工作）

| 阶段 | 交付 | 规模 |
|---|---|---|
| L1 Step 1-3 | 25 ICP × 53 Reddit sub × 4 渠道映射 | — |
| L1 Step 4 | Reddit 抓取 3572 帖 + Quora 80 + IH 50 → 三层池筛 | Pool A 46 / B 91 / C 903 |
| L1 Step 5 | 产品语义补缺 14 词（manifest 反推 + Google Suggest 验证）| +13 词进 Pool A |
| L1 Step 6 | 8 渠道新兴生态扫描 → EXPLORATORY 双源验证 | +7 词进 Pool A |
| L1 Step 7 | 跨 Step 去重 + 4 文件 final | Pool A 66 词 |
| L2 Step 1 | Pool 升级（B→A 10 / C→B 78）| Pool A 76 / B 169 |
| L2 Step 2 | 4 个安全渠道（Google/YouTube/Bing/DDG Suggest）| 1890 候选词 |
| L2 Step 3 | Pool B 广扫 D3 Suggest | 27 候选（数据稀薄但已尝试）|

**已投入工时**：~30+ hr 净执行（含 plan 设计 + 实际抓取 + 三层池筛选 + 8 渠道交叉验证）

**已规避的 11 个第 1 轮坑**：6.2 Claude 12.5% / 6.3 show-off 帖 / 6.4 1/1 孤例 / 6.5 内部人名 / 6.10 yoy +∞ / 6.11 Handoff stale / 等。

---

## 2 · 卡点本质：付费工具 vs 目标的矛盾

### 2.1 为什么需要付费工具

L2 阶段必须做的 2 件事**只能**靠 Ahrefs / Semrush 类工具完成：

| 任务 | 用途 | 免费替代是否可行 |
|---|---|---|
| **扩词主力**（76 seed → ~3000-5000 候选）| Keyword Magic Tool / Keywords Explorer Matching | ❌ Google Suggest 公开 API 仅给 prefix autocomplete 10-15 词，深度不够 |
| **竞品反查**（5 站 organic keywords top 1000）| Site Explorer / Domain Overview | ❌ 无免费替代 · Google 不公开域名 organic keyword 数据 |
| **KD/Volume 验证**（76 词 + 主库 v0 500 词）| Keywords Explorer / Overview | 🟡 GAKP 给 Volume 区间 + 27 月历史，但**无 KD**（关键词难度）|

→ 没付费工具 = L2 主库 v0 300-500 词目标无法达成。

### 2.2 付费工具选项验证（2026-05-04 实测）

| 工具 | 价格 | Export | Historical | 致命缺陷 |
|---|---|---|---|---|
| **Ahrefs $7 / 7-day Trial** | ~~$7~~ | — | — | ❌ **2026 年已废止**（ahrefs.com/pricing 原文："We never run discounts"）|
| **Ahrefs Starter** | $29/月 | **NONE** | 1 month | ❌ 无 export，单月仅 250 rows/report |
| **Ahrefs Lite** | $129/月 | 500K rows/月 | 6 months | ✅ 能用但贵 |
| **Semrush Pro Trial** | $0（绑卡 7 天）| ⚠️ **月限 3 次** | 26 months | ❌ 3 次 export 不够 5 站 + 多 seed 工作 |
| **Semrush Pro** | $139.95/月 | 高限额 | 26 months | ✅ 能用但贵 |

**Source**：
- [Ahrefs Pricing](https://ahrefs.com/pricing) - "We never run discounts. But if you're a website owner, you can sign up for Ahrefs Free..."
- [Ahrefs Starter Plan official help](https://help.ahrefs.com/en/articles/9419051-about-ahrefs-starter-plan)
- Semrush Pro Trial 实测（小刀老师 2026-05-02 激活，2026-05-04 验证 export 限额）

---

## 3 · 4 个可行选项 · 利弊对比

| 选项 | 成本 | 操作时间 | 数据质量 | 主库 v0 预期 | 风险 |
|---|---|---|---|---|---|
| **A · DataForSEO API** | $25-40 一次性 | 1-2 天（注册 + 我代调）| 中-高（行业 70-80% Ahrefs 水平）| **300-500 词**（达原目标）| 🟡 需注册 + 充值 + 给我 API key |
| B · Mangools KWFinder | $29.9 / 月 + 10-day money-back | 立即 | 中（70% Ahrefs 水平）| 300-500 词 | 🔑 10 天内忘 cancel → $29.9 被扣 |
| C · Ahrefs Lite | **$129/月**（一次性）| 立即 | 高（行业最高）| 300-500 词 | 单次性价比差 vs A |
| D · 缩水目标 + 用现有 1890 词 | **$0** | 今天即可 | 低（无 KD / Volume）| **100-200 词**（缩 60%）| ⚠️ Tier 分档不准 · L4 仍需付费工具补 |

### 3.1 选项 A · DataForSEO API（推荐）

**做法**：
- 你（Leader）批准 budget $25-40
- 小刀老师注册 dataforseo.com + 充值 $25 + 给我 API key
- 我写脚本调 API：
  - 76 词扩词（Search Volume API + Keyword Suggestions API）
  - 5 站 organic keywords（Domain Analytics API）
  - 主库 v0 验证（KD + Volume + Intent）
- 输出 CSV → 走 Step 5 4 级筛漏斗 → 主库 v0 300-500 词

**为什么推荐**：
- ✅ 我直接 control（不依赖小刀老师 web UI 操作）
- ✅ 没 export 限额
- ✅ 单次成本最低
- ✅ Round-2 完成后无续费风险

**风险**：
- 数据精度 70-80% Ahrefs（足够 Tier 分档 + 趋势判断，不影响主库决策）
- DataForSEO 是 B2B API，新手注册 + 充值流程稍复杂（10-20 min）

### 3.2 选项 B · Mangools KWFinder

- $29.9 月费 + 10 天内 cancel 退全款
- ⚠️ Cancel 流程容易忘——多次行业反馈"忘 cancel 被扣"
- 数据精度中等
- **小刀老师另需要管 cancel 倒计时**（额外认知负担）

### 3.3 选项 C · Ahrefs Lite $129

- 行业最高数据精度
- 单次性价比差（$129 vs A $25-40 完成同样工作）
- 唯一优势：**永久订阅可用**——如果未来 Round-3/4 还要做 SEO，$129/月持续用更划算
- 当前 Round-2 范围内：浪费

### 3.4 选项 D · 缩水目标 · 0 成本

**接受现状的代价**：
- 主库 v0 缩到 100-200 词（vs 原 300-500）
- 6 篇博客大纲缩到 3-4 篇
- L4 阶段（KD/Volume Tier 分档）仍需要付费工具补 → 决策推迟到那时
- ⚠️ 实质上 = "**把 budget 决策推迟 2 周**"，最终还是要花钱

---

## 4 · 我的推荐

### 优先级排序

| 排序 | 选项 | 理由 |
|---|---|---|
| **1** | **A · DataForSEO API $25-40** | ROI 最高 · 一次性投入 · 达原目标 · 我可代操作 |
| 2 | D · 缩水现有 1890 词 | 0 成本 · 但只是把决策推到 L4 阶段 |
| 3 | C · Ahrefs Lite $129 | 数据最佳 · 但单次性价比差 |
| 4 | B · Mangools | cancel 风险高 · 不推荐 |

### Trade-off 框架

| 关注点 | 推 A | 推 D |
|---|---|---|
| 现金流紧 | ❌ | ✅ |
| 时间紧（本周必须出主库 v0）| ✅ | ❌ |
| 数据精度要求高 | ✅ | ❌ |
| 接受目标缩水 50-60% | ❌ | ✅ |

---

## 5 · Leader 决策点

请 Leader 在以下 3 个问题选项中拍板：

1. **是否批 budget**：
   - [ ] 批 $25-40（走选项 A）
   - [ ] 批 $129（走选项 C）
   - [ ] 不批（走选项 D · 缩水目标）

2. **目标调整**：
   - [ ] 维持原目标（主库 v0 300-500 词 / 6 篇博客）
   - [ ] 接受缩水（主库 100-200 词 / 3-4 篇博客）

3. **后续路径**：
   - [ ] 一次性付费 + Round-2 完成后取消
   - [ ] 永久订阅（如 Ahrefs Lite 月费）支持未来多轮 SEO 工作

---

## 6 · 错误复盘 + 修正承诺

### 错误源

`docs/seo/keyword-research/METHODOLOGY.md` v1.1 §7 引用了 **"Ahrefs Trial · $7 · 7 天 · 一次性批量查 200 词 KD + Volume"**——这是 Round-1 沿用的**过时信息**。

Round-2 plan 文档（HANDOFF.md / L0 / L2 / L7）全部基于此 budget 假设。

2026-05-04 实测发现：Ahrefs 当前已无 $7 trial 选项（pricing 页明确 "We never run discounts"）。

### 影响

- L2 budget 假设全部需要重审
- METHODOLOGY v1.1 → v1.2 修正
- HANDOFF / L2 plan 注明此变更

### 修正动作（待 Leader 决策后执行）

无论 Leader 选 A/B/C/D，在 L7 整理阶段都会：
- METHODOLOGY v1.2 修正 §7 工具栈表
- 添加"工具 budget 验证 SOP"（每轮调研启动前实测当前 trial / pricing）
- HANDOFF v2 更新到下一轮

---

## 7 · 时间线 · Leader 决策后

### 如果选 A（DataForSEO）

```
Day 1（你/小刀）：注册 + 充值 + 给 API key
Day 1-2（Agent B）：写 API 调用脚本 + 跑 76 词扩词 + 5 站 organic
Day 2（Agent B）：Step 5 4 级筛漏斗 → 主库 v0
Day 3（Agent B）：L3 6 维度打分（plan 不变）
Day 4-5（Agent B）：L4 量化验证 + L5 Pillar/Cluster
Day 6-7（Agent B）：L6 博客大纲 + L7 落库
```

### 如果选 D（缩水）

```
Day 1（Agent B）：用 Step 2 已有 1890 词 + Pool A 76 直接进 Step 5
Day 2（Agent B）：Step 5 简化筛漏斗（无 KD/Volume，仅按 ICP × Reddit 互动信号筛）→ 主库 v0 100-200 词
Day 3（Agent B）：L3 简化打分
Day 4-7（Agent B）：L4 阶段重新评估是否需付费工具补充
```

---

## 8 · 附录：当前完成度数据

### 三层池规模（已 commit `19c300c`）

```
Pool A · 66 词（46 ICP + 13 产品语义 + 7 EXPLORATORY）
Pool B · 91 词（Layer 2 真 4 问筛后）
Pool C · 903 帖（去重后机械筛通过）
Watchlist · 7 词（3 双源降级 + 4 单源新兴）
```

### Step 2 安全渠道产出

```
Google Suggest 241 / YouTube Suggest 240 / Bing Suggest 880 / DuckDuckGo Suggest 529
合计 1890 候选词（来自 Pool A 76 词 × 4 渠道）
```

### Step 4 / Step 5 待付费工具

- Step 4：5 站竞品 organic keywords（cassidyai.com / lindy.ai / ema.co / cognosys.ai / beam.ai）
- Step 5：4 级筛漏斗（机械去重 + Volume/KD 砍 + 4 问语义筛 + 4 标准）

---

**联系**：小刀老师（liuyouxuan570@gmail.com）+ Agent B（Claude Opus 4.7 · feat/seo-keyword-research worktree）
**所有数据可追溯**：commit `19c300c` + `~/tools/opencli-raw/round2-day1-*.json`（144 raw files）

---

**等 Leader 在 §5 三个决策点拍板**。
