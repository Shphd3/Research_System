# Detailed Report: H0527a Router Initialization Trajectory

## 1. 目的

H0527a 测试一个具体因果问题：

```text
H0526 的 unstable functional specialization 是否主要由 random router initialization 导致？
```

实验比较：

| Condition | Router init | 作用 |
|---|---|---|
| random_init | 默认随机初始化 | H0526-aligned baseline |
| semantic_context_init | B-context whitened-centroid prototype init | 语义初始化干预 |

## 2. 实验设置

Dataset:

```text
A-only, B-only, AB-composite, CB-composite, background
```

Model:

```text
top1_selected_gate
experts: 4
load_balance: none
top-2: disabled
z-loss: disabled
```

Training:

```text
steps: 1600
batch size: 384
lr: 0.0008
weight decay: 0.01
seeds: 20260521, 20260522, 20260523, 20260524
SCO job: pt-rc74x1rq
GPU: 4 x H100 via n6ls.iu.i40.4
```

Semantic init construction:

```text
1. Collect untrained router-input hidden states.
2. Estimate B-source context centroids for B_in_B_only, B_in_AB, B_in_CB.
3. Whiten centroid directions using pooled covariance.
4. Initialize three router rows from whitened centroid directions; reserve the fourth expert with a negative unused bias.
```

This is a stronger version of centroid initialization than raw centroids because raw centroids only gave a tiny NMI increase in smoke audit.

Implementation details:

```text
code: XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0527a_router_initialization_trajectory.py
function: apply_semantic_context_init
config: XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0527a_router_initialization_trajectory.json
```

The semantic init is **not** simply `router.weight[e] = raw semantic centroid`. It is a whitened discriminative-direction initialization:

1. Build a calibration dataset with `calibration_samples_per_class = 1200`.
2. Run the untrained model and collect `info["ffn_input"]`, the hidden state immediately before the MoE router.
3. Keep only B-source motif tokens whose source roles are:

```text
B_in_B_only
B_in_AB
B_in_CB
```

4. For each role \(k\), compute its centroid:

\[
m_k=\mathbb{E}[h\mid \kappa=k].
\]

5. Pool all three role samples and compute a global mean:

\[
\bar m=\mathbb{E}[h].
\]

6. Center each centroid:

\[
\tilde m_k=m_k-\bar m.
\]

7. Estimate pooled covariance with ridge regularization:

\[
\Sigma
=
\frac{1}{N-1}
\sum_i
(h_i-\bar m)(h_i-\bar m)^\top
+\lambda I,
\quad
\lambda=0.001.
\]

8. Convert each centered centroid into a whitened direction:

\[
d_k=\Sigma^{-1}\tilde m_k.
\]

9. Normalize the direction:

\[
u_k=\frac{d_k}{\|d_k\|_2}.
\]

10. Initialize the first three router rows as scaled directions:

\[
W_{r,k}=8.0\,u_k.
\]

11. Center the corresponding router bias around the pooled mean:

\[
b_{r,k}=-W_{r,k}^\top \bar m.
\]

12. The fourth expert is not assigned a semantic B-context role. Its weight row stays zero after the router reset, and its bias is set to:

\[
b_{r,3}=-8.0.
\]

Therefore the implemented intervention is better described as:

```text
Use B-context hidden centroids to construct whitened semantic discrimination directions, then initialize router rows to those directions.
```

It is not:

```text
Use raw semantic centers directly as router row vectors.
```

Audit implication:

```text
If step-0 B-context NMI does not increase over random init, this construction should not be interpreted as semantic initialization.
```

## 3. Validity Audit

Required condition:

```text
router gradient > 0
router parameter delta > 0
active experts per token = 1
no full soft mixture
semantic init step-0 B-context NMI > random init
```

Audit result:

| Condition | Router weight grad | Router bias grad | Router weight delta | Step-0 B-context NMI | Pass |
|---|---:|---:|---:|---:|---:|
| random_init | 0.043502 | 0.003369 | 0.018101 | 0.0045 | 1 |
| semantic_context_init | 0.023592 | 0.000910 | 0.017244 | 0.3124 | 1 |

Interpretation:

```text
The semantic init condition is a valid sparse-router intervention. It has task-loss router gradients and changes initial B-context routing.
```

## 4. Primary Metric

Functional ablation:

\[
\Delta L_{c,e}=L_c(\text{ablate expert }e)-L_c(\text{full model})
\]

AB specificity:

\[
S_{AB}
=
\max_e
\left[
\Delta L_{AB,e}
-
\max
\left(
\Delta L_{A,e},
\Delta L_{B,e},
\Delta L_{CB,e}
\right)
\right].
\]

Final \(S_{AB}\):

