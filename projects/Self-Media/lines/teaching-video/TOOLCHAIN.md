# Teaching Video 工具栈方案

更新日期：2026-05-29

交付等级：🟡 可用方案。目标是先支撑 1-2 条真实教程视频试产，不把还没稳定的内容形态提前固化成完整自动化产线。

## 结论

新内容线不要一开始押注 Remotion。对“教程干货 / 实操教学 / AI 工具 walkthrough / 类产品发布 demo”来说，最省 solo-op 成本的路线是：

```text
成品录屏工具录主体
-> 剪掉停顿、处理 zoom/cursor、补字幕
-> HyperFrames 做品牌包装、章节卡、总结卡、CTA
-> Remotion 只做产品发布感 spike
```

核心原因：

- 真实教程的难点是讲清楚、录顺、剪干净，不是渲染动画。
- Remotion 和 HyperFrames 都是视频合成/包装引擎，不是成熟录屏剪辑器。
- 自动 zoom、鼠标跟随、点击高亮、剪停顿这类能力，成品录屏工具已经解决得更快。
- 本项目已有 HyperFrames 产线经验，短期用它做包装比新增 Remotion 主线更稳。

## 新赛道定义

这条内容线暂定为“实际应用教学视频”，不是固定日报，也不是纯工具评测。

| 类型 | 内容例子 | 主要产物 |
|---|---|---|
| 教程干货 | “用 Codex 搭一个可复用 prompt 工作流” | 竖屏/横屏教程视频 + 图文摘要 |
| 实操教学 | “从 0 到 1 做一个小红书选题库” | 录屏 walkthrough + 步骤清单 |
| AI 工具 walkthrough | “FocuSee / HyperFrames / Remotion 怎么进内容生产线” | 屏幕操作视频 + 结论卡 |
| 类产品发布 demo | “展示一个我做的小工具/产线能力” | 更强包装感的 demo 视频 |

明确不做：

- 不做纯炫技 motion graphics。
- 不做泛知识口播。
- 不做复杂影视后期。
- 不为了自动化而自动化。

## 工具栈分层

| 环节 | 推荐工具 | 作用 | 当前建议 |
|---|---|---|---|
| 选题与脚本 | Codex / ChatGPT / 搜索工具 | 选题拆解、教学路径、口播稿、操作清单 | 主力使用 |
| 录屏主体 | FocuSee / Pane Studio / Tella / OBS / Camtasia | 录真实操作、处理镜头、鼠标、点击、zoom | 优先成品工具 |
| 快速剪辑 | CapCut / 剪映 / Descript | 剪停顿、字幕、口播清理、短视频适配 | 先用简单工具 |
| 专业剪辑 | DaVinci Resolve | 多轨、调色、音频、复杂后期 | 需要时再学 |
| 视频包装 | HyperFrames | 片头、章节卡、总结卡、CTA、统一品牌模板 | 短期主线 |
| 高定发布片 | Remotion | React 组件化视频、复杂产品发布片、可配置视频 app | 先做 spike |
| 字幕与转写 | CapCut / Descript / Whisper / HyperFrames captions | 字幕生成、校对、烧录 | 根据素材选 |
| 素材管理 | `daily/` / `lines/` / `topics/` | 单期产物、可复用产线、选题素材 | 沿用项目规则 |

## 录屏工具选择

| 工具 | 适合 | 优点 | 风险 |
|---|---|---|---|
| FocuSee | Windows/Mac 教程、demo、产品发布感录屏 | 自动跟随 cursor、zoom、背景、字幕、AI 功能较完整 | 收费；效果风格可能同质化 |
| Pane Studio | Windows 教程、产品 demo | Windows-native，主打 click auto zoom、smooth cursor、内置剪辑 | 新工具生态较小；长期稳定性要试 |
| Tella | 浏览器/在线产品 demo、团队分享 | 录屏 + 编辑 + 线上分享顺滑 | 本地深度后期能力有限 |
| OBS | 免费录屏、直播、复杂源组合 | 免费、稳定、可控 | 新手成本高；不自动美化教程画面 |
| Camtasia | 传统软件教程 | 录屏和教学编辑成熟 | 成本较高；视觉风格偏传统 |

首轮试产建议：

1. Windows 主力先试 FocuSee 和 Pane Studio。
2. OBS 只作为兜底录屏，不作为主剪辑工具。
3. 如果教程里需要大量口播清理，再试 Descript 或 CapCut。

## Remotion vs HyperFrames

| 维度 | Remotion | HyperFrames | 本赛道判断 |
|---|---|---|---|
| 技术栈 | React / TypeScript / JSX | HTML / CSS / JS / GSAP / CLI | HyperFrames 更容易被 Codex 快速改 |
| 核心定位 | 用 React 编程生成视频 | 用 HTML 作为时间线渲染 MP4 | 都是合成引擎，不是录屏工具 |
| 录屏支持 | Remotion Recorder 支持屏幕和 facecam 分离录制 | 不原生录屏，可接入已有 MP4 | 录屏主体仍交给成品工具 |
| 自动 zoom/cursor | 需要额外规则或 Recorder 能力验证 | 需要额外 mouse/click 数据和 keyframes | 不应短期自研 |
| 模板化 | React 组件、props、schema | HTML 模板、变量、batch render | 本项目当前更偏 HyperFrames |
| 学习成本 | 中高，需要维护 React 视频项目 | 中低，单 HTML/CLI 更轻 | solo-op 起步选 HyperFrames |
| 视觉上限 | 高，适合复杂产品发布片 | 高，适合网页式动效和品牌包装 | 产品发布 spike 可试 Remotion |
| AI 协作 | AI 能写 React，但调试链路更重 | AI 更容易读写 HTML/CSS 并跑 inspect | 当前优先 HyperFrames |

