# Round-2 关键词研究 · 文档导航

> **日期**:2026-04-28 启动 / 2026-05-08 主体完成
> **作者**:小刀老师 + Agent B
> **状态**:🟡 主体研究完成 · 4 Pillar × 20 Cluster 架构 final · 25 篇博客大纲 ship · 等待 Round-3 实施

---

## 🎯 团队 review 入口 → `0-share/`

如果你是第一次进来 review,直接看 [`0-share/`](./0-share/) 文件夹:

- **[`0-share/keyword-coverage.md`](./0-share/keyword-coverage.md)** — 关键词使用全景(570 词分类 + Round-3 候选)
- **[`0-share/frontend-spec.md`](./0-share/frontend-spec.md)** — yolox blog 前端调整需求(P0 / P1 / P2)

---

## 📁 详细 reference 文档 → `_process/`

team review 后想深挖时看(已 Ben reviewed,作为 evidence chain 保留):

| 文件 | 内容 |
|---|---|
| [`_process/03-master-scored.md`](./_process/03-master-scored.md) | L3 主库 6 维度打分 · 570 词 Tier 1/1.5/2/3 分档 |
| [`_process/04-pillar-cluster.md`](./_process/04-pillar-cluster.md) | L5 v2.1 · 4 Pillar × 20 Cluster 架构(已 ship 进度 update) |
| [`_process/99-handoff-leader-review.md`](./_process/99-handoff-leader-review.md) | Leader 审核版 · 精确索引证据链(Ben reviewed) |

---

## 📚 25 篇 blog 大纲 → `blog-outlines/`

[`blog-outlines/`](./blog-outlines/) 25 篇大纲:
- 4 Pillar 主文(`L6-00-pillar-*.md`)
- 21 Cluster 文章(`L6-01.md` ~ `L6-21.md`,L6-06 双重身份)

---

## 📊 结构化数据 → `data/`

| 文件 | 内容 |
|---|---|
| `data/master_scored.json` | 570 词 KWFinder 全数据 + 6 维度打分 |
| `data/pool_v2_*.json` | Pool A 76 + Haiku Layer 3 verdicts |
| `data/Data_Gotted/` | 原始 KWFinder export(4 个 paid + 1 个 recovered)|

---

## 🔧 脚本 → `scripts/`

12 个 Python 脚本(漏斗 / 打分 / Pillar/Cluster 决策 / coverage 分析)

---

## 📂 过程文档 → `_process/`

[_process/](./_process/) 历史中间产出 — 通常不需要看,作研究 trail 保留:
- 7 个 plan 文档(L0-L7)+ BOOT-PROMPT / HANDOFF
- 7 个中间产出(seed / pool / watchlist / master v0 / promote-updates 等)
- `_drafts-deprecated/` 3 个废弃方案文档(早期 Ahrefs / Semrush 评估)

---

## 🚦 当前状态 · Round 进展

| Round | 范围 | 状态 |
|---|---|---|
| Round-1 | 24 ICP 种子 + Pool A 66 词 + 12 篇博客大纲 | ✅(`archive/round-1/`) |
| **Round-2(本期)** | 570 词主库 + 4 Pillar × 20 Cluster + 25 篇大纲 | ✅ |
| Round-3 | Ben 锁定 6 篇快赢写 markdown + 设计另 20-30 大纲 | ⏳ |
| Round-4+ | 全量 ship | ⏳ |

---

## 📌 待办(下一阶段开始前需完成)

- [ ] 团队 review `0-share/keyword-coverage.md`,标 🟢 A / 🟡 B / ⚪ C
- [ ] 前端按 `0-share/frontend-spec.md` 实施 P0 模块(估 ~10h)
- [ ] Round-3 启动:写 6 篇 markdown(L6-01 / L6-02 / L6-03 / L6-04 / L6-05 / L6-06)
- [ ] KWFinder 5/9 18:00 前退订(已用 paid 跑完 570 词,无续订必要)
