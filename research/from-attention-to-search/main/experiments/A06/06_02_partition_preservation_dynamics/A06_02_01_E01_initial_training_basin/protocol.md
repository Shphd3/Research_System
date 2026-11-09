# Protocol: A06_02_01_E01 Training Basin Preservation

## 0. Approval Snapshot

Approval status: Executed full run on 2026-06-22 after user approval.
Purpose: decide whether feature-aligned initialization alone preserves feature routing during ordinary top-1 training.
Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`
Anchor decision question: does a feature-aligned step-0 initialization preserve feature_NMI while the model learns?
Anchor physical prior tested: good initialization may define a specialization basin, but top-1 training may override it.
Anchor core model term tested: \(a_i(t)=\arg\max_e w_e(t)^\top h_i(t)\) and \(NMI(f_i,a_i(t))\) over training.
Anchor falsifier: high step-0 NMI becomes low final NMI while accuracy is acceptable.
Experiment role: training-dynamics diagnostic.
Primary metric from anchor: held-out `feature_NMI(t)` and final `feature_NMI`; accuracy is a constraint.
Claim boundary from anchor: synthetic uniform feature task only.
Minimal setup: matched `slot_token_len=4` training runs from random, equal-norm random, oracle centroid, and conditional A06_01_03_E02 pseudo initialization.
Basic configuration: repeated four-token `SLOT_s` span, route position at the last slot token (`pair_start + 3`); no anti-lockin; same schedule; evaluate step 0, early checkpoints, final checkpoint.
Conditions to run: `random_gaussian_init`, `equal_norm_random_init`, `oracle_feature_centroid_init`, `label_shuffled_centroid_guard`, conditional `best_A06_08_pseudo_center_init` if A06_01_03_E02 has a passing clustering / spectral / dictionary method.
Pass: oracle init preserves high final NMI with acceptable accuracy; pseudo is judged only if A06_01_03_E02 passed.
Fail: oracle starts high but final NMI collapses or features merge under acceptable accuracy.
Insufficient: missing step-0 audit, NMI trajectory, accuracy constraint, matched schedule, or A06_01_03_E02 dependency audit.
Cannot claim: anti-lockin solved, real DCLM transfer, expert utility, semantic specialization, final router method.
Approval decision: approved and executed.

## 1. Anchor Alignment

The protocol tests whether initialization defines a preserved training basin. The model term is `feature_NMI(t)` under matched ordinary top-1 training. The boundary is synthetic training only.

## 2. Tested Hypothesis

H1: oracle centroid init preserves specialization. Supported if final NMI remains high with acceptable accuracy; weakened if NMI collapses or routes merge.

H2: passed A06_01_03_E02 pseudo init transfers. Supported if pseudo remains closer to oracle than random; weakened if pseudo becomes random-like.

## 3. Rival Explanations

- Accuracy-only success: separated by feature_NMI.
- Load-only success: separated by route heatmaps and NMI.
- Bad initialization: separated by step-0 audit.
- Pseudo discovery failure: pseudo condition included only if A06_01_03_E02 passes.

## 4. Data / Model / Algorithm / Objective

Data: uniform synthetic four-feature task with `slot_token_len=4` and held-out labels for metrics. Each example contains a repeated four-token `SLOT_s` span followed immediately by `TARGET_s`; background tokens are independent of pair id. Model: top-1 MoE with four experts. Algorithm: initialize router by condition, train with matched ordinary schedule, evaluate checkpoints. Objective: cross entropy for predicting the target token from the last slot position; full-sequence next-token loss is reported only as a diagnostic because random background tokens are not learnable. Specialization is judged by NMI.

## 5. Conditions, Seeds, And Checkpoints

Seeds: A06 seed set unless a smoke subset is explicitly approved. Checkpoints: step 0, early checkpoints, final checkpoint. Main data setting: `slot_token_len=4`, route at the last slot position.

| Item | Why needed | Evidence |
| --- | --- | --- |
| `random_gaussian_init` | baseline | trajectory/final tables |
| `equal_norm_random_init` | row-norm guard | trajectory/final tables |
| `oracle_feature_centroid_init` | core basin test | `figures/nmi_trajectory.png` |
| `label_shuffled_centroid_guard` | artifact guard | final table |
| conditional `best_A06_08_pseudo_center_init` | label-free bridge from the best passing A06_01_03_E02 discovery family | NMI trajectory |

## 6. Primary Metric

Held-out `feature_NMI(t)` and final held-out `feature_NMI`. It decides because the question is route preservation; accuracy and load alone are insufficient.

Support threshold: oracle final `feature_NMI >= 0.80`, NMI drop no more than `0.15`, and acceptable accuracy.

Failure threshold: oracle step-0 `feature_NMI >= 0.95` but final `feature_NMI < 0.50`, or drop greater than `0.30` with acceptable accuracy.

## 7. Secondary Metrics

Task accuracy, load \(L(t)\), margin p05, feature purity, many-to-one merge count, route-change rate, route heatmaps.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: oracle init should start with high NMI. Known bad: random baselines are not specialization evidence. Known confusing: high accuracy with low NMI is failure for this anchor.

## 9. Stage-Level Profiling Plan

| Stage | Rule | Artifact |
| --- | --- | --- |
| dependency audit | pseudo only if A06_01_03_E02 passed | `tables/dependency_audit.csv` |
| step-0 audit | oracle high NMI required | `tables/initialization_audit.csv`, `tables/training_trajectory.csv` |
| trajectory | apply NMI thresholds | `tables/training_trajectory.csv` |
| accuracy guard | success requires acceptable accuracy | `tables/trajectory_aggregate.csv`, `figures/accuracy_trajectory.png` |
| merge analysis | identify merge/collapse | `figures/route_heatmaps_step0_final.png` |

## 10. Algorithm Specification, If Nontrivial

Input: `slot_token_len=4` synthetic train/eval data, initialization condition, training schedule. Parameters: learning rate, steps, batch size, initialization scale, checkpoints. Steps: initialize router; evaluate step-0 route metrics; train on route-position target cross entropy; evaluate route and accuracy at checkpoints; aggregate by condition and seed. Outputs: `summary.md`, `detailed.md`, trajectory tables, final table, `figures/nmi_trajectory.png`, `figures/accuracy_trajectory.png`, and `figures/route_heatmaps_step0_final.png`. Failure reasons: top-1 lock-in, representation drift, expert co-adaptation, low margin, bad pseudo init.

## 11. Success / Failure / Insufficient Evidence

Support: oracle, and pseudo if available, preserve high final NMI with acceptable accuracy. Partial support: oracle survives but pseudo fails. Weaken: oracle starts high and collapses; next step is anti-lockin. Insufficient: missing step-0 audit, NMI trajectory, accuracy constraint, or dependency audit.

## 12. What This Cannot Claim

No claim about real DCLM, expert utility, semantic specialization, deployable router, or anti-lockin solution.

## 13. Review Notes And Protocol Changes

2026-06-22: compressed to initialization-only basin preservation. Anti-lockin is the next anchor only if this fails.
2026-06-22: main run fixed to `slot_token_len=4`; route readout is the last slot token.
2026-06-22: pseudo init is conditional on A06_01_03_E02 passing under one of clustering, spectral, or dictionary discovery.
2026-06-22: training objective fixed to route-position target prediction; random background full-sequence NTP is diagnostic only.
2026-06-22: full four-GPU ACP run completed as `a06_09_training_basin_full_20260622_2`; job id `pt-epdfv6pd`.
