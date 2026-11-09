# A10_02 Frequency-Singular SGD Instability Detailed Record

## 1. Purpose And Decision

This experiment tests the first operational version of the 0701 design:

\[
\text{Zipfian frequency} \to \text{common-feature gradient coherence} \to \text{singular-value growth} \to \text{gradient amplification} \to \text{high-learning-rate SGD instability}.
\]

Decision question:
In a small nested-prefix causal model, does Zipfian frequency produce output-head singular concentration that predicts high-learning-rate SGD instability?

Decision after this run:
The full late-instability claim is not established. The main evidence supports a narrower rare-suppression mechanism under high SGD learning rate.

## 2. Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| Nested-prefix task | A controlled next-token task where prefixes inherit earlier tokens | \(A\to AB\to ABC\to \cdots \to ABCDEFG\) | Sequence family | Creates common parent and rare child transitions | Not real language |
| Common target | A frequent early prefix target | Targets \(A\) and \(B\) | Accuracy/loss over labels \(\le 1\) | Measures early common learning | Not semantic common features |
| Rare target | A late prefix extension target | Targets \(E\), \(F\), and \(G\) | Accuracy/loss over labels \(\ge 4\) | Measures long-tail extension learning | Not real rare-token semantics |
| Top singular-value growth | Growth of the largest singular value of the output head | final \(\sigma_1(W_{\mathrm{out}})\) / initial \(\sigma_1(W_{\mathrm{out}})\) | Ratio | Measures high-gain readout formation | Not a Hessian eigenvalue |
| Top-2 energy | Fraction of output-head spectral energy in the top two singular modes | \(\sum_{i\le2}\sigma_i^2/\sum_i\sigma_i^2\) | Fraction | Measures spectral concentration | Not causal alone |
| Top-band gradient mass | Output-head gradient energy in the top right-singular subspace | \(B_{\mathrm{top}}(G)=\|G V_{\mathrm{top}}\|_F^2/(\|G\|_F^2+\epsilon)\) | Fraction | Tests whether updates use amplified modes | Not sufficient without intervention |
| Extra-feature effective rank | Effective number of directions used by adjacent prefix hidden differences | SVD entropy rank of \(E\) | \(\operatorname{erank}(E)\) | Tests extension-direction collapse | Not semantic interpretability |
| Extra top-2 mass | Mean projection of extension directions onto top two output-head right singular vectors | \(\|E_{\mathrm{norm}}V_{\mathrm{top}}\|^2\) averaged over extensions | Fraction | Tests reuse of high-gain subspace | Not causal alone |

## 3. Setup

Workspace:
`/data/250010109/Research_System`.

Experiment directory:
`Projects/from-attention-to-search/main/experiments/A10/A10_02_frequency_singular_sgd_instability`.

Anchor:
`Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_02_frequency_singular_sgd_instability_anchor.md`.

Script:
`scripts/run_frequency_singular_sgd_instability.py`.

Data:
Synthetic Zipfian nested-prefix next-token examples. Maximum prefix depth is 7. A sampled depth \(L\) contributes next-token labels for prefixes up to that depth, so early targets have higher realized frequency than late targets.

Model:
One-layer, one-head causal next-token model with hidden dimension 32, token embeddings, position embeddings, causal attention, feed-forward block, LayerNorm, and output head.

Main local run:

| Field | Value |
| --- | --- |
| run name | `full_local_20260703_033712` |
| seeds | `0,1,2` |
| steps | 240 |
| batch size | 192 |
| eval size | 2048 |
| safe SGD LR | 0.25 |
| high SGD LR | 0.9 |
| AdamW LR | 0.006 |
| stop on instability | enabled |

Remote stress run:

| Field | Value |
| --- | --- |
| SCO job | `pt-c6a1nhsr` |
| state | `SUCCEEDED` |
| run name | `full_sco_20260703_033834` |
| high SGD LR | 2.0 |
| role | stress run, not calibrated boundary run |

## 4. Conditions

| Condition | Purpose | Mechanism tested |
| --- | --- | --- |
| `adamw_ce` | Adaptive stable baseline | Whether adaptive scaling avoids the failure |
| `sgd_safe_ce` | Low-LR SGD baseline | Whether ordinary SGD can learn when LR is safe |
| `sgd_high_ce` | Main boundary probe | Whether high LR causes spectral rare suppression or instability |
| `sgd_high_row_clip` | SGD-LL-style probe | Whether clipping output-token rows rescues the failure |
| `sgd_high_row_norm` | SCALE-like probe | Whether row normalization rescues the failure |
| `sgd_high_label_smoothing` | Margin-pressure probe | Whether reducing margin pressure rescues rare learning |
| `sgd_high_spectral_clip` | Direct spectral probe | Whether capping output-head singular values is enough |

