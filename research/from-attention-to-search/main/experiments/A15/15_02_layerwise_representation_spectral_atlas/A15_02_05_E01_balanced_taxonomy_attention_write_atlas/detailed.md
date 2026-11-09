# Detailed: A15_02_05_E01 Balanced-Taxonomy Attention-Write Atlas

Primary Anchor: [A15_02_05](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_05_balanced_taxonomy_attention_write_atlas_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), `A15_02_05_E01_r1`  
Summary: [summary.md](summary.md)  
Result eligibility: **ELIGIBLE**, with one documentation-only provenance deviation and one rendering-only revision recorded below.

Judgment status: the registered numerical verdict is fixed; the interpretation is an AI-drafted bounded reading under the researcher's execution delegation and awaits researcher correction or confirmation.

## 0. Quick Recap

**Purpose:** determine whether sibling-relative fine semantic residuals acquire a depth-dependent local spectral position beyond coarse parent residuals, while separating absolute strength, normalized allocation, broad-band averaging, and direction stability.

**Hypothesis:** the late-minus-early change in fine-minus-coarse normalized local-rank centroid, \(T_\rho\), is positive and survives the registered semantic and basis controls.

**Experiment logic:** freeze one balanced 512-record academic taxonomy, extract the isolated attention write and actual attention-induced MLP-input increment from all 36 Qwen3-8B blocks, define each layer's F1--F16 basis from independent DCLM activations, and compare matched coarse and conditional-fine residuals under split, permutation, and Haar controls.

**Direct result:** \(T_\rho=-0.009573\) with registered one-sided 95% lower/upper bounds [-0.011199, -0.004492].

**Eligibility:** all data, extraction, semantic-reliability, basis, numerical, resampling-count, resource, and visual guards pass. The missing pre-execution command-manifest file is reconstructed from the pre-run-hashed runner and ordered run log; it does not make any scientific input or operation ambiguous.

**Verdict:** `nonpositive_location_fail`.

**Claim boundary:** this is a static representation-localization result for one model, one taxonomy, one readout, and layer-local DCLM rank bases. It is not a causal-use, Router, expert, or training result.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| coarse residual | one broad academic domain against the other domains | parent center minus leave-one-parent-out center | activation vector | matched control for broad semantics | a pure parent concept |
| conditional-fine residual | one child field against its siblings inside one parent | child center minus leave-one-child-out sibling center | activation vector | operational fine-semantic treatment | child information independent of the parent |
| \(\Delta n_\ell\) | attention's actual same-layer change to the MLP input | \(RMSNorm_\ell(h_\ell+a_\ell)-RMSNorm_\ell(h_\ell)\) | activation | registered primary site | MLP causal use |
| attention write \(a_\ell\) | isolated post-`o_proj` attention output | captured before residual addition | activation | source-boundary control | the downstream state seen by the MLP |
| local DCLM spectrum | one layer/site's natural-background covariance ordering | eigenbasis of 65,536 independent DCLM calibration tokens | rank 1--4,096 | defines the coordinate used here | the same vector across layers |
| F1--F16 | sixteen consecutive equal-rank regions | 256 covariance directions per band | band index | exposes broad rank allocation | a functional module |
| absolute cross-expression energy \(A^\times\) | reproducible contrast strength across two wording halves | mean \(v^{A\top}P_{\ell k}v^B/256\) | activation squared per direction | prevents a normalized curve at zero signal from passing | causal information use |
| normalized share \(q\) | fraction of within-half squared contrast energy in one band | band energy divided by all-band energy | fraction, sums to one | describes allocation independent of total scale | absolute growth |
| rank centroid \(\rho\) | energy-weighted local-rank percentile | \(\sum_k (k-0.5)q_k/16\) | 0=head, 1=tail | compact location summary | direction identity or shared coordinates |
| \(T_\rho\) | extra fine-versus-coarse location change with depth | median blocks 25--35 minus median blocks 1--12 of \(\rho_F-\rho_C\) | normalized rank percentile | sole primary metric | which individual band or direction is useful |
| direction cosine | whether two residual vectors point similarly | cross-expression cosine after reliability mask | [-1,1] | tests vector stability | semantic equivalence |
| band-profile correlation | similarity of two F1--F16 energy shapes | Pearson correlation over 16 normalized shares | [-1,1] | tests coarse spectral-shape similarity | shared within-band direction |

