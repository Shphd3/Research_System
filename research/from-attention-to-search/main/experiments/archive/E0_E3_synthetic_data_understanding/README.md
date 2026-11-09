# E0-E3 Synthetic Data Understanding

This recursive experiment project stores the 0513 data-understanding line.

## Read Order

1. `purpose_card.md` - why this whole line exists.
2. `execution_plan.md` - staged execution order and pass/fail gates.
3. `experiment_parameters.md` - implementation parameters for E0-E2.2.
4. `stages/E0_data_sanity/` - data generator and audit.
5. `stages/E1_dense_feature_readback/` - dense Transformer next-token readback.
6. `stages/E2_moe_feature_separation/` - MoE feature separation package, containing E2.0/E2.1/E2.2.
7. `stages/E3_synthetic_vs_real_statistics/` - synthetic-vs-real statistics comparison.
8. `stages/E4_hierarchical_phrase_extension/` - optional second-stage phrase hierarchy extension.
9. `source_notes/` - copied 0513 daily planning notes used as raw material.

## Current Status

E0, E1, E2, E2.1, and E2.2 completed. The current usable dataset is the all-trigram
clean long-tail corpus with `V=1000,N=10^6`.

E2 is now organized as one package:

```text
stages/E2_moe_feature_separation/versions/E2_0_moe_feature_separation
stages/E2_moe_feature_separation/versions/E2_1_router_input_geometry
stages/E2_moe_feature_separation/versions/E2_2_specialization_pressure
stages/E2_moe_feature_separation/versions/E2_3_router_behavior_decomposition
```

E2 supports controlled synthetic MoE feature-expert alignment, but weakens the
stronger one-feature-one-expert story. E2.1 shows feature identity remains
available in router input space, while router boundaries are weakly aligned
with feature-difference directions. E2.2 shows lowering expert capacity or
increasing feature count does not force cleaner feature-aligned specialization.

E2.3 shared-B control shows the learned router is not explained by prefix-end
`B_token` alone. Feature identity is linearly readable from hidden state, but
expert choice is better explained by full hidden geometry, PCA coordinates, and
router projections than by a clean feature-label partition.

## Claim Boundary

This line can build evidence about controlled synthetic data, dense feature
readback, MoE feature separation, and synthetic-vs-real statistical mismatch.
It cannot yet claim real LLM expert semantics, H-MoE superiority, or indexed-KV
inference speedup.
