派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/protocol.md)；研究修改仍回到原件。

---

# Protocol A15_29 R01: Progressive versus full contextual spectral supervision

## 0. Approval Snapshot

Document status: APPROVED_FOR_IMPLEMENTATION_OFFLINE_2GPU_SMOKE_AND_PASS_GATED_8GPU_FORMAL.
Approval: explicit researcher instruction in this conversation,2026-10-31. The user delegated routine implementation and profiling choices; no repeated approval is needed. Execution gates remain mandatory. Scientific result/acceptance: UNKNOWN. Role: method construction and curriculum comparison. Primary readout: paired validation LM loss P-minus-F at inherited common checkpoints; no cross-seed significance claim. Resource cap: one2xRTX5090spot smoke allocation, then two sequential8xRTX5090spot formal jobs, never16 GPUs. Baseline remains untouched. Actual2x5090 hardware access passed; full smoke and shared8GPU formal serialization remain distinct gates.

## 1. Terminology / Definitions

Valid prediction tokens count nonignored shifted targets once across all DP ranks and complete accumulation windows. The supplied binary stream is already shifted, so no second shift is allowed. Spectral head/middle/tail are engineering variance-coordinate ranges, not semantic coarse/fine categories. A document here is a physical packed-stream span delimited by observed151645, not a verified semantic family.

## 2. Anchor Alignment

A15_29 owns whether this fixed token curriculum helps relative to its full-information control. R12 on1031 supplies motivation only: its frozen Qwen feature/readout results did not establish a universal semantic hierarchy. No cached clustering picture is reused as token labels.

## 3. Tested Hypothesis

P may improve the validation-loss trajectory by delaying deeper constraints. F tests the rival that the same information is as useful or more useful from the beginning. Ordinary baseline references broader teacher effects but does not isolate curriculum by itself.

## 4. Rival Explanations

Hold teacher, tree, expert numbering, initialization, data/masks, optimizer and resources common so they cannot explain P/F differences. Independently inspect target instability, document concentration, collapse and routing-versus-probability mismatch. One seed and artificial hierarchy remain limits.

## 5. Data Construction And Provenance

Reuse dclm_pair_v1, frozen manifest8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d and tokenizer_qwen3_0p6b_base. Final V5 A/B/C5 sample262144/262144/16384 positions from the same first30B training view, never validation. Preserve each original2048input sequence, packing, causal context and target positions. Cap256 selected positions per document, disallow any context document in another calibration split. A/B retain seed103120 and exactV4fit positions; freshC5 seed103121 excludes all prior check-context documents. Actual selected contexts and hashes are in inputs/calibration_manifest_v5.json. V1–V4 failures and their original samples remain in the amendment ledger. Physical separation does not guarantee semantic near-duplicate separation. The tokenizer's default151643 is absent from the inspected training prefix; actual corpus marker151645 is used for calibration document identity only. Training attention/masks are not changed.

## 6. Learning Task And Permitted Supervision

Frozen exact teacher model_dense_33b uses native state at token033000000000, SHA256a0b21cb3b8c5217aa5638101ed60c28747edf474bd33ae62f91cda57952586cd. Every layer exports actual post-norm2 FFN input. No future text or target IDs enter teacher features. Teacher and student receive identical complete input IDs/context/mask; targets depend on context and position, not token ID lookup. Online teacher is frozen and does not generate text. No50B target cache is materialized.

## 7. Model / Architecture And Frozen Variants

Student exactly copies the corrected baseline's8layers,hidden1024,8independent1536SwiGLU experts/layer,top2,no shared expert,16Q/8KV/head128,QK RMSNorm,pre-norm,RoPE1e6,151936vocabulary and tied embedding/head. Total507988992=205933568shared+301989888experts+65536router. Load-free bias0.001*sign(global valid tokens*2/8-count), once per complete update, all ranks/all microbatches, used next update. Original softmax+bias selects top2; original selected probabilities renormalize mixture. Execute all selected assignments, no capacity drop. No auxiliary balance loss. Freeze bias for validation. Both groups reset original common random model,seed17,emptyAdam,zero bias/counters/cursor and mapped reference RNG; no Dense initialization and no baseline-endpoint continuation. Mapping2/8physical ranks to4reference RNG is explicit and identical acrossP/F; forward dropout is zero.