## 2. Anchor Link And Decision Point

The Anchor asks one decision question: does a child concept's sibling-relative residual acquire a reproducible depth-dependent spectral location beyond coarse parent distinctions, and is that result inspectable rather than produced by averaging? The experiment addresses three evidence levels under that one decision: aggregate coarse/fine localization, registered measurement defects, and two named mathematics cases.

The experiment does not test whether a Router should use any band. A positive representation result would still require separate functional-coordinate admission; a Fail closes only the registered fine-specific rightward-localization relation.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Protocol | revision `A15_02_05_E01_r1`; frozen Sections 1--16 | scientific-body SHA-256 `9fb217...82fb` unchanged | pass | [protocol.md](protocol.md), [run audit](evidence/run_audit.json) | none |
| execution scope | implementation, preflight, 16-record extraction check, one local full run | exactly this scope executed; no remote submission | pass | Protocol approval receipt; `logs/run.log` | none |
| semantic data | 512 balanced, label-free records; `linear algebra` replaces `algebra` | 8 parents × 8 children × 4 templates × 2 bundles; SHA-256 `c37329...d88` | pass | [data audit](evidence/data_audit.json), [source hashes](evidence/source_hashes.json) | none |
| calibration data | frozen 128 × 512 DCLM tokens; no exact prompt/fact overlap | 65,536 tokens; zero exact prompt and fact matches | pass | [data audit](evidence/data_audit.json) | none |
| model and sites | frozen Qwen3-8B; \(\Delta n\) primary; \(a\) secondary | all 36 blocks and both sites captured | pass | [full hook audit](evidence/full_hook_audit.json) | none |
| matched contrasts | eight coarse and eight fine contrasts per rotation; eight rotations | complete; maximum registered rotation-to-aggregate \(\rho\) deviation 0.015122 | pass | [rotations](evidence/rotations.json), [rotation table](tables/matched_rotation_metrics.csv) | none |
| uncertainty and nulls | 2,000 bootstrap / 2,000 permutation / 1,000 Haar | exactly complete | pass | [verdict](evidence/verdict.json), null tables | none |
| numerical guards | hook/replay \(<10^{-6}\); projection reconstruction \(<10^{-5}\) | hook maxima 0; projection maximum \(7.662\times10^{-7}\) | pass | hook audit; [projection guards](tables/projection_energy_guards.csv) | none |
| resources | two H100s, 80 GiB, 12 hours | two H100s; 36.707 GB; under 30 minutes to initial artifact manifest | pass | [environment](evidence/environment.json), [run audit](evidence/run_audit.json) | none |
| command receipt | resolved commands and environment recorded before execution | environment recorded before execution; separate command-manifest file omitted | deviation | pre-run [code manifest](evidence/code_manifest.json), [post-hoc command reconstruction](evidence/command_reconstruction.json), ordered run log | documentation-only; exact operations remain identifiable, so eligible |
| central figures | four registered panels plus original-resolution audit | all four produced; Figure 3 labels and Figure 4 table repaired after inspection | rendering-only revision | [render revision](evidence/render_revision.json), [visual audit](evidence/visual_audit.json) | none; verdict and decision-table hashes unchanged |

Frozen Protocol revision: `A15_02_05_E01_r1`.  
Execution scope approved: yes, by the researcher's 2026-08-09 approval quoted in the Protocol.  
Amendments: none to Sections 1--16 and none to the scientific analysis.  
Retries and exclusions: no scientific retry, record exclusion, layer exclusion, or post-result threshold change. Block 36 remained the registered terminal diagnostic.  
Missing conditions or artifacts: no scientific condition is missing. The separate pre-execution command manifest is the documented provenance deviation above.  
Post-hoc analyses: none enter the verdict. The regional and named-case readings below use only preregistered tables. The rendering repair changed labels/layout only.

