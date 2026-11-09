# A15_17_E05 Result Summary: 0--10B Sidecar-SAE Representation, Loss, and Gradient Audit

Status: `COMPLETED_ELIGIBLE_AI_READING_AWAITING_RESEARCHER_CONFIRMATION`  
Protocol: [protocol.md](protocol.md)  
Full record: [detailed.md](detailed.md)  
Chinese companion: [summary_cn.md](summary_cn.md)

## Purpose

Determine whether an SAE used only as a training-time reconstruction sidecar makes the language model's native representation more class-separable while attaining lower, or at least non-worse, language-model loss at matched cumulative valid tokens. A second objective was to measure the total auxiliary-gradient pressure from one, two, and eight sidecars on shared backbone parameters and to calibrate their near-90-degree angles against high-dimensional random references.

## Hypothesis

If the sidecar usefully reorganizes the backbone, Fisher geometry and held-out probe accessibility should improve together, survive direct removal of the largest uncentered singular direction, and not coincide with worse token-aligned language-model loss. A Fisher-only increase is geometry, not improved representation quality. A near-90-degree angle is not special orthogonality unless it is distinguished from a dimension-matched random reference.

## Analysis Method

The audit used exact 0/0.5/1/3/5/10B checkpoints for M0, M2, S7, S37, and SALL. Frozen synthetic panel P and frozen M2D2 panel N were reported separately. The shared primary surface was each model's native final representation; sidecar Attention outputs and SAE reconstructions were compared separately.

For \(C\) classes, class-balanced Fisher geometry was

\[
B=\frac1C\sum_c\lVert\mu_c-\bar\mu\rVert_2^2,
\qquad
W=\frac1C\sum_c\mathbb E_{x\mid c}\lVert x-\mu_c\rVert_2^2,
\qquad
F=\frac BW.
\]

The audit jointly reported \(B/W/F\), held-out linear probes, fixed two-layer neural probes, and the same metrics after fit-only direct removal of the largest uncentered singular direction. Fisher differences used 1,000 paired class-stratified bootstrap draws; absolute Fisher used 1,000 balanced-label permutations.

On 281,431,040 shared backbone parameters, \(g_C\) was the language gradient and \(g_A\) was the sum of coefficient-weighted, layer-mean reconstruction gradients:

\[
\rho=\frac{\lVert g_A\rVert}{\lVert g_C\rVert},
\qquad
c=\frac{g_C^\top g_A}{\lVert g_C\rVert\lVert g_A\rVert}.
\]

Cosine and angle were suppressed whenever either norm was numerically negligible. Direction was calibrated with the dimension-matched isotropic bound and an analytic magnitude-preserving sign-flip null. Main gradient values are four-batch means.

## Conclusion

**The result does not support the strong claim that the SAE sidecar already yields a stable training benefit or uniformly better native representations.** At exact 10B, S37 and SALL had credible Fisher differences on selected panels that survived top-direction removal, but the large P-panel gap was driven substantially by a sharp 10B M0 endpoint drop and was only weakly mirrored by probe changes. The 0--10B trajectories did not show a coherent advantage across models and metrics. All three sidecar models had worse frozen-M2D2 held-out NLL than M0.

The strongest allowed result is a checkpoint- and dataset-dependent geometric reorganization, with small positive native-readout point differences for S37/SALL at 10B, not a causal or general representation-quality gain. All absolute Fisher values were above balanced-label permutation nulls (\(p=0.000999\)). On P-raw, the S37 and SALL Fisher differences versus M0 were \(+0.430\) (95% CI \([0.032,0.493]\)) and \(+0.447\) (\([0.045,0.523]\)); S7 crossed zero. On N-raw, SALL was \(+0.0205\) (\([0.0137,0.0291]\)), while S37 was a small \(+0.0087\) (\([0.0002,0.0186]\)). These effects largely survived direct top-direction removal. However, across eleven terminal sidecar-layer pairs, reconstruction increased Fisher in 5/11 P-raw and 8/11 N-raw cases, while increasing linear-probe accuracy in only 0/11 and 1/11; reconstruction therefore changes geometry without reliably improving accessibility.

At 10B, M0's training NLL was 3.34677 and frozen-M2D2 held-out NLL was 3.61427. S7/S37/SALL training-NLL differences were \(+0.01091/+0.00496/-0.00227\), but their held-out differences were all worse: \(+0.00729/+0.01853/+0.00619\). M2 was lower on both surfaces (\(-0.00579/-0.01245\)), but is a serial mediated-SAE condition rather than a sidecar-count control.

The sidecar objective used a layer mean with total \(\lambda_{\mathrm{rec}}=1\), giving direct per-sidecar coefficients 1, 0.5, and 0.125 for S7, S37, and SALL. Their 10B reconstruction/LM-loss ratios were 2.98%, 6.59%, and 5.15%, whereas their measured shared-parameter gradient ratios were 3.54%, 3.06%, and 1.24%. Thus layer averaging does not equalize total backbone pressure, and scalar loss ratios do not predict gradient ratios.

The 10B cosines were \(+0.01348\), \(+0.00595\), and \(+0.01208\), corresponding to angles 89.23°, 89.66°, and 89.31°. The dimension-matched isotropic 97.5% absolute-cosine bound was only \(1.168\times10^{-4}\). All 72 reliable model-checkpoint-batch whole-backbone cells lay outside that bound, and only 7/72 were compatible with the magnitude-preserving sign-flip null. The gradients are therefore near 90 degrees but not random-compatible: they contain detectable structured alignment or opposition whose sign is unstable. Their first-order LM-parallel fractions \(\rho c\) at 10B were nevertheless only 0.0477%, 0.0182%, and 0.0150%. This does not establish a mechanism for escaping local optima.

The earlier `0.1/0.2/0.8` total-coefficient proposal is not supported as a cross-layer-count fairness rule. The next coefficient test should target total shared-backbone \(\rho\), not equal direct per-sidecar weights. An AI-proposed conservative starting target is \(\rho_*=0.02\), with a calibration-window or EMA controller

\[
\lambda_t=\operatorname{clip}\left(\frac{\rho_*}{\widetilde\rho_{\lambda=1,t}},\lambda_{\min},\lambda_{\max}\right).
\]

The 3/5/10B median measurements imply starting total coefficients near 0.57/0.69/1.40 for S7/S37/SALL. These are gradient-balancing starts, not optima; SALL must not simply be upweighted because its held-out NLL is already worse. The single proposed next experiment is a matched S7-versus-SALL comparison of current \(\lambda=1\) and target-\(\rho=0.02\), using checkpoints 0/0.1/0.25/0.5/1B before any gated continuation to 3/5/10B.

Key figures: [geometry trajectory](figures/13_geometry_trajectory_reader.png), [10B Fisher credibility](figures/14_fisher_10b_credibility_reader.png), [training loss](figures/05_language_loss.png), [held-out loss](figures/12_heldout_m2d2_language_loss.png), [raw versus reconstruction](figures/10_terminal_raw_vs_reconstruction.png), and [shared-gradient random calibration](figures/15_shared_gradient_random_calibration_reader.png). Full source tables are in [tables/](tables), including the compact [10B sidecar loss/gradient comparison](tables/exact_10b_sidecar_loss_gradient_comparison.csv).

The audit cannot establish increased parameter capacity, general language ability, downstream performance, a causal sidecar-count effect, native use of the reconstruction, or a special orthogonal-optimization mechanism from these single-seed unmatched training trajectories.
