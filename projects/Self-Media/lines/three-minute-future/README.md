# 三分钟未来产线说明

`three-minute-future` 是当前主线，负责《三分钟未来》的图文和视频生产。

## 当前状态

🟡 可用：已经能抓取、筛选、配图、生成图文、预览、导出 PNG，并通过 Hyperframes + TTS 音频生成视频。还不是 🔴 生产级，因为视频合成、TTS 声音确认和发布后复盘还需要更稳定的自动化。

## 先读顺序

| 顺序 | 文件 | 用途 |
|---|---|---|
| 1 | `PRODUCTION_LINE.md` | 产线总览和当前规则 |
| 2 | `RUNBOOK.md` | 具体怎么跑 |
| 3 | `TASK_FLOW.md` | 任务拆解和每步输入输出 |
| 4 | `VIDEO_SOP.md` | 视频与 TTS 流程 |
| 5 | `VISUAL_BRIEF.md` | 视觉规则 |
| 6 | `COVER_PROMPT_FRAMEWORK.md` | 仅在重新探索封面时参考 |

## 关键目录

| 路径 | 用途 |
|---|---|
| `config/` | 信源、选题、视觉资产策略 |
| `templates/` | HTML 页面模板 |
| `styles/` | 图文样式 |
| `remotion/` | Remotion 草稿工程 |
| `hyperframes/` | Hyperframes 视频工程 |

## 常用命令

常规图文流程：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL>
```

停在选题审核：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL> --stop-after select
```

区间内容：

```powershell
python lines\three-minute-future\run_daily.py <publishDate> --vol <VOL> --content-start <YYYY-MM-DD> --content-end <YYYY-MM-DD>
```

本地预览：

```powershell
python lines\three-minute-future\serve_preview.py <publishDate> --port 58419
```

视频包：

```powershell
python lines\three-minute-future\build_video_package.py <publishDate>
```

Hyperframes 工程：

```powershell
python lines\three-minute-future\build_hyperframes_sample.py <publishDate> --variant audio-120 --audio-dir daily\<publishDate>\three-minute-future\work\tts --audio-speed 1.2
```

## 硬规则

- 默认不重新生成封面背景；固定复用已确认构成主义背景。
- 重新探索封面前，先给方案，再压缩 prompt。
- 不要把静态图文尺寸改小来解决抖音裁切；平台安全区只在视频合成层处理。
- 不要替用户选择 TTS 声音。
- 不要只改 `daily/`，可复用修复必须回写到本目录。