选择规则：

- 选 HyperFrames：片头、章节卡、总结卡、步骤卡、统一品牌包装、平台安全区模板。
- 选 Remotion：要做高定产品发布片、React 组件化视频系统、可配置视频生成器。
- 选成品录屏工具：视频主体是网页、软件、IDE、AI 工具、后台系统的真实操作。

## 推荐 MVP 工作流

第一阶段已经建立 `lines/teaching-video/` 作为源头文档目录，但仍不急着写复杂自动化。先用这套文档驱动 1-2 条真实试产。

```text
1. 选题
   -> 明确观众、学完能做什么、最终交付物

2. 教学路径
   -> 拆成 3-5 个步骤，每步写“屏幕上要发生什么”

3. 录屏前 checklist
   -> 账号隐私、窗口大小、素材准备、脚本要点、演示路径

4. 录屏
   -> 用 FocuSee / Pane Studio 录主体

5. 粗剪
   -> 删停顿、处理口误、保留关键鼠标动作

6. 包装
   -> HyperFrames 生成片头、章节卡、总结卡、CTA

7. 发布物
   -> MP4、封面、标题、简介、评论区置顶步骤

8. 复盘
   -> 记录哪些步骤观众可能看不懂，决定是否升级为脚本化模板
```

## AI 可以如何参与

| 阶段 | AI 参与方式 | 你需要给 AI 的输入 | 产出 |
|---|---|---|---|
| 选题 | 判断是否值得做、拆隐藏假设、找受众痛点 | 想法、目标观众、平台 | 选题判断 + 风险 |
| 教学设计 | 把教程拆成可录屏步骤 | 工具目标、最终效果 | step-by-step 操作脚本 |
| 脚本 | 写口播稿、提示词、屏幕操作说明 | 主题、时长、风格 | `script.md` |
| 录屏前 | 检查隐私、素材、窗口、账号、路径 | 录屏对象和路径 | `recording-checklist.md` |
| 录屏后 | 从转写稿找废话、断点、可剪位置 | transcript / rough notes | `edit-notes.md` |
| 字幕 | 改字幕口语、术语、断句 | srt / vtt / json | revised captions |
| 包装 | 生成片头、章节卡、总结卡、CTA | 文案、时长、画布 | HyperFrames 项目 |
| 发布 | 生成标题、简介、封面文案、置顶评论 | 成片内容和平台 | `post.md` |
| 复盘 | 总结观众卡点和下期优化 | 评论、数据、主观反馈 | iteration notes |

AI 在这条赛道的真正价值：

- 帮你把“我想讲这个”变成“观众能跟着做完”。
- 帮你提前发现教程步骤里的断层。
- 帮你把录屏素材变成结构化发布物。
- 帮你把高频教程沉淀成可复用模板。

AI 不应该替你做的部分：

- 不替你决定真实产品体验好不好。
- 不替你确认软件当前界面是否变了，界面必须实测。
- 不替你最后发布前审隐私信息。
- 不为了炫技把简单教程变成复杂工程。

## 交付等级与升级路径

| 等级 | 状态 | 该做什么 |
|---|---|---|
| 🟢 spike | 验证单条教程能不能跑通 | 选 1 个工具，录 1 条 60-180 秒视频 |
| 🟡 可用 | 日常能稳定出片 | 固定 checklist、目录结构、包装模板 |
| 🔴 结实 | 可复用生产线 | 补脚本、模板工程、自动校验、固定发布复盘 |

当前停在 🟡 可用骨架。下一步应该做 🟢 spike，而不是直接写完整自动化。

## 大坑

- 🔑 隐私：录屏前必须退出私人账号、隐藏 API key、清理浏览器书签栏和通知。
- 💸 成本：FocuSee、Pane Studio、Descript、Camtasia 都可能形成订阅成本，先试单条再买长期。
- 🐛 复杂度：Remotion 主线化太早，会把内容生产问题变成 React 视频工程问题。
- 🗑 数据不可撤销：录到隐私信息后再补救很麻烦，发布前必须逐帧抽查关键片段。
- 平台适配：抖音/小红书竖屏安全区和 B 站/YouTube 横屏不是同一个成片，不要指望一版全平台无脑发。

## 来源

- Remotion fundamentals: https://www.remotion.dev/docs/the-fundamentals
- Remotion Recorder: https://www.remotion.dev/docs/recorder
- HyperFrames introduction: https://hyperframes.video/docs/getting-started/introduction
- HyperFrames vs Remotion: https://hyperframes.video/docs/recipes/hyperframes-vs-remotion
- FocuSee basic information: https://focusee.imobie.com/guide/basic-information.htm
- Pane Studio: https://pane.studio/
- Tella welcome: https://www.tella.tv/help/introduction/welcome
- OBS Studio: https://obsproject.com/
- DaVinci Resolve: https://www.blackmagicdesign.com/products/davinciresolve
- CapCut desktop editor: https://www.capcut.com/tools/desktop-video-editor
- Descript video editing: https://www.descript.com/video-editing
- Camtasia screen recording: https://www.techsmith.com/solutions/screen-recording/

