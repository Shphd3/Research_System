# Latest completion and reasoning audit: both training arms complete (2026-10-07T01:33:37.835761+00:00)

[Summary](summary.md) owns the current conclusion. This supersedes the previous A-running snapshot; retain all dated history below. [Pre-update snapshots](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/canonical_before).

## Completion and conformance

A pt-txeitsor/H4 Reserved and B pt-3u6bcqbq/RTX 8 Spot both SUCCEEDED, supervisors COMPLETED / child exit 0. Completion timestamps UTC 2026-10-06T21:47:33 and 13:10:33 respectively. Both completed 7629 updates / 1999896576 targets / 100%. Platform+completion+supervision+durable pod terminal+full endpoint manifest agree: [A platform](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/A_platform.json), [B platform](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/B_platform.json), [A pod](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/A/pod_completion_evidence.json), [B pod](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/B/pod_completion_evidence.json). Endpoint state and 4/8-rank RNG files exist with matching declared sizes; large payload checksums NOT recomputed. Common weight checkpoints: 0/64/1024/3814/7629.

[Source lock](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/source_lock_verification.json): 68 files PASS / SHA 7faa926ec24d2664a3cc0f2ad66978382c363ac42cafc974a84ac1fd458821aa. No changes to trainer/config/Protocol/data. inspect_completed_pair.py adapts the prior inspector's completion checks and plot caption; earlier source/plots preserved. All records 1..7629 contiguous/finite/262144 targets per update, weighted = .01 × raw, error<1e-7,total sum error<1e-5, canonical config hashes valid. No dropped rows/NUL/ignored incomplete tail. Matched batch/exposure does not remove hardware confounding.

## Intervention and matched results

This section asks how one changed backward edge affects the complete training trajectory. Identical forward values at a common state exclude an initial input-value intervention. Learned parameters and assignments can diverge, leaving expert exposure and hardware as rival explanations. The router is a trained weight-mapping matrix and experts are trained networks reading h; the shared expert always contributes. None is a frozen candidate increment.

A gradient returned to activation r is not a direct optimizer update of r. It changes upstream parameter gradients; AdamW changes parameters and may thereby change r on the next forward. Training CE describes fit, sealed-document CE tests generalization, and load-preserving route permutations test functional assignment dependence. The latter two have no results yet.

r is attention output before residual addition; h is the normalized post-residual expert input. A retains LM gate→r feedback; B cuts only this edge; both experts / shared expert receive live h. Router W and other backbone paths train. Common auxiliary loss uses W stop_gradient(r) in both arms. Same-state/input forward formulas agree, learned states need not. This is neither a frozen router nor balancing-on/off.

| Final 64-update mean | A: live LM gate feedback | B: detached LM gate input | B−A |
| --- | --- | --- | --- |
| LM CE, nat/valid target | 4.109270 | 4.123641 | +0.014371 |
| Weighted balancing | 0.013589 | 0.012073 | −0.001516 |
| Total training objective | 4.122859 | 4.135714 | +0.012855 |

The final update alone has CE A 4.091892 / B 4.106052 (B−A +.014160). Trailing 32/128/256-update differences are +.014477 / +.014643 / +.014735; overlapping windows are not replications. [Milestone descriptions](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/milestone_training_description.json): at 268435456 targets the difference is +.007740, at 999817216 it is +.011823, at 1999896576 it is +.014371 (trailing 64-update training-batch means, not heldout checkpoint CE). Mean layerwise effective expert counts from load entropy in the last 64 updates are A 7.034546 / B 7.523360; these describe allocation, not semantic expert number. All health guard failure flags are false; latest layer streak maxima are 0/no globally unused experts. The original zero-aux failure is separate, cannot establish balancing causality.

## Figure and evidence lineage

![Completed pair comparison](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/loss_comparison.png)

The x-axis is cumulative valid targets (billions); upper left: LM CE, upper right: matched B−A, lower left: weighted auxiliary loss, lower right: total objective. Faint raw values plus a common trailing 64-update mean (16777216 targets); dashed vertical warmup marker. Positive B−A means lower A training CE. The recorded inspection viewed the complete PNG: readable panels/axes/legend/caption, no cropping; PDF saved. Pure training telemetry is not independent TEST/function/geometry evidence.

