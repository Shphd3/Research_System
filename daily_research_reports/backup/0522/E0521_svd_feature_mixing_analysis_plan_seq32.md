# E0521 / E0522 SVD Feature-Mixing Analysis Plan  
## 已训练 seq_len=32 MoE 的 post-training diagnostic

## Conclusion

你现在已经完成了导师之前要求的训练，且当前训练设置为 `seq_len=32`。下一步不要立刻重新训练，也不要先改 routing 结构；应该先做 **post-training analysis**：

> 在已经训练好的 `seq_len=32` 模型上，诊断 ordinary MoE routing 得到的 expert bucket 到底是 feature-level specialist，还是 mixed token/context bucket。

最重要的判定对象是：

> **AB-dominant expert 的 dominant subspace 是否同时包含 A、B、AB interaction 三类 feature direction。**

最重要的指标是：

```text
ProjectionScore(v_A, S_e)
ProjectionScore(v_B, S_e)
ProjectionScore(v_AB_interaction, S_e)
+
mask expert 后 A-only / B-only / AB-composite 的 loss change
```

如果 AB-dominant expert 同时包含 A/B/AB，并且 mask 它同时伤害 A-only、B-only、AB-composite，说明当前 top-1 MoE 更像 mixed expert，不是干净的 feature-level index。

如果 AB-dominant expert 主要只包含 AB interaction，并且 mask 它主要伤害 AB-composite，说明当前 setup 下 ordinary MoE 至少有可能形成 composite-feature specialization。

---

## Self-Contained Context

我们的主线问题是：

> Long-context attention 是否可以被理解成对 KV memory 的 learned search / learned indexing？

MoE expert id 是一个可能的 index candidate：

```text
token hidden state -> router -> expert id
```

如果 expert bucket 是 feature-pure 的，那么它可能帮助我们缩小 KV candidate set。  
如果 expert bucket 是 mixed 的，那么它不适合直接作为 KV index。

导师提到 SVD 的意思不是让我们用 SVD 设计新模型，而是让我们做 representation diagnostic：

```text
收集某个 expert 接收的 hidden states
-> 对这些 hidden states 做 SVD
-> 看 expert 的主方向里是否混入 A、B、AB 多种 feature
```

当前 `seq_len=32` 的边界：

> 这个分析只证明 controlled synthetic setup 下的 specialization / feature mixing 机制；它不能证明真实长上下文语言模型中的 retrieval speedup。

---

## Decision Question

本轮分析只回答一个问题：

> 在已经训练好的 `seq_len=32` MoE 中，ordinary routing 是否形成 feature-level specialization，还是把 A、B、AB 这些 feature 混在同一个 token-level expert bucket 中？

更具体地说：

> AB-composite 样本的 dominant expert 是否主要承载 AB interaction，还是同时承载 A-only、B-only、AB-composite 的表示与功能？

---

## Hypothesis

### H1: Feature-entangled expert hypothesis

普通 top-1 MoE router 看到的是整个 hidden state：

```text
h = mixed context-conditioned token representation
```

这个 hidden state 里可能同时包含：

```text
A feature
B feature
AB interaction feature
background / positional information
```

因此 top-1 router 可能把整个 mixed representation 送给一个 expert，导致 expert bucket 不是 feature-pure。

### H2: Feature-specialized expert hypothesis

如果模型真的学到了 feature-level specialization，那么：

```text
A-only 样本主要进入 A expert
B-only 样本主要进入 B expert
AB-composite 样本主要进入 AB expert
```

并且 AB expert 的 dominant representation subspace 应该主要包含 AB interaction direction，而不是同时包含 A 和 B。

### H3: Mainline relevance

只有当 expert bucket 在 representation 和 function 上都足够 feature-coherent，它才有资格被继续测试为 KV retrieval index candidate。

---

## Mathematical Modeling

### 1. Hidden state

