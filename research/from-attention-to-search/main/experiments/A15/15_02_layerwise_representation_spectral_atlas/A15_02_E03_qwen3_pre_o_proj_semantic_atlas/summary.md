# A15_02_E03 Summary: Full-Width Qwen3-8B Attention-Output Semantic Variance Atlas

## Verdict

The typed verdict is **`depth_pass_spectral_fail`**.

- Fine-relative-to-coarse discriminability increases from early to late blocks in the full 4096-dimensional pre-`o_proj` attention output.
- Actual between-class variance for both semantic granularities remains F1-dominant in every block from 1 through 35.
- A descriptive late tail enrichment does not survive the registered calibration-half direction guard; middle enrichment fails additional design, floor, and half-split guards. No fixed non-head semantic coordinate is established.

The narrow knowledge update is:

> Late fine-semantic refinement is already present before `o_proj`, residual merging, and the MLP, but it remains broadly distributed across the covariance spectrum and does not identify a stable middle/tail routing coordinate.

## Primary Result

Discriminability is \(D=B/W\), between-class variance divided by within-class perturbation variance. The comparison statistic is

\[
R=\log(D_{fine}/D_{coarse}).
\]

For full pre-`o_proj` attention, median \(R\) rises from 0.153 in blocks 1--12 to 0.764 in blocks 25--35. The registered contrast is \(T_{attention}=0.611\) with paired basic-bootstrap 95% interval [0.624, 1.156]. All four template contrasts and all eight leave-one-parent contrasts are positive. Blocks 35 and 36 have fine/coarse discriminability ratios 1.99 and 2.21, so the final block does not reverse the trend.

![Depth trajectory and residual comparison](figures/figure1_attention_depth_and_residual_comparison.png)

The residual E01 contrast is smaller descriptively (\(T_{depth}=0.451\)), but the two architecture boundaries are not a causal ablation: `o_proj`, residual merging, normalization, and the MLP intervene between them.

## Spectral Result

The 4096 dimensions are divided into 16 equal-rank 256-dimensional bands: F1=head, F2--F8=middle, and F9--F16=tail. Actual between-class variance \(b\) is maximal in F1 for both semantic roles in every block 1--35.

Late fine-versus-coarse relative variance enrichment is -0.107 in head, -0.010 in middle, and +0.162 in tail. The tail point exceeds the equal-dimensional random q95 of 0.059, but it does not remain positive across every late layer under both independent calibration-half bases. The registered spectral clause therefore fails.

![Layer-band atlas](figures/figure2_attention_layer_band_heatmaps.png)

![Band discriminability decision figure](figures/figure3_decisive_attention_band_discriminability.png)

## Validity And Boundary

All 36 blocks, 65,536 calibration tokens, and 512 semantic records are covered. Hook replay and head concatenation are exact; `o_proj` reconstruction relative error is \(1.50\times10^{-7}\); the FP32-versus-direct-FP64 Gram error is at most \(7.03\times10^{-8}\). Covariance reconstruction, projection energy conservation, and H/M/T half-split stability pass.

E01's object is the raw full decoder-block residual output, not the strict MoE post-attention input. E03's object is the direct input to `self_attn.o_proj`. The results localize where the signal is observable; they do not establish attention necessity, module-level causality, compositional computation, Router utility, expert compatibility, or training benefit.

The one next decision is whether an independent balanced taxonomy reproduces positive depth contrasts at both pre-`o_proj` attention and block-residual boundaries. Fixed middle/tail coordinates remain ineligible for Router training.
