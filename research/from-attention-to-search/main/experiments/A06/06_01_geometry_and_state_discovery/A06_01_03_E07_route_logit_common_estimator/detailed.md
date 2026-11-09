# Detailed: A06_01_03_E07 Route-Logit Common Estimator Under Random-Init Training

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 1. Decision Record

**Decision:** the anchor hypothesis is weakened. The tested route-logit common
estimator is not a reliable feature-recovery method.

**Why:** the primary metric is held-out route-position feature NMI improvement
over raw all-position clustering. Route-logit subtraction has mean
\(\Delta \mathrm{NMI}=-0.014\) and mean margin delta \(-0.080\) over 40
seed-checkpoint cases. It changes load, but does not improve feature recovery.

**Boundary:** this is a controlled no-position mechanism audit. It does not
settle real-DCLM semantic discovery or all possible routing-aware estimators.

## 2. Data Construction

The data follows the controlled A06 no-position bridge.

- Vocabulary size: 4096.
- Sequence length: 32.
- Number of features: 4.
- Number of nuisance ids: 4.
- Number of experts/clusters: 4.
- Feature slot length: 4.
- Slot starts: `[2, 10, 18]`.
- Target depends on the feature slot.
- Routing/evaluation position is the last token of the slot.
- Slot starts, feature ids, and nuisance ids are balanced by construction.

The estimator fits on all-position hidden states. Feature labels, nuisance
labels, slot-start labels, and route-position membership are used only for
post-hoc evaluation and guards.

## 3. Model And Training Setup

- Model: one-layer Transformer + top-1 MoE.
- Hidden dimension: 128.
- Attention heads: 4.
- MoE experts: 4.
- FFN dimension: 256.
- Router metric: dot product.
- Router initialization: equal-norm random router.
- Learned absolute positional embedding: disabled.
- Training steps: 1600.
- Optimizer configuration: learning rate 0.0008, weight decay 0.01, gradient
  clipping 1.0.
- Checkpoints audited: `0, 5, 10, 100, 1600`.
- Seeds: `20260623, 20260624, 20260625, 20260626, 20260627, 20260628,
  20260629, 20260630`.

## 4. Estimators

### Raw all-position baseline

Fit k-means centers on all-position hidden states with no subtraction.

### Route-only control

Fit centers only on route-position states. This is a positive control, not a
label-free method. It answers whether the feature geometry exists at all.

### Mean subtraction

Subtract the global mean direction from all-position hidden states.

### Top-PC subtraction

Subtract the top hidden-state principal components. This tests whether high
variance is a useful common estimate.

### Random-direction subtraction

Subtract a random orthonormal subspace of the same rank. This controls for the
act of removing dimensions.

### Load-sensitive ablation

Select candidate directions by how much subtracting each direction changes
expert load under the current router. This isolates load-only explanations.

### Route-logit subtraction

For a candidate unit direction \(v\), score it by

\[
S_{\mathrm{logit}}(v;t)
=
\operatorname{Var}_i(v^\top h_i(t))
\left\|P_E W_t v\right\|_2^2.
\]

The selected subspace is subtracted before clustering.

## 5. Primary Results

| Estimator | Mean feature NMI | Min feature NMI | Mean delta NMI vs raw | Mean delta margin vs raw | NMI wins / 40 |
|---|---:|---:|---:|---:|---:|
| route-only control | 0.995 | 0.807 | +0.166 | +3.862 | 36 |
| mean subtraction | 0.883 | 0.637 | +0.054 | +0.419 | 16 |
| raw all-position | 0.829 | 0.637 | 0.000 | 0.000 | 0 |
| load-sensitive ablation | 0.831 | 0.628 | +0.002 | +0.006 | 12 |
| route-logit subtraction | 0.815 | 0.637 | -0.014 | -0.080 | 12 |
| random-direction subtraction | 0.810 | 0.000 | -0.020 | +0.084 | 11 |
| top-PC subtraction | 0.798 | 0.637 | -0.031 | -0.598 | 10 |

Step-level route-logit deltas:

| Step | Route-logit mean feature NMI | Delta NMI vs raw | Delta margin vs raw |
|---:|---:|---:|---:|
| 0 | 0.817 | -0.017 | -0.067 |
| 5 | 0.871 | +0.056 | +0.045 |
| 10 | 0.851 | +0.005 | +0.234 |
| 100 | 0.757 | -0.085 | -0.198 |
| 1600 | 0.777 | -0.032 | -0.413 |

The only encouraging route-logit behavior appears at very early checkpoints,
but it is not stable and becomes negative later. Mean subtraction is stronger
at steps 100 and 1600.

## 6. Direction Audit

Route-logit subtraction selected router-contrast directions in every
seed-checkpoint case. Across 40 seed-checkpoint cases, the selected subspace
included:

| Candidate direction | Count |
|---|---:|
| router_contrast_0 | 40 |
| router_contrast_1 | 40 |
| router_contrast_2 | 40 |
| router_contrast_3 | 40 |

Rank-0 winners were distributed across router contrasts:

| Rank-0 candidate | Count |
|---|---:|
| router_contrast_1 | 19 |
| router_contrast_3 | 8 |
| router_contrast_2 | 7 |
| router_contrast_0 | 6 |

Interpretation: the estimator is dominated by router-relative directions. This
is expected from the formula, but it also explains the failure mode: selected
directions can strongly affect current expert logits/load without representing
feature residual geometry.

## 7. Guard Metrics

Shortcut guards are clean.

