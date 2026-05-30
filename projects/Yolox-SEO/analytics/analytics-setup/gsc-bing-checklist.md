# GSC + Bing Webmaster Tools 提交清单（小刀老师代操作）

**日期**：2026-04-22（Day 1）
**预计耗时**：30–45 分钟
**产出**：
- GSC `https://yolox.ai/` URL-prefix property 可用 + sitemap 提交成功
- Bing WMT 从 GSC 导入完成
- 基线截图 5 张归档到 `docs/seo/analytics-setup/gsc-bing-screenshots/2026-04-22/`

---

## Step 0 · 先判断现有 GSC property 归属（关键！先做这步）

> **为啥先判断**：你说"网站应该已经在 GSC 提交了"。如果你本来就是 owner，整个 Step 1（HTML 文件验证）**可以跳过**。

### 0.1 登录 https://search.google.com/search-console/ （用你日常工作的 Google 账号）

### 0.2 看左上角的 property 下拉

**三种情况，分别处理**：

#### 情况 A · 你的账号里**已经有** `yolox.ai` 或 `https://yolox.ai/` 这个 property

→ **你就是 owner，皆大欢喜**。
→ 跳过 Step 1，直接去 **Step 2（提交 sitemap）**。

#### 情况 B · 下拉里没有 yolox.ai，但你知道**是同事提交的**

→ 最省事做法（先试这个）：
  1. 找到当初提交的同事
  2. 让他登录 GSC → 选中 `yolox.ai` property → 左侧 **Settings（齿轮）** → **Users and permissions** → **Add user**
  3. 邮箱填 `liuyouxuan570@gmail.com`，Permission 选 **Owner**（最高）
  4. 你会收到邮件确认，确认后这个 property 就出现在你账号里
→ 接着跳去 **Step 2**

如果联系不上同事或对方失联 → 走**情况 C**。

#### 情况 C · 你账号里没有、也找不到当初提交的人

→ 自己加一个独立 URL-prefix property，**这不会和任何现存的 property 冲突**（GSC 允许同一站点多个 property 并存，各自的数据独立）。
→ 走完整的 **Step 1（HTML 文件验证）**。

---

## Step 1 · 添加 URL-prefix property + HTML 文件验证（仅情况 C）

### 1.1 GSC 左上角点 property 下拉 → **Add property**

### 1.2 选 **URL prefix**（右边那个）

- 填：`https://yolox.ai/`（**https、尾部斜杠必须有**）
- 点 **Continue**

### 1.3 选验证方式

Google 会列多种方式。选 **HTML file** 那张卡。

### 1.4 下载验证文件

文件名形如 `google1a2b3c4d5e6f7890.html`（每个 property 唯一）。**下载到本地**，别改名、别编辑内容。

### 1.5 把文件放进仓库（我来做，你把文件发给我）

> **🔑 重要**：把下载的 `.html` 文件**原封不动**发我（丢到对话框拖进来即可），**我负责放到 `public/` 目录 + commit + 推部署**。
>
> 部署目标路径：`yolox-web/public/google1a2b3c4d5e6f7890.html`
> 部署后可访问地址：`https://yolox.ai/google1a2b3c4d5e6f7890.html`
>
> ⚠️ **千万不要改文件内容**。Google 按字节匹配，改一个字节就失败。

### 1.6 部署后通知我"已上线"

我会帮你 `curl https://yolox.ai/googleXXXX.html` 确认文件能访问。

### 1.7 回到 GSC 点 **Verify**

看到绿色对勾 = 成功。看到红色失败：
- CDN 缓存没刷新 → 等 2–5 分钟重试
- 路径不对 → 我 curl 一下告诉你到底返回啥

**🗑 坑**：验证成功后**这个 HTML 文件要一直留在 public/ 里**。Google 会不定期回查，文件消失就验证失效。

---

## Step 2 · 提交 Sitemap

### 2.1 在 `https://yolox.ai/` property 里，左侧点 **Sitemaps**

### 2.2 在 "Add a new sitemap" 输入框填

```
sitemap.xml
```

（只填文件名，不用完整 URL，前缀会自动拼）

### 2.3 点 Submit

成功后 Status 列会显示 "Success"（可能要等几分钟到几小时）。

### 2.4 📸 截图 1

截 Sitemaps 页面，显示 sitemap.xml 的 Status + Discovered URLs 数字。
文件名：`01-gsc-sitemap.png`，存到 `docs/seo/analytics-setup/gsc-bing-screenshots/2026-04-22/`

> **Discovered URLs** 应该 > 0（我们的 `src/app/sitemap.ts` 会生成静态页 + 动态 agents/skills/teams）。
> 如果是 0 或 "Couldn't fetch"，告诉我，我查 sitemap route。

---

## Step 3 · Coverage 基线截图

### 3.1 左侧点 **Pages**（新版 GSC 把 Coverage 改名叫 Pages）

