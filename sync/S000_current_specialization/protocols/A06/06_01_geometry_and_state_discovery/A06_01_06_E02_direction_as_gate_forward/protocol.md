# Protocol: A06_01_06_E02 Direction As Gate-Forward

## 0. Approval Snapshot

Approval status: executed under the user's four-card A08 run request on 2026-06-28.

Purpose: test whether a converged singular direction can be converted into a gate row that routes examples by the intended feature.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_06_spectral_reservoir_method_audit_anchor.md`

Anchor decision question: can a converged singular direction be converted into a useful gate-forward row?

Anchor physical prior tested: stable read/write directions can act as stable routing axes.

Anchor core model term tested: $q(x)=\arg\max_e g_e^\top h(x)$ with $g_e\propto v_e$.

Anchor falsifier: direction-derived routes are no better than random or norm controls.

Experiment role: operationalization / proxy test.

Primary metric from anchor: feature-route NMI.

Claim boundary from anchor: controlled direction-to-gate conversion only.

Minimal setup: use A06_01_06_E01 converged directions on nested synthetic checkpoints; initialize gate rows from directions and compare random/norm/shuffled controls.

Basic configuration: 8 seeds, fixed checkpoint from A06_01_06_E01 stable window.

Conditions to run: `direction_gate`, `random_equal_norm_gate`, `shuffled_direction_gate`, `oracle_feature_gate`.

Pass: direction gate has high feature-route NMI and beats random/norm/shuffled controls.

Fail: no route identity or identity explained by norm/frequency.

Insufficient: A06_01_06_E01 convergence threshold did not pass.

Cannot claim: early training preservation or utility.

Approval decision: execute after A06_01_06_E01 stable directions are identified.

## 1. Anchor Alignment

Decision question: direction-to-gate conversion.

Physical prior tested: stable singular direction is a routing axis.

Core model term tested: gate row alignment.

Falsifier: route NMI near random.

Claim boundary: synthetic operationalization.

## 2. Tested Hypothesis

Converged singular directions initialize gate rows that recover known feature partitions.

## 3. Rival Explanations

Routes may follow vector norm, frequency, token position, or label leakage.

## 4. Data / Model / Algorithm / Objective

Use A06_01_06_E01 checkpoints and hidden states. No training is required for the first gate read; this is a forward-routing audit.

## 5. Conditions, Seeds, And Checkpoints

| Item | Why needed | Evidence |
| --- | --- | --- |
| direction gate | primary operationalization | feature-route NMI |
| random equal norm | norm/load control | NMI/load table |
| shuffled direction | false-positive guard | NMI table |
| oracle feature gate | upper bound | NMI/loss table |

## 6. Primary Metric

Feature-route NMI on held-out synthetic examples.

## 7. Secondary Metrics

Max load, active experts, route entropy, nuisance NMI, route margin.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: oracle feature gate.

Known bad: shuffled direction gate.

Known confusing: high NMI with collapsed load.

## 9. Stage-Level Profiling Plan

Audit route identity, load, nuisance correlation, and gate margins.

## 10. Algorithm Specification, If Nontrivial

input: converged directions, held-out hidden states, feature labels for audit.

steps: create gate rows, route held-out states, compute NMI and guards.

## 11. Success / Failure / Insufficient Evidence

Success: direction-derived gates recover feature routes.

Failure: directions do not define route-forward partitions.

Insufficient: convergence source failed.

## 12. What This Cannot Claim

No training preservation or utility claim.

## 13. Review Notes And Protocol Changes

This bridges r1's "direction fixed -> gating forward fixed" intuition.

2026-06-28: full run `a08_singular_preservation_full_20260628_2` completed.
Result supports direction-to-gate conversion on the controlled surface. A
single random-control spike was retained as a future guard.
