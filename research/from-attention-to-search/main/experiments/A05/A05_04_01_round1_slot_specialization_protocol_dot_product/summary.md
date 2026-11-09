# Result Summary: Round-1 Slot-Block Collapse Audit With Dot-Product Router

Anchor:

`Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_01_uniform_feature_specialization_after_position_removal_anchor.md`

Story:

This is the standard linear-router version of the Round-1 audit. The router uses dot-product logits, so P3 margin decomposition is directly linear in the hidden-state components.

## Purpose

The decision question is: in the minimal uniform slot task, does collapse come from missing slot signal in `h_B`, non-slot logit dominance, early sparse top-1 lock-in, or insufficient evidence?

## How It Was Done

Data:

- Dataset: `D_min_block_shift`
- `S=4` slots, `E=4` experts, sequence length `L=12`
- Each sequence contains one moving block: `SLOT_s B_CONST Y_s`
- Valid block starts: `0..9`
- Slot position is `block_start`; `B_CONST` position is `block_start + 1`
- Loss and routing metrics are computed only at the `B_CONST` position

Model and run:

- Small causal Transformer + sparse top-1 MoE
- Dot-product router: `z_e = w_e^T h_B`
- Position embeddings are zeroed and frozen from initialization
- No auxiliary load-balance loss
- 8 seeds: `20260521..20260528`
- 1600 training steps per seed
- Variants: `P1_clean_baseline`, `P5_slot_centroid_init`

## Metrics

Primary collapse metric:

`max_load`, because it measures whether traffic concentrates on one or a few experts.

Primary specialization metric:

`slot_to_expert_NMI`, because balanced load alone is not slot-level specialization.

Trust checks:

- `target_accuracy`: whether the task is learned
- `slot_probe_accuracy_heldout_position`: whether slot information exists in `h_B`
- P3 dominant margin component: whether dot-product router logits are driven by slot, common, block-position, or residual components

## What Result A Would Mean

If P1 collapses while P2 shows decodable slot signal, then missing slot representation is not the main explanation.

If P3 shows common or other non-slot components dominating the router margin, then collapse is likely a router-logit selection problem.

If P5 preserves slot routing, then the slot partition is reachable and stable when the router starts in the intended partition.

## What Result B Would Mean

If P2 fails to decode slot from `h_B`, then collapse could be explained by missing slot signal.

If P3 shows slot margin dominates but routing still collapses, then common-logit dominance is weakened.

If P5 collapses despite supervised slot initialization, then the intended slot partition may be unstable under this task/objective.

## Concrete Result Analysis

P0 passed all data checks: slot counts, block-start counts, `(slot, block_start)` counts, target mapping, route position, and loss target are all valid.

P1 dot-product baseline collapses despite perfect task learning:

| Variant | Seeds | Mean slot-expert NMI | Mean max load | Mean accuracy | Hard collapse rate |
|---|---:|---:|---:|---:|---:|
| `P1_clean_baseline` | 8 | 0.080 | 0.969 | 1.000 | 1.000 |

Seven of eight P1 seeds route all slots to one expert. The remaining seed uses two experts but still has `max_load=0.75`.

P2 rules out missing slot signal in this minimal task. In P1, final random-split slot probe accuracy and held-out-block-start slot probe accuracy are both 1.0 in all seeds.

P3 supports non-slot dot-product logit dominance. In P1, the common component dominates the final top-2 router margin in 290 / 320 `(seed, slot, block_start)` rows. All 32 seed-slot rows have `stable_lock_step <= 10`.

P5 supervised slot initialization gives perfect slot-level specialization in all seeds:

| Variant | Seeds | Mean slot-expert NMI | Mean max load | Mean accuracy | Hard collapse rate |
|---|---:|---:|---:|---:|---:|
| `P5_slot_centroid_init` | 8 | 1.000 | 0.250 | 1.000 | 0.000 |

P5 uses slot labels for router initialization/calibration. Therefore it is a supervised positive control, not a label-free discovery method.

## Key Figures

![P1 route heatmaps](figures/round1_slot_specialization_dot_product_4gpu_20260609/p1_route_heatmaps.png)

P1 shows deterministic but collapsed routing.

![P3 margin decomposition](figures/round1_slot_specialization_dot_product_4gpu_20260609/p3_margin_decomposition_plots.png)

P3 shows common-component dominance in dot-product router margins.

![P5 baseline vs positive control](figures/round1_slot_specialization_dot_product_4gpu_20260609/p5_baseline_vs_positive_control.png)

P5 shows perfect slot-aligned routing under supervised initialization.

## Claim Boundary

Can claim:

- With the standard dot-product router, vanilla sparse top-1 routing collapses in `D_min_block_shift`.
- Slot information is present in `h_B`; collapse is not explained by missing slot representation.
- Dot-product router margins are usually dominated by the common component, not the slot component.
- Supervised slot initialization reaches perfect slot-level specialization in all 8 seeds.

Cannot claim:

- P4 was not run, so slot-specific expert causal utility is not established.
- P5 is not an unsupervised or deployable anti-lock-in method.
- This result does not yet establish behavior for longer sequences, multi-B exact-feature routing, or real language-model settings.

## Next Decision

Use this dot-product version as the standard Round-1 result. The next scientific test is whether a label-free intervention can make the trainable router enter the reachable slot/exact-feature partition.

## Source Files

- Detailed record: `detailed.md`
- Results: `results/round1_slot_specialization_dot_product_4gpu_20260609/`
- Figures: `figures/round1_slot_specialization_dot_product_4gpu_20260609/`
- ACP job: `pt-eajzxnl3`