| Fact / derived claim | Raw → computation | Eligibility |
| --- | --- | --- |
| Both engineering completion | platform+supervision+completion+pod+full manifest/weights | Verified engineering, not scientific closure |
| A lower final 64-update training CE by .014371 | metrics snapshots → schema/targets → aligned CSV → window mean | BOUNDED single trajectory / post-hoc / hardware confounded |
| B lower balancing cost | same-window auxiliary mean | Load proxy, not specialization |
| Figure/statistics | inspect_completed_pair.py →JSON/CSV/PNG/PDF | Contract plus producer/source/output hashes |
| Primary TEST/function/geometry | Unexecuted | NOT_RUN |

[Comparison](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/comparison.json), [aligned table](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/aligned_updates.csv), [figure contract](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/figure_contract.json), [provenance](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261007T013337Z/figure_provenance.json). Raw metrics / scalar CSV / resolved config / completion / manifest / pod proof under A/B. Batch CE is evaluated before its update and logged at the completed-update coordinate, not independent CE at the final checkpoint.

## Reasoning audit (AI analysis; researcher judgment Unknown)

Observation: the same budget was completed; A has slightly better training prediction, while B has more uniform allocation. Purpose: whether allowing route-choice prediction error to shape upstream representation improves predictive/functional utility.

Candidate explanation: task gating feedback jointly adaptsrepresentation/routing. Local gradient qualification confirms the changed backward edge; the bridges from changed gradients to useful representations and then independent prediction remain empirically untested. The current curve only measures fitting.

Rivals: different expert data exposure / gradient scale / Adam preconditioning and completely confounded H100/RTX 5090 can produce the gap without better semantic division. A training advantage may not transfer to new documents. More balance with higher CE does not prove concentration causes benefit.

Allowed claim: this single balanced paired trajectory has lower A training CE / lower B balancing cost. Disallowed: universal algorithm superiority, an identified representation mechanism, useful semantic experts or adoption/closure. A training gap > .01 cannot satisfy registered TEST CI / function rules.

AI suggestion for the next minimal check: same independent registered panel at both endpoints. Retained advantage supports bounded generalization; disappearance/reversal weakens the training-to-generalization bridge; wide interval is INSUFFICIENT. A mechanism claim needs load-preserving route-bundle intervention and hardware control. None has been executed; explanation cannot substitute for evidence.

## Complete current round

Question/hypothesis: finite-budget LM feedback utility, bidirectional. Setup/controls: A3 common balancing / same initialization / AdamW, LM edge intervention, hardware rival. Data: frozen DCLM order/262144 targets per update/7629 updates. Confirmation: original 1024-documentFIT/DEV/DIAG/TEST panel unchanged, unaccessed this round. Result: both training arms complete, matched training comparison; primary TEST / function NOT_RUN. Insight/boundary/next: predictive fit and balancing are distinct; researcher mechanism / adoption Unknown; AI suggested endpoint independent assessment is unlaunched. Both supervisors ended normally; no new GPU job/resubmission/commit/push.

Following dated records remain intact historical evidence; do not reuse their status as current completion.

# Current progress and loss comparison: B complete, A running (2026-10-06T13:31:44.223681+00:00)

[Current Summary](summary.md) is the conclusion entry. This is the latest factual record of rrc_1006_balanced_r3; preceding dated records below are historical. [Pre-update canonical snapshots](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/canonical_before).

## Objects, intervention and contract

The Anchor question remains finite-budget predictive/functional utility of direct LM gate feedback. r is pre-residual Attention output; h is full post-residual normalized expert input. A routes withW r; B withW stop_gradient(r). Both feed live full h to experts. Router weights and all other backbone/expert paths continue training. Forward values are identical at the same state/input; learned states can diverge.

Current Protocol A3 adds common CE+0.01×router_aux. For each1024-position sequence/layer, top2 slot fraction f_i=count_i/(2T), mean softmax probability pbar_i, aux=8Σ_i f_i pbar_i; average12layers and256global sequences (uniform baseline1). Both auxiliary softmax branches useW stop_gradient(r), retainingW gradients and removing aux-to-backbone feedback. Thus the treatment still changes only LM gate feedback. Shared init/seed1005/data/order/Adam/global batch are preserved; hardware is A4H100/B8RTX5090.

## Conformance, completion and eligibility

[68 locked files PASS](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/source_lock_verification.json); resolved config canonical compact JSON hashes match training declarations. All4173/7629records are contiguous, finite,262144targets/update; weighted aux=.01×raw (error<1e-7), total=LM+weighted aux (error<1e-5). Pair/data/initial-state identities remain as frozen. No training/config edits.

