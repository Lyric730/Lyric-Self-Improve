# 05 · 零量词策略 · Day 4 产出

**创建**：2026-04-24（Day 4）
**对应 playbook**：§2.3.4 零搜索量关键词策略 + §2.3.5 Keyword Map
**交付等级**：🟡 可用（指导下周博客选题）
**学习目标**：**小刀老师读完本文档能独立判断哪些 Reddit 问句值得做博客**（playbook §4.1 DoD）

---

## 0 · 本文档对小刀老师是什么

不是"30 个词的罗列"，是**一套博客选题的判断纪律** + **30 个已筛选好的第一批狙击词**。

读完你应该能回答：
- 新来 1 个 Reddit 问句，要不要写博客？
- 怎么看一个词值不值得占位？
- YOLOX 零流量期的内容节奏怎么走？

---

## 1 · 什么是"零量词"（60 秒讲完）

**零量词 = 月搜索量 < 10，或主流 SEO 工具查不到数据的搜索查询。**

不是"没人搜"，是"**搜的人太少，工具数据库没收录**"。

具体例子（本周真实数据）：
- `is llms.txt a scam` → Google Keyword Planner 显示 "---"（无数据）= 零量词
- `how to create llms.txt` → 50/mo（低量但有）= 低量词
- `AI agents` → 几千/mo（主流词）= 非零量

**零量词 ≠ 没价值**，原因在 §2。

---

## 2 · 为什么零量词对 YOLOX 有用（playbook §2.3.4 逻辑）

### 🟢 3 个优势

1. **竞争极低 = 新站能抢 Top 3**
   零量词 Google 往往只有 3-5 条相关结果，写一篇精准内容大概率 1-2 周就能排进第一页
2. **AI Overview 友好**
   ChatGPT / Perplexity / Claude 等 AI 搜索在 long-tail 查询上**直接引用博客段落**作为答案（见 handoff §4.1 Study of 1.4M Prompts 证据）
3. **用户意图纯净 = 转化率高**
   搜 `struggling to get consistent clients cleaning business` 的用户**明确知道自己要什么**，转化率远高于宽泛词

### 🔴 3 个陷阱（不讲清你会栽）

1. **零量 × 多 = 真的零流量**
   写 10 篇零量词博客、每篇 5/mo 搜索 = 月 50 访问。比单篇 1000/mo 的高量词糟糕得多
   **解法**：零量词必须**主题集群**写（Cluster 链接到 Pillar），靠**语义密度**获取 Google 对站点的"主题权威"判断
2. **零量 ≠ 一定零人搜，但也 ≠ 一定有人搜**
   有些零量词是 Claude 造的假词（YOLOX 内部 Agent 名 / tagline 反推），**真的没人搜**
   **本周教训**：我 Day 3 主库 C 类 Claude 造词 16 条里，GAKP 查出 14 条零量，真实命中率只 12.5%
3. **Reddit 问句 ≠ Google 搜索词**
   用户在 Reddit 写"How do I find out why people visited my website are not signing up?"（119 条评论热帖），但 Google 时会缩短成"why visitors not converting"或"website signup conversion"
   **解法**：Reddit 问句作为**痛点清单**用，不作为"Google 搜索词清单"——真正的搜索词要去 GAKP / 自动补全验证

---

## 3 · 本周数据真相 · GAKP 给的 brutal truth

Day 3 我产出了 200 词主库（04-keyword-map-v1.md），Day 3 结束你质疑其可信度。我们跑了 Google Ads Keyword Planner（免费工具）验证 217 词，结果反直觉：

### 3.1 核心数字

```
217 词粘进 GAKP
  ↓
  12 词返回 volume（全部 50/mo，已是最小可显示档位）
  205 词返回 "---"（低于 Google 可展示阈值）
```

**94% 词在 GAKP 眼中是零量**，符合 playbook "零流量期只打长尾"的预期，但**比我预测的更彻底**。

### 3.2 12 个有数据的词（意外 vs 证实）

