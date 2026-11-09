# Protocol: A15_17_E02 Gradient, Parameter, And Local-Utility Follow-up

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_EXECUTION
Approval status: HUMAN_CONFIRMED by the researcher's 2026-09-16 instruction to execute the referenced follow-up prompt and add 15B checkpoints
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: L1-L4 read-only supplements; G0 gradient audit; G1 isolated one-step tests; E frozen-model N-report NLL; 10B plus the explicitly added 15B checkpoints
Design frozen at: 2026-09-16 before new computation
Purpose: test whether M2's additional reconstruction gradient has a favorable local increment for fixed domain readouts, while completing missing representation, weight, dictionary, and local-performance measurements
Primary Anchor: A15_17 three-model SAE representation trajectory
Anchor decision question: whether an existing SAE-mediated state merits a causal functional intervention
Experiment role: robustness check plus local causal operationalization
Primary metric: at M2 10B, P-report class-balanced cross-entropy difference U = CE(U0) - CE(U1), after averaging per-example losses across the four isolated batch directions and using a 5,000-draw stratified paired bootstrap
Minimal setup: four frozen N-fit batches; each condition restores the same checkpoint, freezes SAE parameters and activity buffers, and performs exactly one AdamW backbone update
Treatment: U1 = LM plus lambda=1 reconstruction gradient to the backbone
Control: U0 = LM-only backbone update with the same mediated forward
Changed variable: inclusion of the reconstruction objective in the backbone update
Held fixed: checkpoint, model forward, SAE weights/buffers, Top32 mask rule, batch, optimizer/scheduler state, clipping, weight decay, RNG, readout, and evaluation panels
Conditions: M2 10B primary; M2 15B registered sensitivity; M0/M1/M2 10B and 15B frozen N-report NLL; L1-L4 supplements as specified below
Pass: 10B primary 95% interval above zero, at least 3/4 batch directions positive, and all state/update guards pass
Fail: 10B primary 95% interval below zero with all guards passing
Insufficient: interval includes zero, fewer than 3/4 directions agree, or any identity, optimizer, freeze, normalization, or artifact guard fails
Cannot claim: long-run or from-scratch causal formation, general language ability, semantic feature identity, or that historical M2-M1 differences arise only from reconstruction gradients
Resource exception: h100-1-spot, at most one GPU-hour, explicitly inherited from the referenced execution card for this user-authorized scope; no fallback profile
```

Active Focus: `Projects/from-attention-to-search/main/focus/legacy/0915_focus_three_model_sae_representation_audit.md`. The Focus's pending local-gradient next decision is explicitly accepted by the researcher's current instruction. The 15B addition is a registered sensitivity and does not rewrite the completed E01 result.

## 1. Terminology And Definitions

- `h`: final block post-`norm2` state before the SAE.
- `actual`: SAE reconstruction consumed by the final MLP in M1/M2; equal to `h` in M0.
- `U0`: one backbone AdamW update using LM loss only.
- `U1`: the same update with the original lambda=1 normalized reconstruction term added.
- `local`: one 2,048-prediction-token batch, not the original 262,144-token effective training update.

## 2. Anchor Alignment And Hypothesis

The experiment tests the Anchor's unresolved rival that the added local reconstruction gradient may exist without producing useful held-out structure. If it supplies a favorable increment, U1 should lower the already-frozen P-report readout cross-entropy relative to U0 at the same M2 state. The strongest rival is an optimizer-scale or reconstruction-only change with no favorable independent readout effect.

The 15B checkpoint is not used to select the primary result. It tests whether the 10B local conclusion is checkpoint-specific. It cannot rescue a failed 10B primary result.

## 3. Blocks A-G

### A. Question And Claim Boundary — CONFIRMED

The allowed claim is only a one-step, state-local increment under the frozen readout. Historical trajectory causality, long-run benefit, and semantic mechanism remain outside scope.

### B. Data And Provenance — CONFIRMED

Reuse the exact P panel (360 rows, family-disjoint 120/60/180 fit/tune/report) and N M2D2 panel (600/200/400 fit/tune/report) from E01, including tokenizer, token windows, masks, four registered N-fit gradient batches, and sample IDs. Labels are used only for fitting/evaluation and never for the backbone update.

### C. Learning Task And Supervision — CONFIRMED

G1 updates only on next-token LM targets and self-reconstruction targets already present in M2. No P/N class label enters the update. P and N readouts are fitted before any update and then frozen.

### D. Model And Architecture — CONFIRMED

Use the existing eight-layer hidden-1024 M2 model with width-30,000 Top32 SAE at post-`norm2`/pre-MLP. Freeze all `sae.*` parameters plus `firing_counts`, `tokens_observed`, and `last_fired_at`. Preserve the mediated main forward in both conditions.

### E. Objective And Optimization — CONFIRMED

For each batch, LM is normalized by 2,048 valid targets and reconstruction by 256 registered SAE positions. U0 backpropagates LM only. U1 backpropagates LM plus lambda=1 reconstruction. AuxK is disabled in both arms because the SAE is frozen. Restore checkpoint AdamW moments, group hyperparameters, current learning rate, scheduler state, clipping=1.0, and weight decay. Each of the eight trials per checkpoint starts from the same state; trials never chain.

### F. Comparison And Decision Evidence — CONFIRMED

At 10B, compute per-report-example P readout cross-entropy for U0 and U1, average each example across four batch directions, then take class-balanced means. Bootstrap 5,000 times by the frozen P family/class strata. Positive `CE(U0)-CE(U1)` favors U1. Also report balanced accuracy, h/actual Fisher B and W separately, N readout replication, and N-report token-weighted NLL. Secondary metrics cannot rescue the primary result.

At 15B repeat the same complete matrix as a registered sensitivity. Report it separately; no pooled checkpoint p-value or post-hoc checkpoint selection is allowed.

### G. Execution And Reproducibility — CONFIRMED

Execution surface is ACP with `resource_profile: h100-1-spot`, `image_id: shphd-lite-0911`, one worker, one process, and a hard one-GPU-hour compute ceiling. The exact checkpoint manifests and state hashes are recorded before computation. New artifacts live under `/data/250010109/MoE_Router/experiments/20260916_sae_gradient_parameter_followup/`; source checkpoints and E01 artifacts are read-only. No fallback resource, new training, extra checkpoint, lambda sweep, longer update, commit, push, or publication is authorized.

## 4. Read-Only Supplements L1-L4

- **L1:** reuse E01 caches for 0--10B and collect the same P/N cache schema for 15B. For raw h and B3, report class-balanced between-class energy B, within-class energy W, and F=B/W separately. B3 fit mean/direction comes only from fit rows. Critical differences use the existing paired 5,000-draw rule.
- **L2:** compare 0B, 10B, and 15B physical parameters. Deduplicate tied embedding/output storage; report parameter count, parameter norm, absolute displacement, relative displacement where the initial norm is nonzero, and M2-M1 common-parameter distance normalized by the verified common-initial norm. SAE is separate.
- **L3:** for M1/M2 SAE decoder columns, report all 30,000 same-ID signed cosines/angles and raw column norms for 0-to-10B and 0-to-15B. Zero columns are separate. No cross-model matching or full Gram matrix.
- **L4/E:** audit existing 15B training-loss provenance and compute frozen M0/M1/M2 N-report token-weighted NLL at 10B and 15B. Bootstrap rows within the frozen fine-class strata using loss sums divided by valid-token sums. Report M2-M1, M1-M0, and M2-M0. No equivalence claim is allowed without a registered margin.

## 5. G0 Gradient Audit

For M2 10B and 15B, run the exact four N-fit batches. Save LM and reconstruction gradients at the h node and mutually exclusive backbone parameter groups: norms, RMS, cosine, active/outside-SAE-position support, and finite-value checks. Verify that reconstruction gradient is zero outside the 32 registered positions per row and that target/denominator remain detached. Do not compute a full Jacobian or spectrum.

## 6. G1 Frozen Analysis Plan

1. Fit P and N readouts on the untouched checkpoint using fit/tune only and freeze the selected C, scaler, coefficients, classes, and preprocessing.
2. For each of four batches and U0/U1, restore the same model/optimizer/scheduler/RNG state, verify frozen SAE identity, perform one isolated update, and save actual parameter deltas rather than learning-rate-times-gradient proxies.
3. Evaluate P report and N report after the update. Save per-example readout losses/predictions, Fisher B/W, token loss sums/counts, parameter-group delta norms, U1-U0 delta vectors summarized by group, and h/actual change norms. Delete trial models after summaries; do not save eight full checkpoints.

Missing or failed trials are not imputed. Any mismatch in pre-update model hash, optimizer step, tokens, parameter-group mapping, current LR, freeze state, batch IDs, or post-update SAE state makes the affected checkpoint `INSUFFICIENT`.

## 7. Stages And Stops

| Stage | Goal | Output | Gate / stop |
|---|---|---|---|
| S0 | Freeze identities and 10B/15B manifests | provenance JSON and hashes | mismatch stops affected condition |
| S1 | Local L1-L3 implementation/tests and dry run | tests, source manifest, resource tuple | failure stops submission |
| S2 | One fixed-batch GPU smoke at 10B | runtime, memory, gradient/freeze/update guards | any guard failure stops full matrix |
| S3 | L4/E and 15B cache collection | NLL tables, 15B caches | missing model or nonfinite value stops analysis |
| S4 | G0 at 10B/15B | h and parameter gradient tables | support/finiteness failure stops G1 |
| S5 | G1 at 10B/15B | eight isolated trials per checkpoint | no retries with changed scientific settings |
| S6 | CPU synthesis | tables, figures, receipts | incomplete lineage yields `INSUFFICIENT` |

## 8. Artifacts And Provenance

Expected outputs are `audit/`, `config/`, `tables/`, `figures/`, `runs/<run_id>/`, `acp_receipts/`, and a durable pod log. The implementation records source SHA256 values, checkpoint manifest SHA256 values, exact command, resolved execution tuple, image URL, peak memory, timing, and terminal status. Reader copies may be added to this experiment directory only after evidence is eligible.

## 9. Confirmation And Freeze Ledger

| Block | State | Grounding |
|---|---|---|
| A | CONFIRMED | Existing Focus/plan plus current researcher execution instruction |
| B | CONFIRMED | E01 frozen panels/splits and referenced prompt |
| C | CONFIRMED | Frozen G0/G1 card |
| D | CONFIRMED | Verified M2 source and checkpoint config |
| E | CONFIRMED | Frozen G1 card and checkpoint optimizer state |
| F | CONFIRMED | Frozen primary metric/branches; 15B added explicitly as sensitivity |
| G | CONFIRMED | Current instruction plus referenced one-H100-Spot, one-GPU-hour ceiling |

Cross-block audit: `PASS`. The treatment changes only the registered reconstruction-to-backbone objective; the readout is frozen before update; the 15B addition is separate and cannot alter the 10B primary verdict; artifacts and guards cover every registered branch.

Post-start amendments must append before/after values, reason, visible-data status, affected blocks, approval, and eligibility impact. The scientific body above is frozen once S2 begins.

## 10. Append-Only Amendments

### R001 — Reserved four-H100 resource replacement and completion supervision

```text
amendment time: 2026-09-16T07:06Z, before any GPU worker was allocated
before: h100-1-spot, one worker process, one-GPU-hour ceiling; bounded startup supervision
after: h100-4-reserved, one node with four H100 80GB GPUs; complete the Smoke first, then submit and supervise the full run to terminal state
reason: explicit researcher instruction to use four-card H100 Reserved and to complete Smoke plus supervise the full run
visible data before amendment: none; pt-vyrf07oi remained Pending/Starting with zero replicas, no pod log, and no scientific artifact
affected block: G execution/resource and monitoring only
unchanged: checkpoints, data, G0/G1 batches, objectives, optimizer semantics, 10B primary metric, 15B sensitivity, bootstrap, stop rules, and claim boundary
approval: HUMAN_CONFIRMED in the current task
eligibility impact: none; the stopped Spot job is scheduling evidence only and contributes no scientific result
supersedes: the h100-1-spot resource line in the approval snapshot and Block G
```

### R002 — G0 AuxK-mask call-contract repair

```text
amendment time: 2026-09-16T07:13Z, after Reserved Smoke failed before any optimizer update
before: G0 called the M2 forward without the required checkpoint-derived AuxK dead-feature mask
after: G0 passes model.sae.dead_feature_mask(model.config.sae_dead_tokens_threshold) unchanged into the forward; G0 still differentiates and reports only the registered LM and reconstruction components
reason: the M2 source rejects an AuxK-enabled forward without one boolean mask, even when the AuxK scalar is not a requested G0 gradient
visible data before amendment: exception only; no completed G0 batch, optimizer update, representation result, or scientific metric
affected block: G implementation guard only
unchanged: model state, mask definition, LM/reconstruction objectives and denominators, batches, primary metric, conditions, and claim boundary
approval: engineering repair within the already approved execution scope
eligibility impact: failed Smoke pt-mwjknz0d is INELIGIBLE for scientific claims; a fresh run root is required
```

### R003 — Frozen-NLL inference-context repair

```text
amendment time: 2026-09-16T07:26Z, after the first full attempt failed during frozen N-report evaluation and before any G1 optimizer update
before: the NLL helper consumed tensors created under torch.inference_mode outside an inference context while the output weight still carried its trainability flag
after: the same chunked linear projection and cross-entropy are evaluated inside torch.inference_mode with a detached view of the unchanged output weight
reason: PyTorch rejected saving an inference tensor for backward even though frozen NLL evaluation neither requests nor uses gradients
visible data before amendment: exception only; no completed cache set, G0 checkpoint result, G1 update, primary metric, or terminal receipt
affected block: S3 frozen-evaluation implementation only
unchanged: logits, targets, cross-entropy formula, chunking, model/checkpoint state, all G0/G1 conditions, primary metric, and claim boundary
approval: numerically equivalent engineering repair within the already approved execution scope
eligibility impact: failed full job pt-tthi96r1 and run root full_h100_4reserved_v1 are INELIGIBLE for scientific claims; a fresh run root is required
```
