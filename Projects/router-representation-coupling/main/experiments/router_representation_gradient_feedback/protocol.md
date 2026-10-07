# Protocol: Router representation feedback training

## 0. Approval Snapshot

Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_PASS_GATED_SUBMISSION.
Approval source: [direct researcher request and latest revision](../../../handoff/researcher_request_cn.md); current execution thread reiterates it. This is explicit delegation of engineering/experimental concretization, overriding skill defaults that otherwise require a new A-G confirmation. It is not a claim that the researcher supplied every hyperparameter.
Registered revision: R1; design_frozen_at: 2026-10-05T09:37:28.180373+00:00.
A-G: scope/core CONFIRMED by request; remaining exact implementation choices DELEGATED_AND_REGISTERED. Consistency: self-audited, engineering eligibility requires tests below. Scientific threshold/strongest-rival ranking/adoption/closure: Unknown. Parent [Focus](../../focus/focus_router_representation_gradient_feedback.md), [Anchor](../../problem_anchors/router_representation_gradient_feedback/anchor.md).
Purpose: test direct backward feedback at unchanged same-state forward. Role: root-cause audit, exploratory. Primary measure B-minus-A heldout CE. Conditions: coupled/4H100 reserved; router_input_detached/8RTX5090 spot. Both hardware Smokes must PASS before either full create. Submit each formal arm once; record direct result and stop polling immediately. No extra seed/arm, fallback, commit/push, reminders or automatic re-submission.

## 1. Terminology / Definitions

r=pre-residual attention output; h=post-residual normalized expert input. detach cuts only derivative through r into router, preserving its numeric value and router-parameter gradients. valid prediction token is a non-ignored next-token target. A/B refer to algorithms, H/G to Smoke hardware; Smoke runs both algorithms on both hardware types.

## 2. Anchor Alignment

Intervene all 12 MoE layers on the gate-to-r edge. CE measures finite trajectory utility, function reassignment probes within-model assignment dependence. Path identities qualify implementation, not learning benefit. Retain full hardware confounding and single-seed boundary.

## 3. Tested Hypothesis

Both help and harm remain possible. Positive B-minus-A CE supports A's bounded utility; negative supports B. Geometry-only differences are descriptive. Do not reinterpret a failed primary measure using another secondary metric.

## 4. Rival Explanations

Live alternatives: gradient magnitude/Adam statistics, realized expert load and exposure, hardware kernels/reduction topology. No third arm isolates these. Both hardware Smokes replay A/B same-state short windows; require common libraries/math modes, characterize numeric spread and retain unresolved long-run hardware effect.

## 5. Data Construction And Provenance

Train uses /data/250010109/training_data_views/dclm_pair_v1/train with manifest SHA256 8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d. Verify full path/size/target inventory, validation exclusion, first/mid/terminal sample bounds; original manifest is not a 1.2TB content hash. First-pass sequential global sample order; no epoch wrapping and no state-dependent sampling. Across topologies, update u consists of the same 256 consecutive 1024-target sequences, rank assignment only partitions that set. The boundary input token overlaps; targets do not.
Qwen3 tokenizer defining files fingerprinted from /data/share/Qwen3-0.6B-Base; no pretrained model weights loaded. Post-test raw docs come from separate global shard 02; original source hash and document/token manifest frozen in inputs/analysis_manifest.json. Source-level split and within-panel exact-text deduplication do not prove corpus-wide semantic deduplication.

## 6. Learning Task And Permitted Supervision

Causal next-token prediction: source tokens t through t+1023 predict the shifted targets. Data contain no ignore targets; fail if target count differs from source size. No domain label/future target enters router; targets supervise ordinary training only. Heldout panel is excluded from training and model selection; Smoke reads training samples only.

## 7. Model / Architecture And Frozen Variants

Inspected 342,097,408-parameter native Qwen3 MoE: hidden512, 12 layers, 8 routed experts, top2, each expert width1536, one shared expert/layer, tied vocabulary151936, 4 attention/2 KV heads, head_dim128, dropout0. Retain non-renormalized selected softmax mass and temperature1. EMA mode none, aux coefficient0, no capacity dropping, no spectral/SAE/de-common objectives. A uses router_input_detached=false; B true. Experts read live full h. Both use BF16 autocast with FP32 parameters/Adam state, identical mounted torch2.8/cu128 layer and transformers4.53.3, SDPA, TF32 off; no activation checkpointing. Same CE chunk256 in all conditions. Potential SDPA hardware differences remain.

## 8. Training Objective And Optimization

