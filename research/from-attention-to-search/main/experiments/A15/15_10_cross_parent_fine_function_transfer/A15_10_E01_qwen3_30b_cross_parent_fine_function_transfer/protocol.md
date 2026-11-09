---
experiment_id: A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-28
primary_anchor: A15_10_cross_parent_fine_function_transfer
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
scientific_contract_frozen: true
scientific_body_frozen_at: 2026-08-28T03:09:28Z
resource_profile: h100-4-reserved
---

# Protocol: Qwen3-30B-A3B Cross-Parent Fine-Function Transfer Audit

## 0. Approval Snapshot

| Field | Value |
| --- | --- |
| Document status | `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN` |
| Execution scope approved | implementation, label-blind smoke, and full run on one 4×H100 reserved worker |
| Purpose | determine whether mathematics and physics fine-class spaces carry each other's held-out target function |
| Primary Anchor | [A15_10](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_10_cross_parent_fine_function_transfer/15_10_cross_parent_fine_function_transfer_anchor.md) |
| Confirmed Focus | [focus_cross_parent_fine_function_transfer.md](../../../../../../../daily_research_reports/backup/2026/08/0828/meeting_reports/focus_cross_parent_fine_function_transfer.md) |
| Experiment role | frozen-representation functional transfer audit |
| Treatment | target examples projected into the other parent's fine Fisher space, followed by a newly trained target head |
| Primary control | target examples projected into their own fine Fisher space |
| Matched null | source child labels permuted by complete template-family blocks, with the entire source-space to target-test pipeline rerun |
| Primary metric | continuous relative retention `RR`; never clipped |
| Descriptive reference | `RR=0.9`; not a hard scientific gate |
| Cannot claim | native Router use, expert utility, causal necessity, architecture gain, or universal natural-language behavior |

Block status: A--G `CONFIRMED`. Cross-block consistency is `PASS`. The
scientific body and decision-bearing configuration were frozen before
implementation at `2026-08-28T03:09:28Z`.

## 1. Terminology / Definitions

- **Source parent:** the parent whose fine labels and training-half states
  estimate the seven-dimensional projection space.
- **Target parent:** the parent whose true fine labels train the linear head and
  whose untouched opposite half is scored.
- **Own:** source and target parent are the same.
- **Cross:** source and target parent differ.
- **Strict cross-fit:** A estimates the space and trains the target head, B is
  test-only; then B estimates/trains and A is test-only. Every example is
  scored only by a pipeline that did not use its half for space estimation,
  standardization, regularization selection, or head fitting.
- **Complete-pipeline permutation null:** one source-label randomization reruns
  Fisher-space estimation, target projection, train-only preprocessing and
  regularization selection, target-head fitting, and held-out target scoring.
- **Complete template family:** one `template_family_id` block spanning all 64
  panel leaves. For a parent-specific operation, the block contributes that
  parent's complete set of eight fine-class rows. Those rows remain together;
  the family ID is never split during resampling or randomization.
- **Relative retention (`RR`):** the empirical position of Cross between its
  matched null (`0`) and Own (`1`) on held-out negative log likelihood. It is
  not a population percentage or a risk ratio.

## 2. Anchor Alignment — A: CONFIRMED

The uncertainty is whether the low coarse--fine overlap found by A15_09 hides
a cross-parent functionally interchangeable fine space or instead accompanies
parent-local fine function. The test changes only the parent that supplies the
seven-dimensional projection space. Geometry is secondary; target held-out
function is primary.

The strongest rival is pipeline mismatch: Cross could look weaker because it
received a different head, regularization rule, sample count, dimension, or
test set, or stronger because its null did not repeat source-space estimation.
The matching contract in Sections 6--10 removes those differences.

## 3. Tested Hypothesis

At a fixed registered layer, mathematics and physics have transferable fine
function if both Cross directions beat their complete-pipeline source-label
null and the relation reproduces from C4 to C5 after Own validity gates pass.
The competing parent-local profile is Own function without replicated Cross
excess. Failure to establish transfer is not proof of zero transfer.

## 4. Rival Explanations

