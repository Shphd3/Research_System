# Execution Plan: H0528a Router Prior Decay Audit

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

Use H0527a artifacts to answer:

```text
At final checkpoint, does the current hidden representation still contain a recoverable B-context semantic boundary, and does the trained router use it?
```

This is an offline audit. It must not introduce a new training method or new router objective.

## 2. Artifact Reality Check

H0527a saved final `model.pt` for each condition/seed and per-step routing CSVs, but did not save intermediate model checkpoints. Therefore H0528a cannot honestly compute `frozen_init` / `recentered` / `trained` comparisons at steps `200/400/800/1200`.

The valid minimum audit is:

```text
step 0: reconstruct initial model / router
step 1600: load final model.pt
```

Per-step H0527a trajectory CSVs may be used only as supporting context for actual trained-router NMI decay, not as full checkpoint replay evidence.

## 3. Data Construction

Use the same H0527a data generation and config.

Two independent splits:

```text
calibration split: estimate recentered semantic router C^t
audit split: evaluate router NMI, heatmaps, load entropy, and forced utility
```

This avoids fitting \(C^t\) and evaluating it on the same B-source hidden states.

## 4. Model / Evaluation Setup

Source final checkpoints:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0527a_router_initialization_trajectory/h0527a_router_initialization_4gpu_20260524/
```

Conditions:

```text
random_init
semantic_context_init
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Router variants evaluated:

| Router variant | Meaning |
|---|---|
| `frozen_init` | reconstruct condition-specific step-0 router and apply it to final hidden states |
| `recentered_current` | estimate whitened B-context directions from current hidden states and evaluate on held-out audit hidden states |
| `trained_final` | actual trained final router from `model.pt` |

## 5. Metrics And Artifacts

Primary metric:

\[
\Delta_{\text{unused}}
=
\mathrm{NMI}(r_{C^{1600}}(h^{1600}),\kappa)
-
\mathrm{NMI}(r_{W^{1600}}(h^{1600}),\kappa).
\]

Supporting metrics:

```text
NMI(frozen_init, B-context)
NMI(recentered_current, B-context)
NMI(trained_final, B-context)
load entropy by router variant
B-context routing heatmap
forced-routing utility margin at final checkpoint
```

Required tables:

```text
tables/router_nmi_by_condition_seed_variant.csv
tables/router_load_by_condition_seed_variant.csv
tables/b_context_routing_by_condition_seed_variant.csv
tables/forced_utility_by_condition_seed_group.csv
tables/forced_utility_margin_by_condition_seed_group.csv
tables/artifact_availability.csv
```

Required figures:

```text
figures/router_nmi_comparison.png
figures/unused_semantic_gap_by_seed.png
figures/b_context_routing_heatmap_by_variant.png
figures/forced_utility_margin_heatmap.png
```

Every report figure must have one sentence explaining what it shows.

## 6. Pass / Fail Criteria

Valid audit requires:

```text
all 8 final H0527a model.pt files exist
step-0 routers are reconstructable from config and seed
calibration and audit splits are separated
recentered router uses only calibration hidden states
evaluation uses router input h before MoE dispatch
missing intermediate checkpoints are explicitly reported
```

Stop condition:

```text
If final checkpoints are missing or cannot be loaded, stop and write a failure audit instead of inferring from CSVs alone.
```

## 7. Decision Rules

Case A:

```text
recentered_current high, trained_final low
```

Interpretation:

```text
semantic boundary still exists in current representation, but trained router does not use it.
```

Case B:

```text
recentered_current low, trained_final low
```

Interpretation:

```text
current representation or B-context centroid definition no longer supports this semantic partition.
```

Case C:

```text
recentered_current high, trained_final low, forced utility margin small
```

Interpretation:

```text
semantic routing is recoverable, but expert utility is underdetermined under the task loss.
```

Case D:

```text
recentered_current high, trained_final low, forced utility margin large
```

Interpretation:

```text
router objective / credit assignment failed to use an available useful semantic boundary.
```

## 8. Result Location

Curated reports:

```text
main/experiments/H0521_router_feature_specialization/H0528a_router_prior_decay_audit/summary.md
main/experiments/H0521_router_feature_specialization/H0528a_router_prior_decay_audit/detailed.md
main/experiments/H0521_router_feature_specialization/H0528a_router_prior_decay_audit/reliability_audit.md
```

Raw outputs stay under ignored experiment result directories.
