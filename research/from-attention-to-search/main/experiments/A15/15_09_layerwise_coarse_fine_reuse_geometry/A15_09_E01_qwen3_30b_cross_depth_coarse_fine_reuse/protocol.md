---
experiment_id: A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-27
approval_date: 2026-08-27
primary_anchor: A15_09_layerwise_coarse_fine_reuse_geometry
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
scientific_contract_frozen: true
preferred_resource_profile: 5090-8-spot
conditional_fallback: 5090-4-spot_after_exact_profile_check
---

# Protocol: Qwen3-30B-A3B Cross-Depth Coarse--Fine Reuse Audit

## 0. Approval and freeze snapshot

The researcher approved implementation, a label-blind smoke, and the complete
frozen run on 2026-08-27. This Protocol records the approved scientific body
before any Qwen3-30B-A3B audit result is read. After execution starts, no layer,
panel, target parent, threshold, estimator, seed, or invalid-layer treatment may
change. Hardware fallback may change parallelism only.

The experiment is a frozen representation audit. It does not train a model,
Router, expert, probe, or architecture.

**Anchor:** [A15_09](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/15_09_layerwise_coarse_fine_reuse_geometry_anchor.md).

**Human-confirmed Focus:** [focus_coarse_fine_direction_alignment.md](../../../../../../../daily_research_reports/backup/2026/08/0826/focus_coarse_fine_direction_alignment.md).

## A. Question and claim boundary — CONFIRMED

### A1. Core questions

1. At each fixed layer, how much does the parent-conditional fine-class Fisher
   space for mathematics or physics reuse the common eight-parent coarse-class
   Fisher space?
2. How does this coarse--fine relation change across the six fixed depths?

“Reuse” means geometric overlap between stable seven-dimensional supervised
discriminant spaces in the same native representation. It does not mean that
the native Router uses those directions, that experts benefit from them, or
that the relation is causal.

### A2. Eligible conclusion

The audit may establish per-layer reuse values and a C4/C5-replicated monotone,
stage-structured, non-monotone, or unresolved depth trajectory on these two
controlled natural-language expression panels.

It cannot establish Router training benefit, expert utility, native gate use,
causal necessity, PCA-spectrum location, other-parent geometry, or universal
natural-language behavior. No Router training is authorized.

## B. Frozen model, representation, data, and selections — CONFIRMED

### B1. Model and representation

| Item | Frozen value |
| --- | --- |
| model | `/data/share/Qwen3-30B-A3B` |
| architecture | `Qwen3MoeForCausalLM` |
| blocks / hidden width | 48 / 2048 |
| experts / selected experts | 128 / top 8 |
| state | frozen inference, no backward or optimizer |
| measured tensor | final decision-token vector received by `block.mlp`, captured by a forward pre-hook |
| fixed blocks | 4, 12, 20, 28, 36, 44 |

Block numbers are one-based in reports and map to Python module indices
3, 11, 19, 27, 35, and 43. The hook captures the actual common input to that
block's MoE gate and experts; it does not reconstruct \(X+U\) from separate
tensors.

### B2. Panels and provenance

| Role | Frozen path | SHA-256 | Rows |
| --- | --- | --- | ---: |
| C4 primary | `/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum/data_v1/controlled_c4_expression.jsonl` | `4432e1493695542dd820c3e25483f81a31b10244bc1035c10ba1d15cd6b24f53` | 1,920 |
| C5 replication | `/data/250010109/MoE_Router/experiments/20260820_a15_07_e02_fixed_axis_low_rank_atlas/data_v1/controlled_c5_expression.jsonl` | `17619aa07e1b41f7d3ec36decf532f3a162240ca3f45e5925c574912a2d6e682` | 1,920 |

Each panel contains 8 parents by 8 children by 30 whole-template families.
C4 and C5 are separately generated controlled natural-language expression
panels. They are not an unrestricted organic corpus.

### B3. Fixed split and targets

