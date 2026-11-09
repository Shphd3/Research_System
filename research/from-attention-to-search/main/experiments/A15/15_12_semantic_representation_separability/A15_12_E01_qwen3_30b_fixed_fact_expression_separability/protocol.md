---
experiment_id: A15_12_E01_qwen3_30b_fixed_fact_expression_separability
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-30
primary_anchor: A15_12_semantic_representation_separability
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
scientific_contract_frozen: true
scientific_body_frozen_at: 2026-08-30T17:03:05Z
resource_profile: cpu_cached_activation_analysis_no_gpu
---

# Protocol: Qwen3-30B Fixed-Fact Cross-Expression Semantic Separability Audit

## 0. Approval Snapshot

| Field | Frozen value |
| --- | --- |
| Document status | `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN` |
| Human authorization | direct request on 2026-08-30 to start now and waive iterative Anchor/Protocol approval |
| Unique question | how predictive, low-tail robust, globally coherent, and readout-complex are coarse/fine semantic labels in the actual frozen MoE input |
| Primary Anchor | [A15_12](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_12_semantic_representation_separability/15_12_semantic_representation_separability_anchor.md) |
| Confirmed Focus | [focus_qwen3_30b_semantic_representation_separability.md](../../../../focus/focus_qwen3_30b_semantic_representation_separability.md) |
| Training surface | C4E half A only |
| Evaluation surfaces | C4E half B and full C5E, never refitted |
| Primary metric | fifth percentile of RMS-scale-normalized geometric multiclass margin |
| Capability guard | held-out balanced accuracy with template-preserving fixed-prediction label-permutation calibration |
| Independence unit | complete template family |
| Cannot claim | unseen-fact generalization, native Gate use, expert utility, LM gain, causal formation, or low-rank sufficiency |

Blocks A--G are `CONFIRMED_BY_DIRECT_EXECUTION_AUTHORIZATION`. Cross-block
consistency is `PASS`. This Protocol is the implementation plan; no separate
chat-only execution plan owns scientific choices.

## 1. Terminology / Definitions

- **C4E / C5E:** two controlled expression banks. They change template and
  wording but reuse the same six atomic statements for each of the same 64
  semantic leaves. C5E is therefore an expression replication, not an unseen-
  fact confirmation set.
- **Parent task (`P`):** one eight-way classifier over broad academic fields.
- **Conditional fine task (`F_p`):** for one fixed parent \(p\), one eight-way
  classifier over that parent's child labels. Eight separate tasks are fit.
  Reused numeric child IDs are never pooled across parents.
- **Joint task (`J`):** one 64-way classifier over the complete
  parent--child leaf label. This is the closest registered proxy for one
  global semantic linear Router.
- **Actual MoE input:** the final decision-token tensor received by the
  registered block's `mlp` and native Gate, before sparse expert selection.
- **Average readability:** above-null held-out balanced accuracy.
- **Low-tail robustness:** a positive simultaneous lower bound for the fifth
  percentile of geometric margins.
- **CDNV:** class-distance-normalized variance,
  \((\operatorname{tr}\Sigma_a+\operatorname{tr}\Sigma_b)/(2\lVert
  \mu_a-\mu_b\rVert_2^2)\). Lower is descriptively cleaner; it has no verdict
  threshold.

## 2. Anchor Alignment — A: CONFIRMED

The experiment adjudicates only the frozen representation object. It separates
semantic label definition, held-out linear readability, low-tail geometry,
and global composition. It deliberately stops before Gate behavior, expert
utility, and representation-shaping training.

## 3. Tested Hypotheses And Rivals

At least one registered layer has fixed-fact cross-expression robust linear
readout if all ten tasks are associated with their held-out labels and have a
jointly positive low-tail certificate on both evaluation panels.

Named rivals are:

1. `average_only`: accuracy is high but difficult examples have non-positive
   margins;
2. `conditional_only`: parent and oracle-parent fine heads work but the global
   64-way head does not;
3. `pair_localized`: a small number of parent or leaf pairs dominate failure;
4. `fixed_fact_only`: expression transfer works but the design cannot identify
   unseen-fact generalization.

## 4. Data Construction And Provenance — B: CONFIRMED

The model is frozen Qwen3-30B-A3B. The representation width is 2048 and layers
are fixed at 4, 12, 20, 28, 36, and 44.

