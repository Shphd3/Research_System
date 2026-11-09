# A15_02_E01 Detailed Evidence Ledger

## 1. Question And Typed Verdict

**Question.** In a frozen Qwen3-8B, are conditional fine-grained semantic classes increasingly discriminable relative to coarse classes with depth, and do coarse/fine between-class variances occupy distinct positions in a 16-band natural-background covariance basis?

**Typed verdict:** `depth_pass_spectral_fail`.

| Clause | Verdict | Direct result |
| --- | --- | --- |
| Fine-relative depth discriminability | Pass | \(T_{depth}=0.4514\); paired basic-bootstrap 95% CI \([0.3327,1.1891]\) |
| Actual semantic-variance head dominance | Pass | F1 is the 16-band \(b\) argmax in 100% of blocks 1--35 for both roles |
| Fine middle enrichment | Fail | late log enrichment 0.0347, CI \([-0.0042,0.0562]\); below random q95 0.0617 |
| Fine tail enrichment | Fail | late log enrichment 0.0359, CI \([-0.0118,0.1024]\); below random q95 0.0617 |

The result supports a late, basis-free fine-relative representational effect. It does not identify a fixed non-head covariance coordinate for that effect.

## 2. Model And Representation

- Model path: `/data/share/Qwen3-8B`.
- Architecture: `Qwen3ForCausalLM`; 36 decoder blocks; hidden width 4096.
- Tokenizer: `Qwen2TokenizerFast`; vocabulary size 151,669.
- Forward dtype: bfloat16; covariance and inferential statistics: FP64 where applicable.
- Model snapshot manifest SHA-256: `3e33117aebc01710cf1011093bbf4c2700336fce4600788f15d80d69f165dc25`.
- Representation: embedding output plus the raw residual output of every decoder block before final model norm, for 37 sites total.
- Readout: the final colon token in the shared `Classification:` suffix.
- Full extraction: 512 records × 37 sites; hidden width 4096; replay maximum absolute error 0; elapsed time 58.54 s on `cuda:0`.

The inherited `semantic_pairs_sha256` field in [model_manifest.json](provenance/model_manifest.json) belongs to the earlier model-provenance audit and is not the current dataset identity. The current dataset hash is recorded separately below.

## 3. Semantic Dataset

### 3.1 Structure

The dataset contains 8 academic parents and 8 children per parent:

- mathematics, physics, chemistry, biology;
- computer science, economics, medicine, linguistics.

Each of the 64 children has six label-free fact atoms. Four natural-language templates combine two disjoint three-fact bundles, giving

\[
8\ \text{parents}\times8\ \text{children}\times4\ \text{templates}\times2\ \text{bundles}=512\ \text{texts}.
\]

Templates 0--1 form the design split and templates 2--3 form the sealed confirmation split, 256 records each. All 512 full texts and their token ids, labels, template/bundle identities, readout spans, and per-text hashes are in [actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json).

Dataset SHA-256: `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859`.

### 3.2 Data guards

- 512/512 text strings and hashes are unique.
- Correct parent and child label names occur zero times in their description bodies.
- Natural lengths range from 41 to 58 tokens, median 49.
- Masked left padding plus explicit position ids fixes all readouts at absolute RoPE position 57 and padded length 58.
- Every template has 128 records; each fact bundle has 256; every parent/child/split cell has four records.
- A length-only classifier reaches only 0.1914 coarse and 0.1836 fine accuracy, compared with chance 0.125 and near-ceiling contextual-state probes.

### 3.3 What is and is not fixed

Fixed factors include model weights, tokenizer, representation site, readout token and absolute position, taxonomy balance, class counts, four templates, two disjoint fact bundles, design/confirmation split, calibration token set, 16-band boundaries, random seeds, and statistical units.

Factors not fully fixed include natural description length before masked padding, lexical content that necessarily differs by semantic class, English-only wording, one prompt family, one set of eight academic parents, and one pretrained model. Position is fixed and length/template/bundle effects are measured or residualized, so the remaining natural-language variation is acceptable for the within-model question. It restricts cross-taxonomy, cross-language, and cross-model generalization.