Within each panel, sort the 30 unique `template_family_id` strings by the byte
sequence of `SHA256(template_family_id)`, breaking impossible hash ties by the
literal string. The first 15 families form half A and the remaining 15 form
half B. This split is label-independent, balanced by construction, saved as a
manifest, and reused at every block and for every task.

The only target parents are `mathematics` and `physics`. They may not be added,
removed, or replaced after extraction begins.

## C. Frozen Fisher estimator and seven-dimensional spaces — CONFIRMED

For panel \(p\), block \(\ell\), and half \(s\), let
\(x_i\in\mathbb{R}^{2048}\) be the captured native representation. First fit one
task-independent within-leaf metric from all 64 parent--child leaf classes.
If \(q_i\) is the complete leaf label and \(\mu_{q_i}^{leaf}\) its mean, define
\(E_i=x_i-\mu_{q_i}^{leaf}\). Fit Ledoit--Wolf shrinkage once to all rows \(E_i\)
and call it \(\widehat W_{p,\ell,s}\). This same matrix is frozen for the coarse
task, both target-parent fine tasks, and every label permutation in that
panel/block/half.

For any one \(K=8\) classification task, let \(\mu_k\) and \(\mu\) denote its class
and pooled means. Define the class-contrast matrix

\[
M=[\sqrt{n_1}(\mu_1-\mu),\ldots,\sqrt{n_8}(\mu_8-\mu)].
\]

\[
S=\operatorname{orth}(\widehat W_{p,\ell,s}^{-1}M).
\]

Equivalently, its directions are the nonzero generalized eigenvectors of
\(MM^\top v=\lambda\widehat W_{p,\ell,s}v\). Numerical code may use a stable linear solve
or dual identity, but must pass a small-dimensional identity test against an
explicit solve. Basis vectors are Euclidean-orthonormalized only after the
common Fisher solve.

The coarse space \(S_C\) uses all 1,920 panel rows and the eight parent labels.
The fine space \(S_{F\mid c}\) uses the 240 rows inside fixed parent \(c\) and its
eight child labels, while still using the common all-leaf \(\widehat W\) fitted
above. Each half contains 960 coarse rows and 120 rows for each target parent.
The requested dimension is always \(r=K-1=7\); no lower-rank space is silently
substituted.

### C1. Rank gate

For every task/half, independently permute labels 200 times under the exact
balanced template-cluster scheme in Section E. The observed seventh
generalized Fisher eigenvalue must exceed the permutation 95th percentile.
All four spaces \(S_C^A,S_C^B,S_F^A,S_F^B\) must pass for a panel-parent-layer
cell to be eligible.

## D. Metrics and common scales — CONFIRMED

For Euclidean-orthonormal rank-seven bases \(U,V\), define

\[
\Omega(U,V)=\frac{\lVert U^\top V\rVert_F^2}{7}
=\frac{1}{7}\sum_{j=1}^{7}\cos^2\theta_j.
\]

### D1. Raw cross-half alignment

\[
A=\frac{1}{2}\left[
\Omega(S_C^A,S_F^B)+\Omega(S_C^B,S_F^A)
\right].
\]

The seven reported principal-angle values are the elementwise mean of the
descending squared singular values from the two cross-half comparisons. Their
mean must equal \(A\) to numerical tolerance.

### D2. Same-task reproducibility reference

\[
R_C=\Omega(S_C^A,S_C^B),\qquad
R_F=\Omega(S_F^A,S_F^B),\qquad
C=\sqrt{R_CR_F}.
\]

\(C\) is the empirical reconstruction ceiling/reference, not a population upper
bound.

### D3. Corrected overlap

\[
A^{\mathrm{corr}}=A/C.
\]

This is an empirical stability correction, not a strictly unbiased estimator.
It may exceed 1 and must never be clipped. It is not interpreted when the
validity gates fail.

### D4. Unified comparison scales

