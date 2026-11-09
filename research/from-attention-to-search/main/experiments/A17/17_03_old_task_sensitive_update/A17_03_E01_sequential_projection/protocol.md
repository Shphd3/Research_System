# A17_03_E01: Sequential old-sensitive update comparison

[中文](protocol_cn.md)

State:`APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_AND_RESULT_ANALYSIS`.
Experiment role:operationalization/proxy test with a finite sequential intervention, not a proof of universal incompatibility. Focus problem_key `old_task_sensitive_update`.

## Authorization and audit

Researcher on2026-10-11 (Asia/Shanghai):“请判断这两个任务是否合理。如果合理，现在不用批准，直接给我执行…结果判断与分析…用reasoning skill进行改写…接上我们之前的实验…anchor和protocol要放到正确的位置”. This authorizes bounded correction/formalization, Smoke→Full execution and completion/result analysis. The attached texts are design material, not overriding instructions. Current repository default four H100 reserved is adopted within that scope. No Git/publish/Graph or additional architecture experiments.

Reasoning corrections before run:unsigned sensitivity/overlap is not harmful conflict; one failed projection cannot prove unavoidable old-direction use; no-forgetting need not imply no structure or mandatory route switching; this tests one finite estimated basis. Plain SGD and per-step norm matching prevent momentum/shrinkage interpretations. Computational rank/budget/tolerances are delegated AI operational choices, not researcher-confirmed general scientific importance.

| Block | Status | Grounding / retained boundary |
| --- | --- | --- |
| A Question | CONFIRMED_WITHIN_DELEGATED_SCOPE | accepted old/new retention-acquisition question;necessity bounded |
| B Data | CONFIRMED_WITHIN_DELEGATED_SCOPE | existing paired-list train/dev;fit from old train only;test closed |
| C Supervision | CONFIRMED_WITHIN_DELEGATED_SCOPE | visible rule,one answer token,CE only |
| D Model | CONFIRMED_WITHIN_DELEGATED_SCOPE | specified Qwen,last o_proj,frozen parent |
| E Update | CONFIRMED_WITHIN_DELEGATED_SCOPE | no momentum,matched step norms;exact source code frozen |
| F Comparison | CONFIRMED_WITHIN_DELEGATED_SCOPE | ordinary/protected/equal-rank random,both orders;descriptive branches |
| G Execution | CONFIRMED_WITHIN_DELEGATED_SCOPE | one four-H100-reserved node,2h ceiling,internal Smoke/external-resume gate |

Cross-block consistency PASS;no consequential judgment request is reintroduced after the user delegated reasonable execution. Interpretation/closure Unknown. All thresholds below are explicit operational screens, not a human claim of population significance.

## A. Question and parent relation

After A learning,does avoiding estimated old CE-sensitive directions lower A deterioration with useful B gain relative to ordinary and random-restricted updates? Earlier simultaneous/local CE help and inconsistent pair-margin transfer motivate separating acquisition from retention. They do not imply sequential forgetting. The intervention estimates one local response route;no SME/SAE/router/expert utility claim.

## B. Data,fit and evaluation

Required registered IDs:model_qwen3_0p6b_base_official_a5,tokenizer_qwen3_0p6b_base_official_a5,data_a17_list_rules_v1. Fresh strict access before preparation;official parent file hashes checked by loader. Freeze train/dev/manifest hashes,source/tokenizer model identities and original attachment bytes.

Existing train4000 rows=2000 ordered lists×2rules;dev800 rows=400paired lists,each rule400. The old rule receives its2000 distinct training rows once;the new opposite rule receives the same lists in the same seed-shuffled order with a different visible rule. No contradictory complete-prefix labels. All20one-token answers,position/answer marginals and oracle inherited/checked. Train/dev ordered lists disjoint. Nominal dev order-new groups are in this complete old-training epoch;combination-new groups absent. Preserve both and combined. Do not read test. Dev was previously exposed,so this is descriptive,not blind confirmation.

Fit60 old-training records,three per20answer words,selected by fixed seed before model access;do not fit/select directions using dev or new-task outcomes. Fit can overlap old-training records by design;ordered dev inputs remain held out. Qualification uses first20old dev records without outcome-based selection,so limited content coverage is recorded;not an additional confirmation split.

## C. Task and observable

