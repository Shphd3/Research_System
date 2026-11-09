# A15_02_E02 Corrected Summary: Qwen3-8B Individual Attention-Head Semantic Atlas

> Correction, 2026-08-05. The prior template split mixed NumPy basic and advanced indexing, moving the template axis before reshape and scrambling parent/template hierarchy. The corrected implementation takes templates explicitly along axis 2 and adds an axis-order regression test. This page and its companion tables/figures supersede the prior result.

## Verdict

The corrected typed verdict is **`attention_depth_pass_head_localization_pass_spectral_fail`**.

- The pooled pre-`o_proj` attention depth effect passes: \(T_{attention}=0.6106\), paired basic-bootstrap 95% interval [0.6039, 1.2096], with 4/4 template and 8/8 leave-parent directions positive.
- Individual-head localization passes: 9 late layer-head cells exceed the family-wise maximum-permutation q95 of 1.746 and all registered robustness conditions.
- Within-head spectral specificity fails: zero bands pass paired uncertainty, basis stability, and same-head random-8D orientation control.

The nine qualified cells are L30H27, L30H5, L32H15, L31H8, L30H25, L33H10, L32H20, L31H11, and L34H14. The strongest is L30H27 with \(R=2.425\), a fine/coarse discriminability ratio of about 11.30.

![Corrected layer-head atlas](figures/figure1_layer_head_discriminability_atlas.png)

![Corrected selected-head result](figures/figure2_head_localization_and_global_null.png)

![Corrected within-head band atlas](figures/figure3_selected_head_16band_atlas.png)

The corrected result preserves the architecture-level depth effect and selection-corrected head localization, but withdraws the prior single F1-band claim. It establishes no fixed head, middle, or tail coordinate and does not establish attention causality, head identity across layers, Router utility, expert compatibility, or training benefit.

The one next decision is whether an independent balanced taxonomy reproduces the pooled pre-`o_proj` depth contrast and at least one family-wise-corrected late head. Fixed covariance bands remain ineligible for Router training.
