# 三分钟未来 · 封面生图提示词框架

> 2026-05-27 状态：此文件已降级为“重新探索封面时的参考文档”。标准生产流程不再默认生图，统一复用已确认的构成主义背景：`daily\2026-05-23\three-minute-future\work\cover\constructivist-cover-bg-v1.png`。

## 核心规则

封面提示词分成两层：

1. 固定的是美学母版：新构成主义、工业新闻海报、前卫摄影蒙太奇、强斜线构图、粗粝纸张质感、黑 / 脏白 / 酸绿 / 警示红的受限色盘。
2. 变化的是每期主题锚点：每期必须根据当期 selection 的主线重新选择视觉主体，不能把上一期的发票、政策文件、机器人、机场、门店等元素固定成永久模板。

单期封面不能只画一条新闻，但也不能把所有新闻平均堆进去。做法是：

- 先选一个本期主钩子，作为最大视觉权重。
- 再选 2-3 个辅助锚点，作为背景碎片、角落面板或隐性线索。
- 所有元素必须服从同一个工业海报构图，不做素材截图墙。

## 固定美学母版

```text
Create a square 1:1 cover background in the spirit of early Soviet Constructivist propaganda posters and avant-garde photomontage, reinterpreted as a contemporary AI industry news cover.

This is NOT a sci-fi illustration. It is a severe industrial news poster.

Visual language:
- Constructivist diagonal composition, aggressive asymmetry, sharp triangular planes, hard geometric blocks.
- Photomontage logic: realistic fragments collaged together, not a single cinematic scene.
- Strong scale distortion: one oversized thematic object cuts diagonally through the frame like a warning placard.
- The objects should feel arranged by force, not naturally placed.
- Use compressed perspective, hard crops, and overlapping planes.
- Use a sense of propaganda-poster urgency, but without political symbols.

Composition:
- 1080x1080 square poster background.
- Main diagonal force runs from upper left to lower right.
- Do not center everything. The layout must feel engineered and tense.
- Leave a dark open title zone for Chinese typography added later.
- Leave a small clean zone near the top-right or right-middle for date and VOL added later.
- Leave secondary dark zones for 2-3 short cover hooks added later.

Surface and texture:
- Screen-printed poster texture.
- Rough ink edges, halftone dots, grainy newsprint, slight misregistration.
- Matte paper, not glossy 3D render.
- High contrast black shadows and flat graphic color fields.
- Subtle cyan/magenta registration error, but keep objects readable.

Color palette:
- Dominant: deep black, graphite gray, dirty off-white.
- Accent: acid lime, cyan, warning red/magenta.
- Limit the palette. No rainbow neon, no purple-blue AI cliché.
- The image should read as black / off-white / acid green / red at thumbnail size.

Mood:
urgent, severe, industrial, institutional pressure, machine-age warning, editorial, confrontational.

Important:
No readable text.
No fake letters.
No Chinese characters.
No English words.
No company logos.
No brand names.
No smiling people.
No generic glowing AI face.
No futuristic city skyline.
No soft cinematic office stock photo.
No clean corporate presentation style.
No cute cyberpunk.
No decorative gradients.
```

## 每期动态主题锚点

每期先从 `work/final.json` 的入选报道里提炼 3-4 个视觉锚点，再填入母版。锚点必须是当期内容决定的，不得复用上一期锚点。

示例：

- 如果主线是 AI 成本 / 政策压力：可以使用成本单、政策文件、工位、服务器、工牌、计算器。
- 如果主线是机器人进入现实：可以使用物流通道、行李车、工厂机械臂、公共空间管理标识、设备编号牌。
- 如果主线是 AI 医疗：可以使用诊疗室、机械臂、医学影像屏、病历夹、责任链图形隐喻。
- 如果主线是身份协议 / 智能体权限：可以使用门禁卡、身份令牌、权限面板、服务器柜、空白协议纸张。
- 如果主线是零售 / 门店运营：可以使用货架、库存标签、扫码光束、收银台、后台办公室。

## 本期化提示词拼装模板

```text
Core idea:
<一句话描述本期主线，不超过 20 个中文词。>

This cover should feel like:
<本期情绪，例如：financial warning / labor pressure / infrastructure anxiety / public-space control / medical responsibility.>

Primary visual anchor:
<当期主钩子对应的最大视觉主体。不要固定成发票或政策文件。>

Secondary visual anchors:
- <辅助锚点 1>
- <辅助锚点 2>
- <辅助锚点 3>

Important composition rule:
The cover must not represent only one single news item. The primary visual anchor can dominate, but secondary anchors must appear as collaged fragments, cut panels, shadows, or background evidence. Keep one unified Constructivist industrial poster, not a collage wall.
```

## 最终提示词压缩规则

实际送去生图的提示词不能把整份文档原样复制进去。最终提示词必须压缩成 5 段：

1. `Asset / size`：说明 `1080x1080 square cover background`，背景图不含文字。
2. `Core idea`：一句话描述本期主线。
3. `Primary visual anchor`：只写一个最大视觉主体。
4. `Secondary fragments`：最多 3 个辅助碎片，用 `fragments / shadows / cut panels / background evidence` 表达。
5. `Style + negatives`：构成主义工业海报语言 + 一行禁用项。

禁用会触发“信息图 / 教育图 / 对比表”的提示词：

- infographic
- diagram
- table
- chart
- comparison
- list
- labels
- UI
- protocol
- assessment
- forms
- channel
- educational
- presentation
- good habits / bad habits

如果当期内容确实涉及“协议、评估、表格”，提示词也不要直接写这些词，改用视觉物件表达：

- 协议：`blank access cards`, `permission gates`, `locked server doors`
- 评估：`public administration desk`, `stamped blank folders`, `institutional files`
- 表格：`blank paper blocks`, `unreadable paper slabs`

## 禁止误用

- 禁止把“巨型成本单 / 政策文件 / 发票”固定成栏目长期模板。
- 禁止为了表现多新闻，把每条新闻都画成一个同等权重的小图标。
- 禁止生成可读文字；所有标题、日期、期数、账号名交给 HTML/CSS。
- 禁止直接复刻竞品封面的具体主题物、栏目名和包装。
