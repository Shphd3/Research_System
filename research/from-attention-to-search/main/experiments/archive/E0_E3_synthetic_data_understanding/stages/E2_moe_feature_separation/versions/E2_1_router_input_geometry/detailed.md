# Detailed Result: E2.1 Router Input Geometry Diagnostic

## Run

Workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
```

Command:

```bash
python active/synthetic_data_understanding/scripts/analyze_moe_router_input_geometry.py \
  --e2-out-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000 \
  --data-path active/synthetic_data_understanding/data_all_trigram_v1000/four_feature_all_trigram_v1000_tokens.txt \
  --data-config active/synthetic_data_understanding/configs/e1_all_trigram_v1000.json \
  --out-dir active/synthetic_data_understanding/outputs/e2_1_router_input_geometry \
  --fig-dir active/synthetic_data_understanding/figures/e2_1_router_input_geometry \
  --variants moe_top1_no_lb,moe_top1_lb
```

No model was trained.

## Output Tables

```text
embedding_token_cosine_matrix.csv
router_input_samples.csv
router_input_centroid_cosine.csv
router_input_distance_table.csv
router_input_pca_projection.csv
router_boundary_alignment.csv
router_margin_table.csv
hidden_vs_routing_similarity.csv
force_routing_table.csv
force_routing_summary.csv
```

## Diagnostic 1: Embedding Geometry

| Variant | Mean off-diagonal abs cosine | Max off-diagonal abs cosine |
|---|---:|---:|
| no-LB | 0.108 | 0.348 |
| LB | 0.109 | 0.376 |

Reading:

- prefix-end token embeddings are not collapsed;
- token identity is available before contextualization.

## Diagnostic 2: Router Input Geometry

| Variant | Mean centroid cosine | Fisher ratio mean | Fisher ratio range |
|---|---:|---:|---:|
| no-LB | 0.203 | 123.220 | 55.277-306.048 |
| LB | 0.214 | 104.152 | 52.645-199.311 |

Reading:

- feature centroids remain separated in router input space;
- H2.1a is weakened: router input is not simply mixed into one shared cloud.

## Diagnostic 3: Router Boundary Alignment

| Variant | Mean abs alignment with dominant boundary | Max abs alignment |
|---|---:|---:|
| no-LB | 0.129 | 0.266 |
| LB | 0.109 | 0.176 |

Reading:

- feature-difference directions are weakly aligned with router boundary directions;
- router does not strongly implement feature-identity linear boundaries.

## Diagnostic 4: Router Margin

| Feature | no-LB margin | no-LB entropy | no-LB dominant frac | LB margin | LB entropy | LB dominant frac |
|---|---:|---:|---:|---:|---:|---:|
| ABC | 0.374 | 1.301 | 0.953 | 0.250 | 1.365 | 1.000 |
| DEF | 0.234 | 1.334 | 0.921 | 0.094 | 1.372 | 0.859 |
| GHI | 0.139 | 1.338 | 0.917 | 0.182 | 1.366 | 0.903 |
| JKL | 0.348 | 1.334 | 0.842 | 0.226 | 1.359 | 0.984 |

Reading:

- top-1 choices can be stable by count, but router logit margins are not large;
- entropy is close to $\log(4)=1.386$;
- LB makes router decisions softer.

## Diagnostic 5: Hidden Geometry vs Routing Outcome

| Variant | Corr(hidden similarity, routing similarity) |
|---|---:|
| no-LB | 0.220 |
| LB | 0.175 |

Reading:

- routing similarity is only weakly explained by hidden centroid similarity;
- imperfect routing separation is not just a nearest-neighbor geometry effect.

## Diagnostic 6: Force-Routing Expert Competence

| Feature | no-LB dominant advantage | LB dominant advantage |
|---|---:|---:|
| ABC | 0.269 | 0.117 |
| DEF | 0.228 | 0.127 |
| GHI | 0.286 | 0.218 |
| JKL | 0.251 | 0.475 |

Reading:

- dominant experts usually have direct predictive advantage;
- non-dominant experts are often still competent;
- capacity sharing is a plausible reason one-feature-one-expert is not necessary.

## Figures

![Embedding cosine](figures/embedding_token_cosine_heatmap.png)

![Router input centroid cosine](figures/router_input_centroid_cosine_heatmap.png)

![Router input PCA](figures/router_input_pca_by_feature_and_expert.png)

![Router boundary alignment](figures/router_boundary_alignment_heatmap.png)

![Router margin](figures/router_margin_by_feature.png)

![Router entropy](figures/router_entropy_by_feature.png)

![Hidden vs routing similarity](figures/hidden_vs_routing_similarity_scatter.png)

![Force routing probability](figures/force_routing_probability_by_expert.png)

![Dominant vs best forced expert](figures/dominant_vs_best_forced_expert.png)

![Dominant advantage](figures/dominant_advantage_by_feature.png)

## Failure Mode Check

- Representation collapse: not observed.
- Router boundary uses feature directions strongly: not observed.
- Router confidence is hard / low entropy: not observed.
- Expert competence is exclusive to one expert: not observed.
- Real-data transfer: not tested.
