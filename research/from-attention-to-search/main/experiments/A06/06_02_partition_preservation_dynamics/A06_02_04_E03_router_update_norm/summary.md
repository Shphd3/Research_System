# A06_02_04_E03 Result Summary: Router Update Norm And Margin Budget

## Conclusion

A direction-fixed router norm transition exists, but the pre-registered router-only budget is not a calibrated controller.

1. **Update scale causally controls early crossing.** At full raw-gradient norm, early-cross rates are 41.67% and 45.83% in the two biased regimes. Halving the norm reduces them to 3.13% and 4.17%; quarter and eighth norms produce zero crossings. The registered critical interval is \(\alpha=1\rightarrow0.5\).
2. **Router-only pressure strongly ranks risk but misses most events at the fixed threshold.** On held-out seeds, \(\rho^{router}\) has ranking AUC 0.978, but the fixed threshold \(\rho\ge1\) has only 20% recall and 0.599 balanced accuracy. It is precise (90%) and has 0.3% false-positive rate, but is too conservative.
3. **Early representation motion contributes directly to crossing, while re-entry is driven by router correction in this raw-gradient surface.** At crossing, normalized consumption is 0.748 from router motion, 0.290 from representation-center motion, and 0.007 from interaction. By re-entry, router consumption falls to 0.591, while direct representation consumption remains harmful at 0.302.

The result refines A06_02_04_E01: representation training is causally helpful for recovery in the freeze intervention, but its direct geometric margin term is not the observed corrective term here. Its beneficial effect is likely indirect through future hidden states and router gradients. That mechanism is the next decision before constructing a margin controller.

## Terminology / Definitions

| Term | Plain meaning | Computation | Why it decides | Cannot prove |
| --- | --- | --- | --- | --- |
| Norm multiplier | Applied raw-gradient router-update norm relative to the same-state full AdamW candidate | \(\alpha\in\{1,0.5,0.25,0.125\}\) | Causal scale intervention | Real-LLM optimal scale |
| Router-only pressure ratio | Maximum cumulative negative router row term relative to initial pairwise margin | \(\rho_f^{router}(50)\) | Candidate label-free risk statistic | Exact crossing with moving representation |
| Balanced accuracy | Mean recall for crossing and non-crossing cells | \((TPR+TNR)/2\) | Protects against low event prevalence | Probability calibration |
| Ranking AUC | Probability a crossed cell receives a higher risk score than a non-crossed cell | pairwise score ranking | Separates ranking from threshold calibration | A usable threshold |
| Direct representation consumption | Normalized margin loss from feature-center motion | \(-\sum v^\top\Delta\mu/m(0)\) | Identifies the algebraic center-motion term | Total causal effect of representation learning |

The primary event population is features 1--3 across 32 seeds, two critical regimes, and four norm multipliers.

## Exact Setup

- Data/model/initialization: identical to A06_02_04_E02; full-sequence LM loss, no positional embedding, one causal attention layer, fixed function-matched experts, initial margin p05 0.5.
- Representation: standard AdamW in all conditions.
- Router: current raw-gradient direction with norm \(\alpha\|\Delta W^{full}\|_F\).
- Multipliers: 1, 0.5, 0.25, 0.125.
- Run: 32 seeds, 1,000 updates, four GPUs, two biased regimes and two guards.
- Budget audit: every feature-competitor pair for steps 1--50.

## Primary Evidence

### Scale Transition

| Multiplier \(\alpha\) | 8/32 signal crossing | 4/32 signal crossing | Final margin p05 | Final route NMI |
| ---: | ---: | ---: | ---: | ---: |
| 1.0 | 41.67% | 45.83% | 0.298--0.327 | 1.0 |
| 0.5 | 3.13% | 4.17% | 0.411--0.421 | 1.0 |
| 0.25 | 0% | 0% | 0.414--0.421 | 1.0 |
| 0.125 | 0% | 0% | 0.406--0.414 | 1.0 |

![Router norm scale transition](figures/scale_transition.png)

**Question:** Does crossing change monotonically when only the applied router norm changes?

**How to read:** The dashed line is the 25% event-bearing threshold; the dotted line is the 10% safe threshold.

**Observed result:** Both background ratios show the same sharp transition between full and half norm.

**Take-home:** Actual router-update scale is causal on this surface.

