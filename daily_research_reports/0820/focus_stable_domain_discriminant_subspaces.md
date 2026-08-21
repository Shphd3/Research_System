# 已学到的低秩功能空间在新表达和真实数据上是否仍然成立，并且它落在表征频谱的哪里？

```text
type: meeting_cycle_core_task
status: REPLACED_BY_RESEARCHER
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
plain_language_design_last_human_confirmation: 2026-08-20
cycle_start: 2026-08-19
target_meeting: 2026-08-21
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E01_stable_domain_discriminant_subspaces/protocol.md
source_meeting: daily_research_reports/0819/meeting/0819_频谱意义会议原文_清晰转述版.md
core_experiment_count: 2
```

> 研究者在 2026-08-20 明确批准：直接写成 Protocol，受控数据和真实数据两轨都
> 实现、冒烟并正式执行。这里保留的是本次批准后的唯一核心任务，不再执行此前
> 草案中的广义特征值/Fisher 方向方案。

> **状态更新（2026-08-20）：**本任务的实验与 canonical 证据已经完成，但研究者
> 尚未填写自己的结果判断。研究者随后明确把组会唯一任务替换为“逐层领域方向
> 图谱”，新活动卡见
> [focus_layerwise_domain_direction_atlas.md](focus_layerwise_domain_direction_atlas.md)。
> 本文件保留为上一任务的历史卡，不再是活动 Focus。

## 1. 核心问题

我们已经在旧的受控数据上看到：每个领域单独学到的低秩方向彼此重合很小，把
多个任务放进一个共享空间时维数会上升，而且这些方向主要不在 PCA 最大方差的
头部。现在只补上最关键的可信度缺口：

> 冻结旧实验学到的“每任务 8 维”和“共享 56 维”空间后，它们能否在从未用于
> 选方向的新表达上继续保留完整 $R_U$ 的分类增益；类似现象能否在具有官方
> 粗领域—细类别划分的真实用户请求数据上复现；真正有功能的方向主要落在总体
> 频谱的哪一段？

$R_U$ 仍指本层注意力写入造成的状态改变中，扣除旧状态可线性预测部分后的候选
更新。它不是“新知识”。“低秩功能空间”指把 $R_U$ 投影进去后仍能保留分类增益
的可学习线性子空间，不用分类数或协方差能量直接替代功能判定。

## 2. 实验目的

本轮有两个互补实验，但共同回答同一个可信度问题：

1. **受控新密封确认。**完全冻结旧实验的逐任务 8 维空间、共享 56 维空间、分类
   头、残差化器和 PCA；在“新模板/新组合”和“新事实原子”两套新数据上检查完整
   $R_U$ 是否仍有增益、低秩空间能保留多少，以及保留功能的方向落在哪个谱段。
2. **真实数据外部复制。**使用 MASSIVE 英文真实用户请求的官方训练/验证/测试划分，
   在多个粗领域内部做细类别分类。先检查完整 $R_U$ 是否相对旧状态带来未见测试
   增益；只有入场通过，才学习逐领域低秩空间、共享空间并检查维数上升与谱段位置。

**完成标准：**两轨都必须产出可审计的入场结果。受控轨还必须产出新数据上的
完整/逐任务 8 维/共享 56 维功能结果，以及“谱段方向重合 + 只保留该谱段 + 删除
该谱段”的联合结果；真实轨若入场失败则按协议停止，这个负结果本身就是完成，
不能继续用低秩图解释。

本轮仍不回答 Router 是否有效、专家是否专门化、LoRA 为什么有效、是否因果使用、
是否一学就会且永不遗忘。

## 3. 分析方法

1. **先看功能还在不在。**旧空间在新受控数据上只评估、不重学；真实数据只用
   训练集拟合、验证集选设置、官方测试集一次裁定。完整 $R_U$ 相对只用旧状态
   没有正增益时，低秩问题直接记为不适用。
2. **再问低秩和共享。**比较完整 $R_U$、逐任务低秩、共享低秩、同秩随机空间和
   标签打乱；看逐任务最小维数，以及用一个空间服务所有任务时维数是否上升。
3. **最后定位到频谱。**PCA 只由训练集拟合，在训练样本真正能识别的子空间内切
   成五个谱段。方向重合只说明“朝哪里”；只保留/删除某段后的未见数据功能变化
   才说明“这一段是否足够/必要”。

## 4. 结论

### 执行前：两种预期结果

- **若支持：**受控新表达上完整 $R_U$ 入场，逐任务 8 维和共享 56 维继续保留注册
  的功能比例；真实数据也先通过完整 $R_U$ 入场，并出现“逐任务较低维、共享维数
  上升”的同向结果。若功能与方向重合都集中在中后谱段，可更新为“分类有用方向
  不等于最大方差方向，而且共享多个任务要付出更高维数”。
- **若不支持或只部分支持：**受控新表达失败说明旧结果可能依赖旧表达；新事实或
  真实数据失败则把结论限制为受控同分布存在性；真实数据完整 $R_U$ 入场失败时，
  只能说当前自然任务没有给低秩分析提供前提，不能反推所有自然数据都不存在
  层间新增功能。

### 执行后：由研究者完成

- **直接结果：**实验正在执行，等待 canonical `summary.md` / `detailed.md`。
- **我的结论：**等待研究者在看到图表后用自己的话填写。
- **仍不能说：**当前没有本轮已完成的正式结果，也没有 Router/专家机制结论。
- **唯一下一决策：**两轨完成后，研究者根据直接结果决定是否把“功能低秩且位于
  非头部谱段”作为后续 Router 候选表示的可信先验。

## 路径

- **会议来源：**[0819 频谱意义会议原文](../0819/meeting/0819_频谱意义会议原文_清晰转述版.md)
- **研究锚点：**[A15_07 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md)
- **实验协议：**[A15_07 E01 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E01_stable_domain_discriminant_subspaces/protocol.md)
- **先验证据：**[E03 低秩功能实验](../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E03_aligned_hierarchical_taxonomy_replication/summary.md)
- **简明结果、详细证据与日报：**结果文件待正式运行后创建；完整日报必须等待研究者确认本节“执行后”字段。
