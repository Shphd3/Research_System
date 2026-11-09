# E03 Post-Hoc Reliability Audit: Fisher, Random Gradient Null, And LM Loss

Parent result: [summary.md](summary.md)  
Chinese companion: [fisher_gradient_reliability_cn.md](fisher_gradient_reliability_cn.md)  
Status: POST_HOC_RELIABILITY_AUDIT; qualified caches, scalar gradient contractions, and immutable training ledgers only; zero optimizer updates; no change to the frozen Protocol.

## 1. Purpose

Test whether the Fisher calculation reflects non-random class geometry, whether the observed near-90-degree gradient angles are more orthogonal than dimension-matched random directions, and whether the existing loss and local-gradient measurements can identify a reconstruction coefficient.

## 2. Hypothesis

Meaningful Fisher structure should exceed a balanced label-permutation null and support above-chance held-out linear readout. A special orthogonality mechanism should place observed cosines closer to zero than independent random directions in the same dimension. A coefficient claim requires aggregate parameter-space gradients and a matched coefficient intervention; local activation contractions and scalar loss ratios alone are insufficient.

## 3. Analysis Method

For class means \(\mu_c\) and their class-balanced center \(\bar{\mu}\), the fixed definition is

\[
B=C^{-1}\sum_c\lVert\mu_c-\bar{\mu}\rVert_2^2,\qquad
W=C^{-1}\sum_c\mathbb{E}_{x\mid c}\lVert x-\mu_c\rVert_2^2,\qquad
F=B/W.
\]

The audit uses 256 class-stratified paired report-row bootstrap draws for \(B/W/F\), 256 balanced report-label permutations at 3B in raw coordinates, and fit/tune/report-separated linear probes. Raw and fit-only B3 coordinates remain separate.

The common gradient support has \(d=8\times32\times1024=262{,}144\) coordinates per batch. Under independent isotropic random directions,

\[
C^2\sim\operatorname{Beta}\left(\frac12,\frac{d-1}{2}\right),\qquad
\operatorname{SD}(C)=d^{-1/2}.
\]

Observed cosines are standardized by \(\sqrt d\); four disjoint batches are summarized per model-checkpoint-layer and the 44 group tests are Benjamini–Hochberg adjusted separately for unusually small and unusually large absolute cosine. This is an isotropic reference only because raw gradient vectors were not retained for coordinate-preserving permutation, sign-flip, effective-dimension, or cross-batch nulls.

Training LM loss is reconstructed from immutable ledgers as 100M-valid-token bin means. Coefficient interpretation remains bounded because the measured gradients are local activation gradients rather than summed gradients in shared parameter space.

## 4. Conclusion

**Fisher is correctly computed and reflects non-random label geometry, but its change is not a sufficient representation-quality verdict. The observed near-90-degree angles are generally ordinary for the measured dimension, not evidence of a special orthogonality mechanism. Existing data do not identify an optimal reconstruction coefficient.**

At 3B, all 44 raw-coordinate surfaces exceed their balanced shuffled-label 95th percentile by 4.49–23.46 times, with one-sided \(p=1/257\), and every held-out probe is above chance. Fisher therefore has a meaningful bounded interpretation as class geometry. However, all 22 raw-coordinate Attention-to-reconstruction panels reduce both \(B\) and \(W\): \(B\) ratios are 0.532–0.911 and \(W\) ratios are 0.440–0.826. Among 44 raw/B3 probe pairs, reconstruction is lower in 42, tied in one, and higher in one. A higher Fisher can therefore arise because within-class energy contracts faster while held-out readout still degrades.

![Fisher sources at 3B](figures/fisher_bw_ratio_3b.png)

For gradient direction, the dimension-matched random null has cosine SD 0.001953 and a 95% angle interval of 89.781–90.219 degrees. After group-level adjustment, 43/44 checkpoint-layer groups are compatible with this null, none is closer to exact orthogonality, and only SALL 1B L0 has larger absolute departure from zero (\(q=9.67\times10^{-6}\)); all 11 groups at 3B are random-compatible.

![Dimension-calibrated gradient cosine](figures/gradient_cosine_vs_dimension_matched_random.png)

In the shared 3.0–4.4B window, mean LM-loss differences from Dense are M2 +0.00065, S7 +0.01254, S37 +0.00333, and SALL −0.00378 nats/token. These single-trajectory descriptive differences cannot isolate gradient norm, angle, topology, or coefficient. Scalar regularization is 5.55%–6.33% of LM loss at 3B while local gradient ratios span nearly two orders of magnitude, so scalar loss balancing is invalid.

The bounded engineering candidate for the next Smoke remains a common \(\lambda_{\rm rec}=0.1\), which linearly scales the largest observed local ratio from 1.564 to about 0.156 at the frozen state. It is not an optimum. The next protocol must measure summed shared-parameter gradients, retain enough gradient structure for non-isotropic nulls, and run a matched short coefficient intervention before selecting a full-run value.

### Claim Boundary

Can claim: correct Fisher reconstruction; non-random and held-out-readable class geometry; simultaneous 3B contraction of between- and within-class energy under reconstruction; dimension-matched random compatibility of most observed gradient angles; scalar loss ratios do not determine gradient ratios.

Cannot claim: Fisher improvement equals representation improvement or native use; special learned orthogonality; local activation contractions equal parameter updates; the observed LM-loss differences are caused by gradient norm; or 0.1 is optimal.
