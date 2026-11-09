# from-attention-to-search 项目入口

[English](README.md) · [研究路线图](roadmap_cn.md) · [项目规则](../AGENTS.md) · [研究地图](research_map_cn.md)

从 [路线图](roadmap_cn.md) 按 A 编号和问题进入。本轮小模型关系分析在 [A15_18 事实报告](experiments/A15/15_18_context_relation_organization_use/first_flow_v3/summary_cn.md)。已有明确结果链接时，可以直接阅读结果，不必遍历全部目录。

## 11月4日当前地图入口

[谱、组合、局部干预与训练效用](research_map_update_20261104_cn.md)：166个正式问题，85父问题、81子问题。先看七组新增证据，再查完整树。

## 10月31日地图更新

[新增内容与归类核对](research_map_update_20261031_cn.md)：159个正式问题，84个父问题、75个子问题。七组阅读入口覆盖新增轮次，原问题的优先级与科学判断保持原记录。

## 研究地图与离线交互版

[中文研究地图](research_map_cn.md)和[英文入口](research_map.md)说明各研究线、父问题与局部子问题的作用；[research_map.json](research_map.json)是它们的派生导航数据。科学设计、研究判断与结果仍由原 Anchor、Focus 和实验记录持有。

从项目根目录运行 `python scripts/render_research_map.py --data main/research_map.json --output <execution-side-html>`，将输出参数换成执行侧 HTML 文件路径，即可生成可离线打开的交互版。[本机已生成文件](/data/250010109/MoE_Router/research_reading/20261104_project_map/research_map.html)是本地阅读产物，不是跨机器网页地址；其他机器从同一数据重新生成。

## 和 AI 一起推进研究地图

你直接用自己的话说想法、疑问或看不懂的地方。我负责找到最相关的已有问题，
说明它与当前讨论的关系，并用真实例子确认我们谈的是同一件事。

接着先分清：已有解释需要讲清，还是确实缺少证据。需要继续研究时，
我会把已有发现、竞争解释和剩余缺口连起来，提出一个具体的下一步分叉，
说明各条路能多回答什么。研究取舍与机制结论由你判断。

讨论形成新的明确联系、证据边界或你确认的下一决定后，我同步维护原记录、
地图文字和交互版，再简短告诉你哪里改变、为什么改变、还剩什么问题。
新想法先作为待讨论内容，不自动变成新 Anchor 或实验。你无需先学编号或整理文件。

## 文件归属

| 位置 | 持有的内容 | 不能代替 |
|---|---|---|
| [focus/](focus/README_cn.md) | 稳定问题、研究者判断与下一决定 | 不授予运行权限 |
| [problem_anchors/](problem_anchors/README_cn.md) | 按 A 编号登记的科学设计 | 不代替 Focus 判断或 Protocol 批准 |
| [experiments/](experiments/README_cn.md) | 精确协议、结果摘要与完整证据 | 不以执行完成代替科研接受 |
| [datasets/](datasets/README.md) | 数据身份、来源与视图登记 | 原始数据及激活仍留执行侧 |
| [research_notes/](research_notes/) | 推导、讨论、来源包与支持笔记 | 不成为第二份当前设计 |
| [stories/](stories/) | 跨轮次阅读叙述 | 不改写冻结结果或科学状态 |
| [organization_migrations/](organization_migrations/20261022/README_cn.md) | 组织迁移、原路径与新编号映射 | 不创建新假设、批准或结果 |

[归属登记](anchor_ownership.json) 覆盖 166 个正式 owner，区分父 Anchor、局部子 Anchor、语言伴随版、实验归属及旧身份。A00 只作历史定义重定向；archive、sources、supporting_records 与 historical_support 是保存材料，不是额外正式 Anchor。

## 两种已登记布局

- `parent_subanchor`：每个独立父问题有自己的目录；局部控制、修复和竞争解释位于其 `subanchors/`。依赖不自动产生父子关系。
- `registered_flat`：已登记旧研究线 A01 / A05 / A07 / A09 / A10 保留平铺形式，不与嵌套形式混用。A01 实验目录名 `A01_common_operator` 已显式登记。

正式实验记录按其 A 研究线及 owner 归类。协议、摘要、详细记录各有职责；模型、原始输出、大缓存与未筛选日志留在执行仓库。新增工作遵循 [项目规则](../AGENTS.md) 和 [系统规则](../../../AGENTS.md)。

本入口只导航。Focus 身份、语言权威、研究判断与批准边界均保留在原记录中。[PROJECTS.md](../../../PROJECTS.md) 负责选择项目，项目内工作流由 [路线图](roadmap_cn.md) 和各 owner 定位。
