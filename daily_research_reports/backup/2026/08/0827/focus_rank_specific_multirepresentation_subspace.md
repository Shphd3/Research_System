# 逐秩重新学习后，单域低秩而多域高秩的判断是否仍然成立？

```text
type: meeting_cycle_core_task
status: EVIDENCE_READY_AWAITING_HUMAN_RESULT
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
cycle_start: 2026-08-27
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: ../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_semantic_conditioned_functional_subspace_anchor.md
protocol: ../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/protocol.md
source_meeting: daily_research_reports/backup/2026/08/0826/focus.md and the researcher-confirmed 2026-08-27 correction discussion
core_experiment_count: 1
```

## 1. 核心问题

旧实验把一次学到的最大秩共享空间截成不同前缀，再把这些前缀当成每个候选秩的最优解。纠正为“每个候选秩独立学习”以后，是否仍能确认：单个学科域只需要较低维的判别子空间，而八个域共用一个子空间需要更高维？这个判断是否同时出现在四种表征中：更新残差 $R_U$、归一化后的注意力更新 $U$、原生路由输入 $G=X+U$，以及相邻层路由输入之差 $\Delta G$？

这里“功能秩”指在未参与拟合的数据上，达到完整线性映射 90% 判别收益所需的最小投影维数；它不是矩阵非零奇异值个数，也不是熵有效秩。

## 2. 实验目的

1. 用逐候选秩独立优化消除旧前缀方法的算法偏差，并保留旧方法作为错误来源对照。
2. 在 Qwen3-30B-A3B、同一冻结 taxonomy、同一数据划分和相同 8-way 域内子类任务上，对四种表征分别比较“八个局部空间的总预算”和“一个八域共享空间的功能秩”。
3. 先在现有 19,200 条数据上得到纠错性回溯结果，再在冻结的新表达确认集上复验；只有后一阶段支持的关系才能称为独立确认。

完成标准：四种表征均完成选层、局部逐秩曲线、八域共享逐秩曲线、局部并集 oracle、旧最大秩前缀对照、数值秩/熵有效秩诊断、置信区间、表格、核心图和完成审计。另在 $R_U\mid X$ 上复核旧 E05 的条件增益口径。

**本轮不回答：**模型原生 gate 是否使用这些方向、方向是否提高专家效用、非线性判别秩、或学习新 Router 是否有效。

## 3. 分析方法

1. 从同一冻结的 $(X,U)$ 张量构造四种表征，只用 TRAIN/DEVELOPMENT 选择每种表征的层和训练设置；同时在共同层做横向对照，防止把层差异误当成表征差异。
2. 单域分别学习秩 1--7 的八个局部映射；八域共享条件在每个候选秩 1--56 上从头独立学习一个公共输入子空间和八个任务头，并与局部映射并集及旧最大秩前缀比较。
3. 用模板族为独立单位计算 90% 功能保留的同时置信下界；先报告回溯结果，再打开冻结的新确认集复验。

## 4. 结论

### 执行前：两种预期结果

- **若支持：**逐秩独立学习后，局部任务在低维达到完整映射收益，而统一八域空间仍需要显著更高的维数，并且该差异在新确认集上存在。可以说这些标签相关线性方向随域联合而扩张；不能说扩张方向就是模型实际路由或专家效用方向。
- **若不支持或证据不足：**若逐秩共享学习在远低于 56 维时已保留功能，旧“多个域需要近 56 维”的认识主要是前缀算法伪影；若完整映射无可靠收益或区间过宽，则功能秩不可识别。两种情况都必须停止把 7/56 当作已证实结构事实。

### 执行后：由研究者完成

- **直接结果：**[AWAITING_HUMAN_RESULT]
- **我的结论：**[AWAITING_HUMAN_RESULT]
- **仍不能说：**[AWAITING_HUMAN_RESULT]
- **唯一下一决策：**[AWAITING_HUMAN_RESULT]

## 路径

- **Protocol：**[protocol.md](../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/protocol.md)
- **Summary：**[summary.md](../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/summary.md)
- **Detailed：**[detailed.md](../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/detailed.md)
- **Daily Report：**研究者完成结果报告后再补
- **Parking Lot：**[README.md](../../Projects/from-attention-to-search/main/parking_lot/README.md)
