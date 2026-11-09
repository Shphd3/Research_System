---
experiment_id: A15_02_06_E05_all_adjacent_depth_transitions
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
eligibility: ELIGIBLE_REGISTERED_RESULT_WITH_POSTHOC_BOUNDARY_AUDIT
---

# Detailed: all adjacent-layer transitions in the frozen Mean Response basis

## 0. Quick recap

- Purpose: test whether the negative block-8→9 normalized transition generalizes across depth.
- Direct result: 16/35 transitions are simultaneously positive, 11/35 simultaneously negative, and 8/35 unresolved for F9--F12 normalized share.
- Registered depth verdict: `stage_dependent_nonmonotonic`.
- Central boundary: the registered stage contrast is significant but sensitive to a large sign reversal at the middle/deep cut; the full linear depth slope is unresolved.
- Cannot claim: added knowledge, conditional novelty, low rank, causal function, or Router utility.

## 1. Terms and estimators

| Term | Plain meaning | Computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| Attention write | current block's Attention branch output | post-`o_proj`, pre-residual \(A_\ell(x)\) | measured activation | information absent from incoming state |
| Mean Response direction | one common parameter-only axis | column \(v_j\) of frozen \(V\) | same identity across blocks | universal semantic axis |
| \(D_{sem,\ell}\) | change in normalized F9--F12 share | \(Q_{\ell+1}(B_{sem})-Q_\ell(B_{sem})\) | primary transition proxy | absolute growth or novelty |
| \(G_{sem,\ell}\) | raw F9--F12 variance ratio | \(\log_2(E_{\ell+1}/E_\ell)\) | scale guard | relative redistribution |
| simultaneous interval | one family-wise band over all transitions | centered bootstrap maximum deviation | pair significance | architecture-population uncertainty |

Projection and normalization follow

\[
z_{\ell xj}=A_\ell(x)^\top v_j,
\quad
e_{\ell j}=\operatorname{Var}_x(z_{\ell xj}),
\quad
p_{\ell j}=e_{\ell j}/\sum_ke_{\ell k}.
\]

No recordwise unit normalization is applied.

## 2. Protocol conformance

| Registered item | Actual | Status | Eligibility impact |
| --- | --- | --- | --- |
| all 36 layers and 35 adjacent pairs | completed | PASS | eligible |
| frozen 512 records and readout | hash-identical | PASS | eligible |
| frozen Mean Response basis | hash-identical; orthogonality error \(2.658\times10^{-6}\) | PASS | eligible |
| projection energy conservation | maximum relative error \(2.291\times10^{-7}\) | PASS | eligible |
| 2,000 parent bootstraps, seed 8120605 | completed, no draw dropped | PASS | eligible |
| A/B expression halves | all transition and stage points recomputed | PASS | eligible |
| E04 block-8→9 identity | exact full/A/B match | PASS | eligible |
| three required figures | rendered and visually audited | PASS | eligible |
| protocol deviations | none | PASS | eligible |
| ±1 stage-boundary audit | post-hoc, labeled and non-verdict-bearing | BOUNDED | limits stage-law interpretation only |

## 3. Per-transition results

The 35-transition simultaneous radius is `0.008340` for \(D_{sem}\). The jointly protected sign classification is:

- positive: `1→2`, `2→3`, `4→5`, `6→7`, `7→8`, `10→11`, `12→13`, `13→14`, `19→20`, `20→21`, `25→26`, `26→27`, `29→30`, `31→32`, `33→34`, `35→36`;
- negative: `3→4`, `5→6`, `8→9`, `9→10`, `11→12`, `16→17`, `22→23`, `24→25`, `27→28`, `30→31`, `34→35`;
- unresolved: the remaining eight.

Having protected positive and negative transitions establishes local heterogeneity in this fixed model. It does not establish a smooth depth effect.

### Eight display pairs

| Pair | \(D_{sem}\) and simultaneous interval | \(G_{sem}\) and simultaneous interval | Reading |
| --- | --- | --- | --- |
| 1→2 | +0.00922 [+0.00088,+0.01756] | +1.703 [+1.229,+2.176] | relative and absolute positive |
| 5→6 | -0.01819 [-0.02653,-0.00985] | +0.182 [-0.291,+0.656] | relative negative; raw unresolved |
| 8→9 | -0.01831 [-0.02665,-0.00997] | +0.790 [+0.316,+1.264] | relative down despite raw growth |
| 13→14 | +0.01544 [+0.00710,+0.02378] | -0.677 [-1.151,-0.203] | relative up despite raw decline |
| 18→19 | -0.00421 [-0.01255,+0.00413] | +0.392 [-0.081,+0.866] | both unresolved |
| 24→25 | -0.05557 [-0.06391,-0.04723] | +1.445 [+0.971,+1.918] | large relative fall with raw growth |
| 30→31 | -0.01780 [-0.02614,-0.00946] | +1.010 [+0.536,+1.484] | relative down despite raw growth |
| 35→36 | +0.01157 [+0.00323,+0.01991] | -0.160 [-0.634,+0.314] | relative positive; raw unresolved |

## 4. Registered depth comparison