**Limitation:** The tested grid identifies an interval, not a continuous critical value.

### Held-Out Router-Only Budget

On seeds 16--31, the fixed threshold yields:

| Metric | Value |
| --- | ---: |
| Balanced accuracy | 0.599 |
| True-positive rate | 0.200 |
| True-negative rate | 0.997 |
| Precision | 0.900 |
| False-positive rate | 0.003 |
| Ranking AUC | 0.978 |

![Held-out budget prediction](figures/budget_prediction.png)

**Question:** Can router-only pressure relative to initial margin predict crossing without representation terms?

**How to read:** The dashed line is the fixed, untuned threshold 1.

**Observed result:** Crossed cells have much larger scores, but most remain below 1. The statistic ranks risk extremely well and is poorly calibrated.

**Take-home:** A router-only controller cannot use the physical threshold 1 unchanged; representation and interaction consume missing budget.

**Limitation:** AUC does not justify post-hoc threshold tuning or real-model transfer.

### Exact Crossing And Re-entry Budget

For 84 full-norm crossed cells:

| Time | Router consumption | Representation consumption | Interaction | Total |
| --- | ---: | ---: | ---: | ---: |
| First crossing | 0.748 | 0.290 | 0.007 | 1.045 |
| Re-entry | 0.591 | 0.302 | 0.007 | 0.900 |

Consumption is normalized by the initial pairwise margin; total above 1 means the initial budget is exhausted.

**Interpretation:** Direct representation movement supplies about 28% of the crossing budget. Re-entry occurs because the cumulative router term becomes less harmful by about 0.156; the direct representation term does not reverse sign. Thus representation learning's causal recovery benefit from A06_02_04_E01 is not equivalent to direct center-motion correction.

## Learning Guard

The largest safe multiplier is 0.5. Its final route NMI and positive-margin rate are both 1.0. The registered relative final-loss guard formally fails: mean terminal loss is \(4.50\times10^{-6}\) versus \(4.19\times10^{-6}\) at full norm, a 7.42% relative increase.

This is a formal failure under the protocol, but not evidence of meaningful under-training: both losses are near zero, final accuracies are 1.0, and losses at steps 10, 20, and 50 are comparable, with the half-norm condition sometimes lower. Future guards should use time-to-target loss or excess loss above a numerical floor rather than relative terminal loss near zero.

## Validity And Guards

- Completed: 32/32 seeds, 2,048 event rows, 28,672 trajectory rows, and 307,200 pairwise budget rows.
- Maximum norm-scale error: \(2.15\times10^{-7}\).
- Maximum exact budget closure error: \(6.70\times10^{-7}\).
- Manual AdamW parity error: \(9.54\times10^{-7}\).
- Maximum guard early-cross rate: 4.17%, below the registered 25% threshold.

## Hypothesis Update

| Hypothesis | Verdict | Evidence |
| --- | --- | --- |
| H1: scale monotonicity | **Supported** | both regimes move from about 43.75% at \(\alpha=1\) to below 5% at \(0.5\), then 0% |
| H2: adjacent critical interval | **Supported** | registered interval \(1.0\rightarrow0.5\) in both regimes |
| H3: router-only threshold predicts held-out crossing | **Rejected** | balanced accuracy 0.599 and recall 0.200, despite AUC 0.978 |
| H4: safe scale passes relative final-loss guard | **Formally rejected** | +7.42% relative terminal loss; metric is ill-conditioned near zero |

The overall anchor does not authorize an adaptive router method because H3 and H4 fail as registered.

## Claim Boundary

The experiment establishes a sharp direction-fixed scale transition and a high-quality risk ranking on the fixed-utility synthetic bridge. It does not establish a calibrated router-only budget, a meaningful learning-efficiency penalty, a real-LLM margin controller, learned-expert utility, MTP benefit, or downstream conditional-compute value.

## Next Decision

Use event-triggered branching from the same crossed state to determine how representation learning enables recovery:

- joint continuation;
- freeze representation after crossing;
- freeze router after crossing;
- compare direct center-motion terms with representation-induced changes in future router gradients.

If representation learning is necessary after crossing while its direct term remains margin-consuming, the recovery mechanism is indirect gradient shaping. That mechanism determines how much budget a future native-margin controller must reserve.

