---
protocol_id: A06_01_07_E02_static_2x2_region_audit
anchor_id: A06_2x2_expert_geometry_gate
status: executed_after_user_request
created: 2026-06-17
canonical_language: en
---

# Protocol: A06_01_07_E02_static_2x2_region_audit

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question:
In the minimal \(2\times2\) setting, which expert-initialization-induced compatibility metric can define a non-degenerate routing rule that supports both balanced load and metric-defined specialization under uniform input?

Experiment role:
This is a follow-up boundary audit for A06_01_07_E01. It tests whether the 2D load-balance conclusions depend on using only the unit circle, or whether they survive when input radius varies and when the input region is uniformly filled.

## 1. Decision Question

When 2D inputs are sampled from radially symmetric regions or simple centered regions, does the selected expert-aware score still route near 50/50 while preserving positive margin?

## 2. Tested Hypothesis

H1:
For radially symmetric inputs \(x=ru\) with \(u\) uniformly distributed on \(S^1\), homogeneous score differences keep the same sign as on the unit circle. Therefore load should match the unit-circle result, while margin changes with the radius distribution.

H2:
For centered regions with enough symmetry, especially the centered square, centered M4 should still route near 50/50 in 2D because the centered quadratic score difference changes sign under a 90-degree rotation.

H3:
Low-radius mass should not change the assignment rule, but it should reduce margin and increase the low-margin fraction.

## 3. Rival Explanations

R1:
The previous 50/50 result is only a unit-circle artifact and disappears when inputs fill a 2D region.

R2:
Raw M4 looks useful only because some expert conditions have equal average energy; random Gaussian experts should expose raw average-energy bias.

R3:
Uniform load can remain good while specialization evidence weakens because many points lie near the origin and have tiny score differences.

## 4. Data / Model / Algorithm / Objective

Experts:
Two experts are \(2\times2\) matrices \(A_1,A_2\) using the same condition families as A06_01_07_E01:

- `C1_random_unconstrained`;
- `C2_orthogonal_equal_singular`;
- `C3_orthogonal_unequal_singular`;
- `C4_near_identical`;
- `C5_separated_anisotropic`.

Input distributions:

- `unit_circle`: \(x\) uniformly on \(S^1\).
- `uniform_disk`: \(x\) uniformly in the unit disk.
- `annulus`: \(x\) uniformly in \(0.5\leq \|x\|\leq 1\).
- `centered_square`: \(x\) uniformly in \([-1,1]^2\).
- `near_origin_mixture`: radially symmetric mixture with most mass near the origin.
- `shifted_disk`: unit disk shifted away from the origin, a symmetry-breaking control.
- `centered_rectangle`: centered rectangle, a non-rotational symmetric region control.

Compared scores:

- M1 signed prototype: \(q_e(x)=x^\top m_e\).
- M2 unsigned prototype: \(q_e(x)=(x^\top m_e)^2\).
- M3 top-1 projection: \(q_e(x)=\|V_{e,1}^\top x\|^2\).
- M3 full-span control: \(q_e(x)=\|V_{e,1:2}^\top x\|^2\).
- raw M4: \(q_e(x)=x^\top A_e^\top A_ex\).
- trace-centered M4: \(\tilde q_e(x)=x^\top (G_e-\mathrm{tr}(G_e)I/2)x\). This is the proof-facing radial extension because the centering scales with \(\|x\|^2\).
- distribution-centered M4: \(q^P_e(x)=x^\top G_ex-\mathbb{E}_{x\sim P}[x^\top G_ex]\). This is included as a confusion control; when radii vary and experts have different traces, it need not preserve the unit-circle assignment.

## 5. Conditions, Seeds, And Checkpoints

Seeds:
100 expert-geometry seeds per stochastic condition.

Samples:
20,000 input samples per seed and distribution.

Checkpoints:
None. This is a static routing audit.

## 6. Primary Metric

Primary metric:
`natural_load_error = |P(g(x)=1)-0.5|`, read together with `mean_margin`.

Why:
The current question is whether a score rule can split uniform 2D feature mass. Load error answers the split question. Mean margin prevents a false positive where the split is balanced but the expert preference is numerically unclear.

## 7. Secondary Metrics

- `low_margin_fraction`: fraction of points with selected-expert margin below \(10^{-4}\).
- `degeneracy_rate`: fraction of nearly tied scores.
- `mean_margin_ratio_to_unit_circle`: margin change relative to unit circle for the same expert condition and metric.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good:
`annulus` should preserve unit-circle assignments and keep stronger margin than `uniform_disk`.

Known bad:
`C2_orthogonal_equal_singular` should remain degenerate for M3 top-1 and M4 because experts have no directional distinction.

Known confusing:
`near_origin_mixture` can keep balanced load but have weak margin; it should not be read as strong specialization.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Distribution sampling | Did the sampler implement the intended region? | Radius and coordinate summaries | Pass if summaries match definitions | `tables/distribution_summary.csv` | Detailed setup |
| Score computation | Are raw, trace-centered, and distribution-centered scores separate? | Per-method rows | Pass if all M4 variants are present | `tables/per_seed_region_metrics.csv` | Main results |
| Load/margin read | Does load survive radius changes? | Aggregate table | Pass if symmetric cases keep low load error and positive margin | `tables/region_metric_summary.csv` | Summary |
| Boundary controls | Do broken-symmetry controls break the proof boundary? | Shifted/rectangle rows | Pass if controls are not overclaimed | Figures and boundary text | Claim boundary |

## 10. Algorithm Specification, If Nontrivial

input:
Expert matrices, input samples, metric definitions.

parameters:
100 seeds, 20,000 samples per distribution, low-margin threshold \(10^{-4}\).

intermediate variables:
\(G_e=A_e^\top A_e\), trace-centered matrices \(G_e-\mathrm{tr}(G_e)I/2\), score differences, analytic distribution second moment, and distribution-centered M4 mean response.

steps:
Generate expert pairs, sample each distribution, compute scores, route by larger score, record load and margin, aggregate by condition/distribution/method, produce figures and result records.

outputs:
`summary.md`, `detailed.md`, aggregate tables, and central figures.

pass conditions:
Radially symmetric and centered-square settings preserve near-balanced centered-M4 load in non-degenerate expert conditions; margin changes as predicted by radius.

fail conditions:
Radius variation alone breaks the 2D trace-centered-M4 split, or centered-square uniform input becomes strongly imbalanced without a symmetry explanation.

failure reasons:
Distribution sampler mismatch, metric centering mismatch, degeneracy, low-margin ambiguity, or actual failure of the symmetry hypothesis.

## 11. Success / Failure / Insufficient Evidence

Success:
The run confirms that radius variation does not invalidate the 2D proof-facing claim, while identifying which region distributions fall outside the proof boundary.

Failure:
Uniform disk or annulus breaks the unit-circle assignment/load behavior for homogeneous scores.

Insufficient evidence:
Only load is reported, or raw M4, trace-centered M4, and distribution-centered M4 are mixed.

## 12. What This Cannot Claim

This experiment cannot claim trainable router learnability, real MoE specialization, high-dimensional generalization, semantic feature specialization, or expert utility binding.

## 13. Approval Status

Executed after explicit user request on 2026-06-17.
