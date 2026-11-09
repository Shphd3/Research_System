---
experiment_id: A15_02_06_E05_multidepth_adjacent_pair_growth
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
---

# Detailed evidence record

## 0. Quick recap

- Question: do adjacent-layer normalized spectral changes differ significantly at four selected depths?
- Object: post-`o_proj`, pre-residual Attention writes projected into one frozen Mean Response basis.
- Direct result: all six registered cross-pair contrasts exclude zero after familywise correction.
- Eligibility: all source, implementation, projection, bootstrap, E04 identity, and visual guards pass.
- Typed verdict: `significant_depth_heterogeneity`.
- Boundary: selected-pair variance redistribution, not information novelty or a universal depth law.

## 1. Definitions

| Term | Plain meaning | Computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| Attention write | output written by one Attention branch before residual addition | \(A_\ell(x)\) at the final colon | measured layer object | information absent from the incoming residual |
| common direction | identical parameter-only vector used by every block | column \(v_j\) of frozen Mean Response \(V\) | makes directionwise comparison meaningful | universal semantic identity |
| normalized share | fraction of one block's total write variance | \(p_{\ell j}=e_{\ell j}/\sum_ke_{\ell k}\) | relative redistribution | absolute variance growth |
| \(D_q\) | target minus source share in F9--F12 | \(\sum_{b=9}^{12}\Delta Q_{qb}\) | per-pair primary endpoint | new knowledge |
| \(G_q\) | raw growth in the same region | \(\log_2(E_t/E_s)\) | scale guard | semantic or causal value |
| cross-depth contrast | difference between two transition endpoints | \(H_{ab}=D_b-D_a\) | significance of depth heterogeneity | smooth layerwise law |

Projection coefficients are not normalized record by record. Records are projected, centered across examples, converted into population variance, and only then normalized within block.

## 2. Actual setup

- Model: frozen Qwen3-8B, residual width 4096.
- Data: 512 balanced taxonomy records, 8 parent domains, 8 children per parent, 4 templates, 2 bundles.
- Readout: shared final `Classification:` colon at absolute position 57.
- Pairs: 2→3, 8→9, 17→18, 34→35.
- Coordinate: unchanged parameter-only Mean Response basis from all 36 trace-normalized MLP gate/up input Grams.
- Bands: F1--F16, 256 directions each; frozen semantic region F9--F12.
- Uncertainty: 2,000 paired parent bootstraps, seed `8120605`.
- Multiplicity: separate centered maximum-deviation families over four \(D_q\), four \(G_q\), 64 \((q,b)\) band changes, and six cross-depth contrasts.
- Expression halves: A/B sign guards.
- No new model inference or data selection was performed.

## 3. Protocol conformance

| Registered item | Actual | Status | Eligibility impact |
| --- | --- | --- | --- |
| four frozen pairs | 2→3, 8→9, 17→18, 34→35 | PASS | eligible |
| eight cache identities | all match extraction manifest hashes | PASS | eligible |
| common basis identity | SHA-256 frozen E02 Mean Response basis | PASS | eligible |
| projection trace conservation | maximum relative error \(1.2003\times10^{-7}\) | PASS | eligible |
| unit tests | 4/4 pass | PASS | eligible |
| paired bootstrap | 2,000/2,000 draws retained | PASS | eligible |
| E04 8→9 reproduction | \(D\) and \(G\) absolute error 0 | PASS | eligible |
| exactly two visual-audited figures | complete | PASS | eligible |
| deviations, retries, post-hoc exclusions | none | PASS | eligible |

## 4. Per-pair results

### 4.1 Pair 2→3

The frozen-region normalized share increases by `+0.021452`, simultaneous interval `[+0.017046,+0.025859]`; both A/B halves are positive. Raw region variance grows `3.07×`, while total write variance grows `2.75×`, explaining the positive normalized change. Under the more conservative 64-band family, F14--F15 are positive and F1 is negative.

### 4.2 Pair 8→9

The normalized share decreases by `-0.018314`, simultaneous interval `[-0.022720,-0.013907]`; both halves are negative. Raw region variance still grows `1.73×`, but total variance grows faster at `1.88×`. Under the 64-band family, F1--F4 are positive and F16 is negative. This exactly reproduces E04's registered \(D\) and \(G\).

### 4.3 Pair 17→18

The full-data normalized share increases by `+0.004798`, simultaneous interval `[+0.000392,+0.009204]`. Raw region variance grows `1.19×`, slightly faster than total variance at `1.16×`. However A is positive (`+0.005126`) and B is negative (`-0.002392`). Therefore this is a statistically positive full-data endpoint with an explicit expression-split stability warning, not a robust positive transition. F1--F4 and F7 are positive and F16 negative under the 64-band family.

### 4.4 Pair 34→35

