# 冻结教师后，高层语义能否通过动态专家树整理第二层有效表示？

```text
type: meeting_cycle_core_task
status: HUMAN_CONFIRMED_EXECUTION_AUTHORIZED
problem_key: A15.semantic_supervision_middle_layer_separability
focus_role: PRIMARY
conversation_owner: codex-thread:01a0508f-34cb-7d20-bda8-d9271307c0a6
ownership_status: CLAIMED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
data_definition: HUMAN_CONFIRMED
cycle_start: 2026-08-28
target_meeting: 2026-08-31
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E04_frozen_teacher_route_only_dynamic_expert_tree/protocol.md
source_meeting: daily_research_reports/0828/docs/0828组会_逐句校订与下一步研究方向.md
core_experiment_count: 3
execution_status: E04_APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_TWO_SEED_FULL_RUN
interpretation_status: NOT_RUN
```

## 1. 核心问题

三层因果语言模型只用整条序列的下一词元损失学会任务后，将其全部冻结。第三层答案前表示形成的语义标签，能否通过第二层之后新增的“先粗分、固定粗路径、再在父类内细分”的动态路由—专家树，把第二层的有效表示整理得比公平的平铺基线更符合真实粗细语义？正确标签能否给出上界，第三层自产标签能否复现该方向，删除粗判别方向是否改善细路由？

原始第二层表示和原模型参数始终固定。本轮所说的“第二层有效表示”是原始第二层表示加上被路由父专家与叶专家的残差输出；因此结果不能表述成原第二层参数被塑造。

## 2. 实验一：监督、拓扑与标签来源的核心比较

### 1. 目的

比较平铺续训、无标签层级生长、真实标签层级监督和第三层伪标签层级监督，区分新增容量、层级拓扑、正确语义监督和自产语义监督各自的作用。

### 2. 假设

若语义监督确实能整理新增模块形成的有效表示，真实标签层级组应稳定优于结构完全相同但只训练语言损失的组；若只是层级拓扑或额外参数起作用，无标签层级组也会得到同等改善。第三层伪标签只有先通过不看真值的稳定性和非坍缩检查，并在冻结后高于随机地对齐真值，才有资格被解释为语义入口。

### 3. 分析方法

1. 所有条件从同一种子教师快照出发，使用同一数据顺序、优化器、总步数和最终步检查点；平铺组匹配层级组的总参数与每样本活动专家计算量。
2. 第一比较是真实标签层级组减去无标签层级组；第二比较是无标签层级组减去平铺组；第三比较是伪标签层级组减去无标签层级组，并用真实标签层级组作为方向上界。
3. 第一眼只看未见模板测试集上，父类内细标签的低尾归一化间隔；语言损失、答案损失和答案准确率只负责守卫原任务未被破坏。

### 4. 结论分支

- 真实标签组不优于无标签层级组：停止解释去粗与伪标签机制；本实现未建立语义路由监督对有效表示的作用。
- 真实标签有效而伪标签入口或下游比较失败：只支持表示整理可行，标签发现失败。
- 真实标签有效、伪标签入口通过且伪标签组复现同向改善：才支持第三层自产标签能够指导第二层后的新增模块。

## 3. 实验二：去粗路由与专家输入消融

### 1. 目的

在真实标签上检验导师“固定粗路径后处理剩余细信息”的具体实现，区分细路由是否需要删除粗判别方向，以及叶专家应并行读取原始第二层表示还是顺序读取父专家输出。

### 2. 假设

若已解释的粗判别方向会干扰父类内细路由，细路由读取去粗表示应优于读取完整表示；若父、叶专家承担互补残差而非串行改写，并行读取原始表示应不差于顺序读取父专家输出。

### 3. 分析方法

1. 在真实标签、粗阶段冻结和并行专家固定时，只改变细路由读取完整表示还是去粗表示。
2. 在真实标签、去粗细路由和粗阶段冻结固定时，只改变叶专家读取原始表示还是父专家更新后的表示。
3. 分别比较最终有效表示的同一低尾间隔，并检查路由准确率、熵、负载和语言功能守卫。

### 4. 结论分支

- 只有真实标签主比较先通过，去粗或输入消融才可作机制解释。
- 去粗优于完整输入只支持删除这一条已学粗判别方向有帮助，不等于已经删除全部粗语义。
- 并行不差于顺序支持使用可并行的父、叶残差路径；反之则保留顺序依赖为后续候选。

## 4. 实验三：粗阶段冻结的次要机制检查

### 1. 目的

检查细阶段完全固定粗路由和父专家，是否比粗细共同更新更符合当前渐进生长实现。

### 2. 假设

若固定粗路径能保护已学父类划分，冻结组应至少不差于联合更新组；若联合更新更好，只说明联合优化在本任务中更有效，不能支持“固定粗路径后学习剩余信息”。

### 3. 分析方法

1. 在真实标签、去粗细路由和并行专家固定时，只改变细阶段是否继续更新粗路由与父专家。
2. 同时检查粗路由准确率是否保持、有效表示低尾间隔和语言功能是否变化。

### 4. 结论分支

- 冻结组更好或不差：保留导师机制的主实现。
- 联合更新更好：记录优化优势，但不把它用作导师固定粗路径机制的证据。

## 5. 当前认识与边界

旧 E02-R 已证明微型模型能够学会修复后的合成语言任务，但旧的“每个专家都预测全部标签”的辅助分类头没有给出稳定 Oracle 效果；E03 在真实 CLINC150 上也未证明自产标签层级路由优于平铺路由。本次 E04 不覆盖这些失败，而是针对最直接的操作错配进行修复：分类监督只训练路由器，专家只通过被选中样本的语言损失训练，并把原始第二层与新增模块形成的有效表示严格分开。

当前不能声称导师直觉成立、原第二层参数被塑造、伪标签天然具有语义、专家已经功能专门化，或结果可迁移到开放域语言。

**唯一下一决策：**完成两个配对种子的 E04 全运行后，先裁定真实标签层级组是否稳定优于无标签层级组。只有这一步通过，才依次解释去粗、专家输入、层级拓扑与伪标签结果。

## 6. 证据入口

- **会议来源：**[0828 组会逐句校订与下一步研究方向](../0828/docs/0828组会_逐句校订与下一步研究方向.md)
- **Anchor：**[A15.13 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md)
- **E04 Protocol：**[A15.13 E04 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E04_frozen_teacher_route_only_dynamic_expert_tree/protocol.md)
- **历史 E02-R：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E02_repaired_rule_induction_teacher_entrance_and_full_semantic_supervision/summary.md)
- **历史 E03：**[Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E03_qwen06b_clinc150_one_layer_backward_hierarchical_router/summary.md)
