派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/protocol.md)；研究修改仍回到原件。

---

# Protocol A15_24_03: frequency and direction-intervention impact

## 0. Approval Snapshot

Explicit researcher authorization covers Anchor, Protocol and autonomous bounded verification; continuation was reaffirmed. This completed draft moves from DRAFT_NOT_EXECUTABLE to FROZEN_FOR_BOUNDED_ANALYSIS upon hash freeze. Owner15_24_03 under15_24, no independent Focus or imported task directions. Scientific judgment Unknown. Local H100 MIG only;2 CPU threads,12GiB GPU,900s worker,1GiB output. No remote submission, training, publication or closure.

## 1. Terms And Units

Feature=fixed dictionary coordinate; p=original TRAIN positive-activation rate; B1/B4=original low/high bands. An event is a feature-position activation, not an independent question. NLL is actual next-token negative log probability in nat. PCA is input geometry; D is final-minus-initial displacement, not full W.

## 2. Anchor Alignment

Tests the Anchor conditional association: same parameter intervention, frequency bands, measured covariate matching and random controls. Existing rollback effects motivate but do not identify frequency causation or long-horizon complement training.

## 3. Hypothesis And Branches

Primary T is low-minus-high mean excess effect at50% rollback; two-sided. A qualified numerical pattern requires support/balance, consistent seed signs, both conditional95% intervals excluding zero and |T|>1e-6nat. It does not accept a mechanism. Crossing zero is insufficient, not equivalence. Inconsistent signs do not form the pattern. Failed qualification takes precedence and cannot be rescued by secondary analyses. The floor is descriptive, not an error bound or practical threshold.

## 4. Rivals And Controls

Eight same-rank random bases matched in actual parameter-edit norm; exact rewrite; two fixed doses; measured context/amplitude matching; same-position identity check. No outcome-driven basis, dose, random draw or stopping choice. Residual semantic confounding remains.

## 5. Data And Frequency Provenance

Original Tulu TRAIN85548 positions/1024 dialogues, DEV10340/128;693 E0 positions. groups.npz p was rechecked against original TRAIN positive counts/85548 and matches exactly. No DEV frequency rebins. Event counts B1=908,B2=7195,B3=97021,B4=132768 reuse position losses and are not independent sample counts. data/dev.jsonl aligns current/next token with cache block/position/target. DEV is exposed, not fresh confirmation.

## 6. Supervision And Selection

DEV labels only evaluate loss. No gradient, basis/dose/matching/stopping selection uses intervened loss. Matching uses fixed inherited mean two-seed baseline NLL as a pretreatment covariate. Covariate scales are candidate-event SDs for descriptive balancing, not an independent confirmation design.

## 7. Model And Frozen Objects

Original T_F seeds11/22 step168,85548targets; eight full-input SwiGLU residual experts, top2 coefficients.5. Only experts.0.up.weight changes temporarily. All23 other matrices, scale and head fixed. Restore after every edit and verify final full-model digest. No gradient, optimizer, continuation or new checkpoint.

## 8. Parameter Intervention

D=W168-Winit; P=VVᵀ from existing TRAIN PCA16. a=.25/.5. PCA edit=-aDP. Random r=0..7 uses NumPy seed20261024+31r, Gaussian1024×16 and QR, shared across models. Edit=-aDQQᵀ rescaled to PCA norm; actual FP32 norm mismatch<=.002. FP32 forward, TF32off, FP64 projections.

## 9. Conditions And Counts

Per seed baseline, exact_noop and2doses×(PCA+8random)=18, total20readouts;40overall. Recompute the same693 positions with identical micro64 batches. Extra algebra/schema guards are not scientific conditions.

## 10. Primary Metric And Aggregation

Position delta=edited-baseline NLL; y=delta_PCA-mean8random delta. T=equal pair mean(y_low-y_high). Resample dialogues5000times, keeping all fixed pairs within a dialogue together; conditional95% intervals. These do not quantify model-seed or random-basis population uncertainty. Retain each random T and leave-one-random-out values. Middle-band and feature macros descriptive only.

## 11. Matching Support And Balance

Primary exact dialogue/current-token/other-expert; five continuous covariates log(z×decoder norm),log decoder norm,log hidden RMS,inherited mean baseline NLL,position/input length. Scale by combined B1+B4 event SD. Each coordinate caliper.5; global greedy squared distance, deterministic distance/position/feature ties, no position reuse or same-position pairs. Qualification >=20pairs,>=10dialogues,all |SMD|<=.1. Covariate-only preflight gives11pairs/9dialogues,max|SMD|.1513 and already fails. Disjoint cross-dialogue same-source/token/route diagnostic gives1pair and does not replace primary. No post-outcome relaxation.

## 12. Known Good And Confusing Cases

Original four tensor hashes and fixed sources; inherited FP32 baseline replay maxerror<=1e-6; exact no-op; finite losses; frozen tensors/head; exact pair identities/calipers/no reused position. Same-position B1/B4 duplicate outcomes must give zero. Independent CPU reaggregation and audit required.

## 13. Execution And Stops

Metadata preflight and repair record; complete/freeze bilingual design; bounded forwards; save position NLL/edit diagnostics; independently verify statistics,three audits and coverage; deliver bilingual facts. Failed numerical gates invalidate dependencies and remain recorded. Insufficient matching does not cancel independent finite measurements. Stop at900s,12GiB,1GiB or nonfinite values; no expanded model/data/parameter scope.

## 14. Artifacts And Identity

Execution root /data/250010109/MoE_Router/experiments/20261024_frequency_effect_association. frozen.json,design_freeze.json,worker.py,matching.py,event_covariates.npz,matched_pairs_*.npz,seed*_nll.npz,results.json,audits.json,verification.json. Payloads remain execution-side; project retains small manifest/factual records. Hash code,inputs,bases,models and frozen documents.

## 15. Eligibility And State

All40 conditions need outcomes or explicit failures. Finite-intervention eligibility and frequency-association eligibility are separate. Known inadequate matching makes primary INSUFFICIENT, not NOT RUN or evidence of no association. Scientific judgment and next experiment await researcher review.

## 16. Nonclaims

No frequency causation,feature semantics,independent modules,all-expert regularity,long-training benefit,general forgetting or untouched confirmation. All693 positions contain both bands; matched events do not isolate feature contributions.

## 17. Freeze And Deviations

Covariates/support/inherited baseline were inspected before freeze; prior A15_24_02 PCA and one-random effects are already exposed. This is follow-up exploration, not independent preregistration. Eight new random controls are computed after freeze. Metadata-only repeated compressed-array decompression was repaired before outcomes and retained. Later implementation repairs must preserve failed evidence and dated amendments without scientific retuning.