## 4. Independent Natural-Text Covariance

- Source: `/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst`.
- Source SHA-256: `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`.
- Selection: 128 independent documents × 512 tokens = 65,536 tokens.
- Calibration token SHA-256: `5c2e9f6b7d307436eda018b7719bc38cddab6387881d77f89bc74fb717b2f792`.
- The current 512 full texts, 512 definition strings, and all three fixed prompt fragments were rechecked against the selected 128 calibration documents: zero exact matches in every category. See [new_dataset_calibration_independence.json](provenance/new_dataset_calibration_independence.json).

Each site uses its own background covariance eigensystem. Hidden width 4096 is split into 16 contiguous 256-dimensional rank bands: F1=head, F2--F8=middle, F9--F16=tail.

![Natural-background singular-value spectrum](figures/figure0_singular_value_spectrum.png)

The upper panel plots background standard deviation \(\sqrt{\lambda_i}\) against decreasing covariance rank; the lower heatmap plots \(\log_{10}(\lambda_i/\lambda_1)\). These are background-data scales, not semantic importance scores.

## 5. Metrics And Physical Meaning

For site \(\ell\), parent \(p\), child \(c\), and template/bundle replicate \(t\):

\[
B_\ell^{coarse}=\operatorname{Cov}_p\left(\mathbb E_{c,t}h_{\ell,p,c,t}\right),
\]

\[
B_\ell^{fine}=\mathbb E_p\operatorname{Cov}_{c\mid p}\left(\mathbb E_t h_{\ell,p,c,t}\right).
\]

Coarse within-class variance includes child and wording variation inside a parent; fine within-class variance includes wording variation inside one child. The primary discriminability metric is

\[
D_{\ell,g}=\frac{\operatorname{tr}(B_\ell^g)}{\operatorname{tr}(W_\ell^g)+\epsilon}.
\]

\(D\) is dimensionless. It is large when class centers are far apart relative to same-class wording variation. It is not total activation energy and does not prove that a classifier or Router uses the distinction.

The relative depth metric is

\[
R_\ell=\log(D_{\ell,fine}/D_{\ell,coarse}).
\]

For covariance band \(k\):

- \(b\): actual between-class semantic variance per direction; units are hidden-state squared;
- \(q\): \(b\) divided directionwise by background eigenvalues; dimensionless background-normalized unusualness;
- \(j\): band between-class variance divided by band within-class variance; dimensionless band discriminability;
- \(e\): \(b\) divided by the role's full-spectrum per-direction mean; dimensionless relative spectral share.

None of \(b\), \(q\), \(j\), or \(e\) is an expert-utility or training-benefit metric.

## 6. Execution And Engineering Audit

Execution was local and frozen; no model training occurred.

1. Data preparation froze the 512 records and copied immutable model/calibration provenance.
2. The first smoke attempt stopped before model inference because system ONNX-generated code was incompatible with the installed protobuf runtime. The run was retained as an invalid engineering attempt. The rerun used the already project-local `protobuf==3.20.3` dependency and did not change model, data, metrics, or thresholds.
3. Smoke covered 8 records and sites 0/1/12/24/35/36; state replay, shape, and projection-energy checks passed.
4. Full extraction covered every record and site with replay error 0.
5. Full analysis used 2,000 nested parent→child→template bootstrap draws, 5,000 hierarchical label permutations, and 256 equal-dimensional random orientations.
6. During result audit, the bootstrap estimate was corrected from the resampled-distribution mean to the original-sample statistic, with paired basic-bootstrap intervals reflected around that statistic. This repair was required because duplicate parents/children mechanically bias raw covariance ratios. Data, model, pass rules, and resample count were unchanged.
7. Maximum projection-energy reconstruction error was below \(1.77\times10^{-6}\), under the \(10^{-5}\) guard.
8. On 2026-08-04, Figure 3 received a visualization-only correction: the N/A
   site-0 panel was replaced by site 28. Site 0 is an identical
   uncontextualized colon embedding rather than a semantic layer; site 28 is
   the first block in the sustained late fine/coarse rise. No data, metric,
   interval, verdict, or other figure changed.

