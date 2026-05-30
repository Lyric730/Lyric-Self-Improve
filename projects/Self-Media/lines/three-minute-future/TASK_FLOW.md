# 三分钟未来 · 任务拆解

## 日期与去重规则

状态：已接入源头脚本

规则：
- 常规日报：`publishDate` 做页面日期，默认抓取前一自然日完整 24 小时内容，即 `contentDate = publishDate - 1 day`。
- 同日加更：`publishDate` 和 `contentDate` 相同，但必须显式传入 `--content-date <YYYY-MM-DD>`。
- Selection 默认读取 `daily/_state/three-minute-future/published-ledger.json`，排除已经发过的 URL、标题、主题簇和图片。
- 5 月 23 日第一期已写入账本；后续 5 月 24 日增量内容不会再重复第一期主题。

命令：

```powershell
# 常规日报：2026.05.25 发布 2026.05.24 完整内容
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3

# 同日加更：2026.05.24 发布 2026.05.24 当日增量内容
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24 --stop-after select --min-score 2

# 人工确认发布后写入账本
python lines\three-minute-future\mark_published.py 2026-05-24 --vol 2
```

验收：
- `candidates.json`、`enriched.json`、`selection.json`、`final.json` 都保留 `publishDate` 和 `contentDate`。
- `filtered-published.json` 能看到被账本过滤掉的候选。
- 不为了凑满 15 条而塞入无现实标签的弱内容；选出来多少条就做多少个内页。

## 0. 规格冻结

状态：已完成

产物：

- `PLAN.md`
- `VISUAL_BRIEF.md`

关键决策：

- AI 为主，外扩只收“AI 改变现实”的事。
- 封面使用固定栏目包装层 + 当天素材重组背景。
- 固定背景只做兜底。
- 配图优先真实素材，AI 生图兜底。

## 1. 候选池抓取

状态：初版完成

目标：

- 从 `AI HOT` 抓 AI 圈基础候选。
- 从新闻检索补“现实影响”候选。
- 合并、去重、打初筛标签。

输出：

- `daily/<date>/three-minute-future/work/candidates.json`

验收：

- 每天至少有 20 条候选。
- 至少 5 条带有现实场景标签，例如法律、教育、劳动、机器人、医疗、零售、国防、影视、硬件、政策。
- 每条包含标题、来源、URL、发布时间、初筛分数、标签。

## 2. 详情精读与图片候选

状态：初版完成

目标：

- 打开候选 URL，提取正文摘要、`og:image`、原文标题、来源站点。
- 对 X 链接抓推文正文与媒体图。
- 对新闻链接优先下载原新闻图或 OG 图。
- 当新闻涉及明确公司时，优先抓公司 logo / 招牌 / 门店 / 总部建筑，但不叠加品牌 slogan。

输出：

- `daily/<date>/three-minute-future/work/enriched.json`
- `daily/<date>/three-minute-future/work/assets/`

验收：

- 入选候选尽量都有图片候选。
- 明确标出图片来源：原图、OG 图、官网图、媒体图、AI 兜底。

当前结论：

- 文章直连源可以抓正文大图。
- Google News RSS 适合发现候选，但中转 URL 不适合直接抓素材。
- 下一步需要增加“原文 URL 解析 / 白名单源”能力。
- 已增加关键词免费素材兜底：原文无图或截图不可用时，按标题关键词找可免费商用的相关图片，并记录授权来源。
- 已增加公司视觉规则：公司相关内容不再优先使用泛建筑图，除非图中能清楚看到品牌主体。

## 3. 选题排序

状态：执行中

目标：

- 从候选池里最多选 15 条，选出来多少条就生成多少个内页。
- 选出当天封面主事件。

筛选标准：

- 一眼能懂。
- 和 AI 改变现实有关。
- 有真实场景。
- 有好图。
- 不只是模型、论文、工具小更新。
- 国外 / 海外信息源优先。
- 国内媒体降权，但不硬删。
- 医疗类资讯降权，每期默认最多 1 条。
- 默认最多 15 条，目标配比为 AI HOT 8 条、外部新闻 5 条、国内媒体 2 条。
- 某一类候选不足时，用剩余高分候选回填，不为了比例硬塞弱内容。
- 具体权重写在 `config/selection_policy.json`，每次审核后迭代。

输出：

- `daily/<date>/three-minute-future/work/selection.json`

## 4. 文案生成

状态：待执行

目标：

- 每条生成标题、事实句、思考句。
- 避开旧日报表达。

输出：

- `daily/<date>/three-minute-future/work/final.json`

格式：

```json
{
  "title": "AI 高中遭强烈抗议",
  "fact": "一所由 AI 驱动的高中因强烈抵制而取消",
  "thought": "问题不是 AI 教课，是没人为结果负责。"
}
```

## 5. 封面生成

状态：初版完成

目标：

- 标准流程固定复用已确认的 `1080×1080` 背景；不再每期重新生图。
- 覆盖固定栏目包装层：栏目名、日期、VOL、账号名、内页标题预告。
- 文字层全部由 HTML/CSS 渲染，不直接烧进 AI 背景图。