## 4. Actual Setup

**Research question:** does conditional-fine semantic structure move to later layer-local covariance ranks beyond coarse semantic structure?

**Data construction and provenance:** 512 English descriptions with no explicit parent/child labels: eight academic parents, eight children per parent, four wording templates, and two disjoint three-fact bundles. Mathematics contains `linear algebra`, analysis, geometry, topology, number theory, combinatorics, probability, and statistics. Natural token counts span 41--58; all sequences are left padded to 58 and read at absolute position 57.

**Train / development / confirmation split:** no training occurs. Templates 0--1 form expression half A and templates 2--3 form expression half B. The DCLM calibration set is split into two ordered 32,768-token halves for independent bases.

**Learning task and permitted supervision:** no learned classifier, probe, Router, expert, objective, or parameter update. Taxonomy labels are used only after activation extraction to form registered offline contrasts.

**Model / architecture / algorithm:** `/data/share/Qwen3-8B`, 36 blocks, hidden width 4,096. The model configuration SHA-256 is `deaa300...2ffb`; tokenizer SHA-256 is `aeb133...dae4`.

**Input representation / position encoding:** the same padded geometry and explicit absolute position IDs are used for all records. Primary representation is \(\Delta n\); isolated post-`o_proj` \(a\) is secondary.

**Training objective and constraints:** not applicable; model parameters are frozen.

**Optimizer or update rule:** none.

**Training steps / tokens / batch size:** no training. Calibration uses 65,536 tokens. Extraction uses calibration batch size 4 and semantic batch size 8 on two local GPUs.

**Checkpoints:** one frozen local Qwen3-8B checkpoint; no checkpoint selection.

**Seeds:** `20260809` for the registered analysis; deterministic extraction environment uses `PYTHONHASHSEED=0` and `CUBLAS_WORKSPACE_CONFIG=:4096:8`.

**Conditions and plain-language labels:** actual \(\Delta n\) primary atlas; isolated attention-write source replay; eight matched rotations; full and two half bases; expression halves; leave-one-parent-out; child-label permutation; same-dimensional Haar partitions; two named mathematics cases.

**Changed variables:** layer, semantic granularity, expression half, calibration half, and registered null assignment.

**Held fixed:** model, record bank, readout token/position, padding, representation definitions, layer windows, band sizes, contrast counts, aggregation, resampling counts, and verdict thresholds.

**Code / config / data identities:** pre-run code hashes are in [code_manifest.json](evidence/code_manifest.json); data/model/calibration hashes are in [source_hashes.json](evidence/source_hashes.json).

**Script and result paths:** worker `XingyuD/MoE_Routing_Experiments/active/a15_02_05_e01_balanced_taxonomy_attention_write_atlas/`; raw run `/data/250010109/MoE_Router/experiments/20260809_a15_02_05_balanced_taxonomy_attention_write_atlas/runs/a15-02-05-e01-20260809T165500Z/`.

**Known setup limitations:** the taxonomy is operational rather than a validated equal-depth ontology; the bank has no independent parent-only descriptions; local ranks do not identify the same cross-layer vector; all data are English and from one model/readout.

## 5. Metrics And Registered Decision Rules

For each layer \(\ell\), granularity \(g\), and band \(k\), \(A^\times_{\ell gk}\) measures cross-expression activation-squared energy per direction, and \(q_{\ell gk}\) is its within-half normalized allocation. The rank centroid is

\[
\rho_{\ell g}=\sum_{k=1}^{16}\frac{k-0.5}{16}q_{\ell gk}.
\]

The primary statistic is

\[
T_\rho=
\operatorname{median}_{25:35}(\rho_{\ell F}-\rho_{\ell C})
-
\operatorname{median}_{1:12}(\rho_{\ell F}-\rho_{\ell C}).
\]