Objective is global token-mean LM CE. Raw router_aux is computed for load telemetry in both, weighted0 and absent from backward. Uniform-length, non-ignored batches make local means plus DDP average exact global mean. AdamW betas(0.9,0.95), eps1e-8, LR1e-4 for all groups, weight_decay0.01, fused=false, global gradient clip1.0. Warmup128 updates=33,554,432 tokens; cosine to zero at update7629, token target1,999,896,576 (<2B,<10B). First finite-budget test uses ~2B to bound cost and expose early/mid/endpoint changes; it is not a converged or compute-optimal model assertion. No skipped updates: nonfinite loss/gradient fails before update; token coordinate advances only after successful full accumulation. No tuning on heldout or formal results.

## 9. Conditions, Seeds, And Checkpoints

One seed1005 and one saved CPU-generated random state inputs/initial_state.pt with file and tensor hashes. Optimizer fresh empty moments; every arm loads the identical state rather than independently trusting same seed. Seqlen1024, microbatch1 on all hardware. A formal4 ranks×64 accumulation; B formal8×32; G Smoke2×128; H Smoke4×64. Each update262,144 actual targets. Formal weights at updates0,64,1024,3814,7629; tokens0,16,777,216,268,435,456,999,817,216,1,999,896,576. Common initial payload plus per-arm 0 weights retained. Rolling full state checkpoint10min or >=0.2B tokens whichever earlier, latest2 retained, complete terminal full state retained. Weights and resume checkpoint/RNG live only under execution root; no old-project payload deletion.

## 10. Primary Metric And Frozen Analysis Plan

Frozen analysis_protocol.md owns the heldout estimand, cluster CI and secondary procedures. Main endpoint is update7629 only; all earlier checkpoints are descriptive, no best-checkpoint selection. B-minus-A per-token document losses, paired document bootstrap5000 replicates seed1005, percentile95% two-sided. Tokens are weights, documents are clusters; bootstrap is not seed uncertainty. AI-proposed practical delta0.01 nat/token is reported alongside zero and cannot become human adoption authority.

## 11. Secondary Metrics And Guards

Required tags and count/resume behavior follow System observability contract; both arms record raw/weighted zero aux tags. Route load/entropy/dead experts every full update, peak allocated/reserved and valid targets/s. LOAD_COLLAPSE engineering stop if any layer effective-expert entropy count<1.5 or >=6 exactly zero-load experts for128 consecutive global updates; both conditions and window identical. Health guard EMA beta0.9, from update128, max EMA log(vocab)+1, reversal>2nat, embedding RMS ratio>4 or sampled logit RMS>20 for3 consecutive updates; fail, do not switch balancing or silently resume. Storage cap100GiB/arm; estimate roughly40GiB/arm including two rolling checkpoints, temporary publish, terminal full state and five weights. Preserve failure receipts.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: same-state A/B logits, routes, gates and CE equal; router/expert parameter gradients equal for isolated block with same outgoing adjoint; expert-input and residual gradients nonzero; B router updates. Full-network A/B expert gradients can differ indirectly from later-layer detach: only final-layer gate/expert gradients are expected equal; decompose all changed edges using independent gate-only VJP accumulation. Known bad: detach expert h or gate weights fails path/nonzero tests; aux>0 or top1 renormalized-to1 refused. Confusing: same logits but upstream gradients differ is intended; higher effective rank without CE utility is not success.

## 13. Scientific Procedure And Stage Contracts

Stage1 local: inspect source/data, generate common init and frozen heldout panel; tiny FP64 path identity and sampler topology/CE chunk tests. Stage2 hardware: one H=4H100 reserved and one G=2RTX5090 spot allocation, both algorithms from common initial state on identical data. Full-model same-state logits/gates/routes with atol1e-6/rtol1e-6 within same hardware; isolated FP64 path checks atol1e-10/rtol1e-8. Record gradients, VJP residual and router/expert updates; common fixed diagnostic sample; cross-hardware logits relative RMS<=0.02 and CE absolute<=0.02nat (engineering tolerances, no after-failure unexplained relaxation), route mismatch measured, not forced0 near ties. Two completed production-global-batch updates per A/B with external-process checkpoint/resume at update1; separate uninterrupted tiny external-process resume parity check. Full shape peak memory below physical minus2GiB and finite throughput; 5090 Smoke certifies2 ranks only.
Stage3: both audited PASS, same registered common config/source freeze; dry-run exact profile tuples. Formal8-rank script fails closed on rank/world, collectives, disjoint sample sets/global batch, identical loaded state, OOM and nonfinites. No claim it was qualified on eight GPUs by two-GPU Smoke. Create A and B once, save each direct CLI result/jobID/error, stop formal polling and no background monitors. SUBMISSION_UNKNOWN prohibits blind repeat. Training completion is not this execution turn's completion condition.

