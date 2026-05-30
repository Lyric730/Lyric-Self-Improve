# Layer 4 · Day 4 量化验证 + 零量词策略方案

**日期**：2026-04-29
**讨论方**：小刀老师 + Agent B
**状态**：草案 v1（讨论中）
**前置依赖**：L3 v1 已交付（04-keyword-map.md 主库 v1）

---

## 0 · 你的决策（输入）

| # | 决策 | 选择 |
|---|---|---|
| 1 | GAKP 跑法 | **1a** · 一次跑全 515 词（主库 v1 500 + Tier-E 15）|
| 2 | UTF-16 LE 处理 | **2a** · 立即 iconv 转 UTF-8（坑 6.7 规避）|
| 3 | Volume 进入 Priority | **3a** · 加第 7 维度 + yoy 修正（16 分制）|
| 4 | EXPLORATORY 处理 | **4a** · 有量自动重打分 |
| 5 | 零量词 30 选法 | **5a** · 从 Tier 1+2 中 Vol=0 + 蓝海 + Reddit 真问 |
| 6 | 输出文件 | **6b** · 3 文件（04 v2 + 05 零量 + 05.5 yoy 红利）|
| 7 | Pool B+C 撒网 | **a** · 加 Step：GAKP 撒网（+30 min，找意外爆点）|
| 8 | Ahrefs Bulk lookup | **1a** · 加（双源 Volume，trial 第 2 次用，~15 min）|
| 9 | Volume 公式改加分 | **2a** · 是（只加不扣，避免冤杀 95% "---" 长尾）|
| 10 | 零量词清单定位 | **3a** · 重要交付物（接受 60-95% "---" 是 expected）|

---

## 1 · L4 边界（不越界）

按 L0 §7 验证粒度分层：

| 越界 | 谁做 |
|---|---|
| ❌ 重新做存在性（PAA/KE 出现）| L2 已做 |
| ❌ 精确 KD（trial 完整数据）| L7 做 |
| ❌ Pillar 决策 | L5 |
| ❌ Cluster 精细化 | L5（L3 已粗分）|

**L4 只做**：
1. GAKP 跑全候选池（515 主库 + 1750 Pool B/C 撒网）→ Volume + 27 月 yoy + competition
2. Ahrefs Bulk lookup 双源补充（重要 ≤1000 词）
3. EXPLORATORY 验证后分流
4. yoy 红利标 + 死词砍
5. Pool B/C 撒网中"被低估的词"升回主库
6. 零量词 30 选 + 4 选题纪律
7. 主库 v2 整理（v4_扩展 公式 16 分制）

---

## 2 · 关键认知 · 接受"---"是 expected

**第 1 轮 GAKP 真实数据**：217 词 → 205 "---"（94.5%）→ 12 有量（5.5%）

GAKP "---" **不一定是真零量**：

| 原因 | 占比（估）|
|---|---|
| GAKP 数据库没收录（长尾词常见）| ~50% |
| 真零量（确实没人搜）| ~30% |
| 低于 GAKP 阈值（<10/mo 不显示）| ~15% |
| 账户级别限制（不绑卡 free）| ~5% |

**v4 应对**：
- Volume_score **改为加分项**（只加不扣）→ "---" 词不被冤杀
- Ahrefs Bulk lookup 双源补充 → 把 GAKP 没收录但 Ahrefs 有的捞回来
- 双源后预计零量比例从 95% 降到 60-70%
- **剩余 60-70% 真零量是策略性输入，不是失败** → 进零量狙击词候选

---

## 3 · 当天目标

| 维度 | 目标 |
|---|---|
| GAKP 跑全 | 515 主库 + 1750 Pool B/C 撒网 = ~2265 词 |
| Ahrefs Bulk | ≤1000 词（主库 500 + Pool B/C 重点 500）|
| 双源覆盖率 | 有量比例从 5% → 30-40% |
| yoy 红利词标 | 5-15 个（+900%/+∞）|
| 死词砍 | 10-30 个（-100%）|
| Pool B/C 升回主库 | 5-20 个意外爆点 |
| 零量词清单 | 30 个狙击词 |
| 主库 v2 | 500 + 升回 = ~520 词 |
| 工期 | ~3 hr 净执行 |

---

