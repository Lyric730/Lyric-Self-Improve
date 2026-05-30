# Multi-Source Ingest Pipeline Design

- **日期**: 2026-03-28
- **状态**: Active
- **关联产品**: Growth Engine Pipeline

---

## 1. Problem Statement

Topic engine 设计了五源架构（official_x / article_x / post_x / podcast / github_trending），但实际只接了 official_x 一根管子。导致：

- `cross_source_resonance_score`（权重 25%）被浪费，单源永远 50 分
- T02（信号解码）、T08（信号转行动）的 `require_external_source` 永远不满足
- topic 聚类退化为单源罗列，无热度验证

## 2. Design Overview

Ingest 层按数据源独立抓取，Normalize 层按内容类型自动分类。

### 2.1 X 源分类逻辑

```
RSS item 含 x.com/i/article/{id} → article_x
    ↓ 同时用 jina.ai reader 抓 article 全文
其余 → 看账号归属：
    官方 13 账号 → official_x
    seed 141 账号 → post_x
```

### 2.2 五源接入表

| 源 | Fetcher | 改动 | 说明 |
|----|---------|------|------|
| official_x | `discover_official_x_guest_rss.py` | 已修好 | 13 个官方账号 |
| post_x | 复用同一个 fetcher | 新增调用 | seed_accounts.txt（141 账号） |
| article_x | 无独立 fetcher | 改 normalize | normalize 检测 article URL → 归类 + 抓全文 |
| podcast | `discover_podcast_episodes.py` | 接入 run_pipeline.sh | 代码已有 |
| github_trending | 新建 fetcher | 新建 | 抓 GitHub Trending |

## 3. Detailed Changes

### 3.1 normalize.py — 分类 + article 全文抓取

**现状**：所有 RSS item 统一输出为 `source_kind: "x_thread"`，不区分内容类型，不区分账号归属。

**改动**：

1. 新增 `--official-handles` 参数，接收官方账号列表（JSON 或 txt）
2. 支持多个 `--guest-rss-catalog` 输入（合并处理）
3. 分类逻辑：
   - 检测 RSS item 的 description/title/link 中是否含 `x.com/i/article/{id}` 模式
   - 是 article → `source_kind: "x_article"`，用 jina.ai reader 抓全文，输出到 `{out_root}/article_x/{source_id}/`
   - 否 article + 账号在 official handles 列表 → `source_kind: "x_thread"`，输出到 `{out_root}/official_x/{source_id}/`
   - 否 article + 账号不在 official handles → `source_kind: "x_thread"`，输出到 `{out_root}/post_x/{source_id}/`
4. article 全文抓取复用现有 `fetch_link_context()`，`max_chars=5000`

### 3.2 discover_official_x_guest_rss.py — 支持 txt 格式

**现状**：`--account-profile` 只接受 JSON 格式。

**改动**：

1. `parse_handles()` 检测文件扩展名
2. `.txt` → 每行一个 handle（支持 `@` 前缀和空行/注释行 `#`）
3. `.json` → 保持现有逻辑

### 3.3 run_pipeline.sh L0 段 — 接入全部源

```bash
# 1. official_x（13 官方账号）
python3 pipeline/ingest/x/discover_official_x_guest_rss.py \
    --account-profile configs/image/official_x_account_profile.json \
    --out-dir "${INGEST_OUT}/official_x"

# 2. post_x（141 seed 账号）
python3 pipeline/ingest/x/discover_official_x_guest_rss.py \
    --account-profile configs/frameworks/seed_accounts.txt \
    --out-dir "${INGEST_OUT}/post_x"

# 3. normalize（合并处理，自动分类）
python3 pipeline/ingest/normalize.py \
    --guest-rss-catalog "${INGEST_OUT}/official_x/guest_rss_catalog.json" \
    --guest-rss-catalog "${INGEST_OUT}/post_x/guest_rss_catalog.json" \
    --official-handles configs/image/official_x_account_profile.json \
    --out-root "${INGEST_OUT}/items"

# 4. podcast
python3 pipeline/ingest/podcast/discover_podcast_episodes.py \
    --out-dir "${INGEST_OUT}/podcast"
python3 pipeline/ingest/build_source_items.py \
    --episode-catalog "${INGEST_OUT}/podcast/episode_catalog.json" \
    --out-root "${INGEST_OUT}/items/podcast"

# 5. github_trending
python3 pipeline/ingest/github/discover_github_trending.py \
    --out-dir "${INGEST_OUT}/github_trending/items"
```

