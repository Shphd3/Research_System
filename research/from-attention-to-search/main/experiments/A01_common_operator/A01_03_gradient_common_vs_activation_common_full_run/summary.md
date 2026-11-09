# Summary: A01_03 Gradient Common Versus Activation Common Full Run

## Conclusion

The controlled full run supports the gradient-common hypothesis for
optimization interference. In all four activation-gradient mismatch regimes,
gradient intersection beats activation PCA on the primary metric
`gradient_overlap_reduction_advantage`.

Primary result:

```text
n_passed_mismatch_regimes = 4 / 4
pass = true
```

This means activation covariance is not a reliable estimator for
optimization-relevant common when high activation energy is nuisance, unique,
or functional shared structure. Gradient common should be carried into the
next functional/feedback bridge as the primary optimization-common estimator,
with activation PCA retained as a rival explanation.

## Primary Metric

`gradient_overlap_reduction_advantage` is:

\[
\Delta C(P_{\mathrm{grad}})-\Delta C(P_{\mathrm{act}})
\]

where \(\Delta C(P)\) is average pairwise group-gradient cosine before
residualization minus after residualization.

Pass rule: gradient intersection must beat activation PCA in at least three of
four mismatch regimes with seed win rate at least 0.8.

Observed: 4 of 4 mismatch regimes pass, each with seed win rate 1.0.

## Setup

Synthetic hidden states separate gradient common, functional shared common,
group-unique structure, and activation nuisance:

\[
h = s_g A_g z_g + s_f A_f z_f + s_u B_g z_u + s_n A_n z_n + \epsilon
\]

Configuration: hidden dimension 32, common rank 2, six groups, 500 samples per
group, twenty seeds, and five regimes.

Compared estimators:

- activation PCA;
- gradient intersection;
- functional shared;
- random control.

## Main Results

| Regime | Activation PCA reduction | Gradient reduction | Advantage | Seed win rate | Decision |
|---|---:|---:|---:|---:|---|
| aligned_common | 0.8885 | 0.8257 | -0.0628 | 0.05 | sanity check; mechanisms aligned, PCA can win |
| activation_nuisance | -0.0557 | 0.5936 | 0.6494 | 1.0 | gradient wins |
| unique_variance | -0.0578 | 0.6202 | 0.6779 | 1.0 | gradient wins |
| functional_gradient_split | -0.0354 | 0.6494 | 0.6848 | 1.0 | gradient wins |
| entangled_residual | 0.2300 | 0.7003 | 0.4703 | 1.0 | gradient wins |

Random control never wins the aggregate optimization criterion.

## Functional Guard

The `functional_gradient_split` regime separates useful shared common from
optimization common. Functional shared wins `shared_loss_sensitivity` with
8.5791, while gradient intersection wins `gradient_overlap_reduction` with
0.6494 and has near-zero shared-loss sensitivity, 0.0037.

Interpretation: useful shared common and harmful/redundant gradient common can
be different objects. A method should not delete all common directions; it
should first state which mechanism it is targeting.

## Central Figures

![Gradient advantage by regime](figures/gradient_advantage_by_regime.png)

This figure tests the primary metric. Positive bars mean gradient intersection
removes more cross-group gradient overlap than activation PCA. All mismatch
regimes are positive; the aligned sanity-check regime is negative, as expected.

![Gradient overlap reduction by regime](figures/gradient_overlap_reduction_by_regime.png)

This figure shows the raw optimization metric for all estimators. Gradient
intersection is the only estimator that consistently produces large positive
gradient-overlap reduction in mismatch regimes.

![Criterion winners by regime](figures/criterion_winners_by_regime.png)

This figure shows the mechanism split. Gradient intersection wins
optimization-overlap and gradient-common alignment; functional shared wins
shared-loss sensitivity and functional-common alignment.

## Claim Boundary

This run supports: in controlled activation-gradient mismatch settings,
optimization-relevant common is better estimated by cross-group gradient
intersection than activation PCA.

This run does not support: real-DCLM feedback common, preservation rescue,
layerwise estimator choice, residualized MoE improvement, or rare-token utility
improvement.

## Next Decision

Proceed to the functional/feedback bridge. The next anchor should ask whether
the gradient-common estimator explains useful-vs-harmful common boundaries and
whether feedback common can explain step-0 to step-5/10 proxy-route collapse.

