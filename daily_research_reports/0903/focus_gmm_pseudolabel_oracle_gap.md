# 对角高斯伪标签能否缩小语义 Router 的 Oracle 差距？

```text
type: meeting_cycle_core_task
status: EXECUTION_APPROVED_IN_PROGRESS
problem_key: A15.semantic_supervision_middle_layer_separability
focus_role: SECONDARY
conversation_owner: codex-thread:01a0652d-8c53-71e0-aab2-4008063e91a3
ownership_status: CLAIMED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
cycle_start: 2026-09-03
target_meeting: 2026-09-04
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md
core_experiment_count: 2
```

## 1. 核心问题

最后一层整窗表征拟合出的对角高斯层级伪标签，能否训练出接近强制正确路径 Oracle 的因果 Router，并在不损害八项任务内部能力的同时，提高学习效率和专家不可互换功能；无梯度负载均衡偏置能否进一步缩小差距？

## 2. 本轮实验

### 实验 1：M2D2 对角高斯伪标签闭环

#### 目的

在已知自然语言粗细领域结构的数据上，隔离标签几何、学习路径、硬伪路径和负载均衡对 Oracle 差距的影响。

#### 假设

1. 完整向量的对角高斯伪标签应比旧方向加模长标签更接近 Oracle 的损失与专家干预结果。
2. 若主要瓶颈是概率缩放或负载偏斜，单位系数硬伪路径或无梯度负载均衡应稳定缩小差距。

#### 分析方法

1. 用训练集末层整窗平均表征拟合并冻结 `3×3` 对角高斯标签；真实领域标签只用于事后审计。
2. 在同一两阶段训练预算下比较学习路径、单位系数硬伪路径、频率匹配随机标签及其负载均衡开关。
3. 所有 checkpoint 冻结后统一比较留出 NLL 曲线、路由语义、负载、删除与换错专家干预和参数几何。

#### 结论

执行前分支：若无监督标签稳定缩小 Oracle 的最终 NLL、曲线面积和专家干预差距且不损害任务性能，进入裁决 A；若只学会语义分发而任务证据不改善，进入 B；若任何注册组、种子、数组或统一评测不完整，进入 C。

### 实验 2：八任务答案监督内部能力诊断

#### 目的

检验同一方法在八种真实任务答案续训中，是否以相同活动秩保持任务能力并提高数据效率与专家功能。

#### 假设

1. 对角高斯伪标签的硬路径训练应比普通学习路径更接近真实来源 Oracle。
2. 最强竞争解释是语义一致性与参数差异上升，但 task-only 的损失、任务分数和专家功能仍不弱于语义方法。

#### 分析方法

1. 在固定的八任务均衡答案混合上，以相同数据顺序、答案词元预算和活动秩训练十个注册条件、两个种子。
2. 全部模型训练完并登记哈希后，用同一提示、解码、答案抽取和代码沙箱做八项逐题评测。
3. 将任务分数和答案词元 NLL 作为主证据；路由、负载、专家干预和参数谱只用于定位原因。

#### 结论

执行前分支与实验 1 共用 A/B/C 裁决；本数据含官方评测题，因此八项分数只称为“混合任务内部能力诊断”，不声称无污染泛化。

## 3. 冻结边界

- 不使用“减去粗 Router 行空间”。
- Oracle 与硬伪路径的专家输出系数固定为一，影子 Router 只作诊断。
- 负载均衡偏置无梯度，只改变前一选择，且统计整个有效批次。
- 训练中检查不用于删组、改配置或按结果选 checkpoint。
- 第一张结果表必须是完整八项任务表；第一张曲线必须比较 task-only、对角高斯学习路径、对角高斯硬伪路径与 Oracle。

## 4. 路径

- [Anchor](../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md)
- [Protocol](../../Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_gmm_pseudolabel_oracle_gap/protocol.md)
