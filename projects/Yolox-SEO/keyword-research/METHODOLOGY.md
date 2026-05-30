# 关键词调研方法论 · Solo-op SOP v1.1

**作者**：小刀老师 + Agent B（2026-04-22 → 2026-04-28 第 1 轮实战提炼）
**适用场景**：零流量新站 / SaaS / 内容站，从 0 到 1 建博客选题池
**前提资源**：solo-op、无 SEO 团队、初期工具预算 $0
**交付等级**：🟡 可用（基于 1 轮 YOLOX 实战 + 11 个踩坑提炼，未跨多项目验证）
**v1.1 更新**：合并 Q&A 关键认知；新增 §9 重做调研工作流（方案先行）

---

## 0 · 这份文档要回答什么

| 问题 | 答案章节 |
|---|---|
| **为什么**做关键词调研 | §1 |
| **整体流程**长什么样 | §2 |
| **从哪里挖**关键词（含命中率对比）| §3 |
| **怎么验证**词靠不靠谱 | §4 |
| **拿到词怎么用**到博客 / Pillar / 内链 | §5 |
| 有哪些**坑不要再踩** | §6 |
| **预算工具栈**怎么搭 | §7 |
| **一页式 checklist**速查 | §8 |
| **重做调研**怎么走"方案先行"流程 | §9 |

**和其他文档的关系**：
- `playbook.md §2.3` 是上游"应该做什么"的官方规范
- `archive/round-1-2026-04-22/` 是第 1 轮的踩坑数据（教材性质）
- `REVIEW-index.md` 是给 leadership 看的本周成果索引（已归档）
- **本文是写给"未来再做一次"的可复用 SOP**——抽象掉 YOLOX 特定数据，留判断框架

---

## 1 · 为什么做关键词调研

### 1.1 对零流量新站的角色

新站没有任何流量信号 → Google 不知道你能答什么 → 不会给你曝光。
关键词调研是把这条死锁打开的第一把钥匙。

```
[关键词调研]
    ↓ 决定
[博客选题 + 写作角度 + URL 结构 + Pillar 主题]
    ↓ 决定
[3 个月后 Google 怎么认识你 / 你能拿到什么排名 / AI 助手会不会引用你]
```

**不做的代价**（按真实程度排序）：
1. 写出一堆**没人搜的内容**（最常见，YOLOX 第 1 轮 Claude 扩词命中率仅 12.5%）
2. 写出**搜索量很大但 KD>50** 的词（永远进不了首页 → 0 流量）
3. 选题之间**没有主题集群**（Google 看不到专业度，AI 不会把你选作权威源）
4. 内链网随机 → 失去 Pillar/Cluster 协同

### 1.2 它决定的下游产物

| 下游产物 | 依赖关键词调研的什么 |
|---|---|
| 博客选题 | Tier 1 词 + Reddit 真实问句 |
| 标题 / H1 / TL;DR | 主词的具体长尾形式 |
| H2-H3 结构 | Cluster 内邻近词的子问题 |
| 内链锚文本 | Cluster 间的语义距离 |
| 发布顺序 | 5-3-1 策略（Cluster 先 / Pillar 后） |
| 转化漏斗 | Info → Compare → Buy 三段式 |

### 1.3 什么时候**不**值得做

- 已有大量自然流量，可以直接看 GSC 数据反向推词
- 短期推广（一次性 PR campaign），SEO 不是主战场
- 产品定位还在剧烈变化（这周做完下周就过期）

---

## 2 · 整体流程（7 步可复用 SOP）

```
Day 0: 方案审核     ← v1.1 新增（见 §9）
Day 1: 种子词       → 60-70 词
Day 2: 扩词 + 社区  → 300+ 候选 / 70+ Reddit 问句
Day 3: 主库打分     → 200 词 + Tier 1/2/3
Day 4: 零量词策略   → 30 狙击词 + 选题纪律
Day 5: 主题图       → 3 Pillar × 5 Cluster
Day 6: 博客大纲     → 6 篇 1 页大纲
Day 7: 落库 + 交接  → 飞书 CSV + 下周 handoff
```

**关键节奏**：Day 1-3 是输入（"找词"），Day 4-7 是结构化（"用词"）。如果 Day 3 结束发现词的质量太差，**回到 Day 1 重做种子，不要硬往后推**。

