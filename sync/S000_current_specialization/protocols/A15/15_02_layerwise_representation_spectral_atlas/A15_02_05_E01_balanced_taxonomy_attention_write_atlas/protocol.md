---
experiment_id: A15_02_05_E01_balanced_taxonomy_attention_write_atlas
anchor_id: 15_02_05_balanced_taxonomy_attention_write_atlas
status: COMPLETED_ELIGIBLE_NONPOSITIVE_LOCATION_FAIL
canonical_language: en
created: 2026-08-07
revised: 2026-08-09
---

# Protocol: Coarse--Fine Semantic Layerwise Spectral Localization

## 0. Approval Snapshot

- **Document status:** `COMPLETED_ELIGIBLE_NONPOSITIVE_LOCATION_FAIL`.
- **Approval status:** the researcher explicitly approved the complete design and authorized implementation, preflight, the 16-record extraction check, and the full run on 2026-08-09.
- **Block audit status:** A--G `CONFIRMED`.
- **Cross-block consistency:** `PASS`.
- **Execution scope approved:** implementation, model-independent preflight, the registered extraction check, and one complete local full run. Publication, root sync, Git commit, and push remain unauthorized.
- **Execution outcome:** the approved run completed; the final artifact and visual audits pass; the registered verdict is `nonpositive_location_fail`; no further execution is authorized by this Protocol.
- **Design frozen at / registered revision:** `2026-08-09T16:45:32Z` / `A15_02_05_E01_r1`; scientific-body SHA-256 is recorded below before the first activation-bearing command.
- **Purpose:** determine whether conditional-fine semantic residuals have a depth-dependent local spectral location distinct from coarse-domain residuals, while exposing normalization and aggregation defects and showing preregistered child cases.
- **Primary Anchor:** [A15_02_05](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_05_balanced_taxonomy_attention_write_atlas_anchor.md).
- **Anchor decision question:** does a child concept's sibling-relative residual acquire a reproducible depth-dependent spectral location beyond coarse parent distinctions, and is the aggregate result visible rather than averaged into existence?
- **Anchor prior tested:** semantic granularity may change normalized local spectral location with depth, but a valid interpretation requires absolute split-reproducible strength and case-level audit.
- **Anchor core term:** $T_\rho$, the late-minus-early change in the conditional-fine minus coarse normalized local-rank centroid.
- **Anchor falsifier:** reliable coarse and fine structure exists, but $T_\rho$ is nonpositive or no more specific than parent-preserving label permutations.
- **Experiment role:** static representation and metric audit; no model learning and no Router functionality test.
- **Primary metric:** $T_\rho$ on actual attention-induced MLP-input increment $\Delta n$.
- **Claim boundary:** one frozen Qwen3-8B, one English 512-record academic bank, local per-layer covariance ranks, and two named mathematics cases; no pure semantic subtraction, causal use, Router, expert utility, or training claim.
- **Minimal setup:** 512 label-free descriptions; 36 blocks; $\Delta n$ primary and isolated post-`o_proj` write secondary; independent DCLM bases; 16 equal-rank bands; expression/calibration halves; matched contrast rotations; label-permutation and Haar controls.
- **Treatment:** conditional-fine sibling residuals.
- **Control:** coarse leave-one-parent-out residuals, matched to eight contrasts per rotation.
- **Changed variable:** semantic granularity under the same prompt states and representation site.
- **Held fixed:** model checkpoint, 512-record manifest, readout position, layer windows, covariance calibration, band dimensions, expression counts, contrast count, aggregation, nulls, and plot rules.
- **Conditions:** aggregate $\Delta n$ atlas; source-write replay; matched rotations; absolute versus normalized analysis; expression/calibration halves; leave-one-parent-out; parent-preserving label permutation; Haar rank partitions; named-case correlations.
- **Pass:** all validity gates pass; the 95% lower bound of $T_\rho$ is above zero; the estimate exceeds permutation q95; expression halves, calibration halves, and leave-one-parent-out estimates do not reverse sign.
- **Fail:** validity gates pass and the interval is wholly nonpositive, or the interval is positive but the estimate does not exceed the registered permutation q95 (`nonspecific_location_fail`).
- **Insufficient:** the confidence interval crosses zero, or any data, reliability, basis, numerical, or precision gate fails.
- **Cannot claim:** an independent parent concept was subtracted; fine semantics are universally later-rank; the same direction moves across layers; attention/MLP uses the signal; any Router or expert would benefit.
- **Approval decision:** execute revision `A15_02_05_E01_r1` under the registered local resource and stop rules; any scientific change after start requires an append-only amendment.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Decision role | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| coarse residual | one parent domain relative to the other domains | parent center minus leave-one-parent-out center | activation | coarse control | a standalone parent concept vector |
| conditional-fine residual | one child field relative to sibling fields under the same parent | child center minus leave-one-child-out sibling center | activation | fine treatment | a purified fine-semantic feature |
| $\Delta n_\ell$ | actual change to this block's normalized MLP input caused by attention | $\operatorname{RMSNorm}(h+a)-\operatorname{RMSNorm}(h)$ | activation | primary representation | information creation or MLP use |
| local F1--F16 spectrum | one layer's DCLM activation-covariance directions sorted by variance | sixteen 256-direction projectors | rank percentile | location coordinate | cross-layer direction identity |
| absolute cross-expression energy $A^\times$ | semantic contrast that agrees across independent wording halves | cross-half projected inner product per direction | activation squared/direction | reliability and strength | causal utility |
| normalized allocation $q$ | fraction of within-half squared contrast energy in one band | band energy divided by all-band energy | fraction, sums to one | spectral location | absolute growth |
| rank centroid $\rho$ | average local rank percentile under $q$ | $\sum_k (k-0.5)q_k/16$ | 0--1 | primary location summary | internal redistribution with zero centroid change |
| direction correlation | whether one residual points similarly across layers or cases | cross-expression cosine | -1--1 | named-case stability | semantic equivalence |

