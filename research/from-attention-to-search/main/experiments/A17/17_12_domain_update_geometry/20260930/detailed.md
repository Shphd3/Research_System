# Detailed: domain_update_geometry

[Summary](summary.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_12_domain_update_geometry/17_12_domain_update_geometry_anchor.md) · [Frozen Protocol](protocol.md) · [中文](detailed_cn.md)

**Final text R2 after the reasoning-auditor review; the scientific question is not closed.** Eligibility: measurement COMPLETE; panel descriptions BOUNDED; population directional inference insufficient because percentile coverage is uncalibrated; original program NON_SUPPORT preserved; human judgment Unknown. R denotes the [immutable result directory](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z/result), A its analysis subdirectory, V the [first post-run audit](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_result_audit), and V2 the [final reasoning audit](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_reasoning_audit_final).

## 0. Quick Recap

Purpose: characterize domain, representation and SAE relationships with natural-text update demands. The primary hypothesis tests this empirical domain-mean descriptor, not the existence of all domain structure. Last-target Q=−0.005715; the program returns NON_SUPPORT but population directional inference is insufficient. Domain-mean activation profiles replicate and estimated gradient directions have limited readout capture. Fit-selected common body atoms exceed three random spaces in the rank64 pooled-readout last-target energy comparison; enriched sets are below those controls in that comparison. This neither denies own-domain selective utility nor establishes interference mediation or expert-separation benefits.

## 1. Terminology / Definitions

| Term | Concrete definition | Purpose and boundary |
| --- | --- | --- |
| c / a | 2048-dimensional W input / 1024-dimensional native output, a=Wc | Identify the actual SAE site; SAE encodes a, not c |
| e | Full-vocabulary next-token CE derivative with respect to a | Output sensitivity; includes the true target |
| G / K | Single-position G=ecᵀ and the selected W block's gradient Gram | Local update geometry, not native representations or gradients of all model parameters |
| mean16 | Mean of16 actual target outer products | Aggregation scale; not outer product of mean c and mean e |
| μ / δ_s | Pooled fit mean / domain deviation from that mean | Common direction versus domain difference; rank≤3 for four deviations is definitional |
| Q_D | 1−domain-prototype MSE/pooled-prototype MSE | Held-out value of this descriptor, not all possible domain information |
| z / atom / P | SAE positive coefficients / normalized decoder columns / orthogonal decoder-span projector | Activation versus gradient coverage; overlapping spans cannot be added |

When only W changes, upstream inputs and all other parameters remain fixed, and common scalar SGD is used, ΔW_A=−ηG_A and Δa_B=−ηe_A(c_Aᵀc_B) are exact. Only the loss relation is first order: ΔL_B=−ηK_AB+O(η²). No finite step was executed, and no other-optimizer or long-horizon consequence is established. The final block is chosen because no cross-position attention follows its output, allowing a single target to involve one use of W; this does not directly extend to intermediate layers.

For pure cross-entropy, \(e_i=J_i^\top(p_i-\mathbf 1_{y_i})\), with J the current record's Jacobian of logits with respect to a, p the prediction probabilities and y the true target. J, p and y vary together across records. Thus e is not an external noise variable independent of representations, and alignment between e geometry and K does not isolate target or downstream causality.

Output projection is PG and projected/complement Gram contributions add exactly. Energy capture is \(\sum_{i\in R}\|PG_i\|_F^2/\sum_{i\in R}\|G_i\|_F^2\), the diagonal total of K. It cannot substitute for signed off-diagonal compatibility \(K_{ij}\).

## 2. Anchor Link And Decision Point

The researcher accepted domain-first analysis and explicitly authorized SVD, existing atoms, complete activation analysis and necessary4-H100 Reserved execution without renewed approval. Documents preceded submission; numerical choices were operationalized under that delegation. One core observational experiment runs all diagnostics regardless of its primary outcome. The future language-grouping/scale decision remains open; previous questions and frozen verdicts are unchanged.

## 3. Protocol Freeze, Conformance, And Deviations

Frozen before numerical Smoke: English Protocol SHA256 `b8b08172ebc4c044fe7206c8008d4667b6077363c4e53ea124e1ef5c4ccc54e4`; Chinese `f56042c6225696e1bdc65dd7093d741049534ba12d3b19b25805d4baf66c4966`. R/registration.json holds complete source/design/data hashes and R/source contains snapshots.

