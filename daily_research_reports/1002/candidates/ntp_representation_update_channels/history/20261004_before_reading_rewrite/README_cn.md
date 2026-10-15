# 1002 临时候选：共享学习、有限效用与MoE路由

## 2026-10-03 07:27—10:47 UTC：共享决策与MoE路由

当前先读[何时共享、何时分开：本轮完整报告](sharing_routing_report_cn.md)，再读[决策与路由数学](sharing_routing_mathematics_cn.md)。用户授权约3小时20分钟继续研究，目标是改进MoE路由与架构；SAE与谱是工具。

已完成旧S7有限动作的选路效用、组别对照与八族输入比较：多种表示保留类别内条件信息，却未稳定超过强FIT固定动作；全维固定线性规则也未支配低维表示。推导进一步将可预测学习差异、有限步曲率与估计噪声接成有条件的共享判断。Router可以读决策表示，expert保留完整因果输入。当前未宣称已得到更好的在线MoE或下游能力。具体数值、反例、CI与边界以新报告为准。

[Anchor](anchor_cn.md)保有当前问题，[Protocol](protocol_cn.md)保留原capacity合同并追加routing比较；[前版原件/阅读副本](history/20261003_before_routing_refinement/)可追溯。新任务`pt-meoxfrko`检查Dense/S7/SALL精确33B新面板，旧容量任务`pt-uasnh61d`独立保留，均8×5090 SPOT；不要将提交当成结果。最新核验见报告执行段与[作业清单](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/job_ledger.json)。

## 2026-10-03 04:14—06:44 UTC：上一容量研究窗口

研究问题进一步细化为：**有限的特异专家能否通过共同处理与计算耦合，接近较大 Dense 的学习效果，并保持已学领域？** 用户已明确授权约2.5小时自主研究及8×RTX5090 SPOT训练。旧文中的“不在远程训练范围”和旧审批状态仅属于10月2日历史窗口。

该窗口形成 [容量与机制报告](capacity_report_cn.md)。

该窗口设计见 [Anchor](history/20261003_before_routing_refinement/reading/anchor_cn.md) 与 [Protocol](history/20261003_before_routing_refinement/reading/protocol_cn.md)。它们是临时候选，没有移入正式项目；此前版本在 [history](history/20261002_before_capacity_refinement/) 完整保留。新训练与原始证据位于 [20261003 执行目录](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity)。六臂×两个配对seed/order，每条轨迹固定37,748,736次有效token暴露。作业 `pt-uasnh61d` 已提交；提交不是训练完成或科学结果。

先理解 [共同容量的线性反例与边界](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/math_capacity_round2_cn.md)，再读 [计算与恢复审计](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/code_audit_round1_cn.md)。正式结果与有限回滚分析将在同一临时目录补齐；[研究过程](research_process_cn.md)记录实际推进。

以下内容为10月2日研究历史，数字与原边界保持不变。


本目录是研究者指定的当日备选位置。它不属于正式项目，不替换已有 Focus、Anchor、Protocol 或冻结结果。

**研究目的：**理解哪些自然文本具有可重复的学习关系，并用 S7 及其 SAE 旁支解释这些关系在表征空间中如何形成。长期共享／分开训练的净收益仍需单独验证。

最初研究窗口：2026-10-02 16:44—18:44，Asia/Shanghai；后续续研时间见下。任务范围：持续研究、数学分析、已有自然文本缓存的有界本地分析，以及候选 Anchor／Protocol／阶段报告。新的远程完整实验与长期训练不在本次自动执行范围内。

本轮采用直白的叙述顺序：先说问题和结论，再给具体例子，接上计算链，最后说明证据边界与下一决定。每个阶段区分推导、测量和 AI 建议。

**深入更新（2026-10-02 17:30 UTC起）：**上一轮99%的“平均部分”指每个领域内A/B来源批次的平均，不是四领域共同部分。跨领域相对有限作用仍有部分复现；扣除所选共同参数轴的幅度差后，导数响应复现内积保留约69%。但只用较早前文预测未来8目标时，SAE额外Q仅约0.077%／0.289%，普通投影更强。当前输出消去的部分输入仍会参与更新作用；这不是SAE信息损失比例或低Q原因的证明。详见[领域作用、真实续写与可见信息](domain_response_structure_cn.md)。

**续研更新（2026-10-02 16:35 UTC起）：**冻结读出器在两份记录不重叠的来源间，仍保留约0.48%—0.60%的有限响应预测误差改善。在当前固定正则读出器中，两份同来源预测的绝对MSE改善中，约99%来自各领域内部A/B响应的平均部分；专门针对同域A/B来源差异选正则后，SAE增益约0.009%，很小但不能称为零。这是旧面板、既往特征设置下的两来源探索，不是一般来源泛化。详见[来源迁移续研](source_transfer_addendum_cn.md)。

## 本轮得到的回答

平均层面，这批来源更新帮助了各读出领域；单事件层面，约44%—53%的作用不利，且来源换一半后部分事件会反号。更新前SAE特征能读出少量有限响应信息，普通表征投影也有效。静态SAE重构误差较小，并不保证编码差能重建真实小位移。

因此，本轮把自然文本、来源更新、原生位移与实际损失接通了，也明确了工具与来源稳定性的限制；“长期分开是否值得”仍待直接比较。详细数字都限定在旧科学文本面板和指定S7状态。

## 从这里阅读

先读 [阶段研究报告](research_report_cn.md)。它把目的、假设、三步分析、确切自然文本例子、结果与边界放在同一条叙述中；三张图都有原始表与来源。

| 文件 | 阅读用途 | 状态 |
| --- | --- | --- |
| [研究报告](research_report_cn.md) | 快速理解本轮推进与仍未回答的问题 | 已曝光自然文本上的探索性研究 |
| [领域响应深入分析](domain_response_structure_cn.md) | 同域批次与跨域差异、严格前缀预测、共同方向与输入核空间 | 新增旧面板探索 |
| [数学分析](mathematical_analysis_cn.md) | 从真实续写、梯度、原生位移到有限损失；Fisher及SAE反例 | 推导条件明确，含数值核查 |
| [Anchor候选](history/20261002_before_capacity_refinement/reading/anchor_cn.md) | 一个问题、假设、模型、最小反证与下一决定 | `CANDIDATE_FOR_REVIEW` |
| [Protocol候选](history/20261002_before_capacity_refinement/reading/protocol_cn.md) | 新独立记录确认的具体比较、输入、拟合、统计与边界 | `DRAFT_NOT_EXECUTABLE`；独立群与资源待定 |
| [研究过程](research_process_cn.md) | 各阶段做了什么、遇到什么、得到什么确定结论 | 按实际时间记录，包括失败修复 |

## 数值与来源

[精选证据](evidence/)和[图](figures/)仅用于本目录阅读；[payload manifest](payload_manifest.json)记录大小、hash与来源。模型、原始数据、逐事件数组、执行代码与日志留在[执行工作区](/data/250010109/MoE_Router/experiments/20261002_s7_representation_update_channels/README.md)。

研究者拥有科学判断与状态转换。文件写完、数学恒等式通过、CPU计算完成，均不代表新确认设计已获批准。旧主结果仍由正式Summary持有，本目录不重新裁决它。

[English index](README.md)。
