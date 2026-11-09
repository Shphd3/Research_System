---
experiment_id: A15_13_E02_repaired_rule_induction_teacher_entrance_and_full_semantic_supervision
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_EXECUTION
approval_date: 2026-08-30
design_frozen_at: 2026-08-30T22:16:48Z
scientific_body_sha256: 55bb327cdcd749270a6f5e88ab341dfe21e718c22afc669521a1043da900907e
---

# Protocol: Repaired Rule-Induction Teacher Entrance And Gated Full Semantic Supervision

## 0. Approval Snapshot

**Document status:** frozen execution contract.  
**Approval status:** the researcher explicitly approved choices 1--13 and authorized construction, smoke, troubleshooting within the frozen candidates, and full execution without another approval gate.  
**Block audit status:** A--G confirmed.  
**Cross-block consistency:** PASS.  
**Execution scope approved:** implementation, tests, data construction, local and ACP smoke, all 24 teacher lineages, teacher audit, and—only after the non-truth teacher entrance passes—the complete registered second-stage grid.  
**Purpose:** establish whether the three-layer teacher actually learns transferable rule semantics before using it to test final-to-middle supervision.  
**Primary Anchor:** A15_13 final-layer semantic supervision and hierarchical middle-layer formation.  
**Anchor decision question:** can labels formed from the third-layer pre-answer state causally improve second-layer hierarchical semantic separation over matched controls?  
**Anchor prior tested:** learn and freeze the parent-common path before learning parent-conditional fine differences; optionally remove the learned coarse discriminant only from the fine Gate input.  
**Experiment role:** root-cause audit followed by a gated robustness repetition of the approved method construction.  
**Primary teacher metric:** DEV-OOD query-answer accuracy, with third-layer true-parent linear readability as a required entrance guard.  
**Primary second-stage metric:** the smaller parent-specific TEST-OOD fifth-percentile normalized fine-label margin at effective layer two.  
**Claim boundary:** a controlled four-rule affine language task only; no open-domain semantics, native large-model Gate use, functional expert utility, or training-efficiency claim.  
**Minimal setup:** fixed three-layer Transformer, clean combination-held-out data, three data histories, four objectives, two seeds.  
**Changed variables:** pretraining rule diversity and teacher objective; after entrance, second-stage supervision and architecture.  
**Held fixed:** target data, model, optimizer, target-training steps, seeds, DEV selection rule, TEST seal, second-stage budgets, metrics, and bootstrap rule.  
**Pass:** a registered non-truth teacher family passes all teacher entrances for both seeds; second-stage links pass only by their separately frozen paired rules.  
**Fail:** no non-truth teacher passes after every frozen lineage completes, or a gated second-stage contrast is non-positive with otherwise eligible evidence.  
**Insufficient:** corrupted data/artifacts, resource mismatch, missing lineage, seed disagreement, failed function guard, or post-start unregistered scientific change.  
**Cannot claim:** that an Oracle objective is self-supervision, that a probe is native routing, or that a synthetic result transfers to natural language.  
**Approval decision:** execute in causal order and fail closed at the teacher entrance.

## 1. Terminology / Definitions

- **Next-token prediction:** at each non-padding position, predict the following token by cross entropy. There are 21 scored transitions in every 22-token target sequence.
- **Semantic key:** `(rule, ordered three demonstration inputs, query input)`. Two rows with the same key have identical mathematical content even when wording differs.
- **Paraphrase group:** four rows sharing one semantic key and differing only in template. It is the resampling and split-isolation unit.
- **DEV-ID / DEV-OOD:** development rows with seen template combinations / held-out template combinations. TEST-ID and TEST-OOD are untouched confirmation counterparts.
- **Non-truth teacher:** a teacher whose training objective never reads affine coefficients or target coarse/fine labels. O0, O1, and O2 qualify; O3 does not.
- **Third-layer entrance:** evidence that the final pre-answer state both answers held-out combinations and supports the registered true-parent linear readout. It is a prerequisite, not the final claim.
- **Oracle:** supervision from generator metadata. It is a positive-control upper bound, not a deployable label source.
- **Search label:** a frozen split constructed from third-layer states without reading generator truth; truth is revealed only for post-freeze alignment analysis.
- **Normalized conditional-fine margin:** within each true parent, signed binary probe distance divided by probe-weight norm; higher is better. The primary value takes the worse parent's fifth percentile.

