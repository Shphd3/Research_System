派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD.md)；研究修改仍回到原件。

---

# A–D supplement: connecting usage, direction and actual contribution

This supplement reuses the R09 caches and 141 frozen members. It does not change the candidate lists or original Protocol. B reuses the qualified original figure; A/C/D and the full-dictionary background are saved separately. New model forwards, training and PCA fitting are all zero. The [figure guide](figures.md) provides the visual reading path; this document retains reasoning, formulas and audit lineage.

Low/middle/high in B, D and the background use the primary log-rate bins, with boundaries 0.451726% and 6.686506% and the unchanged minimum support of 20 reference hits. Definitions and sensitivity to three binning schemes are in the [Summary](summary.md); group names must retain their boundaries.

## Comparisons that can change the interpretation

The purpose is to connect three observations without preassigning frequency-group functions: a member is used differently across domains; its decoder points toward a spectral range; and its actual usage change contributes to the true domain difference in that range.

| Intuition or hypothesis | Distinguishing comparison | Observation and bounded update | Remaining rival |
|---|---|---|---|
| Candidate response follows domain across endings, wording and families | A compares discovery/old held-out, both endings and both wordings on the fixed list | 36 pass the original usage rule; 7 have exploratory interval-supported reversal; 98 are insufficient | Lexicon, topics and framing covary with domain; pointwise intervals are not formal member confirmation |
| Rare members dominate the domain difference | B aggregates the whole dictionary; family variance separately addresses individual themes | Middle/high groups dominate the current net contribution; low-frequency target coverage is sparse | Target and panel selection; low opportunity does not imply absent function |
| Candidate head alignment is merely general dictionary head bias | C plus all-member, frequency-bin-matched, and active frequency-bin-matched non-candidates | Mild bias is common, strong concentration rare; candidate mean remains higher, median is much lower than mean | Contribution-based selection favors alignment; continuous rates within bins remain unmatched |
| Placing B beside C identifies frequency-by-spectrum contributions | D directly computes the joint signed contribution | Actual activation differences and directions must enter together; the first band has the largest middle/high contributions | A vector decomposition does not establish how the model causally computes |

The final row is a computation-dependency check, not a new empirical discovery from an algebraic identity. Background matching narrows general geometry explanations but does not remove candidate selection effects.

## Distinct denominators

Let \(\delta\) be the true math-minus-biology mean difference, \(\Delta z_f\) the member activation difference, \(d_f\) its final-layer decoder, and \(s\) the training restoration scale. The contribution vector is \(c_f=s\Delta z_f d_f\). All quantities are computed separately by ending and split, including zero activations with equal family/wording weights.

C measures a unit direction:

\[
e_{f,b}=\sum_{j\in b}\langle d_f/\|d_f\|,u_j\rangle^2,
\qquad \sum_b e_{f,b}=1.
\]

Here \(u_j\) is an orthonormal direction of the independent natural-text R07 reference basis and \(b\) is a contiguous 64-PC band. Normalization uses each decoder's own length, without activation, restoration-scale or eigenvalue weights. All 16,384 decoders are nonzero. C is ending-invariant, so there is one geometry set.

D first composes \(v_g=\sum_{f\in g}c_f\) for each frequency group:

\[
J_{g,b}=\frac{\langle P_bv_g,P_b\delta\rangle}{\|\delta\|^2},
\qquad
J_{r,b}=\frac{\langle P_br,P_b\delta\rangle}{\|\delta\|^2}.
\]

\(P_b\) projects onto the band, and \(r=\delta-\sum_gv_g\). Every cell uses the complete true squared length; bands are not individually normalized to 100%. Each frequency row sums to B's net. Each column including residual sums to the true band's squared-projection fraction. All cells including residual sum to one. Negative values remain. C's unit row sum and D's total sum concern different objects.

Original figure 4 computes \(\|P_bv\|^2/\|\delta\|^2\), with \(v\) equal to the true \(\delta\) or reconstructed \(\widehat\delta\). **Both curves use the true difference's squared length as denominator**; reconstructed bars need not sum to one. D replaces the numerator with an inner product against the true difference while retaining that denominator. The two numerators generally differ and are not interchangeable. Squaring a composed vector must preserve cross terms.

## One member across the measurements

The first pages of A and C show the same fixed first 24 members. f516 places 81.49% of unit-decoder energy in PC1–64, yet its held-out explanation activation difference 0.003670 has interval [−0.001261, 0.008618], leaving usage replication insufficient. f424 places only 6.97% there but retains biology preference in both endings, with pooled-wording intervals excluding zero, passing the original rule. Concentrated direction and recurring usage are not equivalent, as this same-page comparison shows.

High-frequency f13964 has independent occurrence rate 98.97%. It occurs in 100% of old held-out texts in both domains and endings. Its preference is an intensity difference: example math/biology means 0.033092/0.044375, explanation 0.094827/0.102423. Both activation differences are negative while the directional contributions are positive because decoder direction also enters the vector contribution.

Its unit decoder places 89.28% in PC1–64; high-frequency f13473 places only 9.61% there and still reproduces math preference. The f13964 explanation contribution interval crosses zero even though its usage-preference interval excludes zero. Occurrence, preference replication, head alignment and reliable contribution cannot be one label. [Real cases](../../../../../../../../UNAVAILABLE.md) · [Member directions](../../../../../../../../UNAVAILABLE.md)

Residual also has two readings: for example, its share along the true difference is 27.21%, whereas its full length is 53.68% of the true difference length. The latter contains parallel and perpendicular error, so B/D cannot replace original figure 1. D shows residual contribution across spectral bands, not only in the tail.

## Completeness and three audit layers

A has 141 fixed members, 6 pages and 1,692 raw estimates with family intervals from 500 resamples. The original 36-member rule is unchanged: the 128 domain candidates split 36/7/85, and all 13 extras are insufficient. C has the same ordered six pages plus the complete figure and a 16,384×16 matrix. B/D cover the complete dictionary in four frequency groups plus residual, separately by ending; all splits are saved. Each of two background pools supplies 1,000 random sets matching 1 low/62 middle/78 high candidates without quota replacement.

Identification audit: usage, geometry and contribution are separated; frequency is not semantics and closure is not discovery. Data/statistics audit: frozen lists/order, family units, prior held-out exposure, pointwise intervals and selection remain explicit; random-set intervals are not family confidence intervals. Implementation audit: cache-only, no coefficient in C, common denominator and signs in D. Passing these audits qualifies measurement/reporting, not scientific closure.

[Joint closure](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/evidence/supplement_ABCD_20261029/analysis/joint_audit.json) · [Independent C/D audit](../../../../../../../../UNAVAILABLE.md) · [Independent background audit](../../../../../../../../UNAVAILABLE.md) · [A audit](../../../../../../../../UNAVAILABLE.md). Configurations: [A](../../../../../../../../UNAVAILABLE.md), [background](../../../../../../../../UNAVAILABLE.md), [D](../../../../../../../../UNAVAILABLE.md); code: [D computation](../../../../../../../../UNAVAILABLE.md), [C/D rendering](../../../../../../../../UNAVAILABLE.md). Original Protocol and pre-execution snapshots retain their identities.
