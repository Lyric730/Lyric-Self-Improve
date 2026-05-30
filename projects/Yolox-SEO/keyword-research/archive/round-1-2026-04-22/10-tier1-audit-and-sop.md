# Tier 1 40 词 · 逐词审计 + 可执行验证 SOP

**创建**：2026-04-23（Day 3 结束·Agent B P1 验证后）
**用途**：小刀老师人工审计材料 + 下次 session cold-start 复用
**产出等级**：🟡 可用（定性验证完整，定量待 Day 7 补）

---

## 0 · 本文档要解决什么

小刀老师原话：**"我不太信任你的直接产出"** + **"必须验证出一种可执行的手段"**。

所以本文档做三件事：

1. **摊开**：40 词每条的原始依据、P1 信号、问题、局限（不用汇总表糊过去）
2. **诚实**：每个词"还缺什么才算真·验证"单独列出
3. **交付**：可复用的验证 SOP（Standard Operating Procedure），未来 200 词全库验证都能跑

---

## 1 · 本轮验证经过（2 分钟读完）

```
小刀老师质疑 200 词可信度
    ↓
分类：A·Reddit URL 实锤 18 / B·llms.txt 变体 6 / C·Claude 模板造词 16
    ↓
验证 18 条 Reddit URL 真实存在（jq 原始 json）✅ 全部存在
    ↓
工具选型：排除 Google Trends（低量词显示为 0，无区分力）
    ↓
跑 P1 = opencli google search + suggest（40 词 × 2 查询，15-20min 全自动）
    ↓
结果：17 🟢 Keep / 23 🟡 Re-examine / 0 🔴 Kill
    ↓
小刀老师要求：逐词审计 + 产出可执行 SOP
```

---

## 2 · 全局局限（所有 40 词都吃这套限制）

在读逐词审计前，这 5 条**必须先理解**——不然你会对某些词的"为什么没砍"困惑：

### 2.1 Google SERP 语义兜底

Google 对**任何**组合查询几乎都返回 7+ 条结果，因为它做语义匹配。  
→ `serp_count` 在 Tier 1 全部 ≥ 7，**零区分力**。

### 2.2 Google suggest 长句失效

suggest 只对**前缀**（prefix）有效，对完整长尾句几乎零返回。  
→ 40 词里只有 5 词有 suggest，不是"剩下 35 个没人搜"，是"suggest 工具不对长句测"。

### 2.3 AI Overview 检测不可靠

40 词只有 1 条 `has_ai_overview=true`（`AI email closer for Gmail`）。可能是：
- (a) opencli google search 原生 JSON 不暴露 AI Overview 块
- (b) 我 jq 检测逻辑只抓了 `type="ai_overview"` + snippet 含 "AI Overview" 字样，覆盖不全
- (c) 确实只有 1 条触发

→ **AI Overview 列作为参考值，不作为判断依据**。

### 2.4 P1 所有信号都是"有没有"，不是"多少"

定量数据（月搜索量 / KD 分）P1 **给不出**。这是 Google Ads Keyword Planner / Ahrefs / KE 的职责。

### 2.5 opencli 走本机 Chrome，结果受地区/登录态污染

我 Chrome 登 Google 账号 + 浏览历史会影响 SERP 排序。  
→ 缓解：未来跑 SOP 时建议隐身窗口 + 固定 --geo=US 参数（opencli 暂不支持 geo 参数，SOP 里标 🚧 TODO）。

---

## 3 · 审计指南（怎么读下面 40 节）

每个词条包含 6 个字段：

| 字段 | 含义 | 可信度 |
|---|---|---|
| **来源** | Reddit URL + 原帖 score/comments / Claude 推导路径 | 🟢 硬证据 or 🔴 Claude 推 |
| **YOLOX Agent** | 从 04 文档 Tier 1 表提取 | 🟢 代码可验 |
| **P1 信号** | suggest / serp / community / AI Overview 原始值 | 🟡 工具限制 |
| **当前问题** | 本词特有的信号解读坑 | 必读 |
| **本词特局限** | 这个词**特有**的不可越障碍（不是 §2 通用局限）| 必读 |
| **下一步验** | 具体可执行动作（不是"看情况"）| 🟢 可执行 |

评分：
- 🟢 **可行**：多源交叉证据存在 + YOLOX 强匹配 + 无致命局限
- 🟡 **边缘**：部分证据缺失 or YOLOX 匹配弱 or 需 Day 7 量化
- 🔴 **砍**：证据为零 + Claude 造词嫌疑重 + YOLOX 勉强匹配

---

## 4 · A 类 · Reddit URL 实锤（18 条）

### #1 · is llms.txt a scam

- **来源**：r/SEO 1srvco1「Is llms.txt file a scam?」· score 9 / **43 comments**（评论数高，说明引发讨论）
- **YOLOX Agent**：Sophie（SEO Doctor）
- **P1 信号**：sug=0 · serp=11 · comm=2 · AIO=❌
- **当前问题**：suggest 无返回（长句正常现象）；SERP 11 条里有 Medium / SearchEngineJournal / SearchEngineLand 等权威站讨论同主题——说明**不止 Reddit 有人问**
- **本词特局限**：
  - ⚠️ llms.txt 是 2025-2026 新兴词，热度可能 2026 Q2 后快速下滑（handoff §4 隐忧 2 已提）
  - ⚠️ Google Trends 单词查不到数据（低量词显示 0），主题趋势验证只能人工跑 `llms.txt` 宽主题
- **下一步验**：(a) Google Trends 跑 `llms.txt`（宽主题）看 6 月曲线；(b) 人工看 SERP 前 10 条发布日期，判断是否 2026 Q1 才爆发
- **评分**：🟢（但注意主题生命周期）

### #2 · how to create llms.txt

