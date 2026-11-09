# Summary: A13_00_01_E02 Budget-Only Carrier Replay

Primary anchor:
[13_00_01](../../../../problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md)

Protocol: [protocol.md](protocol.md)

## Result Snapshot

Verdict: **fail; tripling the budget is not sufficient.**

What we established: E02 exactly reproduced every E01 research metric through
step 1,000, then extended the same trajectories to step 3,000. The one-layer
bypass gate now passed (`0.9515` mean), while one-layer relay remained at
chance (`0.0602`).

What the experiment shows: two-layer relay mean accuracy improved from
`0.7243` to `0.8097` but still failed the `0.95` gate. Seeds 1301 and 1304
reached at least `0.971` during training and later fluctuated, while three seeds
remained in lower plateaus. More time alone does not create a stable carrier.

What we do next: keep the 3,000-step budget and change only the learning-rate
schedule from constant `0.003` to cosine decay ending at `0.0001`. This tests
whether persistent background-gradient updates erase or destabilize an already
formed relay state.

## Purpose

Separate premature stopping from persistent optimization instability without
changing the workload or learner.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| budget extension | allow more updates with everything else fixed | 3,000 versus 1,000 steps | steps | tests premature stopping | optimal training |
| late-window instability | capability rises and then falls under continued updates | accuracy variance over the final 200 steps | fraction correct | motivates a schedule audit | exact gradient cause |

## Exact Setup

E02 is an exact E01 replay except `max_steps=3000`. The same five seeds,
batches, model, constant learning rate, masks, split, metrics, and thresholds
were retained.

## Primary Metric

The unchanged carrier-eligibility conjunction failed because two-layer
capability, counterfactual follow, and donor-patch follow remained below their
registered thresholds.

## Result

| Condition / audit | E01 at 1,000 | E02 at 3,000 | E02 verdict |
| --- | ---: | ---: | --- |
| relay 1L mean accuracy | 0.0641 | 0.0602 | pass negative control |
| relay 2L mean accuracy | 0.7243 | 0.8097 | fail |
| bypass 1L mean accuracy | 0.9320 | 0.9515 | pass |
| selected-swap follow | 0.7359 | 0.8136 | fail downstream |
| unselected invariance | 0.8350 | 0.9223 | pass |
| different-label donor follow | 0.4155 | 0.4214 | fail downstream |
| same-label donor preservation | 0.7243 | 0.8019 | fail downstream |

## Key Figures

### Figure: Extended carrier trajectories

![Extended carrier trajectories](figures/carrier_trajectory.png)

What this tests: whether the failed 1,000-step carrier merely needed more
updates.

Metric shown: held-out standard-head answer accuracy.

Metric unit: fraction correct.

Data source: five registered seeds, 151 checkpoints per condition.

How to read: a budget-only repair requires stable crossing of the `0.95` line.

Observed result: two relay seeds reached the line, but the multi-seed surface
remained unstable and three seeds stayed below it.

Allowed claim: the 1,000-step limit was part of the problem but not the only
problem.

What this does not prove: cosine decay will repair the failure.

## Claim Boundary

Can claim: longer constant-rate training does not make this carrier eligible.

Cannot claim: NTP cannot learn the task, because individual two-layer seeds
reached exact or near-exact performance; no MTP result exists.

## Next Decision

Run the schedule-only E03 audit. Do not change task, layer count, width, or
objective.
