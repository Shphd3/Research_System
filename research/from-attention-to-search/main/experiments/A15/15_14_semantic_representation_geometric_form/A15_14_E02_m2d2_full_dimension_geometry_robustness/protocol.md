# Protocol: A15_14_E02 M2D2 Full-Dimension Geometry Robustness

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_ANALYSIS
Approval status: HUMAN_CONFIRMED on 2026-09-02
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: protocol freeze, implementation, tests, smoke, full analysis, figures, summary, and detailed record
Design frozen at: 2026-09-02T03:16:29Z before implementation and before raw-dimension results were read
Purpose: test whether the E01 direction/radius/shape conclusion depends on PCA compression
Primary Anchor: 15_14_semantic_representation_geometric_form_anchor.md
Experiment role: robustness check of the registered representation geometry
Primary metric: confirmation normalized mutual information (NMI), from 0 to 1
Treatment: centered original 1,024-dimensional hidden state with no PCA fit or projection
Reference: the eligible E01 centered PCA-rank-64 result at the same fixed cell
Changed variable: coordinate width and projection only, from train-only PCA-64 to centered raw 1,024 dimensions
Held fixed: saved Qwen states, data and splits, labels, pooling, hidden-state index 15, model families, three clusters, 20 restarts, radius control, nulls, bootstrap, and verdict thresholds
Pass reading: raw geometry is semantically readable and its typed carrier verdict can be compared with E01
Scientific fail reading: eligible raw geometry produces a different carrier verdict from E01
Insufficient: identity, label isolation, centering, width, fit, uncertainty, or artifact completeness fails
Cannot claim: token-level accessibility, native Router use, expert utility, causal semantic use, or next-token gain
Approval decision: the researcher explicitly requested immediate completion without a second approval round; later token screening remains unauthorized
```

Active Focus: [focus_m2d2_semantic_geometric_form.md](../../../../focus/focus_m2d2_semantic_geometric_form.md)  
Primary Anchor: [A15_14 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md)  
Reference experiment: [E01 Protocol](../A15_14_E01_m2d2_direction_norm_covariance_atlas/protocol.md)

## 1. Terminology And Definitions

The original-dimension representation is the 1,024-dimensional frozen hidden
state after subtracting the training-set mean. No principal-component basis is
fit, selected, or applied. Direction is the unit vector of this centered state;
radius is its Euclidean length. Raw hidden norm means the length before
centering and remains a separate descriptive quantity.

NMI measures agreement between label-blind cluster assignments and held-out
domain labels; it cannot show that the native model or a Router uses the
information. A typed carrier verdict applies the E01 direction, radius, and
shape rules without changing their 0.02 threshold.

## 2. Anchor Alignment

The Anchor asks whether coarse and parent-conditional fine M2D2 domain
semantics are carried by direction, radius, shape, or a mixture. E01 fixed a
train-only PCA coordinate to make that question measurable. E02 tests the
named rival that PCA itself creates, suppresses, or rotates the apparent
carrier. It does not replace the E01 primary verdict; it determines whether
that verdict is robust to retaining all original coordinates.

## 3. Tested Hypothesis

The prediction is that direction remains readable and radius remains a
registered contributor after PCA is removed. The strongest rival is that the
E01 attribution is projection-dependent: high-dimensional nuisance or removed
low-variance coordinates change direction readability, radius contribution,
or shape attribution.

## 4. Data Construction And Provenance

Reuse the four eligible E01 representation shards without re-extracting the
model. They contain the exact balanced M2D2-Wikipedia 3-by-3 hierarchy:
9,216 train, 2,304 development, and 4,608 confirmation windows. Each window has
256 tokens. Labels are metadata only. The source manifest SHA-256 is
`83ed6f7a99d48667664ea2f73fef188996c1105cadb99fd0f2901f244f5237e6`.

The packed 256-token window remains the uncertainty unit. This does not create
independent source documents and does not remove lexical/topic composition as
a rival.

## 5. Representation And No-Training Contract

The saved model is Qwen3-0.6B-Base with every model parameter frozen during
E01 extraction. E02 performs no model forward pass, backward pass, optimizer
step, epoch, Router fit, expert fit, or checkpoint transition.

For split \(s\), layer \(\ell\), and pooling object \(p\), let \(h_{i,s}^{(\ell,p)}\)
be the saved 1,024-dimensional state. Fit only the train mean
\(\mu_{\ell,p}\) and compute

\[
z_{i,s}^{(\ell,p)}=h_{i,s}^{(\ell,p)}-\mu_{\ell,p},\qquad
r_i=\lVert z_i\rVert_2,\qquad
u_i=\frac{z_i}{\max(r_i,\epsilon)}.
\]

No PCA object may be instantiated or called in the E02 path. The primary cell
remains mean pooling over token positions 64--255 at hidden-state index 15,
the output of zero-indexed block 14. The final-position pooling and all 29
saved hidden-state locations remain descriptive guards.

## 6. Conditions And Unsupervised Fits

For every layer and pooling object, fit the same five E01 families on the same
samples: log-radius Gaussian mixture, spherical k-means on direction,
von-Mises--Fisher direction mixture, Euclidean k-means on the full vector, and
diagonal Gaussian mixture on the full vector. Coarse clustering uses three
global clusters. Fine clustering uses three clusters separately inside each
known parent; child labels never enter fitting.

Each family receives restarts 0--19. Train objective selects the restart and
development objective breaks ties. Confirmation labels are forbidden from
selection. At the primary cell, retain direction and permute radius within
each split and, for fine analysis, within each parent; refit Euclidean and
diagonal full-vector models.

## 7. Metrics And Frozen Analysis

The primary point estimate is confirmation NMI. The primary directional model
is the von-Mises--Fisher mixture; spherical k-means is a guard. The exact E01
rules remain frozen:

- direction readability requires directional NMI above the 97.5th percentile
  of 1,000 matched label permutations;
- radius contribution passes when radius-only NMI is above its matched null or
  the lower 95% bound of observed-minus-permuted-radius diagonal-model NMI is
  above 0.02;
- independent shape requires the diagonal model to beat both the directional
  and Euclidean models by lower 95% bounds above 0.02 without radius already
  explaining the gain;
- 10,000 stratified window bootstraps with seed 1701 quantify uncertainty.

The result record must show raw-1,024 and E01 PCA-64 values side by side. A
numerical difference is descriptive unless it changes a registered gate or
typed verdict. Confirmation labels cannot choose a layer, regularizer,
dimension, or model family.

## 8. Scientific Stages And Stop Rules

| Stage | Goal | Input | Operation | Required output | Stop rule |
| --- | --- | --- | --- | --- | --- |
| Identity preflight | prove exact E01 reuse | four shards and manifest | verify hashes, counts, widths, layer count, and frozen receipts | identity receipt | any mismatch stops |
| Red/green tests | protect no-PCA meaning | synthetic matrices and saved-schema fixture | require 1,024-dimensional centered output and no PCA call; verify label-blind fitting and radius permutation | passing unit tests with recorded initial failure | wrong failure or missing guard stops |
| Smoke | test numerical viability | bounded samples from all splits | run all five families and both tasks at the primary cell | finite predictions and objectives | non-finite or collapsed implementation stops full analysis |
| Full analysis | produce eligible evidence | all 16,128 saved windows | all layers, both pools, five families, 20 restarts; primary controls, nulls, and bootstraps | source tables, prediction arrays, results, figures, completion audit | missing registered artifact yields insufficient evidence |
| Result audit | compare with E01 | eligible raw result and canonical E01 result | trace every value and apply frozen typed rules | Summary and Detailed | no later screening may start |

## 9. Artifacts And Execution Boundary

Worker code and raw outputs live under
`/data/250010109/MoE_Router/experiments/20260902_a15_14_e02_m2d2_full_dimension_geometry_robustness/`.
The worker reuses the E01 shards read-only. The Research_System experiment
folder owns this Protocol, `summary.md`, `detailed.md`, and curated figures.

The required full artifacts are: source identity receipt, red/green test log,
smoke receipt, 584-row raw-dimension atlas, primary prediction archive,
10,000-draw bootstrap archive, 1,000-draw label-null archive, primary results,
raw-versus-PCA table, two decision figures, environment/code/protocol hashes,
and completion audit.

Resource ceiling: reuse existing local/AFS artifacts and CPU analysis; no new
GPU allocation is required because no extraction occurs. If a later run needs
GPU extraction, it is outside this approval.

## 10. Outcome Branches And Claim Boundary

- Same typed verdict in both tasks: the E01 carrier attribution is robust to
  retaining all 1,024 centered coordinates under the registered model families.
- Different eligible typed verdict: PCA changes the measured carrier
  attribution; report the exact gate that changes and preserve both results.
- Missing identity, finite fits, uncertainty, or required artifacts:
  `INSUFFICIENT`, with no geometry update.

Even a same-verdict result cannot establish token-level accessibility, native
Gate use, expert utility, task improvement, abstract rather than lexical
semantics, or a universally privileged coordinate system.

## 11. Confirmation And Freeze Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question and boundary | CONFIRMED | active Focus and Anchor; unchanged |
| B data and provenance | CONFIRMED | eligible E01 shards and manifest |
| C task and supervision | CONFIRMED | label-blind geometry audit; unchanged |
| D model and representation | CONFIRMED | user explicitly required original dimensions and no PCA |
| E optimization | CONFIRMED | no model training; same 20-restart unsupervised selection |
| F comparison and decision evidence | CONFIRMED | E01 rules preserved; raw-1,024 versus PCA-64 |
| G execution and reproducibility | CONFIRMED | user explicitly authorized immediate completion; later gates require approval |

Cross-block consistency audit: `PASS`. The treatment changes only projection
width. Data, saved states, labels, pooling, layer, estimators, restart budget,
uncertainty, and claim boundary remain fixed. The scientific body freezes at
the timestamp in the approval snapshot; subsequent changes require an
append-only amendment and eligibility audit.
