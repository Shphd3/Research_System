---
protocol_id: A07_E02_text_static_expert_geometry_transfer
anchor_id: A07_high_dim_uniform_expert_geometry_gate
status: proposed_after_A07_E01
created: 2026-06-16
canonical_language: en
---

# Protocol A07_E02: Text-Facing Static Expert-Geometry Transfer

## Purpose

Decide which static expert-geometry score is the best bridge from synthetic uniform features to real or semi-real text hidden states.

## Decision Question

Among centered/calibrated full M4, weighted low-rank M4, top-r projection, prototype baselines, and linear router surrogates, which method best preserves expert preference, load control, and robustness on text hidden-state distributions?

## Key Boundary

This protocol does not claim semantic expert specialization. Text labels are diagnostics. The main target is whether a static expert-geometry score remains stable when the feature distribution is no longer uniform or isotropic.

## Setup

Hidden states:

```text
source: frozen transformer or toy LM hidden states
layer: fixed layer l
positions: controlled routed positions plus natural text positions
samples: balanced by corpus slice when possible
```

Expert matrices:

```text
source A: random initialized expert matrices
source B: trained or partially trained expert matrices if available
source C: synthetic experts embedded into hidden dimension for controlled tests
```

Preprocessing variants:

```text
raw hidden state h
mean-centered h - E[h]
whitened hidden state Sigma^{-1/2}(h - E[h])
common-controlled h with top common direction removed
router-only controlled h while expert input remains full h
```

## Methods

Full empirical-centered M4:

```math
q_e(h)=h^TG_eh - \mathbb{E}_{h\sim\mathcal{D}_{ref}}[h^TG_eh].
```

Quantile-calibrated M4:

```math
q_e(h)=h^TG_eh-\tau_e.
```

Weighted low-rank M4:

```math
q^{(r)}_e(h)=\sum_{k=1}^r \sigma_{e,k}^2(v_{e,k}^T h)^2-c_{e,r}.
```

Unweighted top-r projection:

```math
q^{(r,unw)}_e(h)=\sum_{k=1}^r(v_{e,k}^T h)^2-c_{e,r}.
```

Prototype baselines:

```text
M1/M2 only with explicit sign or line convention;
otherwise report as sign-sensitive controls.
```

Linear router surrogate:

```text
fit a linear classifier to centered-M4 oracle labels;
measure how much M4 can be approximated by a dot-product router.
```

## Metrics

Primary:

```text
load_error
mean_margin
low_margin_fraction
agreement_with_full_centered_M4
rank_needed_for_90_percent_agreement
common_sensitivity = route change after common removal
calibration_margin_retention
```

If forced routing is available:

```text
utility_best_expert
router_or_metric_to_utility_match
loss_delta_best_minus_selected
```

Diagnostic only:

```text
part_of_speech_NMI
syntax_label_NMI
format_label_NMI
token_frequency_stratified_load
position_stratified_load
```

## Procedure

1. Extract hidden states from fixed layers and positions.
2. Split data into calibration and evaluation sets.
3. Estimate hidden-state mean, covariance, and common directions on calibration data.
4. Compute expert geometry `G_e` and its top singular directions.
5. Compute all static routing scores under all preprocessing variants.
6. Fit thresholds on calibration data only.
7. Evaluate load, margin, and agreement on held-out data.
8. If possible, force-route held-out hidden states to each expert and measure loss/logit utility.
9. Report text labels only as diagnostics, not as proof of utility.
10. Select the method most suitable for the next trainable-router experiment.

## Success Criteria

A method is considered suitable for real text if:

```text
load is controllable without margin collapse;
agreement with full centered M4 is high or the method has stronger utility match;
common-direction sensitivity is lower than raw dot-product routing;
rank requirement is modest;
results are stable across corpus slices, positions, and layers;
text-label correlations do not contradict utility evidence.
```

## Failure Criteria

A method is weakened if:

```text
it only balances load after destroying margin;
it is dominated by token frequency, position, or common direction;
it has poor agreement with M4 and poor utility match;
it depends on arbitrary SVD signs;
it requires a rank close to full dimension to behave well.
```

## Expected Decision

The expected best bridge is not raw M4 and not M1/M2. The leading candidate is empirical-centered or calibrated weighted low-rank M4:

```math
q^{(r)}_e(h)=\sum_{k=1}^r \sigma_{e,k}^2(v_{e,k}^T h)^2-c_{e,r},
```

with thresholds fit on a calibration set. This keeps the matrix-response prior, avoids prototype sign dependence, scales better than full M4, and can be common-controlled for text hidden states.

## Expected Artifacts

```text
tables/text_static_metric_summary.csv
tables/layer_position_breakdown.csv
tables/common_sensitivity.csv
tables/utility_match.csv
figures/load_margin_by_method.png
figures/agreement_vs_rank.png
figures/common_control_effect.png
summary.md
detailed.md
```
