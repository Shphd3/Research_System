# Summary: Qwen3-30B Fixed-Fact Cross-Expression Semantic Separability

Primary Anchor: [A15_12](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_12_semantic_representation_separability/15_12_semantic_representation_separability_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `COMPUTATION_COMPLETE_BOUNDED`  
Knowledge status: `AI_EVIDENCE_RECORD_AWAITING_HUMAN_JUDGMENT`

## Result Snapshot

All 120 frozen evaluation cells retained statistically detectable label
association, but no registered layer obtained a positive all-task low-tail
certificate on both expression panels. All six layers therefore receive the
registered machine verdict `READABLE_BUT_LOW_TAIL_FRAGILE`.

The result is sharply panel-dependent. A head learned from C4E-A passes the
registered all-task fifth-percentile margin bound on C4E-B at every layer. The
same head fails that bound on C5E at every layer. Parent labels are the most
stable; the decisive failures are parent-conditioned fine labels, especially
physics at Blocks 4--20 and mathematics at Blocks 28--44.

This establishes a failure of the **C4E-A-learned boundary to transfer across
expression banks**. It does not establish that C5E is internally nonseparable.
That missing distinction is tested separately by
[A15_12_E02](../A15_12_E02_expression_bank_boundary_coverage_controls/protocol.md).

## Registered Verdict Basis

The value before the slash is the observed minimum task-level fifth-percentile
geometric margin. The value after the slash is its registered simultaneous
one-sided lower bound.

| Qwen block | C4E-B bottleneck / lower bound | C5E bottleneck / lower bound | C5E worst task | Verdict |
| ---: | ---: | ---: | --- | --- |
| 4 | 5.095 / 4.865 | -1.677 / -2.741 | physics fine | `READABLE_BUT_LOW_TAIL_FRAGILE` |
| 12 | 3.997 / 3.026 | -5.822 / -8.573 | physics fine | `READABLE_BUT_LOW_TAIL_FRAGILE` |
| 20 | 2.767 / 2.340 | -7.566 / -11.405 | physics fine | `READABLE_BUT_LOW_TAIL_FRAGILE` |
| 28 | 1.984 / 1.145 | -6.878 / -7.770 | mathematics fine | `READABLE_BUT_LOW_TAIL_FRAGILE` |
| 36 | 1.195 / 0.111 | -10.880 / -11.982 | mathematics fine | `READABLE_BUT_LOW_TAIL_FRAGILE` |
| 44 | 6.560 / 5.568 | -1.905 / -3.080 | mathematics fine | `READABLE_BUT_LOW_TAIL_FRAGILE` |

Source: [bottlenecks.csv](tables/bottlenecks.csv).

![Corrected one-sided all-task bottleneck figure](figures/all_task_bottleneck_margin_one_sided.png)

The plotted whiskers are one-sided lower bounds. The original worker figure
incorrectly mirrored that distance above the point; the data and registered
lower bounds were correct. The canonical figure above is a display-only
post-run correction generated from the frozen table and does not overwrite the
completed worker run.

## Average Readability Versus Low-Tail Geometry

All 120 fixed-prediction label-permutation tests reached raw \(p=0.0001\) and
Holm-adjusted \(p=0.012\). Thus even the weakest cells retain above-null average
association. This cannot erase the negative low-tail result.

| Panel / block | Parent accuracy / \(q_{.05}\) | Joint accuracy / \(q_{.05}\) | Pooled fine accuracy / \(q_{.05}\) |
| --- | ---: | ---: | ---: |
| C4E-B / 4 | 1.000 / 5.095 | 1.000 / 7.463 | 1.000 / 7.901 |
| C4E-B / 36 | .997 / 1.456 | .999 / 1.986 | .996 / 1.996 |
| C4E-B / 44 | 1.000 / 6.852 | 1.000 / 8.243 | 1.000 / 8.516 |
| C5E / 4 | 1.000 / 4.066 | .985 / 2.227 | .986 / 3.059 |
| C5E / 36 | .856 / -1.373 | .666 / -4.261 | .688 / -5.414 |
| C5E / 44 | .999 / 4.669 | .991 / 3.518 | .985 / 3.124 |

The pooled fine column is descriptive only. It hides the physics failure at
Block 4 and mathematics failure at Block 44; the registered verdict uses the
minimum across all eight fine tasks.

![Layerwise average readability and low-tail margin](figures/layerwise_readability_and_margin.png)

## Failure Structure

- At C5E Block 4, physics balanced accuracy is .9125, but all 21 errors arise
  from the 30 mechanics rows; 16 are classified as relativity and four as
  electromagnetism.
- At C5E Block 36, mathematics balanced accuracy is .4792. Probability and
  analysis each have zero class accuracy, and many classes are attracted to
  algebra or topology.
- C5E exhibits a descriptive U-shaped six-block trajectory: Blocks 4 and 44
  are much stronger than Blocks 12--36. This is not a continuous-layer trend
  test or a causal formation result.
- Joint 64-way accuracy closely tracks pooled conditional-fine accuracy. The
  main failure is already present within parents; the evidence does not support
  a separate dominant global-composition bottleneck.

## What Is Established

- On these 64 fixed fact bundles, full-space linear readout learned from C4E-A
  transfers strongly to unseen C4E template families.
- The same frozen readout does not retain a positive all-granularity low-tail
  certificate under the stronger C4E-to-C5E expression-bank shift.
- Average association and robust low-tail geometry are empirically different
  properties.
- Parent semantics are more expression-stable than the weakest fine semantic
  partitions in this audit.

## Claim Boundary

This result does **not** establish:

- unseen-fact semantic generalization: C4E and C5E reuse the same six atomic
  statements for every leaf;
- intrinsic C5E nonseparability: no C5E head was fitted in E01;
- strict separability of every C4E-B sample: Blocks 28 and 36 contain a small
  number of errors despite positive fifth-percentile bounds;
- native Gate use, expert utility, language-model gain, causal representation
  formation, or low-rank Router sufficiency;
- stable probability calibration, exact margin magnitude, or intrinsic rank:
  all 60 probes selected the \(C=100\) upper grid edge and their cross-validation
  NLL decreased throughout the registered grid.

## Next Decision

E02 is now complete: [its Summary](../A15_12_E02_expression_bank_boundary_coverage_controls/summary.md)
shows robust C5E within-bank readout at Blocks 4, 12, and 44, failed single-bank
transfer in both directions, and a common full-pooled certificate at Blocks 4,
12, 20, and 44. The next decisive experiment is the frozen-probe `TAX-C4A`
fact-package joint-shift stress test. It records whether the frozen boundary
extends to that one additional panel; because fact package, length, and surface
naturalness all change, failure cannot isolate fact identity. Architecture or
expert-utility claims remain premature regardless of the E03 outcome.
