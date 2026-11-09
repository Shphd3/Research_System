---
experiment_id: A15_02_06_E03_shared_basis_semantic_granularity
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
---

# Detailed evidence record

## 1. Question, object, and registered decision

The bounded question is whether semantic granularity maps to later normalized rank in one fixed common MLP parameter coordinate. The primary variable is fine minus coarse; medium is an ordinal guard built from a frozen, semantically named pairing of the eight children inside each parent.

The activation is Qwen3-8B's direct `self_attn.o_proj` output before residual addition at the common final `Classification:` colon. The coordinate is the E02 mean-response basis, obtained by eigendecomposing the average of all 36 trace-normalized operators

\[
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}.
\]

No semantic activation selects or changes this basis. The complete frozen definitions and medium mapping are in [protocol.md](protocol.md).

## 2. Data and hierarchy decomposition

The source is the audited 512-record balanced taxonomy cube: 8 parents, 8 children per parent, 4 templates, and 2 fact bundles. A/B each retain four expressions per parent-child cell. No new model inference was required; all 36 cached 512-by-4096 Attention-write tensors were hash-verified and reused.

For child mean \(\mu_{pc}\), medium-group mean \(\mu_{pm}\), parent mean \(\mu_p\), and grand mean \(\mu\), the three pure components are

\[
d^C_p=\mu_p-\mu,\quad
d^M_{pm}=\mu_{pm}-\mu_p,\quad
d^F_{pc}=\mu_{pc}-\mu_{p,m(c)}.
\]

The implementation verifies \(\mu_{pc}-\mu=d^C_p+d^M_{p,m(c)}+d^F_{pc}\). For each level, projected direction energy is normalized to unit total before computing rank centroid and interval share. Effective rank is not used because it measures spectral width rather than location.

## 3. Inference contract

- Primary endpoint: median over blocks 1--35 of \(r_F-r_C\); block 36 is displayed and excluded.
- Uncertainty: 2,000 paired bootstraps over the eight parent domains, recomputing the coarse grand mean in every draw; layers are not treated as independent samples.
- Expression guard: recompute endpoints independently on halves A and B.
- Medium guard: compare the real semantic pairing's \(\min(T_{M-C},T_{F-M})\) against 256 balanced random child pairings.
- Auxiliary requested band: normalized ranks `[0.50,0.75)`, one-based ranks 2049--3072. Neighboring registered intervals are `[0.375,0.625)` and `[0.625,0.875)`.

## 4. Eligibility and numerical audit

| Guard | Result |
| --- | --- |
| semantic/model/extraction/basis/reference hashes | PASS |
| exact 512-record balance and complete child pairing | PASS |
| unit tests | 5/5 PASS |
| real-cache smoke, blocks 1/18/35 | PASS |
| mean-response basis relative orthogonality error | \(2.6581\times10^{-6}\) |
| maximum projection/direct energy relative error | \(3.7913\times10^{-7}\) |
| full 36-layer execution | PASS |
| 2,000 parent bootstrap draws | PASS; no NaN centroid draws |
| 256 random-pairing controls | PASS |
| exactly two registered final figures, full-resolution visual audit | PASS; the later two-metric figure is presentation-only |

The evidence is eligible for the frozen static comparison. Exact source, code, environment, execution, and visual receipts are under [provenance](provenance).

## 5. Results

### 5.1 Threshold-free spectral location

| Contrast | Point | 95% interval | Half A | Half B | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| \(T_{M-C}\) | +0.005181 | [+0.001451, +0.009696] | +0.007818 | +0.002797 | medium later than coarse |
| \(T_{F-C}\) | +0.008175 | [+0.001964, +0.012620] | +0.009568 | +0.006794 | primary Pass |
| \(T_{F-M}\) | +0.004089 | [+0.000958, +0.005287] | +0.003737 | +0.003570 | fine later than medium |

Fine minus coarse is positive as a point estimate in 28 of 35 registered blocks. Several layerwise intervals cross zero; therefore the result is not an assertion of strict ordering at every block.

### 5.2 Medium specificity

The real mapping's ordered score is `0.004089`. The 95th percentile under 256 balanced random pairings is `0.001540`. The mapping-specificity guard therefore passes and the registered medium outcome is `ordered_three_level_support`.

This guard rules out the claim that any arbitrary pairing of the same eight children gives an equally strong ordered result. It does not make the constructed groups independent observations or native dataset annotations.

### 5.3 Fixed middle-late share and sensitivity