The raw-overlap plot compares quantities on the same raw \([0,1]\) projector
scale: Haar rank-seven expectation and interval, matched label-permutation
null, observed \(A\), and empirical reference \(C\).

The corrected plot compares quantities on the same ratio scale: matched-null
overlap divided by the same \(C\), observed \(A/C\), and the reference value 1.
The two scales are shown separately and are never mixed on one ordinate.

The intervals 0.25 and 0.75 are descriptive labels only. They are not theory,
pass/fail thresholds, or architecture gates.

## E. Nulls, stability gate, and fixed randomization — CONFIRMED

### E1. Label permutation null

Use 200 replicates with root seed `150901`. For the coarse task, within every
template family permute the eight parent labels across the 64 balanced
parent-child rows. For a target fine task, within every template family and
target parent permute its eight child labels across the eight rows. Apply each
permutation separately to A and B before fitting spaces. This preserves sample
counts and template clustering while breaking the corresponding semantic
mapping.

The matched raw-alignment null fits independently permuted coarse and fine
spaces across A/B and computes the same \(A\) formula. Same-task stability nulls
fit independently permuted copies of the same task and compute the same \(R\)
formula.

### E2. Haar baseline

Use 10,000 independent pairs of Haar-distributed rank-seven subspaces in
\(\mathbb{R}^{2048}\) with root seed `150902`. Report mean, 2.5th, 50th, and
97.5th percentiles of \(\Omega\). Haar is a geometric reference, not the
finite-sample task null.

### E3. Cell validity

A panel-parent-layer cell is valid only if:

1. all four requested spaces pass the seventh-eigenvalue rank gate;
2. both \(R_C\) and \(R_F\) exceed their matched permutation 95th percentiles;
3. \(C\) exceeds the matched raw-alignment-null 95th percentile;
4. every tensor, eigenvalue, and metric is finite and the principal-angle
   identity holds.

An invalid cell remains in every table and plot position as `Insufficient`.
It is never dropped or replaced. Its raw diagnostics remain reportable, but its
corrected value and trajectory inference are ineligible.

## F. Cross-depth analysis and plots — CONFIRMED

### F1. Per-panel analysis

C4 and C5 are analyzed separately before comparison. For each panel and target
parent, report all six raw cells in block order, including invalid cells.

If all six cells are valid, compute Spearman \(\rho\) between block number and
corrected overlap with the exact two-sided permutation \(p\) over all \(6!\) layer
orders. Spearman is an auxiliary monotonicity description, never the sole
verdict. If any layer is invalid, the complete six-layer trend is
`Insufficient`; no complete-case deletion is allowed.

Define fixed stage means:

\[
\text{shallow}=\operatorname{mean}(4,12),\quad
\text{middle}=\operatorname{mean}(20,28),\quad
\text{deep}=\operatorname{mean}(36,44).
\]

Report the stage ordering. A middle-stage maximum or minimum is called
non-monotone only when the middle mean is strictly above or below both adjacent
stage means and the two adjacent differences have opposite signs. Otherwise
report the literal six-layer trajectory and stage ordering without forcing a
shape label.

### F2. Replication across panels

For each parent, report the Spearman correlation between the six C4 and six C5
corrected trajectories when all twelve cells are valid. A monotone direction
replicates only when C4 and C5 Spearman signs agree. A staged/non-monotone
description replicates only when stage ordering and middle-extremum type agree.
Any disagreement is reported as non-replication, not averaged away.

### F3. Required core figures

1. Per-layer mathematics/physics raw overlap, with matched permutation null,
   Haar baseline, and empirical reproducibility reference, faceted by C4/C5.
2. Block-to-corrected-overlap trajectories for mathematics and physics,
   showing C4 and C5 separately and marking invalid cells.
3. Seven principal-angle \(\cos^2\) heatmaps across blocks, with separate panels
   and target parents.

Every figure must state the metric, unit, data source, validity marks, allowed
conclusion, and limitation. Rendered files must be visually inspected.

