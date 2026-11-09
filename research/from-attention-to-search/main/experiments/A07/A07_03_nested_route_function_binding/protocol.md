# Protocol: A07_03 Nested Route-Function Binding

## 0. Approval Snapshot

Approval status: user requested immediate sequential protocols and experiments on 2026-06-28.

Purpose: test, conditionally and conservatively, whether a routed expert has nested-level-specific causal utility rather than only route-label alignment.

Primary anchor: `../../../problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md`

Anchor decision question: conditional on route preservation, do routed experts have nested-level-specific causal utility?

Anchor physical prior tested: assignment and function can be unbound, so utility requires forced-routing and fixed-route ablation.

Anchor core model term tested: fixed-route ablation selectivity \(A_\ell\).

Anchor falsifier: no utility advantage, no selective ablation damage, or effect explained by load-matched random routes.

Experiment role: positive-control / conditional utility diagnostic. It is not a real-DCLM utility claim.

Primary metric from anchor: fixed-route ablation selectivity \(A_\ell\).

Claim boundary from anchor: MoE utility remains conditional on route preservation and a valid nested interference surface.

Minimal setup: train a small oracle-routed nested MoE positive control and compare against a load-matched random route baseline; run forced-route utility and fixed-route ablation.

Basic configuration: 8 seeds, same nested data as A07_01, small top-1 expert model, balanced evaluation.

Conditions to run: `oracle_nested_route_moe` and `random_load_matched_moe`.

Pass: oracle nested routes show route-conditioned utility and selective ablation; random load-matched routes do not.

Fail: forced utility is flat or fixed-route ablation is nonselective.

Insufficient: A07_01/A07_02 do not define a valid surface, or route concentration is too diffuse.

Cannot claim: real expert specialization, preserved DCLM utility, or deployable routing.

Approval decision: run as diagnostic sanity only; do not promote to Level 4 real utility unless A06 preservation is solved.

## 1. Anchor Alignment

Decision question: does routing select function, not just labels?

Physical prior tested: route assignment and expert function can be unbound.

Core model term tested: \(A_\ell\).

Falsifier: no selective fixed-route damage.

Claim boundary: controlled positive-control diagnostic only.

## 2. Tested Hypothesis

If a route genuinely binds nested function, then forcing the routed expert should lower that level's loss and ablating it under fixed routes should selectively damage that level.

## 3. Rival Explanations

1. Route purity only reflects level labels.
2. Load balance creates an apparent utility gain.
3. Expert ablation damages all levels uniformly.
4. Utility appears only because oracle routes are hand-coded.

## 4. Data / Model / Algorithm / Objective

Data: same nested-prefix surface.

Model: small top-1 MoE with fixed oracle or random routes. This is a diagnostic control, not a deployable router.

Objective: CE on nested targets.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Oracle nested route | positive control | route-function binding | checks diagnostic can see utility | primary | selective \(A_\ell\) | flat utility | too little training | `figures/a07_03_route_binding.png` |
| Random load-matched route | load rival | load-only explanation | guards against load-only utility | guard | no selectivity | same selectivity | unmatched load | `tables/a07_03_summary.csv` |

Seeds: `20260628-20260635`.

Checkpoints: final model after matched training budget.

## 6. Primary Metric

\[
A_\ell=CE_{\ell}^{-\mathrm{routed}}-\frac{1}{E-1}\sum_{e\ne \mathrm{routed}}CE_{\ell}^{-e}.
\]

Positive \(A_\ell\) means ablating the routed expert hurts its level more than ablating other experts.

## 7. Secondary Metrics

Route-conditioned utility \(U_\ell\), selected-best rate, route concentration, loss by level, and load by expert.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: oracle nested route should be a positive control.

Known bad: random load-matched route should not show consistent selectivity.

Known confusing: oracle route passes but A07_02 fails; then the diagnostic works, but A07 mainline utility remains parked.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Route audit | are routes concentrated? | route table | concentrated routes | `tables/a07_03_summary.csv` | detailed |
| Forced utility | does routed use help? | forced matrix | routed beats uniform | `figures/a07_03_route_binding.png` | summary |
| Ablation | is damage selective? | ablation matrix | positive \(A_\ell\) | `tables/a07_03_summary.csv` | summary |

## 10. Algorithm Specification, If Nontrivial

input: nested data, fixed route function, expert model, evaluation hooks.

parameters: expert count, training steps, seeds.

steps: train fixed-route MoE; compute forced expert loss matrix; compute fixed-route ablation loss matrix; aggregate selectivity.

outputs: `summary.md`, `detailed.md`, tables, and figures.

## 11. Success / Failure / Insufficient Evidence

Success: oracle route positive control shows selective utility and random route does not.

Failure: utility matrix is flat or ablation nonselective.

Insufficient evidence: route concentration or training validity fails.

## 12. What This Cannot Claim

This cannot claim real-DCLM expert utility or solve the A06 preservation bottleneck.

## 13. Review Notes And Protocol Changes

This protocol exists to keep the route-function diagnostic ready while the mainline remains gated by A06 preservation and A07_01/A07_02 mechanism validity.
