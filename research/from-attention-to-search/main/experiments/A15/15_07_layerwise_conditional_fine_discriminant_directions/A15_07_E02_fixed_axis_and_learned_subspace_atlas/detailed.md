# A15_07_E02 Detailed Evidence Record

## 1. Registered Question and Verdict

Question: at Qwen3-8B blocks 24 and 28, which frozen spectrum, axes, and minimum
subspace dimension stably carry each domain's eight-way fine-class function on
unseen expressions, and which function-qualified components are shared or
domain-specific?

Registered global result: `MIXED_OR_INSUFFICIENT` at both blocks. All 16
domain-layer outcomes are `INSUFFICIENT` under the complete compact-atlas rule.
The negative Router-relevant statement is firmer: no learned rank at most four
and no fixed-basis condition qualifies.

The [Protocol](protocol.md) was approved and frozen before C5 activations.

## 2. Frozen Objects

- model: `/data/share/Qwen3-8B`, frozen, evaluation mode;
- blocks: 24 and 28;
- object: native same-token attention update after subtracting the TRAIN-linear
  component predictable from the old state, denoted \(R_U\);
- hierarchy: eight domains, eight fine classes per domain;
- construction/development: exact E03 rows and states;
- C5: 1,920 newly expressed confirmation rows, 30 per domain-by-class cell;
- fixed rulers: local MLP parameter response, across-layer mean MLP response,
  and frozen activation PCA top-500;
- learned comparison: seven-dimensional Helmert output contrasts with requested
  input ranks 1, 2, 4, and 7.

The Helmert contrast refit prevents floating-point leakage into a redundant
eighth class-output coordinate. Rank seven is the full independent contrast
ceiling, not a low-rank success.

## 3. C5 Construction and Identity

C5 reused the six registered source propositions per fine class but changed
all expression templates and proposition orderings. The sealed audit reports:

| Guard | Result |
| --- | ---: |
| Rows | 1,920 |
| Balanced cells | 64 / 64 |
| Rows per cell | 30 |
| Normalized-text overlap with old data | 0 |
| Template-ID overlap | 0 |
| Combination-ID overlap | 0 |
| Record-ID overlap | 0 |
| Explicit-label leaks | 0 |

Metadata SHA-256:
`17619aa07e1b41f7d3ec36decf532f3a162240ca3f45e5925c574912a2d6e682`.

The 16-row smoke and 1,920-row formal extraction both passed. For both blocks,
replay maximum error, update reconstruction relative error, native MLP-input
relative error, and output-projection relative error were exactly 0 in the
recorded identity receipt. Formal extraction elapsed time was 65.46 seconds.

## 4. Methods

### 4.1 Fixed-axis score

For each domain and each frozen basis axis \(v_j\):

\[
s_j=\frac{v_j^\top Bv_j}{v_j^\top Wv_j+\rho},
\qquad
\rho=10^{-2}\frac{\operatorname{tr}(W)}{4096}.
\]

\(B\) is between-fine-class mean variation and \(W\) is mean within-class
expression variation. The score was recomputed at \(10\rho\). Selected
coordinates were TRAIN-standardized, then used by a ridge correction head.
Development chose the smallest \(k\in\{1,2,4,8,16,32,64\}\) reaching 90% of
full-\(R_U\) gain.

Controls were the first \(k\) spectral axes, 64 same-size random axis sets, 64
end-to-end within-domain label permutations, duplicate old-state access, and 64
within-domain mismatches.

### 4.2 Freely learned space

Reduced-rank ridge regression mapped standardized \(R_U\) to the residual
seven-dimensional class-contrast target after a five-fold out-of-fold old-state
classifier. Development selected among ranks 1, 2, 4, and 7. Sixty-four label
permutations supplied the functional null.

For spectral localization, the learned coefficient's input modes were mapped
back to native coordinates and orthonormalized. Band energy was
\(\lVert V_b^\top Q\rVert_F^2/r\).

### 4.3 Uncertainty

The analysis used 2,000 paired resamples within each domain-by-fine-class cell.
Max-statistic intervals were computed separately for admission, fixed
retention, fixed control excess, learned retention, and learned control excess.
Ratios with nonpositive full-gain denominators were not clipped.