## G. Execution contract — CONFIRMED

### G1. Worker and immutable run root

Worker code and raw outputs live under:

`/data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse`

Every run receives a new timestamped directory and refuses overwrite.
Research_System receives only curated Protocol, Summary, Detailed, and core
figures after evidence exists.

### G2. Ordered stages and acceptance

| Stage | Reads labels? | Required output | Acceptance / stop rule |
| --- | --- | --- | --- |
| local unit tests | synthetic labels only | test log | all estimator, split, metric, invalid-cell, and plot-contract tests pass |
| remote preflight | schema only | provenance receipt | exact hashes, model config, GPU tuple, and package compatibility pass |
| remote smoke | no semantic metric | hook/replay and shape receipt | fixed six hooks, 2 panels, final-token shape 2048, finite output, deterministic repeat, immutable ordering |
| full extraction | no analysis | two activation stores | all 3,840 rows and six blocks complete with checksums |
| frozen analysis | yes | complete metric tables | all registered cells/nulls/gates present; invalid cells retained |
| render/audit | yes | three figures and audit | identities pass and rendered artifacts are inspected |

The smoke may use a fixed label-blind prefix of 16 rows per panel. It may not
compute Fisher spaces, overlap, principal angles, rank gates, or trends.
Passing smoke authorizes continuation inside the same already-approved job; it
does not authorize any scientific amendment.

### G3. Resources

Preferred submission tuple:

| Field | Value |
| --- | --- |
| surface | ACP |
| workspace | `share-space` |
| AEC2 cluster | `computing-cluster-5090-01g` |
| worker spec | `n12lp.nn.i10a.8` |
| nodes | 1 |
| quota | `spot` |
| GPUs | 8 x RTX 5090 |
| storage | AFS mount `01995892-d478-76d8-aec7-13fd8284477e:/data` |

If the eight-GPU profile has no capacity, the user has authorized a four-RTX
5090 fallback in principle. Before that fallback is submitted, the actual
non-debug four-GPU cluster/spec tuple must be queried, printed, and recorded.
The fallback may alter only model sharding and wall-clock time.

The 2026-08-27 live pool audit resolved that fallback as
`share-space / computing-cluster-5090-01g / n12lp.nn.i10a.4 / one node / spot /
four RTX 5090 GPUs / the same AFS mount`. This value came from active jobs on
the non-debug pool; it was not inferred from the eight-GPU spec.

### G4. Failure and amendment policy

- Queue wait is monitored; a zero-replica preferred job may be stopped only
  before it starts and only to enter the authorized resource fallback.
- OOM, package incompatibility, hook mismatch, preemption with incomplete
  artifacts, data-hash mismatch, or smoke failure stops the pipeline before
  scientific analysis.
- A scientific change requires a new human-approved amendment and new run ID.
- No result-driven substitution, threshold repair, extra parent, extra layer,
  or hidden rerun is allowed.

## H. Cross-block consistency audit

| Check | Status |
| --- | --- |
| question matches Anchor and Focus | PASS |
| object matches actual native MoE input | PASS |
| fixed selections cover the user-approved design | PASS |
| Fisher dimension, estimator, and rank gate agree | PASS |
| raw, null, reference, corrected, and angle scales agree | PASS |
| invalid-layer policy agrees across metrics and trends | PASS |
| C4 primary / C5 replication roles remain separate | PASS |
| monotone, staged, and non-monotone outcomes are all allowed | PASS |
| smoke is label-blind and full run is explicitly approved | PASS |
| Router training remains unauthorized | PASS |

**Final protocol verdict:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`.

## I. Append-Only Post-Completion Supplement: Coarse--Fine Covariance-Spectrum Location

```text
Amendment status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
Added after original result unsealing: 2026-08-28
Original eligibility and verdict impact: NONE
Purpose: locate the already-frozen coarse and conditional-fine Fisher spaces
         along each layer's empirical activation-covariance spectrum