| Role | Frozen artifact | Shape / rows | SHA-256 |
| --- | --- | --- | --- |
| C4E activations | `/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z/extraction/c4_activations.npy` | \(6\times1920\times2048\) | `c1748f785e4563689f52cb94951861dbb994d6437f559baeb1a3306e34d43107` |
| C4E metadata | same directory, `c4_metadata.jsonl` | 1,920 | `a94a2f59655fd152953f8a2e0086bc69a4f15bb2886a2a15b93eb83fca888ad9` |
| C5E activations | same directory, `c5_activations.npy` | \(6\times1920\times2048\) | `cf68c95288306386d1b82bed0ca64066af0073873f41aa278da9cd86010a2422` |
| C5E metadata | same directory, `c5_metadata.jsonl` | 1,920 | `4708b9e655d6152102f9d58f363d947ef4ced1c74658b7078bc0988d01f1bc52` |

Every panel has 8 parents, 8 children per parent, and 30 complete template
families. The existing hash-sorted C4E split is frozen: 15 families / 960 rows
in half A and 15 families / 960 rows in half B. Each conditional-fine task has
120 C4E-A training rows, 120 C4E-B rows, and 240 C5E rows. The parent and joint
tasks use all rows.

Preflight must verify hashes, shapes, layer order, row IDs, label balance,
template balance, A/B disjointness, and the fact-reuse relation between C4E and
C5E. Any mismatch stops the run.

## 5. Learning Task And Permitted Supervision — C: CONFIRMED

Only C4E-A representations, labels, and template-family IDs may fit
normalization, select regularization, or fit weights. C4E-B and C5E labels may
enter scoring, cluster bootstrap, and the fixed-prediction label-permutation
calibration only after the head is frozen.

There are exactly 60 fitted heads: six layers times ten tasks. Those heads
produce 120 evaluation cells because each is scored on C4E-B and C5E. No layer,
parent, task, panel, sample, or failed cell may be silently removed.

## 6. Model And Optimization — D/E: CONFIRMED

At each layer, estimate one training mean \(\mu_\ell\) and global root-mean-square
scale \(s_\ell\) from all C4E-A rows. This isotropic transformation is applied to
every task and both evaluation panels. Coordinatewise standardization is
forbidden because it changes the L2 geometry independently by coordinate.

Fit multinomial logistic regression with L2 penalty, intercept, no class
weights, `lbfgs`, `max_iter=5000`, and `tol=1e-8`. Candidate inverse penalties
are

\[
C\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\}.
\]

Use five deterministic folds of complete C4E-A template families. Choose the
\(C\) with minimum mean validation negative log likelihood; ties within
\(10^{-12}\) choose the smaller \(C\) (stronger regularization). Every fold uses
the already registered layerwise global isotropic transform, which itself is
fit only on C4E-A and contains no test information. Any convergence warning in
selection or final fitting marks that model `Insufficient`; there is no
result-dependent solver change.

## 7. Primary Metrics And Frozen Analysis — F: CONFIRMED

For test row \(i\), compute

\[
\gamma_i=\min_{j\ne y_i}
\frac{(w_{y_i}-w_j)^\top z_i+b_{y_i}-b_j}
{\lVert w_{y_i}-w_j\rVert_2}.
\]

The primary continuous metric is \(q_{0.05}(\gamma)\). Also report balanced
accuracy, macro negative log likelihood, median margin, and the fraction of
non-positive margins. A positive sample fifth percentile means that roughly no
more than 5% of rows in that panel lie on a non-positive nearest-competitor
boundary; it is not a population theorem.

For each panel and layer, define the all-task bottleneck

\[
B_{p,\ell}=\min_{t\in\{P,J,F_1,\ldots,F_8\}}q_{0.05}(\gamma_{p,\ell,t}).
\]

Resample complete template families jointly across all tasks 10,000 times.
For the registered all-task certificate, use a one-sided Bonferroni lower
percentile at \(0.05/12\) across six layers and two panels. A layer has a
low-tail certificate only when the lower bound of \(B_{p,\ell}\) is positive for
both panels.

### Held-out label-association calibration

Predictions remain fixed. For each of 9,999 deterministic draws, permute
evaluation labels inside every complete template family while preserving the
task structure:

- `P`: permute the eight parent identities and carry all eight child rows in a
  parent block together;
- `F_p`: within fixed parent \(p\), permute its eight child labels;
- `J`: permute all 64 leaf labels.

