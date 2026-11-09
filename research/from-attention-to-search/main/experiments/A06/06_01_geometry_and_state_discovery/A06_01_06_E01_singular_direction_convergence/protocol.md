# Protocol: A06_01_06_E01 Singular Direction Convergence Metric

## 0. Approval Snapshot

Approval status: executed under the user's four-card A08 run request on 2026-06-28.

Purpose: define when a singular direction is stable enough to be treated as a fixed gate-forward direction.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question: what operational threshold makes a singular direction safe to treat as fixed for gating?

Anchor physical prior tested: direction drift can become small while singular gain continues to grow.

Anchor core model term tested: \(K_i(t)=\|P_i(t)-P_i(t-\Delta)\|_2\) and \(G_i(t)=\sigma_i(t)-\sigma_i(t-\Delta)\).

Anchor falsifier: low drift is unrelated to known feature readout, or drift/gain do not separate.

Experiment role: metric audit.

Primary metric from anchor: low \(K_i\) with positive \(G_i\) and stable known-feature alignment.

Claim boundary from anchor: synthetic/convergence metric only.

Minimal setup: reuse A07 nested rank-one and add a wide controlled guard. Save checkpoints and compute singular direction drift, gain, and known-feature alignment.

Basic configuration: 8 seeds; nested skewed and balanced guard; rank-one and wide small MLP variants.

Conditions to run: `rank1_nested`, `wide_nested`, `balanced_guard`, `shuffled_feature_guard`.

Pass: a stable window exists where \(K_i\) is low, \(G_i\) remains positive, and known-feature alignment is stable.

Fail: no stable window exists or low drift does not correspond to feature readout.

Insufficient: checkpoint matrices are missing or feature direction is not known.

Cannot claim: real-DCLM convergence, preservation, gating method success, or utility.

Approval decision: execute as synthetic metric audit before A06_01_06_E02.

## 1. Anchor Alignment

Decision question: define singular-direction convergence.

Physical prior tested: direction convergence and gain growth separate.

Core model term tested: \(K_i\) and \(G_i\).

Falsifier: convergence metric does not predict stable feature readout.

Claim boundary: controlled synthetic metric.

## 2. Tested Hypothesis

A feature direction can enter a low-drift window while its singular gain still grows.

## 3. Rival Explanations

Low drift may be numerical saturation, rank collapse, or unrelated to the known feature.

## 4. Data / Model / Algorithm / Objective

Use nested synthetic data with known feature directions. Train CE/AdamW models and compute top singular projectors per checkpoint.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Why needed | Evidence |
| --- | --- | --- | --- |
| rank1 nested | mentor minimal model | known-good mechanism surface | drift/gain curve |
| wide nested | robustness guard | checks whether metric survives capacity | drift/gain curve |
| balanced guard | frequency rival | checks frequency dependence | table |
| shuffled feature guard | feature-readout rival | checks false positives | table |

## 6. Primary Metric

Stable convergence window:

\[
K_i(t)\le \kappa,\qquad G_i(t)>0,\qquad |\Delta a_i(t)|\le \epsilon_a.
\]

## 7. Secondary Metrics

Per-level loss, known-feature alignment, singular energy, effective rank.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: A07_01 rank-one nested surface.

Known bad: shuffled features should not show meaningful feature-readout stability.

Known confusing: wide model may rotate multiple equivalent directions.

## 9. Stage-Level Profiling Plan

Profile data validity, checkpoint spectra, drift/gain windows, and feature alignment.

## 10. Algorithm Specification, If Nontrivial

input: nested data config, checkpoint matrices, known feature directions.

steps: train, checkpoint, compute SVD, compute \(K_i/G_i/a_i\), aggregate, plot.

## 11. Success / Failure / Insufficient Evidence

Success: stable convergence threshold is supported.

Failure: convergence is not operationally meaningful.

Insufficient: missing checkpoints or feature direction labels.

## 12. What This Cannot Claim

No real-data or method claim.

## 13. Review Notes And Protocol Changes

This protocol turns r1's "define converge" request into the first A08 metric audit.

2026-06-28: full run `a08_singular_preservation_full_20260628_2` completed.
Result is supported for the rank-one nested surface and insufficient for wide
robustness.
