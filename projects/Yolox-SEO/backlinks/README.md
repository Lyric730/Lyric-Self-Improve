# Yolox 外链建设

Yolox（**AI agent team platform**）的外链自动化建设工程。

## 📍 接手者从这里开始

| 优先 | 文件 | 用途 |
|---|---|---|
| 1 | **`AGENTS.md`** | 接手主入口（Codex / Claude / 其他 agent）— 1 分钟看完当前状态 |
| 2 | **`HANDOFF.md`** | 完整上下文 + 决策档案 + 风险评估 + outreach 候选清单 |
| 3 | **`TODO.md`** | 当前阶段 + 下一步任务（O 阶段 outreach）|
| 4 | `Yolox外链执行方案.md` | 完整方案 v3（1969 行，主参考） |

## 📁 目录索引

| 入口 | 用途 |
|---|---|
| `data/backlinks.db` | SQLite 主数据库（9 表，single source of truth） |
| `data/archive/ahrefs-raw/` | 21 个 ahrefs JSON 备份（已入库） |
| `data/gefei-226-resources.csv` | 226 池子 CSV 备份（已入库） |
| `data/yolox-related-projects.xlsx` | 24 个 Yolox 同行项目（已入库） |
| `scripts/init_db.py` | DB schema + 预灌（幂等） |
| `scripts/insert_ahrefs_json.py` | ahrefs JSON → DB |
| `scripts/scrape_ahrefs.py` | ⚠️ headless 被 Cloudflare 拦，用 MCP 浏览器路径 |
| `scripts/audit_profiles*.py` | Profile audit v1/v2 |
| `scripts/run-batch.py` | D 阶段批量调度（暂停中） |
| `outreach/status.md` | Outreach 状态看板（PR / 投稿 / 复核队列） |
| `outreach/226-review-candidates.csv` | 226 池子复核候选（155 条 blog_comment + url_field） |
| `.claude/skills/backlinks/*.md` | SOP（5 个 markdown，Codex 直接 read） |
| `refs/深度长文.md` | 35 篇社群学习材料综合 |

## 唯一 KPI

```sql
SELECT COUNT(*) FROM submissions
WHERE rel_actual='dofollow' AND status='live';
-- 当前 = 0
```

## 当前状态（2026-05-24）

- ✅ 知识体系：35 篇学习材料综合完毕（`refs/深度长文.md`）
- ✅ 行动手册：v3 完整（`Yolox外链执行方案.md`）
- ✅ 环境就位：Playwright MCP / 2 邮箱 / 数据库 9 表
- ✅ **F1 ahrefs 反推**：380 候选 + 24 个跨同行高频站
- ⏳ **GitHub awesome-vibe-coding PR**：[#195](https://github.com/filipecalegario/awesome-vibe-coding/pull/195) 已提交，等待维护者 merge
- 🔁 **226 池子复核**：不再整体废弃，改为只筛可投稿/可提交/低摩擦站点；`rel="me"` 仍不计入 KPI
- 🧊 **邮件 outreach**：Prismic / n8n / Zapier 降到最低优先级

## 流水线（修订版）

```
F1 ahrefs 反推（done）→ GitHub PR / showcase / 可提交站点
       ↓
226 池子复核（只挑可提交、可验证、低摩擦）
       ↓
  submissions 表记录 pending/submitted/live/rejected
       ↓
  submissions 表（rel_actual='dofollow' AND status='live'）⭐ 唯一 KPI
       ↓
  GSC + Ahrefs 监控
```

`邮件 outreach` 只作为补充，不作为当前主线。
