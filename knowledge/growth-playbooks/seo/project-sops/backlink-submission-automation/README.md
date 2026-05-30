# Backlink Submission Automation SOP

交付等级：🟡 可用

最后整理：2026-05-30

来源项目：

- [projects/backlink-submission-automation/SKILL.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/SKILL.md)
- [projects/backlink-submission-automation/SKILL.zh-CN.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/SKILL.zh-CN.md)
- [projects/backlink-submission-automation/references/sql-workflows.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/references/sql-workflows.md)
- [projects/backlink-submission-automation/references/submission-sop.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/references/submission-sop.md)
- [projects/backlink-submission-automation/references/data-contract.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/references/data-contract.md)
- [projects/backlink-submission-automation/references/environment.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/references/environment.md)
- [projects/backlink-submission-automation/references/source-to-candidate.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/references/source-to-candidate.md)
- [projects/backlink-submission-automation/references/verification-and-reporting.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/references/verification-and-reporting.md)

## 这份 SOP 解决什么

把外链提交从“靠一堆 Python 脚本点状操作”收敛成一条可审计流程：

1. 用结构化 intake 建 campaign profile。
2. 用 SQLite 存候选站点、提交记录、账号、错误模式。
3. 候选导入、排序、写库、报表优先走 SQL workflow。
4. Python 只保留小工具：profile 初始化、首页截图 fallback、静态 rel 验证。
5. 真实提交必须走已授权交互式浏览器，不能用 headless Playwright 假装完成。

唯一硬 KPI：

```sql
SELECT COUNT(*)
FROM submissions
WHERE status='live' AND rel_actual='dofollow';
```

`pending_review`、`nofollow/ugc`、纯文本 URL 都不能算 dofollow KPI。

## 什么时候用

适合：

- AI tool / SaaS / directory / showcase / awesome-list / profile 型外链提交
- 需要把提交、验证、重试、交接写进 SQLite 的场景
- 团队已经有候选包 CSV，希望复制给新 campaign 直接跑

不适合：

- 纯邮件 outreach
- 必须强依赖登录后台但无法公开验证链接的站点
- 需要保存敏感账号、cookie、密钥到知识库的流程

## 输入和产物

### 输入

- 产品 profile：品牌名、官网、联系人、类目、素材、禁用词
- 候选来源：CSV、预打包 candidate pack、旧 SQLite、LXX/Ahrefs 导出
- 可操作浏览器：Codex Chrome Extension 或同类已授权交互式控制器

### 产物

- `campaigns/<campaign-slug>/profile/`
- `campaigns/<campaign-slug>/data/backlinks.db`
- `candidate-packs/*.csv` 作为可分发候选资产
- `submissions` / `submission_attempts` / `error_patterns` / `account_credentials` 记录

## 首次启动

### 1. 建 profile

```bash
python skills/backlink-submission-automation/scripts/init_campaign_profile.py \
  --campaign-root campaigns \
  --answers-json path/to/structured-answers.json
```

`answers.json` 里必须记录 `intake.mode`，区分原生结构化、混合结构化、Markdown fallback、文件导入。

### 2. 初始化数据库

打开 [projects/backlink-submission-automation/references/sql-workflows.md](/F:/Making%20money/Lyric-Self-Improve/projects/backlink-submission-automation/references/sql-workflows.md)，依次执行：

1. `Bootstrap Schema`
2. `Live Write Guards`
3. `Seed Profile Basics`

这一版的关键变化是：DB 初始化、迁移、候选导入、排序、写提交、报表都转成 SQL-first，不再依赖一组独立 Python CLI。

## 执行主流程

### 1. 导入候选

候选包默认字段顺序：

```text
id,source_id,source,domain,url,dr,traffic,category,submission_type,priority,notes
```

执行 `sql-workflows.md` 里的 `Import Candidate CSV`：

- prepared pack 直接指向 `candidate-packs/*.csv`
- 自己导出的 CSV 也先规整到同一字段顺序
- 导入时自动补 `evidence_score`
- 已有记录走 `ON CONFLICT(source, url)` 更新，不重复造脏数据