## 8. Training Objective And Optimization

Use teacher-to-student conditional KL chain as Anchor. Student supervision uses the same ambient-autocast linear router(stopgrad(hidden)) as the main route, followed by FP32 log-softmax/KL; all8pre-bias probabilities are used. LM path remains normal, all student parameters train throughout. Reduce each component by global valid targets and8layers; DDP gradient averaging is compensated byworld/global_count. Stable logsumexp avoids empty-parent division. Enable no KL2+KL4+KL8 repeated constraint. Sum of three conditional terms must numerically equal full8leafKL, including gradients. AdamW3e-4,betas(.9,.95),eps1e-8,matrixwd.1/normwd0,clip1,fused,FP32params/Adam+BF16autocast.1000update linear warmup thenconstant LR; actual completed-token/update correspondence matches baseline; no2B decay/end.

## 9. Conditions, Seeds, And Checkpoints

Lambda=.05*min(N/.5B,1),N=completed actual tokens BEFORE update. P middle=clip((N-5B)/5B,0,1),tail=clip((N-15B)/5B,0,1); F middle=tail=1. Thus P phases0–5,5–10,10–15,15–20,20–50B. All earlier terms remain enabled. Each target exactly50000000000,update safety ceiling190749; config,CLI and loop agree. No stop-step or virtual-clock flag in formal commands. Keep inherited exact milestones0,.5,1,3,5,10,13.000238080,15,17,...49,50B. Log crossings5/10/15/20B without slicing an extra optimizer update at20B, preserving baseline data masks and update count. Recover every1000completeupdates,keep last2 plus permanent milestones and common initial. Stage boundary20B is a crossing record, not an invented exact Dense checkpoint.

## 10. Primary Metric And Frozen Analysis Plan

Independent validation is the same first32sequences/65536targets, global token-weighted natural-log LM loss; no teacher loss or bias fitting on validation. Compare P-minus-F at matched reached checkpoints, retain trajectories and missing outcomes. The present authorization fixes implementation and runs; it does not preaccept a minimum scientific effect. Negative/zero/positive difference is directional within-seed description, with no cross-seed uncertainty claim. Data efficiency may later compare token exposure to prespecified common validation-loss thresholds; do not select thresholds using confirmation results.

## 11. Secondary Metrics And Guards

Record LM/total loss, raw/weighted head/middle/tail terms,lambda/gammas,valid tokens,updates,LR,throughput,teacher time,allocated/reserved memory,each layer's actual expert counts/bias/raw probabilities/entropy,teacher target entropy,raw probabilityL1/top1agreement,teacher mass under rawtop2 and bias-selectedtop2, and how often these selected sets differ. Raw probabilities and dispatch are distinct quantities. Fixed C contexts/positions/teacher targets support tomorrow's analysis.

## 12. Known Good / Known Bad / Known Confusing Cases

Good: identical q/p has zero KL; conditional terms sum full KL; zero lambda exactly preserves baseline LM gradients. Bad: changed tree hash or data cursor refuses resume; dropped assignments/count mismatch fail; near-empty parent/nonfinite state fail. Confusing: stable eigenspaces with unstable leaf probabilities are NOT accepted by subspace checks alone; entropy tuning alone cannot pass target qualification. Synthetic tests verify implementation only, never replace actual teacher targets.

## 13. Scientific Procedure And Stage Contracts

Freeze inputs/document split; verify exact teacher hash/load/causality; extract selected FFN positions; independently fit A/B; check C; run2GPU hardware/teacher parity/gradient/phase checks and both real restarts; then submit P first andFsecond with actual platform serialization proof, confirm both8cardrequests and50B configs accepted. Finish supervision after those accepted IDs/states. A resource/permission/correctness failure is reported, without changing hardware,randomizing targets,lowering budget or bypassing gates.

## 14. Algorithm, Output, And Provenance Contract