The requested labels `combinatorics - mathematics` and `linear algebra - mathematics` mean child-minus-sibling-centroid residuals within mathematics. They must not be described as literal subtraction from an independently observed mathematics state.

## 2. Anchor Alignment

- **One uncertainty:** whether the retained depth effect contains fine-specific spectral localization or only common amplification/heterogeneous averaging.
- **Three evidence levels:** aggregate location, difference-defect audit, and named-case correlation structure.
- **One primary metric:** $T_\rho$ only. Absolute curves and named cases interpret or type the verdict; they do not replace it.
- **Smallest claim if Pass:** in this fixed model and bank, conditional-fine residual allocation becomes relatively later-rank with depth after the registered controls.
- **Boundary if Fail:** reject only this fine-specific localization relation; do not reject all depth-dependent semantic organization.
- **Out of scope:** Router construction or evaluation, expert utility, training, shared-middle/shared-tail geometry, composition, and nonlinear semantic use.

## 3. Tested Hypotheses

**H1 — Fine-specific depth localization.** $T_\rho>0$ on $\Delta n$ after matched contrast counts and all reliability guards.

**H2 — Non-artifactual difference.** The H1 result exceeds parent-preserving label permutations and replicates across expression halves, calibration-half bases, and leave-one-parent-out views. Absolute and normalized F1--F16 evidence distinguishes absolute growth, relative reallocation, and opposing internal changes.

**H3 — Named-case structure.** The two registered mathematics child residuals are individually split-reliable in eligible layers. Their direction and spectral-profile correlation maps type the aggregate effect as case-concordant, child-specific, or aggregate-only. H3 cannot promote a failed H1.

## 4. Rival Explanations

1. **Common depth amplification:** coarse and fine absolute strength rise together while normalized location is unchanged.
2. **Normalization artifact:** total fine energy changes, making one band's share rise without its absolute energy rising.
3. **Contrast-cardinality artifact:** 64 fine residuals span more directions than eight coarse residuals.
4. **Self-inclusion artifact:** a child contributes to the parent center that is subtracted from it.
5. **Expression or basis noise:** wording halves or DCLM calibration halves yield different signs.
6. **Aggregate cancellation:** different children move in opposite spectral directions, and their average looks stable or smooth.
7. **Shared-reference correlation:** two child residuals appear correlated because both subtract a common mathematics centroid.
8. **Taxonomy-specific geometry:** the chosen academic fields differ in semantic distance for reasons unrelated to granularity.