| Stage | Mean \(D_{sem}\) | 95% interval | Mean \(G_{sem}\) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| early, starts 1--12 | +0.002168 | [+0.001678,+0.002425] | +0.6831 | [+0.6765,+0.6890] |
| middle, starts 13--24 | -0.003779 | [-0.004046,-0.003294] | +0.4371 | [+0.4213,+0.4452] |
| deep, starts 25--35 | +0.007947 | [+0.007512,+0.008050] | +0.2545 | [+0.2455,+0.2621] |

All registered \(D_{sem}\) stage contrasts exclude zero under the simultaneous interval:

- middle minus early: `−0.005947` [`−0.006707`,`−0.005187`];
- deep minus early: `+0.005779` [`+0.005019`,`+0.006539`];
- deep minus middle: `+0.011726` [`+0.010966`,`+0.012486`].

All \(G_{sem}\) stage contrasts are significantly negative: middle−early `−0.2460`, deep−early `−0.4286`, and deep−middle `−0.1826`, with simultaneous intervals fully below zero. Thus average raw multiplicative growth per transition becomes smaller with depth even while normalized stage drift is U-shaped.

The OLS slope of \(D_{sem,\ell}\) against transition start block is

\[
-2.27\times10^{-5},
\qquad95\%\ \mathrm{CI}=[-4.63\times10^{-5},+1.27\times10^{-5}],
\]

which does not support monotonic increase or decrease.

### Telescoping and boundary sensitivity

Stage-average adjacent differences telescope:

\[
\frac1n\sum_{\ell=a}^{b}(Q_{\ell+1}-Q_\ell)
=\frac{Q_{b+1}-Q_a}{n}.
\]

The registered middle stage contains the large `24→25` drop (`−0.05557`), while the deep stage starts with the `25→26` rebound (`+0.06033`). Therefore the stage contrast partly reflects where the fixed boundary cuts this reversal.

The labeled post-hoc ±1-boundary audit gives deep-minus-early points from `−0.000535` to `+0.006355`; some pointwise intervals cross zero. This audit cannot replace the registered verdict, but it blocks a robust early/middle/deep law.

## 5. Figures

### Eight preselected pairs

![Eight preselected pairs](figures/figure1_eight_representative_adjacent_pairs.png)

Each panel compares two blocks in identical direction identities. The smoothing is visual only; printed intervals use unsmoothed fixed F9--F12 shares and simultaneous all-pair correction.

### Complete transition atlas

![Complete transition atlas](figures/figure2_all_adjacent_transition_atlas.png)

The heatmap shows strong local changes, especially near F1 and F16. The lower panels show that relative F9--F12 redistribution and raw growth can have opposite signs.

### Registered depth inference

![Depth inference](figures/figure3_depth_difference_inference.png)

The registered stages differ, but the full-depth slope crosses zero. The figure explicitly directs the reader to the separate boundary-sensitivity table.

## 6. Evidence lineage

| Decision | Raw artifact | Transformation | Uncertainty | Observed value | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| pair signs | 36 cached Attention-write tensors | shared projection → variance → normalization → adjacent difference | max-deviation interval over 35 pairs | 16 positive, 11 negative, 8 unresolved | heterogeneous | fixed model/data |
| registered depth difference | same | equal-third stage means | paired parent bootstrap; 3-contrast simultaneous interval | deep−early +0.005779 | stage difference | boundary-sensitive telescoping summary |
| monotonic depth law | same | OLS slope across starts 1--35 | paired parent bootstrap | interval crosses zero | unsupported | linear guard only |
| raw scale | same raw band energies | adjacent log2 ratios | all-pair and stage bootstrap intervals | stage means decline | scale differs with depth | not normalized location |

## 7. Verdict and claim boundary

- Registered verdict: `stage_dependent_nonmonotonic`.
- Can claim: the fixed normalized variance proxy varies strongly and reproducibly across adjacent depth positions.
- Cannot claim: a monotonic later shift, a stable three-stage law, added knowledge, conditional novelty, low rank, causal use, or Router utility.
- The full atlas should not be mined for a favorable pair or replacement basis.

## 8. One next decision

Human decision required: whether to close total normalized Attention-write variance as the “new information” metric and replace it with a residual-relative held-out accessibility estimator at one fixed adjacent transition. Completion means explicitly accepting or rejecting that metric change before any new run.

## 9. Artifact map

| Artifact | Location |
| --- | --- |
| Frozen protocol and receipt | [protocol.md](protocol.md) |
| Conclusion-first record | [summary.md](summary.md) |
| all 35 transition metrics | [tables/transition_metrics.csv](tables/transition_metrics.csv) |
| 35×16 band atlas | [tables/bandwise_transition_atlas.csv](tables/bandwise_transition_atlas.csv) |
| registered stage means | [tables/stage_summary.csv](tables/stage_summary.csv) |
| stage and slope contrasts | [tables/depth_contrasts.csv](tables/depth_contrasts.csv) |
| post-hoc boundary audit | [tables/stage_boundary_sensitivity.csv](tables/stage_boundary_sensitivity.csv) |
| projection guards | [tables/projection_diagnostics.csv](tables/projection_diagnostics.csv) |
| worker arrays, logs, and receipts | `/data/250010109/MoE_Router/experiments/20260812_a15_02_06_all_adjacent_depth_transitions/runs/a15-02-06-e05-20260812-all-adjacent/` |
