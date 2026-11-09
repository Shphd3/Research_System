# Protocol: S7 single-branch acquisition and retention

## 0. Approval Snapshot

[中文](protocol_cn.md). Date: 2026-10-07, Asia/Shanghai.

| Field | Current contract |
|---|---|
| Document / scientific approval | **DRAFT_NOT_EXECUTABLE / awaiting researcher review** |
| Execution approval in this file | **None for formal training**; the separate [Smoke Protocol](smoke_protocol.md) has explicit Smoke-only authorization |
| Primary Anchor | [Single-branch retention Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_14_s7_single_branch_retention/17_14_s7_single_branch_retention_anchor.md), review draft |
| Confirmed purpose | Under the same training compute, improve new-task prediction while damaging old-task prediction less |
| Confirmed architecture family | Eight-layer fresh S7; fixed SAE; one insertion position; Dense one branch / MoE Top-1 selected expert; no added shared expert; old-task-used factors remain trainable |
| Active Focus | Current conversation explicitly activates this bounded question; stable Focus identity is pending review. No unrelated Focus is represented as its owner |
| Experiment role | Operationalization / proxy test: establish a sequential prediction-learning and damage phenomenon before mechanism analysis |
| Tested clause | MoE retention advantage conditional on non-inferior new learning and an eligible compute comparison |
| Primary outcomes | New-task held-out answer CE improvement, final new-task CE guard, and old-task CE increase, in nat / valid answer token |
| Scientific result state | **NOT RUN** |
| Block audit | A partially confirmed; B–G proposed or blocked; detailed ledger in §17 |
| Cross-block consistency | Draft reviewed for internal consistency; **promotion blocked** by unapproved margins, compute budget, split and training choices |
| Freeze | Formal scientific body not frozen; Smoke has its own freeze and receipts |

The purpose is to resolve whether a retention difference exists, not to show that SAE directions are harmful. The candidate hypothesis, data and technical settings below are complete review proposals. User approval of bounded engineering Smoke neither approves formal training nor fixes scientific thresholds.

## 1. Terminology / Definitions

A **LoRA branch** adds a scaled product of two trainable low-rank factors to one frozen linear projection. Dense uses one factor pair at all positions. MoE stores a bank of factor pairs; a **router** computes probabilities from the visible-prefix projection input and selects one expert per position. Selection does not assign one permanent expert to a dataset.

**Acquisition** is a task's fixed-heldout prediction-loss improvement during its own training stage. **Retention / damage** is the change in the same old-task loss while another task is learned; an increase means damage and a decrease is retained as improvement. **Teacher forcing** supplies preceding reference-answer tokens as context, then scores the next reference token. It measures prediction on those contexts, not independent answer generation.

The fixed **SAE** converts the Attention output to sparse coordinates and reconstructs it for analysis. Its weights, reconstruction loss and activations do not train the branch. **Direct task gradient** means the current minibatch derivative before optimizer state and weight decay; zero direct gradient does not imply zero parameter change.

## 2. Anchor Alignment

The Anchor's blocking uncertainty is the absence of an eligible current-architecture sequential comparison. The proposed first experiment learns GSM8K, then MMLU, measuring the same held-out sets at each boundary. A favorable result would establish a complete-architecture prediction-retention difference and justify a later mechanism test. It would not attribute the difference uniquely to routing.

The confirmed root purpose is preserved. Dataset choice, no replay, insertion point and the exact decision criteria are `AI_PROPOSAL`; the draft does not reset an existing research question or claim previous mixed training already answered this one.

## 3. Tested Hypothesis

At the registered stage-2 training-compute endpoint, MoE has a smaller old-task loss increase than Dense, while new-task loss improvement and final new-task loss satisfy their non-inferiority guards. Both arms must have learned the old task first, and Dense must show meaningful old damage before this is interpreted as mitigation of forgetting. Bigger improvement is not equal final quality when starting losses differ; retain both quantities.

Let \(G_{{\rm new},a}\) and \(F_{{\rm old},a}\) denote new improvement and old damage for arm \(a\). Define \(D_F=F_{{\rm old},Dense}-F_{{\rm old},MoE}\), and final new-quality gap \(Q_{\rm new}=L_{{\rm new},2,MoE}-L_{{\rm new},2,Dense}\), where positive \(Q_{\rm new}\) means MoE ends worse. Practical improvement, damage and both non-inferiority margins are **BLOCKED pending researcher judgment**, not estimated from Smoke effects.