| Registered item | Actual | Eligibility/evidence |
| --- | --- | --- |
| State, matrix, pure NTP, freeze | Exact33B; final attn.o; zero LM/SAE updates | PASS; Smoke and checkpoint hashes |
| Four domains;64 records/category/split | 1024 distinct record IDs, no omissions/duplicates | PASS; manifest/receipt; distinct IDs do not establish statistical independence; paper dependence unknown |
|16 targets,255 positions |16384 targets,261120 activation positions | PASS; verification |
|2000 resamples,999 permutations | Registered seeds, strata and prototype refitting | Implementation conforms; interval coverage limitation below |
| Fit-only sets/axes | Persisted before readout evaluation; mandatory analyses complete | PASS; fit registration/frozen selection/spectral arrays |
| Matched SAE/PCA/three random controls | Nine spaces at actual ranks8/32/64;54 rows | PASS; projection receipt/table |
| Resources/numerics | Actual H100;230.05-second runner;18.63GB outputs | PASS;4 GPUs Reserved, below6h/50GiB limits |
| Figures | Nine figures; original Q errorbar misrepresented endpoints outside point estimate | Immutable original retained; V corrects display only |

No collection retries, exclusions, early stopping or scientific threshold amendments. Initial post-hoc additions comprised the bootstrap algebra audit, descriptive atom-table correlations/intersections, reading tables and a plotting correction. This user-requested R2 revises interpretation and checks the exact §5 risk identity against saved Gram matrices. Pre-revision documents are retained in V2/before. No recollection, statistical-test rerun, model fitting or registered-result replacement occurs.

**Estimator limitation.** For registered within-category resampling, let v_c be empirical covariance trace and n_c=64. Refitting a mean adds Σ_c n_c v_c/N² expected squared error. The pooled mean has N=512; each of four domain means has N=128 before equal-domain averaging. Added MSE is0.213213 pooled versus0.852853 domain, a difference of0.639640. A ratio of expected MSEs gives Q≈−0.011650, close to bootstrap mean−0.011636 versus observed−0.005715. **A ratio of expectations is not the expectation of a ratio: this checks the center shift, not a corrected estimate or interval.** Exclusion of the estimate alone is not a general percentile-interval error criterion, but a material quadratic-estimator bias mechanism is identified here. Nominal95% coverage is unverified. Retain finite-panel errors and original NON_SUPPORT; population directional inference is insufficient. [First audit](evidence/review.json)

**R2 reasoning corrections.** The [12 traceable findings](evidence/reasoning_audit_final.json) are resolved as follows:

| Inference gap | Final repair |
| --- | --- |
| Structure existence versus prototype utility | Restrict Q to empirical means; retain weak true association and estimation variance as competing explanations |
| Program field versus statistical eligibility | Preserve NON_SUPPORT; separately mark population directional evidence insufficient without rewriting thresholds |
| SVD dimensions, output rank and denominators | Distinguish full W-gradient directions, a directions and PG projection; see §7 |
| SAE energy versus compatibility | Separate diagonal trace from signed off-diagonal relations; restrict pooled-readout comparison |
| Domain averages versus record-level ability | Profile cosine concerns means; registered statistics do not exhaust higher-order or causal structure |
| Shared construction versus isolated mechanism | Expose K's c/e construction and CE derivative chain |
| Target conditioning assumed to remove confounding | Retain total and conditional associations; targets belong to the task; see §13 |
| Final text versus scientific closure | Finalize records only; human judgment and new design remain unconfirmed |

## 4. Actual Setup

Fresh S7 has an eight-layer dense281,431,040-parameter backbone and a61,471,024-parameter SAE. λ_rec=.1 belongs to training history; current gradients use NTP only. Checkpoint: `20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`, optimizer_step125894, state SHA `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`.

W is `model.blocks[7].attn.o.weight`,1024×2048, without bias. The30,000-atom TopK32 SAE observes native output before residual addition and does not replace it. FP32 eval, TF32/autocast disabled, FP64 full-vocabulary tail CE, individual residuals preserved. Qwen3-0.6B supplies only the original tokenizer assets, not model weights.

