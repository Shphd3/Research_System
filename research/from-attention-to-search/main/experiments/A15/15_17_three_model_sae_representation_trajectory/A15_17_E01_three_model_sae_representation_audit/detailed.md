# Detailed: A15_17_E01 Three-Model SAE Representation Audit

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), including R001--R006  
Summary: [summary.md](summary.md); Chinese companion: [summary_cn.md](summary_cn.md)  
Result eligibility: S2--S6 `PASS`; evidence `ELIGIBLE`; scientific verdict `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

- Purpose: compare existing M0/M1/M2 representation trajectories and their dependence on the leading common direction.
- Hypothesis: an SAE-mediated residual difference forms a coherent paired trajectory and survives B2 or B3; the strongest rival is a lexical, reconstruction, probe, mean, or dominant-direction artifact.
- Experiment logic: S2 eligibility → S3 18-shard collection and local gradients → S4 raw Part A → S5 fit-only B1/B2/B3 → S6 paired evidence and required figures.
- Direct result: M1 actual-input parent-conditioned fine Fisher geometry differs from M0 from 1B through 10B in P and from 0.5B through 10B in N; the difference survives B2/B3. Probe advantages are checkpoint- and panel-specific rather than a global ranking.
- Eligibility: `ELIGIBLE`. Six qualification tasks, 18 caches, 18 four-batch gradient records, 216 transforms, 19 nonempty tables, 5,000-draw paired uncertainty, and 16 required figures passed the final audit.
- Verdict: `AI_DRAFT_SUPPORTING_BOUNDED_AWAITING_HUMAN_CONFIRMATION`.
- Claim boundary: frozen representation accessibility, residual geometry, sparse usage, and local gradients only; no causal use, task benefit, or general model superiority.

The researcher has not yet supplied the required closed-book result judgment. All measurements and eligibility calls below are canonical; the scientific branch label remains an AI draft until the researcher confirms or corrects it.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| raw \(h\) | state before SAE mediation at the final block | final block `norm2` output | vector | pre-mediation accessibility | model use |
| actual input | state consumed by the final MLP | gate/up pre-hook input | vector | distinguishes native \(h\) from mediated reconstruction | downstream benefit |
| Fisher trace | class-balanced between-class energy relative to within-class energy | parent-conditioned fine labels | dimensionless ratio | detects organized class geometry even when probe accuracy is near ceiling | causal use |
| B2 | remove the common first axis without centering | first right singular vector of the uncentered fit matrix | projected vector | teacher-required common-representation removal | unique causal factor |
| B3 | remove mean and first centered axis | fit mean plus centered first right singular vector | projected vector | distinguishes mean from leading centered variation | intrinsic ontology |
| paired interval | resample the same report units for both models | 5,000 stratum-preserving bootstrap draws | model metric difference | uncertainty of a matched model contrast | family-wise significance |
| sparse contribution | active coefficient weighted by decoder-column norm | normalized \(z_j\\lVert d_j\\rVert_2\) | share | atom-usage audit | cross-model atom identity |
| pointwise descriptive interval | an interval for one registered cell | 2.5/97.5 percentiles of paired draws | metric units | identifies bounded per-cell separation | a global any-checkpoint test |

## 2. Anchor Link And Decision Point

The Anchor asks whether the existing SAE-mediated models differ from Dense and from each other in residual domain-readable organization. The only next decision is whether one eligible residual difference is strong enough to nominate a separately designed causal functional intervention. This run does not authorize or execute that intervention.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
|---|---|---|---|---|---|
| approval and scope | full S2--S6, no ETA reduction | full matrix executed | `PASS` | Protocol approval snapshot | permits result use |
| resource | one single-node 4×H100 Reserved job after R003 | `pt-we1cni15`, `n6ls.iu.i40.4`, four H100 80GB | `CONFORMING` | [execution receipt](execution_receipt.md) | no scientific change |
| source/config identity | submitted hashes fixed before v4 | manifest hash set matches submitted source | `PASS` | `audit/submitted_code_manifest.json` | eligible |
| data and split identity | P 120/60/180 by family; N 600/200/400 | exact frozen inventories and split guards | `PASS` | S0 source audit and spec | eligible |
| task matrix | 3 models × 6 checkpoints | 18/18 task specs, completions, caches, gradients | `PASS` | `stages/S3_PASS.json` and final hash audit | eligible |
| S2 runtime guards | six 0B/10B tasks; four GPUs; hooks; finite values; unchanged state | 6/6 pass; 17 tests; zero optimizer/buffer updates | `PASS` | `qualification/qualification.json` | eligible |
| probes | frozen split, four \(C\) values, convergence, identical paired report units | 804 raw cells and 1,296 B cells eligible; every fitted cell converges; 144 fixed \(h\)-to-actual transfer rows are not refit and mark convergence N/A | `PASS` | `probe_metrics*.csv` | eligible |
| Part A | raw coordinates retained | all raw tables and predictions present | `PASS` | `A_raw/tables/` | eligible |
| Part B | fit-only B1/B2/B3, B2 and B3 mandatory | 216 transforms = 2 panels × 3 models × 6 checkpoints × 2 surfaces × 3 transforms | `PASS` | `transform_registry.csv` plus transform files | eligible |
| uncertainty | 5,000 paired stratified draws | receipt records 5,000 | `PASS` | `analysis_receipt.json` | eligible |
| required figures | A01--A09 and B01--B04; A06/A09 include 0B | 16/16 present, nonzero, PNG-decodable | `PASS` | final artifact audit | eligible |
| model immutability | no optimizer or buffer updates | all before/after state hashes match; update counts 0 | `PASS` | six S2 and 18 completion records | eligible |
| UMAP initialization | deterministic descriptive embedding | spectral initialization warned three times and fell back to random initialization under fixed seed | `BOUNDED_DESCRIPTIVE` | persistent pod log lines 56--74 | no impact on metric tables; UMAP not decision-bearing |

Frozen Protocol revision: SHA-256 `f88b3854b81b09a1916fa1dfa02761786f755880ea06c81649b0c31787ce6aa5` in the submitted manifest.  
Execution scope approved: full S2--S6, with no ETA-based scale reduction.  
Amendments: R001 changed 4×RTX5090 Spot to 2×H100 Spot; R002 corrected stale execution text; R003 recorded the failed AFS lock and 4×H100 Reserved rerun; R004 repaired scalar-buffer hashing; R005 repaired detached NumPy export; R006 represented inactive AuxK as an exact zero-gradient component. None changed a model, checkpoint, panel, metric, transform, bootstrap rule, figure requirement, or claim boundary.  
Retries and exclusions: `pt-7yis2se8` never started; `pt-20q3i7pd`, `pt-xsmaub14`, `pt-i2ofctjz`, and `pt-ix1stwdr` are engineering-only and `INELIGIBLE`. Fresh v4 reused no partial artifacts.  
Missing conditions or artifacts: none. The 90 MiB per-sample raw prediction CSV remains in the execution workspace rather than the research repository; it is complete and referenced by the manifest.  
Post-hoc analyses: no post-hoc inferential test or selection. This record summarizes registered tables. Visual inspection and copying of eligible figures do not alter the analysis.

### Final completion audit

- Qualification files: 6/6.
- Completion/cache/gradient files: 18/18/18; SHA-256 matches every completion record.
- Gradient batches: exactly 4 in every gradient record.
- M2 0B AuxK: active examples `0` and maximum raw norm `0.0` in all four batches.
- Fit-only transform files: 216.
- Table files: 19, all nonempty; raw per-sample predictions contain 322,860 rows.
- Required figures: 16, all nonempty and decodable.
- Analysis receipt: `PASS`, 5,000 bootstrap rounds, 0 optimizer updates, 2,106.34 analysis seconds.
- Terminal receipt: `PASS`, exit code 0, 0 optimizer updates.

## 4. Actual Setup

- Research question: whether M0/M1/M2 differ in residual representation trajectories after common-direction removal.
- Data: P 360 sentences with 120/60/180 family-disjoint fit/tune/report; N academic M2D2 1,200 rows with 600/200/400 fit/tune/report.
- Confirmation status: N is a development replication, not untouched confirmation. Checkpoints are trajectory points, not independent experimental replicates.
- Permitted supervision: labels enter probe fitting/scoring only under frozen splits; no model training.
- Models: M0 Dense; M1 detached reconstruction into the final MLP; M2 live reconstruction into the final MLP plus SAE-only AuxK.
- Representations: final-block post-`norm2` raw \(h\), actual final-MLP input, and M1/M2 sparse Top-k contributions.
- Training/update rule: `NOT_APPLICABLE`; existing checkpoints only; zero optimizer, scheduler, buffer, or training-token updates.
- Checkpoints: 0, 0.5, 1, 3, 5, and 10B for each model.
- Seed: 17 for registered selection, probes, uncertainty, and descriptive embeddings.
- Changed variables: model lineage and Part B transform.
- Held fixed: checkpoint tokens, panels/splits, extraction site, pooling, probes, metrics, bootstrap, figures, and claim boundary.
- Code identities: `collect_full_task.py` `5aeb2180...`; `analyze_full.py` `eac4ef6c...`; `run_full_remote_audit.sh` `2dac95c8...`; complete hashes live in the submitted manifest.
- Runner: `scripts/run_full_remote_audit.sh`.
- Result root: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4/`.
- Known limitation: the same pretrained data path underlies the three model lineages; this is a controlled checkpoint comparison, not independent training-seed replication.

