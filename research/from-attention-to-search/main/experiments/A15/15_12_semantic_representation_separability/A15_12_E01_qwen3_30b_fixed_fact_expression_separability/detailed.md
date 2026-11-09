# Detailed Evidence: Qwen3-30B Fixed-Fact Cross-Expression Semantic Separability

Primary Anchor: [A15_12](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_12_semantic_representation_separability/15_12_semantic_representation_separability_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)  
Result status: `COMPUTATION_COMPLETE_BOUNDED`  
Knowledge status: `AI_EVIDENCE_RECORD_AWAITING_HUMAN_JUDGMENT`

## 1. Quick Recap

E01 asks whether the actual frozen Qwen3-30B-A3B MoE input contains a single
cross-expression linear organization for parent, every parent-conditioned
fine label, and the global 64-way leaf label. The answer is:

> Every named layer retains above-null average fixed-fact label association,
> but none has a positive registered all-task low-tail bound on both expression
> panels. C4E-B passes at all six layers; C5E fails at all six layers.

The evidence is eligible only for fixed-fact cross-expression readability. A
post-E01 control is required before interpreting the C5E failure as an
intrinsic representation deficit.

## 2. Exact Research Object

### 2.1 Data unit

Each row is one generated classification prompt for one of 64 leaves:

\[
8\text{ parents}\times8\text{ children per parent}.
\]

Every leaf owns six atomic propositions. A complete template family instantiates
one expression frame for all 64 leaves. C4E and C5E change framing, connective
structure, and atom order while reusing the same six atoms for each leaf.

Example C4E row, labels `mathematics` and `algebra`:

> A newly written profile begins with symbolic expressions and equations with
> unknown quantities; and polynomials and systems transformed by exact rules.
> A separate part then considers groups, rings, and fields defined through
> axioms; together with structure-preserving maps between formal systems. The
> final two clues concern solutions derived by manipulating symbolic relations;
> and abstract operations satisfying closure and inverse properties.  
> Determine the broad academic field and its specific subfield.  
> Classification:

### 2.2 Representation unit

For each prompt, the representation is the 2,048-dimensional tensor received
by `block.mlp` at the final `Classification:` decision position, before the
native Gate performs sparse expert selection. Registered blocks are 4, 12, 20,
28, 36, and 44. No answer text is present.

### 2.3 Tasks

- `P`: one balanced eight-way parent task.
- `F_0`--`F_7`: eight separate balanced eight-way child tasks, each with the
  true parent fixed. Numeric child IDs are never pooled across parents.
- `J`: one balanced 64-way parent--child task, the closest registered proxy for
  one global semantic linear Router.

## 3. Frozen Inputs And Provenance

| Artifact | Shape / rows | SHA-256 |
| --- | ---: | --- |
| `c4_activations.npy` | \(6\times1920\times2048\) | `c1748f785e4563689f52cb94951861dbb994d6437f559baeb1a3306e34d43107` |
| `c4_metadata.jsonl` | 1,920 | `a94a2f59655fd152953f8a2e0086bc69a4f15bb2886a2a15b93eb83fca888ad9` |
| `c5_activations.npy` | \(6\times1920\times2048\) | `cf68c95288306386d1b82bed0ca64066af0073873f41aa278da9cd86010a2422` |
| `c5_metadata.jsonl` | 1,920 | `4708b9e655d6152102f9d58f363d947ef4ced1c74658b7078bc0988d01f1bc52` |

Worker extraction:

`/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z/extraction`