A platform/supervisorRUNNING at4173updates/1093926912targets(54.699%); B platformSUCCEEDED/supervisorCOMPLETED,7629updates/1999896576targets(100%). [A platform](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/A_platform.json), [B platform](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B_platform.json). B platform completion13:10:33UTC; completion JSON, pod training_complete and supervisor exit0 agree: [pod evidence](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/pod_completion_evidence.json), [terminal excerpt](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/pod_terminal_excerpt.txt), [completion](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/completion.json). B endpoint full state and8rankRNG manifest complete; latest A full recovery manifeststep4151. All listed files exist with declared sizes; large checkpoint hashes were NOT recomputed. [B endpoint manifest](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/B/latest_checkpoint_manifest.json). A recent supervisor ETA26808.69seconds(7.45hours) is provisional.

Both recorded health guards have zero failures; latest fixed-layer collapse streak maxima0 and every global-batch layer has zero unused routed experts. This describes load, not semantic specialization. Registered TEST/bootstrap/function endpoints remainNOT_RUN; advanced entries can remainPREPARED_NOT_IMPLEMENTED. Windows are post-hoc and BOUNDED; steps/windows/layers are not independent replicates. Single seed and complete algorithm–hardware/rank confounding prevent a hardware-independent treatment claim.

## Matched results

Common horizon4173updates/1093926912targets. Trailing64updates4110–4173 (16777216targets):

| Metric | A | B | B−A |
| --- | --- | --- | --- |
| LM CE, nat/valid target | 4.243208 | 4.256216 | +0.013008 |
| Weighted balancing | 0.013676 | 0.012065 | −0.001611 |
| Total objective | 4.256884 | 4.268281 | +0.011397 |
| Mean layer effective routed experts | 6.971997 | 7.419154 | +0.447158 |

Instantaneousstep4173CE A4.244847/B4.258299. Trailing32/128/256CE differences+.013271/+.012634/+.012051 have the same current tail direction; overlapping windows are not repetitions. B final trailing64CE4.123641 is at a later budget and is not paired with current A. Raw telemetry is each processed batch's pre-update CE with the completed-update target coordinate, not heldout checkpoint loss.

## Figure and lineage

![Balanced pair losses](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/loss_comparison.png)

Linear x-axis is cumulative valid prediction targets in billions. Upper-left pureLMCE; upper-right matchedB−A; lower-left weightedbalancing; lower-right totalobjective. Faint lines retain raw values, solid lines are trailing64-update means. Warmup at33554432targets; dotted common horizon1093926912targets. Shaded right region/dashed B is B-only exposure and excluded from the paired difference. PositiveB−A means lowerAtrainingCE. Complete rendered PNG was inspected: all panels/axes/legend/caption legible, no cropping. PDF also saved. Neither geometry/function nor generalization follows from this figure.

| Observation / derived statistic | Raw → computation | Eligibility / limitation |
| --- | --- | --- |
| Bcomplete/Aprogress | platform+supervision+completion+pod+manifest → comparison | Engineering completion only |
| A lower matched trailing64CE by.013008 | rawmetrics snapshots → schema/token/component checks → aligned_updates.csv → common window mean | BOUNDED training/single seed/hardware confounded |
| B lower weighted balancing by.001611 | same rawrecords → common window mean | Auxiliary/load property only |
| Figure | snapshots/scalar CSV → inspect_balanced_pair.py → PNG/PDF | Explicit contract and source/producer/output hashes |

[comparison](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/comparison.json), [4173row aligned table](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/aligned_updates.csv), [figure contract](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/figure_contract.json), [figure provenance](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/analysis/progress_20261006T133144Z/figure_provenance.json). Raw snapshots/scalar CSV/config/manifest/supervisor receipts are underA/B in this evidence directory. Source lockSHA7faa926ec24d2664a3cc0f2ad66978382c363ac42cafc974a84ac1fd458821aa remains unchanged. The first local inspector attempt rejected a pretty-printed raw config hash against the canonical trainer hash; parser corrected and rerun, training files untouched. Incomplete attempt is explicitly labeled non-result.

## Round, claim and next action

Question/hypothesis: finite-budget LM-feedback utility under common balancing; help/harm remain open. Setup/controls: frozenA3, LM gate-to-r intervention, hardware rival retained. Data: identical frozenDCLMview/order/globalbatch. Confirmation: original sealed panel unchanged, TEST/functionNOT_RUN. Result: Btrainingcomplete/Aincomplete, matchedtrainingCE and balance favor different arms. Insight/boundary: load balance cannot substitute for predictive utility, and trainingCE does not establish mechanism/adoption. Next execution: existingAmanagedsupervisor continues, Bendednormally; no resubmission/restart/newGPUanalysis. Researcher mechanism/adoption/closureUnknown. No commit/push.