## 5. Metrics And Registered Decision Rules

Primary evidence consists of paired model differences in report balanced accuracy, parent-conditioned fine Fisher trace, and fine cosine relation margin across checkpoints. Supporting evidence requires a coherent contrast in the same object and metric that survives B2 or B3. A raw-only contrast removed or reversed by both B2 and B3 is non-supporting. Sparse and gradient measurements may explain or qualify representation evidence but cannot replace it.

Balanced accuracy is the mean per-class recall. Fisher trace is the class-balanced between-class scatter divided by within-class scatter. Relation margin is positive-pair cosine similarity minus registered rival-pair similarity. Positive M1−M0 means M1 has the larger metric. All 95% intervals are pointwise descriptive paired-bootstrap intervals, not family-wise claims.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
|---|---|---|---|---|---|---|---|---|
| M1 has a coherent actual-input fine-geometry trajectory vs M0 | same object/metric, bounded trajectory | 18 hash-verified caches | parent-conditioned fine Fisher on raw actual input | same report units; 5,000 paired draws | P M1−M0 positive at 1/3/5/10B; N positive at 0.5/1/3/5/10B | `ELIGIBLE` | `SUPPORTING_BOUNDED` | pointwise intervals; development replication |
| M1 geometry is not only first-direction energy | retained after B2 or B3 | fit caches and 216 fit-only transforms | project with uncentered PC1 or center then project; recompute Fisher | same report units; 5,000 paired draws | P B3 M1−M0 `+0.0757/+0.1098/+0.1141/+0.2661` at 1/3/5/10B | `ELIGIBLE` | `SUPPORTING_BOUNDED` | coordinate-sensitive geometry, not causal use |
| global-fine readability does not define a universal ranking | consistent paired separation would be required | per-sample probe predictions | frozen probe/tune rule; raw-selected \(C\) reused for B | 5,000 paired draws | P 3B M1−M0 positive; most other cells unresolved; all N raw-\(h\) cells unresolved | `ELIGIBLE` | `NOT_SUPPORTED_AS_GLOBAL_RANKING` | high absolute accuracy and pointwise testing |
| M2 live reconstruction reaches the backbone while M1 detached reconstruction does not | gradient topology must match model definition | four fixed N-fit batches per checkpoint | objective-weighted gradients by disjoint parameter group | batch/group descriptive values | M1 backbone reconstruction gradient 0; M2 10B median ratio `0.0406` | `ELIGIBLE_DIAGNOSTIC` | `CONFORMS` | local checkpoint gradients do not prove training causality |
| sparse features carry class-related reuse signal | positive within-vs-rival overlap margin | Top-k indices/values and decoder norms | normalized contribution weighted Jaccard | report independent units with descriptive interval | P fine weighted-Jaccard M1 peaks at 3B `0.1108 [0.0893,0.1309]`; M2 3B `0.0896 [0.0692,0.1099]` | `ELIGIBLE_DIAGNOSTIC` | `BOUNDED` | atom IDs are not aligned across checkpoints/models |

