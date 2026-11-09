# Detailed: A15_08_09_E02 Qwen3-30B-A3B All-Layer Gain And Preservation

Primary Anchor: [A15_08_09](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)  
Result eligibility: `COMPUTATION_COMPLETE_EXTERNAL_H1_GUARD_UNRESOLVED`

## 0. Conclusion First

- Computational protocol completeness: `PASS`; the formal completion audit passes every artifact and semantic check.
- H0 all-layer localization: `Pass`; 31 of 48 layers have positive familywise simultaneous lower bounds.
- Maximum controlled gain: block 39, 0.10994 nats/example [0.09872, 0.12080].
- Frozen confirmation layers: block 48 primary and block 38 replication, selected without TEST labels.
- Numerical confirmation: block 48 H2 `Fail`, H3 `Fail`; block 38 H2 `Pass`, H3 `Fail`.
- Conditional projection: H4 `SKIPPED_H3_NOT_PASS`.
- External H1: `Insufficient`, because the existing 64-row independent human semantic review remains unresolved.
- Main interpretation: \(R_U\) contributes conditional label information beyond \(X\), but it is not a stable standalone positive-margin Router representation.

Worker root: `/data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation`  
Formal run root: `runs/e02-all-layer-full-20260824T014000Z`  
Formal ACP job: `pt-bo87sah1`

## 1. Frozen Objects And Model Identity

At the final token of the common `Answer:` suffix for block \(\ell\),

\[
X_\ell=N_\ell(h_\ell),\qquad
U_\ell=N_\ell(h_\ell+a_\ell)-N_\ell(h_\ell),
\]

\[
R_{U,\ell}=U_\ell-(X_\ell\widehat B_\ell+\widehat b_\ell).
\]

- Model: `/data/share/Qwen3-30B-A3B`, 48 blocks, hidden width 2,048, BF16 evaluation and FP32 saved arrays.
- Token: tokenizer suffix IDs `[16141, 25]`; decision token ID `25`; observed prompt lengths 119--302 tokens.
- Data: frozen binding-controlled 19,200 rows; 11,520 TRAIN, 2,560 DEV, 2,560 TEST-same, and 2,560 TEST-new.
- Main label: eight parent domains. The 64 fine labels appear only in descriptive functional-dimension diagnostics.
- Model identity: config `2850ddb3...c2297`, index `df0d481e...b3c24`, tokenizer `aeb13307...2dae4`; all 16 checkpoint shards were hashed in the formal preflight.
- Resource: one `n6ls.iu.i40.4` worker, 4×NVIDIA H100 80 GB, quota type `RESERVED`, normal priority.

The TEST-label-redacted selection file contains exactly 19,200 rows and no TEST label fields. E02 reuses TEST panels already opened by E01, so it is a pre-registered successor on new all-layer observables, not a pristine new-dataset replication.

## 2. Data And H1 Boundary

E02 does not reconstruct or retune the dataset. It inherits the E01 v2 data identity and reruns the model representation and gate pipeline. The existing machine evidence remains:

- 19,200 unique rows over the frozen 8×8 taxonomy;
- no registered direct label leaks, split-isolation violations, normalized duplicates, or binding violations;
- raw-text unigram+bigram accuracy 0.1270 on TEST-same and 0.1195 on TEST-new;
- 64-row AI review: 52 `PASS`, 12 `PASS_WITH_NOTE`, zero class or arithmetic mismatch;
- independent human review not completed.

Thus all executable H1 guards pass, while overall H1 remains `Insufficient` because AI review is not human evidence.

## 3. Extraction And Residualization

Formal merged extraction:

- shape `[48, 19200, 2, 2048]` for objects `[X,U]`;
- merged SHA-256 `cba20c5e3eb484a82c03246f6471b8da1e1c1a40f29c7cde9a037a99fa8ea144`;
- four exact 4,800-row shards;
- exact partition, all-finite, and merged identity flags: `Pass`;
- every rank and layer passes replay, native-MLP-input, attention-output-projection, and \(U=Z-X\) reconstruction checks;
- all 48 architecture blocks executed, with zero skipped suffix blocks.

All 48 TRAIN residualizers were refit. DEV selected \(\lambda\) independently per layer from \(10^{-6}\) through \(10^2\); no standardized coordinate had zero TRAIN variance. The BF16 native-input tolerance repair from `1e-5` to `1e-3` is recorded as Protocol Amendment A01. In the eligible formal run all recorded identity errors are zero.

## 4. All-Layer H0 Localization

For each layer, the base ridge score uses \(X_\ell\). A second TRAIN-fitted ridge correction uses matched \(R_{U,\ell}\). Its DEV cross-entropy reduction is compared with a duplicate-\(X\) correction and the 95th percentile over 30 independently mismatched-\(R_U\) corrections:

\[
T_\ell=G^{\mathrm{true}}_\ell-
\max\left(G^{\mathrm{dupX}}_\ell,Q_{.95}\{G^{\mathrm{mis}}_{\ell,j}\}_{j=1}^{30}\right).
\]

The formal 2,000-draw bootstrap uses the maximum centered error across all 48 layers to produce a familywise simultaneous interval. H0-admitted layers are:

`12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 48`.

### 4.1 Decision-bearing layers

| Block | True gain | Duplicate-\(X\) gain | Mismatch q95 | Controlled excess [simultaneous 95% interval] | Standalone DEV BA | Standalone DEV margin \(Q_{.05}\) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 39 | 0.10990 | -0.00003 | -0.00260 | 0.10994 [0.09872, 0.12080] | 0.37383 | -0.54060 |
| 24 | 0.10241 | -0.00003 | -0.00242 | 0.10244 [0.09122, 0.11331] | 0.30078 | -0.60267 |
| 38 | 0.06438 | -0.00004 | -0.00286 | 0.06442 [0.05320, 0.07529] | 0.31016 | -0.53000 |
| 48 | 0.01364 | -0.00005 | -0.00342 | 0.01369 [0.00248, 0.02456] | 0.16563 | -0.52554 |

Block 39 is the exact maximum-gain layer. It is not the frozen H3 primary because the frozen selector first requires H0 admission, then ranks admitted layers by standalone DEV margin \(Q_{.05}\), balanced accuracy, and smaller layer index. Block 48 wins that H3-readiness ranking; block 38 is the best admitted candidate at least four blocks away. Block 1 has a less-negative standalone margin (-0.30395) but is not H0-admitted and therefore cannot enter the downstream selector.

The selector receipt reports `test_labels_present: false`, `fallback_used: false`, and minimum replication separation 4. Source hash: `636df2b0810da344967c9436f11a160a43f4720baeaa7ca7c6af919dc6b16ca7`.

## 5. Full-Space H2/H3 Confirmation

All five-seed L2 multinomial-logistic fits converged. DEV selected the registered \(C\) grid, and TEST was evaluated only after the layer freeze.

| Block | Panel | Accuracy [95% CI] | Seed SD | Positive-margin fraction | Margin \(Q_{.05}\) [95% CI] |
| ---: | --- | --- | ---: | ---: | --- |
| 48 | TEST-same | 0.17125 [0.16484, 0.17813] | 0.000214 | 0.17148 at seed 24001 | -5.82955 [-5.95216, -5.74825] |
| 48 | TEST-new | 0.12969 [0.12445, 0.13500] | 0 | 0.12969 at seed 24001 | -11.19046 [-11.40759, -11.06038] |
| 38 | TEST-same | 0.31016 [0.30203, 0.31805] | 0 | 0.31016 | -3.52356 [-3.59236, -3.46685] |
| 38 | TEST-new | 0.23125 [0.22429, 0.23859] | approximately 0 | 0.23125 | -6.66276 [-6.79532, -6.54119] |

Block 48 H2 fails because the TEST-new accuracy lower bound 0.12445 does not strictly exceed chance 0.125. Block 38 H2 passes. Both H3 verdicts fail because the accuracy lower bounds are far below 0.90 and all four low-tail-margin intervals are negative. Confidence-width and convergence guards are sufficient, so these are scientific failures, not `Insufficient` outcomes.

### 5.1 Controls

- Permuted-label aggregate intervals contain chance on both panels at both layers; maximum individual absolute chance deviation is 0.01289.
- Identity-projection relative error is zero at both layers.
- Common-offset pairwise relative errors are \(4.21\times10^{-17}\) at block 48 and \(4.24\times10^{-17}\) at block 38.
- All selected and permutation fits converge.

## 6. Conditional H4 State

The projection artifact is:

```json
{"h3":"Fail","primary_layer":48,"schema":"a15_08_09_projection_scan_v1","status":"SKIPPED_H3_NOT_PASS"}
```

This is the required terminal state. H4 normalized margin retention divides by a positive full-space low-tail margin whose existence must first be established. The primary margin is negative, so a dimension scan would be mathematically uninterpretable under the frozen theorem-to-experiment contract.

## 7. Descriptive Diagnostics

### 7.1 Exact full-space distance geometry

Each TEST panel contains 2,560 rows and 3,275,520 unordered pairs: 408,320 within-parent and 2,867,200 between-parent. No pair sampling is used in the final result.