## 5. Domain-Layer Admission

| Block | Domain | Full gain | Admission margin | Simultaneous LCB | Status |
| --- | --- | ---: | ---: | ---: | --- |
| 24 | mathematics | 0.02295 | -0.00255 | -0.02811 | unresolved |
| 24 | physics | 0.17029 | 0.10380 | 0.07824 | pass |
| 24 | chemistry | 0.12735 | 0.09124 | 0.06568 | pass |
| 24 | biology | 0.12833 | 0.05402 | 0.02846 | pass |
| 24 | computer science | 0.16621 | 0.13977 | 0.11421 | pass |
| 24 | economics | 0.11360 | 0.07755 | 0.05199 | pass |
| 24 | medicine | 0.21598 | 0.18690 | 0.16133 | pass |
| 24 | linguistics | 0.09194 | 0.04937 | 0.02381 | pass |
| 28 | mathematics | 0.14686 | 0.11575 | 0.09019 | pass |
| 28 | physics | 0.05820 | 0.03608 | 0.01052 | pass |
| 28 | chemistry | 0.08808 | 0.06134 | 0.03577 | pass |
| 28 | biology | 0.08963 | 0.04829 | 0.02273 | pass |
| 28 | computer science | 0.10030 | 0.07467 | 0.04911 | pass |
| 28 | economics | 0.11742 | 0.08459 | 0.05902 | pass |
| 28 | medicine | 0.16235 | 0.07114 | 0.04557 | pass |
| 28 | linguistics | 0.09063 | 0.06379 | 0.03822 | pass |

Unit is nats/example after equal fine-class aggregation.

## 6. Compactness and Fixed-Basis Result

Every freely learned task selected rank seven. For the 15 admitted pairs,
rank-seven C5 point retention is 0.991--1.009 and learned gain minus permutation
q95 has a simultaneous LCB between 0.01651 and 0.17814. Simultaneous retention
LCBs are 0.76497--0.78345, below 0.80. Block-24 mathematics has point retention
0.84575 but no full-access admission and negative permutation excess.

No fixed basis qualifies. Most development crossings require 32--64 axes or do
not occur by 64. The apparent block-28 compact candidates fail either the strict
point boundary or the simultaneous family:

- physics/common-response rank 8: retention 0.79958, excess 0.01608,
  stressed retention 0.79958, axis-set Jaccard 1.00;
- medicine/local-response rank 16: retention 0.830996, excess 0.02268,
  stressed retention 0.80453, stressed excess 0.01838, Jaccard 0.882.

Because no fixed basis passes, the registered fine-class fingerprint panels
correctly remain empty. Candidate fingerprints and axis ranks remain in
`selected_axes.csv` for audit only.

## 7. Spectral Location

Across all eight domains, the learned full-contrast spaces show the same band
ordering. The final one-sixteenth of both parameter-response spectra dominates:

| Block | Basis | Tail mean | Domain range | Haar q95 range | Domains above q95 |
| --- | --- | ---: | --- | --- | ---: |
| 24 | local parameter | 0.24607 | 0.2362--0.2642 | 0.06573--0.06606 | 8/8 |
| 24 | common response | 0.26952 | 0.2578--0.2949 | 0.06568--0.06606 | 8/8 |
| 28 | local parameter | 0.41075 | 0.4026--0.4234 | 0.06571--0.06598 | 8/8 |
| 28 | common response | 0.43501 | 0.4210--0.4455 | 0.06565--0.06604 | 8/8 |

The activation basis identifies only 500 directions. The unresolved complement
contains 0.7476--0.7549 of block-24 learned energy and 0.6161--0.6264 of
block-28 energy. Inside top 500, the first 1/8 band is largest, with means
0.1348 and 0.2645. Therefore “outside top 500” is justified, but no finer PCA
tail rank is identified.

## 8. Cross-Domain and Cross-Layer Geometry

The Amendment-001 completion used construction/development rows only and no C5
row for fit or selection. Within-layer cross-domain rank-seven overlap is:

| Block | Mean | Median | Range | Haar q95 | Pairs above q95 |
| --- | ---: | ---: | --- | ---: | ---: |
| 24 | 0.15217 | 0.15177 | 0.14858--0.15865 | 0.00230 | 28/28 |
| 28 | 0.29702 | 0.29746 | 0.29069--0.30490 | 0.00230 | 28/28 |

Same-domain cross-layer overlap is 0.14747--0.15104 and exceeds the same q95 for
8/8 domains. This is projector geometry only. No shared learned component was
held-out tested, so “shared functional direction” remains unresolved.

## 9. Figure Audit

1. `figure_1_functional_dimension_curves`: all 16 panels, four methods, ranks,
   development-selected markers, and 0.80 boundary match
   `functional_curves.csv`.
2. `figure_2_direction_and_spectral_band_atlas`: the six curve panels and six
   individual curve figures match `learned_spectral_energy.csv`. Thin lines are
   domains, the thick line is their mean, block 24 is light and block 28 dark,
   and the activation-PCA complement is disconnected because it has no internal
   rank resolution. No fixed-axis semantic marker appears because no basis
   qualifies.
3. `figure_3_overlap_and_fine_class_fingerprint`: top panels match
   `learned_subspace_overlap.csv`; bottom panels explicitly show that no fixed
   basis passed and therefore no semantic fingerprint is claimable.

Both PNG and PDF variants were rendered and visually inspected.

## 10. Deviations and Mechanical Incidents

The primary analysis reports no scientific deviation. Amendment 001 completes
the Protocol-registered learned-space overlap table that the initial writer
omitted. Its first attempt stopped before output because a frozen CPU state was
multiplied by a CUDA input. A regression test reproduced the device mismatch;
the single fix moves the immutable coefficient/intercept to the input device.
The targeted and full local tests passed. Amendment 002 only renders the
completed table and improves Figure-1 spacing. Amendment 003 replaces the six
spectral heatmap panels with curves over the same frozen energy table and adds
six individual PNG/PDF curve figures. It changes no scientific result or rule.

## 11. Artifact Map

### Canonical

- `protocol.md`
- `summary.md`
- `detailed.md`
- `detailed_cn.md`
- `meeting_sync_cn.md`
- `tables/domain_layer_atlas.csv`
- `tables/functional_curves.csv`
- `tables/selected_axes.csv`
- `tables/learned_spectral_energy.csv`
- `tables/learned_subspace_overlap.csv`
- `figures/figure_1_functional_dimension_curves.{png,pdf}`
- `figures/figure_2_direction_and_spectral_band_atlas.{png,pdf}`
- `figures/figure_2a_local_parameter_block24_curve.{png,pdf}`
- `figures/figure_2b_local_parameter_block28_curve.{png,pdf}`
- `figures/figure_2c_mean_response_block24_curve.{png,pdf}`
- `figures/figure_2d_mean_response_block28_curve.{png,pdf}`
- `figures/figure_2e_activation_pca_block24_curve.{png,pdf}`
- `figures/figure_2f_activation_pca_block28_curve.{png,pdf}`
- `figures/figure_3_overlap_and_fine_class_fingerprint.{png,pdf}`

### Worker

`/data/250010109/MoE_Router/experiments/20260820_a15_07_e02_fixed_axis_low_rank_atlas/`

Key worker receipts:

- `data_v1/data_manifest.json`
- `frozen/freeze.json`
- `frozen/amendment_001.md`
- `frozen/amendment_002.md`
- `frozen/amendment_003.md`
- `runs/smoke-20260821T/extraction/extraction_manifest.json`
- `runs/formal-20260821T/extraction/extraction_manifest.json`
- `runs/formal-20260821T/analysis/result_manifest.json`
- `runs/formal-20260821T/analysis/tables/learned_subspace_overlap_receipt.json`

## 12. Cannot Claim and Next Decision

Cannot claim: compact domain directions, trustworthy individual-axis semantics,
function-qualified shared/specific components, Router utility, expert
specialization, native causal use, new knowledge, or transfer.

Exactly one next decision: the researcher confirms or corrects the result
boundary “do not modify the Router proxy from this atlas.” No follow-on Router
experiment is promoted automatically.