Worker analysis run:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_12_e01_qwen3_30b_fixed_fact_expression_separability/runs/full-20260830T172302Z`

Preflight verified hashes, tensor shapes, block order, representation identity,
label factorial balance, complete families, C4E A/B disjointness, and C4E/C5E
fact reuse.

## 4. Split And Probe Flow

| Surface | Families | Rows | Allowed role |
| --- | ---: | ---: | --- |
| C4E-A | 15 | 960 | normalization, grouped CV, and fitting only |
| C4E-B | 15 | 960 | frozen evaluation only |
| C5E | 30 | 1,920 | frozen evaluation only |

At each layer, all C4E-A rows fit one mean \(\mu_\ell\) and one isotropic RMS
scale \(s_\ell\). The transform is

\[
z_i^{(\ell)}=(x_i^{(\ell)}-\mu_\ell)/s_\ell.
\]

Each of ten tasks then fits multinomial logistic regression with an intercept,
L2 penalty, `lbfgs`, `max_iter=5000`, and `tol=1e-8`. Five deterministic folds
hold out complete C4E-A template families. Candidate inverse penalties are
\(10^{-6}\) through \(100\) in powers of ten. Validation NLL chooses the penalty;
ties choose the smaller \(C\).

The layerwise normalizer is fitted on all C4E-A rows before internal CV. It is
label-free and never sees either evaluation panel, but it is a transductive
A-side convention rather than fold-local preprocessing. E02 preserves this
convention for matched comparisons.

## 5. Metrics And Decision Rules

For a correct class \(y\) and competitor \(j\), the normalized geometric margin is

\[
\gamma_i=
\min_{j\ne y_i}
\frac{(w_{y_i}-w_j)^\top z_i+b_{y_i}-b_j}
{\lVert w_{y_i}-w_j\rVert_2}.
\]

The primary cell metric is \(q_{0.05}(\gamma)\). For each panel and layer, the
all-task bottleneck is the minimum of that value across `P`, `J`, and all eight
fine tasks.

Ten thousand bootstrap draws resample complete evaluation families jointly
across all tasks. The registered one-sided lower percentile is \(0.05/12\) for
six layers times two panels. This is conditional on the one fitted C4E-A head:
it does not refit the probe or resample training families.

Nine thousand nine hundred ninety-nine fixed-prediction draws permute labels
inside every complete evaluation family while preserving task structure. Holm
correction covers 120 cells. This tests held-out prediction--label association;
it is not a full-pipeline retraining permutation or a fact-identity selectivity
control.

## 6. Execution And Validation Ledger

### 6.1 Actions and feedback

| Action | Direct feedback | Consequence |
| --- | --- | --- |
| Read the 2026-08-28 meeting correction and prior A15 records | PCA variance, linear readout, low-tail margin, Gate access, and utility were previously conflated | Registered a full-space held-out probe rather than a PCA plot |
| Audit C4E/C5E data provenance | Same 64 leaves and same atoms; only expression changes | Restricted claim to fixed facts |
| Write unit and integration tests before the formal run | Split isolation, task construction, normalized margin, permutation, bootstrap, and synthetic end-to-end checks passed | Authorized preflight and full analysis |
| Run preflight smoke | All hashes, shapes, halves, families, and fact-reuse guards passed | No Qwen forward pass or GPU was required |
| Run six layers with six CPU workers | 60/60 models converged; 120/120 cells and all registered artifacts were produced | Proceeded to conditional permutation and bootstrap |
| Independently recompute cells, bottlenecks, counts, and artifact hashes | Zero numeric mismatches; 78 worker artifact hashes matched | Numerical result retained |
| Visually inspect all three figures | One-sided lower bounds had been mirrored upward by symmetric plotting | Patched display helper, added regression test, and created a corrected canonical figure without modifying the completed run |
| Audit the scientific inference | C5E had never been used to fit a head | Opened E02 rather than claiming intrinsic C5E nonseparability |

### 6.2 Reconstructed commands

The full terminal stdout was not preserved. The following invocations are
reconstructed from the run configuration and surviving output directories:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python run_audit.py \
  --output runs/smoke-20260830T172204Z \
  --jobs 6 --preflight-only

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python run_audit.py \
  --output runs/full-20260830T172302Z \
  --jobs 6 --n-permutations 9999 --n-bootstrap 10000
```

The completed run reports 690.791 seconds. The current validation suite has 18
passing tests; its machine-readable receipt is [pytest.xml](validation/pytest.xml).
Current reconstructed source hashes are in
[current_source_hashes.txt](validation/current_source_hashes.txt). Scientific
modules were unchanged after the run; `render.py` contains the explicitly
recorded post-run one-sided display correction.

## 7. Complete Decision-Bearing Results