Execution approved: implementation, smoke, and full cached-activation analysis
Human amendment: sort all 2,048 covariance directions by decreasing variance
                 and divide them into 16 fixed bands of 128 directions
```

This is a post-completion, non-decision-bearing companion diagnostic requested
after the original result was known. It must not alter the original estimator,
24-cell eligibility, overlap/null comparison, depth result, or claim boundary.
Its only new question is whether the already-estimated coarse and fine
directions concentrate in the same broad variance region even though their
directions themselves showed null-subordinate overlap.

### I1. Frozen inputs and exclusions

- Reuse the immutable C4/C5 activation arrays and metadata from
  `full-20260827T163900Z`; do not run Qwen3-30B-A3B again.
- Keep Blocks 4, 12, 20, 28, 36, and 44, the A/B template-family split,
  mathematics, physics, rank seven, the shared Ledoit--Wolf Fisher estimator,
  and the 200 matched label permutations unchanged.
- Analyze C4 and C5 separately. C5 remains an independent replication panel;
  no pooled C4+C5 covariance basis is used for the primary supplement.
- Do not select layers, principal-component bands, plot limits, or wording from
  the observed spectrum.
- The supplement cannot establish Router use, causal importance, functional
  sufficiency, or that two spaces share directions merely because they occupy
  the same broad variance band.

### I2. Per-panel, per-layer empirical covariance basis

For panel \(p\) and block \(\ell\), stack all 1,920 frozen activations before
reading labels:

\[
H_{p,\ell}\in\mathbb R^{1920\times2048},\qquad
\widetilde H_{p,\ell}=H_{p,\ell}-\mathbf 1\bar h_{p,\ell}^{\top}.
\]

Compute the complete symmetric eigendecomposition

\[
\frac{\widetilde H_{p,\ell}^{\top}\widetilde H_{p,\ell}}{1920-1}
=V_{p,\ell}\Lambda_{p,\ell}V_{p,\ell}^{\top},
\]

with

\[
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_{2048}\ge0.
\]

Let \(r_{\mathrm{emp}}\) be the number of covariance eigenvalues above the frozen
numerical threshold

\[
\lambda_j>\lambda_1\left[\epsilon_{\mathrm{float32}}
\max(1920,2048)\right]^2.
\]

Because one centered panel has rank at most 1,919, the last at least 129
eigenvectors span an empirically zero-variance subspace whose individual basis
vectors are not identifiable. All 2,048 indices are nevertheless retained to
honor the approved equal-width partition. For every fitted Fisher space \(U\),
record its energy outside the identifiable empirical span

\[
e_{\perp}(U)=1-\lVert V_{[:,1:r_{\mathrm{emp}}]}^{\top}U\rVert_F^2/7.
\]

If \(e_{\perp}(U)>10^{-5}\), keep the cell and mark its spectral localization
`INSUFFICIENT`; do not renormalize it away. Band 16 is always labeled
`EMPIRICAL_NULL_BAND` and is never given a semantic interpretation.

### I3. Direction-wise and band-wise location metrics

The 16 primary descriptive bands are fixed by covariance-rank index, not by
cumulative explained variance. Band \(b\in\{1,\ldots,16\}\) contains

\[
J_b=\{128(b-1)+1,\ldots,128b\}.
\]

If \(V_b=V_{[:,J_b]}\in\mathbb R^{2048\times128}\), define the direct
discriminant-to-band alignment

\[
a_b(U)=\frac{\lVert V_b^{\top}U\rVert_F^2}{7},\qquad
\operatorname{Enrich}_b(U)=\frac{a_b(U)}{128/2048}=16a_b(U).
\]

Thus \(a_b\) is the fraction of a seven-dimensional Fisher space lying in that
128-dimensional covariance band, and the 16 values sum to one up to numerical
tolerance. The uniform ambient-space reference is \(1/16=0.0625\) per band;
enrichment one is exactly that reference. Because the fitted Fisher spaces are
constrained by the finite empirical sample span, the matched label-permutation
distribution remains the inferential reference; \(0.0625\) is descriptive only.

Compute these quantities separately for

\[
U_C^A,\ U_C^B,\ U_{F\mid\mathrm{math}}^A,\
U_{F\mid\mathrm{math}}^B,\ U_{F\mid\mathrm{physics}}^A,\
U_{F\mid\mathrm{physics}}^B.
\]

For each task, report the A/B mean and both individual estimates. A band
location is called reproducible only when C4 and C5 have the same enrichment
side relative to one and the A/B estimates within both panels agree on that
side. Otherwise report the literal values as panel- or split-dependent.

### I4. Matched semantic-null comparison

Reuse the original 200 within-template label permutations and refit the same
Fisher spaces against the fixed, label-blind covariance bands. For every task,
panel, layer, and band, report the observed \(a_b\) and
\(\operatorname{Enrich}_b\) beside the permutation median and 95% interval.
This separates semantic-label localization from localization induced by the
shared covariance and Fisher estimator. It remains a secondary comparison and
cannot change the original coarse--fine overlap verdict.

### I5. Required outputs and reading rule

1. `spectral_band_alignment.csv`: all 16 equal-width-band alignments \(a_b\),
   enrichment, A/B agreement, matched-null summaries, and off-span energy.
2. `figure4_coarse_fine_band_alignment.png`: 16-band observed alignment
   heatmaps for coarse, mathematics-fine, and physics-fine spaces, with C4/C5
   and A/B estimates retained.
3. `figure5_coarse_fine_band_null_excess.png`: observed minus matched-null
   median alignment, with the matched-null 95% interval marked.
4. `spectral_location_audit.json`: shape, energy-conservation, empirical-rank,
   off-span, permutation-completeness, and render-audit checks.

The interpretation order is fixed:

1. first retain the original result that coarse--fine directional overlap did
   not exceed the matched semantic null;
2. then report which of the 16 fixed covariance-rank bands each space aligns
   with beyond its matched null;
3. if coarse and fine occupy the same band, say only that they share a broad
   variance region, not that they share directions;
4. if they occupy different bands, say only that their spectral locations
   differ in these panels, not that either band is causally used by the Router.

The researcher approved implementation, smoke, and full cached-activation
execution on 2026-08-28. Use a new immutable supplement run ID and append its
evidence to `summary.md` and `detailed.md` without rewriting the original
registered result.

### I6. Pre-Full-Run Amendment Ledger

```text
Amendment: SPECTRAL-BAND-v2
Timing: after one-layer implementation smoke, before the full 12 panel-layer run
Observed engineering fact: Block-4 C4 covariance had empirical rank 1,884 and
                           the two coarse half-spaces had 0.000324/0.000355
                           energy below that numerical-rank threshold, while
                           all 16 bands summed to one within 4e-9
