# Layer 7 · Day 7 落库 + Ahrefs 精排 + Handoff 方案

**日期**：2026-04-29
**讨论方**：小刀老师 + Agent B
**状态**：草案 v1（讨论中）
**前置依赖**：L6 v1 已交付（08-blog-outlines.md · 6 篇 1.5 页大纲）

---

## 0 · 你的决策（输入）

| # | 决策 | 选择 |
|---|---|---|
| L7.1 | Ahrefs 精排范围 | **b** · Tier 0+1+2（~230 词）|
| L7.2 | 精排后重打分 | **b** · v4_扩展 + KD 维度（17 分制）|
| L7.3 | 飞书 CSV 字段 | **b** · 核心 10-15 列 |
| L7.4 | Handoff 内容 | **b** · 标准 4 段 + 写作风格指南 |

---

## 1 · L7 边界（不越界）

按 L0 §7：

| 越界 | 谁做 |
|---|---|
| ❌ 写博客内容 | 下周 Day 8+ |
| ❌ Schema 实施 | L8 实现层 |
| ❌ 重新做扩词 | 月度刷新做 |
| ❌ 上线监控 | L9（如有）|

**L7 只做**：
1. Ahrefs Bulk lookup 第 2 次 · 拿精确 KD + Volume（~230 词）
2. 主库 v2 → v3：v4_扩展 + KD 维度（17 分制）重打分
3. 飞书 CSV 导入指南（核心 10-15 字段）
4. 写作风格指南（每 Pillar 1 段）
5. 标准 handoff（进度 / 红线 / 工具 / 下一步）

---

## 2 · 当天目标

| 维度 | 目标 |
|---|---|
| Ahrefs 精排词数 | ~230（Tier 0+1+2）|
| 主库 v3 总分制 | 17 分（v4_扩展 16 + KD_modifier ±1）|
| 飞书 CSV 字段 | 12-15 核心列 |
| 写作风格指南 | 3 Pillar × 1 段 = 3 段 |
| Handoff 4 段 | 进度 / 红线 / 工具 / 下一步 |
| 工期 | ~3 hr 净执行 |

---

## 3 · 当天动作（6 步）

### Step 1 · Ahrefs Bulk lookup 第 2 次（30 min · 决策 L7.1b）

#### 1.1 词单准备
- 主库 v2 中 Tier 0 + Tier 1 + Tier 2 = ~5 + 40 + 130 = ~175 词
- 加 6 篇博客大纲的核心词 + 长尾词 ~50 词
- 加 yoy 红利清单 ~10 词
- 总 ~230 词

#### 1.2 trial expiry 检查
- L2 激活日期 + 7 = 失效日期
- L7 必须在 expiry 前完成
- 如已过期 → E1 退出条件（重激活 $7）

#### 1.3 Ahrefs 操作
1. Keywords Explorer → Bulk Analysis
2. 粘 230 词 → Run
3. 导出 CSV：`/tmp/ahrefs-final-precision.csv`
4. 字段：keyword / Volume（精确数）/ KD / CPC / Top SERP

#### 1.4 编码处理
- Ahrefs 通常 UTF-8（验证 `head -3`）
- 如 UTF-16 → iconv 转

### Step 2 · KD_modifier 计算（15 min）

#### 2.1 KD_modifier 评分表

| KD 区间 | 含义 | KD_modifier |
|---|---|---|
| ≤ 10 | 极易（新站可挤）| **+1** |
| 10-30 | 中易 | +0.5 |
| 30-50 | 中等 | 0 |
| 50-70 | 中难 | -0.5 |
| > 70 | 极难（巨头垄断）| **-1** |

#### 2.2 应用
- 230 词每个计算 KD_modifier
- 主库 v2 中未精排的 270 词 KD_modifier = 0（默认中等）
- 输出 `/tmp/kd-modifiers.csv`

### Step 3 · 主库 v3 重打分 + Tier 升级（30 min · 决策 L7.2b）

#### 3.1 v4_最终 公式（17 分制）

```
Priority_v4_最终 (-3.5 ~ 17.5) =
    [v4_扩展 6 维度，13 分] +
    Volume_score      × 1.0   = 0~3
  + yoy_modifier              = -0.5~+0.5
  + KD_modifier               = -1~+1     ← L7 新增
                              ─────────
                              -3.5 ~ 17.5
                              实际 5-14
```

#### 3.2 Tier 阈值（17 分制 · 重切）

| Tier | 旧（16 分）| 新（17 分） | 数量预期 |
|---|---|---|---|
| Tier 0 | 12-16 | **13-17** | 5-10 |
| Tier 1 | 9-11.9 | **10-12.9** | 30-50 |
| Tier 2 | 5.5-8.9 | **6-9.9** | 100-150 |
| Tier 3 | 1-5.4 | **1-5.9** | 100-200 |
| 砍 | <1 | <1 | +死词 |

