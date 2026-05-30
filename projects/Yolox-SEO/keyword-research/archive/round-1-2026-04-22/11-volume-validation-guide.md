# 免费定量验证操作指南 · Day 3→4 过渡

**创建**：2026-04-23
**用途**：用 Google Ads Keyword Planner + Google Trends 免费验证 217 词真实搜索度，产出 Priority v1
**预期总时长**：小刀老师 ~30 min + Agent B 后续处理 ~30 min
**成本**：$0

---

## 0 · 分工

| 做什么 | 谁 | 时长 |
|---|---|---|
| Step 1 · 开 Google Ads Keyword Planner 账号 | **小刀老师** | 10 min |
| Step 2 · 粘 217 词查 volume + 导出 CSV | **小刀老师** | 10 min |
| Step 3 · 跑 7 组 GT 对比 + 回报观察 | **小刀老师** | 10-15 min |
| Step 4 · 整合 GAKP + GT + P1 → Priority v1 | **Agent B** | 30 min |

---

## Step 1 · 开 Google Ads Keyword Planner 账号（10 min，免费）

### 关键：不要真投广告，只用 Keyword Planner 工具

1. 打开 [ads.google.com](https://ads.google.com)，用你日常 Google 账号登入
2. 看到欢迎页时 → 找一个小字链接 **"Switch to Expert Mode"**（通常在页面底部或右上角）
   - 🔑 **不要走 "Smart Mode"**，它会强迫你设广告
3. 到 "Create an account without a campaign" 页面 → 填基本信息（币种 USD、时区 America/New_York 即可）
4. 账号创建成功，跳转到 Google Ads 后台
5. 顶部导航 → **Tools** → **Planning** → **Keyword Planner**
6. 看到两个选项：
   - "Discover new keywords"（扩词用，**不用这个**）
   - **"Get search volume and forecasts"** ← **点这个**

### 🐛 可能遇到的坑

- 🔑 如果看不到 "Expert Mode" 链接：清 cookies / 换 Chrome 隐身窗口重试
- 💸 **系统可能提示"设置账单信息"**——**不要填信用卡**，找页面上 "Skip" 或 "Later" 按钮
- 🐛 如果 Keyword Planner 入口灰掉：确认账号状态是 "Active"（不是 "Pending Payment"），有时要等 5-10 min 激活

---

## Step 2 · 查 217 词 volume + 导出（10 min）

### 2.1 粘贴词表

1. 打开文件 `docs/seo/keyword-research/11-gakp-keywords-220.txt`（你本地路径）
2. 全选复制（Ctrl+A → Ctrl+C）
3. 回到 GAKP "Get search volume and forecasts" 页面
4. 在大文本框里粘贴 → 点 **"Get Started"**

### 2.2 读结果

GAKP 会返回一张表，每行一个关键词，字段包含：

| 字段 | 含义 |
|---|---|
| **Keyword** | 你粘进去的词 |
| **Avg. monthly searches** | 月均搜索量。**不活跃账号会显示区间**（如 "10–100" / "100–1K"） |
| Competition | Low / Medium / High（广告竞争，不是 SEO 竞争）|
| Top of page bid (low/high) | CPC 范围 |

### 2.3 导出 CSV

1. 页面右上角 → **Download** 图标 → **Historical Metrics** → CSV
2. 保存文件为：`docs/seo/keyword-research/raw-gakp-volume.csv`

### 🐛 常见坑

- 🐛 **某些词显示为 "–"（空）**：Google 未收录该词搜索数据，通常 = 月搜索量 < 10
- 🐛 **精确数字 vs 区间**：不活跃账号（没投过广告）只给区间。想要精确数字需要充值 $5-10 激活账号。**对当前阶段，区间够用**
- 🐛 **粘 217 词一次性成功率 ~95%**：若有几个词被截断，手动补粘即可

---

## Step 3 · Google Trends 对比（10-15 min）

**目的**：验证 YOLOX 内部职能名（如 "AI SEO Doctor"）vs 通用词（如 "AI SEO tool"）的相对热度。GAKP 给绝对数字，GT 给趋势曲线。

### 操作方式

直接点下面 7 组 URL，每组页面会自动对比 3-5 个词。每组**看 1-2 min 即可**，填写观察到 §3.x 模板里。

---

### Group 1 · SEO Doctor vs 通用 SEO AI 词（C1/C2 Cluster · Sophie）

👉 [打开 GT Group 1](https://trends.google.com/trends/explore?q=AI%20SEO%20Doctor,AI%20SEO%20tool,AI%20SEO%20agent,AI%20for%20SEO&geo=US&date=today%2012-m)

**对比词**：`AI SEO Doctor` vs `AI SEO tool` vs `AI SEO agent` vs `AI for SEO`

**你要观察**：
- 哪个词的曲线**最高**？
- "AI SEO Doctor" 是 flatline=0 还是有任何曲线？
- 有没有明显的**2026 Q1 上升趋势**？

**你回报模板**（填完发给 Agent B）：
```
Group 1 热度排序：<高到低>
YOLOX 词（AI SEO Doctor）：flatline / 有小曲线 / 与通用词差距 <百分比>
最强竞对词：<哪个>
观察：<自由补充>
```

---

### Group 2 · Traffic Commander vs 通用 marketing AI 词（C3/C4 · Elias）

👉 [打开 GT Group 2](https://trends.google.com/trends/explore?q=AI%20Traffic%20Commander,AI%20marketing%20tool,AI%20growth%20tool,AI%20traffic%20tool&geo=US&date=today%2012-m)

**对比词**：`AI Traffic Commander` vs `AI marketing tool` vs `AI growth tool` vs `AI traffic tool`

---

### Group 3 · Email Closer vs 通用 sales AI 词（C6 · Daniel）

👉 [打开 GT Group 3](https://trends.google.com/trends/explore?q=AI%20Email%20Closer,AI%20sales%20email,AI%20cold%20email,AI%20email%20assistant&geo=US&date=today%2012-m)

**对比词**：`AI Email Closer` vs `AI sales email` vs `AI cold email` vs `AI email assistant`

---

### Group 4 · Competitor Scout vs 通用 competitor intel 词（C8 · Evelyn）

👉 [打开 GT Group 4](https://trends.google.com/trends/explore?q=AI%20Competitor%20Scout,AI%20competitor%20monitoring,competitive%20intelligence%20AI,competitor%20tracking%20AI&geo=US&date=today%2012-m)

**对比词**：`AI Competitor Scout` vs `AI competitor monitoring` vs `competitive intelligence AI` vs `competitor tracking AI`

---

### Group 5 · Referral Architect vs 通用 referral 词（C12 · Quinn）

👉 [打开 GT Group 5](https://trends.google.com/trends/explore?q=AI%20Referral%20Architect,AI%20referral%20program,referral%20marketing%20AI,referral%20tool%20AI&geo=US&date=today%2012-m)

**对比词**：`AI Referral Architect` vs `AI referral program` vs `referral marketing AI` vs `referral tool AI`

---

### Group 6 · Pillar 1 · Solopreneur AI 词云

👉 [打开 GT Group 6](https://trends.google.com/trends/explore?q=AI%20agents%20for%20solopreneurs,AI%20for%20solopreneurs,AI%20tools%20for%20small%20business,one-person%20AI%20team&geo=US&date=today%2012-m)

**对比词**：`AI agents for solopreneurs` vs `AI for solopreneurs` vs `AI tools for small business` vs `one-person AI team`

**重点**：这组是 **Pillar 1 候选主词**的验证。如果 `AI agents for solopreneurs` 真有上升趋势（哪怕低量），Pillar 1 定稿就稳了。

---

### Group 7 · Pillar 2 · AEO / llms.txt 生态

👉 [打开 GT Group 7](https://trends.google.com/trends/explore?q=llms.txt,robots.txt,AEO,answer%20engine%20optimization&geo=US&date=today%2012-m)

**对比词**：`llms.txt` vs `robots.txt` vs `AEO` vs `answer engine optimization`

**重点**：验证 llms.txt 是否真的 2025-2026 新兴爆发。如果 `llms.txt` 曲线 2026 Q1 明显跳升（vs `robots.txt` 这条平稳老词），说明主题热度真实，C1 Cluster 做 Pillar 2 站得住。

---

### 🐛 Google Trends 常见坑

- 🟠 **低量词可能全部 flatline=0**：如果一组里最高的词也才 5 以下，说明**这个话题还没破圈**
- 🟠 **GT 默认地区是 Worldwide**：URL 里已设 `geo=US`（我们 ICP 主要 US），打开后不用改
- 🟠 **曲线相对值不是绝对量**：曲线 100 代表**该组内峰值**，不是月搜多少。Group 之间不可比
- 💸 **不要对比不同主题**：比如 `llms.txt` vs `AI agents` 放一组没意义

---

## Step 4 · 把数据给 Agent B

你跑完 Step 2 + Step 3 后，产出两样：

1. `docs/seo/keyword-research/raw-gakp-volume.csv`（GAKP 导出的 CSV 文件）
2. `docs/seo/keyword-research/raw-gt-observations.md`（你填 7 组 GT 观察，模板在下面）

然后跟我说一句 **"GAKP + GT 数据好了"**，我就会：
- 合并 P1 + GAKP + GT 三源数据
- 重排 Priority v1 分数
- 输出 `docs/seo/keyword-research/12-volume-validation-result.md`：
  - 按 volume 重分 Tier 1/2/3
  - 标出真正的 🔴 死词（GAKP volume=0 + GT flatline）
  - 标出意外高量词（你 Day 3 没预期但 GAKP 显示 ≥ 100/mo）
  - Day 6 博客选题最终强候选池

---

## 附录 A · Step 3 回报模板（直接复制到新文件）

文件路径：`docs/seo/keyword-research/raw-gt-observations.md`

```markdown
# GT 对比观察 · 2026-04-2X 小刀老师人工跑

## Group 1 · SEO Doctor
热度排序：
YOLOX 词状态：
最强竞对词：
观察：

## Group 2 · Traffic Commander
...

## Group 3 · Email Closer
...

## Group 4 · Competitor Scout
...

## Group 5 · Referral Architect
...

## Group 6 · Pillar 1 Solopreneur
...

## Group 7 · Pillar 2 llms.txt
...
```

---

## 附录 B · 预期发现（跑完前先想一遍，有助于你判断数据合理性）

| 预测 | 如果数据匹配说明什么 | 如果数据反向说明什么 |
|---|---|---|
| `llms.txt` 2026 Q1 曲线跳升 vs `robots.txt` 平稳 | ✅ 主题真实爆发，C1 Cluster 做 Pillar 2 有支撑 | ❌ llms.txt 只是营销炒作，C1 Cluster 20 词可能要砍一半 |
| `AI agents for solopreneurs` 真有小曲线 | ✅ Pillar 1 主词有市场认知基础 | ❌ Pillar 1 要重选主词 |
| YOLOX 职能名词（SEO Doctor 等）全部 flatline | ⚠️ 战略占位词**现在**没人搜——靠内容推广 / PR 激活品类词 | —— |
| GAKP 里有 10+ 词 volume ≥ 1K | ✅ 高量词意外出现，Day 6 博客优先写这些 | ⚠️ volume 全 0 或 10-100，坐实"零流量期只打长尾" |

---

## 附录 C · 如果你完全没时间做 Step 1-3

退路方案（不推荐，但有）：

- **方案 X1**：只做 Step 3（GT 对比），跳过 GAKP。省 20 min。代价：没有绝对 volume，Priority v1 仍半定量
- **方案 X2**：只对 Tier 1 前 40 词做 GAKP，跳过 Tier 2/3 的 175 词。省 5 min。代价：Tier 2/3 仍然只有 Day 3 主观打分

---

**就绪后你跟我说 "GAKP + GT 数据好了" 即可。**