- **来源**：🔴 **无 URL**。我从 llms.txt 主题扩展出的变体（"how to create X" 是信息型查询模板）
- **YOLOX Agent**：Sophie
- **P1 信号**：**sug=3（Google 自动补全有返回！）** · serp=10 · comm=1 · AIO=❌
- **当前问题**：sug=3 是强信号——意味着**确实有真人搜 "how to create llms.txt"** 的前缀。这是 B 类词里**最有证据的**
- **本词特局限**：
  - ⚠️ 虽然 sug 有返回，但我还是不知道月搜索量（50/mo 还是 500/mo？）
  - ⚠️ 题材完全依赖 llms.txt 标准的延续性
- **下一步验**：Google Ads KP 查 volume；如果 ≥ 100/mo 就是博客强候选
- **评分**：🟢

### #3 · what is llms.txt file

- **来源**：🔴 **无 URL**。我从 "what is X" 模板扩展的变体
- **YOLOX Agent**：Sophie
- **P1 信号**：sug=2 · serp=9 · comm=1 · AIO=❌
- **当前问题**：suggest 有 2 条返回 → 真人搜
- **本词特局限**：与 #2 同源（llms.txt 主题依赖）；"what is" 信息型词通常被 Wikipedia / 官方 spec 页霸榜，新站抢位难
- **下一步验**：人工搜 "what is llms.txt file" 看 SERP 前 3 是什么站——如果是 llms.txt 官方 spec + 维基，新站无望
- **评分**：🟢（但排名难度可能比 #2 高）

### #4 · why ChatGPT cites one page over another

- **来源**：r/SEO 1ss0drr「Why ChatGPT Cites One Page Over Another (Study of 1.4M Prompts)」· score **40** / 17 comments
- **YOLOX Agent**：Sophie
- **P1 信号**：sug=0 · serp=10 · comm=**1** · AIO=❌
- **当前问题**：comm=1 意味着**只有 Reddit 原帖被 Google 索引**，没有其他独立社区重复讨论——这是"引发关注但未扩散"的信号
- **本词特局限**：
  - ⚠️ 原帖是"研究分享"（Study of 1.4M Prompts），不是提问——**用户不会去 Google 搜这个完整句**
  - ⚠️ 我把"研究 title"直接当成关键词，这是方法论瑕疵
- **下一步验**：拆成更搜索化的短句，如 "why does ChatGPT cite some pages"、"how ChatGPT chooses sources"——这些再跑 P1
- **评分**：🟡（关键词表述本身可能不对，需改写）

### #5 · struggling to get consistent clients cleaning business

- **来源**：r/smallbusiness 1srl89h「Struggling to get consistent clients for my cleaning business — what worked for you?」· score 18 / **33 comments**
- **YOLOX Agent**：Elias（Traffic Commander）
- **P1 信号**：sug=0 · serp=8 · comm=2 · AIO=❌
- **当前问题**：comm=2 说明除了原帖还有一个独立社区讨论同题（可能是另一个 cleaning business 相关帖）
- **本词特局限**：
  - ⚠️ 极具体三层词（solopreneur + cleaning + client acquisition），ICP 范围窄
  - ⚠️ "cleaning business" 可能搜索习惯更偏向 "how to get clients for cleaning business" 而不是 "struggling" 开头
- **下一步验**：用 `opencli reddit search "cleaning business clients"` 看相关帖数量；同时人工改写成更"搜索化"的短句再测
- **评分**：🟡（问题真实但表述偏口语）

### #6 · how to acquire customers for indie SaaS

- **来源**：r/SaaS 1srm4yl「How I think I should acquire customers」· score 19 / **41 comments**
- **YOLOX Agent**：Elias
- **P1 信号**：sug=0 · serp=8 · comm=**3** · AIO=❌
- **当前问题**：comm=3 是本词最强信号——Google 索引了 3 个独立社区帖讨论同题
- **本词特局限**：
  - 🔴 **原帖标题没说 "indie SaaS"**，是我从 subreddit=r/SaaS 反推加的限定词。所以"how to acquire customers for indie SaaS" 这个完整短语实际上**是我组合的**
  - ⚠️ "for indie SaaS" 是不是 Google 用户真的加的限定词？不确定
- **下一步验**：跑两版 P1 对比——"how to acquire customers for SaaS" vs "how to acquire customers for indie SaaS"，看 suggest / comm 哪个强
- **评分**：🟡（强社区证据但关键词表述可能要改）

### #7 · how to promote Shopify store for sales

- **来源**：r/shopify 1srsdlw「How do you promote your Shopify store for sales?」· score 7 / **38 comments**
- **YOLOX Agent**：Elias + Savannah + Stella
- **P1 信号**：sug=0 · serp=7 · comm=1 · AIO=❌
- **当前问题**：comm=1 仅原 Reddit 帖被索引；Shopify 相关搜索通常被 Shopify 官方 / 大型博客霸榜
- **本词特局限**：
  - ⚠️ "for sales" 的"sales"意思含糊（到底是"销量"还是"促销活动"？搜索意图分叉）
  - ⚠️ 关键词中部有"for"，不是最 Google 友好的写法（用户倾向搜 "how to promote Shopify store" 或 "Shopify store promotion"）
- **下一步验**：拆成 "how to promote a Shopify store" + "Shopify store marketing" 两版再测 P1
- **评分**：🟡

### #8 · how to do distribution for indie SaaS

- **来源**：r/SaaS 1ss43uq「How to do distribution?」· score **2** / 4 comments（**原帖极冷**）
- **YOLOX Agent**：Arlo + Quinn
- **P1 信号**：sug=0 · serp=9 · comm=3 · AIO=❌
- **当前问题**：**原帖冷 (2/4)** 但 comm=3 → 说明 Google 索引了更多其他独立帖讨论"SaaS distribution"。这意味着**词本身真实，但我抓的那个原帖不是最强证据**
- **本词特局限**：
  - 🔴 我在关键词里加了 "for indie SaaS"，原帖 title 只有 "How to do distribution?"——又是我加的限定词
  - ⚠️ "distribution" 在 SaaS 语境下歧义多（GTM / 渠道 / 增长）
- **下一步验**：用 opencli reddit search "SaaS distribution" 找更强原帖；同时考虑关键词改写成 "SaaS distribution strategy" / "how indie SaaS gets distribution"
- **评分**：🟡

