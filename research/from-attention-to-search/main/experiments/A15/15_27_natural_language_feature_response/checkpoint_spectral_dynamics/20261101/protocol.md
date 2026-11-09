# Protocol: A15_27_05_01 / Dense checkpoint spectral dynamics / 2026-11-01

## 0. Approval Snapshot

Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FORMAL_READ_ONLY_ANALYSIS.
Approval source: researcher request in this conversation on2026-11-01 explicitly asks to write Anchor/Protocol, audit, smoke and complete formal analysis; routine deterministic operational choices implement that scope. A-G: CONFIRMED_WITHIN_USER_SPECIFIED_SCOPE; cross-block consistency: PASS after recorded audits. Scientific acceptance/closure: Unknown. No language-model or dictionary training, existing-job changes, new conversations, commit/push or external publication.

Purpose: distinguish time courses of variance scale, normalized spectrum, original directions, rotation-tolerant sample relations and external-label readability. Primary [Anchor](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/subanchors/15_27_05_01_checkpoint_spectral_dynamics_anchor.md). Existing [Focus](../../../../../focus/focus_spectral_semantic_granularity.md) remains the question owner; this is its bounded Dense extension, not a reset. The original coordinates and three questions remain separate. Primary metric: adjacent normalized projection distance and spectral distance per actual training-token interval, interpreted with sampling sensitivity. Pass/Fail/Insufficient refer to each registered clause, not a combined positive verdict.33B is an observation endpoint. No onset time will be estimated because a scientific tolerance has not been justified.

## 1. Terminology / Definitions

B=10^9 actual cumulative valid language-model prediction targets; not parameter billions. Checkpoint means saved model weights with immutable manifest and internal training counters. One geometry observation is one selected token vector; one resampling unit is a document record. N8 paper IDs are unavailable. A spectral band is a contiguous range in a checkpoint's own descending eigenvalue order; it is not a persistent semantic identity. Residual-post means after the block attention and MLP residual additions, before final global norm.

## 2. Anchor Alignment

A assesses scale and allocation, B original directions, C paired sample relations and linear classification. The rival is ongoing coordinate rotation and/or sampling error despite stable eigenvalues. The answer may support different times, continued change, or insufficient estimation. It cannot establish native causal semantics, learning cessation, mathematical convergence or routing benefit. Complete curves precede semantic readouts.

## 3. Tested Hypothesis

No fixed positive temporal ordering is assumed. Compare whether late adjacent changes decrease across several intervals, reach the within-checkpoint sampling reference or rebound. Head-first versus middle/tail-later is checked only under this corpus/interface. Absence of such order weakens its dynamics interpretation without judging separate unfinished optimization experiments.

## 4. Rival Explanations

Pure orthogonal coordinate rotation can change raw axes while preserving eigenvalues and sample relations. Scale changes can preserve normalized spectra and CKA. Nearly equal eigenvalues can arbitrarily rotate an estimated basis. Vocabulary, source and a small labeled panel can generate apparent class information; labels are external associations, not native model usage. Irregular checkpoint gaps change raw distances; both distances and per-billion-token rates are required.

## 5. Data Construction And Provenance

Freeze [config.json](config.json) and [manifest.json](manifest.json) before model forwards. Native tokenizer is the local Qwen3-0.6B-Base tokenizer with recorded files digest3b602daf74810b313b8e1eca542d50b639a4e3f9de9b7185a309e09289306eda, separate from model weights. Geometry uses asset ntp_statistics_panel_2048: existing selected.jsonl,2048 exact256-token sequences, fit1024/test1024, balanced eight academic categories. Use positions7,15,...,255,32 per record,32768 observations per split. Equal positions per document imply equal document mass. Input IDs, all-one attention masks, context, order and positions are identical at every checkpoint. Exact text/token and record-group cross-split collisions must be absent. Reference covariance, means and Procrustes fit only fit records. Test centers itself only for CKA as a statistic; no evaluation fitting is reused for a learned transformation. Historical panel exposure and unavailable paper-level grouping make evaluation descriptive, not pristine confirmation.

Semantic bridge uses R12's96the records from the inherited R11 A02 documents, exact token279 occurrences and192-token contexts. Preserve fitted_document_ids.csv's16TRAIN/8DEV per binary task and the original heldout sets; apply the saved visible-prefix H label review. Three tasks: math/biology, algebra/analysis conditional on math, cell/ecology_evolution conditional on biology. No labels or thresholds derive from Dense responses. The bridge cannot fit the1024D spectrum. Existing Qwen activation caches have incompatible parents and are excluded. No Dense dictionary is required; no CrossCoder is applied.

