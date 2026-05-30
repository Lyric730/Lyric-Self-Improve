# Ahrefs Trial 激活 + 7 天操作 SOP

**日期**：2026-05-02
**面向**：小刀老师（Ahrefs 操作）
**目的**：用 $7 / 7 天 trial 完成 L2 Step 2d/2e + L2 Step 4 + L4 + L7 共 5 个使用点
**前提**：worktree 隔离，trial 只跑一次，Agent B 等你拿 CSV 后做合并筛选

---

## 0 · 激活前 checklist

- [ ] 备好 $7 信用卡 / 国际支付方式
- [ ] 用一个**无 Ahrefs 历史**的邮箱注册（trial 限 1 次/邮箱）
- [ ] 浏览器开 Cookie + JS（避免被反爬）
- [ ] 准备好导出 CSV 路径：建议 `/tmp/ahrefs-*.csv`（统一命名）

⏰ **激活后立即记录日期**——告诉我激活日，我标 expiry = +7 天到期

---

## 1 · 激活步骤

```
1. https://ahrefs.com/awt → 7-day trial $7
2. 注册账号 + 信用卡支付 $7（trial 期满自动续约 / 你 7 天后取消）
3. 登录后进入 dashboard
4. 验证：能进 Keywords Explorer + Site Explorer
```

---

## 2 · L2 Step 2d · KE Matching Terms（~2000-3500 词）

**输入**：Pool A 76 词清单（已导出到 `/tmp/pool-a-76-keywords.txt`）

**操作**：
```
1. Ahrefs → Keywords Explorer
2. 顶部 region 选 "United States" + Language "English"
3. 大文本框粘贴 /tmp/pool-a-76-keywords.txt 全部 76 词（一行一词）
4. 点击 "Search"（or "Explore"）
5. 等待加载 → 进入 Overview 页
6. 左边导航点 "Matching terms"
7. 右上 Filter 设：
   - Volume: 不限
   - KD: 不限（先全拿）
   - Word count: 不限
8. 顶部 Export → CSV（默认 1000 行/查询，可能分多次）
9. 保存到 /tmp/ahrefs-matching.csv
```

**预期**：30-50 词/种子 × 76 = ~2000-3500 行 CSV

---

## 3 · L2 Step 2e · KE Questions（~500-1000 词）

**操作**：
```
1. 同上 Keywords Explorer 已导入 76 词
2. 左边导航点 "Matching terms" → 上面切换到 "Questions" tab
   （或左导航直接 "Questions" 子菜单）
3. 顶部 Export → CSV
4. 保存到 /tmp/ahrefs-questions.csv
```

**预期**：how/what/why 开头问句词 ~500-1000

---

## 4 · L2 Step 4 · 5 站竞品 organic keywords（~3000-5000 词）

5 个域名分别跑 Site Explorer：

| # | 域名 | filter | 导出文件 |
|---|---|---|---|
| 1 | lindy.ai | (无 filter) | `/tmp/ahrefs-lindy.csv` |
| 2 | relevance.ai | (无 filter) | `/tmp/ahrefs-relevance.csv` |
| 3 | zapier.com | URL contains `/ai/` | `/tmp/ahrefs-zapier.csv` |
| 4 | n8n.io | (无 filter) | `/tmp/ahrefs-n8n.csv` |
| 5 | make.com | (无 filter) | `/tmp/ahrefs-make.csv` |

**操作**：
```
1. Ahrefs → Site Explorer
2. 输入域名（如 lindy.ai）→ Search
3. 左导航 Organic search → "Organic keywords"
4. 顶部 Filter:
   - Position: 1-100（默认）
   - Volume: 1+（去掉 0）
   - Country: United States
5. （仅 zapier）URL filter contains "/ai/"
6. 排序 by Traffic desc 或 Volume desc
7. 顶部 Export → CSV → top 1000
8. 保存到对应 /tmp/ahrefs-{domain}.csv
```

**预期**：每站 1000 行 × 5 = 5000 行（合并去重后 ~3000-4500 unique）

---

## 5 · trial 倒计时管理

trial 7 天内必须做：
- ✅ Step 2d/2e（本周）
- ✅ Step 4 5 站（本周）
- ⏳ L4 主库 v0 KD + Volume 精排（约 1 周后，主库做完 L3 后跑）
- ⏳ L7 主库 v1 最终精排（trial 期内最后 1-2 天用完）

**风险**：
- 🔑 trial 自动续约 → **第 6 天**记得手动 cancel 避免被扣 $99/月
- 🔑 CSV 数据**离线下载**保留——trial 结束后 Ahrefs 数据进不去，但 CSV 永久可用

---

## 6 · 激活后告诉 Agent B 什么

回到 conversation 告诉我：
1. ✅ trial 已激活（具体日期 + 时间 → 我标 expiry）
2. CSV 文件路径列表（如果按上面命名约定，我直接读 `/tmp/ahrefs-*.csv`）

我会立刻开始：
- 解析 7 个 CSV（matching + questions + 5 站）
- 跨源合并去重
- 进 L2 Step 5 4 级筛选漏斗
- 输出 `02-expanded-keywords.md` 主库 v0 300-500 词

---

## 7 · 76 词清单（参考 · 完整列表在 /tmp/pool-a-76-keywords.txt）

| # | 类型 | 关键词样本 |
|---|---|---|
| 1-46 | Step 4 ICP 痛点 | AI agent for code review / how to get amazon reviews without vine / cold email metrics that matter / ... |
| 47-59 | Step 5 产品语义 | AI proposal generator / AI ad creative generator / AI app builder / AI for ML research / ... |
| 60-66 | Step 6 EXPLORATORY | Generative Engine Optimization / Model Context Protocol / Claude Code workflow / Claude agent skills / llms.txt SEO / Answer Engine Optimization / Google AI Overview optimization |
| 67-76 | L2 Step 1 升级 | tasks entrepreneurs can automate / AI generated podcasts 2026 / how to build TikTok presence in 2026 / ... |

完整 76 词：cat /tmp/pool-a-76-keywords.txt
