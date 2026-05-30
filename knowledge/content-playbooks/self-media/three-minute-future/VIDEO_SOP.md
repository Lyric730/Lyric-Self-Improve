# 三分钟未来 · 视频生产 SOP

> 总入口：先读 `PRODUCTION_LINE.md`。本文件只记录视频/TTS/Hyperframes 细节；如果和 `PRODUCTION_LINE.md` 冲突，以 `PRODUCTION_LINE.md` 为准。

状态：第一版  
用途：把《三分钟未来》的图文产线接到 Remotion / TTS / 视频导出。  
原则：当前稳定方向是 Hyperframes 组件化视频，不再只做整张 PNG 串联。HTML/PNG 产线仍是静态视觉源头，视频里要让封面、图片、标题、短讯、思考、底部账号条等组件分层入场。

## 0. 总原则

1. 先出方案，再执行。任何视觉、脚本、视频、TTS、自动化改动，都要先写清楚目标、范围、结构和验证方式。
2. 可复用规则写在 `lines/three-minute-future/`，不要只写在某一天的 `daily/` 目录里。
3. 当期素材、旁白、时间轴和导出结果放在 `daily/<publishDate>/three-minute-future/`。
4. 不替用户选 TTS 声音。系统只准备文案、音频路径和时长对齐逻辑。
5. 视频时长由旁白驱动，不写死每页 12 秒。
6. 图片清晰优先。快闪感放在转场、边框、扫描线和轻微错位，不牺牲主体识别。

## 1. 日期与选题

输入：

- `publishDate`：发布时间，也是输出目录日期。
- `contentDate` 或 `coverageStart / coverageEnd`：实际报道覆盖时间。
- `vol`：期数。

默认规则：

- 单日版：`publishDate` 做页面日期，`contentDate = publishDate - 1 day`。
- 一周三更版：每期覆盖一个连续区间，一周拆成三个内容包。

