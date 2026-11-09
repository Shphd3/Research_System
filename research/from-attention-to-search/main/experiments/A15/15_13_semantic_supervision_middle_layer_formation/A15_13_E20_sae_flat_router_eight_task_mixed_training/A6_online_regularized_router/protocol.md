# A6: Online SAE/GMM routing, fixed-target versus pairwise regularization

## 0. Read this first: purpose, scope and authorization

Document status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`. The online-training purpose and four-condition scope were HUMAN_CONFIRMED on 2026-09-08, and the researcher accepted the complete numerical-default bundle and implementation/smoke/full-run scope on 2026-09-08. The researcher's latest staging instruction limits the current execution checkpoint to implementation stages 1--3 and requires an audit before teacher fitting, GPU smoke, or full execution continues. That checkpoint does not alter the frozen design or silently narrow the approved eventual run.

Purpose: from identical router/expert initialization, test whether SAE or GMM structure gives better and more repeatable task learning when the router AND experts learn online. Structural regularization encourages tokens to follow their initial group structure while task gradients can change routing. It does not move frozen features or establish that a cluster is a true semantic class.

Run four new conditions: `sae_a`, `gmm_a`, `sae_b`, `gmm_b`; each has seeds 17/29/43 and 512 updates (12 new trajectories). Reuse the three compatible A5 `task_only` trajectories. No random-feature, Dense, frozen-router, or combined A+B condition. If baseline equivalence fails, report the exact mismatch before adding any new baseline training or changing settings.

Primary outcome: final-checkpoint answer-token negative log likelihood on the existing full internal test. First deadline deliverable is all training plus this internal evaluation, not a full external generation benchmark. Proposed deadline interpretation: 2026-09-09 09:00 Asia/Shanghai = 01:00 UTC; it is a target, not a guaranteed ETA.

Resource default for prompt acceptance: one four-H100 node, four independent single-GPU workers, at most six allocated node-hours total including GPU smoke and full execution (24 GPU-hours). Prefer one allocation with smoke then full training. Preserve all old runs, do not commit/push, and do not interfere with another evaluation task. No unlimited retries, sweeps or resource escalation.

## 1. Research alignment and what changed

The historical [Anchor](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md) and [Focus](../../../../../focus/focus_sae_flat_router_functional_training.md) describe the older frozen-router question. They are context, NOT approval of this online experiment. The researcher has now explicitly selected online joint training and removal of random/Dense controls. Do not carry the old random-control verdict rule into this experiment.

The experiment agent may, on the launch prompt's authorization, minimally align those current design references with this user-selected scope, preserving their historical evidence and leaving new results UNKNOWN. Do not invent a new independent problem or new Focus, and do not turn stale derived-view warnings into execution gates. The current next decision is which, if any, online-regularized configuration merits continued evaluation under this fixed budget.

Hypothesis: the initial structure can guide useful expert specialization without preventing task-driven adaptation. Rival: ordinary task-trained routing already suffices, or the structural constraint impedes task learning. A/B compare two uses of the same teacher; SAE/GMM compare teacher constructions, not just clustering algorithms in isolation. Without a random control, do not claim that any gain uniquely requires semantic rather than generic regularization.

## 2. Exact inherited setup and source map

Read-only baseline run (`A5_RUN`):
`/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z`.

New execution workspace (`A6_ROOT`):
`/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router`.
If it already exists, inspect its manifest and resume matching work; never overwrite unrelated work. Each new full run gets a unique directory under `A6_ROOT/runs/`.

Use `A5_RUN/source/model.py`, `train.py`, `data.py`, `cache.py`, `teacher.py`, `analysis.py`, `config.py`, `full_run.py`, `acp_full.sh` and its runtime wrapper as the implementation starting point. Copy needed source into the new workspace; do not edit frozen source or reuse old source-identity receipts to certify new code.

- Backbone: frozen Qwen3-0.6B-Base; zero-indexed layer 27 MLP pre-input h, dimension 1024, for router, teacher and expert. Backbone and language head remain frozen.
- Adapter: one shared rank-16 branch plus eight rank-16 experts, Top-1, scale 1/8. A matrices Kaiming initialized, B matrices zero. Same initialization order as A5 task-only.
- Router: linear 1024-to-8 with bias, 8,200 parameters; trainable in EVERY condition. No offline-fitted router initialization.
- Input: `A5_RUN/data/data.pt`, SHA256 `58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`. Preserve all splits, IDs, labels, truncation and answer masks. Full development has 8,480 records; internal test has 8,481.
- SAE: existing frozen 30,000-feature Top-32 model from A5 config; groups from `A5_RUN/groups/groups.pt`, key `sae`. Do not retrain SAE or regroup features.
- Training: AdamW, experts/shared LR 2e-4 with weight decay .01; router LR 5e-4 with weight decay zero. 26-update warmup then the existing cosine schedule, global gradient clipping 1.0, microbatch eight records, accumulation 16, effective batch 128, 512 updates. Preserve bfloat16 backbone and float32 adapter behavior.
- Seeds 17/29/43; use each A5 task-only seed's exact initial adapter/router state and full sample_schedule.pt. Initialize fresh optimizer state at update zero. Extra sampling uses a private generator, never the global training RNG.

## 3. Online routing and gradient contract

For token-position state h_t, compute z_t=W h_t+c and p_t=softmax(z_t). Dispatch k_t=argmax_e(z_te+b_e), then add S(h_t)+p_t,k_t E_k_t(h_t) to the MLP output. Preserve the unbiased selected coefficient; do not renormalize a singleton Top-1 coefficient to one or detach p_t.

Keep A5 load adjustment: count ALL nonpadding prompt/answer positions across one effective batch, then b_e <- b_e + .001 sign(mean(n)-n_e). b is a buffer, not an optimizer parameter; update once after optimizer.step, separately per condition. Freeze b at evaluation.

Task gradients reach shared/expert weights and router scores through the selected coefficient. The discrete argmax has no selection-index gradient; do not introduce straight-through estimators or soft all-expert training in only one condition. The structural loss reaches router W,c directly. Teacher targets and h are detached from teacher computation; p is not detached. The first task-only router gradient may be zero because expert B matrices start at zero; verify task gradients after an expert update, not solely on update zero.

## 4. Teacher targets: explicit token-level construction

Let M contain causal positions t where attention is valid and labels[t+1] != -100. Use h_t, never h_(t+1). The visible prefix may contain previous answer tokens under the same teacher-forcing task; the target token and future answer must not enter its teacher state. Structural loss is only on M; task loss uses all original answer targets. Both teachers use this position convention.

### 4.1 SAE target, shared by A and B

Compute frozen sparse activations a_t=Top32(ReLU(Encoder(h_t))). For retained group G_e:

\[u_{te}=\sum_{j\in G_e}a_{tj},\qquad q^{S}_{te}=u_{te}/\sum_r u_{tr}.\]

Use only retained features (the old group map can contain -1). Exclude zero-retained-mass positions from structural losses in ALL four conditions, so the structural mask is common. Do not exclude them from task loss. If an effective batch has no valid structural positions, R=0 with a differentiable zero attached to p; count this event. A smoke with no usable teacher targets is a failure.

### 4.2 GMM target, shared by A and B

This intentionally changes the old prompt-mean hard GMM into an initial TOKEN-level soft GMM. Do not apply old prompt-mean centers to token states and call the result an equivalent teacher.

Fit once before training, using only the existing router-fit half of the training split. Its cached h_t states exist at:
`/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z/cache/router/`.
The discovery cache contains incidence graphs, not token-state shards; do not assume it contains h_t. Check cached record IDs belong to the inherited training subset and verify model/data identity. Use uniform reservoir sampling over cached causal answer-prediction positions, at most 65,536 positions, private seed 17029. Use the sampled float32 states for PCA and GMM fitting. This is a frozen data-derived teacher, not an online GMM fit.

PCA: 64 components, no whitening, randomized solver, seed 17029. GMM: eight diagonal components, n_init=3, max_iter=100, tol=1e-3, reg_covar=1e-6, seed 17029. Retain the selected token IDs, PCA, mixture weights/means/covariances and convergence record. SAE/GMM use different teacher construction procedures/subsets within training; do not claim this isolates the clustering algorithm alone.

With v_t=PCA(h_t), use the numerically stable posterior:

\[q^G_{te}=\operatorname{softmax}_e\left[\log\pi_e-\frac12\sum_d\left(\log\sigma_{ed}^2+\frac{(v_{td}-\mu_{ed})^2}{\sigma_{ed}^2}\right)\right].\]

Implement this as frozen float32 tensor arithmetic on GPU for online target creation; check several predictions against the saved mixture's predict_proba. No learned mixture parameters, temperature change, hard-label conversion or target sharpening. Reuse exactly the same fitted teacher for GMM-A, GMM-B and all seeds. Stop on nonfinite/invalid posterior, nonconvergence or effectively constant targets across the smoke sample; do not add a teacher search overnight.

### 4.3 Practical target computation

Because the backbone is frozen and the adapter is injected after this final-layer h_t, targets do not change during training. The simplest implementation computes both teachers under no_grad on the selected structural positions of the current microbatch; run the large SAE encoder in chunks of at most 256 positions to bound memory. Compute the common validity mask for every condition, including GMM. No 30,000-dimensional pairwise matrices are needed.

Caching is optional, not a prerequisite: cache compact q vectors and validity only when it reduces measured runtime, keyed by data ID/position/teacher identity. Do not re-forward the full backbone merely to obtain targets already available from the hook. Never read development or test states to fit either teacher.

## 5. Scheme A: fixed-group alignment

For T in {S,G} use the corresponding detached q_t. Let N_M count valid structural positions across the complete effective batch:

\[R_A=\frac{1}{N_M}\sum_{t\in M}\sum_e q^T_{te}\log\frac{q^T_{te}}{p_{te}},\qquad L=L_{task}+0.1 R_A.\]

Use log_softmax(z), torch.special.xlogy or an equivalent zero-safe KL computation in float32. Evaluate p before balancing bias. No temperature, smoothing or sharpening: a target (0.9,0.1) encourages that preference; (0.5,0.5) remains ambiguous. Targets do not receive gradients.

Gradient accumulation: divide each microbatch's KL SUM by the effective-batch N_M, not by its own token count and then average 16 different means. Obtain this denominator from compact cached validity or rescale the accumulated structural router gradients separately after counting N_M. Keep task-gradient normalization unchanged. The structural term only updates router parameters, so separate accumulation buffers are a practical option; combine gradients before the same global clipping and optimizer step.

## 6. Scheme B: token-pair attraction and separation

Use the SAME teacher q and structural mask as A, but no fixed expert-ID alignment. For each microbatch choose at most K=256 eligible positions with a private deterministic generator keyed by (seed, update, microbatch); identical selection across SAE-B/GMM-B. If fewer exist, use all. Consider all distinct unordered pairs, excluding pairs from the same record, so a single long answer does not dominate pair relations.

For each eligible pair i,j define:

\[s_{ij}=\operatorname{clip}_{[0,1]}\frac{q_i^\top q_j}{\|q_i\|_2\|q_j\|_2},\quad d_{ij}=\sqrt{\|p_i-p_j\|_2^2+10^{-8}},\quad m=0.5.\]

This compares 8-dimensional group profiles, not raw 30,000-dimensional SAE features. Across all microbatches in the effective batch:

\[R_B=\frac12\left[\frac{\sum_{(i,j)}s_{ij}d_{ij}^2}{\sum_{(i,j)}s_{ij}}+\frac{\sum_{(i,j)}(1-s_{ij})\max(0,m-d_{ij})^2}{\sum_{(i,j)}(1-s_{ij})}\right],\qquad L=L_{task}+0.1R_B.\]

Treat a zero denominator term as differentiable zero. Accumulate attractive/repulsive router-gradient sums separately and normalize with their respective effective-batch weight sums before combining; do not retain 16 backbone graphs, backpropagate through s, or average unequally sized microbatch ratios. The 1/2 factor balances the two relation types and is part of the definition. It is not a load-balancing loss.

Identical teacher profiles give s=1 and attract; orthogonal one-hot profiles give s=0 and repel until the margin. Global permutation of p's expert coordinates leaves R_B unchanged, unlike A. If profiles are all identical, B has no separation signal: report that failure instead of inventing negatives. Task loss and the inherited load bias remain the same. Do not add an A term to B.

The fixed coefficient .1 for both schemes is an overnight engineering default, not a claim that they exert equal gradient pressure. Record task and structural router-gradient norms at the smoke and a few training checkpoints; no automatic tuning, no lambda grid, and no optimum-method claim from this single setting.

## 7. Implementation sequence and only necessary checks

1. Create a new execution source/config. Remove new arms from FROZEN_ROUTER_ARMS; include their router in the same optimizer group as task-only. Preserve initial states, forward coefficient, sample schedules and all inherited task settings. Add teacher preparation and pure A/B loss functions; do not invoke old offline fit_router or the old five-arm pipeline.
2. Fit/save the token GMM once; reuse the SAE/groups. Add online targets, common masks, explicit effective-batch normalizations and private pair sampling. Implement task-only/no-regularizer mode in the new source for parity checking, not as a new full training condition.
3. Small local checks: p=q gives A approximately zero; an incorrect distribution gives larger A; B attracts matching profiles and repels orthogonal ones below margin; targets have no gradients and router does; frozen teachers stay unchanged. Compare accumulated versus unsplit gradients on a tiny synthetic effective batch. For teacher-GPU posterior compare with saved GMM. These are a compact test file, not a new audit project.
4. Exact intended runtime image: one fresh eight-update GPU smoke per new arm at seed 17, plus a two-update no-regularizer parity check against old task-only code on the same batches. Confirm finite task/structural losses, nonzero structural router gradient, post-first-update task-router gradient, changing router weights, unchanged teachers/backbone, correct mask and bias update. No short-run loss-improvement gate, clustering-bootstrap campaign, benchmark requalification, or offline-router retraining. Write one compact smoke receipt and proceed immediately on pass within the accepted scope.
5. Freeze source/config/teacher identity and submit the 12 trajectories. Do not resume formal runs from smoke checkpoints. On implementation failure fix the cause, rerun affected short checks, and resume only compatible states. Do not silently alter objective, seeds, steps, precision or teachers to obtain a passing score.

Baseline reuse check is bounded: compare init tensors, data/schedule identity, optimizer groups/LR schedule, coefficient and bias semantics plus no-regularizer two-update parity. The new source hash will differ and is not itself disqualifying; preserve a separate baseline-equivalence record. Existing baseline results are known, so this is a follow-up on a reused internal test, not untouched confirmatory evidence.

## 8. Full-run scheduling, runtime and retention

Use the previously working ACP runtime image:
`registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`.
Resource default is the inherited reserved four-H100 profile `n6ls.iu.i40.4` in `share-space/share-cluster`; the execution agent must resolve current availability and mounts using its normal SCO skill. Do not change another job or silently switch resource class. Keep process-scoped runtime dependencies; do not install into shared base environments.

Four independent workers, each on one GPU; no cross-condition distributed gradient or load-count reduction. First wave: all four arms seed 17; next waves: seeds 29 and 43. Serialize a condition's optimizer/bias state; never combine partial states from different arms. Reuse the existing shell launch pattern after updating the matrix and new manifest checks.

Each trajectory saves initial state; update 128/256/384/512 checkpoints; recovery state every 64 updates; complete sample schedule, optimizer, load bias, losses and raw evaluations. Resume must preserve step, RNG/pair sampling and bias. Retain an input/source/teacher/config manifest plus a single job submission receipt. No copying unfiltered logs or checkpoints into Research_System.

Time allocation: target implementation plus CPU teacher preparation within 1–2 hours, then runtime smoke and full training/internal evaluation. These are planning targets, not measured durations. After the first 32 real updates, estimate remaining wall time from measured throughput, include development/test evaluation and leave margin for output writing. If the target morning time is at risk, notify with actual progress/ETA; keep running within the approved resource cap. Do not secretly reduce three seeds to one or 512 updates to fewer. Stop with recoverable state at the cap.

Use the product's supported monitor/wakeup mechanism if waiting must outlive an active task turn. Stay quiet when unchanged; notify only failure, required action, deadline risk, or completion. Do not end work at submission alone when the launch prompt asks for completed results.

## 9. Evaluation, reading and decision boundaries

Reuse the full internal evaluation implementation without changing its answer loss definition. Evaluate final update 512 on all 8,481 records, with frozen bias and no structural loss added to reported task NLL. Preserve per-record loss sums, answer counts, source and stable IDs. Full development curves at updates 0/128/256/384/512 remain available; no best-checkpoint selection. No fresh interventions or full external-generation benchmark are required for this overnight matrix.

Per model/seed: NLL=sum(answer loss)/sum(answer tokens), nats/token; not average record loss or average task means. Compare SAE-A versus GMM-A, SAE-B versus GMM-B, A versus B within each teacher, and each new arm versus matched task-only. Show all three seed values, equal-weight seed mean and sample SD. Show paired differences by seed; do not pool record counts as extra training seeds or claim an optimal method after selecting the best of four scores.

Descriptive reading rule (AI_PROPOSAL): all three paired differences favoring one configuration = directionally consistent advantage under this configuration; any sign reversal = no stable ordering; incomplete/invalid trajectories = incomplete comparison. Equal values are ties. This is not a significance test, no multiplicity-adjusted population claim, and no inheritance of the old random-control PASS/FAIL rule. A tiny consistent change should be reported as tiny, not promoted into mechanism proof. Lower regularizer loss alone is not success; if none improves task-only consistently, report no demonstrated stable task benefit here.

Required morning artifacts: a table of 12 new final trajectories plus three reused task-only baselines; seed-level and mean/SD per-task NLL; task-loss curves (structural losses shown separately); SAE/GMM and A/B paired contrasts; completion/missing-run status. Create result summary.md and detailed.md beside this protocol after measurement, clearly labeling AI interpretation and leaving human-owned mechanism judgment/next transition unconfirmed. Link plots near the claims they support.

Do not claim clean benchmark generalization, true semantic centers, causal feature disentanglement, superior expert utility under intervention, or broad superiority of SAE/GMM from this experiment. The absent random/Dense arms are deliberate user scope, not missing work to add overnight.

## 10. Approval and change ledger

- 2026-09-08: user confirmed the routing-alignment purpose; requested explicit A and B implementations, memory and an agent launch prompt to train four missing conditions and submit full run for next-morning results. This turn writes the requested documents, not the implementation.
- HUMAN_CONFIRMED: online router/expert training; identical initialization; four new SAE/GMM × A/B conditions; no random/Dense; concise checks; next-morning result intent.
- AI_PROPOSAL defaults accepted as one bundle by the launch prompt: 3 seeds × 512 steps; .1 coefficient; token-level GMM fit on the training-only cached subset; unsharpened targets; B pair sampling/margin/normalization; baseline reuse conditions; internal evaluation as overnight deliverable; four H100/six-node-hour cap and timezone interpretation.
- When the researcher sends the launch prompt accepting this document, the agent records `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`, approval time and frozen protocol hash here. No separate repeated approval questions for A–G. Material deviations outside the accepted document still need direction; ordinary implementation fixes do not.
- After execution starts, append changes with before/after, reason and affected run IDs; never silently rewrite this body or old A5. No observed result belongs in the pre-run scientific body.
- 2026-09-08T17:05:56Z: the researcher accepted the complete A6 default bundle and authorized implementation, necessary smoke, the four-condition by three-seed full run, internal evaluation, and result records under the stated four-H100 / six-node-hour ceiling. Audit blocks A--G are `CONFIRMED`; cross-block consistency is `PASS`; the approved scope is `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`.
- 2026-09-08T17:05:56Z execution checkpoint: complete authorization recording, isolated A6 workspace creation, and implementation source only, then stop for researcher audit. Token sampling/GMM fitting, baseline parity execution, GPU smoke, job submission, training, and evaluation remain `NOT_STARTED` at this checkpoint.
- Frozen scientific-body SHA256: `9bd54f34371ef3e4bace0c40ecaa035ff3d185f6bbe05ea0349073bfb3a708c9`. The hash covers Sections 0--9 exactly and excludes this append-only approval/change ledger, so later receipt links do not rewrite the frozen design identity.
- 2026-09-08T17:52:36Z: after auditing the staged work and risks, the researcher explicitly lifted the stage-1--3 checkpoint and directed completion of the entire approved plan. Execution may proceed through implementation, authenticated task-only parity, all four eight-update GPU smokes with evaluation, and the four-arm by three-seed full ACP run. Full submission remains gated on a passing smoke receipt; correctness failures are repaired and rechecked rather than bypassed, and the frozen arms, seeds, 512 updates, internal evaluation, and task-only comparison remain unchanged.
- 2026-09-08T18:42:20Z: run `full-20260908T183139Z` passed ACP qualification job `pt-80s7l3fm`: exact two-update task-only parity had zero adapter, optimizer, and history difference; all four eight-update smoke/evaluation gates passed; the authenticated common target cache covers 2,617,687 training positions. This is an operational qualification, not a scientific result.
- 2026-09-08T18:48:12Z: formal ACP job `pt-jn404t7l` was submitted with the frozen 12-trajectory matrix and was RUNNING on the approved reserved 4-H100 tuple. All four seed-17 arms had exceeded update 32 (updates 134--144) with finite gradients, changing Routers, and update-64 recovery checkpoints. Estimated completion 19:25--19:40 UTC is an engineering projection from observed throughput, not a result verdict.
- 2026-09-08T19:32:25Z: formal ACP job `pt-jn404t7l` completed `SUCCEEDED` with zero retries. All 12 registered trajectories reached update 512; 60 fixed-checkpoint development evaluations and 12 full new-arm internal-test evaluations completed. Independent post-run pairing, coverage, hash, finite-value, gradient, and aggregation checks passed. The [Summary](summary.md) and [Detailed](detailed.md) records preserve the registered direct reading and remain `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`; this receipt does not make a human-owned mechanism judgment.