| Cluster | 词 | Vol | yoy 同比 | 状态 |
|---|---|---|---|---|
| **C1** | what is llms.txt file | 50/mo | **+900%** | 🔥 爆发 |
| **C1** | llms.txt vs robots.txt | 50/mo | **+∞** | 🔥 爆发 |
| **C1** | llms.txt example | 50/mo | **+900%** | 🔥 爆发 |
| **C1** | llms-full.txt vs llms.txt | 50/mo | **+∞** | 🔥 爆发 |
| **C1** | how to create llms.txt | 50/mo | 0% | 稳定 |
| **C7** | **AI agents for solopreneurs** | 50/mo | **+∞** | 🔥 Pillar 候选主词 |
| C4 | seo for local service business | 50/mo | 0% | 稳定 |
| C2 | ai agent for keyword research | 50/mo | +∞ | 新兴 |
| C10 | ai consulting business ideas | 50/mo | +∞ | 新兴 |
| C4 | ai for small business automation | 50/mo | +∞ | 新兴 |
| C5 | ai for youtube scripts | 50/mo | 0% | 稳定 |
| **C6** | how to close more sales faster | 50/mo | **-100%** | 🔴 **衰退必降级** |

### 3.3 反直觉洞察

- 🔑 **C1 (llms.txt) 6/6 全部有量 + 多条爆发式增长**：主题生态真实，值得本周 ship 博客
- 🔑 **C7 Solopreneur Pillar 主词验证**：`AI agents for solopreneurs` 是目前唯一同时满足"有量 + 爆发 + YOLOX 整体强匹配"的 Pillar 候选
- 🔴 **`how to close more sales faster` yoy -100%**：Tier 1 #13 必须从主库降级
- 🔴 **C 类 Claude 造词 14/16 零量**：Day 5 Pillar 定稿时，不要用"AI X for Y"模板当主词

### 3.4 数据诚实边界

- GAKP 对新/不活跃账号给的是**区间中位**（"50/mo" = "10-100" 区间的中位数），不是精确值
- "---" = "低于 Google 展示阈值"，**不等于真零**；也可能是"词太新，Google 数据库没收录"
- 真·权威定量要等 Agent A 上线 GSC + Day 7 Ahrefs 批量补 KD

---

## 4 · 30 个第一批狙击词（密度表）

从 `03-reddit-quora-questions.md` 末尾预选表来。按 Cluster 重组 + 补每词"预期写什么"字段。

