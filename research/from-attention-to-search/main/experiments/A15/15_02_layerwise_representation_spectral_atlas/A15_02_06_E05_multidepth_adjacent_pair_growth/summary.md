---
experiment_id: A15_02_06_E05_multidepth_adjacent_pair_growth
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
---

# Adjacent-layer normalized spectral redistribution differs significantly across selected depths

## Result snapshot

Four frozen adjacent pairs—2→3, 8→9, 17→18, and 34→35—were compared in identical Mean Response directions using the same 512 records. The registered F9--F12 normalized-share change was:

| Pair | \(D=Q_{target}-Q_{source}\) | Simultaneous 95% interval | A / B signs | Raw F9--F12 growth |
| --- | ---: | ---: | ---: | ---: |
| 2→3 | +0.021452 | [+0.017046, +0.025859] | + / + | \(+1.6188\) log2 = 3.07× |
| 8→9 | -0.018314 | [-0.022720, -0.013907] | - / - | \(+0.7900\) log2 = 1.73× |
| 17→18 | +0.004798 | [+0.000392, +0.009204] | + / − | \(+0.2548\) log2 = 1.19× |
| 34→35 | -0.027280 | [-0.031686, -0.022874] | - / - | \(+0.6314\) log2 = 1.55× |

All six deeper-pair minus shallower-pair contrasts exclude zero after one simultaneous correction. The registered outcome is therefore `significant_depth_heterogeneity`: the four selected transitions are not interchangeable.

The pattern is **not monotonic**. It alternates positive, negative, weakly positive, and negative. The selected-depth linear slope is negative (`-0.001123` per block, 95% interval `[-0.001206,-0.001007]`), but the 17→18 rebound violates a monotone-decrease interpretation. Its A/B signs also disagree, so this weak positive transition is expression-sensitive.

All four raw F9--F12 variances increase. Hence the sign changes concern how each target layer reallocates its own normalized variance share, not whether raw variance exists or grows.

## Required figures

Figure 1 separates the four same-direction source/target curves. Difference panels use a signed symmetric-log scale so narrow terminal spikes do not erase the middle-rank sign pattern.

![Four separate adjacent-layer transitions](figures/figure1_four_pair_same_direction_curves.png)

Figure 2 is the inferential figure: fixed-band redistribution, four-pair registered-region estimates, raw growth, and all six corrected depth contrasts.

![Cross-depth significance](figures/figure2_cross_depth_significance.png)

## Claim boundary

The experiment establishes significant heterogeneity among these four selected adjacent transitions in the frozen Mean Response coordinate. It does not establish an all-layer or monotone depth law, identify information absent from the source layer, prove low rank, or support Router utility. The 17→18 full-data positive result must remain qualified by its A/B sign mismatch.

## One next decision

Human confirmation required: decide whether the observed non-monotonicity warrants a registered scan of every eligible adjacent pair before any depth-law or routing interpretation. The current four-pair result should not be repaired by selecting a new basis.

Evidence: [Protocol](protocol.md), [Detailed record](detailed.md), [pair summary](tables/pair_summary.csv), [six corrected contrasts](tables/pairwise_depth_contrasts.csv), and [bandwise transitions](tables/bandwise_transition.csv).