Historical `20260925_sae_domain_activation/selected.jsonl` supplies256-token records: input0..254 and output positions14,30,…,254 predict15,31,…,255. Domains/subfields: computer_science(cs.CL/cs.CV), mathematics(math.AG/math.NT), physics(physics.flu-dyn/physics.optics), biology(q-bio.GN/q-bio.NC);64 records per category per fit/test split. Panel SHA `7e8858adfbf1ead8330937dc147eee3eb815be9025e620e53c0af0fc86d155d9`.

This is historically exposed descriptive replication, not untouched confirmation. Record/input identities are unique; no cross-split exact duplicate or5-token Jaccard≥.80 near duplicate was detected. Paper IDs are unavailable. Original windows contain mixed-domain and formatting material, so source category is not pure semantics.

No optimization occurs. Fit512 estimates prototypes/axes/sets; readout512 measures replication. Seeds: bootstrap20261001, permutation20261002, random groups20261003, Gaussian QR31/43/59. Four workers partition record index mod4. Old21B activations, old MLP gradients and the old binary tail are rejected as current measurements.

## 5. Metrics And Registered Decision Rules

Q is dimensionless; raw-gradient MSE uses squared gradient coordinates of W. Registered support requires lower bound>0 and p≤.05; non-support requires upper bound≤0; otherwise insufficient, with separate measurement/variation guards. The automated rule returns NON_SUPPORT. An uncalibrated interval cannot complete the audited population directional determination, which remains insufficient. Unit/mean16, spectral, atom and scale descriptions do not substitute for valid primary inference.

**Why negative Q does not imply absent domain structure.** Let \(\widehat\mu_s^F,\widehat\mu_s^R\) be domain means and \(\widehat\mu^F,\widehat\mu^R\) pooled means. Set \(\widehat\delta_s^F=\widehat\mu_s^F-\widehat\mu^F\), analogously for R. In this balanced four-domain panel define

\[
B_F=\frac14\sum_s\|\widehat\delta_s^F\|^2,\qquad
H_{FR}=\frac14\sum_s\langle\widehat\delta_s^F,\widehat\delta_s^R\rangle.
\]

Domain deviations sum to zero in each split. Expanding squared errors yields the exact identities

\[
\operatorname{MSE}_{D}-\operatorname{MSE}_{0}
=B_F-2H_{FR},\qquad
Q_D=\frac{2H_{FR}-B_F}{\operatorname{MSE}_{0}}.
\]

Last: B_F=.643336, H_FR=.014834, MSE difference=.613669. Mean16: .043553, .005514 and .032525. Direct checks on saved Gram matrices close within1e−14. [Arithmetic audit](evidence/reasoning_audit_final.json) Empirical deviations can align weakly across splits without making their full fitted displacement useful. This neither establishes significant population H_FR nor validates shrinkage or another estimator. It is an identity check on existing measurements, not a new experiment.

## 6. Evidence Lineage

| Claim | Raw/intermediate artifact and computation | Observation/eligibility |
| --- | --- | --- |
| Domain prototype performance | Collection→Gram→frozen stats.py→primary | Q−.005715; valid panel statistic, uncalibrated interval |
| Common/domain/within energy | Gram→common_decomposition | .19%/.58%/99.23%; closure1.3e−16; fit description |
| SVD transfer | Gram and c/a/e→fit axes→cross-split coordinates | Top64 gradient3.18% versus a53.18%; conditional on fitted axes |
| Activation replication | Full indices/values→all-atom stats→fit sets→readout |65/99 common atoms meet same rule; source-category association |
| Decoder coverage | Frozen activation sets+decoder→P→PG | Common rank64 8.96%; exact projection, not causal use |
| Target/error relationship | Events+K→nuisance/alignment | Same-target cosine.193; e alignment.903; target-informed descriptions |
| Scale | K→100 fixed draws and subfield transfer | Mean16/m64 .104 versus.074; no population CI |
| Estimator/plot audit | Existing Gram, bootstrap arrays and primary→V/review.py | No recollection or replacement gate; original outputs retained |

Hashes and curated transformations are in [evidence/origins](evidence/origins.json), [figure origins](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/origins.json), R/registration and V/review. Independence is at most record-level, not pairs, tokens, atoms or random bases.

## 7. Main Results

