# 共享学习与路由：阶段报告阅读指南

更新：2026-10-04，Asia/Shanghai（UTC+8）。[English](reading_guide.md)。

这两天的研究围绕同一个问题推进：**不同文本何时应共享学习，何时值得分别学习，怎样让路由使用事前可见的信息作决定？** 现有工作把更新响应、有限动作选择、有限样本学习和共同计算分开建模，再检查它们之间的联系。局部响应可预测，不自动说明路由有收益；条件模型中的共享收益，也不自动证明自然文本训练获益。

首次阅读从[当前阶段报告](sharing_routing_report_cn.md)开始。它负责完整论证；本指南负责阅读顺序和来源定位。本目录仍是当日备选位置，研究者的科学判断与正式记录的状态不由阅读材料改变。

所有项目相对路径以 `Research_System/` 为根。阅读目录为 `daily_research_reports/1002/candidates/ntp_representation_update_channels/`；中文文件的英文伴随文件去掉 `_cn` 即可定位。

## 1. 先完整阅读当前报告

文件职责：把目的、观察、解释、模型、检验和认识更新连成一条论证。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_report_cn.md`。

建议按第1至第6节顺序阅读。各节回答的问题不同：

| 顺序 | 本节回答什么 | 阅读时保留的区别 |
|---|---|---|
| 1．目的 | 回答共享与分开学习的问题，会改变什么认识？ | 研究目的与当前能测的小问题 |
| 2．观察 | 已经看到了什么，比较对象和条件是什么？ | 测量事实与拟议解释 |
| 3．假设及竞争解释 | 什么可能产生这些观察，什么比较能区分解释？ | 候选假设与已支持判断 |
| 4．统一对象下的分阶段数学 | 固定模型状态怎样选动作；从共同初值学习时，样本和分工怎样影响收益；共同计算怎样改变表达与更新？ | 固定动作选择、学习动态与架构计算三个层次 |
| 5．实验验证与结果分析 | 实际比较检验了哪条关系？结果、有效性和不确定性允许怎样解释？ | 公式核查、自然文本测量与执行事实 |
| 6．认识更新与下一问题 | 证据改变了哪项理解，哪个问题仍值得继续？ | 认识结论与再次罗列数值；研究者判断与AI建议 |

时间有限时，可先读第1、2、3、6节，建立问题与有边界的回答，再回读第4、5节核对推导和证据。这个顺序用于先取得概览；完整理解仍需读完六节。

## 2. 再按发展顺序追溯五篇阶段材料

前四篇保存不同阶段的问题、比较和边界，第五篇将它们接到当前共享与路由问题。历史文件中的日期和执行状态属于当时的快照。当前执行事实统一读当前报告的执行说明及其所引收据，不从历史入口推断。

1. [自然文本更新响应](research_report_cn.md)：最初把真实续写、共享矩阵更新、原生表征位移和有限损失变化接起来；说明SAE读数能做什么、不能替代什么。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/research_report_cn.md`。
2. [来源批次迁移](source_transfer_addendum_cn.md)：固定读出器后更换来源批次，区分“换来源仍能预测”与“能区分哪份来源更合适”。这里的A/B来自同一来源域内不同记录。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/source_transfer_addendum_cn.md`。
3. [领域响应结构](domain_response_structure_cn.md)：分开同域A/B差异与跨域相对作用，再检查只看较早前文能预测多少，以及当前输出遗漏哪些更新输入。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/domain_response_structure_cn.md`。
4. [共同计算与有限容量](capacity_report_cn.md)：把问题推进到小专家的习得和保持，讨论重复存储、统计汇聚、串行计算及共享漂移，并说明架构比较与局部干预分别检验什么。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_report_cn.md`。
5. [共享决策与路由阶段报告](sharing_routing_report_cn.md)：综合上述进展，将响应预测接到有限动作效用，并区分固定状态选择、共同初值学习与共同计算结构。它是本次重写后的主阅读入口。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_report_cn.md`。

来源迁移材料中“约99%的改善来自平均部分”，指的是**各领域内部A/B来源批次响应的平均部分**。它没有把四个领域平均成一个对象，也不表示四域的更新作用没有差异。读第二篇时保留这个定义，再由第三篇查看跨域比较。

## 3. 数学细节按依赖阅读

当前主报告第4节先给共同对象和阶段之间的联系。需要检查推导时，再按以下顺序读三份数学说明；不必先读完所有公式才能进入主报告。

1. [从更新到响应](mathematical_analysis_cn.md)：定义文本事件、共享矩阵、输入、输出和下一词损失；推导梯度如何产生表征位移及损失变化，再区分Fisher、SAE坐标、来源均值和差异。它提供后两篇讨论“响应”的基础对象。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/mathematical_analysis_cn.md`。
2. [共同结构与串行收益](capacity_mathematics_cn.md)：在明确函数族与学习规则后，讨论线性等价、非线性区别、相同参数更新下不同功能轨迹，以及有限样本统计汇聚。它把表达能力、估计误差和保持行为分开，为路由篇讨论学习收益提供条件。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/capacity_mathematics_cn.md`。
3. [共享决策与路由信息](sharing_routing_mathematics_cn.md)：说明有限共享差值、事前可见信息、预测误差与动作选择之间的关系；再连接学习分工、曲率和估计噪声。读压缩输入的条件时，注意router读取的信息与expert实际计算的输入不是同一个限制。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_routing_mathematics_cn.md`。

证明和反例回答其假设内的问题。平方损失、独立样本、固定任务、固定动作或固定步长等条件不能省去。自然文本下一词预测是否满足相应关系，要回到主报告第5节的实际测量；语言token重复曝光也不能直接作为独立样本数。

## 4. 最后按用途查看过程与约定

- [研究过程](research_process_cn.md)回答“何时做了什么、为什么继续、产物在哪里”。它保存操作和推理沿革，不能用完成记录代替科学结论。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/research_process_cn.md`。
- [当前候选Anchor](anchor_cn.md)回答“当前问题、假设、模型和下一决定是什么”。它持有本候选的科学设计；报告不另立设计，未确认判断仍为Unknown。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/anchor_cn.md`。
- [当前候选Protocol](protocol_cn.md)回答“具体如何比较、使用哪些输入和预算、有哪些约定与修订”。核对精确执行契约时连同英文伴随文件阅读。它不因报告完成而自动取得新的授权或结果。项目相对路径：`daily_research_reports/1002/candidates/ntp_representation_update_channels/protocol_cn.md`。

重写前的README、主报告和过程记录保存在 `daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261004_before_reading_rewrite/`。该目录用于版本追溯；当前阅读从本指南和主报告开始。

## 5. 阅读结果时先确认比较对象

**结果分析**解释某次测量、比较、不确定性及竞争解释；**认识结论**回答这些证据怎样改变最初问题的理解。主报告第5节承担前者，第6节承担后者。没有新科学判断时保留未解决项，不把完成标签写成结论。

旧S7有限更新、旧Dense/S7/SALL训练曲线、新的固定状态面板，以及capacity小模型架构比较各有不同模型和时间范围。训练CE、固定检查点的有限干预、下游任务成绩不能互换。先核对主报告给出的模型身份、目标是否事前可见、基线和观测量，再理解结果的含义。执行事实与科学结论分别阅读。
