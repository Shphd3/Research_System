# Detailed: post-hoc SAE classification plots for meeting v2

[Summary](summary.md). Eligibility: **BOUNDED / POST-HOC**; scientific interpretation remains AI draft. This addendum owns only the new fixed-label geometry, classification/coverage trajectories and display transformations. Existing training, replay, reconstruction, grouping-swap and semantic-audit provenance remains in [the parent Detailed](../detailed.md), whose limitations are inherited.

## 0. Quick recap

The user requested a second meeting report with an explicit SAE curve, ordinary versus high-node classification, and SAE evolution including its existing training-time updates. Measurements were computed from existing replay/code artifacts. There were zero new main-model updates, zero SAE updates and zero graph fits. This does not replace missing parent E21 result records, revise its frozen Protocol, or change the human-owned Focus/Anchor.

## 1. Definitions and design link

The graph/node language refers to the same model layer and same SAE, not different neural layers. The ordinary map groups29471 retained atoms and includes some high nodes; it is not a leaf-only map. The historical high28 map selects the28 atoms with depth≥2 in the authenticated historical graph and groups them into eight sets. It does not directly use parent edges as nested routing constraints, nor establish broad semantic parents.

For sparse positive activations a and group map G, q(k) is the sum of covered activation in group k divided by total covered activation. If total mass is zero, the position is unclassified. The scatter's hard class is argmax q, whereas the actual structural supervision uses soft q pair relations. A class color is not an expert ID or semantic label.

The relevant methodological question is how much apparent structural evolution belongs to model states versus their readout. The registered research Focus remains [the earlier functional-training Focus](../../../../../../focus/focus_sae_flat_router_functional_training.md); this requested derived meeting does not reset its question or next decision. The parent [Protocol](../../protocol.md) remains frozen.

## 2. Scope, conformance and actual setup

| Item | Actual work | Eligibility consequence |
|---|---|---|
| Authorization | User explicitly requested meeting v2, SAE trajectories and ordinary/high-node results | Authorizes local post-hoc analysis and report, not new scientific state or training |
| Main training | Existing dynamic_sae_b_u, seeds17/29/43,512updates | Same model trajectory for all displayed readouts per seed |
| SAE training | Existing receipts: refresh at32/64/128/256,400SAE optimizer steps per refresh | 1600existing SAE updates per seed; at512 the most recent SAE is from256 |
| Refresh sample | Existing262144cached positions per refresh,261881after norm trimming in checked seed17 receipt | Mixed-step buffer; not current-checkpoint-only fitting; prior stale-buffer limitation remains |
| New compute | CPU readout, geometry, label alignment and plotting only | Zero new main/SAE updates, zero group fits |
| Held-out panel | Existing247records,1247answer-prediction positions | Source/record/position weighting from probe_weights.npy; no new panel selection |
| Times | 0,32,64,128,256,512 | Six saved analysis points, not continuous dynamics |
| Fixed readout | Initial encoder and original ordinary or historical high28 group map | Current model h changes; q recomputed offline |
| Adaptive readout | Already-saved updated encoder and refreshed ordinary map | Includes both encoder and map changes; source-identity limitation inherited |
| Missing counterpart | No refreshed high28 hierarchy/map | No dynamic high-node line is manufactured |
| Visualization | Seed17 preselected as smallest registered seed, all1247points | Single-seed illustration; three-seed metrics separately |

Training stages, parameter groups, optimization schedules and source weaknesses are inherited from parent Detailed. Checked seed17 receipt reports512updates and4339651cumulative answer tokens; no elapsed-time efficiency claim is inferred.

## 3. Metrics and transformations

### Fixed-membership geometry

At t0, take each teacher's hard argmax label on its covered positions. Keep those labels and that covered cohort fixed over time. Normalize every1024-dimensional h to unit length. Use the existing source-record-position weights, renormalized once on the teacher's t0 covered cohort. Compute weighted class centroids and total centroid, within dispersion W and between dispersion B. Validate W+B equals total weighted dispersion. Report per-seed percent change in W,B,and B/W, then equal-weight mean over the three training seeds.

The ordinary cohort includes all1247positions; high28 includes82. Consequently its curve is a conditional geometric description, not a controlled ranking against ordinary readout. New metrics for method=changing repeat fixed t0 geometry because all t0 labels and h are identical; this redundant column is not plotted as an independent geometric result.

