# L6-01 · `answer engine optimization services` · 大纲(设计稿)

> **状态**:v0 sample · 待小刀老师 + Ben 复审 → 通过后批量做剩 5 篇
> **日期**:2026-05-07
> **作者**:Agent B
> **优先级**:Ben 锁定 #1(α6 cluster anchor)
> **发布形态**:yolox 官网 blog · 标题 + markdown 正文 + 图(可选)

---

## 0 · 元数据

| 字段 | 值 | 索引 |
|---|---|---|
| 关键词 | `answer engine optimization services` | `data/master_scored.json` |
| Volume | 350(月均) | KWFinder |
| KD | **19**(极低) | KWFinder |
| Growth | **+909%** YoY | KWFinder |
| Search Intent | (KWFinder 未填) → 我判断为 **Commercial buy intent** | 推断:含 "services" 后缀 |
| Tier | Tier 1 (9/13) | `03-master-scored.md` |
| SERP Features | **AI Overview 占位** ⚠️ | KWFinder Serp Features 字段 |
| Pillar/Cluster | **α6**(α · AI 工具替代专业岗位 · 第 6 cluster) | `04-pillar-cluster.md` |
| 发布 URL | **`/blog/aeo/services-guide`**(嵌套 silo) | 5/7 决策 |
| 落地 CTA | → `/agents-store`(暂总店,后续有具体 agent 再回改) | Ben PR #14 + 5/7 决策 |

---

## 1 · ICP 定位 + 痛点 hypothesis

### 主 ICP
**marketer / SMB owner / 内容运营**听说了"AI 搜索来了"和"Google AI Overview 抢流量",想找服务做 AEO 但自己不懂技术细节,**正在评估要不要花钱外包**。

### 次 ICP
**in-house SEO manager**:被老板要求"我们也得做 AEO",在做 vendor evaluation。

### 痛点 hypothesis(待 Reddit/Quora 帖文佐证,我会在 L6 收尾时补 2-3 条原话)
1. 不知道 AEO vs SEO 差别在哪 — 需要 services 还是自己改改 meta 就行?
2. Google AI Overview 已经抢了 30%+ 的 click(数据来源:SparkToro 2025 study) → 老板要求"补救"
3. 不知道 AEO services 收费 — $500/月 起还是 $5000/月起?
4. 不知道找谁做 — 老 SEO agency 转型的 vs 新 AEO-first 公司哪个更靠谱?
5. 自己跑过 ChatGPT 引用源,发现引的都不是自己网站 — 不知道为什么

### 现有解决方案为什么不够
- 老 SEO agency 给的 AEO 方案 = old SEO + sprinkled "AI"(噱头)
- AEO-first 服务费用高 + 不透明($5k-15k/月)
- DIY 没工具、没经验、没时间

---

## 2 · SERP 当前格局(基于 KWFinder Serp Features + 推断)

| 信号 | 解读 |
|---|---|
| **AI Overview 占位** | Google 在 SERP 顶部直接给答案,organic CTR 会下降 30-50% |
| KD=19 | top 10 是 long-tail content,**主要是 SEO 博客 + AEO 创业公司 landing 页** |
| Volume 350 + Growth +909% | 词刚崛起 12 个月,头部内容**还没沉淀**(老内容 KD 应早就 > 30) |

### 内容空缺(我们的差异化机会)
- 大多 top 10 是"卖 AEO services"的 landing page(销售口吻),不是教育内容
- 缺一篇 **"how to evaluate AEO services + DIY 最低门槛 checklist"** 的中立指南 → 我们能占这个位置
- AI Overview 引用源 = 信号清晰、列表化、有结构化数据的页 → 我们的文章设计要让 LLM 容易 "拎出引用"

### 待小刀老师 / Ben 手工查证
- 跑一次 google.com/search?q=answer+engine+optimization+services
- 截 top 5 标题 + URL
- 我会在批量做 6 篇时统一收 SERP 数据(或你定个时间窗,一次跑完)

---

## 3 · 文章结构(写作图纸,非最终发布版)

### 标题候选(3 个)
1. ⭐ **"Answer Engine Optimization Services: What They Cost, What They Deliver, and When You Don't Need One (2026 Guide)"**
2. "AEO Services Explained: A Marketer's Guide to Pricing, ROI, and DIY Alternatives"
3. "Should You Hire an AEO Service in 2026? A Buyer's Guide for SMBs and In-House Teams"

> 推荐 #1:含 "services" + "cost" + "DIY" 三个 buyer-stage 信号词,LLM 容易识别为 buyer's guide

### H2 / H3 结构(7 个 H2)