## 5. Data Construction And Provenance

### 5.1 Source population and one example

The population is a controlled English academic-description bank, not a sample from natural occurrence frequencies. One record is a label-free description of one child field, rendered through one template and one of two disjoint fact bundles. The model sees the description and common readout suffix; parent and child labels remain analysis metadata.

### 5.2 Proposed fixed taxonomy

The bank has eight parents and eight children per parent:

| Parent | Eight child fields |
| --- | --- |
| mathematics | **linear algebra**; analysis; **combinatorics**; geometry; number theory; probability; statistics; topology |
| physics | condensed matter physics; electromagnetism; mechanics; optics; particle physics; quantum physics; relativity; thermodynamics |
| chemistry | analytical chemistry; electrochemistry; inorganic chemistry; nuclear chemistry; organic chemistry; physical chemistry; polymer chemistry; theoretical chemistry |
| biology | cell biology; developmental biology; ecology; evolutionary biology; genetics; microbiology; molecular biology; physiology |
| computer science | algorithms; artificial intelligence; cybersecurity; databases; graphics; networks; operating systems; programming languages |
| economics | development economics; econometrics; financial economics; international economics; labor economics; macroeconomics; microeconomics; public economics |
| medicine | cardiology; endocrinology; gastroenterology; immunology; nephrology; neurology; oncology; pulmonology |
| linguistics | morphology; phonetics; phonology; pragmatics; psycholinguistics; semantics; sociolinguistics; syntax |

**Decision-critical dataset choice — `AI_PROPOSAL`:** use the earlier audited academic bank as the source but replace its eight `algebra` records with eight matched `linear algebra` records before freezing a new 512-record manifest. The six proposed fact atoms are vector spaces and bases; systems of linear equations and matrices; linear transformations; rank and determinants; eigenvalues and eigenvectors; inner products and orthogonality. They require source and leakage audit before confirmation.

This option satisfies both named cases and preserves 8 parents × 8 children × 4 templates × 2 bundles = 512 records. It does **not** preserve the earlier dataset hash or constitute an independent taxonomy replication. Treating `linear algebra` and `combinatorics` as co-level children is an operational grouping, not proof of matched taxonomy depth or semantic distance. If the researcher instead requires literal reuse of the old 512 records, `linear algebra` is unavailable and the second case must be renamed `algebra - mathematics`; mixing the separate natural-hierarchy corpus is forbidden in the primary comparison.

### 5.3 Splits, balance, and permitted fields

- Four templates × two disjoint three-fact bundles = eight records per child.
- Templates 0--1 are expression half A; templates 2--3 are expression half B; both bundles occur in both halves.
- Every child has identical template and bundle counts; every parent has 64 records.
- A common suffix, left padding, explicit position IDs, and one readout token fix the readout position.
- Forward-pass permitted fields: label-free text, attention mask, and position IDs only.
- Forbidden from the prompt: parent label, child label, template identifier, split identifier, or any answer token.
- Analysis-only fields: parent, child, template, bundle, record ID, and frozen rotation.

### 5.4 Validity and leakage gates

The frozen manifest must pass: exact count and complete parent × child × template × bundle crossing; no parent/child string leakage; a common padded length and readout position; an explicit label-level natural-token-count ledger; exact text/token hashes; duplicate detection; two-pass manual child-is-a-parent audit; and no exact prompt/fact match in the DCLM calibration corpus. Natural description length is not silently treated as equal: it remains a documented text nuisance, while every child receives the same four templates and two bundles and the technical padding/readout geometry is identical.

No label, wording, child, or fact may be replaced after any semantic activation or spectrum is unsealed. A failed gate yields `insufficient_data_guard`.

## 6. Learning Task And Permitted Supervision

There is no learned task, probe, checkpoint selection, or model update. Offline metadata forms means and contrasts only. The analysis may not use label prediction to choose layers, bands, children, templates, nulls, or thresholds. Therefore the learnable-design gate is `NOT_APPLICABLE`.

## 7. Model / Architecture And Frozen Variants

