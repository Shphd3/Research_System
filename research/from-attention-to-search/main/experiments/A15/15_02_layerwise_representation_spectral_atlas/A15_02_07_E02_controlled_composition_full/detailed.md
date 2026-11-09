---
experiment_id: A15_02_07_E02_controlled_composition_full
record_type: full_result_detailed
status: COMPLETE
typed_outcome: insufficient_mixed
human_closed_book_judgment: confirmed_2026-08-09
---

# Detailed Result Record: Controlled Composition 10-Layer Run

## 1. Scope And Evidence Boundary

This record covers the initial capability failure, the append-only data amendment, the successful capability retry, the approved E03 full run, registered H1/H2 analysis, and required COMP figures. COMP is adjudicated independently from TAX. All amended-data full-run guards passed, so the result is eligible.

The researcher supplied the closed-book judgment on 2026-08-09. The record below verifies it against the frozen Protocol and eligible evidence without strengthening it.

## 2. Frozen Sources And Amendment Lineage

| Object | Frozen identity |
| --- | --- |
| Final Protocol | `protocol.md`, preflight SHA-256 `0d2d2c31dc0438c524dfe790c77124bc7689973d51146221d78cd027814f2962` |
| Model | frozen local `/data/share/Qwen3-8B` |
| Initial COMP data | SHA-256 `341202eedccf635760aa43d2bd2936601258f29198d2881c3add59ad09e413b1` |
| Amended full-run data | SHA-256 `bd8f29581c502c157785609ff8e87c157734e3e4caf934abcd2ba95c6f68ac77` |
| Parameter bases | A15_02_06 native input-Gram bases for layers 1/5/9/13/17/21/25/29/33/36; all hashes matched |
| Full-run preflight | SHA-256 `2942a75bd4678ce79c94efcb1a9880232ba0f55f2cb07566e4049c95365820b4` |
| Protocol freeze | SHA-256 `e63ad894fa3f58e880ab96cc83c56bb5fe7cfb715b5186e5fb48ab2679750fd8` |

The initial prompts randomly interleaved all 16 rules. Capability smoke passed simple at 0.953125 but failed complex at 0.53125 against the 0.60 gate. Amendment A1 retained every map, class, target, episode, split, condition, and threshold, but placed sorted \(U\to V\) and \(V\to C\) rules in separate tables and added a label-free retrieval instruction. The amended capability smoke passed at 1.0 simple and 0.75 complex. No ten-layer extraction was run on the failed data.

## 3. Actual Data And Comparison

- 3,072 records: 3 splits × 64 independent map episodes × 8 targets × 2 conditions.
- Every paired simple/complex record shares the exact context and terminal code.
- Simple starts from the relevant \(V\) and retrieves one \(V\to C\) edge.
- Complex starts from the matched \(U\) and composes \(U\to V\to C\).
- Each condition has eight balanced classes. Eight registered replicate groups contain eight episodes per split and are the paired bootstrap units.
- TRAIN fits readouts, DEVELOPMENT selects ridge strength, and CONFIRMATION supplies capability and the registered H1/H2 result.

The amendment removes rule-order disorder as a treatment-dependent nuisance. It does not make the task equivalent to natural-language composition or free generation.

## 4. Runtime And Stage Ledger

Environment: Python 3.10.12, PyTorch `2.3.0a0+6ddf5cf85e.nv24.04`, CUDA 12.4, two NVIDIA H100 80GB.

| Stage | Data / scope | Direct result | Eligibility |
| --- | --- | --- | --- |
| Capability preflight 0 | initial data; 8 episodes / 128 paired records | simple 0.953125, complex 0.53125 | Failed and retained; ineligible |
| Amendment A1 | table-order repair only | final data hash frozen | requires unchanged gate |
| Capability preflight 1 | amended data; 8 episodes / 128 records | simple 1.0, complex 0.75 | Passed |
| Full extraction | amended 3,072 records; ten layers; GPU 1; batch 8 | 112.43 s | eligible |
| Analysis | FP64 covariance; dual ridge; 2,000 paired bootstraps | complete | eligible |
| Tests | final and post-ledger | 4/4 passed | pass |
| Figure audit | COMP-only raw/normalized and H1/H2 figures | visually complete | pass |