Pass requires a positive lower one-sided 95% bootstrap bound, an estimate above the parent-preserving permutation q95, positive expression- and calibration-half estimates, and no negative leave-one-parent-out estimate. `nonpositive_location_fail` requires all mandatory guards to pass and the upper one-sided 95% bound to be at or below zero. An interval crossing zero or any failed mandatory guard is Insufficient.

Named cases and the isolated attention write are typed diagnostics only. They cannot override the primary \(\Delta n\) verdict.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| semantic contrasts are measurable | positive root-bootstrap lower bounds in early and late windows | `full_consolidated/semantic_states/`; [bootstrap](tables/bootstrap.csv) | frozen `analyze.py` | root-family bootstrap, 2,000 draws | coarse early/late lower bounds \(6.890\times10^{-5}\) / \(4.297\times10^{-4}\); fine \(7.012\times10^{-5}\) / \(8.646\times10^{-4}\) | eligible | reliability pass | strength is not function |
| fine-specific rightward relocation | upper bound \(\le0\) gives registered Fail | [primary table](tables/primary_layer_metrics.csv), [bootstrap](tables/bootstrap.csv) | frozen \(T_\rho\) | equal parent/rotation weight; early/late medians; root bootstrap | -0.009573; bounds [-0.011199, -0.004492] | eligible | `nonpositive_location_fail` | one model/bank/site |
| sign does not depend on wording or basis split | both expression and calibration halves retain sign | [expression halves](tables/expression_half_metrics.csv), [calibration halves](tables/calibration_half_metrics.csv) | frozen split replay | two prespecified halves each | expression -0.008048/-0.009896; basis -0.010694/-0.005900 | eligible | stable nonpositive sign | only two fixed halves |
| no single parent drives the result | every leave-one-parent-out estimate nonpositive | [leave-one-parent-out](tables/leave_one_parent_out.csv) | frozen family deletion | eight root-family deletions | [-0.010891, -0.007446] | eligible | stable across parents | not population replication |
| semantic identity does not provide positive specificity | estimate must exceed permutation q95 for Pass | [permutation null](tables/permutation_null.csv) | parent-preserving label permutation | 2,000 draws | observed -0.009573; q95 -0.006383 | eligible | no positive specificity | null distribution need not center at zero |
| DCLM ordering is not a generic positive random-partition effect | compare with exact Haar partitions | [Haar null](tables/haar_null.csv) | exact quadratic-summary Stiefel partitions | 1,000 draws | Haar q95 +0.002275; observed negative | eligible secondary | positive relocation absent | not a two-sided causal test |
| no corrected replacement band is established | max-absolute-statistic correction over 16 bands | [band changes](tables/band_depth_changes.csv) | frozen band audit | early/late band medians; 2,000 permutations | only normalized F1 is corrected-significant; no absolute band is | eligible secondary | no admitted middle/tail replacement | broad trends remain descriptive |
| result depends on representation site | report \(a\) without changing verdict | [source boundary](tables/source_boundary.csv) | same contrasts on isolated write | same registered windows | \(T_\rho(a)=+0.011327\) versus \(T_\rho(\Delta n)=-0.009573\) | bounded secondary | site-dependent sign | no uncertainty rule registered for \(a\) |
| named residuals are readable | positive same-layer split reliability before unmasking | [named metrics](tables/named_case_metrics.csv) | frozen split-half cosine | all 36 blocks | minimum 0.603 combinatorics; 0.639 linear algebra | eligible diagnostic | both cases readable | readability is not causal use |
| band-shape similarity is not direction identity | compare requested pair to all mathematics pairs | [pair controls](tables/mathematics_pair_controls.csv) | frozen same-layer comparison | 36 layers; 28 pair envelope | median profile correlation 0.9943; median direction cosine -0.1801 | eligible diagnostic | aggregate heterogeneous | shared sibling reference remains |

## 7. Main Results

### 7.1 Eligible decision evidence

The paired fine-minus-coarse centroid is positive in the early window (+0.009334) and approximately zero/slightly negative in the late window (-0.000239). Their difference is the negative primary result. Block 36 is also negative (-0.005593) but is not part of either decision window.