The following dated records preserve startup, original zero-aux failure and1005submission history; do not mix their conditions or status with this snapshot.

## New formal balanced pair: actual startup verified

Snapshot 2026-10-06T03:30:26.518923+00:00. A=pt-txeitsor, world4, updates73, valid targets19136512; B=pt-3u6bcqbq, world8, updates19, valid targets4980736. Both platform RUNNING, actual startup/finite tags/counts PASS, both managed supervisors active. Each new create called once; max_retries=0. New H4/G2 Smokes pt-96b4ccz1/pt-xdfrqwsi acceptance PASS and platform SUCCEEDED; cross-hardware acceptance PASS. Source lock SHA7faa926ec24d2664a3cc0f2ad66978382c363ac42cafc974a84ac1fd458821aa. All five local qualifications PASS.

[Current Summary](summary.md); [analysis notes](analysis_notes_20261006.md); [actual startup snapshot](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/receipts/startup_pair_20261006.json); [new pair freeze](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/receipts/formal_pair_freeze.json); [read-only old-source preservation](/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced/receipts/old_execution_preservation.json). Logs/checkpoints/metrics remain below /data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced; per-run supervision.json is refreshed by the ACP supervisor. No TEST/function/post-analysis executed. Original zero-aux failure remains separate and primary evidence insufficient. Advanced entries remain pending implementation. No commit/push/other-project changes.

The earlier staged entry immediately below is historical, superseded by this actual startup observation. Whole-pod termination stops embedded monitoring; it has no external notification or automatic resubmission capability.

## Current A3 balanced retraining

New paired condition registered; local gradient/auxiliary, checkpoint/resume, terminal guard persistence and supervisor classification checks PASS. Newly created Smoke A4H100 pt-96b4ccz1; the RTX2 Smoke receipt is in the new root below. Formal balanced trajectories NOT_SUBMITTED until both new hardware qualifications PASS. Prior zero-aux failure remains separate. Monitoring is expressly requested.

Execution root: `/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced`. [Protocol A3](protocol.md); [analysis notes](analysis_notes_20261006.md).

# Detailed: router_representation_gradient_feedback

## Current inspection: formal interrupted runs,2026-10-06

Snapshot:2026-10-06T02:29:47.761936+00:00;requested status and training comparison. BothFAILED:pt-9egkfirg ended2026-10-05T11:08:06Z;pt-86fsmog5 ended12:12:55Z. Last durable update274/71827456targets=3.59% of registered7629/1999896576. No completion.json or endpoint milestone. Latest complete recovery manifests A265/69468160targets and B157/41156608;payload checksums were not rehashed in this status inspection. Common weights0/64 only;requested1024/3814/7629missing. Source receipts:[platform snapshots](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/status_20261006);durable [A log](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/acp_receipts/pod/rrc-1005-full-coupled-v1-20261005T103331Z.log) and [B log](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/acp_receipts/pod/rrc-1005-full-router-input-detached-v1-20261005T115134Z.log) explicitly showLOAD_COLLAPSE. Formal4/8rank runs now observed;older unobserved status remains historical.

Evidence lineage:[comparison.json](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/comparison.json) records source hashes and calculations;[aligned updates](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/aligned_updates.csv) contains all274 token-aligned rows. Last CE A6.321735/B6.322187nat,target difference+.000452;posthoc last32 means6.484663/6.483023,difference−.001640;last64 means6.576622/6.576355,difference−.000267. Windows are descriptive,not independent replicates,no CI or primary TEST threshold applied. Losses remainfinite and decline;no LM health guard failure in274logged steps.

Global load fractions are aggregated over all microbatches/ranks before zero-load/entropy metrics. Last mean effective experts A2.0166/B2.1191;mean zero-load experts4.8333/3.0833. A layers3–10(8/12) have6/8routed experts unused;B layers7–10(4/12). IDs locate within-model behavior,not cross-model semantic matching;shared expert remains active.

[guard source](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/src/coupling/train.py:1486) updates optimizer/counters before the load guard and before metrics publication. Any-layer streak starts148,continues127logged steps through274,and exception indicates128on the next update;275execution is source-inferred,not a saved loss/state. One counter tracksANY-layer violation,not per-layer streaks;no fixed layer violates for all127logged updates. If frozen wording requires one fixed layer violating128times,this implementation has not established it. This aggregation caveat does not erase observed concentration. Guard exception bypasses terminal checkpoint/completion writing;do not assume last274/275weights recoverable.

