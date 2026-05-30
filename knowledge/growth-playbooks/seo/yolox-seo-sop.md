# Yolox SEO 实际执行 SOP

这份 SOP 只沉淀实际执行动作，不写泛泛原则，不写时间安排，不写管理流程。

覆盖范围只有五块：

1. 看板与数据搭建
2. 关键词挖掘
3. Blog 内容生产
4. 外链建设
5. 技术 SEO 修补

每一块都按“输入是什么、怎么做、做到什么程度算完成、常见坑”来写。

---

## 1. 看板与数据搭建

看板不是为了好看，是为了把 SEO 执行后产生的信号接住。

Yolox 目前需要看的信号主要有四类：

- Google 是否抓到并索引页面。
- 哪些 query 开始出现 impression。
- 哪些外部渠道真的带来了 session 或注册。
- 从自然流量进入网站后，用户有没有继续看 pricing、agents store、注册或购买。

### 1.1 接入 GSC

先确认有没有现成的 `yolox.ai` 或 `https://yolox.ai/` GSC property。

如果已经有人是 owner，就让对方在 GSC 的 `Settings > Users and permissions` 里把账号加成 Owner。不要重复验证。

如果没有 property，就新建 URL-prefix property，然后用 HTML file verification 做验证。

验证完成后提交 sitemap：

- 进入 GSC 对应 property。
- 打开 `Sitemaps`。
- 输入 `sitemap.xml`，不要填完整 URL。
- 看到状态为 `Success`，并且 Discovered URLs 大于 0。

GSC 初始数据为空是正常的，关键是 property、sitemap、索引覆盖数据入口要先建立起来。

需要保存的截图：

- sitemap 提交成功页。
- Pages / Coverage 页面。
- Performance / Search results 页面。

### 1.2 接入 Bing Webmaster

Bing Webmaster 直接从 GSC import。

操作重点：

- 使用同一个 Google 账号授权。
- 让 Bing 自动创建站点 property。
- 复用 GSC 验证。
- 同步 sitemap。

做 Bing 不是因为它本身流量一定大，而是因为一部分 AI 搜索入口会参考 Bing 体系里的索引信号。

### 1.3 规范 GA4 事件

事件名统一用 snake_case，不传邮箱、姓名、电话、IP、地址、信用卡等 PII。

核心转化事件：

| 事件名 | 用途 |
|---|---|
| `auth_register_complete` | 注册完成 |
| `agent_instantiated` | 创建或实例化 agent |
| `purchase` | 购买 |

关键漏斗事件：

| 事件名 | 用途 |
|---|---|
| `page_view` | 基础访问 |
| `lp_hero_input_submit` | 首页 hero 输入提交 |
| `lp_auth_btn_click` | 首页登录/注册按钮点击 |
| `store_card_click` | agent store 卡片点击 |
| `agent_view` | agent 详情查看 |
| `message_sent` | 发送消息 |
| `scroll_depth` | 页面滚动深度 |

在 GA4 Admin 里把这些事件处理好：

- `auth_register_complete`、`agent_instantiated`、`purchase` 标记为 conversion / key event。
- `app_version`、`env` 这类参数设置成 custom dimension。
- 新事件上线前先用 DebugView 或 Realtime 验证。

### 1.4 规范 UTM

所有外部分发链接都要带 UTM，包括目录提交、社区帖、guest post、邮件、AI 搜索监控链接。

格式：

```text
https://yolox.ai/<path>?utm_source=<site>&utm_medium=<channel>&utm_campaign=<content>
```

填写规则：

| 字段 | 写什么 | 示例 |
|---|---|---|
| `utm_source` | 具体站点或平台 | `reddit`、`producthunt`、`github` |
| `utm_medium` | 渠道类型 | `directory`、`community`、`guest-post`、`ai-search`、`email`、`social` |
| `utm_campaign` | 本次内容或动作 | `reddit-aiagents-workflow`、`producthunt-submit` |

硬规则：

- 全部小写。
- 单词之间用连字符。
- 不用中文、空格、下划线。
- 站内链接不要加 UTM，避免污染真实来源。
- 链接发出去前，用无痕窗口点一次，在 GA4 Realtime 里确认能看到来源。