对第 `l` 层、第 `p` 个位置、第 `i` 个样本，记 hidden state 为：

$$
h_{i,p,l} \in \mathbb{R}^d
$$

router 的输入应该优先使用模型代码里真正传给 router 的 tensor，例如：

```text
router_input
pre_expert_hidden
post_attention_pre_mlp_hidden
pre_router_layernorm_output
```

**原则：用 router 实际看到的 hidden state，而不是随便取一个中间张量。**

---

### 2. Feature classes

构造 balanced eval set，至少包含四类：

```text
C0: background / neither A nor B
CA: A-only
CB: B-only
CAB: AB-composite
```

每类样本数建议：

```text
n_eval_per_class >= 1024
```

如果模型很小或专家数较多，建议：

```text
n_eval_per_class >= 4096
```

因为每个 expert 内部需要有足够样本才能做 SVD。

---

### 3. Feature direction definitions

对某个 layer `l`、某个分析位置 `p*`，定义各类 hidden mean：

$$
\mu_0 = \mathbb{E}[h_{p*,l} \mid C0]
$$

$$
\mu_A = \mathbb{E}[h_{p*,l} \mid CA]
$$

$$
\mu_B = \mathbb{E}[h_{p*,l} \mid CB]
$$

$$
\mu_{AB} = \mathbb{E}[h_{p*,l} \mid CAB]
$$

定义 A direction：

$$
v_A = \mu_A - \mu_0
$$

定义 B direction：

$$
v_B = \mu_B - \mu_0
$$

定义 raw AB direction：

$$
v_{AB}^{raw} = \mu_{AB} - \mu_0
$$

但 raw AB 很容易混入 A 和 B，所以更重要的是 AB interaction direction：

$$
v_{AB}^{int} = \mu_{AB} - \mu_A - \mu_B + \mu_0
$$

这是本实验最关键的数学定义。

解释：

```text
v_AB_raw  = AB 相对于 background 的整体差异，里面可能包含 A+B。
v_AB_int  = AB 共同出现时，超出 A-only + B-only 加和的 interaction component。
```

如果只看 `v_AB_raw`，容易把 A+B 误认为 AB composite feature。

---

### 4. Expert subspace

对某个 expert `e`，收集所有被 router 分到该 expert 的 hidden states：

$$
H_e =
\begin{bmatrix}
h_1 \\
h_2 \\
\cdots \\
h_n
\end{bmatrix}
\in \mathbb{R}^{n \times d}
$$

中心化：

$$
\tilde{H}_e = H_e - \bar{H}_e
$$

做 SVD：

$$
\tilde{H}_e = U_e \Sigma_e V_e^\top
$$

取前 `r` 个 right singular vectors：

$$
S_{e,r} = \mathrm{span}(V_{e,1}, \dots, V_{e,r})
$$

`S_{e,r}` 就是 expert `e` 的 dominant representation subspace。

---

### 5. Projection score

对任意 feature direction `v`，定义它落在 expert dominant subspace 上的比例：

$$
\mathrm{ProjScore}(v, e, r)
=
\frac{
\|P_{S_{e,r}} v\|_2^2
}{
\|v\|_2^2
}
$$

其中 `P` 是投影矩阵。

解释：

```text
ProjScore 接近 1:
  该 feature direction 很大程度落在 expert e 的 dominant subspace 中。

ProjScore 接近 0:
  该 feature direction 不在 expert e 的主要表示方向中。
```

---

## Critical Implementation Choice: Analyze Which Position?

当前 `seq_len=32`，必须先明确分析位置。

### Primary position: prediction/query position

默认优先分析：

```text
p* = 用来预测 target 的最后一个 context 位置
```

如果你的输入是长度 32 的 context，用第 32 个 token 预测下一个 target，那么：

```text
0-based index: p* = 31
1-based index: p* = 32
```

这是最重要的位置，因为它最接近模型做 next-token prediction 的 decision state。