### Current classification and coverage

At each t, obtain current argmax q and validity. Coverage sums weights of valid positions. For label retention, restrict to positions valid at both t0 and t; construct the8×8weighted contingency matrix and solve a global one-to-one label assignment maximizing agreement. Divide agreeing weight by common-covered weight. Store unweighted adjusted Rand index as an additional descriptive guard against pure label changes and imbalance; neither statistic is semantic accuracy. No confidence interval treats positions as independent training replicates.

At t0 seed17, ordinary hard counts are[0,917,20,309,1,0,0,0]; this imbalance means96%retention does not by itself certify informative classes. Refreshed512 counts before display renaming are[46,370,11,108,268,72,353,19]. High28 t0 counts are[68,0,1,7,6,0,0,0], but group count/mass does not tell us semantic meaning.

### Projection and color contract

Fit a two-component full-SVD PCA on unit-normalized seed17t0 h only, unweighted for display, and transform every subsequent h using that identical mean/components. Fix axis ranges using all six projected time points. The axes explain22.024%and12.344%of t0variance, totaling34.368%. Do not fit a fresh projection for each frame or per readout.

Scatter rows share EXACTLY the same positions at each t. Fixed ordinary/high rows retain their actual group names. Adaptive colors use the weighted assignment to t0 ordinary labels; this is display alignment only. Pairwise drift is inherently label-permutation invariant and is copied from the existing analysis. Cross-row matching color does not establish matched semantics. Draw every unclassified high28 point gray, rather than excluding it.

## 4. Evidence lineage and results

| Observation | Inputs / transform | Aggregate | Result and boundary |
|---|---|---|---|
| Ordinary fixed-class geometry | Saved dynamic h; fixed q at0; unit h; weighted W/B | Seed-wise changes, mean/min/max | W−3.604%,B+20.939%,B/W+25.468%; does not establish semantic separation |
| High28 geometry and scope | Existing high28.pt applied to saved initial-encoder codes | Same method on t0covered cohort | B/W−2.390%;82positions,weighted coverage4.865%; not matched ordinary cohort |
| Label retention | Current q, global weighted name alignment | Mean over3seeds | 95.997%fixed vs59.020%adaptive; class imbalance-sensitive |
| Adaptive readout drift | Parent sae_metrics.csv | Existing cross-record weighted relation RMS | 0.0534fixed vs0.3527adaptive; not changed-point percentage |
| SAE adaptation | Parent sae_metrics.csv and training receipts | Existing residual/current-h variance | 0.3374fixed vs0.1078adaptive; not semantic or task utility |
| Current classifications | Saved q or high28aggregation; fixed t0PCA | Seed17allpositions | Only visual evidence of changing assignments in a partial projection |

New table: [readout_metrics.csv](tables/readout_metrics.csv). Source lineage and figure hashes: [manifest.json](tables/manifest.json). Verification: [validation.json](tables/validation.json).

Validation passed:54table rows,57input hashes,36independently recomputed geometry cases (maximum error4.44e−16), teacher aggregation parity (maximum error1.79e−7), exact t0fixed/adaptive equality,20curated PNG/PDF copies,27local links and the group-renaming hand calculation. Repository check returned ok=true with zero errors; existing advisory items remain unchanged. [Repository receipt](tables/repository_check.json).

The previous supplement's task-only K-means/GMM geometry used a different arm, pre-answer panel, and label construction. It does not conflict with current ordinary-SAE tightening. We explicitly correct any blanket claim that all group definitions disperse within classes. This follow-up does not isolate the effect of switching clustering algorithm while holding every other factor fixed.

## 5. Figure contract

| Figure | Meaning / source | Allowed reading | Main limitation |
|---|---|---|---|
| fig1_expectation | Same150synthetic point coordinates in all3frames; only class colors change, per researcher clarification | Assignment becomes more organized without moving h | No empirical support or semantic label evidence; lower-left consistency curve is illustrative |
| fig2a_curves | New readout_metrics plus existing sae_metrics | Fixed-class geometry, pair-relation drift, reconstruction adaptation | High28different cohort; bands are seed range; adaptive high28missing |
| fig2b_clusters | Same h projection; current teacher colors | Across time and across readouts | Seed17and34.37%variance only; hard colors compress soft distributions |
| fig2b_intermediate | Same transform at32/64/256 | Additional observed checkpoints | No interpolation or proof of natural class birth |
| coverage_membership | New readout_metrics | Coverage alongside descriptive class retention | Not semantic accuracy; common-covered subset changes for high28 |