## 2. Anchor Alignment

E01 failed before the Anchor mechanism became identifiable: both teachers solved new content under seen templates but failed unseen-template answers and the registered third-layer parent entrance. E02 changes only the upstream data and teacher-learning audit needed to establish that premise. If a non-truth teacher passes, the downstream architecture, metrics, and claim boundary return to the E01 Anchor clauses: correct semantic supervision, staged parent-first growth, frozen coarse path, residual fine routing, and learned-label replacement.

The strongest rival is surface memorization or generic extra compute. D1 controls extra target-rule data and steps; D2 changes only rule diversity at the same pretraining rows and steps; O1 tests answer-signal dilution; O2 tests template invariance without truth; O3 establishes a truth-supervised capacity ceiling.

## 3. Tested Hypothesis

The ordered hypothesis is:

1. repairing atomic token support and semantic-key overlap permits genuine combination-held-out evaluation;
2. O1 improves answer learning over O0 if full-sequence averaging dilutes the answer signal;
3. D2 improves cross-template rule transfer over D1 if diverse rule induction matters beyond extra data and compute;
4. O2 narrows the gap to O3 if paraphrase invariance is a useful truth-free formation signal;
5. after a non-truth teacher passes, Oracle flat supervision improves second-layer conditional-fine low-tail margin over the matched no-semantic flat model; only then are staged hierarchy, residual fine routing, and Search interpretable.

## 4. Rival Explanations

| Rival | Separating comparison or guard | Meaning if retained |
| --- | --- | --- |
| unseen token embedding caused E01 OOD failure | all atomic tokens occur in TRAIN; OOD holds out combinations only | remaining failure is not attributable to a never-trained token |
| more optimization is sufficient | D0 versus D1 and training-curve slope | supports extra target exposure, not rule diversity |
| any pretraining is sufficient | D1 versus D2 with equal rows and steps | separates target repetition from diverse-rule transfer |
| answer signal was diluted | O0 versus O1 | isolates fixed answer upweighting |
| explicit truth is required | O1/O2 versus O3 | O3-only success is capacity evidence, not a usable teacher |
| probe reads template | DEV-OOD accuracy, group split, bag-token leakage, paraphrase consistency | prevents a seen-template or count shortcut reading |
| downstream gains are generic adaptation | B1, shuffled labels, matched flat/hierarchy capacity and function guards | blocks causal semantic claims when generic controls match |

## 5. Data Construction And Provenance

### 5.1 Target four-rule task

All arithmetic is modulo 11. The four target leaves are:

| leaf | parent | fine | rule |
| ---: | ---: | ---: | --- |
| 0 | 0 | 0 | \(y=u+1\) |
| 1 | 0 | 1 | \(y=u+3\) |
| 2 | 1 | 0 | \(y=-u+3\) |
| 3 | 1 | 1 | \(y=-u+1\) |

Every row is exactly `<BOS> opening` followed by three five-token demonstrations, one three-token query prefix, the numeric answer, and `<EOS>`. Labels and affine coefficients remain metadata and never appear in visible text.

There are 24 templates formed by four openings crossed with six wording bundles. TRAIN combinations are `[0,1,2,3,8,9,10,11,12,13,16,17,18,19,20,21]`; DEV-OOD uses `[4,6,14,23]`; TEST-OOD uses `[5,7,15,22]`. TRAIN groups cycle through the four quartets `{0,8,16,19}`, `{1,9,17,20}`, `{2,10,12,21}`, `{3,11,13,18}` so each group contains four distinct openings and four distinct wording bundles. ID development and test use TRAIN combinations. Every atomic word and number token occurs in TRAIN; OOD withholds only combinations.

Enumerate all target semantic keys whose three rendered demonstrations identify exactly one of the four target rules. Allocate without replacement across TRAIN 25,000 groups, DEV-ID 2,000, DEV-OOD 2,000, TEST-ID 3,000, and TEST-OOD 6,000. Each group yields four paraphrases, giving 100,000 / 8,000 / 8,000 / 12,000 / 24,000 rows. Every split is exactly balanced over leaves.

### 5.2 Pretraining histories

Use affine rules \(y=au+b\pmod{11}\) for all \(a,b\in\mathbb Z_{11}\).