### Secondary positions

后续可以分析：

```text
A token 所在位置
B token 所在位置
所有非-padding位置
```

但第一轮不要把所有位置混在一起，否则 position signal、feature signal、task signal 会混在一起，解释困难。

### Recommended first pass

第一轮只做：

```text
position = prediction position p*
layer = 每一个 MoE layer 的 router input
```

如果模型只有一个 MoE layer，就只分析该层。

---

## Analysis Pipeline

---

# Experiment 0: Evaluation Data Sanity

## Purpose

确认测试集中的 A-only、B-only、AB-composite、background 四类样本定义清楚，并且没有 target leakage 或 positional shortcut。

## Mainline Relation

如果 feature label 本身不干净，那么后续无法判断 expert 是否 feature-specialized，也无法判断 expert bucket 是否可作为 KV index。

## Design

构造 balanced eval set：

```text
C0:  no A, no B
CA:  contains A, does not contain B
CB:  contains B, does not contain A
CAB: contains both A and B, target requires AB composite rule
```

建议两个版本：

### Protocol 0A: fixed-position eval

固定 A/B 出现位置，减少 positional confound：

```text
A position fixed
B position fixed
other tokens random distractors
seq_len = 32
```

### Protocol 0B: randomized-position eval

随机 A/B 出现位置，测试模型是否只学位置 shortcut：

```text
A and B positions randomized
distance(A, B) varied
seq_len = 32
```

第一轮先跑 fixed-position eval。  
如果结果清楚，再跑 randomized-position robustness。

## Required checks

```text
class balance
target distribution
A/B position distribution
no target token appears in context
no accidental B in A-only
no accidental A in B-only
```

## Deliverables

```text
tables/eval_data_summary.csv
figures/feature_position_histogram.png
```

---

# Experiment 1: Dense / Task Performance Sanity on Trained Model

## Purpose

确认已经训练好的模型确实学会了这个 synthetic task。  
如果模型没有学会任务，就不能解释 expert specialization。

## Mainline Relation

specialization analysis 的前提是模型已经能解决任务。  
如果模型 loss 很高，routing/SVD 现象可能只是未训练充分或容量不足。

## Metrics

按 class 分别统计：

```text
loss_C0
loss_A_only
loss_B_only
loss_AB
accuracy_C0
accuracy_A_only
accuracy_B_only
accuracy_AB
```

## Decision Rule

### If task performance is good

继续做 routing/SVD。

### If dense/task performance is poor

不要 claim MoE specialization。先回到训练或数据构造问题。

## Deliverables

```text
tables/per_class_performance.csv
figures/per_class_loss_bar.png
figures/per_class_accuracy_bar.png
```

---

# Experiment 2: Routing Distribution Diagnostic

## Purpose

先不用 SVD，直接看 feature class 到 expert id 的分配是否集中。

要回答：

```text
A-only / B-only / AB-composite 是否进入不同 expert？
AB-composite 是否有 dominant expert？
AB-dominant expert 是否也大量接收 A-only / B-only？
```

## Mainline Relation

如果 routing 本身都不按 feature class 组织，那么 expert bucket 作为 KV index 的希望较弱。  
如果 routing 有清晰结构，再看 representation subspace 是否也干净。

## Data to collect

对每个样本，在 position `p*`、layer `l` 上记录：

```text
sample_id
class_label in {C0, CA, CB, CAB}
expert_id
router_logits
router_probs
prediction_loss
correct_or_not
```

## Metrics

### 1. Class-to-expert routing

$$
P(e \mid c)
$$

即：

```text
给定 class c，样本被送到 expert e 的概率。
```

### 2. Expert composition

$$
P(c \mid e)
$$

即：

```text
给定 expert e，它接收到的样本分别来自哪些 class。
```

### 3. Expert purity

$$
\mathrm{Purity}(e) = \max_c P(c \mid e)
$$

