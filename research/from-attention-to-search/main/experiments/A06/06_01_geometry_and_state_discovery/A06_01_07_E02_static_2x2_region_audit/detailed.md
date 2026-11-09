# Detailed: A06_01_07_E02_static_2x2_region_audit

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Protocol: `protocol.md`
Summary: `summary.md`

## 0. Quick Recap

Purpose:
Audit whether the A06 two-dimensional uniform-load claim survives radius variation and simple uniform region inputs.

Hypothesis:
The clean 2D theorem object is trace-centered M4, not raw M4 and not necessarily distribution-centered M4.

Experiment logic:
Reuse the A06_01_07_E01 \(2\times2\) expert conditions, replace the unit-circle-only input with several 2D regions, and measure natural load, margin, low-margin fraction, and degeneracy.

Conclusion:
Trace-centered M4 preserves near-uniform load on unit circle, uniform disk, annulus, centered square, and near-origin radial mixture. It does not support an arbitrary-uniform-region claim: centered rectangles can be strongly imbalanced.

Evidence:
Across C3/C5, trace-centered M4 has load error 0.0030 on uniform disk, 0.0045 on annulus, 0.0015 on centered square, and 0.2308 on centered rectangle.

## 1. Anchor Link And Decision Point

Anchor decision question:
Which expert-initialization-induced compatibility metric can define a non-degenerate routing rule that supports balanced load and metric-defined specialization under uniform input?

Decision after this experiment:
Use trace-centered M4 as the 2D proof-facing object. Treat distribution-centered M4 as a different calibration object that can fail under radius variation.

## 2. Protocol Compliance Audit

approved conditions match actual conditions:
Yes. Final run used the revised protocol: 5 expert conditions, 7 input distributions, 7 methods, 100 seeds, and 20,000 samples per distribution.

primary metric exists:
Yes. `load_error`, `mean_margin`, `low_margin_fraction`, and `degeneracy_rate` are in `tables/region_metric_summary.csv`.

central figures/tables exist:
Yes. Three central figures and three tables were produced.

seeds/checkpoints recorded:
Yes. 100 seeds. No checkpoints because this is a static audit.

known good/bad/confusing cases reviewed:
Yes. Annulus is the expected good case; C2 remains degenerate; near-origin mixture is the confusing low-margin case; centered rectangle is the boundary control.

success/failure/insufficient-evidence criteria applied:
Yes. The result supports trace-centered M4 under symmetric regions and weakens any arbitrary uniform-region claim.

Execution note:
Two earlier attempts were interrupted because a secondary direction-normalized disagreement diagnostic repeated score computations inside the full loop. That diagnostic was removed before the final full run because it was not a decision metric.

## 3. Setup

Runner:
`run_region_uniform_audit.py`

Command:

```bash
python run_region_uniform_audit.py
```

Expert conditions:

- `C1_random_unconstrained`;
- `C2_orthogonal_equal_singular`;
- `C3_orthogonal_unequal_singular`;
- `C4_near_identical`;
- `C5_separated_anisotropic`.

Input distributions:

| Distribution | Meaning | Proof role |
| --- | --- | --- |
| `unit_circle` | Uniform on \(S^1\) | proof baseline |
| `uniform_disk` | Uniform area measure in unit disk | radial symmetric uniform region |
| `annulus` | Uniform area measure in \(0.5\leq \|x\|\leq 1\) | radial symmetric region |
| `centered_square` | Uniform in \([-1,1]^2\) | centered region with 90-degree symmetry |
| `near_origin_mixture` | Radial mixture with most mass near origin | low-margin stress |
| `shifted_disk` | Shifted disk | symmetry-breaking control |
| `centered_rectangle` | Uniform in \([-1.5,1.5]\times[-0.5,0.5]\) | anisotropic region control |

Distribution summary:

| Distribution | Mean radius squared | \(E[x_1^2]\) | \(E[x_2^2]\) |
| --- | ---: | ---: | ---: |
| unit circle | 1.0000 | 0.5000 | 0.5000 |
| uniform disk | 0.5024 | 0.2500 | 0.2500 |
| annulus | 0.6240 | 0.3125 | 0.3125 |
| centered square | 0.6684 | 0.3333 | 0.3333 |
| near-origin mixture | 0.1181 | 0.0592 | 0.0588 |
| shifted disk | 0.4060 | 0.2645 | 0.1415 |
| centered rectangle | 0.8388 | 0.7500 | 0.0833 |

Methods:

- M1 signed prototype;
- M2 unsigned prototype;
- M3 top-1 projection;
- M3 full-span control;
- M4 raw;
- M4 trace-centered;
- M4 distribution-centered.

## 4. Metrics And Decision Rules

Primary metric:
`load_error = |P(g(x)=1)-0.5|`.

Required companion metric:
`mean_margin = E[|q_1(x)-q_2(x)|]` after routing by the larger score.

Boundary metric:
`low_margin_fraction = P(|q_1(x)-q_2(x)|<10^{-4})`.

Decision rule:
Balanced load without margin is not enough. A method supports the 2D routing claim only if it has low load error and non-collapsed margin in non-degenerate expert conditions.

## 5. Main Results

### Trace-Centered M4 Across Non-Degenerate C3/C5

| Distribution | Load error | Mean margin | Low-margin fraction | Margin ratio to unit circle |
| --- | ---: | ---: | ---: | ---: |
| unit circle | 0.0000 | 1.9315 | 0.0000 | 1.0000 |
| uniform disk | 0.0030 | 0.9702 | 0.0005 | 0.5023 |
| annulus | 0.0045 | 1.2053 | 0.0001 | 0.6241 |
| centered square | 0.0015 | 1.2854 | 0.0004 | 0.6660 |
| near-origin mixture | 0.0013 | 0.2281 | 0.0162 | 0.1181 |
| shifted disk | 0.0442 | 0.7842 | 0.0009 | 0.4060 |
| centered rectangle | 0.2308 | 1.6342 | 0.0004 | 0.8453 |

Interpretation:
Radial symmetry and centered-square symmetry preserve the split. Near-origin mass mainly weakens margin. A centered rectangle is uniform but not sufficiently symmetric for the quadratic sign-mass argument.

### Random Unconstrained Experts Expose Raw M4 Bias

| Distribution | Raw M4 load error | Trace-centered M4 load error | Distribution-centered M4 load error |
| --- | ---: | ---: | ---: |
| unit circle | 0.2545 | 0.0000 | 0.0000 |
| uniform disk | 0.2544 | 0.0027 | 0.0896 |
| annulus | 0.2542 | 0.0045 | 0.0402 |
| centered square | 0.2554 | 0.0015 | 0.0942 |
| near-origin mixture | 0.2547 | 0.0015 | 0.3863 |
| centered rectangle | 0.3111 | 0.2306 | 0.0896 |

Interpretation:
Raw M4 is biased by average expert response energy. Distribution-centered M4 fixes the unit circle but can fail when radii vary. Trace-centered M4 is the clean proof object for symmetric radial or square settings.

### Other Metrics

In C3/C5, M1 remains balanced on many centered regions, including the centered rectangle, because it is a linear half-plane split through the origin. M2 and M3 top-1 behave like line-squared comparisons and fail on the centered rectangle similarly to trace-centered M4.

This does not change the A06_01_07_E01 conclusion: M1/M2/M3 can be useful baselines, but M4 remains the core expert-matrix response object.

## 6. Visualization Results

### M4 Load Error By Region

![M4 load error by region](figures/m4_load_error_by_region.png)

Purpose:
Compare raw, trace-centered, and distribution-centered M4 across input regions.

Setup:
100 seeds, 20,000 samples per distribution, grouped by expert condition.

How to read:
Lower load error means closer to 50/50. The dashed line is a loose 0.05 reading threshold.

Observed result:
Trace-centered M4 has low load error on unit circle, uniform disk, annulus, centered square, and near-origin mixture. Centered rectangle breaks the split in C3/C5.

Take-home:
The valid 2D proof boundary is symmetry-dependent, not arbitrary-region uniform.

Remaining uncertainty:
This is still 2D static routing; high-dimensional behavior requires separate spectral conditions.

### M4 Margin By Region

![M4 margin by region](figures/m4_margin_by_region.png)

Purpose:
Check whether balanced load remains a clear expert preference.

Setup:
Same run, mean selected-expert score margin.

How to read:
Higher is better. A low margin means assignments are easier to perturb.

Observed result:
Uniform disk roughly halves the unit-circle margin for quadratic scores. Annulus and centered square keep more margin. Near-origin mixture has the weakest margin.

Take-home:
Radius distribution mainly affects confidence, not just load.

Remaining uncertainty:
Margin is a static score margin, not downstream task utility.

### C5 Margin Ratio By Region

![C5 margin ratio by region](figures/c5_margin_ratio_by_region.png)

Purpose:
Show margin scaling in the clean separated-anisotropic condition.