- **D0:** no pretraining.
- **D1:** 20,340 additional target-rule groups, 5,085 per target rule, disjoint from all target splits. It controls the extra rows and steps of D2.
- **D2:** 113 meta-training rules, excluding the four target rules `(1,1),(1,3),(10,3),(10,1)` and four meta-development rules `(1,0),(1,2),(10,0),(10,2)`. Draw 180 unique identifiable groups per rule, totaling 20,340 groups.

Meta-development uses the four held-out meta-development rules only as a diagnostic; it cannot select a checkpoint or objective. Pretraining uses only the 16 TRAIN template combinations. No target OOD template combination appears anywhere before target DEV-OOD.

### 5.3 Mandatory preflight

The data receipt must verify exact row/group counts, exact class/rule balance, four rows per group, four distinct templates per group, rule uniqueness from visible demonstrations, correct answer indexing, no label tokens, complete TRAIN token support, pairwise semantic-key isolation, target/pretraining disjointness, template partitions, deterministic hashes, and held-out unordered bag-of-token leakage near chance. Any failed structural check blocks smoke and full execution.

## 6. Learning Task And Permitted Supervision

All teacher families train the same causal sequence model. O0--O2 may read tokens, answer positions, and paraphrase group membership but may not read rule coefficients, parent, fine, or leaf truth. O3 may read affine coefficients only in its registered auxiliary heads. Target labels are never used for teacher checkpoint selection.

After teacher selection, Oracle branches may read parent/fine/leaf metadata only in their registered losses. Search fitting and selection may not read truth. TEST labels are unsealed only after the teacher, Search centers, assignments, and all analysis choices are immutable.

## 7. Model / Architecture And Frozen Variants

The teacher is a decoder-only three-block Transformer: hidden width 256, eight heads, feed-forward width 1,024, pre-normalization, SwiGLU, rotary positions, tied embeddings/language head, maximum length 64, and zero dropout. The third-layer and second-layer representations are taken at the last prefix position before the numeric answer.

After teacher entrance, clone the selected seed-matched teacher, freeze embeddings, all three blocks, final normalization, and language head, and insert modules after block two. Use the E01-verified modules and parameter ledger: dense bottleneck 128; hierarchy with two parent and four leaf adapters of bottleneck 64; flat control with shared bottleneck 43 and four leaf adapters of bottleneck 85. Flat versus hierarchy must remain within 1% for total trainable parameters and active-path adapter multiply-adds.

Hierarchical training uses 500 root language-only steps, 1,500 coarse steps, then 2,000 fine steps. At the fine transition, the coarse Gate and both parent experts are frozen. Residual routing removes the normalized learned binary coarse discriminant only from the fine Gate input; experts and the residual stream retain the full state.

## 8. Training Objective And Optimization

Let \(L_{full}\) average cross entropy over all 21 next-token transitions and \(L_{ans}\) be cross entropy only for the numeric answer.

- **O0:** \(L=L_{full}\).
- **O1:** \(L=(L_{full}+0.2L_{ans})/1.2\).
- **O2:** O1 plus within-group consistency. L2-normalize each third-layer pre-answer state, compute the four-row group centroid, and average squared distance from each state to its detached-or-live common centroid as one joint differentiable loss. Calibrate its scalar on the first eight batches so its gradient norm on shared Transformer parameters is 10% of the O1 gradient norm; clip the scalar to `[1e-3,100]` and freeze it.
- **O3:** O1 plus two linear heads on the third-layer pre-answer state predicting \(a\) and \(b\) as separate 11-way cross-entropies. Calibrate their mean auxiliary loss to the same 10% shared-parameter gradient-norm ratio and freeze the clipped scalar. This is an Oracle capacity control.

Use AdamW with learning rate \(3\times10^{-4}\), weight decay 0.1, global batch 256, 5% linear warm-up followed by cosine decay, global gradient clipping 1.0, bfloat16 autocast, and float32 losses. Seeds are 1701 and 2903. D0 trains 8,000 target updates. D1 and D2 train 8,000 pretraining updates followed by 8,000 target updates. The final pretraining state initializes target training; the final target checkpoint is audited, with no DEV-best or TEST-based checkpoint selection.

## 9. Conditions, Seeds, And Checkpoints

The full teacher matrix is `D0,D1,D2 × O0,O1,O2,O3 × seeds 1701,2903`, totaling 24 lineages. Every lineage must have a config, curve, final checkpoint, DEV-ID and DEV-OOD metrics, h2/h3 representation artifact, and completion status.

