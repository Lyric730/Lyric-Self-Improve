# Round-2 关键词研究 · Leader 审核版 (handoff v1)

**Round**:Round-2(2026-04-28 启动)
**Author**:Agent B + 小刀老师
**Date**:2026-05-07
**Branch**:`feat/seo-keyword-research`(worktree)
**Status**:🟡 可用 · L5 完成 / L6+L7 待 leader 审核后启动
**审核范围**:L0-L5(8 层中前 6 层) — Pillar/Cluster 决策与索引证据

---

## 0 · TL;DR

> Round-2 在 Round-1 的 Pool A/B/C 三层架构上,通过 8 渠道公共 Suggest 扩展 + Haiku 批量语义筛选 + KWFinder paid 全量化验证(570/570 词),产出 666 词主库 v0,经 6 维度 13 分公式打分得到:
> 
> **Tier 1**:6 词(Pillar 候选) · **Tier 1.5**:58 词(ICP 长尾,博客大纲候选) · **Tier 2**:88 词(Cluster 候选) · **Tier 3**:418 词(长尾备用)
>
> 选定 **3 Pillar × 5 Cluster = 15 词**:**A · AEO** + **B · Agent 开发栈(MCP)** + **C · SMB AI 工具(AI app builder)**
>
> 待 leader 拍板后启动 **L6 (6 篇博客大纲)** + **L7 (精排 + handoff final)** — 我侧预估 4-6h

## 1 · 文档地图(精确索引)

| Layer | 文档 | 行数 | 核心交付 |
|---|---|---|---|
| L1 种子词 | `01-seed-keywords.md` | 161 | Pool A 76 词(46 ICP + 13 product + 7 EXPLORATORY + 10 promoted) |
| L2 Step 0 watchlist | `01.5-watchlist.md` | 60 | 7 词 watchlist(双源降级 3 + 单源 4) |
| L2 Step 1-2 候选 | `01.5-pool-b-candidates.md` | 249 | Pool B 91 词(Layer 2 真筛) |
| L2 Step 1 原料 | `01.5-pool-c-raw.md` | 1051 | Pool C 903 帖原料(Reddit/Quora/IH) |
| L2 Step 1 升级 | `02.5-pool-updates.md` | 110 | 10 B→A + 78 C→B 升级记录 |
| L2 Step 5 主库 | `02-expanded-keywords.md` | 719 | master v0 666 词(Pool A 76 + Haiku keep 590) |
| L2 备用池 | `02.5-pool-b-reserve.md` | 188 | 175 keep_weak(3/4 yes,Layer 3 待复审) |
| L3 主库打分 | `03-master-scored.md` | 264 | 6 维度 13 分 + Tier 1/1.5/2/3 分档 |
| L5 Pillar/Cluster | `04-pillar-cluster.md` | 88 | 15 词决策 + 精确数据(本批新增) |
| **本审核文档** | `99-handoff-leader-review.md` | 172 | leader 审核入口 |
| 结构化数据 | `data/master_scored.json` | — | 570 词 KWFinder 全数据(Vol/KD/Growth/Intent/SERP) |
| 原始 KWFinder | `data/Data_Gotted/kwfinder_*.csv` | 4 个文件 | 570 词原始 export |

## 2 · 漏斗证据链(数字可追溯)