## 4. Rival Explanations

| Rival | Registered guard | What remains unresolved |
|---|---|---|
| MoE learns the new task less | Minimum improvement plus non-inferiority guards for improvement and final loss | Margins must reflect meaningful prediction learning; CE is not generated-answer competence |
| Different compute or data exposure | Separate compute ledger and valid-input/target-token curves; equal global batch | Equal FLOPs may require different data exposure; it cannot silently be described as both equal compute and equal tokens |
| Different old-stage skill | Report identical base-checkpoint losses and each arm's stage-1 losses / acquisition | Post-training states cannot be identical across independently learned architectures; a large mismatch makes attribution insufficient |
| More stored capacity | Report total stored and per-position active trainable parameters | This two-arm comparison does not isolate routing from capacity |
| Selected-probability gate weakens updates | Record selected probability, branch displacement and factor-update norms | This diagnostic alone does not equate useful new-task learning or exclude optimization effects |

SAE overlap, representation distance and router usage are descriptive secondary records. They cannot rescue an unsupported primary result.

## 5. Data Construction And Provenance

**AI_PROPOSAL:** old task GSM8K, new task MMLU; reuse the audited answer-only post-training representation rather than synthetic math/physics templates. Candidate source is `/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/data/data.pt`, SHA256 `58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`. Its overall split inventory is train 39,571, dev 8,480, test 8,481 across eight tasks, not counts for these two tasks.

The cache's train/dev/test names are internal resplits, not official dataset splits; selected MMLU source IDs originate from its official test population. Deserializing the combined cache also loads its internal test container even when no internal-test records are selected. Do not claim official-test isolation or untouched benchmark truth from internal split names.

Before promotion, freeze a two-task manifest with source item IDs, task counts, question/answer fingerprints, selected splits, sequence lengths, valid-target counts, and transformations. Exact/normalized duplicates cannot cross training and evaluation; near-duplicate, source/pretraining overlap and previously exposed benchmark truth must be reported rather than called absent. Existing reports have used existing benchmark tests; their status is not automatically a new untouched confirmation set. The scientific evaluation-set provenance is **BLOCKED** until approved.

Train/dev/confirmation populations and sizes are proposed, not the 32/8 engineering subset. Use only train for gradients, only dev for any approved training choice, and freeze the primary heldout manifest and rule before any formal model losses. Direction selection or SAE-feature fitting is not part of this experiment. The two stages do not replay old training data in this first proposal. Replacing that choice reopens B, E and F.

## 6. Learning Task And Permitted Supervision

The model receives tokenized question/prompt and preceding reference-answer tokens. It predicts the next reference-answer token; prompt, padding and missing-target positions are ignored. Dataset identity is used for scheduling and reporting, not router input. No future answer token or task label enters the router.

Candidate tokenizer: the checkpoint's Qwen3 tokenizer identity, not pretrained Qwen3 weights. Candidate sequence cap: 512. Targets are already shifted: target at position \(t\) corresponds to token \(t+1\); final target and non-answer targets are `-100`. Audit shift, question/answer boundaries and whether truncation retains valid answers. Freeze an approved exclusion policy with per-task counts. No silent substitution of a short MMLU label for GSM8K reasoning tokens; report their different supervised lengths.

## 7. Model / Architecture And Frozen Variants

