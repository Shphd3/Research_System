# Detailed Report: R1 E1/E2 Full-Prefix Router Retrieval

This report stores detailed analysis for the branch-local experiment codebase. The mainline-facing short report is:

```text
main/experiments/R1_synthetic_router_retrieval_0512/summary.md
```

## Scope

Current closure focuses on:

```text
E1 NTP training -> E2 block2 retrieval analysis
```

Variants:

```text
flat_lb_on
hmoe_lb_off
```

Evaluation:

```text
prefix_len >= 128
full-prefix candidate evaluation
random/local/oracle baselines use the same candidate_count as router top-K
```

## Key Figure Folder

```text
figures/R1_synthetic_router_retrieval_0512_nocap/
```

Key figures:

```text
e2_nocap_topk_recall_mass_l2_prefix_ge128.png
e2_nocap_candidate_ratio_prefix_ge128.png
e2_nocap_router_delta_vs_random_prefix_ge128.png
e2_rank_k_only_recall_mass_prefix_ge128.png
```

SAE figures:

```text
bucket_to_path_flat_vs_hmoe_shared_scale.png
sae_e1/flat_lb_on/bucket_to_path_heatmap.png
sae_e1/hmoe_lb_off/bucket_to_path_heatmap.png
sae_e1/flat_lb_on/sae_activation_matrix_tokens_x_top_features.png
sae_e1/hmoe_lb_off/sae_activation_matrix_tokens_x_top_features.png
sae_e1/*/sae_feature_mean_activation_top64.png
sae_e1/*/sae_feature_fire_rate_top64.png
```

Data distribution diagnostics:

```text
data_distribution_diagnostics/zipf_rank_frequency_atom_token_rule.png
data_distribution_diagnostics/hierarchical_label_distribution.png
data_distribution_diagnostics/hidden_state_spectral_decomposition.png
data_distribution_diagnostics/hidden_state_pca_outer_path.png
```

## Data Distribution Diagnostic

| Diagnostic | Value | Reading |
|---|---:|---|
| atom Zipf fit | alpha 0.70, R2 0.81 | latent feature activations are long-tailed but mixed by global/path/noise levels |
| NTP token Zipf fit | alpha 1.88, R2 0.74 | token labels are heavy-tailed with truncation |
| path entropy | 1.000 | paths are deliberately balanced |
| covariance effective rank | 43.9 / 64 | hidden states are broad-spectrum, not low-rank |
| top-32 PC variance | 0.833 | spectrum decays, but many dimensions matter |
| path between-trace ratio | 0.000065 | path hierarchy is weak in mean/PCA geometry |

Conclusion:

```text
The data is long-tail enough for a synthetic language-like NTP proxy, but the
hierarchy is not exposed as clean PCA-separated clusters. It is mostly present
in sparse atom co-activation metadata. This likely makes clean router-bucket
retrieval harder and explains why R1 only gives weak support.
```

## Parameter Balance

| Variant | Total params | Router params | Expert params | Active params/token proxy |
|---|---:|---:|---:|---:|
| MoE+LB | 155,856 | 1,040 | 67,072 | 92,976 |
| H-MoE | 156,116 | 1,300 | 67,072 | 93,236 |

The total-parameter mismatch is 260 parameters and the active-proxy mismatch is about 0.28%. This is within the planned matched-budget tolerance.

## Retrieval Result

| Variant | K | Candidate ratio | Router recall | Random recall | Local recall | Oracle mass | Router mass | Random mass | Router L2 | Random L2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MoE+LB | 1 | 0.084 | 0.210 | 0.083 | 0.083 | 0.707 | 0.280 | 0.089 | 0.540 | 0.718 |
| MoE+LB | 2 | 0.159 | 0.347 | 0.157 | 0.158 | 0.818 | 0.418 | 0.159 | 0.390 | 0.600 |
| MoE+LB | 4 | 0.295 | 0.519 | 0.302 | 0.293 | 0.908 | 0.587 | 0.304 | 0.255 | 0.438 |
| MoE+LB | 8 | 0.541 | 0.738 | 0.541 | 0.548 | 0.972 | 0.780 | 0.535 | 0.131 | 0.280 |
| H-MoE | 1 | 0.095 | 0.240 | 0.093 | 0.088 | 0.704 | 0.310 | 0.093 | 0.551 | 0.707 |
| H-MoE | 2 | 0.173 | 0.360 | 0.176 | 0.168 | 0.819 | 0.441 | 0.169 | 0.397 | 0.586 |
| H-MoE | 4 | 0.324 | 0.509 | 0.326 | 0.332 | 0.913 | 0.588 | 0.324 | 0.264 | 0.416 |
| H-MoE | 8 | 0.593 | 0.702 | 0.600 | 0.619 | 0.975 | 0.751 | 0.600 | 0.164 | 0.233 |