## 4 · 当天动作（8 步）

### Step 1 · GAKP 主库 v1 + Tier-E 跑（15 min）

#### 1.1 准备词单
```bash
# 从 04-keyword-map.md 提取主库 + Tier-E 词单 → 一行一词
grep -E '^\| [0-9]+ ' /path/to/04-keyword-map.md | awk -F'|' '{print $3}' | sed 's/^ *//; s/ *$//' > /tmp/gakp-input-main.txt
```

预计 ~515 词，GAKP 上限 1000，一次跑。

#### 1.2 GAKP 操作
1. 进 Google Ads（不绑卡） → Tools → Keyword Planner
2. **必选 "已保存的关键字" / Historical metrics 标签**（坑 6.6，不要 Forecast）
3. 复制 /tmp/gakp-input-main.txt 内容粘进去
4. 点 Get results → 等返回
5. 导出 CSV → `/tmp/gakp-main-raw.csv`（UTF-16 LE 编码）

#### 1.3 立即 iconv 转码（决策 2a）
```bash
iconv -f UTF-16LE -t UTF-8 /tmp/gakp-main-raw.csv > /tmp/gakp-main.csv
head -3 /tmp/gakp-main.csv  # 验证读得了
```

#### 1.4 解析输出
- 字段：keyword / Avg. monthly searches / 27 月历史 / Competition / Top of page bid (low/high)
- 落 `/tmp/gakp-main-parsed.csv` 标准化

### Step 2 · GAKP 撒网 Pool B+C（20 min · 决策撒网 a）

#### 2.1 准备撒网词单
- Pool B 1000 + Pool C 750 = 1750 词
- 分 2 批（每批 ~875，避开 GAKP 1000 限制）

#### 2.2 跑 + iconv（同 Step 1.3）

输出：
- `/tmp/gakp-pool-b.csv`
- `/tmp/gakp-pool-c.csv`

#### 2.3 解析输出 + 合并
- 与 Step 1.4 主库数据合并 → `/tmp/gakp-all.csv`（~2265 词）

### Step 3 · Ahrefs Bulk lookup（15 min · 决策 8a · trial 第 2 次用）

#### 3.1 选词进 Ahrefs Bulk
预算 1000 词（Ahrefs trial 上限通常足够）：
- 主库 500 全部
- Pool B+C 中**GAKP 撒网显示有量但 yoy 不全 + 长尾且 GAKP "---" 的优先** ~500

#### 3.2 操作
1. Ahrefs Keywords Explorer → Bulk
2. 粘 1000 词 → Run
3. 导出 CSV → `/tmp/ahrefs-bulk.csv`

字段：keyword / Volume / KD（粗略）/ CPC / Top SERP

#### 3.3 编码处理
- Ahrefs 通常 UTF-8（不需要 iconv，但仍验证一次）
- `head -3 /tmp/ahrefs-bulk.csv` 检查

### Step 4 · 双源数据合并 + Volume_score 计算（15 min）

#### 4.1 Python 脚本合并

```python
import pandas as pd

gakp = pd.read_csv('/tmp/gakp-all.csv')
ahrefs = pd.read_csv('/tmp/ahrefs-bulk.csv')

# 按 keyword 合并
merged = gakp.merge(ahrefs, on='keyword', how='outer', suffixes=('_gakp', '_ahrefs'))

# Volume_score 计算（任一源有量就给分）
def volume_score(row):
    vol_gakp = row.get('avg_monthly_gakp', 0) or 0
    vol_ahrefs = row.get('volume_ahrefs', 0) or 0
    vol_max = max(vol_gakp, vol_ahrefs)
    if vol_max >= 1000: return 3
    elif vol_max >= 100: return 2
    elif vol_max >= 10: return 1
    else: return 0

merged['volume_score'] = merged.apply(volume_score, axis=1)
```

#### 4.2 yoy 修正（仅 GAKP 给）
```python
# 27 月数据计算最近 12 月 vs 前 12 月 yoy
def yoy_modifier(row):
    yoy = row.get('yoy_gakp', 0)
    if yoy >= 9 or yoy == float('inf'): return 0.5  # +900%/+∞
    elif yoy <= -1 or yoy == -1: return -0.5  # -100%
    else: return 0

merged['yoy_modifier'] = merged.apply(yoy_modifier, axis=1)
```

