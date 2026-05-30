# UTM 链接规范（YOLOX）

**版本**：v1.0 · 2026-04-22
**交付等级**：🟡 可用 — 团队日常执行就按这份来
**适用范围**：所有把流量引回 yolox.ai 的外链，包括目录、社区、客座博客、邮件、AI 搜索引用、Podcast shownotes

---

## 0. 为什么要有这份规范

GA4 的 Acquisition 报告按 `utm_source` / `utm_medium` / `utm_campaign` **三个字段分组**。只要命名不统一，同一个来源会散成多行：

```
# 错误示例（GA4 会把这些当成 4 个不同来源）
producthunt / Directory
Producthunt / directory
product-hunt / DIRECTORY
producthunt /directory        ← 多了空格
```

两个月后想复盘"Directory 渠道总共带了几个注册"，你得手工合并这些行 —— **很痛**。本规范就是把命名钉死，一劳永逸。

**零流量期尤其关键**：自然流量≈0，**每条进站访客几乎都来自你主动分发**。UTM 是唯一能告诉你"哪条目录真的有用"的数据源（playbook §2.2.2 + §2.5）。

---

## 1. 标准模板

### 最小形式（必须）

```
https://yolox.ai/<path>?utm_source=<site>&utm_medium=<channel>&utm_campaign=<content>
```

### 扩展形式（可选）

```
https://yolox.ai/<path>?utm_source=<site>&utm_medium=<channel>&utm_campaign=<content>&utm_content=<variant>&utm_term=<keyword>
```

- `utm_content`：A/B 不同落地页、不同 copy 变体时用
- `utm_term`：付费投放时记录关键词用（有机分发场景一般用不到，**本阶段不用**）

### 命名约束（所有字段适用）

| 规则 | 原因 |
|---|---|
| **全小写** | GA4 区分大小写，`Reddit` 和 `reddit` 是两行 |
| **单词间用连字符 `-`**（不用下划线、空格、点） | 统一风格，URL-safe |
| **只用 ASCII**（拉丁字母 + 数字 + `-`） | 中文、空格、`/`、`#` 会被 URL 编码成 `%xx`，GA4 显示乱码 |
| **无尾部空格** | 粘贴时最容易带入的 bug |

---

## 2. `utm_source` — 具体来源站点

**含义**：**具体的那个站**，不是渠道类型。

### 枚举示例（可扩展）

| 类别 | `utm_source` 取值 |
|---|---|
| 工具目录 | `producthunt` / `taaft` / `futurepedia` / `aitoolsclub` / `toolify` / `indiehackers` |
| 社区 | `reddit` / `hackernews` / `lobsters` / `devto` / `jike`（即刻）/ `v2ex` |
| AI 搜索 | `chatgpt` / `perplexity` / `claude` / `gemini` / `copilot` |
| 博客/内容平台 | `substack` / `medium` / `dev-to` / `xiaoyuzhou`（小宇宙）|
| 社交媒体 | `twitter` / `linkedin` / `weibo` / `xiaohongshu` |
| 邮件 | `mailchimp` / `newsletter-<name>` |
| Podcast | `lenny-podcast` / `acquired` / `indie-hackers-podcast` |

**小众站**：直接用主域名去掉 `.com`，如 `aixiaogen`、`airtable-templates`。

### 反面例子

```
❌ utm_source=Product Hunt              # 空格 + 大写
❌ utm_source=producthunt.com           # 不要带域名后缀
❌ utm_source=小宇宙                    # 不要中文，用拼音 xiaoyuzhou
❌ utm_source=Reddit/r/aiagents        # 斜杠会被编码
✅ utm_source=reddit                    # 子版信息放 utm_campaign
```

---

## 3. `utm_medium` — 渠道类型（封闭枚举）

**含义**：**什么类型的渠道**。这是封闭枚举，**只能从下表里选**。