---

## 3 · 怎么挖关键词（输入端）

### 3.1 种子词的 4 类来源

| 来源 | 占比 | 例子（YOLOX）| 注意事项 |
|---|---|---|---|
| **产品功能层** | 30% | "AI agent for SEO"、"AI agent for shopify" | 用产品**职能名**而非内部 Agent **人名**（见 §6.5） |
| **ICP 痛点层** | 30% | "how to get more sales as a solopreneur" | 必须能落到具体职业/场景 |
| **竞品定位层** | 20% | "Lindy alternative"、"Zapier vs n8n" | 砍掉 80% 商业调查词，留少数信息型 |
| **新兴生态层** | 20% | "llms.txt"、"AEO"、"AI Overview citation" | 高 yoy 同比 = 红利期，先占位 |

**Day 1 输出**：60-70 词种子，每条标 [来源] [初步 intent]。

### 3.2 6 条扩词路径 + 命中率对比（v1.1 新增）

| 路径 | 命中率 | 成本 | 推荐度 |
|---|---|---|---|
| ❌ A · Claude 凭空 `Agent × ICP × 场景` | **12.5%** | $0 | 不推荐（已踩坑）|
| ✅ B · 从 GAKP 已验有量词派生 long-tail | ~50% | $0 | 推荐 |
| ✅ C · Reddit/Quora 原帖直接挖 | ~80% | $0 | **首推** |
| ✅ D · Google PAA + 相关搜索链式 | ~60% | $0 | **首推** |
| 🟡 E · KE Bronze "相关关键词" | ~70% | $84/yr | 长期推荐 |
| 🟡 F · DataForSEO `keyword_suggestions` API | ~70% | ~$1-2/次 | 规模化时 |

**默认组合：B + C + D**（全免费，平均命中率 60-80%）

#### 路径 B · GAKP 已验有量词派生（操作）
```
种子（已验 50/mo）："ai agent for shopify"
   → "ai agent for shopify product description"
   → "ai agent for shopify abandoned cart"
   → "ai agent for shopify upsell email"
每个种子派 5-8 词 → 12 种子 × 6 = ~70 高质量候选 → GAKP 一次性回查
```

#### 路径 C · Reddit/Quora 真实问句（最高 ROI）
```bash
opencli reddit search --query "how do I get more customers" --sort top --time year
opencli reddit search --query "ChatGPT cite" --subreddit SEO --sort top
```
**筛选规则**：
- ✅ score≥5 且 comments≥10 且帖子是**问题**
- ❌ score<5 或 comments<5（孤例信号）
- ❌ show-off / announcement / launch 帖（不是搜索需求，见 §6.3）

#### 路径 D · Google PAA 链式（最低成本 + 高命中）
```
1. Google 搜种子词 "is llms.txt a scam"
2. 看 SERP 中部 "People Also Ask" 的 4-6 个问题
3. 点开任一个 → PAA 自动展开新的 4-6 个
4. 重复 3 层 → 一个种子能扩出 30+ 长尾
```
PAA 是 **Google 自己分类相关的问题**，命中率 ~60%。

### 3.3 内部 Agent 人名 ≠ 搜索词（陷阱）

**人名层**（"Sophie agent"）：用户根本不知道，绝对零搜索量。
**职能层**（"SEO Agent"、"Traffic Commander"）：用户会搜的功能词。

→ 用职能层做种子，**人名只在落地页里出现**。

---

## 4 · 怎么验证关键词（核心 · 反踩坑）

### 4.1 关键认知 · 「验证关键词」在零流量期是伪命题（v1.1 新增）

**真相**：你不发布就**无法**真正验证一个词。能做的只是**降低踩雷概率**。

- 真正的验证 = 上线后 GSC 实际 CTR / Position / Impressions
- pre-publish 的所有"验证"都是**代理信号（proxy）**，不是结果信号
- 这是为什么 playbook 接受 "Volume=log10、KD 标 TODO"——再精确也不等于答案

**接受这点意味着**：
- 不要追求 100% 排除踩雷
- 要追求 60-70% 命中率 + **快速发布** + GSC 反馈校准
- 把验证带宽留给"真正会变的决策"，不是"再多查一次精确数据"
- 想再验证时问自己：**这次验证是否会改变下一步动作？** 不会就停