| Condition | Seed | \(S_{AB}\) | Expert |
|---|---:|---:|---:|
| random_init | 20260521 | -0.0002 | E3 |
| random_init | 20260522 | 0.0000 | E1 |
| random_init | 20260523 | 0.7449 | E2 |
| random_init | 20260524 | 0.0003 | E0 |
| semantic_context_init | 20260521 | 0.0000 | E3 |
| semantic_context_init | 20260522 | 0.0000 | E3 |
| semantic_context_init | 20260523 | 0.0000 | E3 |
| semantic_context_init | 20260524 | 0.2876 | E2 |

Interpretation:

```text
semantic init does not stabilize AB-specific functional specialization. It moves the one positive seed from random seed 20260523 to semantic seed 20260524 and lowers the mean margin.
```

## 5. Task Metrics

Mean final accuracy:

| Condition | A-only | B-only | AB-composite | CB-composite |
|---|---:|---:|---:|---:|
| random_init | 1.0000 | 0.9997 | 0.9992 | 0.9997 |
| semantic_context_init | 0.9998 | 1.0000 | 0.9998 | 1.0000 |

The task is learned in both conditions. Therefore low or unstable \(S_{AB}\) is not caused by basic task failure.

## 6. Routing Trajectory

Mean B-context routing NMI:

| Condition | Step 0 | Step 1600 |
|---|---:|---:|
| random_init | 0.0019 | 0.0437 |
| semantic_context_init | 0.2469 | 0.0468 |

Mean load entropy and selected probability at final step:

| Condition | Load entropy | Selected probability |
|---|---:|---:|
| random_init | 1.0940 | 0.6298 |
| semantic_context_init | 0.7770 | 0.9610 |

Interpretation:

```text
semantic init starts with more context-aware routing, but training erases most of that context alignment. It also creates more confident and lower-entropy routing, which may reflect path dependence or load concentration rather than functional specialization.
```

## 7. Route-Function Alignment

Final AB route-function alignment:

| Condition | Seed | Dominant routed expert | Routed CE delta | Max CE delta | Alignment |
|---|---:|---:|---:|---:|---:|
| random_init | 20260521 | E2 | 0.0009 | 0.0009 | 1.0000 |
| random_init | 20260522 | E3 | 0.0385 | 0.0385 | 1.0000 |
| random_init | 20260523 | E2 | 0.7782 | 0.7782 | 1.0000 |
| random_init | 20260524 | E0 | 0.0003 | 0.1338 | 0.0019 |
| semantic_context_init | 20260521 | E1 | 0.0646 | 0.0646 | 1.0000 |
| semantic_context_init | 20260522 | E0 | 0.0000 | 0.0469 | 0.0000 |
| semantic_context_init | 20260523 | E0 | 0.0252 | 0.0252 | 1.0000 |
| semantic_context_init | 20260524 | E2 | 0.5908 | 0.5908 | 1.0000 |

Alignment can be high even when max CE delta is tiny. Therefore alignment is not sufficient evidence of meaningful specialization; \(S_{AB}\) remains the primary metric.

## 8. Figures

![S_AB trajectory by init](figures/S_AB_trajectory_by_init.png)

这张图说明：semantic initialization 没有让 mean \(S_{AB}\) 稳定超过 random initialization。

![Context routing NMI trajectory by init](figures/context_routing_nmi_trajectory_by_init.png)

这张图说明：semantic initialization 的初始 B-context routing 优势在训练中衰减到接近 random init。

![Final B context routing heatmap](figures/init_vs_final_b_context_routing_heatmap.png)

这张图说明：final B-source routing 仍然强烈依赖 seed 和 init condition，不能单独作为功能证据。

![Class expert ablation delta by init](figures/class_expert_ablation_delta_by_init.png)

这张图说明：AB-specific functional expert 没有跨 seed 稳定出现。

![Router movement from init](figures/router_prototype_cosine_trajectory.png)

这张图说明：router 参数离开初始化状态，semantic prior 没有作为稳定边界保留。

## 9. Artifact / Repro Map

Runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0527a_router_initialization_trajectory.py
```

SCO submit wrapper:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_h0527a_router_initialization_4gpu_acp.sh
```

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0527a_router_initialization_trajectory.json
```

Result dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0527a_router_initialization_trajectory/h0527a_router_initialization_4gpu_20260524
```

Figure dir:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/h0527a_router_initialization_trajectory/h0527a_router_initialization_4gpu_20260524
```

SCO job:

```text
pt-rc74x1rq
```

Runtime log:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/h0527a_router_initialization_4gpu_20260524_runtime_20260524_161526.log
```

Repro command:

```bash
cd XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
H0527A_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=h0527a_router_initialization_4gpu_20260524 \
JOB_NAME=ats-h0527a-router-init-4gpu \
bash scripts/submit_h0527a_router_initialization_4gpu_acp.sh
```
