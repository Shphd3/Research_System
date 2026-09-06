# 静态语义可读性能够预测 MoE 应该插在哪一层吗？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15.layerwise_moe_insertion_validation
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: AWAITING_HUMAN_CONFIRMATION
cycle_start: 2026-09-04
target_meeting: 2026-09-05
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md
core_experiment_count: 2
```

## 核心问题

冻结模型在某一层越容易读出真实粗细领域，是否就意味着把同一套语义 MoE 放在这一层时，更容易学会语义分发，并带来更大的下一词元损失收益和更明确的专家功能？

这里的“静态可读性”只指冻结表示上新训练分类器的表现；“功能收益”必须由语言模型损失或换错、删除专家的干预来证明，不能由分类准确率代替。

## 实验 1：补齐平铺 Oracle

### 1. 目的

补齐平铺八专家的正确来源强制路径上界，从而区分“层级结构本身的收益”和“任何正确语义分组都能带来的收益”。

### 2. 假设

如果层级结构有额外价值，层级 Oracle 应优于同活动秩的平铺 Oracle；竞争解释是收益只来自正确分组，两种 Oracle 相近。

### 3. 分析方法

1. 在原八任务答案监督续训设置中，只新增平铺 Oracle；真实来源标签强制选择八个秩 24 专家之一，专家输出不乘 Router 概率，同时保留影子 Router。
2. 与已有平铺 task-only、层级 task-only和层级 Oracle 使用相同数据、128 次更新、两个种子和统一评测器比较。
3. 用答案词元负对数似然、八任务内部能力分数和删除／换错专家损失确认任务效果与专家不可互换性。

### 4. 结论分支

- 若层级 Oracle 稳定优于平铺 Oracle，保留“层级结构带来额外上界”的解释。
- 若两者相近或平铺更好，只能声称正确语义分组有价值，不能把上界归因于层级结构。

## 实验 2：第 9 块与低可读第 1 块的功能性插层对照

### 1. 目的

检验逐层静态语义可读性是否能够作为选择 MoE 插层位置的低成本筛选指标。

### 2. 假设

静态审计中可读性最高并首先稳定的零起始第 9 块，应比同一审计中粗细恢复率最低的第 1 块产生更小的 learned-to-Oracle 差距和更大的语义功能收益。最强竞争解释是静态分类器只说明信息存在，并不能预测训练中的路由或专家效用。

### 3. 分析方法

1. 在相同 M2D2 `3×3` 下一词元任务上，将同一层级 LoRA MoE 分别插入第 9 块与第 1 块；每层比较 task-only、正确路径 Oracle 和真实粗细标签监督的学习 Router。
2. 对学习 Router 复现两项既有消融：细 Router 是否减去粗 Router 的中心化行空间，以及第二阶段粗专家冻结还是继续训练；粗 Router 在第二阶段始终冻结。
3. 先比较路由语义一致性，再比较 held-out 下一词元损失和删除／换错专家干预；只有后两者更好，才说明静态可读性预测了功能性插层价值。

### 4. 结论分支

- 若第 9 块在两个种子中都缩小 learned-to-Oracle 损失差距，并提高专家干预效应，可把静态审计作为当前任务中的候选层筛选器。
- 若第 9 块只提高标签读出或路由一致性，却不提高任务／专家功能，静态审计只能筛“可读层”，不能筛“有用插层”。
- 若两个层的方向不一致或种子相反，结果不足，必须增加层位或独立种子，不能给出普遍选层规则。

## AI 草拟结果，等待研究者确认

- 完整性：替代作业 `pt-lxue71oe` 在单节点 reserved 4×H100 上完成；12 个第一阶段 checkpoint、24 个最终层级模型、2 个 Flat Oracle、全部统一评估与图表齐全，`completion_audit` 返回 `FULL_RUN_COMPLETE`。
- 实验 1：Flat Oracle 相对 Flat task-only 的两种子平均答案词元 NLL 从 `0.831329` 降到 `0.825400`，内部八任务平均从 `0.136719` 升到 `0.152344`；但仍不如层级 task-only 的 `0.806323` NLL 和层级 Oracle 的 `0.794920`。
- 实验 2：第 9 块的学习 Router 确实更接近真实粗细标签，但主指标 $I=G_1-G_9$ 在 seed 17 为 `+0.000625`、seed 29 为 `-0.000911`，方向相反；第 9 块的专家干预效应也没有全面更强。注册裁决为 `INSUFFICIENT`。
- 消融：第二阶段冻结粗专家在两层、两种子中都提高 NLL；减去粗 Router 行空间的影响接近零且方向不稳定。当前实现应只冻结粗 Router，粗专家继续训练，并默认保留原生表示。

不能声称：第 9 块是更好的功能插层位置、静态读出性可以独立决定 MoE 层位，或两层结果构成普遍深度规律。E15 的静态候选本身也仍受 `0.000132` nat 的置乱护栏失败限制。

## 唯一下一决策

研究者确认或修正上述结果后，决定是否保留“静态审计只生成候选层，再用低成本功能试验定层位”的流程；若继续验证，最小补充是一层中等读出性位置和两个新 seed，而不是直接宣布第 9 块。
