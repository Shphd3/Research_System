---
experiment_id: A15_02_07_E01_matched_taxonomy_full
record_type: full_result_detailed
status: COMPLETE
typed_outcome: insufficient_mixed
human_closed_book_judgment: confirmed_2026-08-09
---

# Detailed Result Record: Matched Taxonomy 10-Layer Run

## 1. Scope And Evidence Boundary

This record covers the approved E02 TAX full run, its registered H1/H2 analysis, the required ten-layer figures, and evidence lineage. TAX and COMP were executed in one two-GPU worker run but were analyzed and adjudicated independently. The result is eligible because all E02 mandatory guards passed.

The researcher supplied the closed-book judgment on 2026-08-09. The record below verifies it against the frozen Protocol and eligible evidence without strengthening it.

## 2. Frozen Sources

| Object | Frozen identity |
| --- | --- |
| Protocol | `protocol.md`, preflight SHA-256 `9519f53b90969e73bd1bd77f6ceb9360f1c154fbc26973aef4061503f1db615e` |
| Model | frozen local `/data/share/Qwen3-8B` |
| TAX data | SHA-256 `ce91dbbd3c5071e17beeccf0d86a280dc8a3e48e0fdbf2178868da45eea18af4` |
| Parameter bases | A15_02_06 native input-Gram bases for layers 1/5/9/13/17/21/25/29/33/36; all ten expected hashes matched |
| Preflight | SHA-256 `2942a75bd4678ce79c94efcb1a9880232ba0f55f2cb07566e4049c95365820b4` |
| Protocol freeze | SHA-256 `e63ad894fa3f58e880ab96cc83c56bb5fe7cfb715b5186e5fb48ab2679750fd8` |

The local rank in every layer is descending eigenvalue order of that layer's own \(W_{gate}^{\top}W_{gate}+W_{up}^{\top}W_{up}\). Rank equality across layers is not vector identity.

## 3. Actual Data And Comparison

- 1,920 texts: 64 leaves × 10 TRAIN + 10 DEVELOPMENT + 10 CONFIRMATION expressions.
- Eight simple 8-way tasks: one selected leaf represents each of eight parents; Latin-square rotations use every leaf once across tasks.
- Eight complex 8-way tasks: eight leaves are classified within each parent.
- Both conditions therefore use exactly eight labels, one leaf per label, 10 examples per label and split, the same prompt endpoint, and the same unbiased 8-class center-variance estimator.
- TRAIN fits ridge readouts, DEVELOPMENT selects regularization, and CONFIRMATION supplies the registered result. Tasks are the eight paired bootstrap units.

This construction removes the earlier systematic difference between a pooled parent center and a single-leaf center. It does not equate semantic distance or empirical difficulty between the natural labels.

## 4. Runtime And Implementation

- Host: `app-527825a6c39545639c7c70a32677976f-5cd6cd4747-lbzmd`.
- Environment: Python 3.10.12, PyTorch `2.3.0a0+6ddf5cf85e.nv24.04`, CUDA 12.4, two NVIDIA H100 80GB.
- TAX forward: GPU 0, batch size 16, bfloat16 SDPA, no gradients; extraction elapsed 90.22 s.
- Stored representations: \(n^{old}\), exact \(\Delta n\), and its 4,096-dimensional parameter-basis projection for all ten layers.
- Analysis: FP64 class-center covariance and deterministic dual ridge; 2,000 paired bootstrap resamples.
- Final and post-ledger tests: 4/4 passed. No confirmation value selected a prompt, ridge value, layer, smoothing window, or threshold.

Worker root:

`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_10_e02_e03_tax_comp_10layer_full/`

Full run:

`runs/a15-01-10-e02-e03-full-20260808T-final/`

## 5. Guard Ledger

| Guard | Direct value | Threshold | Status |
| --- | ---: | ---: | --- |
| Same-run repeated-batch replay | maximum absolute error 0 | exactly 0 | Pass |
| Direct hook-site identity, layers 1/21/36 | maximum relative error 0 | \(<10^{-5}\) | Pass |
| Projection reconstruction | maximum relative error \(2.641\times10^{-6}\) | \(<10^{-4}\) | Pass |
| Augmented readout information, simple | mean `Disc` 0.5963 nats/example | \(>0.1\) | Pass |
| Augmented readout information, complex | mean `Disc` 0.4876 nats/example | \(>0.1\) | Pass |
| Schema/task/split balance | exact | exact | Pass |
| Finite/nonnegative curves and normalized sums | exact | required | Pass |
| Required figures and machine tables | present and visually audited | required | Pass |

The same-run replay replaces the failed E01 cross-hardware cache oracle. It verifies reproducibility on this execution surface but does not establish bitwise equivalence to the old 5090 cache.

## 6. H1: Direction-Variance Location

\(R_\ell>0\) means that the normalized complex curve has a later centroid than the normalized simple curve inside that layer's local rank order. Raw traces are total between-class variance and are not normalized.