Pooled MSE107.370350 versus domain107.984019. Last-unit Q−.005533, mean16−.005060, mean16-unit−.005182; no finite-panel improvement. Bidirectional subfield transfer gives last−.011600/−.012194 and mean16−.011665/−.010279. Permutation p=.022 means the statistic exceeds most generated shuffled-label values; population interpretation needs exchangeability and record-dependence assumptions and does not establish improvement over pooling. [Primary](evidence/primary.json), [scale](evidence/scale.json)

Centered last participation ratio238.72 and251 directions for90% fit energy; mean16 participation ratio399.80 and409 directions. Rank64 readout coverage: c34.50%, a53.18%, e18.15%, SAE frequency56.62%, SAE amplitude70.80%, last gradient3.18%, mean16 gradient4.83%. Two axes do not summarize full update demands. [Spectrum](evidence/spectral_reading_rows.csv)

Each fraction uses its own readout energy centered on its fit mean. Spaces differ in dimension and geometry. W gradients have2,097,152 coordinates but only512 fit records, limiting centered sample rank to511; this cannot identify population intrinsic dimension. The analysis measures pooled spectra and common/domain/within energy decomposition, not separately identified transferable domain-specific spectral axes.

**Two rank64 analyses are not equivalent.** Full-gradient SVD selects64 W-gradient directions. SAE rank64 is P in the1024-dimensional output space. Under column-major vectorization, \(\mathrm{vec}(PG)=(I_{2048}\otimes P)\mathrm{vec}(G)\), with operator rank131072. Its8.96% and gradient-SVD3.18% are not matched-budget results. Native-a PCA retains a-energy in the spectral table and gradient energy in the projection table;53.18% and6.74% use different denominators too.

| Body set | Fit qualifying | Same readout rule | Positive readout enrichment difference |
| --- | ---: | ---: | ---: |
| Common |99|65| N/A |
| Computer science |211|144|206|
| Mathematics |221|175|217|
| Physics |182|143|176|
| Biology |124|78|112|

Last-position same-rule replication is6/14 common,22/31 CS,45/67 math,34/53 physics and12/27 biology. Rule failure near a threshold need not be reversal. Body CS/biology sets share11 atoms and physics/biology6: enrichment is not exclusivity. Full-profile cosine compares domain means over records/positions, not an individual-record classifier. Common/enriched rules are not per-atom significance tests. [Audit](evidence/review.json); original A/atom_replication.csv.

| Readout domain | Observed atoms | Mean distinct atoms/record | Adjacent support Jaccard | Reconstruction relative squared error |
| --- | ---: | ---: | ---: | ---: |
| Computer science |10267|1080.66|.305|.0616|
| Mathematics |8380|923.21|.325|.0696|
| Physics |8924|1016.38|.317|.0601|
| Biology |10158|1105.68|.299|.0588|

Pooled readout observes14120 atoms; the remainder are unobserved on this panel, not globally dead. Every position has32 positive activations. Atom24605 fires at every position in all domains without receiving a semantic name. Amplitude-profile cosine is≥.9994 same-domain and≥.9794 cross-domain; frequency profiles distinguish domains more strongly. Common large amplitudes can dominate similarity. Full positive-value quantiles, position statistics, run lengths1..255 and sparse coactivation pairs are stored; display examples use fit selection only. [All-atom table](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z/result/analysis/activation_stats.csv)

Descriptive summaries of existing run-length tables show68.9–71.4% of activation runs last one position, while runs≥16 account for10.7–14.4% of positive activation occurrences, highest in mathematics. Both brief changes and persistent background coexist. All100 fit-count-selected coactivation edges per domain reappear on readout; count-rank Spearman is.878 CS,.865 math,.838 physics,.671 biology. This frequency-selected subset does not establish generalization or semantic function for every edge. Full sparse counts remain available. [Audit](evidence/review.json)

For fit-selected body sets, rank64, pooled readout and the last target, common captures8.96% squared-gradient energy, four enriched sets5.12–5.41%, three random spaces6.21–6.31% and native-a PCA6.74%. Three seeds and matched rank do not match all decoder anisotropy or activation amplitude; this is not overall SAE superiority or a causal effect of commonness. Pooled trace does not determine whether each enriched set selectively helps its own domain.