The full-run restricted-choice accuracy was 0.990234 simple and 0.757812 complex on CONFIRMATION, 0.978516/0.837891 on DEVELOPMENT, and 0.962891/0.812500 on TRAIN.

## 5. Guard Ledger

| Guard | Direct value | Threshold | Status |
| --- | ---: | ---: | --- |
| Same-run repeated-batch replay | maximum absolute error 0 | exactly 0 | Pass |
| Direct hook-site identity, layers 1/21/36 | maximum relative error 0 | \(<10^{-5}\) | Pass |
| Projection reconstruction | maximum relative error \(2.651\times10^{-6}\) | \(<10^{-4}\) | Pass |
| Augmented `Disc`, simple | mean 0.2698 nats/example | \(>0.1\) | Pass |
| Augmented `Disc`, complex | mean 0.1199 nats/example | \(>0.1\) | Pass |
| Confirmation capability, simple | 0.9902 | \(\ge0.80\) | Pass |
| Confirmation capability, complex | 0.7578 | \(\ge0.60\) | Pass |
| Schema/balance/numerical checks | exact | required | Pass |
| Figures and complete machine ledgers | present and audited | required | Pass |

## 6. H1: Direction-Variance Location

| Layer | Raw trace simple | Raw trace complex | \(R_\ell\) |
| ---: | ---: | ---: | ---: |
| 1 | 0.00002453 | 0.00002416 | -0.002302 |
| 5 | 0.00379683 | 0.00308553 | -0.034750 |
| 9 | 0.00129655 | 0.00086124 | +0.008574 |
| 13 | 0.01029342 | 0.00430407 | +0.022419 |
| 17 | 0.02000020 | 0.01302869 | -0.002061 |
| 21 | 0.12806150 | 0.11026413 | -0.017378 |
| 25 | 22.709460 | 9.669526 | -0.000189 |
| 29 | 5.941326 | 1.434623 | -0.029128 |
| 33 | 10.147199 | 5.832275 | +0.000276 |
| 36 | 24.069465 | 12.292594 | +0.002071 |

Registered statistics:

- CONFIRMATION \(T_{rank}=+0.0021138\).
- Paired-bootstrap 95% interval: \([-0.0023843,0.0052256]\).
- DEVELOPMENT \(T_{rank}=-0.0036084\); TRAIN \(+0.0010528\).
- Eight CONFIRMATION replicate diagnostics: `[+0.006477, -0.002232, -0.001233, +0.000708, +0.004102, +0.008017, -0.007923, -0.009127]`.
- Typed H1 status: `insufficient_precision_or_split`.

The complex raw trace is lower at all ten layers. The normalized difference changes sign and DEVELOPMENT reverses the registered early/late contrast, so H1 does not pass despite the positive confirmation point estimate.

## 7. H2: Conditional Novelty And Update Readability

| Layer | CIG simple | CIG complex | Complex−simple \(G_\ell\) | \(Disc(\Delta n)\) simple | \(Disc(\Delta n)\) complex |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | -0.158778 | -0.195069 | -0.036292 | -0.158778 | -0.195069 |
| 5 | -0.198904 | -0.136712 | +0.062192 | -0.232335 | -0.200899 |
| 9 | -0.031284 | -0.046902 | -0.015617 | -0.038089 | -0.058497 |
| 13 | -0.022159 | -0.025004 | -0.002845 | -0.019516 | -0.016857 |
| 17 | -0.007395 | -0.006354 | +0.001041 | -0.003216 | -0.002585 |
| 21 | +0.002797 | -0.005089 | -0.007886 | +0.004760 | -0.005583 |
| 25 | +0.001814 | +0.080064 | +0.078250 | +0.943344 | +0.627891 |
| 29 | +0.000002 | +0.002417 | +0.002415 | +0.875675 | +0.650315 |
| 33 | +0.000199 | +0.003104 | +0.002906 | +0.778301 | +0.474382 |
| 36 | -0.000021 | +0.000319 | +0.000339 | +0.786415 | +0.580573 |