### 4. Routing entropy by class

$$
H(E \mid C=c)
$$

如果某个 class 被分散到很多 expert，entropy 高。  
如果集中到少数 expert，entropy 低。

### 5. Mutual information / NMI

```text
NMI(feature_class, expert_id)
```

用于衡量 feature label 和 expert id 是否对齐。

## Key Figures

```text
figures/routing_heatmap_P_expert_given_class.png
figures/expert_composition_P_class_given_expert.png
figures/expert_purity_bar.png
figures/routing_entropy_by_class.png
```

## First decision

找到：

```text
e_AB_route = argmax_e P(e | CAB)
e_AB_pure  = argmax_e P(CAB | e), with minimum sample count
```

后续 SVD 分析至少看这两个 expert。

---

# Experiment 3: Feature Direction Construction

## Purpose

把 A、B、AB 这些口头概念变成可计算的向量方向。

## Mainline Relation

如果没有可计算的 feature direction，就无法判断 expert 主子空间是否包含某个 feature，也无法说 expert 是否 feature-pure。

## Procedure

对每个 layer `l`、position `p*`，在所有样本上计算：

```text
mu_0
mu_A
mu_B
mu_AB
```

然后计算：

```text
v_A
v_B
v_AB_raw
v_AB_int
```

## Required normalization

建议对 direction 做 L2 normalization：

$$
\hat{v} = \frac{v}{\|v\|_2 + \epsilon}
$$

保留 direction norm 作为附加信息：

```text
norm_v_A
norm_v_B
norm_v_AB_raw
norm_v_AB_int
```

如果 `norm_v_AB_int` 非常小，说明 AB interaction 本身在该 layer/position 可能不明显，后续 projection 解释要谨慎。

## Deliverables

```text
tables/feature_direction_norms.csv
artifacts/feature_directions_layer{l}_pos{p}.pt
```

---

# Experiment 4: Expert Input SVD

## Purpose

检查每个 expert 接收的 hidden states 的 dominant subspace 中包含哪些 feature direction。

这是导师提到 SVD 时最核心的分析。

## Mainline Relation

如果某个 expert 的 dominant subspace 同时包含 A、B、AB interaction，那么它是 mixed representation bucket，不是干净的 feature-level index。  
如果 AB expert 主要只包含 AB interaction，那么它更像 feature-level specialist。

## Procedure

对每个 layer `l`、每个 expert `e`：

1. 收集所有被路由到 expert `e` 的 hidden states：

```text
H_e = {h_i | expert_id_i = e}
```

2. 如果样本数太少，跳过：

```text
min_count_per_expert = 128
```

3. 中心化：

```text
H_e_centered = H_e - mean(H_e)
```

4. 做 SVD：

```text
H_e_centered = U S V^T
```

5. 取不同 rank：

```text
r in {1, 2, 4, 8, 16}
```

6. 计算 projection score：

```text
ProjScore(v_A, e, r)
ProjScore(v_B, e, r)
ProjScore(v_AB_raw, e, r)
ProjScore(v_AB_int, e, r)
```

## Important control

同时计算 global subspace baseline：

```text
对所有样本 hidden states 做 SVD，得到 S_global,r
计算 feature directions 在 global subspace 上的 projection score
```

原因：

```text
如果所有 feature directions 本来就在 global top subspace 中，
那么 expert subspace 高 projection 不一定说明 expert 特殊。
```

## Deliverables

```text
tables/svd_projection_scores.csv
tables/svd_explained_variance.csv
figures/proj_scores_by_expert_r4.png
figures/proj_score_curves_for_AB_expert.png
figures/singular_value_spectrum_by_expert.png
```

---

# Experiment 5: AB-Dominant Expert Deep Dive

## Purpose

专门回答导师最关心的问题：

> 如果一个 expert 看起来学到了 AB，它里面是不是也包含 A 和 B？