All reliability lower bounds are positive. Median total fine cross-expression energy grows from \(8.009\times10^{-5}\) early to \(9.407\times10^{-4}\) late, while coarse grows from \(8.980\times10^{-5}\) to \(5.211\times10^{-4}\). These separate-window medians describe strength only; subtracting their separate location medians is not the registered paired \(T_\rho\) computation.

The bootstrap distribution has q05 -0.011199, median -0.007925, and q95 -0.004492. Both expression halves, both basis halves, and all leave-one-parent-out estimates retain the nonpositive direction. This is a precise Fail, not an underpowered estimate.

### 7.2 Bounded secondary evidence

The absolute-location moment changes by +0.000285, but no individual band's absolute fine-minus-coarse depth change survives max-statistic correction. The normalized F1 change is -0.015421 and is the only corrected bandwise result. F2--F7 are descriptively positive, while F8--F16 are negative, but the experiment has no registered post-Fail rule that promotes their union. No corrected positive/negative opposing-band pair exists, so `redistribution_without_centroid_shift` is not certified.

The isolated attention write has a positive descriptive \(T_\rho\) while actual \(\Delta n\) is negative. This localizes a measurement boundary: the spectral statement changes across two adjacent representation sites. It does not identify whether residual addition, RMSNorm scale, direction interaction, or another component is causally responsible.

### 7.3 Named-case diagnostics

| Named residual | minimum same-layer split reliability | early median \(\rho\) | late median \(\rho\) | raw child \(T_\rho\) | block 36 \(\rho\) |
| --- | ---: | ---: | ---: | ---: | ---: |
| combinatorics within mathematics | 0.6034 | 0.1327 | 0.2062 | +0.0735 | 0.1927 |
| linear algebra within mathematics | 0.6389 | 0.1295 | 0.1865 | +0.0570 | 0.1717 |

Each named residual individually moves to a later local-rank centroid. This answers the case-level descriptive question, but it does not answer the fine-versus-coarse interaction because the registered control also relocates with depth.

The two named cases have early/late median same-layer direction cosines -0.2815/+0.0455, while their 16-band-profile correlations are 0.9973/0.9863. Across all layers, the requested pair has median direction cosine -0.1801 and median profile correlation 0.9943. Its median layerwise positions are the 31st percentile for direction cosine and 46th percentile for profile correlation among the other mathematics pairs, so it is not a registered outlier.

Within each named case, cross-layer direction identity is weak: early-to-late median cross-expression cosines are 0.0024 for combinatorics and 0.0034 for linear algebra. The corresponding cross-layer band-profile medians are 0.9416 and 0.9623. Thus a stable-looking F1--F16 allocation can coexist with almost orthogonal layerwise residual directions.

### 7.4 Failed, ambiguous, and non-evidence items

- A positive isolated-write point estimate cannot rescue the actual-\(\Delta n\) primary Fail.
- Named cases cannot substitute for the 64-child aggregate or demonstrate a pure `child - mathematics` vector.
- F2--F7 cannot be selected after seeing the result as a new middle coordinate.
- No smoothed curve enters any statistic; Figure 2's direction-level data are unsmoothed.
- No Router, expert, loss, task accuracy, or intervention was run.

## 8. Visualization Results

### Coarse/fine strength and registered location

![Coarse/fine strength and registered location](figures/figure1_strength_and_location.png)

Purpose: show whether the primary Fail is due to absent semantic strength or to the relative spectral-location relation.  
Source: [primary_layer_metrics.csv](tables/primary_layer_metrics.csv).  
Metric and unit: cross-expression activation squared per direction; normalized local-rank percentile.  
How to read: the first two panels show separate coarse/fine trajectories; the third is the paired fine-minus-coarse quantity used by \(T_\rho\). Blue shading is blocks 1--12, orange shading blocks 25--35, and the dotted boundary separates diagnostic block 36.  
Take-home: strength is present and increases, while the registered extra fine right shift is nonpositive.  
Cannot prove: shared directions or causal use.

### Full F1--F16 and direction-level redistribution

