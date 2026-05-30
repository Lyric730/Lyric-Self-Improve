# 三分钟未来生产线总览

> Source of truth for the Three-Minute Future content pipeline.  
> 详细执行可继续看 `RUNBOOK.md`、`TASK_FLOW.md`、`VIDEO_SOP.md`、`VISUAL_BRIEF.md`、`COVER_PROMPT_FRAMEWORK.md`。

## 0. 当前交付等级

🟡 可用：已经能从信息源抓取、筛选、配图、生成图文、预览、导出 PNG，并用 Hyperframes + TTS 音频生成视频。

还不是 🔴 生产级，原因：

- 封面已切换为固定复用已确认背景；默认流程不再重新生图。
- Hyperframes 现在由单个较大的 `index.html` 承载，全量视频可导出，但 `hyperframes lint` 会提示 composition 文件偏大。
- TTS 声音和最终语速仍由用户确认，系统只负责脚本、切段、插入和对齐。

## 1. 栏目定位

栏目名：`三分钟未来`

账号名：`@小刀のAI 实验室`

内容边界：

- AI 为主。
- 外扩只收“AI 改变现实”的事：劳动力、教育、医疗、影视、零售、机器人、硬件、国防、政策、法律、身份协议、基础设施。
- 不收纯论文、纯模型分数、普通工具小更新，除非它已经造成现实影响。

更新节奏：

- 后续方向是一周三更：把一个区间的信息拆成三期。
- 当前脚本已支持单日和区间：`--content-date`、`--content-start`、`--content-end`。
- 常规日更逻辑仍可用：发布日做前一整天内容，避免中午只抓到半天素材。

## 2. 必须先出方案

非纯问答任务不能直接执行。执行前先给用户一版可审阅方案，至少包含：

1. 目标：这次要解决什么。
2. 范围：动哪些文件、脚本、页面、视觉组件。
3. 细节构建：信息源、selection、图片、封面、内页、TTS、视频节奏怎么处理。
4. 取舍理由：为什么这样做，放弃什么。
5. 交付物：最后会产出哪些文件。
6. 验证方式：怎么确认做好了。

用户明确说“执行”“确认”“没问题”“就这样”后，再进入执行。

## 3. 源头目录与产物目录

```text
F:\Making money\Lyric-Self-Improve\projects\Self-Media
```

源头生产线：

```text
lines\three-minute-future\
  config\
  scripts / *.py
  templates\
  styles\
  remotion\
  hyperframes\
  PRODUCTION_LINE.md
  RUNBOOK.md
  TASK_FLOW.md
  VIDEO_SOP.md
  VISUAL_BRIEF.md
  COVER_PROMPT_FRAMEWORK.md
```

每期产物：

```text
daily\<publishDate>\three-minute-future\
  work\
    candidates.json
    enriched.json
    selection.json
    final.json
    cover-prompt.txt
    tts\
    video\
  publish\
    live-preview.html
    index.html
    images\
    video\
```

原则：可复用规则、样式、模板、脚本必须改 `lines\three-minute-future\`；不要只改某一天 `daily\...` 下的临时文件。

## 4. 选题规则

默认上限：15 条。选出来多少条就做多少个内页，不为了凑满 15 条硬塞弱内容。

15 条目标配比：

```text
AI Hot : 外部新闻 : 国内媒体 = 8 : 5 : 2
```

8 条目标配比：

```text
AI Hot : 外部新闻 : 国内媒体 = 4 : 3 : 1
```

排序原则：

- AI Hot 默认权重高，但不能只做 AI 圈内部消息。
- 国外 / 海外信息源优先。
- 国内媒体降权但不硬删。
- 医疗默认降权，每期最多 1 条，除非用户特别要求。
- 某类候选不足时，用高分候选回填，不为比例牺牲质量。

配置源头：

```text
lines\three-minute-future\config\selection_policy.json
```

## 5. 图片与封面规则

内页图片优先级：

1. 原文清晰大图。
2. 公司主体图：logo、招牌、门店、总部、产品现场。
3. 免费商用关键词图，优先可记录授权来源的素材。
4. 原报道截图。
5. 人工指定图片。

硬规则：

- 一张图只用一次。
- 内页主体图清晰优先，不做重度模糊、撕裂、强 glitch。
- X 截图只截核心帖子，不要右侧登录框、推荐用户、趋势栏。
- 公司新闻不加 slogan，识别来自图片主体本身。

封面规则：

- 封面卡片尺寸：`1080 x 1080`。
- 封面背景默认固定复用已确认构成主义背景；不再每期重新生图。
- 封面不能只表现单条新闻，要从本期 selection 抽 3-4 个视觉锚点。
- 固定的是“新构成主义工业新闻海报语言”，不是固定物件。
- 不把上一期成本单、政策文件、机器人、机场、门店等元素沿用成永久模板。
- 背景图不生成可读文字，栏目名、标题、日期、期数、账号名都由 HTML/CSS 渲染。

提示词源头：

```text
lines\three-minute-future\COVER_PROMPT_FRAMEWORK.md
lines\three-minute-future\config\visual_asset_policy.json
```

仅当用户明确要求重新探索封面时，才生成封面 prompt：

```powershell
python lines\three-minute-future\build_cover_prompt.py <publishDate> --write-final
```

## 6. 视觉尺寸

静态图：

```text
封面：1080 x 1080
内页：1080 x 1416
```

视频：

```text
视频画布：1080 x 1920
封面卡片：1080 x 1080，位于画布上部
内页卡片：1080 x 1416，位于画布中部
```

视觉源头：

```text
lines\three-minute-future\styles\three-minute-future.css
lines\three-minute-future\templates\
```

## 7. 图文生产流程

常规一键流程：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL>
```

