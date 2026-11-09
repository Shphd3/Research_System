# A15_08_E01 Layer-25 Conditional Innovation — Detailed Evidence Record

## 1. Evidence Status

- Frozen Protocol: [protocol.md](protocol.md), revision `A15_08_E01_v1`, with
  execution amendments A1--A2 and verdict-status clarification A3.
- Execution: one complete local full run on 2026-08-10.
- Mechanical registered label:
  `H2_INSUFFICIENT_H1_NOT_ADJUDICATED`.
- Post-result construct qualification:
  `PRIMARY_H2_INELIGIBLE_CONTROL_DESIGN`.
- H1' status: `NOT_ADJUDICATED`; its retention and null comparisons also fail
  an object/search-budget audit.
- Scientific use: metric-failure diagnosis and bounded readout observations
  only. E01 does not provide an H2/H1 verdict about layer-added information.

## 2. Frozen Inputs

| Object | Frozen value |
| --- | --- |
| model | `/data/share/Qwen3-8B`, 36 blocks, width 4,096 |
| site | block index 24 / reported layer 25, final `Answer:` token |
| old/new/update | \(X=N_{25}(h)\), \(Z=N_{25}(h+a)\), \(U=Z-X\) |
| data | 128 TRAIN / 64 DEVELOPMENT / 128 CONFIRMATION episodes; eight targets; paired simple/complex |
| generation seeds | 5101 / 5102 / 5103 |
| full data SHA-256 | `a1059be934aaa930a5664b3e93f9fa68a2d942d5b0a7ac6f653806e2ae4f7dec` |
| simple data SHA-256 | `23a76f2bba7c8a18759e0d50ad29741f3a0ba0ae6e51ab673199c7520c22fcd0` |
| complex data SHA-256 | `52a55ef415c31959bfccedef292675d2b89a0d425116461124bd5e2dd6aa5c5c` |
| bootstrap | 2,000 complete-episode draws, seed 5181 |
| random rank-two controls | 64, seeds 5200--5263 |
| TRAIN-label permutations | 64, seeds 5300--5363 |

The source generator, extractor, analyzer, metric helpers, and tests were hashed
before analysis in [code_hashes_before_analysis.txt](evidence/code_hashes_before_analysis.txt).

## 3. Execution History And Protocol Conformance

### 3.1 Preflight and data

The generated 5,120-record dataset passed exact count, ID, pair, split, episode,
and target-balance tests. Deterministic known-good, known-bad, redundant-readable,
covariance-identity, group-leakage, and helper tests passed before model
extraction.

The first smoke command failed before import because the default environment did
not expose `transformers`; Protocol amendment A1 records sourcing the verified
project dependency environment. Retry A1 then failed in `argparse` because the
command supplied a redundant unsupported `--condition` option; amendment A2
records removing it. Neither attempt loaded a model, read data, or exposed a
scientific value. Both failed logs remain in the worker.

The corrected smoke ran 16 episodes per split and condition. The complete full
run then extracted 2,560 rows per condition in parallel on two H100s.

### 3.2 Extraction guards

| Guard | Simple | Complex | Limit | State |
| --- | ---: | ---: | ---: | --- |
| confirmation restricted-choice accuracy | 0.991211 | 0.777344 | 0.80 / 0.60 | pass |
| same-run replay max absolute error | 0 | 0 | \(\le10^{-5}\) | pass |
| direct `o_proj` relative error | 0 | 0 | \(\le10^{-5}\) | pass |
| loaded \(Z-X-U\) relative error | 0 | 0 | \(\le10^{-6}\) | pass |

The simple and complex representation files have SHA-256
`db7aa6ab9e65f8f063871b8254878936349655627a186035176f8bde006c07f2`
and
`06382535c24b24d784c272f2c3d1080a9d0fc1242ab7793b5148d5658ea3e393`.

### 3.3 Selection freeze

The analyzer used TRAIN/DEVELOPMENT only to fit the common basis, old-state and
update readouts, four-fold episode residualizers, four \(\rho\) candidates, the
rank-two direction, and both 64-member null families. It then wrote and hashed
the frozen selection ledger as
`2dddc9bf938ce71560142118790fbd3e94815c7363009e11c21620820855b5ee`
before computing confirmation conditional losses.

Confirmation labels were visible before this freeze only for the preregistered
restricted-choice capability guard. They were not used for representation
centering, model/direction/rank/hyperparameter selection, or exclusions.

## 4. Common Coordinate And Exact Difference

Episode-centered TRAIN \(X\) and \(Z\) from both conditions were pooled in one
coordinate. Exact seven-dimensional episode contrasts compressed 4,096 centered
rows to 3,584 rows without changing covariance trace. An economy dual
eigendecomposition retained rank 3,584.

| Numerical quantity | Value | Limit | State |
| --- | ---: | ---: | --- |
| stored-basis orthogonality relative error | \(7.5278\times10^{-7}\) | \(10^{-5}\) | pass |
| solver-float64 orthogonality error | \(2.9251\times10^{-10}\) | descriptive | pass |
| trace reconstruction relative error | 0 at reported precision | \(10^{-4}\) | pass |
| covariance identity, simple | \(1.2877\times10^{-15}\) | \(10^{-5}\) | pass |
| covariance identity, complex | \(1.4061\times10^{-15}\) | \(10^{-5}\) | pass |

This establishes that all three visualized objects share one legitimate
coordinate and that \(U\) is the exact transition. It does not make \(U\) new
knowledge. The source table is
[common_basis_spectrum.csv](tables/common_basis_spectrum.csv), and the audited
display is [figure_common_basis.png](figures/figure_common_basis.png).

## 5. Direct Confirmation Results

### 5.1 Complex primary condition