```
H1: Answer Engine Optimization Services: What They Cost, What They Deliver,
    and When You Don't Need One

[TL;DR 引用框 · 80 字] AEO services 帮你的网站被 ChatGPT/Perplexity/Google AI
Overview 引用为答案。$500-15k/月,自己也能做基础项。本文给你 services 拆解 +
DIY checklist + 何时该外包的决策框架。

H2.1 · What is AEO (and why it's different from SEO)
  H3 · AEO 一句话定义
  H3 · vs SEO:目标从"排名"变成"被引用"
  H3 · 数据:Google AI Overview 已占 SERP 35%+(SparkToro 2025)

H2.2 · What does an AEO service actually do?
  H3 · 6 项核心交付物 checklist
       - Citation audit(谁在引用你/竞品)
       - Schema markup 加固
       - llms.txt + AI crawler 配置
       - Content restructuring(LLM 友好的 H2/H3 + 列表化)
       - FAQ + entity 标注
       - 月度 LLM 引用报告
  H3 · 6 项 services *不该* 收钱做的事(老 SEO agency 重定向常见骗局)

H2.3 · Pricing tiers · 真实价格分布
  H3 · DIY tier($0,1-2 周自己摸):适合 SMB owner / solo
  H3 · Boutique tier($800-2,500/月):2-3 人 AEO-first 公司
  H3 · Agency tier($3,000-8,000/月):老 SEO agency 转型,人多服务广
  H3 · Enterprise tier($10k-25k/月):专做 Fortune 1000,不适合 SMB

H2.4 · DIY 最低门槛 checklist(把 80% 价值自己拿到)
  H3 · 1 小时内能做的 5 件事(llms.txt / schema / FAQ / entity / sitemap 优化)
  H3 · 1 周能做的 3 件事(content restructure / citation audit / FAQ 全站铺)
  H3 · 跨过这 3 道坎才需要找 services(规模 / 多语言 / B2B 复杂 funnel)

H2.5 · How to evaluate an AEO service · 5 个问题问 vendor
  H3 · "show me your last 3 client citation lift screenshots"(看真实数据)
  H3 · "do you do content writing or only audit"(知道 scope)
  H3 · "how do you measure results"(避免 vanity metrics)
  H3 · "what's your pivot from SEO"(老 SEO agency 转型 vs AEO native)
  H3 · 月度报告 sample(看是否真的看 AI engines)

H2.6 · Red flags · 4 种该 walk away 的 pitch
  H3 · "We guarantee #1 in ChatGPT"(没人能 guarantee)
  H3 · 全包 $99/月(底层是 outsourced 模板)
  H3 · 不给月度报告(看不到效果)
  H3 · 拒绝跑 baseline citation audit(怕暴露起点)

H2.7 · When to skip AEO services entirely
  H3 · 月流量 < 5,000 时:DIY 时间投入 > services 月费
  H3 · 不卖给 marketers/SMB(B2B niche 受 AI 影响小):暂时不需要
  H3 · 已经有 strong SEO baseline 时:加 schema + llms.txt 就够

CTA(留引子,不强制 gate):
"想跑一次免费 AEO audit?yolox 正在开发 AEO audit agent — 自动检测
你的 llms.txt / schema / citation lift,生成优化建议清单。alpha 阶段,
[关注更新 → /agents-store](#)。"

FAQ(为 PAA 优化,触发 FAQ schema 自动生成)
- Q1: How much do AEO services cost?
- Q2: Can I do AEO myself?
- Q3: What's the difference between SEO and AEO?
- Q4: How long does AEO take to show results?
- Q5: Do I need both SEO and AEO services?
```

### 字数预估
- H1 + TL;DR: 100 字
- 7 H2 各 250-400 字 = 2,000 字
- DIY checklist + pricing tiers 表格 = 300 字
- FAQ 5 条 × 50 字 = 250 字
- CTA(留引子)= 50 字
- **总:2,500-2,800 字**

> 中型权威文章,KD=19 + 词龄短,2-3 个月内有机会上首页

---

## 4 · 内链规划

### 上行(到 Pillar 主词文章 — Round-3 再写)
- → `Answer Engine Optimization`(Pillar 主词,目前未写,文章末预埋占位 anchor)

### 横向(同 Pillar 内其他 cluster 文章)
- → `cold email deliverability`(L6-04)— 在 H2.4 DIY checklist 节末提:"想看更多 evergreen 优化的实战案例?cold email deliverability 也是被 AI Overview 顶替的高风险类目"
- → `AI proposal generator`(L6-03)— 在 H2.7 时点到:"如果你做的是 SMB consultant 业务,与其自己手写 proposal 不如先把 proposal 流程 AI 化"

