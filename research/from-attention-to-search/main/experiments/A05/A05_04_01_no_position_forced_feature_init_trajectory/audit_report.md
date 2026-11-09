# Audit Report: Uniform Feature-to-Expert Collapse

## 1. Executive Verdict

| Audit area | Verdict | Evidence | Boundary |
|---|---|---|---|
| Data/position construction | PASS | `position_support_audit.csv` shows every slot supports positions 5-30; `generate_varpos_batch` randomizes the logical feature block. | This is one-B slot-level data, not multi-B exact feature data. |
| Position removal | PASS | `make_model` zeros `model.pos_emb.weight` and freezes gradients. | Fixed template tokens still exist; the intervention removes learned absolute position embedding and randomizes routed logical position. |
| Metric validity | PASS | `route_slot_nmi`, `max_load`, `active_experts`, and `target_accuracy` are logged by seed and step. | `target_accuracy` alone is misleading because collapsed and specialized runs both reach 1.0. |
| Representation visibility | PASS | final `probe_slot_from_h=1.0` for every variant and seed. | Probe is a final-state diagnostic; it does not prove router gradients use this feature. |
| Oracle feature utility | PASS | `V3_oracle_frozen` reaches `NMI=1.0`, `max_load=0.25`, `accuracy=1.0` in all seeds. | Oracle control is externally forced, not naturally discovered. |
| Vanilla router specialization | FAIL | `V0_vanilla_random` reaches final `NMI=0.0`, `max_load=1.0` in all seeds. | Failure is at logical B routing only. |
| Current feature-init robustness | FAIL | `V2_feature_init_trainable` succeeds only in seed 20260522 and collapses in 20260521/20260523. | This does not rule out better feature-init. |
| Current inhibition robustness | FAIL | `V4_feature_init_inhibition` succeeds only in seed 20260522 and collapses in 20260521/20260523. | This does not rule out other inhibition schedules or weights. |
| Exact training mechanism | UNCLEAR | Trajectories and final utility matrices are logged, but no frozen-to-trainable release or causal gradient intervention was run. | Next experiment should isolate when a verified partition breaks. |

Safest conclusion: slot-level routing is feasible and useful after position removal, but the tested trainable top-1 router controls do not reliably discover or preserve it.

## 2. Experiment Matrix Reconstructed

Actual run:

| item | value |
|---|---|
| run name | `a05_04_forced_feature_init_trajectory_4gpu_20260609` |
| ACP job | `pt-ah9hhx0s` |
| seeds | `20260521`, `20260522`, `20260523` |
| experts | 4 |
| top-k | hard top-1 |
| router metric | cosine |
| position setting | learned position embedding zeroed and frozen |
| feature position setting | logical B block randomized over valid positions 5-30 |
| feature key | slot id |
| train steps | 1600 |
| batch size | 384 |
| eval samples per slot | 256 |
| optimizer settings | lr 0.0008, weight decay 0.01, grad clip 1.0 |
| result dir | `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/` |

Variant matrix:

| Variant | Role | Final verdict |
|---|---|---|
| `V0_vanilla_random` | random trainable top-1 router | collapses in all seeds |
| `V1_random_balanced_init` | candidate-selected balanced random initialization | partial structure only |
| `V2_feature_init_trainable` | slot-centroid-directed trainable router initialization | seed-dependent; 1/3 structured |
| `V3_oracle_frozen` | frozen oracle slot router at logical B position | perfect positive control |
| `V4_feature_init_inhibition` | slot-centroid-directed init plus inhibition loss | seed-dependent; 1/3 structured |

## 3. Code / Data / Init Findings

| Finding | Evidence |
|---|---|
| Logical feature block is randomized. | `scripts/run_a05_04_forced_feature_init_trajectory.py:110` defines `generate_varpos_batch`; `valid_block_starts` at line 103 provides valid positions; output `position_support_audit.csv` confirms all slots cover positions 5-30. |
| No-position intervention is applied in the model. | `make_model` at lines 159-164 zeros `model.pos_emb.weight` and sets `requires_grad_(False)`. |
| Route/eval happens at the logical B token position. | `forward_variant` at lines 298-306 takes `batch.route_pos`; route matrices are computed from logical slot labels and selected experts. |
| Feature-init is slot-centroid based. | `feature_init_router` at lines 213-240 constructs router rows from slot centroids. |
| Balanced init is candidate-selected random init. | `random_balanced_init` at lines 262-279 selects the candidate with lower step-0 max load / higher NMI. |
| Oracle routing is forced and frozen. | `forward_variant` at lines 298-306 forces expert=`slot`; `train_one` at lines 495-498 freezes router parameters for `V3`. |
| Inhibition is added only for `V4`. | `gradient_diagnostic` at lines 445-456 and `train_one` at lines 532-537 call `true_token_conditioned_inhibition_loss`. |
| `V2`/`V4` are not clean successful step-0 feature-init controls here. | Step-0 heatmaps show `NMI=0.0`, `max_load=1.0` for all `V2`/`V4` seeds; only seed 20260522 later recovers structure. |

