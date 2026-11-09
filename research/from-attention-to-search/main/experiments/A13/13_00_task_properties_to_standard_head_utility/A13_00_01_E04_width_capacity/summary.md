# Summary: A13_00_01_E04 Width-Only Carrier Capacity Audit

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

## Result Snapshot

Verdict: **fail; the query-conditioned carrier is closed as the first
comparison surface.**

What we established: width 128 did not repair the width-64 instability.
Two-layer relay mean accuracy fell from `0.9437` to `0.6194`, while the
one-layer bypass mean still passed at `0.9534` and one-layer relay remained at
chance (`0.0583`).

What the experiment shows: missing raw width is not the supported explanation.
The first carrier bundled two properties—state relay and query-conditioned
selection—and therefore remained an unnecessarily difficult capability gate.

What we do next: simplify rather than enlarge. Freeze the same sequence and
relay graph, make the answer always equal `value-A`, and treat `value-B` and
the selector as nuisances. This isolates relay necessity; query-conditioned
binding becomes a later task-property subanchor.

## Terminology / Definitions

| Term | Plain meaning | Concrete object | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| closed carrier | no more learner repairs are allowed for this task as the first gate | E01--E04 combined verdict | decision | prevents endless tuning | query binding is impossible |
| task-property bundling | more than one mechanism is required before comparison | relay plus selector-dependent binding | design flaw | motivates simplification | which mechanism caused every failed seed |

## Exact Setup

E04 changed only hidden width `64 -> 128` and proportional FFN width
`256 -> 512` relative to E03. The task, depth, schedule, objective, seeds, and
gates were unchanged.

## Primary Metric

Carrier eligibility failed: two-layer capability, input counterfactuals, and
relay-use aggregates were below threshold.

## Result

| Metric | width 64 | width 128 |
| --- | ---: | ---: |
| relay 1L mean accuracy | 0.0583 | 0.0583 |
| relay 2L mean accuracy | 0.9437 | 0.6194 |
| bypass 1L mean accuracy | 0.9670 | 0.9534 |
| different-label donor follow | 0.9845 | 0.7922 |

One width-128 relay seed reached exact accuracy; the remaining four ranged from
`0.2621` to `0.8252`. Width does not monotonically repair the carrier.

## Key Figures

![Width-128 carrier trajectories](figures/carrier_trajectory.png)

Observed result: increased capacity preserved the structural controls but
worsened the multi-seed relay surface.

Allowed claim: width insufficiency is weakened as the primary explanation.

What this does not prove: query-conditioned relay is generally hard or that
MTP would solve it.

## Claim Boundary

Can claim: this carrier is not eligible for objective comparison after the
registered budget, schedule, and width audits.

Cannot claim: any NTP/MTP difference.

## Next Decision

Open a new single-value relay carrier subanchor. Do not run MTP on the closed
query-conditioned carrier.