Before: off-span energy above 1e-5 made spectral localization INSUFFICIENT
After: off-span energy is retained as a mandatory numerical-limit diagnostic;
       it does not invalidate the all-2,048-direction band decomposition
Reason: the researcher explicitly selected all 2,048 directions / 16 bands;
        using a numerical-rank threshold to delete an otherwise energy-
        conserving layer contradicts that estimand
Eligibility impact: the supplement remains descriptive; Band 16 and every
                    below-threshold component remain ineligible for semantic
                    interpretation, but the layer is not dropped
Original A15_09_E01 verdict impact: NONE
```

The first attempted full supplement run was stopped before producing result
tables because a float32 covariance eigensolve reported empirical rank 1,931
for a centered \(1920\times2048\) matrix, exceeding the algebraic maximum 1,919.
The root cause was round-off from explicitly forming \(H^\top H\). The eligible
implementation therefore obtains the same covariance eigenvectors from the
complete right-singular-vector matrix of centered \(H\) and obtains empirical
rank from its singular values. This is an algebraically identical solver
repair, not a change to bands, spaces, metrics, nulls, or interpretation.
The interrupted directory is ineligible and a new immutable run ID is required.

### I7. Execution Receipt

```text
Interrupted ineligible run:
  /data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/spectral-band-20260828T042753Z