- Model: frozen local Qwen3-8B, 36 decoder blocks, width 4096; exact checkpoint identity must be recorded before implementation approval.
- Primary tensor: $\Delta n_\ell=\operatorname{post\_attention\_RMSNorm}(h_\ell+a_\ell)-\operatorname{post\_attention\_RMSNorm}(h_\ell)$ at the shared readout position.
- Secondary tensor: isolated output $a_\ell$ of `self_attn.o_proj`, before residual addition.
- Required hook inputs: pre-attention residual $h_\ell$, direct `o_proj` output, and actual post-attention RMSNorm output.
- Excluded: residual-state atlas, MLP output, parameter eigenspectrum, SAE features, Router input, expert state, and any learned readout.
- Each layer/site has a separate DCLM covariance basis. A full basis is primary; two 32,768-token calibration halves provide replication.
- F1--F16 are 16 equal-rank, 256-direction projectors sorted by descending DCLM variance.

## 8. Training Objective And Optimization

No objective is optimized. All data, layers, windows, contrasts, nulls, plot definitions, and verdict rules must be frozen before semantic projection results are opened. No development data may select an operating point.

## 9. Conditions, Seeds, And Checkpoints

| Item | Anchor clause / rival | Why needed | Evidence role | Required artifact |
| --- | --- | --- | --- | --- |
| $\Delta n$ coarse/fine atlas | H1 | decisive representation | primary | `tables/primary_layer_metrics.csv` |
| isolated $a$ replay | source-boundary control | tells whether RMSNorm/residual interaction changes the description | secondary | `tables/source_boundary.csv` |
| eight matched rotations | contrast-cardinality rival | eight fine and eight coarse contrasts per estimate | hard guard | `provenance/rotations.json` |
| expression halves A/B | wording noise | independent semantic replication | hard guard | `tables/expression_half_metrics.csv` |
| calibration halves A/B | basis instability | independent local spectral bases | hard guard | `tables/calibration_half_metrics.csv` |
| leave-one-parent-out | single-parent dominance | tests aggregate dependence | hard guard | `tables/leave_one_parent_out.csv` |
| parent-preserving child permutation | semantic grouping artifact | destroys child identity while retaining parent and counts | primary null | `tables/permutation_null.csv` |
| Haar 16-band partitions | rank-coordinate specificity | same band dimensions without DCLM ordering | secondary null | `tables/haar_null.csv` |
| named mathematics cases | aggregate cancellation and shared-reference rivals | makes case structure inspectable | typed diagnostic | `tables/named_case_metrics.csv` |

There is one frozen model checkpoint and no model seed. Use seed `20260809`, 2,000 root-family bootstrap replicates, 2,000 parent-preserving permutations, and 1,000 Haar partitions.

## 10. Primary Metric And Frozen Analysis Plan

### 10.1 Contrast construction

For each expression half, construct coarse leave-one-parent-out residuals and fine leave-one-child-out sibling residuals exactly as defined in the Anchor. Eight frozen rotations each choose one child per parent and cover every child once. Compute each rotation separately, then average rotations with equal parent weight.

### 10.2 Absolute and normalized quantities

Compute unsmoothed $A^\times_{\ell gk}$ in activation-squared/direction and normalized $q_{\ell gk}$ in fraction of total within-half squared energy. Report both before any centroid. A band with nonpositive cross-expression energy is retained and visibly marked; it is never clipped for statistics.

### 10.3 Primary estimand

$$
T_{\rho}
=\operatorname{median}_{25:35}(\rho_{\ell F}-\rho_{\ell C})
-\operatorname{median}_{1:12}(\rho_{\ell F}-\rho_{\ell C}).
$$

Block 36 is a registered terminal diagnostic and never enters either window. The unit is normalized local-rank percentile. Multiplying by 4096 may be used only as an equivalent-local-rank description.

### 10.4 Independence, uncertainty, and nulls

