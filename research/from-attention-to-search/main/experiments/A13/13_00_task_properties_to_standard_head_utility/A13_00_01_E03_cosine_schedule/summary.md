# Summary: A13_00_01_E03 Schedule-Only Carrier Audit

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

## Result Snapshot

Verdict: **near-pass but formally fail; thresholds were not relaxed.**

What we established: cosine decay raised two-layer relay mean accuracy from
`0.8097` to `0.9437`, made all five relay seeds reach at least `0.9806` at some
checkpoint, passed the input-counterfactual gate, and raised different-label
relay-donor follow to `0.9845`.

What the experiment shows: non-decaying optimization was a real part of the
E02 failure, but width-64 training remained seed-sensitive. Final relay mean
accuracy missed the `0.95` gate by `0.0063`; same-label donor preservation
missed its gate by `0.0005`. Seed 1304 reached exact accuracy and later settled
at `0.8252`, so existence of a capable checkpoint is not stable eligibility.

What we do next: retain the task, two-layer limit, NTP objective, cosine
schedule, seeds, and gates; change only the representation width from 64 to 128
with the FFN kept at four times width. This tests whether shared all-position
prediction and relay binding exceed the reliable width-64 capacity.

## Purpose

Test whether diminishing update size stabilizes the carrier.

## Terminology / Definitions

| Term | Plain meaning | Concrete object | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| near-pass | numerical result close to, but below, a registered threshold | `0.9437 < 0.95` and `0.9495 < 0.95` | fraction | preserves preregistration | practical equivalence |
| branch accuracy | accuracy conditional on selector A or B | held-out standard-head accuracy per selector | fraction | reveals branch-specific plateaus | internal head specialization |

## Exact Setup

The only E02-to-E03 change was a cosine learning-rate schedule from `0.003` to
`0.0001` over the same 3,000 steps. Branch metrics were debug-only additions.

## Primary Metric

The carrier conjunction remained false because \(G_2\) and \(G_6\) missed their
registered thresholds.

## Result

| Metric | E02 constant rate | E03 cosine | Gate |
| --- | ---: | ---: | --- |
| relay 2L mean final accuracy | 0.8097 | 0.9437 | \(\ge0.95\) |
| bypass 1L mean final accuracy | 0.9515 | 0.9670 | \(\ge0.95\) |
| selected-swap follow | 0.8136 | 0.9437 | \(\ge0.90\) |
| unselected invariance | 0.9223 | 0.9825 | \(\ge0.90\) |
| different-label donor follow | 0.4214 | 0.9845 | \(\ge0.90\) |
| same-label donor preservation | 0.8019 | 0.9495 | \(\ge0.95\) |

Four relay seeds ended above `0.90`; all five reached above `0.95` during
training. This proves capability is reachable, not stable under the registered
width-64 learner.

## Key Figures

### Figure: Cosine schedule carrier trajectories

![Cosine schedule carrier trajectories](figures/carrier_trajectory.png)

What this tests: whether shrinking updates converts partial relay learning into
stable multi-seed capability.

Metric shown: held-out standard-head answer accuracy.

Observed result: a large improvement and nearly perfect causal donor control,
but one final seed remained below the carrier gate.

Allowed claim: constant-rate background updates contributed to E02 failure.

What this does not prove: width is the remaining cause.

## Claim Boundary

Can claim: the intended relay is reachable and can exercise content-specific
control in every seed at some point; the registered width-64 final-state carrier
is still ineligible.

Cannot claim: MTP benefit or general capacity scaling.

## Next Decision

Run one width-only capacity audit; if it fails, close this learner realization
rather than add task complexity.
