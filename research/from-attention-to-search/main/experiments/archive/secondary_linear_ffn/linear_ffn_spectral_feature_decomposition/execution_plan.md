# Execution Plan: linear_ffn_spectral_feature_decomposition

Anchor: [03_hierarchical_route_utility_binding_anchor.md](../../../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md)

## 1. Run Goal

不改模型，不重新定义训练任务，只对 trained linear FFN 矩阵 $W$ 做 post-hoc decomposition，判断 tail failure 到底是：

```text
A. tail feature 被写进 W，但被 top/high-frequency/common directions 干扰；
B. tail feature 本身没有被充分写进 W。
```

这个实验不能只看 top-1 singular direction，必须看 top-r subspace、spectral truncation 和 oracle feature projection。

## 2. Required Input

严格输入是已有 trained $W$ checkpoint：

```text
checkpoints/<condition>_seed<seed>_step5000.pt
```

每个 checkpoint 至少包含：

```text
W
condition
seed
step
forward_convention
```

当前 audit 结果：

```text
已有正式 run 只有 CSV/figures，没有保存 W checkpoint。
因此不能从现有 artifact 严格完成 spectral truncation / P_key W P_value。
```

已补齐未来保存路径：

```text
configs/linear_ffn_frequency_anisotropy.json
checkpoint.save_eval_weights = true
checkpoint.save_steps = [5000]
```

## 3. Analysis Items

### 3.1 SVD Side Audit

确认 runner convention：

```text
case A: y = x @ W
input/key side = U
output/value side = Vh.T

case B: y = x @ W.T or F.linear(x, weight)
input/key side = Vh.T
output/value side = U
```

当前 runner:

```text
LinearFFN.forward(): return x @ self.W
```

因此本实验使用 case A。

### 3.2 Top-r Subspace Coverage

Ranks:

```text
r = 1, 2, 4, 8, 16, 32, 64, 128
```

Input side:

$$
P_{\mathrm{in}}(r)=U_rU_r^T.
$$

For feature keys $K_A$:

$$
\mathrm{coverage\_key}(A,r)=\mathbb E_{k_i\in A}\|P_{\mathrm{in}}(r)k_i\|^2.
$$

Output side:

$$
P_{\mathrm{out}}(r)=V_rV_r^T.
$$

For feature values $V_A$:

$$
\mathrm{coverage\_value}(A,r)=\mathbb E_{v_i\in A}\|P_{\mathrm{out}}(r)v_i\|^2.
$$

Weighted version:

$$
\mathrm{weighted\_key\_energy}(A,r)=
\mathbb E_{k_i\in A}\sum_{j\le r}s_j^2\langle k_i,u_j\rangle^2.
$$

$$
\mathrm{weighted\_value\_energy}(A,r)=
\mathbb E_{v_i\in A}\sum_{j\le r}s_j^2\langle v_i,v_j^{SVD}\rangle^2.
$$

### 3.3 Spectral Truncation Test

For each $r$:

$$
W_{\mathrm{top}}(r)=\sum_{j\le r}s_ju_jv_j^T,
$$

$$
W_{\mathrm{low}}(r)=\sum_{j>r}s_ju_jv_j^T.
$$

Evaluate head/middle/tail error under:

```text
full W
W_top(r)
W_low(r) = W - W_top(r)
```

Decision rule:

```text
If W_low / remove_top significantly lowers tail error:
  high-frequency/common top subspace is interfering with tail prediction.

If W_low does not lower tail error:
  tail failure is more likely that tail feature was not written into W.
```

### 3.4 Oracle Feature Projection Test

Build group subspace projectors:

$$
P_{\mathrm{head,key}},P_{\mathrm{middle,key}},P_{\mathrm{tail,key}}
$$

and:

$$
P_{\mathrm{head,value}},P_{\mathrm{middle,value}},P_{\mathrm{tail,value}}.
$$

Measure:

$$
P_{A,\mathrm{key}} W P_{B,\mathrm{value}}.
$$

Primary table:

```text
component_fro_sq_ratio(A_key, B_value)
unique_mse_to_own_value(A)
```

Decision rule:

```text
If P_tail_key W P_tail_value is weak:
  tail component was not written into W.

If P_tail_key W P_tail_value is strong but full tail error is high:
  tail information exists but is interfered with by other spectral/value components.
```

## 4. Code

Analyzer:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/analyze_linear_ffn_spectral_feature_decomposition.py
```

Command:

```bash
python scripts/analyze_linear_ffn_spectral_feature_decomposition.py \
  --config configs/linear_ffn_frequency_anisotropy.json \
  --checkpoint-root results/linear_ffn_frequency_anisotropy/<run_name>/checkpoints \
  --run-name linear_ffn_spectral_feature_decomposition_20260529
```

Smoke status:

```text
smoke checkpoint save: passed
smoke analyzer: passed
```

## 5. Current Blocker

The existing formal full runs do not contain trained $W$ checkpoints:

```text
linear_ffn_frequency_anisotropy_cluster_full_20260528
linear_ffn_frequency_anisotropy_subspace_full_20260529
```

Therefore strict post-hoc decomposition cannot be completed on the already-finished formal runs.

The next operational decision is one of:

```text
1. provide an existing checkpoint root if trained W was saved elsewhere;
2. run a recovery full run with identical model/training and checkpoint saving enabled, then apply this analyzer.
```

## 6. Recovery Completion

Recovery full run completed:

```text
job id: pt-aehu8m75
display name: ats-linear-ffn-ckpt-4gpu
state: SUCCEEDED
run name: linear_ffn_frequency_anisotropy_checkpoint_full_20260529
checkpoints: 15
```

Post-hoc decomposition completed:

```text
run name: linear_ffn_spectral_feature_decomposition_20260529
raw result dir:
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/linear_ffn_spectral_feature_decomposition/linear_ffn_spectral_feature_decomposition_20260529
```

Result closure:

```text
summary.md
detailed.md
```
