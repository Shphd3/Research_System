# Protocol: A06_01_04_E04 Real-DCLM Proxy-Init Failure Decomposition

## 0. Approval Snapshot

Approval status: Conditional; execute only if A06_01_04_E02 or A06_01_04_E03 fails.
Purpose: localize the first failed stage in the real-data proxy initialization pipeline.
Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Anchor decision question: is the bottleneck proxy instability, linear bridge mismatch, nuisance capture, or training feedback?
Anchor physical prior tested: multi-stage pipelines must be decomposed before method changes.
Anchor core model term tested: \(h\to q\), \(q\to a(0)\), \(a(0)\to a(t)\).
Anchor falsifier: no stage-local metric explains the final failure.
Experiment role: failure decomposition.
Primary metric from anchor: first failed stage contract.
Claim boundary from anchor: bottleneck localization only.
Minimal setup: reuse A06_01_04_E01/A06_01_04_E02/A06_01_04_E03 artifacts.
Conditions to run: only the failed branch plus targeted diagnostics.
Pass: one bottleneck is localized.
Fail: diagnostics remain ambiguous.
Insufficient: missing prior artifacts.
Cannot claim: final solution or broad impossibility.
Approval decision: conditional.

## 1. Anchor Alignment

This protocol is a stage-contract audit, not a method proposal.

## 2. Tested Hypothesis

H1 proxy instability; H2 linear bridge mismatch; H3 training feedback override.

## 3. Rival Explanations

Proxy, bridge, nuisance, and training drift are separated by stage order.

## 4. Data / Model / Algorithm / Objective

Reuse prior artifacts. Add only targeted diagnostics needed for the first unclear failed stage.

## 5. Conditions, Seeds, And Checkpoints

Use the failed A06_01_04_E02/A06_01_04_E03 condition and matching random/proxy controls.

## 6. Primary Metric

First failed stage contract: proxy stability, bridge NMI, or training NMI.

## 7. Secondary Metrics

Center margin, linear classifier upper bound, prototype-router upper bound, nuisance ablations, replay decomposition.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: synthetic A06_01_03_E02/A06_02_01_E01 full pipeline.
Known bad: A06_01_01_E01 low oracle-to-linear agreement.
Known confusing: multiple simultaneous failures.

## 9. Stage-Level Profiling Plan

Create `tables/bottleneck_summary.csv` with stage, metric, threshold, status, evidence path, and next action.

## 10. Algorithm Specification, If Nontrivial

input: prior artifacts.
steps: score stage metrics in order; stop at first failed stage; run one targeted diagnostic; save bottleneck table.
outputs: bottleneck summary and debug figures.

## 11. Success / Failure / Insufficient Evidence

Support: bottleneck localized.
Weaken: no single stage explains failure.
Insufficient: prior artifacts missing.

## 12. What This Cannot Claim

No final method, no broad impossibility, no semantic claim.

## 13. Review Notes And Protocol Changes

2026-06-22: created as conditional failure branch.
