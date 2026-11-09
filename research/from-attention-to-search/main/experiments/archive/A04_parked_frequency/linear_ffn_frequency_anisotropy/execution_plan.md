# Execution Plan: linear_ffn_frequency_anisotropy

Anchor: [03_hierarchical_route_utility_binding_anchor.md](../../../../problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md)

## 1. Run Goal

这次不先证明 H-MoE 有效，而是先检验更小的机制：在组合 feature 里，频率不均衡是否会让线性 FFN 的矩阵 $W$ 优先形成 common / 高频方向，从而产生 anisotropy；如果做 inverse-frequency reweight，这种偏置是否下降。

## 2. Data Construction

每条样本只有一个 common feature 和一个 unique feature：

$$
x = k_c + k_{u_i} + \epsilon,\quad y = v_c + v_{u_i}
$$

其中 $c$ 每条样本都有，$u_i$ 从 $N=256$ 个 unique feature 中采样。

三组条件：

| Condition | Unique feature sampling | Loss |
| --- | --- | --- |
| `uniform_normal` | uniform | normal MSE |
| `zipf_normal` | Zipf, $P(u_i)\propto i^{-\alpha}$ | normal MSE |
| `zipf_reweight` | Zipf, $P(u_i)\propto i^{-\alpha}$ | inverse-frequency weighted MSE |

## 3. Model / Training / Evaluation Setup

模型是单层线性 FFN：

$$
\hat y = xW
$$

训练目标是 MSE。`zipf_reweight` 必须用 normalized weighted mean：

$$
\mathcal L=\frac{\sum_b w_i\operatorname{MSE}_b}{\sum_b w_i},\quad w_i=\frac{1}{N P(u_i)}
$$

训练 5000 steps，并保存 trajectory：`0, 100, 300, 1000, 3000, 5000`。重点看早中期，因为 noiseless 或训练足够久时三组最后都可能接近解出来。

## 4. Configs And Commands

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Config:

```text
configs/linear_ffn_frequency_anisotropy.json
```

Smoke:

```bash
python scripts/run_linear_ffn_frequency_anisotropy.py \
  --config configs/linear_ffn_frequency_anisotropy.json \
  --run-name smoke_linear_ffn_frequency_anisotropy \
  --stage smoke
```

Full:

```bash
python scripts/run_linear_ffn_frequency_anisotropy.py \
  --config configs/linear_ffn_frequency_anisotropy.json \
  --run-name linear_ffn_frequency_anisotropy_full_20260528 \
  --stage full
```

Formal 4-GPU ACP full run:

```bash
LINEAR_FFN_FREQ_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=linear_ffn_frequency_anisotropy_cluster_full_20260528 \
scripts/submit_linear_ffn_frequency_anisotropy_4gpu_acp.sh
```

Submitted job:

```text
job id: pt-98tw742y
display name: ats-linear-ffn-freq-4gpu
final state: SUCCEEDED
```

Subspace audit rerun:

```bash
LINEAR_FFN_FREQ_ALLOW_REAL_SUBMIT=1 \
RUN_NAME=linear_ffn_frequency_anisotropy_subspace_full_20260529 \
JOB_NAME=ats-linear-ffn-subspace-4gpu \
scripts/submit_linear_ffn_frequency_anisotropy_4gpu_acp.sh
```

```text
job id: pt-ssf0gyl5
added metrics:
  subspace_coverage_by_step.csv
  summary_subspace_coverage_by_step.csv
  common_singular_alignment_by_step.csv
  summary_common_singular_alignment_by_step.csv
added figures:
  subspace_coverage_key.png
  subspace_coverage_value.png
  subspace_weighted_energy_key.png
  subspace_weighted_energy_value.png
  common_singular_alignment_heatmap.png
  common_singular_alignment_sigma_weighted_heatmap.png
```

## 5. Metrics And Artifacts

Primary metric 是 trajectory 上的 spectrum anisotropy：

- `top_energy_ratio`: $s_1^2 / \sum_j s_j^2$，判断 $W$ 是否形成主方向。
- `effective_rank`: 判断谱是否更尖。
- SVD alignment：若 `U, S, Vh = torch.linalg.svd(W)`，则 input/key side 看 `U[:,0]`，output/value side 看 `Vh.T[:,0]`。
- `head_mse` / `tail_mse`: 判断频率是否让 head 先学好而 tail 被压住。

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Data sanity | uniform / zipf / weight 是否正确 | probability table, batch sample count | zipf head probability clearly larger; reweight uses normalized denominator | `metadata.json` | train |
| Smoke | code path 是否跑通 | 40-step tables and figures | all three conditions produce metrics and figures | smoke result dir | full |
| Full trajectory | 频率效应是否出现在早中期 | steps 100/300/1000 curves | zipf-normal vs uniform/reweight has distinguishable spectrum/error pattern | `metrics_by_step.csv`, figures | summary |

## 7. Pass / Fail Criteria

支持最小假设，如果：

- `zipf_normal` 在 100/300/1000 step 的 `top_energy_ratio` 更高或 `effective_rank` 更低；
- top singular vector 更对齐 common / head key-value directions；
- head error 明显低于 tail error；
- `zipf_reweight` 降低这些差异。

削弱最小假设，如果：

- uniform、zipf、reweight 三组在 spectrum、alignment、head/tail error trajectory 上几乎没有差异。

## 8. Failure Modes To Check

- SVD side 不能写反：input/key side = `U[:,0]`，output/value side = `Vh.T[:,0]`。
- 不能只看 final：必须看 trajectory。
- reweight loss 不能直接 `mean(weight * mse)`，必须做 normalized weighted mean。

## 9. Result Location

Curated result:

```text
Projects/from-attention-to-search/main/experiments/linear_ffn_frequency_anisotropy/
```

Raw result:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/linear_ffn_frequency_anisotropy/
```
