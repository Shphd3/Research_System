# Execution Plan: E2-S Spectral Covariance Router Side Branch

## 1. Run Goal

Direct full run. No hierarchy data. Test whether no-LB spectral covariance projection routers can match or beat ordinary `full_hidden_lb` feature-aligned routing.

## 2. Data

Use:

```text
configs/e1_all_trigram_v1000.json
data_all_trigram_v1000/
regime = four_feature_all_trigram_v1000
```

Features:

| feature | relation | count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 10000 |
| DEF | `[3,4] -> 23` | 5000 |
| GHI | `[6,7] -> 20` | 500 |
| JKL | `[8,9] -> 21` | 100 |

## 3. $\mu$ And Covariance Statistics

For each source:

```text
mu_source = mean(h)
C_source = E[(h - mu_source)(h - mu_source)^T]
```

Sources:

| source | role |
|---|---|
| `trained_dense_cov` | main statistic |
| `random_init_cov` | random-hidden control |
| `shuffled_dense_cov` | unigram-only control |

Sampling:

```text
sample_tokens_for_covariance = 250000
positions = all token positions
feature_prefix_positions are logged separately, not used to define global mu
```

Projection rules:

- all spectral projections use `h - mu_source`;
- each source uses only its own $\mu$ and eigenvectors;
- `full_hidden_lb` and `full_hidden_no_lb` use raw hidden, no centering;
- $\mu$ is global hidden mean, not feature-conditioned mean.

## 4. Model / Training

Model:

```text
1-layer causal Transformer
top-1 4-expert MoE FFN
router input = projection(h)
expert input = original h
```

Full run:

```text
steps = 10000
batch_size = 128
seq_len = 32
d_model = 64
n_heads = 4
expert_ffn_dim = 128
seeds = [20260513, 20260514, 20260515, 20260516, 20260517]
```

## 5. Variants

Primary `trained_dense_cov` variants:

| variant | router input | LB |
|---|---|---|
| `full_hidden_lb` | original hidden | yes, `0.01` |
| `full_hidden_no_lb` | original hidden | no |
| `pca_full_coord_no_lb` | PCs 0:64 | no |
| `top_0_25_raw_no_lb` | PCs 0:16 | no |
| `topdrop_25_100_raw_no_lb` | PCs 16:64 | no |
| `mid_25_75_raw_no_lb` | PCs 16:48 | no |
| `midlate_25_90_raw_no_lb` | PCs 16:58 | no |
| `midlate_25_90_whiten_no_lb` | PCs 16:58 whitened | no |
| `tail_50_100_raw_no_lb` | PCs 32:64 | no |
| `random_matched_42_no_lb` | random 42-dim | no |

Statistic-quality controls:

```text
random_init_cov: midlate_25_90_raw_no_lb, midlate_25_90_whiten_no_lb
shuffled_dense_cov: midlate_25_90_raw_no_lb, midlate_25_90_whiten_no_lb
```

## 6. Commands

Run:

```bash
cd XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
python scripts/run_spectral_covariance_router.py \
  --config configs/e2_s_spectral_covariance_router_all_trigram_v1000.json
```

## 7. Metrics And Artifacts

Statistic audit:

```text
mu_covariance_audit.json
mu_covariance_table.csv
covariance_spectrum_by_source.csv
feature_projection_probe_table.csv
feature_centroid_distance_by_band.csv
projection_band_table.csv
```

Router evaluation:

```text
readback_table.csv
routing_matrix_p_expert_given_feature.csv
routing_alignment_table.csv
expert_load_table.csv
ablation_delta_table.csv
force_routing_summary.csv
variant_summary_table.csv
```

Required figures:

```text
mu_norm_by_source.png
covariance_spectrum_by_source.png
cumulative_variance_by_source.png
feature_probe_accuracy_by_band_<source>.png
fisher_ratio_by_projection.png
pc_feature_alignment_heatmap.png
readback_by_projection.png
routing_nmi_by_projection.png
routing_matrix_midlate_vs_full_lb_vs_random.png
expert_load_by_projection.png
dominant_ablation_by_projection.png
force_routing_by_projection.png
```

## 8. Pass / Fail Criteria

Strong support:

- trained-dense midlate probe accuracy beats random/shuffled covariance;
- `midlate_25_90_*_no_lb` routing NMI/purity approaches or beats `full_hidden_lb`;
- spectral no-LB router does not collapse;
- readback stays high for all four features;
- dominant expert ablation is clearer than no-LB/random controls.

No support:

- midlate probe does not beat random matched subspace;
- trained covariance does not beat random/shuffled covariance;
- spectral no-LB routing does not beat `full_hidden_no_lb`;
- only `full_hidden_lb` is stable.

## 9. Result Location

Ignored runnable outputs:

```text
outputs/e2_s_spectral_covariance_router/
figures/e2_s_spectral_covariance_router/
```

Mainline-safe report:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_S_spectral_covariance_router_side_branch/
```
