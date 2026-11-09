# Summary: A06_01_06_E02 Direction As Gate-Forward

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Purpose

Test whether the converged A06_01_06_E01 direction can be used as a gate-forward row.

## Exact Setup

Run: `a08_singular_preservation_full_20260628_2`.

Seeds: `20260628-20260635`, 8 seeds, local CUDA.

Conditions: `direction_gate`, `random_equal_norm_gate`,
`shuffled_direction_gate`, `oracle_feature_gate`.

## Primary Metric

Primary metric: feature-route NMI, the agreement between the gate route and the
known synthetic feature sign.

This metric decides whether the stable direction creates a real route identity.

## Result

Judgment: supported on the controlled synthetic surface.

Key numbers:

| Metric | Value |
| --- | ---: |
| direction gate NMI | `1.0000` |
| random equal-norm mean NMI | `0.1741` |
| shuffled direction NMI | `0.0001` |
| oracle NMI | `1.0000` |
| direction max load | `0.5097` |
| direction nuisance NMI | `0.0002` |
| max single random-control NMI | `0.5952` |

The single random-control spike is a guard: future protocols should use a
distribution of random controls, not a single random row.

## Key Figure

### Figure: Gate NMI

![Gate NMI](figures/a08_02_gate_nmi.png)

Anchor question: can a converged singular direction become a gate row?

Metric shown: feature-route NMI across gate conditions.

Observed result: direction gate matches the oracle and beats random/shuffled
controls in mean NMI.

Allowed claim: a converged synthetic direction can be converted into a route
identity.

What this does not prove: that the route survives training or has utility.

## Claim Boundary

Can claim: direction-to-gate conversion works in this controlled rank-one
feature surface.

Cannot claim: preservation, utility, real-DCLM transfer, or robustness to random
control spikes.

## Next Decision

Test whether using the direction for common/residual splitting changes tail
learning in A06_01_06_E03.