The normalized share decreases by `-0.027280`, simultaneous interval `[-0.031686,-0.022874]`; both halves are negative. Raw region variance grows `1.55×`, while total variance grows `1.73×`. F1 and F16 are positive under the 64-band family; no individual band is simultaneously negative even though the aggregate F9--F12 endpoint is negative.

## 5. Are the depths significantly different?

| Deeper pair − shallower pair | Difference in \(D\) | Six-contrast simultaneous 95% interval | Result |
| --- | ---: | ---: | --- |
| 8→9 − 2→3 | -0.039766 | [-0.045987, -0.033546] | different |
| 17→18 − 2→3 | -0.016654 | [-0.022875, -0.010434] | different |
| 34→35 − 2→3 | -0.048733 | [-0.054953, -0.042512] | different |
| 17→18 − 8→9 | +0.023112 | [+0.016891, +0.029332] | different |
| 34→35 − 8→9 | -0.008966 | [-0.015187, -0.002746] | different |
| 34→35 − 17→18 | -0.032078 | [-0.038299, -0.025858] | different |

Every registered contrast excludes zero after the joint correction. This is strong evidence that the four selected transitions have distinct normalized redistribution profiles.

The fitted selected-depth slope is `-0.001123` per block with interval `[-0.001206,-0.001007]`. This is an overall downward association, not a monotonic law: the sequence `+0.02145, -0.01831, +0.00480, -0.02728` contains a clear 17→18 rebound, and that rebound is itself split-unstable.

## 6. Relative versus absolute readings

All four \(G_q\) simultaneous intervals lie above zero, so raw F9--F12 variance grows in every pair. Two \(D_q\) values are positive and two negative. The apparent contradiction is only a normalization effect:

\[
D_q>0 \Longleftrightarrow \text{F9--F12 grows faster than total write variance},
\]

while \(D_q<0\) means it grows more slowly than the total. Neither case identifies information unavailable in the source block.

## 7. Figure audit

### Figure 1: four separate transitions

![Four separate adjacent-layer transitions](figures/figure1_four_pair_same_direction_curves.png)

Purpose: show each pair's source and target curves and signed directionwise change without mixing direction identities. The left panels are log normalized densities. The right panels use signed symmetric-log axes to retain both small middle-rank changes and narrow terminal spikes. The curves are 129-direction moving averages for display only. Allowed reading: qualitative within-pair location. Limitation: no visual cross-pair significance claim.

### Figure 2: cross-depth inference

![Cross-depth significance](figures/figure2_cross_depth_significance.png)

Panel A shows all fixed-band point changes. Panel B shows the four registered \(D_q\) values and the A/B warning at 17→18. Panel C separates raw growth. Panel D contains the verdict-bearing six corrected contrasts. Allowed reading: selected transitions differ significantly and non-monotonically. Limitation: only four preselected adjacent pairs were tested.

## 8. Failure decomposition and claim boundary

- Implementation or coordinate failure: ruled out by identity, orthogonality, conservation, and E04 reproduction guards.
- Uniform adjacent-layer later-shift prior: not supported; signs alternate across selected pairs.
- Smooth monotone depth model: not supported by the observed rebound, despite a negative four-point slope.
- Relative-versus-absolute confusion: ruled out by positive raw growth in every pair and explicit total-growth comparison.
- Remaining rivals: local layer function, expression sensitivity, narrow terminal-band effects, and Attention-write variance being an incomplete proxy for residual-relative novelty.

Can claim: significant heterogeneity among these four selected adjacent-layer normalized variance redistributions in the frozen coordinate.

Cannot claim: every adjacent layer differs, a universal oscillation or monotone law, semantic novelty, causal function, low rank, or Router utility.

## 9. One next decision

Human decision required: whether to run a registered all-eligible-adjacent-pair scan to determine if this non-monotonic selected-pair pattern is systematic before any depth-law or routing interpretation. Completion would require one multiplicity-controlled layerwise map with the same coordinate and estimator; resume from the E05 worker without changing the basis.

## 10. Artifact map

| Artifact | Location |
| --- | --- |
| Frozen protocol | [protocol.md](protocol.md) |
| Conclusion-first result | [summary.md](summary.md) |
| Four pair endpoints | [tables/pair_summary.csv](tables/pair_summary.csv) |
| Six corrected contrasts | [tables/pairwise_depth_contrasts.csv](tables/pairwise_depth_contrasts.csv) |
| 64 fixed-band changes | [tables/bandwise_transition.csv](tables/bandwise_transition.csv) |
| Projection audit | [tables/projection_diagnostics.csv](tables/projection_diagnostics.csv) |
| Provenance and visual audit | [provenance](provenance) |
| Full arrays and logs | `/data/250010109/MoE_Router/experiments/20260812_a15_02_06_multidepth_adjacent_pair_growth/runs/a15-02-06-e05-20260812-multidepth-pairs/` |