## 14. Algorithm, Output, And Provenance Contract

execution_surface=acp; image_id=shphd-lite-0911; H/A resource_profile=h100-4-reserved; G=5090-2-spot; B=5090-8-spot. Resolve current values only from System docs/execution_envelope.md and use templates/execution/acp_submit_template.sh; receipt captures expanded tuple/image/command. env_layer=scripts/runtime.sh with existing isolated mounted torch280_cu128_py310 and Qwen3 HF layer; refuse absent layer, do not modify base environment. New execution root=/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling. Source/config/request/Protocol/init/data/analysis hashes recorded before Smoke and full. Single-writer flock per run, atomic checksum manifests, same-topology exact resume only within existing job; no automatic platform resubmission. Submission owner=thread01a10b5e-939f-7302-ab6f-bac7b48758d9; Smoke polling owner same; formal monitor=NONE_BY_USER_REQUEST. Code and raw outputs remain execution-side. No commit/push/publication.

## 15. Success / Failure / Insufficient Evidence

Engineering PASS is complete gradient/count/resume/TensorBoard/data/environment/resource qualification on both hardware and within registered numeric thresholds. FAIL blocks both formal creates. Science: directional CE plus function evidence is bounded support; no CE utility/reverse direction weakens relevant hypothesis; unresolved confounds, overlapping interval or incomplete budget give INSUFFICIENT. Researcher owns adoption and mechanism interpretation. No label derived from Smoke can become scientific support.

## 16. What This Cannot Claim

No hardware-independent causal treatment effect, seed generality, guaranteed collapse prevention, fixed representation/routing, future-utility guarantee from gradient dots, semantic-specialization guarantee from labels/geometry, all common adaptation, downstream benchmarks or converged performance.

## 17. Block Confirmation, Freeze, And Amendment Ledger

R1: latest user request overrides original two8×5090 arrangement. A4H100 reserved/G2×5090 Smoke/B8×5090 spot formal and direct-return-only submission are explicitly authorized. Exact model/optimizer/budget/post-test choices are executor concretization under that authority. A-G do not pretend to be individually reviewed hyperparameters. Scientific adoption/strongest-rival ranking remain Unknown. Before any execution register body/hash; after execution preserve body, only append amendments with before/after, reason, exposed data, affected eligibility and existing authorization. Failed tolerances remain failed evidence; no retroactive PASS. Execution outcomes belong to detailed.md, not this registered scientific body.


### Amendment A1 — 2026-10-05T09:54:38.943548+00:00, before GPU Smoke and formal data exposure

Original body retained. Source qualification disclosed FP32 casts inside nominal FP64 HF norms/softmax/CE: strict multi-layer VJP comparison failed with max residual1.65e-8 (receipts/local_gradient_contract_r5.log). A true FP64 independent reference now tests the unchanged chain-rule identity at original atol1e-10/rtol1e-8, max residual<8e-17. This qualifies the reference calculation, not production bitwise gradients. Native BF16 final-layer gradient/path GPU checks are prospectively atol2e-6/rtol2e-3 for reference-path subtraction and1e-6/1e-6 for parameter/forward parity; no failed GPU tolerance has been relaxed. Block F/G affected; initial formal weights/objective unchanged. Smoke optimization schedule is explicitly engineering-only warmup1/total2 updates, preserving actual production shape and262144target batch; formal warmup128/total7629 unchanged.

Runtime adaptation stays project-local: mounted torch2.8 libraries precede incompatible base CUDA libraries; optional base FlashAttention/torchvision are hidden for registered text-only SDPA. No base or shared dependency files edited. torchrun wraps preemption75 as launcher1: external continuation is allowed only after durable preempted_checkpoint_complete at step1 with manifest/checksum, inside the same Smoke allocation. Formal create calls never include scheduling polls. Existing scoped delegation authorizes these engineering repairs; science result NOT RUN.


## Amendment A2 — diagnostic index and Smoke retry (2026-10-05)

Both v1 hardware Smokes failed before the training loop: H100 `pt-0bhf38z4`; RTX 5090 `pt-oz88x40i`. The diagnostic used FP32 `linspace` to select gradient fingerprints from 77,791,232-element embedding tensors; its last integer index became 77,791,232, outside the tensor. Replace it by int64 `arange(16) * (numel - 1) // 15`. The arithmetic boundary check passes for dimensions 1, 2, 4,096, 2,359,296 and 77,791,232. Algorithm, hardware choices, optimizer, data, model, budgets and acceptance tolerances remain unchanged. Preserve v1 logs and source lock. Only confirmed terminal FAILED Smokes may use the explicit v2 create attempt; formal create stays limited to v1. No GPU training run artifacts existed before this retry.


