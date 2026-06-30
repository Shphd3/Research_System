# A06_17_04 Margin Mechanism Memory

## Current Status

We are still in mechanism understanding, not yet in deployable method design.
The current controlled chain is:

```text
uniform feature slots can be clustered into route-relevant centers
-> center initialization creates feature-to-expert routing
-> the reason it survives is large positive route margin
-> training drift can reduce that margin
-> if the boundary is explicitly crossed, original feature-to-expert
   preservation breaks
```

## What Was Completed In This Side Conversation

Created and ran A06_17_04:

- anchor:
  `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_17_04_margin_crossing_causal_stress_anchor.md`
- protocol:
  `Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/protocol.md`
- summary:
  `Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md`
- detailed:
  `Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/detailed.md`
- runner:
  `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_17_04_margin_crossing_causal_stress.py`
- forced-crossing addendum runner:
  `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_17_04_forced_crossing_addendum.py`

## Main Result

The original 17_04 full run showed:

- static boundary crossing works: feature centers switch near predicted margin
  distance, with center switch ratio about `1.04-1.07`;
- norm weakening and LR 3x lower dynamic margin but do not cross the boundary;
- all training-stress conditions keep final feature NMI `1.0`.

The forced-crossing addendum then showed:

- post-hoc row interpolation toward the nearest competitor makes dynamic
  margin negative at mean alpha `0.578`;
- feature NMI drops below `0.95` at mean alpha `0.656`;
- identity-sensitive preserve fraction drops from `1.000` at alpha `0.0` to
  about `0.31` at alpha `0.75` and near zero by alpha `1.25`.

Important boundary: NMI is permutation-invariant. It can remain nonzero if
features switch consistently to other experts. For preservation, matched-region
preserve fraction is the stricter guard.

## Current Interpretation

The causal chain is now locally coherent in the controlled bridge:

```text
positive margin protects the initial feature-to-expert region;
natural training stress in 17_04 did not consume all margin;
forced crossing consumes the margin and breaks the original region.
```

This does not yet solve real-data initialization because real data lacks known
ground-truth feature labels and known correct expert assignment.

## A06_17_05 Update: Margin Basin Robustness

After the 17_04 forced-crossing result, we tested the rival explanation:

```text
Maybe exact feature-center initialization is not necessary. It may be enough
to initialize inside a positive-margin basin around the center.
```

Experiment:

- anchor:
  `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_17_05_margin_basin_robust_initialization_anchor.md`
- summary:
  `Projects/from-attention-to-search/main/experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md`
- detailed:
  `Projects/from-attention-to-search/main/experiments/A06/A06_17_05_margin_basin_robust_initialization/detailed.md`

Setup:

- controlled no-position bridge;
- no B token;
- slot length 4;
- route on the last slot token;
- C0-C3;
- 4 seeds;
- pseudo-center rows mixed with random directions at
  `rho = 0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 1.0`.

Result:

```text
rho <= 0.7: final preserve fraction = 1.0, final NMI = 1.0, margin positive.
rho = 1.0: step-0 margin negative, final preserve fraction = 0.219.
```

Representative table:

| rho | step-0 min margin | final min margin | final preserve fraction | final NMI |
|---:|---:|---:|---:|---:|
| 0.00 | 6.004 | 3.765 | 1.000 | 1.000 |
| 0.35 | 4.953 | 3.289 | 1.000 | 1.000 |
| 0.50 | 3.773 | 2.733 | 1.000 | 1.000 |
| 0.70 | 1.531 | 2.142 | 1.000 | 1.000 |
| 1.00 | -1.337 | -4.205 | 0.219 | 0.793 |

Conclusion:

```text
Exact center rows are not required in the controlled bridge. The mechanism is
better described as a positive-margin basin.
```

Method implication:

```text
For future label-free methods, do not only ask whether a candidate is the exact
feature center. Ask whether it creates enough positive margin before training.
```

## Rival Explanation To Test Next

Rival explanation:

```text
Maybe precise center initialization is not necessary. Any initialization inside
a sufficiently large basin around the feature center may preserve routing,
even if it is not exactly at the discovered center.
```

Meaning: the method may not need exact feature centers; it may only need to
land in a positive-margin basin.

## Two Method-Facing Directions

### Direction 1: Margin-Basin Robustness

Question:

```text
How far can candidate router rows deviate from feature centers while still
keeping positive margin and preserving routing?
```

Test:

- perturb center rows by angular noise or interpolate with random rows;
- measure initial margin, preserve fraction, final route NMI, and loss;
- identify a pass/fail margin threshold.

Method implication:

```text
If a wide basin exists, label-free initialization does not need exact centers;
it only needs candidates that pass a positive-margin audit.
```

Status: supported in A06_17_05 for the controlled no-position bridge.

### Direction 2: Label-Free Margin Acceptance Gate

Question:

```text
Can we accept or reject label-free discovered centers using only route-margin
statistics before training?
```

Test:

- generate multiple candidate center sets from label-free methods;
- compute unsupervised or proxy margin guards before training;
- only train candidates above the margin threshold;
- test whether rejected candidates are the ones that would fail preservation.

Method implication:

```text
A practical method may be: discover many candidate centers, keep only those
with enough margin, and do not enter preservation training when the audit
fails.
```

## Suggested Next Anchor

Updated name idea:

```text
A06_17_06_label_free_margin_acceptance_gate_anchor
```

One-sentence question:

```text
Can we accept or reject label-free discovered center candidates using only
pre-training margin-like statistics, before spending training budget?
```

Primary metric:

```text
candidate pre-training margin score versus final matched-region preserve
fraction / feature NMI
```

Pass:

```text
accepted candidates preserve and rejected candidates fail more often than
chance or split-stability alone.
```

Fail:

```text
margin-like acceptance does not predict preservation.
```

Cannot claim:

```text
real semantic feature discovery or utility.
```

## Files To Read First In Main Conversation

1. `Projects/from-attention-to-search/main/experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md`
2. `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_17_04_margin_crossing_causal_stress_anchor.md`
3. this memory file:
   `daily_research_reports/0629/a06_17_04_margin_mechanism_memory.md`