| Panel | Block | P accuracy / \(q_{.05}\) | J accuracy / \(q_{.05}\) | pooled F accuracy / \(q_{.05}\) | registered bottleneck / lower |
| --- | ---: | ---: | ---: | ---: | ---: |
| C4E-B | 4 | 1.000 / 5.095 | 1.000 / 7.463 | 1.000 / 7.901 | 5.095 / 4.865 |
| C4E-B | 12 | 1.000 / 3.997 | 1.000 / 5.013 | 1.000 / 5.092 | 3.997 / 3.026 |
| C4E-B | 20 | 1.000 / 2.767 | 1.000 / 3.910 | 1.000 / 3.758 | 2.767 / 2.340 |
| C4E-B | 28 | 1.000 / 1.984 | .999 / 2.872 | .999 / 2.937 | 1.984 / 1.145 |
| C4E-B | 36 | .997 / 1.456 | .999 / 1.986 | .996 / 1.996 | 1.195 / 0.111 |
| C4E-B | 44 | 1.000 / 6.852 | 1.000 / 8.243 | 1.000 / 8.516 | 6.560 / 5.568 |
| C5E | 4 | 1.000 / 4.066 | .985 / 2.227 | .986 / 3.059 | -1.677 / -2.741 |
| C5E | 12 | .984 / 1.104 | .840 / -2.733 | .859 / -2.513 | -5.822 / -8.573 |
| C5E | 20 | .972 / 0.537 | .765 / -3.940 | .786 / -4.451 | -7.566 / -11.405 |
| C5E | 28 | .920 / -0.607 | .697 / -4.021 | .729 / -4.398 | -6.878 / -7.770 |
| C5E | 36 | .856 / -1.373 | .666 / -4.261 | .688 / -5.414 | -10.880 / -11.982 |
| C5E | 44 | .999 / 4.669 | .991 / 3.518 | .985 / 3.124 | -1.905 / -3.080 |

Pooled fine results concatenate eight equal-sized fine tasks for description.
They do not own the verdict. Exact cell rows are in [cells.csv](tables/cells.csv)
and derived group rows in [task_group_summary.csv](tables/task_group_summary.csv).

### 7.1 Strict minimum versus fifth percentile

The all-task strict minimum margin is positive at C4E-B Blocks 4, 12, 20, and
44. It is negative at Blocks 28 and 36, which contain small error fractions.
Every C5E layer has a negative strict minimum. See
[strict_minima.csv](tables/strict_minima.csv).

Therefore the registered C4E-B pass is a fifth-percentile standard, not a
claim that every sample at every layer is strictly separable.

### 7.2 C5E parent-conditioned fine results

Each cell has 240 rows, 30 per child class.

| Parent | B4 accuracy / \(q_{.05}\) | B12 | B20 | B28 | B36 | B44 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| mathematics | 1.000 / 6.14 | .867 / -2.79 | .650 / -7.31 | .533 / -6.88 | .479 / -10.88 | .900 / -1.90 |
| physics | .912 / -1.68 | .846 / -5.82 | .746 / -7.57 | .729 / -4.89 | .633 / -6.22 | 1.000 / 6.29 |
| chemistry | 1.000 / 3.24 | .846 / -2.20 | .683 / -6.23 | .642 / -6.03 | .692 / -3.52 | 1.000 / 4.36 |
| biology | 1.000 / 4.59 | .967 / 0.74 | .908 / -0.85 | .846 / -2.21 | .783 / -2.25 | 1.000 / 5.87 |
| computer science | 1.000 / 7.80 | .779 / -2.96 | .854 / -1.47 | .821 / -1.67 | .833 / -1.08 | 1.000 / 6.51 |
| economics | 1.000 / 4.75 | .838 / -1.92 | .738 / -3.78 | .608 / -4.11 | .562 / -4.54 | 1.000 / 3.91 |
| medicine | .979 / 1.18 | .900 / -1.24 | .871 / -1.93 | .800 / -1.80 | .683 / -2.90 | 1.000 / 7.65 |
| linguistics | 1.000 / 6.21 | .833 / -3.00 | .838 / -1.94 | .854 / -1.93 | .838 / -2.12 | .979 / 1.29 |