### 1.5 搭 Looker Studio 看板

看板固定做 6 个模块。

#### 模块 1：Organic Funnel

用途：看自然搜索用户有没有从访问进入关键页面，再走到注册。

图表类型：Funnel chart。

漏斗步骤：

1. `page_view`
2. `page_view`，并且 `page_location` 包含 `/pricing` 或 `/agents-store`
3. `auth_register_complete`

过滤条件：

- `Session default channel group` contains `Organic Search`

#### 模块 2：Acquisition by UTM Medium

用途：看不同外部分发渠道带来的 session 和注册。

维度：

- `Session medium`

指标：

- `Sessions`
- `Key events`，过滤到 `auth_register_complete`

排序：

- 按 Sessions 降序。

#### 模块 3：Landing Page Performance

用途：看哪些入口页承接了访问，以及页面质量如何。

维度：

- `Landing page + query string`

指标：

- `Users` 或 `Active users`
- `Average engagement time per session`
- `Key events`

排序：

- 按 Users 降序，显示 Top 20。

#### 模块 4：Top Queries from GSC

用途：看 Google 已经开始给 Yolox 哪些搜索词曝光。

数据源：

- Search Console。

维度：

- `Query`

指标：

- `Impressions`
- `Clicks`
- `Average position`

排序：

- 按 Impressions 降序，显示 Top 20。

新站早期这里为空是正常的，不要因为空就删掉。

#### 模块 5：Event Count Trend

用途：看关键行为事件有没有正常发生。

图表类型：

- Time series。

维度：

- `Event name`

指标：

- `Event count`

过滤事件：

- `auth_register_complete`
- `agent_view`
- `lp_hero_input_submit`
- `agent_instantiated`
- `purchase`

#### 模块 6：Purchase Revenue

用途：看购买和收入。

图表类型：

- Table。

维度：

- `Item name`

指标：

- `Purchase revenue`
- `Ecommerce purchases`

过滤条件：

- `Event name` equals `purchase`

### 1.6 看板完成标准

看板搭完后，必须能回答这些问题：

- GSC property 是否验证完成。
- sitemap 是否提交成功。
- Bing 是否从 GSC import 成功。
- GA4 是否能看到关键事件。
- UTM 点击是否能在 Realtime 看到。
- Looker 6 个模块是否都有正确数据源、维度、指标和过滤条件。

---

## 2. 关键词挖掘

关键词挖掘不是为了做一个漂亮词表，而是为了决定 Blog 写什么、怎么写、怎么做内链、放在哪个 URL silo 里。

每轮关键词工作最后至少要产出：

- 关键词主表。
- 负向关键词表。
- Pillar / Cluster 结构。
- 可直接交给 Blog 写作的 L6 大纲。
- 每个选题对应的搜索意图、目标读者、证据来源和产品切入点。

### 2.1 先做种子词

种子词从四个来源来。

| 来源 | 关注点 | 注意事项 |
|---|---|---|
| 产品功能 | Yolox 能解决什么具体任务 | 用用户会搜的功能名，不用内部 agent 名 |
| ICP 痛点 | 用户遇到什么问题 | 词要像真实问题，不要像产品介绍 |
| 竞品定位 | 用户会怎么比较工具 | 保留 useful、compare、alternative intent |
| 新兴生态 | AEO、AI Overview、llms.txt 等 | 适合做前沿解释型内容 |

不要用 Claude 凭空生成 `Agent x ICP x 场景` 的大表。

之前已经验证过，这种方式命中率低，很容易产出看起来合理、实际没人搜的词。

### 2.2 扩词优先级

扩词按这个顺序做：

1. 从 GAKP 已验证有量的词继续派生长尾词。
2. 从 Reddit、Quora、HN、Indie Hackers 这类真实社区里挖问题。
3. 用 Google PAA 和 related searches 链式扩展。
4. 需要规模化时再用 Keywords Everywhere、DataForSEO、KWFinder、Ahrefs。

社区问题的筛选标准：

- 优先 question post。
- 不要把 show-off、announcement、launch post 当成搜索需求。
- 看 score、评论数、是否有多个帖子重复出现。
- 单个孤立帖子不能直接作为强证据。