Backbone family and fixed analysis SAE are human-confirmed. **AI_PROPOSAL:** use the exact fresh S7 checkpoint at 33,000,000,000 pretraining tokens, not a 33-billion-parameter model: `/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000/state.pt`, SHA256 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`. Load only model and SAE weights; initialize a new optimizer for this post-training experiment.

The backbone has 281,431,040 parameters, eight blocks, hidden width 1024 and final Attention-projection input width 2048. The fixed SAE has 61,471,024 parameters, width 30,000 and Top-K 32. All backbone weights, norm, tied embedding/head and SAE weights are frozen throughout both stages. The SAE reads the modified Attention output after projection and before residual addition; it is detached from training and never replaces native activations.

Candidate insertion: `blocks[7].attn.o`; candidate rank \(r=8\), expert count \(E=8\), fixed scale \(s=1/8\). Dense computes \(W_Oc+sBAc\). MoE computes \(W_Oc+p_k sB_kA_kc\), with \(p=\operatorname{softmax}(Rc+b)\), \(k=\arg\max_jp_j\), and \(c\in\mathbb R^{2048}\). Retain selected probability; no shared expert, normalization-to-one or straight-through index estimator. Initialization proposal follows Smoke: input factors uniform on \([-1/\sqrt{2048},1/\sqrt{2048}]\), output factors zero; router weights normal with standard deviation 0.01, bias zero; first-index exact-maximum tie rule. Freeze the adopted rule in the final config. Only valid-answer positions contribute the registered CE gradient; routing a prompt position does not mean that position directly trains its expert.

Trainable factors: Dense \(A:8\times2048\), \(B:1024\times8\), 24,576 parameters. MoE eight pairs, 196,608 factor parameters, plus 16,392 router parameters, total 213,000. One factor pair is active per position in either arm; router computation and optimizer bank overhead differ. Both stages permit all factors and the MoE router to update. Do not freeze the experts that old samples used. Candidate bank storage is independent Parameters (`nn.ModuleList`): `grad=None` permits AdamW to skip an unselected expert, while an allocated zero gradient can still change it through moments/decay. This differs from the historical stacked bank; record direct-gradient support and actual increments separately.

Candidate precision follows the Smoke proposal, whose qualification is recorded separately: frozen backbone BF16, source SAE FP32, adapter/router FP32. Verify frozen-state identity against initial state at the same loaded precision. Real-arithmetic factor/SAE identities require an explicitly reported numerical tolerance under casts/addition; native activation and finite loss changes are measured directly. Do not identify these BF16 readings with the previous 1002 FP32 panel.

## 8. Training Objective And Optimization

The only proposed objective is summed next-reference-answer-token cross-entropy divided by the global valid-answer-token count across the whole completed accumulation window. Use natural logs; the mean is not a mean of unequal microbatch/rank means. SAE reconstruction, AuxK and load-balancing coefficients are zero / not part of the objective. Any addition reopens E and the claim.

Candidate AdamW: factor learning rate 2e-4, router rate 5e-4, betas (0.9, 0.999), epsilon 1e-8; factor weight decay 0.01, router decay zero; joint trainable-gradient norm clipped at 1. These are explicit post-training proposals adapted from E20, not inherited S7 pretraining settings. The formal learning-rate warmup/decay schedule, global batch and stage budgets are **BLOCKED** pending Smoke measurement and researcher review. The Smoke uses constant rates only for engineering qualification.

Propose continuity of factor/router optimizer state across the task boundary; no reset to suppress old-expert momentum. Checkpoints include factors, router, optimizer, schedule, RNG, data cursor, tokens and update counters. Completed accumulation windows advance the scientific token axis; skipped updates are recorded and cannot silently advance it.

## 9. Conditions, Seeds, And Checkpoints

Exactly two primary arms: one Dense rank-8 branch and one MoE eight-expert rank-8 bank with trainable Top-1 routing. Seed proposal: 17, 29, 43, paired by identical per-stage data schedules. That is six trajectories / twelve training stages, not twelve independent scientific seeds. No full-stage GPU resource or wall-time budget is approved here.

Save and evaluate the common zero-branch baseline, old-stage endpoint, and pre-registered stage-2 cumulative-target-token checkpoints. The primary comparison is the frozen compute endpoint; paired token curves are diagnostics. No best-confirmation-loss checkpoint selection. Exact checkpoint grid and budget rounding rules are **BLOCKED** before promotion.

## 10. Primary Metric And Frozen Analysis Plan

For task \(d\), checkpoint \(t\), arm \(a\), compute heldout loss

\[
L_{d,t,a}=\frac{\sum_{i,u}m_{i,u}[-\log P_{t,a}(y_{i,u}\mid X_{i,u})]}{\sum_{i,u}m_{i,u}}.
\]

Here \(i\) indexes the fixed question records, \(u\) answer prediction positions, \(m\) marks valid targets, and \(X\) contains only preceding tokens. Loss is empirical heldout total CE in nat / valid token, not training error or excess risk. Keep per-record loss sums and counts; compute the token-weighted mean, not an unweighted mean of record means.

Record \(G_{{\rm old},a}=L_{{\rm old},0,a}-L_{{\rm old},1,a}\), \(G_{{\rm new},a}=L_{{\rm new},1,a}-L_{{\rm new},2,a}\), \(F_{{\rm old},a}=L_{{\rm old},2,a}-L_{{\rm old},1,a}\), paired \(D_F\), and final new-quality gap \(Q_{\rm new}\) defined in §3. All before/after comparisons use identical question IDs and target masks. Negative damage is reported, not clipped to zero.

Uncertainty proposal: paired whole-question resampling, keeping all answer tokens of a question together; pair arms/checkpoints within each seed. Report each seed and paired seed differences separately. A proposed 95% whole-question interval is conditional on the trained states and does not replace training-seed uncertainty. The seed-level interval/test, resample count, multiplicity and exact one-/two-sided decision mapping are **BLOCKED** for researcher approval. There is one primary hypothesis; secondary descriptive coordinates cannot supply a post-hoc scientific victory.

Missing or failed arms make the primary comparison insufficient; no result-dependent seed replacement or outlier removal. Evaluate the frozen endpoint, not a retrospectively selected point. The practical minimum old acquisition, new acquisition, old damage, retention benefit, improvement and endpoint-loss non-inferiority margins, and tolerated start-skill mismatch are **BLOCKED**. Freeze them without viewing formal heldout effects; engineering Smoke magnitude cannot set them to favor either architecture.

## 11. Secondary Metrics And Guards

Record total/stored/active parameters, optimizer-state bytes, input and valid-answer tokens, sequence/padding counts, routed-position counts, expert direct-gradient norms and actual increments, selected probability, branch/output displacement norms, and measured runtime/memory. Enumerate full forward, downstream backward, router, active-factor and optimizer FLOP components with any profiler omissions. Wall-clock GPU time measures system efficiency, not an interchangeable scientific compute axis. The current Smoke records costs/exposure but does not provide a complete FLOP ledger; formal compute matching remains blocked.

For same fixed old records, save Attention-projection input \(c\), updated output \(a\), SAE code \(z\), reconstruction residual \(\varepsilon\), logits/loss sums and native-tail recomputation errors. Check \(\Delta a=D\Delta z+\Delta\varepsilon\), retaining SAE reconstruction quality before and after. This is an identity / analysis qualification, not proof of a harmful SAE subspace. Large sparse-code changes do not establish damage; large residual changes can expose an incomplete analysis tool.

There is no SAE direction-selection/removal/restoration scientific condition in this Protocol. If later proposed, candidate selection and efficacy data must be disjoint, with dimension/amplitude random controls and a separate parameter-realizability boundary.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: zero-initialized output factors reproduce the native frozen model; unchanged checkpoints yield zero loss/representation change. Known bad: a duplicated target shift, a non-answer target, leaked future token or SAE-loss gradient must be detected and stop eligibility.

Known confusing: initially zero output factors can give the router zero task gradient; this is expected, not failed routing. An unselected expert can have zero direct gradient yet change via AdamW state/decay. Different per-task token counts can move pooled CE without moving either registered task mean. These cases are checked in the independent Smoke, not assigned scientific outcomes.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How and why | Output / handoff |
|---|---|---|---|
| Data preflight | Correct source records and answer targets | Freeze fingerprints, split exclusions, masks and paired schedule to prevent leakage / reduction errors | Audited data manifest; stop on invalid target or unresolved evaluation lineage |
| Engineering qualification | Model, trainer and analysis are executable | Independent bounded Smoke; freeze gradients, native tail, valid-token counters and resume | Smoke receipts; failure blocks dependent full execution, success grants no full-run approval |
| Stage 1 | Establish old-task acquisition | Train each architecture on old train data to approved budget; evaluate both tasks on fixed heldouts | Full state and starting-loss table; insufficient acquisition blocks retention interpretation |
| Stage 2 | Observe new learning and old damage | Continue all trainable factors/router on new train data, no replay in proposed first setting | Registered checkpoints, new-learning / old-damage table; invalid compute or learning makes judgment insufficient |
| Primary analysis | Decide whether phenomenon warrants mechanism work | Apply frozen joint criterion and uncertainty rule before secondary interpretation | Complete result records and one bounded phenomenon judgment; no automatic new mechanism run |

## 14. Algorithm, Output, And Provenance Contract

Execution code/raw artifacts belong to `/data/250010109/MoE_Router/experiments/`; the exact formal execution root is `BLOCKED` until the formal scope is approved. Formal results belong beside this Protocol as Summary/Detailed bilingual records after actual execution. Do not prewrite them as results.

Each run saves Anchor/Protocol hashes, immutable code/config snapshot, checkpoint and SAE identities, tokenizer/data manifests, environment/image certificate, seeds, paired sampler/cursor, optimizer state and counters. Required training telemetry is owned by [the root observability contract](../../../../../../../docs/training_observability_contract.md): `run_root`, `tokens/train_lm_loss`, `updates/train_lm_loss`, `tokens/train_total_loss`, `updates/learning_rate`, `progress/tokens_seen`, `progress/optimizer_step`, `progress/effective_tokens_per_update`, all with their defined axes. No SAE objective component is registered; unused historical tags are not evidence of an active SAE loss.

Preflight must independently count valid targets for one full update, check monotonic token coordinates, finite tags and external-process recovery of both counters without overlapping steps. Stop on nonfinite loss/gradients, frozen-weight change, invalid target/schema, coordinate corruption, missing required artifact or approved resource ceiling. Preserve failure receipts; do not silently rerun into scientific eligibility.

## 15. Success / Failure / Insufficient Evidence

**Support:** approved compute and data guards pass; old-task acquisition and new-task acquisition satisfy their margins; Dense old damage is meaningful; MoE new improvement and final new loss meet both non-inferiority guards; registered uncertainty supports a practically meaningful positive \(D_F\).

**Non-support:** an otherwise eligible comparison reliably rules out that registered benefit. No old damage in this setting means the targeted forgetting phenomenon is not established; do not invent a negative architecture conclusion.

**Insufficient:** unapproved thresholds, invalid measurements, failed learning, unmatched compute, excessive start-skill mismatch, missing arms, or an interval crossing the registered boundary. Thresholds are currently unapproved, so this Protocol cannot produce an executable scientific verdict yet.

## 16. What This Cannot Claim

No causal attribution to routing versus stored capacity, gating or optimization. No universal sharing rule. No generation-competence claim from teacher-forced CE. No harmful common SAE subspace claim from overlap. No full-matrix-update equivalence for LoRA factors. No fixed old expert: every branch remains eligible for training. Smoke qualification is not scientific support and not formal-run authorization.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Grounded / confirmed | Proposed or blocked | State |
|---|---|---|---|
| A | Purpose and phenomenon-first route accepted in conversation | Primary scientific criterion and strongest-rival ranking | Partly confirmed / PROPOSED |
| B | Existing source identity available; engineering subset separate | Formal data populations, split eligibility, no replay | PROPOSED / BLOCKED |
| C | Prediction loss accepted as primary class; generation accuracy not mandatory | Exact answer view / exclusions and practical learning scale | PROPOSED |
| D | S7 + fixed SAE; one insertion; Top-1; no shared expert; no old-branch freeze | Exact checkpoint, insertion, rank/count, retained gate, initialization | PROPOSED |
| E | Only prediction learning required | AdamW proposal, schedules, batch and budgets | PROPOSED / BLOCKED |
| F | New improvement and old damage both needed | Margins, uncertainty, compute equivalence, endpoint and starting-skill guard | BLOCKED |
| G | Four reserved H100 Smoke explicitly authorized separately | Formal resources, cost ceiling, seeds and execution root | PROPOSED / BLOCKED |

2026-10-07: researcher requested Anchor/Protocol drafts and explicitly authorized training-plus-analysis Smoke on four reserved H100 GPUs. No formal run, commit/push or external publication is authorized by this request. These drafts record proposals, not an approved state transition.

Promotion requires researcher-confirmed A–G and cross-block consistency. Execution then requires the exact formal scope, separate from Smoke. At first authorized execution, freeze scientific body/config hashes and append subsequent material amendments with before/after, reason, visible evidence, affected blocks, authorization and eligibility impact. Never silently rewrite a running contract.