### 4.2 Pre-publish 代理信号 vs Post-publish 真验证（v1.1 新增）

| 阶段 | 指标 | 怎么看 | 可信度 |
|---|---|---|---|
| **Pre** | SERP 前 10 是不是大站垄断 | Google 搜词，看域名权重 | 🟢 高 |
| **Pre** | GAKP 月搜索量区间 + yoy 趋势 | GAKP Historical metrics | 🟡 中（区间不精确）|
| **Pre** | opencli suggest + 社区出现 | P1 验证脚本 | 🟡 中 |
| **Pre** | Reddit 真实问句证据 | 原帖 score / 评论数 | 🟡 中 |
| **Pre** | AI Overview 引用机会 | SERP 是否含 AI 答案块 | 🟢 高（AEO 维度）|
| **Pre** | Ahrefs KD（trial 一次性）| Ahrefs 7-day trial | 🟢 高 |
| **Post** | GSC Impressions（曝光）| GSC | 🟢 真信号 |
| **Post** | GSC Position（平均排名）| GSC | 🟢 真信号 |
| **Post** | GSC CTR | GSC | 🟢 真信号 |
| **Post** | GSC Clicks | GSC | 🟢 真信号 |
| **Post** | LLM 引用率 | 手动 / Profound 等 | 🟢 真信号 |

**核心原则**：pre 阶段做到 4-5 个 🟡 信号一致就该写了，post 阶段才是真验证。

### 4.3 验证手段 4 层（按成本）

#### Layer 0 · opencli 免费 P1 验证（$0，全自动）

**4 信号交叉**：
| 信号 | 命令 | 含义 |
|---|---|---|
| Suggest | `opencli google suggest "<词>"` | suggest≥1 = 有人搜过 |
| SERP 社区 | `opencli google search "<词>"` 看 Reddit/Quora/HN 域名出现 | community≥2 = 有讨论 |
| AI Overview | 同上 | 有 = 信息型 + AI 引用机会 |
| Prefix Suggest | `opencli google suggest "how to <词>"` | 看长尾派生 |

**判定**：suggest≥1 OR community≥2 → 🟢 Keep

#### Layer 1 · GAKP 免费定量（$0，需 Google Ads 账号不绑卡）

**关键流程**：
1. 注册 Google Ads（不要点"启动 campaign"）→ Tools → Keyword Planner
2. 选**"已保存的关键字" / Historical metrics** 标签（**不是 Forecast**，见 §6.6）
3. 复制最多 1000 词进去
4. 导出 CSV → **UTF-16 LE 编码** → `iconv -f UTF-16LE -t UTF-8` 转码
5. 看 yoy 同比：**+900% / +∞** = 新兴红利词；**-100%** = 死词砍掉

#### Layer 2 · SOP v1 五信号（$0，新品类专用）

S1 suggest + S1' prefix suggest + S2 SERP 社区 + S3 Reddit 全站搜 + S4 HN/SO 交叉
≥3 hit = 有真实需求。**对新品牌词无效**。

#### Layer 3 · 付费工具（$7 一次起）

| 工具 | 价格 | 用途 |
|---|---|---|
| Keywords Everywhere Bronze | $84/yr · 100k credits | 实时 Volume / CPC / KD |
| **Ahrefs Trial** | $7 · 7 天 | 一次性批量查 200 词 KD + Volume |
| DataForSEO API | ~$1-2 / 200 词 | 脚本批量查 |
| Ahrefs 订阅 | $99/mo | 长期监控（solo-op 起步不必要）|

### 4.4 验证陷阱：何时停止验证

**症状**：
- 验证完一轮，又开始想"那这些验证数据本身怎么验证？"
- 文档名出现 `verify-of-verify.md` / `validation-of-validation-result.md`
- 一天过去还在写"如何更精确地证明 50/mo 是不是真 50"

**根因**：playbook 已接受零流量期的不精确，但人对"精确"的执念会自驱补偿。

**纪律**：
1. 验证完一轮 → **直接做下一步交付**
2. 想再验证时问：**这次验证是否会改变下一步动作？** 不会就停
3. 把"还想验证什么"写进 §诚实边界，而不是再开一个验证文档

---

## 5 · 怎么用关键词（输出端）

### 5.1 优先级公式（零流量期临时版）