A-centered unbiased covariance, descending eigenvectors, initial bands[0,128),[128,512),[512,1024). If boundary relative gap<.001, search+/-8; move only to largest gap>=.005 and>=5x original, else retain and measure stability. One fixed overall RMS per band. All2center fits retain all positions with soft parent weights and deterministic weighted-median seeds. The finalV5solver uses exactlyone nearest-center reassignment and weighted centroid update at EVERY node, after weighted-median initialization. Rootseed is the first headPC; childseeds are fixed original-hidden-coordinate projections. This bounds centroid drift and is not claimed to optimize unrestricted kmeans. HistoricalV1–V4solvers are documented below. Binary temperature is calibrated solely onA to weighted conditional entropy.5ln2. IndependentBrefits its own center/covariance/scales/temperatures with same frozen boundaries. Tree-preserving B label alignment is chosen onA; C is untouched by fitting/alignment. Engineering gates, selected before extraction: mean subspace overlaps at least .70/.45/.65; CmeanleafJS<=.15nats; root argmaxagreement>=.80,leaf>=.50; eachleafmeanmass .005–.50 andeffectivepositions>=128; maxdocumentmass<=.15 with>=16supportdocuments; nodeconditionalentropywithin.01. These are engineering guards, not proof of semantic reliability. Failure retains diagnostics; repairs require documented sampling/scale/numerical reasons and a new version, not random labels or test-outcome tuning.

Checkpoint includes model/bias,Adam,scheduler,allrankRNG,counters,data/samplerposition andnextsampleIDs,source/configcontract,exactteacher/tree/calibrationreferences+hashes,curriculum coefficients for next update. Save only complete accumulation boundaries with atomic files/complete manifests. Loader refuses mismatched identities. TwoGPU restart is continuous4 versus2save/exit-allworkers/newtorchrun/resume2 for EACHgroup,comparing nextsamples,LR,bias,stage,counters,RNG and fullmodel/Adam/scheduler. Loss tolerancesatol/rtol1e-6; fullparameterstateatol1e-7/rtol1e-6. Additional CPU restart is only an engineering unit check, not a substitute. Formal entry resumes same run's last complete checkpoint, allowsone in-allocation retry; platform retry cap3, no fresh-job submission loop. A hard interruption may replay from last checkpoint; counters and logs reconcile to committed progress;50Btargetnever changes.

## 15. Success / Failure / Insufficient Evidence

This conversation succeeds operationally only with real target/smoke/restartPASS plus two real accepted/queued/running IDs, each8GPUrequest and50Btarget, under verified shared8GPUmaximum. Generated scripts,CPUtests or a submitted-but-failed qualification do not satisfy completion. Scientific support remains deferred to actual matched validation results.

## 16. What This Cannot Claim

No natural semantic hierarchy,adaptive student-convergence switch,seed robustness,zero teacher cost,complete target-training-distribution coverage from a small calibration panel,or 50Bcompletion on job acceptance. The teacher itself has33B prior training exposure. Subspace overlap,activation frequency,eigenvalue size andactivation amplitude remain different objects.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–G core design and execution scope are researcher-confirmed by this explicit request. Engineering implementation choices are delegated and recorded above, not claimed as empirically optimal. Source/config/calibration/target hashes are frozen before dependent stages; microbatch/accumulation may be chosen jointly forP/F by2GPU throughput with>=4GiB memory margin,globalbatchunchanged. Production configs freeze after selection and before formal submission. Actual hardware access is verified. All-layer targetPASS and GPU restartPASS gate formal submission; shared8GPU serialization is independently required before accepting both jobs. No resource or50Bscope relaxation is authorized. All outcomes retain original evidence.

[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_29_spectral_hierarchical_router_curriculum/15_29_spectral_hierarchical_router_curriculum_anchor.md) · [Focus](../../../../focus/focus_spectral_hierarchical_router_curriculum.md) · [Execution package](../../../../../../../../UNAVAILABLE.md) · [1031 analysis](../../../../../../../../UNAVAILABLE.md)

### Numerical repair R01-v2 (before any GPU/student training)

V1 passed all band subspace/entropy/occupancy/document checks but failed leaf target reproducibility on originalC: all8layers JS.230–.278 and leafargmax.282–.381, despite rootagreement.967–.998. Diagnostics are retained in targets/attempt_v1. Initializing weighted Lloyd by each band's first eigenvector is not invariant to a basis rotation inside a stable near-degenerate subspace. V2 keeps head initialization unchanged and initializes middle/tail splits by fixed original-hidden-coordinate axes0..5 projected into each band; child numbering uses that same physical direction. No random labels, loss-threshold changes or semantic labels are introduced. Rotation-invariance unit passes. A/B data and all gates remain unchanged; freshC2(seed103118,74documents) excludes all originalC/A/Bcontextdocuments. Its manifest is inputs/calibration_manifest_v2.json. RawV1data/records are preserved. CPU extraction is not GPUparity qualification.