Among non-truth families for which both seeds pass, select the simplest in frozen order: objective O0 before O1 before O2, then data history D0 before D1 before D2 within the same objective. O3 is never selectable as the primary teacher. TEST is not read during selection.

If a non-truth family passes, run both seed-matched selected teachers through all conditions: T0, B0, B1, O-F, O-HF, O-HR, O-S, S-F, S-HF, S-HR, S-S, L1-SEQ, and L1-JOINT. Search and Oracle rows run fully even when their local entrance or positive control fails; their eligibility is typed rather than skipped.

## 10. Primary Metric And Frozen Analysis Plan

### Teacher entrance

For both seeds of one non-truth family, require simultaneously:

- DEV-ID answer accuracy at least 95%;
- DEV-OOD answer accuracy at least 85%;
- frozen h3 true-parent L2-logistic probe balanced accuracy at least 80%, fitted on TRAIN groups and evaluated on DEV-OOD groups;
- raw h2 is not already saturated under the E01 rule: its parent-conditional fine fifth-percentile normalized margin is not positive for both parents with a positive paired group-bootstrap lower bound.

The unit of independence is the paraphrase group. Teacher accuracies aggregate equally over rows after exact class/group balance is verified. Probe regularization is selected on DEV-ID from `C={1e-4,1e-3,1e-2,1e-1,1,10}` and then fixed for DEV-OOD. TEST is sealed. No family passes by averaging seeds.

### Second stage

Use the unchanged E01 analysis: parent-specific L2-logistic probes on TRAIN effective h2, penalty chosen once on B1 DEV-OOD and reused; primary value is the worse TEST-OOD parent fifth-percentile normalized margin. Bootstrap 2,000 paired complete groups within seed and in an equal-seed pooled analysis. A contrast is `STABLE_POSITIVE` only if both seed deltas are positive and the pooled one-sided 95% lower bound exceeds zero.

Function guards pass only if the pooled 95% upper bound of relative full-sequence NLL is at most +0.02 nat/token, answer NLL at most +0.05 nat/query, and the lower bound of answer-accuracy change at least -1 percentage point. Missing or failed rows are never imputed; any missing lineage makes the relevant verdict `INSUFFICIENT`. No multiplicity correction is used because each contrast answers a registered ordered link and later links cannot rescue an earlier failed link.

## 11. Secondary Metrics And Guards

Teacher diagnostics are TRAIN/DEV-ID/DEV-OOD answer accuracy and NLL, full-sequence NLL, curve slopes over the last 500 steps, exact-match by template and rule, h1/h2/h3 parent/fine/leaf probe scores, paraphrase cosine dispersion, O3 coefficient accuracy, and meta-development accuracy for D2. They locate failure but cannot replace the teacher entrance.

Second-stage diagnostics remain full margin distributions, true parent/leaf balanced accuracy, routing accuracy, Gate entropy, residual effective rank, Search stability/alignment after freezing, and training curves. Readability, routing correlation, and expert utility remain distinct evidentiary levels.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good data case: hand-checked demonstrations `0→1, 1→2, 2→3; query 4` under \(u+1\) must answer `5` under all four paraphrases.
- Known bad data case: duplicate semantic key across TRAIN and DEV-OOD must fail preflight.
- Known confusing case: all three demonstration inputs equal may fail to identify one affine rule among 121; meta pretraining must reject it even when it identifies one of the four target rules.
- Known good objective case: answer-only logits changed while all earlier logits are fixed must change O1 more than O0 by the frozen weighting formula.
- Known bad supervision case: O2/O0/O1 touching coefficient or coarse/fine metadata must fail the contract test.
- No-op architecture case: zero-initialized inserted adapters reproduce frozen-teacher logits before training.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / operation | Expected output | Pass / fail / insufficient | Handoff |
| --- | --- | --- | --- | --- | --- |
| S0 data | remove E01 data confounds | enumerate, allocate, render, hash, and audit v2 and pretraining data | manifests plus audit receipt | every structural guard PASS or execution blocks | immutable manifests to S1 |
| S1 teacher smoke | prove code and objectives operate | tiny rows/steps for all 12 family cells and both seeds where cheap | finite curves, checkpoints, metrics, representation artifacts | exact enumeration and artifacts PASS | permits ACP full teacher run |
| S2 teacher full | exhaust frozen formation candidates | train all 24 lineages on one 4-H100 node | complete lineage ledger and curves | all complete or relevant result insufficient | immutable DEV audit to S3 |
| S3 entrance | choose without TEST | apply both-seed thresholds and frozen simplicity order | selected non-truth family or typed no-entry result | pass unlocks S4; fail ends scientific route | teacher checkpoint pair or stop record |
| S4 second stage | test Anchor mechanism | run all 13 conditions for both selected seeds | 26 complete condition records | negative Oracle/Search never stops execution | artifacts to S5 |
| S5 analysis | adjudicate ordered links | unseal TEST, compute frozen probes/bootstrap/guards | tables, two clear figures, completion receipt | one verdict per registered link | summary/detailed evidence record |