- Unit of observation: one parent or child residual in one expression half and layer.
- Unit of semantic independence: root parent family; prompts and layers are repeated measurements.
- Aggregation: equal parent weight, equal rotation weight, early/late layer medians.
- Interval: one-sided 95% root-family cluster bootstrap. Each draw samples eight parent families with replacement and retains every child, expression, and layer trajectory inside a selected family. The 5th and 95th percentiles are reported as one-sided lower and upper bounds; the lower bound controls Pass and the upper bound controls precise nonpositive Fail.
- Primary null: independently permute the eight child assignments inside every parent × template × bundle cell, thereby retaining parent, cell counts, and expression balance while destroying cross-expression child identity; replay the entire statistic 2,000 times.
- Multiplicity: none for $T_\rho$; 16 bandwise secondary contrasts use max-absolute-statistic permutation correction.
- Missing/failed cells: no imputation. A required missing parent, half, layer, or basis makes the primary verdict Insufficient.
- Outliers: no result-based exclusion. Predeclared data-invalid records are removed only before unsealing and require a re-frozen manifest.
- Expression-half guards recompute $q$, $\rho$, and $T_\rho$ from one half's squared energy at a time. Calibration-half guards keep the semantic contrasts fixed and change only the DCLM basis. Leave-one-parent-out views remove one family and recompute the coarse leave-one-out reference among the remaining families.
- Haar partitions are exact for the registered quadratic summaries: for each layer, a Gaussian-polar Haar Stiefel draw is formed on the joint span of all coarse/fine expression contrasts, then divided into sixteen 256-direction blocks. This is algebraically equivalent to drawing a full 4,096-dimensional Haar basis for those summaries and avoids storing irrelevant orthogonal-complement coordinates.
- Unsealing point: after manifest hash, basis identities, rotations, seed, analysis revision, and this decision rule are frozen.

### 10.5 Verdict mapping

1. Reliability gate: root-bootstrap lower bounds for total coarse and fine $A^\times$ exceed zero in both early and late windows.
2. Pass: reliability passes; the lower bound of $T_\rho$ exceeds zero; the estimate exceeds permutation q95; expression-half and calibration-half point estimates are positive; all leave-one-parent-out estimates are nonnegative.
3. `nonspecific_location_fail`: the $T_\rho$ interval is wholly positive but the estimate does not exceed permutation q95.
4. `nonpositive_location_fail`: the upper bound of $T_\rho$ is at or below zero with all validity gates passed.
5. Insufficient: the interval crosses zero or any mandatory gate fails.

False-positive cost is higher than false-negative cost: a spurious smooth curve would be promoted as a semantic localization law. Therefore secondary plots cannot rescue a failed or insufficient primary result.

## 11. Secondary Metrics And Guards

