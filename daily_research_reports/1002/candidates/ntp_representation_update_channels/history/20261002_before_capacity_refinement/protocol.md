# Candidate Protocol: Can pre-update representations predict finite natural-text update responses?

[中文](protocol_cn.md) · [Anchor](anchor.md) · [Derivations](mathematical_analysis.md). This is a prospective candidate contract. It is not a retrospective registration of today's exploratory work, whose process and outcomes belong to the [process record](research_process.md) and [report](research_report.md).

## 0. Approval Snapshot

| Field | Current value |
| --- | --- |
| Document status | `DRAFT_NOT_EXECUTABLE` |
| Approval / blocks | New confirmation design unconfirmed; A/C/D/E/F PROPOSED; B/G BLOCKED |
| Cross-block consistency | Objects and computation align; independent sampling units and new manifest remain unresolved |
| Approved scope | The user authorized two hours of research and candidate documents, including bounded local analysis. This document does not authorize new confirmation, remote work, or training |
| Design frozen at | Not frozen; 2026-10-02 candidate; record body/configuration hashes at future approval |
| Purpose | Test whether pre-update representations add finite-response prediction information beyond the lexical and scale baseline, conditional on fixed source updates |
| Primary Anchor | This directory's Anchor §§3–6, AI_PROPOSAL, not approved scientific design |
| Existing active Focus | [Domain update geometry](../../../../Projects/from-attention-to-search/main/focus/focus_domain_update_geometry_cn.md), background only; its question and state are not changed |
| Prior / term / falsifier | Natural continuations and current model errors jointly determine response; actual finite loss change is the target; no distinguishable readout gain does not support this operationalization |
| Role | Operationalization or proxy test |
| Minimal setup | One S7 checkpoint, four fixed source gradients, new fit/confirmation records, two step lengths, no LM/SAE training |
| Treatment / changed variable | Add 320 frozen SAE coefficients to a common baseline |
| Controls / held fixed | Native PCA/random projections and target-identity diagnostic; identical records, updates, loss, fitting and evaluation |
| Primary metric | Equal-source mean relative squared-error improvement, \(Q_{\rm macro}\), dimensionless |
| Pass / fail / insufficient | Interval lower bound > 0 / upper bound ≤ 0 / overlap with zero or failed validity guards; useful effect threshold Unknown |
| Cannot claim | SAE-exclusive information, pure semantics, full response knowable before the target, long-term interference or separation utility |
| Approval decision | Awaiting researcher review; no automatic promotion or run approval |

Continuation note,2026-10-02: [within-domain A/B batch transfer](source_transfer_addendum.md) and [between-domain response structure](domain_response_structure.md) are completed old-panel explorations. The former mean/contrast is within-domain; the latter adds domain differences, earlier-prefix forecasting and input channels. Neither changes this Protocol primary test, threshold, approval or resources. Promoting prefix-based relative benefit to the primary comparison remains an AI suggestion for researcher selection.

## 1. Terminology / Definitions

A **source update** is one matrix direction formed from natural-text true-next-token gradients. A **readout event** is a different prefix and its true next token. The **representation** is the native final attention output \(a\), not its SAE reconstruction. The **response** \(I\) is the native model's finite true-target loss change, in nats: positive is adverse and negative is helpful. A **readout** is a ridge predictor using pre-update features; it does not train the language model.

**Confirmation** requires new results not used for the present design. Previously exposed R cannot become untouched again. **Fixed-source conditional inference** holds the four source matrices constant and concerns new target records; it does not average over resampled sources. The **independent unit** is the actual sampling group used for inference and need not equal a dataset row.

## 2. Anchor Alignment

The experiment addresses one candidate statement: whether specified pre-update features add readable information about finite responses to fixed source updates. Its chain is prefix/target → average source gradient → native displacement → actual loss difference → prediction error on new records. The Anchor and mathematical analysis own the full model.

AI_PROPOSAL: SAE320 is the single primary augmented representation. Native controls must be reported even if stronger. Do not select the best representation after confirmation. Failure of SAE320 does not establish absence of information in the complete native representation.

## 3. Tested Hypothesis

Conditional on the checkpoint, four source matrices and specified population, adding pre-update SAE320 reduces the prescribed predictor's squared error on new records. The primary candidate statement is \(Q_{\rm macro}>0\). This is a predictive relation, not a claim that any nonzero gain justifies a Router.

Target identity is an independent explanatory diagnostic and is excluded from the primary inputs. A diagnostic requiring the realized target cannot establish before-target routing performance.