### #9 · how to structure headings for listicles

- **来源**：r/SEO 1ss6uxv「how to structure headings for listicles?」· score **1** / **1 comments**（**最冷帖**）
- **YOLOX Agent**：Isaiah（SEO Content Factory）
- **P1 信号**：sug=0 · serp=10 · comm=1 · AIO=❌
- **当前问题**：原帖 1/1 极冷——**1 个人问过，没引起任何讨论**。comm=1 就是这一个原帖
- **本词特局限**：
  - 🔴 原帖冷度 = 本词是"孤例"，不代表群体需求
  - ⚠️ 技术 SEO 话题，Claude 能答但 ICP（solopreneur）可能不关心 listicle 结构
- **下一步验**：**考虑从 Tier 1 降级到 Tier 2 或砍**；或者如果 GAKP 查出 ≥ 30/mo 再保留
- **评分**：🔴→🟡（原帖证据弱，需定量救）

### #10 · how to rank new site vs high traffic sites

- **来源**：r/SEO 1sri4ht「Is it possible for a new site to compete with older high-traffic websites?」· score 18 / 17 comments
- **YOLOX Agent**：Stella（Programmatic SEO Builder）
- **P1 信号**：sug=0 · serp=7 · comm=1 · AIO=❌
- **当前问题**：关键词是我从原帖 title 意译的（原帖是问句"Is it possible..."，我改成了动作句"how to rank..."）
- **本词特局限**：
  - ⚠️ 我改写关键词时**没留原 title 版本作对照**，现在 P1 跑的是我的改写版，不是原 title 版
  - ⚠️ 新站 SEO 话题竞争极激烈（Ahrefs / Backlinko / Moz 等全占前排）
- **下一步验**：同时跑原 title "is it possible for new site to compete with older sites" 和我改写版，对比两组信号
- **评分**：🟡（YOLOX 匹配强但竞争激烈）

### #11 · SEO for local service business

- **来源**：r/SEO 1srh3al「How to do SEO for a local service business (cleaning company)?」· score 5 / **12 comments**
- **YOLOX Agent**：Stella
- **P1 信号**：**sug=1（唯一 A 类中有 suggest 的）** · serp=9 · comm=1 · AIO=❌
- **当前问题**：sug=1 是 A 类里唯一的 autocomplete 信号——说明 "SEO for local service business" 这个**短语本身**有人搜
- **本词特局限**：
  - ⚠️ "local SEO" 是红海市场（竞争极大，local SEO 工具厂商 bombardment）
  - ⚠️ 新站想占"SEO for local service business"排名困难
- **下一步验**：GAKP 查 volume + KD；如果 KD < 30 可做，KD > 50 放弃
- **评分**：🟢（P1 信号最强的 A 类词之一）

### #12 · how to get more clients for service business

- **来源**：r/smallbusiness 1ss4ibj「Need Help With Getting More Clients (lashes, brows etc…)」· score 5 / **12 comments**
- **YOLOX Agent**：Elias
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：原帖是"lashes, brows"（美容行业具体），我泛化到了"service business"
- **本词特局限**：
  - 🔴 **我泛化了 ICP**：原帖是美容，我写成服务业 → 可能脱离原帖真实语境
  - ⚠️ "how to get more clients" 是商业话题通用长尾，SERP 竞争者多
- **下一步验**：考虑改回 "how to get clients for beauty salon" 之类更具体的 ICP 短语；或跑 `opencli reddit search "get more clients"` 看是否有 service business 维度的独立帖
- **评分**：🟡

### #13 · how to close more sales faster

- **来源**：r/smallbusiness 1ss8ngr「How do I close more sales, and that too faster? Are business owners feeling the same pain?」· score **1** / 2 comments（**极冷帖**）
- **YOLOX Agent**：Daniel（Email Closer）
- **P1 信号**：sug=0 · serp=10 · comm=1 · AIO=❌
- **当前问题**：**原帖 1/2 冷**，但 serp=10 → 这个话题 Google 有内容但原帖不是核心信号
- **本词特局限**：
  - 🔴 原帖冷度 = 个人小抱怨，不代表群体需求
  - ⚠️ "close more sales" 是销售话题红海，大量销售培训/CRM 工具内容霸榜
- **下一步验**：人工看 SERP 前 10 条竞品——如果全是 HubSpot / Salesforce / Sales Hacker 这种大站，新站无望；考虑改写成 "AI to close sales faster"（更具体、YOLOX 匹配）
- **评分**：🟡

### #14 · turn social media attention into clients

- **来源**：r/smallbusiness 1srignl「How are you turning social media attention into actual clients?」· score 20 / **49 comments**（**讨论热度高**）
- **YOLOX Agent**：Mia + Savannah + Addison
- **P1 信号**：sug=0 · serp=9 · comm=2 · AIO=❌
- **当前问题**：comm=2 + 原帖 49 comments → 最强 A 类词之一
- **本词特局限**：
  - ⚠️ 关键词句长（7 词），SEO 长尾友好但用户真这么搜？
  - ⚠️ "social media to clients" 在营销圈是老话题，大量内容竞争
- **下一步验**：拆 prefix 测 suggest："turn social media" → 看补全是啥；考虑改写 "social media to clients funnel"
- **评分**：🟢（原帖强 + 三 Agent 协作案例）

### #15 · get more genuine Google reviews for business

- **来源**：r/smallbusiness 1srnijf「What actually helped you get more genuine Google reviews for your business?」· score 9 / **29 comments**
- **YOLOX Agent**：Quinn（Referral Architect）
- **P1 信号**：sug=0 · serp=7 · comm=1 · AIO=❌
- **当前问题**：原帖讨论热，但 comm=1 说明其他社区独立讨论少
- **本词特局限**：
  - ⚠️ "Google reviews" 是 local business 红海话题（BrightLocal / Podium 等 review management SaaS 霸榜）
  - ⚠️ 新站占不到前 10
- **下一步验**：GAKP 查 KD，如果 KD > 40 放弃；或拆成更长尾 "get more Google reviews for cleaning service" 之类
- **评分**：🟡

