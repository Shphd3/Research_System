# Protocol: A15_09_01_E01 Native-G Domain Consensus And Variance Atlas

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
Approval status: researcher confirmed design and all execution scopes on 2026-08-28
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, smoke, full run
Design frozen at: 2026-08-28, revision v1
Purpose: test whether E06 shared-rank compression is explained by stable label-dependent reuse among eight local Native-G spaces
Primary Anchor: 15_09_01_native_g_domain_consensus_variance_atlas
Experiment role: root-cause audit
Primary metric: Block-46 equal-pair mean rank-seven projector overlap versus matched label-permutation distribution
Minimal setup: frozen Qwen3-30B-A3B cached G=X+U; eight parent-conditioned eight-class tasks; Block 46 primary; all 48 blocks secondary
Pass: validity gates pass and Block-46 observed mean overlap exceeds matched-permutation 97.5th percentile
Fail: validity gates pass and observed mean does not exceed that percentile
Insufficient: any rank, reproducibility, identity, finiteness, or artifact guard fails
Cannot claim: native Router use, expert utility, causal necessity, nonlinear structure, or training gain
Approval decision: execute without another design-review round; do not create Summary, Detailed, or daily report in this iteration
```

Active Focus: [focus_native_g_domain_consensus_variance_atlas.md](/daily_research_reports/backup/2026/08/0828/meeting_reports/focus_native_g_domain_consensus_variance_atlas.md)
Primary Anchor: [15_09_01_native_g_domain_consensus_variance_atlas_anchor.md](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/subanchors/15_09_01_native_g_domain_consensus_variance_atlas_anchor.md)

## 1. Terminology / Definitions

- **Native Router input $G$:** the final decision-token vector $X+U$ passed to the same block's MoE gate and experts; this experiment measures its offline linear geometry only.
- **Local discriminant space:** the rank-seven input column space of a reduced-rank ridge coefficient distinguishing eight children inside one known parent domain.
- **Raw-coordinate space:** a discriminant coefficient learned after TRAIN coordinate standardization and mapped back by inverse TRAIN standard deviations before QR orthonormalization.
- **Projector overlap:** $\Omega(Q_1,Q_2)=\lVert Q_1^\top Q_2\rVert_F^2/7$, unitless in $[0,1]$.
- **Matched label-permutation null:** the same fit after permuting child labels within each parent and template family, preserving representations, row counts, domains, templates, covariance, rank, and estimator.
- **Same-task reproducibility:** mean pairwise projector overlap among three leave-one-TRAIN-template-family-out fits of the same domain task.
- **Consensus spectrum:** eigenvalues of the average of eight local projectors.
- **Variance enrichment:** fraction of a discriminant or consensus space inside a raw TRAIN principal-component band divided by that band's ambient dimension fraction.

## 2. Anchor Alignment — CONFIRMED

The experiment tests the Anchor's sole unknown: whether Block-46 local Native-G spaces share stable label-dependent directions beyond a covariance-preserving null. E06's retrospective $G$ ranks motivate the question but do not determine its result. The claim stops at offline linear geometry.

## 3. Tested Hypothesis — CONFIRMED

If shared-rank compression reflects direction reuse, all eight local spaces will be rank-valid and reproducible, and their Block-46 mean overlap will exceed the matched-permutation 97.5th percentile. If covariance or estimator bias explains the overlap, the observed statistic will lie inside the matched null. If the spaces do not reproduce, the mechanism is unidentified.

## 4. Rival Explanations — CONFIRMED

1. shared input covariance produces aligned supervised coefficients even after labels carry no semantics;
2. coordinate standardization changes Euclidean orientation;
3. finite template families yield unstable fitted directions;
4. visual layer selection creates a false depth story.

Matched permutations address (1), raw-coordinate back-mapping addresses (2), leave-one-family-out reproducibility addresses (3), and Block 46 plus a max-over-layers null addresses (4).

## 5. Data Construction And Provenance — CONFIRMED

Source tensor:
`/data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation/runs/e02-all-layer-full-20260824T014000Z/extraction/objects.npy`

Manifest identity: `cba20c5e3eb484a82c03246f6471b8da1e1c1a40f29c7cde9a037a99fa8ea144`; shape `[48, 19200, 2, 2048]`; objects are $X$ and $U$. Metadata has 11,520 TRAIN, 2,560 DEVELOPMENT, 2,560 same-template TEST, and 2,560 new-template TEST rows; eight parents, eight children per parent, and five template families overall. TRAIN contains only the three same-template families; the other two families are confined to new-template TEST and remain excluded from fitting. The source taxonomy and rows remain frozen. Only $G=X+U$ is constructed.

TRAIN fits statistics, spaces, nulls, covariance, and PCA. DEVELOPMENT supplies the already frozen per-layer ridge selected by the predecessor layer scan. TEST labels cannot select ranks, layers, bands, thresholds, plot ranges, or wording. All results are retrospective because these panels were previously opened.

## 6. Learning Task And Permitted Supervision — CONFIRMED

For each block and known parent, the permitted input is $G\in\mathbb R^{2048}$ and the target is the eight-way child label. The parent label is a task selector, not a prediction target. Child labels are used only on TRAIN for coefficient fitting and DEVELOPMENT for the predecessor ridge selection. The output is a rank-seven input space, not a deployed classifier.

## 7. Model / Architecture And Frozen Variants — CONFIRMED

The scientific estimator is the existing E06 reduced-rank ridge coefficient. Each of the eight tasks is fit independently. The requested rank is always seven for the primary comparison; no lower rank replaces a failed space. A sensitivity table may report DEVELOPMENT-retention ranks six or seven but cannot change the verdict. No neural model is trained and no model forward pass is required.

## 8. Training Objective And Optimization — CONFIRMED

For standardized TRAIN input $Z_d$ and centered one-hot child target $Y_d$, ridge regression minimizes

$$
\lVert Y_d-Z_dW_d\rVert_F^2+n_d\lambda_\ell\lVert W_d\rVert_F^2.
$$

$\lambda_\ell$ is the frozen layer-specific value from the predecessor DEVELOPMENT scan. Singular value decomposition of $W_d$ supplies its seven-dimensional input column space. The coefficient is then mapped to raw coordinates by inverse TRAIN feature scale and QR orthonormalized.

## 9. Conditions, Seeds, And Checkpoints — CONFIRMED

| Condition | Value | Role |
| --- | --- | --- |
| Primary block | 46 | only verdict-bearing layer |
| Atlas blocks | 1--48 | secondary depth description |
| Local tasks | 8 parents $\times$ 8 children | fixed rank-seven spaces |
| Leave-family-out fits | 3 per domain and layer, one for each TRAIN family | reproducibility guard |
| Label permutations | 200 | matched semantic null |
| Permutation seed | 150911 | reproducibility |
| PCA bands | cumulative variance 0--50%, 50--90%, 90--100% | variance location |
| Uniform-subspace draws | analytic $7/2048$ reference plus 10,000 draws only if needed for plotting | geometric reference, not verdict |
| Smoke | Blocks 4 and 46, two domains, four permutations | code/schema guard only |

There are no checkpoints. Full-run outputs use a timestamped, refuse-to-overwrite run root.

## 10. Primary Metric And Frozen Analysis Plan — CONFIRMED

For block $\ell$, compute all 28 pair overlaps and their equal-pair mean $T_\ell$. For each permutation replicate, independently permute child labels inside every `(parent, template_family)` group, refit all eight spaces, and recompute the same $T_\ell$. Block 46 passes only when $T_{46}$ is strictly above the empirical 97.5th percentile.

Validity requires every observed full coefficient to have numerical rank seven, every domain's leave-one-family-out mean reproducibility to exceed its matched-permutation 95th percentile, all arrays to be finite, orthonormality error below $10^{-5}$, and the mean of seven principal-angle $\cos^2$ components to match projector overlap within $10^{-8}$.

The observation unit is one row. The independence unit is a template family. Domain pairs are an exhaustive fixed set, not 28 independent replicates. Permutation uncertainty is conditional on the frozen 19,200-row dataset. No outlier is removed. Missing or invalid layers remain present as `INSUFFICIENT`.

For the secondary atlas, compare each $T_\ell$ with its per-layer permutation distribution and with the distribution of $\max_{\ell=1}^{48}(T_\ell^{perm}-\operatorname{median}T_\ell^{perm})$. The latter controls visual layer selection. Spearman depth correlation is descriptive only.

## 11. Secondary Metrics And Guards — CONFIRMED

1. all 28 Block-46 raw and null-corrected overlaps;
2. seven principal-angle $\cos^2$ components per pair;
3. eigenvalues and directions of the average eight-domain projector;
4. raw-coordinate PCA spectrum and head/middle/tail enrichment for local and admitted consensus directions;
5. existing DEVELOPMENT balanced-accuracy trajectory as a readability reference;
6. standardization-versus-raw-coordinate overlap sensitivity;
7. full 48-layer metric completeness and finite-value audit.

Secondary metrics cannot rescue a failed or insufficient Block-46 verdict.

## 12. Known Good / Known Bad / Known Confusing Cases — CONFIRMED

- **Known good:** identical and sign-rotated rank-seven bases must have overlap one; a synthetic shared three-direction construction must exceed its matched null.
- **Known bad:** orthogonal rank-seven bases must have zero overlap; label-permuted real tasks should define the null rather than pass by construction.
- **Known confusing:** two unstable fitted spaces can have nonzero point overlap; the reproducibility guard must type this `INSUFFICIENT` rather than shared or separate.

## 13. Scientific Procedure And Stage Contracts — CONFIRMED

| Stage | Goal | Input and assumptions | How | Why | Expected output | Pass / fail / insufficient | Named failure | Artifact | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| preflight | verify frozen source | objects, metadata, manifests | identity, shape, split, balance, finiteness checks | prevent source drift | receipt | all checks pass / stop | data failure | `preflight.json` | smoke |
| smoke | validate estimator and metrics | two blocks, two domains | run real pipeline with four permutations plus synthetic cases | catch coordinate and null bugs | compact tables and figures | all unit and schema guards pass / stop | implementation failure | `smoke/` | full run |
| local spaces | identify task directions | TRAIN $G$, frozen ridge | full and leave-family-out ridge/SVD fits | estimate spaces and stability | bases and stability table | rank/reproducibility typed | estimator instability | `tables/local_spaces.csv` | overlap |
| matched null | separate semantics from covariance | same rows and estimator | 200 within-group permutations | strongest rival | null tables | complete / stop | null failure | `tables/nulls.csv` | verdict |
| consensus | locate shared geometry | eight valid spaces | pairwise angles and average projector eigensystem | answer which directions overlap | overlap matrix and spectrum | typed Block-46 verdict | metric failure | `tables/block46_*.csv` | variance atlas |
| variance atlas | locate directions by variance and depth | raw TRAIN $G$ | covariance eigenspectrum, band enrichment, 48-layer aggregation | explain geometry | tables and figures | complete or secondary missing | analysis failure | `tables/layer_atlas.csv` | chat report |

## 14. Algorithm, Output, And Provenance Contract — CONFIRMED

Worker code root:
`/data/250010109/MoE_Router/experiments/20260828_a15_09_01_e01_native_g_domain_consensus_variance_atlas/`

Expected full-run root:
`runs/full-<UTC timestamp>/`

Required outputs are `preflight.json`, `config.json`, `tables/block46_pairwise.csv`, `tables/block46_consensus_spectrum.csv`, `tables/layer_atlas.csv`, `tables/variance_enrichment.csv`, `results.json`, `completion_audit.json`, and three PNG figures. Raw fitted bases may stay on the worker surface. No Summary, Detailed, daily report, graph, root sync, commit, or push is authorized.

## 15. Success / Failure / Insufficient Evidence — CONFIRMED

- **Pass:** all validity guards pass and Block-46 observed mean overlap exceeds the matched-permutation 97.5th percentile. Allowed claim: stable label-dependent local spaces show excess geometric reuse at Block 46.
- **Fail:** all validity guards pass and the statistic does not exceed that percentile. Allowed claim: stable direction reuse is not supported as the explanation of E06 compression.
- **Insufficient:** any validity guard fails or required artifact is missing. Allowed claim: this estimator cannot adjudicate the reuse explanation.

## 16. What This Cannot Claim — CONFIRMED

No outcome establishes shared label meaning, native gate use, expert-relative utility, causal necessity or sufficiency, nonlinear structure, generalization beyond this taxonomy/model, or benefit from projection or Router training. PCA location is geometry, not utility.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question and boundary | CONFIRMED | researcher approved the stated MVP on 2026-08-28 |
| B data and provenance | CONFIRMED | verified cached E06 source and researcher approved reuse |
| C task and supervision | CONFIRMED | inherited E06 eight within-domain tasks |
| D estimator | CONFIRMED | reduced-rank ridge plus A15_09 null/principal-angle reuse |
| E optimization | CONFIRMED | predecessor DEVELOPMENT ridge, fixed rank seven |
| F evidence and verdict | CONFIRMED | researcher approved stability, matched null, PCA, and layer-trend analysis |
| G execution | CONFIRMED | implementation, smoke, and full run explicitly approved on 2026-08-28 |

Cross-block consistency audit: **PASS**.  
Scientific body frozen before implementation: **yes**.  
Post-start changes to data, estimator, rank, primary block, permutation scheme/count, validity gates, or verdict rule require an append-only amendment and eligibility ruling.

### Amendment A1 — 2026-08-28 TRAIN-family count correction

- **Trigger:** implementation preflight established that the five template families are not all present in TRAIN. TRAIN and same-template panels contain three families; the two remaining families occur only in new-template TEST.
- **Correction:** replace five leave-one-template-family-out fits with three leave-one-TRAIN-template-family-out fits. Matched permutations remain within `(parent, TRAIN template_family)` groups.
- **Reason:** using five folds is impossible on TRAIN; importing the two new-template TEST families would violate the frozen supervision boundary.
- **Unchanged:** source rows, representation, estimator, rank seven, Block 46 primary metric, 200 permutations, thresholds, validity logic, secondary atlas, and claim boundary.
- **Eligibility ruling:** `ELIGIBLE`. This corrects an impossible fold count without opening TEST or changing the primary estimand.