## Mainline Relation

这是判断 expert bucket 是否可作为 feature-level KV index 的核心证据。

## Procedure

选择两个 candidate AB expert：

```text
e_AB_route = argmax_e P(e | CAB)
e_AB_pure  = argmax_e P(CAB | e), with count(e) >= min_count
```

对它们报告：

```text
P(e | C0), P(e | CA), P(e | CB), P(e | CAB)
P(C0 | e), P(CA | e), P(CB | e), P(CAB | e)

ProjScore(v_A, e, r)
ProjScore(v_B, e, r)
ProjScore(v_AB_raw, e, r)
ProjScore(v_AB_int, e, r)
```

建议重点报告：

```text
r = 1, 2, 4, 8
```

## Interpretation cases

### Case A: mixed AB expert

```text
ProjScore(v_A, e_AB) high
ProjScore(v_B, e_AB) high
ProjScore(v_AB_int, e_AB) high or moderate
```

解释：

```text
AB expert 同时承载 A/B/AB 信息。
这支持 feature-entangled expert hypothesis。
```

### Case B: clean AB-interaction expert

```text
ProjScore(v_A, e_AB) low
ProjScore(v_B, e_AB) low
ProjScore(v_AB_int, e_AB) high
```

解释：

```text
AB expert 更像 composite-feature specialist。
```

### Case C: raw AB high, interaction AB low

```text
ProjScore(v_AB_raw, e_AB) high
ProjScore(v_AB_int, e_AB) low
ProjScore(v_A, e_AB) high
ProjScore(v_B, e_AB) high
```

解释：

```text
这个 expert 可能只是包含 A+B，并没有学到真正 AB interaction。
不能 claim 它是 AB composite specialist。
```

## Deliverables

```text
tables/ab_expert_deep_dive.csv
figures/ab_expert_projection_curve.png
figures/ab_expert_routing_composition.png
```

---

# Experiment 6: Random / Permutation Baselines

## Purpose

避免把普通高维几何重合误判成 expert specialization。

## Mainline Relation

我们需要知道 expert subspace 的 projection score 是否真的比随机 bucket 更有结构。  
如果 random bucket 也有类似 projection score，那么 expert bucket 没有特殊 indexing value。

## Baseline 1: random matched bucket

对每个 expert `e`，随机抽取相同数量的 hidden states，构造：

```text
H_random_e
```

做同样 SVD 和 projection。

比较：

```text
ProjScore_expert - ProjScore_random_matched
```

## Baseline 2: label permutation

随机打乱 class label，重新计算：

```text
v_A_perm
v_B_perm
v_AB_int_perm
```

检查真实 feature direction 的 projection 是否显著高于 permuted direction。

## Baseline 3: global subspace

见 Experiment 4。

## Deliverables

```text
tables/random_baseline_projection_scores.csv
figures/expert_vs_random_projection.png
figures/true_vs_permuted_feature_projection.png
```

---

# Experiment 7: Expert Mask / Causal Ablation

## Purpose

SVD 是相关性诊断。  
为了判断某个 expert 是否功能上承载 A/B/AB，需要做 expert intervention。

## Mainline Relation

能作为 KV index 的 bucket 不只要 representation coherent，也应该 functionally relevant。  
如果 AB expert 表示上混合，功能上也同时影响 A/B/AB，那么它不是干净 index。

## Procedure

对 candidate experts：

```text
e_A
e_B
e_AB_route
e_AB_pure
```

做 expert output mask：

```text
正常 forward:
  y = model(x)

ablation forward:
  将 expert e 的输出置零，其他保持不变
```

不要重新 routing。  
第一版建议：

```text
mask after routing, before residual add
```

这样诊断的是“该 expert 当前承担了什么功能”。

## Metrics

按 class 统计：

