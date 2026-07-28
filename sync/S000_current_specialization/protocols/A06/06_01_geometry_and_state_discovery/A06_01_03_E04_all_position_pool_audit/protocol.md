---
experiment_id: A06_01_03_E04_all_position_pool_audit
anchor_id: A06_01_03_E04_all_position_pool_audit
status: approved_by_user_for_full_run
created: 2026-06-23
canonical_language: en
---

# A06_01_03_E04 Protocol: All-Position Route-Relevant Feature Discovery

## Purpose

A06_01_03_E03 shows that route-position pseudo centers work in the corrected no-position bridge, while all-position clustering can still merge feature classes in C4. This protocol tests whether the merge is caused by using the wrong hidden-state population for clustering.

Decision question: if the router is evaluated at the slot-end route position, should the proxy centers be discovered from all hidden states, only route-position states, slot states, or a label-free route-enriched subset?

## Fixed Setup

- Model: the same one-layer Transformer + top-1 MoE family used in A06_01_03_E03.
- Positional embedding: disabled; no learned absolute position signal.
- Data cell: A06_01_03_E03 `C4_all_position_scope`.
- Sequence length: 32.
- Feature slot length: 4.
- Route position: the last token of the feature slot, offset 3.
- Slot starts: `[2, 10, 18]`.
- Feature, nuisance, and slot-start distribution: strict balanced Cartesian product.
- Number of features / experts: 4 / 4.
- Fitting method: residual k-means with K=4. Feature labels are not used to fit pseudo centers.
- Evaluation: every center set is evaluated only on held-out route-position hidden states.

## Conditions

| Condition | Fit centers on | Why it exists |
| --- | --- | --- |
| Oracle route upper bound | route states grouped by true feature label | checks whether route feature geometry exists |
| Route-only pseudo | route states only, label-free k-means | tests whether unsupervised discovery works when the right state pool is known |
| All-position baseline | every sequence position | reproduces the A06_01_03_E03 C4 boundary |
| Slot-only mixed | all four feature-slot positions | tests whether non-slot states are the main interference |
| Slot offset 0/1/2/3 | one slot offset at a time | tests whether only the route offset carries the separable feature geometry |
| Role-balanced all-position | equal route, non-route-slot, nuisance, and neutral states | tests whether all-position failure is caused by occupancy imbalance |
| Non-slot no-target negative control | positions outside the feature slot and target token | checks whether feature identity leaks outside the slot |

## Primary Metric

Primary metric: held-out route-position `feature_NMI`.

This metric decides the anchor because the intended router decision is feature-level assignment at the slot-end route position. A high value means the fitted centers recover the route-relevant feature partition; a low value means the center set is not usable for feature-level router initialization.

Guard metrics:

- `nuisance_NMI`: high values indicate nuisance-aligned routing.
- `slot_start_NMI`: high values indicate position-aligned routing.
- dominant expert count and load imbalance: low values indicate feature collapse.
- feature-to-expert heatmaps: expose whole-feature merges.
- cluster role composition: shows whether k-means centers were spent on route, slot, nuisance, or neutral states.
- merged-pair route distance: tests whether merged features are genuinely close in route hidden space.

## Decision Rules

Support sample-set mismatch if:

- oracle route upper bound and route-only pseudo both have high route-position `feature_NMI`;
- all-position is lower or has whole-feature merges;
- slot-only, route-only, or role-balanced pools recover the partition.

Support slot-role mixture if:

- route-only and slot offset 3 pass;
- mixed slot or earlier slot offsets fail or merge different features.

Support route-geometry weakness if:

- oracle route works but every label-free candidate pool merges the same nearest feature pairs;
- merged pairs are among the closest route centroids with weak margins.

Insufficient evidence if:

- oracle route upper bound is low;
- k-means is unstable without a consistent failure pattern;
- heatmaps do not show whether failure is merge, nuisance alignment, or load collapse.

## Full-Run Parameters

- Seeds: `20260623` to `20260630`.
- Calibration samples per `(feature, nuisance, slot_start)`: 256.
- Evaluation samples per `(feature, nuisance, slot_start)`: 256.
- Smoke samples per combo: 48.
- Batch size: 1024.
- K-means backend: torch/GPU.
- K-means restarts: 20.
- K-means maximum iterations: 80.

## Outputs

Experiment workspace outputs:

- `tables/pool_comparison.csv`
- `tables/pool_comparison_aggregate.csv`
- `tables/pool_heatmap.csv`
- `tables/pool_mapping_audit.csv`
- `tables/cluster_role_composition.csv`
- `tables/cluster_position_composition.csv`
- `tables/merge_audit.csv`
- `tables/route_feature_distance.csv`
- `tables/route_feature_pca.csv`
- `figures/pool_feature_nmi.png`
- `figures/pool_feature_nmi_heatmap.png`

Research-system outputs:

- `summary.md`
- `detailed.md`
- updated A06_01_03_E04 anchor
- daily meeting brief for A06_01_03_E03 to A06_01_03_E04

## Claim Boundary

This protocol can decide whether all-position clustering is the wrong proxy population in the controlled no-position bridge. It cannot prove real-language semantic feature discovery, RoPE robustness, whole-slot composition, or a deployable DCLM router initializer.

## Addendum: Training-Time Common Subtraction Rescue Audit

**Approval status:** approved by user in chat as an A06_01_03_E04 addendum; completed
locally.

**Purpose:** test whether failed all-position initialization can be rescued by
subtracting common router-input components during training.

**Anchor clause tested:** A06_01_03_E04 says all-position failure is mainly a wrong
state-pool problem. The addendum checks the rival explanation that common bias,
not state-pool mismatch, is the rescuable cause.

**Minimal setup:** use the lowest A06_01_03_E04 all-position failure seeds:
`20260623`, `20260625`, and `20260626`. For each seed, fit all-position
residual k-means centers at step 0 and initialize the router from those centers.

**Conditions:**

| Condition | Router input during training | Initialization | Why needed |
|---|---|---|---|
| raw all-position init | raw post-attention state | raw all-position residual-kmeans centers mapped back to raw space | baseline failed-basin training |
| fixed common subtraction | $h-c_0$ where $c_0$ is step-0 all-position mean | residual centers | tests whether static common removal rescues the basin |
| dynamic common subtraction | $h-\bar h_{\mathrm{batch}}(t)$ using current batch all-position mean | residual centers | tests whether common must be tracked during optimization |

**Primary metric:** held-out route-position `feature_NMI(t)`.

**Pass:** fixed or dynamic common subtraction raises failed seeds to stable
high `feature_NMI` while target accuracy remains valid.

**Fail:** common subtraction improves load but not `feature_NMI`, or the route
partition remains merged.

**Insufficient:** all-position initialization unexpectedly starts already
perfect, target learning fails, or the intervention changes objective validity.

**Cannot claim:** real-DCLM behavior, semantic features, expert utility, or a
general common-subtraction method.

**Result pointer:** `addendum_common_subtraction_rescue/summary.md`.