先停在选题审核：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL> --stop-after select
```

指定区间：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL> --content-start <YYYY-MM-DD> --content-end <YYYY-MM-DD>
```

确认封面图后继续：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL> --start-at copy --cover-image <approved-cover-path> --require-cover
```

实时预览：

```powershell
python lines\three-minute-future\serve_preview.py <publishDate> --port 58419
```

打开：

```text
http://127.0.0.1:58419/live-preview.html
```

## 8. 视频生产流程

先生成视频包：

```powershell
python lines\three-minute-future\build_video_package.py <publishDate>
```

输出：

```text
daily\<publishDate>\three-minute-future\work\video\episode.video.json
daily\<publishDate>\three-minute-future\work\video\voiceover-script.md
daily\<publishDate>\three-minute-future\work\video\tts-input.txt
daily\<publishDate>\three-minute-future\work\video\assets\
```

TTS 文件命名：

```text
work\tts\
  00.mp3   # 封面
  01.mp3   # 第 1 条报道
  ...
  14.mp3   # 第 14 条报道
  15.mp3   # 片尾
```

封面旁白当前默认：

```text
三分钟未来，带你用三分钟了解这一期 AI 圈发生了什么，用<报道数>条报道，看 AI 怎么继续进入现实。
```

片尾旁白当前默认：

```text
这就是本期三分钟未来，关注我，持续为你带来最新消息
```

生成 Hyperframes 工程并插入音频：

```powershell
python lines\three-minute-future\build_hyperframes_sample.py <publishDate> --variant audio-120 --audio-dir daily\<publishDate>\three-minute-future\work\tts --audio-speed 1.2
```

当前推荐语速：`1.0 - 1.2`。之前 `1.45` 被确认太快。

验证与导出在生成的 Hyperframes 目录中执行：

```powershell
cd lines\three-minute-future\hyperframes\vol-<VOL>-audio-120
npx hyperframes lint
npx hyperframes inspect --samples 24
```

如果 Windows 找不到 Remotion compositor，把它临时加入 PATH：

```powershell
$env:PATH = "F:\Making money\Lyric-Self-Improve\projects\Self-Media\lines\three-minute-future\remotion\node_modules\@remotion\compositor-win32-x64-msvc;$env:PATH"
```

导出示例：

```powershell
npx hyperframes render --quality standard --output F:\Making money\Lyric-Self-Improve\projects\Self-Media\daily\<publishDate>\three-minute-future\publish\video\three-minute-future-<publishDate>-vol-<VOL>-audio-120.mp4
```

视频不是 PPT 图片轮播。Hyperframes 版本必须让封面、图片、标题、短讯、思考、底部账号条等组件分层入场，而不是整张 PNG 平移缩放。

## 9. 质量验收清单

图文：

- [ ] 日期、期数、账号名正确。
- [ ] 封面 3 秒内能看出栏目与本期钩子。
- [ ] 封面目录采用“右侧主看点 + 左下补充看点”。
- [ ] 内页一篇报道一页。
- [ ] 图片清晰，不重用。
- [ ] 标题、短讯、思考不遮挡来源和底部信息。
- [ ] `publish/images/00-cover.png` 为 1080x1080。
- [ ] `publish/images/01.png...` 为 1080x1416。

视频：

- [ ] 画布为 1080x1920。
- [ ] 音频与画面同步，转场不切旁白关键字。
- [ ] 每页旁白读完后至少留 0.5 秒视觉停顿。
- [ ] 语速在用户确认范围内，默认不超过 1.2。
- [ ] 导出文件在 `publish/video/`。
- [ ] `hyperframes inspect` 没有布局错误。

## 10. 已知坑

- 不要在长上下文里继续硬生封面图；先压缩 prompt，再审图。
- 不要把整份提示词框架原样塞给生图模型。
- 不要只在 `daily` 目录改模板，否则下一期会丢。
- 不要把封面图文卡片做成 1080x1920；1080x1920 是视频画布。
- 不要替用户选择 TTS 声音。
- 不要用强模糊制造“赛博感”，用户会以为图片坏了。
- 不要让 `estimatedDuration` 停留在旧估算；有 TTS 后必须用真实音频时长更新视频节奏。

## 11. 当前代表性产物

第二期完整样例：

```text
daily\2026-05-26\three-minute-future\
```

最终音频版视频样例：

```text
daily\2026-05-26\three-minute-future\publish\video\three-minute-future-2026-05-26-vol-002-audio-120-14.mp4
```

对应 Hyperframes 工程：

```text
lines\three-minute-future\hyperframes\vol-002-audio-120\
```
## 12. 2026-05-27 源头更新：封面固定复用与抖音安全区

- 标准封面背景固定复用：`daily\2026-05-23\three-minute-future\work\cover\constructivist-cover-bg-v1.png`。
- 默认生产流程不再生成新封面图。只有用户明确要求重新探索封面时，才使用 `COVER_PROMPT_FRAMEWORK.md` 作为人工设计参考。
- `run_daily.py` 会从 `config\visual_asset_policy.json` 读取固定封面；新一期 `generate_final.py` 也会默认写入固定封面路径。
- 视频最终画布仍为 `1080x1920`。静态封面仍为 `1080x1080`，静态内页仍为 `1080x1416`。
- 为适配抖音播放器裁切，Hyperframes 视频层使用 `safe-frame`：卡片源尺寸不变，合成时居中缩放到 `0.92`，左右各留约 `43px` 安全边。
- 不要把静态图文尺寸改小来解决抖音裁切；只在视频合成层处理平台安全区。
