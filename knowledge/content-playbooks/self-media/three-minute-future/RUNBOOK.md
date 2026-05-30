# 三分钟未来 · 运行手册

> 总入口：先读 `PRODUCTION_LINE.md`。本文件保留分步命令和调试细节；如果和 `PRODUCTION_LINE.md` 冲突，以 `PRODUCTION_LINE.md` 为准。

## 日期规则

这条产线现在把两个日期分开：

- `publishDate`：页面上显示的日期，也是 `daily/<date>/...` 输出目录。
- `contentDate`：本期实际抓取和筛选的新闻日期。

默认规则是：`publishDate` 做页面日期，`contentDate = publishDate - 1 day`。例如：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3
```

等价于：

```text
publishDate = 2026-05-25
contentDate = 2026-05-24
```

如果要做同日加更，只抓取 `publishDate` 当日已出现的增量内容，需要显式指定 `--content-date`：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24 --stop-after select --min-score 2
```

同日加更会先查已发布账本，排除已经发过的 URL、标题、主题簇和图片。账本位置：

```text
daily/_state/three-minute-future/published-ledger.json
```

人工确认某一期已经发布后，写入账本：

```powershell
python lines\three-minute-future\mark_published.py 2026-05-24 --vol 2
```

被过滤掉的重复候选会写到：

```text
daily/<publishDate>/three-minute-future/work/filtered-published.json
```

## 当前可跑步骤

一键跑完整日产线：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3
```

先抓取、精读、排序，停在选题审核：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --stop-after select
```

选题和封面确认后，从文案生成继续跑到 PNG：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --start-at copy --cover-image daily\2026-05-24\three-minute-future\work\cover\cover.png
```

只重新渲染和导出：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --start-at render
```

封面生图当前是人工确认节点：脚本可以接收 `--cover-image` 并继续自动渲染导出；如果正式发布必须有封面图，可以加 `--require-cover`，避免兜底背景混进发布包。

下面是分段命令，方便单独调试某一步。

抓候选：

```powershell
python lines\three-minute-future\fetch_candidates.py 2026-05-23
```

抓详情与图片：

```powershell
python lines\three-minute-future\enrich_assets.py 2026-05-23 --limit 30 --min-score 3
```

选题排序：

```powershell
python lines\three-minute-future\select_items.py 2026-05-23 --limit 15
```

默认最多 15 条，选出来多少条就生成多少个内页，不为了凑满 15 条硬塞弱内容。

默认 15 条目标配比：

- AI Hot：8 条
- 外部新闻：5 条
- 国内媒体：2 条

如果某个桶的候选质量不够，再用高分候选回填，不为了凑比例硬塞弱内容。

关键词免费素材兜底：

```powershell
python lines\three-minute-future\search_keyword_images.py 2026-05-23
```

当内容涉及 Meta、Starbucks、Google、X、OpenAI、NVIDIA 等公司时，脚本会优先找 logo / 招牌 / 门店 / 总部建筑，但不在版式里叠加品牌 slogan。公司规则在：

```text
lines\three-minute-future\config\visual_asset_policy.json
```

如果帖子截图不满意，可以让关键词素材覆盖截图兜底：

```powershell
python lines\three-minute-future\search_keyword_images.py 2026-05-23 --prefer-keyword
```

缺图时截取来源页面：

```powershell
python lines\three-minute-future\capture_source_screenshots.py 2026-05-23
```

生成可预览 HTML：

```powershell
python lines\three-minute-future\render_pages.py 2026-05-23
```

打开 Codex 侧边栏实时预览：

```powershell
python lines\three-minute-future\serve_preview.py 2026-05-23 --port 58417
```

然后在侧边栏打开：

```text
http://localhost:58417/
```

导出发布 PNG：

```powershell
python lines\three-minute-future\screenshot_pages.py 2026-05-23
```

## 2026-05-23 试跑结果

候选池：

- 总候选：113 条
- 命中现实影响标签：54 条
- 代表选题：
  - AI 替代入门级工作
  - 星巴克叫停 AI 库存系统
  - 人形机器人管理平台
  - AI 医助进入基层医疗
  - AI 与裁员、招聘、教育抗议等现实场景

详情与图片：

- 详情精读：30 条里 28 条成功
- 有效图片：30 条里 4 条达标
- 原因：Google News RSS 多数是中转页，页面图是 300×300 的 Google News 占位图，不能作为正文配图。

## 当前判断

候选源方向成立，但图片链路不能只靠 `og:image`。

下一步需要补：

- 原文 URL 解析：把 Google News 中转链接尽量还原到原站。
- 搜索配图：对标题和关键词做二次搜索；自动化默认先用 Wikimedia Commons 这类能记录授权的免费商用素材，避免图搜素材版权不清。
- 公司配图：优先品牌现场，不接受 logo 太小、主体不可识别的泛建筑图。
- 白名单源：IT之家、公司博客、官方新闻稿、政府/法院页面、主流媒体页面优先抓正文大图。
- 素材质量检查：尺寸、文件大小、是否 logo / 占位图、是否适合竖屏重构。
- 排序策略：AI Hot 权重高于外部新闻；默认最多 15 条，目标配比 `8:5:2`，即 AI Hot 8 条、外部新闻 5 条、国内媒体 2 条；选出来多少条就做多少个内页，不硬凑；医疗资讯降权并限制数量；具体权重看 `config/selection_policy.json`。
- 图片策略：一张图只使用一次；缺图先截原文；封面不使用内页新闻图，生图优先。
- 视觉效果：静态内页默认清晰优先，快闪感放在边框、ticker、色差、扫描线；重度霓虹闪烁和高斯模糊留给视频转场。

## 已有脚本

- `fetch_candidates.py`：AI HOT + Google News RSS 候选池
- `enrich_assets.py`：详情抓取 + OG 图 / 正文大图下载
- `select_items.py`：按最多 15 条、目标 `8:5:2` 默认配比选题
- `search_keyword_images.py`：按标题关键词搜索免费商用兜底图，并记录授权信息
- `capture_source_screenshots.py`：缺图时截取来源页面作为素材
- `generate_final.py`：生成当天最终文案、VOL、账号名、封面配置
- `render_pages.py`：渲染封面和内页 HTML，并生成 `live-preview.html` / `index.html`
- `serve_preview.py`：把当天 `publish` 目录服务到本地端口，供 Codex 侧边栏实时预览
- `screenshot_pages.py`：把 HTML 页面导出为发布 PNG
- `run_daily.py`：串联抓源、精读、选题、文案、配图、渲染、导出的总控脚本
- `config/visual_asset_policy.json`：公司视觉、X 截图和清晰度 / 快闪效果策略