| Quantity | Estimate | 95% interval |
| --- | ---: | ---: |
| old-only CE | 2.013558 | point estimate only |
| raw-\(U\) full CE | 1.352130 | point estimate only |
| cyclic-control CE | 1.325146 | point estimate only |
| \(Z\)-only CE | 1.327382 | point estimate only |
| rank-two CE | 1.787668 | point estimate only |
| raw-\(U\) gain \(G_{full}\) | +0.661428 | [0.646973, 0.675533] |
| cyclic gain \(G_{shuffle}\) | +0.688412 | [0.673629, 0.703148] |
| true minus cyclic \(T_{shuffle}\) | -0.026983 | [-0.030384, -0.023705] |
| same-dimensional state gain | +0.686176 | [0.672119, 0.700464] |
| rank-two gain \(G_2\) | +0.225890 | [0.215740, 0.235682] |
| \(D_{80}\) | -0.303253 | [-0.313918, -0.292715] |

The registered H2 conjunction requires positive lower bounds for both
\(G_{full}\) and \(T_{shuffle}\). Its arithmetic label is therefore H2
`INSUFFICIENT`, not Fail. H1' is gated off.

The 64 random rank-two gains ranged from 0.156097 to 0.211987 with empirical
q95 0.202879. The 64 TRAIN-label-permutation gains ranged from -0.026353 to
0.021623 with q95 0.018305. Although \(G_2\) exceeds both point q95 values, it
retains only 34.15% of raw-\(U\) gain and cannot be adjudicated because H2 did not
Pass and the H1' comparison objects/search budgets are not matched.

### 5.2 Secondary simple condition

Simple raw-\(U\) gain was +0.605816 [0.597444, 0.613970], while cyclic gain was
+0.612641 and true-minus-cyclic was -0.006825 [-0.009077, -0.004615]. The same
failure reproduces, but this secondary condition cannot alter the complex
verdict.

Complete registered quantities are in
[confirmation_metrics.csv](tables/confirmation_metrics.csv), control points in
[control_gains.csv](tables/control_gains.csv), and episode aggregates in
[per_episode_metrics.csv](tables/per_episode_metrics.csv).

## 6. Post-Result Construct Audit

### 6.1 Primary cyclic control

For each target \(y\), the registered index map always supplies the update from
target \((y+1)\bmod8\). This mapping is applied consistently in all three splits,
and the control correction is retrained on that mapping. Its target-source
contingency is a permutation matrix, not the independent uniform matrix; it
preserves the full class code. A separate readout can learn the inverse.

A read-only post-hoc diagnosis varied the offset independently by episode and
split and refit the same correction budget. Its complex confirmation gain fell
to approximately -0.00225 nats/example; applying a cyclic mismatch only at
confirmation to the true model gave -0.19154. These values identify the control
bug but are not registered evidence and do not replace E01's label.

### 6.2 H1' object and search budget

E01's full correction used standardized raw \(U\), whereas its conditional
directions and rank-two correction used \(R_U\). Therefore \(D_{80}\) is not a
retention comparison between a full space and its two-dimensional subspace.
The real direction also searched four \(\rho\) candidates on DEVELOPMENT, while
label-permutation controls reused the selected real \(\rho\) and random controls
each supplied one plane. This is not equal selection budget.

These issues justify the construct qualification
`PRIMARY_H2_INELIGIBLE_CONTROL_DESIGN`; they do not license post-hoc selection
of a favorable E01 comparison.

## 7. Reproducibility And Artifact Map

Worker root:
`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_e01_layer25_conditional_innovation/`.

Complete full run:
`runs/a15-08-e01-full-20260810/` relative to that worker. It contains original
data, smoke/full representations, restricted logits, all logs, 58.7 MB common
basis, frozen direction/null arrays, per-record losses, environment receipt,
and a complete 17-file analysis artifact manifest.

Curated canonical evidence beside this record:

- `evidence/result.json`, `guard_report.json`,
  `frozen_selection_ledger.json`, `plot_contracts.json`, environment and code
  receipts;
- `tables/confirmation_metrics.csv`, `control_gains.csv`,
  `per_episode_metrics.csv`, and `common_basis_spectrum.csv`;
- two audited figures in PNG and PDF.

Independent audit exactly reproduced per-record means, episode aggregation,
2,000 bootstrap intervals, q95 values, and verdict mapping. Canonical copied
artifacts match worker hashes. Two provenance limitations remain: E01 did not
persist per-episode values for every null control, and its extraction manifest
records the model path rather than a complete model-weight content hash.

## 8. Visualization Audit

- [figure_confirmation_gains.png](figures/figure_confirmation_gains.png) is
  legible and numerically sourced from the confirmation/control CSVs. Its
  cyclic bar must be read as a learned relabeling, not a valid nuisance null.
- [figure_common_basis.png](figures/figure_common_basis.png) is legible and
  answers only where variance and retrieved directions lie in one TRAIN-only
  coordinate. It cannot determine H2/H1.
- Plot question, units, aggregation, allowed conclusions, and limitations are
  frozen in [plot_contracts.json](evidence/plot_contracts.json).

## 9. Claim Boundary And One Next Decision

E01 establishes only that its tensors and algebra are valid and that two
specific fitted readout comparisons are positive. It does not establish
layer-added information, two-dimensional sufficiency, adjacent-layer novelty,
global low rank, native use, expert utility, or Router gain.

**Exactly one next decision:** run the already frozen
[A15_08_E02 fresh balanced-mismatch repair](../A15_08_E02_fresh_balanced_mismatch_repair/protocol.md)
on wholly new episodes. No E01 confirmation value may select an E02 rank,
threshold, control seed, or result wording.