## 7. Main Results

### 7.1 Eligible decision evidence: M1 actual-input Fisher trajectory

P parent-conditioned fine Fisher, M1−M0:

| checkpoint | raw delta [95% interval] | B2 delta [95% interval] | B3 delta [95% interval] |
|---|---:|---:|---:|
| 0B | −0.0166 [−0.0302, −0.0081] | −0.0205 [−0.0332, −0.0129] | −0.0202 [−0.0329, −0.0127] |
| 0.5B | +0.0061 [−0.0198, +0.0337] | +0.0077 [−0.0184, +0.0354] | +0.0087 [−0.0172, +0.0368] |
| 1B | +0.0709 [+0.0392, +0.1148] | +0.0742 [+0.0424, +0.1187] | +0.0757 [+0.0445, +0.1217] |
| 3B | +0.1045 [+0.0707, +0.1568] | +0.1081 [+0.0746, +0.1615] | +0.1098 [+0.0818, +0.1598] |
| 5B | +0.0995 [+0.0671, +0.1508] | +0.1037 [+0.0711, +0.1556] | +0.1141 [+0.0828, +0.1671] |
| 10B | +0.2777 [+0.1301, +0.3700] | +0.2702 [+0.1318, +0.3615] | +0.2661 [+0.1325, +0.3544] |