![Measured training comparison](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/training_comparison.png)

Read:xvalidtargetsM;topoverlappingtrainCE;middle small sign-changingB−A;bottomterminalsix-deadlayer count8A/4B. Dashed line=warmup128;shade=any-layer streak148–274. Producer inspect_training_20261006.py;[aligned updates](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/aligned_updates.csv);[figure provenance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/analysis/20261006_training_comparison/figure_provenance.json). Render inspected,no clipping. Maximum claim:descriptive interrupted training only,not TEST or mechanism.

Observed loop-average speeds including checkpoints A37029/B67932targets/s;last64median44222/108974;peakreserved10.047/10.031GiB/GPU. Hardware,rank count and sparsity differ,so these are not causal algorithm speedups. Primary endpointmissing;comparisonINSUFFICIENT;human utility/mechanism/adoptionUnknown. No TEST/function analysis,new submission,repair,guard relaxation orresume. Researcher next decision:how to obtain an eligible comparison,unconfirmed. Original delivery manifest is a1005historical identity snapshot;dated source identities live incomparison.json/current receipts.

## Original1005 qualification and submission record,preserved verbatim

Updated: 2026-10-05T10:40:26.520517+00:00. [Summary](summary.md); [Anchor](../../problem_anchors/router_representation_gradient_feedback/anchor.md); [Protocol R1 + A1/A2](protocol.md); [analysis Protocol](analysis_protocol.md).

## 0. Quick recap and eligibility

Question: net effect of direct router feedback under a finite trajectory. Both directional hypotheses remain open. Direct result: two hardware Smokes and cross checks PASS; formal A/B create calls each returned one ID. Qualification evidence is ELIGIBLE for wiring, production shape and short-window restoration only. Endpoint analysis NOT_RUN; formal runtime NOT_OBSERVED by user instruction. Researcher mechanism/adoption judgment Unknown. No question closure or final scientific report.

## 1. Objects and computation

| Object | Concrete meaning | Boundary |
| --- | --- | --- |
| reference r | Attention output before residual addition | Different from expert input |
| expert input h | normalized hidden state after Attention residual addition | Remains live in both arms |
| A coupled | gate receives live r | router task gradient can return to r |
| B router_input_detached | gate receives r.detach() | only this backward edge is removed; router, experts, gate weights and residual remain trainable |
| valid targets | nonignored next-token prediction labels | global sum advances only after a successful optimizer update |
| hardware comparison | same-state A/B on each hardware | formal algorithm and hardware are fully confounded |

## 2. Anchor and decision point

The unique Anchor owns scientific design; Focus holds the researcher-owned retain/remove/further-verify decision. Execution approval is the direct [researcher request](../../../handoff/researcher_request_cn.md), normalized in Protocol. Approval and engineering PASS do not establish benefit, mechanism or adoption.

## 3. Freeze, conformance and deviations

| Registered item | Expected | Actual / evidence | Eligibility |
| --- | --- | --- | --- |
| Intervention | only router-input edge, all12 layers; aux=0 | local_gradient_contract.json and diagnostics_*.pt PASS | wiring only |
| Model/data/init | same model, view, ordered global batch and saved state | source_lock.sha256 and resolved Smoke contracts | same-state input checks PASS |
| Production shape | 262144 targets/update; H4/G2 qualified | 2 updates and external restart per arm on both | short-window qualified |
| Formal resources | H4 reserved A; G8 spot B | direct-return expanded tuples | requested; actual runtime NOT_OBSERVED |
| Schedule | formal warmup128,total7629 | Smoke deliberately warmup1,total2 | engineering schedule, not formal trajectory |
| A1 | true FP64 identity reference and isolated ABI/runtime fixes | original mixed-FP64 strict failures retained | no production tolerance relaxation |
| A2 | repair diagnostic endpoint index only | v1 bothFAILED before training; int64 index check PASS;v2 bothSUCCEEDED | v1 excluded from positive qualification |
| Endpoint/uncertainty | one TEST endpoint, whole-doc bootstrap | panel locked before loss exposure; analysis not run | primary result absent |
| Monitoring | stop after formal direct return | no formal runtime read; no background monitor/retry | deliberate observation boundary |

