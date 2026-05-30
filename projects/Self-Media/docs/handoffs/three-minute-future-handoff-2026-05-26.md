# 三分钟未来交接文档 2026-05-26

## 当前结论

本阶段停止继续在当前长上下文里尝试封面生图。内置生图连续偏离构成主义工业新闻海报方向，原因不是栏目视觉方向本身，而是当前上下文和提示词执行环境已经不稳定。

第二期先复用 2026-05-23 已确认可用的构成主义封面背景，继续推进视频化。

## 当前目录

项目根目录：

```text
F:\Making money\Lyric-Self-Improve\projects\Self-Media
```

栏目源头目录：

```text
lines\three-minute-future\
```

第二期目录：

```text
daily\2026-05-26\three-minute-future\
```

第二期发布图文：

```text
daily\2026-05-26\three-minute-future\publish\
```

第二期视频输入包：

```text
daily\2026-05-26\three-minute-future\work\video\
```

## 已确认规格

- 栏目名：三分钟未来。
- 更新节奏：后续倾向一周三更，一个区间内信息拆成三期。
- 内容范围：AI 为主，只外扩到“AI 改变现实”的新闻。
- 每期条数：选出来多少条做多少个内页，最多 15 条。
- 默认配比：AI Hot / 外部新闻 / 国内媒体约为 8:5:2，不为凑比例硬塞低质量内容。
- 封面尺寸：1080×1080。
- 内页尺寸：1080×1416。
- 视频画布：1080×1920。
- 内页规则：一篇报道固定一页。
- TTS 声音：由用户选择，Agent 不替用户定声音。

## 视觉状态

### 封面

当前第二期封面临时复用：

```text
daily\2026-05-26\three-minute-future\work\cover\reuse-2026-05-23-constructivist-cover-bg-v1.png
```

来源：

```text
daily\2026-05-23\three-minute-future\work\cover\constructivist-cover-bg-v1.png
```

注意：

- 当前上下文不再继续生图。
- 新上下文中如果继续封面生图，要从 `lines\three-minute-future\COVER_PROMPT_FRAMEWORK.md` 和 `work\cover-prompt.txt` 重新开始。
- 封面不能只表现单条新闻，必须从本期 selection 中抽 3-4 个重要视觉元素组合。
- 固定的是“构成主义工业新闻海报语言”，不是固定使用成本单、政策文件、机器人、机场或门店。

### 内页

第二期已按当前确认的新版内页框架导出 14 张：

```text
daily\2026-05-26\three-minute-future\publish\images\01.png
...
daily\2026-05-26\three-minute-future\publish\images\14.png
```

图片清晰优先，不再做明显高斯模糊。快闪感留给视频转场、边框错位、扫描线和轻微运动。

## 第二期当前产物

重新导出完成：

```text
daily\2026-05-26\three-minute-future\publish\images\00-cover.png
daily\2026-05-26\three-minute-future\publish\images\01.png
...
daily\2026-05-26\three-minute-future\publish\images\14.png
```

页面预览：

```text
daily\2026-05-26\three-minute-future\publish\live-preview.html
```

视频输入：

```text
daily\2026-05-26\three-minute-future\work\video\episode.video.json
daily\2026-05-26\three-minute-future\work\video\voiceover-script.md
daily\2026-05-26\three-minute-future\work\video\tts-input.txt
daily\2026-05-26\three-minute-future\work\video\assets\
```

`tts-input.txt` 已按段落拆分。给 TTS 工具时，建议一段生成一个音频文件，后续命名为：

```text
00-cover.mp3
01.mp3
02.mp3
...
14.mp3
outro.mp3
```

## 新增源头脚本

新增：

```text
lines\three-minute-future\build_video_package.py
```

用途：

```powershell
python lines\three-minute-future\build_video_package.py 2026-05-26
```

它会从当期 `final.json` 和 `publish/images` 生成视频合成所需的 JSON、旁白稿、TTS 输入文本和图片资产副本。

## Remotion 草稿工程

新增目录：