| Block | Panel | Extreme \(D_{out}/D_{in}\) | Robust \(Q_{.05}(D_{out})/Q_{.95}(D_{in})\) |
| ---: | --- | ---: | ---: |
| 48 | same | 0.3321 | 0.7026 |
| 48 | new | 0.2027 | 0.5315 |
| 38 | same | 0.2314 | 0.5832 |
| 38 | new | 0.2205 | 0.5357 |

Every ratio is below one, so neither an extreme nor robust Euclidean parent-cluster gap exists at the selected layers. This agrees with H3 but cannot replace it.

### 7.2 Supervised orthogonal fine-label dimension

The final diagnostic learns \(W_q=P_qA_q\) on TRAIN with \(P_q^TP_q=I\), uses DEV-only early stopping, and evaluates ranks 1--512 on TEST for five seeds. The registered \(r_{90}\) is 64 at both blocks. Full 64-way accuracy at seed 24001 is 0.05547/0.03281 at block 48 and 0.15742/0.08750 at block 38 on TEST-same/new, against chance 0.015625. Thus \(r_{90}\) compresses a weak supervised readout; it is not geometric rank or expert specialization.

### 7.3 Uniformity and coordinate eligibility

| Block | Coherence \(\mu\) | Haar mean [95% interval] | Entropy | TRAIN theorem-required \(m\) | Coordinate state |
| ---: | ---: | --- | ---: | ---: | --- |
| 48 | 2.0435 | 1.7121 [1.5895, 1.9184] | 0.9888 | 83,892 | `SKIPPED_TRAIN_COHERENCE_BOUND` |
| 38 | 3.5639 | 1.7058 [1.5743, 1.9100] | 0.9534 | 114,975 | `SKIPPED_TRAIN_COHERENCE_BOUND` |

Block 48 is much more diffuse than historical E01 block 24, but is still measurably above the same-rank Haar coherence range. More importantly, the TRAIN difference-vector sufficient bounds exceed the registered maximum 1,024 by two orders of magnitude. These facts govern only random spectral-coordinate sampling, not dense Gaussian projection.

## 8. Execution Ledger

| Job | Role | Terminal state |
| --- | --- | --- |
| `pt-hilwjbo0` | first all-layer smoke under inherited `1e-5` BF16 native-input tolerance | `FAILED`; retained as ineligible engineering attempt |
| `pt-y34d399q` | amended all-layer 128-row smoke | `SUCCEEDED`; completion audit passed |
| `pt-bo87sah1` | formal 19,200-row all-layer extraction, H0, H2/H3, conditional H4, diagnostics, theory conformance, and figure | `SUCCEEDED`; reserved 4×H100 |

The formal job ran from 2026-08-24 01:39:16 UTC to 02:39:03 UTC on one reserved four-H100 worker. The post-result figure annotation repair (Protocol Amendment A02) only rerendered frozen JSON/CSV and reran the completion audit; no numerical artifact or verdict changed.

## 9. Verification And Completeness

- Fresh implementation suite before the formal run: `51 passed`.
- Successful smoke semantic audit: all 48 layers, TEST-label absence, freeze consistency, selected blocks, and projection terminal state pass.
- Formal `completion_audit.json`: every required artifact exists; all seven semantic checks pass.
- Post-annotation rerender: completion audit passes again.
- Formal ACP state: `SUCCEEDED`.

The only non-computational unresolved item is the independent human H1 review. It does not alter the already frozen numerical H0/H2/H3/H4 branch but prevents labeling the overall result fully sufficient.

## 10. Artifact Map

| Artifact | Purpose | Status |
| --- | --- | --- |
| [protocol.md](protocol.md) | frozen E02 contract and amendments | Complete |
| [tables/layer_scan.csv](tables/layer_scan.csv) | curated 48-layer metrics and simultaneous intervals | Complete |
| [tables/layer_freeze.json](tables/layer_freeze.json) | immutable TEST-blind selector receipt | Complete |
| [figures/qwen30b_ru_layer_gain_curve.png](figures/qwen30b_ru_layer_gain_curve.png) | audited primary result figure | Complete |
| Worker `.../preflight.json` | GPU/model hashes | Complete |
| Worker `.../extraction/manifest.json` | 48-layer extraction identity and merge | Complete |
| Worker `.../residualizer/manifest.json` | all residualizer choices and hashes | Complete |
| Worker `.../full_space_probe/result.json` | H2/H3 and controls | Complete |
| Worker `.../projection_scan/result.json` | conditional H4 terminal state | Complete |
| Worker `.../diagnostics/result.json` | functional rank, uniformity, coordinate eligibility | Complete |
| Worker `.../theory_conformance/result.json` | exact pair geometry and learned orthogonal rank | Complete |
| Worker `.../completion_audit.json` | formal completeness receipt | Pass |
