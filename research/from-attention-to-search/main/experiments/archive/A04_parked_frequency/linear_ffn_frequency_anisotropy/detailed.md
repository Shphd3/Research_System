# Detailed Result: linear_ffn_frequency_anisotropy

Anchor: [03_hierarchical_route_utility_binding_anchor.md](../../../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md)

Story: 用导师建议的 linear FFN/KV toy 检验 frequency dominance 是否是 gating failure 的更小上游机制。

## 0. Quick Recap

目的：

先不跑 slot、hierarchy、common-residual，检查最小线性模型中频率是否足以造成 head-feature dominance 和矩阵 anisotropy。

假设：

在组合 feature 里，Zipf 频率会让 $W$ 优先学习高频 feature，tail feature error 更高，singular spectrum 更尖；inverse-frequency reweight 应该削弱这些现象。

实验思路：

每条样本都有 common feature $c$，再采一个 unique feature $u_i$：

$$
x=k_c+k_{u_i}+\epsilon,\qquad y=v_c+v_{u_i}.
$$

模型：

$$
\hat y=xW.
$$

结论：

支持 frequency-induced head-feature anisotropy；不支持在这个 toy 中把 top direction 解释成 Zipf 下的 common feature dominance。

证据：

`zipf_normal` 在 step 1000 的 top energy ratio 是 0.0316，effective rank 是 108.6，tail/head full MSE 是 32.32；`uniform_normal` 与 `zipf_reweight` 的 tail/head ratio 都约 1.0，effective rank 约 142。

## 1. Data Construction

Parameters:

```text
num_unique_features = 256
d_model = 256
zipf_alpha = 1.15
noise_std = 0.03
head_fraction = 0.1
tail_fraction = 0.1
seeds = 20260528, 20260529, 20260530, 20260531, 20260601
```

Feature construction:

```text
common key/value: random unit vectors
unique keys/values: random unit vectors projected away from common direction
```

This projection makes the common direction auditable: if top singular vector aligns with common, it is not caused by trivial random overlap.

Conditions:

| Condition | Sampling | Loss |
| --- | --- | --- |
| `uniform_normal` | uniform over 256 unique features | MSE mean |
| `zipf_normal` | $P(u_i)\propto i^{-1.15}$ | MSE mean under sampled distribution |
| `zipf_reweight` | same Zipf sampling | normalized inverse-frequency weighted MSE |

Reweight loss:

$$
\mathcal L = \frac{\sum_b w_i \operatorname{MSE}_b}{\sum_b w_i},\qquad w_i=\frac{1}{N P(u_i)}.
$$

## 2. Model / Training / Evaluation Setup

Model:

```text
single matrix W, y_hat = x @ W
init_std = 0.02
optimizer = AdamW
lr = 1e-3
weight_decay = 1e-3
batch_size = 512
steps = 5000
```

Trajectory checkpoints:

```text
0, 100, 300, 1000, 3000, 5000
```

SVD convention:

```python
U, S, Vh = torch.linalg.svd(W)
input/key side = U[:, 0]
output/value side = Vh.T[:, 0]
```

This implements the corrected convention for the experiment and is written into `metadata.json`.

SVD side audit:

```text
runner line: scripts/run_linear_ffn_frequency_anisotropy.py:123
actual forward: return x @ self.W
not used: nn.Linear, F.linear, x @ W.T
```

Therefore the experiment is case A:

$$
W = U\Sigma V^T,\qquad \hat y=xW=xU\Sigma V^T.
$$

So the input/key-side coordinate is $xU$ and the first input direction is `U[:,0]`; the output/value-side direction is `Vh.T[:,0]`.

Perturbation sanity check:

```text
forward=x@W
u0@W projects_to_v0 = 5.493153
expected s0 = 5.493154
v0@W projects_to_v0 = 2.941116
input_side_is_U = True
```

This confirms that using `U[:,0]` for input/key-side alignment is correct for this runner. If the code were changed to `x @ W.T` or PyTorch `F.linear(x, weight)`, the input side would switch to `Vh.T[:,0]` and the report would need to be recomputed.

## 3. Job And Repro Map

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Runner:

```text
scripts/run_linear_ffn_frequency_anisotropy.py
scripts/submit_linear_ffn_frequency_anisotropy_4gpu_acp.sh
```

Config:

```text
configs/linear_ffn_frequency_anisotropy.json
```

ACP full run:

```text
job id: pt-98tw742y
display name: ats-linear-ffn-freq-4gpu
state: SUCCEEDED
run name: linear_ffn_frequency_anisotropy_cluster_full_20260528
```

Repro command:

```bash
LINEAR_FFN_FREQ_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=linear_ffn_frequency_anisotropy_cluster_full_20260528 \
scripts/submit_linear_ffn_frequency_anisotropy_4gpu_acp.sh
```

Raw result dir:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/linear_ffn_frequency_anisotropy/linear_ffn_frequency_anisotropy_cluster_full_20260528
```

Raw figure dir:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/linear_ffn_frequency_anisotropy/linear_ffn_frequency_anisotropy_cluster_full_20260528
```