| Rival | Guard or comparison |
| --- | --- |
| Fisher spaces are unstable or rank-deficient | inherited rank-seven and A/B stability gates, recomputed from the cached activations |
| math and physics use different whitening metrics | exactly one pooled \(\widehat W\) per panel/layer/split is shared by both parents and every condition |
| head capacity or target data differs | Own/Cross use the same target rows, labels, seven dimensions, head family, and scoring |
| a random anisotropic source subspace transfers | source-label permutation rebuilds the full pipeline; Haar is diagnostic only |
| general coarse semantics explains transfer | rank-seven common coarse-space target-head control |
| one expression panel drives the result | C4 primary and C5 independent replication are never pooled to rescue a claim |

## 5. Data Construction And Provenance — B: CONFIRMED

The frozen model is Qwen3-30B-A3B. The measured tensor is the native final
decision-token vector received by each registered block's MoE MLP/Gate, with
hidden width 2048. Blocks are fixed at 4, 12, 20, 28, 36, and 44.

| Role | Frozen artifact | Shape | SHA-256 |
| --- | --- | --- | --- |
| C4 primary activations | `/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z/extraction/c4_activations.npy` | \(6\times1920\times2048\) | `c1748f785e4563689f52cb94951861dbb994d6437f559baeb1a3306e34d43107` |
| C5 replication activations | `/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/full-20260827T163900Z/extraction/c5_activations.npy` | \(6\times1920\times2048\) | `cf68c95288306386d1b82bed0ca64066af0073873f41aa278da9cd86010a2422` |

The matching metadata and extraction manifest from that run are required and
must pass their recorded hashes before analysis. Each panel has 8 parents by 8
children by 30 complete template families. Mathematics and physics are fixed;
no parent, layer, or panel may be added or replaced after any scientific output
is visible. The existing SHA-sorted 15-family A/B split is reused unchanged.

The panels are controlled natural-language expression panels, not unrestricted
organic text. No Qwen forward pass or model training is part of this experiment.

## 6. Learning Task And Permitted Supervision — C: CONFIRMED

For a target parent, the permitted input is only its seven-dimensional
projected native state from the training half. The required output is one of
its eight true child labels. Source child labels may estimate the source
Fisher space but never define, train, or evaluate the target head. Target test
labels are confirmation-only and enter scoring after the complete fold has
frozen.

For fold A-to-B:

1. use split A and the shared \(\widehat W^A\) to estimate the registered space;
2. project target-A and target-B states through that space;
3. fit all preprocessing, regularization selection, and the target head using
   target-A true labels only;
4. score target-B once.

Fold B-to-A reverses A and B. The two out-of-fold prediction sets are combined
only after both fits finish.

## 7. Model / Architecture And Frozen Variants — D: CONFIRMED

### 7.1 One pooled Fisher metric per panel, layer, and split

For split \(a\), let \(q_i\) be the full parent--child leaf label and define

\[
E_i=x_i-\overline x_{q_i}.
\]

Fit one Ledoit--Wolf covariance \(\widehat W_{p,\ell}^{a}\) from all 64 leaf
classes in that panel/layer/split. Mathematics and physics use this exact same
matrix, not separately estimated parent metrics. Own, Cross, coarse control,
observed spaces, and every permutation reuse the same frozen
\(\widehat W_{p,\ell}^{a}\).

For one eight-class task with class-contrast matrix \(M\), estimate

\[
S=\operatorname{orth}\!\left((\widehat W_{p,\ell}^{a})^{-1}M\right),
\]

with requested rank seven and the inherited numerical-rank gate.

### 7.2 Matched target head

Every condition uses a seven-dimensional projection and the same multinomial
logistic-regression implementation, objective, preprocessing class,
regularization candidate grid, inner split rule, selection criterion,
tie-breaker, convergence rule, and held-out scorer. The learned coefficients,
training-derived standardization statistics, and selected regularization value
may differ because they are outputs of the same train-only algorithm applied
to different projected features; they are never copied between conditions.

Thus the controlled intervention is the projection-space source. Target
training rows and labels, target test rows, dimension, and algorithmic rules
are otherwise identical.

## 8. Training Objective And Optimization — E: CONFIRMED