Full rows: [c5_conditional_fine_summary.csv](tables/c5_conditional_fine_summary.csv).

Positive fine-task fifth percentiles occur for 7/8 parents at Block 4, 1/8 at
Block 12, 0/8 at Blocks 20/28/36, and 7/8 at Block 44. This supports a
descriptive endpoint-strong/middle-weak trajectory across six sampled blocks,
not a monotone or causal depth law.

### 7.3 Most frequent directed confusions

The complete confusion table remains on the worker surface. Curated top
directed errors are in
[c5_top_directed_confusions.csv](tables/c5_top_directed_confusions.csv).

Examples:

- B4 physics: mechanics \(\rightarrow\) relativity, 16; mechanics
  \(\rightarrow\) electromagnetism, 4.
- B20 physics: mechanics \(\rightarrow\) electromagnetism, 22;
  thermodynamics \(\rightarrow\) electromagnetism, 11.
- B36 mathematics: probability \(\rightarrow\) algebra, 23; geometry
  \(\rightarrow\) algebra, 20; analysis \(\rightarrow\) algebra, 19.
- B36 joint: financial economics \(\rightarrow\) public economics, 21; labor
  \(\rightarrow\) public economics, 19; microeconomics \(\rightarrow\) public
  economics, 15.

The worker `weakest_pairs.csv` is ranked by highest CDNV and only overlays
confusion counts; it is not the most-confused-pair table. CDNV and actual
confusion are weakly coupled and must remain separate diagnostics.

## 8. Diagnostic Findings

### 8.1 Template-family effects

C5E errors are not only class-local. At Block 36, pooled fine errors per
complete template family range from 7 to 31 of 64 leaves, with median 19.5.
Across families, joint and pooled-fine accuracy correlations are .974, .946,
.915, and .928 at Blocks 12, 20, 28, and 36. Thus some expression frames are
globally harder across many labels, while the most extreme confusions remain
class-specific. This is compatible with a template-by-class boundary shift;
it is not a causal account of how Qwen forms it.

### 8.2 Joint versus conditional fine

On C5E, joint accuracy differs from pooled fine accuracy by only -0.10 to
-3.23 percentage points across the first five sampled blocks and is 0.57 points
higher at Block 44. The data do not show strong local fine success followed by
a separate catastrophic global-composition failure. Fine transfer already
fails.

### 8.3 Weight spectra and regularization

All 60 models converged and selected \(C=100\), the maximum candidate. Their CV
NLL strictly decreased across the entire grid. Parent centered-weight
effective rank ranges 5.13--5.71, joint rank 36.90--47.04, and fine rank
6.08--6.87. These values are close to task-dependent algebraic class-rank
limits and cannot be read as an intrinsic semantic dimension or sufficient
Router rank.

See [model_selection_summary.csv](tables/model_selection_summary.csv). The
upper-edge selection makes exact NLL, coefficient spectra, and margin
magnitudes regularization-sensitive. The large C5E negative signs remain the
registered result; E02 adds fixed-\(C\) sign sensitivity.

### 8.4 CDNV heatmap

![C5E joint pairwise CDNV](figures/c5_joint_cdnv_heatmaps.png)

The heatmap shows \(\log_{10}\) pairwise class-distance-normalized variance.
Lower values mean lower total within-class trace variance relative to squared
class-centroid distance. Blocks 28 and 36 have broadly larger values than
Blocks 4 and 44. The color range is clipped to the global 2nd--98th
percentiles; the diagonal is undefined. This figure is diagnostic only: CDNV
does not optimize a decision direction or guarantee positive margin.

## 9. Comparison With The Prior Native-Router Representation Probe

The earlier A15_08_09_E03 result and E01 are compatible but not numerically
interchangeable.