Material hyperparameter or data changes after S0 registration require an amendment. More steps are allowed only through an approved amendment after DEV curves show continuing improvement; they cannot be triggered by TEST.

## 14. Algorithm, Output, And Provenance Contract

The worker root is `/data/250010109/MoE_Router/experiments/20260830_a15_13_semantic_supervision_hierarchical_experts`. E02 code, tests, configs, generated manifests, checkpoints, curves, raw metrics, logs, and figures remain there under a distinct `e02` namespace and run stamp. E01 files and defaults are immutable.

Formal execution uses SCO ACP, workspace `share-space`, cluster `share-cluster`, one worker node, spec `n6ls.iu.i40.4`, four H100 80GB GPUs / four worker processes, reserved quota, normal priority, image `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`, and storage `01995892-d478-76d8-aec7-13fd8284477e:/data`. Submission must print this exact tuple and refuse any mismatch.

Each process owns disjoint lineages; rank zero maintains an atomic global ledger. Resume accepts only a complete checkpoint whose config, data hashes, code hash, seed, phase, and optimizer/scheduler state match exactly. Non-finite loss, data hash mismatch, resource mismatch, artifact overwrite, or incomplete resume metadata stops the affected lineage and the job records the named reason.

Expected canonical evidence after completion is `summary.md`, `detailed.md`, `tables/`, `figures/`, and small receipts in this E02 directory. Raw datasets, logs, and checkpoints are not copied into Research_System.

## 15. Success / Failure / Insufficient Evidence

- **Teacher PASS:** at least one non-truth family passes every entrance in both seeds; selection follows the frozen order.
- **Teacher FAIL:** all 18 non-truth lineages complete and no family passes. O3 may show capacity but cannot alter this verdict.
- **Teacher INSUFFICIENT:** any required non-truth lineage or artifact is missing/corrupt, data audit fails, or an unregistered post-start change affects eligibility.
- **Second-stage link PASS:** stable positive primary delta and every matched language guard passes after teacher PASS.
- **Second-stage link FAIL:** eligible evidence is non-positive or violates a function guard with both seed records complete.
- **Second-stage link INSUFFICIENT:** seed disagreement, failed prerequisite, missing artifact, or analysis-contract violation.

## 16. What This Cannot Claim

Even a full PASS cannot show that generic language models naturally discover human semantic hierarchies, that a linear probe is a native Gate, that an expert performs a distinct function, that hierarchy is compute-efficient, or that removing one coarse discriminant removes all common information. D2 can establish a benefit of affine-rule diversity under matched exposure, not abstract reasoning in general. O3 can establish capacity under explicit truth, not self-discovery.

## 17. Block Confirmation, Freeze, And Amendment Ledger

### Confirmation ledger

| Block | State | Human confirmation |
| --- | --- | --- |
| A question and scope | CONFIRMED | approved staged teacher audit and full gated experiment |
| B data | CONFIRMED | approved affine-121 construction, target exclusions, sizes, and clean combination OOD |
| C task / supervision | CONFIRMED | approved full-sequence CE plus O0--O3 variants and truth boundary |
| D architecture | CONFIRMED | approved fixed three-layer teacher and E01 downstream architecture |
| E objective / optimization | CONFIRMED | approved 0.2 answer weight, 10% gradient calibration, and 8k schedules |
| F conditions / metrics | CONFIRMED | approved 3×4×2 teachers, entrances, selection, and complete downstream grid |
| G execution / reporting | CONFIRMED | approved one-node four-reserved-H100 full execution and clear bounded reporting |