The target head minimizes multinomial negative log likelihood plus L2 weight
penalty. The projected features are mean-centered using the current target
training half and the same center is applied to its held-out half. No
coordinatewise variance scaling is allowed: such scaling would make the L2
head depend on an arbitrary orthonormal basis rotation inside the same Fisher
subspace.

Use `lbfgs`, an intercept, no class
weighting, `max_iter=5000`, `tol=1e-8`, and candidate inverse penalties
\(C\in\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\}\). Within each target
training half, use five deterministic folds of complete template families;
choose the \(C\) with the lowest mean inner-fold NLL and break ties toward the
smaller \(C\) (stronger regularization). Repeat the same selection rule
independently for Own, Cross, coarse control, and every null realization.

No held-out A/B truth may choose preprocessing, \(C\), convergence retry,
checkpoint, layer, or condition. A non-converged fit after the registered
iteration limit makes that condition insufficient; it is not silently retried
with a different solver or grid.

## 9. Conditions, Randomization, And Independence Units

For each panel, layer, target, and A/B direction, run:

1. `Own`: target fine space;
2. `Cross`: other-parent fine space;
3. `Coarse`: common eight-parent rank-seven Fisher space;
4. `OwnPerm`: target-label-permuted target spaces;
5. `CrossPerm`: source-label-permuted source spaces.

Use 200 permutation realizations, preserving the predecessor's registered
count. For one realization and one training half, each complete template
family is one randomization block: draw one permutation of its eight source
child labels and apply it to the entire eight-row family. Do not permute target
head labels or held-out labels. Re-estimate the permuted source contrast and
space with the same pooled \(\widehat W\), then rerun target projection,
train-only preprocessing and regularization selection, target-head training,
and held-out testing. Reusing only an old geometric null is forbidden.

For bootstrap uncertainty, combine the two out-of-fold prediction ledgers and
resample the 30 complete target template families with replacement. Each draw
keeps all eight fine-class rows of a family together and uses paired family
indices across Own, Cross, Coarse, and their matched comparisons. This
prediction-level bootstrap measures held-out family sampling uncertainty; it
does not claim to include full training-set or model-pretraining uncertainty.

Use 10,000 paired family-bootstrap draws with
root seed `151001`; permutation root seed `151002`.

## 10. Primary Metric And Frozen Analysis Plan — F: CONFIRMED

For target \(t\), source \(s\), and a fixed panel/layer, let \(L_t(S_s)\) and
\(L_t(S_t)\) be the sample-weighted NLL over the combined A-to-B and B-to-A
out-of-fold predictions. Let \(L_{s\rightarrow t}^{null}\) be the median NLL of
the 200 complete `CrossPerm` pipelines. Define

\[
RR_{s\rightarrow t}=
\frac{L_{s\rightarrow t}^{null}-L_t(S_s)}
{L_{s\rightarrow t}^{null}-L_t(S_t)}.
\]

`RR` is primary and continuous. It is never clipped. `RR=0.9` is drawn only as
a descriptive reference and never changes eligibility, a scientific verdict,
layer selection, or the architecture route.

The independence unit is a complete template family. C4 and C5 are analyzed
separately; parents, directions, and layers are not pooled. Missing or invalid
registered cells remain visible and are not replaced. The six raw layer values
are primary; no monotonic trend is assumed and no result-dependent layer is
selected.

At one fixed layer, call transferable
fine function established only if all Own gates pass and observed Cross NLL is
below the 2.5th percentile of its complete-pipeline `CrossPerm` distribution
in both directions and independently in C4 and C5. This null-excess rule does
not use 0.9. If Own is valid but the conjunction fails, report “transfer not
established at this layer,” not “strict parent specificity proved.” If any Own
gate fails, the RR denominator is non-positive/non-finite, or either panel is
invalid, report `Insufficient` for that layer. No global “any of six layers”
claim is allowed without a separately confirmed multiplicity rule.

## 11. Secondary Metrics And Guards

- held-out NLL for every individual condition and null quantiles;
- balanced accuracy, with 0.125 as the eight-class chance reference;
- Own versus complete `OwnPerm` function admission;
- A/B Fisher rank and same-task stability inherited from A15_09;
- mathematics--physics fine-space projector overlap and seven principal-angle
  \(\cos^2\) values as geometry diagnostics only;
