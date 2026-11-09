# Smoke Protocol: S7 single-branch training and analysis qualification

[中文](smoke_protocol_cn.md). Engineering scope authorized explicitly by the researcher on 2026-10-07 (Asia/Shanghai): prepare and submit a bounded Smoke including training and analysis on **four reserved H100 GPUs**. This authorization is independent of the [formal Protocol](protocol.md), which remains `DRAFT_NOT_EXECUTABLE`. No new Work/Codex task is required or authorized here.

## 1. Purpose, Hypothesis And Boundary

Purpose: qualify whether the proposed one-position Dense/MoE implementation can produce trustworthy two-stage training, frozen-SAE records and native heldout-loss measurements. The engineering hypothesis is that the implemented inputs, trainable paths, checkpoints, counters and analysis satisfy the declared identities and freeze boundaries. Its rival is an implementation artifact: a shifted target twice, a live SAE loss, unexpected trainable backbone, incorrect routed gradient, broken resume or mismatched analysis tail.

Smoke **does not test** whether MoE retains old skills better. Eight updates per stage and eight development records per task do not supply scientific evidence for the formal hypothesis. Loss improvements, damage values and SAE distances are diagnostic outputs without a scientific Pass threshold. Formal practical margins cannot be selected from these effects.

## 2. Frozen Engineering Inputs

Execution owner: `/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/`. Raw data, outputs, checkpoints, immutable snapshots, TensorBoard and receipts remain there.