```text
DeltaLoss_C0 = Loss_masked_C0 - Loss_normal_C0
DeltaLoss_CA = Loss_masked_CA - Loss_normal_CA
DeltaLoss_CB = Loss_masked_CB - Loss_normal_CB
DeltaLoss_CAB = Loss_masked_CAB - Loss_normal_CAB
```

也可以统计：

```text
DeltaAccuracy by class
```

## Interpretation

### If mask AB expert mainly hurts CAB

```text
DeltaLoss_CAB high
DeltaLoss_CA low
DeltaLoss_CB low
DeltaLoss_C0 low
```

解释：

```text
AB expert functionally specialized.
```

### If mask AB expert hurts CA, CB, CAB together

```text
DeltaLoss_CA high
DeltaLoss_CB high
DeltaLoss_CAB high
```

解释：

```text
AB expert functionally mixed.
```

### If mask AB expert barely hurts anything

解释：

```text
该 expert 可能不是 functional bottleneck；
routing/SVD 结构不一定参与最终预测。
```

## Deliverables

```text
tables/expert_ablation_delta_loss.csv
figures/expert_ablation_delta_loss_heatmap.png
```

---

# Experiment 8: Optional Top-k / Soft Routing Comparison

## Purpose

只有在当前模型或代码支持 top-k / soft routing 时才做。  
这不是第一优先级。

## Mainline Relation

如果 top-1 expert 是 mixed bucket，那么 top-k / soft routing 是后续可能的 architecture direction。  
但本轮不能把它当作已经证明有效的方法。

## Suggested comparison

如果已有 top-k checkpoint：

```text
Top-1 trained model
Top-3 trained model
Soft routing trained model
```

比较同样的：

```text
routing heatmap
expert purity
SVD projection
expert ablation
```

## Do Not Claim

不能 claim：

```text
Top-k 一定解决 feature mixing。
```

只能 claim：

```text
在当前 synthetic setup 下，top-k 是否比 top-1 更接近 feature-level decomposition。
```

---

# Experiment 9: Gated Retrieval Alignment

## Purpose

只有当前面分析显示 expert bucket 确实有 feature-level structure，才进入 retrieval alignment。

## Mainline Relation

这是回到主线的步骤：

> expert bucket 是否能帮助 retrieve dense attention winners？

## Gating condition

满足以下条件再做：

```text
routing heatmap shows class-expert structure
AB expert has clear v_AB_int projection
expert mask shows class-specific functional role
```

## Retrieval metrics

如果进入这一步，测试：

```text
Recall@K of dense attention top-M
attention mass covered
output reconstruction error under sparse attention over expert bucket
matched-random baseline
```

如果前面显示 expert bucket 是 mixed，就不要急着做 retrieval claim。

---

## Pass / Fail Criteria

### Strong evidence for feature mixing

满足多数条件：

```text
AB-dominant expert also receives A-only / B-only samples
ProjScore(v_A, e_AB) high
ProjScore(v_B, e_AB) high
ProjScore(v_AB_int, e_AB) not uniquely dominant
Mask e_AB hurts A-only / B-only / AB together
Expert projection not significantly better than random matched bucket
```

Claim:

```text
In this controlled seq_len=32 setup, ordinary MoE expert buckets are mixed token/context buckets rather than clean feature-level specialists.
```

### Strong evidence for feature specialization

满足多数条件：

```text
AB-composite routes to stable AB expert
P(CAB | e_AB) high
ProjScore(v_AB_int, e_AB) high
ProjScore(v_A, e_AB) low
ProjScore(v_B, e_AB) low
Mask e_AB mainly hurts AB-composite
Expert projection beats random matched bucket
```

Claim:

```text
In this controlled seq_len=32 setup, ordinary MoE can form a composite-feature specialist.
```

### Inconclusive

以下情况都应标为 inconclusive：

```text
model task performance poor
expert counts too small
v_AB_int norm too small
routing differs wildly across seeds
SVD projection similar to random baseline
ablation does not change loss
```