- selected \(C\), convergence status, coefficients, and per-template predictions
  as audit data, never post hoc selection variables.

Secondary metrics cannot rescue a failed or insufficient RR result.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good implementation case:** changing an orthonormal basis inside the
  same seven-dimensional space must leave fitted predictions invariant within
  numerical tolerance after identical train-only selection.
- **Known bad case:** a target test row enters space estimation, standardization,
  inner cross-validation, or head fitting; the entire affected cell is
  ineligible.
- **Known confusing case:** geometry is low but RR is positive, or geometry is
  high but RR is null. This is a valid mixed scientific result, not an
  implementation failure.
- **No-signal control:** `OwnPerm` and `CrossPerm` must run the same head pipeline
  as observed conditions; an old subspace-overlap null cannot substitute.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / operation | Pass / stop | Artifact |
| --- | --- | --- | --- | --- |
| 0 preflight | prove cached inputs are the frozen predecessor assets | verify activation, metadata, split, layer and manifest hashes | any mismatch stops all work | `preflight.json` |
| 1 numerical smoke | validate computation without reading a scientific result | test pooled-\(W\) identity, A/B isolation, rotation invariance, full null traversal and non-overwrite behavior | all identities pass; smoke cannot authorize full run | `smoke_receipt.json` |
| 2 space and head audit | produce all registered out-of-fold observed and null predictions | run all panels, layers, targets, directions and permutations without changing settings | invalid cells retained; no replacement | `predictions.*`, `null_ledger.*` |
| 3 analysis | compute RR, raw metrics, uncertainty and geometry diagnostics | use frozen aggregation only | formula and row-count identities pass | `results.json`, `cells.csv` |
| 4 rendering and completion | create decision evidence and audit provenance | render registered figures and hash every artifact | missing cell or figure fails completion | `figures/`, `completion_audit.json` |

## 14. Algorithm, Output, And Provenance Contract

The worker experiment must live in a new directory and treat the predecessor
run as read-only. It must refuse to overwrite an existing output directory.
Required outputs are:

- one row per panel/layer/direction with Own, Cross, Coarse, null summaries,
  RR, validity and uncertainty;
- one out-of-fold prediction row per target example and condition;
- complete per-permutation loss and selected-regularization ledger;
- Fisher rank/stability and geometry diagnostic ledger;
- configuration, environment, input hashes, code revision and dirty-state
  receipt;
- one primary functional-transfer figure, one RR trajectory figure, and one
  optional geometry--function relation figure;
- a completion audit proving all registered cells and figures are present.

The primary figure is a four-facet layerwise functional ladder: C4/C5 by
transfer direction, with raw held-out NLL for Own, Cross and Coarse plus the
complete-pipeline permutation band. The RR trajectory is separate so raw NLL
and normalized retention are never mixed on one ordinate.

## 15. Success / Failure / Insufficient Evidence

- **Pass for transferable function at a layer:** the confirmed Section 10
  full-pipeline null-excess and C4/C5 bidirectional replication rule passes.
- **Fail to establish transfer at a layer:** all Own gates pass but the
  registered transfer rule does not; this weakens shared-fine transfer at that
  layer without proving strict locality.
- **Insufficient:** any Own admission, rank, stability, leakage, convergence,
  RR denominator, artifact, or panel-replication prerequisite fails.

The result must report all six layers. A Pass, Fail, or Insufficient outcome
does not itself authorize Router training.

## 16. What This Cannot Claim

The experiment cannot show that Qwen's native Router reads either Fisher
space, that a shared or local Router improves language-model loss, that any
direction is causally necessary, that low transfer implies orthogonality, or
that mathematics and physics represent all domains or natural-language styles.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding / unresolved item |
| --- | --- | --- |
| A question and boundary | `CONFIRMED` | researcher approved the unique real-data transfer question |
| B data and provenance | `CONFIRMED` | inherited frozen model, layers, panels, parents, A/B split and cached activations |
| C task and supervision | `CONFIRMED` | strict target-head cross-fit and source/target label separation explicitly required |
| D model and matching | `CONFIRMED` | one pooled \(W\) and matched Own/Cross pipeline explicitly required |
| E optimization | `CONFIRMED` | `lbfgs`, fixed \(C\) grid, five family folds, train-only NLL selection and stronger-regularization tie-breaker |
| F comparison and decision evidence | `CONFIRMED` | continuous RR, descriptive-only 0.9, 200 full-pipeline permutations, 10,000 family bootstraps, and per-layer bidirectional C4/C5 rule |
| G execution and reproducibility | `CONFIRMED` | implementation, label-blind smoke, and full run authorized on one `h100-4-reserved` ACP worker |