## 5. Main Local Evidence

Main table from `tables/local_full_condition_summary.csv`:

| condition | stable rate | final eval loss | common acc | rare acc | top-SV growth | top-2 energy | top-band grad mass | extra erank | extra top-2 mass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `adamw_ce` | 1.00 | 0.0007 | 1.000 | 1.000 | 1.91 | 0.413 | 0.352 | 4.68 | 0.303 |
| `sgd_safe_ce` | 1.00 | 0.0019 | 1.000 | 1.000 | 1.96 | 0.422 | 0.240 | 4.45 | 0.344 |
| `sgd_high_ce` | 1.00 | 0.5818 | 0.895 | 0.434 | 3.68 | 0.662 | 0.556 | 2.46 | 0.472 |
| `sgd_high_row_clip` | 1.00 | 0.0004 | 1.000 | 1.000 | 2.42 | 0.448 | 0.213 | 4.47 | 0.258 |
| `sgd_high_row_norm` | 1.00 | 0.0004 | 1.000 | 1.000 | 2.82 | 0.505 | 0.255 | 4.45 | 0.244 |
| `sgd_high_label_smoothing` | 1.00 | 0.1603 | 1.000 | 1.000 | 2.36 | 0.475 | 0.350 | 4.34 | 0.280 |
| `sgd_high_spectral_clip` | 1.00 | 0.4769 | 0.895 | 0.667 | 2.96 | 0.562 | 0.347 | 3.19 | 0.317 |

### Interpretation

`sgd_high_ce` did not diverge at `high_lr=0.9`, so the primary instability-localization metric is not satisfied. However, it produced a clear rare-suppression pattern:

- rare accuracy dropped to `0.4335`, while AdamW, safe SGD, row clipping, row normalization, and label smoothing reached `1.0000`;
- top singular-value growth rose to `3.6756`, compared with `1.9569` for safe SGD;
- top-2 spectral energy rose to `0.6622`, compared with `0.4223` for safe SGD;
- extra-feature effective rank fell to `2.4621`, compared with `4.4471` for safe SGD;
- extra top-2 mass rose to `0.4721`, compared with `0.3443` for safe SGD.

This supports a narrowed mechanism:

\[
\text{high SGD LR} \to \text{stronger spectral concentration} \to \text{rare extension rank collapse / top-subspace reuse}.
\]

It does not yet prove:

\[
\text{spectral concentration} \to \text{late divergence}.
\]

## 6. Per-Seed Failure Pattern

`sgd_high_ce` was seed-sensitive:

| seed | final eval loss | common accuracy | rare accuracy | top-SV growth | top-band grad mass | extra erank | extra top-2 mass |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.0004 | 1.000 | 1.000 | 3.55 | 0.083 | 4.51 | 0.249 |
| 1 | 0.8012 | 1.000 | 0.301 | 4.06 | 0.817 | 1.86 | 0.473 |
| 2 | 0.9439 | 0.685 | 0.000 | 3.41 | 0.769 | 1.01 | 0.694 |

Interpretation:
The two failing seeds show high top-band gradient mass and collapsed extra-feature rank. The successful seed has low top-band mass and high extra-feature rank. This is useful mechanism evidence but not a deterministic theorem.

## 7. Remote Stress Evidence

The remote run used default `high_lr=2.0`; this is a stress run, not the calibrated main boundary.

Main stress table from `tables/remote_stress_condition_summary.csv`:

| condition | stable rate | mean instability step | rare acc | top-SV growth | top-2 energy | top-band grad mass | extra erank |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `sgd_high_ce` | 0.00 | 12.33 | 0.000 | 3248.10 | 0.996 | 0.945 | 1.01 |
| `sgd_high_row_clip` | 0.33 | 46.00 | 0.333 | 1121.52 | 0.873 | 0.659 | 4.44 |
| `sgd_high_row_norm` | 0.33 | 16.50 | 0.333 | 13131.24 | 0.893 | 0.723 | 2.69 |
| `sgd_high_label_smoothing` | 0.00 | 13.33 | 0.000 | 6749.30 | 0.997 | 0.838 | 1.00 |
| `sgd_high_spectral_clip` | 0.33 | 7.50 | 0.524 | 4.04 | 0.664 | 0.490 | 2.16 |

Interpretation:
At `high_lr=2.0`, SGD can fail with extreme spectral concentration. But this run is too aggressive: failures often occur around steps 11-13, before a clean common-to-rare temporal story is available. It is therefore a stress artifact, not the primary anchor decision evidence.

## 8. Visualization Results

### Temporal Profile

![Temporal profile](figures/local_full/temporal_profile.png)