#### 3.3 重新分档 + 输出
- 230 精排词重打分 → 重新分 Tier
- 270 未精排词 KD_modifier=0 → 微调 Tier
- 输出 `04-keyword-map-v3.md` 主库终版

#### 3.4 边界检查
- Tier 0 数量从 v2 的 5-10 变到 v3 的多/少 → 调阈值
- KD ≤ 10 的词 + 高 Priority → 标 `LOW-KD-OPPORTUNITY`（新站重点）

### Step 4 · 飞书 CSV 导入（30 min · 决策 L7.3b · 核心 12-15 字段）

#### 4.1 飞书 CSV 字段表

| # | 飞书列名 | 来源字段 | 类型 |
|---|---|---|---|
| 1 | 关键词 | keyword | 文本 |
| 2 | Tier | tier | 单选（0/1/2/3/E）|
| 3 | Priority | priority_v4_final | 数字 |
| 4 | Volume | volume_max（双源 max）| 数字 |
| 5 | KD | kd | 数字（精排）|
| 6 | yoy | yoy | 文本（+∞ / +900% / -100% 等）|
| 7 | Intent | intent | 单选（info/compare/buy）|
| 8 | ICP | icp | 文本（多 ICP 用 / 分隔）|
| 9 | 产品对接 | product_match | 文本（agent/skill/team 名）|
| 10 | Cluster | cluster_id | 文本（C1.1 等）|
| 11 | Pillar | pillar | 单选（P1/P2/P3）|
| 12 | 来源 | source | 文本（L1 ICP / L2 PAA / L4 升级 等）|
| 13 | 标签 | tags | 多选（EXPLORATORY / RISING / DEAD / LOW-KD / ZERO-VOL-SNIPER）|
| 14 | 备注 | notes | 文本 |
| 15 | 落盘日期 | date | 日期 |

#### 4.2 CSV 生成脚本
- Python 脚本：`04-keyword-map-v3.md` → `/tmp/feishu-import.csv`
- 字段对齐 + UTF-8 编码（飞书要求）

#### 4.3 飞书导入指南文档
- 创建 `09-feishu-import.md` 含：
  - 飞书 base 创建步骤（建表 / 字段类型）
  - CSV 导入步骤（飞书 → 数据 → 导入）
  - 字段映射表
  - 排序 / 筛选模板（按 Tier / Pillar / Cluster）
  - 视图建议（Tier 0 视图 / 6 篇博客视图 / yoy 红利视图）

### Step 5 · 写作风格指南（30 min · 决策 L7.4b）

#### 5.1 每 Pillar 1 段风格定调

模板：
```markdown
### Pillar 1: {主词}

**目标 ICP**：{1-2 ICP}
**Pillar 定位**：{主题边界 1 句话}

**写作风格**：
- 语气：{专业 / 教学 / 对话 / 故事 ...}
- 视角：{第二人称"你" / 第三人称客观 / 第一人称"我们"}
- 段落长度：{短 2-3 句 / 中 4-6 句 / 长 7+ 句}
- 数据密度：{高数据驱动 / 中等 / 偏故事性}
- 例子比例：{多 / 中 / 少}
- AEO 友好程度：{TL;DR + FAQ 强化 / 普通 / 弱}
- 转化语气：{硬卖 / 软推 / 教育型不卖}

**避免**：
- {本 Pillar 的常见雷区，如"过度技术化"或"营销味重"}
- {语气不一致情况}

**示范段落**（50 字）：
{1 段 sample，让写作者抓感觉}
```

#### 5.2 3 Pillar 共用规则
- AEO-friendly：TL;DR 3-5 行 + FAQ 5 个
- Reddit 引用风格：直接引用 + 链接
- 内链锚文本：完整语义短语（不要 "click here"）
- 长度：1500-2000 字（Cluster）/ 3000+ 字（Pillar）

### Step 6 · 标准 Handoff 4 段 + 落盘（45 min · 决策 L7.4b）

#### 6.1 `2.3-handoff.md` 文件结构