```
Priority_v0 (0-10) =
    Info_intent_bonus  (0|1)  × 2.0    # 是不是信息型？
  + Product_Match      (0-3)  × 1.5    # 你产品能不能直接答？
  + Reddit_Evidence    (0|1)  × 2.0    # 有原帖证据吗？
  + Specificity        (0-2)  × 1.0    # 长尾几层？
```

**为什么改公式**：playbook 原公式 `Vol×0.4 + Intent×0.4 + KD×-0.2`，零流量期 Vol 和 KD 都缺，退化只剩 Intent。

**Tier 分档**：
| Tier | Priority | 含义 | 动作 |
|---|---|---|---|
| 🔴 1 | 8-10 | 本周博客强候选 | Day 6 必选 |
| 🟠 2 | 5-7 | 下周-下下周 | Day 6 备选 |
| 🟡 3 | 2-4 | 月度储备 | 月度刷新时看 |
| ⚫ 砍 | ≤1 | 进负向词库 | → 07-negative-keywords |

**Day 7 升级**：拿到 Ahrefs KD + Volume 后用 playbook 原公式重排，主库升 v1.1。

### 5.2 指标真实重要性排序（v1.1 新增 · 反直觉）

**KD 和搜索量不是最重要的**——这是反 SEO 行业共识，但对零流量新站确实如此。

| 排序 | 指标 | 为什么 |
|---|---|---|
| **1** | Intent 是不是信息型 | Google 把信息型流量优先给中小站；商业型词被大站锁死 |
| **2** | 你产品能不能独特地答 | 写出别人写过的 = me-too，无差异化抓不到 AI 引用 |
| **3** | SERP 前 10 是大站还是小站 | 比 KD 数字更直观——前 10 都是 medium / dev.to / 个人博客就能挤进去 |
| **4** | Reddit 真实问句佐证 | 证明是真用户问的，不是工具拼的 |
| **5** | AI Overview 是否出现 | 2025-2026 AEO 新维度，AI 引用 = 0 click 也有品牌价值 |
| 6 | KD（关键词难度）| 参考不是决策点；KD<10 是必要不充分条件 |
| 7 | Volume（搜索量）| 区间够用，精确数字对决策无意义 |

**反直觉点**：很多 KD<10 的词其实**没人搜**；反过来很多 KD 50+ 的词新站发了一样能在 6-12 月慢慢爬上来——**前提是 SERP 前 10 不是 Google/Wikipedia/Forbes**。

### 5.3 Pillar / Cluster 主题图（hub-and-spoke）

```
Pillar (3000+ 字宽文 · KD 中-高)
   ├── Cluster 1 (1000-2000 字深文 · KD<10 长尾)
   ├── Cluster 2
   ├── Cluster 3
   ├── Cluster 4
   └── Cluster 5
```

**怎么选 Pillar**（3 个，不要更多）：
1. 必须是**信息型**主题（不是 best/vs/pricing）
2. 5+ 个 Cluster 长尾词能挂在下面
3. 至少 1 个 Cluster 词有 GAKP 实数据（不全是零量）

**怎么选 Cluster**（每 Pillar 5 个）：
1. 每个 Cluster 是**一个具体子问题**（"is X a scam"、"how to X for Y"）
2. KD 估计 <10（长尾 + 社区证据 + 低 SERP 竞争）
3. 至少有 1 个 Reddit 原帖佐证

### 5.4 5-3-1 发布顺序（关键策略）

**反直觉**：**Pillar 不首发**。

```
Week 1-3: 先发 5 个 Cluster（每天 1 篇）
   ↓ 等 Google 索引 + AI 抓取 + 内链积累
Week 5-6: 3 个 Cluster 已被索引，开始发对应 Pillar
   ↓ Pillar 借 Cluster 已有权重起跑
Week 7+: 持续发 Cluster 完善长尾覆盖
```

**为什么**：新站发 Pillar，Google 看不到专业度（孤峰）→ KD 高直接进不去。
先发 Cluster，等 Google 看到"这个站在 X 主题有 5 篇深度内容" → Pillar 才有机会。

### 5.5 选题判断 4 条纪律（防复发）

