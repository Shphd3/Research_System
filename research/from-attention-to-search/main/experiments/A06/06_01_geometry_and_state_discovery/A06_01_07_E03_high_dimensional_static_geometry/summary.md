# Summary: A06_01_07_E03_high_dimensional_static_geometry

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Protocol: `protocol.md`

## Purpose

This experiment tests whether the 2D centered-M4 load-balance result becomes a usable high-dimensional rule under uniform sphere features.

The uncertainty reduced here is not whether a trainable router can learn the rule. The uncertainty is whether raw M4, centered M4, calibrated M4, or a weighted top-r proxy is the right next static expert-geometry target.

## Exact Setup

Inputs are sampled from \(x\sim\mathrm{Unif}(S^{d-1})\) for \(d\in\{2,4,8,16,32,64,128,256,512\}\). The run uses 100 seeds, 20,000 evaluation samples per seed, and 5,000 calibration samples per seed.

Compared score rules:

- raw M4: \(q_e(x)=x^\top G_ex\);
- centered M4: \(\tilde q_e(x)=x^\top G_ex-\mathrm{tr}(G_e)/d\);
- calibrated M4: raw M4 with a median threshold fit on calibration samples;
- weighted / unweighted top-r spectral proxies.

Expert conditions:

- Gaussian-like random spectrum proxy;
- equal isotropic;
- unequal isotropic;
- random anisotropic spectrum;
- separated low-rank;
- near-identical;
- spiked traceless counterexample;
- balanced spectrum control.

Implementation caveat:
The `random_gaussian` condition is a fast Gaussian-like positive-spectrum proxy, not an exact dense Wishart eigendecomposition. The run still tests the intended spectral-spread mechanism, but it should not be cited as exact Gaussian-matrix evidence.

## Primary Metric

Primary metric: centered-M4 natural load error read together with mean margin and spectral spread.

Load error decides whether uniform features are distributed close to 50/50. Mean margin decides whether the split has a clear score preference. Spectral spread tests the proposed high-dimensional reason for success or failure:

\[
r_3(H_0)=\frac{\sum_i|\lambda_i|^3}{(\sum_i\lambda_i^2)^{3/2}}.
\]

## Result

Centered M4 is supported as the right high-dimensional static target, but only as an approximate or calibrated rule.

Key evidence at \(d=512\):

| Condition | Method | Load error | Mean margin | \(r_3\) | Interpretation |
| --- | --- | ---: | ---: | ---: | --- |
| random Gaussian spectrum proxy | raw M4 | 0.4644 | 0.0287 | 0.2690 | Raw response is heavily biased by average expert energy. |
| random Gaussian spectrum proxy | centered M4 | 0.0358 | 0.0029 | 0.2690 | Centering greatly improves load but is not exact. |
| random Gaussian spectrum proxy | calibrated M4 | 0.0070 | 0.0029 | 0.2690 | Calibration enforces load while preserving small margin. |
| random anisotropic | raw M4 | 0.4556 | 0.0560 | 0.3884 | Raw M4 is again highly imbalanced. |
| random anisotropic | centered M4 | 0.0574 | 0.0094 | 0.3884 | Centering helps but spectrum remains too spiky for exact balance. |
| spiked counterexample | centered M4 | 0.1824 | 0.9659 | 0.9971 | Centering fails as predicted when one eigen-direction dominates. |
| balanced spectrum control | centered M4 | 0.0029 | 0.0543 | 0.0505 | Spread spectrum gives near-perfect balance. |
| separated low-rank | centered M4 | 0.0028 | 0.0368 | 0.1768 | Structured balanced low-rank difference works. |

Across non-isotropic conditions, spectral spread predicts centered-M4 load error: overall Pearson correlation between \(r_3\) and centered load error is 0.726, and Spearman correlation is 0.565.

Calibration is useful but not a specialization proof. In near-identical experts at \(d=512\), calibrated load error is 0.0068, but mean margin is only 0.0005 and low-margin fraction is 0.1275.