执行：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-25 --vol 3
```

如果要做同日加更，必须显式传 `--content-date`，并走已发布账本去重：

```powershell
python lines\three-minute-future\run_daily.py 2026-05-24 --vol 2 --content-date 2026-05-24 --stop-after select
```

输出：

- `work/candidates.json`
- `work/enriched.json`
- `work/selection.json`
- `review/selection-review.md`

人工确认点：

- 选题是否命中“AI 改变现实”。
- 是否和上一期重复。
- AI Hot / 外部新闻 / 国内媒体比例是否合理。

已知坑：

- 当天中午做当天内容，素材只有半天，容易弱。
- 5.23 和 5.24 不能混成一包；必须区分 `publishDate` 和内容覆盖时间。
- 不要为了凑比例硬塞低质量国内媒体。

## 2. 配图

优先级：

1. 原文清晰大图。
2. 公司主体图：logo、总部、门店、产品现场。
3. 免费商用关键词图，优先 Wikimedia Commons，并记录授权。
4. 原报道截图。
5. 人工指定图片。

规则：

- 一张图只用一次。
- 封面不直接使用内页新闻图。
- 公司图必须一眼看出主体，不接受 logo 藏在角落的泛建筑。
- 静态内页不做高斯模糊。

执行：

```powershell
python lines\three-minute-future\enrich_assets.py 2026-05-23 --limit 30 --min-score 3
python lines\three-minute-future\search_keyword_images.py 2026-05-23
python lines\three-minute-future\capture_source_screenshots.py 2026-05-23
```

输出：

- `work/assets/`
- `work/keyword-assets/`
- `work/source-shots/`
- `review/effective-images.md`

人工确认点：

- 图片是否清晰。
- 主体是否和新闻有关。
- 是否有版权记录。
- 是否重复使用。

已知坑：

- Google News RSS 常给 300x300 占位图，不能直接用。
- X 截图不能截到右侧登录区或无关 UI。
- 搜索配图不必百分百还原新闻现场，但必须匹配关键词和主题。

## 3. 文案与静态页面

输入：

- `work/selection.json`
- 图片素材路径
- 期数、日期、账号名

输出：

- `work/final.json`
- `publish/index.html`
- `publish/live-preview.html`
- `publish/images/*.png`

执行：

```powershell
python lines\three-minute-future\generate_final.py 2026-05-23
python lines\three-minute-future\render_pages.py 2026-05-23
python lines\three-minute-future\screenshot_pages.py 2026-05-23
```

静态尺寸：

- 封面：按当前确认基准输出。
- 内页：`1080 x 1416`。
- 视频画布：建议 `1080 x 1920`，用背景延展承接图文卡片。

文字规则：

- 封面目录：右侧主看点 1 条，左下补充看点 2 条。
- 内页：一篇报道一页。
- 内页总正文建议 `100-150` 字。
- 短讯和思考可以组合在一个阅读区里，但标签要清楚。

人工确认点：

- 封面是否一眼能看出栏目和本期钩子。
- 内页字体、间距、信息量是否舒服。
- 账号、日期、期数是否正确。
- 预览页和导出 PNG 是否一致。

已知坑：

- 不要把 reusable 改动只写在 daily 预览页。
- 不要为了装饰压缩正文空间。
- 内页图片模糊会让用户怀疑手机或画质有问题。

## 4. 旁白脚本

位置：

```text
daily/<publishDate>/three-minute-future/work/video/voiceover-script.md
```

每条报道需要四类文字：

1. 页面标题：用于画面。
2. 页面正文：用于阅读。
3. 旁白：用于 TTS，不照读页面正文。
4. 思考句：用于收束，可以读，也可以只在画面停留。

旁白长度：

- 封面：25-40 字。
- 单条报道：45-65 字。
- 片尾：15-30 字。

节奏：

- 封面时长 = 封面旁白真实时长 + 0.5 秒。
- 单页时长 = 该条旁白真实时长 + 1.0 到 1.5 秒。
- 转场不读关键信息。
- 总时长超过 3 分钟时，优先删弱选题或压旁白，不强行加速。

已知坑：

- 不能先写死每页 12 秒，再强行塞 TTS。
- 不能让旁白跨过转场读关键字。
- 不能把正文照搬成旁白，听起来会像稿件朗读。

## 5. TTS 接入

人工确认点：

- 声音由用户选择。
- 语速由用户确认。
- 每条音频是否单独导出，建议一条报道一个文件。

建议音频结构：

```text
daily/<publishDate>/three-minute-future/work/video/audio/
  00-cover.mp3
  01.mp3
  02.mp3
  ...
  outro.mp3
```

自动化需要读取：

- 音频真实时长。
- 旁白文本。
- 对应画面 PNG。
- 每条转场时长。

Remotion 不应该依赖估算秒数。正式合成时，读取音频文件时长后反推 frame。

## 6. Remotion 合成

第一阶段：PNG 串联。

输入：

- `publish/images/00-cover.png`
- `publish/images/01.png` 到 `publish/images/NN.png`
- `work/video/voiceover-script.md`
- `work/video/audio/*.mp3`，可先为空

输出：

- `publish/video/three-minute-future-<date>-vol-<vol>.mp4`

推荐组件：

```text
VideoRoot
CoverScene
StoryScene
TransitionFlash
BackgroundPlate
AudioTrack
OutroScene
```

画面规则：

- 主体图文卡片居中偏上。
- 背景用暗色网格、低亮放大底图或纯色结构，不抢信息。
- 每页允许轻微推近、轻微错位、短暂扫描线。
- 转场控制在 0.3-0.5 秒。

第二阶段：组件化。

等版式稳定后，再把 HTML/CSS 视觉转成 Remotion 原生组件。不要在视觉还没定稿时重写一遍。

## 7. 导出检查

每次导出前检查：

- 总时长是否在目标范围内。
- 音频是否和画面同步。
- 转场时是否有关键字被切掉。
- 字幕、标题、账号名是否在安全区。
- 图片是否清楚。
- 文件名、日期、期数是否正确。

建议验收清单：

```text
[ ] 封面 3 秒内能看懂栏目和本期看点
[ ] 每页旁白读完后，画面至少停 0.5 秒
[ ] 转场期间没有读关键信息
[ ] 总时长小于 3 分钟
[ ] 账号名、期数、日期正确
[ ] 图片不糊，不重复
[ ] 产物路径在 publish/video/
```

## 8. 当期目录建议

```text
daily/<publishDate>/three-minute-future/
  work/
    final.json
    video/
      voiceover-script.md
      episode.video.json
      audio/
      timing-report.json
  publish/
    images/
    video/
```

`episode.video.json` 后续作为 Remotion 的主输入。它不替代 `final.json`，只负责视频合成需要的信息。

## 9. Hyperframes 组件化样片

用途：

- 当用户认为 Remotion/PNG 串联太像 PPT 时，先用 Hyperframes 做“封面 + 2 条报道”的组件化样片。
- 样片只验证动效语言、转场节奏、文字出现顺序，不直接代表全量成片。

源头脚本：

```text
python lines/three-minute-future/build_hyperframes_sample.py <publishDate>
```

生成目录：

```text
lines/three-minute-future/hyperframes/vol-<VOL>-sample/
  DESIGN.md
  data.js
  index.html
  assets/
```

验证命令：

```text
npx hyperframes lint
npx hyperframes inspect --samples 10
npx hyperframes validate
```

预览命令：

```text
npx hyperframes preview --port 3027
```

导出命令：

```text
$env:PATH = "lines/three-minute-future/remotion/node_modules/@remotion/compositor-win32-x64-msvc;$env:PATH"
npx hyperframes render --quality draft --workers 2 --output daily/<publishDate>/three-minute-future/publish/video/<name>.mp4
```

注意：

- GSAP 必须使用本地 `lines/three-minute-future/hyperframes/vendor/gsap.min.js`，不要依赖 CDN。
- 字体必须嵌入样片工程，避免导出时中文字体回退。
- 转场色块默认透明度必须为 0，只在转场时间轴里打开。
- 每个场景的图片、标题、来源、短讯、思考必须分别入场，不能只推拉整张页面 PNG。
- 2026-05-27 起，Hyperframes 视频层必须使用平台安全区：最终 MP4 仍为 `1080x1920`，但 `1080` 宽卡片需要放入居中 `safe-frame`，按 `0.92` 缩放，左右各留约 `43px`。这是为了解决抖音播放器横向裁切导致左侧标题/账号/顶部信息被吃的问题。
- 不要改静态页面尺寸来修复视频裁切。静态输出继续保持：封面 `1080x1080`，内页 `1080x1416`。只在 `build_hyperframes_sample.py` 的视频合成层处理安全边距。
