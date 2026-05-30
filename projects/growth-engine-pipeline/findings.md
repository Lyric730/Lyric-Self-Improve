# Findings — Multi-Source Ingest Pipeline

## 2026-03-28: 现状诊断

### Bug: official_x_account_profile.json 路径错误
- `discover_official_x_guest_rss.py` 和 `normalize.py` 默认路径指向 `content/pipeline/configs/...`（不存在）
- 实际文件在 `configs/image/official_x_account_profile.json`
- **已修复**

### Bug: run_pipeline.sh 调用 normalize.py 参数不匹配
- 脚本用 `--source-dir` / `--out-dir`，normalize.py 期望 `--guest-rss-catalog` / `--out-root`
- **已修复**

### 发现: Nitter RSS 能返回 X Article
- X Article URL 格式：`x.com/i/article/{id}`
- 在 @dotey 的 RSS 中确认：`title: x.com/i/article/203777295021...`
- description 中包含 `<a href="http://x.com/i/article/{id}">`
- 检测模式：正则 `x\.com/i/article/\d+`

### 发现: normalize.py 的 linked_source_enrichment
- 已在用 jina.ai reader (`r.jina.ai`) 抓推文外链内容
- `fetch_link_context()`: max_chars=5000, min_words=80
- 可直接复用于 X Article 全文抓取

### 发现: seed_accounts.txt 格式
- 每行一个 handle，部分带 `@` 前缀
- 141 个账号
- `parse_handles()` 当前只支持 JSON 格式的 account_profile

### 发现: podcast 代码已完整但未接入
- fetcher: `discover_podcast_episodes.py`
- transcript: `attach_podcast_transcript.py` + `batch_attach_podcast_transcripts.py`
- normalizer: `build_source_items.py`
- 需要 `podcast_discovery_registry.json` 有内容
