# 里程碑告警配置清单

**日期**：2026-04-23（Day 5）
**预计耗时**：30–45 分钟
**交付等级**：🟢 spike（workaround 为主，零流量期不追求结实）
**基于**：playbook §2.2.5 的 5 个里程碑告警

---

## 0. 为什么告警这么简陋

零流量期的特殊性（playbook §1.1）：
- 没排名 → 没"排名掉位"告警（真·没排可掉）
- 几乎没流量 → 没"流量异常下跌"告警（本来就是 0）
- 真正要报的是**里程碑解锁**："哦第一个词出 impression 了！"

所以本周不追求"结实"的告警，**能知道里程碑解锁就行**。很多条是"每天早晚手动扫一眼" workaround，不丢人。

---

## 1. 5 个里程碑告警 · 总览

| # | 告警事件 | 方式 | 响应紧迫度 |
|---|---|---|---|
| 1 | Site down / 爬虫错误激增 | GSC 自带邮件订阅 | 当天 |
| 2 | 索引页数单日减少 >10% | 手动每日扫 GSC Coverage | 当天 |
| 3 | GSC 首次出现 Impressions | 手动每日扫 GSC Performance | 即时（但里程碑事件，不急）|
| 4 | GA4 首次 auth_register_complete 来自 organic | GA4 Custom insight | GA4 邮件 24h 内到 |
| 5 | GA4 daily sessions 异常下跌 20%+ | GA4 Intelligence 默认异常检测 | GA4 邮件 24h 内到 |

---

## 2. 告警 #1 · Site Down / 爬虫错误激增

### 原理

GSC 自带 "Crawl stats" 报告，如果 Google 爬你的站失败率异常高，会触发邮件。

### 配置步骤

1. https://search.google.com/search-console → 选 `yolox.ai` property
2. 左下 **Settings（设置）** → **Crawl stats（抓取统计）** → 点进去
3. 右上角铃铛 / 三个点菜单 → **Email preferences**
4. 勾选：
   - ☑ Critical issues
   - ☑ New issues
5. 验证收件邮箱是 `fabry.coffee@gmail.com`

### 📸 截图存档

`docs/seo/analytics-setup/alerts-screenshots/01-gsc-crawl-alert.png`

---

## 3. 告警 #2 · 索引页数单日减少 >10%

### 为啥手动

GSC 本身**不支持** Coverage 数据的实时告警（没这个功能）。要做自动化需要：
- 每日脚本拉 GSC API 存数 → diff
- 成本 > 收益（零流量期页面也就几十个）

### 简化做法：每日手动扫（1 分钟/次）

**固定动作**：每天早上 10 点打开 GSC Coverage / Pages 扫一眼。

1. GSC → 左侧 **Pages**
2. 看顶部的 "Indexed pages" 数字
3. 心里对比昨天（零流量期数字不大，脑子记得住）
4. 掉超过 10% → 去看 "Why pages aren't indexed" 找原因

### 手机日历提醒

设个每天 10:00 的 daily reminder："**扫 GSC Coverage，1 分钟**"。

---

## 4. 告警 #3 · GSC 首次出现 Impressions

### 为啥是里程碑

playbook §1.1 定义的 **里程碑 2 · 首个 impression**。这是新站离开"域名沙盒期"的第一个信号。

### 为啥手动

GSC 也不支持这个告警（同上）。

### 简化做法：每日扫（30 秒/次）

1. GSC → **Performance → Search results**
2. 日期选 "Last 28 days"
3. 看 **Impressions** 数字
4. 从 0 变成非 0 = 🎉 里程碑解锁

### 📢 触发时做

1. 截图 GSC Performance 当天状态
2. 存到 `docs/seo/analytics-setup/milestone-screenshots/YYYY-MM-DD-first-impression.png`
3. 周报顶格庆祝，记录**是哪个词**触发的（点开看 Query 栏）

---

## 5. 告警 #4 · GA4 首次 auth_register_complete 来自 organic

### 原理

GA4 **Custom insight** 能配"当某事件满足条件时发邮件"。

### 配置步骤

#### 5.1 GA4 → 左侧 **Insights** → **Create**

（某些新版 GA4 UI 叫"Intelligence" 或 "Advertising workspace"，找不到就搜 "insight"）

#### 5.2 选 **Create custom insight**

#### 5.3 填参数