Common off-diagonal K relative squared reconstruction error remains.803. Thus higher energy capture does not sufficiently explain signed compatibility; every projected Q remains negative. Registered signed block relations are in projection_domain_relations, not replaced by trace. Post-hoc all-atom frequency/direction-energy Spearman is.005–.023, or.080–.165 among observed last-firing atoms. Many zero frequencies and overlapping decoder directions prevent independent-atom significance or functional attribution. [Projection](evidence/projection_results.csv), [audit](evidence/review.json)

Last K alignment: e=.903, c=.00513, a=.00315, SAE frequency=.00557. K is constructed from c/e, so this is not independent evidence that only e matters, and low alignment does not establish absent nonlinear predictive information. Centering precedes diagonal removal and still depends on sample diagonal norms. Identical-target1944 directed pairs have meanK5.797 and cosine.193; different-target259688 pairs have meanK−.0384 and cosine.000458. Context, predictions and Jacobians change jointly between groups; target causality is not isolated. Pair counts are not independent samples. Four-domain block alignment also reflects prototype self-energy and rank≤3 construction and is not independent replication evidence.

## 8. Visualization Results

All nine figures were visually inspected. Same33B state/panel throughout; values and units come from source tables. Figure observations are not new tests. [Origins and hashes](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/origins.json)

| Figure/purpose | Source, aggregation, reading, observation and limit |
| --- | --- |
| [Domain K matrices](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/domain_compatibility.png) | domain_relations; readout directed-pair means excluding self. Raw last means mix signs, unit blocks are slightly positive, mean16 blocks positive. Not every pair is compatible |
| [Spectral transfer](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/update_spectra_transfer.png) | spectra; relative singular values and readout energy by fit rank. Weak top64 transfer; sample rank is not population rank |
| [Energy decomposition](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/common_domain_within.png) | energy_decomposition; fit squared-gradient fractions, within>99%. Small means do not establish no domain information |
| [Audited primary display](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/domain_generalization_audited.png) | Unchanged primary values; separate points/endpoints reveal bootstrap displacement. Not calibrated intervals |
| [Fixed fit coordinates](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/common_fit_coordinates.png) | Spectral arrays;512 readout records, separate axes per space. Activation structure visible; gradient plane captures only≈.1% |
| [All atoms and examples](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/sae_activation_patterns.png) | Patterns+sets; all30000 frequency ranks and fit-selected readout heatmap. Zeros/common/enriched retained; no semantic labels |
| [Position/persistence/coactivation](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/sae_position_persistence_coactivation.png) | Position profiles/records/display edges; eight bins, record Jaccard and fit-selected readout edge counts. Domain differences; examples are not all atoms |
| [SAE gradient coverage](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/sae_update_span_capture.png) | Projection table; actual output rank, trace and fit-between-domain fractions. Common exceeds random; fit capture is not readout domain effect |
| [Aggregation scale](../../../../../../../daily_research_reports/backup/2026/09/0930/figures/domain_update_geometry/aggregation_scale.png) | Scale;100 draw-mean cosines, not CIs. Mean16/m64 .104 true versus.074 mixed. Separate averaging from grouping |

## 9. Stage Evidence And Failure Decomposition

S0 provenance/data qualified with historical exposure and unknown paper dependence. S1 Smoke PASS. S2 complete four-shard collection. S3 fit choices frozen. S4 all analyses complete. S5 figures/records complete with estimator/display audit. Smoke last/mean16 outer-product error0, non-target derivative ratio0, Wc error0; OPS CE maximum9.30e−6, full tail maximum1.63e−5, below2e−5. Projection closure approximately1.4e−14.

No gradient identity is falsified and no absence-of-domain mechanism is established. This panel shows no gain for unshrunk empirical domain means and no pooled-rank64 energy advantage for the selected enriched sets. Weak reproducible association and estimation error masking association remain unresolved rivals. Bootstrap calibration and record dependence further limit population direction. Target composition, downstream sensitivity, source and scale can act jointly; none is an established sole cause.

## 10. Full Experiment Record

One round, archived under0930 and executed on2026-09-29 UTC. Question/hypothesis:§2. Model/controls/data:§4. No training; fit512 for analysis and readout512 for replication. Results:§7. Job pt-t33awf9u submitted19:38:37, platform start19:41:21; runner230.05seconds, all mandatory artifacts present, zero retries. [Execution certificate](execution_record.md). Insight: domain structure in activations and updates must be measured separately. A future scientific choice is not automatically approved.

