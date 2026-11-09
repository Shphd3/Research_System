# Detailed: A15_14_E02 M2D2 Full-Dimension Geometry Robustness

Primary Anchor: [A15_14 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE_FULL_RUN`; knowledge wording is `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

Purpose: test whether the E01 carrier conclusion was created by PCA
compression.  
Hypothesis: centered raw-1,024 direction remains readable and radius remains a
registered contributor; the rival is projection-dependent attribution.  
Experiment logic: reuse the exact frozen E01 states, subtract only the train
mean, retain all 1,024 coordinates, and rerun the same label-blind model
families and controls.  
Direct result: both tasks retain `RADIUS_CONTRIBUTING`; direction and radius
scores are close to PCA-64, while the fine diagonal-density score falls by
0.0418.  
Eligibility: 14/14 completion checks passed.  
Verdict: `RAW_REPLICATES_TYPED_VERDICT`.  
Claim boundary: this is whole-window representation accessibility, not token-
level or functional routing evidence.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete computation | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Centered raw coordinate | original hidden dimensions after fixing an origin | \(z=h-\mu_{train}\), width 1,024 | hidden-state units | removes PCA as an explanation | privileged intrinsic coordinates |
| Direction | where the centered vector points | \(u=z/\lVert z\rVert_2\) | unit vector | semantic identity candidate | native use |
| Radius | length from the training center | \(r=\lVert z\rVert_2\) | hidden-state length | intensity/familiarity candidate | meaning by itself |
| NMI | cluster-label agreement invariant to cluster-number names | normalized mutual information | 0--1 | primary accessibility score | task or expert benefit |
| Radius permutation | preserve every direction but reassign observed lengths | \(\tilde z_i=r_{\pi(i)}u_i\) | paired NMI contrast | model-family radius contribution | unique conditional information |

## 2. Anchor Link And Decision Point

E01 fixed a train-only PCA coordinate because direction and radius require an
origin and coordinate system. E02 is a robustness check of that
operationalization. It asks whether retaining all 1,024 centered coordinates
changes the measured carrier. It does not replace the E01 primary verdict or
authorize a Router.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Source | eligible E01 full run | exact four saved shards; source E01 status `FULL_RUN_COMPLETE` | passed | `source_identity.json` | eligible |
| Data | 9,216 / 2,304 / 4,608 windows | exact reused source states | passed | E01 manifest hash and shard hashes | eligible |
| Coordinate | train centering, width 1,024, no PCA | `centered_raw`, dimension 1,024, `pca_used=false` | passed | receipts and primary result | eligible |
| Primary cell | mean pooling, hidden state 15 | exact | passed | primary predictions and result | eligible |
| Fits | five families, 20 restarts, both tasks, all layers and pools | 584 atlas rows | passed | `atlas.csv` | eligible |
| Uncertainty | 10,000 bootstraps and 1,000 label nulls | exact | passed | score archives | eligible |
| Figures | raw-vs-PCA and pooling guard | both present and visually inspected | passed | local `figures/` | eligible |

Frozen Protocol revision: SHA-256 is recorded in the eligible run log.  
Execution scope approved: implementation, tests, smoke, full analysis,
figures, and result records.  
Amendments: none.  
Retries and exclusions: none.  
Missing conditions or artifacts: none.  
Post-hoc analysis: paired raw-minus-PCA intervals below are descriptive and do
not change a registered gate.

## 4. Actual Setup

Research question: does removing PCA change direction/radius/shape attribution?  
Data: balanced M2D2-Wikipedia 3-by-3 hierarchy, 16,128 packed windows.  
Splits: 9,216 train, 2,304 development, 4,608 confirmation.  
Model: saved Qwen3-0.6B-Base states from E01; no new model forward pass.  
Representation: embedding plus 28 block outputs, mean positions 64--255 and
final-position guard, hidden width 1,024.  
Transformation: subtract the train mean separately for every layer and pool;
no rotation, scaling, truncation, or PCA.  
Task: three global coarse clusters and three child clusters separately within
each known parent.  
Fitting: log-radius Gaussian mixture, spherical k-means, von-Mises--Fisher
direction mixture, Euclidean k-means, and diagonal Gaussian mixture.  
Selection: 20 deterministic restarts, train objective first and development
objective as tie-breaker; no label agreement enters selection.  
Training audit: zero neural-network updates, zero backward passes, zero epochs,
zero optimizer steps, zero checkpoints, zero Router or expert parameters.  
Changed variable: PCA-64 projection versus centered raw-1,024 coordinates.  
Held fixed: all other scientific objects and thresholds.

Code worker:
`/data/250010109/MoE_Router/experiments/20260902_a15_14_e02_m2d2_full_dimension_geometry_robustness/`.  
Eligible run: `runs/full-20260902T032501Z/`.  
Source run:
`/data/250010109/MoE_Router/experiments/20260901_a15_14_e01_m2d2_direction_norm_covariance_atlas/runs/full-20260901T181100Z/`.

## 5. Metrics And Registered Decision Rules

Confirmation NMI is primary. Direction readability requires vMF direction NMI
above the matched label-null 97.5% quantile. Radius contribution passes when
radius-only NMI exceeds its null or the lower 95% bound of observed-minus-
permuted-radius diagonal-model NMI exceeds 0.02. Independent shape requires
the diagonal model to beat both vMF direction and Euclidean k-means by lower
bounds above 0.02 without radius already explaining the gain.

The packed window is the bootstrap unit. Ten thousand stratified resamples use
seed 1701. One thousand stratified label permutations use the frozen E01 null
logic. Layers are not replicates and their maxima are descriptive.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| raw direction readable | vMF above label null | `primary_predictions.npz` | full NMI and 1,000 nulls | coarse 0.1298 > 0.0013; fine 0.3180 > 0.0027 | eligible | pass | mean-pooled |
| raw radius associated | radius-only above label null | same | full NMI and matched null | coarse 0.0321 > 0.0010; fine 0.1283 > 0.0025 | eligible | pass | not conditional information |
| radius contributes to full density | lower bound > 0.02 | predictions and bootstrap archive | 10,000 paired draws | coarse [0.1424, 0.1705]; fine [0.1666, 0.1996] | eligible | pass | model-family contrast |
| independent shape | both lower bounds > 0.02 without radius explanation | same | paired NMI differences | coarse 0.0198/0.0179 lower bounds; fine -0.0198/-0.0132 | eligible | fail | diagonal estimator and dimension dependent |
| typed verdict survives dimension change | raw typed results match PCA-64 | raw and E01 primary results | exact registered rule | both tasks `RADIUS_CONTRIBUTING` in both dimensions | eligible | `RAW_REPLICATES_TYPED_VERDICT` | qualitative verdict, not numerical equivalence |
| token transfer | final position retains signal | 584-row atlas | raw vMF at fixed layer | coarse 0.0014; fine 0.0060 | eligible guard | not supported | one position is not every causal state |

## 7. Main Results

### 7.1 Primary cell

| Model family | Raw coarse | PCA coarse | Raw minus PCA | Raw fine | PCA fine | Raw minus PCA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| radius only | 0.0321 | 0.0315 | +0.0006 | 0.1283 | 0.1397 | -0.0114 |
| spherical direction | 0.1327 | 0.1337 | -0.0010 | 0.3242 | 0.3272 | -0.0030 |
| vMF direction | 0.1298 | 0.1289 | +0.0008 | 0.3180 | 0.3223 | -0.0042 |
| Euclidean full vector | 0.1306 | 0.1306 | 0.0000 | 0.3125 | 0.3113 | +0.0012 |
| diagonal density | 0.1615 | 0.1518 | +0.0097 | 0.3151 | 0.3569 | -0.0418 |

The paired raw-minus-PCA vMF intervals are [-0.0027, 0.0039] coarse and
[-0.0077, -0.0007] fine. The fine reduction is statistically visible at the
packed-window level but small in absolute NMI and does not change readability
or the typed verdict. Fine radius-only also decreases by 0.0114 with interval
[-0.0191, -0.0040] and remains far above its null.

### 7.2 Radius and shape

The raw observed-minus-permuted diagonal-density point differences are 0.1563
coarse and 0.1829 fine. These exceed their PCA-64 counterparts by intervals
[0.0060, 0.0379] and [0.1163, 0.1562]. This is strong evidence that the raw
diagonal model depends on the original direction-radius pairing. It is not a
clean estimate of unique radius information because permuting radius also
changes the high-dimensional density geometry.

Fine diagonal-density NMI falls from 0.3569 to 0.3151 and no longer beats the
direction model. Coarse diagonal density rises to 0.1615, but its two lower
bounds, 0.0198 and 0.0179, remain below the registered 0.02 requirement and
radius already passes. Independent shape remains unestablished.

### 7.3 Meaning and pooling

At the primary cell, centered raw log-radius has within-semantic-group
Spearman correlation -0.3471 with frozen-model NLL and +0.0579 with lexical
rarity. Its relation is therefore again stronger with predictability than
with rare vocabulary. Raw hidden norm reproduces the E01 values -0.1175 and
+0.2116 because it is the same untransformed object.

The raw full-dimensional final-position vMF NMI is 0.0014 coarse and 0.0060
fine, compared with 0.1298 and 0.3180 for whole-window means. Removing PCA does
not repair the token-level boundary.

## 8. Visualization Results

### Raw coordinates preserve direction and radius but weaken fine shape

![Raw 1,024 dimensions versus PCA-64](figures/raw1024_vs_pca64_primary_geometry.png)

Purpose: show whether the fixed-cell carrier result changes without PCA.  
Metric: confirmation NMI, 0--1; higher means stronger cluster-label agreement.  
Raw source: eligible raw and E01 primary result JSON files.  
Aggregation: direct confirmation point estimates; error bars show raw 95%
window-bootstrap intervals.  
How to read: compare orange raw bars with blue PCA bars inside each model
family.  
Observed result: direction and radius stay close; the fine diagonal-density
bar falls below direction.  
Take-home: PCA does not create directional readability or radius association,
but it materially affects the high-capacity fine density estimator.  
Cannot prove: native use, causal geometry, or expert value.

### Full dimension does not rescue a single final-token state

![Raw full-dimensional pooling guard](figures/raw1024_pooling_location_guard.png)

Purpose: preserve the deployment boundary after removing PCA.  
Metric: raw-1,024 vMF confirmation NMI across hidden-state index.  
How to read: solid lines average positions 64--255; dashed lines use only the
final position.  
Observed result: dashed lines stay near zero while mean-pooled lines are
positive and non-monotonic.  
Take-home: the result remains an aggregated sequence representation.  
Cannot prove: every other token is unreadable or a causal-prefix aggregate
will fail.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What it rules out | What remains live |
| --- | --- | --- | --- | --- |
| identity | four source hashes and eligible E01 receipt | passed | new model/data explanation | source-document dependence |
| no-PCA implementation | red/green tests and raw-1,024 receipts | passed | hidden PCA or dimension truncation | origin choice |
| smoke | five families and both tasks finite at the primary layer | passed | immediate numerical failure | full-atlas cost |
| full atlas | 29 layers, two pools, 584 rows | passed | favorable layer substitution | post-hoc peak interpretation |
| semantics | direction above null in both tasks | passed | PCA-created readability | lexical/topic aggregation |
| radius | null and permutation gates | passed | direction-only sufficiency | unique conditional information |
| shape | registered lower bounds | failed | robust necessary covariance | estimator dependence |
| token guard | final position near zero | failed transfer | direct raw-token promotion | causal-prefix aggregation |

## 10. Full Experiment Record

- Test-driven implementation: the missing raw-geometry module, missing
  analysis entry point, missing finalizer selector, and missing completion
  audit each produced the expected initial failing test before implementation.
- Final unit tests: 6/6 pass.
- Smoke: `SMOKE_COMPLETE`, raw centered width 1,024.
- Full completion: 14/14, `FULL_RUN_COMPLETE`.
- Analysis parts: 16; all 29 layers occur exactly once.
- Atlas rows: 584; radius-meaning rows: 232.
- Bootstrap draws: 10,000; label permutations: 1,000.
- CPU execution reused existing representation shards; no new GPU job or model
  extraction was used.
- No protocol amendment, retry, exclusion, or failed full run occurred.

## 11. Interpretation

The stable direction and radius scores answer the robustness question: PCA-64
did not manufacture the mixed direction/radius reading. Direction remains the
larger stand-alone carrier in both tasks, and radius remains non-random.

The result also clarifies what is not stable. Fine-domain diagonal-density
performance is substantially better after PCA compression than in raw space.
This is consistent with PCA suppressing nuisance dimensions or regularizing a
high-capacity density estimator. It strengthens the refusal to interpret the
E01 diagonal-model advantage as an intrinsic covariance ontology.

## 12. Claim Boundary

Can claim: at the fixed whole-window mean-pooled block output, the E01 reading
is not created by PCA compression; centered raw-1,024 M2D2 domain information
is direction-primary and radius-contributing under the registered model
families.

Cannot claim: PCA is irrelevant to every estimator; raw coordinates improve
semantic recovery; radius supplies unique conditional information; covariance
is necessary; individual token states are semantically clustered; the native
Gate uses the signal; experts specialize; or language modeling improves.

## 13. Next Decision

Decision: await explicit researcher approval before opening the current-token
semantic-object screen; the second geometry gate remains downstream and also
unauthorized.  
Completion criterion: the researcher names and approves the next screening
scope.  
Resume action: if approved, formalize the current-token versus causal-prefix
screen before any execution.

## 14. Artifact Manifest

| Artifact | Purpose | Source inputs | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- |
| `protocol.md` | frozen contract | Anchor, Focus, human request | yes | yes | no amendment |
| worker `source_identity.json` | source-shard identity | eligible E01 run | yes | yes | hashes four shards |
| worker `analysis/atlas.csv` | all raw layer/model cells | saved E01 representations | yes | yes | 584 rows |
| worker `analysis/primary_predictions.npz` | primary labels and predictions | fixed raw cell | yes | yes | feeds nulls and bootstrap |
| worker `analysis/bootstrap_scores.npz` | paired uncertainty | primary predictions | yes | yes | 10,000 draws |
| worker `analysis/label_null_scores.npz` | random-label controls | primary predictions | yes | yes | 1,000 draws |
| worker `analysis/primary_results.json` | typed result | predictions and registered rules | yes | yes | `RAW_REPLICATES_TYPED_VERDICT` |
| local figures | curated visual evidence | eligible raw and E01 tables | yes | yes | visually inspected |
| worker `completion_audit.json` | completion guard | all artifacts | yes | yes | 14/14 |

## 15. Links

- anchor: [A15_14 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- code workspace: `/data/250010109/MoE_Router/experiments/20260902_a15_14_e02_m2d2_full_dimension_geometry_robustness/`
- runner: `run_approved.sh`
- source run: `/data/250010109/MoE_Router/experiments/20260901_a15_14_e01_m2d2_direction_norm_covariance_atlas/runs/full-20260901T181100Z/`
- result dir: `/data/250010109/MoE_Router/experiments/20260902_a15_14_e02_m2d2_full_dimension_geometry_robustness/runs/full-20260902T032501Z/`
- figure dir: `figures/`
- job IDs: none; local CPU analysis reused existing saved representations
