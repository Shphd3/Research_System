# SAE 训练历史下的注意力写入浓缩是否伴随 N8 领域可读性增强？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15_17_02.sae_n8_separability
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-23
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/protocol.md
core_experiment_count: 1
```

## 核心问题与边界

N8 是八个学术来源领域的固定分类面板。比较相同训练词元坐标下、模型原生第八层注意力写入的领域可读性，判断稀疏自编码器（SAE）相关的表征浓缩是否伴随更清楚的领域区分。本轮不裁定系数的孤立因果作用、模型实际使用、语言模型质量或跨种子普遍性。

## 预测、竞争解释与实验

**目的：**把已观察的表征浓缩与同一面板上的领域读出直接联系起来。

**假设：**从头采用较低 SAE 系数训练的模型可能比 Dense 模型更易读出 N8 领域。最强竞争解释是训练历史只改变共同方向、尺度或稀疏原子使用，并未改善领域区分；重加权模型与从头训练模型的差异有助于暴露这个边界，但不能隔离系数效应。

**分析方法：**在固定输入、相同训练坐标和同一读出规则下比较模型；仅用拟合与开发数据训练和选择线性读出器，用留出测试数据判断差异。表征浓缩与聚类指标只用于解释，不替代主要读出判断。精确设置及支持、不支持、证据不足的预注册分支见 [E01 协议](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/protocol.md)。

**结论分支：**读出优势满足协议判据才支持有限的可读性优势；浓缩更强但读出明确更弱则反对把浓缩视为领域可读性的可靠替身；方向区间跨零或资格检查失败时保持不足或不可裁定。

## 当前证据与轮次摘要

| 日期（UTC） | 本轮问题 | 结果或 `NOT RUN` | 认识更新 |
|---|---|---|---|
| 2026-09-23 | 相同 17B 坐标下的 N8 读出 | E01 测量完成且合格；研究者判断待定 | 从头 S7 对 Dense 的主要方向仍不足；重加权 S7 读出低于从头 S7。见 [结果摘要](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/summary.md)。 |
| 2026-09-23 | 15B/17B 四模型描述性矩阵 | 原作业失败；已有缓存的 CPU 恢复完成 | 矩阵仅作事后描述，原失败与批量差异保留。见 [E02 证据记录](../../Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E02_n8_15b17b_matrix/detailed.md)。 |

## 待研究者裁决

- **我的认识更新：** Unknown，待研究者判断。
- **仍不能说：** 已证明 SAE 系数因果效应、普遍语义改善、模型使用或性能增益。
- **唯一下一决策：** Unknown／待研究者判断。尺度或白化能否恢复读出缺口只是 AI 建议，尚非研究者决定，也不是执行授权。