Cross-block consistency: `PASS`. The researcher explicitly stated that the
experiment could be implemented and submitted to a four-H100 reserved worker,
thereby confirming the surfaced E--G proposals and authorizing the named
scopes. After execution begins, any change
to data, spaces, pooled \(W\), cross-fit, null pipeline, head rule, RR, randomization
unit, layer, parent, panel, or decision rule requires an append-only amendment
and an explicit evidence-eligibility judgment.

### Pre-run amendment A1 — basis-invariant preprocessing

- **Time:** 2026-08-28, before implementation, smoke, submission, or any
  A15_10 scientific output.
- **Before:** train-half feature centering and coordinatewise scaling.
- **After:** train-half mean centering only; no coordinatewise scaling.
- **Reason:** coordinatewise scaling does not commute with an orthonormal basis
  rotation and contradicts the registered same-subspace rotation-invariance
  smoke. Mean centering plus L2 multinomial logistic regression preserves that
  invariance.
- **Affected block:** E preprocessing only. Data, supervision, spaces, pooled
  \(W\), cross-fit, regularization grid and selection, null, RR, uncertainty,
  verdict rule, and execution scope are unchanged.
- **Evidence visibility:** no implementation or scientific result existed.
- **Eligibility:** no prior evidence is affected; A15_10 execution must use the
  amended rule.

### Pre-run clarification A2 — Own functional-admission gate

- **Time:** 2026-08-28, before smoke, submission, or scientific output.
- **Clarification:** an Own condition passes functional admission only when its
  observed held-out NLL is below the 2.5th percentile of its complete-pipeline
  `OwnPerm` distribution. Rank seven, A/B stability, convergence, finite
  denominator, and artifact gates remain jointly required.
- **Reason:** Section 10 required “all Own gates” but Section 11 had not written
  the exact function-null quantile locally. This records the same lower-is-
  better null-excess rule used for Cross and adds no result-derived choice.
- **Evidence visibility and eligibility:** no A15_10 result existed; all future
  cells use this clarification.

## 18. Execution Ledger

### Submission S1

- **Submitted:** 2026-08-28T03:25:14Z
- **ACP job:** `pt-9dwr9q52`
- **Resource:** workspace `share-space`, cluster `share-cluster`, one
  `n6ls.iu.i40.4` worker, four visible H100 GPUs, `reserved` quota
- **Run stamp:** `20260828T032514Z`
- **Worker output:**
  `/data/250010109/MoE_Router/experiments/20260828_a15_10_e01_qwen3_30b_cross_parent_fine_function_transfer/runs/full-20260828T032514Z`
- **Pre-submission gates:** 10/10 unit tests passed; shell syntax and Python
  compilation passed; frozen C4/C5 activation hashes, metadata hashes, shapes,
  six layers, predecessor result and Protocol all passed local preflight.
- **Scientific visibility:** no A15_10 result was read before submission.

### Completion C1

- **Completed:** 2026-08-28T03:35:25Z; ACP state `SUCCEEDED`; no retry.
- **Completion audit:** `PASS`, 24/24 registered cells present, 18 eligible,
  6 retained as insufficient, and all three registered figures present.
- **Primary artifacts:** `results.json` SHA-256
  `6b1a559099523f2289eab0dd409531a180d856b9739adcd32d3a39b94b0eef19`;
  `completion_audit.json` SHA-256
  `df0973a1c75b0d2d053d67f446e144bf7d8aed7e062038bfcdbc153659c4f95f`.
- **Result records:** [summary.md](summary.md) and
  [detailed.md](detailed.md).
- **Boundary:** evidence is complete; the AI interpretation and one proposed
  next decision await the researcher's result/boundary confirmation. Router
  training remains unauthorized.