![Full spectral difference atlas](figures/figure2_full_spectral_difference_atlas.png)

Purpose: expose whether the centroid hides absolute/normalized band changes or within-spectrum cancellation.  
Source: [full_band_metrics.csv](tables/full_band_metrics.csv); raw 4,096-direction table remains in the worker run.  
Metric and unit: activation squared per direction and normalized-share difference.  
How to read: the absolute and normalized panels use separate scales; the final panel shows unsmoothed fine-minus-coarse direction shares at five registered layers.  
Take-home: there is broad reallocation but no corrected middle/tail replacement and no opposing-band cancellation certificate.  
Cannot prove: a useful band or post-hoc endpoint.

### Named mathematics residuals

![Named mathematics residuals](figures/figure3_named_mathematics_residuals.png)

Purpose: show each registered child's absolute/normalized band pattern and reliable cross-layer direction matrix.  
Source: [named_case_band_metrics.csv](tables/named_case_band_metrics.csv), [named_cross_layer_direction.csv](tables/named_cross_layer_direction.csv).  
Metric and unit: activation squared per direction, normalized share, and cosine.  
How to read: both rows have strong low-rank band allocation, but off-diagonal direction similarities are weak.  
Take-home: both cases are readable and have later raw centroids, yet neither supplies a stable transported direction.  
Cannot prove: population generality or semantic equivalence.

### Requested-pair position and measurement guards

![Requested-pair correlation and defect audit](figures/figure4_case_correlation_and_defects.png)

Purpose: compare the requested pair with all mathematics pairs and expose registered defects/robustness checks.  
Source: [mathematics_pair_controls.csv](tables/mathematics_pair_controls.csv), [defect_audit.csv](tables/defect_audit.csv), [verdict.json](evidence/verdict.json).  
Metric and unit: cosine, Pearson correlation, and \(T_\rho\).  
How to read: the red curve is combinatorics versus linear algebra; the grey envelope is the other-pair q10--q90. The table reports self-inclusion, contrast count, token count, cancellation, expression-half, basis-half, and leave-parent checks.  
Take-home: the pair is spectrally shape-similar but not direction-identical or unusual relative to its shared-parent controls.  
Cannot prove: pure semantic subtraction, composition, or function.

The final original-resolution audit is [visual_audit.json](evidence/visual_audit.json). All four figures pass their registered reading contracts.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| data identity | 512/512 records; balanced crossings; zero exact DCLM overlap | pass | none | imbalance, explicit labels, exact leakage | taxonomy-depth mismatch |
| tensor identity | 16-record smoke and 512-record full hook audits; zero replay errors | pass | none | wrong hook or \(\Delta n\) construction | semantic interpretation of the tensor |
| local basis | full/two-half eigensystems; projection error \(<7.662\times10^{-7}\) | pass | none | numerical or reconstruction failure | cross-layer direction identity |
| absolute reliability | all four early/late lower bounds positive | pass | none | normalized result at zero semantic signal | function and sufficiency |
| primary location | upper bound -0.004492 | fail H1 | fine-specific depth interaction is nonpositive | registered extra right shift | other forms of layerwise organization |
| semantic/basis/parent robustness | all estimates negative | pass as falsifier | none | single wording half, basis half, or parent as cause | other datasets/models |
| band/cancellation audit | one corrected normalized band; zero corrected absolute bands; no opposing signs | no rescue | no registered middle/tail certificate | centroid hiding a corrected opposing-band effect | independent middle audit |
| named cases | reliable, raw right shifts, unstable directions | typed heterogeneous | cases do not match a shared transported vector | average-only direction interpretation | case-specific rotating representations |
| visual audit | four final figures pass | pass | initial labels/table repaired | unreadable/mislabelled evidence | human judgment wording |

**Falsified physical prior:** depth does not add a fine-specific rightward local-rank allocation beyond coarse semantics at the actual \(\Delta n\) site in this setup.

**Falsified mathematical model:** the sign clause \(T_\rho>0\) for H1.

