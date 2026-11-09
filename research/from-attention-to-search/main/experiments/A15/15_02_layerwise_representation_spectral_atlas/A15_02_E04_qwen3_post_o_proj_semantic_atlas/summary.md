# A15_02_E04 Summary: Post-`o_proj` Full-Attention Semantic Variance Atlas

## Verdict

The typed verdict is **`depth_pass_spectral_fail`**.

- The post-`o_proj` attention branch retains the late-layer increase in fine-relative-to-coarse semantic discriminability.
- Actual between-class variance remains F1-dominant for both semantic granularities in every block 1--35.
- A modest late middle-band relative enrichment passes its local registered controls, but tail enrichment fails the independent calibration-half stability guard; the joint fixed non-head spectral clause therefore fails.

The narrow knowledge update is:

> Cross-head mixing by `o_proj` preserves the late fine-semantic refinement signal and redistributes a small relative share toward the middle spectrum, but it does not establish a stable full non-head coordinate or a useful Router feature.

## Primary Depth Result

Discriminability is \(D=B/W\): between-class variance divided by within-class wording/fact variation. The same-layer fine-versus-coarse comparison is

\[
R=\log(D_{fine}/D_{coarse}).
\]

Median \(R\) rises from 0.131 in blocks 1--12 to 0.762 in blocks 25--35. The registered contrast is \(T_{post}=0.631\) with hierarchical-bootstrap 95% interval [0.553, 1.148]. All four template contrasts and all eight leave-one-parent contrasts are positive. Blocks 35 and 36 have fine/coarse discriminability ratios 2.13 and 2.36, so the last block does not reverse the trend.

![Cross-site depth comparison](figures/figure1_cross_site_depth_comparison.png)

Pre- and post-`o_proj` trajectories are descriptively close. Site-to-site differences are not causal estimates because no activation replacement or matched intervention was performed.

## Spectral Result

The 4096 dimensions are divided into 16 equal-rank 256-dimensional bands: F1=head, F2--F8=middle, and F9--F16=tail. Actual semantic variance \(b\) is maximal in F1 for both roles in every block 1--35.

Late fine-versus-coarse relative actual-variance enrichment is -0.106 in head, +0.063 in middle, and +0.159 in tail. In ordinary language, relative to each role's total semantic variance, fine semantics allocate about 10.0% less share to head, 6.5% more to middle, and 17.2% more to tail than coarse semantics.

The middle estimate exceeds the equal-dimensional random-direction q95=0.059 and remains positive under design/confirmation templates, both calibration-half bases, nuisance residualization, and all eigenvalue floors. The tail estimate is larger but changes direction in at least one late-layer independent-half basis, so tail does not pass. Because the registered joint spectral clause requires stable middle and tail evidence, the typed spectral verdict remains Fail.

![Post-o_proj layer-band atlas](figures/figure2_post_o_proj_layer_band_heatmaps.png)

![Band-local discriminability](figures/figure3_decisive_post_o_proj_band_discriminability.png)

## Validity And Boundary

All 36 blocks, 65,536 calibration tokens, and 512 semantic records are covered. Native module output and direct \(W_Oa\) replay agree exactly in the final smoke/full route; FP32-versus-direct-FP64 Gram error is at most \(7.22\times10^{-8}\). Covariance reconstruction, energy conservation, half-split basis stability, template checks, leave-one-parent checks, nuisance residualization, and floor sensitivity pass their registered guards.

The first ACP attempt (`om-1hc00w00`) is an invalid engineering record: its guard changed the GEMM shape while checking bfloat16 replay. After repairing the guard without changing data, model, metric, threshold, or scientific condition, the formal 8×5090 job `om-5y1d8uf1` succeeded with zero retries.

This audit establishes where a frozen semantic signal is visible. It does not prove that `o_proj` causally creates the middle pattern, that the model performs compositional computation, that a fixed middle band predicts expert utility, or that spectral routing improves training.

The one next decision is whether an independent balanced taxonomy reproduces both positive post-`o_proj` depth contrast and the modest late middle enrichment. Until then, the middle pattern is a one-taxonomy representation finding, not a Router coordinate.
