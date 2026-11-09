---
experiment_id: A15_02_06_E04_layer8_to9_shared_basis_growth
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
---

# Detailed evidence record

## 1. Question and comparison object

The bounded question is whether block 9, relative to block 8, reallocates Attention-write variance toward the previously frozen fine-enriched part of one common parameter spectrum. For record \(x\), \(A_\ell(x)\) is the direct `self_attn.o_proj` output before residual addition at the common final `Classification:` colon.

The coordinate is the unchanged 4096-direction Mean Response basis \(V\), constructed only from all 36 blocks' trace-normalized MLP gate/up input-side Gram operators. Blocks 8 and 9 use the same columns and ordering of \(V\). Therefore direction \(j\) means the same vector in both curves.

## 2. Projection and normalization

The implemented sequence is:

\[
A_\ell(x)\longrightarrow z_{\ell x}=A_\ell(x)^\top V
\longrightarrow e_{\ell j}=\operatorname{Var}_x(z_{\ell xj})
\longrightarrow p_{\ell j}=\frac{e_{\ell j}}{\sum_k e_{\ell k}}.
\]

Thus the projection coefficients are not unit-normalized per record. Normalization happens only after across-record centering and variance estimation. This preserves the meaning of \(p_{\ell j}\) as a fraction of that block's total Attention-write variance. The raw \(e_{\ell j}\) values are retained as an interpretation guard.

Inference uses 16 fixed consecutive bands of 256 directions. The semantic region \(B_{sem}=F_9\cup F_{10}\cup F_{11}\cup F_{12}\) was frozen from E03 before the current transition curve was observed.

## 3. Data, uncertainty, and medium definition

- Data: the same balanced 512-record taxonomy cube, with 8 parents, 8 children per parent, 4 templates, and 2 fact bundles.
- Uncertainty: 2,000 paired parent-bootstrap draws, recomputing global means, variances, normalization, and bands.
- Replication guard: expression halves A and B.
- Bandwise normalized inference: centered 95% simultaneous interval over all 16 fixed bands.

Medium appears only in the block-9 semantic bridge, not in the primary block-8 versus block-9 variance curve. For child mean \(\mu_{pc}\), frozen paired-group mean \(\mu_{pm}\), and parent mean \(\mu_p\):

\[
d^C_p=\mu_p-\mu,
\qquad
d^M_{pm}=\mu_{pm}-\mu_p,
\qquad
d^F_{pc}=\mu_{pc}-\mu_{p,m(c)}.
\]

The medium spectrum is the projected energy of \(d^M_{pm}\) under the same block-9 Mean Response directions. It is a constructed, pairing-specific intermediate scale and is reported descriptively; it is not a native label or the representation used to compute \(p_{8j}\) and \(p_{9j}\).

## 4. Eligibility and conformance

| Guard | Result |
| --- | --- |
| frozen dataset/model/extraction/basis/E03 hashes | PASS |
| block-8 and block-9 cache identities | PASS |
| same Mean Response direction matrix | PASS |
| basis relative orthogonality error | \(2.658\times10^{-6}\) |
| maximum projection/direct trace error | \(9.235\times10^{-8}\) |
| unit tests | 5/5 PASS |
| parent bootstrap | 2,000/2,000 draws retained |
| E03 block-9 fine-minus-coarse point cross-check | absolute error \(4.47\times10^{-8}\); PASS |
| exactly two full-resolution figures and visual audit | PASS |
| protocol deviations | none |

The evidence is eligible for the registered static comparison.

## 5. Registered results

| Metric | Point | 95% interval | Half A | Half B | Registered reading |
| --- | ---: | ---: | ---: | ---: | --- |
| \(D_{sem}\), normalized share change | -0.018314 | [-0.021459, -0.015450] | -0.021707 | -0.014631 | `no_aligned_growth` |
| \(G_{sem}\), raw log2 growth | +0.78997 | [+0.74506, +0.86178] | +0.72021 | +0.74543 | absolute energy increased |
| region specificity | -0.064376 | [-0.073269, -0.058150] | — | — | semantic region did not lead |
| block-9 fine − coarse share | +0.012511 | [+0.001083, +0.020505] | +0.008822 | +0.010406 | semantic bridge remains positive |

The raw growth corresponds to approximately `1.73×` in F9--F12. Across the entire spectrum, total raw write variance rose from `2.872786` to `5.409590`, or `1.88×`. The semantic region therefore grew more slowly than the block-wide total, which explains the negative normalized-share change without contradiction.

### 5.1 Which fixed directions gained normalized share?

The simultaneously positive fixed bands are F1--F6, normalized ranks `[0,0.375)`. F7 is unresolved under the simultaneous interval. F8--F16 are not simultaneously positive; F9, F11, F12, and F13--F16 are simultaneously negative. The narrow terminal spike visible in the smoothed 4096-direction curve does not make the entire F16 band positive.

### 5.2 Why this is not the sought “later new-information band”

All 16 bands show positive raw log2 growth, but the strongest proportional raw increases occur earlier. The transition therefore looks like a broad scale increase with an early-spectrum-biased relative redistribution, not a selective later-spectrum write. Variance growth alone cannot identify information absent from block 8.

## 6. Figure audit

### Figure 1

![Same-direction curves](figures/figure1_layer8_layer9_same_direction_curves.png)

Source: all 512 cached Attention writes for blocks 8 and 9. Metric: \(4096p_{\ell j}\) on log scale and \(4096(p_{9j}-p_{8j})\). Aggregation: unsmoothed estimators; centered 129-direction moving average only for display. Allowed reading: where relative variance is redistributed in identical directions. Limitation: it does not show uncertainty or absolute growth.

### Figure 2

![Registered band evidence](figures/figure2_registered_band_evidence.png)

Panel A carries the 16-band normalized inference with simultaneous intervals. Panel B shows raw band growth with pointwise parent-bootstrap intervals. Panel C shows the separately defined block-9 coarse, medium, and fine semantic spectra and annotates the frozen-region fine-minus-coarse contrast. The figure makes the decisive mismatch visible: F9--F12 are fine-enriched, yet their block-9 normalized transition change is negative.

## 7. Verdict, boundary, and next decision

- Registered typed verdict: `no_aligned_growth`.
- Direct bounded result: block 9 does not increase normalized Attention-write variance share in the frozen fine-enriched region relative to block 8, although raw variance increases there.
- Cannot claim: no new information, no late-spectrum content, universal basis failure, conditional novelty, low rank, causality, or Router utility.
- Human decision required: whether to test a residual-relative conditional-novelty estimator next while keeping block 8→9 and the coordinate fixed. A new basis should not be selected from this negative curve.

## 8. Artifact map

| Artifact | Location |
| --- | --- |
| Frozen protocol and receipt | [protocol.md](protocol.md) |
| Conclusion-first record | [summary.md](summary.md) |
| Registered endpoints | [tables/registered_summary.csv](tables/registered_summary.csv) |
| Complete 16-band evidence | [tables/bandwise_transition.csv](tables/bandwise_transition.csv) |
| A/B guards and semantic contrasts | [tables/split_guards.csv](tables/split_guards.csv) |
| Projection audit | [tables/projection_diagnostics.csv](tables/projection_diagnostics.csv) |
| Provenance and visual audit | [provenance](provenance) |
| Full arrays and logs | `/data/250010109/MoE_Router/experiments/20260812_a15_02_06_layer8_to9_shared_basis_growth/runs/a15-02-06-e04-20260812-layer8-to9/` |