#### 4.3 输出
- `/tmp/round2-day4-volume-merged.csv` · 含 Volume_score + yoy_modifier
- 双源覆盖率统计：实际有量词数 vs 总词数

### Step 5 · yoy 红利标 + 死词砍（15 min）

#### 5.1 yoy 红利识别（坑 6.10 规避）
- 筛选 yoy ≥ +900% 或 +∞ 的词
- 标 `RISING`
- 输出 `05.5-yoy-rising.md`（决策 6b）

字段：keyword / GAKP Volume 当前 / 27 月走势简述 / 起飞月份 / 对应 ICP / 产品对接

#### 5.2 死词砍
- yoy ≤ -100% 的词
- 进 `07-negative-keywords-v4.md`（增量）
- 标 `DEAD-yoy-100`

### Step 6 · Pool B/C 撒网回升（15 min）

#### 6.1 识别"被低估的词"
Pool B/C 中**满足任一条件**的：
- Volume ≥ 100/mo（任一源）
- yoy ≥ +200%
- yoy = +∞ 且双源都给数据

#### 6.2 升回主库
- 这些词从 Pool B/C 升到主库 v2
- 重新打 Priority（v4_扩展 16 分公式）
- 重新分 Tier
- 输出：`02.5-pool-promotions.md` 升级清单

预计 5-20 词意外爆点。

### Step 7 · 零量词 30 选（30 min · 决策 5a + 4 选题纪律）

#### 7.1 候选筛选（按 5a）
从主库 Tier 1+2 中筛：
- Volume_score = 0（双源都"---"）
- Competitor_signal ≥ 0（gap-new / gap-overlap / 未知）
- Reddit_Evidence = 1（有原帖证据）
- Product_Match ≥ 2

预计 30-60 候选。

#### 7.2 4 选题纪律过滤（防"自嗨型"零量）

继承 archive/round-1/05 §6 的 4 条纪律：

| # | 问题 | 不通过 |
|---|---|---|
| 1 | 原帖是"提问"还是"公告/show-off"？ | 后者砍 |
| 2 | 原帖 + Cluster 邻近证据累计够吗？ | 孤例砍 |
| 3 | 你的产品有现成能力答这题吗？ | 答不了不写 |
| 4 | 关键词是用户会 Google 的吗？ | 内部 Agent 人名 / 行业黑话不行 |

每条候选过 4 问 → 4 yes 通过。

#### 7.3 选 30 个
- 4 yes 通过的全部入选（如 ≤30 全留）
- 多于 30 → 按 Priority_v4_扩展 排前 30
- 输出 `05-zero-volume-strategy.md`（决策 6b）

字段：# / 关键词 / Tier（来自 Tier 1/2）/ ICP / 产品对接 / 原帖 URL / Competitor_signal / 4 纪律过 / 狙击理由

### Step 8 · 主库 v2 整理 + 落盘（30 min）

#### 8.1 v4_扩展 公式（16 分制）

```
Priority_v4_扩展 (0-16) =
    Info_intent      (0|1)  × 2.0   = 0~2
  + Product_Match    (0-3)  × 1.5   = 0~4.5
  + Reddit_Evidence  (0|1)  × 2.0   = 0~2
  + Specificity      (0-2)  × 1.0   = 0~2
  + Existence        (0-3)  × 0.5   = 0~1.5
  + Competitor       (-2~1) × 1.0   = -2~+1
  + Volume_score     (0-3)  × 1.0   = 0~3       ← v4 新增加分项
  + yoy_modifier     (-0.5~+0.5)    = -0.5~+0.5

最高: ~16.5  最低: ~-2.5  实际范围: 5-13
```

#### 8.2 Tier 阈值调整（16 分制）

| Tier | 旧（13 分）| 新（16 分） | 含义 |
|---|---|---|---|
| Tier 0 | 10-13 | **12-16** | 顶 5-10 词，下周博客必选 |
| Tier 1 | 7.5-9.9 | **9-11.9** | 博客强候选 |
| Tier 2 | 4.5-7.4 | **5.5-8.9** | 下周-下下周 |
| Tier 3 | 1-4.4 | **1-5.4** | 月度储备 |
| 砍 | <1 | **<1** | 进负向词库 |

