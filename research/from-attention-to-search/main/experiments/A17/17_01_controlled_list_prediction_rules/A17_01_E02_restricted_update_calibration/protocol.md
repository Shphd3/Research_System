# Protocol: A17_01_E02 Restricted Update Calibration

## 0. Approval Snapshot

`APPROVED_FOR_IMPLEMENTATION_AND_SMOKE`; result `NOT RUN` at this pre-submission freeze. On 2026-10-10 Asia/Shanghai, the researcher explicitly requested a child-agent LoRA Smoke and asked whether directly updating the last projection is preferable. Because these are not equivalent, the already proposed same-location L/R8 engineering comparison is retained. This approval covers one four-H100 reserved bounded Smoke only; frequency, representation/SAE execution, Full, publication and scientific adoption remain unauthorized or Unknown.

Routine pilot settings below are engineering choices within that authorized scope. No new scientific threshold, mechanism judgment, capacity optimum or preferred learner is inferred from authorization. F's scientific near-zero threshold and learner/window adoption remain `Unknown`; they do not block target/freeze/resume/finite-readout engineering checks.

Purpose: qualify the restricted updater and its measurable outputs. Strongest engineering rivals are a broken/ineffective restricted learner and rapid saturation. The primary scientific purpose remains the [A17 Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md); [Focus](../../../../focus/focus_list_rule_shared_update.md) owns the question.

[中文](protocol_cn.md) · [E01 result](../A17_01_E01_stage1_smoke/summary.md) · [frequency draft](../A17_01_E03_fixed_pool_frequency/protocol.md).

## 1. Terminology / Definitions

A restricted update changes one named matrix or its LoRA factors while other weights stay fixed. LoRA writes an added matrix as a product of two low-rank trainable factors; it does not guarantee only formatting changes. “Upper layer” is a location, not a proved functional surface. All FIRST/LAST examples use the same shared trainable module. No per-rule adapter, expert or router is introduced.

Full-vocabulary answer CE is in nats/answer. Negative recipient after-minus-before CE means local improvement; the useful-source guard requires same-rule held-out improvement. Order-new and combination-new retain E01 meanings relative to task training.

## 2. Anchor Alignment

Keep the FIRST/LAST question, paired carrier, tokenizer, answer loss and both novelty panels. Restrict the update domain to improve attribution to a parameter location, not to prove a rule's unique function. LoRA can introduce a capacity bottleneck, so any conflict is conditional on this restricted learner. The original unrestricted labels are simultaneously satisfiable.

## 3. Tested Hypothesis

AI hypothesis: a late output-projection update can adapt this carrier while leaving sufficient residual answer error to measure finite cross-rule effects. Rival: this location/rank cannot implement useful adaptation, or it still saturates rapidly. Distinguish useful source learning from cross-recipient sign and numerical resolution.

## 4. Rival Explanations

A final all-correct endpoint need not have resolved CE changes. Fewer trainable parameters do not guarantee slower learning. Format/answer-prior drift can explain initial low accuracy. LoRA versus local full-rank differs in parameterization, optimization and capacity; equal learning rates do not match functional step size. Zero-initialized output factors legitimately give an initially zero gradient for the other factor; this is not a broken gradient path.

## 5. Data Construction And Provenance

Reuse `data_a17_list_rules_v1` only after fresh strict access: 4,000 train/800 dev/800 model-sealed test rows, 20 Chinese words, visible rule, one fixed template, exact balanced marginals. E02 operates on train/dev only and cannot produce confirmation evidence from the already opened dev. Five independently seeded source batches per rule, each100 rows stratified to five answers per vocabulary word, sampled from training. Pair source list selections across FIRST/LAST where feasible. Save source IDs, content groups and target counts; do not select lexicographic prefixes or choose batches by cross-rule loss.

## 6. Learning Task And Permitted Supervision

Feed only the prefix ending at 答案：; supervise exactly its next answer token. The answer can appear in the list, never as a filled answer field. Full-vocabulary CE remains unchanged; no three-choice-only head, auxiliary objective or representation/SAE analysis.

## 7. Model / Architecture And Frozen Variants

AI default carrier: original `model_qwen3_0p6b_base`, not E01's adapted endpoint. The local verified config has28 layers, hidden1024,16 attention heads of128 dimensions. Final module is `model.layers.27.self_attn.o_proj`, weight1024×2048.

Two calibration conditions: (L) train this matrix directly,2,097,152 parameters; (R8) freeze it and add shared rank8 LoRA, alpha8, scale1, dropout0, no trainable bias,24,576 factor parameters. Freeze embedding/tied LM head, all norms, MLP and all other attention parameters. Zero output-factor initialization preserves initial logits under matched precision. Because this is the final attention output projection, its upstream computation is unchanged; the fixed downstream MLP/norm/head still responds to the changed output. This does not confine functional changes to formatting.

