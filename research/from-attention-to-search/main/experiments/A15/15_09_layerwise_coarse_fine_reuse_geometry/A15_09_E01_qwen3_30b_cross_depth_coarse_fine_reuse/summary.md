---
experiment_id: A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse
status: EVIDENCE_COMPLETE_AI_INTERPRETATION_AWAITING_HUMAN_CONFIRMATION
completed: 2026-08-27
primary_panel: C4
replication_panel: C5
model: Qwen3-30B-A3B
---

# Summary: Cross-Depth Coarse--Fine Reuse Audit

## Result first

The stable mathematics and physics fine-class Fisher spaces do **not** show
positive excess reuse of the common eight-parent coarse Fisher space at any of
the six registered blocks. All 24 panel--parent--block cells passed the rank
and A/B stability guards, but every observed raw overlap was below its matched
label-permutation median.

Across all cells, raw projector overlap was 0.00649--0.03858 and the empirical
A/B reproducibility reference was 0.09778--0.27062. Their registered empirical
ratio, corrected overlap, was 0.05964--0.14452. These ratios describe how small
the observed alignment is relative to same-task reconstruction; they are not
an unbiased population estimate and, because the raw values do not beat the
matched null, they are not evidence for a shared semantic subspace.

The safest knowledge update is:

> In these frozen Qwen3-30B-A3B controlled expression panels, stable coarse and
> parent-conditional fine discriminants are mostly geometrically distinct.
> A fine-residual premise is more consistent with this audit than a dominant
> shared-coarse-space premise, but residual causal sufficiency remains untested.

## Per-layer corrected overlap

| Panel / parent | Block 4 | Block 12 | Block 20 | Block 28 | Block 36 | Block 44 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| C4 mathematics | 0.1350 | 0.0659 | 0.0630 | 0.0773 | 0.0687 | 0.0845 |
| C5 mathematics | 0.1445 | 0.0775 | 0.0753 | 0.0765 | 0.0768 | 0.0739 |
| C4 physics | 0.1352 | 0.0811 | 0.0781 | 0.0829 | 0.0862 | 0.0596 |
| C5 physics | 0.1356 | 0.0813 | 0.0895 | 0.0807 | 0.0934 | 0.0719 |

All entries are eligible. No layer was removed or replaced.

## Depth result

There is no general replicated monotone trend across both parents.

- Mathematics: C4 Spearman \(\rho=0.029\) with exact \(p=1.000\); C5
  \(\rho=-0.771\), \(p=0.103\). Cross-panel trajectory correlation is only
  \(\rho=0.200\), \(p=0.714\). The C4 middle-stage minimum does not reproduce in
  C5, and the full shallow/middle/deep ordering differs.
- Physics: C4 \(\rho=-0.486\), \(p=0.356\); C5 \(\rho=-0.600\), \(p=0.242\).
  Both panels have shallow \(>\) middle \(>\) deep stage means, and the cross-panel
  trajectory correlation is \(\rho=0.771\), \(p=0.103\). This is a replicated
  descriptive stage ordering, not a thresholded monotonic law.
- The visible common feature is that Block 4 has the largest corrected overlap
  in all four trajectories, followed by a low 0.060--0.093 band at Blocks
  12--44. This is a descriptive shallow-layer elevation. It does not overturn
  the null result: Block 4 raw overlap is also below the matched permutation
  median in all four cells.

No registered middle-stage maximum or minimum reproduces across C4 and C5.

## Principal-angle result

The best individual \(\cos^2\theta\) across all cells is only 0.1093, equivalent
to a principal angle of at least 70.7 degrees. The first three ordered
components account for 78.2%--93.7% of the already-small total overlap, while
the sixth and seventh components are nearly zero. Descriptively, the residual
alignment is concentrated in a few directions rather than spread across all
seven. Because the Protocol did not register angle-wise permutation bands,
this concentration cannot be called semantic excess reuse by itself.

## Required figures

1. [Raw overlap, permutation/Haar baselines, and reproducibility reference](figures/figure1_raw_overlap_with_baselines.png)
2. [Corrected-overlap trajectories](figures/figure2_corrected_overlap_trajectory.png)
3. [Seven principal-angle components](figures/figure3_principal_angle_cos2_heatmap.png)

## Claim boundary

### Directly established

- all 24 registered coarse/fine cells are rank-seven and A/B stable under the
  frozen gates;
- corrected overlap is 0.05964--0.14452;
- raw overlap is below the matched label-permutation median in 24/24 cells and
  below its 2.5th percentile in 15/24 cells;
- physics, but not mathematics, reproduces the complete
  shallow \(>\) middle \(>\) deep stage ordering;
- no replicated non-monotone middle-stage extremum is established.

### Allowed interpretation

Stable parent-conditional fine discrimination is not organized as substantial
reuse of the stable common coarse discriminant space in these panels. The
geometry is more compatible with fine information living mainly outside the
coarse space.

### Not established

This audit does not show that the native Router uses either space, that
orthogonal removal is harmless, that a fine-residual Router improves loss,
that layer-specific routing is useful, or that the result generalizes beyond
mathematics/physics and the controlled C4/C5 panels. Low overlap is not causal
necessity, functional sufficiency, or architecture gain.

## Unique next question

> After conditioning on one parent, is fine-class function causally retained in
> the complement of the coarse Fisher space, and specifically lost when the
> fine-specific residual directions are removed?

The next minimal test should remain a frozen-representation intervention with
cross-fitted evaluation. It should compare the native state, coarse-only
projection, coarse-complement projection, and removal of the registered
fine-specific residual directions. It must not begin with Router training.

## Sources

- [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/15_09_layerwise_coarse_fine_reuse_geometry_anchor.md)
- [Approved Protocol](protocol.md)
- [Detailed evidence record](detailed.md)
- Worker run: `/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z`