Google PAA 的做法：

- 输入 seed keyword。
- 打开第一层 PAA。
- 继续展开相关问题。
- 至少展开到能看到一组稳定重复的问题。
- 把问题改写成可写 Blog 的长尾关键词。

### 2.3 验证关键词

验证不是无限加工具，而是判断这个词值不值得进入内容生产。

优先看这些信号：

- SERP Top 10 是谁，是否全是强站。
- 搜索意图是不是信息型、问题型、比较型或高购买前意图。
- GAKP 是否有搜索量、同比变化、相关词。
- Reddit / Quora 是否有真实讨论。
- PAA 是否存在大量相关问题。
- 是否有 AI Overview / answer engine 引用机会。
- Yolox 是否能给出比泛泛文章更具体的回答。

GAKP 要用 Historical metrics，不要用 Forecast 当判断依据。

如果导出的 CSV 是 UTF-16 LE，需要先转码再进表格或脚本处理。

### 2.4 打分与分层

关键词可以用 6 个维度打分：

| 维度 | 看什么 |
|---|---|
| Volume | 有没有基本搜索需求 |
| KD | 新站有没有机会进入 |
| Intent | 是否符合信息型、比较型、购买前需求 |
| Growth | 主题是否在增长 |
| ICP | 是否命中目标用户 |
| Product fit | Yolox 是否能自然接上 |

分层规则：

| 层级 | 含义 |
|---|---|
| Tier 1 | 高优先级，适合尽快进入内容生产 |
| Tier 1.5 | 搜索量不漂亮，但 ICP 和产品匹配很强，适合保留 |
| Tier 2 | 有价值，但需要排队 |
| Tier 3 | 暂存，不优先 |
| Negative | 不做，避免浪费内容资源 |

Tier 1.5 很重要。

很多适合 Yolox 的长尾问题，工具里 volume 不一定好看，但如果真实社区证据强、产品能解决、SERP 弱，就不能被机械分数误杀。

### 2.5 组织 Pillar / Cluster

先做 cluster，再做 pillar。

原因很简单：cluster 更具体，长尾竞争更低，也更容易证明一个主题有没有机会。

Pillar 的判断标准：

- 是一个信息型大主题。
- 下面至少能挂 5 个 cluster。
- 至少有一个 cluster 有数据或社区证据支撑。
- Yolox 能讲出和普通 SEO 文章不同的东西。

Cluster 的判断标准：

- 只解决一个具体问题。
- SERP 竞争不要太强。
- 有真实社区问题或 PAA 支撑。
- 能自然连接到 Yolox 的产品能力。

URL silo 按主题归类，例如：

```text
/blog/aeo/{slug}
/blog/ai-tools/{slug}
/blog/b2b/{slug}
/blog/creator/{slug}
```

### 2.6 关键词交付给 Blog 的格式

每个进入写作的选题，至少要交付这些信息：

- Primary keyword。
- Secondary keywords。
- LSI / 相关表达。
- 搜索意图。
- 目标读者。
- 用户真实问题。
- 竞品或 SERP 里常见回答。
- Yolox 的不同角度。
- 推荐 H1。
- TL;DR 草稿。
- H2 / H3 大纲。
- FAQ 问题。
- 内链建议。
- 可用外部证据链接。

不要只给一个标题就开始写。

---

## 3. Blog 内容生产

Blog 的目标是把关键词机会变成可索引、可引用、可转化的页面。

标准输入是关键词研究产出的 L6 大纲。

标准输出是：

- `posts/{slug}/index.md`
- 对应图片或占位图
- 更新后的 `manifest.json`
- 通过 `node scripts/validate.js`

### 3.1 写前先补 brief

每篇文章开始前先补齐 brief。

必填内容：

| 模块 | 要写清楚什么 |
|---|---|
| 关键词 | primary keyword、5-8 个 secondary keywords、5-8 个 LSI |
| 读者 | 谁在搜、为什么搜、卡在哪里 |
| 文章类型 | list、step-by-step、definition、beginner guide、comparison、contrarian、buyer guide |
| 角度 | SERP Top 5 都在说什么，Yolox 准备怎么写得不一样 |
| 证据池 | 至少 2 个 case、3 条近年数据、1 条 quote，全部带 URL |
| 链接 | 内链、产品链接、权威外链 |
| SEO 字段 | title、description、slug、tags、schema、OG 信息 |

