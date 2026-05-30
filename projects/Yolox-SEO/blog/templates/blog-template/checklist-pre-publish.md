# 发布前 checklist

> 一篇文章 drafting 完 + 隔 24h 后，逐项检查。
> **必须 18 项**全 ✅ 才允许 ship。建议 13 项尽量过。

---

## 必须 18 项（不过不 ship）

### A · brief & 素材（2 项）
- [ ] **M1** brief 必填 6 项全 ✅，素材池齐（≥2 case + ≥3 data + ≥1 quote）
- [ ] **M2** 所有 case / data / quote 都带原文链，原文链可点开（无 404）；找不到原文的 stat 必须改写为 "industry anecdotal estimate" 不留模糊归属

### B · 字数 & 结构（3 项）
- [ ] **M3** 字数在 type 规定区间（参考主模板 §3 表格）
- [ ] **M4** H2 数量 + 顺序符合 type 骨架（参考 type-X.md）
- [ ] **M5** 段落长度 50-150 字 / 3-5 句，无超 400 字段（最多 1-2 个长段例外）

### C · 内容质量（3 项）
- [ ] **M6** 每个 H2 ≥1 evidence（case/data/quote）+ ≥1 actionable step
- [ ] **M7** citation 钩子密度 ≥1/千字（2500 字 → ≥3 个可引 stat/quote）
- [ ] **M8** 视觉元素密度 ≥1/400-500 字（表 > 列表 > 图）

### D · SEO 落地（3 项）
- [ ] **M9** 主词出现位置全 ✅：title（**≤60 chars**）/ H1 / 首段 / URL / meta（**≤155 chars**）/ 至少 1 个 H2
- [ ] **M10** 内链 5-8 个，silo 内 ≥3 个，锚文本 30/30/30/10 分布。**yolox 内部 product 链**（agent/skill/team/category）**必须**来自 [`url-inventory.md`](./url-inventory.md)（不允许凭记忆/猜 slug）+ 用完整 `https://yolox.ai/...` 形
- [ ] **M11** 外链 ≥3 个权威源（**≥2 条必须 🟢 强权威** — 第一手研究 / 业界领袖个人 blog / 官方文档，详见 [`routing-matrix-v0.5.md §4`](./routing-matrix-v0.5.md)）+ meta description ≤155 chars + 含主词

### E · AEO 落地（2 项）
- [ ] **M12** chunk 自包含 ✅（随机抽 3 段，单独读得懂 = pass）
- [ ] **M13** TL;DR / Answer-first（Pillar / Buyer's / How-to / Definition 必含），1 屏内可见

### F · 前端 frontmatter & yolox 嵌入（1 项）
- [ ] **M14** frontmatter 字段齐：title / slug / silo / type / author / author_avatar / author_linkedin / date / last_updated / description / tags / toc / schema_type；**`author_linkedin` 必须是真 URL 不是 TBD**；**slug 必含主词全名或核心副词**；yolox product mention ≤3 处

### G · 编辑纪律（1 项）
- [ ] **M15** **drafting 完已隔 ≥24h** 才进入编辑

### H · CTA / 日期 / 图片（3 项 — v0.6 升必须）
- [ ] **M16** CTA ≥3 处布点（intro 末软 / 中段 / 结尾硬），不只结尾 1 处
- [ ] **M17** `last_updated` 字段改到今天（每编辑 1 次同步改）；文内日期写 "YYYY-MM" 精确到月，不用 "YYYY-Q"
- [ ] **M18** ≥1 个图片占位（hero / 信息图 / 截图）。即使设计未完成，必含 `[INSERT IMAGE: <详细 prompt>]` 标记给设计师；占位 0 张 = 不允许 ship

---

## 建议 13 项（应过，不强卡）

### I · 标题 & intro（3 项）
- [ ] **S1** title 含 1 个 buyer-stage hook 词（cost / 2026 / DIY / vs / best）
- [ ] **S2** intro 字数符合 type（Beginner's 250-300 / Contrarian 100-150 等）
- [ ] **S3** intro 用了对应 type 的公式（PSP / 双层 / 学习点 map 等）

### J · 数据时效 & EEAT（2 项）
- [ ] **S4** 数据全部 2024-2026，2023 之前的已标 "（XX 年数据，可能已变）"
- [ ] **S5** 至少 1 个 first-hand 视角（yolox 实战 / 我们的 case / 不是网上抄）

### K · 关键词嵌入（3 项）
- [ ] **S7** 主词密度 0.5%-1.5%（不堆砌，不缺漏）
- [ ] **S8** 5-8 个副词每个 ≥1 次自然嵌入
- [ ] **S9** 5-8 个 LSI 散布全文

### L · 视觉 & 多模态（2 项）
- [ ] **S10** 至少 1 个表（LLM 最易引）
- [ ] **S11** 所有图都有 alt text，alt 含主词或同义词

### M · 内链（1 项）
- [ ] **S13** Continue Reading 推荐 silo 内 ≥2 篇相关文章

### N · 风格 & 可读性（2 项）
- [ ] **S14** 没有"上面说过 / 如前所述"等违反 chunk 自包含的表述
- [ ] **S15** 全文不出现 "based on / according to my understanding" 等 LLM 招牌句

---

## 一键命令（dogfood 后实现）

```bash
# 未来想做的：自动跑这个脚本，输出 checklist 报告
npm run blog:check L6-01.md
```

v0.5 阶段：**人工逐项过**。R3 ship 完后做自动化（v1 计划）。

---

## 出错怎么办

| 必须项不过 | 怎么修 |
|---|---|
| M1（素材不齐） | 回 brief，补素材后重写 H2 |
| M3（字数不够 / 超） | 删水段 / 补 case；不要硬凑字数 |
| M5（段过长） | 拆段，加视觉元素切分 |
| M6（H2 无 evidence） | 从素材池里调 1 个 case/data 嵌入 |
| M12（chunk 不自包含） | 改段首句，加自释 |
| M15（24h 没过） | **等够 24h 再编辑**，不要捷径 |