## 6. Interpretation, failures and next decision

The researcher subsequently clarified the desired hypothesis figure as fixed point coordinates with increasingly organized classification/dispatch. Only the synthetic expectation figure and explanatory wording were changed; empirical figures and measurements were not altered. Its coordinate-equality check is recorded in [expectation_receipt.json](tables/expectation_receipt.json). Producer: execution-root `expectation.py`, also called by `build.py` for reproduction.

The minimum supported update is: fixed ordinary-SAE labels describe relative geometric separation on this trajectory, while adaptive SAE/readout changes produce considerable reclassification and better reconstruction. Their semantic interpretation remains unestablished. Existing same-h swap and co-occurrence-unit controls show that readout construction can generate changes without model updates. Those controls do not attribute the entire historical trajectory.

No new failure was hidden. High-node coverage is explicitly displayed. No refreshed high28history exists. Historical source/extraction discrepancies, mixed-time refresh buffers, lack of independent human semantic truth and absence of expert-utility intervention are inherited limitations. No result is promoted to the registered E21 verdict or a human-owned Focus judgment.

**AI proposed next decision:** under one co-occurrence rule, track an independently interpretable operation relation with fixed and refreshed readouts, with ordinary unsupervised routing as a reference. Completion means distinguishing restored relation, already-retained relation, or predominantly format-driven relation. First action is to choose the relation and independent counterexamples; no new training budget is implied.

## 7. Artifact map and reproduction

Execution root: `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/audits/0911_minimal_followup/meeting_v2/`.

Producer: `build.py`; output `readout_metrics.csv`, `projection.npz`, `figures/`, `manifest.json`, `build.log`. Inputs are individually hashed in manifest. `validate.py` produces `validation.json`; all curated figures and tables are byte copies.

Reproduce in the qualified existing runtime by sourcing `experiments/20260910_sft_routing_representation_full_matrix/runtime.sh`, then running the absolute build.py path with OPENBLAS_NUM_THREADS=4 and OMP_NUM_THREADS=4. It reads local artifacts only and performs no model optimizer updates. Font file: `/tmp/NotoSansCJKsc-Regular.otf`; record its hash in validation receipt.

The date-local reading figures live under `daily_research_reports/0911/figures/`, with provenance appended to that directory's SOURCES.md. [Second meeting report](../../../../../../../../../daily_research_reports/backup/2026/09/0911/meeting_report/history/meeting_brief_sae_coordinate_evolution_v2.md).

## 8. Matched K-Means/GMM/SAE variance and centroid follow-up

**Scope and eligibility.** The researcher explicitly requested separate within/between variance plots, a K-Means/GMM/SAE comparison on representations, and scatter trajectories with centers. Then requested a rewritten meeting surface placing one concise hypothesis/conclusion directly before its figure. This is a further local post-hoc descriptive analysis, not neural training, a new registered success criterion, or an Anchor/Focus transition.

**Common inputs.** Exactly the same dynamic_sae_b_u states,247records/1247positions, three seeds, six times and source-record-position weights as this addendum. All methods cover all positions. For each seed, fit K-Means with K8,n_init20,random_state20260910 and a diagonal GaussianMixture with K8,n_init1,max_iter200,reg_covar1e-6,random_state20260910 on full1024dimensional unit-normalized t0h. These are the same readout recipes as the earlier geometry audit, applied to this different common panel. Fits are unweighted descriptive fits on the panel, not held-out classification validation. All six fits converged, no recorded warnings. Fixed SAE uses its existing q0argmax labels. Class sizes, fitted objectives and effective nonempty group counts differ; no semantic quality ranking follows.

**Fixed memberships.** Freeze each method's t0labels, then evaluate weighted W/B on exactly the same h at each step. K-Means/GMM are not refitted at later steps for these curves. W is the weighted trace of within-group covariance (total squared-distance variance), B the weighted squared centroid distance to the global mean; neither is a single coordinate's sample variance. W+B equals total variance. Means/min/max summarize the three training seeds; solver variability was not newly audited for this panel.