| Dimension | A15_08_09_E03 | A15_12_E01 |
| --- | --- | --- |
| Dataset | 19,200-row `BIND-TAX-V2` | 1,920-row C4E and 1,920-row C5E |
| Target | parent eight-way only | parent, eight conditional fine, joint 64-way |
| Token | final `Answer:` token | final `Classification:` token |
| Representation | native input \(G\) and adjacent difference \(\Delta G\) | actual `block.mlp`/Gate input |
| Layers | all-layer screen, then freeze B42/B41 | six pre-registered blocks, no best-layer selection |
| Split | TRAIN/DEV/same/new | complete C4E template halves and separate C5E bank |
| Margin | unnormalized true-minus-rival score | RMS-normalized geometric boundary distance |
| Result | new-template BA .7543/.7121; all \(q_{.05}<0\) | C4E-B near perfect; C5E panel- and task-dependent failures |

The old audit shows that parent information is broadly accessible on a
different dataset. E01 adds hierarchy, a global 64-way pressure test, exact
representation identity, and stronger expression-bank transfer. Different
data, tokens, layer selection, and margin formulas explain different numerical
strength; they are not contradictory replications.

## 10. Deviations And Evidence Limits

1. The Protocol stage contract named `predictions.npz`; the complete worker
   ledger is `predictions.csv`. Content and counts are complete, but the format
   mismatch is recorded.
2. Smoke and full outputs are separate. `smoke_receipt.json` remains in the
   smoke directory, not the full directory.
3. The original full-run terminal log and an immutable pre-run code snapshot
   were not saved. The completion audit covers internal guards and hashes 78
   produced artifacts; the canonical test and reconstructed source receipts
   close the surviving provenance but cannot retroactively create the missing
   stdout record.
4. The original bottleneck PNG used symmetric plotting for a one-sided lower
   bound. No numerical table was affected. The raw run is preserved; the
   corrected canonical figure is explicitly post-run and display-only.
5. C4E-B has 15 and C5E has 30 independent template families. The extreme
   bootstrap percentile for C4E-B is discrete; Block 36's 0.111 lower bound is
   close to zero.
6. The permutation and bootstrap condition on a single C4E-A fit and an
   already inspected evaluation collection. They do not supply pristine
   confirmation or training-procedure uncertainty.
7. Non-positive margin rate is numerically the error rate under the unique
   argmax rule in these cells. The extra geometric information comes from the
   magnitude and low quantile of the margin, not from that rate alone.

## 11. Artifact Map

### Canonical curated evidence

- [cells.csv](tables/cells.csv): all 120 registered evaluation cells.
- [bottlenecks.csv](tables/bottlenecks.csv): 12 registered bottleneck bounds.
- [class_metrics.csv](tables/class_metrics.csv): all class-level accuracy and
  margin summaries.
- [task_group_summary.csv](tables/task_group_summary.csv): parent, joint, and
  pooled-fine reading table.
- [c5_conditional_fine_summary.csv](tables/c5_conditional_fine_summary.csv):
  eight parent-local trajectories.
- [c5_top_directed_confusions.csv](tables/c5_top_directed_confusions.csv):
  actual error-ranked pairs.
- [strict_minima.csv](tables/strict_minima.csv): empirical all-sample minima.
- [model_selection_summary.csv](tables/model_selection_summary.csv): penalty,
  convergence, and descriptive spectra.
- [figures/](figures): audited report figures.
- [validation/](validation): table curation, current tests, and source receipt.

### Worker-only complete evidence

The worker run retains 51,840 prediction rows, 56,064 confusion rows, 27,216
CDNV pairs, fitted coefficients, bootstrap draws, permutation draws, raw
figures, run configuration, and the completion audit. These are linked by the
absolute worker path in Section 3 and are not duplicated into the research
mainline.

## 12. Claim Boundary And Next Decision

Allowed: named-layer, fixed-fact, C4E-A-learned cross-expression linear
readability or fragility.

Forbidden: unseen-fact abstraction, intrinsic C5E nonseparability, native Gate
use, expert utility, language-model improvement, causal formation, universal
depth law, or low-rank Router sufficiency.

E02 is complete; see its
[Summary](../A15_12_E02_expression_bank_boundary_coverage_controls/summary.md).
The only next decision-bearing data extension is the `TAX-C4A`
new-to-probe fact-package joint-shift panel at the same six actual MoE inputs.
Because it also changes length and surface naturalness, failure cannot isolate
fact identity.
