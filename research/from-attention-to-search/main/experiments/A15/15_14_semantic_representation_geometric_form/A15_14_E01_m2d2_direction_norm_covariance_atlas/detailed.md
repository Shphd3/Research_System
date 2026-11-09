# Detailed: A15_14_E01 M2D2 Direction, Radius, and Covariance Atlas

Primary Anchor: [A15_14 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), including pre-extraction C001/C002  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE_FULL_RUN`; knowledge wording is `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

Purpose: identify whether frozen natural-language domain semantics are carried
by direction, radius, covariance shape, or a mixture.  
Hypothesis: direction is sufficient; the strongest rival is stable incremental
radius or covariance information.  
Experiment logic: fit label-blind geometry models on train, select restarts by
unsupervised objectives, and open labels only for confirmation scoring.  
Direct result: direction is the larger carrier, radius contribution passes the
registered rule in both tasks, and independent shape does not.  
Eligibility: all 16 full-run completion guards pass.  
Verdict: `RADIUS_CONTRIBUTING`.  
Claim boundary: the positive result is mean-pooled and does not transfer to the
single final-token guard.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Direction | where the centered vector points | \(u=z/\lVert z\rVert_2\) after train-only PCA | unit vector | semantic identity candidate | causal use |
| Radius | how long that centered vector is | \(r=\lVert z\rVert_2\) | PCA-coordinate length | intensity/familiarity candidate | meaning by itself |
| Shape | class-like density spread beyond one centroid | diagonal Gaussian mixture on \(z\) | NMI after clustering | covariance evidence | intrinsic ontology |
| NMI | agreement of cluster IDs and labels, invariant to ID permutation | normalized mutual information | 0--1 | primary accessibility score | expert utility or task gain |
| Radius permutation | keep every direction but reassign observed radii | \(\tilde z_i=r_{\pi(i)}u_i\) | NMI contrast | radius contribution control | perfect conditional-information decomposition |

## 2. Anchor Link And Decision Point

This experiment adjudicates the geometric-form clause of A15_14. It is
separate from the concurrent M2D2 next-token Router experiment. Its only
downstream decision is which Router-visible geometry deserves a later causal
test; it cannot itself promote a Router.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Resource | exactly 4 RTX5090, no H100 | four GeForce RTX5090 | passed | rank receipts; job `pt-zkuak3ej` | eligible |
| Data | 9,216 / 2,304 / 4,608 windows | exact counts, zero exact duplicate windows | passed | data manifest | eligible |
| Model | frozen Qwen3-0.6B-Base, 29 states | exact; three-parameter fingerprints unchanged on four ranks | passed | extraction receipts | eligible |
| Primary cell | mean pooling, hidden state 15, PCA-64 | exact | passed | atlas and primary results | eligible |
| Fits | five families, 20 restarts, coarse and conditional fine | 624 atlas rows including controls/sensitivity | passed | `atlas.csv` | eligible |
| Uncertainty | 10,000 bootstrap and 1,000 label permutations | exact | passed | score archives | eligible |
| Figures | audited decision figures | three rendered and visually inspected | passed | local `figures/` | eligible |

Execution history:

- `pt-ul0gol39` failed at platform startup before a run directory existed; no evidence was produced.
- `pt-l4czs4tk` exposed a startup-only manifest bug after verifying four RTX5090 devices; it failed before unit tests, data, or extraction.
- The single root fix allowed a base image that already provided the analysis dependencies. Local reproduction changed from exit code 1 to success and all tests remained green.
- `pt-zkuak3ej` completed the approved smoke and full run. The smoke passed 16/16 gates before full extraction began.
- Post-run analysis revision C004 replaced bootstrap-mean bars with the direct full-confirmation NMI point estimate and added the pre-registered pooling guard figure. Prediction arrays, bootstrap draws, intervals, nulls, thresholds, and typed verdict did not change. The analysis revision hashes are recorded under the worker run logs.

## 4. Actual Setup

Data: balanced M2D2-Wikipedia `3×3`: Culture and the arts (Mass media,
Performing arts, Visual arts), Health and fitness (Exercise, Nutrition, Public
health), and Natural and physical sciences (Biology, Earth sciences, Physical
sciences). Each fine domain contributes 1,024 train, 256 development, and 512
confirmation windows. Each window has 256 tokens; labels are metadata only.

Model: local Qwen3-0.6B-Base-official. No parameters receive gradients. There
is no optimizer, epoch, update, checkpoint, Router, or expert. Four GPUs shard
only inference windows.