| 值 | 含义 | 举例 |
|---|---|---|
| `directory` | 工具目录 / listings | Product Hunt、TAAFT、Futurepedia |
| `community` | 用户驱动的讨论社区 | Reddit、HN、Dev.to、即刻 |
| `guest-post` | 别人博客上发的客座文章 | 某个 SaaS 博客收录的 use case |
| `ai-search` | AI 搜索引擎的引用链接 | ChatGPT 回答里被引用 |
| `email` | 邮件（自有 newsletter + outbound） | welcome 邮件、冷邮件回复 |
| `social` | 社交媒体 feed | Twitter、LinkedIn、微博 |
| `podcast` | 播客 shownotes 链接 | Lenny's Podcast |
| `cpc` | 付费搜索广告（**本阶段未开启**） | Google Ads、Bing Ads |
| `display` | 展示广告（**本阶段未开启**） | Reddit Ads |

### 为啥要封闭枚举？

因为 GA4 的 **Default channel grouping** 是按 `utm_medium` 归类的，用 `email` 就进 Email channel，乱写 `mail` / `newsletter` 会被扔进 (other) 桶，**看不到了**。

### 反面例子

```
❌ utm_medium=newsletter                # 用 email
❌ utm_medium=forum                     # 用 community
❌ utm_medium=blog                      # 自己的博客不打 UTM；别人博客用 guest-post
❌ utm_medium=referral                  # 这是 GA4 内置分类，不要手动写
✅ utm_medium=community                 # 标准
```

---

## 4. `utm_campaign` — 内容 / 活动

**含义**：**这次引流的具体用途**。比 medium/source 更细。

### 命名约定

| 场景 | 命名模式 | 示例 |
|---|---|---|
| 产品发布 | `launch-YYYY-MM` | `launch-2026-04` |
| 目录提交 | `<source>-submit` | `producthunt-submit`、`taaft-submit` |
| 社区 thread | `<source>-<topic>` | `reddit-aiagents-workflow`、`hn-show-2026-04` |
| 客座博客 | `guestpost-<host>-<slug>` | `guestpost-zapier-automation` |
| 邮件 | `email-<campaign-name>` | `email-welcome-day-3`、`email-relaunch-2026-05` |
| AI 搜索引用 | `aeo-<query-topic>` | `aeo-ai-agent-tools`（监控 LLM 引用回流）|
| Podcast 冠名 | `podcast-<show>-<episode>` | `podcast-lenny-e102` |

### 反面例子

```
❌ utm_campaign=test                    # 啥都没说清
❌ utm_campaign=first_launch            # 下划线 + 没日期
❌ utm_campaign=Reddit AI Agent Thread  # 空格 + 大写
❌ utm_campaign=发布活动                # 中文
✅ utm_campaign=launch-2026-04          # 好
✅ utm_campaign=reddit-aiagents-workflow # 好
```

---

## 5. 完整示例（抄这个就对了）

### 工具目录提交（TAAFT）

```
https://yolox.ai/?utm_source=taaft&utm_medium=directory&utm_campaign=taaft-submit
```

### Reddit r/AIAgent 回答里放的链接

```
https://yolox.ai/agents-store?utm_source=reddit&utm_medium=community&utm_campaign=reddit-aiagents-workflow-2026-04
```

### Show HN 主帖链接

```
https://yolox.ai/?utm_source=hackernews&utm_medium=community&utm_campaign=hn-show-2026-04
```

### 客座博客（假设给 Zapier 博客投稿）

```
https://yolox.ai/agents-store/email-triage?utm_source=zapier&utm_medium=guest-post&utm_campaign=guestpost-zapier-email-automation
```

### Welcome 邮件第 3 天

```
https://yolox.ai/client-home?utm_source=mailchimp&utm_medium=email&utm_campaign=email-welcome-day-3
```

### 小宇宙播客 shownotes

```
https://yolox.ai/?utm_source=xiaoyuzhou&utm_medium=podcast&utm_campaign=podcast-kelaoshi-e45
```

---

## 6. 在 GA4 里能看到什么

### 路径