E01 whole-model results are historical context, not a matched control for the new batch/optimizer grid. Dense is a proposed later carrier replication; S7 and rank expansion are not included in this first calibration. If R8 fails while L works, rank16 can be proposed prospectively, not silently inserted.

## 8. Training Objective And Optimization

AI grid: AdamW LR1e-5 and1e-4 in each condition, betas(.9,.95), eps1e-8, weight_decay0, clip1. FP32 trainables/state, frozen weights loaded consistently, BF16 compute plus FP32 effect checks. One-answer sum divided by exact global target count. Independent single-GPU arms, micro5×accum4=20 answers/update; equal FIRST/LAST exposure. Warmup40 valid answers, then fixed LR; do not stretch schedules by final budget. Maximum50updates/1,000answers per arm. This batch differs from E01's64; comparisons to E01 are unmatched. The exact grid is proposed, not an approved optimum.

## 9. Conditions, Seeds, And Checkpoints

Four pilot arms: L/R8×two LRs, seed17. Evaluate/save at updates0,1,2,4,8,16,32,50 (initial is an adapter/native baseline save). Measure capability/CE at all; source-batch finite probes at0,2,8,16 to prioritize early states. Save optimizer/scheduler/RNG/data cursor/counters and parent model identity; qualify an independent restart at8 using a continuous next-step reference. Resume is a check, not a second scientific trajectory. All checkpoints are retained even if saturated; no test-driven selection.

## 10. Primary Metric And Frozen Analysis Plan

Primary output is a map of state×source×recipient finite CE changes. From each fixed base state, independently apply plainSGD on the declared trainables with candidate eta1e-5/1e-4/1e-3, restore weights/RNG between sources, and evaluate paired per-record changes on a preselected 80-row engineering dev panel (one per rule × novelty × answer word). Full 800-row dev capability/CE is measured at all saved states; finite probes do not qualify full-dev source efficacy. Training optimizer state is untouched. Report every candidate, not only favorable signs. Source eligibility uses its own dev effect; cross-rule sign cannot choose a learning rate/checkpoint/source batch. Never compare LoRA-factor gradient dots with full-rank dots as identical functional updates.

Report each rule×novelty, panel totals and record-weighted combined, along with source-batch variation. Numerical qualification compares repeated no-op (five repeats), parameter restoration and the same finite contrast in BF16 and FP32. A nonzero sign without calibrated precision evidence is unresolved. AI operational criterion: at least one early R8 state has both source rules yielding resolved own-rule decreases across at least4/5 batches at a candidate scale and no contradictory BF16/FP32 resolved signs. Tolerance/near-zero band and the joint scale selection rule are BLOCKED until pilot numeric evidence and researcher review; no confirmatory verdict/CI is produced by this calibration.

## 11. Secondary Metrics And Guards

Record source losses, recipient losses, actual added-matrix norm, frozen-weight drift, trainable count, per-rule answer exposure, total valid targets, optimizer steps, required TensorBoard tags, optimizer moments/resume checks and probability of the correct token. Frozen-weight drift must be zero under identical load precision. Factor gradients need not both be nonzero at initialization. Optional two meaning-preserving prompt variants are a future format-vs-rule diagnostic, not an assumed result or an activated condition.

## 12. Known Good / Known Bad / Known Confusing Cases

Good: zero adapter equals original native logits/CE; restored same state gives no-op reference. Bad: answer field appended, a frozen head changes, source targets collapse to one word, resume loses cursor, or cross-rule effects select the state. Confusing: all-correct dev with residual CE; unchanged low-rank factor at the first update; native-BF16 zero delta with FP32-resolved delta; R8 fails while L learns.

## 13. Scientific Procedure And Stage Contracts

1. Data/shape preflight: inspect registered inputs and qualify target scope, source counts and exact module; fail on identity/schema mismatch.
2. Local contract checks: zero-adapter/native equivalence, frozen weights, normalization and full state restoration; output qualification receipt.
3. Bounded pilot: four arms, early saves/CE and declared finite probes; stop on nonfinite values, frozen drift, wrong counters, failed restore or wall ceiling. Every observed value is dev-only.
4. Audit: source efficacy and precision/remaining-error map. Researcher chooses scope/window or repairs it before a frequency run. LoRA adoption is not mandatory if a different learner offers a qualified window.

## 14. Algorithm, Output, And Provenance Contract

Frozen execution root: `/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/`; new code/config and new run root required, never rewrite completed E01 outputs. Reuse answer wrapper/generator/aggregation interfaces; adapt existing final-projection low-rank/freeze/resume checks from the inspected1007 SingleBranch implementation. Do not reuse its router, SAE diagnostics, benchmarks,1/8 scale, or old submission script; R8 scale1 is explicit.