| Rank interval | Contrast | Point | 95% interval | Interpretation |
| --- | --- | ---: | ---: | --- |
| `[0.50,0.75)` | fine − coarse | +0.004893 | [+0.002433, +0.007840] | requested band positive |
| `[0.375,0.625)` | fine − coarse | +0.003290 | [+0.001204, +0.006421] | neighboring band positive |
| `[0.625,0.875)` | fine − coarse | +0.005357 | [+0.003253, +0.008375] | neighboring band positive |
| `[0.375,0.625)` | fine − medium | -0.000165 | [-0.000858, +0.002109] | local three-level ordering unresolved |

The fine-minus-coarse location conclusion is not created by the chosen `[0.50,0.75)` boundary. The stronger claim that all three levels are ordered inside every candidate middle band is not supported.

### 5.4 Absolute-scale reminder

Across blocks 1--35, median direct component traces are 2.757 (coarse), 1.227 (medium), and 1.369 (fine), with strong growth across depth. These quantities have different hierarchical meanings and are not the primary comparison. The normalized spectral results must not be restated as “fine contains more variance” or “fine contains more information.”

## 6. Figure audit

### Figure 1

![Mean-response common-basis reference](figures/figure1_mean_response_common_basis_reference.png)

Question: what layer-dependent fine-only curve motivated the semantic comparison? Source: unchanged E02 normalized-energy array. Aggregation: selected layers, 129-rank moving average for display only. Allowed reading: the mean-response basis gives different normalized profiles across depth. Limitation: no coarse/medium contrast and no absolute scale.

### Figure 2

![Semantic-granularity result](figures/figure2_semantic_granularity_spectral_location.png)

Panel A shows the threshold-free fine-minus-coarse normalized density across all ranks and layers. Panel B shows centroid differences and parent-bootstrap intervals. Panel C shows the requested fixed `[0.50,0.75)` share differences. The dashed horizontal/vertical boundary identifies block 36, which is excluded from global endpoints. Allowed reading: in this fixed coordinate and taxonomy, the normalized semantic spectrum is ordered later with finer granularity at the trajectory level.

### Presentation-only two-metric view

![Explained two-metric semantic trend](figures/presentation_two_metric_semantic_trend_explained.png)

This presentation view contains only the two registered scalar metrics from Figure 2. The left axis is explicitly \(100(r_F-r_C)\) in rank-percentile points; the right axis is \(100(s_F-s_C)\) in energy-share percentage points. Multiplication by 100 is a display-unit conversion only and does not change the observations, bootstrap draws, estimators, or verdict. The complete Chinese generation and reading contract is recorded in [presentation_two_metric_semantic_trend_explained_cn.md](figures/presentation_two_metric_semantic_trend_explained_cn.md).

## 7. Verdict, boundary, and one next decision

- Primary typed verdict: `fine_later_than_coarse`.
- Medium typed verdict: `ordered_three_level_support`.
- Direct bounded inference: a positive semantic-granularity-to-spectral-location relationship exists in the frozen mean-response basis for these Attention writes.
- Cannot claim: universal rank semantics, every-layer or every-band monotonicity, residual-relative novelty, low rank, causal use, or Router utility.
- Exactly one next decision: the researcher must decide whether this basis-specific ordering is sufficient to authorize a separate frozen functional Router-admission test.

## 8. Artifact map

| Artifact | Location |
| --- | --- |
| Frozen protocol | [protocol.md](protocol.md) |
| Conclusion-first record | [summary.md](summary.md) |
| Global metrics | [tables/global_summary.csv](tables/global_summary.csv) |
| Complete layerwise metrics | [tables/layerwise_metrics.csv](tables/layerwise_metrics.csv) |
| Band sensitivity | [tables/middle_late_sensitivity.csv](tables/middle_late_sensitivity.csv) |
| Medium random-pairing control | [tables/random_pairing_control.csv](tables/random_pairing_control.csv) |
| Projection audit | [tables/projection_diagnostics.csv](tables/projection_diagnostics.csv) |
| Presentation-only two-metric figure | [figures/presentation_two_metric_semantic_trend_explained.png](figures/presentation_two_metric_semantic_trend_explained.png) |
| Presentation figure generation and reading contract | [figures/presentation_two_metric_semantic_trend_explained_cn.md](figures/presentation_two_metric_semantic_trend_explained_cn.md) |
| Provenance receipts | [provenance](provenance) |
| Full arrays and logs | `/data/250010109/MoE_Router/experiments/20260812_a15_02_06_shared_basis_semantic_granularity/runs/a15-02-06-e03-20260812-granularity/` |