1. 登录 `analytics.google.com`
2. 左侧 **Reports → Acquisition → Traffic acquisition**
3. 主表默认按 **Session default channel group** 分组；点击表头把 **Primary dimension** 切换成：
   - `Session source` → 看 `utm_source`（具体站点）
   - `Session medium` → 看 `utm_medium`（渠道）
   - `Session campaign` → 看 `utm_campaign`（具体活动）
   - `Session source / medium` → 一体显示（最常用）

### 具体指标

| 你想看 | 在哪看 |
|---|---|
| 哪个目录真的带访客了 | Traffic acquisition → Session source，filter `session medium = directory` |
| 某个 Reddit thread 带了几个 sign_up | Traffic acquisition → Session campaign，key event column |
| 某封邮件点击率 | Traffic acquisition → Session medium = `email`，切到某 campaign |
| Organic vs 所有分发对比 | Default channel grouping 视角（Organic / Direct / Referral / Paid / etc.）|

### 实时验证（新埋 UTM 必做）

1. GA4 左侧 **Reports → Realtime**
2. 另开浏览器**隐身窗口**，访问你的 UTM 链接
3. 看 Realtime 报表里的 **Users by Source / Medium / Campaign** 卡片，10 秒内应该出现一条记录
4. 如果没出现：
   - 检查浏览器扩展是否拦截了 GA4（uBlock、Ghostery 会拦）
   - 检查 URL 里的 UTM 参数是否完整没漏
   - F12 Network 筛 `google-analytics.com/g/collect` 看请求是否发出、参数是否被编码

---

## 7. 常见错误清单（部署前自查）

| 错误 | 后果 | 修正 |
|---|---|---|
| `utm_Source=...`（大写） | GA4 忽略，按 `(not set)` 归类 | 全小写：`utm_source` |
| `utm_source=Product Hunt` | GA4 显示 `Product%20Hunt`，后续聚合困难 | 改 `producthunt`，词间用 `-` |
| 把 UTM 加在 hash 后（`#section?utm_source=...`） | GA4 读不到（hash 不发服务器）| 必须放在 `?` 之后、`#` 之前 |
| 同一条外链分发时 UTM 被 CMS 去掉 | 流量全算 `(direct)` | 提交前用隐身窗口点一次，看地址栏 UTM 是否保留 |
| 自己站内链接带 UTM | 会清空原始来源，把"Reddit 过来的人"改成"Reddit→自己站内点击的" | **自己的站内链接永远不要带 UTM** |

---

## 8. 实操小工具

### 手工拼接易错，用 URL Builder：

- Google 官方：https://ga-dev-tools.google/ga4/campaign-url-builder/
- 本地 JS（可以贴进浏览器控制台快速生成）：

```js
function utm(path, source, medium, campaign, content) {
  const u = new URL('https://yolox.ai' + path);
  u.searchParams.set('utm_source', source);
  u.searchParams.set('utm_medium', medium);
  u.searchParams.set('utm_campaign', campaign);
  if (content) u.searchParams.set('utm_content', content);
  return u.toString();
}
// 用法：utm('/', 'taaft', 'directory', 'taaft-submit')
```

### 提交前 checklist（投出去前自检）

- [ ] URL 全小写（域名除外）
- [ ] `utm_source` 是具体站点，不是类别
- [ ] `utm_medium` 在第 3 节的枚举里
- [ ] `utm_campaign` 带日期或 topic，**不是** `test` / `campaign1`
- [ ] 没有空格、中文、下划线
- [ ] 隐身窗口点一次，GA4 Realtime 能看到

---

## 9. 归档 & 版本控制

所有用过的 UTM 链接由 **Agent C** 统一登记在 `docs/seo/backlinks/log.md`：

```markdown
| 日期 | 目的地 | source | medium | campaign | 完整链接 | 状态 |
|---|---|---|---|---|---|---|
| 2026-04-23 | TAAFT 提交 | taaft | directory | taaft-submit | https://yolox.ai/?utm_source=taaft&utm_medium=directory&utm_campaign=taaft-submit | submitted |
```

**每个外链投出去之前，必须在这张表里登记一行**，方便未来反查。

---

## 10. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-22 | v1.0 | 初版，Agent A 产出 |
