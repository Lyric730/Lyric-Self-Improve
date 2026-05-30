# Multi-Source Ingest Pipeline Implementation Plan

**Spec**: `docs/superpowers/specs/2026-03-28-multi-source-ingest-design.md`
**Created**: 2026-03-28
**Status**: In Progress

---

## Phase 1: X Fetcher — 支持 txt 格式 (小改)
- [ ] `discover_official_x_guest_rss.py`: `parse_handles()` 支持 `.txt` 文件（每行一个 handle）
- [ ] 测试：用 `seed_accounts.txt` 跑 fetcher，确认能解析 141 个 handle

## Phase 2: normalize.py — 分类逻辑 + article 全文抓取 (核心改动)
- [ ] 支持多个 `--guest-rss-catalog` 输入
- [ ] 新增 `--official-handles` 参数
- [ ] 检测 `x.com/i/article/{id}` → 标记为 article_x，用 jina.ai 抓全文
- [ ] 按账号归属分类：official handles → `official_x/`，其余 → `post_x/`
- [ ] 输出目录结构：`{out_root}/official_x/`、`{out_root}/article_x/`、`{out_root}/post_x/`
- [ ] 测试：用两份 catalog 跑 normalize，确认三个目录都有正确产出

## Phase 3: run_pipeline.sh L0 — 接入 official_x + post_x + normalize
- [ ] L0 段接入 official_x fetcher（13 账号）
- [ ] L0 段接入 post_x fetcher（141 seed 账号）
- [ ] L0 段接入 normalize（合并处理，自动分类）
- [ ] SOURCE_DIRS 自动收集 ingest 输出
- [ ] 测试：`--run-ingest --dry-run` 端到端验证

## Phase 4: run_pipeline.sh L0 — 接入 podcast
- [ ] L0 段接入 `discover_podcast_episodes.py`
- [ ] L0 段接入 `build_source_items.py` normalizer
- [ ] 确认 `podcast_discovery_registry.json` 有 feed 列表
- [ ] 测试：podcast source_items 正确输出到 `items/podcast/`

## Phase 5: 新建 discover_github_trending.py
- [ ] 创建 `pipeline/ingest/github/discover_github_trending.py`
- [ ] 用 jina.ai reader 抓取 GitHub Trending 页面
- [ ] 解析 repo 列表，输出 `source_item.json`
- [ ] 测试：确认输出格式与 SOURCE_ITEM_SCHEMA 兼容

## Phase 6: run_pipeline.sh L0 — 接入 github_trending
- [ ] L0 段接入 github_trending fetcher
- [ ] SOURCE_DIRS 包含 github_trending 输出
- [ ] 测试：github_trending source_items 正确输出

## Phase 7: 端到端 dry-run 测试
- [ ] 全部五源 ingest → normalize → topic_engine → writer
- [ ] 确认 cross_source_resonance_score 正确计算
- [ ] 确认 T02/T08 的 require_external_source 能被满足
- [ ] 确认 article_x 的全文内容进入 writer input

---

## Decisions Log
| Date | Decision | Reason |
|------|----------|--------|
| 2026-03-28 | article_x 由 normalize 自动检测，不建独立 fetcher | RSS 已能返回 article，只需分类 |
| 2026-03-28 | article 全文用 jina.ai reader，max_chars=5000 | 复用现有基础设施，成本可控 |
| 2026-03-28 | github trending 用 jina.ai 抓页面 | 无需 API key，简单可靠 |
