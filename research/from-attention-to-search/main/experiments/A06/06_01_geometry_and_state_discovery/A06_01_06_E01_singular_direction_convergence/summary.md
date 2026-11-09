# Summary: A06_01_06_E01 Singular Direction Convergence Metric

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Purpose

Define whether "singular direction convergence" can be measured as low
projector drift while singular gain still grows.

## Exact Setup

Run: `a08_singular_preservation_full_20260628_2`.

Seeds: `20260628-20260635`, 8 seeds, local CUDA.

Conditions: `rank1_nested`, `wide_nested`, `balanced_guard`,
`shuffled_feature_guard`.

Data: controlled nested feature surface `A -> AB -> ABC -> ABCD`.

## Primary Metric

Primary metric: stable convergence window with low
\(K_i(t)=\|P_i(t)-P_i(t-\Delta)\|_2\), positive gain
\(G_i(t)=\sigma_i(t)-\sigma_i(t-\Delta)\), and stable known-feature alignment.

This metric decides whether "converged direction" is an auditable object rather
than a phrase.

## Result

Judgment: supported for the rank-one common-direction surface; insufficient for
wide/multi-direction robustness.

Key numbers:

| Metric | Value |
| --- | ---: |
| rank-one pass rate | `1.0000` |
| rank-one final \(K\) | `0.0316` |
| rank-one final \(G\) | `0.0301` |
| rank-one A alignment | `0.7865` |
| shuffled B alignment | `0.0218` |
| wide pass rate | `0.5000` |

## Key Figure

### Figure: Convergence Curves

![Convergence curves](figures/a08_01_convergence_curves.png)

Anchor question: what threshold makes a singular direction safe to treat as
fixed for gating?

Metric shown: projector drift, singular value, and known A alignment.

How to read: after the early phase, good evidence means drift stays low while
singular value continues to grow and A alignment remains high.

Observed result: the rank-one surface has stable low drift and continuing gain.

Allowed claim: A08 can use \(K_i/G_i\) as a controlled convergence metric.

What this does not prove: the same threshold works in wide models or real DCLM.

## Claim Boundary

Can claim: a rank-one nested common direction can converge in direction before
gain growth stops.

Cannot claim: real-data convergence or robust multi-direction convergence.

## Next Decision

Use the converged direction in A06_01_06_E02, but keep wide robustness as a guard for
later real-data work.
