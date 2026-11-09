# Detailed Notes: E2-B2 Prototype Center Separation

## 1. Implementation

Added to runtime script:

```text
scripts/train_moe_prototype_center_gating.py
```

New loss:

$$
L_{\text{center-sep}}
=
\mathrm{mean}_{e\neq e'}
\max(0,\cos(c_e,c_{e'})-m)^2
$$

Run config:

```text
configs/e2_b2_prototype_center_separation_uniform_all_trigram_v1000.json
```

Outputs:

```text
outputs/e2_b2_prototype_center_separation/
figures/e2_b2_prototype_center_separation/
```

Mainline report:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_B2_prototype_center_separation/
```

## 2. Commands

```bash
python scripts/train_moe_prototype_center_gating.py \
  --run-config configs/e2_b2_prototype_center_separation_uniform_all_trigram_v1000.json
```

```bash
python scripts/plot_router_gating_variants.py \
  --mode prototype \
  --out-dir outputs/e2_b2_prototype_center_separation \
  --fig-dir figures/e2_b2_prototype_center_separation
```

## 3. Result Table

| variant | readback_probability | NMI | ARI | best_permutation_accuracy | fixed_label_accuracy | expert_load_entropy | ablation_drop |
|---|---:|---:|---:|---:|---:|---:|---:|
| prototype_center_sep_0_1_no_lb | 0.9952 | 0.4843 | 0.2980 | 0.5077 | 0.2493 | 1.1363 | 0.3629 |
| prototype_center_sep_1_0_no_lb | 0.9948 | 0.4875 | 0.3077 | 0.5238 | 0.2487 | 1.1414 | 0.3980 |
| prototype_center_sep_1_0_lb | 0.9949 | 0.5783 | 0.3793 | 0.5284 | 0.2381 | 1.3862 | 0.4060 |

## 4. Prototype Geometry

| variant | mean offdiag cosine | max offdiag cosine | min offdiag cosine |
|---|---:|---:|---:|
| prototype_center_sep_0_1_no_lb | -0.0755 | -0.0127 | -0.2424 |
| prototype_center_sep_1_0_no_lb | -0.0756 | -0.0127 | -0.2424 |
| prototype_center_sep_1_0_lb | -0.0221 | -0.0011 | -0.1440 |

Interpretation:

```text
centers were separated successfully;
routing still did not become clean.
```

## 5. Figure Index

- `figures/routing_matrix_by_variant.png`: $P(expert|feature)$ for each center-separation variant.
- `figures/prototype_cosine_heatmap.png`: cosine between expert prototype centers.
- `figures/feature_centroid_to_prototype_heatmap.png`: cosine between feature centroids and prototype centers.
- `figures/best_permutation_accuracy_by_variant.png`: best one-to-one assignment after expert permutation.
- `figures/ablation_delta_by_variant.png`: dominant expert causal drop.
- `figures/expert_load_by_variant.png`: expert load entropy.
- `figures/readback_by_variant.png`: feature readback.

## 6. Comparison To E2-B

E2-B no-aux prototype:

```text
NMI ≈ 0.47-0.52
best-perm acc ≈ 0.51-0.53
```

E2-B2 center separation:

```text
NMI ≈ 0.48-0.58
best-perm acc ≈ 0.51-0.53
```

E2-B supervised prototype aux:

```text
NMI = 1.0
best-perm acc = 1.0
fixed-label acc = 1.0
```

Conclusion:

```text
center repulsion is not enough;
direct or indirect feature-to-center assignment pressure is needed.
```