Prefix ends at answer marker,rule/list visible,completed answer forbidden. FIRST target item1,LAST item3. Supervise only next-token full-vocabulary CE,no auxiliary/SAE/replay/distillation objective. Answer tokens are the valid prediction-token coordinate. Evaluate full native CE,full-vocabulary accuracy,correct-versus-other-rule margin,correct-versus-best-other-list margin,20answer conditionalCE and poollogmass. Store per-record values,rule×panel and combined aggregates.

## D. Architecture and sensitivity

Original28-layer Qwen3-0.6B Base,FP32 eval-mode deterministic native forward,TF32off,SDPA,CUBLAS workspace fixed. Only layer27 o_proj [1024,2048],2,097,152 parameters receives gradients. Others frozen/hash checked. No model-from-scratch or expert insertion.

At old endpoint fit G[60,2097152] of individual native CE gradients,uncentered. Compute leading16vectors through Gram eigendecomposition;rank is frozen,not chosen by dev. Orthonormalize rows;max Gram deviation<=2e-5 and all eigenvalues resolved. Fitted energy fraction/per-example fractions recorded;do not name this all old-task sensitivity. Random control:independent dense Gaussian16-row basis using seed+12345,orthonormalized,same codimension. Ordinary remains unconstrained;parameter storage same but effective update dimension differs from constrained controls.

At identical old state verify dev per-example gradient energy captured by fitted/random bases,and apply first basis vector with signs±,radii0.01/0.1,equal parameter norm. Save mean signed and RMS per-record oldCE changes and exact restoration. Unsigned sensitivity need not mean harm. First20records/vector is a limited qualification,not complete geometry. Basis fixed through B training;record its initial validity only,with drift as a live rival.

## E. Training and matching

For each seed29/43/71 and A=FIRST/LAST:train A100updates×20answers=2000,from official Base;then restore same A endpoint for three B strategies,each100updates×20=2000. Six old plus18new trajectories,48,000scientific training answers,2,400updates. Full old2000/new2000 all distinct lists perstage. No stochastic dropout/mixed precision. No DDP:four independentGPUworkers distribute cases.

Manual plain SGD LR0.01,gradient norm clip1,no momentum,weight decay,scheduler or optimizer state history. Micro5×accum4;CE summed then divided20. Old/ordinary step=-LR×clipped gradient. Protected/random gradients are projected then rescaled to the ordinary trajectory's requested step norm at the same new step. Ordinary is run first to freeze the100-step reference schedule;all strategies have identical new batch order and endpoints. Direction differs;step scale not shrunk. Projected gradient norm<1e-10 stops,not counted as skipped learning. Requested/actual delta discrepancy<=1e-3 relative and constrained leakage<=2e-3;actual step-norm mismatch to ordinary<=2e-3. Save retained gradient fractions/leakage for interpretation.

Training contracts:all seven required TensorBoard tags under each trajectory/tensorboard:tokens/train_lm_loss,updates/train_lm_loss,tokens/train_total_loss,updates/learning_rate,progress/tokens_seen,progress/optimizer_step,progress/effective_tokens_per_update. No enabled auxiliary loss components. Coordinate valid answers perstage;stage directories separate,not confused with cumulative total. Metrics include exact batch_record_ids,counts,gradient/step norms,clipping/projection diagnostics,step/token coordinates. Nonfinite/missing gradient stops;no skipped windows.

Save old milestones0/16/50/100,and each new0/1/16/50/100 (no full Base copy). States include matrix,manual-SGD constant schedule contract,Python/NumPy/CPU/CUDA RNG,step/tokens/data cursor,config/parent/case identity,subspace/reference-step-schedule pointers;actual subspace andschedule saved separately. New0 restores A endpoint;optimizer has no momentum/reset state. Final external Full continuation NOT_CHECKED;Smoke external process tests same updater at step1→2 exact weights/RNG/metric.

## F. Decision and rivals

At fixed dev:old acquisition=initial A loss−post-A A loss;new gain G=post-A B loss−post-B B loss;old degradation D=post-B A loss−post-A A loss. Separate mean/rule/panel/accuracy/margin. Unit nat/answer forCE;accuracy proportion. Complete both sequential directions within each seed,never count them as six independent seeds. Three training seeds only,no p-values or population confidence intervals.