**Falsified operationalization / proxy:** no; conditional-fine residuals are reliable, and the tensor/basis implementation passes. The result rejects the relation rather than the ability to measure it.

**Falsified implementation:** no scientific implementation guard failed.

**Falsified metric:** no; the metric is precise and gives the registered negative verdict. It remains only a location summary, not a function metric.

**Remaining rival explanations:** site-specific residual/RMSNorm reorientation; within-middle redistribution too diffuse for this 16-band correction; child-specific trajectories with rotating within-band directions; model/taxonomy specificity.

## 10. Full Experiment Record

| Stage | Actual execution | Receipt |
| --- | --- | --- |
| freeze and tests | 19 source files frozen before smoke; 21 pre-run tests passed | `provenance/code_manifest.json`, `logs/unit_tests.log` |
| data preflight | 512 records and 65,536 calibration tokens validated | `provenance/data_audit.json` |
| extraction check | 16 records; blocks 1/18/35/36; two sites; two GPUs | `provenance/smoke_hook_audit.json` |
| full extraction | 512 records × 36 blocks × two sites complete | `provenance/full_hook_audit.json` |
| local bases | full plus two half bases per layer/site complete | `full_bases/basis_manifest_rank00.json`, `rank01.json` |
| sealed analysis | 36/36 layers; 2,000/2,000/1,000 resamples; 183.0 seconds | `analysis/verdict.json`, `analysis/tables/` |
| render/audit | four figures; visual correction; final `PASS` | `analysis/provenance/`, `provenance/run_audit.json` |
| final implementation verification | 24 tests pass after adding three rendering regressions | worker `tests/` |

Run identity: `a15-02-05-e01-20260809T165500Z`. The initial complete artifact manifest was written at 2026-08-09 17:24 UTC; the final visual audit passed at 17:30 UTC. No scheduler or remote job ID exists. Total raw-run size at final audit was 36,707,450,533 bytes, below the 80 GiB ceiling.

## 11. Interpretation

The result changes the interpretation of “deeper means later in the spectrum.” Coarse and fine semantic contrasts both become stronger and their raw centroids can both move right. The question relevant to granularity is the paired difference: does fine structure move later **more than** coarse structure at the same layers? In actual \(\Delta n\), that extra movement disappears and becomes precisely nonpositive.

The named cases explain why broad spectral curves are insufficient. Combinatorics and linear algebra retain nearly identical 16-band shapes, and each case retains high band-profile similarity across layers, while their underlying residual directions rotate enough that off-diagonal cosines are near zero. A band can therefore describe where energy lies without identifying what semantic direction lies there. This is useful negative knowledge for a later Router: a fixed band label is not yet a semantic routing coordinate.

The positive isolated-write point estimate and negative actual-input estimate make the representation site part of the claim. A layerwise statement must name whether it concerns the source write or the state actually passed to the MLP. The present experiment cannot decide which operation causes the sign change, only that the sign is not site-invariant.

## 12. Claim Boundary

**Can claim:**

- the frozen 512-record bank contains reproducible coarse and conditional-fine residual structure at every registered decision level;
- the actual-\(\Delta n\) fine-specific depth-location relation fails precisely under the registered metric and guards;
- the sign differs descriptively at the isolated attention-write site;
- combinatorics and linear algebra have reliable residuals and very similar band shapes but weak direction identity;
- no registered bandwise or named-case diagnostic rescues H1.

**Cannot claim:**

- fine semantics are absent or not useful;
- deeper layers never form new or more detailed semantics;
- an independent mathematics vector was subtracted;
- residual addition or RMSNorm causally destroys the signal;
- middle or tail has a universal semantic role;
- band-profile stability implies direction stability;
- any Router, expert selection, model quality, or training benefit follows.

## 13. Next Decision

**Decision:** review and either approve or correct the independent A15_03 middle-band decomposition with explicit absolute-energy, within-middle, cross-layer-direction, representation-site, and Haar controls.

**Completion criterion:** A15_03 freezes one middle object and one primary verdict that distinguishes real within-middle stability from normalization, broad-band averaging, cancellation, and direction rotation, without using post-hoc bands or named cases to rescue the result.

