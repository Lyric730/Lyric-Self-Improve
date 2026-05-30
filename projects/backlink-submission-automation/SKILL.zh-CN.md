# 外链提交建设自动化 Skill（中文审阅版）

> 本文件给人审阅。Agent 正式入口是 `SKILL.md`。
> 本 Skill 是通用版，不绑定任何具体产品。产品名、官网、定位、HQ、素材、禁用词、DR 阈值、人工保留平台都从 campaign profile 读取。

## 目标

为任意产品建立一条可审计、可交接的外链提交流程。

唯一 KPI：

```sql
SELECT COUNT(*)
FROM submissions
WHERE status='live' AND rel_actual='dofollow';
```

不要把 `pending_review`、`nofollow/ugc`、纯文本 URL 说成已建成 dofollow 外链。

## Skill 包结构

```text
backlink-submission-automation/
  SKILL.md
  SKILL.zh-CN.md
  agents/openai.yaml
  assets/
    intake-schema.json
    structured-answers.example.json
  candidate-packs/
    manifest.json
    starter-pack.csv
    lxx-ai.csv
    ahrefs-competitor-backlinks.csv
    legacy-226-review.csv
  references/
  scripts/
```

候选包是 Skill 文件夹的一部分。通过 Git clone、ZIP、或复制整个文件夹安装时，CSV 候选包一起交付。用户不需要拥有原始 SQLite、LXX 邀请码或 Ahrefs 账号才能使用已打包候选包。

## 启动输入

没有选定 profile 时，Agent 按顺序收集：

1. 优先使用宿主的原生结构化输入：Codex Asked、Claude/Gemini 表单适配器、JSON schema 表单、CLI prompt wizard。
2. 结构化能力不完整时，用混合模式：选择题走结构化，自由文本写 JSON。
3. 没有结构化能力时，才用普通 Markdown 问卷。
4. 无人值守时，直接读取 `--answers-json`、`--import-path` 或已有 profile 文件夹。

Agent 必须在 answers JSON 里记录 `intake.mode`：

| 值 | 含义 |
|---|---|
| `native_structured` | 使用宿主原生结构化输入 |
| `hybrid_structured` | 选择题结构化，文本字段用 JSON/普通消息 |
| `markdown_fallback` | 只能普通消息问卷 |
| `file_import` | 读取已有 answers/profile |

字段契约见 `assets/intake-schema.json`。

## 首次运行

创建或导入 profile：

```bash
python skills/backlink-submission-automation/scripts/init_campaign_profile.py \
  --campaign-root campaigns \
  --answers-json path/to/structured-answers.json
```

初始化数据库：

```bash
python skills/backlink-submission-automation/scripts/bootstrap_backlink_db.py \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --profile campaigns/<campaign-slug>/profile/profile.json
```

导入候选包：

```bash
python skills/backlink-submission-automation/scripts/import_candidates.py \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --csv skills/backlink-submission-automation/candidate-packs/lxx-ai.csv \
  --source lxx_ai
```

查看下一批：

```bash
python skills/backlink-submission-automation/scripts/next_candidates.py \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --limit 10
```

## 执行规则

真实提交必须使用当前 Agent 的已授权交互式真实浏览器控制器：

| Agent / 运行环境 | 真实提交默认执行器 |
|---|---|
| Codex | Codex Chrome Extension 控制用户 Chrome |
| Claude Code | browser MCP / 浏览器插件 / Chrome control，必须连到用户已登录 profile |
| Gemini / 自研 Agent | 已授权交互式浏览器控制器，必须支持 cookies、OAuth、文件上传、人机验证交接 |

禁止用 headless Playwright 点真实 `submit/save/publish`。Playwright 只允许做 smoke、静态 HTML 检查、未登录只读预检、截图 fallback。

每个候选页面必须：

1. 打开页面并等待加载。
2. 滚到底部。
3. 检查 footer、导航、账号菜单、下拉菜单、弹窗、iframe、嵌入表单。
4. 尝试 `Submit`、`Add tool`、`List your product`、`Add startup`、`Claim profile`、`Contribute` 等入口。
5. 没有 website 字段但有 public description/bio 时，把目标 URL 自然写入 description，再验证是否渲染成真实 `<a href>`。

## 排序规则

候选排序不只看 DR。`next_candidates.py` 会综合：

- DR
- 已存 `priority`
- 产品 profile 相关性
- 公开链接证据，如 dofollow 样本、website 字段、可提交入口
- 摩擦和风险，如 CAPTCHA、付费、manual hold、nofollow/ugc

DR 低于 profile 阈值默认跳过。DR 20-39 只有高相关、低摩擦时才值得做。

## 记录和验证

提交后先记录为 `submitted` 或 `pending_review`。不能因为看到成功页就标 `live`。

`record_submission.py submission` 对 `status=live` / `status=live_plain_text` 强制要求：

- `--verified`
- `--evidence`
- `--live-url`
- `--rel`，其中 `live` 不能是 `unknown`、`no_link_found`、`pending_expected_dofollow`、`live_plain_text`

静态 HTML 可用：

```bash
python skills/backlink-submission-automation/scripts/verify_rel.py \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --submission-id 123 \
  --url https://example.com/products/product-name \
  --target-domain product.example
```

JS 渲染页面需要用真实浏览器检查 DOM，再带证据写库：

```bash
python skills/backlink-submission-automation/scripts/record_submission.py submission \
  --db campaigns/<campaign-slug>/data/backlinks.db \
  --id 123 \
  --status live \
  --rel nofollow \
  --live-url https://example.com/products/product-name \
  --verified \
  --evidence "logged-out DOM showed public anchor rel=nofollow"
```

## 状态值

常用 `submissions.status`：

- `submitted`
- `pending_review`
- `pending_email_confirmation`
- `pending_human_verification`
- `blocked_browser_controller`
- `blocked_auth`
- `blocked_captcha` / `blocked_recaptcha` / `blocked_turnstile`
- `failed`
- `failed_after_3_attempts`
- `skipped` / `skipped_low_dr` / `skipped_manual_hold` / `skipped_no_submission_form` / `skipped_no_public_link`
- `live`
- `live_plain_text`

常用 `rel_actual`：

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

## 候选包维护

候选包是源资产，不是运行输出。正常 campaign 不要把结果写回 `candidate-packs/`。

刷新候选包时，手动导出 CSV，确认非空，再替换对应文件。不要用 0 行导出覆盖已有包。

可从 canonical DB 导出参考 SQL：

```sql
SELECT source_id, source, domain, url, dr, traffic, category,
       submission_type, priority, relevance_score, evidence_score, notes
FROM candidates
WHERE status IN ('new', 'queued')
  AND (dr IS NULL OR dr >= 20)
ORDER BY priority DESC, relevance_score DESC, evidence_score DESC, COALESCE(dr, 0) DESC;
```

## 交付前检查

1. 每个尝试过的网站都有 `submissions` 记录。
2. 每个失败尝试都有 `submission_attempts` 记录。
3. 同类错误 3 次以上，必须进入 `error_patterns`。
4. 同一错误只优化一次；仍失败则标 `unresolved_high_priority`。
5. live 状态有公开证据。
6. KPI 从 SQL 重算。
7. pending、nofollow、plain text、failed、skipped 分开汇报。
8. 用过的浏览器标签页已关闭，除非特意留给人工验证。
