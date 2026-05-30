# 第 1 轮关键词调研归档（2026-04-22 → 2026-04-28）

## 归档原因

第 1 轮调研踩了 11 个坑（详见 `../../METHODOLOGY.md` §6）。和老板对接后决定**重做一遍**，约束新流程"方案先行"。
为避免新一轮被旧产出污染，把全部数据交付物归档到此处。

**这不是删除——是教材性留档**。下次方案审核时引用 §8 复用矩阵决定哪些复用、哪些弃用。

## 文件清单

| 文件 | 内容 | 第 2 轮处理建议 |
|---|---|---|
| `00-session-handoff.md` | Day 3 收尾 handoff（已 stale） | ❌ 弃（信息已合入 METHODOLOGY）|
| `01-seed-keywords.md` | 种子词 70 个 · Day 1 | 🟢 复用 ~60% + 补 40 词新种子 |
| `02-expanded-keywords.md` | 扩展词 325 个 · Day 2 | ❌ 弃 Claude 扩词部分（命中率 12.5%）|
| `03-reddit-quora-questions.md` | Reddit/Quora 真实问句 74 条 | 🟢 复用 + Day 2 再深挖 |
| `04-keyword-map-v1.md` | 200 词主库 + Priority 打分 · Day 3 | 🟡 参考结构，词重新打分 |
| `05-zero-volume-strategy.md` | 30 狙击词 + 4 选题纪律 · Day 4 | 🟡 大部分有效，重过 4 纪律 |
| `06-pillar-cluster-map.md` | 3 Pillar × 5 Cluster · Day 5 | 🟡 参考结构，可能调整 |
| `07-negative-keywords.md` | 117 负向词 · Day 3 | 🟢 直接复用 |
| `10-tier1-audit-and-sop.md` | Tier 1 40 词逐词审计 + SOP v1 | 🟢 SOP 框架复用 |
| `11-gakp-keywords-220.txt` | GAKP 输入词单 217 词 | 🟢 复用作 Day 2 GAKP 输入 |
| `11-volume-validation-guide.md` | GAKP + GT 验证 4 步指南 | 🟢 流程复用 |
| `REVIEW-index.md` | 给 leadership 的本周审核索引 | ❌ 弃（已对接完成）|
| `p1-verdict.csv` | Tier 1 40 词 P1 验证原始信号 | 🟡 部分复用（词没变就有效）|
| `raw-gakp-historical.csv` | **GAKP 217 词 27 月历史 · 重要原始数据** | 🟢 **直接复用**（27 月历史不会变） |

## 重要原始数据（下次复用）

- **`raw-gakp-historical.csv`** —— GAKP 217 词 × 27 月逐月数据 + yoy 同比 + competition + CPC 区间。这是花了不少时间获取的原始数据，27 个月的历史**不会因为重做调研而失效**。
  - 关键发现：12 词有 volume（多数 50/mo），205 词显示 "---"
  - llms.txt 生态：6/6 全有量 + 多个 yoy +900%/+∞（Pillar 1 决策依据）
  - "how to close more sales faster" yoy -100%（已确认死词）

- **`p1-verdict.csv`** —— Tier 1 40 词 opencli P1 验证结果（17🟢/23🟡/0🔴）。如果第 2 轮的 Tier 1 词与第 1 轮重叠，可以直接复用。

## 第 1 轮的 11 个坑速查（对应规避动作）

| # | 坑 | 第 2 轮规避动作 |
|---|---|---|
| 1 | 验证递归循环 | Day 4 设硬性截止 |
| 2 | Claude 扩词命中率 12.5% | Day 2 禁用路径 A，默认 B+C+D |
| 3 | Reddit show-off 帖陷阱 | 只留**问题型**帖子 |
| 4 | Reddit 1/1 score 孤例 | 进 Tier 1 必须 ≥10 评论 OR ≥2 帖子 |
| 5 | 内部 Agent 人名 ≠ 搜索词 | Day 1 种子词审核就过滤人名 |
| 6 | GAKP Forecast vs Historical 混淆 | Day 4 前 5 分钟检查标签 |
| 7 | GAKP CSV UTF-16 LE 乱码 | iconv 模板命令写进 Day 4 checklist |
| 8 | Volume 区间够不够 | 接受区间 + 同比方向 |
| 9 | Pillar 拍脑袋 | Day 5 前必须有 GAKP 数据 |
| 10 | yoy +∞ 是真信号 | 主动找 +∞ 词作为 Pillar 候选 |
| 11 | Handoff stale | session 第一件事 git status |

详细规避见 `../../METHODOLOGY.md` §9.4。

## 不要再用的文件

- `REVIEW-index.md` —— 给 leadership 的成果索引，已经对接过，不再有效
- `00-session-handoff.md` —— 第 1 轮的 Day 3 中段 handoff，所有信息已合并到 METHODOLOGY

---

**归档日期**：2026-04-28
**第 2 轮启动条件**：方案文档审核通过后
