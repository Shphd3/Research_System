---
experiment_id: A15_12_E02_expression_bank_boundary_coverage_controls
status: COMPUTATION_COMPLETE_BOUNDED
run: full-20260830T184100Z
human_result_confirmation: pending
---

# E02 Detailed Evidence: Expression-Bank Boundary Coverage

## 1. Question and Evidence Role

E01 showed that probes fit on C4E-A remain strongly associated with the labels
but lose positive low-tail margins on C5E. E02 separates two rivals:

1. C5E has no stable linear readout even from C5E training data; or
2. C5E is internally readable, but a boundary learned only from C4E is not
   invariant to the C4E-to-C5E expression shift.

E02 is a post-E01 mechanism control. C5E-A and C5E-B were already present in
the frozen metadata, and E01 had already opened C5E. E02 is therefore not an
independent confirmation panel.

## 2. Provenance

### 2.1 Frozen representations

Raw extraction directory:

```text
/data/250010109/MoE_Router/experiments/
20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/
runs/full-20260827T163900Z/extraction
```

| Artifact | SHA-256 | Shape / role |
|---|---|---|
| `c4_activations.npy` | `c1748f785e4563689f52cb94951861dbb994d6437f559baeb1a3306e34d43107` | `[6,1920,2048]` |
| `c5_activations.npy` | `cf68c95288306386d1b82bed0ca64066af0073873f41aa278da9cd86010a2422` | `[6,1920,2048]` |
| `c4_metadata.jsonl` | `a94a2f59655fd152953f8a2e0086bc69a4f15bb2886a2a15b93eb83fca888ad9` | C4E labels and frozen halves |
| `c5_metadata.jsonl` | `4708b9e655d6152102f9d58f363d947ef4ced1c74658b7078bc0988d01f1bc52` | C5E labels and frozen halves |

The representation is the actual 2,048-dimensional `block.mlp` input at the
final `Classification:` decision token, before Gate logits, top-k, and experts,
at Blocks 4, 12, 20, 28, 36, and 44.

### 2.2 Frozen E01 reference

Reference run:

```text
Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/
a15_12_e01_qwen3_30b_fixed_fact_expression_separability/
runs/full-20260830T172302Z
```

- E01 completion audit SHA-256:
  `5d4259165ccfb590cbe603b2a88bc8021e5205e8921575b53ffc6d96e3b5db64`.
- E01 model ledger SHA-256:
  `8f5485d185745992cd16984c34a005da0458e40b3f9ca62cd0fa7511f621073c`.
- E01 prediction ledger SHA-256:
  `80dfda5e79d51d9a6f4b143aa74ccfb18ed629249bee469bf2f2251332ec7394`.
- All 60 referenced NPZ files were checked individually against E01's
  completion manifest.
- The independently defined 60-model bundle hash is
  `45343f748b9c81b3feaca5ccb1774edfd6eb788f16dc8031700ccd414c01061b`.
  Its algorithm sorts NPZ basenames and updates one SHA-256 state with each
  basename, a NUL byte, and the raw 32-byte file digest.

### 2.3 E02 source and runtime identity

- E02 source bundle:
  `e10b0231047ec529f7d2cf4e2381665e014a3f62defdbdf24327a861cafd59d4`.
- Python `3.10.12`; NumPy `1.24.4`; pandas `1.5.3`; SciPy `1.12.0`;
  scikit-learn `1.2.0`.
- Resume and completion guards bind the source bundle and these runtime
  versions. The source bundle was unchanged at completion.

## 3. Data Split Audit

Each bank has 30 complete template families and 1,920 rows. Its frozen A and B
halves each contain 15 complete families and 960 rows. Each complete family
contains one row for every one of the 64 semantic leaves.

The four half-specific complete 64-leaf atom-order maps are pairwise disjoint.
At row level, however, a few evaluation rows use an atom order seen in C5A for
the same semantic leaf:

| C5-containing training regime | Evaluation panel | Overlap rows | Affected families |
|---|---:|---:|---:|
| C5A / full pooled | C4B | 20 | 11 |
| C5A / full pooled | C5B | 15 | 8 |
| matched pooled | C4B | 7 | 6 |
| matched pooled | C5B | 6 | 5 |