Representation: embedding output plus 28 Transformer outputs. Primary pooling
averages positions 64--255. The final position is a guard. PCA is fit only on
train; the primary rank is 64. Ranks 32 and 128 are fixed-layer sensitivities.

Unsupervised models: log-radius Gaussian mixture, spherical k-means, von
Mises--Fisher direction mixture, Euclidean k-means, and diagonal Gaussian
mixture. Gold coarse labels define the global coarse evaluation and the parent
boundary for three separate fine evaluations; child labels never fit a model.

Code worker: `/data/250010109/MoE_Router/experiments/20260901_a15_14_e01_m2d2_direction_norm_covariance_atlas/`.  
Eligible run: `runs/full-20260901T181100Z/`.  
Data SHA-256: `fbcbc8e01d3b738d5fdc27059ce2eced757f3674f84bf70bbb17012cd31f6e7f`.  
Frozen Protocol SHA-256: `89e6a5820392cee01caea609e926055e37ed48df47be3b852ca020e73d0e8dc0`.

## 5. Metrics And Registered Decision Rules

The primary metric is confirmation NMI. `RADIUS_CONTRIBUTING` requires readable
direction plus either radius-only NMI above its label null or an observed-
minus-permuted-radius lower 95% confidence bound above 0.02. Independent shape
requires diagonal GMM to beat both direction and Euclidean centroid models by
lower bounds above 0.02 without radius explaining the gain.

Bootstrap resamples packed windows within all nine semantic cells. This
preserves balance but does not create document-level independence. Layer
curves are descriptive; only the fixed cell owns the verdict.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| direction readable | vMF above null | `primary_predictions.npz` | full NMI and 1,000 label nulls | coarse 0.1289 > 0.0014; fine 0.3223 > 0.0028 | eligible | pass | mean-pooled |
| radius associated | radius NMI above null | same | full NMI and matched null | coarse 0.0315 > 0.0011; fine 0.1397 > 0.0025 | eligible | pass | not conditional information alone |
| radius contributes to full density | observed-minus-permuted lower bound > 0.02 | predictions + bootstrap scores | 10,000 paired draws | coarse [0.1237, 0.1451]; fine [0.0321, 0.0619] | eligible | pass | model-family contrast |
| independent shape | both lower bounds > 0.02 | same | paired NMI differences | coarse lower bounds 0.0094/0.0088; fine 0.0162/0.0276 | eligible | fail | diagonal model rank-sensitive |
| token-level transfer | final-position guard retains signal | full atlas | same vMF fit family | block-14 coarse 0.0017; fine 0.0057 | eligible guard | not supported | one final position is not all token positions |

## 7. Main Results

At the fixed cell, direction is the larger carrier: its vMF NMI is 0.1289
coarse and 0.3223 fine, versus radius-only 0.0315 and 0.1397. Radius is not
zero: both radius-only null gates and both paired radius-permutation gates pass.
The correct reading is therefore “direction-primary, radius-contributing,” not
“radius-dominant.”

The diagonal model is highest at PCA-64, but its independent-shape rule fails.
Its rank sensitivity is also unstable: fine NMI is 0.4252 at rank 32, 0.3569
at rank 64, and 0.2055 at rank 128. Direction is much steadier: 0.3187, 0.3223,
and 0.3198. This reinforces the registered refusal to infer a necessary
covariance ontology.

The strongest boundary is pooling. At hidden state 15, final-position vMF NMI
is 0.0017 coarse and 0.0057 fine, compared with 0.1289 and 0.3223 after
whole-window mean pooling. The evidence therefore identifies a sequence-
aggregate domain representation, not a demonstrated token-Router input.

## 8. Visualization Results

### Direction is primary and radius contributes

![Fixed-cell carrier and radius meaning](figures/primary_geometry_and_radius_meaning.png)

How to read: compare radius-only with the two direction bars and full-vector
bars on the left. The right panel shows that projected radius at block 14 is
more negatively related to model surprise than positively related to lexical
rarity after domain means are removed.

At the primary layer, log projected radius has within-domain Spearman
\(\rho=-0.3235\) with NLL and \(\rho=0.0442\) with lexical rarity. Raw hidden norm
instead has \(\rho=-0.1175\) and \(\rho=0.2116\). These are descriptive
associations: projected radius looks more like predictability/familiarity,
while raw norm retains more rarity association.

### The signal depends on whole-window aggregation

![Pooling location guard](figures/pooling_location_guard.png)

How to read: the solid line averages 192 target-region positions; the dashed
line uses only the last position. Only the aggregated object is strongly
aligned with M2D2 domains.

