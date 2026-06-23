# Protocol: A07_02 Common-Controlled Rare Interference

## 0. Approval Snapshot

Approval status: Approved by user execution request on 2026-06-23; full run completed.

Purpose: test whether label-free common-control lowers rare loss beyond matched balance-only MoE.

Primary anchor: `../../problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md`

Anchor decision question: on A07_01-valid D07, does label-free common-control beat load-matched balance-only MoE on rare loss?

Anchor physical prior tested: common-logit bias can block conflict-conditioned routing, and common-control should help only if it preserves conflict signal.

Anchor core model term tested: method-level effect of $\phi(h_i)$ on rare loss.

Anchor falsifier: nonpositive `RIR_cc`, unmatched load comparison, conflict-signal removal, or label leakage.

Experiment role: method construction after validated metric surface.

Primary metric from anchor: `RIR_cc`.

Claim boundary from anchor: controlled D07 method benefit only.

Minimal setup: A07_01-passing D07, matched balance-only MoE, one or two label-free common-control variants.

Basic configuration: match load, budget, objective, split, and report `FoO_cc`.

Conditions to run: balance-only, common-control variant(s), conflict-signal readout before/after $\phi$, label-free audit.

Pass: positive `RIR_cc` under matched-load comparison, with loss and signal guards passing.

Fail: rare-loss gain absent, load-only, signal-erasing, or label-leaking.

Insufficient: A07_01 not passed, missing matched-load table, or missing conflict-signal readout.

Cannot claim: expert utility, semantic routing, route-function binding, real-language transfer, deployable architecture.

Approval decision: executed as the A07 shared full run on 2026-06-23.

## 1. Anchor Alignment

Decision question: does common-control reduce rare loss beyond matched balance-only MoE?

Physical prior tested: common bias can hide conflict signal, but common removal must preserve $q_{b_i}$.

Core model term tested: $z'_{i,e}=w_e^T\phi(h_i)$.

Falsifier: no rare-loss gain under fair comparison.

Claim boundary: method benefit only.

## 2. Tested Hypothesis

Label-free common-control has positive `RIR_cc` and recovers positive `FoO_cc` without better load balance being the explanation.

## 3. Rival Explanations

Load-only gain: common-control wins only because load is better.

Signal removal: $\phi$ removes conflict signal, making failure ambiguous.

Label leakage: $\hat c$ or logit cancellation uses parent, conflict, rare/common, target, oracle centroid, or eval metadata.

Optimization mismatch: budget, objective, or split differs from baseline.

## 4. Data / Model / Algorithm / Objective

Use A07_01-approved D07 and `Delta_vs_best_null`.

Common-control may use unlabeled hidden-state statistics, batch averages, early-window averages, or fixed unsupervised centering. It may not use labels or oracle centroids.

Experts receive full $h_i$ unless explicitly audited otherwise; routing uses $\phi(h_i)$ or logit-side common cancellation.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Balance-only | matched null | load-only | main comparator | loss/load table | matched | mismatch | missing | `matched_load_guard.csv` |
| Common-control | H1 | no method effect | candidate | `RIR_cc` | positive | nonpositive | A07_01 missing | `common_control_rir.csv` |
| Load match | H2 | anti-collapse only | fair comparison | max load/experts/entropy | within tolerance | outside tolerance | no trajectory | `matched_load_guard.csv` |
| Signal readout | H3 | signal removal | protects mechanism | before/after $\phi$ readout | preserved | collapsed | missing | `conflict_signal_preservation.csv` |
| Checkpoint save | A07_03 dependency | co-adaptation | enables utility audit | manifest | saved | missing | unclear ids | `checkpoint_assignment_manifest.csv` |

Seeds: smoke first, full count after metric extraction works.

Checkpoints: initialization, early, final; save route assignments, expert IDs, and group IDs.

## 6. Primary Metric

`RIR_cc = L_rare(balance_only) - L_rare(common_control)`.

This metric decides whether common-control improves rare loss beyond the null. It is valid only after A07_01 passes and load comparison is matched.

## 7. Secondary Metrics

`FoO_cc = RIR_cc / Delta_vs_best_null`, rare/common/total loss, max load, active experts, entropy, load objective strength, conflict readout before/after $\phi$, and conflict margin before/after $\phi$.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: positive `RIR_cc`, positive `FoO_cc`, matched load, preserved conflict signal.

Known bad: load improves but rare loss does not.

Known confusing: rare loss improves while load is not matched; this supports anti-collapse, not common-control-specific benefit.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Dependency | Did A07_01 pass? | A07_01 summary | stop if not passed | dependency note | protocol |
| Method effect | Does rare loss improve? | loss table | primary metric | `common_control_rir.csv` | summary |
| Validity guards | Is effect interpretable? | load/signal/audit tables | fail if guard fails | guard tables | detailed |

## 10. Algorithm Specification, If Nontrivial

input: A07_01-valid data, balance-only baseline, common-control variants.

parameters: matched-load tolerance, common-control window, threshold for signal preservation.

intermediate variables: rare loss, common loss, load metrics, conflict readouts, route assignments.

steps: verify A07_01; run matched baseline and common-control; compute `RIR_cc` and `FoO_cc`; audit load, labels, and signal; save checkpoints.

outputs: summary, detailed, tables, figures, checkpoint manifest.

debug artifacts: label-free audit, readout table, load table.

pass conditions: positive `RIR_cc` and all guards pass.

fail conditions: no gain, unfair load, signal removal, or leakage.

failure reasons: method ineffective, null too strong, control removes signal, invalid implementation.

## 11. Success / Failure / Insufficient Evidence

Success: common-control has controlled D07 rare-interference benefit.

Failure: common-control is not supported as a method benefit beyond matched load.

Insufficient: missing dependency, matched-load table, signal readout, or checkpoint manifest.

## 12. What This Cannot Claim

No route-function binding, no causal expert specialization, no real-language transfer, no deployable architecture.

## 13. Review Notes And Protocol Changes

2026-06-23: user requested execution. Full run used matched max-load tolerance `0.08`; common-control variant was unlabeled mean-centering plus k-means routing.