The registered sensitivity deletes these rows only for point estimates; it
does not bootstrap incomplete families. No deletion changes a bottleneck sign.

## 4. Training Regimes

| Regime | Training rows | Bank coverage | Evaluation panels |
|---|---:|---|---|
| `C4A` | 960 | C4E only | C4B and C5B; frozen E01 models |
| `C5A` | 960 | C5E only | C4B and C5B |
| `POOLED_MATCHED_A` | 896 | seven SHA-selected complete A families from each bank | C4B and C5B |
| `POOLED_FULL_A` | 1,920 | all 15 A families from each bank | C4B and C5B |

The matched regime has no sample-size advantage over the 960-row single-bank
references. It is slightly smaller, so it is evidence for bank exposure under
no sample advantage, not an exact sample-count identity control. The full
regime jointly changes coverage and sample count.

For every regime and layer, the ten tasks are parent eight-way `P`, joint
64-way `J`, and the eight separate parent-conditional fine eight-way heads
`F_0` through `F_7`. Child IDs are never pooled across parents.

Each regime computes one training-side 2,048-dimensional mean and one positive
isotropic RMS scale, then applies multinomial L2 logistic regression. Five-fold
cross-validation is grouped by complete template family; pooled folds are
balanced by bank. The penalty grid is:

```text
1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100
```

All C4A, C5A, and full-pooled cells select `C=100`. In the 120 matched-pooled
evaluation cells, 98 use `C=100`, 16 use `C=10`, and 6 use `C=1`; each fitted
model appears in two panel cells. All fits converge.

## 5. Metrics and Inference

For a correct class \(y\) and competitor \(j\), the normalized geometric margin is

\[
\gamma_i=\min_{j\ne y}
\frac{(w_y-w_j)^\top z_i+b_y-b_j}
{\lVert w_y-w_j\rVert_2}.
\]

Each task reports balanced accuracy, negative log likelihood when available,
fifth-percentile margin, median, minimum, and non-positive rate. Frozen C4A
reference predictions do not retain all class probabilities, so their NLL is
explicitly unavailable; this does not affect registered margins.

For each regime-panel-layer cell, the registered bottleneck is the minimum
task-level fifth percentile across all ten tasks. The analysis resamples the 15
complete families of C4B and C5B 10,000 times. A panel-specific draw is shared
across all regimes, layers, and tasks. One studentized minimum-deviation
statistic supplies a one-sided lower band for all 48 cells; the realized global
studentized quantile is `-4.980203569973034`.

Paired contrasts subtract raw-activation-unit bottleneck margins, never margins
normalized under separate regime scales. Their 95% intervals reuse the same
panel-family draws.

## 6. Direct Results

### 6.1 All 48 bottlenecks

| Regime | Panel | Block 4 | Block 12 | Block 20 | Block 28 | Block 36 | Block 44 |
|---|---|---:|---:|---:|---:|---:|---:|
| C4A | C4B | 5.095 / 4.639 | 3.997 / 2.517 | 2.767 / 2.111 | 1.984 / 1.277 | 1.195 / -0.326 | 6.560 / 4.737 |
| C4A | C5B | -1.346 / -5.423 | -3.336 / -7.420 | -6.546 / -11.057 | -5.906 / -8.106 | -10.131 / -14.131 | -1.117 / -7.105 |
| C5A | C4B | -2.446 / -6.492 | -6.920 / -13.784 | -6.125 / -10.645 | -8.311 / -15.415 | -15.470 / -22.422 | 3.094 / -0.858 |
| C5A | C5B | 5.143 / 4.934 | 3.107 / 0.697 | 2.034 / -0.159 | 0.015 / -3.262 | 0.667 / -1.873 | 6.947 / 5.068 |
| Matched pooled | C4B | 4.565 / 3.772 | 2.004 / -0.331 | 1.783 / -1.398 | 0.920 / -1.255 | -0.451 / -1.990 | 6.476 / 5.260 |
| Matched pooled | C5B | 3.946 / 1.845 | 1.961 / -0.401 | 0.263 / -2.674 | -1.958 / -5.025 | -1.831 / -7.824 | 5.537 / 2.711 |
| Full pooled | C4B | 4.791 / 4.250 | 3.446 / 2.339 | 2.520 / 1.863 | 1.796 / 0.622 | 0.654 / -0.389 | 6.273 / 4.710 |
| Full pooled | C5B | 4.615 / 4.380 | 3.269 / 2.904 | 2.357 / 1.676 | 1.390 / -0.154 | 1.195 / 0.309 | 6.233 / 4.735 |

