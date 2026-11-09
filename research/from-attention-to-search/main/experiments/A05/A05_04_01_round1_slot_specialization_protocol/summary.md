# Result Summary: Round-1 Slot-Block Collapse Audit

Anchor:

`Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_01_uniform_feature_specialization_after_position_removal_anchor.md`

Story:

This staged audit tests whether a minimal no-position uniform slot task still produces sparse top-1 router collapse, and whether that collapse is better explained by missing slot signal, non-slot router-logit dominance, or early lock-in.

## Purpose

The decision question is: in the minimal uniform slot task, does collapse come from missing slot signal in `h_B`, non-slot logit dominance, early sparse top-1 lock-in, or insufficient evidence?

Round 1 executed P0, P1, P2, P3, and P5. P4 forced-routing utility, P6 anti-lock-in, and P7 slot-order diagnostics were not run.

## How It Was Done

Data:

- Dataset: `D_min_block_shift`
- `S=4` slots, `E=4` experts, sequence length `L=12`
- Each sequence contains one moving block: `SLOT_s B_CONST Y_s`
- Valid block starts: `0..9`
- Slot position is `block_start`; `B_CONST` position is `block_start + 1`
- Loss and routing metrics are computed only at the `B_CONST` position

Model:

- Small causal Transformer + sparse top-1 MoE
- Cosine router, `num_experts=4`
- Position embeddings are zeroed and frozen from initialization
- No auxiliary load-balance loss

Run:

- 8 seeds: `20260521..20260528`
- 1600 training steps per seed
- Variants: `P1_clean_baseline`, `P5_slot_centroid_init`

## Metrics

Primary collapse metric:

`max_load`, because it directly measures whether traffic concentrates on one or a few experts.

Primary specialization metric:

`slot_to_expert_NMI`, because balanced load alone is not slot specialization; routed expert identity must align with slot identity.

Trust checks:

- `target_accuracy`: whether the task was learned
- `slot_probe_accuracy_heldout_position`: whether `h_B` contains slot information that generalizes across block starts
- P3 dominant margin component: whether router logits are driven by slot, common, block-position, or residual components

## What Result A Would Mean

If P1 collapses while P2 shows decodable slot signal, then missing slot representation is not the main explanation. The failure is more likely in router selection or training dynamics.

If P3 shows common or other non-slot components dominating the router margin, then collapse is likely caused by non-slot logit dominance rather than absence of slot information.

If P5 preserves slot routing, then the slot partition is reachable and mostly stable under favorable initialization.

## What Result B Would Mean

If P2 fails to decode slot from `h_B`, then collapse could be explained by missing slot signal.

If P3 shows slot margin dominates but routing still collapses, then common-logit dominance is weakened and expert utility or load dynamics become stronger rivals.

If P5 collapses despite favorable initialization, then the slot partition may be unstable under the task/objective/expert capacity.

## Concrete Result Analysis

P0 passed all dataset checks:

- each slot appears 320 times in the audit set;
- each block start appears 128 times;
- each `(slot, block_start)` pair appears 32 times;
- each slot maps to exactly one target;
- every block start contains all four targets;
- route/loss positions are the `B_CONST` positions.

P1 clean baseline collapses despite perfect task learning:

| Variant | Seeds | Mean slot-expert NMI | Mean max load | Mean accuracy | Hard collapse rate |
|---|---:|---:|---:|---:|---:|
| `P1_clean_baseline` | 8 | 0.080 | 0.969 | 1.000 | 1.000 |

Seven of eight P1 seeds route all slots to one expert at the final checkpoint. The remaining seed uses two experts but still has `max_load=0.75`, so it is still hard-collapsed under the protocol threshold.

P2 weakens the missing-slot-signal explanation. Final held-out-block-start slot probe accuracy is 1.0 in all P1 seeds, so `h_B` contains linearly decodable slot information even when the router collapses.

P3 supports non-slot router-logit dominance. In P1, the common component is the dominant top-2 router-margin component for 290 / 320 final `(seed, slot, block_start)` rows. All 32 seed-slot rows have `stable_lock_step <= 10`, so routing locks early.

P5 shows reachability under favorable initialization:

| Variant | Seeds | Mean slot-expert NMI | Mean max load | Mean accuracy | Hard collapse rate |
|---|---:|---:|---:|---:|---:|
| `P5_slot_centroid_init` | 8 | 0.980 | 0.278 | 1.000 | 0.000 |

Seven of eight P5 seeds preserve perfect slot routing. Seed `20260524` mildly erodes to `slot_to_expert_NMI=0.842` and `max_load=0.475`, but still uses all four experts and is not hard-collapsed.

## Key Figures

![P1 route heatmaps](figures/round1_slot_specialization_4gpu_20260609/p1_route_heatmaps.png)

P1 heatmaps show deterministic but collapsed routing. High per-slot route purity is misleading here because every slot can consistently route to the same expert.

![P3 margin decomposition](figures/round1_slot_specialization_4gpu_20260609/p3_margin_decomposition_plots.png)

P3 shows common-component dominance in the router margin for the baseline.

![P5 baseline vs positive control](figures/round1_slot_specialization_4gpu_20260609/p5_baseline_vs_positive_control.png)

P5 shows that slot-aligned routing is reachable when the router is initialized into the slot partition.

## Claim Boundary

Can claim:

- In `D_min_block_shift`, vanilla sparse top-1 routing collapses despite perfect task learning.
- Slot information is decodable from `h_B`, so missing slot representation is not the main Round-1 explanation.
- P3 points to common-component router-logit dominance as the strongest Round-1 mechanism.
- Slot routing is reachable and mostly stable under favorable slot-aware initialization.

Cannot claim:

- P4 was not run, so expert causal utility for each slot is not established.
- P5 is not a label-free or deployable anti-lock-in method.
- The result does not yet transfer to multi-B exact-feature routing or real language-model settings.

## Next Decision

Run a Round-2 intervention test: does common-logit cancellation, feature-aware initialization, or anti-lock-in make a trainable sparse top-1 router enter the reachable slot/exact-feature partition without oracle labels?

## Source Files

- Protocol: `daily_research_reports/0609/round1_slot_specialization_protocol.md`
- Detailed record: `detailed.md`
- Results: `results/round1_slot_specialization_4gpu_20260609/`
- Figures: `figures/round1_slot_specialization_4gpu_20260609/`
