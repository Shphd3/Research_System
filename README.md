# Research System

这里保存研究问题、能够复现的项目代码和支持结论的证据。当前主线是理解 MoE 表征与长尾学习，并决定小模型的哪些特征值得共享参数。

**[系统组织图与实验流程](docs/system_map.html) · [在办项目与问题](PROJECTS.md) · [小模型研究](research/small-model-moe/README.md)**

## 从当前工作进入

| 想做什么 | 从哪里开始 |
|---|---|
| 继续具体问题或实验 | 直接打开对应的探索日志、Anchor 或实验记录；找项目时看[项目表](PROJECTS.md)。 |
| 写代码、复现实验 | `Projects/<项目>/` 保存可执行代码、配置和启动入口。外部运行目录、资产 ID 与结果由实验记录串联。[资产目录](assets/README_cn.md) · [训练代码复用](docs/training_reuse_index.md) |
| 准备组会 | [按日期读组会稿](daily_research_reports/README_cn.md)，稿件回链原始实验。查写法时读[组会与报告写法](docs/report_writing_cn.md)。 |
| 查旧工程、路径或跨仓记录 | [归档工程](Projects/archive/README.md) · [旧路径与独立仓库](docs/project_access_cn.md) · [Anchor 阅读副本](sync/anchors/README_cn.md) |

## 记录放在哪里

`research/<项目>/main/explore/` 保存按问题追加的探索日志。进入正式实验后，Anchor 给出科学设计，Protocol 将实验名关联到 Anchor、代码版本和运行方式，Summary 和 Detailed 记录实际结果与边界。[正式记录约定](docs/formal_lane.md)

`daily_research_reports/` 保存组会材料。`.research/memory/conversations/` 保存跨会话续接线索。执行回执、原始日志、数据和检查点保存在执行工作区，默认位于 `/data/250010109/MoE_Router/`。归档项目通过[位置表](docs/research_locations.json)找回历史路径。

Agent 从[工作规则](AGENTS.md)进入，只在任务需要时查看[技能索引](docs/skills.md)。系统仓维护上述研究记录与系统自有代码，独立项目由各自的 Git 仓维护。
