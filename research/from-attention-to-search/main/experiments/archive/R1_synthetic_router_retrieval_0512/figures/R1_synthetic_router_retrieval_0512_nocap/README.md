# R1 Figures - E1/E2 Focus

Scope:
- E1 checkpoints only: `flat_lb_on`, `hmoe_lb_off`.
- E2 full-prefix retrieval analysis only.
- `prefix_len >= 128` stable-cache view.
- Baselines use the same candidate count as router top-K.

Key figures:
1. `e2_nocap_topk_recall_mass_l2_prefix_ge128.png`
2. `e2_nocap_candidate_ratio_prefix_ge128.png`
3. `e2_nocap_router_delta_vs_random_prefix_ge128.png`
4. `e2_rank_k_only_recall_mass_prefix_ge128.png`
5. `bucket_to_path_flat_vs_hmoe_shared_scale.png`

Reading rule:
- `K=16` selects all 16 buckets/paths and becomes full prefix, so it is a sanity check.
- The meaningful retrieval region is `K=1/2/4/8`, where candidate ratio is below full prefix.
- Router is useful only if it beats same-count random/local before `K=16`.
- `rank-K-only` measures only the K-th bucket/path, not cumulative top-K.
- The shared-scale bucket/path figure is the preferred Flat vs H-MoE distribution comparison.
