# R09: Which CrossCoder members compose the domain mean difference?

**Some members reproduce their usage preference across endings, wordings and the original held-out families, but they do not fully explain the representation difference. Under the primary log-rate bins, middle- and high-frequency members supply most of this panel's reconstructed directional contribution. Frequency alone does not assign domain, family, or distance function.**

The objects are the final target token's true Qwen3-0.6B block27 residual-post vector and one native A22 shared activation from its 14-layer joint encoder. We reuse 384 texts, 48 families and the 24/12/12 split, analyzing `example` and `explanation` separately. Discovery fixes candidates; the old held-out data were already exposed in R07/R08. Family bootstrap keeps associated wordings together. This is an exploratory continuation.

[Figure guide](figures.md) · [Detailed evidence](detailed.md) · [A–D reasoning and computation](supplement_ABCD.md) · [Frozen Protocol](protocol.md)

## Purpose and alternatives

R07/R08 distinguished a reproducible center difference, its coverage by a principal subspace, and its share of total variance. R09 asks which fixed dictionary coordinates compose that particular difference, how concentrated their contributions are, and how reference frequency connects to spectral position. The alternatives are concentrated recurring contributions, distributed contributions, wording/ending dependence, and a substantial dictionary residual. The supplement tests whether candidate head alignment merely reflects general dictionary geometry.

## The dictionary leaves a substantial vector residual

Each member's math-minus-biology mean activation is multiplied by its final-layer decoder and training scale. The sum over all 16,384 members is the reconstructed difference; the residual is the true difference minus this sum. Results on 12 original held-out families:

| Fixed ending | Residual length / true difference length [95% family interval] | Cosine | Frozen Top32 relative error |
|---|---:|---:|---:|
| example | 53.68% [52.12–57.96%] | 0.844 | 71.96% |
| explanation | 72.14% [68.40–76.50%] | 0.693 | 82.89% |

Top32 improves over equal-size random subsets but does not reach the full dictionary, which itself remains incomplete. A 53.68% residual-length ratio is not 46.32% explained information. [Lengths and intervals](evidence/tables/dictionary_reconstruction.csv) · [All k and random sets](evidence/tables/cumulative_reconstruction.csv)

## A: Usage preference is the replicated property

Discovery freezes 64 candidates per preferred domain. Sixteen math and twenty biology candidates pass the original usage-replication rule. The 141-member union additionally contains contribution-only Top32 members. Figure A retains 36 replicated preferences, 7 candidates with exploratory interval-supported reversal evidence, and 98 insufficient cases. Forty-eight show a point reversal somewhere; point reversals are not all established condition dependence.

For f13473, held-out math-minus-biology activation differences are 0.005457 [0.002120, 0.008622] and 0.006877 [0.003360, 0.010456] across the two endings. In contrast, f12179 has an explanation discovery mean difference of −0.003026 but a held-out W1 difference of +0.003690 [0.002014, 0.005323]. Only 26 of the original 36 additionally have positive contribution intervals in both endings. That diagnostic does not redefine usage replication. [A, raw values and labels](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD_20261029/figure_A/README.md)

## B–D: Frequency contribution and decoder geometry are distinct

Frequency is the native post-gate `z>0` rate over 65,536 independent DCLM positions. Members with at least 20 hits are split into equal-width log-rate bins: low 0.030518%–0.451726%, middle >0.451726%–6.686506%, high >6.686506%–98.974609%. Counts are 5,808/6,917/632; 3,027 insufficient-reference-support members remain separate. Each bin spans about a 14.8-fold change. Equal-count and linear-rate bins remain sensitivity analyses; no three-bin convention is universally scientific. [Definitions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/summary.md)

B aggregates every member's signed projection onto the true domain difference, preserving positive and negative parts. Net values are:

| Ending | Low | Middle | High | Insufficient support | Residual directional share |
|---|---:|---:|---:|---:|---:|
| example | 0.31% | 44.84% | 27.64% | 0 | 27.21% |
| explanation | 0.17% | 24.51% | 25.77% | −0.002% | 49.56% |

Rows including residual sum to 100%. These are additive directional accounts, not information shares; perpendicular error is outside this scalar. Only 13/11 low-frequency members are active under the two held-out endings. [Signs, support and intervals](evidence/tables/frequency_signed_contributions.csv)

Group names depend on the scheme: the legacy equal-count high group contributes 65.13% for example; the linear-rate low group contributes 58.07%, but its upper boundary is 33.01% and it contains 13,281 members. Members and contributions did not change; the meaning of low/middle/high did. Interpretations must retain rate boundaries.

C normalizes each decoder to unit length and projects it onto 16 fixed 64-PC bands of the R07 independent natural-text basis. It contains no activation, decoder-length, or eigenvalue weight. Each row sums to one. Both f13964 and f13473 reproduce usage preference, yet their PC1–64 fractions are 89.28% and 9.61%. Recurring preference does not require concentrated head alignment.

Across the full dictionary, PC1–64 has mean 8.85%; 63.59% of members exceed its 6.25% dimensional reference, but only 0.38% place more than half of their energy there. Mild bias is common; strong concentration is rare. Candidates average 18.15%, versus 10.44% for frequency-bin-matched non-candidates and 10.69% with discovery activity also required. Candidate median is only 9.47%. The contribution-based selection effect remains. [Background comparison](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD_20261029/background/summary.md)

D first sums each frequency group's contribution vector, then takes its bandwise inner product with the true difference, divided by the complete true squared length. For example, PC1–64 contributions are middle 26.31%, high 15.49%, low 0.24%, residual 5.66%; for explanation they are 10.41%, 9.60%, −0.03%, 9.88%. Middle/high contributions are largest in the first band but extend to later bands. C alone cannot establish this. D row sums equal B nets, and all cells including residual sum to one. [Joint table](evidence/supplement_ABCD_20261029/tables/frequency_spectral_joint_contribution.csv)

## Frequency does not determine family or distance behavior

The equal-member average between-domain activation variance fractions for low/middle/high are 8.94%/12.93%/11.23% with example and 18.55%/10.07%/7.74% with explanation. The latter low-bin mean uses just 11 varying members. There is no ending-invariant ordering; within-domain family and wording variation account for most average member variation. This is compatible with a nonzero contribution to the domain mean difference. [Decomposition and denominators](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/summary.md)

The controlled distance branch uses distances 16/32/64/96/144, target position 239, length 240, and the same filler inventory moved across distances. These inputs differ from the original short texts. Fourteen of 141 candidates pass the far-distance date-edit comparison after correction and retain the original direction in both wordings and endings: 9 middle, 5 high. Requiring the new near condition also to retain direction leaves 10. Within the original 36, the analogous counts are 7 and 3. Only 9 of those 36 retain both-ending preference at the new near condition, so mismatch cannot all be called distance decay. Low-bin coverage is insufficient for a general distance conclusion. [Distance results and real cases](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/summary.md)

**Bounded update:** the real domain center difference is now connected to concrete dictionary coordinates, reference frequencies and spectral bands, alongside condition dependence and omitted difference. Recurring usage and middle/high contributions in this panel are supported descriptions. Semantic exclusivity, causal necessity and expert-routing benefits remain unestablished. Human scientific acceptance and the next decision remain Unknown; the interpretation here is a bounded AI account.

Main decomposition and A–D use caches. Distance completed 3,840 derived inputs plus 2 exact replays, totaling 3,842 attempts, without training. Supplemental outputs are separate and the original Protocol is unchanged. Computation is complete and stopped. Provenance, deviations and audits are in [Detailed](detailed.md) and the [supplement](supplement_ABCD.md).