R2 source-lock SHA256: `9e5d2d288c7c9a12dc23f9dba6d60631ec19ceaafa7ebb5a0c602f11d398bf9e`;56 locked files. Formal pair freeze is [freeze receipt](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/formal_pair_freeze.json). No post-hoc scientific analysis or test-based endpoint selection.

## 4. Actual setup versus registered formal trajectory

Smoke model:342097408 parameters,12layers,hidden512,4Attention/2KV heads,head_dim128,RoPE theta1000000,vocab151936,tied embedding,8routed experts/top2,width1536,one shared expert/layer,no dropout. Top2 softmax gate weights are not renormalized;temperature1. All parameters trainable. EMA/de-common/SAE/spectral penalties disabled;raw auxiliary balance statistic logged, weighted auxiliary objective0.

Common fresh CPU random seed1005 state;file SHA256 `a232a4fc0a7afad23cf1f410089239ef125edcefc9760942a5365c5825d3abcd`;tensor SHA256 `d835c0afd8ca57302506c5f23009268c2e4173b75b79361a32a9a39029c72e2c`. No pretrained or prior experiment weights.

Training view `/data/250010109/training_data_views/dclm_pair_v1/train`;manifest SHA256 `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`. Path/size inventory and sampled token bounds checked;not full1.2TB content hashing. GlobalUpdateSampler reads consecutive256 sequences/update and partitions them across ranks;no reshuffle or epoch wrap. Tokenizer identity is frozen in inputs/analysis_manifest.json. Independent raw heldout shard02 SHA256 `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`;panel1024unique docs,FIT128/DEV128/DIAG128/TEST640,panelSHA256 `350d883e439ac62e6303e6d00b86a7e882ce7b0454fe3402a405d89ae51bb05a`. No model loss exposure during selection;whole-corpus semantic dedup unverified.

LM next-token CE uses globally valid-target-weighted reduction;chunk256. AdamW1e-4,betas(.9,.95),eps1e-8,WD.01,clip1,fused=false. BF16 autocast with FP32 parameters/Adam,SDPA,TF32 off,no activation checkpoint. Both observed runtimes=torch2.8.0+cu128/CUDA12.8/HF4.53.3/cuDNN91002/NCCL2.27.3;isolated mounted layer,base environment untouched.

Sequence1024,microbatch1. H4 accumulation64,G2 accumulation128,formalG8 accumulation32. All give262144 valid targets/update. Smoke ran2updates/524288targets/arm,external process checkpoint continuation at1;only step2 uses nonzero LR under the registered1-step warmup. Formal plans7629updates/1999896576targets,warmup128steps=33554432targets,cosine to endpoint. Formal completion and checkpoint existence are not inspected.

Registered weights at0/64/1024/3814/7629steps;tokens0/16777216/268435456/999817216/1999896576. Rolling full optimizer/RNG checkpoints every10min or>=0.2B targets,whichever first,latest2 retained;terminal complete state. Cap100GiB/run. Smoke observed10.197GiB/run after retention. Formal payload estimate roughly18–25GiB/arm before future activation caches;cap100GiB/arm is not an exact forecast. Source/config/scripts are independent copies; [source reuse audit](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/reuse_sources.json) and [read audit](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/source_read_audit.json) distinguish reused data/DDP/checkpoint/runtime from adapted detach/sampler/telemetry/guards and rejected old weights/regularization.

## 5. Metrics and decision rules

Engineering gates: full same-hardware same-state forward/routing parity; last-layer router/expert gradients and reference removed path;B router update;tiny true-FP64 full-network telescoping;DDP/accumulation;exact external resume;finite required TensorBoard tags;two correctly counted steps;peak reserved<78GiBH/<30GiBG. Cross initial relative-logit-RMS<=.02 and CE difference<=.02nat. Gradients/routes/short updates are reported, not falsely thresholded as exact hardware parity.

Scientific primary metric is endpoint TEST summed negative log probability/valid targets,B-minus-A,nat/token. Whole-doc paired5000-bootstrap percentile95% CI,seed1005;AI proposed practical delta.01nat,not human adoption rule. [Analysis Protocol](analysis_protocol.md) owns all6post-test families and support/opposition/INSUFFICIENT branches. Primary analysis NOT_RUN;single seed and hardware confounding remain.

## 6. Evidence lineage

