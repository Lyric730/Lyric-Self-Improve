# 0-share · 团队 review 重点文件夹

> 这个文件夹是 **Round-2 研究中需要团队协作 / 决策的核心产出**。
> 不需要看其他文件夹的细节,这里是 entrance。

---

## 📋 文件清单

| 文件 | 内容 | 谁要看 |
|---|---|---|
| [`keyword-coverage.md`](./keyword-coverage.md) | 570 词使用全景:24 已用 / 546 未用 / Round-3 候选分类 | 小刀老师 / Ben / Product |
| [`frontend-spec.md`](./frontend-spec.md) | yolox blog 前端 P0/P1/P2 调整需求 | 前端开发 / Tech lead |

---

## 🎯 团队待办(2 件事)

### 1.关键词分类(小刀老师 + Ben)

打开 [`keyword-coverage.md`](./keyword-coverage.md),为以下 4 个 Pillar 下的 top 30 词各标:

- 🟢 **A 类**:有 yolox 已 ship / 即将 ship 的 agent 对接 → Round-3 直接出 cluster 文章
- 🟡 **B 类**:词热度好,但 yolox 暂无对应 agent → 需要做新 Skill / Agent
- ⚪ **C 类**:跳过(主题偏离 ICP / 词义不合适)

完成后 A 类词排 Round-3 写作 sequencing,B 类词同步给 product 团队。

### 2.前端 ship spec(前端开发 + 小刀老师)

打开 [`frontend-spec.md`](./frontend-spec.md):

- **P0** 必做(~10h)— 阻塞第一篇 blog 上线
- **P1** 强烈推荐(~7h)— 放大 SEO 价值
- **P2** 锦上添花 — Round-3 / Round-4 再做

文档末有 minimum spec 可直接抄给前端。

---

## 🔗 上下文文档(深挖时看 · 在 `_process/` 或 `blog-outlines/`)

- [`../_process/03-master-scored.md`](../_process/03-master-scored.md) — 570 词主库 + Tier 分档
- [`../_process/04-pillar-cluster.md`](../_process/04-pillar-cluster.md) — 4 Pillar × 20 Cluster 架构
- [`../_process/99-handoff-leader-review.md`](../_process/99-handoff-leader-review.md) — Leader 审核版(Ben 已 review)
- [`../blog-outlines/`](../blog-outlines/) — 25 篇 blog 大纲设计稿