### #16 · build AI workers in plain English

- **来源**：r/Entrepreneur 1snchax「anthropic just made it possible to build AI workers in plain english」· score **122** / **97 comments**（**超热帖**）
- **YOLOX Agent**：YOLOX 整体
- **P1 信号**：sug=0 · serp=11 · comm=1 · AIO=❌
- **当前问题**：🔴 **原帖是 Anthropic 公告的转发，不是"用户提问"——用户不会 Google 这个完整句**
- **本词特局限**：
  - 🔴🔴 **关键词本质有问题**：它是 Anthropic 发布后媒体引用的标语，不是搜索 query。用户要搜"AI worker" / "AI agent"才对
  - ⚠️ 热度是 Anthropic 营销外溢，不代表搜索意图存在
- **下一步验**：**删掉这个关键词**，换成 "how to build AI workers" / "AI worker vs AI agent" 等真·搜索化短语
- **评分**：🔴（关键词表述方法论错误，应砍重选）

### #17 · why people visit website but don't sign up

- **来源**：r/indiehackers 1smtafn「How do I find out why people visited my website are not signing up?」· score **39** / **119 comments**（**极热**）
- **YOLOX Agent**：Sophie + Addison
- **P1 信号**：sug=0 · serp=9 · comm=2 · AIO=❌
- **当前问题**：119 comments + comm=2 → 本词**最强证据之一**
- **本词特局限**：
  - ⚠️ 关键词偏口语（"people visit website but don't sign up"），用户 Google 时可能搜 "website visitor not converting" / "low signup conversion"
  - ⚠️ 同主题 SaaS/CRO 大量内容竞争（Unbounce / VWO / Hotjar）
- **下一步验**：拆 "why visitors don't sign up" / "website signup conversion low" 两个更 Google 化的版本再测 P1
- **评分**：🟢（原帖超热 + YOLOX 两 Agent 对应）

### #18 · how to automate order tracking inquiries Shopify

- **来源**：r/ecommerce 1srh6iv「how to automate order tracking inquiries on shopify without it making things worse」· score 3 / 6 comments
- **YOLOX Agent**：客服 Agent
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：原帖中热（3/6），comm=1 独立讨论少
- **本词特局限**：
  - ⚠️ 极窄三层长尾（Shopify + 订单查询 + 自动化），搜索基数小
  - 🔴 **YOLOX 实际有没有对应"客服 Agent"**？04 文档里标的是"客服 Agent"，但 handoff §8.1 的 15 个 heroActionCards Agent 里**没有直接叫客服 Agent 的**——最接近是 Daniel (Email Closer)，但不是客服。可能 YOLOX 根本没这个能力
- **下一步验**：(a) 跑 grep 看 `en.json` 里是否真有客服 Agent；(b) 如果没有，这词应该砍——没产品支撑
- **评分**：🔴（YOLOX 能力缺失嫌疑）

### #19 · open source social media scheduling alternative

- **来源**：r/SideProject 1sk8fn3「My girlfriend runs a small social media agency... built an open-source alternative」· score **266** / 47 comments（**超热**）
- **YOLOX Agent**：Mia
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：🔴 **原帖是"我造了个开源工具"的 Show-off 帖，不是"我在找开源工具"的提问帖**——**关键词表述完全颠倒了搜索意图**
- **本词特局限**：
  - 🔴🔴 和 #16 同类问题：热度来自开源项目发布，不代表搜索 "open source social media scheduling alternative" 的人很多
  - ⚠️ 如果真要抓这个意图，应该用 "best open source social media scheduler" / "free alternative to Hootsuite"
- **下一步验**：**砍掉**；换成 "best free social media scheduler" 之类
- **评分**：🔴（关键词表述方法论错误）

### #20 · how to get Google reviews without pressure

- **来源**：r/ContentMarketing 1srx6uo「How to naturally get more Google reviews from customers without putting pressure on them?」· score **1** / 2 comments（**极冷帖**）
- **YOLOX Agent**：Quinn
- **P1 信号**：sug=0 · serp=9 · comm=1 · AIO=❌
- **当前问题**：原帖 1/2 冷，我简写了原 title（去掉了 "naturally" "from customers" "on them"）
- **本词特局限**：
  - 🔴 原帖冷 + 我的改写失去 "naturally" 这个关键修饰
  - ⚠️ 与 #15 主题重合（Google reviews），两条词实际上可以合并成 1 条（信息对话不切分这么细）
- **下一步验**：和 #15 合并成 1 条主词，节省博客产能
- **评分**：🟡（可合并入 #15）

---

## 5 · B 类 · llms.txt 主题变体（6 条）

### #21 · llms.txt vs robots.txt

- **来源**：🔴 无 URL。我从"X vs Y"对比模板推的（llms.txt 和 robots.txt 是相关两个技术概念）
- **YOLOX Agent**：Sophie
- **P1 信号**：**sug=1** · serp=8 · comm=1 · AIO=❌
- **当前问题**：sug=1 → 真人搜这个对比
- **本词特局限**：
  - ⚠️ 技术对比词信息密度高，1 篇文章能答完，不适合 Pillar 级
  - ⚠️ 主题生命周期依赖 llms.txt
- **下一步验**：GAKP 查 volume
- **评分**：🟢（Cluster 短文候选）

### #22 · does llms.txt help SEO

- **来源**：🔴 无 URL。"does X help Y" 信任度疑问模板
- **YOLOX Agent**：Sophie
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：sug=0 → 没人搜完整句（但前缀 "does llms.txt" 可能有人搜，待补测）
- **本词特局限**：
  - ⚠️ 主题生命周期依赖
- **下一步验**：测前缀 "does llms.txt" suggest；补 GAKP volume
- **评分**：🟡

### #23 · does ChatGPT read llms.txt