Reading rule:

```text
K=16 selects all 16 buckets/paths, so it is full prefix and only a sanity check.
The meaningful retrieval region is K=1/2/4/8.
```

## Retrieval Interpretation

Observation:

```text
Router top-K beats same-count random/local for K=1/2/4/8.
```

Interpretation:

```text
E1 NTP-trained router has coarse KV retrieval signal.
```

Limitation:

```text
K=8 already uses about 54%-59% of prefix candidates.
The signal is not yet efficient enough for a strong sparse-retrieval claim.
```

Decision:

```text
Do not claim current router bucket is already a usable efficient KV index.
Do claim it contains a weak/coarse retrieval signal worth diagnosing.
```

## Rank-K-Only Diagnostic

This diagnostic measures only the bucket/path at router rank K, not cumulative top-K.

| Variant | rank K | Bucket ratio | Single-bucket recall | Single-bucket mass |
|---|---:|---:|---:|---:|
| MoE+LB | 1 | 0.084 | 0.210 | 0.280 |
| MoE+LB | 2 | 0.076 | 0.137 | 0.138 |
| MoE+LB | 4 | 0.065 | 0.072 | 0.072 |
| MoE+LB | 8 | 0.061 | 0.047 | 0.042 |
| MoE+LB | 16 | 0.053 | 0.032 | 0.023 |
| H-MoE | 1 | 0.095 | 0.240 | 0.310 |
| H-MoE | 2 | 0.078 | 0.119 | 0.132 |
| H-MoE | 4 | 0.081 | 0.066 | 0.069 |
| H-MoE | 8 | 0.059 | 0.043 | 0.033 |
| H-MoE | 16 | 0.037 | 0.037 | 0.028 |

Observation:

```text
The rank-1 bucket/path contributes the most. Contribution drops quickly after rank 2.
```

Interpretation:

```text
Router rank has real ordering signal, but individual buckets are not clean semantic or KV clusters.
The cumulative top-K gain partly comes from adding many mixed buckets, not from one sharply aligned index.
```

## SAE Diagnostic

Representation:

```text
block2_input_after_router_before_block2_attention
```

SAE config:

```text
hidden = 256
tokens = 32768
steps = 1000
```

Summary:

| Variant | SAE recon MSE | SAE L0 mean | bucket-path purity | bucket-rule purity | bucket-path entropy | SAE-path purity | SAE-rule purity |
|---|---:|---:|---:|---:|---:|---:|---:|
| MoE+LB | 0.00689 | 187.2 | 0.155 | 0.204 | 0.928 | 0.257 | 0.330 |
| H-MoE | 0.00713 | 187.3 | 0.161 | 0.191 | 0.908 | 0.264 | 0.363 |

Observation:

```text
Bucket-to-path and bucket-to-rule purity are low; entropy is high.
SAE features have weak path/rule signal but are not clean enough.
```

Interpretation:

```text
The router buckets are mixed semantic groups rather than clean latent path/rule clusters.
This explains why the router has coarse retrieval signal but does not form a clean KV index.
```

Flat and H-MoE bucket/path figures must be compared with the shared-scale figure:

```text
bucket_to_path_flat_vs_hmoe_shared_scale.png
```

The separate SAE heatmaps use independently trained SAEs and independently chosen top features, so their feature columns are diagnostic within a variant, not one-to-one comparable across variants.

Limitation:

```text
SAE L0 is high, so this SAE is a diagnostic probe, not a final sparse-feature proof.
```

## Final Working Claim

```text
E1-trained router buckets contain coarse KV retrieval signal, but the current ordinary
MoE/H-MoE buckets are too mixed and too candidate-heavy to be called clean or efficient
KV indexes.
```

## Next Experiments

1. Improve candidate selection inside selected buckets.
2. Test a router/index objective that better aligns buckets with attention-relevant memory.
3. Treat E1.5/E2.5 as mechanism-only contrast, not as the main E1/E2 advisor claim.
