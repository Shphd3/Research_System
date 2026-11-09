# Detailed Report: H0522b CB Context B Routing Seq32

## 1. Run

Run:

```text
h0522b_cb_context_b_routing_seq32_local2gpu_20260522
```

Device:

```text
local 2 x H100
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Runner:

```text
active/synthetic_data_understanding/scripts/run_h0522b_cb_context_b_routing_seq32.py
```

Config:

```text
active/synthetic_data_understanding/configs/h0522b_cb_context_b_routing_seq32.json
```

Result dir:

```text
active/synthetic_data_understanding/results/h0522b_cb_context_b_routing_seq32/h0522b_cb_context_b_routing_seq32_local2gpu_20260522/
```

Figure dir:

```text
active/synthetic_data_understanding/figures/h0522b_cb_context_b_routing_seq32/h0522b_cb_context_b_routing_seq32_local2gpu_20260522/
```

## 2. Data

```text
A-only:       [A, r] -> y_A
B-only:       [r, B] -> y_B
AB-composite: [A, B] -> y_AB
CB-composite: [C, B] -> y_CB
background:  random background -> random background target
```

Every class has the same number of samples. `AB` and `CB` have the same frequency.

## 3. Metrics

Most important metric:

```text
B source-token expert distribution per seed across B-only, AB, and CB.
```

Secondary metrics:

```text
same dominant expert across B contexts
routing distribution cosine
class accuracy
```

## 4. Results

Class accuracy:

| Class | Mean accuracy |
|---|---:|
| A-only | 1.0000 |
| B-only | 1.0000 |
| AB-composite | 0.9997 |
| CB-composite | 1.0000 |
| background | 0.0081 |

`background` target is random background token, so it is not used as task-success evidence.

Seed-level B context:

| Seed | B-only expert | AB expert | CB expert | All same |
|---|---:|---:|---:|---:|
| 20260521 | 2 | 2 | 2 | 1 |
| 20260522 | 2 | 2 | 2 | 1 |
| 20260523 | 0 | 0 | 0 | 1 |
| 20260524 | 3 | 1 | 2 | 0 |

Cross-seed:

```text
B_all_three_same = 3/4 seeds
```

Distribution cosine:

| Seed | B-only vs AB | B-only vs CB | AB vs CB |
|---|---:|---:|---:|
| 20260521 | 0.9956 | 0.9885 | 0.9844 |
| 20260522 | 0.9910 | 0.9967 | 0.9899 |
| 20260523 | 0.9507 | 0.9914 | 0.9208 |
| 20260524 | 0.9827 | 0.8759 | 0.8667 |

## 5. Figures

![B context routing by seed](figures/b_context_routing_horizontal_by_seed.png)

![Source role routing by seed](figures/source_role_routing_matrix_by_seed_row.png)

## 6. Tables

```text
tables/class_metrics.csv
tables/class_metrics_by_seed.csv
tables/seed_rule_summary_by_seed.csv
tables/b_context_similarity_by_seed.csv
tables/cross_seed_b_context_intersection.csv
```

## 7. Claim Boundary

The claim is local:

```text
In this seq_len=32 balanced AB/CB synthetic setup, B routing mostly keeps B
identity across contexts, with seed-dependent context modulation.
```

This does not rule out context-conditioned routing under stronger anti-identity data.

## 8. Post-Hoc Analysis: Why Does Seed 20260524 Split?

This analysis does not retrain the model. It reloads the four trained
checkpoints and extracts B source-token router-input hidden states.

Definitions:

```text
B_identity = mean(all B source states) - mean(background source states)
AB_context = mean(B_in_AB) - mean(B_in_B_only)
CB_context = mean(B_in_CB) - mean(B_in_B_only)
AB_vs_CB   = mean(B_in_AB) - mean(B_in_CB)
```

### 8.1 Hidden Centroids

For seed `20260524`, B-context centroids are more separated:

| Comparison | Centroid cosine | L2 distance |
|---|---:|---:|
| B-only vs AB | 0.9640 | 2.2590 |
| B-only vs CB | 0.8557 | 4.4307 |
| AB vs CB | 0.8069 | 4.9168 |

![B-position hidden PCA centroids](figures/subspace_analysis/b_context_hidden_pca_centroids_by_seed.png)

![B context centroid cosine](figures/subspace_analysis/b_context_centroid_cosine_by_seed.png)

Interpretation:

```text
20260524 really has stronger representation-level context separation,
especially between AB and CB.
```

### 8.2 Router Boundary Alignment

For seed `20260524`, the dominant expert split is:

```text
B-only -> E3
AB     -> E1
CB     -> E2
```

But the cosine between context directions and the corresponding dominant
router-boundary vectors is small:

| Direction | Boundary | Cosine |
|---|---|---:|
| B-only -> AB | E3 -> E1 | 0.0763 |
| B-only -> CB | E3 -> E2 | 0.1127 |
| AB -> CB | E1 -> E2 | 0.0634 |

![B context router boundary alignment](figures/subspace_analysis/b_context_router_boundary_alignment_by_seed.png)

Interpretation:

```text
The split is not well explained by a clean linear router boundary aligned with
the simple context-difference directions.
```

### 8.3 Expert Subspace Projection

Rank-4 SVD projection for seed `20260524`:

| Direction | E0 | E1 | E2 | E3 |
|---|---:|---:|---:|---:|
| B_identity | 0.907 | 0.564 | 0.791 | 0.841 |
| AB_context | 0.901 | 0.921 | 0.782 | 0.129 |
| CB_context | 0.197 | 0.910 | 0.819 | 0.490 |
| AB_vs_CB | 0.279 | 0.928 | 0.823 | 0.331 |

![B context expert subspace projection](figures/subspace_analysis/b_context_expert_subspace_projection_rank4_by_seed.png)

Interpretation:

```text
20260524 has seed-specific evidence that E1/E2 subspaces contain context
directions, while E3 still contains B identity. This supports
context-conditioned geometry, but not a clean cross-seed feature-specialized
router rule.
```

For the other three seeds, the dominant B expert usually has strong
`B_identity` projection. Context directions may exist in some expert subspaces,
but they do not become the dominant routing split.