| # | 零量词 | Reddit URL | Cluster | YOLOX Agent | 预期写什么 |
|---|---|---|---|---|---|
| 1 | why ChatGPT cites one page over another | [r/SEO 1ss0drr](https://reddit.com/r/SEO/comments/1ss0drr/) | C1 | Sophie | **博客**（AEO 原理）|
| 2 | is llms.txt a scam | [r/SEO 1srvco1](https://reddit.com/r/SEO/comments/1srvco1/) | C1 | Sophie | **博客**（下周 #1 强候选）|
| 3 | how to structure headings for listicles | [r/SEO 1ss6uxv](https://reddit.com/r/SEO/comments/1ss6uxv/) | C5 | Isaiah | doc（不博客，原帖冷）|
| 4 | struggling to get consistent clients cleaning business | [r/smallbusiness 1srl89h](https://reddit.com/r/smallbusiness/comments/1srl89h/) | C4 | Elias | **博客**（SMB 高情感）|
| 5 | how to get more genuine Google reviews | [r/smallbusiness 1srnijf](https://reddit.com/r/smallbusiness/comments/1srnijf/) + [r/ContentMarketing 1srx6uo](https://reddit.com/r/ContentMarketing/comments/1srx6uo/) | C12 | Quinn | **博客**（2 帖交叉）|
| 6 | build AI workers in plain English | [r/Entrepreneur 1snchax](https://reddit.com/r/Entrepreneur/comments/1snchax/) | C7 | YOLOX 整体 | 🔴 **砍**（Anthropic 公告标语，非搜索 query）|
| 7 | open source social media scheduling alternative | [r/SideProject 1sk8fn3](https://reddit.com/r/SideProject/comments/1sk8fn3/) | C9 | Mia | 🔴 **砍**（show-off 帖意图颠倒）|
| 8 | best AI agent for Shopify store owner | [r/shopify 1srps0d](https://reddit.com/r/shopify/comments/1srps0d/) | C3 | YOLOX 平台 | **博客**（商业调查但 ICP 强）|
| 9 | how to reach Shopify store owners B2B | [r/shopify 1ss1lnw](https://reddit.com/r/shopify/comments/1ss1lnw/) | C3 | Daniel | doc（YOLOX GTM 内部用）|
| 10 | manage workflow made-to-order Shopify Etsy | [r/shopify 1srd6gf](https://reddit.com/r/shopify/comments/1srd6gf/) | C3 | 跨平台编排 | agent 详情页（连接器场景）|
| 11 | how to acquire customers for my SaaS | [r/SaaS 1srm4yl](https://reddit.com/r/SaaS/comments/1srm4yl/) | C4 | Elias | **博客**（41 comments 热帖）|
| 12 | how to do distribution for indie SaaS | [r/SaaS 1ss43uq](https://reddit.com/r/SaaS/comments/1ss43uq/) | C4 | Arlo + Quinn | **博客**（跨 Agent 协作案例）|
| 13 | why people visit website but don't sign up | [r/indiehackers 1smtafn](https://reddit.com/r/indiehackers/comments/1smtafn/) | C2 | Addison | **博客**（119 comments 超热）|
| 14 | help post product on Hacker News | [r/indiehackers 1srn06k](https://reddit.com/r/indiehackers/comments/1srn06k/) | C12 | Arlo | **博客**（发布场景具体）|
| 15 | how to market niche ecommerce products (grip socks) | [r/ecommerce 1ss81mp](https://reddit.com/r/ecommerce/comments/1ss81mp/) | C3 | Elias + Olivia | 博客（case study 形式）|
| 16 | traffic shift from Google to ChatGPT for ecommerce | [r/ecommerce 1srpe36](https://reddit.com/r/ecommerce/comments/1srpe36/) | C1 | Sophie (AEO) | **博客**（AEO + 电商交叉）|
| 17 | automate Shopify order tracking inquiries with AI | [r/ecommerce 1srh6iv](https://reddit.com/r/ecommerce/comments/1srh6iv/) | C3 | 客服 Agent | 🔴 **砍**（YOLOX 无对应 Agent）|
| 18 | AI driven team for luxury packaging design | [r/ecommerce 1srlppd](https://reddit.com/r/ecommerce/comments/1srlppd/) | C3 | Eli | agent 详情页（Eli × Shopify 场景）|
| 19 | AI for e-commerce customer questions | [r/ecommerce 1sr1zk5](https://reddit.com/r/ecommerce/comments/1sr1zk5/) | C3 | 客服 Agent | 🔴 **砍**（同 #17，无产品）|
| 20 | avoid scams on Etsy as seller | [r/Etsy 1sqnbwd](https://reddit.com/r/Etsy/comments/1sqnbwd/) | C3 | Evelyn | doc（防欺诈指南）|
| 21 | naturally get Google reviews without pressure | [r/ContentMarketing 1srx6uo](https://reddit.com/r/ContentMarketing/comments/1srx6uo/) | C12 | Quinn | 🟡 **合并进 #5** |
| 22 | best Claude setup for SEO content writing ad copy free | [r/ContentMarketing 1sldf7d](https://reddit.com/r/ContentMarketing/comments/1sldf7d/) | C5 | Sophie+Isaiah+Olivia | **博客**（多 Agent 协作教程）|
| 23 | where to find reference ads examples | [r/ContentMarketing 1sjwb65](https://reddit.com/r/ContentMarketing/comments/1sjwb65/) | C5 | Olivia | agent 详情页 |
| 24 | how to find new Instagram creators | [r/ContentMarketing 1shv026](https://reddit.com/r/ContentMarketing/comments/1shv026/) | C9 | Mia | doc（发现型，窄用例）|
| 25 | what features AI agents for small business need | [r/AI_Agents 1ssa9zx](https://reddit.com/r/AI_Agents/comments/1ssa9zx/) | C7 | YOLOX 平台设计 | **博客**（产品定位文章）|
| 26 | top AI business ideas for beginners | Quora | C10 | YOLOX 间接 | 博客（SEO 长尾）|
| 27 | efficiently automate Etsy Shopify with Printful/Printify | Quora | C3 | POD 间接 | agent 详情页 |
| 28 | upload POD designs in bulk automated | Quora | C3 | Eli | agent 详情页 |
| 29 | AI content writing tools easy content | Quora | C5 | Theodore | 博客（长尾 how-to）|
| 30 | best way to use AI to get new clients | Quora | C6 | Elias + Daniel | **博客**（跨 Agent 方法论）|

### 统计

- **博客选题强候选**：15 条（占 50%）
- 🔴 **砍**：4 条（#6 #7 #17 #19）—— 与 `10-tier1-audit-and-sop.md` §7.1 一致
- 🟡 **合并**：1 条（#21 合并入 #5）
- **doc / agent 详情页**：10 条（写长文不划算，做产品文档更合适）

---

## 5 · 深挖 10 个典型案例 · 给小刀老师的教材

**选取标准**：覆盖所有判断维度（热度 / YOLOX 匹配 / 选题类型 / 砍词红线）。读完你就能独立判断剩下 20 条和未来新出现的 Reddit 问句。

### Case 1 · 🟢 强候选模板 · `is llms.txt a scam`

- **原帖热度**：[r/SEO 1srvco1](https://reddit.com/r/SEO/comments/1srvco1/) · score 9 / **43 comments**
- **GAKP 数据**：主题族群 6/6 有量 + yoy +900%
- **YOLOX 对应**：Sophie (SEO Doctor) 一个 Agent 就能覆盖 AEO 全流程
- **为啥强**：情感切入点（"scam"=用户焦虑）+ 主题爆发 + 单 Agent 清晰回答
- **写作模板**：1. 解释 llms.txt 是啥 → 2. 引原帖和其他权威怀疑 → 3. YOLOX Sophie 的 AEO 检查清单
- **预期效果**：下周 #1 博客，1500-2000 字，引 3-5 条 Reddit / Medium 证据

### Case 2 · 🟢 SMB 高情感模板 · `struggling to get consistent clients cleaning business`

- **原帖热度**：[r/smallbusiness 1srl89h](https://reddit.com/r/smallbusiness/comments/1srl89h/) · score 18 / **33 comments**
- **为啥强**：**不是"how to X"技术问题，是"I'm struggling"情感问题**——这类搜索用户**读完就想行动**，转化率高
- **YOLOQX 答**：Elias (Traffic Commander) 做获客诊断 + 3 个具体动作
- **坑提醒**：原帖是"cleaning business"，写博客时**不要泛化成"服务业"**（#12 审计已说），要么用"cleaning"要么用其他具体细分
- **写作模板**：1. 共情开头（引原帖用户语言）→ 2. 不是你不努力（心理） → 3. AI 获客三板斧（可复用 Elias 实际能力）

### Case 3 · 🟢 跨 Agent 协作模板 · `how to do distribution for indie SaaS`

- **原帖热度**：[r/SaaS 1ss43uq](https://reddit.com/r/SaaS/comments/1ss43uq/) · score 2 / 4 comments（原帖本身冷，但**主题真实**）
- **为啥选**：indie SaaS 这个 ICP 对 YOLOX 是**精确人群**，即使单帖冷，话题本身被 #6 `how to acquire customers for my SaaS`（41 comments）强相关地支撑
- **YOLOX 答**：Arlo (Launch Strategist) + Quinn (Referral Architect) + Daniel (Email Closer) 三 Agent 协作展示
- **写作价值**：**教小刀老师：原帖冷度不决定话题价值**，要看整个 Cluster 的证据密度

### Case 4 · 🟢 数据爆发词模板 · `how to create llms.txt`

- **原帖**：无直接 URL（是我从 llms.txt 主题扩展的变体）
- **GAKP**：50/mo + comp 低
- **为啥选**：**证明"Day 3 Claude 推的变体不是全假"**——llms.txt 族群是 12.5% 中的黄金命中
- **判断要点**：扩展变体要**基于真实主题**（llms.txt 是 2025-2026 新兴 spec），不能基于 YOLOX 内部命名（traffic commander / referral architect）

### Case 5 · 🔴 必砍案例 · `build AI workers in plain English`

- **原帖热度**：[r/Entrepreneur 1snchax](https://reddit.com/r/Entrepreneur/comments/1snchax/) · score **122** / **97 comments**（**本周最热**）
- **为啥还要砍**：🔑 **原帖是 Anthropic 公告转发**，标题是 Anthropic 市场团队写的 PR 语言，**不是用户问的问题**。热度来自公告曝光，不是搜索需求
- **教训**：**看原帖要看是"提问" vs "公告"**。热度高不一定能写博客
- **对策**：要瞄准 "AI worker vs AI agent"、"how AI workers work" 等用户真会问的短句

### Case 6 · 🔴 show-off 帖陷阱 · `open source social media scheduling alternative`

- **原帖热度**：[r/SideProject 1sk8fn3](https://reddit.com/r/SideProject/comments/1sk8fn3/) · score **266** / 47 comments
- **为啥砍**：🔑 **原帖是"我 built 了一个开源 scheduler"**——作者是**提供者**，不是**搜索者**。关键词意图完全颠倒
- **教训**：**看原帖的第一人称动作**：是"I built / I launched"还是"how do I / anyone know"？
- **对策**：要想抓"找开源工具"这个意图，得去 r/selfhosted 或 r/marketing 搜 "looking for open source alternative"

### Case 7 · 🔴 产品能力缺失陷阱 · `automate Shopify order tracking inquiries with AI`

- **原帖**：[r/ecommerce 1srh6iv](https://reddit.com/r/ecommerce/comments/1srh6iv/) · score 3 / 6
- **为啥砍**：🔑 **YOLOX 没有对应的"客服 Agent"**（15 个 heroActionCards Agent 名单里查证）
- **教训**：**写博客前必须核验"YOLOX 能不能真的做"**。博客转化落地页是产品页，产品做不到则博客是**空头支票**，Google 算法 + 用户都会识破
- **对策**：等 YOLOX 真正实现这个能力再写，或者**现在写但导流到 product roadmap 公示页**

### Case 8 · 🟡 合并案例 · `naturally get Google reviews without pressure` + `get more genuine Google reviews`

- **原帖 1**：[r/smallbusiness 1srnijf](https://reddit.com/r/smallbusiness/comments/1srnijf/) · 9/29
- **原帖 2**：[r/ContentMarketing 1srx6uo](https://reddit.com/r/ContentMarketing/comments/1srx6uo/) · 1/2
- **为啥合并**：两个问题本质一样（Google reviews 获取），Quinn 一个 Agent 答
- **教训**：**主题相近的 Reddit 问句合并写 1 篇，不要拆 2 篇**——避免内链自相残杀，也避免博客产能被稀释
- **对策**：搜 Cluster 内其他相关帖（如 "Google My Business 评分策略"）综合引用

### Case 9 · 🟢 商业调查但可写 · `best AI agent for Shopify store owner`

- **原帖**：[r/shopify 1srps0d](https://reddit.com/r/shopify/comments/1srps0d/) · 中等热度
- **为啥值得**：**07 negative-keywords.md 把 "best X" 整体 defer，但这词例外**：Shopify store owner 是 YOLOX 强 ICP，写一篇"我们是 Shopify 店主 AI 首选"实际是产品市场定位
- **教训**：**规则有 exception**。商业调查词一般不打，但**当它是你的精确 ICP**时，写博客是品类词占位
- **对策**：写"Best AI Agent Platform for Shopify Store Owners: A 2026 Guide" + 内链到 YOLOX Shopify 集成页

### Case 10 · 🟢 产品定位博客 · `what features AI agents for small business need`

- **原帖**：[r/AI_Agents 1ssa9zx](https://reddit.com/r/AI_Agents/comments/1ssa9zx/) · 中等
- **为啥值得**：这是**用户列需求**的帖，读完就能列 10 条 YOLOX 产品特性
- **教训**：**"what features / what criteria" 这类问题等于帮 YOLOX 写产品对照表**——转化率高
- **对策**：直接写"12 Features AI Agents for Small Business MUST Have (2026 Checklist)" 每个特性点 YOLOX 是否支持 → CTA

---

## 6 · 判断博客选题的 4 条纪律

**读 Reddit 新问句时，按这个顺序自问：**

### 纪律 1 · 原帖是"提问"还是"公告"/"show-off"？

- ✅ "how do I" / "anyone know" / "struggling with" / "what actually helped" → **可写**
- 🔴 "I built" / "[Company] just made" / "we launched" / Study of X → **砍**，这是营销/分享，不是搜索

### 纪律 2 · 原帖 + Cluster 证据累计 ≥ 某阈值？

阈值：`score ≥ 3 且 comments ≥ 5` OR `同 Cluster 另有 1+ 相关帖` OR `GAKP 主题族群有量`

- 单帖 1/1 孤例（如 #9 listicle headings）→ 🔴 **不够**
- 单帖冷但 Cluster 热（如 #12 distribution for SaaS）→ 🟢 **可写**
- 单帖热且 Cluster 薄（如 #16 build AI workers）→ 🔴 **还要看纪律 1**

### 纪律 3 · YOLOX 有没有现成能力答？

查 `en.json > home.heroActionCards` 的 15 个 Agent + 补充 Nova/Kit/Mia/Alex/Eli 等。

- ✅ 有对应 Agent（如 Quinn × Google reviews）→ **可写**
- 🔴 需要 YOLOX 没有的能力（如 Shopify 订单客服 Agent #17 #19）→ **砍，写了是空头支票**

### 纪律 4 · 关键词本身是用户会 Google 的吗？

这是**最常错的一条**：

- 用户会 Google：`why ChatGPT cites some pages` / `is llms.txt worth it` / `how to get SaaS customers`
- 用户**不会** Google：`AI Traffic Commander for Shopify` / `build AI workers in plain English` / `YOLOX 24/7 team`

**判断方法**：
1. 把关键词读出声，听起来是不是像 Google 搜索？
2. 关键词里有没有 YOLOX 内部命名（Traffic Commander 等）？有则转成通用能力词
3. 可以拿到 Google 搜索框跑 autocomplete，看 Google 补不补

---

## 7 · 下周 6 篇博客强候选池 · Day 6 前瞻

按纪律 1-4 + GAKP 数据筛出的 9 条强候选（Day 6 再从里面挑 6 条定稿）：

| 优先级 | 博客题（暂拟）| 来源 30 词表 | 证据强度 |
|---|---|---|---|
| 🔥🔥🔥 | Is llms.txt a scam? A 2026 reality check | #2 | Reddit 43 comments + GAKP 主题 +900% |
| 🔥🔥🔥 | Why does ChatGPT cite some pages over others (AEO playbook) | #1 | Reddit 40 score + AEO 主题热 |
| 🔥🔥 | How to create llms.txt for your new site | 30 词表外（GAKP 高分）| GAKP 50/mo + comp 低 |
| 🔥🔥 | Why website visitors don't sign up (and how to find out) | #13 | Reddit 119 comments |
| 🔥🔥 | How to acquire customers for indie SaaS in 2026 | #11 | Reddit 41 comments |
| 🔥🔥 | How to get genuine Google reviews without pressure | #5 (+#21 合并) | 2 帖交叉 |
| 🔥 | AI agents for solopreneurs: complete guide | C7 Pillar 主词 | GAKP +∞ yoy |
| 🔥 | How to do distribution for indie SaaS | #12 | 跨 Agent 协作案例 |
| 🔥 | 12 features AI agents for small business need | #25 | 产品定位 + ICP 清单 |

---

## 8 · 给小刀老师的操作指南

### 8.1 今天结束要做的事

- [ ] 读完本文档
- [ ] Review §5 的 10 个案例（教材性质，必读）
- [ ] 对 §7 的 9 条候选博客**排优先级**（Day 6 挑 6 条）

### 8.2 下次 session（Day 5）要决定的

- [ ] 3 个 Pillar 定稿（handoff §4.5 已预测：Pillar 1 llms.txt 生态 / Pillar 2 Solopreneur / Pillar 3 Shopify 或 SMB）
- [ ] 根据 GAKP 数据**确认 Pillar 1 = llms.txt**（原 handoff 预测是 Pillar 2，数据支持对调）
- [ ] 每个 Pillar 配 4-5 个 Cluster

### 8.3 一周内要持续做的

- [ ] 遇到新 Reddit 问句 → 按 §6 四条纪律判断，不用每次问 Agent B
- [ ] Day 7 拿到 Ahrefs trial 后回头给 Tier 2/3 补 KD

---

## 9 · 附录

### 9.1 本文档涉及的其他文档

**当前目录**（对新 session 有用）：
- `04-keyword-map-v1.md` — 200 词主库（Day 3 快照，未打补丁；Day 7 最终清洗时统一更新）
- `06-pillar-cluster-map.md` — Day 5 Pillar/Cluster 主题图（衔接 Day 6 博客选题）
- `07-negative-keywords.md` — 117 负向词
- `10-tier1-audit-and-sop.md` — Tier 1 40 词逐词审计 + 验证方法论存档
- `raw-gakp-historical.csv` — GAKP 217 词月搜索量原始数据
- `p1-verdict.csv` — P1 验证原始信号

**归档**（`archive/` 子目录，已过期但保留历史）：
- `archive/00-session-handoff.md` — Day 3 cold-start 指南（Day 7 会被 `2.3-handoff.md` 取代）
- `archive/11-gakp-keywords-220.txt` — GAKP 输入词表（已用完）
- `archive/11-volume-validation-guide.md` — 免费验证操作指南（已用过一次）

### 9.2 本文档未做的事（留给 Day 5-7）

- Day 5 · Pillar / Cluster 主题图定稿
- Day 6 · 6 篇博客大纲（挑本文档 §7 候选池的 6 条）
- Day 7 · Ahrefs trial 批量补 KD + 飞书 CSV 导入
- Agent A 上线后 · GSC 真实流量数据校准

### 9.3 Day 4 任务完成自检

- [x] playbook §2.3.4 零量词策略解释（§1-2）
- [x] playbook §4.1 · 30 个第一批狙击词（§4）
- [x] 每个词标出原始 URL + YOLOX Agent + 预期写什么（§4 表格）
- [x] 学习目标：小刀老师能独立判断博客选题（§5-6 四条纪律）
- [x] 交付等级 🟡 · 可 ship 到 Day 5

### 9.4 未决策（等小刀老师）

- [ ] Day 5 开始前是否对 04 主库打 audit 补丁（Tier 1 #13 降级 + C 类标 🔴）
- [ ] 下周博客发布节奏（6 篇同日 or 隔日）
- [ ] Pillar 1 / Pillar 2 顺序对调（GAKP 数据支持 llms.txt 升主）

---

**Day 4 产出结束。**