| # | 问题 | 不通过 |
|---|---|---|
| 1 | 原帖是"提问"还是"公告/show-off"？ | 后者砍 |
| 2 | 原帖 + Cluster 邻近证据累计够吗？ | 孤例（1/1 score）不够 |
| 3 | 你的产品有现成能力答这题吗？ | 答不了不写 |
| 4 | 关键词是用户会 Google 的吗？ | 内部 Agent 人名 / 行业黑话不行 |

### 5.6 内链网设计

- **Cluster → Pillar**：每篇 Cluster 文末 1 个**主链**到 Pillar
- **Cluster → Cluster (同 Pillar)**：正文 2-3 个**邻近链**
- **Pillar → Cluster**：导航/锚点链接每个 Cluster
- **跨 Pillar**：少量（1-2 个/篇），不滥用

锚文本用**完整语义短语**（"why ChatGPT cites some pages"），不要 "click here"。

---

## 6 · 11 个踩过的坑（教材）

| # | 坑 | 教训 | 触发 SOP |
|---|---|---|---|
| 6.1 | 验证陷阱：递归验证循环 | playbook 已接受不精确，停在颗粒度即可 | §4.1 / §4.4 |
| 6.2 | Claude 扩词命中率 12.5% | Claude 不是搜索词验证器，必须 GAKP 回查 | §3.2 路径 A |
| 6.3 | Reddit show-off 帖陷阱 | 只留**问题型**帖子，公告 / show-off / launch 砍 | §3.2 路径 C |
| 6.4 | Reddit 1/1 score 孤例陷阱 | 至少 2-3 个帖子或 1 个高互动帖（≥10 评论）| §5.5 纪律 #2 |
| 6.5 | 内部 Agent 人名 ≠ 搜索词 | 用职能名做种子，人名只在落地页 | §3.3 |
| 6.6 | GAKP Forecast vs Historical 混淆 | 列名 "Estimated Clicks/Impressions" = Forecast；"Avg. monthly searches" = Historical | §4.3 Layer 1 |
| 6.7 | GAKP CSV UTF-16 LE 乱码 | `iconv -f UTF-16LE -t UTF-8 in.csv > out.csv` | §4.3 Layer 1 |
| 6.8 | Volume 区间够不够 | 零流量期看**有/没有 + 同比方向**就够 | §4.1 |
| 6.9 | Pillar 数据驱动 vs 拍脑袋 | Pillar 决策**等 Layer 1 数据再做** | §5.3 |
| 6.10 | yoy +∞ 是真信号 | +∞ = 新兴生态起飞，**先占位红利** | §3.1 新兴生态层 |
| 6.11 | Handoff stale（隔夜过期）| 用 git status / 实际分支名核对，不依赖记忆 | session 第一件事 |

---

## 7 · 工具栈推荐（按预算）

### Tier 0 · 完全免费（推荐起步）
| 工具 | 用途 | 限制 |
|---|---|---|
| opencli | google search/suggest + reddit/HN/SO | 速率 ~30 req/min |
| GAKP（不绑卡）| Volume 区间 + 27 月历史 | 不精确，无 KD |
| Reddit/Quora 网页 | 真实问句挖掘 | 手动筛选 |
| Claude（已订阅）| 扩词辅助 | 命中率 12.5%，必须回验 |

**适用阶段**：Week 1-4，从 0 到主库 + 选题池

### Tier 1 · ~$84/年
| 工具 | 用途 |
|---|---|
| Keywords Everywhere Bronze | 实时 Volume + KD |

**触发**：月度词库刷新；想要精确 Volume 时

### Tier 2 · 一次性 $7
| 工具 | 用途 |
|---|---|
| Ahrefs 7-day Trial | 一次性批量查 200 词 KD + Volume |

**触发**：Day 7 上线前精排；季度大刷新

### Tier 3 · $99/月+
仅当：3+ 站点 / 有团队监控竞品。Solo-op 单站起步**不必要**。

---

## 8 · 一页式 Checklist（速查）

### Day 0（v1.1 新增 · 方案审核）
- [ ] 写方案文档（模板见 §9.2）
- [ ] 老板审核（checklist 见 §9.3）
- [ ] 通过后才进 Day 1

### Day 1（种子词）
- [ ] 4 类来源各挖 15-20 词
- [ ] 每条标 [来源] [intent: info/compare/buy]
- [ ] 输出：`01-seed-keywords.md` 60-70 词