## 6. Learning Task And Permitted Supervision

Statistical fitting: reference means/PCA/orthogonal Procrustes. Supervised fitting: binary logistic readouts on external TRAIN labels, C chosen on DEV; no language-model updates. Fit each checkpoint independently in its own basis and in fixed33B reference basis. These readouts measure linearly accessible association only. No fixed-endpoint classifier transfer is substituted for refitting. No task token loss, epochs or dictionary training are invented for closed-form statistics.

## 7. Model / Architecture And Frozen Variants

Native Dense:8blocks, hidden1024,MLP3072,16query heads,8KVheads,head128,vocab151936,tied embedding/output,281431040parameters,SAE mode none. Use exact original dense_sae model source, strict load. Main tensor final_raw_h is blocks[7] residual-post before model.norm. For early/mid/late only, capture outputs of blocks[0] and blocks[3]. Last block is manually unrolled by native forward_intermediates, so use norm's pre-hook to verify main tensor rather than assume blocks[7]'s forward hook fires. Existing pre_mlp_input is final block norm2 input to MLP, a different interface. All model parameters frozen, eval mode, inference_mode, FP32 forwards, TF32 off, math SDPA, dropout zero. Compute covariance/eigendecomposition/alignment in FP64. No activation normalization/whitening.

## 8. Training Objective And Optimization

Language-model training: NOT_APPLICABLE; zero optimizer steps. Orthogonal alignment R=UV^T from SVD(X_t^TX_33)=USV^T allows reflections as well as rotations, no fitted scaling. Each X is centered by its own reference mean. Apply R to evaluation vectors after their own checkpoint reference centering. Readout uses TRAIN-only per-coordinate standardization, class-balanced L2 logistic regression, C in0.01/0.1/1/10, max_iter3000,tol1e-8,DEV balanced-accuracy selection, smallest C on ties. Same splits, capacity, grid and selection at all three checkpoints. Report convergence failures rather than silently relaxing tolerances.

## 9. Conditions, Seeds, And Checkpoints

Main: all12readable states at0.5/1/3/5/10/15/17/19/21/22.018691584/31/33B. Inventory also retains missing payloads and out-of-window states.19B uses its exact manifest/digest-matched continuation archive. No interpolation is a measurement. Early/mid/late fixed0.5/17/33B for first smoke, semantics and early/middle layer supplements. Seed1101. Complete actual state tokens/step/config and source/hash must match manifest at runtime; native strict load and architecture match are hard gates. The continuation from10B and the later continuation from22.018691584B must be linked by original start-pointer/spec records.

## 10. Primary Metric And Frozen Analysis Plan

Reference-centered C=X^TX/(N−1),N32768,all checkpoints own mean. Save s_i and lambda_i=s_i²/(N−1) separately. Save absolute lambda,trace,p=lambda/trace,cumulative sum p,dimensions to50/80/90/95/99%,effective rank exp(−sum p log p),numerical rank at lambda_max*1e-10,mean norm and raw mean drift.

For pair a,b, absolute spectral distance=||lambda_a−lambda_b||_2 (variance units); symmetric relative absolute-spectrum distance=that/sqrt(||lambda_a||||lambda_b||); normalized-spectrum distance=0.5||p_a−p_b||_1. Report adjacent and33B pairs; divide each by actual delta tokens/1e9 for rates. Keep raw values and intervals visible. Ratios to endpoint do not demonstrate stability.

For each own-basis band and nested rank compute all principal angles, RMS/max angle and d_proj=sqrt(max(0,1−||U^TV||²_F/k)). Also compare after Procrustes: row vectors X_tR have column basis R^TV_t. Save raw/aligned results separately. Fixed33B basis variances diag(V_33^TC_tV_33) are named projected variance, never eigenvalues. Band eigengap boundaries are saved. Single-vector sign-absolute cosines are permitted only when both left/right relative gaps are >=0.05 at both checkpoints; otherwise UNIDENTIFIABLE. Near-degenerate band boundaries remain sensitivity-limited; no semantic vector tracking.

## 11. Secondary Metrics And Guards

CKA on exactly paired independent test vectors: center each test matrix, use ||X^TY||²_F /(||X^TX||_F||Y^TY||_F), streaming cross-moments without a full sample Gram. Report adjacent and endpoint CKA. Raw and aligned evaluation residual=||X−Y||_F/||Y||_F with own reference means; mean drift is separately recorded. Procrustes fits reference only. Save orthogonality and train/eval residuals, raw/aligned subspace distance. Aligned stability cannot overwrite raw drift.