The 0B negative actual-input difference is an architecture baseline: M0 feeds raw \(h\), whereas M1/M2 feed an untrained SAE reconstruction. Raw \(h\) is identical across models at 0B. The scientific trajectory begins after training; 0B is not evidence that training harmed M1.

N B3 actual-input Fisher M1−M0 is also positive from 0.5B onward:

| checkpoint | delta [95% interval] |
|---|---:|
| 0.5B | +0.0126 [+0.0061, +0.0207] |
| 1B | +0.0209 [+0.0143, +0.0296] |
| 3B | +0.0303 [+0.0230, +0.0404] |
| 5B | +0.0337 [+0.0261, +0.0448] |
| 10B | +0.0346 [+0.0268, +0.0451] |

M2 does not dominate M1 on this metric. In P B3 actual input, M2−M1 is negative at 1/3/5/10B: `−0.0571`, `−0.0818`, `−0.0694`, and `−0.0752`, with every interval excluding zero. M2 is positive over M1 only at 0.5B. The live-gradient plus AuxK topology therefore does not establish stronger residual fine geometry than detached M1.

### 7.2 Eligible but bounded probe evidence

P global-fine balanced-accuracy contrasts:

| surface / transform / checkpoint | M1−M0 | M2−M0 | M2−M1 | reading |
|---|---:|---:|---:|---|
| raw \(h\), raw, 3B | +0.0833 [+0.0389,+0.1333] | +0.0833 [+0.0389,+0.1278] | 0.0000 [−0.0389,+0.0389] | both SAE lineages above M0 |
| raw \(h\), raw, 5B | +0.0556 [+0.0167,+0.1000] | +0.0444 [0.0000,+0.0889] | −0.0111 [−0.0444,+0.0222] | only M1 interval separates |
| raw \(h\), raw, 10B | 0.0000 [−0.0389,+0.0389] | +0.0444 [+0.0111,+0.0778] | +0.0444 [+0.0167,+0.0722] | M2 is checkpoint-specific leader |
| actual, raw, 3B | +0.0778 [+0.0333,+0.1222] | +0.0111 [−0.0333,+0.0556] | −0.0667 [−0.1111,−0.0222] | M1 above M0 and M2 |
| actual, B3, 3B | +0.0611 [+0.0167,+0.1111] | 0.0000 [−0.0444,+0.0444] | −0.0611 [−0.1056,−0.0167] | same bounded M1 candidate survives |

N raw-\(h\) global-fine balanced-accuracy intervals are unresolved for all 18 model-pair/checkpoint cells. Absolute N trained-model values are near `0.79--0.83`, and the frozen lexical TF-IDF baseline is `0.8350`. P TF-IDF is `0.7278` while trained representations reach about `0.83--0.96`. These baselines reinforce the panel-specific boundary and argue against interpreting every high probe score as a model-lineage effect.

