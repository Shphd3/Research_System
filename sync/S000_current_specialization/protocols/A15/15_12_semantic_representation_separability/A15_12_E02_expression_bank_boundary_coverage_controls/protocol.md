---
experiment_id: A15_12_E02_expression_bank_boundary_coverage_controls
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-30
primary_anchor: A15_12_semantic_representation_separability
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
authorization_basis: direct request to execute the separability audit without iterative Anchor or Protocol approval
resource_profile: cpu_cached_activation_analysis_no_gpu
evidence_role: necessary_post_E01_mechanism_control
---

# Protocol: Expression-Bank Boundary-Coverage Controls

## 0. Why This Control Is Necessary

E01 tests whether a linear decision system learned only from C4E-A transfers
unchanged to C4E-B and C5E. A failure on C5E has two rival explanations:

1. C5E is not linearly readable even within its own expression family; or
2. C5E is linearly readable, but a boundary learned from C4E alone is not
   stable under the C4E-to-C5E expression shift.

E01 cannot distinguish these explanations. E02 is the smallest cached-
activation control needed to close that logical gap. It does not alter E01's
registered verdict.

## 1. Decision Question

For the same 64 fixed semantic leaves and six Qwen3-30B-A3B MoE-input layers:

- is each expression bank internally readable on unseen template families;
- do bank-specific linear boundaries transfer in either direction; and
- does training on both expression banks admit one common linear boundary on
  held-out template families from both banks?

## 2. Frozen Data And Tasks

Reuse the exact E01 activation and metadata artifacts, hashes, representation
identity, layers 4/12/20/28/36/44, and ten tasks: parent (`P`), joint 64-way
leaf (`J`), and eight parent-conditioned fine tasks (`F_0`--`F_7`). C4E and
C5E each contain 30 complete template families split into 15 A families and
15 B families. A and B never share a template family.

The semantic facts remain fixed across all banks. This control still cannot
test unseen-fact generalization.

## 3. Training-Regime Contrast

All regimes use the E01 multinomial L2 logistic probe, one global training
mean plus isotropic RMS scale per layer and regime, five complete-template-
family folds, and the frozen grid

$$
C\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\}.
$$

| Regime | Fitting and tuning data | Frozen evaluation panels | Role |
| --- | --- | --- | --- |
| `C4A` | C4E-A only | C4E-B, C5E-B | matched E01 reference |
| `C5A` | C5E-A only | C5E-B, C4E-B | within-C5 readability and reverse transfer |
| `POOLED_MATCHED_A` | seven complete C4E-A families plus seven complete C5E-A families, selected by frozen SHA-256 order (896 rows) | C4E-B, C5E-B | bank coverage without a larger training set than either 960-row single-bank regime |
| `POOLED_FULL_A` | all C4E-A plus all C5E-A families (1,920 rows) | C4E-B, C5E-B | upper-bound common-boundary test with all available A-side coverage |

The `C4A` row is recomputed from the frozen E01 prediction ledger after a
`record_id` join to the frozen metadata and restriction of C5E to half B; its
models are not refit. The other three regimes fit 180 new heads in total and
produce 480 matched regime--layer--panel--task cells including the reference.

C5E half identities come directly from the existing metadata field. Preflight
must freeze and hash all four 15-family lists. Pooled cross-validation groups
use `(bank, template_family_id)` identities; every one of five validation folds
contains the same number of complete C4E and C5E families. As in E01, the
label-free mean and RMS scale are fit once on the complete A-side training
surface before grouped penalty selection. This is a matched, transductive
normalization convention inside the A-side cross-validation, not fold-local
preprocessing.

The family IDs and complete 64-leaf family-order mappings are disjoint. A
row-level audit nevertheless finds that, for the same semantic leaf, 15 of 960
C5E-B rows and 20 of 960 C4E-B rows reuse an atom permutation seen in at least
one C5E-A row. Preflight must freeze and hash those record IDs, and the control
must repeat affected point estimates after removing those rows. This
sensitivity does not preserve complete families and therefore does not own a
bootstrap verdict. "Held-out family" is allowed; "every row has an unseen atom
order" is not.

## 4. Metrics And Uncertainty

For every regime, layer, panel, and task report balanced accuracy, the fifth
percentile of the E01 RMS-normalized geometric multiclass margin, median
margin, non-positive-margin rate, and strict minimum margin. Also convert each
margin back to raw-activation distance units using that regime's positive RMS
scale. The all-task
bottleneck is the minimum task-level fifth percentile across `P`, `J`, and all
eight fine tasks.

Resample the 15 complete C4E-B families and the 15 complete C5E-B families
10,000 times, using the same panel-specific draw for every regime, layer, and
task. For each draw compute every all-task bottleneck. Construct simultaneous
one-sided lower bands from the fifth percentile of the minimum centered
bootstrap deviation after dividing every cell by its own bootstrap standard
error. The resulting studentized max-statistic is converted back to each
cell's normalized-margin units. This avoids both an unstable $0.05/48$
extreme percentile and comparisons of unstandardized margins across layers.
It remains a conditional bootstrap approximation: training families and
fitted probes are not resampled. In addition, drop each evaluation family once
and report whether every bottleneck keeps its observed sign.

On the same paired family draws, report 95% bootstrap intervals for the
within-panel, within-layer raw-activation-unit bottleneck differences `C5A - C4A`,
`POOLED_MATCHED_A - C4A`, and `POOLED_FULL_A - C4A`. Merely observing one
positive bound and one negative bound is not evidence that their difference
is nonzero. Normalized-margin magnitudes from separately normalized regimes
must never be subtracted.

Because this is a post-E01 mechanism control, it does not add a second
permutation verdict. Positive all-task low-tail bounds already imply strong
held-out accuracy; all raw accuracies remain visible.

All selected penalties and convergence states must be reported. Since E01
selected the upper grid edge for every model, recompute every new and reference
all-task bottleneck at fixed $C\in\{10,100,1000\}$ using the same training and
evaluation rows. A reading is called sign-stable only if its bottleneck sign is
unchanged across these three values. Exact margin magnitudes and coefficient
spectra remain regularization-sensitive; the sign pattern and paired regime
contrast own the diagnostic, not an exact rank claim.

## 5. Reading Rules

- If `C5A -> C5B` is robust while `C4A -> C5B` is not, E01 diagnosed boundary
  transfer failure, not intrinsic C5E non-separability.
- If both bank-specific within-bank directions are robust but both cross-bank
  directions fail, the readable axes are bank-conditioned.
- If `POOLED_MATCHED_A` is robust on both held-out banks and improves over
  `C4A` under the paired interval, bank coverage repairs the boundary without
  a training-size advantage. A `POOLED_FULL_A`-only repair remains confounded
  by both target-bank exposure and twice as many fitting rows.
- If both pooled regimes still lack a positive bound, the two held-out banks do not
  establish one sufficiently robust common linear separator under this probe.
- All comparisons are within the same layer and the same ten-task set. If
  `C4A -> C5B` and `C5A -> C4B` differ, report directional transfer rather
  than a symmetric coordinate-mismatch claim.
- Any failed hash, split, class-balance, convergence, or completeness guard is
  `INSUFFICIENT`, not a scientific failure.

## 6. Claim Boundary

The strongest result is restricted to fixed facts, two synthetic expression
generators, named layers, and full-space linear probes. It cannot establish
unseen-fact semantic abstraction, a universal semantic coordinate system,
native Gate use, expert specialization or utility, causal representation
formation, low-rank Router sufficiency, or language-model gain.