Each cell is `observed bottleneck / simultaneous lower bound`, in its
training-regime RMS units. Positive observed values with non-positive lower
bounds are not registered as robust.

### 6.2 Within-bank readability

For C5A-to-C5B, the minimum task accuracy by block is 100%, 100%, 99.17%,
95.00%, 97.50%, and 100%. The mean accuracy over the ten tasks is 100%, 100%,
99.92%, 99.26%, 99.13%, and 100%. All six observed bottleneck margins are
positive. The evidence therefore rejects the simple reading that C5E lacks
linear semantic information altogether.

The middle-depth uncertainty is real rather than a reporting artifact. At
Block 28, the observed bottleneck is only `0.015` and is owned by `F_6`.
Dropping one family once can move it to `-0.019`; fixed `C=10,100,1000`
produces bottlenecks `-0.016`, `0.015`, and `0.057`. This is the sole cell that
fails both registered sign-stability guards.

Consequently, the two rivals in Section 1 are decisively separated only at
Blocks 4, 12, and 44: both C4E and C5E have certified within-bank readout there,
while neither single-bank head has certified cross-bank transfer. At Blocks 20,
28, and 36, C5E's positive point estimate and high accuracy show substantial
internal readability, but its simultaneous lower tail is not certified. Those
blocks retain both boundary-transfer failure and internal low-tail fragility as
live explanations.

### 6.3 Directional boundary trade-off

With equal 960-row single-bank training sets, `C5A - C4A` raw-unit bottleneck
differences are negative on C4B and positive on C5B at every block; all 12
paired intervals exclude zero. Examples:

- C4B Block 36: `-3.013`, 95% interval `[-3.545, -2.706]`;
- C5B Block 36: `+2.311`, 95% interval `[1.858, 2.567]`;
- C4B Block 44: `-1.593`, 95% interval `[-2.206, -1.331]`;
- C5B Block 44: `+2.897`, 95% interval `[1.755, 3.649]`.

The matched pooled regime improves C5B over C4A at all six blocks despite no
sample advantage, but worsens C4B at Blocks 4--36 with intervals excluding
zero; the Block 44 C4B interval includes zero. It certifies both panels only at
Blocks 4 and 44. Full pooled training certifies both panels at Blocks 4, 12,
20, and 44, but this combines bank exposure and twice-bank training coverage.

The correct layer-local verdict is therefore:

- Blocks 4, 12, and 44: established expression-bank-conditioned boundary
  incompatibility, distinct from within-bank unreadability;
- Blocks 20, 28, and 36: bank-specific fitting improves the matched panel, but
  C5E internal simultaneous robustness is not established, so the mechanism
  remains mixed;
- full pooled Blocks 4, 12, 20, and 44: a common robust linear boundary exists
  after both-bank exposure and more training data, without isolating which of
  those changes is causal.

### 6.4 Which semantic granularity fails

Across the 48 bottlenecks, `P` and `F_6` each own 15, while `F_0`, `F_7`,
`F_1`, and `F_5` own the rest. The joint 64-way head never uniquely owns an
all-task bottleneck. This is consistent with the E01 reading: most residual
failures arise within particular parent-conditioned fine tasks, not from an
additional global composition barrier.

This does not prove that a low-budget deployed hierarchy can realize the full
linear heads. It only locates the full-space readout bottleneck.

## 7. Controls and Deviations

### 7.1 Passed controls

- 23 unit/integration tests pass.
- Completion counts match exactly: 240 model entries, 480 cells, 138,240
  predictions, 48 bottlenecks, 36 paired intervals, 720 leave-one-family-out
  rows, 1,440 fixed-penalty task cells, 120 fixed-`C=100` conformance cells,
  360 overlap-excluded cells, and two figures.