证据池没补齐，不要直接写正文。

这样写出来的文章通常会空、泛、像摘要，而不是能排名的内容资产。

### 3.2 选择文章类型

文章类型要和搜索意图匹配。

| 搜索意图 | 适合类型 |
|---|---|
| 想找工具 | List post、Buyer guide |
| 想知道怎么做 | Step-by-step |
| 想理解概念 | Expanded definition、Beginner guide |
| 想比较方案 | Comparison |
| 搜索结果同质化严重 | Contrarian |

不要所有文章都写成“终极指南”。

如果关键词是很具体的问题，就直接回答，不要绕成大而全教程。

### 3.3 正文结构

每篇文章固定要有：

- Intro
- TL;DR 或 answer-first
- H2 body
- FAQ，适合时添加
- Conclusion
- CTA

正文执行规则：

- 主关键词出现在 title、H1、前 100 words、URL slug、meta description、至少一个 H2。
- 每个 H2 至少有一个证据或一个可执行步骤。
- 段落不要过长，避免大块文字。
- 每段第一句尽量自包含，单独摘出来也能看懂。
- 不要频繁写 “as mentioned above” 这类依赖上下文的话。
- 至少放一个 hero image placeholder。
- 能用表格、清单、步骤、决策树讲清楚的地方，不要硬写成长段落。

### 3.4 AEO 写法直接融入正文

不要把 AEO 单独当成一套玄学流程。

写 Blog 时顺手做到这些：

- 开头先给明确答案。
- TL;DR 能被单独引用。
- H2 尽量写成用户会问的问题。
- FAQ 问题用自然语言。
- 定义、步骤、对比结论写得短而完整。
- 表格里的结论不要只有关键词，要有完整判断。
- 引用外部数据时写清来源和年份。

目标是让 ChatGPT、Perplexity、Gemini、Copilot 这类 answer engine 更容易摘取文章里的答案块。

### 3.5 链接规则

每篇文章至少做三类链接：

| 类型 | 要求 |
|---|---|
| Silo 内链 | 至少 3 条，连接同主题 cluster / pillar |
| 产品链接 | 至少 1 条，指向 Yolox 相关产品页 |
| 权威外链 | 至少 3 条，指向官方文档、一手研究、权威报告或原始数据 |

URL 不要凭空编。

只能从这些地方拿：

- `docs/seo` 里已有 URL inventory。
- 关键词研究文档里的来源链接。
- 实际打开验证过的外部页面。
- Yolox 站内真实存在的页面。

锚文本不要全是 exact match。

大致保持：

- 一部分 exact match。
- 一部分 partial match。
- 一部分品牌词或裸 URL。
- 少量 generic anchor。

### 3.6 控制产品露出

Yolox 可以出现，但不要硬卖。

推荐三种位置：

- 开头：用一句话说明这个问题和自动化 agent 场景有关。
- 中段：在具体步骤里自然给 Yolox 一个使用场景。
- 结尾：给明确 CTA。

不要每个 H2 都塞产品。

读者是来解决问题的，不是来读宣传页的。

### 3.7 发布到 `yolox-blog`

实际落库步骤：

1. 在 `yolox-blog/posts/` 下新建 `{slug}/index.md`。
2. 写 frontmatter。
3. 正文 heading 从 `##` 开始，因为页面标题由 frontmatter 渲染。
4. 图片放在同一个 slug 目录，或使用项目已有图片规范。
5. 更新 `manifest.json`。
6. 检查 frontmatter 和 manifest 里的 title、description、date、author、tags 是否一致。
7. 运行：

```bash
node scripts/validate.js
```

发布前必须检查：

- title 不要太长。
- meta description 不要太长。
- slug 清晰、短、可读。
- frontmatter 没有 TBD。
- 外链都能打开。
- 内链都是真实 URL。
- 图片 alt 不为空。
- schema 类型和文章类型匹配。

---

## 4. 外链建设

外链工作的唯一硬 KPI 是：

```sql
status = 'live' AND rel_actual = 'dofollow'
```