执行规则：

- 不做“单条新闻封面”。封面必须从本期选题里挑 3-4 个强视觉元素组合布局。
- 主钩子可以占最大视觉权重，但只能是画面的一部分。
- 优先组合能代表本期现实冲击的元素。具体物件由当期 selection 决定，不能把上一期的政策文件、成本单、机器人、机场、门店等元素固定为长期模板。
- 画面必须统一调色、统一光线和统一颗粒质感，不能像素材拼贴截图墙。
- `COVER_PROMPT_FRAMEWORK.md` 只在用户明确要求重新探索封面时使用；普通生产不调用生图。

如果用户明确要求重新探索封面，生图前必须先生成压缩 prompt：

```powershell
python lines\three-minute-future\build_cover_prompt.py <date> --write-final
```

该脚本会输出：

- `daily/<date>/three-minute-future/work/cover-prompt.txt`
- `work/final.json` 里的 `cover.promptPath`
- `work/final.json` 里的 `cover.promptPlan`

如果 prompt 包含信息图触发词，脚本会直接失败，不能继续出图。

输出：

- `daily/<date>/three-minute-future/publish/html/00-cover.html`
- `daily/<date>/three-minute-future/publish/images/00-cover.png`

## 6. 内页生成

状态：初版完成

目标：

- 每条新闻生成一张竖屏内页。
- 真实图片优先，统一视觉处理。
- 图片不得跨条目重复使用。
- 没有图片时，尝试截取原报道 / 原文页面作为素材。
- 原文无图、帖子截图不理想或 Google News 中转页不可截时，按标题关键词检索免费商用素材图；素材不要求百分百对应原报道，但必须服务标题信息，比如“AI 硬件 / 芯片”可使用芯片、服务器、半导体照片。
- X 截图必须围绕帖子核心内容，不截右侧登录框、推荐用户、趋势栏等杂质。
- 静态内页默认“清晰优先”：AI 快闪感放在包装层，主体图片不做重度模糊；更强的霓虹闪烁和高斯模糊留给视频转场或封面动效。

输出：

- `daily/<date>/three-minute-future/publish/html/01-*.html`
- `daily/<date>/three-minute-future/publish/images/01.png`
- `daily/<date>/three-minute-future/publish/images/02.png`
- ...

说明：

- `render_pages.py` 是版式源头：从 `work/final.json` 生成封面和内页 HTML，同时生成 `live-preview.html` / `index.html`。
- `screenshot_pages.py` 负责把 HTML 导出成 PNG 发布图。
- `daily/<date>/.../publish/` 是每日产物目录，不是栏目模板目录。

## 7. 视频化

状态：待执行

目标：

- 用 Hyperframes 或 Remotion 把图片串成短视频。
- 加转场、节奏、轻运动、可选旁白字幕。

输出：

- `daily/<date>/three-minute-future/publish/video.mp4`

## 8. 质检与发布包

状态：初版完成

目标：

- 检查标题、日期、VOL、账号名。
- 检查图片是否糊、文字是否被遮挡、事实是否有来源。
- 用 `serve_preview.py` 服务当天 `publish` 目录，在 Codex 侧边栏实时检查页面。

输出：

- `daily/<date>/three-minute-future/publish/live-preview.html`
- `daily/<date>/three-minute-future/publish/index.html`
- `daily/<date>/three-minute-future/publish/post.md`
- `daily/<date>/three-minute-future/publish/README.md`

## 9. 自动化入口

状态：初版完成

目标：

- 用一个命令串起从信息源抓取到发布图片导出的常规流程。
- 保留人工审核断点，尤其是选题审核和封面图确认。

输出：

- `daily/<date>/three-minute-future/work/run-report.json`

默认完整流程：

```powershell
python lines\three-minute-future\run_daily.py <date> --vol <期数>
```

常用审核流程：

```powershell
python lines\three-minute-future\run_daily.py <date> --vol <期数> --stop-after select
python lines\three-minute-future\run_daily.py <date> --vol <期数> --start-at copy --cover-image <封面图路径>
```

边界：

- 选题、素材、版式可以自动产出初稿。
- 标准流程会自动复用固定封面；`--cover-image` 只用于用户明确确认的替换封面。
## 2026-05-27 更新：封面与视频合成规则

- 标准流程不再生成新封面图，固定复用 `daily\2026-05-23\three-minute-future\work\cover\constructivist-cover-bg-v1.png`。
- `run_daily.py` 在没有 `--cover-image` 时会自动读取固定封面配置；手动传 `--cover-image` 仅用于用户明确确认的替换封面。
- 视频合成不是直接把 1080 宽卡片贴到 1080 画布边缘。Hyperframes 必须使用 `safe-frame`：卡片源尺寸不变，合成时居中缩放到 `0.92`，为抖音播放器裁切预留左右安全区。
- 验收时必须检查导出 MP4 仍为 `1080x1920`，并抽帧确认左侧顶部文字、底部横幅、账号名没有贴边被裁。