Base checkpoint: `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/state.pt`, SHA256 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`. This is 33 billion pretraining tokens, not 33 billion parameters. The native model source SHA256 is `8c13b85a1d07b6bb30a9727785540ef3f7b836828f7afc1682d52decfa252422`. Freeze final adapted source/config hashes after CPU qualification and before submission; immutable execution snapshot and receipt govern the actual revision.

Source data: `/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/data/data.pt`, SHA256 `58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`. Use exactly 32 existing training and 8 existing development records for each of GSM8K and MMLU: 80 records total. Only the cache's internal train/development records are selected; no internal-test records are selected or evaluated. Loading the combined cache also deserializes its internal-test storage. Internal splits contain official-test-origin benchmark IDs, so this is not an untouched official-test evaluation. Do not fetch network data. The new `data/manifest.json` owns source IDs, selections, masks and exclusions; `smoke_records` payload SHA256 is `241134c739fde35903d615a9101afe36aca6f3b87a009a6d7d9705098a87117f`.

Use full stored prefixes capped at 512 positions. Convert source labels once to already-shifted `target_ids`: position \(t\) predicts input token \(t+1\), last position and all non-answer targets `-100`. Every record retains the original valid-answer-token count; invalid/empty answer records are a preflight failure rather than silently replaced. Development records are engineering-only, not untouched scientific confirmation.

## 3. Architecture And Trainable Paths

Freeze eight-layer S7 backbone, tied embedding/head, all norms and the fixed width-30,000 Top-K-32 SAE. Add the only trainable branch at `blocks[7].attn.o` (2048→1024). Dense: rank 8, scale 1/8, one pair. MoE: eight independent rank-8 expert pairs, no shared expert; router reads the same 2048-dimensional pre-projection vector, selects Top-1 and retains its softmax probability. No target or task-ID router input.

Dense has 24,576 trainable factor parameters. MoE has 196,608 expert-factor and 16,392 router parameters, total 213,000. Per position one factor pair is active; total capacity, routing and optimizer cost are not equal. This Smoke records parameter counts, routing, elapsed time, memory and token exposure; it does not implement a complete training-FLOP account or assign a fair-comparison scientific verdict.

The adapted expert bank uses independent expert Parameters (`nn.ModuleList`), unlike the historical stacked bank. With gradients reset to `None`, an unselected expert can have `grad=None` and AdamW skips that Parameter. An allocated zero gradient can still cause a moment/decay update. Inspect actual gradients and increments, and qualify both distinctions. All expert Parameters remain `requires_grad=True` in both stages; no old-task expert is manually frozen. Router updates may change old-sample selections even if an expert's own weights do not change.

Precision: the frozen backbone uses BF16 compute; the fixed SAE retains source FP32 weights; adapter and router weights/optimization use FP32. Freeze checks compare like-for-like loaded precision to its initial state, and source checkpoint identity remains recorded separately. These native BF16 loss changes are not numerically identical to the previous 1002 FP32 panel. Real-arithmetic factor-product identities do not imply exact machine activation equality after casts/addition; measure the native activation difference and report any rounding residual.

SAE is detached, evaluation-only. Never add reconstruction / AuxK loss to the objective or replace native Attention outputs with SAE reconstruction. Zero output-factor initialization must reproduce frozen native logits and heldout loss under the same precision. Initially zero expert outputs can give zero router gradient; this is an expected first-step case.

## 4. Training, Scheduling And Recovery

Four independent single-GPU processes, **no DDP and no cross-arm loss reduction**: Dense seed 17, MoE seed 17, Dense seed 29, MoE seed 29. Within each seed, pair the data order and accumulation windows. Each process uses microbatch 2, accumulation 2, effective batch **4 records**, sequence cap 512. Count observed valid answer targets rather than treating all padded positions as targets.

Each arm learns GSM8K for 8 updates, then MMLU for 8. Keep factors, router and optimizer state live across the stage boundary. AdamW factor LR 2e-4 / decay 0.01; router LR 5e-4 / decay 0; betas (0.9,0.999), epsilon 1e-8, joint clipping norm 1; constant LR and no warmup for this engineering scope only. The objective is valid-answer-token CE sum divided by the full accumulation window's valid target count. No extra objective components.

At new-task update 4, save all adapter/router weights, optimizer, RNG, sampler/cursor, cumulative valid-target tokens and optimizer updates. Compute one continuous reference update 5 and preserve its resulting state. Start an independent process from update 4, reproduce update 5, compare model/optimizer/RNG/token state, then finish updates 6–8. Resume must preserve both coordinate axes without duplicate events; start an explicitly named resume event segment if needed. The discarded continuous reference is an engineering check, not another scientific trajectory.

Cost: 4 arms × (8 old + 8 new) = **64 logical updates**, plus 4 reference updates = **68 actual updates**. Count additional analysis/recovery costs explicitly. Never turn Smoke learning curves into formal endpoint selection.

## 5. Analysis Qualification

Use the identical eight old development records before old learning, at the old-stage endpoint and at the new-stage endpoint. Evaluate both tasks with token-weighted native answer CE. Save per-record loss sums/counts, raw Attention inputs/outputs and route IDs/probabilities; record starting state and both stages. No generation accuracy gate.

For the same old prefixes, the projection input should remain unchanged because all earlier computations are frozen. Save raw Attention output \(a\), SAE code \(z\), and reconstruction residual \(\varepsilon=a-b_{\rm SAE}-Dz\), then check the exact accounting \(\Delta a=D\Delta z+\Delta\varepsilon\). Retain pre/post reconstruction quality and unrepresented changes; an identity check does not show harmful sparse directions.

Recompute pre/post native loss through the unchanged residual, complete final MLP, norm and head. Replay the entire stored old Attention output through this frozen tail to check loss restoration; this qualifies the interface, not a selected-direction mechanism. Check replay against normal forward with explicit dtype/tolerance recorded in the frozen config. First-order loss changes may be emitted with error against measured finite loss, but are not substitutes for that loss; a route switch is not assumed differentiable. Local approximation quality is reported, not used as a scientific mechanism threshold. No selected-direction removal/restoration scientific experiment is included.

## 6. Mandatory Engineering Evidence And Stop Rules

Pass requires CPU schema/no-op/gradient-boundary tests before submission, correct 80-record source manifest, finite training loss/gradients, unchanged frozen-backbone/SAE hashes, trainable factor updates and qualified routed gradient semantics, complete native-tail/SAE analysis, and successful independent-process recovery with registered equality/tolerance. Preserve exact versus tolerance-based comparisons separately.

Each arm writes `arm_run` and the required [observability tags](../../../../../../../docs/training_observability_contract.md): `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`. The primary token count must match an independent full-update valid-target count and increase only for completed logical accumulation windows. Log LR for factor/router groups and phase without inventing regularization tags for disabled losses.

Stop on nonfinite values, changed frozen weights, invalid target/schema, source/hash mismatch, incorrect counters, failed restore/native-tail check, or wall-time ceiling. Preserve a typed failure receipt. An engineering failure does not mean an architecture has a negative scientific effect; absence of a loss reduction is not itself a Smoke failure.

## 7. Resource And Authorization Envelope

Use the current execution envelope's **`h100-4-reserved`** profile: exactly four H100 GPUs, reserved resource pool. Resolve the current image, submission entry point and certificate through [the execution envelope](../../../../../../../docs/execution_envelope.md); do not reuse historical profile/image commands. Hard payload wall-time limit **1,800 seconds**, approximately **2 H100 GPU-hours** for four simultaneously allocated cards, with up to 30 seconds termination grace plus separately reported environment startup/platform-release overhead and scheduler queue. This is a payload budget, not an exact platform billing ceiling. No automated retry or full-run scale-up.

Record immutable code/config/data hashes, profile/image/resource certificate, job submission receipt, pod/log identity, per-arm training and analysis receipts, recovery comparison and artifact inventory. Scope allows implementation, CPU qualification, one bounded Smoke submission and bounded startup/progress/failure verification. Additional submissions after failure require the owner to assess whether the already authorized repair scope applies; no silent resource escalation.

## 8. Freeze, Results And Remaining Approval

Before GPU execution, freeze this engineering contract and the qualified immutable executable snapshot in the execution receipt. Status before a receipt exists: **AUTHORIZED_FOR_SMOKE; NOT RUN**. Actual submission/completion comes only from receipts; this body does not predict it. Post-start material changes need an append-only amendment with before/after, reason, visible artifacts, authorization and eligibility impact.

The only permissible engineering judgment is qualified / failed / incomplete for the properties above. The formal hypothesis and compute-matched two-stage run await researcher approval of the draft Anchor/Protocol, data boundary, learning schedule, budgets and scientific criteria. Passing Smoke cannot promote them automatically.