### 下行(到 agent store / product page)
- → `/agents-store`(待开发,埋占位 anchor)
- → `/agent-store`(总店,在 CTA 旁加 secondary link)

### 外链(权威信源,提升 LLM 引用概率)
- SparkToro 2025 AI Overview impact study
- Google Search Central · structured data docs
- Schema.org · FAQ schema spec

---

## 5 · 落地 CTA 详解

### 主 CTA(文末)
**纯 markdown link + 引子段**(无邮箱表单):

```markdown
> 想跑一次免费 AEO audit?yolox 正在开发 AEO audit agent — 自动检测
> 你的 llms.txt / schema / citation lift,生成优化建议清单。
> alpha 阶段,[关注更新 →](/agents-store)
```

### 次 CTA(中段穿插,2 处)
- H2.4 DIY checklist 末:"懒得自己跑 schema audit?[试试 yolox AEO audit agent →](/agents-store)"
- H2.5 evaluate vendor 末:"想要一份 AEO vendor evaluation 模板?[加入 alpha 等候名单 →](/agent-store)"

### 引子设计(soft lead gen,符合"先 A 留引子")
- 不强制邮箱 gate
- 但每次 CTA 都指向 agent store 的"alpha 等候页",用户主动点击 = soft opt-in
- agent store 自己有"关注 / 通知我上线"按钮(若已实现) → 转化 lead

---

## 6 · 成功指标(Ben 在 PR comment 要求标注)

### Primary · Search Console
| 时间窗 | 目标 |
|---|---|
| 4 周 | 首次 impression(Google index 完成) |
| 8 周 | impressions > 200/月 + clicks > 30/月(正常 CTR 15%) |
| 12 周 | top 5 排名 + clicks > 80/月 |
| 16 周 | top 3 + 月度 clicks > 150 |

### Secondary · GA4 events(需提前注册)
| Event | trigger | 期望值(12 周) |
|---|---|---|
| `blog_view` | 文章页浏览 | 600+/月 |
| `blog_scroll_75` | 滚动到 75% | 240+/月(40% scroll-through) |
| `internal_link_click_agent_store` | 点击文末 CTA | 60+/月(10% CTR) |
| `internal_link_click_blog` | 点击横向链接(L6 其他文章) | 30+/月 |

### Tertiary · LLM 引用监测(AEO 专属指标)
| 检查源 | 频率 | 目标(12 周) |
|---|---|---|
| ChatGPT 搜 "AEO services" | 月 | 至少 1 次被引用 |
| Perplexity 搜 "AEO services" | 月 | top 5 来源里有我们 |
| Google AI Overview 占位 | 月 | 8 周后开始扫,12 周时被引用 |

---

## 7 · 风险与隐忧

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 🐛 AI Overview 抢流量 | 中 | 文章主战略 = 被 AI 引用,不是 organic 排第一(转化路径靠 CTA + agent store) |
| 🗑 AEO audit agent 没 ship 时 CTA 是死链 | **高** | 文末"alpha 关注页"提前部署,即便 agent 没上,先收 lead |
| 💸 SparkToro 数据已过期 | 低 | 写文章前 fact-check 一次,如有更新数据替换 |
| 🐛 12 周排名不达目标 | 中 | 有 Search Console 周度数据可早判,8 周如还在 100+ 名说明 word 选错或内容问题,需复盘 |

---

## 8 · 待小刀老师 / Ben 复审 checklist

- [ ] **战略**:文章核心 thesis "AEO services 中立买家指南"(不卖货)是否符合 yolox 内容定位?
- [ ] **ICP**:主 ICP 锁 marketer/SMB 是否准确?(vs in-house SEO)
- [ ] **CTA**:agent store "alpha 等候" 是当前能做的 CTA 形态吗?(还是直接 /agent-store 总店即可)
- [ ] **字数**:2,500-2,800 字 OK?(KD=19 中等竞争通常 2,000-3,000 合适)
- [ ] **结构**:7 H2 + 5 FAQ 是否过满?要不要砍 1-2 个?
- [ ] **数据**:SparkToro 2025 AI Overview study 引用 OK?(我会写文章前 fact-check 链接)
- [ ] **成功指标**:Ben 提的 GA4 events,这 4 个事件你的 GA4 已注册吗?
- [ ] **agent CTA URL**:`/agents-store` 是预期的路由吗?

---

## 9 · 下一步

如果这个大纲格式 OK → 我立即批量做剩 5 篇(L6-02 到 L6-06)。

如果格式要调整 → 你 + Ben 反馈,我改完再做剩 5 篇。

⏱️ 工时估计:
- 1 篇大纲 ~30-40min
- 6 篇 ~3-4h
- 我能今晚 + 明天上午做完