## 4. Rival Explanations

| Rival | Separating comparison | Remaining limitation |
| --- | --- | --- |
| Gains repeat local lexical composition | Common baseline includes current/previous token, preceding16-token bag, position and representation scales | It does not represent every nonlinear function of the full prefix |
| SAE is necessary or uniquely strong | Dimension-matched native PCA and random projections, identical fitting | One random basis does not characterize all bases; comparisons are secondary |
| The actual target explains the response | Separate true-target diagnostic | Target one-hot is not the complete continuation distribution |
| Leakage or selection produces gain | Independent-group splits, F-only choices, whole-record label permutation | The source/population relation is still conditional |
| The derivative proxy is inaccurate | Actual finite \(I\) is the primary label; half-step and derivative are diagnostics | Only one local scale is studied |

## 5. Data Construction And Provenance

VERIFIED_SOURCE: N8_v1 scientific text at revision `6ae613ba744ee56f645aee9c577d04f7e3d48b30`, four domains and two subcategories per domain. All old 2048 records and results are exposed. The source root is `/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/`; old manifests are `data/selected.jsonl` and `data/data_manifest.json`.

Verified subcategories are CS: `cs.CL`/`cs.CV`; math: `math.AG`/`math.NT`; physics: `physics.flu-dyn`/`physics.optics`; biology: `q-bio.GN`/`q-bio.NC`. The proposed population is this scientific-text source, not all natural language.

AI_PROPOSAL: retain the four frozen old F-half0 source matrices, each from 128 records ×16 targets. Draw new fitting data with 128 records/domain and new confirmation data with 256 records/domain, balanced across the two subcategories. This is a budget proposal, not a power guarantee. Use the first256 tokens and predict the following token at zero-based positions14, 30,…, 254. Do not concatenate short records. Freeze exclusion/truncation rules before sampling.

Exclude every exposed record, identical text hash and registered near duplicate across sets. Save revision, record ID, group ID, text hash, token-ID hash, positions and targets. Use original targets; no synthetic labels and no selection by effect or semantic typicality.

BLOCKED: available rows lack verified paper identities. A new manifest supporting independent-group sampling has not been chosen, and the acceptable record-level generalization scope is unconfirmed. The researcher must settle population and unit before sampling. Distinct rows from one paper are not independent papers. Training exposure is unverified; do not claim training-unseen generalization.

## 6. Learning Task And Permitted Supervision

Predict four source-specific responses per event. Primary inputs exclude actual next token, loss, gradients, source/target domain labels and updated representations. The common baseline contains F-selected top128 current-token and previous-token one-hot vectors; an F-selected top512 bag of the preceding16 tokens; 16 position indicators; and \(\log(1+\|c\|)\), \(\log(1+\|a\|)\). Out-of-vocabulary categories are zero; vocabulary selection uses new F only.

The SAE arm adds320 frozen coefficients transformed by \(\log(1+\alpha_k)\). Select atoms on new F by distinct-record coverage, tie by ID, requiring at least16 fitting records per atom. Fewer than 320 eligible atoms stops the primary condition; do not fill from confirmation. Actual native finite losses supply labels only for fitting/scoring. The separately marked after-target diagnostic adds one-hot indicators for F's top128 true target tokens.

## 7. Model / Architecture And Frozen Variants

Freeze the S7 checkpoint at 33B training tokens: `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`. Its `state.pt` SHA256 is `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`. 33B is a training-token count, not parameter count.

The matrix is `blocks[7].attn.o.weight`, 1024×2048. Its input \(c\) is 2048-dimensional; native \(a=Wc\) is 1024-dimensional; \(r\) is the pre-addition residual. Preserve native downstream normalization, MLP, final normalization and 151936-vocabulary output. Freeze the SAE's30000 normalized decoder columns, encoder, bias and TopK32. The SAE is not in the measured NTP loss.

Fit PCA320 only to new-F native outputs. For random320, QR-orthogonalize a1024×320 Gaussian matrix with seed31 and save the actual basis. Use identical records in all primary-input conditions.

## 8. Training Objective And Optimization

No LM or SAE training occurs. Fit a four-output ridge predictor after standardizing each feature and response using training-fold statistics; set constant feature scales to 1. Minimize mean squared error plus \(\lambda\|\beta\|_F^2\), with an unpenalized intercept. Use four group-level folds; validation statistics must not enter training-fold normalization.