### Final audit

Anchor question unchanged: PASS. Decision-bearing choices grounded or human-confirmed: PASS. Cold-reader snapshot: PASS. Treatments and held-fixed variables explicit: PASS. Causal stage contract: PASS. Frozen analysis gives typed verdicts: PASS. Preflight/smoke protect scale-up: PASS. TEST and confirmation truth leakage blocked: PASS. Artifact provenance auditable: PASS. A--G confirmed and cross-block consistency PASS: PASS. Named execution scope approved: PASS. Amendment rule recorded: PASS.

### Amendment ledger

After the first data artifact or training update is produced, the scientific body above is append-only. Every amendment must record ID/time, before/after, reason, visible data/results, affected blocks/conditions, human approval, and eligibility impact.

#### A1 — pre-training operational clarification (2026-08-30T22:29:00Z)

- **Before:** O2 said “detached-or-live common centroid”; the D1/D2 optimizer boundary was unstated; the h2 non-saturation sentence added a bootstrap phrase although the researcher approved “the same E01 rule.”
- **After:** O2 uses one fully differentiable live group centroid. D1/D2 reset AdamW and the warm-up/cosine schedule at the target phase, transferring model and O3-head weights but not optimizer moments; this gives D0, D1, and D2 the same cold target optimizer. The h2 entrance uses the exact E01 rule: the worse-parent DEV-OOD fifth-percentile normalized conditional-fine margin must be at most zero; no bootstrap is part of this entrance.
- **Reason:** remove implementation ambiguity and restore the explicitly approved E01 entrance definition before any teacher update.
- **Visible data/results:** the v2 data manifest and structural audit were visible; no teacher training, development metric, or TEST result existed.
- **Affected blocks/conditions:** objective O2, D1/D2 phase boundary, all teacher entrances.
- **Approval:** covered by the researcher's explicit instruction to directly construct and execute the confirmed choices without another approval pause; the h2 clause is a correction back to the human-approved E01 rule.
- **Eligibility impact:** none; applied before the first training update and uniformly to every relevant lineage.

#### A2 — paired base initialization correction (2026-08-30T22:46:00Z)

- **Before:** the first non-scientific cluster smoke derived model initialization from seed plus history/objective names, so smoke groups were not paired at initialization.
- **After:** the base Transformer initialization is a deterministic function of registered seed only. All D0/D1/D2 and O0/O1/O2/O3 lineages with seed 1701 share one exact initial Transformer state; the same holds independently for seed 2903. Data history and objective begin to differ only after initialization.
- **Reason:** restore the Protocol's held-fixed paired-seed comparison before scientific execution.
- **Visible data/results:** one explicitly non-scientific three-step smoke had completed; no full teacher update or scientific development/TEST result existed.
- **Affected blocks/conditions:** all 24 teacher lineages.
- **Approval:** implementation correction required by the already confirmed paired-seed design and direct-execution authorization.
- **Eligibility impact:** the first smoke remains engineering-only and ineligible, as already registered. All later full lineages use the corrected initialization and remain eligible.

#### A3 — remove target leaf/template-quartet coupling (2026-08-30T22:49:00Z)

- **Before:** in data-v2a, target leaf and TRAIN quartet both used `group_index mod 4`, so each leaf was tied to one quartet despite complete atomic-token support. Dataset hash was `b60b9cf9d057b2c15eb14587db3523e62c60c64179feefee3b0d80fe2b932f94`.
- **After:** four consecutive leaf groups share one quartet, then the quartet rotates. Every target leaf sees all 16 TRAIN template combinations with counts differing by at most one. The immutable data-v2b hash is `586f53b12289beebe90f81fa1ecf33b7e865898613f3782e0c5452ec5751caca`.
- **Reason:** eliminate a newly audited template shortcut while preserving the already confirmed template partitions, rule keys, split sizes, histories, and visible sequence format.
- **Visible data/results:** v2a structural diagnostics and one non-scientific smoke were visible; no full teacher update or scientific TEST result existed.
- **Affected blocks/conditions:** target TRAIN/DEV-ID/TEST-ID template assignment for all teacher and second-stage conditions. Semantic keys and OOD template sets are unchanged.
- **Approval:** direct data-repair and full-execution authorization; this change enforces rather than changes the confirmed requirement that OOD withhold only combinations and that rule labels not be coupled to templates.
- **Eligibility impact:** data-v2a and its smoke are ineligible and retained only for debugging provenance. All full runs must refuse any hash other than v2b.

