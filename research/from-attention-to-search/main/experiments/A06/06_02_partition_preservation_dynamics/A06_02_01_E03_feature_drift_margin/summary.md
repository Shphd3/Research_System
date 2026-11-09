---
experiment_id: A06_02_01_E03_feature_drift_margin
anchor_id: A06_02_01_E03_feature_drift_margin
status: completed
run_name: a06_17_03_feature_drift_margin_boundary_full_20260629_011201
job_id: local-two-gpu
canonical_language: en
---

# Summary: A06_02_01_E03 Feature Drift Margin Boundary

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol:
`protocol.md`

## Purpose

This audit asks whether A06_02_01_E02 preservation has a measurable geometric
limit: does feature-center drift stay inside the initial distance to the
nearest expert boundary?

## Exact Setup

Full local two-GPU rerun:
`a06_17_03_feature_drift_margin_boundary_full_20260629_011201`.

Setup matches A06_02_01_E02: one-layer Transformer + top-1 MoE, 4 experts,
feature slot length 4, no learned absolute positional embedding, route on the
last slot token, C0-C3 bridge cells, 8 seeds, snapshots through step 1600.

Conditions: pseudo-center init, oracle-center init, random Gaussian guard.

## Primary Metric

Primary metric: boundary consumption,

\[
B_f(t)=1-\frac{d_f^{\mathrm{frozen}}(t)}{d_f(0)+\epsilon}.
\]

It measures how much of the step-0 nearest-boundary distance has been consumed
by the observed feature-center trajectory. Values below 1 mean the feature
center has not crossed the frozen step-0 nearest boundary.

Guards:

- dynamic margin under the current router rows;
- dynamic switch rate;
- frozen switch rate;
- feature NMI.

## Result

The observed successful preservation stays inside the margin buffer.

For pseudo-center and oracle-center initialization:

- final feature NMI is 1.000 in every C0-C3 cell and seed;
- final dynamic switch rate is 0.000;
- final frozen switch rate is 0.000;
- final mean boundary consumption is about 0.40;
- final worst observed boundary consumption is below 0.70;
- final dynamic margin remains positive, with the worst pseudo-center feature
  still at 1.838.

Random Gaussian is the guard: feature NMI is lower and unstable, dynamic margin
is negative on average, and switch rate is 0.375.

| Condition | Final feature NMI mean | Max boundary consumption mean | Worst max consumption | Min dynamic margin mean | Worst dynamic margin | Dynamic switch rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pseudo-center | 1.000 | 0.530 | 0.693 | 3.417 | 1.838 | 0.000 |
| Oracle-center | 1.000 | 0.523 | 0.691 | 3.573 | 2.312 | 0.000 |
| Random Gaussian | 0.783 | 21.697 | 376.255 | -3.646 | -4.662 | 0.375 |

Interpretation: A06_02_01_E03 supports the finite margin-buffer explanation for
the observed A06_02_01_E02 trajectory. The feature centers drift, but in successful
center-init runs they do not consume the full step-0 boundary distance, and the
current router keeps a positive margin.

## Key Figures

### Figure: Boundary Consumption Trajectory

![Boundary consumption trajectory](figures/boundary_consumption_trajectory.png)

What this tests: whether feature-center drift approaches the step-0 nearest
expert boundary.

Observed result: pseudo-center and oracle-center stay well below 1 throughout
training. Random is unstable because its initial boundary can be small or
misaligned.

Allowed claim: observed center-init preservation stays within the initial
margin buffer.

What this does not prove: the exact adversarial perturbation limit.

### Figure: Dynamic Margin Trajectory

![Dynamic margin trajectory](figures/dynamic_margin_trajectory.png)

What this tests: whether the current router still gives the matched feature a
positive margin.

Observed result: center-init conditions keep positive dynamic margins; random
has negative margins.

Allowed claim: the current router boundary remains safe for center-init runs.

### Figure: Final Boundary Consumption Versus Margin

![Final boundary consumption versus margin](figures/final_boundary_consumption_vs_margin.png)

What this tests: whether high boundary consumption coincides with margin loss.

Observed result: center-init points remain in the positive-margin region even
when consumption is moderately high.

Allowed claim: observed drift consumes part of the buffer but does not cross
the decision boundary.

## Claim Boundary

Can claim: in the controlled no-position bridge, observed center-init
preservation is consistent with a finite margin-buffer boundary. The successful
features drift, but not far enough to cross the initial or dynamic boundary.

Cannot claim: exact perturbation tolerance, real-DCLM behavior, semantic
experts, or utility.

## Next Decision

Use boundary consumption and dynamic margin as design metrics for future
margin-aware center search. If a future method produces centers with small
initial boundary distance or high predicted consumption, it should not be
advanced to preservation training.