```
L0/L1: Pool A 66 词(46 ICP + 13 product + 7 EXPLORATORY)
       ↓ source: 01-seed-keywords.md L1-161
L2 Step 1: B→A 10 词 + C→B 78 词 升级
       ↓ source: 02.5-pool-updates.md L1-110
L2 Step 2: 8 渠道 Suggest 扩展 → 1890 sugg
       ↓ Google/YouTube/Bing/DDG Suggest + Reddit/Quora/IH/Twitter
L2 Step 3: Pool B 27 词广扫 → 27 sugg
L2 Step 5 Layer 1: 机械去重 → 1316 unique
       ↓ scripts/step5_funnel.py
L2 Step 5 Layer 2: 自动质量信号(hero name 黑名单 / 负向词 / Vol=0+KD>30)
       ↓ tier-1-validated 8 + tier-2-pool-a 66 + tier-2-kd-only 2 = 76 direct keep
       ↓ tier-3+4: 1240 → Haiku 13 batches × 4 问语义筛
L2 Step 5 Layer 3 (Haiku 4.5): 1240 → 590 keep + 175 keep_weak + 475 cut
       ↓ 通过率 47.6% (590/1240)
L2 Step 5 final: master v0 = 76 direct + 590 Haiku keep = 666 词
       ↓ source: 02-expanded-keywords.md L1-719
L3 主库打分: 666 → 去重 570 → 6 维度 13 分公式 → Tier 1/1.5/2/3
       ↓ KWFinder paid 570/570 全量化(Vol/KD/Growth/Intent/SERP)
       ↓ source: 03-master-scored.md L1-264 + data/master_scored.json
L5 Pillar/Cluster: Tier 1 6 + Tier 1.5 58 + Tier 2 88 → 选 15 词(3 Pillar × 5 Cluster)
       ↓ source: 04-pillar-cluster.md (新生成)
```

## 3 · 三 Pillar 决策(A+B+C 全做)

### Pillar A · Answer Engine Optimization (AEO)

**Thesis**:AI 搜索时代的 SEO — 从'被 Google 排名'转向'被 ChatGPT/Perplexity/Google AI Overview 引用'。
**ICP**:SaaS 产品经理、SEO 从业者、内容创作者
**产品对接**:YOLOX agent 可帮内容自动检测 AEO 信号(llms.txt/schema/citations)并生成优化建议

**Pillar 主词**:`Answer Engine Optimization`
- Tier Tier 1 (得分 10/13)
- 数据:V=2100, KD=50, Growth=200%, Intent=informational
- 索引:`03-master-scored.md` L37+4 | `02-expanded-keywords.md` L120+20 | `01-seed-keywords.md` L92

**5 Cluster**:

| # | 关键词 | Tier | V | KD | Growth | 决策依据 | 主库索引 |
|---|---|---|---|---|---|---|---|
| A1 | `answer engine optimization services` | Tier 1 | 350 | 19 | 909% | shoulder commercial — 极低 KD + 爆发增长,蓝海 | L42 |
| A2 | `Generative Engine Optimization` | Tier 1 | 4800 | 66 | 180% | alternative concept,GEO 在 Google 内部生态有差异化 | L40 |
| A3 | `google ai overview` | Tier 2 | 22500 | 68 | 100% | Google specific,大流量但 KD 偏高 | L95+1 |
| A4 | `llms.txt SEO` | Tier 1.5 | — | — | — | 技术实现层(ICP 长尾,但社区真实存在) | L94 |
| A5 | `why ChatGPT cites pages` | Tier 1.5 | — | — | — | informational long-tail(博客金字塔底层) | L65 |

### Pillar B · AI Agent 开发栈 (Model Context Protocol & Claude)

**Thesis**:Agent 开发标准化 — MCP/Claude agent skills 是 2026 年的 React/Vue,开发者必学。
**ICP**:独立开发者、技术 founder、AI 应用开发者
**产品对接**:YOLOX 本身是 agent team SaaS,这部分是技术权威 + 给我们的 agent store 引流

**Pillar 主词**:`Model Context Protocol`
- Tier Tier 1 (得分 9/13)
- 数据:V=21500, KD=55, Growth=-35%, Intent=commercial, informational, transactional
- 索引:`03-master-scored.md` L38 | `02-expanded-keywords.md` L119 | `01-seed-keywords.md` L88

**5 Cluster**:

| # | 关键词 | Tier | V | KD | Growth | 决策依据 | 主库索引 |
|---|---|---|---|---|---|---|---|
| B1 | `ai coding agent` | Tier 2 | 3000 | 45 | 1236% | 大流量(V=3000) + 极高增长(+1236%) — 必投 | L115 |
| B2 | `Claude agent skills` | Tier 1.5 | — | — | — | ICP 长尾,但 Claude skills 生态在爆发期 | L93 |
| B3 | `Claude Code workflow` | Tier 1.5 | — | — | — | ICP 长尾,Claude Code 用户教程刚需 | L92 |
| B4 | `ai agents for project management` | Tier 2 | 120 | 25 | 158% | ICP 直击 + KD 25 友好 | L120 |
| B5 | `ai agent for code review` | Tier 2 | — | 34 | — | ICP 直击,V 空但 KD=34 + 真实社区帖文证据 | L144 |

### Pillar C · SMB AI 工具直击 (AI app builder & 衍生)

**Thesis**:中小企业'非技术'用户用 AI agent 替代专业工具(设计/proposal/广告) — 这是 YOLOX 的 ICP 主战场。
**ICP**:中小企业主、咨询顾问、自由职业者、内容创作者
**产品对接**:YOLOX agent store 直接对接 — 每个 Cluster 词能挂一个或多个 product agent

**Pillar 主词**:`AI app builder`
- Tier Tier 1 (得分 9/13)
- 数据:V=9600, KD=47, Growth=305%, Intent=navigational
- 索引:`03-master-scored.md` L39+1 | `02-expanded-keywords.md` L45+17 | `01-seed-keywords.md` L31+2

**5 Cluster**:

| # | 关键词 | Tier | V | KD | Growth | 决策依据 | 主库索引 |
|---|---|---|---|---|---|---|---|
| C1 | `AI infographic generator` | Tier 1 | 1700 | 37 | -40% | Tier 1 (V=1700, KD=37) — 设计场景 ICP | L41 |
| C2 | `AI proposal generator` | Tier 2 | 530 | 34 | -50% | consultant/freelancer ICP, V=530 | L117 |
| C3 | `AI ad creative generator` | Tier 2 | 60 | 45 | 75% | PPC agency ICP, +75% 增长 | L121 |
| C4 | `AI newsletter writer` | Tier 2 | 10 | 30 | -67% | creator ICP, KD=30 友好 | L141 |
| C5 | `Marketing & Growth AI agents` | Tier 1.5 | — | — | — | ICP 长尾,直接对接 agent store 'Marketing' 分类 | L90 |

## 4 · 数据质量与可信度

| 维度 | 状态 | 证据 |
|---|---|---|
| 主库覆盖 | 570/570 词 KWFinder 全量化 | `data/master_scored.json` 字段 has_kwf 全 true |
| 长尾未量化 | 58 词(Tier 1.5) | 来自 Reddit/Quora/IH 真实帖文 — `01.5-pool-c-raw.md` 903 帖原料可追 |
| Haiku 4-yes 通过率 | 47.6% (590/1240) | 4 问标准:真问题/产品能解/搜索形/ICP 25-list,`pool_v2_haiku_verdicts.json` 可审计 |
| KD 极低 + 高增长词 | 1 词(AEO services KD=19, +909%) | `03-master-scored.md` Tier 1 #6 |
| KD<30 + 真 ICP 词 | 7 词(ai agents for project management 等) | Tier 2 top 30 |

## 5 · 风险与隐忧

