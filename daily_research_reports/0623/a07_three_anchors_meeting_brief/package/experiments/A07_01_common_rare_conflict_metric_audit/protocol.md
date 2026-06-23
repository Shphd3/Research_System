# Protocol: A07_01 Common / Rare Conflict Metric Audit

## 0. Approval Snapshot

Approval status: Approved by user execution request on 2026-06-23; full run completed.

Purpose: validate D07 and `Delta_vs_best_null` as the audit surface for later rare-interference method tests.

Primary anchor: `../../problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md`

Anchor decision question: does D07 plus `Delta_vs_best_null` create a valid method-test surface?

Anchor physical prior tested: valid rare-interference data must have oracle-relievable rare loss, comparable null baselines, no dominant shortcut explanation, and readable routed-token conflict signal.

Anchor core model term tested: operational validity of D07 and the oracle-relievable rare-loss gap.

Anchor falsifier: `Delta_vs_best_null <= 0`, oracle leakage, incomparable nulls, shortcut explanation, or unreadable conflict signal.

Experiment role: metric audit / operationalization test.

Primary metric from anchor: `Delta_vs_best_null`.

Claim boundary from anchor: controlled D07 validity only.

Minimal setup: D07 data, dense null, load-only MoE null, oracle feature gate, routed-token hidden-state readout.

Basic configuration: matched objective, budget, evaluation split, and reported compute / parameter differences.

Conditions to run: dense, load-only MoE, oracle feature gate, shortcut-only predictors, routed-token conflict readout.

Pass: positive `Delta_vs_best_null` and all validity guards pass.

Fail: primary gap fails or is explained by leakage, shortcut, or invalid baseline comparison.

Insufficient: missing oracle-variable audit, hidden-state readout, or null-comparability evidence.

Cannot claim: common-control benefit, `RIR_cc`, expert utility, semantic routing, or real-data transfer.

Approval decision: executed as the A07 shared full run on 2026-06-23.

## 1. Anchor Alignment

Decision question: does D07 plus `Delta_vs_best_null` create a valid method-test surface?

Physical prior tested: oracle-relievable rare loss must be measurable without shortcut or leakage.

Core model term tested: rare-loss gap between oracle and best null.

Falsifier: the oracle gap or validity guards fail.

Claim boundary: D07 metric validity only.

## 2. Tested Hypothesis

D07 is valid if the oracle feature gate lowers rare loss beyond the best null while null baselines are comparable, shortcut-only variables fail, and $b_i/g_i$ is readable from $h_i$.

## 3. Rival Explanations

Oracle leakage: oracle uses target, split, loss, future token, or frequency label.

Shortcut surface: position, token identity, nuisance cue, or $r_i$ explains the task.

Null mismatch: oracle wins because of budget, capacity, objective, or split mismatch.

Unreadable conflict signal: oracle can solve the task but learned routing would not have access to $b_i/g_i$ at `B_CONST`.

## 4. Data / Model / Algorithm / Objective

D07 should instantiate `PARENT_a SLOT_s B_CONST -> Y_{a,s}` with balanced evaluation over parent, conflict group, route position, nuisance cue, and rare/common class.

The oracle may use only $b_i$ or $g_i$ for routing. It must not use $y_i$, loss values, future token identity, $r_i$, split identity, or target-derived shortcuts.

Dense, load-only MoE, and oracle-gated MoE must use matched objective, budget, and evaluation split. MoE comparisons should match expert count where possible.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dense null | oracle gap | no partition value | tests partition value | rare/common loss | comparable null | mismatch | missing loss | `d07_metric_audit.csv` |
| Load-only null | oracle gap | load-only solves | tests beyond load balance | rare/common loss | comparable null | matches oracle | missing loss | `d07_metric_audit.csv` |
| Oracle gate | oracle validity | leakage | upper bound | oracle-variable audit | uses only $b_i/g_i$ | forbidden variable | path unclear | `oracle_audit.csv` |
| Shortcut audit | shortcut rival | shortcut surface | protects metric | shortcut predictor scores | below threshold | above threshold | missing manifest | `shortcut_audit.csv` |
| Hidden readout | readability | unreadable route signal | protects later gating test | $h_i\to b_i/g_i$ probe | above threshold | below threshold | no artifact | `router_input_readability.csv` |

Seeds: minimal smoke count first; full count decided at approval.

Checkpoints: only those needed to extract routed-token hidden states for readout.

## 6. Primary Metric

`Delta_vs_best_null = min(L_rare(dense), L_rare(load_only)) - L_rare(oracle_feature_gate)`.

This metric decides whether D07 has oracle-relievable rare conflict beyond the strongest null. False positive cost: testing methods on an invalid surface. False negative cost: discarding a usable surface due to too little power.

## 7. Secondary Metrics

`Delta_vs_dense`, `Delta_vs_load_only`, common loss, total loss, target accuracy, null-comparability checks, shortcut-only predictor scores, and routed-token conflict readout accuracy.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: oracle lowers rare loss while common/total loss stay stable.

Known bad: load-only matches oracle or oracle requires forbidden variables.

Known confusing: oracle helps but $b_i/g_i$ is not readable from $h_i$; later gating failure would be ambiguous.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Data manifest | Are factors balanced? | group counts | pass if eval balanced | `data_manifest.csv` | summary |
| Null comparison | Is oracle gap real? | loss table | pass if primary gap > threshold | `d07_metric_audit.csv` | summary |
| Validity guards | Is gap interpretable? | audits | fail on leakage/shortcut/unreadability | audit tables | detailed |

## 10. Algorithm Specification, If Nontrivial

input: D07 manifest, null models, oracle gate, hidden states.

parameters: oracle-gap threshold, shortcut threshold, readability threshold.

intermediate variables: rare/common losses, oracle gaps, shortcut scores, readout scores.

steps: build manifest; run/evaluate nulls and oracle; audit oracle variables; train/evaluate hidden readout; apply pass/fail rules.

outputs: summary, detailed, tables, central figure.

debug artifacts: manifest, oracle audit, shortcut audit, readout table.

pass conditions: positive primary gap and validity guards pass.

fail conditions: primary gap fails or validity guard fails.

failure reasons: invalid data, invalid oracle, invalid null, shortcut, unreadable route signal.

## 11. Success / Failure / Insufficient Evidence

Success: D07 is valid enough for A07_02.

Failure: D07 cannot support method testing as currently specified.

Insufficient evidence: missing audit artifact or threshold not approved.

## 12. What This Cannot Claim

No common-control benefit, no expert utility, no semantic routing, no real-data transfer.

## 13. Review Notes And Protocol Changes

2026-06-23: user requested execution. Full run used `Delta_vs_best_null > 0.10`, shortcut accuracy `< 0.60`, and readability accuracy `> 0.70`.