| Bounded statement | Source / producer | Computation and observed value | Eligibility / limit |
| --- | --- | --- | --- |
| intervention wiring | [local gradient](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/local_gradient_contract.json);tests/gradient_contract.py | trueFP64 residuals7.446e-17/4.054e-17;negative expert-detach control fails as expected | tiny mathematical check,not trajectory benefit |
| CPU external resume/DDP | [external resume](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/local_external_resume.json);tests/external_resume.py | same-topology restored model/Adam/schedule exact;1vs2rank accumulation parity;64tokens/2steps | CPU tiny only |
| full GPU same-state paths | [H100 diagnostic](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/diagnostics_h100.json);[5090 diagnostic](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/diagnostics_5090.json) | full logits/all routes/gates same;last-layer paths and B updatePASS | other-layer parameter differences need full-network decomposition |
| production batch/restart/telemetry | [H100 acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/smoke_h100_acceptance.json);[RTX5090 acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/smoke_5090_acceptance.json);scripts/verify_smoke.py | each hardware/arm2updates,524288targets,one external resume segment | one seed,two updates;no long-run stability |
| cross-hardware initial read | [cross-hardware acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/cross_hardware_acceptance.json);diagnostics_*.pt -> compare_hardware.py | relative RMS.008265;CEabs.0002336502nat;route slot mismatch.003051758;gradient sample relativeL2.02864A/.02868B | initial gatesPASS;not hardware effect zero |
| short-window fixed training sample | [cross-hardware acceptance](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/cross_hardware_acceptance.json);short_window_*.pt | H B−A=−.0001573563nat;G B−A=.0003747940nat;cross CE G−H A=−.0003385544/B=.0001935959 | descriptive single training sample;signs differ;not TEST science |
| formal create calls | [A direct return](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/submissions/full_coupled/direct_return.json);[B direct return](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/submissions/full_router_input_detached/direct_return.json);submit.py | rc0,oneIDeach:pt-9egkfirg/pt-86fsmog5 | submission result only;runtimeNOT_OBSERVED |
| future analysis readiness | [entry manifest](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/analysis_entrypoints.json);[synthetic statistics test](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/analysis_stats_qualification.json) | CE/statistics runnable;gradient/capture/functional/finite-update PREPARED_NOT_IMPLEMENTED | no trained-model post-test result |

## 7. Measured Smoke memory and throughput

| Hardware / arm | Ranks | Updates / valid targets | Peak allocated / reserved GiB per GPU | valid targets/s | Qualification |
| --- | --- | --- | --- | --- | --- |
| h100 / coupled | 4 | 2 / 524,288 | 9.211 / 9.686 | 15996.3 | PASS |
| h100 / router_input_detached | 4 | 2 / 524,288 | 9.211 / 9.686 | 16140.2 | PASS |
| 5090 / coupled | 2 | 2 / 524,288 | 9.165 / 9.670 | 19578.1 | PASS |
| 5090 / router_input_detached | 2 | 2 / 524,288 | 9.165 / 9.670 | 19968.8 | PASS |

These are observed short-window peaks and post-resume training-loop speeds,not long-run average. A compute-only extrapolation is34.73h;B ideal2-to8GPU extrapolation6.95h. Queue time,checkpoint overhead and spot interruptions are excluded;8GPU actual throughput/topology unverified. No execution deadline is promised.

## 9. Failure decomposition

v1 H=pt-0bhf38z4 andG=pt-oz88x40i:both FAILED before any GPU training loop,diagnostic FP32 linspace rounded embedding endpoint77791231 to77791232. Integer arithmetic fixes the index;dimension boundary testPASS;A2 preserves old source lock/logs and tolerances. Local ABI,cuDNN-path and nominal mixed-FP64 strict failures stay in receipts,not relabelled PASS. No scientific hypothesis was rejected by these implementation failures.

## 10. Append-only execution checkpoints

The original checkpoint entries below are historical observations,not current runtime claims.

Registered R1; result_state=NOT_RUN. Execution records and amendments follow below. Authority: handoff/researcher_request_cn.md; code/raw root /data/250010109/MoE_Router/experiments/20261005_router_representation_coupling.


## Execution checkpoint — 2026-10-05, Smoke create calls returned

