# A15_02_E02 Corrected Detailed Evidence Ledger

## 1. Correction Notice

On 2026-08-05, consistency work for E03 found an axis-order defect in E02's template split. The old expression

```python
cube[:, :, templates, :, layer]
```

combined advanced indexing on `templates` with a later scalar index. NumPy moved the advanced-index axis to the front; the subsequent reshape therefore did not preserve parent×child×template×bundle hierarchy.

The corrected implementation uses explicit axis-preserving selection:

```python
np.take(cube, templates, axis=2)[:, :, :, :, layer]
```

A regression test now constructs distinct parent/child/template/bundle markers and checks the full split order. The test suite passes 5/5.

This correction changes the selection-localization evidence but not the extracted model states. All tables, verdict, and figures in this experiment directory have been replaced by the corrected reanalysis at:

`XingyuD/MoE_Routing_Experiments/active/a15_01_05_e02_qwen3_attention_head_semantic_variance_atlas/runs/reanalysis_axisfix_20260805/`

## 2. Question And Corrected Verdict

**Question.** Is the late fine-semantic discriminability found in Qwen3-8B residual states already present in individual multi-head-attention outputs before `o_proj`, and is it localized to reproducible heads or fixed within-head covariance bands?

Corrected typed verdict: **`attention_depth_pass_head_localization_pass_spectral_fail`**.

| Clause | Corrected verdict |
| --- | --- |
| Pooled pre-`o_proj` depth effect | Pass |
| Family-wise-corrected individual-head localization | Pass |
| Within-head fixed-band specificity | Fail |

The superseded result was `attention_depth_pass_head_localization_pass_spectral_pass`, with 14 qualified heads and one F1 band. Those two localization numbers must not be used.

## 3. Frozen Object And Data

| Item | Value |
| --- | --- |
| Model | `/data/share/Qwen3-8B` |
| Object | input to each `self_attn.o_proj`, reshaped `[batch,sequence,32,128]` |
| Semantic data | 8 parents ×8 children ×4 templates ×2 bundles =512 records |
| Natural covariance | 128 DCLM documents ×512 tokens =65,536 tokens |
| Semantic SHA-256 | `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859` |
| Calibration SHA-256 | `d88620267dbdc9c2b87ec24c2f51d9e6fb317cb8c051ec96503414ea9bff60b9` |

The extraction remains valid: hook replay and head concatenation are exact; separate-head projection reconstructs native `o_proj` inside tolerance; calibration coverage and state shapes are complete.

## 4. Metrics

For each layer-head cell:

\[
D^c=\frac{\operatorname{tr}(B^c)}{\operatorname{tr}(W^c)+\epsilon},
\qquad
D^f=\frac{\operatorname{tr}(B^f)}{\operatorname{tr}(W^f)+\epsilon},
\qquad
R=\log(D^f/D^c).
\]

\(R>0\) means fine classes are relatively more separable than coarse classes inside that head. It does not measure causal use.

Each qualified 128-dimensional head is independently decomposed into 16 equal-rank 8-dimensional bands. A band passes only if it exceeds paired uncertainty, calibration-basis stability, and a same-head random-8D orientation q95.

## 5. Corrected Pooled Depth Result

| Quantity | Value |
| --- | ---: |
| \(T_{attention}\) | 0.6106198 |
| paired basic-bootstrap 95% interval | [0.6039343, 1.2096409] |
| template contrasts | 0.5803, 0.2113, 0.3386, 0.6349 |
| leave-parent contrasts | 0.5098, 0.7157, 0.5830, 0.6298, 0.7785, 0.6614, 0.4651, 0.6511 |

The same pooled \(T\) is independently recovered by E03's full-width 4096-dimensional analysis to approximately \(10^{-7}\). This cross-analysis agreement supports the corrected hierarchy handling.

![Corrected layer-head atlas](figures/figure1_layer_head_discriminability_atlas.png)

## 6. Corrected Individual-Head Localization

The family-wise late-layer maximum-permutation q95 is 1.7460428. Nine cells pass all registered conditions:

| Cell | \(R\) | Fine/coarse ratio |
| --- | ---: | ---: |
| L30H27 | 2.4246 | 11.30 |
| L30H5 | 2.0880 | 8.07 |
| L32H15 | 1.9835 | 7.27 |
| L31H8 | 1.9570 | 7.08 |
| L30H25 | 1.9567 | 7.08 |
| L33H10 | 1.9173 | 6.80 |
| L32H20 | 1.8860 | 6.59 |
| L31H11 | 1.7798 | 5.93 |
| L34H14 | 1.7795 | 5.93 |

![Corrected global head selection](figures/figure2_head_localization_and_global_null.png)

These numerical head indices identify positions only inside their own layers. They do not imply cross-layer functional identity.

## 7. Corrected Within-Head Spectral Result

Passing spectral-band count: **0**.

![Corrected selected-head 16-band atlas](figures/figure3_selected_head_16band_atlas.png)

No F1, F2--F8, or F9--F16 band in any qualified head passes the registered same-head orientation and stability gates. The former `L32H27-F1` claim is withdrawn.

## 8. Corrected Claim Ledger

| Claim | Verdict |
| --- | --- |
| Late fine-relative discriminability exists before `o_proj` | Pass |
| At least one late individual head is exceptional after family-wise correction | Pass; 9 cells |
| A fixed within-head covariance band carries the effect | Fail; 0 bands |
| Attention causes the semantic refinement | Not tested |
| The qualified cells improve Router or expert training | Not tested |

## 9. Artifact Map

- Corrected typed verdict: [provenance/verdict.json](provenance/verdict.json)
- Corrected source hash: [provenance/source_hashes.sha256](provenance/source_hashes.sha256)
- Pooled trajectory: [tables/pooled_attention_trajectory.csv](tables/pooled_attention_trajectory.csv)
- Full head table: [tables/head_discriminability.csv](tables/head_discriminability.csv)
- Qualified heads: [tables/qualified_heads.csv](tables/qualified_heads.csv)
- Global null: [tables/global_head_permutation_null.csv](tables/global_head_permutation_null.csv)
- Band metrics: [tables/head_band_metrics.csv](tables/head_band_metrics.csv)
- Orientation controls: [tables/spectral_random_orientation_controls.csv](tables/spectral_random_orientation_controls.csv)
- Basis stability: [tables/basis_stability.csv](tables/basis_stability.csv)
- Corrected figures: [figure 1](figures/figure1_layer_head_discriminability_atlas.png), [figure 2](figures/figure2_head_localization_and_global_null.png), [figure 3](figures/figure3_selected_head_16band_atlas.png), [figure 4](figures/figure4_selected_head_covariance_spectra.png)

## 10. Boundary And Next Decision

The corrected result establishes a robust pooled depth effect and globally corrected late-head peaks, but no fixed within-head spectral coordinate. It cannot establish attention necessity, causal computation, cross-layer head identity, Router utility, expert compatibility, or training benefit.

The one next decision is whether an independent balanced taxonomy reproduces the pooled pre-`o_proj` depth effect and at least one family-wise-corrected late layer-head cell. Fixed covariance bands remain ineligible for Router training.
