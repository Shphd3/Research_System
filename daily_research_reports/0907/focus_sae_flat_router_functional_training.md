# 结构路由是否形成值得局部增量学习的功能分工？

```text
type: meeting_cycle_core_task
task_state: ACTIVE
problem_key: A15.sae_hierarchical_teacher_construction
focus_role: SECONDARY
question_state: HUMAN_CONFIRMED
design_state: HUMAN_CONFIRMED
result_state: NOT_AVAILABLE
cycle_start: 2026-09-09
target_meeting: 2026-09-09
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/post_training_analysis/protocol.md
source_meeting: USER_CONFIRMATION_2026-09-09
core_experiment_count: 2
```

## 1. 核心问题

A6R1 已把结构权重从第 1 次更新的 `0.01` 线性衰减到第 512 次更新的 `0.001`。GMM-B 的三种子平均损失低于纯任务路由，但 seed 43 反向，因此没有稳定方法排序。本轮问题是：这种结构是否仍形成了可干预的专家功能与学习分工，并且当后训练阶段未暴露的任务依次到达时，基于该分工选择复用或局部增长，能否比固定容量适配获得更好的新任务—旧任务权衡。

## 2. 本轮实验

**本轮不回答：**这些分组是否是真实语义类别、Qwen 主干是否从未见过后到知识、内部留出分数是否是官方基准成绩，以及更多专家是否普遍更好。

### 实验 1：A6R1 训练后机制与局部学习审计（S0–S5）

#### 目的

从“教师关系是否进入路由”依次推进到“实际路径是否承担不同函数”和“局部更新是否产生跨组干扰”，并只在固定容量解释不足时比较修路由、更新旧专家、无条件修正和输入条件化修正。

#### 假设

若结构正则形成了有用分工，教师关系应至少传到实际路径或专家函数，并在局部更新中暴露可复现的共享收益、干扰、路由失败或容量不足。最强竞争解释是只改变了概率/负载，专家可互换，或旧 Router/专家已足够。

#### 分析方法

1. S0–S3 在 task-only、SAE-A、GMM-A、SAE-B、GMM-B 的三个种子最终检查点上核验资格、任务损失、路由关系与固定专家干预。
2. S4 在预先锁定的一个双组上比较学习自己与影响另一组；支持集、发现集与探针集隔离，原检查点只读。
3. S5 在同一支持/重放预算下比较 K/R/U/C/G；只有已注册证据触发增长分支，停止分支本身是完整结果。

#### 结论

**支持分支：**若路径有可检出功能、局部更新出现可复现干扰或固定容量不足，且条件化修正改善已注册的新旧权衡，则进入 S6 检验；每一段只支持该段对应的关系。

**不支持分支：**若教师关系未传到路径、专家可互换、局部学习有益共享，或旧 Router/专家达到同一前沿，则停止相应增长主张；不能用后续指标挽救前一段失败。

**证据不足分支：**资格、尾部重建、自替换、组支持量、隔离副本或置信区间任何一项不合格，都只报告准确缺口，不把无候选写成“没有机制”。

### 实验 2：后训练阶段未暴露任务的顺序适配（S6）

#### 目的

把 S5 的局部学习关系推进到真实时间顺序：从原适配器初始化只训练固定哈希顺序中的前六任务，再让 HumanEval 与 MBPP 依次到达，检验结构路由的自适应复用/增长策略能否优于固定容量适配并保留旧任务。

#### 假设

若 GMM-B 的分工对应不同更新需求，则在相同支持记录数、16 次更新和重放预算下，它相对自身最佳固定容量对照的增长增量，应比 task-only 的同一增量更大，同时旧任务损伤不超过 `0.001 nat/token`。最强竞争解释是固定容量联合适配已经足够，或额外容量的作用不依赖结构路由与输入门控。

#### 分析方法

1. 八任务按 `SHA256("continual-v1|task_id")` 固定排序；前六任务训练 task-only 与仅在前六任务词元上拟合教师的 GMM-B，种子为 17/29/43。
2. 对两个后到任务分别用嵌套的 1/4/16/64 条唯一训练记录，从同一阶段起点独立恢复，比较 K、Router-only、旧专家、Router+旧专家、常量门控修正和输入门控修正，记录 0/1/4/8/16 次更新。
3. 在旧任务重复、旧任务混合比例变化和真实新任务窗口上评估不使用 task_id 的损失预警；预警只开启候选比较，永久动作由独立开发记录选择，最终在固定测试面板比较新任务收益、旧任务损伤和成本。

#### 结论

**支持分支：**至少一个后到任务在不超过 16 条支持记录时，GMM-B 的结构增长增量三个种子均超过 task-only `0.001 nat/token`，旧任务损伤上界合格，输入门控优于无条件修正与固定容量，而且两个控制流均不发生永久增长。

**不支持分支：**固定容量匹配或更好、种子反转、旧任务损伤超界、输入门控不优于无条件容量，或控制流发生系统性不必要增长，均停止相应自适应增长主张。

**证据不足分支：**未来任务泄漏、起点/路径不一致、支持或探针不足、自动预警不触发、初始化 no-op 失败或区间跨越判定区时，不改阈值、不缩种子，保留为明确的不足状态。

## 3. 核心任务卡总结论

- **当前证据：**A6R1 的 12 条轨迹与完整内部评估已完成。GMM-B 平均 NLL 为 `0.694560`，task-only 为 `0.696578`；逐种子差值为 `-0.003897/-0.002480/+0.000322`，因此平均改善存在但稳定排序不成立。S0–S6 尚无 A6R1 结果。
- **仍不能说：**不能声称结构正则稳定提高任务表现、形成真实语义专家、旧容量已耗尽、局部增长有用，或已经实现自动持续学习。
- **唯一下一决策：**执行冻结的 S0–S6 链，判断 GMM-B 的有界自适应局部策略是否在后到任务上通过结构增量、旧任务保留和控制流误增长三项护栏。完成标准是所有注册阶段产生合格结果或类型化停止状态，且模型、种子、支持规模和资源成本均可审计。

## 路径

- **实验协议：**[A6 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/protocol.md)
- **A6 结果摘要：**[A6 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/summary.md)
- **当前 Anchor：**[A15_13_11 Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md)
- **A6R1 重训协议：**[A6R1 Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/protocol.md)
- **S0–S6 协议：**[A6R1 Post-training Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/post_training_analysis/protocol.md)
- **A6 完整证据：**[A6 Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/detailed.md)
- **前序结果摘要：**[A5 Summary](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A5_balanced_h/summary.md)
- **前序完整证据：**[A5 Detailed](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A5_balanced_h/detailed.md)
- **每日研究报告：**NOT_YET_WRITTEN
- **待研究问题清单：**[Parking Lot](../../Projects/from-attention-to-search/main/parking_lot/README.md)