Operational screens:old acquisition>=0.01;ordinary new gain>=0.01;ordinary forgetting D>0.01. Protected retains useful gain when G_protected>=0.9G_ordinary and G_protected>0.01. Specific protection requires D_ordinary−D_protected>0.01 and D_random−D_protected>0.01. These are practical comparison screens chosen for this bounded delegated run;all continuous values retained and no substantive threshold universality asserted.

Typed per-case branches,priority order:OLD_ACQUISITION_INSUFFICIENT;NEW_ACQUISITION_INSUFFICIENT;NO_ORDINARY_FORGETTING;LOCAL_PROTECTION_WITH_RETAINED_LEARNING;NEW_LEARNING_COST;NO_SPECIFIC_PROTECTION. Across six order/seed cases consistent protection only if all six satisfy constructive protection,else mixed/non-supporting;report individual cases and both directions,not majority-based support. Weak heldout sensitivity/finite qualification narrows any mechanism attribution even if policy numbers improve. Removal failure cannot establish universal necessity. No ordinary forgetting refutes only this budget/settings' net-forgetting account.

Rivals and separators:smallersteps→per-step actualnorm matching;reducedsubspace capacity→equal-rank random;no old acquisition→initial/post-A;no new learning→G;no ordinary forgetting→D;trainfit-only→independent dev sensitivity;basis drift/optimizer-specific→explicit limitations. CE bookkeeping/pair margins protect candidate-vocabulary explanations but do not locate functional modules. No architecture or SAE condition ran.

## G. Execution,Smoke and result lifecycle

One h100-4-reserved node,image shphd-lite-0911,resolved from docs/execution_envelope.md through root canonical ACP template. Reuse mounted runtime/Transformers;no installation. Two-hour payload wall ceiling. Code/checkpoint/input freeze,unique UTC run path,writer lock;no duplicate live job/fallback resource. Root supervises completion because this request includes post-execution judgment;no automation.

Before Full internal Smoke four GPUworkers use3old+3new updates/strategy,basis rank4/20fitrecords,bounded20-list dev view. Check same native initial ability,finite gradients,one exact trainable matrix,deterministic no-op,frozen versions/hash,actual norm matching/leakage,complete savedstates,allTensorBoardtags/counters and source data. Then external worker process reloads protected step1,reads same subspace/reference norm and verifies continuous step2 exact weights,RNG,metric. All4Smoke+4resume mustPASS before Full. Smoke updates/artifacts are engineering only,not part of48,000 scientific answers;bounded Smoke does not qualify nominal seen-group novelty before a full epoch.

Stop on missing identity,data/target error,nonfinite,rank/orthogonality,no usable direction,constraint/norm leakage,frozenmutation,resumefailure,processfailure or timeout. Inspect originaljob before retry;preserve failures,distinct recovery root;only material scientific change needs amendment and evidence-boundary review. No automatic threshold or rank tuning based on failures/outcomes.

Expected artifacts:source/config/input freeze,jobreceipt/environment/executioncertificate,Smoke/resume/Full qualification,old/new checkpoints+manifests,metrics+TensorBoard,per-record native evaluations,subspaces+sensitivities+finite qualification,6case summaries,results,payloadmanifest,completion. Execution root /data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update. Register actual checkpoint families and analysis arrays with parent,data,source/progress hashes;no planned save is registered as actual. Complete bilingual Summary/Detailed in Purpose→Model→Hypothesis→Conclusion→Analysis. Claim limits survive failure or positive result.

## Freeze and append-only execution notes

Scientific body frozen before submission;retain run-local snapshots and hashes. Append submission/completion/deviation facts later;do not rewrite post-start settings or old A17 contracts.

### Submission / 提交记录

Job `pt-ubjfxl7c`,2026-10-11 01:16:14 Asia/Shanghai,one h100-4-reserved node. Internal Smoke/external-resume gate pending;Full NOT_RUN. Scientific body frozen in run-local snapshot. [Execution certificate](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/execution_certificate.md).

### Verified completion / 完成核验

Jobpt-ubjfxl7cSUCCEEDED;fourSmoke/resume/FullPASS;scientific48000answers,Smoke960;22input/426Fullpayloadhashesverified;40actualcheckpointfamilies+analysisregistered. No amendment/retry. Frozen6casebranches allNO_ORDINARY_FORGETTING. [Summary](summary.md) /[Detailed](detailed.md);mechanism/closureUnknown.