Setup:
C5 only, margin divided by the unit-circle margin for each method.

How to read:
Values below 1 mean weaker score separation than on the unit circle.

Observed result:
Trace-centered M4 keeps about 0.50 margin on uniform disk, 0.62 on annulus, 0.66 on centered square, and 0.12 on near-origin mixture.

Take-home:
The margin scaling matches the radius-squared intuition for quadratic scores.

Remaining uncertainty:
The figure does not decide which high-dimensional low-rank approximation is best.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| Distribution sampling | `distribution_summary.csv` | Passed | None | Sampler mismatch as main explanation |
| Raw-vs-centered M4 split | C1 raw load error about 0.25, trace-centered near zero in symmetric regions | Passed | None | Raw M4 as the proof object |
| Radius variation | uniform disk and annulus keep low load error | Passed | None | Unit-circle-only explanation |
| Low-radius stress | near-origin mixture load stays balanced but margin ratio is about 0.12 | Passed | Low radius reduces quadratic score margin | Load-only interpretation |
| Region boundary | centered rectangle load error about 0.23 in C3/C5 | Passed as boundary control | Region lacks required rotational symmetry | Arbitrary uniform-region claim |

Falsified physical prior:
None. The result refines the prior: symmetry, not just uniformity, is the key condition.

Falsified mathematical model:
Distribution-centered M4 as the direct radial extension of the unit-circle proof is weakened.

Falsified operationalization / proxy:
Using "uniform region" without specifying symmetry is too broad.

Falsified implementation:
None in the final run.

Falsified metric:
Raw M4 remains unsuitable for random unconstrained experts when the goal is natural 50/50 load.

Remaining rival explanations:
Finite-sample noise may explain tiny load errors under symmetric settings, but not the large centered-rectangle imbalance.

## 8. Full Experiment Record

Run date:
2026-06-17.

Final command:

```bash
python Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_07_E02_static_2x2_region_audit/run_region_uniform_audit.py
```

Samples:
20,000 per distribution.

Seeds:
100 expert seeds.

Tables:

- `tables/distribution_summary.csv`;
- `tables/per_seed_region_metrics.csv`;
- `tables/region_metric_summary.csv`.

Figures:

- `figures/m4_load_error_by_region.png`;
- `figures/m4_margin_by_region.png`;
- `figures/c5_margin_ratio_by_region.png`.

## 9. Interpretation

Observation:
Uniform disk, annulus, and centered square preserve near-50/50 trace-centered M4 routing.

Interpretation:
The 2D proof is not limited to points on the unit circle. It extends to distributions with enough symmetry when the score is trace-centered as a homogeneous quadratic form.

Claim:
The advisor-facing proof should use trace-centered M4 and state the symmetry assumption explicitly.

Speculation:
This symmetry condition is the low-dimensional analogue of the high-dimensional spectral-spread condition: both prevent one part of the quadratic form from dominating sign mass.

## 10. Claim Boundary

Can claim:

- Trace-centered M4 is the correct 2D proof-facing object.
- Uniform disk and annulus are valid radius-varying settings for the 2D argument.
- Centered square is also safe because of 90-degree rotational symmetry.
- Near-origin mass weakens margin even when load remains balanced.
- Centered rectangle shows that arbitrary uniform region claims are too strong.

Cannot claim:

- Raw M4 gives balanced load under random Gaussian experts.
- Distribution-centered M4 is equivalent to trace-centered M4 when radius varies.
- Any uniform 2D region is valid.
- This experiment proves high-dimensional behavior, real text behavior, trainable gate learning, or expert utility binding.

## 11. Next Decision

For the 2D proof document, state the theorem for trace-centered M4 under:

- unit circle;
- radially symmetric radius-varying distributions;
- centered square or other regions with the needed sign-flip symmetry.

Do not state the result for arbitrary uniform regions.

## 12. Links And Artifact Map

anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

protocol:
`protocol.md`

summary:
`summary.md`

code workspace:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_07_E02_static_2x2_region_audit/`

runner:
`run_region_uniform_audit.py`

config:
Constants in `run_region_uniform_audit.py`.

key code files:
`run_region_uniform_audit.py`

data / manifest:
Synthetic generated data only; no external dataset.

result dir:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_07_E02_static_2x2_region_audit/`

figure dir:
`figures/`

key tables:
`tables/region_metric_summary.csv`

logs / checkpoints:
No persistent logs or checkpoints.

repro command:
`python run_region_uniform_audit.py`

job id:
Local run, no job id.
