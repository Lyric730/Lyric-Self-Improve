# AI PM 能力补强学习路线

更新日期：2026-05-29  
阶段：Step 4A v1  
适用方向：Agent / AI 工具 / 生产力产品；副线为 C 端 AI 助手 / AI 应用  
依据文件：[ai-pm-jd-requirement-frequency.md](ai-pm-jd-requirement-frequency.md)、[ai-pm-ability-material-gap-analysis.md](ai-pm-ability-material-gap-analysis.md)、[ai-pm-experience-profile.md](ai-pm-experience-profile.md)  

## 结论

你现在不是“缺一个漂亮简历”，而是缺 3 类可验证证据：

1. AI 技术表达证据：能讲清 LLM、Agent、RAG、Prompt、工具调用、评测。
2. 可运行 demo 证据：能把 AI 求职 / 知识工作流场景做成一个最小可用工具。
3. 标准评测证据：能把“效果好不好”变成测试集、指标、badcase 和迭代记录。

你的强项是产品增长、信息组织、SOP、内容/SEO 体系化执行。补强路线不应该从“学完机器学习”开始，而应该围绕目标岗位做项目化学习。

## JD 要求和个人差距

| JD 高频能力 | JD 覆盖 | 你的当前证据 | 差距判断 | 优先级 |
|---|---:|---|---|---|
| AI/大模型/机器学习基础理解 | 38/46 | Growth Engine、Self-Media、AI PM JD 研究、Huoshanbei 设想 | 有场景，但技术表达不够硬 | S |
| 数据分析/指标/实验 | 30/46 | Yolox SEO、高顿、JD 频率统计、Growth Engine 排序指标 | 强项，但需要转成 AI 产品指标 | S |
| 沟通协作/跨团队推进 | 29/46 | 高顿、NeuralOPT、校园组织经历 | 证据偏旧，近期项目要补协作/推进叙事 | B |
| 用户研究/市场/竞品/行业洞察 | 27/46 | JD 研究、Yolox 关键词/社区问题、NeuralOPT 调研 | 强项，可继续用 JD 研究强化 | A |
| 产品设计/规划/需求分析 | 22/46 | Growth Engine、Self-Media、Taiqiu、高顿、NeuralOPT | 有素材，需要整理成目标岗位语言 | A |
| 编程/工程理解 | 21/46 | Python/SQL/Vibe Coding、pipeline 项目 | 边界不清，需要可运行 demo 和说明 | S |
| Agent/Prompt/RAG/工具调用 | 19/46 | Growth Engine、Huoshanbei、AI 求职 Agent 设想 | 方向正确，但缺标准 demo | S |
| 模型评测/数据闭环/训练反馈 | 14/46 | Growth Engine 质量门禁、Huoshanbei 测试题设想 | 有意识，缺标准 evals 案例 | S |
| 商业化/增长/运营 | 15/46 | Yolox SEO、Self-Media、高顿 | 强项，适合变成差异化叙事 | A |

## 4-8 周路线

### 第 1-2 周：AI Agent / LLM 基础表达

目标：能讲清楚 Agent 产品的基本结构，不再只说“AI 工作流”。

| 学习内容 | 输出 |
|---|---|
| Agent 是什么、工具调用、状态、handoff、human review | `agent-product-notes.md` |
| Prompt 结构、变量、版本、few-shot、输出格式 | `prompt-patterns-for-career-agent.md` |
| Growth Engine 的 L0-L4 改写成 Agent 任务流 | `growth-engine-agent-workflow-map.md` |

推荐资源：