Registered statistics:

- \(T_{CIG}=+0.0185229\) nats/example.
- Paired-bootstrap 95% interval: \([-0.0504125,0.0810519]\).
- Eight replicate-level early/late diagnostics: `[+0.191400, +0.017551, -0.218547, +0.087726, +0.038275, +0.102148, -0.029219, -0.012953]`; five are positive and three negative.
- Typed H2 status: `insufficient_precision`.

The update-only readout changes sharply between layers 21 and 25, after which both simple and complex codes are readable from \(\Delta n\). The conditional correction also becomes positive for complex examples at layer 25, but its replicate effects are heterogeneous and the interval crosses zero. Negative early CIG means that the TRAIN/DEVELOPMENT-selected delta correction worsened untouched confirmation relative to the frozen base; it is a warning about readout variance or shift, not “negative information.”

## 8. Bootstrap And Evidence Completeness

H1 resamples the eight paired replicate curves before recomputing aggregate centroids. H2 resamples the paired replicate gain curves. The final result stores all split-specific H1 task centroids and differences, all task-level H2 ridge grids and confirmation losses, and all replicate/layer gains. The task ledger was added after the first render from existing frozen inputs. Aggregate metrics and verdicts were reproduced exactly.

The registered grouping has only eight inference units even though the dataset has 64 generated episodes per split. This is the immediate source of the broad H2 interval. Reinterpreting the already opened confirmation episodes as more post-hoc units would change the inference contract and is not used to rescue the current result.

## 9. Visualization Audit

The required direction figure contains ten shallow-to-deep rows, raw variance on the left and normalized mass on the right. Thin lines retain all exact direction ordinates. Thick lines use a centered 129-rank arithmetic mean on linear variance before `log10`, which exposes broad shape while preserving isolated directions in the background. The window is display-only and spans about 3.15% of the 4,096 ranks.

The H2 panel uses a symmetric-log scale with a \(10^{-6}\)-nat linear region. This is necessary because CIG spans negative values near \(-0.2\), positive values near \(0.08\), and near-zero values. The scale preserves sign and zero; no metric is log-transformed for analysis.

Curated PNG hashes:

- direction variance: `94bef378540531c18ec7910c1d9369d629bb584097fdd236b962d94cec4697b2`;
- H1/H2 metrics: `89ca90665927db2411e75f85ead5ebf6643d590c520f7882eb2b4308e0496a9c`.

### Post-hoc all-layer overlay and layer-block audit

![COMP ten-layer overlays and layer-block trends](figures/comp_10layer_overlay_and_block_trends.png)

Purpose: determine whether the composition effect is gradual or block-local while separating common depth relocation from complex-specific residuals. All ten stored curves share raw and normalized axes; early 1/5/9, middle 13/17/21, late 25/29/33, and terminal 36 medians are descriptive only.

Observed result: simple and complex rank centroids jump together in the late block, whereas their relative \(R\) medians remain near zero: `-0.0023, -0.0021, -0.0002, +0.0021`. Update-only readability changes from negative/near-zero to strongly positive in the late block; complex-specific conditional gain changes from negative to small positive, but the registered replicate interval still crosses zero.

Allowed conclusion: the visual supports a late-block formation/readability onset, not a gradual complex-specific parameter-rank shift. Limitation: this post-hoc block view cannot change the registered `insufficient_mixed` outcome or treat the selected layers as independent evidence.