Eight deterministic reference document512/512splits, identical across checkpoints, at0.5/17/33B and one possible key turn. Turn rule: right endpoint of largest absolute successive log normalized-spectrum-rate change, ties earliest; selector saved. Each half gives own mean/covariance. Show within-checkpoint split spectral/subspace distance and mean-drift reference; report empirical2.5/50/97.5%ranges as sensitivity, not calibrated population CIs. Adjacent metric / split-reference ratios with thresholds0.5/1/2 are descriptive only. For early/mid/late endpoint pair, use corresponding same halves across time and report paired ranges. No statistically certified onset. Tail sensitivity implies estimator insufficiency.

Readout sets:64Dhead1–64,middle481–544,tail961–1024;128Dhead1–128,head+middle,head+tail;full1024. Each in own/current and fixed33B bases. Balanced accuracy averages the two class recalls. Report heldout sample counts, TRAIN/DEV fit ledger, selected C, full-space baseline,2000paired stratified heldout resamples. Primary incremental contrasts:head+middle−head128 and head+tail−head128; also show head gains to separate generic added dimension. Holm correction across3checkpoints×2bases×3tasks×2increments=36prespecified contrasts; no label permutation sweep required to declare absent gain. Wide intervals remain insufficient. No chance-based onset is estimated on only three timepoints. Existing source/format matching insufficiency is retained.

## 12. Known Good / Known Bad / Known Confusing Cases

Identity:zero spectral/subspace/residual,CKA1. Synthetic rotation:same spectrum,possibly changed raw leading subspace,CKA1,aligned residual near0. Positive scale:normalized spectrum and CKA unchanged,trace/residual changed. Shuffled paired rows:CKA/alignment relations degrade despite unchanged individual spectrum. Full1024Dprojection distance is structurally0 and excluded as evidence. Numeric acceptance1e-8for FP64 identities,FP32 hook equality exact/no-op tolerance1e-6relative;finite covariance,orthogonal eigenbasis,residual<1e-8FP64,trace reconstruction<1e-8relative. Any critical guard failure stops scale-up.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How and why | Output / pass | Failure and handoff |
| --- | --- | --- | --- | --- |
| Inventory | Compatible saved trajectory | Source manifests/configs,actual paths,archive digest binding,strict asset checks | Exact readable list and missing table | Identity mismatch blocks that state;no replacement trajectory |
| Data freeze | Paired samples without fit leakage | Freeze existing tokens/masks/positions/splits before forwards | Panel hashes and counts | Collision/schema failure blocks all geometry |
| Audit | Rival and fit separation | Three recorded identification,data/statistics,numerics reviews | A-G consistency and calibration | Repair within scope and record changes |
| Smoke | Native load/interface/cache | Three fixed states,8records,main+supplement hooks;reload cache test | Counter/load/hook/finite/resume PASS | No formal batch before PASS |
| Main geometry | Complete training curves | One checkpoint at a time,atomic per-layer cache,FP64stats | All12main states,three supplements,paired relations | Preserve completed caches;missing states remain missing |
| Semantics | Information availability | Only after geometry tables,refit matched readouts | Accuracy/increment/uncertainty tables | Failed label coverage blocks only affected task |
| Delivery | Auditable bounded result | Four figure groups,Summary/Detailed,coverage,lineage,caches | Local artifacts and registered outputs | Scientific acceptance remains Unknown |

## 14. Algorithm, Output, And Provenance Contract

Execution root:/data/250010109/MoE_Router/experiments/20261101_dense_checkpoint_spectral_dynamics. Code: scripts/prepare.py,collect.py,analyze.py and calibration script. Registered config/scientific-body hash saved before forwards; code hashes saved in a pre-execution receipt. Cache key hashes checkpoint payload digest,manifest,exact panel bytes,positions,layer,precision/preprocessing and collector code. Each cache uses atomic file+metadata completion; partial files never qualify. Reuse requires key and payload digest equality; each checkpoint releases model/weights and empties CUDA cache. No cache name alone establishes identity.

Input assets:model_dense_33b,model_s7_temporal_dense_1b_a24_20261013,model_s7_temporal_dense_5b_a24_20261013,model_s7_temporal_dense_15b_a24_20261013,model_s7_temporal_dense_31b_a24_20261013,ntp_statistics_panel_2048,tokenizer_qwen3_0p6b_base,analysis_a15_27_05_r12_spectral_semantic_granularity_20261031,data_a15_27_r11_qualified_three_domain_A02_20261030,and newly registered exact Dense12state family. Current strict checks required before payload use. Large caches stay execution-side; code/config,small metadata,curated evidence and source tables live with this record.