| 资源 | 用途 | 可信度 |
|---|---|---|
| [OpenAI Agents SDK docs](https://developers.openai.com/api/docs/guides/agents) | 学 Agent 的工具、编排、状态、human review、trace | 🟢 官方 |
| [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction) | 系统学 Agent 概念、工具、实践和 certificate 路线 | 🟢 官方课程 |
| [DeepLearning.AI - AI Agents in LangGraph](https://www.deeplearning.ai/courses/ai-agents-in-langgraph) | 学 LangGraph、可控 Agent、human-in-loop、flow-based app | 🟡 高可信课程 |
| [OpenAI Prompting docs](https://developers.openai.com/api/docs/guides/prompting) | 学 prompt、变量、版本管理和 eval 关联 | 🟢 官方 |

验收标准：

- 能用 5 分钟讲清一个 Agent 产品包含：任务、工具、上下文、状态、失败兜底、评测。
- 把 Growth Engine 解释成 Agent-like Pipeline，而不是内容项目。

### 第 3-4 周：RAG 和知识工作流

目标：为 AI 求职 Agent / Huoshanbei 补 RAG 能力，不追求深算法，追求产品可解释。

| 学习内容 | 输出 |
|---|---|
| RAG 数据源、切分、召回、重排、引用、幻觉控制 | `rag-product-notes.md` |
| JD / 简历 / 项目经历如何做成知识库 | `career-agent-data-schema.md` |
| 做一个最小 RAG QA 或 JD 检索 demo | `career-agent-rag-demo/` |

推荐资源：

| 资源 | 用途 | 可信度 |
|---|---|---|
| [DeepLearning.AI - Building and Evaluating Advanced RAG](https://www.deeplearning.ai/courses/building-evaluating-advanced-rag) | 学 RAG 检索、RAG triad、上下文相关性和答案 groundedness | 🟡 高可信课程 |
| [Hugging Face AI Agents Course - Agentic RAG 单元](https://huggingface.co/learn/agents-course/en) | 看 Agent 和 RAG 如何合在一起 | 🟢 官方课程 |
| [pandas Getting Started](https://pandas.pydata.org/docs/getting_started/) | 用表格数据处理 JD / 项目素材 | 🟢 官方 |

验收标准：

- 能讲清“为什么 RAG 不等于把文档丢给模型”。
- 能给 AI 求职 Agent 定义数据结构：JD、能力、项目、证据、缺口、学习任务。

### 第 5 周：Evals / 质量评测

目标：把“质量门禁”“测试题”升级成标准评测表达。

| 学习内容 | 输出 |
|---|---|
| 测试集、grader、badcase、component eval、end-to-end eval | `evals-product-notes.md` |
| 给 AI 求职 Agent 设计 10 条测试样例 | `career-agent-eval-set.md` |
| 给 Growth Engine 质量门禁补失败类型表 | `growth-engine-failure-taxonomy.md` |

推荐资源：

| 资源 | 用途 | 可信度 |
|---|---|---|
| [OpenAI Model optimization docs](https://developers.openai.com/api/docs/guides/model-optimization) | 学 evals、prompt 迭代、测试集思路 | 🟢 官方 |
| [OpenAI Evals API reference](https://developers.openai.com/api/reference/resources/evals) | 理解 eval 对象、数据源、run 的概念 | 🟢 官方 |
| [DeepLearning.AI - Evaluating AI Agents](https://www.deeplearning.ai/courses/evaluating-ai-agents) | 学 trace、router/skill eval、LLM-as-judge、实验迭代 | 🟡 高可信课程 |

验收标准：

- AI 求职 Agent 至少有 10 条测试样例。
- 每条 badcase 能归因到：数据、检索、Prompt、工具、评测口径、用户输入。

### 第 6 周：基础 Coding / AI Coding

目标：不是变成后端工程师，而是能读脚本、改配置、跑 demo、定位常见错误。

| 学习内容 | 输出 |
|---|---|
| Python 文件读写、JSON/CSV、requests、基础 CLI | `career-agent-demo/` |
| pandas 处理 JD 表格和项目素材 | `jd_analysis.ipynb` 或 `.py` |
| SQL 基础查询、聚合、join | `jd_requirement_queries.sql` |

推荐资源：

| 资源 | 用途 | 可信度 |
|---|---|---|
| [Python 官方文档 Tutorial](https://docs.python.org/3/) | 查语法、标准库、文件处理 | 🟢 官方 |
| [pandas Getting Started](https://pandas.pydata.org/docs/getting_started/) | 处理表格数据、清洗 JD 和项目素材 | 🟢 官方 |
| [SQLBolt](https://sqlbolt.com/) | 快速补 SQL 查询、过滤、join、聚合 | 🟡 高可信练习站 |

验收标准：

- 能用 Python 读入一批 JD Markdown / CSV，抽出岗位、公司、要求。
- 能用 SQL 或 pandas 统计能力要求频次。
- 能跑通一个本地 AI 求职 Agent 原型。

### 第 7 周：产品数据分析 / 增长指标

目标：把你的增长强项翻译成 AI PM 能听懂的指标体系。

| 学习内容 | 输出 |
|---|---|
| GA4、GSC、Search Console、Looker/Power BI 基础 | `growth-metric-dictionary.md` |
| 把 Yolox / Self-Media 指标转成产品增长指标 | `growth-system-metric-map.md` |
| 设计 AI 产品指标：任务完成率、召回率、采纳率、留存、badcase 率 | `ai-product-metric-map.md` |

推荐资源：

| 资源 | 用途 | 可信度 |
|---|---|---|
| [Google Analytics Academy / Skillshop](https://support.google.com/analytics/answer/15440208?hl=en-AT) | 学 GA4 免费课程和认证结构 | 🟢 官方 |
| [Google Search Console](https://search.google.com/search-console/about) | 学搜索流量、query、impression、click、index coverage | 🟢 官方 |
| [Microsoft Learn - Get started with Microsoft data analytics](https://learn.microsoft.com/en-us/training/paths/data-analytics-microsoft/) | 学 Power BI / 数据分析叙事 | 🟢 官方 |

验收标准：

- 能把 `Yolox SEO` 讲成“增长指标系统”，不是 SEO 杂活。
- 能给 AI 求职 Agent 定义 5 个核心指标。

### 第 8 周：整合成作品集和求职材料

目标：把学习成果变成可投递证据。

| 输出 | 内容 |
|---|---|
| `ai-job-agent-prd.md` | 用户、任务、功能、数据结构、非目标、验收标准 |
| `ai-job-agent-demo/` | 可运行 MVP |
| `career-agent-eval-set.md` | 10 条评测样例 |
| `resume-project-rewrite-plan.md` | 简历和项目改造方案 |
| `career-action-plan.md` | 投递和复盘计划 |

验收标准：

- 简历上能写 1 个新 Agent 项目。
- 面试能讲 2 个现有项目：Growth Engine、Yolox / Self-Media。
- 你能解释自己现在不是“泛 PM”，而是“增长和工作流背景的 AI 工具 PM”。

## 补强项目

### 项目 1：AI 求职 Agent MVP

| 项 | 内容 |
|---|---|
| 目标岗位能力 | Agent、RAG、JD 解析、能力匹配、评测 |
| 用户任务 | 输入目标方向和简历，输出岗位要求、能力缺口、学习路线、投递建议 |
| 数据来源 | 已收集 JD、个人简历、项目 README/SOP |
| 核心功能 | JD 解析、能力聚类、经历匹配、缺口分析、路线生成 |
| 技术/工具 | Python、Markdown/CSV、LLM API、可选向量检索 |
| 评测方式 | 10 条 JD 样例，检查输出是否覆盖核心要求、是否误判经历 |
| 作品集输出 | PRD、demo、测试集、案例报告 |

这是第一优先级补强项目。原因：它直接服务求职，同时证明 Agent / RAG / 评测 / 产品设计。

### 项目 2：Growth Engine 评测升级

| 项 | 内容 |
|---|---|
| 目标岗位能力 | Agent 工作流、质量门禁、评测、human-in-loop |
| 用户任务 | 把现有质量门禁升级成标准 failure taxonomy 和 eval set |
| 数据来源 | Growth Engine 文章草稿、质量门禁日志、失败样本 |
| 核心功能 | 失败类型、测试样例、通过率、修复记录 |
| 技术/工具 | Markdown、Python 统计、LLM-as-judge 可选 |
| 评测方式 | 每次生成输出是否通过规则；badcase 能否归因 |
| 作品集输出 | 质量评测报告、失败样本表、改进前后对比 |

这是第二优先级。原因：它把现有强项目补成 AI PM 更认可的 evals 证据。

### 项目 3：Yolox / Self-Media 增长指标案例

| 项 | 内容 |
|---|---|
| 目标岗位能力 | 产品增长、指标、内容系统、搜索/分发 |
| 用户任务 | 用一条完整链路证明增长系统能力 |
| 数据来源 | GSC、GA4、Looker、SEO docs、Self-Media daily 产物 |
| 核心功能 | 指标定义、链路图、案例复盘 |
| 技术/工具 | Google Search Console、GA4、Looker/Power BI、Markdown |
| 评测方式 | 指标是否闭环：impression -> click -> session -> conversion |
| 作品集输出 | 增长案例页、指标表、复盘结论 |

这是第三优先级。原因：它是你的差异化强项，但不能代替 AI 技术补强。

## 不建议现在做

| 项目 | 原因 |
|---|---|
| 深度 ML / DL 系统课 | 对当前 AI PM 求职转化慢，短期性价比低 |
| 重做 NeuralOPT AI 机制 | AI 部分已废弃，不值得把旧项目强行翻新 |
| 复杂 ToB 平台 demo | 会拉高工程复杂度，solo-op 不利 |
| 全自动投递系统 | 有隐私和账号风险，也不直接证明 AI PM 能力 |

## 课程来源说明

检索日期：2026-05-29

| 来源 | 可信度 | 用途 |
|---|---|---|
| OpenAI Agents SDK / Prompting / Model Optimization / Evals docs | 🟢 官方 | Agent、Prompt、Evals、工具调用 |
| Hugging Face AI Agents Course | 🟢 官方课程 | Agent 概念和实践 |
| DeepLearning.AI short courses | 🟡 高可信课程 | LangGraph、RAG、Agent evals |
| Python / pandas docs | 🟢 官方 | coding 和数据处理 |
| Google Analytics / Search Console | 🟢 官方 | 增长数据和 SEO 指标 |
| Microsoft Learn Power BI | 🟢 官方 | 数据看板和分析表达 |
| SQLBolt | 🟡 练习站 | SQL 快速补基础 |