```markdown
# 第 2 轮关键词调研 · Handoff 给下周（写作启动）

## 1 · 进度
- L0-L7 全部完成
- 主库 v3 终版：~520 词 · 17 分制
- 6 篇博客大纲：08-blog-outlines.md
- 5-3-1 发布计划：见 06-pillar-cluster-map.md §3
- 关键决策（5 项）+ 工作流（每层方案审核）

## 2 · 红线（不能碰）
- 不擅自改 Pillar/Cluster 主词（L5 已锁，要改回 L5）
- 不写 Pool B/C 中的词（仅主库 v3 进入写作）
- 不删 EXPLORATORY 词（等 L4 后续刷新验证）
- 4 选题纪律不破（show-off / 1/1 孤例 / 产品答不上 / 内部人名）
- Ahrefs trial expiry 已过 → 不再用 trial（如需重激活，重启账户 $7）

## 3 · 工具栈
- 当前激活：opencli + GAKP + Ahrefs trial（已过期）
- 下周写作工具：Claude（用 Sonnet/Opus 写博客）+ schema validator
- 飞书 base：09-feishu-import.md

## 4 · 下一步动作（按时间）
- Day 8 周一：写作环境就绪 + 选第 1 篇 Cluster 启动写作
- Day 9-13 周一-周五：每天 1 篇（5 Cluster 完成）
- Week 5 周一：监控 GSC 索引情况
- Week 6：3 Cluster 已索引 → 启动 Pillar 1 写作

## 5 · 写作风格指南
（Step 5 输出 · 3 Pillar × 1 段）

## 6 · 学到了什么 · 11 坑规避升级
- v4 架构关键改进（vs 第 1 轮）：
  - 真实 manifest 拉取（替代营销门面）
  - ICP 反推链（替代 placeholder）
  - 8 渠道扩词 + 4 级筛选漏斗（替代 Claude 凭空 12.5%）
  - Layer 验证粒度分层（L1 来源 / L2 存在性 / L4 量化 / L7 精确）
  - 三层候选词池（Pool A/B/C 不丢词）
  - 17 分制 v4_最终 公式

## 7 · 还不知道的（诚实边界）
- L4 Volume 数据 60-70% 仍 "---"（GAKP + Ahrefs 双源仍有限制）
- 6 篇博客实际写作命中率（GSC 反馈要 6-12 周后）
- yoy 红利词起飞窗口（推断但未验证）

## 8 · 给下次自己的话
- 写博客时遇到"想再调研更多词"→ 停（坑 6.1 验证递归）
- 写博客时遇到"产品好像答不上"→ 立即标 watchlist + 砍此篇（不写空头支票）
- 写完 1 篇 → 立即发 → 看 GSC（不要等 6 篇全写完）
```

#### 6.2 边界
- handoff 文档 ≤ 200 行（精简，避免噪声）
- 重要事实直接列，不长篇大论

---

## 4 · 当天交付物（4 文件）

| 文件 | 内容 |
|---|---|
| `04-keyword-map-v3.md` | 主库 v3 · 终版 · 17 分制 + 重 Tier |
| `09-feishu-import.md` | 飞书 base 导入指南（含 CSV 字段映射）|
| `09-feishu-import.csv` | 飞书直接导入 CSV（核心 12-15 列）|
| `2.3-handoff.md` | 下周写作启动 handoff（含写作风格指南）|

---

## 5 · 当天规避动作（11 坑映射）

| 坑 | 规避 | 在哪 Step |
|---|---|---|
| **6.1 验证递归循环** | L7 是收尾层，不再扩词 / 不再换 Pillar | 全 Step |
| 6.6 GAKP Forecast/Historical | 不涉及（L4 已规避）| — |
| 6.7 UTF-16 LE | Ahrefs 通常 UTF-8 但仍验证 | Step 1.4 |
| 6.8 Volume 区间 | L7 拿到精确 Volume（vs L4 区间）| Step 1 |
| **6.11 Handoff stale** | **handoff 写完立即发 + 用真实状态写**（不写过时信息）| Step 6 |
| 新 · trial 已过期 | E1 退出条件：重激活 $7 或跳过精排 | Step 1.2 |
| 新 · 17 分制 Tier 阈值 | Step 3.4 边界检查 | Step 3.4 |
| 新 · 飞书 CSV 编码 | UTF-8 强制（飞书要求）| Step 4.2 |
| 新 · 写作风格主观偏差 | 每 Pillar 1 段示范，让写作者抓感觉 | Step 5.1 |

---

## 6 · 当天退出条件

| # | 触发 | 动作 |
|---|---|---|
| E1 | Ahrefs trial 已过期 | 选 (a) 重激活 $7 / (b) 跳过精排，KD_modifier 全 0 / (c) 用 SEMrush trial |
| E2 | Ahrefs Bulk 词数限额耗尽 | 减到 Tier 0+1（80 词）|
| E3 | KD 数据有 > 50% 缺失 | 仍按已有数据打分，缺失的 KD_modifier=0 |
| E4 | 主库 v3 Tier 分布异常（Tier 0 = 0 或 > 30）| 调阈值 |
| E5 | 飞书导入失败（编码 / 字段类型）| 检查 UTF-8 + 字段类型映射 |
| E6 | 写作风格指南撰写超时（> 1 hr）| 简化到每 Pillar 5 行要点 |

---

**对齐后下一步**：执行 Step 1（Ahrefs 第 2 次 trial）→ Step 2（KD_modifier）→ Step 3（v3 主库重打分 + 重 Tier）→ 中段对齐 → Step 4（飞书 CSV）→ Step 5（写作风格）→ Step 6（handoff 落盘）

**全 round-2 调研完成 → 启动下周博客写作（Day 8+）**