```text
lines\three-minute-future\remotion\
```

作用：

- 读取 `episode.video.json`。
- 把封面、内页和片尾串成 1080×1920 视频。
- 目前是无 TTS 草稿，时长由旁白文字估算。
- 后续接入 TTS 后，应由真实音频时长反推每个 scene 的帧数。

计划导出位置：

```text
daily\2026-05-26\three-minute-future\publish\video\three-minute-future-2026-05-26-vol-002-draft.mp4
```

## 继续视频化的执行顺序

1. 安装 Remotion 工程依赖：

```powershell
npm install --prefix lines\three-minute-future\remotion
```

2. 生成或刷新视频输入包：

```powershell
python lines\three-minute-future\build_video_package.py 2026-05-26
```

3. 导出无 TTS 视频草稿：

```powershell
$env:TMF_PUBLIC_DIR = "F:\Making money\Lyric-Self-Improve\projects\Self-Media\daily\2026-05-26\three-minute-future\work\video"
npm --prefix lines\three-minute-future\remotion run render -- "F:\Making money\Lyric-Self-Improve\projects\Self-Media\daily\2026-05-26\three-minute-future\publish\video\three-minute-future-2026-05-26-vol-002-draft.mp4" --props "F:\Making money\Lyric-Self-Improve\projects\Self-Media\daily\2026-05-26\three-minute-future\work\video\episode.video.json"
```

4. 用户确认 TTS 声音后，把音频文件放进：

```text
daily\2026-05-26\three-minute-future\work\video\audio\
```

5. 更新 `episode.video.json` 中每个 scene 的 `audio` 字段和真实时长，再重新导出最终版。

## 需要避免的坑

- 不要在没有方案的情况下直接继续重构或生图。
- 不要把封面 prompt 写成一整篇设计文档塞给模型。
- 不要把上一期视觉元素当成永久模板。
- 不要替用户选 TTS 声音。
- 不要把图文卡片做成 1080×1920；视频画布才是 1080×1920。
- 不要让转场切掉旁白关键字；最终应使用真实音频时长驱动。
- 不要让内页图片明显模糊，用户会以为画质或手机有问题。

## 当前下一步

继续从 Remotion 草稿导出开始。若 Remotion 安装或渲染失败，先修工程，不要回头继续生图。
## 2026-05-26 视频执行状态补充

已完成两类 Remotion 导出：

```text
daily\2026-05-26\three-minute-future\publish\video\three-minute-future-2026-05-26-vol-002-sample.mp4
daily\2026-05-26\three-minute-future\publish\video\three-minute-future-2026-05-26-vol-002-draft.mp4
```

- `sample.mp4`：15.5 秒技术样片，包含封面、前两条报道和片尾，用于验证 Remotion 工程、素材路径、画面串联和转场。
- `draft.mp4`：全量无 TTS 草稿，约 207.8 秒，14 条报道，文件约 133 MB。
- 当前视频仍是“文字估算时长”版本，不是最终节奏版。
- 用户选定 TTS 声音后，需要把每段音频放入 `work\video\audio\`，再按真实音频时长回写 `episode.video.json`，重新导出最终版。

全量渲染注意：

```powershell
$env:TMF_PUBLIC_DIR = "F:\Making money\Lyric-Self-Improve\projects\Self-Media\daily\2026-05-26\three-minute-future\work\video"
npm --prefix lines\three-minute-future\remotion run render -- "F:\Making money\Lyric-Self-Improve\projects\Self-Media\daily\2026-05-26\three-minute-future\publish\video\three-minute-future-2026-05-26-vol-002-draft.mp4" --props "F:\Making money\Lyric-Self-Improve\projects\Self-Media\daily\2026-05-26\three-minute-future\work\video\episode.video.json" --concurrency=2
```

如果用后台 `Start-Process` 启动，PowerShell 命令字符串里必须写成 `` `$env:TMF_PUBLIC_DIR ``，否则变量会在父进程提前展开，Remotion 会找不到 `assets/00-cover.png`。