## 4. Metric Validity

- Primary specialization metric: `route_slot_nmi`, because the tested feature key is slot id.
- Load metric: `max_load`; `0.25` is ideal load balance for 4 experts but not sufficient without high NMI.
- Target metric: `target_accuracy`; it is necessary for validity but misleading as a specialization metric.
- Representation check: `probe_slot_from_h`.
- Utility check: `route_utility_match` and `utility_matrix_by_step.csv`; final utility is interpreted as co-adapted, not as an initial causal utility proof.

## 5. Step-0 Geometry Verdict

Step-0 vanilla and feature-init conditions often already have high load concentration. `V1` improves initial balance, but the improvement does not guarantee final specialization.

Boundary: this run does not re-audit the 05_03 common-offset mechanism. It tests the post-position-removal setting. The relevant result is that even when position embedding is removed and logical B position is randomized, trainable routing does not robustly reach oracle specialization.

## 6. Training-Dynamics Verdict

Training can reach perfect target accuracy while preserving collapse. `V0` reaches accuracy 1.0 with final `NMI=0.0` and `max_load=1.0` in every seed.

When routing is externally forced (`V3`), specialization is stable. When routing is trainable (`V2`/`V4`), structure is seed-dependent. This supports a trainable routing stability bottleneck, but the exact gradient mechanism remains unproven.

## 7. Forced Feature-Init Verdict

Frozen oracle routing is the clean positive control. It proves that slot-level routing is feasible and useful. Trainable feature-init does not robustly reproduce this behavior.

Final seed-level contrast:

| Variant | seed 20260521 | seed 20260522 | seed 20260523 |
|---|---:|---:|---:|
| `V2_feature_init_trainable` NMI | 0.000 | 0.866 | 0.000 |
| `V4_feature_init_inhibition` NMI | 0.000 | 0.707 | 0.000 |
| `V3_oracle_frozen` NMI | 1.000 | 1.000 | 1.000 |

## 8. Remaining Rival Explanations

Ranked by current plausibility:

1. Trainable top-1 routing instability / route-expert co-adaptation.
2. Feature-init alignment is not strong enough under randomized position.
3. Inhibition loss weight or schedule is too weak or misaligned.
4. Cosine-router scale/normalization may interact with centroid initialization.
5. Residual template/common signals may remain, but oracle success shows they do not make specialization impossible.

## 9. Claim Boundary

Can claim: the no-position/random-position task admits perfect slot-level specialization under oracle routing.

Can claim: the tested trainable router variants do not robustly discover or preserve that specialization.

Cannot claim: all inhibition methods fail, or all feature-init methods fail.

Cannot claim: full multi-B feature-level specialization has been decided.

## 10. Minimal Next Experiments

1. Frozen-oracle-to-trainable release: start with verified oracle specialization, train until accuracy is high, then unfreeze the router and measure when `route_slot_nmi` drops and `max_load` rises.
2. Verified step-0 feature-init: modify/init router until step-0 `NMI=1.0`, then test whether training preserves it without oracle forcing.
3. Release with anti-lock-in controls: compare no regularizer, inhibition, and route-retention regularization after the same verified specialized start.

## Evidence

![Final slot route heatmaps](figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/final_slot_route_heatmaps_by_seed.png)

Interpretation: oracle routing remains specialized in all seeds; trainable feature-init and inhibition only recover structure in seed 20260522.

![Per-seed trajectory](figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/trajectory_by_seed.png)

Interpretation: target accuracy is not diagnostic of specialization because collapsed and specialized runs both reach accuracy 1.0.

CSV/table paths:

- `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/metrics_by_step.csv`
- `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/final_metrics_by_seed.csv`
- `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/summary_by_variant.csv`
- `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/route_matrix_by_step.csv`
- `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/utility_matrix_by_step.csv`
- `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/logit_decomposition_by_step.csv`
- `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/gradient_decomposition_by_step.csv`
