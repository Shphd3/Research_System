# Execution Plan: E2.1 Router Input Geometry Diagnostic

## 1. Run Goal

Load E2 trained MoE checkpoints and diagnose why ABC / DEF / GHI / JKL prefix hidden states do not form clean one-feature-one-expert separation.

No model is trained in E2.1.

## 2. Data And Checkpoints

Dataset:

```text
active/synthetic_data_understanding/data_all_trigram_v1000/four_feature_all_trigram_v1000_tokens.txt
```

Checkpoints:

```text
active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000/
```

Variants:

```text
moe_top1_no_lb
moe_top1_lb
```

Seeds:

```text
20260513, 20260514, 20260515, 20260516, 20260517
```

## 3. Diagnostics

For each feature prefix-end position:

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
```

Record:

- prefix-end token embedding;
- router input hidden state;
- router logits and top-1 expert;
- target probability;
- force-routing probability for each expert.

Metrics:

- embedding cosine;
- router input centroid cosine;
- within-feature variance and between-feature distance;
- Fisher ratio;
- router boundary alignment;
- router margin and entropy;
- hidden-vs-routing similarity correlation;
- force-routing dominant advantage.

## 4. Command

```bash
python active/synthetic_data_understanding/scripts/analyze_moe_router_input_geometry.py \
  --e2-out-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000 \
  --data-path active/synthetic_data_understanding/data_all_trigram_v1000/four_feature_all_trigram_v1000_tokens.txt \
  --data-config active/synthetic_data_understanding/configs/e1_all_trigram_v1000.json \
  --out-dir active/synthetic_data_understanding/outputs/e2_1_router_input_geometry \
  --fig-dir active/synthetic_data_understanding/figures/e2_1_router_input_geometry \
  --variants moe_top1_no_lb,moe_top1_lb
```

## 5. Artifacts

Tables:

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

Figures:

```text
embedding_token_cosine_heatmap.png
router_input_centroid_cosine_heatmap.png
router_input_pca_by_feature_and_expert.png
router_boundary_alignment_heatmap.png
router_margin_by_feature.png
router_entropy_by_feature.png
hidden_vs_routing_similarity_scatter.png
force_routing_probability_by_expert.png
dominant_vs_best_forced_expert.png
dominant_advantage_by_feature.png
```

## 6. Result Location

Ignored workspace:

```text
active/synthetic_data_understanding/outputs/e2_1_router_input_geometry/
active/synthetic_data_understanding/figures/e2_1_router_input_geometry/
```

Mainline:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_1_router_input_geometry/
```