1. **Absolute-location moment:** $\alpha_{\ell g}=\sum_k m_kA^\times_{\ell gk}$ and its fine-minus-coarse early/late change. Positive support types an H1 Pass as `absolute_and_relative`; otherwise it is `relative_reallocation_only`.
2. **Full F1--F16 difference:** $q_{\ell Fk}-q_{\ell Ck}$ and $A^\times_{\ell Fk}-A^\times_{\ell Ck}$ with max-statistic correction.
3. **Per-direction curves:** all 4,096 unsmoothed values for statistics; a centered 129-rank mean on linear energy may be shown only as a labeled display overlay.
4. **Cancellation audit:** if the centroid is null but corrected band differences contain stable opposing signs, type `redistribution_without_centroid_shift`; this is not H1 Pass.
5. **Basis guard:** full-basis results must keep sign in each calibration-half basis; band-projector overlaps relative to Haar are reported, not used to post hoc merge bands.
6. **Self-inclusion audit:** compare leave-one-child-out residuals with the prohibited self-inclusive parent subtraction to show the bias; only leave-one-out enters evidence.
7. **Named-case reliability:** same-layer $\cos(r^A_{\ell c},r^B_{\ell c})$ must be positive before cross-layer cells for child $c$ are unmasked.
8. **Named-case correlation:** report cross-layer direction matrices, cross-layer 16-band-profile correlations, and same-layer `combinatorics`--`linear algebra` correlation against all 28 mathematics child-pair controls. No single-pair p-value changes the verdict.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** both requested mathematics children have eight label-free, balanced descriptions and positive split-half residual reliability in at least one prespecified layer group.
- **Known bad:** direct subtraction of two layers' covariance matrices; a parent center that includes the target child; treating old `algebra` records as `linear algebra`; mixing the natural-hierarchy corpus into the primary bank; a hook that includes residual addition in $a_\ell$.
- **Known confusing:** normalized right shift while absolute energy falls; a zero centroid created by left/right cancellation; high child-pair cosine caused by the shared mathematics reference; `linear algebra` and `combinatorics` treated as distance-matched merely because both are grouped under mathematics; a stable 16-band profile with an unstable raw direction; an aggregate effect carried by one parent.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How / why | Expected output | Pass / fail / insufficient | Artifact | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 data decision | freeze one 512-record object | researcher chooses old-bank reuse or proposed linear-algebra replacement | prevents cross-corpus or post-result repair | complete candidate manifest | exact option confirmed / otherwise blocked | `provenance/semantic_manifest.json` | data preflight |
| 1 data preflight | establish balance and no leakage | complete manifest, tokenizer, label metadata | run all Section 5.4 checks before activation access | audit ledger and hashes | all pass / stop as data-insufficient | `provenance/data_audit.json` | extraction check |
| 2 deterministic extraction check | validate $h$, $a$, actual normalized input, and $\Delta n$ | 16 records; blocks 1/18/35/36 | direct replay and no-op identities protect tensor meaning | hook/replay report | tolerances pass / stop | `provenance/hook_audit.json` | full extraction only after separate approval |
| 3 full extraction | materialize registered tensors | frozen manifest and model identity | extract all records/layers without viewing semantic curves | tensor shards and manifest | complete / incomplete | `provenance/extraction_manifest.json` | covariance calibration |
| 4 basis calibration | freeze local spectra | independent 65,536 DCLM tokens | full and two half covariance eigensystems; 16 fixed bands | basis manifests and stability | reconstruction passes / stop | `provenance/basis_manifest.json` | sealed analysis |
| 5 sealed analysis | adjudicate H1/H2 and type H3 | frozen tensors, bases, contrasts, nulls | replay Section 10 exactly | decision tables and plot data | registered verdict / insufficient | `tables/` | figure audit |
| 6 figure audit | make inference inspectable | frozen decision tables | render only registered panels and inspect labels/masks/scales | four central figures plus audit | all contracts pass / revise rendering only | `figures/`, `provenance/visual_audit.json` | result records |

The 16-record extraction check proves only hook identity, replay, and artifact schema. It is not a scientific smoke result and cannot authorize full execution.

Numerical tolerances: direct captured $a_\ell$ versus `o_proj(pre)` relative error $<10^{-6}$; reconstructed actual normalized input relative error $<10^{-6}$; stored $\Delta n$ versus replay relative error $<10^{-6}$; covariance projection-energy reconstruction relative error $<10^{-5}$.

## 14. Algorithm, Output, And Provenance Contract

### 14.1 Ordered algorithm

1. Freeze the chosen 512-record manifest, model identity, readout position, layer list, and DCLM indices.
2. Capture $h_\ell$, $a_\ell$, and actual post-attention normalized input; replay $\Delta n_\ell$.
3. Fit no model. Form expression-half parent/child means and leave-one-out residuals.
4. Apply eight frozen matched rotations and save every unaggregated contrast.
5. Project contrasts into full and calibration-half F1--F16 bases; compute $A^\times$, $q$, $\rho$, $T_\rho$, nulls, and guards.
6. Compute named-case reliability and correlations only after reliability masks are fixed.
7. Save tables before rendering; smoothing may read tables but never feed statistics.
8. Produce the registered verdict and typed secondary interpretation without changing thresholds.

Any imbalance, missing layer, failed replay, invalid basis, nonfinite value, or incomplete null stops adjudication and records an explicit reason.

### 14.2 Central figure contracts

**Figure 1 — Coarse/fine strength and location across depth.** Two aligned panels show total $A^\times$ and $\rho$ for coarse/fine plus the fine-minus-coarse trajectory. X is block; units are activation squared/direction and normalized rank percentile. It may establish strength/location trajectories, not direction identity.

