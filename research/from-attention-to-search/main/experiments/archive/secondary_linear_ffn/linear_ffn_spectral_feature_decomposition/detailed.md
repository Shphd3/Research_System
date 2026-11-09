# Detailed Result: linear_ffn_spectral_feature_decomposition

Anchor: [03_hierarchical_route_utility_binding_anchor.md](../../../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md)

Story: post-hoc decomposition of trained linear FFN weights.

## 0. Quick Recap

目的：

不用新模型，直接分析 trained $W$，判断 Zipf tail failure 的机制。

问题：

```text
tail feature 是已经写入 W 但被 top/high-frequency directions 干扰，
还是 tail feature 本身没有充分写入 W？
```

结论：

更支持后者。`P_tail_key W P_tail_value` 弱，`W_low/remove_top` 对 tail error 没有显著改善。

## 1. Input And Recovery Run

原正式 run 没有保存 trained $W$，因此不能严格 post-hoc。已做 recovery full run，只增加 checkpoint 保存，不改模型/数据/训练目标。

Recovery run:

```text
job id: pt-aehu8m75
display name: ats-linear-ffn-ckpt-4gpu
state: SUCCEEDED
run name: linear_ffn_frequency_anisotropy_checkpoint_full_20260529
checkpoints: 15 = 3 conditions x 5 seeds
```

Checkpoint root:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/linear_ffn_frequency_anisotropy/linear_ffn_frequency_anisotropy_checkpoint_full_20260529/checkpoints
```

Post-hoc command:

```bash
python scripts/analyze_linear_ffn_spectral_feature_decomposition.py \
  --config configs/linear_ffn_frequency_anisotropy.json \
  --checkpoint-root results/linear_ffn_frequency_anisotropy/linear_ffn_frequency_anisotropy_checkpoint_full_20260529/checkpoints \
  --run-name linear_ffn_spectral_feature_decomposition_20260529
```

Raw result:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/linear_ffn_spectral_feature_decomposition/linear_ffn_spectral_feature_decomposition_20260529
```

## 2. SVD Side Audit

Runner convention:

```text
LinearFFN.forward(): return x @ self.W
```

Therefore:

$$
W=U\Sigma V^T,\qquad xW=xU\Sigma V^T.
$$

Input/key side is $U$; output/value side is $V$.

Audit result:

```text
15/15 checkpoints: input_side_is_U = True
```

## 3. Top-r Coverage

Ranks:

```text
1, 2, 4, 8, 16, 32, 64, 128
```

Metrics:

$$
\mathrm{coverage\_key}(A,r)=\mathbb E_{k_i\in A}\|U_rU_r^Tk_i\|^2
$$

$$
\mathrm{coverage\_value}(A,r)=\mathbb E_{v_i\in A}\|V_rV_r^Tv_i\|^2
$$

and $\sigma_j^2$-weighted versions.

This analysis confirms the previous subspace result: Zipf-normal allocates top-r energy to common/head before tail.

## 4. Spectral Truncation Test

Definitions:

$$
W_{\mathrm{top}}(r)=\sum_{j\le r}s_ju_jv_j^T,
$$

$$
W_{\mathrm{low}}(r)=W-W_{\mathrm{top}}(r).
$$

Zipf-normal tail unique MSE:

| r | full W | W_top(r) | W_low(r) |
| ---: | ---: | ---: | ---: |
| 1 | 0.00318 | 0.00391 | 0.00318 |
| 2 | 0.00318 | 0.00393 | 0.00316 |
| 4 | 0.00318 | 0.00394 | 0.00315 |
| 8 | 0.00318 | 0.00397 | 0.00312 |
| 16 | 0.00318 | 0.00401 | 0.00308 |
| 32 | 0.00318 | 0.00402 | 0.00307 |
| 64 | 0.00318 | 0.00390 | 0.00319 |
| 128 | 0.00318 | 0.00348 | 0.00361 |

Interpretation:

`W_low` slightly helps tail at r=8/16/32, but the improvement is small. This is not strong evidence for “top directions are the main tail interference.” If that were the main mechanism, removing top subspace should reduce tail error substantially.

## 5. Oracle Feature Projection Test

For group projectors:

$$
P_{A,key}WP_{B,value}
$$

Main result:

| Condition | Head->Head Fro Ratio | Middle->Middle Fro Ratio | Tail->Tail Fro Ratio |
| --- | ---: | ---: | ---: |
| uniform_normal | 0.0677 | 0.8182 | 0.0666 |
| zipf_normal | **0.2869** | 0.7889 | **0.0219** |
| zipf_reweight | 0.0676 | 0.8183 | 0.0661 |

Own projection unique MSE:

| Condition | Head | Middle | Tail |
| --- | ---: | ---: | ---: |
| uniform_normal | 0.00063 | 0.00092 | 0.00064 |
| zipf_normal | **0.00010** | 0.00193 | **0.00254** |
| zipf_reweight | 0.00062 | 0.00093 | 0.00066 |

Interpretation:

Zipf-normal writes head strongly and tail weakly. Reweight restores tail-tail strength and tail own reconstruction quality.

## 6. Figures

![Zipf truncation](figures/spectral_truncation_error_zipf_normal.png)

Zipf tail error is not substantially repaired by removing top-r directions.

![Zipf projection](figures/oracle_projection_energy_zipf_normal.png)

Zipf head->head component is strong; tail->tail component is weak.

![Uniform projection](figures/oracle_projection_energy_uniform_normal.png)

Uniform baseline has balanced head/tail own components.

![Reweight projection](figures/oracle_projection_energy_zipf_reweight.png)

Reweight restores the tail component.

## 7. Claim Boundary

This experiment says:

```text
In the linear FFN toy, Zipf tail failure is mainly tail write-in failure.
```

It does not say:

```text
Transformer router failures are fully explained by this.
```

Next router-facing implication:

```text
When returning to MoE, test whether tail/rare features are written into expert functions at all before blaming route-time interference.
```