Basic-bootstrap intervals can be displaced from their point estimate under strong small-cluster resampling bias. The registered decision therefore uses the paired early-to-late contrast plus template and parent leave-out directions, not whether every sitewise interval contains its point estimate.

## 7. Depth Result

| Site/range | \(D_{coarse}\) | \(D_{fine}\) | \(R\) | \(\exp(R)\) |
| --- | ---: | ---: | ---: | ---: |
| blocks 1--12 median | 0.354 | 0.375 | 0.001 | 1.00 |
| blocks 25--35 median | 0.825 | 1.298 | 0.452 | 1.57 |
| block 28 | 0.710 | 0.938 | 0.279 | 1.32 |
| block 35 | 0.871 | 1.590 | 0.601 | 1.82 |
| block 36 | 0.823 | 1.513 | 0.609 | 1.84 |

The registered contrast \(T_{depth}\) was 0.4514 with paired basic-bootstrap 95% CI \([0.3327,1.1891]\). Template contrasts were 0.5294, 0.0089, 0.2551, and 0.6843; all were positive. Leave-one-parent-out contrasts ranged from 0.2252 to 0.5835; all eight were positive. Matched probe relative depth gain was +0.0332.

The basis-free trajectory begins a sustained rise around block 28. Block 36 is slightly above block 35 in \(R\), so the final block does not reverse the effect.

![Whole-state discriminability trajectories](figures/figure1_depth_discriminability_trajectories.png)

Site 0 is not interpretable: the shared colon embedding is identical across texts before contextual processing, giving zero between and within variance. It is retained in raw tables and shown as N/A in audited figures.

## 8. Spectral Result

### 8.1 Actual variance

F1 is the maximum-\(b\) band in every block 1--35 for coarse and fine roles. Both semantic granularities therefore remain actual-energy head-dominant.

At block 35:

| Role | Head \(b\) | Middle mean \(b\) | Tail mean \(b\) |
| --- | ---: | ---: | ---: |
| Coarse | 38.082 | 17.494 | 15.906 |
| Fine | 24.967 | 15.037 | 13.419 |

The fine effect is not an absolute-variance increase: coarse \(b\) is higher in every broad group.

### 8.2 Discriminability

At block 35:

| Role | Head \(j\) | Middle mean \(j\) | Tail mean \(j\) |
| --- | ---: | ---: | ---: |
| Coarse | 1.055 | 0.824 | 0.876 |
| Fine | 1.426 | 1.528 | 1.717 |

Fine classes are more separable because their between-child variance is large relative to their within-child template variation. The decisive heatmap shows this rise across nearly the entire spectrum after block 28, not only in middle or tail.

![Decisive layer-by-band discriminability heatmap](figures/figure4_decisive_depth_band_discriminability_heatmap.png)

**Figure contract.** Left x-axis: F1--F16; y-axis: representation site. Color: natural-log \(j_{fine}/j_{coarse}\); positive red means fine classes are more discriminable, negative blue means coarse classes are more discriminable. Black dots mean the paired basic-bootstrap 95% interval excludes zero. Right x-axis: site; y-axis: basis-free \(R\). Shaded bands mark registered early and late windows; block 36 is an open circle. The figure supports a late fine-relative discriminability increase and shows that it is broad across bands. It cannot establish causal computation or Router utility.

### 8.3 Non-head specificity failure

Late middle and tail \(e\) log enrichments were 0.0347 and 0.0359. Their 95% intervals crossed zero, while the equal-dimensional random-orientation late q95 was 0.0617. Design templates, nuisance residualization, and both calibration-half bases had the same positive direction, but that direction was too small and unstable to pass the registered inferential and random-orientation gates.

F1 half-split projector overlap was 0.56--0.79 at representative contextual sites. Individual middle/tail band overlaps were much lower in near-degenerate parts of the spectrum, so a named F2--F16 identity is not a stable universal coordinate even when its heatmap value is descriptive.

