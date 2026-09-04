# 静态语义可读性能够预测 MoE 应该插在哪一层吗？

```text
type: meeting_cycle_core_task
status: FULL_RUN_RUNNING_AFTER_SMOKE_PASS
problem_key: A15.layerwise_moe_insertion_validation
focus_role: SECONDARY
conversation_owner: codex-thread:01a054b9-ff32-7012-aae0-ccfea85152cf
ownership_status: CLAIMED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
result_account: NOT_RUN
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

## 唯一下一决策

全量结果完成后，决定是否把“先做静态可读性审计，再只在候选层训练 MoE”纳入后续实验流程；完成标准是两个种子、两层、全部注册消融、Flat Oracle、统一评估和图表均通过完整性审计。

## 执行进度（不构成实验结果）

- 实现与本地回归测试已经完成，完整测试为 `12/12` 通过。
- 首次 ACP 作业 `pt-owrlkt10` 在任何训练开始前，被冻结梯度审计的误报阻断。误报原因是审计把注入基座内部、但本应训练的适配器参数错误计入了冻结基座参数；修复后增加了对应回归测试。
- 替代作业 `pt-lxue71oe` 使用单节点 reserved 4×H100，从第 0 步重新开始。它已通过因果前缀、冻结边界、Flat Oracle 强制路径和单位专家系数检查，当前处于 `RUNNING`。
- 冒烟损失只用于确认数值有限，不能用来判断第 9 块是否优于第 1 块，也不能用来形成 Flat Oracle 结论。`result_account` 在完整性审计通过前保持 `NOT_RUN`。