### 7.3 Common-direction removal strength

For P actual input:

| checkpoint | B2 removed energy, M0/M1/M2 | B2 relative gap, M0/M1/M2 | B3 removed energy, M0/M1/M2 | B3 relative gap, M0/M1/M2 |
|---|---|---|---|---|
| 3B | 0.9451 / 0.7300 / 0.7640 | 0.8856 / 0.6967 / 0.7424 | 0.2277 / 0.2493 / 0.2119 | 0.2510 / 0.1942 / 0.0646 |
| 10B | 0.9942 / 0.8116 / 0.7539 | 0.9383 / 0.7688 / 0.6790 | 0.8286 / 0.2331 / 0.3127 | 0.7891 / 0.2405 / 0.3295 |

B2 often removes most of the raw energy, especially for M0, yet the M1−M0 Fisher trajectory remains. B3 isolates a smaller centered leading component for M1/M2 at 10B and reaches nearly the same paired Fisher result. This makes a single dominant direction an insufficient explanation for the M1 result.

### 7.4 Sparse health and local gradients

- All representation-health rows are finite with zero zero-vectors and effective L0 exactly 32.
- At 10B, P FVU is `0.5485` for M1 and `0.4998` for M2; N FVU is `0.3966` and `0.2811`. Better reconstruction in M2 does not imply stronger probe or Fisher geometry.
- P feature coverage after 0.5B is only about `1.1%--2.0%`, whereas N is `58.5%--65.4%`. This is dataset-dependent usage, not a cross-panel quality scale.
- P fine weighted-Jaccard margins are positive after training for both M1 and M2, but separately trained checkpoints choose different atom IDs. The result supports within-checkpoint class-related reuse only.
- M1 reconstruction gradients are nonzero only in SAE parameter groups, consistent with detached backbone input.
- M2 reconstruction gradients reach upstream block groups. At 10B the median weighted reconstruction/LM ratio across all recorded batch/group rows is `0.0406`; the displayed batch-0 group range reaches `0.2962`.
- M2 AuxK is SAE-only and much smaller: 10B maximum weighted-to-LM ratio `0.0005707`. At 0B its dead-feature mask is empty, so all four batches correctly record zero active examples and exact zero gradients.

### 7.5 Secondary and ambiguous evidence

- Fine relation margins often separate models, but direction and persistence depend on panel, representation, and transform. They support “geometry differs” but do not give a stable three-model ordering.
- M2 relative to M1 changes sign over training on P Fisher and probe metrics. It is not a monotone benefit of live gradient or AuxK.
- PCA/UMAP/t-SNE show domain separation emerging after 0B but are descriptive. They cannot adjudicate model ranking, and UMAP used fixed-seed random initialization after spectral-init warnings.
- No debug-only or failed-attempt artifact is admitted into the scientific aggregate.

## 8. Visualization Results

### Actual-input linear readability

![Actual final-MLP-input global-fine readability](figures/A03_actual_input_readability.png)

- Purpose: show checkpoint-level global-fine probe trajectories on the state actually consumed by the final MLP.
- Raw source: `probe_metrics.csv`; paired uncertainty lives in `paired_probe_differences.csv`.
- Metric and unit: report balanced accuracy, 0--1.
- Axes/legend: x is billions of trained tokens; y is balanced accuracy; color is model.
- Observed result: P M1 is highest at 3B; the other checkpoints do not form a stable model ordering. N curves are close.
- Allowed conclusion: M1 3B is a bounded readability candidate.
- Limitation: the plotted points omit paired intervals; use the table for the verdict. Accuracy does not establish causal use.

### Fit-only first-direction sensitivity

![Raw-h readability after fit-only transforms](figures/B02_probe_after_direction_removal.png)