AI_PROPOSAL grid: \(10^{-4}, 10^{-3}, 10^{-2}, 10^{-1}, 1, 10, 100\). Choose the minimum mean validation error across standardized outputs; break ties toward larger \(\lambda\). Refit once on all F and freeze. If100 is selected, expand before confirmation unsealing and record the revision. Never expand after looking at confirmation. There is no gradient optimizer, LM schedule or checkpoint selection. Any future LM training requires a new contract following the training observability rules.

## 9. Conditions, Seeds, And Checkpoints

| Condition | Role | Fixed definition / rival |
| --- | --- | --- |
| B: strong baseline | Primary denominator | §6; local composition |
| B+SAE320 | Only primary treatment | Frozen atom rule; additional readable response relation |
| B+PCA320 / B+random320 | Secondary tool controls | Same dimension/fitting; SAE uniqueness |
| B+target / B+target+SAE | After-target diagnostics | Actual target allowed only here |
| B+SAE with shuffled labels | Negative control | Shuffle complete F record response blocks within category, seed1002 |
| Full/half step | Primary scale/locality diagnostic | Identical source directions |

Use one checkpoint. Fix the main step at \(\eta=0.05731845587090156\), from an old-F pooled-source relative RMS output displacement of 0.001; the second step is half of it. This is not a proposed optimizer learning rate. Do not select scales by confirmation effects. Use seed1002 for data hash ordering and 2000 bootstrap draws. These are candidate values, not an approved final configuration.

## 10. Primary Metric And Frozen Analysis Plan

For source \(A\), let \(I_{Aj}\) be actual finite response and \(\widehat I^B,\widehat I^F\) the common and augmented predictions. Define

\[
Q_A=1-\frac{\sum_j(I_{Aj}-\widehat I^F_{Aj})^2}{\sum_j(I_{Aj}-\widehat I^B_{Aj})^2},\qquad
Q_{\rm macro}=\frac14\sum_AQ_A.
\]

Equal record counts/domain and 16 targets/record make event weighting also equal-record weighting. Report100Q as a percentage. Equal-source aggregation prevents a high-error source from dominating; the pooled-SSE ratio is secondary. This is not an LM perplexity improvement.

Use paired, subcategory-stratified bootstrap over the confirmed independent groups, retaining all within-group events and paired predictions. Report a two-sided95% percentile interval. Source matrices and fitted predictors remain fixed: uncertainty excludes source resampling, refitting and design selection. There is one primary comparison. Source-specific, tool, half-step and target diagnostics are descriptive and cannot rescue a failed primary claim.

Do not drop failed, nonfinite, missing, duplicated or mismatched events based on results. Stop, repair and record exposure. A scientific revision after exposure makes the affected panel exploratory and requires newly frozen confirmation. Zero baseline SSE makes Q undefined and the outcome insufficient. No confirmation-driven outlier clipping. Unsealing begins with the first confirmation loss, prediction error or aggregate output.

## 11. Secondary Metrics And Guards

Report source/readout-domain mean \(I\), helpful/adverse/unresolved fractions, with proposed \(\pm10^{-5}\)-nat deadband and sensitivities at \(2\times10^{-6}\), \(5\times10^{-5}\). These do not replace primary Q.

Qualify exact no-op, \(G=ec^\top\) relative error≤\(10^{-5}\), temporary full-matrix forward versus tail CE error≤\(2\times10^{-5}\) nat, and stable CPU gradient versus native reference relative error≤0.002. Report \(\sum|I-\eta h|/\sum|I|\) at both steps rather than assuming linearity. Restore temporary weights in a finally block and require identical before/after state hashes. Numerical limits establish measurement qualification, not scientific success.

Any SAE direction analysis must retain native displacement, all 30000 sparse endpoint coordinates, reconstruction residual and support-change flags. For a fixed orthogonal subspace, report full, only-component and removed-component arms and the complement. Select subspaces on F only and register them before confirmation; otherwise their interventions remain exploratory.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: a linear-logit finite CE matches direct matrix replay, and local derivative error shrinks at smaller step. Known bad: outer product of means substituted for mean outer products; target leakage into primary inputs; sums of nonorthogonal atom scores called independent energy. Known confusing: helpful domain mean with adverse individual events; adverse component offset by total help; accurate static reconstruction with inaccurate sparse-code displacement; calibrated predictions with zero first-order mean but nonzero variance.

These qualify measurement and interpretation. They are not natural-text evidence votes.

## 13. Scientific Procedure And Stage Contracts