### 3.2 默认看 "Why pages aren't indexed"（indexed 数 + 未 index 原因）

### 3.3 📸 截图 2

截整张图，包含 "Indexed pages" 数字和下方原因表格。
文件名：`02-gsc-pages-coverage.png`

> **零流量期预期**：本周 indexed 数可能是 0–少量（sitemap 刚交，Google 还没爬完）。这是基线，下周对比用。

---

## Step 4 · Performance / Queries 基线截图

### 4.1 左侧点 **Performance → Search results**

### 4.2 顶部日期改成 **Last 28 days**

### 4.3 📸 截图 3

截主图（Total clicks / Impressions / CTR / Position 四个指标的折线 + 底部 Queries 表）。
文件名：`03-gsc-performance.png`

> **零流量期预期**：四个指标全是 0，Queries 表空。**这是基线**，第一个词冒出来就是"里程碑 2"（playbook §1.1）。

---

## Step 5 · Bing Webmaster Tools（从 GSC 一键导入）

### 5.1 登录 https://www.bing.com/webmasters/（用同一个 Google 账号即可）

### 5.2 首次登录会看到 **Import your sites from Google Search Console**

点 **Import**。

### 5.3 授权 Google 账号读取 GSC properties

弹出 OAuth 授权，同意。

### 5.4 选择要导入的站点

勾 `https://yolox.ai/`，点 Import。

### 5.5 Bing 会自动：
- 创建 property
- 复用 GSC 的验证（不用你再弄 HTML 文件）
- 自动拉 sitemap

### 5.6 📸 截图 4

截 Bing WMT 首页仪表盘，显示 `yolox.ai` 已添加 + sitemap 状态。
文件名：`04-bing-dashboard.png`

> **为啥一定要 Bing**：ChatGPT 和 Copilot 的索引很大部分来自 Bing。零流量期靠 AI 搜索引用，**Bing 比 Google 更早给你流量**（playbook §2.2.1）。

---

## Step 6 · 归档所有截图到仓库

### 6.1 把 5 张截图放到

```
docs/seo/analytics-setup/gsc-bing-screenshots/2026-04-22/
├── 01-gsc-sitemap.png
├── 02-gsc-pages-coverage.png
├── 03-gsc-performance.png
├── 04-bing-dashboard.png
└── 05-bing-sitemaps.png    ← Step 5 之后去 Bing WMT → Sitemaps 再截一张
```

（目录我已经建好了）

### 6.2 在对话里告诉我"截图已存"，我来 `git add` + commit。

---

## 预期问题 FAQ

### Q1: 我点 Import from GSC，Bing 说"No sites found"

**原因**：Bing 可能没成功读到你的 GSC。
**解决**：
1. 确认登录 Bing 用的 **是同一个 Google 账号**
2. 在 GSC 里先确认你**已经是 owner**（不是 viewer，viewer 不给 Bing 读）
3. 手动提交：Bing WMT → Add site → 填 `https://yolox.ai/`，选 XML file 验证（和 Google HTML 类似的流程）

### Q2: GSC Coverage 一直显示 "Couldn't fetch" sitemap

**原因**：sitemap 路径被 robots.ts 意外屏蔽，或 Next.js route 报 500。
**解决**：告诉我，我 curl 一下 `https://yolox.ai/sitemap.xml` 看返回。

### Q3: Performance 28 天数据全是 0，正常吗？

**完全正常**。新站 + 没提交过 sitemap → Google 都还没爬完第一遍。**这就是 baseline**，下周对比用。

### Q4: 我发现 yolox.ai 还有一个 `http://` 或 `www.` 的旧 property

**先放着别删**。不同协议/子域在 GSC 是独立 property，删了会丢历史数据。下周周报我统计时会告诉你该合并哪个（或者都留着各自用途）。

---

## 🔑 / 💸 / 🗑 / 🐛 大坑标红

- 🔑 **验证用的 HTML 文件必须一直留在 public/**。部署时被误删 → 验证失效 → Google 数据收集中断。
- 🗑 **不要随便删 GSC property**。历史数据会跟着 property 走，删了找不回。
- 🐛 **Bing Import 偶尔失败**，别循环点。失败了手动提交反而更快（Step 5 FAQ Q1）。
- 💸 **本周不买 Ahrefs**（playbook §2.2.3：10 词进 top 100 才开 Rank Tracker）。GSC + Bing 都是**免费**的。

---

## 完成标志（Definition of Done）

- [ ] GSC 里 `https://yolox.ai/` property 验证通过（情况 A/B 直接有；情况 C 走完 Step 1）
- [ ] sitemap.xml 在 GSC 状态 Success
- [ ] Bing WMT 导入成功
- [ ] 5 张基线截图存入 `docs/seo/analytics-setup/gsc-bing-screenshots/2026-04-22/`
- [ ] 在对话里告诉我"全部完成"

---

## 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-04-22 | v1.0 | 初版，按小刀老师选 URL-prefix + HTML 文件验证方案 |