Curated files:

```text
figures/trajectory_core_metrics.png
figures/tail_head_error_by_seed.png
figures/top_energy_by_seed.png
figures/singular_spectrum_selected_steps.png
figures/feature_error_by_rank_step1000.png
tables/summary_by_condition_step.csv
tables/metrics_by_step.csv
```

## 4. Main Metrics

Primary metric:

```text
top_energy_ratio and effective_rank
```

It answers whether $W$ forms a dominant direction.

Validity metric:

```text
tail_head_full_mse_ratio
```

It answers whether the learned map is biased toward head features rather than merely having a different spectrum.

Interpretation metric:

```text
top singular vector alignment with common/head/tail key-value directions
```

It answers what the dominant direction corresponds to.

## 5. Results

| Step | Condition | Top Energy | Effective Rank | Tail/Head Full MSE | Common Key Align | Head Key Align | Common Value Align | Head Value Align |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | uniform_normal | 0.0247 | 141.3 | 1.00 | 0.850 | 0.020 | 0.965 | 0.016 |
| 100 | zipf_normal | 0.0380 | 111.1 | 8.04 | 0.049 | 0.100 | 0.056 | 0.156 |
| 100 | zipf_reweight | 0.0315 | 143.3 | 1.03 | 0.858 | 0.020 | 0.975 | 0.013 |
| 300 | uniform_normal | 0.0178 | 142.1 | 1.00 | 0.025 | 0.042 | 0.036 | 0.081 |
| 300 | zipf_normal | 0.0336 | 106.4 | 25.68 | 0.018 | 0.108 | 0.017 | 0.178 |
| 300 | zipf_reweight | 0.0178 | 142.1 | 1.04 | 0.039 | 0.047 | 0.049 | 0.084 |
| 1000 | uniform_normal | 0.0174 | 142.9 | 1.04 | 0.007 | 0.036 | 0.005 | 0.092 |
| 1000 | zipf_normal | 0.0316 | 108.6 | 32.32 | 0.013 | 0.099 | 0.008 | 0.177 |
| 1000 | zipf_reweight | 0.0174 | 142.5 | 1.05 | 0.008 | 0.035 | 0.008 | 0.085 |
| 5000 | uniform_normal | 0.0175 | 142.9 | 1.02 | 0.005 | 0.036 | 0.003 | 0.094 |
| 5000 | zipf_normal | 0.0314 | 108.9 | 33.12 | 0.015 | 0.095 | 0.008 | 0.171 |
| 5000 | zipf_reweight | 0.0174 | 142.6 | 1.06 | 0.005 | 0.036 | 0.004 | 0.093 |

## 6. Figures And Interpretation

![Core trajectory](figures/trajectory_core_metrics.png)

Observation: `zipf_normal` keeps higher top energy, lower effective rank, and much larger tail/head error through training.

Interpretation: frequency imbalance changes the learned matrix geometry and the feature-wise learning order.

![Tail/head by seed](figures/tail_head_error_by_seed.png)

Observation: every seed shows the same qualitative pattern: `zipf_normal` separates head from tail; `uniform_normal` and `zipf_reweight` stay near 1.

Interpretation: the result is stable across seeds.

![Top energy by seed](figures/top_energy_by_seed.png)

Observation: `zipf_normal` has consistently larger top-energy trajectory after early training.

Interpretation: the anisotropy effect is not only a mean artifact.

![Singular spectrum](figures/singular_spectrum_selected_steps.png)

Observation: `zipf_normal` has a visibly sharper singular spectrum at selected steps.

Interpretation: Zipf training produces a lower-dimensional dominant map than uniform or reweighted training.

![Feature error by rank](figures/feature_error_by_rank_step1000.png)

Observation: at step 1000, `zipf_normal` error is lowest on head ranks and much higher on tail ranks.

Interpretation: the model solves high-frequency unique features first and leaves tail features underfit.

## 7. Interpretation

The result supports the reduced mechanism:

```text
frequency imbalance -> head unique feature learned first -> W spectrum sharpens -> tail remains underfit
```

The result does not cleanly support this stronger version:

```text
frequency imbalance -> common feature becomes the top singular direction
```

Common feature appears strongly in early uniform/reweight step 100, likely because it is shared and easy to learn under balanced objectives. But in Zipf-normal, the top direction aligns more with head unique value/key directions than with the common direction.

## 8. Claim Boundary

This experiment supports a frequency/head-dominance mechanism, not H-MoE.

It says the next router story should distinguish:

```text
common component dominance
head-frequency unique component dominance
B/token identity dominance
slot/target feature dominance
```

It does not prove which component dominates a trained Transformer hidden state.

## 9. Next Decision

Before more hierarchy runs, do a router-factor attribution or representation diagnostic where common direction, head-frequency direction, and target/slot direction are explicitly separable. Only then decide whether common-residual, reweighting, or hierarchy is the right intervention.