#### A4 — post-failure top-only behavior-distilled teacher repair (2026-08-30T23:39:00Z)

- **Before:** all 24 registered D0/D1/D2 × O0/O1/O2/O3 lineages jointly trained all three Transformer blocks. The frozen entrance correctly stopped the second stage when no non-truth family passed.
- **After:** retain the completed 24-lineage result unchanged and add one separately named E02-R repair lineage. For each registered seed, first train D0-O1 for 8,000 target updates while freezing the embedding/tied language head and Blocks 1--2; only Block 3 and final normalization update. Freeze this base teacher, replace its query by `0` and `1`, and use the two numeric predictions to form the teacher's own affine signature `(a_hat,b_hat)`. Keep the four most frequent signatures and map rare signatures to their nearest center by squared circular distance modulo 11. Reveal generator truth only after these labels and centers are frozen. Clone the same base checkpoint into a 2,000-update behavior-distilled non-truth branch and a matched 2,000-update Oracle-coefficient branch; both keep the lower representation frozen and use the same 10% shared-gradient auxiliary calibration. Oracle is never selectable. Only if both behavior-distilled seeds pass the original four DEV entrances does the unchanged complete second-stage grid run.
- **Reason:** the complete teacher matrix showed that data repair solved cross-template answering but joint training moved fine-rule information into every layer, eliminating the registered second-layer improvement margin. A one-seed top-only diagnostic preserved the second-layer margin but left third-layer parent semantics implicit; the frozen behavior-label distillation isolated and repaired exactly that remaining failure.
- **Visible data/results:** TEST remained sealed. The complete v2b teacher matrix had 24/24 lineages with near-perfect DEV-OOD answers and h3 parent readability but every h2 fifth-percentile conditional-fine margin positive. For D0-O0, even h1/h2/h3 fine probes were 100% accurate after joint training, whereas the untrained h2 margins were negative. The top-only D0-O1 seed-1701 diagnostic reached DEV-OOD answer accuracy 0.986625 and h2 margin -0.023997 but h3 parent accuracy only 0.635750. Its truth-free two-query behavior labels matched the subsequently revealed coefficient pair on 0.9988 of TRAIN rows; a 2,000-update diagnostic then reached DEV-OOD answer accuracy 0.988375, h3 parent balanced accuracy 0.989250, and h2 margin -0.031029.
- **Affected blocks/conditions:** teacher formation, teacher provenance, and the entrance-to-second-stage handoff only. Target data, answer/full-sequence loss, seeds, original entrance thresholds, TEST seal, second-stage conditions, budgets, metrics, and analysis remain unchanged.
- **Approval:** the researcher explicitly authorized autonomous troubleshooting after choices 1--13, direct construction without another approval pause, and persistent completion of the teacher audit and full run. This amendment stays within that named scope.
- **Eligibility impact:** the original `e02-full-20260830T225500Z` run remains an eligible final `FAIL_NO_NONTRUTH_TEACHER_ENTRANCE` result and is never overwritten or reinterpreted. E02-R uses a distinct run root, checkpoint lineage, label receipt, code hash, and gate. The one-seed local diagnostics are mechanism evidence only and are ineligible for the paired verdict. E02-R is eligible only if both new behavior-distilled seeds and both Oracle controls complete under the amended contract; TEST remains sealed until the paired non-truth gate passes.

### Execution receipt (2026-08-31T00:32:10Z)

- Original full run `e02-full-20260830T225500Z`, ACP job `pt-f2192fu8`: `SUCCEEDED`; all 24 teacher lineages completed; registered result `FAIL_NO_NONTRUTH_TEACHER_ENTRANCE`; second stage remained sealed.
- Repaired full run `e02r-full-20260831T000800Z`, ACP job `pt-0kqh48ql`: `SUCCEEDED`; both behavior-distilled non-truth teachers passed; TEST was then unsealed; all 24 trainable second-stage conditions and two T0 teacher records completed; the 2,000-draw analysis and both registered figures completed.
- Canonical result reading path: [summary.md](summary.md) -> [detailed.md](detailed.md) -> [result tables](tables/result_tables.md).
- Result state: machine evidence complete; researcher-owned closed-book judgment and Focus update pending.