- Purpose: test whether raw-\(h\) probe differences vanish after B1/B2/B3.
- Raw source: `probe_metrics_B.csv` and `paired_probe_differences_B.csv`.
- Metric and unit: report balanced accuracy, 0--1.
- Axes/legend: x is billions of tokens; y is balanced accuracy; color is model; line style is transform.
- Observed result: several P separations persist, while N remains tightly grouped.
- Allowed conclusion: the P candidate is not visually eliminated by common-direction removal.
- Limitation: the decision-bearing residual-geometry result is Fisher, and exact inference comes from paired source tables.

### Removed direction strength

![Removed energy and singular gap](figures/B03_direction_energy_and_gap.png)

- Purpose: quantify how much of fit representation energy the first direction carries.
- Raw source: `transform_registry.csv`.
- Metric and unit: removed energy fraction and relative first/second singular-value gap.
- Observed result: B2 can remove most of P actual-input energy at later checkpoints; B3 is smaller for M1/M2 except the M0 10B case.
- Allowed conclusion: surviving metric deltas are not a trivial consequence of a weak projection.
- Limitation: removed energy does not identify semantic content or causal function.

### 0B-inclusive sparse atom display

![SAE atom-activation evolution including 0B](figures/A06_sae_health_and_features.png)

- Purpose: satisfy the requested 0B-to-10B atom-use display.
- Raw source: `sae_selected_feature_audit.csv`.
- Metric and unit: report normalized contribution share for fit-selected columns.
- How to read: rows are coarse domains; columns are selected atom IDs at each checkpoint.
- Observed result: 0B is diffuse/different from trained checkpoints; trained M1/M2 show structured but non-identical patterns.
- Allowed conclusion: atom usage changes with training within each checkpoint-specific SAE.
- Limitation: columns are selected independently at every checkpoint; visual position or atom ID cannot be aligned across models/checkpoints.

### 0B-inclusive representation evolution

![PCA representation evolution including 0B](figures/A09_representation_evolution_pca.png)

The corresponding [UMAP](figures/A09_representation_evolution_umap.png) and [t-SNE](figures/A09_representation_evolution_tsne.png) grids use the same 3×6 model/checkpoint layout. All include 0B and use frozen embedding coordinates from `A09_embedding_coordinates.npz`.

- Purpose: provide the requested qualitative evolution view.
- Observed result: the four P coarse domains are poorly separated at 0B and visibly separate after training across all three model lineages.
- Allowed conclusion: training produces descriptive coarse-domain organization.
- Limitation: these embeddings are nonlinear/projection-sensitive, lack paired uncertainty, and are never used for variant or checkpoint selection.

The remaining required figures are present in [figures/](figures): A01 analysis path, A02 raw-\(h\) readability, A04 geometry/Fisher, A05 relation matrix, A07 fact overlap, A08 local gradients, A09 alias, B01 transform sensitivity, and B04 inspectable example. Each is supplemental to the source tables.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
|---|---|---|---|---|---|
| local source/contract audit | exact hashes, 17 tests, shell/Python checks, local lock smoke | passed | none | known local contract regressions | remote runtime was still required |
| 5090 Spot attempt | ACP state | suspended / ineligible | researcher changed resource before allocation | no runtime result | full scope remained |
| 2×H100 Spot S2 | pod log, empty qualification set | failed / ineligible | AFS `flock` returned `EAGAIN` | old AFS lock design | node-local lock repair |
| Reserved v1 S2 | two M0 qualification files | failed / ineligible | scalar Long buffer byte-view required flattening | old state-hash shape handling | R004 |
| Reserved v2 S3 | S2 PASS plus two M0 shards | failed / ineligible | requires-grad SAE value exported directly to NumPy | old read-only export boundary | R005 |
| Reserved v3 S3 | S2 PASS plus seven partial shards | stopped / ineligible | inactive AuxK constant sent to autograd | old inactive-objective handling | R006 |
| Reserved v4 allocation/runtime | ACP and terminal receipt | passed | none | scheduling and startup uncertainty | analysis eligibility |
| S2 qualification | 6 task receipts | passed | none | hook, finite, memory, state-mutation, repaired-boundary faults | full matrix |
| S3 collection/gradients | 18 cache/gradient/completion records | passed | none | missing checkpoint shards and gradient records | analysis |
| S4 raw | raw tables/predictions/figures | passed | none | missing Part A | B sensitivity |
| S5 B1/B2/B3 | 216 transforms and B tables/figures | passed | none | missing teacher-requested common removal | synthesis |
| S6 synthesis | analysis and terminal receipts | passed | none | missing paired evidence or required figure | researcher judgment only |