Eligible completed run:
  /data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/spectral-band-20260828T043411Z
Completion status: PASS_WITH_NUMERICAL_LIMIT
Rows: 1,728 / 1,728
Matched permutations: 200 per half and task
Maximum 16-band energy-sum error: 2.680078381445128e-13
Maximum below-numerical-rank energy: 0.00012279702394812908
Runtime: 526.062 seconds
```

Curated evidence:

- `tables/spectral_band_alignment.csv`, SHA-256
  `80847d8567105ebab9d627a80831edd3df7491b35cd4a7bd518d47aa90362d92`;
- `tables/spectral_location_audit.json`, SHA-256
  `1630ff95e0209b591ed074e3123da4d15c2be6b8155714ab8e2e45c5114af853`;
- `figures/figure4_coarse_fine_band_alignment.png`, SHA-256
  `67121220e316fa804d20f193f10966364298c785898f463fe48f7471a4f02733`;
- `figures/figure5_coarse_fine_band_null_excess.png`, SHA-256
  `bd18b44b1bf230b6219f22bbf71100046c5471b867e5dcfb9e22a0b4ab4441e6`.

This receipt records execution only. The original overlap verdict remains
unchanged, and supplement interpretation awaits the researcher's result
wording before Summary or Detailed is revised.

## J. Append-Only Template Sensitivity Check For Covariance-Band Numbering

Amendment status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`

The researcher approved this bounded check on 2026-08-28. It asks whether a
covariance band keeps the same number and directions when the covariance is
estimated from different whole template families. It does not recompute or
change the registered coarse--fine Fisher-overlap result.

### J1. Frozen treatment and matched control

For every panel and frozen Block 4/12/20/28/36/44, the treatment uses the
existing whole-template split: half A contains 15 template families and half B
contains the other 15. Each half contains 960 rows, with exactly 15 rows from
every parent--child leaf.

The matched finite-sample control uses 50 fixed random splits. Within each of
the 64 parent--child leaves, 15 of its 30 rows are assigned to one half and the
other 15 to the second half. Thus both halves still contain 960 rows and have
the same labels as the treatment, but both mix template families. The root
seed is `150903`; no seed, layer, panel, band, or repeat may be selected after
seeing results.

Each half is centered independently. Its covariance eigensystem is obtained
from the complete float64 right-singular-vector matrix of the centered native
representation. Let \(V_a^A,V_b^B\in\mathbb R^{2048\times128}\) be bands \(a\)
and \(b\). The frozen transition matrix is

\[
T_{ab}=\frac{\lVert (V_a^A)^\top V_b^B\rVert_F^2}{128}.
\]

The primary exact-number retention is

\[
D_{1:7}=\frac{1}{7}\sum_{b=1}^{7}T_{bb}.
\]

The secondary same-or-adjacent retention is

\[
L_{1:7}=\frac{1}{7}\sum_{b=1}^{7}
\sum_{j=\max(1,b-1)}^{\min(16,b+1)}T_{bj}.
\]

Per-band diagonal and local retention are retained as diagnostics. The full
C4--C5 transition matrix estimated from all 1,920 rows is a secondary
cross-panel check; because C4 and C5 differ in more than one wording property,
it is not a pure template causal contrast.

### J2. Identifiability and fixed interpretation

A centered 960-row half has rank at most 959. Therefore only Bands 1--7
(directions 1--896) are fully identifiable. Band 8 is only partly identifiable,
and Bands 9--16 contain sample-null directions whose basis is not unique. The
primary verdict is restricted to Bands 1--7; the remaining bands are displayed
only as numerical diagnostics and cannot support a template conclusion.