| 字段 | 值 |
|---|---|
| Evaluation frequency | **Daily**（每天检查一次）|
| Audience | All users |
| Metric | `Key events: auth_register_complete` |
| Condition | **`> 0`** |
| Segment | 加一个 `Session default channel group = Organic Search` 过滤 |

（如果 GA4 UI 里没看到 `Key events`，旧版叫 `Conversions`，同一个东西）

#### 5.4 Notification

- Email: `fabry.coffee@gmail.com`
- Title: `🎉 首个 organic auth_register_complete 来了！`

#### 5.5 Save

### ⏰ 触发条件

本周 100% 不会触发（零流量期没 organic），但埋下去等。首次触发时就是**里程碑 3 · 首个 organic click/signup**。

### 📸 截图存档

`docs/seo/analytics-setup/alerts-screenshots/04-ga4-organic-signup.png`

---

## 6. 告警 #5 · GA4 日 Sessions 异常下跌 20%+

### 原理

GA4 **Intelligence** 自带机器学习异常检测（Anomaly detection），会自动发现异常并邮件通知。**默认已开启**，只需要确认收件邮箱。

### 配置步骤

#### 6.1 GA4 → 左侧 **Insights** → 看已有 insight 列表

默认会有几个叫 "Automated insight" 的条目。

#### 6.2 找到 Sessions 相关的那条（或没有就建一个）

- 如果没有：Create custom insight → Metric: `Sessions` → Condition: `anomaly detected` → Daily

#### 6.3 配 email notification

同上 `fabry.coffee@gmail.com`。

### ⚠️ 本周零流量期的特殊性

Sessions 本来就接近 0，ML 模型的"异常"定义会有噪音（从 0 到 5 可能被标为 "+5 anomaly"）。

**本周简化做法**：默认开着，收到邮件也不必紧张。数据稳定（每周 Sessions > 100）后这个告警才真正有用。

---

## 7. 统一归档位置

所有截图归档到：

```
docs/seo/analytics-setup/alerts-screenshots/
├── 01-gsc-crawl-alert.png
├── 04-ga4-organic-signup.png
└── 05-ga4-anomaly-detection.png
```

（#2 和 #3 是手动扫没固定截图）

### 里程碑触发时的截图放这里

```
docs/seo/analytics-setup/milestone-screenshots/
└── YYYY-MM-DD-<milestone-name>.png
```

例：`2026-05-15-first-impression.png`

---

## 8. 运维节奏

| 频率 | 动作 |
|---|---|
| **每日 10:00** | 1 分钟扫 GSC Coverage（告警 #2）+ Performance（告警 #3）|
| **每日 18:00** | 1 分钟扫同上 |
| **每周一 10:00** | 写周报时顺便扫 GA4 Realtime 最近 7 天 |
| **邮件来时** | 告警 #1、#4、#5 被动等邮件，来了 15 分钟内看 |

手机日历建 daily reminder：`09:55 YOLOX 每日 SEO 扫视（2 分钟）`。

---

## 9. 升档信号（何时切换到"有排名"版本告警）

按 playbook §2.2.5，以下任一触发后，本告警方案升级：

- 10+ 词有稳定 Impressions（> 50/周）
- 首批词进入 top 20
- 每周 Organic Clicks > 20

那时的告警结构（有排名版）：
- Ahrefs Rank Tracker 单日掉位 > 5 的邮件
- GSC 新词进 top 100 / top 10 的邮件
- GA4 Organic clicks 周环比掉 20% 的异常检测

本周**不做**。

---

## 10. 🔑 / 💸 / 🗑 大坑

- 🔑 **GA4 Custom insight 需要 Editor 权限**。如果昨天你建不了 Custom dimension（Widget 6），这里的告警 #4 也建不了。先让管理员给你升权限。
- 💸 **Zapier 级自动化本周不买**。GA4 + GSC + 邮件订阅三件套够用。
- 🗑 **不要信 GA4 Intelligence 的所有 "insight"**。新站前 3 月很多是噪音，淡定看。

---

## 11. 完成标志（Definition of Done）

- [ ] GSC Email preferences 勾选 Critical + New issues
- [ ] 手机日历每日 09:55 reminder 建好
- [ ] GA4 Custom insight `organic auth_register_complete` 已创建（权限够的话）
- [ ] GA4 Anomaly detection 收件邮箱确认
- [ ] 3 张截图存到 `alerts-screenshots/`

---

## 12. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-23 | v1.0 | 初版，Agent A 产出 |