## 11. Interpretation

**AI interpretation, awaiting researcher judgment:** replicated domain-mean activation, negative prototype Q and higher energy capture by selected common decoder directions can coexist without contradiction. Common activation is not a common update direction; a small mean gradient does not preclude shared reusable subspaces. The primary result first constrains the estimator, not all domain structure. e geometry and target strata motivate hypotheses without separating target composition, context and Jacobians. Retain the bounded common-set coverage result without extending it to interference causality or Router benefits.

## 12. Claim Boundary

Can claim finite-panel prototype errors, within-space spectral transfer, registered domain-mean/per-atom activation statistics and specified pooled-span energy coverage. Completing all registered statistics does not identify every higher-order activation combination or causal function. Cannot claim universal semantics, causal feature use, irreducible conditional uncertainty, population domain-effect exclusion, own-domain selective benefit, actual finite-step loss, training benefit, larger-model conclusions or expert separation. Representation-only K prediction was not retested; low alignment is not that test. Label association is not label-free prospective routing success.

## 13. Next Decision

**One AI-proposed next question:** how much domain-associated K structure co-varies with target composition and aggregation scale, and how much remains under comparable target conditions? Targets are part of natural learning demand: domain differences in \(P(y\mid s)\) may contribute to total domain association. Conditioning changes the question; removed association is not automatically spurious.

The minimal distinguishing logic is to report total and conditional associations on a future prespecified grouping/scale, restricting conditional comparisons to common target support. Fit selection, estimator calibration and independent-record eligibility precede readout. Stable conditional gains support a bounded relation beyond those target conditions; qualified precise results below a prespecified effect weaken that relation without denying total association; sparse target overlap, unstable estimates or uncalibrated intervals are insufficient. Conditioning on target identity does not isolate semantics or establish causality.

The researcher still chooses whether to adopt this question. Specific target relationships, effect thresholds and a future protocol are not approved. No new experiment or replacement interval is generated here. Finalization concerns the factual result text; human scientific judgment remains Unknown.

## 14. Artifact Manifest

| Artifact | Completion/use | Authoritative location/identity |
| --- | --- | --- |
| Frozen design/code | COMPLETE; scientific contract/implementation | R/registration and source; Protocol hashes above |
| Submission/device/Smoke/freeze | COMPLETE; engineering qualification | Run submission JSON, R/smoke_receipt, verification |
| Events/gradients/SAE arrays | COMPLETE; raw measurements | R/collection/shard_0..3; A/measured_events, mean16_gradients |
| K/prototypes/spectrum | COMPLETE; primary/secondary | A/gram_matrices, fit_prototypes, spectra, spectral |
| Full activations/patterns | COMPLETE;300000 statistic rows | A/activation_stats, patterns, position_profiles, runs, coactivation |
| Sets/replication/context | COMPLETE; fit-only selection trace | A/atom_selection_frozen, atom_sets, atom_replication, atom_contexts |
| Atom energy/projections | COMPLETE;240000 direction rows,54 projections | A/atom_gradient_energy, projection_results, projection_domain_relations |
| Scale/nuisance | COMPLETE; descriptions | A/scale, nuisance, event_norms, kernel_alignment |
| Result audit | COMPLETE; bounded inference/display repair | V/review.py/json; curated evidence/origins |
| R2 final reasoning audit | COMPLETE;12 inference repairs and saved-Gram identity check | V2/audit.json, before snapshots; evidence/reasoning_audit_final.json |
| Figures | COMPLETE; nine PNG/PDF reading copies | Dated figures/domain_update_geometry and origins |

## 15. Links

[Summary](summary.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_12_domain_update_geometry/17_12_domain_update_geometry_anchor.md) · [Protocol](protocol.md) · [Focus](../../../../focus/focus_domain_update_geometry.md) · [Execution](execution_record.md) · [Code](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/scripts) · [Data manifest](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/data/data_manifest.json) · [Results](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/runs/20260929T193805Z/result) · [Audit code](/data/250010109/MoE_Router/experiments/20260930_domain_update_geometry/reviews/20260929_result_audit/review.py). Reproduction uses runtime.sh then scripts/run.py --out with a new, nonexistent output root; this pointer is not renewed run authorization. Job:pt-t33awf9u.