Falsified physical prior: none.  
Falsified mathematical model: none.  
Falsified operationalization/proxy: a universal probe-ranking interpretation is not supported; Fisher geometry and balanced-accuracy accessibility must remain distinct.  
Falsified implementation: AFS lock placement, scalar hashing, requires-grad NumPy export, and inactive-objective autograd handling were falsified and repaired before the fresh eligible run.  
Falsified metric: none; pointwise uncertainty remains a limitation.  
Remaining rival explanations: lexical/task composition, reconstruction-mediated geometry, checkpoint-specific variation, lack of independent training seeds, and the absence of causal functional intervention.

## 10. Full Experiment Record

1. Question: do M0/M1/M2 differ in residual representation trajectories after common-direction removal?
2. Setup: frozen existing checkpoints, exact P/N panels, same final-block extraction, probe, geometry, uncertainty, and visualization contract.
3. Training data: no new training. Existing checkpoints and their provenance are frozen in the spec.
4. Testing/confirmation data: P report 180 family-disjoint sentences; N report 400 academic M2D2 development-replication rows.
5. Result: the fresh v4 run is fully eligible. M1 actual-input parent-conditioned fine Fisher geometry separates from M0 across multiple checkpoints and survives B2/B3; linear probe advantages are checkpoint- and panel-specific. M2 is not generally stronger than M1.
6. Insight and next decision: residual geometry is a viable candidate object, but it is not evidence of causal use. The researcher must decide whether M1 3B merits a separate functional intervention protocol.

## 11. Interpretation

The cleanest update is not “SAE improves representations” in general. It is narrower: detached-reconstruction M1 develops a reproducible parent-conditioned fine-class geometry in the actual state consumed by the final MLP, and this geometry is not carried only by the first singular direction. The same result appears in P and the N development replication.

The accessibility result is weaker. At P 3B, M1 has a clear actual-input probe advantage that survives B3, making this checkpoint a concrete intervention candidate. But later probe points do not preserve one ordering, N raw-\(h\) probes do not separate the models, and M2 frequently trails M1 in actual-input Fisher geometry. The evidence therefore distinguishes “geometry exists” from “one training topology is generally better.”

The local gradient audit confirms that M2, unlike M1, sends reconstruction gradient into the backbone, while AuxK is small and SAE-only. That difference is real, but the observational checkpoint comparison cannot attribute the representation trajectory to this path. A causal intervention must be designed separately.

## 12. Claim Boundary

Can claim: eligible evidence supports a parent-conditioned fine-class residual-geometry difference between M1 and M0 in frozen actual MLP inputs, coherent across multiple checkpoints and retained after fit-only B2/B3. Checkpoint-specific probe, sparse-use, and local-gradient observations may also be reported.

Cannot claim: native Gate or MLP causal use, expert specialization, downstream language-model improvement, general M1/M2 superiority, or semantic identity of SAE atom IDs across models or checkpoints.

## 13. Next Decision

Decision: `AI suggestion` — after confirming this bounded verdict, decide whether M1 3B should be the candidate for a separately designed causal functional intervention. This experiment does not authorize that follow-up.

Completion criterion: the researcher fills or confirms the judgment fields below and either authorizes a new intervention design or stops this branch.

Resume action: read the M1 3B lineage rows, paired source tables, and central figures; then update the Anchor/Focus only with the researcher-confirmed judgment.

Researcher judgment fields:

```text
Question: Do the observed residual representation differences justify a causal intervention candidate?
Direct result: PENDING_RESEARCHER_CONFIRMATION
Confirmed: PENDING_RESEARCHER_CONFIRMATION
Weakened or rejected: PENDING_RESEARCHER_CONFIRMATION
Current mechanism and reason: PENDING_RESEARCHER_CONFIRMATION
Cannot claim: PENDING_RESEARCHER_CONFIRMATION
Exactly one next decision: PENDING_RESEARCHER_CONFIRMATION
```

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
|---|---|---|---|---|---|---|---|
| Protocol | frozen contract | R001--R006 | Anchor/Focus | `f88b3854...` submitted hash | yes | yes | no result-derived rewrite |
| submitted source manifest | code/config/job lineage | pre-v4 audit | execution workspace | job `pt-we1cni15` | yes | operational | full hashes retained |
| qualification receipt | runtime eligibility | S2 | six 0B/10B tasks | status `PASS` | yes | engineering gate | 6/6, zero updates |
| 18 caches | raw representation evidence | S3 collector | three models × six checkpoints × P/N | every SHA matches completion record | yes | yes | 18 files |
| 18 gradient records | local objective evidence | S3 collector | four N-fit batches each | every SHA matches completion record | yes | diagnostic | 72 batches |
| raw paired Fisher | central geometry evidence | analyzer | verified caches | `b0e163e5...` | yes | yes | [copy](tables/paired_fisher_differences.csv) |
| B paired Fisher | common-direction decision evidence | analyzer | fit-only transforms | `46557824...` | yes | yes | [copy](tables/paired_fisher_differences_B.csv) |
| raw paired probes | accessibility evidence | analyzer | per-sample predictions | `1c172368...` | yes | yes | [copy](tables/paired_probe_differences.csv) |
| B paired probes | transformed accessibility evidence | analyzer | projected representations | `f69a36f3...` | yes | yes | [copy](tables/paired_probe_differences_B.csv) |
| raw/B relation tables | secondary geometry | analyzer | registered triplets | `169c2037...` / `baa628af...` | yes | bounded | copies under [tables/](tables) |
| transform registry and 216 files | B1/B2/B3 provenance | analyzer | fit rows only | registry `8b077e07...` | yes | yes | [copy](tables/transform_registry.csv); transform arrays remain remote |
| sparse health/overlap/selection | diagnostic and requested atom display | analyzer | Top-k contributions | copied source tables | yes | diagnostic | [tables/](tables) |
| per-sample predictions | paired probe provenance | analyzer | report samples | 322,860 rows; raw-workspace file | yes | yes | not copied due 90 MiB size |
| required figures | reader evidence | analyzer | registered source tables | 16/16; selected hashes recorded below | yes | yes/bounded | all copied under [figures/](figures) |
| analysis receipt | machine completion gate | analyzer | all outputs | `7b04e053...` | yes | operational | 5,000 draws; 0 updates |
| terminal receipt | process completion gate | runner | full job | `7f064b4c...` | yes | operational | PASS, exit 0 |

Selected figure hashes: A02 `854d1a51...`, A03 `4b19fe0e...`, A06 `be618c32...`, A09 PCA `c286b042...`, B02 `13535f0c...`, B03 `0c62eb2c...`. Curated copies were checked byte-identical to the execution outputs.

## 15. Links

- Anchor: `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md`
- Protocol: [protocol.md](protocol.md)
- Summary: [summary.md](summary.md) / [summary_cn.md](summary_cn.md)
- Code workspace: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/`
- Runner: `scripts/run_full_remote_audit.sh`
- Config: `Projects/from-attention-to-search/main/research_notes/sae_representation/20260915/analysis_plan1/0915_three_model_analysis_spec_v1.json`
- Data/source manifest: `audit/submitted_code_manifest.json`
- Result directory: `/data/250010109/MoE_Router/experiments/20260915_three_model_representation_audit/runs/full_h100_reserved_v4/`
- Canonical figure copies: [figures/](figures)
- Canonical source-table copies: [tables/](tables)
- Persistent log: `runs/full_h100_reserved_v4/pod_logs/three-model-rep-audit-0916-h100-reserved-full-v4-20260916T013138Z.log`
- Reproduction command: `RUN_ROOT=.../runs/full_h100_reserved_v4 bash scripts/run_full_remote_audit.sh`
- Job IDs: successful `pt-we1cni15`; ineligible `pt-ix1stwdr`, `pt-i2ofctjz`, `pt-xsmaub14`, `pt-20q3i7pd`; suspended pre-start `pt-7yis2se8`.
