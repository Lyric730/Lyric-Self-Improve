# Codex + Obsidian Knowledge Management

等级：🟡 可用

## 目标

让 Obsidian 负责人类浏览和手动编辑，让 Codex 负责批量整理、提炼、补链接、更新索引。

## 分工

| 工具 | 负责 |
| --- | --- |
| Obsidian | 看笔记、改笔记、双链导航、图谱、搜索 |
| Codex | 读目录、整理 Markdown、归档材料、生成索引、检查过期内容 |

## Vault

Obsidian 打开这个目录：

```text
F:\Making money\Lyric-Self-Improve
```

原因：`knowledge/` 和 `projects/` 都需要被看见。只打开 `knowledge/` 会看不到项目上下文。

## 输入入口

| 输入 | 放哪里 | 处理方式 |
| --- | --- | --- |
| 临时网页、摘录、想法 | `knowledge/00-inbox/` | 先标来源和下一步 |
| 项目阶段产出 | `projects/<project>/` | 先作为项目材料保存 |
| 跨项目可复用方法 | `knowledge/<topic>/` | 提炼成 SOP / 模板 / 原则 |
| 外部事实 | 对应主题目录 | 必须保留来源链接或标注“来源待查” |

## Codex 整理流程

1. 先读 `knowledge/_indexes/home.md` 和相关目录 README。
2. 判断材料属于项目资产还是可复用知识。
3. 可复用内容写进 `knowledge/`。
4. 项目上下文继续留在 `projects/`。
5. 新增或移动内容后更新 `_indexes/`。
6. 对外部事实保留链接，不确定就写“不确定 / 没查到”。

## 常用口令

```text
把这次对话沉淀进 knowledge，按现有结构归档，补索引，不要覆盖原文来源。
```

```text
扫描 knowledge 和 projects，找出重复、过期、没入口的文档，给我一个整理方案，先不要改文件。
```

```text
把这个项目阶段产出整理成：ship 了啥 / 学了啥 / 隐忧，并沉淀到合适位置。
```

## 判断规则

| 问题 | 放置 |
| --- | --- |
| 以后多个项目会复用吗？ | 放 `knowledge/` |
| 只服务当前项目交付吗？ | 放 `projects/<project>/` |
| 还没判断价值吗？ | 放 `knowledge/00-inbox/` |
| 是运行产物或日志吗？ | 不进知识库索引 |

## 升级到 🔴 结实还要补

- 给每类笔记加 Obsidian properties 模板。
- 建立周复盘固定命令。
- 给 `projects/` 大项目单独做项目内索引。
- 对 `growth-engine-pipeline` 这类大目录做更细的排除和入口治理。