### Full model-family atlas

![Layerwise model-family atlas](figures/layerwise_semantic_nmi.png)

How to read: the curves are non-monotonic. Directional fine-domain NMI peaks
descriptively at hidden state 23 (0.6907), while coarse peaks at state 25
(0.3013). These post-hoc maxima do not replace the fixed state-15 verdict.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What it rules out | What remains live |
| --- | --- | --- | --- | --- |
| data | exact balance and duplicate audit | passed | missing-domain/count explanation | document dependence |
| extraction | 4 receipts, 29 states, frozen fingerprint | passed | model-update explanation | pooling choice |
| semantics | direction above label null | passed | complete unreadability | lexical/topic rival |
| radius | null and permutation gates | passed | direction-only sufficiency at primary object | unique conditional information |
| shape | registered lower bounds | failed | robust necessary covariance claim | more stable density estimator |
| token guard | final-position near zero | failed transfer | immediate token-Router promotion | causal-prefix aggregation |

## 10. Full Experiment Record

- Unit tests: 18/18 after C004; the ACP smoke recorded 17/17 before the fast-NMI test was added.
- Smoke completion: 16/16, `SMOKE_COMPLETE`.
- Full completion: 16/16, `FULL_RUN_COMPLETE`.
- Formal successful job: `pt-zkuak3ej`, state `SUCCEEDED`.
- Non-evidence attempts: `pt-ul0gol39`, `pt-l4czs4tk`.
- Four full representation shards: approximately 458 MiB each.
- Atlas rows: 624; radius-meaning rows: 232.
- Bootstrap draws: 10,000; label permutations: 1,000.

## 11. Interpretation

The direct evidence supports a mixed geometric account. Domain identity is
mostly encoded by direction in the registered mean-pooled coordinate, while
radius carries a smaller but reliable domain association and helps the full
density model. Radius also covaries with how unsurprising the frozen model
finds the window. Covariance-shape evidence is not robust enough to promote.

The early fine-domain signal at the embedding aggregate (vMF NMI 0.1777) and
the failure of final-token clustering keep a strong rival alive: much of the
measured “semantics” may be distributed lexical/topic composition collected by
mean pooling, rather than an abstract per-token semantic variable formed only
by deep layers.

## 12. Claim Boundary

Can claim: mean-pooled M2D2 domain information at the registered block is
direction-primary and radius-contributing under the registered unsupervised
model families.

Cannot claim: radius has unique conditional mutual information beyond
direction; covariance is necessary; individual token states are semantically
clustered; deeper layers monotonically refine semantics; native routing uses
the signal; experts specialize; or language modeling improves.

## 13. Next Decision

Decision: test current-token versus causal-prefix pooled block-14 states with
lexical controls before selecting the token-Router geometry.  
Completion criterion: a held-out causal representation retains direction and
radius evidence beyond lexical composition and is available at dispatch time.  
Resume action: wait for human confirmation or correction of the present result
and boundary, then open one new Anchor/Protocol only if this decision is kept.

## 14. Artifact Manifest

| Artifact | Purpose | Identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- |
| `protocol.md` | frozen contract | SHA-256 `89e6...8dc0` | yes | yes | C001/C002 pre-extraction |
| worker `prepared/data_manifest.json` | counts and domains | SHA-256 `83ed...63fe1` | yes | yes | exact duplicate count zero |
| four `representations_rank*.pt` | pooled states and NLL | hashes in rank receipts | yes | yes | raw worker artifacts |
| `analysis/atlas.csv` | all layer/model cells | successful full run | yes | yes | worker source table |
| `analysis/primary_results.json` | direct primary values and verdict | C004 revision | yes | yes | direct NMI point estimates |
| `analysis/bootstrap_scores.npz` | paired uncertainty | 10,000 draws | yes | yes | window bootstrap |
| `analysis/label_null_scores.npz` | label nulls | 1,000 draws | yes | yes | matched tasks |
| local figures | curated visual evidence | hashes available from repository | yes | yes | visually audited |
| `completion_audit.json` | completion guard | 16/16 | yes | yes | `FULL_RUN_COMPLETE` |

## 15. Links

- anchor: [A15_14 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- code workspace: `/data/250010109/MoE_Router/experiments/20260901_a15_14_e01_m2d2_direction_norm_covariance_atlas/`
- result dir: `/data/250010109/MoE_Router/experiments/20260901_a15_14_e01_m2d2_direction_norm_covariance_atlas/runs/full-20260901T181100Z/`
- job: `pt-zkuak3ej`