- All 200 registered output artifacts rehash correctly.
- Independent recomputation reproduces observed bottlenecks, standard errors,
  simultaneous lower bounds, and paired intervals to at most
  `1.78e-15` absolute numerical error.
- Removing all registered row-level atom-order overlaps changes no sign.

### 7.2 Evidence hygiene and limitations

- `results.json` is written before the final completion audit. It is not
  authoritative by itself; only `completion_audit.json: passed=true` licenses
  interpretation.
- The interactive full-run stdout was not saved as a local raw log. Immutable
  layer artifacts, run configuration, timestamps, artifact hashes, and the
  passed completion audit retain the computational evidence. This is a
  provenance limitation, not a numerical failure.
- E02's 48-cell simultaneous band differs from E01's registered uncertainty
  procedure and must not be used to retroactively rewrite E01's verdict.
- The bootstrap conditions on fitted heads and training families; it estimates
  evaluation-template variation, not fitting uncertainty.
- All facts are reused between C4E and C5E. E02 cannot adjudicate whether the
  heads learned semantic relations or stable fact signatures.

## 8. Figure Contracts

### `simultaneous_bottleneck_comparison.png`

- **Question:** Which training regimes support positive all-task low tails on
  each bank and block?
- **Source:** `bottlenecks.csv`.
- **Axes:** block on x; normalized observed bottleneck and one-sided
  simultaneous lower bar on y; panels are C4B and C5B; color is training
  regime.
- **Allowed:** compare bottleneck signs and certification across regimes within
  the frozen evaluation contract.
- **Not allowed:** subtract normalized magnitudes across regimes as physical
  distances or infer a causal rotation.

### `paired_raw_margin_differences.png`

- **Question:** How does each alternative training regime change the same
  panel/block bottleneck relative to C4A?
- **Source:** paired raw-unit bootstrap contrasts.
- **Axes:** block on x; treatment-minus-C4A raw-activation margin difference on
  y; panels are C4B and C5B.
- **Allowed:** infer a nonzero directional trade-off when the paired interval
  excludes zero.
- **Not allowed:** compare across blocks as if raw activation scales had one
  universal semantic unit or attribute full-pooled gains to coverage alone.

Both rendered figures were visually inspected after generation.

## 9. Execution Ledger

Worker:

```text
Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/
a15_12_e02_expression_bank_boundary_coverage_controls
```

Full command:

```bash
PYTHONPATH=. MPLCONFIGDIR=/tmp/a15_12_e02_mpl \
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python run_audit.py \
  --output runs/full-20260830T184100Z \
  --jobs 6 \
  --n-bootstrap 10000
```

The run completed with exit code zero in approximately 1,822 seconds. Six
layers completed before the bootstrap stage, and the final completion audit
passed.

## 10. Artifact Map

Canonical reading path:

- [Summary](summary.md)
- [Protocol](protocol.md)
- [Full bottleneck table](tables/bottlenecks.csv)
- [Robustness matrix](tables/robustness_matrix.csv)
- [Same-bank versus cross-bank table](tables/same_bank_vs_cross_bank.csv)
- [Common-boundary table](tables/common_boundary_by_layer.csv)
- [Task-group summary](tables/task_group_summary.csv)
- [Paired raw-unit differences](tables/paired_raw_margin_differences.csv)
- [Overlap exclusion audit](tables/overlap_exclusion_audit.csv)
- [Independent recomputation](validation/independent_recompute.json)
- [Completion audit copy](validation/completion_audit.json)
- [Preflight copy](validation/preflight.json)
- [Run configuration copy](validation/run_config.json)
- [Pytest receipt](validation/pytest.xml)

Raw run:

```text
Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/
a15_12_e02_expression_bank_boundary_coverage_controls/
runs/full-20260830T184100Z
```

## 11. Claim Boundary and Next Decision

The allowed result is fixed-fact, full-space linear readability and
expression-bank boundary compatibility. The evidence does not reach unseen
facts, low-rank deployability, native Gate use, expert utility, or LM function.

The only next decision is the frozen-probe TAX-C4A transfer stress test defined
in A15_12_E03. E03 also does not test an architecture or expert utility; it can
only decide whether a separate representation-shaping Anchor and Protocol
should be opened.