Purpose:
Test whether common learning, rare learning, top singular value, and eval loss separate by condition.

Observed result:
Safe baselines learn both common and rare targets. High-LR SGD has higher top singular value and weaker rare behavior. Spectral clipping only partially rescues this in the boundary run.

Limitation:
The figure averages seeds, hiding the seed-specific rare-collapse pattern.

### Spectral Localization

![Spectral localization](figures/local_full/spectral_localization.png)

Purpose:
Measure whether output-head gradients occupy the current top singular subspace.

Observed result:
`sgd_high_ce` has the highest sustained top-band gradient mass. Row clipping and row normalization lower token-gradient concentration and top-band mass.

Limitation:
This supports localization of the rare-suppression regime, not late divergence.

### Extra-Feature Geometry

![Extra-feature geometry](figures/local_full/extra_feature_geometry.png)

Purpose:
Test whether prefix extensions keep independent hidden directions or collapse into top output-head directions.

Observed result:
`sgd_high_ce` lowers extra-feature effective rank and raises extra top-2 mass. Stable baselines and row-based interventions keep higher rank and lower top-2 mass.

Limitation:
Hidden differences are controlled-task proxies, not real semantic features.

## 9. Hypothesis Ledger

| Hypothesis | Result | Evidence | Boundary |
| --- | --- | --- | --- |
| H1: frequency-gradient link | Partially supported | Early frequency-gradient correlation is positive for unmodified AdamW, high-LR SGD, label smoothing, and spectral clipping | Row interventions intentionally alter the row-gradient geometry |
| H2: common-to-spectrum temporal order | Supported in this setup | Common learning appears early; high-LR SGD has stronger spectral concentration and rare-rank collapse | Does not prove real LM transfer |
| H3: instability localization | Insufficient in main run | No qualifying late instability at `high_lr=0.9`; stress `high_lr=2.0` fails early with spectral blow-up | Stress run is not clean causal-chain evidence |
| Row clipping / normalization as probes | Supported as probes | Both recover rare accuracy and reduce collapse metrics in the boundary run | They are not final optimizer claims |
| Spectral clipping as implemented | Weakened | It only partially rescues rare learning and remains seed-sensitive | Cap value may be too loose or wrong target |

## 10. Artifact Map

Anchor:
`Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_02_frequency_singular_sgd_instability_anchor.md`.

Protocol:
`protocol.md`.

Script:
`scripts/run_frequency_singular_sgd_instability.py`.

Main local run:
`runs/full_local_20260703_033712`.

Remote stress run:
`runs/full_sco_20260703_033834`.

Remote job:
`pt-c6a1nhsr`, state `SUCCEEDED`.

Main tables:
`tables/local_full_condition_summary.csv`, `tables/local_full_final_by_seed.csv`, `tables/local_full_step_metrics.csv`.

Remote stress tables:
`tables/remote_stress_condition_summary.csv`, `tables/remote_stress_final_by_seed.csv`, `tables/remote_stress_step_metrics.csv`.

Default tables:
`tables/condition_summary.csv`, `tables/final_by_seed.csv`, and `tables/step_metrics.csv` have been restored to the main local boundary run.

Main figures:
`figures/local_full/temporal_profile.png`, `figures/local_full/spectral_localization.png`, `figures/local_full/extra_feature_geometry.png`, `figures/local_full/stability_by_condition.png`.

Remote stress figures:
`figures/remote_stress/`.

Remote logs:
`logs/acp/full_sco_20260703_033834_submit_20260703_033835.log`, `logs/acp/full_sco_20260703_033834_runtime_20260703_033917.log`.

## 11. Claim Boundary

Can claim:
The controlled nested-prefix benchmark shows a high-LR SGD rare-suppression regime associated with stronger output-head spectral concentration, higher top-band gradient mass, lower extra-feature effective rank, and higher extra top-2 mass. Row clipping, row normalization, and label smoothing rescue the rare path in the calibrated boundary run.

Cannot claim:
This does not prove the origin of high-LR SGD instability in real language models. It does not prove Adam's advantage comes from common-feature normalization. It does not prove the theoretical maximum learning rate after spectral flattening. It does not update the nested learning / MoE gating mainline.

## 12. Next Decision

The next experiment should be a learning-rate and noise boundary map:

1. noiseless / full-batch: locate the transition from stable learning to rare suppression to divergence;
2. noisy labels or noisy features / full-batch: test whether noise lowers the spectral threshold;
3. noisy data / mini-batch: test whether batch noise turns rare suppression into earlier divergence.

This directly connects the 0701 seminar question about full-batch, noisy full-batch, and noisy mini-batch regimes to measurable spectral diagnostics.