### 2. 选下一批

执行 `Select Next Candidates`，它综合：

- DR
- `priority`
- 产品关键词相关性
- 公共提交证据
- 摩擦成本，如 `captcha`、`manual_hold=true`、`paid=true`

结论：这里已经不是“只按 DR 排序”的外链表，而是一个带风险过滤的队列。

### 3. 真实提交

真实提交必须满足：

- 用真实浏览器 profile
- 支持 cookies、OAuth、文件上传、人机验证交接
- 不用 headless Playwright 点真实 `submit/save/publish`

逐站 preflight：

1. 打开页面并等待稳定。
2. 滚到底。
3. 检查 footer、导航、账号菜单、弹窗、iframe、嵌入表单。
4. 尝试 `Submit`、`Add tool`、`List your product`、`Claim profile`、`Contribute` 等入口。
5. 没有 website 字段但有 bio/description 时，尝试自然写入 URL，再看是否渲染成真实链接。

### 4. 立即写库

提交刚被接受时，只能写：

- `submitted`
- `pending`
- `pending_review`
- `pending_email_confirmation`
- `pending_human_verification`

如果创建了账号，同时写 `account_credentials`。

失败尝试要写 `submission_attempts`，同类错误累计进 `error_patterns`。

### 5. 公网验证后再改 live

只有公网证据成立，才能把记录改成 `live` 或 `live_plain_text`。

写 `live` 之前强制要求：

- `live_url`
- `verification_evidence`
- `rel_actual` 不是 `unknown`

静态 HTML 用：

```bash
python skills/backlink-submission-automation/scripts/verify_rel.py \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --submission-id 123 \
  --url https://example.com/products/product-name \
  --target-domain product.example
```

JS 渲染页用浏览器看公开 DOM，再执行 `Record Live After Verification`。

## 数据约束

### 常用 `submissions.status`

- `submitted`
- `pending_review`
- `pending_email_confirmation`
- `pending_human_verification`
- `blocked_browser_controller`
- `blocked_auth`
- `blocked_captcha`
- `failed`
- `failed_after_3_attempts`
- `skipped`
- `live`
- `live_plain_text`

### 常用 `rel_actual`

- `dofollow`
- `nofollow`
- `ugc`
- `nofollow_ugc`
- `sponsored`
- `me_no_pagerank`
- `live_plain_text`
- `no_link_found`
- `pending_expected_dofollow`
- `unknown`

### 重试规则

- 单条 submission 最多 3 次
- 同类错误累计 3 次，先停下来做 1 次优化
- 优化后再复发，标 `unresolved_high_priority`，绕路继续

## 对 solo-op 最重要的几条硬规则

1. 先记数据库，再谈“感觉成功了”。
2. 先分 `submitted/pending_review/live`，不要混。
3. 只把 `live + dofollow` 算 KPI。
4. candidate pack 是源资产，不是运行输出。
5. 不把 cookie、账号密码、手机号、密钥抄进知识库。

## 这次和旧流程相比，真正变了什么

| 旧习惯 | 新约束 |
| --- | --- |
| Python CLI 分散做 DB 操作 | SQL workflow 统一做 DB 初始化、导入、排序、写库、报表 |
| live 规则主要靠脚本参数约束 | DB trigger 直接拦截缺证据的 live 写入 |
| 候选导入更像一次性脚本 | 候选包成为 Skill 随包资产，可复制复用 |
| 提交流程和数据流程耦合在脚本里 | 浏览器执行和 SQLite 记账明确拆层 |

## 归档建议

- 如果后面继续迭代这个项目，优先看源项目里的 `references/sql-workflows.md`
- 如果只是做日常外链执行，优先看这份 SOP，再按需回源项目
- 如果 Yolox 外链 workflow 跟着切到 SQL-first，再补更新 [knowledge/growth-playbooks/seo/project-sops/yolox-seo/workflows/backlink-workflow.md](/F:/Making%20money/Lyric-Self-Improve/knowledge/growth-playbooks/seo/project-sops/yolox-seo/workflows/backlink-workflow.md)