---

## Required Outputs for Agent

请 Agent 最终产出一个目录：

```text
outputs/E0521_svd_feature_mixing_seq32/
```

目录结构：

```text
outputs/E0521_svd_feature_mixing_seq32/
  config.yaml
  tables/
    eval_data_summary.csv
    per_class_performance.csv
    routing_stats.csv
    feature_direction_norms.csv
    svd_projection_scores.csv
    random_baseline_projection_scores.csv
    ab_expert_deep_dive.csv
    expert_ablation_delta_loss.csv
  figures/
    per_class_loss_bar.png
    per_class_accuracy_bar.png
    routing_heatmap_P_expert_given_class.png
    expert_composition_P_class_given_expert.png
    expert_purity_bar.png
    routing_entropy_by_class.png
    proj_scores_by_expert_r4.png
    proj_score_curves_for_AB_expert.png
    singular_value_spectrum_by_expert.png
    expert_vs_random_projection.png
    expert_ablation_delta_loss_heatmap.png
  artifacts/
    hidden_states_layer*.pt
    routing_records_layer*.pt
    feature_directions_layer*_pos*.pt
    svd_components_layer*_expert*.pt
  report.md
```

---

## Suggested Script Interface

建议新建脚本：

```text
scripts/analyze_feature_mixing_svd.py
```

命令行接口：

```bash
python scripts/analyze_feature_mixing_svd.py \
  --checkpoint_path <PATH_TO_TRAINED_CHECKPOINT> \
  --config_path <PATH_TO_MODEL_CONFIG> \
  --seq_len 32 \
  --n_eval_per_class 4096 \
  --position prediction \
  --layers all_moe \
  --ranks 1,2,4,8,16 \
  --min_count_per_expert 128 \
  --output_dir outputs/E0521_svd_feature_mixing_seq32
```

---

## Pseudocode

```python
# 1. load model
model = load_model(checkpoint_path, config_path)
model.eval()

# 2. build balanced eval set
eval_data = build_eval_set(
    seq_len=32,
    n_per_class=n_eval_per_class,
    classes=["C0", "CA", "CB", "CAB"],
    protocol="fixed_position",
)

# 3. forward with hooks
records = collect_records(
    model=model,
    data=eval_data,
    hook_tensor="router_input",
    position="prediction",
    layers="all_moe",
    save_router_logits=True,
    save_expert_id=True,
    save_loss=True,
)

# 4. per-class performance
compute_per_class_loss_accuracy(records)

# 5. routing diagnostic
compute_P_expert_given_class(records)
compute_P_class_given_expert(records)
compute_purity_entropy_nmi(records)

# 6. feature directions
for layer in moe_layers:
    H0  = hidden(records, class="C0",  layer=layer)
    HA  = hidden(records, class="CA",  layer=layer)
    HB  = hidden(records, class="CB",  layer=layer)
    HAB = hidden(records, class="CAB", layer=layer)

    mu0, muA, muB, muAB = mean(H0), mean(HA), mean(HB), mean(HAB)

    vA = muA - mu0
    vB = muB - mu0
    vAB_raw = muAB - mu0
    vAB_int = muAB - muA - muB + mu0

# 7. expert SVD + projection
for layer in moe_layers:
    for expert in experts:
        He = hidden_assigned_to_expert(records, layer, expert)
        if len(He) < min_count_per_expert:
            continue

        He_centered = He - He.mean(dim=0)
        U, S, Vh = torch.linalg.svd(He_centered, full_matrices=False)

        for r in ranks:
            V = Vh[:r].T  # d x r
            for name, v in feature_dirs.items():
                score = projection_score(v, V)
                save_score(layer, expert, r, name, score)

# 8. random baseline
compute_random_matched_bucket_projection(records)

# 9. expert ablation
for expert in candidate_experts:
    masked_metrics = run_expert_mask_ablation(model, eval_data, expert)
    save_delta_loss(masked_metrics)
```

