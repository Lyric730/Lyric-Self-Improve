# Teaching Video 生产线

- 来源：[`projects/Self-Media/lines/teaching-video/README.md`](../../../../projects/Self-Media/lines/teaching-video/README.md)
- 同步日期：2026-05-29
- 交付等级：🟡 可用骨架

当前目标是支撑 1-2 条真实教程视频试产，先把选题、录屏、剪辑、包装、发布、复盘的源头文档固定下来，不急着做完整自动化。

## 定位

`teaching-video` 是“教学干货 / 实操应用 / AI 工具 walkthrough / 类产品发布 demo”视频生产线。

它不是固定日报，也不是纯工具评测。核心标准是：观众看完后能跟着完成一个具体动作或理解一个真实工作流。

## 当前判断

短期路线：

```text
成品录屏工具录主体
-> 剪掉停顿、处理 zoom/cursor、补字幕
-> HyperFrames 做品牌包装、章节卡、总结卡、CTA
-> Remotion 只做产品发布感 spike
```

不要一开始 All in Remotion。Remotion 和 HyperFrames 都更适合做视频合成/包装，不适合作为教程录屏主体工具。

## 目录

```text
lines/teaching-video/
├── README.md
├── TOOLCHAIN.md
├── SOP.md
├── templates/
│   ├── outline.md
│   ├── recording-checklist.md
│   └── post.md
└── examples/
    └── .gitkeep
```

## 常用入口

| 文件 | 用途 |
|---|---|
| `TOOLCHAIN.md` | 工具栈、Remotion vs HyperFrames、AI 参与方式、风险 |
| `SOP.md` | 最小可用生产流程 |
| `templates/outline.md` | 单期选题和教学路径模板 |
| `templates/recording-checklist.md` | 录屏前隐私、素材、窗口、路径检查 |
| `templates/post.md` | 发布文案模板 |

## 单期落盘建议

```text
daily/<YYYY-MM-DD>/teaching-video/
├── work/
│   ├── outline.md
│   ├── script.md
│   ├── recording-notes.md
│   └── edit-notes.md
└── publish/
    ├── final.mp4
    ├── cover.png
    ├── post.md
    └── steps.md
```

## 升级条件

满足任意两个条件，再开始写脚本和模板工程：

- 连续产出 2-3 条同结构视频。
- 每条都需要固定片头、章节卡、总结卡。
- 录屏前 checklist 能明显减少返工。
- 发布平台和画布比例稳定。
- 有可复用的字幕、封面、步骤卡样式。

## 不做

- 不把旧产线 `digest` 或 `three-minute-future` 的视觉习惯直接混进来。
- 不先写复杂 Remotion/HyperFrames 工程。
- 不用代码重造成熟录屏工具的 auto zoom/cursor 能力。
- 不为了自动化把还没跑通的内容形态固化。
