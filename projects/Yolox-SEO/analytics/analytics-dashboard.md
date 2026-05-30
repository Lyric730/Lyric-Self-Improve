# Looker Studio Dashboard 搭建清单（小刀老师代操作）

**日期**：2026-04-23（Day 5）
**预计耗时**：60–90 分钟（大部分是选 dimension 和调格式）
**产出**：一个叫 **"YOLOX SEO Weekly"** 的 Looker Studio 仪表盘，链接写到第 10 节。
**交付等级目标**：🟡 可用（本周可能没数据，**结构先搭好**就算过）

---

## 0. 前提条件（先确认）

### 0.1 Looker Studio 是什么

Google 免费的 **BI 工具**，能把 GA4 的数据画成图表。入口：
- 网址：https://lookerstudio.google.com/
- 用同一个 Google 账号（`fabry.coffee@gmail.com`）登录

### 0.2 你需要的 GA4 权限

最低 **Viewer（查看者）** 就够 —— 昨天截图确认你有。

### 0.3 建 Custom dimension 的特殊前提

当前埋点已移除 referralSource 自定义维度。只有需要按 `app_version` / `env` 做自定义报表时，才需要 Editor 权限创建对应 Custom dimension。

---

## 1. 先画出来的全景图（6 个 widget）

```
┌────────────────────────────────────────────────────────────────┐
│  YOLOX SEO Weekly · 每周一自动刷新                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐ │
│  │ [Widget 1]           │  │ [Widget 2]                       │ │
│  │ Organic Funnel       │  │ Acquisition by utm_medium        │ │
│  │ (漏斗图)              │  │ (表格)                           │ │
│  └─────────────────────┘  └─────────────────────────────────┘ │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ [Widget 3]                                                 │  │
│  │ Landing page performance (表格)                            │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐ │
│  │ [Widget 4]           │  │ [Widget 5]                       │ │
│  │ Top queries (GSC)    │  │ Event count trend (折线图)       │ │
│  └─────────────────────┘  └─────────────────────────────────┘ │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ [Widget 6]                                                 │  │
│  │ Purchase revenue (表格)                                    │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 2. 预备步骤 · GA4 侧建 Custom dimension（可选）

> 只有 GA4 **Editor 或以上权限**能做这步。当前 dashboard 不依赖 referralSource 维度。

### 2.1 GA4 → 左下角齿轮（Admin）→ 中间"属性"列 → **Custom definitions**（自定义定义）

### 2.2 点右上角 **Create custom dimensions**（创建自定义维度）

### 2.3 填参数

| 字段 | 值 |
|---|---|
| Dimension name | `env` |
| Scope | **Event** |
| Description | App environment from gtag config |
| Event parameter | `env` |

### 2.4 点 **Save**

### 2.5 ⏰ 等 24 小时

GA4 新建的 Custom dimension 要 24 小时后才有数据入库。

---

## 3. Looker Studio 新建 Dashboard

### 3.1 打开 https://lookerstudio.google.com/ 登录

### 3.2 左上角 **+ Create** → **Report**

### 3.3 选数据源

- 弹出"Add data"面板 → 搜索框输 **GA4** → 选 **Google Analytics**
- 选 Account **Infinite Flow Labs** → Property → **production**（生产环境那个 `G-JP6DSCZRJT` 对应的 property）
- 右下角点 **Add**

### 3.4 改报告名

左上角默认叫 "Untitled Report" → 点一下 → 改为：

```
YOLOX SEO Weekly
```

### 3.5 📸 截图这时的空报告界面，存到 `docs/seo/analytics-setup/looker-screenshots/01-empty-report.png`

---

## 4. Widget 1 · Organic Funnel（漏斗图）

> **目标**：看 Organic 访客从"到达首页" → "看定价/feature 页" → "注册"的转化率。

### 4.1 顶部菜单 **Add a chart** → 找 **Funnel chart**（漏斗图）

### 4.2 拖到画布左上角，调大小约占半屏宽

### 4.3 右侧 Setup 面板填：

| 字段 | 值 |
|---|---|
| Dimension（步骤定义） | `Event name` |
| Steps | 手动加 3 步：<br>1. `page_view`（所有 pageview）<br>2. `page_view` 过滤 page_location 包含 `/pricing` OR `/agents-store`（任选一个能代表"考虑期"的页）<br>3. `auth_register_complete` |

### 4.4 Filter（右侧 Setup 面板往下拉）

加一个 filter：
- Include
- `Session default channel group` contains `Organic Search`

这样漏斗只看 Organic Search 来源的人。

### 4.5 标题（右侧 Style tab）

设为 `Organic Funnel (本周)`

---

## 5. Widget 2 · Acquisition by utm_medium（表格）

> **目标**：看每个 UTM 渠道带来多少 sessions 和 auth_register_complete。

### 5.1 Add a chart → **Table**（表格）

### 5.2 拖到 Widget 1 右边

### 5.3 Setup

| 字段 | 值 |
|---|---|
| Dimension | `Session medium` |
| Metric 1 | `Sessions` |
| Metric 2 | `Key events`（筛 `auth_register_complete`）|

### 5.4 Sort

按 `Sessions` 降序。

### 5.5 标题：`Acquisition by UTM Medium`

---

## 6. Widget 3 · Landing page performance（表格）

> **目标**：哪些落地页用户停留最久、转化最高。

### 6.1 Add a chart → Table

### 6.2 横跨整行（Widget 1 和 2 下面）

### 6.3 Setup

| 字段 | 值 |
|---|---|
| Dimension | `Landing page + query string` |
| Metric 1 | `Users`（或 `Active users`）|
| Metric 2 | `Average engagement time per session` |
| Metric 3 | `Key events`（筛 `auth_register_complete`）|

### 6.4 Sort：`Users` 降序，限制前 20 行

### 6.5 标题：`Landing Page Performance`

---

## 7. Widget 4 · Top queries from GSC（表格）

> **目标**：看 Google Search Console 的词。

### 7.1 Add a chart → Table

### 7.2 拖到画布下半部分左侧

### 7.3 **数据源要换**

- 默认用的是 GA4。但 GSC 的词在 GA4 里没有。
- 这个 widget 需要新加一个数据源：
  1. 点 chart → 右边 Setup 面板 → Data source → **Blend data** → **Add data**
  2. 选 **Search Console** connector
  3. 输入 yolox.ai 的 URL prefix → 连接

### 7.4 Setup

| 字段 | 值 |
|---|---|
| Dimension | `Query` |
| Metric 1 | `Impressions` |
| Metric 2 | `Clicks` |
| Metric 3 | `Average position` |

### 7.5 Sort：`Impressions` 降序，前 20 行

### 7.6 标题：`Top Queries (GSC)`

⚠️ 这个 widget 本周可能**完全没数据**（GSC 刚提交，还没爬）。正常，结构先搭好。

---

## 8. Widget 5 · Event count trend（折线图）

> **目标**：看 auth_register_complete / agent_view / lp_hero_input_submit / agent_instantiated / purchase 的 7 日趋势。

### 8.1 Add a chart → **Time series chart**（时间序列图）

### 8.2 拖到 Widget 4 右边

### 8.3 Setup（数据源切回 GA4）

| 字段 | 值 |
|---|---|
| Date range dimension | `Date` |
| Dimension | `Event name` |
| Metric | `Event count` |

### 8.4 Filter

只保留我们关心的事件：

- Include
- `Event name` IN (`auth_register_complete`, `agent_view`, `lp_hero_input_submit`, `agent_instantiated`, `purchase`)

### 8.5 Date range（右侧 Setup 底部）

- Default date range: **Last 7 days**
- 或 Last 14 days 便于看趋势

### 8.6 标题：`Event Trend (7 days)`

---

## 9. Widget 6 · Purchase revenue（表格）

> **目标**：查看 GA4 `purchase` 事件的交易数和收入。

### 9.1 Add a chart → **Table**（表格）

### 9.2 拖到画布最下方

### 9.3 Setup

| 字段 | 值 |
|---|---|
| Dimension | `Item name` |
| Metric | `Purchase revenue` / `Ecommerce purchases` |

### 9.4 Filter

- Include
- `Event name` equals `purchase`

（只看 GA4 purchase 电商事件）

### 9.5 标题：`Purchase Revenue`

### 9.6 ⚠️ 本周大概率空表

- 本周大概率 0 笔真实付费（新站零流量）
- 结构搭好，下月开始有意义

---

## 10. 保存 + 分享 + 归档链接

### 10.1 右上角 **Share** → **Copy link**

### 10.2 把链接粘贴到这里（我需要你填）：

```
Dashboard URL: https://lookerstudio.google.com/reporting/xxxxxxxx
```

（链接格式应该是 `lookerstudio.google.com/reporting/<uuid>`）

### 10.3 顺便在 Share 设置里

- Get link → **Restricted** → 只你自己能看（暂时）
- 或者 **Anyone with the link → Viewer**（如果要分享给合伙人）

### 10.4 📸 截全屏 Dashboard，存到

```
docs/seo/analytics-setup/looker-screenshots/02-dashboard-overview.png
```

---

## 11. 每周一收报的自动化（本周先不配）

Looker Studio 支持"定时邮件发 PDF"：
- Dashboard 右上角 → **Schedule delivery**
- 选 "Every Monday 9:00 AM" → 发到 `fabry.coffee@gmail.com`

本周结构刚搭好，**下周数据开始稳定后再开**（避免前两周空报告骚扰自己）。

---

## 12. 🔑 / 💸 / 🗑 / 🐛 大坑

- 🔑 **GA4 Property ID 切换风险**：本 dashboard 绑的是 production property `G-JP6DSCZRJT`。如果以后你换 property ID，dashboard 的数据源要手动更新，否则数据全断。
- 💸 **Looker Studio 永久免费**，不占 Google 配额。放心用。
- 🗑 **Dashboard 删不回**：误删要重建。建完别在 "My reports" 里清理时误点。
- 🐛 **GSC connector 首次连接卡顿**：Google 端偶尔响应慢，如果 Search Console 选项出不来，关掉重试就好。

---

## 13. 完成标志（Definition of Done）

- [ ] Dashboard 名为 `YOLOX SEO Weekly`
- [ ] 至少 Widget 1, 2, 3, 5 搭好（空数据没关系）
- [ ] Widget 4 (GSC) 搭好（可能显示"no data"）
- [ ] Widget 6 视 Custom dimension 是否建成决定
- [ ] Dashboard URL 填到本文件 §10.2
- [ ] 2 张截图存到 `docs/seo/analytics-setup/looker-screenshots/`

---

## 14. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | v1.0 | 初版，Agent A 产出 |