- **来源**：🔴 无 URL。技术真相问题模板
- **YOLOX Agent**：Sophie
- **P1 信号**：**sug=1** · serp=8 · comm=2 · AIO=❌
- **当前问题**：sug + comm 双信号 → 真问题
- **本词特局限**：
  - ⚠️ 答案可能是 "No"（ChatGPT 官方没说读），博客可能只能写 500 字就说完
- **下一步验**：人工搜看 SERP 前 5 怎么答；若已被 OpenAI docs / Anthropic docs 霸榜则新站无望
- **评分**：🟢

### #24 · how llms.txt helps AI citation

- **来源**：🔴 无 URL。outcome-oriented 模板
- **YOLOX Agent**：Sophie
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：sug=0
- **本词特局限**：
  - ⚠️ "AI citation" 本身还没成为 Google 热词（用户更搜 "AI Overview" / "ChatGPT citation"）
  - ⚠️ 与 #24、#22 主题重叠
- **下一步验**：改写 "does llms.txt improve AI Overview ranking" 等更 Google 化表述
- **评分**：🟡

（B 类的 #2 和 #3 已在 §4 A 类部分放在一起展示，因为 04 文档 Tier 1 里是按 Row 排序）

---

## 6 · C 类 · Claude "Agent × ICP" 模板造词（16 条）

**重要前置说明**：这 16 条都是我用 "YOLOX Agent 名 × ICP placeholder" 两维模板生成的，**没有任何外部搜索证据支撑**。命名公式：`AI <Agent 职能> for <ICP>`。

### #25 · AI agents for solopreneurs

- **来源**：🔴 Claude 造（YOLOX 整体 × ICP #3 solopreneur）
- **YOLOX Agent**：YOLOX 整体
- **P1 信号**：**sug=2** · serp=7 · comm=1 · AIO=❌
- **当前问题**：**sug=2 是 C 类唯一有 autocomplete 的词**——有人真搜；补全结果含 "best ai agents for solopreneurs"
- **本词特局限**：
  - ⚠️ YOLOX 整体 Pillar 词，但竞争激烈（Lindy / Relevance / Beam 等都在打）
  - ⚠️ 短语含 "solopreneur"——部分人拼 "solo-preneur" / "solo preneur"，搜索量分散
- **下一步验**：GAKP 查 KD；人工看 SERP 前 10 是谁（Lindy / Relevance？）
- **评分**：🟢（C 类最强）

### #26 · AI marketing team for solopreneur

- **来源**：🔴 Claude 造（套 "AI marketing team" tagline + ICP）
- **YOLOX Agent**：YOLOX 整体
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：sug=0 → 可能真没人这么搜（"team" 这个词在 solopreneur 语境下拗口）
- **本词特局限**：
  - ⚠️ "marketing team for solopreneur" 内在语义矛盾（solo 就不是 team）
  - ⚠️ 本词是 YOLOX 营销 tagline 反推，不是用户搜索
- **下一步验**：改写 "AI marketing assistant for solopreneurs" / "AI marketing stack for solopreneurs"
- **评分**：🟡

### #27 · AI SEO agent for Shopify store

- **来源**：🔴 Claude 造（Sophie × ICP #2 Shopify）
- **YOLOX Agent**：Sophie
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：sug=0；但 "Shopify SEO" 本身是热话题，问题可能在"AI SEO agent"这个具体说法
- **本词特局限**：
  - ⚠️ 用户可能搜 "Shopify SEO app" / "AI SEO tool for Shopify"——"agent" 还不是主流说法
  - ⚠️ 替代词 "tool" / "app" 没测
- **下一步验**：跑 "AI SEO tool for Shopify" + "AI SEO app Shopify" 对比
- **评分**：🟡

### #28 · AI competitor monitoring agent

- **来源**：🔴 Claude 造（Evelyn × 能力词）
- **YOLOX Agent**：Evelyn（Competitor Scout）
- **P1 信号**：sug=0 · serp=9 · comm=**2** · AIO=❌
- **当前问题**：comm=2 → 有独立社区讨论（但讨论的可能是通用"competitor monitoring"话题，不是专门的 AI agent）
- **本词特局限**：
  - ⚠️ "AI competitor monitoring" 主要被 Crayon / Kompyte 等 competitive intelligence SaaS 霸榜
  - ⚠️ Evelyn 单 Agent 撑不起 Pillar
- **下一步验**：人工看 SERP 前 10 是不是全是 SaaS 工具
- **评分**：🟡

### #29 · AI landing page builder for SaaS

- **来源**：🔴 Claude 造（Addison × ICP SaaS）
- **YOLOX Agent**：Addison（Landing Page Builder）
- **P1 信号**：sug=0 · serp=9 · comm=1 · AIO=❌
- **当前问题**：sug=0；用户更搜 "best AI landing page builder" 或 "landing page AI tool"
- **本词特局限**：
  - ⚠️ "for SaaS" 限定词可能没人加
  - ⚠️ 红海（Unbounce / Instapage / Framer AI 等）
- **下一步验**：改写 "AI landing page for SaaS" / "AI landing page generator" 对比
- **评分**：🟡

### #30 · AI ad creative studio for Shopify

- **来源**：🔴 Claude 造（Olivia × Shopify）
- **YOLOX Agent**：Olivia（Ad Creative Studio）
- **P1 信号**：sug=0 · serp=9 · **comm=0** · AIO=❌
- **当前问题**：🔴 **comm=0！40 词里唯一一条社区零匹配**——Google 爬不到任何独立社区讨论"AI ad creative studio for Shopify"
- **本词特局限**：
  - 🔴🔴 **这是本次验证最可能被砍的词**——纯 Claude 造 + 零社区证据
  - ⚠️ "ad creative studio" 是 YOLOX 内部 Agent 名（Olivia），不是外部用户说法
- **下一步验**：改写 "AI ad generator for Shopify" / "Shopify ad creative AI"
- **评分**：🔴

### #31 · AI agent for Notion automation

- **来源**：🔴 Claude 造（多 Agent × Notion connector）
- **YOLOX Agent**：多 Agent
- **P1 信号**：sug=0 · serp=9 · comm=1 · AIO=❌
- **当前问题**：sug=0；Notion 是热 app，但"AI agent for Notion automation"这个说法具体
- **本词特局限**：
  - ⚠️ 用户可能搜 "Notion AI automation" / "Notion AI agent" / "Notion automation tool"
  - ⚠️ Notion 官方有 Notion AI，自带竞争