### Numerical repair R01-v3 and resource correction

V2 also failed all8 leaf reproducibility gates (retained audit/offline_target_qualification_v2.json). A fixed-reference diagnostic still failed, so subspace rotation alone was insufficient. Free100iteration centroid refinement drifted strongly from fixed-coordinate weighted-median seeds. V3 retains independently fitted A/B means,bases,band scales and converged head; each middle/tail node performs exactlyone soft-parent-weighted nearest-center reassignment and centroid update from its fixed-coordinate seed, then freezes temperature at the original entropy target. This is a bounded centroid fit, not a claim of unrestricted kmeans optimality. Centers remain actual weighted sample estimates; no random target labels. The layer0 C2 pilot is explicitly developmental, not qualification. All original gates apply to fresh C3(seed103119,16384positions,70physicaldocuments), excluding every prior A/B/C1/C2contextdocument. No final validation data is used. Two initial CPU fit attempts include one native UCX crash, preserved in audit/target_fit_v3.log; the retry caps BLAS thread pools.

Actual2xRTX5090spot hardware access was verified by job om-t99qfhv3, actual2GPUs and existingtorch2.8/cu12.8 runtime. AEC2metadata lookup failure did not imply resource unavailability. This hardware-only job is not a student smoke. FormalP/F serial8GPU scheduling proof remains a separate required gate.

### Sampling repair R01-v4, before new target extraction

V3 passed7/8layers;layer7 meanleafJS.155495 andleafagreement.496643 failed the original gates. Do not round these toPASS. V4 preserves the exact V3 bounded child solver and all thresholds; independently sample A/B at262144positions each (1152/1174physicaldocuments), versus65536and289–296documents before. FreshC4 has16384positions/72documents and excludes all previous check-context documents. This tests finite-sample sensitivity with broader document support, not a threshold relaxation. Pre-extraction preparation_sources.json freezes code and inputs. The current local CPU environment hit native segfaults (retained logs); perform V4 teacher-only extraction and all tests within the actual authorized2GPU5090 allocation, using the already verified runtime. Calibration/runtime target replay replaces cross-device parity because this version's frozen reference is itself computed on5090. No student forward before V4all-layerPASS and post-fit source freeze.

### Numerical repair R01-v5, frozen before freshC5

V4passed all8leafJS/leafagreement/support/subspace/entropy checks, but layer5rootagreement.797058<.80. It remainsFAIL. Inspecting A/Bfit geometry without newcheckdata shows firstPCcosine.997773, but freefit root axes havecosine.879412(A)/.973216(B) to their initialPC. V5 therefore applies the SAME bounded refinement already used forchildren also to the root: weightedmedian seed, exactlyone nearest-center reassignment and weightedcentroid update. Rootseed remains firstheadPC; childseeds remain fixedoriginalcoordinates. This freezes one uniform solver at every node, not a looser threshold. A/Bsample and independent covariance/scales are reused exactly; no refitting onC4. FreshC5(seed103121,16384positions,72documents,27contexts) excludes every priorcheckcontextdocument as well as A/B. All original gates remain. The V4job was stopped after known qualification failure to prevent pointless repeated calibration; resume the same2GPUjob after this explicit one-time numerical amendment. No student trained onV4.

Actual execution correction: workspace wsImmutableJobEnabled rejected manual start of suspended om-qwhewj2p. Its stopped state was verified before submitting a uniquely named replacement2GPUqualification job forV5. No overlapping2GPUallocations. This is not a training-state recovery test; real process restart qualification remains mandatory. Platform automatic fault tolerance is separate (V4 showed one actual automatic retry) and is capped3. Manual ACPstart is not promised as a formal recovery mechanism.

### Actual partial submission under the unchanged resource cap

After all engineering gates passed, the first P-only8GPUjob om-867vcrpa was submitted within the original authorization; no FGPUjob is active. This safely advances the first authorized arm without claiming a verified two-job queue or full two-ID completion. F is withheld until an existing serial mechanism is verified or the researcher explicitly changes job format. The proposed one8GPUjob/PthenF alternative has no received approval. The50Btargets and scientific controls are unchanged.