### Day 2（扩词 + 社区）
- [ ] 默认组合 B + C + D（**禁用路径 A**）
- [ ] Reddit/Quora 真实问句（score≥5 / 评论≥10）
- [ ] 砍 show-off / 公告帖
- [ ] 输出：`02-expanded-keywords.md` ~300 词 + `03-reddit-quora-questions.md` ~70 问句

### Day 3（主库打分）
- [ ] 跑 Priority_v0 公式打分
- [ ] Tier 1 / 2 / 3 分档
- [ ] 砍 ≤1 → 负向词库
- [ ] 输出：`04-keyword-map-v1.md` 200 词 + `07-negative-keywords.md`

### Day 4（验证 + 零量词）
- [ ] Layer 0 opencli P1 验证 Tier 1 40 词
- [ ] Layer 1 GAKP 跑全 200 词（导出 → iconv 转码）
- [ ] 标 yoy +∞ 词 + -100% 死词
- [ ] **每个候选词跑 SERP 前 10 域名快查**（v1.1 新加）
- [ ] 选 30 狙击词
- [ ] 输出：`05-zero-volume-strategy.md`

### Day 5（Pillar / Cluster 主题图）
- [ ] 选 3 Pillar（信息型 + 5 Cluster 挂得下 + 至少 1 实数据）
- [ ] 每 Pillar 选 5 Cluster
- [ ] 数据驱动调整 Pillar 排序
- [ ] 输出：`06-pillar-cluster-map.md`

### Day 6（博客大纲）
- [ ] 9 候选砍 6（4 条选题纪律全过）
- [ ] 每篇 1 页：H1 + TL;DR + H2-H3 + Reddit URL + CTA + 3-5 FAQ
- [ ] 标 FAQPage schema 字段
- [ ] 输出：`08-week2-blog-outlines.md`

### Day 7（落库 + 交接）
- [ ] 飞书 CSV 导入
- [ ] 可选：Ahrefs 7-day trial 补 KD
- [ ] 写下周 handoff
- [ ] 输出：`09-feishu-import.md` + `2.x-handoff.md`

### 跨周维护
- [ ] 月度刷新主库
- [ ] 每发 1 篇 Cluster 后 2 周看 GSC 是否被索引
- [ ] 3 Cluster 索引到位后启动对应 Pillar

---

## 9 · 重做调研工作流（v1.1 新增 · 方案先行）

### 9.1 方案先行原则

**约束**：每轮调研 / 大改动 → **先出方案 → 老板审核 → 通过后才执行**。

**理由**：第 1 轮 7 天踩了 11 个坑，根因是"边做边想"——
- Day 3 才意识到 Claude 扩词命中率太低（已浪费 1 天）
- Day 4 中段才搞清楚 GAKP Forecast vs Historical（已浪费半天）
- Day 5 才靠 GAKP 数据对调 Pillar 1/2（如果方案先定就不会出现）

**方案文档目标**：把所有判断点前置，让老板能在 5 分钟内决策。

### 9.2 方案模板（提交审核用）

```markdown
# 第 N 轮关键词调研 · 方案 vN

## 1 · 背景
- 上轮成果（保留什么）：...
- 上轮问题（避免什么）：... ← 必须列上轮的具体坑
- 这一轮要解决什么：（一句话）

## 2 · 目标（具体可量化）
- 词库规模：... 词
- Tier 1 数量：... 词
- 选题池：... 篇
- 完成时间：YYYY-MM-DD ~ YYYY-MM-DD

## 3 · 范围
做什么：...
不做什么：（明确划界，避免 scope creep）

## 4 · 流程（Day 0-7 + 每天交付）
（直接套用 §8 checklist + 本轮特定动作）

## 5 · 工具栈选择
- 免费层：opencli + GAKP + Reddit/Quora
- 是否启用付费：[ ] KE Bronze / [ ] Ahrefs trial / [ ] DataForSEO
- 预算上限：$XX

## 6 · 关键决策点（需老板拍板，3-5 个）
- 决策 1：...（选项 A / B / C，建议 A）
- 决策 2：...
- ...

## 7 · 风险 + 退出条件
- 风险 1：...（缓解措施）
- 退出条件：什么情况下叫停（例如 Day 3 命中率<30% → 重做种子）

## 8 · 时间线 + 里程碑
| Day | 动作 | 交付 | 老板审核点 |
|---|---|---|---|
| Day 0 | 方案审核 | 本文 | ✅ |
| Day 3 | 主库初版 | 04-... | 🟡 抽查 |
| Day 5 | Pillar 锁定 | 06-... | ✅ 必须确认 |
| Day 7 | 完整交付 | 全套 | ✅ 总验收 |
```