- **下一步验**：跑 3-4 个变体对比
- **评分**：🟡

### #32 · AI email closer for Gmail

- **来源**：🔴 Claude 造（Daniel × Gmail connector）
- **YOLOX Agent**：Daniel（Email Closer）
- **P1 信号**：sug=0 · serp=9 · comm=**2** · AIO=**✅**
- **当前问题**：**唯一触发 AI Overview 的词！**——但 AI Overview 检测可信度 🟠（§2.3），不轻易当权威信号
- **本词特局限**：
  - ⚠️ "email closer" 是 YOLOX 内部 Agent 名，外部可能用 "AI email tool" / "AI sales email"
  - ⚠️ AI Overview 触发原因可能是 Gmail 相关查询本身高价值，不一定是本词
- **下一步验**：人工到浏览器搜一次，截屏看是否真有 AI Overview 框
- **评分**：🟢（但 AI Overview 信号待人工校验）

### #33 · AI referral architect for service business

- **来源**：🔴 Claude 造（Quinn × 服务业 ICP）
- **YOLOX Agent**：Quinn（Referral Architect）
- **P1 信号**：sug=0 · serp=9 · comm=1 · AIO=❌
- **当前问题**：sug=0；"referral architect" 是 YOLOX 内部 Agent 名，外部无此说法
- **本词特局限**：
  - 🔴 关键词含专有名词 "referral architect"——Google 大概率把它当品牌词处理
  - ⚠️ 用户搜 "referral program tool" / "AI referral system"
- **下一步验**：删掉 "architect"，改 "AI referral tool for service business"
- **评分**：🔴

### #34 · AI launch strategist for indie SaaS

- **来源**：🔴 Claude 造（Arlo × indie SaaS）
- **YOLOX Agent**：Arlo（Launch Strategist）
- **P1 信号**：sug=0 · serp=8 · comm=**2** · AIO=❌
- **当前问题**：comm=2；"launch strategist" 是 Arlo 内部名
- **本词特局限**：
  - ⚠️ 外部用户搜 "product launch AI" / "AI launch checklist"
  - ⚠️ indie SaaS 内圈讨论多（Product Hunt / r/SaaS），但用 "launch strategist" 说法的少
- **下一步验**：改写 "AI product launch assistant for SaaS"
- **评分**：🟡

### #35 · AI traffic commander for Shopify

- **来源**：🔴 Claude 造（Elias × Shopify）
- **YOLOX Agent**：Elias（Traffic Commander）
- **P1 信号**：sug=0 · serp=8 · comm=1 · AIO=❌
- **当前问题**：🔴 "traffic commander" 是内部 Agent 名，外部完全不是用户词
- **本词特局限**：
  - 🔴🔴 和 #33 一类问题——Agent 职能名不是 Google 用户搜的词
  - ⚠️ Shopify 用户搜 "Shopify traffic tool" / "AI marketing for Shopify"
- **下一步验**：**砍**；或改 "AI marketing for Shopify" / "Shopify SEO AI"
- **评分**：🔴

### #36 · AI competitor scout for SaaS

- **来源**：🔴 Claude 造（Evelyn × SaaS）
- **YOLOX Agent**：Evelyn
- **P1 信号**：sug=0 · serp=9 · comm=1 · AIO=❌
- **当前问题**：和 #28 主题重（Evelyn × competitor 监测）
- **本词特局限**：
  - ⚠️ 与 #28 重叠，可合并
  - ⚠️ "scout" 是内部名
- **下一步验**：与 #28 合并；改写 "AI competitor analysis for SaaS"
- **评分**：🟡

### #37 · AI content machine for YouTube

- **来源**：🔴 Claude 造（Theodore × YouTube creator）
- **YOLOX Agent**：Theodore（Content Machine）
- **P1 信号**：sug=0 · serp=7 · comm=**2** · AIO=❌
- **当前问题**：comm=2；"content machine" 是 Theodore 内部名
- **本词特局限**：
  - ⚠️ YouTube creator 用 "AI script generator" / "AI video content tool"
- **下一步验**：改 "AI content generator for YouTube creators"
- **评分**：🟡

### #38 · AI video producer for TikTok

- **来源**：🔴 Claude 造（Sadie × TikTok creator）
- **YOLOX Agent**：Sadie（Video Producer）
- **P1 信号**：sug=0 · serp=9 · comm=1 · AIO=❌
- **当前问题**：sug=0；"video producer" 是内部名
- **本词特局限**：
  - ⚠️ TikTok 用户搜 "AI video generator for TikTok" / "TikTok AI tool"
  - ⚠️ 极红海（CapCut / Opus Clip / Veed 等霸榜）
- **下一步验**：改写
- **评分**：🔴

### #39 · AI agent for Substack newsletter

- **来源**：🔴 Claude 造（多 Agent × ICP #1 Substack 作者）
- **YOLOX Agent**：多 Agent
- **P1 信号**：sug=0 · serp=10 · comm=1 · AIO=❌
- **当前问题**：sug=0；Substack 是平台，"AI agent for Substack" 对比 "Substack AI tool" 说法都可能
- **本词特局限**：
  - ⚠️ Substack 用户群小，搜索量天然低
  - ⚠️ Substack 官方出了 AI 功能，自带竞争
- **下一步验**：改 "Substack AI writing tool"
- **评分**：🟡

### #40 · 24/7 AI team for solopreneurs

- **来源**：🔴 Claude 造（YOLOX tagline "Teams working 24/7" × solopreneur）
- **YOLOX Agent**：YOLOX 整体
- **P1 信号**：sug=0 · serp=8 · comm=**2** · AIO=❌
- **当前问题**：comm=2；但"24/7 AI team"是 YOLOX 营销语言，不是用户搜索
- **本词特局限**：
  - 🔴 关键词本质是品牌 tagline 反推，不是搜索行为证据
  - ⚠️ comm=2 可能是其他 AI SaaS 营销内容碰巧含 "24/7" + "AI team"