![Full layer-by-band b/q/j atlas](figures/figure2_layer_band_coarse_fine_heatmaps.png)

**Figure contract.** Columns are F1--F16 and rows are sites. Left/middle panels show coarse/fine values; right panels show natural-log fine/coarse ratios. The \(b\) row is actual semantic variance, the \(q\) row is background-normalized semantic variance, and the \(j\) row is between/within-class discriminability. Yellow in single-role panels means larger magnitude; red in ratio panels means fine larger, blue means coarse larger. Cross-row colors are not numerically comparable because each metric has its own colorbar.

## 9. Capability And Rival Controls

- Contextual full-state probes pass the hierarchy permutation null for both tasks; most are near ceiling. Probe accuracy is therefore a capability gate, not the depth-effect metric.
- Length-only classification is near chance and far below the contextual probes.
- The depth effect is positive for every held-out template contrast and every parent leave-out.
- Nuisance residualization for length, template, and fact bundle preserves the late spectral-direction estimates.
- Head dominance holds on the sealed confirmation split.
- Fine non-head specificity fails the equal-dimensional random-orientation comparison.
- The last block does not reverse the depth result.

## 10. Claim Boundary

Established:

1. conditional fine semantic classes are more discriminable relative to coarse classes in late than early Qwen3-8B residual states;
2. both coarse and fine actual semantic between-class variance remains F1/head dominant;
3. the late fine-relative discriminability gain is broadly distributed across bands.

Not established:

1. that deep layers perform compositional reasoning;
2. that covariance rank causes semantic granularity;
3. that fine semantics are encoded in a fixed middle or tail band;
4. that any band should guide a Router;
5. that expert compatibility, held-out NLL, or training efficiency improves;
6. that the effect generalizes beyond this model, English taxonomy, prompt, or domain set.

## 11. Artifact Map

- Protocols: [protocol.md](protocol.md), [protocol_cn.md](protocol_cn.md).
- Result summaries: [summary.md](summary.md), [summary_cn.md](summary_cn.md).
- Full semantic text manifest: [actual_semantic_text_sequences.json](provenance/actual_semantic_text_sequences.json).
- Model/calibration/extraction provenance: [model_manifest.json](provenance/model_manifest.json), [calibration_manifest.json](provenance/calibration_manifest.json), [extraction_manifest.json](provenance/extraction_manifest.json).
- Typed verdict: [verdict.json](provenance/verdict.json), [verdict_clauses.csv](tables/verdict_clauses.csv).
- Depth tables: [decisive_depth_summary.csv](tables/decisive_depth_summary.csv), [depth_discriminability.csv](tables/depth_discriminability.csv), [template_depth_metrics.csv](tables/template_depth_metrics.csv), [leave_one_parent_out.csv](tables/leave_one_parent_out.csv).
- Spectral tables: [band_metrics.csv](tables/band_metrics.csv), [band_comparisons_bootstrap.csv](tables/band_comparisons_bootstrap.csv), [selected_layer_broad_band_summary.csv](tables/selected_layer_broad_band_summary.csv), [eigenvalue_band_summary.csv](tables/eigenvalue_band_summary.csv).
- Guards and controls: [probe_capability.csv](tables/probe_capability.csv), [basis_stability.csv](tables/basis_stability.csv), [energy_conservation.csv](tables/energy_conservation.csv), [sensitivity_controls.csv](tables/sensitivity_controls.csv), [random_subspace_null.csv](tables/random_subspace_null.csv), [new_dataset_calibration_independence.json](provenance/new_dataset_calibration_independence.json).
- Worker code/raw artifacts: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_05_e01_qwen3_coarse_fine_semantic_variance_atlas/`.

## 12. Exactly One Next Decision

Decide whether to run one independent balanced-taxonomy replication of the basis-free \(T_{depth}\) effect. The fixed F2--F16 spectral-coordinate hypothesis is not admitted to Router or matched-training experiments by this result.
