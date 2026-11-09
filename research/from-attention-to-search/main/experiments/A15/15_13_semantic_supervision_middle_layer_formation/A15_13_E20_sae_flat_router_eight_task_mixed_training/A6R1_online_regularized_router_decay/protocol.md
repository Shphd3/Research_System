# A6R1: Lower, linearly decayed online SAE/GMM routing regularization

## 0. Read this first: purpose, scope and authorization

Document status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`. On 2026-09-09 the researcher judged the completed A6 constant structural coefficient `0.1` too high, set the new coefficient to `0.01` at update 1 and `0.001` at update 512, confirmed the previously proposed linear interpolation, authorized the same four-condition by three-seed full run, and required one reserved four-H100 node. Post-training stages S0--S6 remain unauthorized until this training item is reviewed.

Purpose: test whether the completed A6 failure was specific to sustained excessive structural pressure by repeating the same online four-arm comparison with a lower, monotonically decayed structural coefficient. Structural regularization still encourages tokens to follow their initial group structure while task gradients can change routing. This run does not prove that coefficient magnitude caused the old loss increase unless the matched new-versus-old contrast supports that reading.

Run four new conditions: `sae_a`, `gmm_a`, `sae_b`, `gmm_b`; each has seeds 17/29/43 and 512 updates (12 new trajectories). Reuse the three compatible A5 `task_only` trajectories. No random-feature, Dense, frozen-router, or combined A+B condition. If baseline equivalence fails, report the exact mismatch before adding any new baseline training or changing settings.

Primary outcome: final-checkpoint answer-token negative log likelihood on the existing full internal test. First deadline deliverable is all training plus this internal evaluation, not a full external generation benchmark. Proposed deadline interpretation: 2026-09-09 09:00 Asia/Shanghai = 01:00 UTC; it is a target, not a guaranteed ETA.

Resource contract: ACP only, one `n6ls.iu.i40.4` node in `share-space/share-cluster`, four independent H100 workers, `quota_type=reserved`, normal priority, and at most six allocated node-hours total including GPU smoke and full execution (24 GPU-hours). SPOT is forbidden for this run. Preserve all old runs, do not commit/push, and do not interfere with another task. No unlimited retries, sweeps or resource escalation.

## 1. Research alignment and what changed

The current [Anchor](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md) and [Focus](../../../../../focus/focus_sae_flat_router_functional_training.md) own the same online-routing question. Completed A6 is the immediate predecessor: all four constant-`0.1` arms were worse than task-only in all three seeds. This A6R1 run changes only the structural-weight schedule while preserving the teacher, scheme, initialization, data, optimizer, update count, and evaluation contracts.

The researcher explicitly selected this bounded rerun as the next decision. New A6R1 results remain unknown until all registered trajectories and evaluations complete. Do not invent a new independent problem or new Focus, and do not turn stale derived-view warnings into execution gates. After submission, stop for researcher review before any post-training S0--S6 analysis.

Hypothesis: lower early structural pressure followed by linear decay can preserve useful initial guidance without continuing to obstruct task adaptation. The strongest rival is that ordinary task-trained routing already suffices and the SAE/GMM structures remain unhelpful even at lower decaying weight. A/B compare two uses of the same teacher; SAE/GMM compare teacher constructions, not just clustering algorithms in isolation. Without a random control, do not claim that any gain uniquely requires semantic rather than generic regularization.

## 2. Exact inherited setup and source map

Read-only baseline run (`A5_RUN`):
`/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z`.

New execution workspace (`A6R1_ROOT`):
`/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay`.
It is independent of the completed A6 workspace. Each prepared run gets a unique directory under `A6R1_ROOT/runs/`; no old checkpoint is resumed.

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

For T in {S,G} use the corresponding detached q_t. Let N_M count valid structural positions across the complete effective batch. For one-indexed update \(u\in\{1,\ldots,512\}\), freeze the monotonically decreasing coefficient

\[\lambda_u=0.01+\frac{u-1}{511}(0.001-0.01).\]

Thus \(\lambda_1=0.01\) and \(\lambda_{512}=0.001\) exactly; there is no structural-weight warmup. The optimizer learning-rate warmup and cosine schedule remain unchanged:

\[R_A=\frac{1}{N_M}\sum_{t\in M}\sum_e q^T_{te}\log\frac{q^T_{te}}{p_{te}},\qquad L_u=L_{task}+\lambda_u R_A.\]

Use log_softmax(z), torch.special.xlogy or an equivalent zero-safe KL computation in float32. Evaluate p before balancing bias. No temperature, smoothing or sharpening: a target (0.9,0.1) encourages that preference; (0.5,0.5) remains ambiguous. Targets do not receive gradients.

Gradient accumulation: divide each microbatch's KL SUM by the effective-batch N_M, not by its own token count and then average 16 different means. Obtain this denominator from compact cached validity or rescale the accumulated structural router gradients separately after counting N_M. Keep task-gradient normalization unchanged. The structural term only updates router parameters, so separate accumulation buffers are a practical option; combine gradients before the same global clipping and optimizer step.

## 6. Scheme B: token-pair attraction and separation

Use the SAME teacher q and structural mask as A, but no fixed expert-ID alignment. For each microbatch choose at most K=256 eligible positions with a private deterministic generator keyed by (seed, update, microbatch); identical selection across SAE-B/GMM-B. If fewer exist, use all. Consider all distinct unordered pairs, excluding pairs from the same record, so a single long answer does not dominate pair relations.

For each eligible pair i,j define:

\[s_{ij}=\operatorname{clip}_{[0,1]}\frac{q_i^\top q_j}{\|q_i\|_2\|q_j\|_2},\quad d_{ij}=\sqrt{\|p_i-p_j\|_2^2+10^{-8}},\quad m=0.5.\]

This compares 8-dimensional group profiles, not raw 30,000-dimensional SAE features. Across all microbatches in the effective batch:

\[R_B=\frac12\left[\frac{\sum_{(i,j)}s_{ij}d_{ij}^2}{\sum_{(i,j)}s_{ij}}+\frac{\sum_{(i,j)}(1-s_{ij})\max(0,m-d_{ij})^2}{\sum_{(i,j)}(1-s_{ij})}\right],\qquad L_u=L_{task}+\lambda_uR_B.\]

Treat a zero denominator term as differentiable zero. Accumulate attractive/repulsive router-gradient sums separately and normalize with their respective effective-batch weight sums before combining; do not retain 16 backbone graphs, backpropagate through s, or average unequally sized microbatch ratios. The 1/2 factor balances the two relation types and is part of the definition. It is not a load-balancing loss.

Identical teacher profiles give s=1 and attract; orthogonal one-hot profiles give s=0 and repel until the margin. Global permutation of p's expert coordinates leaves R_B unchanged, unlike A. If profiles are all identical, B has no separation signal: report that failure instead of inventing negatives. Task loss and the inherited load bias remain the same. Do not add an A term to B.

The same frozen linear coefficient schedule applies to both schemes. Record the exact coefficient, task Router-gradient norm, structural Router-gradient norm, and combined norm at every update. This is one researcher-selected follow-up setting, not an automatic tuner or coefficient sweep, and it does not imply equal gradient pressure across schemes.

## 7. Implementation sequence and only necessary checks

1. Copy the completed A6 source into an independent A6R1 workspace. Preserve initial states, forward coefficient, sample schedules, teachers and all inherited task settings. Replace only the constant structural coefficient with the frozen linear schedule above, record its value per update, and retain trainable Routers in all arms.
2. Fit/save the token GMM once; reuse the SAE/groups. Add online targets, common masks, explicit effective-batch normalizations and private pair sampling. Implement task-only/no-regularizer mode in the new source for parity checking, not as a new full training condition.
3. Small local checks: p=q gives A approximately zero; an incorrect distribution gives larger A; B attracts matching profiles and repels orthogonal ones below margin; targets have no gradients and router does; frozen teachers stay unchanged. Compare accumulated versus unsplit gradients on a tiny synthetic effective batch. For teacher-GPU posterior compare with saved GMM. These are a compact test file, not a new audit project.
4. Exact intended runtime image: one fresh eight-update GPU smoke per new arm at seed 17, plus a two-update no-regularizer parity check against old task-only code on the same batches. Confirm finite task/structural losses, nonzero structural router gradient, post-first-update task-router gradient, changing router weights, unchanged teachers/backbone, correct mask and bias update. No short-run loss-improvement gate, clustering-bootstrap campaign, benchmark requalification, or offline-router retraining. Write one compact smoke receipt and proceed immediately on pass within the accepted scope.
5. Freeze source/config/teacher identity and submit the 12 trajectories on the reserved four-H100 tuple. Do not resume formal runs from smoke or old A6 checkpoints. On implementation failure fix the cause, rerun affected short checks, and resume only compatible A6R1 states. Do not silently alter objective, seeds, steps, precision or teachers to obtain a passing score.

Baseline reuse check is bounded: compare init tensors, data/schedule identity, optimizer groups/LR schedule, coefficient and bias semantics plus no-regularizer two-update parity. The new source hash will differ and is not itself disqualifying; preserve a separate baseline-equivalence record. Existing baseline results are known, so this is a follow-up on a reused internal test, not untouched confirmatory evidence.

## 8. Full-run scheduling, runtime and retention

Use the previously working ACP runtime image:
`registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`.
The only authorized resource is the reserved four-H100 tuple: ACP, `share-space`, `share-cluster`, `n6ls.iu.i40.4`, one node, four GPU processes, normal priority, `quota_type=reserved`. Do not submit SPOT, change another job, or silently switch resource class. Keep process-scoped runtime dependencies; do not install into shared base environments.

Four independent workers, each on one GPU; no cross-condition distributed gradient or load-count reduction. First wave: all four arms seed 17; next waves: seeds 29 and 43. Serialize a condition's optimizer/bias state; never combine partial states from different arms. Reuse the existing shell launch pattern after updating the matrix and new manifest checks.

Each trajectory saves initial state; update 128/256/384/512 checkpoints; recovery state every 64 updates; complete sample schedule, optimizer, load bias, losses and raw evaluations. Resume must preserve step, RNG/pair sampling and bias. Retain an input/source/teacher/config manifest plus a single job submission receipt. No copying unfiltered logs or checkpoints into Research_System.

Time allocation: target implementation plus CPU teacher preparation within 1–2 hours, then runtime smoke and full training/internal evaluation. These are planning targets, not measured durations. After the first 32 real updates, estimate remaining wall time from measured throughput, include development/test evaluation and leave margin for output writing. If the target morning time is at risk, notify with actual progress/ETA; keep running within the approved resource cap. Do not secretly reduce three seeds to one or 512 updates to fewer. Stop with recoverable state at the cap.

Use the product's supported monitor/wakeup mechanism if waiting must outlive an active task turn. Stay quiet when unchanged; notify only failure, required action, deadline risk, or completion. Do not end work at submission alone when the launch prompt asks for completed results.

## 9. Evaluation, reading and decision boundaries

Reuse the full internal evaluation implementation without changing its answer loss definition. Evaluate final update 512 on all 8,481 records, with frozen bias and no structural loss added to reported task NLL. Preserve per-record loss sums, answer counts, source and stable IDs. Full development curves at updates 0/128/256/384/512 remain available; no best-checkpoint selection. No fresh interventions or full external-generation benchmark are required for this overnight matrix.

Per model/seed: NLL=sum(answer loss)/sum(answer tokens), nats/token; not average record loss or average task means. Compare SAE-A versus GMM-A, SAE-B versus GMM-B, A versus B within each teacher, each new arm versus matched task-only, and each new arm versus its completed constant-`0.1` A6 counterpart. Show all three seed values, equal-weight seed mean and sample SD. Show paired differences by seed; do not pool record counts as extra training seeds or claim an optimal method after selecting the best of four scores.

Descriptive reading rule (AI_PROPOSAL): all three paired differences favoring one configuration = directionally consistent advantage under this configuration; any sign reversal = no stable ordering; incomplete/invalid trajectories = incomplete comparison. Equal values are ties. This is not a significance test, no multiplicity-adjusted population claim, and no inheritance of the old random-control PASS/FAIL rule. A tiny consistent change should be reported as tiny, not promoted into mechanism proof. Lower regularizer loss alone is not success; if none improves task-only consistently, report no demonstrated stable task benefit here.

Required artifacts after execution: a table of 12 new final trajectories plus three reused task-only baselines and the matched old A6 values; seed-level and mean/SD per-task NLL; task-loss curves with structural loss and the coefficient schedule shown separately; SAE/GMM, A/B, new-versus-task-only, and new-versus-old-A6 paired contrasts; completion/missing-run status. Create result `summary.md` and `detailed.md` beside this protocol only after measurement. This submission turn stops before result interpretation and before S0--S6.

Do not claim clean benchmark generalization, true semantic centers, causal feature disentanglement, superior expert utility under intervention, or broad superiority of SAE/GMM from this experiment. The absent random/Dense arms are deliberate user scope, not missing work to add overnight.

## 10. Approval and change ledger

- 2026-09-09: the researcher explicitly judged the completed A6 constant coefficient `0.1` too high and selected a follow-up with update-1 coefficient `0.01`, training-time decay, the same four arms and seeds 17/29/43, and a reserved four-H100 submission. The researcher required completion of this training-submission item and review before post-training S0--S6.
- 2026-09-09: after the implementation proposed a linear schedule, the researcher clarified that update 512 must equal `0.001` and directed work to continue. The registered schedule is therefore linear from `0.01` at update 1 to `0.001` at update 512, with no structural-weight warmup.
- HUMAN_CONFIRMED: audit blocks A--G and cross-block consistency `PASS`; same A6 model/data/teacher/schemes/three seeds/512 updates/internal evaluation, changed only structural-weight schedule; independent new run; one reserved `n6ls.iu.i40.4` four-H100 node; qualification-gated full execution; no S0--S6 in this turn.
- Execution approval: `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`. Passing local checks and a fresh four-arm GPU qualification are required before formal training submission. Ordinary correctness repairs may be made and rechecked without changing the registered schedule or scope.
- After execution starts, append receipts and any deviation with before/after values, reason, affected run IDs, and eligibility impact. Never rewrite completed A6 or its result records.
- Frozen scientific-body SHA256: `e7c82b675507b74d48afbc2b0566e2cfad86977ef832e02eba1b238169e30cdb`. The hash covers Sections 0--9 exactly and excludes this append-only ledger.
- 2026-09-09T01:51:51Z: reserved qualification job `pt-18rmehq3` started on the exact four-H100 tuple. Target-cache construction and zero-difference two-update task-only parity passed; all four eight-update training smokes completed with the registered decayed weights. The job then failed before smoke evaluation because checkpoint creation used the new A6R1 identity string while the copied evaluator retained the old A6 literal. No formal training was submitted and no failed-run checkpoint is eligible for reuse. The repair centralizes the identity string, adds a regression test, and requires a fresh qualification run.
- 2026-09-09T02:11:18Z: repaired reserved qualification job `pt-b5lg9vmt` completed `SUCCEEDED`. Two-update task-only parity again had zero adapter, optimizer, and history difference; all four eight-update train/evaluation smokes passed; update-1 structural weight was `0.01` and update-8 was `0.009876712328767124`. This is an operational qualification, not a scientific result.
- 2026-09-09T02:11:48Z: formal reserved ACP job `pt-b9r9id8m` was submitted for all four arms, seeds 17/29/43, 512 updates, fixed-checkpoint development evaluation, and full internal-test evaluation. No post-training S0--S6 stage is included.
- 2026-09-09T02:21:15Z: submission-health check found `pt-b9r9id8m` `RUNNING` on the exact approved ACP `share-space/share-cluster`, one-node `n6ls.iu.i40.4`, four-H100, `RESERVED`, normal-priority, retry-zero, six-hour tuple. The four seed-17 workers were at updates 459--474; every logged task/structural loss and Router-gradient norm was finite, every task and structural Router-gradient norm was positive, Router deltas were nonzero, structural-weight schedule error was at most `1.734723475976807e-18`, and all four had durable update-384 checkpoints. No failure artifact was present. Full operational snapshot: `/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/submission_health.json`. This is submission-health evidence only, not a completed result or scientific verdict.
- 2026-09-09T02:56:53Z: formal run `pt-b9r9id8m` produced the completion receipt for all 12 registered trajectories (four arms x seeds 17/29/43), each with 512 updates, and completed the registered full internal-test evaluation on 8,481 records / 562,954 answer tokens per condition-seed. The primary aggregate remains `AWAITING_RESEARCHER`; no S0--S6 stage was run. Completion and measurement sources: `/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/completion.json` and `results/aggregate.json`.