Source dirs 自动收集 `${INGEST_OUT}/items/` 下所有子目录。

### 3.4 新建 discover_github_trending.py

**位置**：`pipeline/ingest/github/discover_github_trending.py`

**功能**：
- 抓取 GitHub Trending 页面（`https://github.com/trending`）
- 通过 jina.ai reader 获取页面内容，解析 repo 列表
- 输出 `source_item.json`：
  - `platform: "github"`
  - `source_kind: "github_repo"`
  - `source_family` 由 topic_engine 按路径推断为 `github_trending`

**参数**：
- `--out-dir`：输出目录
- `--language`：过滤语言（可选，如 python/javascript）
- `--since`：时间范围（daily/weekly，默认 daily）

### 3.5 podcast 接入

**现有代码**：
- `discover_podcast_episodes.py` — fetcher
- `attach_podcast_transcript.py` — transcript 附加
- `build_source_items.py` — normalizer

**改动**：仅在 `run_pipeline.sh` 中串联调用，代码本身不需要改。

**前提**：`configs/frameworks/podcast_discovery_registry.json` 中需要有 feed 列表。

## 4. Directory Structure After Implementation

```
runtime/runs/{RUN_ID}/00_ingest/
├── official_x/
│   └── guest_rss_catalog.json        # 13 官方账号 RSS
├── post_x/
│   └── guest_rss_catalog.json        # 141 seed 账号 RSS
├── podcast/
│   └── episode_catalog.json          # podcast episodes
├── github_trending/
│   └── items/                        # github trending repos
└── items/                            # normalize 输出（分类后）
    ├── official_x/
    │   └── x-anthropicai-{hash}/source_item.json
    ├── article_x/
    │   └── x-dotey-{hash}/source_item.json      # 含全文
    ├── post_x/
    │   └── x-karpathy-{hash}/source_item.json
    └── podcast/
        └── podcast-{hash}/source_item.json
```

## 5. What Does NOT Change

- `topic_engine.py` — `infer_source_family()` 按目录路径推断，新目录结构天然兼容
- `topic_engine_policy.v1.json` — source_roles 已定义
- `lane_framework_map.v1.json` — lane requirements 已配好
- `linked_source_enrichment.py` — 复用现有 jina.ai reader
- writer 层完全不需要改

## 6. Expected Outcome

接通后一个 topic 的典型素材组成：

```
topic: "Anthropic 发布 Claude Code auto mode"
  ├─ official_x: @AnthropicAI 的发布推文 (fact_base, event seed)
  ├─ article_x:  @dotey 写的 X Article 深度分析 (fact_base)
  ├─ post_x:     5 条 KOL 讨论推文 (heat_signal)
  └─ cross_source_resonance: 3 families → 25+75=100 分（满分）
```

## 7. Implementation Order

1. `discover_official_x_guest_rss.py` — 支持 txt 格式（小改）
2. `normalize.py` — 分类逻辑 + article 全文抓取（核心改动）
3. `run_pipeline.sh` L0 段 — 接入 official_x + post_x + normalize
4. `run_pipeline.sh` L0 段 — 接入 podcast
5. `discover_github_trending.py` — 新建 fetcher
6. `run_pipeline.sh` L0 段 — 接入 github_trending
7. 端到端 dry-run 测试