Weighted top-r proxies improve with rank, but small rank is not enough in the broad random conditions. At \(d=512\), weighted top-r agreement with full centered M4 is:

| Condition | r=8 | r=32 | r=128 |
| --- | ---: | ---: | ---: |
| random Gaussian spectrum proxy | 0.7438 | 0.8161 | 0.8697 |
| random anisotropic | 0.8004 | 0.8715 | 0.9322 |
| separated low-rank | 0.6684 | 1.0000 | 1.0000 |

## Key Figures

### Figure: Load Error Versus Dimension

![Load error versus dimension](figures/load_error_vs_dimension.png)

What this tests:
Whether raw, centered, and calibrated M4 behave differently as dimension increases.

How to read:
Lower load error means closer to 50/50. The plot highlights random spectrum, spiked, and balanced controls.

Observed result:
Raw M4 remains highly imbalanced in random spectrum settings. Centered M4 improves strongly but fails in the spiked control. Calibrated M4 stays close to balanced.

Take-home:
Raw M4 is not the high-dimensional load target. Centering is the right direction, but calibration is still needed for robust load control.

What this does not prove:
It does not prove a trainable router can implement these scores.

### Figure: Load Error Versus Spectral Spread

![Load error versus spectral spread](figures/load_error_vs_spectral_spread.png)

What this tests:
Whether the spectral-spread statistic tracks centered-M4 load imbalance.

How to read:
Higher \(r_3\) means a more spiky centered score-difference spectrum. Higher y-value means worse load balance.

Observed result:
The relationship is positive overall; spiked examples occupy the high-\(r_3\), high-load-error region.

Take-home:
The result supports the proof document's prediction that high-dimensional centered M4 needs a non-spiky spectrum for near-balance.

What this does not prove:
It is correlational simulation evidence, not a theorem for every trained expert matrix.

### Figure: Weighted Top-r Agreement

![Weighted top-r agreement](figures/agreement_vs_rank.png)

What this tests:
Whether low-rank weighted proxies approach the full centered-M4 routing rule.

How to read:
Higher agreement means the rank-r proxy matches full centered M4 more often.

Observed result:
Agreement improves with rank. Separated low-rank reaches exact agreement once rank covers the constructed subspaces. Random spectrum conditions require substantially larger rank.

Take-home:
M3/top-r is plausible as an approximation family, but tiny rank is not enough for broad random spectra.

What this does not prove:
The top-r proxy here is a spectral proxy, not a trained linear router.

### Figure: Spiked Counterexample Histogram

![Spiked counterexample histogram](figures/spiked_counterexample_hist.png)

What this tests:
Whether centered M4 can still be biased under a traceless but spiky spectrum.

How to read:
The histogram shows the centered score difference; the zero line is the routing boundary.

Observed result:
The distribution is visibly asymmetric in sign mass even though the centered score has zero mean.

Take-home:
Zero mean is not enough for 50/50 load in high dimension.

What this does not prove:
It is a constructed counterexample, not evidence that typical trained experts are spiky.

## Claim Boundary

Can claim:

- Raw M4 is not a suitable uniform-load target.
- Centered M4 is a better high-dimensional static target than raw M4.
- Centered M4 needs spectral-spread conditions or calibration for robust load balance.
- Calibrated M4 can enforce load while preserving margin in non-degenerate cases.
- Weighted top-r proxies become more faithful as rank increases.

Cannot claim:

- Centered M4 guarantees exact 50/50 in all high dimensions.
- The random Gaussian proxy is exact dense Gaussian matrix evidence.
- Calibration proves expert specialization by itself.
- A trainable router will learn centered or calibrated M4.
- The result transfers to real text hidden states.

## Next Decision

Proceed to A06_01_07_E04 only as a static text-facing bridge experiment: evaluate empirical-centered / calibrated weighted low-rank M4 on real or semi-real hidden-state distributions, while treating labels as diagnostics rather than semantic specialization proof.
