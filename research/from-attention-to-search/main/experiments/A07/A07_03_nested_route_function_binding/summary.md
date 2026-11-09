# Summary: A07_03 Nested Route-Function Binding

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md`

Protocol: `protocol.md`

## Purpose

Check whether the route-function binding diagnostic can detect causal expert
utility on the same nested surface. This is a positive-control diagnostic, not
a real-DCLM utility claim.

## Exact Setup

Run: `a07_nested_full_20260628_2`

Seeds: `20260628-20260635`, 8 seeds.

Conditions: `oracle_nested_route_moe` and `random_load_matched_moe`.

Model: fixed-route four-expert MoE on the nested surface.

## Primary Metric

Primary metric: fixed-route ablation selectivity.

\[
A_\ell=CE_{\ell}^{-\mathrm{routed}}-\frac{1}{E-1}\sum_{e\ne \mathrm{routed}}CE_{\ell}^{-e}.
\]

This metric decides whether the routed expert has causal value for its nested
level.

## Result

Judgment: diagnostic positive control passed, but mainline utility remains
conditional.

Key numbers:

| Condition | Ablation selectivity | Route utility | Selected-best rate | Route concentration | Loss | Acc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| oracle nested route | `0.5699` | `0.1746` | `0.7500` | `1.0000` | `0.1232` | `0.9714` |
| random load-matched route | `0.0107` | `-0.0024` | `0.2188` | `0.2635` | `0.3177` | `0.9053` |

## Key Figures

### Figure: Nested Route Binding

![Nested route binding](figures/a07_03_route_binding.png)

What this tests:

Anchor question: do routed experts have nested-level-specific causal utility?

Protocol question: does oracle nested routing produce selective ablation damage
while random load-matched routing does not?

Metric shown: fixed-route ablation selectivity and route-conditioned utility.

Metric definition: ablation selectivity is how much more damage occurs when the
routed expert is ablated than when non-routed experts are ablated.

Data source: 8-seed full local CUDA run.

How to read: higher oracle bars with near-zero random bars indicate the
diagnostic can detect route-function binding.

Observed result: oracle nested route has clear selectivity and utility; random
load-matched route does not.

Allowed claim: the diagnostic is valid as a controlled positive control.

What this figure does not prove: learned or preserved real MoE routing, real
semantic experts, or utility after ordinary top-1 training.

Anchor update implication: A07_03 remains parked until A06 route preservation
is available.

## Claim Boundary

Can claim: the forced-routing and fixed-route ablation diagnostic works on a
controlled positive-control nested MoE.

Cannot claim: real-DCLM expert utility, semantic specialization, or solved MoE
preservation.

## Next Decision

Do not promote A07_03 to real utility. Return to A06 preservation, then reuse
this diagnostic only on a preserved route partition.