- **下一步验**：看 SERP 前 5 有没有真用这个短语的站；若全是"AI team" / "24/7 support"无关内容则砍
- **评分**：🔴→🟡

---

## 7 · 审计小结（读完 40 节后）

### 7.1 必砍清单（4 条）· 2026-04-23 修正版

**小刀老师 2026-04-23 决策**：撤销"含 YOLOX 内部职能名就砍"这条理由。职能名（SEO Doctor / Referral Architect / Traffic Commander / Email Closer / Competitor Scout 等）**反映产品差异化功能**，是零流量期的**战略占位词**，应该验证而不是砍。

只保留 **真正方法论错误** 的 4 条：

| # | 词 | 砍词理由（根因）|
|---|---|---|
| #9 | how to structure headings for listicles | Reddit 原帖 1 score / 1 comment — 孤例，不代表群体需求 |
| #16 | build AI workers in plain English | 关键词源于 Anthropic 公告标语，**不是搜索 query** |
| #18 | how to automate order tracking inquiries Shopify | YOLOX 无对应 Agent — 无产品支撑 |
| #19 | open source social media scheduling alternative | 原帖是 show-off 贴，意图颠倒 |

**4/40（10%）砍**，其余 36 条进入下一步 GAKP + GT 验证池。

### 7.2 从"砍"撤回到"验证"的 5 条（战略占位候选）

| # | 词 | 原砍理由（已撤销）| 新处置 |
|---|---|---|---|
| #30 | AI ad creative studio for Shopify | comm=0 + 内部名 | 进 GAKP 验 volume；如果 volume=0 再考虑砍 |
| #33 | AI referral architect for service business | "referral architect" 内部名 | 🟢 **战略占位**，GT 对比 vs "referral marketing AI" |
| #35 | AI traffic commander for Shopify | "traffic commander" 内部名 | 🟢 **战略占位**，GT 对比 vs "AI marketing tool Shopify" |
| #38 | AI video producer for TikTok | 红海 + 内部名 | GT 对比 vs "AI video tool TikTok" |
| #40 | 24/7 AI team for solopreneurs | tagline 反推 | GAKP 查 volume；0 就砍 |

### 7.3 必改写清单（7 条，不变）

| # | 原词（问题）| 改写方向 |
|---|---|---|
| #6 | how to acquire customers for **indie SaaS**（"indie SaaS" 是我加的）| 同时跑 "how to acquire customers for SaaS" 对比 |
| #8 | how to do distribution for **indie SaaS**（同上）| 改 "SaaS distribution strategy" |
| #10 | how to rank new site vs high traffic sites（我意译的）| 保留原 title "is it possible for new site to compete with older sites" 对照 |
| #12 | how to get more clients for service business（我从美容业泛化）| 改回美容具体词 or 分拆 |
| #26 | AI marketing team for solopreneur（语义矛盾：solo vs team）| 改 "AI marketing assistant for solopreneurs" |
| #27 | AI SEO agent for Shopify store | 对比 "AI SEO tool / app for Shopify" |
| #37 | AI content machine for YouTube | 对比 "AI content generator for YouTube creators" |

### 7.4 可合并

- **#15 + #20** → 合并 1 条 Google reviews 词
- **#28 + #36** → 合并 1 条 competitor 词

### 可合并候选

- #15 + #20 → 合并为 1 个 Google reviews 词
- #28 + #36 → 合并为 1 个 competitor 词

### 真实搜索行为强证据词（🟢 中最强的）

| # | 词 | 证据 |
|---|---|---|
| #2 | how to create llms.txt | sug=3（最强 autocomplete）|
| #25 | AI agents for solopreneurs | sug=2 + C 类唯一 |
| #11 | SEO for local service business | sug=1 + A 类唯一有 sug |
| #17 | why people visit website but don't sign up | 原帖 119 comments + comm=2 |
| #14 | turn social media attention into clients | 原帖 49 comments + comm=2 |
| #6 | how to acquire customers for indie SaaS | comm=3（最强社区交叉）|
| #8 | how to do distribution for indie SaaS | comm=3 |

**这 7 条是 Day 6 博客选题的**真·强候选**，大概率不需要改写就能写**。

---

## 8 · 最终可执行验证 SOP（核心产出）

上面逐词审计暴露的 5 个问题，**SOP 要全部覆盖**：

1. Google SERP 兜底 → 无法砍死词
2. suggest 长句失效 → 需要 prefix 拆解测
3. 关键词表述方法论错误（用内部 Agent 名 / 用公告标语）→ 需要"表述 Google 化"检查
4. 信号源单一 → 需要多社区交叉验证
5. 无定量 → 需要 Day 7 接权威 volume 源

### 8.1 SOP v1 · 五信号组合验证

对**每个候选关键词**跑 5 个独立信号：

| 信号 | 工具 | 问什么 | 权重 | 自动化 |
|---|---|---|---|---|
| **S1** | `opencli google suggest <kw>` | 完整句 autocomplete | 0.5 | ✅ |
| **S1'** | `opencli google suggest <kw 前 3 词>` | **prefix autocomplete**（long-tail 的关键测法）| 1.0 | ✅ |
| **S2** | `opencli google search <kw>` → 数 community（reddit/quora/stackexchange）| Google 索引到的独立社区讨论 | 0.8 | ✅ |
| **S3** | `opencli reddit search <kw>` | Reddit 全站独立搜索命中 | 1.0 | ✅ |
| **S4** | `opencli hackernews search` + `stackoverflow search` | 技术社区交叉 | 0.5（只对技术词有效）| ✅ |
| **S5** | 人工：SERP 前 10 竞品类型 | 红海 / 长尾 / 新站可抢 | — | ❌ 人工 |

### 8.2 打分规则