Required: code/config/data/source-ID manifests; strict input check; shapes and trainable/frozen identities; per-arm losses/capability/probe records/TensorBoard; checkpoints and resume receipts; numerical/terminal audits. Register actually saved adapter families with the base checkpoint and strict output access before handoff. Authorized Smoke hardware: h100-4-reserved, four independent single-GPU arms, no cross-arm DDP reduction. Frozen pilot payload wall ceiling1,800s, at most2 allocated H100 GPU-hours plus reported platform overhead. Current envelope/image must be resolved before any later submission. Only this bounded engineering Smoke is authorized; no Full or frequency run is authorized.

## 15. Success / Failure / Insufficient Evidence

Engineering PASS: correct targets/counts/freeze, native equivalence, finite telemetry, exact saved state/restart and complete panel outputs. Engineering FAIL: demonstrated contract violation; missing outputs are INSUFFICIENT. Operational support: an eligible useful-source/precision window exists in the prescribed scope; non-support: no such window among complete candidates; unresolved source/precision is insufficient. Neither branch supports/refutes stable shared interference. Researcher owns adoption.

## 16. What This Cannot Claim

No LoRA superiority, pure low-rank causal effect, format-only change, naturally necessary conflict, function decomposition, pretraining learning mechanism, universal model mastery, representation finding or expert necessity. Equal adapter/full-matrix learning rates are not equal functional steps. Dev is not untouched confirmation.

## 17. Block Confirmation, Freeze, And Amendment Ledger

The confirmed question/task boundary remains unchanged. A/C reuse confirmed carrier facts. The researcher authorized implementation and child-agent Smoke in the current turn; B/D/E/G's exact pilot values are engineering choices for that scope, not scientific adoption. F engineering gates (exact targets, native equivalence, frozen bytes, finite logs, saved/restarted state, complete panel readouts) are fixed. F near-zero/scientific window rule and later learner adoption remain Unknown and are not evaluated here. This does not promote scientific A-G confirmation or a frequency contract.

Pre-submission operational refinement on 2026-10-10 Asia/Shanghai: finite probes use a deterministic 80-row stratified dev engineering panel rather than all800 rows, to fit the1,800-second aggregate payload ceiling. Five answer-balanced sources × three step sizes × BF16/FP32 are retained at0/2/8/16. Full800 dev remains at each capability checkpoint. Source selections are independently stratified by rule; paired-list source selection is NOT_APPLICABLE to this engineering refinement and is explicitly recorded false. Native equivalence uses20 dev rows in both precisions. No-op uses five repeats; only exact engineering drift/restoration is judged. All raw signs remain scientifically unresolved.

Freeze before first submission: source/config/Protocol/data hashes and the actual command are recorded in the run. No E01 frozen source or result is amended. Once the approved Smoke starts, preserve this body; any needed fix is append-only with its eligibility impact. Stop on nonfinite values, frozen drift, counter/restore violation or aggregate1800s payload ceiling. Do not enlarge the pilot or open test to repair a gate.

Method references: [LoRA original paper](https://arxiv.org/abs/2106.09685), [training observability](/data/250010109/Research_System/docs/training_observability_contract.md).

## Append-only execution ledger: 2026-10-10 Asia/Shanghai

One job submitted: pt-bw3s1pxw, four H100 reserved; no retry/expanded run. Frozen pre-submission body is archived at `/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_20261009T162413Z/protocol_frozen.md` and its original hash in frozen_sources.json. Source amendment01 strengthened the native guard to exact all-vocabulary logits and per-record CE in BF16/FP32 before pod runtime; original runner bytes/hash retained, actual revised hash recorded. No objective/data/optimization/probe/adoption rule changed. Runtime and terminal evidence belong to Summary/Detailed, not this registered body.

## Append-only engineering repair02

First job pt-bw3s1pxw failed at the update0 probe restoration guard; four saved native-equivalent initial states, zero trained trajectory updates. The FP32 baseline had incorrectly retained the final BF16 virtual update. Resetting declared trainables/RNG before each precision repairs that mismatch; eight CPU tests now pass, including the actual probe isolation regression. Failed outputs and source revision1 remain untouched. One same-profile/four-arm/50-update repair retry is within the researcher-authorized bounded engineering Smoke; no scientific adoption, Full, frequency or SAE extension. Retry payload cap1600s plus first durable payload upper64s and30s kill grace stays below aggregate1800s. Exact sources/config/parent lineage are frozen in the new run `/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z`. Source/state numeric values from the failed probe are ineligible and not reused as results.

## Append-only numerical conformance boundary

The pilot computes source gradients separately in BF16 and FP32 and then evaluates in the corresponding precision. Thus it compares two complete update/readout pipelines, not the same fixed functional perturbation under two readers. This is bounded engineering precision evidence; it cannot isolate reader error or qualify scientific source signs. A future scientific numeric qualification must freeze one actual perturbation and evaluate both readers, or otherwise separate update-direction and reader changes. No new run was performed for that future requirement.
