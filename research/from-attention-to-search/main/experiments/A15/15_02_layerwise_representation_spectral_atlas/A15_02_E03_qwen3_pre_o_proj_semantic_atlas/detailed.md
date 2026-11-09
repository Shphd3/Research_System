# A15_02_E03 Detailed Evidence Ledger

## 1. Question And Typed Verdict

**Question.** Does the full Qwen3-8B attention output, before `o_proj`, already exhibit a late-layer increase in fine-relative-to-coarse semantic discriminability, and is that increase stably localized to a fixed part of the 4096-dimensional natural-background covariance spectrum?

Typed verdict: **`depth_pass_spectral_fail`**.

| Clause | Verdict | Direct reading |
| --- | --- | --- |
| Full-attention depth effect | Pass | Fine-relative discriminability increases from early to late blocks |
| Actual-variance head dominance | Pass | F1 is the maximum-\(b\) band for coarse and fine semantics in every block 1--35 |
| Stable middle enrichment | Fail | Point is near zero and fails design, floor, and half-basis guards |
| Stable tail enrichment | Fail | Descriptive positive point exceeds random q95 but fails the per-late-layer calibration-half direction guard |

## 2. Frozen Architecture Boundary

| Item | Frozen value |
| --- | --- |
| Model | `/data/share/Qwen3-8B` |
| Architecture | 36 decoder blocks, hidden size 4096, 32 query heads, 8 KV heads, head dimension 128 |
| Forward | frozen bfloat16, SDPA, no cache |
| Primary object | direct input to every block's `self_attn.o_proj` |
| Shape | 32 query-head outputs × 128 dimensions, concatenated in native order to 4096 dimensions |
| Readout | shared final `Classification:` colon token |

This object has already aggregated values using attention weights, but has not passed through the learned `o_proj`, residual addition, post-attention normalization, or the MLP.

The earlier E01 object is the raw full decoder-block residual output. It is not the strict MoE post-attention input. E03 and E01 are therefore architecture-boundary observations, not a one-variable causal intervention.

## 3. Reused Semantic And Calibration Data

The semantic cube is exactly inherited from E01:

- 8 parent domains;
- 8 child concepts per parent;
- 4 templates;
- 2 disjoint fact bundles;
- 512 label-free English descriptions;
- T1/T2 design templates and T3/T4 sealed confirmation templates;
- identical readout token and absolute readout position.

Semantic dataset SHA-256: `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859`.

The full text and token ledger is inherited without modification from [actual_semantic_text_sequences.json](../A15_02_E01_qwen3_residual_semantic_variance_atlas/provenance/actual_semantic_text_sequences.json). E03 reused the already extracted semantic attention states only after checking record indices 0--511, all 36 layer shapes `[512,4096]`, source manifests, and the dataset hash.

Natural-background covariance uses the same 128 independent DCLM documents × 512 tokens = 65,536 tokens. Calibration tensor SHA-256: `d88620267dbdc9c2b87ec24c2f51d9e6fb317cb8c051ec96503414ea9bff60b9`. The halves contain 32,768 tokens each.

E02 had stored only 32 separate 128-dimensional within-head covariance blocks. Full 4096-dimensional covariance contains cross-head terms, so E03 newly extracted the full second moment rather than pretending the block-diagonal E02 moments were sufficient.

## 4. Metrics

For coarse role, \(B^c\) is the between-parent variance and \(W^c\) includes child and wording variation inside a parent. For fine role, \(B^f\) separates children conditional on parent, while \(W^f\) measures repeated-template/fact variation inside a child.

\[
D^g=\frac{\operatorname{tr}(B^g)}{\operatorname{tr}(W^g)+\epsilon},
\qquad
R=\log\frac{D^f}{D^c}.
\]

\(D\) is dimensionless. \(R>0\) means fine classes are relatively more separable than coarse classes. Neither metric measures causal model use.

Independent natural-background covariance defines \(\Sigma=U\Lambda U^\top\). The 4096 ordered directions are partitioned into 16 equal-rank 256-dimensional bands: F1=head, F2--F8=middle, F9--F16=tail.

For each semantic role and band:

- \(b\): between-class variance per direction, in activation²; this is actual semantic variance and retains the background singular-value scale;
- \(q\): \(b\) divided by the natural-background eigenvalue; this is background-normalized semantic variance, not discriminability;
- \(j=B/W\): between/within variance inside that band; this is band-local discriminability;
- \(e\): band \(b\) divided by the full-spectrum per-direction mean; this is relative actual-variance enrichment.

The primary depth contrast is

\[
T_{attention}
=\operatorname{median}_{\ell=25:35}R_\ell
-\operatorname{median}_{\ell=1:12}R_\ell.
\]

The basic-bootstrap intervals are centered on the original-sample statistic because hierarchical resampling duplicates parents and biases raw between-parent covariance downward. Consequently, a bias-corrected basic interval need not be symmetric around, or contain, the point estimate.

## 5. Implementation And Execution

Worker surface:

`XingyuD/MoE_Routing_Experiments/active/a15_01_05_e03_qwen3_full_attention_output_semantic_variance_atlas/`

Implementation files:

- `extract_full_covariance.py`: full pre-`o_proj` hook and two-half covariance moments;
- `consolidate_semantic.py`: exact reuse and hash audit of E02 semantic states;
- `analyze_full_atlas.py`: eigendecomposition, semantic metrics, bootstrap/null controls, verdict, and figures.

The system Python lacked the frozen model dependencies. Execution therefore reused the existing experiment-private dependency tree from `a15_00_router_band_response/.deps`; no system package or model file was changed.

The full covariance extraction used two GPUs. Rank 0 handled odd-numbered blocks and rank 1 even-numbered blocks; each rank read all 128 calibration documents. Four documents from the same calibration half were batched, the Gram matrix was accumulated on GPU in FP32, and the global moment was accumulated in CPU FP64. A smoke comparison against direct FP64 established the numerical error bound before full execution.

## 6. Smoke And Hard Guards

| Guard | Smoke | Full | Rule / interpretation |
| --- | ---: | ---: | --- |
| Hook replay maximum absolute error | 0 | 0 | exact |
| 32-head concatenation error | 0 | 0 | exact |
| Separate head projection vs native `o_proj` relative error | \(1.52\times10^{-7}\) | \(1.50\times10^{-7}\) | below \(10^{-6}\) |
| FP32 Gram vs direct FP64 relative error | \(5.17\times10^{-8}\) | at most \(7.03\times10^{-8}\) | below registered tolerance |
| Calibration coverage | 256/256 per half in smoke | 32,768/32,768 per half | exact |
| Layer coverage | 1 and 35 per rank smoke | 36/36 blocks | exact |
| H/M/T split-half stability | representative smoke | all registered layers pass | basis guard |
| Covariance reconstruction | representative smoke | maximum below \(5\times10^{-4}\) | pass |
| Projection energy conservation | representative smoke | maximum below \(5\times10^{-4}\) | pass |

The first attempted smoke stopped before model execution because the system Python had no `transformers`. It is an environment-only invalid attempt. After the dependency path was fixed, no model, data, metric, split, seed, or threshold was changed.

## 7. Depth Clause

| Quantity | Estimate |
| --- | ---: |
| Early blocks 1--12 median \(R\) | 0.153; fine/coarse ratio 1.165 |
| Late blocks 25--35 median \(R\) | 0.764; fine/coarse ratio 2.146 |
| \(T_{attention}\) | 0.6106 |
| Paired basic-bootstrap 95% interval | [0.6238, 1.1562] |
| Block 35 \(R\) | 0.6864; ratio 1.987 |
| Block 36 \(R\) | 0.7923; ratio 2.209 |

All four template contrasts are positive: 0.5803, 0.2113, 0.3386, and 0.6349. All eight leave-one-parent contrasts are positive: 0.5098, 0.7157, 0.5830, 0.6298, 0.7785, 0.6614, 0.4651, and 0.6511.

![Depth and architecture-boundary comparison](figures/figure1_attention_depth_and_residual_comparison.png)

The left panel reports \(\log_{10}D\) for coarse and fine roles. The right panel reports \(R\) and includes E01 residual for descriptive comparison. The final block does not reverse the attention trajectory.

## 8. Actual Variance And Spectral Clause

For both semantic roles, the maximum actual between-class variance \(b\) is in F1 for every block 1--35. This establishes actual-variance head dominance, not semantic sufficiency.

![Full attention-output layer-band atlas](figures/figure2_attention_layer_band_heatmaps.png)

Late median fine-versus-coarse relative actual-variance enrichment is:

| Group | Log ratio | 95% interval | Reading |
| --- | ---: | ---: | --- |
| Head | -0.1074 | [-0.1649, -0.0646] | Fine semantics use a smaller relative share of head variance than coarse semantics |
| Middle | -0.0104 | [-0.0399, 0.0047] | No resolved relative difference |
| Tail | +0.1623 | [0.1319, 0.2533] | Descriptive fine-relative tail enrichment |

The equal-dimensional random-direction late q95 is 0.0590. The tail point exceeds it and remains positive in design templates, nuisance-residual analysis, and every eigenvalue-floor setting. However, the registered rule also requires the direction to remain positive at every late layer under both independently fitted calibration-half bases. That guard fails. Tail is therefore a promising descriptive pattern but not a stable fixed coordinate. Middle also fails design, floor, and half-basis guards.

![Band-local discriminability](figures/figure3_decisive_attention_band_discriminability.png)

The black dots show band/layer cells whose paired interval excludes zero, but the typed spectral conclusion is made at the registered group level with random-orientation, design, nuisance, floor, and half-basis controls. A field of red cells is not itself a spectral pass.

## 9. Comparison With E01 Block Residual

| Representation | Early median \(R\) | Late median \(R\) | Early-to-late \(T\) | Block 35 ratio | Block 36 ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full pre-`o_proj` attention | 0.153 | 0.764 | 0.611 | 1.99 | 2.21 |
| Raw decoder-block residual | 0.001 | 0.452 | 0.451 | 1.82 | 1.84 |