Resource exception explicitly selected by researcher:at most twoRTX5090 shared with other analyses. Use envelope5090-2-spot/shphd-lite-0911 and mounted qualifiedSM120runtime; no fallback. Inspect active own analysis jobs before reservation; one analysis allocation holds both slots through smoke and full measurement. Single worker uses at most one GPU at once; second is reserved as part of the selected tuple, not a third worker. Total runtime ceiling6hours and new storage20GiB. Reaching ceiling stops and preserves caches;no data/metric relaxation. Existing training jobs are untouched. ACP submission uses repository template,dry-run first,local compatibility proxy only for old CLI workspace-schema fields. Durable logs,submission and terminal receipts mandatory.

Required output:checkpoint inventory/config/code;all eigen/singular values,bases/means,metrics,pairwiseangles,projected variances,split sensitivities,readout/predictions/contrasts,fit/coverage ledgers;fourfiguregroups;reusablecacheindex;summary.md/summary_cn.md,detailed.md/companion;output asset registration and local Anchor reading sync. Figure x-axis actual trainingB; log/distance axes and missing intervals explicit. Numerical error and sampling variation are different quantities.

## 15. Success / Failure / Insufficient Evidence

Engineering completion=all applicable requested outputs with explicit failed/missing statuses. Scientific clauses remain separate:decreasing changes beyond uncertainty can support within-window stabilization for that metric;precise contrary patterns weaken the named ordering;wide intervals,unresolved direction blocks or weak labels yield insufficient. No pooled pass label rescues a failed clause. No forced convergence time or interpolation.

## 16. What This Cannot Claim

Final convergence,semantic mastery,causal native use,no further learning,optimal routing stages,or benefit/harm in unfinished training. Shared tokenizer does not make Dense Qwen. No CrossCoder result is a Dense result.8reference splits are not8models. Classification availability and geometric stabilization may differ.

## 17. Block Confirmation, Freeze, And Amendment Ledger

2026-11-01:user supplied A-G scientific scope and explicit implementation/smoke/full authorization;deterministic operational instantiation recorded here. Initial status DRAFT_NOT_EXECUTABLE during writing;promoted after in-scope consistency audit. No further permission required for the same authorized scope. Source counts and readout identity follow inspected existing assets. Scalar convergence tolerance remains Unknown;onset estimation is therefore excluded as user permits.

Freeze:the initial body,config,manifest and code hashes are saved in freeze.json before any forward. After start,this body is immutable. Execution receipts/results link from Detailed;material changes append an amendment stating before/after,reason,time,results already visible,authorization and eligibility. No scientific result is written back into this body.


### Amendment A01: proper rotations only

2026-11-01. Before: Section8 permitted orthogonal reflections. After: impose both R^TR=I and det(R)=+1, with R=U diag(1,...,det(UV^T)) V^T from the same reference-only crossmoment SVD. No scale is fitted. This implements the researcher's explicit rotation-only request. All raw caches and spectra plus partial pair metrics were already visible; no semantic result motivated the correction. Recompute only affected aligned metrics and regenerate derived tables/figures. Old negative-determinant aligned outputs are superseded and ineligible for final evidence. Inputs,raw coordinates,CKA,splits,readouts and decision rules remain frozen. Cached CPU correction needs no new forwards or GPU allocation. Initial bytes/hashes remain in audit/frozen_sources; exact amendment and validation are recorded in audit/amendment_A01.json and audit/rotation_only_correction.json.


### Administrative clarification A02: no nominal checkpoint grid

The initial inventory included7/9/11B as examples of unmeasured nominal points. The source training contract did not require that grid. Remove those examples from missing_milestones;only the eight source-manifested states with unavailable weights count as missing. All twelve measured checkpoint rows,inputs,positions,splits,metrics and selections are unchanged. The initial manifest bytes remain archived;see audit/amendment_A02.json.


### Engineering amendment A03: derived-cache identity

The registered run.sh entrypoint now checks a fingerprint of checkpoint payload/manifest,activation keys,exact panels/positions,layer/preprocessing,config and statistical code before reusing derived NPZ files. Completed arrays are sealed with hashes. The current freshly produced and independently audited outputs are explicitly qualified once;unqualified caches or a changed identity are refused. No statistical/data/selection change,new forward or refit occurs. See audit/amendment_A03.json and analysis/cache_context.json in execution storage.