**Resume action:** treat this atlas as descriptive evidence only and continue through A15_08's residual-relative held-out accessibility gate. Do not begin a Router or expert experiment from a fixed band or normalized rank shift.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [protocol.md](protocol.md) | frozen decision contract | `A15_02_05_E01_r1` | approved Anchor | body `9fb217...82fb` | yes | yes | Sections 1--16 unchanged |
| [code_manifest.json](evidence/code_manifest.json) | pre-run source identity | `freeze_code.py` | worker source | manifest `b8aaeb...136f` | yes | yes | original render hash retained |
| [data_audit.json](evidence/data_audit.json) | balance/leakage/readout checks | `prepare_data.py` | semantic/DCLM manifests | `3a5b35...72c` | yes | yes | 512 records, zero exact overlap |
| [full_hook_audit.json](evidence/full_hook_audit.json) | tensor identity and completeness | extraction/consolidation | full activations | `6b9554...f62` | yes | yes | 36 blocks, two sites |
| [verdict.json](evidence/verdict.json) | typed result and guards | frozen `analyze.py` | tensors, bases, nulls | `4abdf5...d92` | yes | yes | primary source of verdict |
| [primary_layer_metrics.csv](tables/primary_layer_metrics.csv) | layerwise primary inputs | frozen `analyze.py` | matched contrasts | `abd285...7ec` | yes | yes | 36 rows |
| [bootstrap.csv](tables/bootstrap.csv) | uncertainty | frozen `analyze.py` | root-family draws | `683dc6...d6a` | yes | yes | 2,000 rows |
| [permutation_null.csv](tables/permutation_null.csv) | semantic grouping null | frozen `analyze.py` | child permutations | `33f6c7...543` | yes | yes | 2,000 rows |
| [haar_null.csv](tables/haar_null.csv) | random-coordinate null | frozen `analyze.py` | exact Haar partitions | `ce59fc...13f` | yes | secondary | 1,000 rows |
| [figure contracts](evidence/figure_contracts.json) | allowed reading for four figures | final render revision | decision tables | `ed2c87...76a` | yes | yes | visual audit passed |
| [render revision](evidence/render_revision.json) | before/after visualization trace | `visualization_only_r1` | unchanged tables | source after `19208b...0e6` | yes | yes | no statistic changed |
| [run audit](evidence/run_audit.json) | final completeness/resources | `audit_run.py` | required artifacts | visual `PASS` | yes | yes | 36.707 GB |
| [raw artifact manifest](evidence/raw_artifact_manifest.json) | complete raw-run hash map | final manifest pass | 330 raw files, excluding the manifest itself | `ed01f3...a60` | yes | by linked artifact | includes command and visual receipts |
| raw run | tensors, bases, contrasts, direction table, logs | run ID above | all frozen inputs | local absolute path below | yes | by linked manifest | not copied into mainline |

## 15. Links

- anchor: [A15_02_05 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_05_balanced_taxonomy_attention_write_atlas_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_02_05_e01_balanced_taxonomy_attention_write_atlas/`
- runner: `scripts/run_local.sh`, pre-run SHA-256 `92201b...9abd`
- config: `/data/share/Qwen3-8B/config.json`, SHA-256 `deaa300...2ffb`
- data / manifest: raw run `provenance/semantic_manifest.json`; dataset SHA-256 `c37329...d88`
- result directory: `/data/250010109/MoE_Router/experiments/20260809_a15_02_05_balanced_taxonomy_attention_write_atlas/runs/a15-02-05-e01-20260809T165500Z/`
- figure directory: [figures/](figures)
- logs / checkpoints: raw result directory `logs/`; frozen model `/data/share/Qwen3-8B`; no new checkpoint
- reproduction command: set the registered `RUN_ROOT`, then invoke the pre-run-hashed `scripts/run_local.sh`; exact sequence is in [command_reconstruction.json](evidence/command_reconstruction.json)
- job IDs: none; local execution only