| Method | Mean W change0→512 | Mean B change0→512 | Mean B/W change0→512 |
|---|---:|---:|---:|
| K-Means | −0.898630% | −4.709826% | −3.844221% |
| Diagonal GMM | −0.994349% | −4.796317% | −3.838713% |
| Fixed ordinary SAE labeling | −3.604238% | +20.939497% | +25.467524% |

These are different labelings of identical trajectories. The older positive K-Means/GMM B changes came from task_u and pre-answer positions, so those previous numbers cannot be directly substituted here. The present common-panel comparison is suitable for explaining why a classification definition matters, not for comparing training methods or claiming semantic advantage.

**Centroids and trajectories.** Use the saved seed17t0PCA without refitting and identical limits in every panel. Plot all1247positions at0/128/512, plus stars and group numbers for their current weighted member centroids. A weighted centroid is computed in full unit-h space before projection; it equals the weighted mean of projected members. It is not the fitted GMM mean parameter. A separate trajectory overlay shows every group's centroid at all six saved times, initial hollow circle and final star, and at most8members/group chosen deterministically by evenly spaced member indices. It does not choose the largest movers or enlarge displacements. The full-dimensional weighted centroid-displacement curve is a backup when arrows are short. The projection's34.37%explained variance and single-seed limits still apply.

**Adaptive SAE and high nodes.** An additional3×3classification figure retains fixed ordinary, refreshed ordinary and fixed high28 rows with CURRENT-label weighted centroids. Its changing centroid can reflect both member motion and reassignment. This differs intentionally from fixed-membership geometry/trajectory figures. Adaptive colors are aligned to t0names; high28uncovered points remain gray. No refreshed high28trajectory is fabricated.

**Audited eight-group display clarification.** The first trajectory figure's SAE panel has all1247input positions but only4nonempty hard classes: displayed group1–8 counts are[0,917,20,309,1,0,0,0]. Every soft target channel nevertheless has positive mass. Weighted q0masses are[0.0242461,0.5856677,0.0574956,0.2374954,0.0539467,0.0192434,0.0052603,0.0166448]. The revised hard-center panel explicitly labels these counts and empty groups rather than fabricating centers. A separate `0911_v2_sae_eight_soft_groups` figure defines a different center, c_k(t)=sum_i w_i q_i(k,0)u_i(t)/sum_i w_i q_i(k,0), then projects it with the same fixed PCA. All eight centers are finite because each denominator is positive. Its target weights are held at t0, not updated with the current teacher. Producer `variance_trajectory/sae_display_fix.py` is called from the common build; [occupancy table](tables/variance_trajectory/sae_group_occupancy.csv) and [display receipt](tables/variance_trajectory/sae_display_receipt.json) document the distinction. Original W/B values are unchanged.

**Files and lineage.** Producer is execution-root `variance_trajectory/build.py`. [Manifest](tables/variance_trajectory/manifest.json) hashes all inputs and figures; [geometry](tables/variance_trajectory/geometry.csv) contains54method×seed×time rows; [fit receipt](tables/variance_trajectory/fit_receipt.json) records convergence; [projected centers](tables/variance_trajectory/centers_projected.csv) contains finite observed centers only. Raw labels/full-dimensional centers remain in the execution workspace's `labels_centers.npz`. [Validation receipt](tables/variance_trajectory/validation.json) owns independent recomputation checks. No source neural artifacts were modified.

Validation passed54independent full-dimensional geometry/centroid checks,45source hashes,32curated figure copies and42local links. Maximum variance/centroid error was4.44e−16, and projecting full-dimensional centroids versus averaging projected members differed by at most5.56e−16. SAE geometry matches the preceding addendum at1e−12absolute tolerance. All six descriptive readout fits converged. Repository validation returned ok=true with zero errors; remaining advisory items were not treated as scientific decisions.

**Interpretation and next decision.** The fixed-membership geometry depends on labeling; current SAE reclassification changes the description of identical h. These findings retain the same bounded conclusion and proposed next decision in Section6: independently interpret one operation relation under a common co-occurrence rule. No new semantic, efficiency, expert-utility or adaptive-necessity claim is introduced.