`nofollow`、`ugc`、`sponsored` 可以记录，但不计入 dofollow KPI。

`rel="me"` 记录为 `me_no_pagerank`，也不计入 dofollow KPI。

### 4.1 外链数据源

外链工作以归档数据库和状态文档为准：

- `projects/Yolox-SEO/backlinks/data/backlinks.db`
- `projects/Yolox-SEO/backlinks/outreach/status.md`

候选来源包括：

- Ahrefs 竞品反查。
- 多个竞品共同出现的网站。
- GitHub awesome list。
- showcase。
- directory。
- profile / signup 页面里有公开 website 字段的网站。
- Tailwind showcase。
- 少量人工筛出的 blog comment / URL field 机会。

不要把邮件 outreach 放在优先级前面。

自助提交、PR、showcase、directory 更适合当前阶段。

### 4.2 筛选候选站点

每个候选先问五个问题：

1. 能不能自助提交？
2. 能不能自然放 `https://yolox.ai/`？
3. 链接会不会出现在公开页面？
4. 能不能从公开 HTML 验证 rel？
5. 单条处理成本是否足够低？

如果一个站点需要大量注册、复杂审核、看不到公开链接位置，先降级。

不要因为 DR 高就硬做。

### 4.3 提交流程

每条外链按这个流程走：

1. 打开候选页面。
2. 判断提交入口：form、GitHub PR、profile field、showcase request、directory submit。
3. 确认是否允许放官网链接。
4. 准备标题、描述、官网 URL、分类、logo 或截图。
5. 提交。
6. 写入 submissions，状态先记为 `pending` 或 `submitted`。
7. 等公开页面可访问后，用 public HTML 验证。
8. 根据验证结果更新为 `live`、`rejected` 或继续 `pending`。

验证只能看公开页面。

后台预览、个人资料编辑页、提交成功提示，都不能算 live。

### 4.4 GitHub Awesome List

GitHub awesome list 是优先级较高的外链来源。

执行时注意：

- 先确认 list 是否仍在维护。
- 看 README 里的分类和收录标准。
- 不要乱放到不匹配分类。
- PR 说明写清 Yolox 是什么、为什么适合这个 list。
- PR 合并后再验证 README 里的实际链接。
- 链接出现在公开 README，且 rel 正常时，才更新为 live / dofollow。

已有 PR 不要重复提交。

先查 `status.md` 和数据库记录。

### 4.5 处理 226 资源池

226 池子已经大范围扫过，不要盲目批量重跑。

后续只把它当成复查池：

- `skipped`、`failed` 不要默认重做。
- `pending` 只做公开页面状态检查。
- `dead` 不投入时间。
- `profile` 类机会要特别谨慎，因为很多只是 `rel="me"` 或 nofollow。

如果要继续挖，只抽小样本人工看：

1. 打开页面确认还活着。
2. 看是否有真实公开 URL 字段。
3. 看链接是否会渲染到 public profile。
4. 看 rel 是否 dofollow。
5. 跑通一个 happy path 后再扩大。

### 4.6 记录状态

每个机会至少记录：

- source site。
- target URL。
- submission type。
- submitted URL。
- status。
- rel expected。
- rel actual。
- evidence URL。
- 备注。

状态不要写模糊词。

用这些：

- `candidate`
- `submitted`
- `pending`
- `live`
- `rejected`
- `failed`
- `skipped`

### 4.7 外链常见坑

不要在没有 URL 字段的评论正文里硬塞 Yolox 链接。

不要用 `marketplace` 当 Yolox 的定位或锚文本。

不要重复提交同一条记录。

不要把 `nofollow` 当 dofollow。

不要把 `rel="me"` 当 SEO 外链。

遇到 PunBB 这类老论坛，如果输入框 value 里出现 PHP Deprecated warning，要先清掉字段再提交，否则可能静默失败。

---

## 5. 技术 SEO 修补

技术 SEO 的目标不是堆工具分数，而是让页面能被抓取、理解、展示和分享。

执行顺序：

1. 从 `docs/seo/audit-report.md` 找具体问题。
2. 定位到代码文件。
3. 一次只修一个明确问题。
4. 修完后用代码检查、页面检查或搜索引擎工具验证。
5. 在 audit 文档里更新状态。

