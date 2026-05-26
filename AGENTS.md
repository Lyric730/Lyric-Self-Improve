# 项目协作规则

## 基本原则

- 对话使用中文，代码注释和内部技术命名使用英文。
- 机制简单，操作简单；员工端尤其要减少判断、计算和学习成本。
- UI 实现必须对照 `docs/design/imagegen-references/07-component-ui-kit-board.png` 逐组件还原，不能只做“黑橙大概像”。
- 组件开发按 `docs/design/component-traceability-map.md` 的编号推进：`01 按钮`、`02 模式卡片`、`03 底分/倍率选择` 等。

## 自动留存规则

后续出现以下情况时，必须同步更新项目文档，不能只留在聊天记录里：

- 重要产出：PRD、方案、UI Kit、原型、组件规格、关键页面完成。
- 重要 research：查到有价值的官方文档、平台限制、硬件/微信能力约束、部署策略。
- 重要开发节点：新增组件、完成一轮设计还原、接入微信开发者工具、修复影响预览/编译的问题。
- 重要规则变更：积分、段位、奖励、排行榜、反作弊、员工端流程发生调整。

默认写入位置：

- 阶段进展：`docs/dev-log.md`
- 产品规则：`docs/prd-taiqiu-ladder-mvp.md` 或 `docs/ladder-plan/`
- 设计映射：`docs/design/component-traceability-map.md`
- 可编码设计规格：`docs/design/yunhan-codable-design-system-spec.md`
- 微信开发者工具/工程问题：`docs/wechat-devtools-cli.md`

文档更新要写清楚：发生了什么、为什么改、影响哪些文件、下一步是什么。

## 微信开发者工具

- 当前项目目录：`F:\Making money\taiqiuxcx-wechat`
- 微信开发者工具 CLI：`F:\微信web开发者工具\cli.bat`
- IDE 服务端口：`55121`
- 每次重要 UI 更新后，优先用 CLI 执行打开、重置文件索引、预览构建。

常用命令：

```powershell
& 'F:\微信web开发者工具\cli.bat' open --project 'F:\Making money\taiqiuxcx-wechat'
& 'F:\微信web开发者工具\cli.bat' reset-fileutils --project 'F:\Making money\taiqiuxcx-wechat'
& 'F:\微信web开发者工具\cli.bat' preview --project 'F:\Making money\taiqiuxcx-wechat'
```