Compute the chance-corrected gain
\(G=(\mathrm{BA}-1/K)/(1-1/K)\). Use the resulting held-out conditional
permutation \(p\) values and Holm correction across all 120 evaluation cells.
This calibration tests prediction--label association on the frozen held-out
panels. It is not a full-pipeline retraining permutation and cannot restore
pristine confirmatory status to already inspected data.

## 8. Verdict Rule

For each layer:

- `EXPRESSION_ROBUST_ALL_GRANULARITIES`: all ten tasks on both panels have
  Holm-adjusted \(p\le0.05\), and the registered low-tail lower bound is positive
  on both panels;
- `READABLE_BUT_LOW_TAIL_FRAGILE`: all ten tasks on both panels pass the
  association guard, but at least one panel lacks a positive low-tail bound;
- `PARTIAL_READABILITY`: at least one of the 20 layer--task--panel cells fails
  the association guard while inputs and fits remain valid;
- `INSUFFICIENT`: any data, leakage, convergence, class-balance, coefficient-
  norm, bootstrap, or completeness guard fails.

The experiment-level answer reports all six layer verdicts. It does not select
one best layer and generalize beyond this audit.

## 9. Secondary Diagnostics

For every valid cell report:

1. row- and class-level confusion, classwise non-positive-margin rate, and the
   ten weakest true-versus-predicted pairs;
2. pairwise CDNV with trace variance and squared mean distance, including
   denominator guards; CDNV localizes overlap but has no pass threshold;
3. the singular spectrum of the class-centered coefficient matrix, its
   90%-energy rank, and participation-ratio effective rank. Because no Router
   rank/sample budget is registered, these values are descriptive and cannot
   establish low-rank sufficiency;
4. parent, conditional-fine, and joint trajectories across all six layers,
   never a PCA scatter as verdict evidence.

## 10. Known Good / Bad / Confusing Cases

- **Known good:** multiplying all raw activations by a positive scalar before
  the registered RMS normalization leaves predictions and geometric margins
  numerically invariant.
- **Known bad:** pooling `child_id=0..7` across different parents into one
  global fine task; this changes the semantic target and invalidates the run.
- **Known bad:** a C4E-B or C5E row enters normalization, CV, fitting, or layer
  selection.
- **Known confusing:** high parent and conditional-fine accuracy with weak
  joint accuracy. This is a substantive global-composition failure, not a
  contradiction.
- **Known confusing:** high accuracy with negative fifth-percentile margin.
  This means average readability coexists with a weak tail; neither metric is
  allowed to erase the other.

## 11. Stage And Output Contract

| Stage | Goal | Stop rule | Required artifacts |
| --- | --- | --- | --- |
| 0 preflight | verify frozen inputs and semantic units | any hash/schema/split/fact-reuse mismatch | `preflight.json` |
| 1 test/smoke | prove split isolation, task construction, margin invariance, permutation structure, and non-overwrite | any failed automated test or smoke identity | `smoke_receipt.json`, test log |
| 2 observed heads | fit all 60 heads and score 120 cells | retain invalid cells; no replacement | `models/`, `predictions.npz`, `cells.csv` |
| 3 uncertainty/null | run grouped bootstrap and fixed-prediction permutations | missing draw/cell stops verdict | `bootstrap.json`, `permutation.json` |
| 4 diagnostics/render | compute CDNV, confusion, coefficient spectra, figures | missing registered table/figure fails completion | `diagnostics.*`, `figures/` |
| 5 completion | hash artifacts and audit the contract | any mismatch => `Insufficient` | `results.json`, `completion_audit.json` |

The worker must use a new output directory and refuse to overwrite a completed
run. Raw arrays and logs stay on the worker surface. Curated tables and report-
ready figures are copied beside `summary.md` and `detailed.md` only after
completion.

## 12. Resource Contract And Claim Boundary — G: CONFIRMED

The frozen activations make this a CPU analysis; no GPU is required. The
expected worker envelope is 6 CPU workers, 16--32 GB RAM, and no model forward
pass. If re-extraction becomes necessary because a hash or representation
identity fails, this Protocol stops; a separate 4× or 8× RTX 5090 extraction
amendment is required. H100 is neither required nor authorized by this
contract.

The strongest allowed claim is fixed-fact, cross-expression linear
readability or fragility at named layers. Unseen facts, native routing,
expert utility, LM improvement, causal formation, and publishable architecture
gain remain outside the experiment.