- Purpose: qualify only the router-reference backward edge before the two finite trajectories.
- Hypothesis: benefit/harm both open; scientific result NOT RUN.
- Setup: one342,097,408-parameter12-layer8E/top2/shared-expert model, seed1005 common saved random state; reference is pre-residual Attention output, expert input is separate normalized post-residual hidden state. All-layer detach in B only. Final target1,999,896,576targets/7629updates,global262144batch.
- Data: training path/size frozen-view inventory verified; no full1.2TB content hash. Separate raw-shard02 source hash checked,1024unique documents frozen128FIT/128DEV/128DIAG/640TEST. No model losses exposed during panel selection.
- Confirmation: one main TEST endpoint. Early checkpoints descriptive; bootstrap whole docs does not estimate seed uncertainty.
- Engineering results: local isolated gradients and true-FP64 full-network edge telescoping PASS; external-process checkpoint/model+optimizer+scheduler exact restoration PASS;1-vs2rank accumulation/model tolerance PASS. Source logs under execution receipts. Preserve initial FlashAttention ABI, torchvision ABI, cuDNN precedence, test indexing/deepcopy and mixed-precision1e-10 residual failures; repaired locally, no old source/base environment edits. Original native mixed-FP64 failure is not relabelledPASS.
- Submitted Smoke: H=pt-0bhf38z4 (4H100 reserved), G=pt-oz88x40i (2RTX5090 spot), each direct create returned an ID. Both observedSTARTING at09:56UTC; actual GPU/qualification not yet verified. Formal jobs NOT_SUBMITTED. Owner currentthread only.
- Post-test readiness: document CE and bootstrap/geometry-statistic scripts runnable. Gradient/capture/functional/finite-update entries PREPARED_NOT_IMPLEMENTED with exact input/output and preregistered procedures; this turn does not perform or submit later expensive analysis.
- Insight/boundary/next action: path checks certify intervention wiring only. Observe these existing Smokes; both auditedPASS plus cross-hardware check required before full creates. Formal submit once each, save direct returns, immediately stop polling. No mechanism/adoption decision inferred.

Evidence root: /data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/receipts/; source lock docs/source_lock.sha256; submission direct_return.json perstage.


## Smoke revision A2 — 2026-10-05T10:10:50.492643+00:00

Both v1 Smokes reached FAILED before any GPU training loop. H100 pt-0bhf38z4 completed10:01:39UTC; RTX5090 pt-oz88x40i completed10:03:56UTC. Diagnostic gradient fingerprint FP32 endpoint indexing overflowed the embedding vector; integer index boundary check PASS. A2 changes only diagnostic index arithmetic and explicit Smoke retry bookkeeping, no algorithm/tolerance change. Previous source_lock_v1.sha256 and pod logs retained. Retry creates returned IDs: 4H100 pt-eemr6vdt;2RTX5090 pt-z63ayg30. Formal runs NOT_SUBMITTED; no scientific result. Evidence: receipts/diagnostic_index_repair_check.json, smoke_*_v1_terminal_raw.json, submissions/smoke_*_v2/direct_return.json and docs/freeze_r2.json under execution root.


## 11. Interpretation and claim boundary

Observed: qualification passed and create calls returnedIDs. Derived: short-window compute ETA and cross-hardware differences. Scientific interpretation/adoption:Unknown. Can claim the registered intervention is wired and short-window4H100/2RTX5090 batches/restoration qualify. Cannot claim benefit,semantic specialization,causal long-term mechanism,completed formal training,zero hardware effect or actual8rank qualification.

## 13. Researcher-owned next decision and operational stop

One next scientific decision: retain/remove/further verify direct feedback after the bounded endpoint tests;human judgmentUnknown. This authorized turn is complete at qualified double submission plus prepared post-tests. No current formal polling,background monitor,additional seed/arm or automatic retry. A later explicit status request must inspect existing jobIDs/receipts;no resubmission. Later post-tests use saved checkpoints under their frozen Protocol;this turn does not run them.

## 14. Artifact manifest

[machine manifest](/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling/docs/delivery_artifact_manifest.json) records small source/receipt hashes and training-input identities. Raw checkpoints remain in the execution root;per-checkpoint manifest/checksums own payload integrity. Its formal entries cover direct-create receipts only,not unseen runtime artifacts.

## 15. Entry points

Code/config/raw root: `/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling`. Launch scripts: `scripts/run_smoke.sh`, `scripts/launch_train.sh`;formal configs: `configs/formal_coupled.json`, `configs/formal_router_input_detached.json`. All submission/failure receipts: `receipts/submissions/`;durable Smoke pod logs: `acp_receipts/pod/rrc-1005-smoke-*-v[12]-*.log`. Post-test input/readiness: `inputs/analysis_manifest.json`, `docs/analysis_entrypoints.json`;future outputs `analysis/`. No decision-bearing figure is needed for these nonvisual qualification results.