At each panel and layer, the whole-template value is compared with the fixed
random-split empirical 2.5%, 50%, and 97.5% quantiles on the same scale:

- \(D_{1:7}\) below the 2.5% control quantile: evidence that whole-template
  change alters exact band numbering beyond matched finite-sample variation;
- \(D_{1:7}\) inside the control interval: no excess template sensitivity is
  established at that panel and layer;
- low \(D_{1:7}\) but control-compatible \(L_{1:7}\): mainly adjacent-band drift;
- both \(D_{1:7}\) and \(L_{1:7}\) below control: broader coordinate rotation.

C4 and C5 are reported separately. A replicated statement requires the same
typed pattern in both panels; no global monotonic, causal, or Router-functional
claim is allowed. The Haar expectation \(128/2048=0.0625\) is retained only as a
geometric reference; the matched random split is the decision reference.

### J3. Required immutable outputs

1. the treatment and all 50 matched-control transition matrices and ranks;
2. a CSV containing per-panel, per-layer exact and local retention with control
   quantiles and typed result;
3. whole-template transition heatmaps, with the Band-8 identifiability boundary
   marked;
4. layerwise \(D_{1:7}\) and \(L_{1:7}\) plots against matched-control intervals;
5. the full-sample C4--C5 transition matrix as a secondary figure;
6. an audit JSON checking row balance, split disjointness, transition row sums,
   finite values, ranks, repeat completeness, and rendered artifacts.

Use a new immutable run directory under the existing worker surface. Cached
activations are the only model-derived input; no model forward pass, Fisher
refit, classifier training, or Router training is authorized.

### J4. Execution Receipt

```text
Implementation smoke:
  /data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/template-band-stability-smoke-20260828T045823Z
Eligible completed run:
  /data/250010109/MoE_Router/experiments/20260827_a15_09_e01_qwen3_30b_cross_depth_coarse_fine_reuse/runs/template-band-stability-20260828T045843Z
Completion status: PASS
Panels x layers: 2 x 6
Matched mixed-template controls: 50 per panel and layer
Treatment split: 960/960 rows, 15/15 disjoint whole template families,
                 15 rows per half in every parent--child leaf
Maximum transition row-sum error: 5.883071807488705e-13
Runtime: 492.906 seconds
```

Direct registered outputs: whole-template exact-number retention over fully
identifiable Bands 1--7 was 0.2271--0.2736 in C4 and 0.2321--0.2741 in C5.
At all 12 panel--layer cells it was below every one of the 50 matched-control
draws, by 0.0038--0.0088 absolute in C4 and 0.0072--0.0101 in C5 relative to
the control median. Same-or-adjacent retention was also below every matched
control draw at all 12 cells. Under the frozen typed rule, all 12 cells are
`BROADER_ROTATION` rather than adjacent-band drift.

Curated evidence:

- `tables/template_band_stability.csv`, SHA-256
  `a5b286254bd2be11bcc23751dccc61b91234ac09f6bd3cd08d9b82d07e3503c1`;
- `tables/template_band_stability_audit.json`, SHA-256
  `0d300dbb5c297fa69e4c5dea081256f67f3057ccf50cbae31db4d52854779f98`;
- `figures/figure6_template_split_band_transition.png`, SHA-256
  `ea7b9e52d3cd2fce4ca0860a5ba8113ab71817720ed1b1e447aa023ff3788cee`;
- `figures/figure7_template_split_retention_vs_control.png`, SHA-256
  `76b2dc24e88d584d5476eaa7b452539a3520a8179167f2e687a040a7ecef8e6c`;
- `figures/figure8_c4_c5_band_transition.png`, SHA-256
  `76e345c491f0b88d5528df0b9a3e9ee59f2d57f75faf440750894d8ae23f815a`.

The complete treatment/control matrices remain in the immutable worker run.
This receipt does not revise the original coarse--fine overlap verdict. The
human still owns any Summary/Detailed wording that turns this direct result
into a knowledge update.