| Stage | Input / operation | Purpose / output | Pass, failure, insufficiency and handoff |
| --- | --- | --- | --- |
| S0 Data | Confirmed population/group rule and full exclusion list; model-free sampling audit | Establish independence and coverage; manifest and collision table | Unknown groups: DATA_INDEPENDENCE_BLOCKED; no confirmation |
| S1 Measurement | Exact checkpoint/interfaces and small F subset; §11 checks | Verify intended W-only response; qualification.json | Any numerical failure: MEASUREMENT_FAILED; repair only |
| S2 Fit/freeze | Fixed source matrices and new-F native states/actual I; F-only choices | Freeze how predictions are made; features, CV, model and hashes | Complete artifacts required; confirmation remains hidden; resolve grid boundary first |
| S3 Confirmation | Frozen body/code/models/manifest; actual I and §10 score | One primary Q, interval, guards and failures | Data/numerical failure means insufficient; otherwise §15; no rule changes |
| S4 Record/decision | All conditions and limitations | Four-part Summary and Detailed; surface the next decision | AI records facts; researcher owns scientific state and next design |

## 14. Algorithm, Output, And Provenance Contract

Ordered algorithm: validate input hashes → construct/verify sources → extract native \(c,a,r,e\) and SAE coefficients → compute native tail losses at \(a-\eta M_Ac\) → F-only fitting → freeze → confirmation → paired group intervals → completeness audit. Never impute a failed computation as zero.

Reuse the old `core.py` model loader/tail and current `finite_replay.py` finite evaluation; adapt data grouping and strong baseline. Reject old synthetic targets, SAE replacement forwards, and gradients of the SAE training objective as NTP source gradients. Current code lives at `/data/250010109/MoE_Router/experiments/20261002_s7_representation_update_channels/scripts/`. New work must use `runs/confirmation_<registered_revision>/`, preserving today's outputs.

Required artifacts: body/config/code hashes, environment, checkpoint lineage, data/group manifests, exclusions, source matrices, qualification, feature freeze, CV, predictions, per-event losses, primary results and complete failures. Raw arrays/caches stay in the execution repository; Research_System holds text, selected small tables/figures and a payload manifest.

AI_PROPOSAL qualification ceiling: local CPU8 threads, peak memory≤64GiB,≤15 minutes per qualification run. The total confirmation budget/environment is unresolved, so G remains BLOCKED. This document cannot submit GPU or remote work.

## 15. Success / Failure / Insufficient Evidence

After all data, numerical and freeze guards pass: lower primary-Q bound>0 gives SUPPORTS_THIS_READOUT; upper bound≤0 gives DOES_NOT_SUPPORT_THIS_READOUT; crossing zero gives INSUFFICIENT_PRECISION. Failed essential guards give INSUFFICIENT_VALIDITY. These labels concern the specified conditional relationship/tool and do not close the overall question.

The effect size required to justify system design and the costs of wrong decisions are researcher-owned and currently Unknown. Any nonzero utility threshold must be registered before unsealing with corresponding decision branches, never added after results.

## 16. What This Cannot Claim

Lexical residual is not pure semantics. Prediction residual is not irreducible natural randomness. Static SAE fidelity is not dynamic fidelity. Sensitivity/local harm is not long-term interference. Fixed sources do not represent all future sources. Different rows do not prove paper independence or training non-exposure. No result here decides parameter separation or Router utility.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Content / unresolved item |
| --- | --- | --- |
| A Question/boundary | PROPOSED | One conditional readout question; no long-term separation claim |
| B Data/provenance | BLOCKED | Old sources verified; new independent-group rule/manifest unconfirmed |
| C Task/supervision | PROPOSED | Before-target inputs, actual finite labels, separate target diagnostic |
| D Architecture | PROPOSED | Frozen exact S7/SAE; SAE320 primary, native controls |
| E Objective/fitting | PROPOSED | No LM training; group-CV ridge and freeze |
| F Comparison/decision | PROPOSED | Macro Q, conditional interval, three branches; utility threshold Unknown |
| G Execution | BLOCKED | New confirmation environment/budget/authorization unresolved |

2026-10-02: researcher-confirmed scope is two-hour research, natural-text representation analysis, S7/SAE as tools and candidate storage. Other decisions are reviewable proposals. AI object-consistency review does not confirm A–G. Unresolved independence, resources and design confirmation keep the document `DRAFT_NOT_EXECUTABLE`.

Promotion requires explicit A–G confirmation, consistency PASS, freeze time and hashes; execution remains restricted to the approved scope. After execution begins, preserve the body. Append material amendments with time, before/after values, reason, exposure, affected blocks, approval and evidence eligibility. Later approval does not convert today's exploration into preregistered confirmation.