Projection score implementation:

```python
def projection_score(v, V):
    # v: [d]
    # V: [d, r], orthonormal columns
    v = v / (v.norm() + 1e-8)
    proj = V @ (V.T @ v)
    return (proj.norm() ** 2).item()
```

---

## Report Template

Agent 最后写 `report.md`，使用以下结构：

```markdown
# SVD Feature-Mixing Diagnostic Report

## Conclusion

## Setup
- checkpoint:
- seq_len:
- model:
- MoE layer(s):
- number of experts:
- eval protocol:
- n_eval_per_class:

## Most Important Metric

## Result 1: Task Performance Sanity

## Result 2: Routing Distribution

## Result 3: Feature Direction Norms

## Result 4: Expert SVD Projection

## Result 5: AB-Dominant Expert Deep Dive

## Result 6: Random / Permutation Baselines

## Result 7: Expert Mask Ablation

## Interpretation

## Claim Update

## What Cannot Be Claimed

## Next Decision
```

---

## Most Important Metric

本轮最重要的 metric 不是单一 accuracy，而是：

```text
AB-dominant expert 的 v_A / v_B / v_AB_int projection pattern
+
mask AB expert 后 per-class DeltaLoss pattern
```

原因：

```text
routing heatmap 只能说明样本被分到哪里；
SVD projection 说明 expert 表示空间里有什么；
expert mask 说明该 expert 功能上影响什么。
```

三者结合，才足以判断 expert 是 feature-specialized 还是 mixed。

---

## Claim Boundary

本实验可以 claim：

```text
在 controlled seq_len=32 synthetic setup 下，已训练 MoE 的 expert bucket 是否表现出 feature-level specialization / feature mixing。
```

不能 claim：

```text
真实语言语义也是这样。
long-context retrieval 一定成功或失败。
top-k / soft routing 一定解决问题。
SVD 证明了模型理解语义。
expert subspace 包含某 feature 就等于模型一定使用该 feature。
```

---

## 30s Meeting Version

> 我现在已经完成了 seq_len=32 的训练。下一步我不先改模型，而是做 post-training diagnostic：收集每个 expert 接收的 router-input hidden states，对每个 expert 做 SVD，得到它的 dominant subspace。然后我构造 A、B、AB interaction 三个 feature directions，尤其 AB interaction 用 $\mu_{AB}-\mu_A-\mu_B+\mu_0$，避免把 A+B 误当成 AB。核心判断是 AB-dominant expert 的主子空间是否同时包含 A/B/AB，以及 mask 这个 expert 后是否同时伤害 A-only、B-only、AB。如果同时包含并同时伤害，说明当前 top-1 MoE 更像 mixed token-level bucket；如果主要只包含并影响 AB，才说明它可能形成了 composite-feature specialist。这个实验只诊断 seq_len=32 synthetic mechanism，不直接 claim 长上下文 retrieval。  

---

## Next Decision

根据结果做下一步决策：

### If mixed

```text
停止直接把 expert id 当 KV index。
转向 feature-level / multi-hot / soft/top-k routing 的设计，但必须先写清 failure evidence。
```

### If specialized

```text
继续测试 expert bucket 是否能 retrieve dense attention top-K KV。
```

### If inconclusive

```text
先修数据、样本数、hook tensor、训练质量或 feature direction 定义。
不要做主线 claim。
```

---

## Files To Update

建议更新：

```text
Projects/from-attention-to-search/XingyuD/main/experiments/E0521_ab_feature_specialization/purpose_card.md
Projects/from-attention-to-search/XingyuD/main/experiments/E0521_ab_feature_specialization/execution_plan.md
Projects/from-attention-to-search/XingyuD/main/experiments/E0521_ab_feature_specialization/svd_analysis_plan.md
daily_research_reports/0522/meeting/pre_meeting_pack.md
```