| Layer | Raw trace simple | Raw trace complex | \(R_\ell\) |
| ---: | ---: | ---: | ---: |
| 1 | 0.088759 | 0.046528 | +0.030639 |
| 5 | 0.883304 | 0.488224 | -0.009213 |
| 9 | 0.567086 | 0.237571 | +0.010588 |
| 13 | 0.886719 | 0.454824 | +0.007277 |
| 17 | 0.677210 | 0.375250 | -0.000695 |
| 21 | 1.203284 | 0.744088 | -0.003179 |
| 25 | 7.472258 | 3.326616 | +0.036806 |
| 29 | 1.399818 | 0.767661 | +0.005898 |
| 33 | 2.800610 | 2.155630 | +0.002085 |
| 36 | 5.188564 | 2.794607 | -0.006195 |

Registered statistics:

- CONFIRMATION \(T_{rank}=-0.0046895\).
- Paired-bootstrap 95% interval: \([-0.0121824,0.0092953]\).
- DEVELOPMENT \(T_{rank}=-0.0063649\); TRAIN \(-0.0051062\).
- Eight CONFIRMATION task-level early/late diagnostics: `[-0.011851, -0.006210, -0.002011, +0.013160, +0.005541, +0.018122, -0.002080, -0.010910]`.
- Typed H1 status: `insufficient_precision_or_split`.

The raw complex trace is lower than the simple trace at all ten layers. The normalized centroid difference changes sign, so the evidence does not show an approximately monotonic later shift.

## 7. H2: Conditional Novelty And Update Readability

`CIG` is \(CE_{base}-CE_{base+\Delta n}\) on untouched confirmation data. Positive values mean the fitted update correction improves the frozen old-state readout. `Disc($\Delta n$)` is the update-only supporting readout.

| Layer | CIG simple | CIG complex | Complex−simple \(G_\ell\) | \(Disc(\Delta n)\) simple | \(Disc(\Delta n)\) complex |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | +0.696158 | +0.653485 | -0.042673 | +0.696158 | +0.653485 |
| 5 | +0.00000064 | +0.00000084 | +0.00000020 | +0.554735 | +0.439541 |
| 9 | +0.00000091 | +0.00000193 | +0.00000103 | +0.606349 | +0.470178 |
| 13 | +0.00000091 | +0.00000116 | +0.00000025 | +0.573519 | +0.441190 |
| 17 | +0.00000066 | +0.00000099 | +0.00000033 | +0.472215 | +0.346994 |
| 21 | +0.00000073 | +0.00000078 | +0.00000004 | +0.421682 | +0.298206 |
| 25 | +0.00000119 | +0.00000183 | +0.00000064 | +0.568028 | +0.490166 |
| 29 | +0.00000052 | +0.00000061 | +0.00000009 | +0.567021 | +0.482630 |
| 33 | +0.00006903 | +0.00000342 | -0.00006561 | +0.530143 | +0.461298 |
| 36 | +0.00036440 | +0.00010986 | -0.00025453 | +0.635001 | +0.564360 |

Registered statistics:

- \(T_{CIG}=-1.0863\times10^{-7}\) nats/example.
- Paired-bootstrap 95% interval: \([-4.2971\times10^{-7},5.9153\times10^{-7}]\).
- Eight task-level early/late diagnostics: `[+3.02e-7, +1.09e-6, +2.14e-7, -1.02e-6, -1.70e-6, +1.88e-7, +9.54e-7, +1.94e-7]`.
- Typed H2 status: `insufficient_precision`.

Layer 1 is special: before the first attention write, the common readout-token old state has no task-specific context, so update-only readability and conditional gain coincide. From layer 5 onward, \(\Delta n\) remains linearly readable while its additional gain beyond \(n^{old}\) is nearly zero. This is compatible with linear redundancy, but nonlinear conditional information remains untested.

## 8. Bootstrap And Evidence Completeness

H1 resamples the eight paired task curves before recomputing aggregate centroids; H2 resamples the eight paired task gain curves. The machine result now stores, for all TRAIN/DEVELOPMENT/CONFIRMATION splits, every task-level H1 simple and complex centroid, rank difference, and early/late diagnostic. It also stores every task/layer H2 base, increment, and delta-only ridge grid and every task conditional gain. This ledger addition was made after the first render from already computed frozen inputs; it did not change the estimator, aggregate values, figures, or verdict.

## 9. Visualization Audit

The central variance figure contains ten rows in shallow-to-deep order, raw variance on the left and normalized mass on the right. Each panel retains a thin exact 4,096-direction trace and overlays a centered 129-rank moving arithmetic mean.

Smoothing is applied before `log10` because the intended display object is local average variance. Smoothing log values would instead show a geometric mean and systematically downweight isolated high-variance directions. The window spans about 3.15% of the spectrum and changes no machine statistic. Shared within-family y-limits prevent per-layer rescaling from creating a false shape match.

The H2 panel uses a symmetric-log scale with a linear region of \(10^{-6}\) nats/example. This post-run display repair exposes the measured near-zero later gains without hiding the layer-1 magnitude. It preserves zero and sign and does not affect adjudication.

Curated PNG hashes:

- direction variance: `80b24db98fbdcec76b08806d7bacc73cf50bab654fab3310a0db29491b0fd487`;
- H1/H2 metrics: `3230c6c03330df8148ffb7756180aec74c3aa15cb9406e9cad0a020e9464f60a`.

### Post-hoc all-layer overlay and layer-block audit

![TAX ten-layer overlays and layer-block trends](figures/tax_10layer_overlay_and_block_trends.png)

Purpose: determine whether the fine curve becomes progressively more prominent, while separating a shared depth relocation from a fine-specific residual. All ten stored curves are overlaid on shared raw and normalized axes. Early 1/5/9, middle 13/17/21, late 25/29/33, and terminal 36 block medians are shown only as descriptive summaries.

Observed result: simple and fine centroids both move later from early to terminal layers, but \(R_\ell\) is not block-ordered: `+0.0106, -0.0007, +0.0059, -0.0062`. The paired fine/simple raw-trace ratio is also stable rather than increasing: `0.5242, 0.5541, 0.5484, 0.5386`. Fine update-only readability is non-monotonic, and fine-specific conditional gain remains near zero until becoming negative at the terminal boundary.

Allowed conclusion: the ten-layer overlay supports a shared depth-dependent redistribution and rejects describing the present TAX evidence as progressively clearer fine-specific emergence. Limitation: these blocks and medians were requested after the registered result; layers are not independent replicates, so this view cannot replace the frozen bootstrap verdict.

Post-hoc figure SHA-256: `14618e988b0a364a0904aaed998c117c1f8d974764dd346f65ca4b3525e02d00`.

## 10. Artifact Map And Lineage

Canonical review surface:

- `protocol.md`: frozen approval contract;
- `summary.md`: conclusion-first result;
- `detailed.md`: this ledger;
- `figures/tax_10layer_direction_variance.{png,pdf}`;
- `figures/tax_10layer_h1_h2_metrics.{png,pdf}`.

Worker evidence under the full-run directory:

- `preflight.json`, `protocol_freeze.json`, `unit_tests.log`, `postledger_unit_tests.log`;
- `tax/extraction/layer_*.pt` and `tax/extraction/extraction_manifest.json` (SHA-256 `dae40b96d43c1c0135a3d5f78e963d810ed48711f7c103adca9b068fed2f0ca3`);
- `tax/analysis/tax_direction_variance_curves.{csv,npz}`; NPZ SHA-256 `e8a247ec3918ec7fdf2aaaeb541a713c75aa1597e2df976e83f962db6d3a5d63`;
- `tax/analysis/tax_full_result.json`, SHA-256 `063e1b069010f74a1bf3281bdb0133c294ece79aab6251ba9adbd7f92fd10aa5`;
- `tax/analysis/figure_contract.json`, SHA-256 `0a08fdae1edf927938d1fe861face07e3b14946c593df7e9910dca403b7b5d09`;
- `posthoc_layer_block_analysis/layer_block_summary.{csv,json}`: descriptive layer-block table; JSON SHA-256 `314659877674ad263d75250ce1261f61acd71ded7d8060c1110b2f925d857235`;
- `posthoc_layer_block_analysis/tax_10layer_overlay_and_block_trends.{png,pdf}`: all-layer overlay and block audit;
- `posthoc_layer_block_analysis/artifact_manifest.json`: post-hoc artifact hashes, SHA-256 `01d67255308afdc8dcba9b32dc50dc892232e3a532af9d839dbb29da377f6731`;
- `full_verdict.json`, SHA-256 `f3fd37ae34a5123a3775a0ed4486e205473789003c86a18dc0ca62bfa66c1e0c`;
- run `artifact_manifest.json`, SHA-256 `0f3a1bc16f6890b7e0a91ea088018766faa82084a7d05583ea99a36722746661`.

Raw tensors and complete machine tables stay in the worker area and were not promoted into `main/`.

## 11. Verdict, Rival, And Next Decision

- **Question:** Under a class-count-matched taxonomy, does conditional-fine information move relatively toward later local MLP-parameter ranks with depth and add linearly accessible information beyond the old MLP input?
- **Direct result:** No. \(T_{rank}=-0.004690\) with interval \([-0.012182,0.009295]\), and conditional information gain is \(-1.09\times10^{-7}\) nats/example with interval \([-4.30\times10^{-7},5.92\times10^{-7}]\). Both registered clauses are `insufficient`.
- **Updated judgment:** Matching covariance cardinality removes the old coarse/fine estimator mismatch but does not reveal a stable fine-specific rank relocation or conditionally new linear information. The retained observation is a target-common depthwise relocation of local-rank centroids.
- **Cannot claim:** TAX does not establish absence of nonlinear information, native MLP use, a functional tail, or Router utility; lower fine readability alone is not evidence for a nonlinear code.
- **Next decision:** Close A15_02_07 jointly with COMP and allow only one A15_04 fixed-bank geometry test of whether the shared relocation aligns with the cross-layer parameter tail beyond equal-rank random, head, and middle controls.

The strongest remaining TAX rival is that natural between-parent and within-parent labels differ in semantic geometry and linear-readout redundancy even after covariance cardinality is matched. No new Protocol or execution is approved by this record.