### 5.1 基础抓取与索引

重点文件：

- `src/app/sitemap.ts`
- `src/app/robots.ts`
- `src/app/layout.tsx`

检查点：

- sitemap 是否包含应该索引的公开页面。
- robots 是否没有误挡核心页面。
- auth、billing、账户类页面是否避免被索引。
- canonical 是否明确。
- `metadataBase` 是否正确。

### 5.2 Metadata

检查点：

- 首页有明确 title 和 description。
- title template 存在。
- 动态详情页在 `generateMetadata` 里生成独立标题、描述和 OG 信息。
- description 不要所有页面复用同一句。
- 页面只有一个清晰 H1。

动态页不要只依赖全局 metadata。

详情页需要自己生成能被分享、能被搜索结果理解的 metadata。

### 5.3 Open Graph / Twitter Card

检查点：

- 不要用 SVG 当主要 OG image。
- 准备 1200 x 630 PNG。
- `public/og-image.png` 真实存在。
- 页面 metadata 指向正确图片。
- Twitter card 配置完整。

验证方式：

- 打开页面 HTML，看 meta tags。
- 用社交预览工具检查。
- 本地确认图片能访问。

### 5.4 图片 alt

重点页面：

- 首页。
- agent store。
- agent detail。
- blog post。

执行规则：

- 装饰性图片可以空 alt。
- 传递信息的图片必须写 alt。
- 首页大量空 alt 要逐个判断，不要机械全补。
- alt 写图片表达的内容，不要堆关键词。

### 5.5 JSON-LD / Schema

优先加这些：

- Home page：Organization / WebSite。
- Blog：Article / BlogPosting。
- FAQ 型内容：FAQPage。
- How-to 型内容：HowTo。
- 产品或 agent 详情页：根据页面实际内容选择合适 schema。

验证方式：

- Rich Results Test。
- Schema Markup Validator。
- 页面源码检查 JSON-LD 是否渲染。

### 5.6 hreflang

如果页面存在多语言版本，要检查：

- 每个语言版本都有对应 alternate。
- 语言代码正确。
- canonical 和 hreflang 不冲突。
- x-default 是否需要。

没有多语言内容时，不要为了“看起来完整”乱加 hreflang。

### 5.7 技术 SEO 完成标准

一项技术 SEO 修补完成，至少满足：

- 代码里能定位到改动。
- 本地或线上页面能看到结果。
- sitemap / robots / metadata / schema 等输出符合预期。
- 对应验证工具没有明显错误。
- audit 文档里的状态同步更新。

---

## 6. 一张执行清单

实际做 SEO 时，可以按这张清单推进。

### 看板与数据

- GSC property 已验证。
- sitemap 已提交成功。
- Bing Webmaster 已 import。
- GA4 关键事件已上线并验证。
- UTM 命名规则已统一。
- Looker 6 个模块已搭好。

### 关键词

- seed keyword 来自产品、ICP、竞品、新兴生态。
- 扩词用了 GAKP、社区问题、PAA、相关搜索。
- 每个候选词有 intent、SERP、社区证据、产品匹配判断。
- 已分 Tier 1、Tier 1.5、Tier 2、Tier 3、Negative。
- 已产出 Pillar / Cluster。
- 已交付 Blog 可用的 L6 大纲。

### Blog

- brief 已补齐。
- 证据池有 case、数据、quote 和 URL。
- 文章类型匹配搜索意图。
- TL;DR 或 answer-first 已写。
- 每个 H2 有证据或动作。
- 内链、产品链接、权威外链已加。
- frontmatter 和 manifest 一致。
- `node scripts/validate.js` 通过。

### 外链

- 候选站点已判断提交入口。
- 能从公开页面验证链接。
- submissions 状态已更新。
- `rel_actual` 已记录。
- 只把 live + dofollow 计入 KPI。
- 没有重复提交。

### 技术 SEO

- sitemap / robots 正常。
- metadata 和 title template 正常。
- 动态页有独立 metadata。
- OG image 使用 1200 x 630 PNG。
- 重要图片 alt 合理。
- schema 可被验证工具识别。
- audit 状态已同步。
