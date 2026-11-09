# A15_27_02: domain-internal and mixed principal subspaces

## 1. Problem Definition
Following R07, compare domain-internal and mixed leading variation spaces at the identical final target tokens. R07 established a bounded paired mean association and head/tail readability; it did not compare within-domain covariance spaces. One question: are math/bio leading variation spaces similar, and is mixed leading variance within-domain or between their centers? Last block27 is primary; blocks1,13 are controls. This is an exposed-data exploratory continuation, not a fresh confirmation.

## 2. Physical Priors
The same-layer residual coordinates permit geometric comparisons. Family variants are dependent. Large variance, class-center differences and readable labels are different objects. No prior identifies shared directions as grammar or different directions as specific knowledge.

## 3. Falsifiable Hypotheses
Four user-defined competitors: similar internal spaces with center difference outside; similar spaces with difference inside; different internal spaces; insufficiently stable estimates. Ending shifts and finite family support are rivals. Different spaces require cross-domain overlap meaningfully below same-domain stability under equal sample counts, not just one low overlap.

## 4. Mathematical Model
For each domain d, covariance C_d=sum (h-mu_d)(h-mu_d)^T/n_d, retaining raw scale. Equal domain mixture C_mix=(C_math+C_bio)/2+delta delta^T/4, delta=mu_math-mu_bio. Orthonormal k-column bases overlap ||U^T V||_F^2/k. Unit delta coverage is ||U^T delta||^2/||delta||^2. Mixed subspace variance decomposes by trace into within and between terms with the same denominator. These are identities/geometric descriptions, not functional mechanisms.

## 5. Computational Realization
Reuse all384 R07 final-token samples and24/12/12 family splits; obtain only missing raw blocks1,13 and native A22 joint z with one forward per existing text. Fit three PCAs per layer on discovery only at k4,8,16,32; retain actual numerical ranks. Repeat family-disjoint half splits with equal cross/within counts and random orthogonal references. Refit by family bootstrap for pointwise uncertainty. Repeat key metrics separately by ending. UMAP is auxiliary, discovery-fit then transform, fixed three seeds; raw1024 inputs and one native16384-dimensional shared z view.

## 6. Minimal Falsification Tests
Check full covariance identity, orthonormality, nonzero rank, old last-layer replay, frozen model/dictionary, and family-only fitting. Low same-domain stability or unsupported ranks retain competitor4. Compare full and equal-half results without a data-selected overlap cutoff. Ending-conditioned reversal limits a pooled interpretation. Similar spectra or 2D clusters cannot replace subspace overlap and variance decomposition.

## 7. Current Evidence
R08 completed384fixed-text forwards; all last-layer vectors exactly match R07 and LM/A22 hashes remain unchanged. At block27/k16, equal-half cross-domain overlap0.2955 versus same-domain0.3946/0.4357 shows a relative difference but finite stability. Mixed16contains99.89% of discovery center-direction squared norm and93.33% of the old-heldout direction, yet between-center variance is9.08%; within-domain90.92%. Fixed-ending between shares36.28%/19.93% show material ending dependence. Intermediate/late registered k comparisons retain lower cross overlap, but no precise independent semantic spaces are established. Single-endingk32half comparison is rank-ineligible; nonlinear bootstrap percentile bias retained. [R08 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R08_within_mixed_subspaces_20261029/summary.md). User scientific acceptance Unknown.

## 8. Claim Boundary And Next Decision
Answer only which geometric competitor is consistent with this fixed panel. No pure semantics, causal function, expert allocation, formation layer or natural cluster claims. Complete all requested views or name exact missing dependencies, then stop for the researcher to review whether domain-internal versus center-difference geometry resolves the question. No automatic next experiment.
