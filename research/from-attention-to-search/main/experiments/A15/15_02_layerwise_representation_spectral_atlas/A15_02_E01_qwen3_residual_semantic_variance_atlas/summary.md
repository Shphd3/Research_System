# A15_02_E01 Result: Qwen3-8B Coarse/Fine Depth And 16-Band Atlas

## Conclusion

The result is clause-specific:

- **Depth clause: Pass.** Conditional fine semantics become more discriminable relative to coarse semantics in late Qwen3-8B blocks.
- **Actual-variance head dominance: Pass.** F1 is the largest actual between-class variance band for both coarse and fine semantics.
- **Fine middle/tail specificity: Fail.** The late fine advantage is broadly distributed across the spectrum and is not stably enriched in F2--F8 or F9--F16 beyond equal-dimensional random orientations.

The supported interpretation is that late Qwen3-8B states reorganize within-parent fine classes into tighter, more separable groups. This is not evidence for a fixed covariance-rank fine-semantic channel.

## Primary Metric And Direct Result

For each representation site and semantic granularity,

\[
D=\frac{\text{between-class variance}}{\text{within-class template/wording variance}},
\qquad
R_\ell=\log\frac{D_{\ell,\mathrm{fine}}}{D_{\ell,\mathrm{coarse}}}.
\]

The median \(R\) was 0.0009 in registered early blocks 1--12 and 0.4523 in registered late blocks 25--35. The paired depth contrast was

\[
T_{\mathrm{depth}}=0.4514,
\qquad 95\%\ \mathrm{CI}=[0.3327,1.1891].
\]

Thus the late fine/coarse discriminability ratio was about 1.57 versus about 1.00 early. All four template contrasts and all eight leave-one-parent-out contrasts were positive. Block 35 had \(D_{coarse}=0.871\) and \(D_{fine}=1.590\); block 36 remained in the same direction at 0.823 and 1.513, so there was no last-block reversal.

![Decisive depth-by-band discriminability heatmap](figures/figure4_decisive_depth_band_discriminability_heatmap.png)

The left panel shows \(\log(j_{fine}/j_{coarse})\) for every site and 16 equal-rank bands, where \(j\) is bandwise between/within-class variance. Red means fine classes are more separable; black dots mark paired 95% intervals excluding zero. The fine advantage becomes broad across F1--F16 after about block 28. The right panel shows the basis-free whole-state \(R_\ell\) trajectory.

## Spectral Result

![Layer-by-band semantic variance atlas](figures/figure2_layer_band_coarse_fine_heatmaps.png)

The atlas separates actual semantic variance \(b\), background-normalized variance \(q\), and band discriminability \(j\). At block 35, coarse head/middle/tail \(b\) was 38.08/17.49/15.91 per direction, while fine \(b\) was 24.97/15.04/13.42. Fine semantics therefore did not have larger absolute variance. Fine \(j\), however, was 1.43/1.53/1.72 versus coarse 1.05/0.82/0.88, showing that the fine gain came from greater separation relative to within-child template variation.

Late fine middle/tail relative-share estimates were only 0.0347/0.0359 in log units. Their 95% intervals crossed zero and the estimates were below the equal-dimensional random-orientation late q95 of 0.0617. The registered spectral-specificity clause therefore failed.

## Boundary And Next Decision

This frozen audit applies to one Qwen3-8B snapshot, one balanced English academic taxonomy, and one shared readout prompt. It does not establish compositional computation, semantic causality of covariance rank, Router utility, or training benefit.

Typed verdict: `depth_pass_spectral_fail`. The one next decision is whether to replicate the basis-free depth effect on an independent taxonomy. Fixed middle/tail Router training is not admitted by this result.

All 512 text sequences are recorded in [actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json). See [detailed.md](detailed.md) for the complete evidence ledger.