#### 8.3 EXPLORATORY 重打分（决策 4a）
- Tier-E 词跑完 GAKP + Ahrefs 后：
  - 有量（Volume_score ≥ 1）→ 用 v4_扩展 公式打分入正常 Tier
  - 仍零量 → 留 Tier-E（标"等下次刷新"）

#### 8.4 输出 04-keyword-map-v2.md

字段表（含 L3 字段 + Volume + yoy）：

| # | 关键词 | Tier | Priority | Volume(GAKP/Ahrefs) | yoy | Vol_score | 6 维度分 | Intent | ICP | 产品 | Cluster | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

末尾汇总：
- 各 Tier 数量（旧 vs 新）
- Volume 覆盖率（有量比例）
- yoy 分布（+∞/+900%/+200%/0/-100%）
- 升回主库的 Pool 词数
- 零量词清单总数（应为 30）
- EXPLORATORY → 正常 Tier 的数量

---

## 5 · 当天交付物（4 文件）

| 文件 | 内容 |
|---|---|
| `04-keyword-map-v2.md` | 主库 v2 · Volume + yoy + 16 分制 + 4 档 Tier |
| `05-zero-volume-strategy.md` | 30 个零量狙击词 + 4 选题纪律 |
| `05.5-yoy-rising.md` | yoy +900% / +∞ 红利清单（5-15 词）|
| `07-negative-keywords-v4.md` | 含 yoy -100% 死词增量 |

---

## 6 · 当天规避动作（11 坑映射）

| 坑 | 规避 | 在哪 Step |
|---|---|---|
| **6.1 验证递归循环** | L4 只做量化区间，不重做存在性，不抢 L7 精确 KD | 全 Step |
| **6.6 GAKP Forecast/Historical 混淆** | Step 1.2 必选 "已保存的关键字 / Historical metrics" | Step 1.2 |
| **6.7 GAKP CSV UTF-16 LE 乱码** | Step 1.3 立即 iconv 转 UTF-8 | Step 1.3 |
| **6.8 Volume 区间够不够** | 接受 GAKP 区间 + Ahrefs 双源补充 | Step 4 |
| **6.10 yoy +∞ 真信号** | Step 5.1 主动找 +900%/+∞ 标 RISING | Step 5 |
| 6.11 Handoff stale | L4 启动前 `git status` | 启动前 |
| 新 · GAKP "---" 冤杀 | Volume_score 改加分项（不扣分） | Step 4.1 |
| 新 · trial 倒计时 | Step 3 用 trial 第 2 次，剩余天数留给 L7 | Step 3 |
| 新 · 双源数据冲突 | 取 max（任一源有量即认）| Step 4.1 |
| 新 · 零量词"自嗨" | 4 选题纪律过滤（archive/round-1/05 §6）| Step 7.2 |

---

## 7 · 当天退出条件

| # | 触发 | 动作 |
|---|---|---|
| E1 | GAKP 注册失败 / paywall | 跳过 Step 1-2，仅 Ahrefs（数据稀疏，需重审）|
| E2 | GAKP "---" 比例 > 95%（主库）| 检查词单是否有问题（人名 / 黑话）|
| E3 | Ahrefs trial 已过期 | 跳过 Step 3，仅 GAKP（损失双源覆盖）|
| E4 | 双源后有量比例仍 < 20% | 警示但继续；零量词清单作为主输出 |
| E5 | yoy +∞ 词数 = 0 | 警示但继续；可能本批没新兴红利 |
| E6 | 零量词候选 < 30 | 阈值放宽（去掉 Reddit_Evidence 必选）|
| E7 | Pool B/C 升回主库的词 = 0 | 警示；可能 L2 4 级筛已经覆盖好了 |
| E8 | 主库 v2 中 Tier 0 词数 = 0 | 异常，回 Step 8 检查公式 |

---

**对齐后下一步**：执行 Step 1（GAKP 主库）→ Step 2（GAKP 撒网）→ Step 3（Ahrefs Bulk）→ Step 4（合并）→ Step 5（yoy 标）→ Step 6（升回主库）→ Step 7（零量词 30）→ Step 8（v2 落盘）→ 起草 L5 Pillar/Cluster 方案
