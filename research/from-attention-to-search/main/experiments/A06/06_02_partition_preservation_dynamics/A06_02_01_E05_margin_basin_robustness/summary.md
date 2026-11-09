# Summary: A06_02_01_E05 Margin-Basin Robust Initialization

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Purpose

This experiment tests whether exact center initialization is required, or
whether there is a positive-margin basin around the discovered center rows.

## Exact Setup

Controlled no-position bridge, C0-C3, 4 seeds, 4 features, 4 experts, slot
length 4, no B token, route on the last token of the slot, uniformly sampled
feature/nuisance/slot position. The model and training objective match
A06_02_01_E04.

Run name: `a06_17_05_margin_basin_full_20260629_1`.

Pseudo-center rows were mixed with random directions:

\[
w_e(\rho)=\alpha\cdot
\mathrm{normalize}\left((1-\rho)\hat c_e+\rho \hat r_e\right).
\]

## Primary Metric

Final matched-region preserve fraction:

\[
P(T)=\frac{1}{F}\sum_f
\Pr_{h\in f}\left[\arg\max_e w_e(T)^\top h=e(f)\right].
\]

This is stricter than NMI because it checks whether the original
feature-to-expert identity is preserved.

## Result

**Verdict:** supported.

Exact feature-center rows are not required in the controlled bridge. There is
a wide positive-margin basin around pseudo centers. Perturbations up to
`rho = 0.7` keep positive step-0 margin and preserve the original routing
region through training. At `rho = 1.0`, the rows are pure random directions:
step-0 margin is already negative, and final preserve fraction collapses.

## Key Evidence

| Pseudo perturbation rho | Step-0 min margin | Final min margin | Final preserve fraction | Final NMI |
|---:|---:|---:|---:|---:|
| 0.00 | 6.004 | 3.765 | 1.000 | 1.000 |
| 0.05 | 5.977 | 3.730 | 1.000 | 1.000 |
| 0.10 | 5.938 | 3.702 | 1.000 | 1.000 |
| 0.20 | 5.795 | 3.680 | 1.000 | 1.000 |
| 0.35 | 4.953 | 3.289 | 1.000 | 1.000 |
| 0.50 | 3.773 | 2.733 | 1.000 | 1.000 |
| 0.70 | 1.531 | 2.142 | 1.000 | 1.000 |
| 1.00 | -1.337 | -4.205 | 0.219 | 0.793 |

Oracle center guard at `rho = 0` also preserves perfectly.

## Key Figures

### Figure: Preserve fraction versus perturbation

![Preserve fraction versus rho](figures/preserve_fraction_vs_rho.png)

What this tests: whether the original feature-to-expert region survives when
center rows are perturbed.

Observed result: preserve fraction stays at `1.0` through `rho = 0.7`, then
collapses at `rho = 1.0`.

Take-home: the successful initialization has a broad basin, not a single exact
point.

### Figure: Margin versus perturbation

![Margin versus rho](figures/margin_vs_rho.png)

What this tests: whether the basin boundary is tracked by positive margin.

Observed result: margins remain positive through `rho = 0.7` and become
negative at `rho = 1.0`.

Take-home: positive margin predicts the basin in this sweep.

### Figure: Preserve fraction versus margin

![Preserve fraction versus margin](figures/preserve_fraction_vs_margin_scatter.png)

What this tests: whether final preservation is organized by margin rather than
exact center distance.

Observed result: positive-margin points preserve; negative-margin points fail.

Take-home: margin is the better operational coordinate for method design.

## Claim Boundary

Can claim: in the controlled no-position bridge, exact pseudo-center rows are
not necessary. A positive-margin neighborhood around the center preserves
routing through early training.

Cannot claim: real-data feature correctness, semantic expert utility, or that
we already have a label-free margin estimator for real data.

## Next Decision

Move toward a label-free margin acceptance gate: generate multiple candidate
center sets, compute pre-training margin-like guards, and reject candidates
that do not produce a positive-margin basin before training.
