# Detailed Notes: E2.3 Router Behavior Decomposition

## Run Record

Workspace:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

New ignored configs/scripts:

```text
configs/e2_3_shared_b_control_data.json
configs/e2_3_shared_b_control_moe.json
scripts/analyze_router_behavior_decomposition.py
```

Commands:

```bash
python scripts/generate_synthetic_patterns.py \
  --config configs/e2_3_shared_b_control_data.json \
  --out-dir data_e2_3_shared_b_control

python scripts/audit_synthetic_patterns.py \
  --config configs/e2_3_shared_b_control_data.json \
  --data-dir data_e2_3_shared_b_control \
  --out-dir outputs/e2_3_shared_b_control_audit \
  --fig-dir figures/e2_3_shared_b_control_audit

python scripts/train_moe_feature_separation.py \
  --run-config configs/e2_3_shared_b_control_moe.json

python scripts/plot_moe_feature_separation.py \
  --out-dir outputs/e2_3_shared_b_control_moe \
  --fig-dir figures/e2_3_shared_b_control_moe

python scripts/analyze_moe_router_input_geometry.py \
  --e2-out-dir outputs/e2_3_shared_b_control_moe \
  --data-path data_e2_3_shared_b_control/shared_b_all_trigram_v1000_tokens.txt \
  --data-config configs/e2_3_shared_b_control_data.json \
  --regime shared_b_all_trigram_v1000 \
  --out-dir outputs/e2_3_shared_b_control_geometry \
  --fig-dir figures/e2_3_shared_b_control_geometry \
  --variants moe_top1_no_lb,moe_top1_lb \
  --max-positions-per-feature 1000

python scripts/analyze_router_behavior_decomposition.py \
  --e2-out-dir outputs/e2_3_shared_b_control_moe \
  --data-path data_e2_3_shared_b_control/shared_b_all_trigram_v1000_tokens.txt \
  --data-config configs/e2_3_shared_b_control_data.json \
  --regime shared_b_all_trigram_v1000 \
  --out-dir outputs/e2_3_router_behavior_decomposition \
  --fig-dir figures/e2_3_router_behavior_decomposition \
  --variants moe_top1_no_lb,moe_top1_lb \
  --max-positions-per-feature 1200 \
  --pca-dims 16
```

## Raw Output Locations

```text
outputs/e2_3_shared_b_control_audit/
outputs/e2_3_shared_b_control_moe/
outputs/e2_3_shared_b_control_geometry/
outputs/e2_3_router_behavior_decomposition/

figures/e2_3_shared_b_control_moe/
figures/e2_3_shared_b_control_geometry/
figures/e2_3_router_behavior_decomposition/
```

## Data Audit

| Feature | Pattern | Target count | Actual count | Collision count | Empirical next-token probability |
|---|---|---:|---:|---:|---:|
| ABC | `1 2 22` | 10000 | 10000 | 0 | 1.000 |
| DEF | `3 2 23` | 5000 | 5000 | 0 | 1.000 |
| GHI | `6 7 20` | 500 | 500 | 0 | 0.998 |
| JKL | `8 7 21` | 100 | 100 | 0 | 0.990 |

Purpose of this data:

```text
B token no longer uniquely identifies feature:
ABC and DEF share B=2; GHI and JKL share B=7.
```

## Main Tables

### Alignment

| Variant | NMI | ARI |
|---|---:|---:|
| no-LB | 0.683 | 0.693 |
| LB | 0.404 | 0.334 |

### Readback

| Variant | ABC | DEF | GHI | JKL |
|---|---:|---:|---:|---:|
| no-LB | 0.998 | 0.996 | 0.968 | 0.791 |
| LB | 0.999 | 0.995 | 0.963 | 0.821 |

### Predictor Accuracy

| Predictor | no-LB | LB |
|---|---:|---:|
| majority baseline | 0.430 | 0.404 |
| B-token-only | 0.478 | 0.449 |
| feature-only | 0.711 | 0.529 |
| A+B-token | 0.711 | 0.522 |
| PCA-only | 0.958 | 0.911 |
| router-projection | 0.974 | 0.944 |
| full-hidden | 0.963 | 0.947 |
| combined | 0.980 | 0.955 |
| feature-linear-probe | 1.000 | 1.000 |

### Projection Intervention

| Variant | Intervention | Expert assignment stability | Feature probe accuracy |
|---|---|---:|---:|
| no-LB | original | 1.000 | 1.000 |
| no-LB | remove feature subspace | 0.528 | 0.335 |
| no-LB | remove router subspace | 0.443 | 1.000 |
| LB | original | 1.000 | 1.000 |
| LB | remove feature subspace | 0.587 | 0.340 |
| LB | remove router subspace | 0.350 | 1.000 |

Interpretation:

- Removing feature subspace damages feature readability and changes expert assignment partly.
- Removing router subspace changes expert assignment more directly while preserving feature probe.
- Therefore expert choice uses router-sensitive directions in hidden space; feature information exists, but router projection determines the actual boundary.

### Routing Counterfactual

| Variant | learned | feature oracle | random expectation | mean expert output | zero expert output |
|---|---:|---:|---:|---:|---:|
| no-LB | 0.938 | 0.781 | 0.715 | 0.857 | 0.379 |
| LB | 0.944 | 0.787 | 0.762 | 0.902 | 0.418 |

Interpretation:

- Zero expert output hurts readback: expert path matters.
- Feature-oracle routing is worse than learned routing: clean one-feature-one-expert is not the learned loss-compatible solution.
- Mean expert output is still strong: multiple experts share competence.

## Figure Support Map

| Figure | Supports |
|---|---|
| `moe_ntp_loss_comparison.png` | shared-B MoE training converges below random baseline |
| `routing_matrix_heatmap_no_lb_vs_lb.png` | alignment persists but weakens under shared-B, especially with LB |
| `feature_readback_no_lb_vs_lb.png` | all four shared-B rules are read back |
| `ablation_delta_by_feature.png` | selected/dominant expert still has causal relevance, with feature-wise asymmetry |
| `router_input_pca_by_feature_and_expert.png` | hidden representation remains separable |
| `router_boundary_alignment_heatmap.png` | router boundary still weakly aligned with feature difference |
| `predictor_accuracy_by_variable_group.png` | full hidden/PCA/router projection explain expert choice best |
| `feature_vs_token_explanation.png` | B-token-only is not enough under shared-B |
| `conditional_importance_bar.png` | PCA/router projection dominate conditional importance |
| `feature_subspace_vs_router_subspace_projection.png` | expert assignment depends on router subspace; feature probe survives router-subspace removal |
| `learned_vs_oracle_vs_random_routing_readback.png` | learned routing beats forced feature-oracle routing |

## Claim Boundary

This run supports:

```text
In the shared-B controlled trigram setting, expert choice is not explained by
prefix-end token alone; feature identity is recoverable from hidden states, but
learned router behavior is better explained by hidden geometry and router
projection than by a clean feature-label partition.
```

This run does not support:

```text
real LLM expert semantics;
universal MoE routing theory;
transfer to natural language;
router-as-KV-index claims.
```