Both boundaries support late fine-relative discriminability, F1 actual-variance dominance, and failure of a stable fixed non-head band. The attention result shows that the signal is observable before `o_proj` and the subsequent residual/MLP path.

The larger attention \(R\) cannot be described as causal attenuation by the residual path because:

1. the coordinate systems and activation scales differ;
2. `o_proj`, residual merging, normalization, and MLP all intervene;
3. \(D=B/W\) is a nonlinear ratio;
4. no activation replacement or module ablation was performed.

## 10. E02 Analysis Correction Discovered During E03 Audit

E03 reused E02 semantic states. A consistency check found that E02's old `split_cube` expression mixed basic and advanced NumPy indexing; the template axis moved to the front before reshape, scrambling parent/template identities. The corrected implementation uses `np.take(..., axis=2)` and adds a regression test for the full parent×child×template×bundle axis order.

The correction preserves the pooled depth effect but changes E02 localization from 14 to 9 globally qualified layer-head cells and removes the former single F1 band pass. E02 is now `attention_depth_pass_head_localization_pass_spectral_fail`. E03's full-width analysis uses the corrected split function and is not affected by the old table.

## 11. Claim Ledger

| Claim | Verdict | Boundary |
| --- | --- | --- |
| Late fine-relative discriminability exists in full pre-`o_proj` attention output | Pass | One frozen Qwen3-8B and one taxonomy |
| Actual coarse/fine semantic variance is head-dominant | Pass | Per-direction \(b\), blocks 1--35 |
| A stable fixed middle band carries fine semantics | Fail | Multiple registered controls fail |
| A stable fixed tail band carries fine semantics | Fail | Calibration-half per-layer direction guard fails |
| Attention signal exists before residual/MLP accumulation | Pass as localization | Not module-level causality |
| Residual path suppresses attention fine semantics | Not tested | No causal intervention |
| Any attention band should guide Router training | Not tested | No expert compatibility or training experiment |

## 12. Visualization Audit

All four PNGs were opened and inspected at rendered resolution.

- Figure 0: spectrum axes, logarithmic scales, block labels, and color bar match `eigenvalue_spectrum.csv`.
- Figure 1: attention and E01 residual use the same \(R\) definition; architecture boundaries are distinguished in legend and caption.
- Figure 2: all nine panels use block on the vertical axis and F1--F16 on the horizontal axis; \(b/q/j\) and log-ratio color bars are explicit.
- Figure 3: the decision heatmap, significance dots, and H/M/T trajectories agree with `band_comparisons_bootstrap.csv`.

## 13. Artifact Map

- Protocol: [protocol.md](protocol.md)
- Chinese Protocol: [protocol_cn.md](protocol_cn.md)
- Canonical summary: [summary.md](summary.md)
- Chinese reading path: [summary_cn.md](summary_cn.md)
- Typed verdict: [provenance/verdict.json](provenance/verdict.json)
- Full extraction manifests: [rank 0](provenance/manifest_rank00.json), [rank 1](provenance/manifest_rank01.json)
- Reused semantic-state audit: [semantic_manifest.json](provenance/semantic_manifest.json)
- Smoke manifests: [rank 0](provenance/smoke_manifest_rank00.json), [rank 1](provenance/smoke_manifest_rank01.json)
- Source hashes: [source_hashes.sha256](provenance/source_hashes.sha256)
- Depth table: [depth_discriminability.csv](tables/depth_discriminability.csv)
- Band metrics: [band_metrics.csv](tables/band_metrics.csv)
- Band intervals: [band_comparisons_bootstrap.csv](tables/band_comparisons_bootstrap.csv)
- Attention/residual comparison: [attention_vs_residual.csv](tables/attention_vs_residual.csv)
- Basis stability: [basis_stability.csv](tables/basis_stability.csv)
- Numerical audit: [energy_conservation.csv](tables/energy_conservation.csv)
- Template robustness: [template_depth_metrics.csv](tables/template_depth_metrics.csv)
- Parent leave-out robustness: [leave_one_parent_out.csv](tables/leave_one_parent_out.csv)
- Random control: [random_subspace_null.csv](tables/random_subspace_null.csv)
- Floor sensitivity: [floor_sensitivity.csv](tables/floor_sensitivity.csv)
- Worker code and large covariance artifacts: `XingyuD/MoE_Routing_Experiments/active/a15_01_05_e03_qwen3_full_attention_output_semantic_variance_atlas/`

## 14. Boundary And One Next Decision

E03 establishes a representation-location fact: the late fine-semantic advantage is visible in the full attention output before `o_proj`. It does not establish attention necessity, causal module contribution, compositional computation, universal covariance coordinates, Router utility, or training benefit.

The one next decision is whether an independent balanced taxonomy reproduces positive depth contrasts at both pre-`o_proj` attention and full block-residual boundaries. Fixed middle/tail bands remain ineligible for Router training.