```
score = S1_hit×0.5 + S1'_hit×1.0 + S2_normalized×0.8 + S3_hit×1.0 + S4_hit×0.5
最高 3.8 分

S1_hit = suggest 返回 ≥ 1 → 1; 否则 0
S1'_hit = prefix suggest 中出现目标词 → 1; 否则 0
S2_normalized = min(community_count / 3, 1)  # 3 条封顶
S3_hit = reddit search 返回 ≥ 3 帖 → 1; 否则 0
S4_hit = HN 或 SO 返回 ≥ 3 → 1; 否则 0

Verdict:
  score ≥ 2.5  → 🟢 强（博客强候选）
  1.5–2.4      → 🟡 中（Tier 2，等 Day 7 定量）
  0.5–1.4      → 🟠 弱（降级）
  < 0.5        → 🔴 砍
```

### 8.3 人工检查清单（S5，自动化前置）

在跑脚本**前**，人工过每个候选词：

- [ ] 关键词里**是否含 YOLOX 内部 Agent 名**（Traffic Commander / Referral Architect / Email Closer / Content Machine / Ad Creative Studio / Landing Page Builder 等）？→ 改成能力词
- [ ] 关键词**是不是搜索 query**（用户真会这样打字）？还是公告标语 / show-off 标题？→ 改写成问句 or 简短短语
- [ ] 关键词的限定词（for indie SaaS / for Shopify store）**是不是我主观加的**？→ 对照原 Reddit title，尽量用原文版本
- [ ] 同 Cluster 里**是否有重复语义词**？→ 合并

### 8.4 SOP 脚本骨架（Day 4 后可实现）

```bash
#!/usr/bin/env bash
# verify-keyword.sh - SOP v1 full implementation
# Usage: bash verify-keyword.sh <keywords.tsv> <out.csv>
# Input TSV: category\tkeyword\tprefix_to_test
# Output CSV: keyword,s1,s1_prefix,s2_community,s3_reddit,s4_hn_so,score,verdict

IN=$1; OUT=$2
echo "keyword,s1,s1_prefix,s2_comm,s3_reddit,s4_hn_so,score,verdict" > $OUT

while IFS=$'\t' read -r cat kw prefix; do
  s1=$(opencli google suggest "$kw" -f json 2>/dev/null | jq 'length // 0')
  s1p_json=$(opencli google suggest "$prefix" -f json 2>/dev/null)
  s1p=$(echo "$s1p_json" | jq --arg kw "$kw" '[.[] | select(.suggestion | test($kw; "i"))] | length // 0')
  serp=$(opencli google search "$kw" -f json 2>/dev/null)
  s2=$(echo "$serp" | jq '[.[] | select(.url // "" | test("reddit|quora|indiehackers|stackexchange"; "i"))] | length')
  s3=$(opencli reddit search "$kw" --limit 15 -f json 2>/dev/null | jq 'length // 0')
  s4_hn=$(opencli hackernews search "$kw" --limit 10 -f json 2>/dev/null | jq 'length // 0')
  s4_so=$(opencli stackoverflow search "$kw" --limit 10 -f json 2>/dev/null | jq 'length // 0')
  s4=$((s4_hn + s4_so))

  # scoring: (see §8.2)
  # ...

  sleep 2
done < $IN
```

🚧 **注意**：SOP 脚本未写完，这是**骨架**。Day 4 05 文档 ship 后再正式实现（估 1-2h）。

### 8.5 SOP 局限（诚实）

- 🔴 **仍无定量**：Day 7 仍需 GAKP / Ahrefs trial 补月搜索量 + KD
- 🔴 **本机 Chrome 污染未解**：opencli 调用走本机登录态，结果可能有地区/历史偏差
- 🟠 **S4（HN/SO）对非技术词价值低**：`AI agents for solopreneurs` 在 HN/SO 命中数有限，但这不代表词差
- 🟠 **reddit search 对小众词可能返回空**：不是"没人搜"而是"Reddit 上没人问"——注意区分

---

## 9 · 分阶段执行路线图

| 阶段 | 用什么 | 产出 | 决定什么 |
|---|---|---|---|
| **Now** | P1 已跑的 40 词 + 本文档 audit | 9 砍 + 2 合并 + 7 强候选 | **Day 4 05 文档基于 29 + 7 真强候选写** |
| **Day 4 晚** | SOP v1 脚本实现 + 跑剩 Tier 2/3 共 160 词 | 全库 200 词 5 信号分数 | **哪些进 Day 6 博客候选池** |
| **Day 5** | 人工 S5 过前 50 强候选 | Pillar 定稿 | **3 Pillar 主词 + 12 Cluster 副词** |
| **Day 7** | GAKP 或 Ahrefs trial 一次性扫全库 | Priority v1（带真实 volume + KD）| **下周 6 篇博客最终选题** |

---

## 10 · 附录

### 10.1 本轮产出文件

- `p1-verdict.csv` — 40 词 P1 原始信号 CSV（/home/lyric/.../keyword-research/）
- `/tmp/p1-verify.sh` — P1 shell 脚本（40 词跑完的那版）
- `/tmp/tier1-keywords.tsv` — Tier 1 40 词 + 分类输入

### 10.2 原始 Reddit 数据路径

`/home/lyric/tools/opencli-raw/day{1,2}-*.json`（15 份）

### 10.3 相关文档

- `04-keyword-map-v1.md` — 200 词主库（原始 Tier 分档）
- `00-session-handoff.md` — Agent B session 切换指南
- `07-negative-keywords.md` — 117 负向词

---

## 11 · 下次 session 或小刀老师审计完后需做决定

- [ ] 9 个 🔴 词是否全部砍？（Day 4 前决定，影响 05 文档词表）
- [ ] #15 + #20 / #28 + #36 是否合并？
- [ ] SOP v1 脚本 Day 4 晚 ship 还是 Day 5 早？
- [ ] Day 7 走 GAKP（免费但要开户）还是 Ahrefs trial（快但要注册）？
- [ ] 04 文档 Tier 1 表是否根据本次 audit 打补丁重发一版（标 🔴 砍和 🟡 改写）？

---

**文档结束。等小刀老师审计后下一步指令。**
