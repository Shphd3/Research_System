# Summary: A06_01_07_E02_static_2x2_region_audit

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Protocol: `protocol.md`

## Purpose

This experiment tests whether the A06 two-dimensional load-balance result is only a unit-circle artifact, or whether it survives when input radius varies and when points uniformly fill simple 2D regions.

The practical uncertainty is how to state the advisor-facing 2D proof boundary: unit circle only, radially symmetric regions, centered square regions, or arbitrary uniform regions.

## Exact Setup

Two experts are \(2\times2\) matrices \(A_1,A_2\). The run uses the same five expert conditions as A06_01_07_E01:

- `C1_random_unconstrained`;
- `C2_orthogonal_equal_singular`;
- `C3_orthogonal_unequal_singular`;
- `C4_near_identical`;
- `C5_separated_anisotropic`.

Input distributions:

- `unit_circle`;
- `uniform_disk`;
- `annulus`;
- `centered_square`;
- `near_origin_mixture`;
- `shifted_disk`;
- `centered_rectangle`.

The run uses 100 expert seeds and 20,000 points per distribution. Compared methods include M1, M2, M3 top-1, M3 full-span, raw M4, trace-centered M4, and distribution-centered M4.

The proof-facing M4 variant is trace-centered M4:

\[
q_e(x)=x^\top \left(G_e-\frac{1}{2}\mathrm{tr}(G_e)I\right)x.
\]

This is different from distribution-centered M4:

\[
q^P_e(x)=x^\top G_ex-\mathbb{E}_{x\sim P}[x^\top G_ex].
\]

## Primary Metric

Primary metric: natural load error, read together with mean margin.

Load error answers whether the region mass is split close to 50/50. Mean margin answers whether the split has a clear selected-expert score advantage. Low-margin fraction is used to catch the near-origin failure mode.

## Result

Trace-centered M4 supports the intended 2D proof boundary:

- unit circle, uniform disk, annulus, and centered square keep near-50/50 load;
- near-origin mass keeps load balanced but sharply weakens margin;
- shifted disk and centered rectangle show the boundary: not every uniform region preserves the split.

For the two non-degenerate anisotropic expert conditions C3/C5, trace-centered M4 gives:

| Distribution | Load error | Mean margin | Low-margin fraction | Margin ratio to unit circle |
| --- | ---: | ---: | ---: | ---: |
| unit circle | 0.0000 | 1.9315 | 0.0000 | 1.0000 |
| uniform disk | 0.0030 | 0.9702 | 0.0005 | 0.5023 |
| annulus | 0.0045 | 1.2053 | 0.0001 | 0.6241 |
| centered square | 0.0015 | 1.2854 | 0.0004 | 0.6660 |
| near-origin mixture | 0.0013 | 0.2281 | 0.0162 | 0.1181 |
| shifted disk | 0.0442 | 0.7842 | 0.0009 | 0.4060 |
| centered rectangle | 0.2308 | 1.6342 | 0.0004 | 0.8453 |

For random unconstrained experts, raw M4 remains imbalanced because the two experts can have different average response energy. Trace-centered M4 fixes this in symmetric regions:

| Distribution | Raw M4 load error | Trace-centered M4 load error | Distribution-centered M4 load error |
| --- | ---: | ---: | ---: |
| unit circle | 0.2545 | 0.0000 | 0.0000 |
| uniform disk | 0.2544 | 0.0027 | 0.0896 |
| annulus | 0.2542 | 0.0045 | 0.0402 |
| centered square | 0.2554 | 0.0015 | 0.0942 |
| near-origin mixture | 0.2547 | 0.0015 | 0.3863 |
| centered rectangle | 0.3111 | 0.2306 | 0.0896 |

Important correction:
When radius varies, subtracting only the distribution mean is not the same as the 2D proof operation. Distribution-centered M4 can be imbalanced under random unconstrained experts. The proof-facing object is trace-centered M4.

## Key Figures

### Figure: M4 Load Error By Region

![M4 load error by region](figures/m4_load_error_by_region.png)

What this tests:
Whether raw, trace-centered, and distribution-centered M4 preserve near-50/50 load across input regions.

How to read:
Lower load error is closer to 50/50. The dashed line marks a loose 0.05 reading threshold.

Observed result:
Trace-centered M4 is stable on unit circle, uniform disk, annulus, centered square, and near-origin mixture. It fails on the centered rectangle because that region breaks the rotational symmetry needed by the 2D quadratic argument.

Take-home:
The result is not unit-circle only, but it is not arbitrary-region uniform either.

What this does not prove:
It does not prove high-dimensional load balance or trainable-router learnability.

### Figure: M4 Margin By Region

![M4 margin by region](figures/m4_margin_by_region.png)

What this tests:
Whether the balanced split remains numerically clear after changing the radius distribution.

How to read:
Higher mean margin means a clearer selected-expert score advantage.

Observed result:
Uniform disk has about half the unit-circle margin. The annulus has higher margin than the disk. The near-origin mixture has much weaker margin despite balanced load.

Take-home:
Radius variation does not necessarily harm load, but radius mass near zero weakens the confidence of the routing decision.

What this does not prove:
It does not prove functional expert utility; it only measures static score separation.

### Figure: C5 Margin Ratio By Region

![C5 margin ratio by region](figures/c5_margin_ratio_by_region.png)

What this tests:
How much margin remains in the clean separated-anisotropic expert condition.

How to read:
A value of 1 matches the unit-circle margin for the same method.

Observed result:
Uniform disk keeps about 0.50 of unit-circle margin, annulus keeps about 0.62, centered square keeps about 0.66, and near-origin mixture keeps about 0.12.

Take-home:
The margin scaling follows the expected radius-squared effect for quadratic scores.

What this does not prove:
It does not show that every non-circular uniform region is safe.

## Claim Boundary

Can claim:

- The 2D trace-centered M4 proof target is not restricted to the unit circle.
- Uniform disk, annulus, and centered square are valid proof-facing or near-proof-facing 2D settings.
- Near-origin mass is a margin risk, not primarily a load risk.
- Arbitrary uniform regions are not safe; centered rectangles can break the 50/50 quadratic split.
- Distribution-centered M4 should not be confused with trace-centered M4 when radius varies.

Cannot claim:

- Raw M4 guarantees balanced load under random experts.
- Mean-subtracted distribution-centered M4 is the correct proof object.
- Every uniform 2D region preserves the split.
- This proves trainable router behavior, real MoE specialization, or high-dimensional generalization.

## Next Decision

Use trace-centered M4 as the clean 2D theorem object. For the advisor-facing proof, state the condition as: inputs must have enough symmetry, such as uniform circle, radial symmetry with pointwise trace-centering, or centered square with 90-degree rotational symmetry. Do not claim arbitrary uniform-region balance.