Post-hoc figure SHA-256: `fd8962ff2cc9ee85d057512fa95f65d2ab71d969eff8f6f74f3dff16dcc60f32`.

## 10. Artifact Map And Lineage

Canonical review surface:

- `protocol.md`, including Amendment A1;
- `summary.md` and `detailed.md`;
- `figures/comp_10layer_direction_variance.{png,pdf}`;
- `figures/comp_10layer_h1_h2_metrics.{png,pdf}`.

Capability lineage:

- failed initial smoke: `runs/a15-01-10-e02-e03-capability-preflight-20260808/capability_smoke.json`;
- successful amended smoke: `runs/a15-01-10-e03-capability-preflight-r1-20260808/capability_smoke.json`.

Full-run worker evidence:

- `comp/extraction/layer_*.pt`, `restricted_choice_logits.pt`, and `extraction_manifest.json`, SHA-256 `04217aec6a5a6573490e93249ec1fad0f36794fd39869130a04c8c9ab49816e5`;
- `comp/analysis/comp_direction_variance_curves.{csv,npz}`; NPZ SHA-256 `57e803b3897c6a23282607cf52552dbdd13241d52d3632922249a16d25901e81`;
- `comp/analysis/comp_full_result.json`, SHA-256 `9e1394e12c71185dbf67dd8dcd7a356b27b31d114a807819c91023e70ceaa82d`;
- `comp/analysis/figure_contract.json`, SHA-256 `473a404b863d81f63cdd65dbddb453e62fdfaa13a5a344ffd2802b47c2dd656d`;
- `posthoc_layer_block_analysis/layer_block_summary.{csv,json}`: descriptive layer-block table; JSON SHA-256 `314659877674ad263d75250ce1261f61acd71ded7d8060c1110b2f925d857235`;
- `posthoc_layer_block_analysis/comp_10layer_overlay_and_block_trends.{png,pdf}`: all-layer overlay and block audit;
- `posthoc_layer_block_analysis/artifact_manifest.json`: post-hoc artifact hashes, SHA-256 `01d67255308afdc8dcba9b32dc50dc892232e3a532af9d839dbb29da377f6731`;
- `full_verdict.json`, SHA-256 `f3fd37ae34a5123a3775a0ed4486e205473789003c86a18dc0ca62bfa66c1e0c`;
- run `artifact_manifest.json`, SHA-256 `0f3a1bc16f6890b7e0a91ea088018766faa82084a7d05583ea99a36722746661`.

Raw tensors, logits, and complete task grids remain in the worker run and were not copied into the research mainline.

## 11. Verdict, Rival, And Next Decision

- **Question:** In a capability-passing one-edge versus two-edge composition task, does the complex target move relatively toward later local MLP-parameter ranks with depth and add conditionally new linear information?
- **Direct result:** Not established. \(T_{rank}=+0.002114\) with interval \([-0.002384,0.005226]\) and a DEVELOPMENT sign reversal; conditional information gain is \(+0.018523\) nats/example with interval \([-0.050412,0.081052]\). Both clauses are `insufficient`.
- **Updated judgment:** The late attention-induced update makes the terminal composition code readable, but neither a stable complex-specific rank relocation nor information linearly new beyond the old state is supported. Shared depthwise spectral-shape change remains the object worth explaining.
- **Cannot claim:** COMP does not establish gradual semantic refinement, conditional novelty, nonlinear coding, native MLP use, a functional tail, or Router utility.
- **Next decision:** Close A15_02_07 jointly with TAX and allow only one A15_04 fixed-bank geometry test of whether the shared relocation aligns with the cross-layer parameter tail beyond equal-rank random, head, and middle controls.

The strongest remaining rival is finite episode/readout variance: one negative replicate has a large H2 effect, the registered interval spans both signs, and H1 reverses on DEVELOPMENT. No new Protocol or execution is approved by this record.