### 9.3 审核 checklist（老板视角）

- [ ] 目标是否对齐这季度 OKR
- [ ] 关键决策点是否够具体（不是"看情况"）
- [ ] 投入产出比是否说服力（X 天 + Y 元 → Z 个博客）
- [ ] 退出条件是否明确（什么时候叫停）
- [ ] 上轮的坑是否有具体规避动作（每个坑对应一个新流程项）

### 9.4 重启时的「留 vs 弃」判断

**老数据复用矩阵**：

| 类型 | 第 1 轮产出 | 第 2 轮处理 |
|---|---|---|
| 种子词 | `01-seed-keywords.md` 70 词 | 🟢 复用 60% + 补 40 词新种子 |
| Claude 扩词 | `02-expanded-keywords.md` 部分 | ❌ 弃用（命中率 12.5%）|
| Reddit 问句 | `03-reddit-quora-questions.md` 70+ | 🟢 复用 + Day 2 再深挖 |
| 200 词主库 | `04-keyword-map-v1.md` | 🟡 参考结构，词重新打分 |
| 30 狙击词 | `05-zero-volume-strategy.md` | 🟡 大部分有效，重过 4 纪律 |
| Pillar/Cluster | `06-pillar-cluster-map.md` | 🟡 参考结构，可能调整 |
| 117 负向词 | `07-negative-keywords.md` | 🟢 直接复用 |
| GAKP 原始数据 | `raw-gakp-historical.csv` | 🟢 直接复用（27 月历史不会变）|
| P1 验证结果 | `p1-verdict.csv` | 🟡 部分复用（词没变就有效）|

**老坑规避动作**（每个坑写进新流程）：

| 上轮坑 | 新流程规避动作 |
|---|---|
| Claude 12.5% 命中率 | Day 2 禁用路径 A，默认 B+C+D |
| 验证递归循环 | Day 4 设硬性截止：完成验证就进 Day 5 |
| Reddit 1/1 孤例 | 进 Tier 1 必须 ≥10 评论 OR ≥2 帖子 |
| Pillar 拍脑袋 | Day 5 前必须有 GAKP 数据，无数据不定 Pillar |
| GAKP 编码 | 模板命令写进 Day 4 checklist |
| Forecast/Historical 混淆 | Day 4 前 5 分钟检查标签 |
| 内部 Agent 人名 | Day 1 种子词审核就过滤人名 |

---

## 10 · 诚实边界

**这套方法论的局限**：
- 🟠 仅基于 1 个项目（YOLOX）1 轮的实战，未跨多项目验证
- 🟠 Priority_v0 公式是 ad-hoc 修正版，未做横向对比
- 🟠 5-3-1 发布顺序是**理论 + 业内共识**，YOLOX 还没跑完一个完整周期来证明
- 🔴 Layer 2 SOP v1 五信号对**新品牌词无效**（已知）
- 🔴 GAKP 数据**只对英文母语市场可信**，中文/小语种需要本地工具（百度指数、Naver 等）

**升级路径**：
- v1.2：第 2 轮调研完成后，对比命中率（路径 A 12.5% → B+C+D 应 ≥60%）
- v1.5：3 个月后 GSC 数据足够，回填实际 CTR / Position 数据，校准 Priority 公式
- v2.0：跑完 YOLOX 第一个完整 Pillar 周期（~2026-07），验证 5-3-1 是否成立

---

## 11 · 引用 / 相关文档

| 文档 | 在哪查 |
|---|---|
| 上游官方规范 | `docs/seo/playbook.md §2.3` |
| 第 1 轮全部产出（教材性归档）| `archive/round-1-2026-04-22/` |
| 第 1 轮踩坑详解 | `archive/round-1-2026-04-22/README.md` |
| 当前进行中调研（如有）| `round-N-YYYY-MM-DD/` |

---

**最后更新**：2026-04-28（v1.1）
**下次更新触发**：第 2 轮调研完成后填充 v1.2
