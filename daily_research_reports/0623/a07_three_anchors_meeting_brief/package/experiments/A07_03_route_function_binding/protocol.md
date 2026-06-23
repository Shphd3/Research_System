# Protocol: A07_03 Route-Function Binding

## 0. Approval Snapshot

Approval status: Approved by user execution request on 2026-06-23; full run completed.

Purpose: test whether A07_02's rare-loss gain is backed by conflict-conditioned expert function.

Primary anchor: `../../problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md`

Anchor decision question: do routed experts have conflict-group-specific causal utility under forced-routing and fixed-routing ablation?

Anchor physical prior tested: expert specialization requires assignment-function binding.

Anchor core model term tested: route-conditioned utility advantage.

Anchor falsifier: flat utility, selected-best near chance, no route-weighted advantage, nonselective fixed-routing ablation, or invalid forced routing.

Experiment role: causal utility audit.

Primary metric from anchor: route-conditioned utility advantage.

Claim boundary from anchor: controlled D07 route-function binding only.

Minimal setup: A07_02-supported checkpoints with route assignments and group IDs.

Basic configuration: forced-routing preserving non-expert paths; fixed-routing ablation as primary ablation.

Conditions to run: forced-routing matrix, selected-best rate, route-weighted utility, fixed-routing ablation, early/final comparison.

Pass: routed/modal use beats alternatives and fixed-routing ablation is group-specific.

Fail: utility flat, near chance, nonselective, or final-only co-adaptation.

Insufficient: forced routing changes other paths, route IDs missing, early checkpoints missing, or groups too small.

Cannot claim: natural-language semantic experts, robust real-DCLM specialization, deployable routing, one-feature-one-expert structure.

Approval decision: executed as the A07 shared full run on 2026-06-23.

## 1. Anchor Alignment

Decision question: do routed experts have conflict-group-specific causal utility?

Physical prior tested: routing must bind to expert function.

Core model term tested: forced-routing and fixed-route ablation utility.

Falsifier: routed expert use does not beat alternatives.

Claim boundary: D07 causal utility only.

## 2. Tested Hypothesis

If A07_02 is real expert specialization, routed expert use should lower group loss and fixed-route ablation should selectively damage that group.

## 3. Rival Explanations

Interchangeable experts: utility matrix is flat.

Diffuse routing: no modal expert is meaningful.

Final co-adaptation: utility appears only at final checkpoint.

Invalid ablation: rerouting changes the tested object.

Forced-routing artifact: forced routing changes non-expert computation paths.

## 4. Data / Model / Algorithm / Objective

Use only A07_02-supported checkpoints. For each conflict group, compute route distribution $P(e\mid g)$.

If $\max_e P(e\mid g)$ exceeds the approved threshold, use modal expert readout. Otherwise use route-distribution-weighted utility.

Forced routing may override only expert choice; token inputs, residual streams, non-expert paths, and objective must remain unchanged.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Route distribution | core model | diffuse routing | choose readout | $P(e\mid g)$ | threshold applied | no valid readout | IDs missing | `route_distribution_by_group.csv` |
| Forced utility | H1 | flat utility | primary evidence | utility matrix | advantage | flat/chance | invalid force | `forced_utility_matrix.csv` |
| Selected-best | H1 | chance match | sanity guard | selected-best vs $1/E$ | above chance | near chance | small groups | `selected_best_rate.csv` |
| Fixed ablation | H2 | nonselective experts | causal guard | ablation deltas | selective | nonselective | rerouting | `fixed_routing_ablation_selectivity.csv` |
| Early/final | H3 | co-adaptation | temporal guard | checkpoint comparison | stable/early | final only | missing ckpt | `early_final_utility.csv` |

Seeds: inherit A07_02 supported seeds.

Checkpoints: initialization, early, final when available.

## 6. Primary Metric

Route-conditioned utility advantage.

Use modal utility gap when route concentration passes threshold. Otherwise use route-weighted utility gap: compare $CE_{g,\mathrm{route}}$ with uniform or alternative expert utility.

## 7. Secondary Metrics

Selected-best rate, chance baseline $1/E$, utility entropy, fixed-routing ablation selectivity, rerouting-enabled ablation as secondary diagnostic, early/final stability.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: routed/modal expert beats alternatives and fixed-route ablation selectively hurts the same group.

Known bad: flat utility matrix and selected-best near $1/E$.

Known confusing: final-only utility; treat as co-adaptation risk.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Dependency | Did A07_02 pass? | A07_02 summary | stop if not passed | dependency note | protocol |
| Route readout | Modal or weighted? | route distribution | choose by threshold | route table | detailed |
| Utility | Is routed use useful? | forced matrix | primary metric | heatmap | summary |
| Ablation | Is function selective? | fixed ablation | guard | ablation table | detailed |

## 10. Algorithm Specification, If Nontrivial

input: A07_02 checkpoints, route assignments, expert IDs, conflict group IDs.

parameters: route concentration threshold, minimum group size, utility margin threshold.

intermediate variables: $P(e\mid g)$, $CE_{g,e}$, selected-best rate, ablation deltas.

steps: verify A07_02; compute route distributions; run forced-routing; compute route-conditioned utility; run fixed-routing ablation; compare checkpoints.

outputs: summary, detailed, tables, figures.

debug artifacts: route table, utility matrix, ablation matrix, early/final comparison.

pass conditions: utility advantage and fixed-ablation selectivity pass.

fail conditions: flat utility, chance selected-best, nonselective ablation.

failure reasons: no utility binding, co-adaptation only, invalid forced routing, invalid ablation.

## 11. Success / Failure / Insufficient Evidence

Success: A07_02 gain has controlled route-function binding evidence.

Failure: A07_02 may be useful but not expert-specialization evidence.

Insufficient: dependency missing, forced-routing invalid, ablation invalid, or checkpoints missing.

## 12. What This Cannot Claim

No natural-language semantic experts, no robust real-DCLM specialization, no deployable routing, no one-feature-one-expert theorem.

## 13. Review Notes And Protocol Changes

2026-06-23: user requested execution. Full run used route concentration `> 0.60` and utility margin `> 0.20`.
