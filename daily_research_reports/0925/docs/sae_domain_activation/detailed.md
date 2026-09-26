# Detailed: frozen sidecar domain-activation readout

[Summary](summary.md) · [中文](summary_cn.md)

## Direct result and eligibility

Bounded descriptive replication supports domain-conditioned activation differences on four fixed natural academic corpora. It does not establish semantic purity, cross-corpus generalization, or prediction of parameter-sharing interference. Researcher asked to complete hypothesis2 by using the existing sidecar on different-domain corpora; this authorizes the bounded read-only measurement, not a new full training run or scientific-state promotion.

## Setup, prior source and selected records

Execution root: `/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation`. Exact model checkpoint: `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_021000000000`; recomputed state SHA256 `edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33`. Sidecar observes layer7/code-index attention output after output projection and before residual addition. Dictionary30,000, fixed top32, original FP32 frozen weights with BF16 autocast inference. Prior verified loading/capture implementation: `/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/scripts/smoke_sites.py`; model identity obtained from the exact21B four-model audit manifest and reverified against current checkpoint bytes. The older cache only retained atom indices for a small reuse panel and lacked full activation values, so it was not sufficient for the requested replication; no old result was presented as a new measurement.

Data source: existing `N8_v1/fit.jsonl` and `test.jsonl`, revision `6ae613ba744ee56f645aee9c577d04f7e3d48b30`. Fields: cs.CL/cs.CV, math.AG/math.NT, physics.flu-dyn/physics.optics, q-bio.GN/q-bio.NC. Map to computer science/mathematics/physics/biology. Each subfield/split selects64 records sorted by SHA256 of `sae-domain-20260925|sample_id`, without activation-dependent selection. Every input is exactly256 pretokenized content tokens;1,024 unique sample IDs and unique complete input hashes. No question/answer template, injected domain label, trainable adapter or generated paraphrase. The source collection was screened previously for exact/approximate duplicates, but paper IDs are unavailable; different record IDs do not guarantee different papers. Previous audit exposure means this is not a new sealed confirmatory test.

## Extraction guards and completion

Local H100 MIG3g40GB, no ACP submission; hard command timeout900s. Exact checkpoint hash, expected architecture, finite/nonnegative values, capture equality to model-native SAE input, repeated encoding equality, frozen state sample and unchanged activity buffers passed. Extraction completed1024 records/262144 tokens in61.18s; optimizer updates0. `extraction.log`, `smoke_receipt.json`, `extraction_receipt.json` and `activations.npz` preserve provenance. The model was not retrained or changed. No figure produced.

## Metrics and evidence lineage

| Object | Raw → computation | Aggregation | Result / boundary |
| --- | --- | --- | --- |
| Body firing profile |Positive top32 indices → per-document feature counts/256 |Mean128 records/domain/batch; normalize sum for distances |Within0.131919, between0.393723; fixed-panel description |
| Cross-batch domain readout |Fit-domain raw-frequency centroids → cosine nearest centroid for each test record |512 heldout records, balanced domains/subfields |458 correct;89.45%; conditional95% interval86.72–91.80% |
| Chance control |Shuffle fit labels199 times, retain balanced counts |Same estimator and fixed test labels |p=(1+0)/200=0.005; association, not causation |
| Amplitude |Positive values sum/256 |Separate profile/centroid pipeline |89.84%; not merged with frequency |
| Last position |Positive top32 indices only at position255 |Separate profile/centroid pipeline |80.66%; not substituted for body primary |
| Feature replication |Top10 fit domain-minus-other frequency differences per domain |Check same signed difference in test |40/40 positive; overlapping features possible, no multiple-test significance claim |
| Lexical comparator |Decode same256 tokens; fit-only unigram TF-IDF vocabulary; cosine class centroid |Same test records |91.80% [89.45%,93.95%]; no beyond-lexical advantage established |

Frequency labels mean selection with value>0, not just top-k inclusion. All observed tokens have32 positive selected features; total count is fixed by architecture. Mean activation amplitude, effective feature count and native input RMS are separately reported in `activation_statistics.csv`. No feature IDs were assigned guessed semantic names.

`analysis_contract.json` was written before extraction. `scripts/analyze.py` computes all three predeclared summaries and controls without best-feature/model selection. Accuracy uncertainty resamples test records within each of8 subfields500 times and is conditional on the fixed fit centroids. It excludes fit/checkpoint/paper/source uncertainty. The distance-gap percentile range[0.230017,0.252404] is below its plug-in0.261804 because the high-dimensional absolute-distance estimator is biased under resampling: the procedure adds sampling variation to same-domain profiles. This range is not a calibrated population confidence interval and is not used as one in the Summary. Original output is preserved; `statistical_audit.json` clarifies the legacy field name `gap_interval95`. TV point effects and heldout-label evidence are reported separately. No threshold or data was changed to improve outcomes.

## Interpretation and next decision

Direct result: domain profiles replicate and identify domain on heldout records. Allowed interpretation: fixed sidecar activation carries stable domain-associated information on these natural-text panels. Not established: pure semantic content, independence from lexical/style cues, feature-level semantic meaning, useful intervention/routing, or prediction of shared-update conflict. Strong classification is compatible with the earlier weak answer-letter results because representation discrimination and supervised knowledge answering are different measurements.

One AI-proposed next decision: whether to measure actual cross-group update consequences on the same natural-text units and test incremental prediction beyond lexical features. This suggestion is not an additional execution or an approved scientific transition.

## Artifact and audit map

All output files, exact source inputs and SHA256 identities: [artifact manifest](/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation/artifact_manifest.json). Primary arrays: `activations.npz` with indices/values/native RMS and ordered sample IDs. Selected source records and token identities: `selected.jsonl`. Analysis: `results.json`, `cross_split_distances.csv`, `domain_profiles.npz`, `confusion.csv`, `activation_statistics.csv`, `fit_selected_features_replication.csv`, `label_permutation_control.json`. Statistical qualification: `statistical_audit.json`; result was independently reconstructed from saved profiles and confusion counts. No changes to the previous frozen training protocol, its results, Focus or Anchor were made.

## Requested direct visual evidence

The researcher asked to present domain activation distributions directly, separately from domain prediction. `scripts/plot_distributions.py` reads the saved `analysis/domain_profiles.npz` and fit-selected feature table. `figure_manifest.json` records generating code, selection rule, every evidence/reading-copy path and SHA256 digest. Evidence copies live under the execution root `figures/`; date-local reading copies live under `daily_research_reports/0925/figures/`. Summary links only the date-local copies.

Frequency heatmap: fixed0–100% color scale,20 selected rows from19 unique features; a unique-feature assertion initially failed because feature36 is enriched for both computing and biology relative to the other-domain mean. The rendering now deliberately retains both group entries and labels this overlap; no feature or result was discarded. Fit selection only; test values are shown unchanged. Neither feature exclusivity nor semantic meaning is inferred.

Distance heatmap: uses all30,000 normalized frequency dimensions, fixed0–0.6 scale, explicit matrix values. Diagonal versus off-diagonal assesses replication without classification. No PCA/t-SNE selection, new inference or retraining. The visual sources and all frozen numeric conclusions remain unchanged.