## Amendment A3 — balanced fresh retraining, 2026-10-06T02:44:52.859460+00:00

This amendment supersedes the aux=0, no-monitoring and formal-v1-only clauses for one new paired condition, `rrc_1006_balanced_r3`; the original registered body and failed jobs remain historical evidence. Direct current-thread researcher authorization: “请重提，重新训练，然后监督训练”; selected objective revision: “两臂共同加入负载均衡后重训（改变原训练目标，需要另列新条件）”. No further submission permission is required. This is one fresh paired seed, not continuation from unequal old recovery points. Old A `pt-9egkfirg` and B `pt-86fsmog5` remain unchanged.

**New objective and only A/B difference.** Each arm optimizes LM CE + 0.01 times `router_aux`; coefficient is executor concretization under the existing delegation, fixed before new training. For each layer and each one-sequence microbatch of T=1024 valid positions, f_i=(number of top2 slots assigned to i)/(2T), pbar_i=mean token softmax probability, and L_l=8 sum_i f_i pbar_i. The auxiliary term is the mean over 12 layers, then the mean over the 256 sequences in the global update. Uniform load gives 1. This is sequence-local balancing, not a product of global-update-averaged statistics; identical microbatch1 preserves the objective across rank/accumulation topologies. Hard selections have no derivative.

Both arms recompute the auxiliary probabilities as softmax(W stop_gradient(r)), using the same gate W and equal-valued reference. Auxiliary gradients update W but never the shared backbone via r in either arm. The main LM routing still uses W r in A and W stop_gradient(r) in B; h, experts, shared experts and residual paths stay live. Thus this condition tests the LM gate feedback edge under a common balancing objective, not a combination of LM and auxiliary feedback removal. No claim that adding balance guarantees stability.

**Engineering corrections.** Load-guard counters are per layer; the same layer must violate the original thresholds for128 consecutive updates. Preserve both thresholds and all loss/finite/scale guards. Restore the per-layer counters from full checkpoints. Persist the terminal metric/TensorBoard record, failure JSON and full optimizer/RNG checkpoint before raising a post-update load/health error; no automatic continuation from a guard failure. Weighted auxiliary telemetry is now 0.01*raw, with the same stable tags and actual total objective recorded.

**Frozen scope and gates.** Execution root=/data/250010109/MoE_Router/experiments/20261006_router_representation_coupling_balanced. Keep all R1 model dimensions, raw-attention reference, common initial state/hash, data/panel/order, single seed1005, optimizer, precision, global262144-target batch, schedules, weight milestones and exact1999896576-target/7629-update endpoint. A stays `h100-4-reserved`; B stays `5090-8-spot`; image and runtime keys unchanged. Requalify actual new auxiliary paths and total objective with local positive/negative checks plus two separate original-profile hardware Smokes (4H100 and2RTX5090), each A/B two global-batch updates with external-process resume. Both new Smokes and cross-hardware checks must PASS before the new formal creates. Prior receipts alone cannot qualify the changed objective. Each new stage gets one create-attempt receipt and a unique job name; no blind resubmission, new arm/seed or resource fallback.

**Requested ongoing supervision.** Current user request overrides the original stop-polling/no-background rule. The submission owner is thread01a10b5e-939f-7302-ab6f-bac7b48758d9. Formal jobs run an ACP-managed supervisor inside their own existing allocation, writing `supervision.json` every30 seconds and state transitions to `supervision_events.jsonl`, checking progress, durable terminal state and failure/exit. No local scheduled task or extra GPU monitor job. No progress for30 minutes before the first update or20 minutes afterward writes the shared preemption request for the trainer's atomic boundary checkpoint path; after5 additional minutes a stuck child is killed. Finite/health checks remain trainer-owned. Report meaningful state changes only. This supervisor creates no jobs and does not send external notifications; explicit desktop-independent push notifications are unavailable. Inspect both formal startups and first-progress receipts in this turn.

**Exposure and interpretation.** Original failed training metrics through274 updates are exposed. New TEST panel remains sealed. Do not pool old zero-aux and new balanced conditions into one treatment effect or redefine the main endpoint from early CE. This new pair still has complete hardware confounding and one paired seed. Scientific mechanism/adoption/closure remain Unknown.