| 风险 | 严重度 | 现状 | 缓解 |
|---|---|---|---|
| 🐛 KWFinder 70% ICP 长尾词无 Volume | 中 | 已识别 | Tier 1.5 单列,L6 大纲依赖 ICP 匹配度而非 Vol |
| 💸 KWFinder 48h 退款窗口 | 高 | $39 已支付 | **5/9 18:00 前必须取消订阅** — 我做 L6/L7 期间需 leader 通知小刀老师 |
| 🔑 内部 agent 人名(坑 6.5) | 低 | Layer 2 黑名单已过滤 | `step5_funnel.py:38-47` 50 个 hero name 全黑 |
| 🗑 主库 100% 工具自动化产出 | 中 | Tier 1 + Tier 1.5 共 64 词需 sanity check | **本审核环节由 leader 把关** |
| 🐛 Pillar B 流量集中在 MCP/Claude | 中 | KD 普遍 50+ | 5 Cluster 中 3 个 ICP 长尾(Tier 1.5)对冲 |
| 🐛 Pillar C 5 Cluster 同型(`AI X generator`)模板化 | 低 | ICP 不同(consultant / PPC / creator / 设计 / agent store) | L6 大纲会按 ICP 角度差异化撰写 |

## 6 · 待办(L6/L7,leader 审核通过后启动)

| Layer | 任务 | 输出 | 工时 |
|---|---|---|---|
| L6 | 6 篇博客大纲(从 15 词中选 6 个 Cluster + 部分 Tier 1.5 长尾) | H2/H3 + 字数估计 + Search Intent + 内链 | 3-4h |
| L7 | 精排 + handoff final | 含 6 篇大纲产出顺序 + 内链矩阵 + 下一轮研究方向(Round-3 提案) | 1h |
| 副 | git commit + push 到 feat/seo-keyword-research | PR 描述 + 文件清单 | 30min |

## 7 · Leader 审核 checklist(建议)

- [ ] **Pillar 战略**:A+B+C 全做合理? 还是聚焦其中 1-2 个?(预算/带宽考虑)
- [ ] **Pillar A**:AEO 是否符合公司主线? 还是 GEO 更稳妥?
- [ ] **Pillar B**:MCP/Claude 技术权威路线 vs 我们 SMB 客群是否错配?
- [ ] **Pillar C**:5 Cluster 中 'Marketing & Growth AI agents' 直接挂 agent store 分类页 OK 吗?
- [ ] **Tier 1.5 ICP 长尾**:58 词无 Vol 数据,是否接受'依赖社区证据'的判断?
- [ ] **预算**:KWFinder $39(48h 退款)是否退? 还是续订做 Round-3?
- [ ] **时间表**:L6/L7 5/9 前完成 OK?(配合 KWFinder 退款窗口)
- [ ] **Round-3 方向**:SERP intent 二次校验 + 真竞品反查(用付费 Ahrefs/Semrush trial)?

## 8 · 附录:工具与脚本清单

```
scripts/
  capture_reddit.py            — Reddit 公共 API 抓取(131 runs)
  capture_quora_ih.py          — Quora/IH via Google site:
  capture_ih_retry.py          — 慢速 IH retry (100-130s 防 ban)
  layer1_filter.py             — Layer 1 机械过滤
  layer2_curate.py             — Layer 2 4 问真筛(由我执行)
  step5_suggest_validate.py    — Step 5 product semantic 验证
  step6_emerging_scan.py       — Step 6 8 渠道新兴生态扫
  build_pool_a.py              — Pool A 76 词 markdown 渲染
  step1_promote_apply.py       — L2 Step 1 升级落地
  step2_safe_suggest.py        — Step 2 4 渠道 Suggest
  step3_poolb_suggest.py       — Step 3 Pool B 广扫
  step5_funnel.py              — Layer 1+2 漏斗机械筛
  prepare_haiku_batches.py     — Haiku 13 batches 拆分
  build_master_v0.py           — master v0 666 词渲染
  generate_kwfinder_batches_200.py — KWFinder paid 200/CSV 拆分
  l3_score_master.py           — L3 6 维度 13 分打分(本轮主交付)
  l5_pillar_cluster.py         — L5 Pillar/Cluster + handoff(本文档生成)
```

---

**审核反馈渠道**:在本文档下方批注 / 直接回复小刀老师 / GitHub PR comment
**预期反馈时间**:审核完成后启动 L6/L7,我侧 4-6h 完成最终交付
