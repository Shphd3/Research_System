# Detailed: A06_01_06_E03 Common Direction Split Reservoir

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: test the r1 common projection / residual reservoir mechanism.

Hypothesis: removing the converged common direction from the reservoir path
should improve tail loss and lower tail update mass in the common subspace.

Conclusion: the intervention moves the intended metrics, but the capacity guard
explains too much; mechanism support is insufficient.

Evidence: `tables/a08_03_aggregate.csv` and `figures/a08_03_split_results.png`.

## 1. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes, tail loss improvement with guards.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, 8 seeds.

known good/bad/confusing cases reviewed: yes.

success/failure/insufficient criteria applied: yes.

## 2. Setup

Data: same nested synthetic surface as A06_01_06_E01.

Main intervention: common branch receives the converged common direction; the
reservoir branch receives the residual input.

Capacity guard: same split architecture with a random direction.

Oracle guard: split using the true A direction.

## 3. Metrics

Tail loss: binary cross-entropy on `ABCD` examples.

Common loss: binary cross-entropy on `A` examples.

\(\alpha_{\mathrm{tail}}\): fraction of the tail gradient/update in the common
projector for the trainable reservoir/baseline path.

Capacity guard: proposed split must outperform the random split, not only CE.

## 4. Main Results

| Condition | Tail loss | Tail gain vs CE | Alpha | Alpha reduction |
| --- | ---: | ---: | ---: | ---: |
| ce_baseline | `0.4098` | `0.0000` | `0.1558` | `0.0000` |
| update_suppression_only | `0.3504` | `0.0594` | `0.2224` | `-0.0666` |
| common_residual_split | `0.3114` | `0.0984` | `0.0000` | `0.1558` |
| capacity_matched_random_split | `0.2502` | `0.1596` | `0.2222` | `-0.0664` |
| oracle_split | `0.2784` | `0.1314` | `0.0048` | `0.1511` |

Interpretation: the proposed split reduces the intended alpha metric, but tail
loss is not uniquely improved by common-direction removal. The capacity-matched
random split is a stronger tail-loss baseline.

## 5. Visualization Results

### Split Results

![Split results](figures/a08_03_split_results.png)

Purpose: compare tail loss and common-subspace tail update fraction.

Setup: 8 seeds, full synthetic run.

How to read: lower tail loss is better; lower alpha is mechanistically cleaner
only when the capacity guard also passes.

Observed result: proposed split lowers alpha to near zero and improves tail
loss, but random split lowers tail loss more.

Take-home: metric movement is real, mechanism attribution fails.

Remaining uncertainty: the random split may add useful capacity or regularize
the task in a way unrelated to common direction removal.

## 6. Failure Decomposition

Falsified physical prior: not fully; removing common direction can reduce alpha.

Falsified mathematical model: partially; \(h_R=(I-P_C)h\) is not enough to
identify the causal reason for tail improvement.

Falsified operationalization / proxy: yes, as a method claim. The current split
does not beat the capacity-matched random split.

Falsified implementation: no.

Falsified metric: tail loss alone would be a false positive; the capacity guard
catches it.

Remaining rival explanations: capacity increase, regularization, easier
optimization, or random-feature decomposition.

## 7. Relation To A07_06

A07_06 also improved rare loss without moving the intended route-level conflict
metric. A06_01_06_E03 repeats the same warning in a cleaner synthetic form: performance
improvement is not mechanism evidence unless the mechanism-specific guard beats
controls.

## 8. Claim Boundary

Can claim: the split intervention is active and reduces alpha.

Cannot claim: common/residual split is the cause of tail improvement or a valid
real-DCLM preservation method.

## 9. Links And Artifact Map

runner:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a08_singular_direction_preservation.py`

raw result dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a08_singular_direction_preservation/a08_singular_preservation_full_20260628_2`

tables: `tables/a08_03_aggregate.csv`, `tables/a08_03_split_metrics.csv`,
`tables/decision_metrics.json`.

figure: `figures/a08_03_split_results.png`.

job id: local CUDA run, no ACP job id.