**Figure 2 — Full spectral difference atlas.** Layer × F1--F16 heatmaps show absolute and normalized fine-minus-coarse values on separate color scales, with selected-layer 4,096-direction overlays. It may expose which ranks drive or cancel the centroid; it cannot select a new post hoc primary band.

**Figure 3 — Named mathematics residuals.** Separate `combinatorics - mathematics` and `linear algebra - mathematics` panels show absolute/normalized layer-band heatmaps and cross-layer split-expression direction matrices. Invalid cells are masked. It may show case stability or heterogeneity, not population generality.

**Figure 4 — Case-to-case correlation and defect audit.** The requested pair's same-layer direction and 16-band-profile correlation curves are shown against the envelope of all mathematics child pairs; a companion compact table shows self-inclusion, unmatched count, expression split, calibration split, and leave-parent effects. It may identify measurement defects, not pure semantic composition.

Every figure records data table, computation revision, aggregation, axes, units, legend, allowed conclusion, limitation, and a rendered-artifact audit.

### 14.3 Provenance and execution boundary

Registered execution boundary:

- worker code root: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_02_05_e01_balanced_taxonomy_attention_write_atlas/`;
- raw artifact root: `/data/250010109/MoE_Router/experiments/20260809_a15_02_05_balanced_taxonomy_attention_write_atlas/runs/<UTC_RUN_ID>/`;
- curated result root: this Protocol's directory; only decision tables, evidence manifests, and audited figures may be copied here;
- model: `/data/share/Qwen3-8B`; `config.json` SHA-256 `deaa300e5384a480c2cafd0db33cba0da89db8eeeb8ddc2b584b89bd46d52ffb`;
- tokenizer SHA-256: `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4`;
- DCLM calibration tensor: the previously audited 128 × 512 token tensor, SHA-256 `2d1aee93af592df45bdfbed668e755052c1fbe8544b05fc31211ae4eb31a62a1`; its two ordered 64-document halves contain 32,768 tokens each;
- environment: local Linux host; Python 3.10.12; PyTorch `2.3.0a0+6ddf5cf85e.nv24.04`; CUDA 12.4; Transformers 4.51.3; NumPy 1.24.4; SciPy 1.12.0; pandas 1.5.3; Matplotlib 3.8.4;
- resource ceiling: two local NVIDIA H100 80GB GPUs, 64 CPU threads, 80 GiB additional disk, 12 wall-clock hours, and no remote or cluster submission;
- code policy: the enclosing project is dirty with unrelated researcher work, so the implementation is isolated by a new experiment directory and its complete source hashes are frozen in the run manifest before smoke; no existing worker implementation is edited;
- command contract: run `prepare_data.py`, the unit suite, `extract.py --mode smoke`, then `extract.py --mode full`, `build_bases.py`, `analyze.py`, `render.py`, and `audit_run.py` through `scripts/run_local.sh`; the script must record every resolved command and environment value before execution;
- stop conditions: any failed data gate, unit test, hook/replay tolerance, missing semantic cell/layer/site, nonfinite tensor, covariance reconstruction failure, incomplete 2,000/2,000/1,000 resampling count, artifact-schema failure, or 80 GiB / 12-hour ceiling breach stops the chain and yields an explicit failure receipt;
- expected receipts: data, hook, extraction, basis, analysis, null-count, visual, environment, command, and artifact manifests, plus stdout/stderr logs and a typed verdict.

## 15. Success / Failure / Insufficient Evidence

- `fine_specific_location_pass__absolute_and_relative__case_concordant`
- `fine_specific_location_pass__relative_reallocation_only__aggregate_heterogeneous`
- `redistribution_without_centroid_shift` — secondary structure; H1 not passed
- `common_amplification_location_fail` — reliable strength, no fine-specific location
- `nonspecific_location_fail` — positive estimate no stronger than registered taxonomy null
- `nonpositive_location_fail` — precise nonpositive depth interaction
- `insufficient_data_guard`
- `insufficient_semantic_reliability`
- `insufficient_basis_or_numerical_guard`
- `insufficient_precision`

The first two strings illustrate composable typing: the primary verdict, absolute-versus-relative interpretation, and case structure are stored separately. H3 never changes the primary Pass/Fail/Insufficient field.

## 16. What This Cannot Claim

The experiment cannot claim that a parent-only mathematics vector was observed; that child residuals are pure or independent; that semantic difficulty equals taxonomy depth; that a band contains a universal concept type; that eigenvectors are transported across layers; that attention creates or the MLP causally uses the signal; that named mathematics cases generalize to all children; or that any Router, expert assignment, loss, or training process benefits.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Decision requiring review |
| --- | --- | --- |
| A question / claim boundary | CONFIRMED | representation localization only; three evidence levels; no Router/function claim |
| B data / provenance | CONFIRMED | freeze a new 512-record bank with `linear algebra` replacing `algebra`; do not mix the natural-hierarchy corpus |
| C task / supervision | CONFIRMED | no learning; offline leave-one-out contrasts only |
| D model / architecture | CONFIRMED | frozen Qwen3-8B; $\Delta n$ primary; isolated $a$ secondary; local DCLM bases |
| E objective / optimization | CONFIRMED | no objective or checkpoint selection; all analysis sealed before semantic unsealing |
| F comparison / evidence | CONFIRMED | $T_\rho$ sole primary; absolute/normalized defect audit; matched rotations; permutation/Haar controls; named-case correlations diagnostic only |
| G execution / reproducibility | CONFIRMED | local two-H100 implementation, preflight, extraction check, and one full run under the registered ceilings and stop rules |

**Cross-block audit:** `PASS`. The new bank exposes the requested cases without cross-corpus mixing; the offline contrast task matches the fixed representation sites; no objective or selection step can access confirmation truth; matched rotations and the registered null separate the strongest rivals; $T_\rho$ has one unambiguous verdict mapping; and the local resource/artifact contract can execute every condition.

**Researcher approval receipt:** on 2026-08-09 the researcher wrote, “现在批准通过，按照你的理解进行执行,” explicitly authorizing the frozen design, implementation, preflight, extraction check, and complete run. This does not authorize publication, root sync, collaborator sync, commit, or push.

**Freeze receipt:** registered revision `A15_02_05_E01_r1`; `design_frozen_at=2026-08-09T16:45:32Z`; approved Anchor SHA-256 `1a522fa73e83f3461a153b5dd00a39792b7871e60f69b1f915c7a1dbbd5412f8`; scientific-body SHA-256 `9fb217b7336e3838c59852aa565a06c8774160e6bf21495a9bcb0abbd6aa82fb`.

Execution has not started at this receipt. Once the first approved activation-bearing command begins, Sections 1--16 are frozen. Any later change to data, supervision, representation, condition logic, metric, threshold, exclusion, or stopping rule requires an append-only amendment stating whether prior evidence remains eligible; execution-status receipts and result links may be appended without rewriting the scientific body.

**Execution receipt:** the first activation-bearing command began in local run `a15-02-05-e01-20260809T165500Z`. The registered smoke, 512-record full extraction, 36-layer full/half basis construction, 2,000 root-family bootstraps, 2,000 parent-preserving permutations, 1,000 Haar partitions, and final visual audit all completed under the resource ceiling. The final artifact audit is `PASS`; the eligible registered verdict is `nonpositive_location_fail`. See [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md) and [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/detailed.md).

**Recorded execution deviations:**

1. The pre-run-hashed runner recorded the environment and ordered stage outputs but omitted the separately promised resolved-command manifest before execution. The exact commands remain fixed by the runner hash and are reconstructable from the runner plus `logs/run.log`; [command_reconstruction.json](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/evidence/command_reconstruction.json) records this post hoc. No scientific input, condition, metric, or result is ambiguous, so this is a documentation deviation with no eligibility change.
2. Original-resolution inspection found zero-based array-position labels in Figure 3 and clipping/missing guard rows in Figure 4. Only rendering code was revised; regression tests passed, and the hashes of `verdict.json`, `primary_layer_metrics.csv`, `full_band_metrics.csv`, and `mathematics_pair_controls.csv` remained unchanged. The before/after source and figure hashes are in [render_revision.json](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/evidence/render_revision.json), and [visual_audit.json](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/evidence/visual_audit.json) is `PASS`. This visualization-only revision does not change evidence eligibility.