| Guard | Max NMI |
|---|---:|
| raw nuisance | 0.000142 |
| residual nuisance | 0.000142 |
| raw slot-start | 0.138658 |
| residual slot-start | 0.138658 |

Estimator-level mean nuisance and slot-start NMI are effectively zero. The
negative result is therefore not explained by a nuisance shortcut or obvious
slot-start shortcut.

## 8. Visualization Results

### Feature NMI By Estimator

![Feature NMI by estimator](figures/feature_nmi_by_estimator.png)

Purpose: test whether each estimator recovers the held-out route-position
feature partition.

Setup: centers are fitted after each estimator's subtraction step; evaluation
uses route-position states only.

How to read: higher feature NMI means stronger agreement between assigned
expert and true feature id.

Observed result: route-only control is near perfect; route-logit subtraction
does not beat raw all-position overall; mean subtraction is the best
non-oracle condition.

Take-home: the tested route-logit estimator is not the missing common
estimator.

Remaining uncertainty: a redesigned routing-aware estimator may still work if
it prevents router-contrast directions from winning by load sensitivity alone.

### Load Change By Estimator

![Load change by estimator](figures/load_change_by_estimator.png)

Purpose: test whether the method mainly changes expert load.

Setup: compare expert-load distribution before and after subtracting selected
directions on the all-position fitting pool.

How to read: higher L1 load change means subtraction more strongly changes the
current router's expert allocation.

Observed result: route-logit and load-sensitive ablation change load more than
raw/random controls, but that load change does not produce stable NMI gain.

Take-home: load-changing directions are not equivalent to feature-recovery
directions.

Remaining uncertainty: load may still be a useful guard, but not a primary
selection objective.

### Margin By Estimator

![Margin by estimator](figures/margin_by_estimator.png)

Purpose: test whether the fitted centers define a stronger linear route
surface.

Setup: use fitted centers as router rows and evaluate held-out route-position
margin.

How to read: higher margin means more robust top-1 assignment.

Observed result: route-logit subtraction has negative mean margin delta
relative to raw; mean subtraction has positive margin delta.

Take-home: the route-logit estimator does not create better feature-separating
centers.

Remaining uncertainty: margin-aware selection remains a better next direction
than common-logit subtraction.

### Load Change Versus Feature NMI

![Load change versus feature NMI](figures/load_vs_feature_nmi.png)

Purpose: check whether load change predicts feature recovery.

Setup: each point is an estimator/seed/checkpoint case.

How to read: if load change were sufficient, high-load-change points would
also have high feature NMI.

Observed result: high load change does not consistently correspond to high
feature NMI.

Take-home: load repair is not the same as feature recovery.

Remaining uncertainty: load can still identify harmful common directions, but
it needs a feature-geometry or margin criterion to decide whether removal
helps.

## 9. Failure Analysis

The route-logit score is mathematically sensible but operationally too broad.
It rewards directions with both hidden-state variance and router sensitivity.
Router-contrast directions naturally satisfy the router-sensitivity term.
Subtracting them changes current expert logits and load, but this does not
force the remaining hidden-state space to align with feature centers.

This separates two mechanisms:

1. **Load mechanism:** a direction changes which expert receives tokens.
2. **Feature mechanism:** a direction helps centers separate the four features
   at the route position.

A06_01_03_E07 shows that mechanism 1 does not imply mechanism 2.

## 10. Artifact Map

Experiment folder:
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_03_E07_route_logit_common_estimator/`

Code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/`

Runner:
`scripts/run_a06_20_route_logit_common_estimator_random_init_feature_recovery.py`

Config:
`configs/a06_20_route_logit_common_estimator_random_init_feature_recovery.json`

Run name:
`a06_20_route_logit_common_estimator_full_20260629_010533`

Local logs:

- `logs/local/a06_20_route_logit_common_estimator_full_20260629_010533_shard0.log`
- `logs/local/a06_20_route_logit_common_estimator_full_20260629_010533_shard1.log`
- `logs/local/a06_20_route_logit_common_estimator_full_20260629_010533_aggregate.log`

Curated tables:

- `tables/estimator_comparison.csv`
- `tables/estimator_comparison_with_deltas.csv`
- `tables/decision_delta_table.csv`
- `tables/step_decision_delta_table.csv`
- `tables/direction_audit.csv`
- `tables/shortcut_guard.csv`
- `tables/trajectory_aggregate.csv`
- `tables/snapshot_inventory.csv`
- `tables/feature_heatmap.csv`
- `tables/feature_mapping.csv`
- `tables/run_config.json`
- `tables/args.json`
- `tables/run_summary.json`

Curated figures:

- `figures/feature_nmi_by_estimator.png`
- `figures/load_change_by_estimator.png`
- `figures/load_vs_feature_nmi.png`
- `figures/margin_by_estimator.png`

## 11. Claim Boundary And Next Decision

Supported:

- route-only positive control remains high, so route-position feature geometry
  is present;
- load-changing directions are not sufficient for feature recovery;
- the route-logit common estimator in this protocol should not be promoted.

Weakened:

- the hypothesis that routing-common subtraction, as operationalized by
  \(S_{\mathrm{logit}}\), reveals feature residual centers.

Still open:

- whether a redesigned routing-aware estimator that blocks trivial router
  contrasts can work;
- whether direct margin-aware center search can solve the same problem more
  cleanly;
- whether these controlled findings transfer to real DCLM.

Next decision:

Return to minimal-prior center selection that directly evaluates route-margin
geometry without feature labels or route-position labels. If common estimation
is revisited, the next estimator must explicitly prevent pure router-contrast
load directions from being selected unless they also improve a held-out
feature-geometry proxy.

