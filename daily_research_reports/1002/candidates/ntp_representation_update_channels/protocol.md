# Candidate Protocol: Common and specialized computation in sequential natural-text learning

Revision: 2026-10-03 capacity-r1. Temporary candidate. Owner: [Anchor](anchor.md). Old experiment contracts remain in [history](history/20261002_before_capacity_refinement/reading/protocol.md). This is one six-condition comparison family and its checkpoint intervention analysis.

## 0. Approval Snapshot

`APPROVED_FOR_BOUNDED_STAGED_EXPLORATION` by the researcher's explicit 2026-10-03 instruction at 04:14:29 UTC: continue approximately 2.5 hours, choose small/approximately 300M eight-layer training as needed, use only 8×RTX5090 SPOT, deepen and repeatedly audit the reasoning, retain temporary artifacts, and do not request further approval. [Verbatim receipt](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/receipts/user_authorization.json). AI-selected choices below are delegated exploratory choices, not individually researcher-certified hypotheses or confirmation thresholds. `question_state=OPEN`; scientific closure and practical-quality threshold remain `Unknown`.

## 1. Terminology / Definitions

Common C: always-used per-layer FFN. Private E_d: per-layer FFN selected by the known text domain. Trunk T: all other parameters, including tied embeddings/output weights, additive domain embeddings, attention and norms. Domain IDs: 0 computer science, 1 mathematics, 2 physics, 3 biology. No learned router. A valid token means one observed next-token target; 257 stored tokens create 256 targets. Exposures include revisits and are not unique data volume.

## 2. Anchor Alignment

Evaluate whether common processing and its serial composition improve finite learning/retention under limited private widths. Do not gate this on prior representation prediction. Results refine the same question; no formal Focus, project migration or scientific state closure is authorized by implementation completion.

## 3. Tested Hypothesis

H1 parallel shared computation improves resource efficiency relative to matched-initial-function private_active. H2 serial improves finite learning/retention relative to parallel. H3 measured old-domain drift can be located to common and/or trunk changes with unchanged old experts. Direction is not pre-assumed. The primary outcome is a vector of acquisition, retention, final losses and resource coordinates, not a single method-goodness verdict.

## 4. Rival Explanations

Track undertraining, budget imbalance, shared-trunk drift, order, initial-function mismatch, depth and optimization, domain labels, data overlap, and old-expert optimizer drift. No depth-matched serial control is included; any serial advantage retains that rival. Two blocks confound seed with order by design and cannot estimate their independent effects.

## 5. Data Construction And Provenance

Source: local `m2d2_paired_dev_v1` archives, official train.txt/valid.txt/test.txt members, categories cs.CL/cs.CV, math.AP/math.NT, physics.optics/physics.flu-dyn, q-bio.GN/q-bio.NC. Qwen3 tokenizer at `/data/share/Qwen3-0.6B-Base`; no special tokens; require at least 257 tokens and retain the first 257. Each category supplies 8192 train, 128 dev and 128 test records. Per domain: 16384 train and 256 each dev/test. Total unique selected train target positions: 16,777,216; total selected records including evaluation: 67,584.

Selection priority is fixed test→dev→train, with global exact full-text and 257-token deduplication, plus exclusion of prior 0930/1002 evaluation panels from current dev/test by full-text and 256-token prefix. No article identity or near-duplicate guarantee is available. Candidate pools expand independently of model outcomes by registered counts/length eligibility. Before any training, insufficient math.AP dev/test and math.NT test pools required scanning their full fixed 5 MB source members. The original failed attempt and data-only amendment are retained. This does not change quotas or select using loss.

Frozen NPZ: [capacity_data.npz](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/data/capacity_data.npz), SHA256 `6ed1bdb93e9734682c2c46338c06303239638eee48e53d6b310bab669c4a7331`. [Manifest](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/data/manifest.json) SHA256 `ea4e6f12d6d413653006391f88bca4dc707c9956d5dde611d802d336c58cded6`; selected record/source hashes and independent 24-record re-tokenization check are retained. Test is evaluated only at the final fixed endpoint and is not used for arm or checkpoint selection.

## 6. Learning Task And Permitted Supervision

Causal NTP on 256 targets per record, record-level fixed domain routing. All targets participate in unregularized CE. Training can use domain IDs and next-token targets. Evaluation uses known domain identity, never the target to choose an expert. No auxiliary losses, SAE, teacher, distillation, replay after the mixed phase, or pretrained weights.

## 7. Model / Architecture And Frozen Variants

Eight native Qwen-style layers: hidden size 256, 4 Q heads, 2 KV heads, head dimension 64, context 256, vocabulary 151936, tied embedding/head and an additive 4×256 domain embedding in every arm (included in trunk; Dense receives the same domain information), RMSNorm epsilon 1e-6, RoPE theta 1e6, SwiGLU, no dropout. Common width 256, private width 384, four experts. Attention/RMS/SwiGLU definitions are adapted from the inspected 20260913 dense baseline; [reuse decision](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/reuse_decision.json) records hashes. The new code only adds experimental composition, fixed-domain selection and measurement logic.

| Arm | Per-layer FFN | Total width | Active width |
|---|---|---:|---:|
| common_parallel | C(z)+E_d(z) | 1792 | 640 |
| common_serial | C(z)+E_d(z+C(z)) | 1792 | 640 |
| private_active | E_d(z) | 2560 | 640 |
| private_total | E_d(z) | 1792 | 448 |
| dense_active | D(z) | 640 | 640 |
| dense_total | D(z) | 1792 | 1792 |

The attention residual is added outside each expression. Serial has a longer dependency chain; nominal FFN operation equality does not imply equal latency. Whole-model counts are measured and saved, including the large shared vocabulary embedding. Name/shape/seed initialization keeps every trunk tensor identical within a block. common arms share identical C/E initial tensors. Each private_active expert concatenates copied C channels and its corresponding E channels in gate/up rows and down columns, matching the initial common_parallel function up to floating-point summation. Other references are not initially function-matched.

## 8. Training Objective And Optimization

Token-weighted mean CE in natural-log units, no regularization components (`NOT_APPLICABLE`). AdamW beta=(0.9,0.95), LR 3e-4, linear 256-update warmup then cosine to 3e-5 at the fixed endpoint; weight decay 0.1 and gradient clipping 1. BF16 autocast with FP32 master parameters/optimizer, no dropout. Fixed batch 32 sequences ×256 targets=8192 targets/update, microbatch 8, accumulation 4, DP world size 1 per condition. CE chunks 512; actual model-specific memory/throughput and any implementation-preserving Smoke amendment must be recorded before full training. Nonfinite updates fail explicitly; no silently skipped coordinate changes.

512 mixed updates (8 records/domain per update), then 1024 updates per domain in the block's order. Total 4608 updates=37,748,736 exposures per trajectory. Data cursors permute deterministically and record revisit cycles. Every arm in a block sees identical records/token order. The endpoint is fixed, not chosen by the lowest loss. The initial 1152-update draft was expanded before training after the undertraining audit; no result selected the increase.

Mixed warmup exposes each domain to4096 records/1,048,576 targets. Own-phase gain measures additional specialized learning of already-seen domains, not first encounters with unseen domains.

## 9. Conditions, Seeds, And Checkpoints

Twelve trajectories: six arms × block A `(seed=1003, order=0,1,2,3)` and block B `(seed=1004, order=3,2,1,0)`. Keep init, mixed-end, and all four phase-end checkpoints. Periodic checkpoints every 512 updates retain the latest two. Save full model, optimizer, update/tokens, data cursor/order/cycles, RNG, config and source identities atomically. One writer lock per run. Exact same-config resume is permitted after SPOT interruption; the same resource profile is required. Restore logging coordinates without duplicate conflicting rows.

## 10. Primary Metric And Frozen Analysis Plan

Evaluate all four dev domains at init, every 512 updates, mixed-end and every phase end. Store token-summed CE and valid counts for every evaluation; the rollback analysis additionally saves per-record CE. Primary fixed comparisons: serial−parallel; parallel−private_active; each common arm−dense_total; report private_total and dense_active reference gaps on their own resource axes. Report both blocks separately and their descriptive mean. No independently powered significance claim from n=2 training blocks.

For domain d in its own phase: learning gain = loss immediately before minus loss immediately after. Forgetting at later stage s = loss at s minus loss immediately after its own phase, preserving signed improvements. Report the full 4×stage matrix, final equal-domain macro dev/test CE and per-domain gaps. No post-hoc “equivalent to Dense” threshold; practical equivalence is `Unknown`.

## 11. Secondary Metrics And Guards

For every phase on a private/common arm, hash the parameters AND optimizer states of every nonselected expert before/after; require exact equality. They must receive grad=None so AdamW neither decays weights nor updates momentum. Common/trunk gradients remain allowed. Unselected domain-embedding rows may still change through AdamW momentum/decay; this belongs to T. Frozen old experts do not imply that all parameters used by an old domain are frozen. Log actual tokens/update, loss, LR, gradient norm, peak allocated/reserved memory, wall time, valid tokens/s and all required TensorBoard coordinates under the repository observability contract. TB `tokens/train_lm_loss` and `tokens/train_total_loss` use cumulative valid targets; `updates/train_lm_loss` uses optimizer updates. No inactive module is executed via a zero-gradient anchor.

For old domain i whose own single-domain phase has already ended, during a later phase, use common/trunk 2×2 rollback on its fixed dev records and unchanged expert. Save L00,L10,L01,L11, interaction, phi_C,phi_T and additive residual. Private-only references need only trunk rollback; Dense has no frozen old expert, so do not interpret it with that condition. The mixed phase is not an old-task forgetting phase. This is a finite parameter intervention, not an on-trajectory causal learning decomposition.

## 12. Known Good / Known Bad / Known Confusing Cases

Good implementation controls: common_parallel/private_active initial function agreement; nonselected expert model/optimizer equality; exact resume versus uninterrupted two-step updates; correct 8192-target count; finite loss/gradients and actual TensorBoard file/tags. Bad: any failed guard, mismatched data/config/source identity, nonfinite loss or OOM. Confusing: serial wins only final aggregate while one old domain worsens; common contribution is helpful but trunk causes net harm; a Dense gap shrinks only with more compute. Report those coordinates rather than converting them to one verdict.

## 13. Scientific Procedure And Stage Contracts

1. Freeze data, code/config identities and this contract. Run local tiny implementation tests.
2. Submit one explicitly staged 8×RTX5090 SPOT allocation. Activate the mounted SM120-compatible Torch 2.8/cu128 layer without changing the base image. Verify eight RTX5090 devices and BF16 execution.
3. Exact-shape Smoke all six arms, verify loss/count/TB/checkpoints and resume. Full trajectories are programmatically blocked unless every gate passes. Smoke is not scientific support.
4. Schedule twelve fixed trajectories over the eight GPUs. A trajectory has a 5400-second bound; if interrupted/bounded before 4608, record incomplete and resume from full state rather than compare it as a final result. No silent budget reduction for a slow arm.
5. Validate endpoints and guards, evaluate rollback, audit competing explanations, update factual records. User-requested research continues approximately until 06:44 UTC; any still-running job is reported with verified state, not invented completion.

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity`. Preserve data/selection manifests, source/config freeze manifest, submit receipt, durable pod log, hardware preflight, Smoke report, per-condition config, metrics JSONL, TensorBoard events, parameter counts, evaluations, guard records, checkpoints and final status. Root scripts orchestrate only this experiment. Scientific tables copied into the temporary bundle require their source and SHA256 in the payload manifest. No raw datasets/checkpoints enter Research_System. No commit, push, publication or formal-project move is requested.

## 15. Success / Failure / Insufficient Evidence

Exploratory support: a prespecified comparison improves its relevant losses consistently across both blocks, with intact guards; resource and domain trade-offs remain explicit. Non-support: no corresponding gain, reversed effect, or gains accompanied by the very loss/retention sacrifice the hypothesis aimed to avoid. Insufficient: failed validity guards, incomplete endpoint, inconsistent blocks, unresolved strong rival, or lack of a quality/saturation definition for a stronger capacity claim. These are interpretation branches, not researcher-approved numerical scientific thresholds. Finish factual results even when judgment stays Unknown.

## 16. What This Cannot Claim

No universal common knowledge, maximum task capacity, slot exhaustion, general learned-routing advantage, long-horizon continual-learning benefit, depth-independent serial mechanism, article-level generalization guarantee, or approximately 300M scaling result. The selected data include repeated exposure. Domain labels give privileged routing information. Final test reuse for new tuning would convert it to development data and requires an explicit amendment.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–G substantive choices are recorded above as AI-selected within the researcher's explicit delegation; none is falsely labelled separately researcher-confirmed. Pre-training changes: (a) data-only expansion of three insufficient fixed evaluation members; (b) budget raised from 1152 to 4608 updates to address short-budget ambiguity; (c) initialization matched between common_parallel and private_active; (d) identical additive domain conditioning in all arms before training, removing the Dense information-access mismatch while leaving structural routing as the treatment. Record subsequent code/runtime Smoke changes and hashes in execution receipts before full trajectories. Amendments after viewing results must be identified as such and cannot retroactively preregister them.


### 2026-10-03 05:15 UTC: Second bounded mechanism diagnostic, before training results

Within the explicit autonomous-research authorization, add a same-forward single-layer gradient-path diagnostic. The six-arm training/data/optimizer/endpoints remain frozen. This is the second experiment, not a seventh trajectory architecture. At registration the worker of pt-uasnh61d remains Pending and no new model loss has been inspected.

Use each common_serial block's first single-domain phase-end checkpoint, global update1536. Fix layer index3 and perturb only that layer's C once. The next domain order[1] supplies fixed train records0:32 and32:64 as two source panels; dev never selects the direction. Keep all other weights and optimizer states unchanged; source checkpoints are read-only.

Compare the ordinary C gradient with a control using z+stopgrad(C(z)) only inside that layer's E input; the outer C(z) remains differentiable. Initial forwards and losses must match. Scale each negative gradient to the same parameter-displacement norm:0.001/0.003/0.01 times the initial C parameter norm. Report all scales and both panels without selecting a best case; zero gradients are degenerate. This one-step SGD-direction diagnostic does not reproduce AdamW history or establish a training trajectory.

Evaluate every perturbation on the same256 dev records in each of four domains and its source panel. Save per-record finite losses, source learning, gradient norms/cosine, actual displacement and non-target parameter hashes. Repeat baseline evaluation to check numerical stability and retain actual BF16 finite behavior. Seed is paired with order, so checkpoints/source/old domains differ across blocks; report separately rather than claiming identical-task replication.

The comparison measures finite cross-domain effects of separately normalized update directions obtained with or without that through-expert gradient path at this state and layer. Normalization also rescales the direct gradient, so their contrast is not an additive contribution of the removed path. On the source panel that generated the gradients, the full gradient is already the steepest first-order equal-norm descent direction in the ideal differentiable model; a source advantage alone is not a discovery of cross-domain reuse. Old-domain finite responses test effects not predetermined by that identity. It does not isolate all serial depth, identify universal semantics, or establish long-term capacity. Support/non-support/insufficient branches retain per-domain and source costs without automatic scientific closure. The [registration](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/coupling_probe_registration.json) and execution receipts hold exact identities and status. Execute only when the same8×RTX5090 SPOT allocation has the checkpoint and a free GPU; otherwise record NOT RUN, preserving the resource constraint.


### 2026-10-03 05:38 UTC: Third finite evaluation — domain/expert matching

Before any new trajectory results, register the final diagnostic: whether domain-specific training corresponds to a functional advantage on the assigned domain. It adds no trajectory and reads the fixed final update4608 of eight expert-bearing runs (parallel, serial, private_active, private_total across both blocks).

For true domain d, retain its domain embedding and force only every layer's selected expert to e, for e=0,1,2,3. Keep C/T and all weights unchanged. Save the4×4 matrix L[d,e] and per-record losses on the same256 dev records/domain. Diagonal e=d must reproduce final training dev within1e-4 and the full parameter hash must remain unchanged. Do not read test. This jointly intervenes on the expert bank across layers, not one layer or semantic feature.

S is mean off-diagonal loss minus mean diagonal loss; positive values indicate better assigned matching on average. Also report each domain's own-versus-other mean, best expert, and double-centered interaction I=L−row mean−column mean+grand mean. In the balanced four-domain design, S=−4/3 times the mean diagonal interaction, so additive domain difficulty and general expert quality cancel. Per-domain best experts/margins can still reflect those effects and are not standalone specialization proof.

The claim is functional domain/expert-bank matching in this checkpoint's shared computational context; co-adaptation, phase LR and order may contribute. It does not identify intrinsic semantics, maximum capacity or a unique training cause. Report continuous S and domain values without an outcome-selected threshold, separately by seed/order block. The [registration](/data/250010109/MoE_Router/experiments/20261003_common_specialized_capacity/notes/expert_swap_registration.json) holds exact implementation details.

These three bounded pieces (six-arm trajectories with C/T rollback, same-forward gradient paths, expert-swap evaluation) complete the current test set; no further experiments are added now. Before first analysis execution, freeze a sequential analysis chain on the same GPU: C/T rollback, expert swap, and serial-only gradient-path probe. Training sources/configs/budgets/initial freeze remain unchanged. At this amendment the worker remains Pending with no new loss; original analysis source and freeze snapshots are preserved.


### 2026-10-03 07:42 UTC: routing-r2, sharing decisions and actual routing utility

At 07:27 the researcher explicitly authorized approximately 3h20 of continued MoE routing/architecture research and up to five 8×RTX5090 SPOT jobs. Count the existing pt-uasnh61d conservatively, allowing at most four additional allocations, only when needed by a hypothesis. [Authorization/job scope](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/user_authorization.json). This is an AI-selected exploratory operationalization under that authorization, not fabricated individual scientific signoff. The capacity-r1 training and its checkpoint subanalyses retain every frozen configuration, token budget, data and executable byte. The current Anchor owns the refined question; its previous bytes are preserved.

The three evidence activities are the existing architecture experiment and subanalyses, the local routing test below, and an optional new-panel equal-token model audit. The latter requires its own exact registration and qualification before execution; this paragraph does not preselect its data or perturbation scale. Spectra and SAE remain tools.

**Purpose/hypothesis.**Does lower response-prediction MSE yield better actual choices? The candidate mechanism is input-dependent source matching; rivals are update rejection and preference for a globally better expert. The observation is finite NTP CE at sixteen fixed positions per old R record, not all-token or downstream performance.

**Data and computation.**Reuse Oct02 source_transfer_01 A/B sources, F-half1 fitting, old R readout and all four frozen history/history_sae/history_pca320/history_random320 predictors. No refitting, selection or new model forward. source_transfer_finite_01 contains eight actual finite actions at the same S7 33B state. M is the mean gradient and η=0.05731845587090156 is applied once. Common a₀=W₀c is always computed; action d adds −ηM_dc with complete 2048-dimensional c, while the router uses pre-target features. The native norm/MLP/head finite losses have already been measured. Per-token selection defines conditional residual computation, generally not one common W update. Preserve identities, numerical computation order and hashes. SAE320 is selected from a full width30000 TopK32 encoder, not a cheap 320-dimensional projection.

**Conditions/information.**A→B and B→A are primary; A→A/B→B secondary. Report every predictor and both four-source and zero-plus-four-source action sets. Scores are frozen derivative predictions times η; zero action has score/effect0. Lowest index breaks ties. The fixed comparator is chosen only from mean F derivative labels for the training source. R targets only evaluate choices and a explicitly nondeployable post-hoc eventwise oracle. Old R is exposed and past feature selection touched A+B, so this is exploratory reuse, not independent confirmation.

**Analysis.**Save finite ΔCE and differences from the F-selected fixed action, uniform random actions and an input-independent random selector with the same global R action proportions. Randomized expectations use the full finite action table without random-seed selection. Report pooled and all four receiving domains. With rejection, decompose the total contrast into source selection and rejection using a fixed domain expert at the same rejection coverage; that expert is still chosen on F. The no-rejection action set isolates source selection. Preserve event choices, per-record differences and action proportions.

**Uncertainty/branches.**Use2000 category-stratified paired record bootstrap draws, all sixteen positions together, seed1003. Intervals condition on fixed sources/fits/selection/old panel, not article or source-population independence. No winner selection or omnibus significance verdict. Consistent utility over fixed and usage-matched input-independent controls supports this local operationalization; absent/reversed benefit weakens it; source inconsistency, undefined practical scale or guard failure preserves insufficiency. Better MSE cannot rescue failed decision utility; the event oracle is not attainable headroom.

**Execution/guards.**Read-only cached CPU analysis, eight threads,600-second bound; zero LM/SAE/probe training, forwards or remote submissions. Register input/code hashes before aggregates; synthetic controls check ordering, signs, zero actions, choices and decomposition. Post-check immutable inputs, finite values, oracle bounds and closure. Outputs: /data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/cached_routing_utility_01; code: /data/250010109/MoE_Router/experiments/20261003_sharing_routing/scripts/cached_routing_utility.py. Preserve failures without overwriting old evidence. Actual values and interpretation belong to receipts and the new report, not this registered body.


### 2026-10-03 08:05 UTC: routing-r3, new-panel equal-token checkpoint audit

**Purpose/hypothesis.** Test what pre-target information supports useful selection among full-input residual experts, and compare specialized source updates with a real common update. The hypothesis is a transportable expert-relative preference, not superior reconstruction or mandatory SAE success. Rivals include a globally better action, rejection, source-sample instability, and finite-sample regularization. This is the previously named third evidence activity, not another training experiment.

**Setup/data.** Use Dense, fresh S7 lambda0.1, and SALL unit-weight checkpoints at exactly 33,000,000,000 training tokens. Their architectures, losses and training histories differ; comparisons across them are descriptive replications, not causal effects of SAE. Source snapshots and actual state hashes must pass worker preflight. The data-only frozen panel has 256 source-A,256 source-B,512 FIT,1024 DEV readout records, balanced across eight categories and four domains, at the same sixteen positions14,30,...,254. Source/FIT use disjoint TRAIN records and readout uses DEV; no TEST array is loaded. The [selection manifest](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/data/probe_33b/manifest.json) and [exact registration](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/probe_33b_registration.json) precede any new forward. Exact records/token strings are disjoint; article-level and pretraining overlap remain Unknown.

**Mechanism/intervention.** At the last block define full attention projection input c (2048), its output a=Wc (1024), pre-attention residual r, and x=r+a (1024). Native full-input tail remains fixed. For each source bank compute four mean event gradients M_d=mean(e c^T), e=gradient of individual selected-position NTP CE with respect to a. Common M is the equal-domain mean of raw M_d. Each of the five actions independently receives delta_W=-0.001 norm(W) M/norm(M), with zero gradients marked degenerate; common is not the mean of already normalized actions. Evaluate actual finite losses using a+delta_W c, retaining complete c, r and native MLP/norm/head. A target-dependent gradient constructs actions only on source records; deployed selection uses prefix-only features. Per-token selection is conditional residual computation and generally cannot be described as one global W update. FP32 native forwards, no autocast/TF32, with FP64 contraction for accurate VJP and direction multiplication where registered; no optimizer step.

**Analysis frozen before losses.** Fit actual finite five-action DeltaCE labels on FIT with centered/standardized ridge, unpenalized intercept and lambda10 in X^T X+10I (no sample-count normalization). Freeze each family and evaluate A→B/B→A primary, A→A/B→B secondary, for five-action and zero-plus-five-action sets. Fixed families are base; base plus64 PCA coordinates of a,c,x,or concat(c,x); base plus64 seeded orthonormal random coordinates of a; base plus64 most frequent FIT SAE atoms where available; and base plus full concat(c,x). PCA, atom selection and scaling use FIT only, without action labels. Base has389 prefix-only coordinates: three128-bin hashed current/previous/prefix-count blocks, position/256 and its square, and log1p norms of c,a,x. Exact hash, seeds and ties are frozen in [config](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/configs/probe_33b.json). SAE64 still requires its entire width30000 encoder, not a64-wide cheap projection.

Compare every frozen selector with zero, the FIT-finite-cost selected constant action (transport its label for cross-bank tests), uniform random and global-usage-matched input-independent random actions, and directly measured common update. Report all families, domains, source transfers and action sets; do not choose a DEV winner. Report source selection versus rejection, action fractions, actual action harm fractions, first-order versus finite discrepancy, and a explicitly nondeployable target-informed event oracle. Source-A/B readouts are labelled in-sample because they constructed the actions. Use2000 category-stratified paired record bootstrap draws, seed1003; all16 positions remain together, and uncertainty conditions on the fixed source banks/fits/panel. New DEV is exploratory, never called confirmation.

**Qualification/execution.** One staged8×RTX5090 SPOT allocation, with Dense/S7/SALL assigned3/3/2 extraction and finite shards. Bound the job to7200seconds and each worker to3600seconds. Check exact native full-forward/tail agreement, no-op, causal-prefix invariance, local derivative identity, temporary weight perturbation and restoration; verify source/config/state hashes and all parameter counts. Extract all selected records, form frozen directions, then finite replay; analysis uses only certified complete shards. Failed guards or partial endpoints stay failed/incomplete, and no reduced scientific budget is substituted. No model or SAE training. The prior capacity job remains separate and is counted conservatively in the five-job limit.

**Branches/boundary.** Useful cross-source finite utility beyond the constant and usage-matched controls supports the bounded decision-information hypothesis. Absent/reversed benefit weakens that operationalization. Inconsistent banks, incomplete runs, invalid guards or unknown practical scale retain insufficiency. Full-input finite experts test a bridge to routing, not online co-adaptation, a learned MoE architecture, downstream task gain or long-term sharing. All new outcomes are currently NOT RUN; exact receipts and the new report will own results.


### 2026-10-03 08:18 UTC: post-hoc mechanism decomposition of cached routing utility

After observing the registered old-cache utility results, add a descriptive decomposition within the same second evidence activity: distinguish coarse receiver-domain/category matching from within-group conditional selection. This is explicitly post-hoc to that old R result, not preregistered confirmation, not a new model run and not a new-DEV analysis. For each existing frozen selector use its R prediction-only choices to estimate global, within-domain and within-category action proportions. Score the corresponding input-independent randomized expected losses using the already measured complete finite action table. Each group control is independent of events only conditional on that group and its fixed proportions; group labels are explanatory information, not silently available deployment features.

For every condition, the global-control gain equals the global-versus-group control gap plus the group-control-versus-policy gain. Also factor fixed-action gain into disagreement probability times mean advantage conditional on disagreement. Keep all32 conditions and pooled/four-domain scopes, recomputing proportions in2000 category-stratified paired-record bootstrap draws, seed1003. No result-based threshold or winner. Exact scripts/input hashes/synthetic identities are registered before this new aggregate in /data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/cached_policy_group_decomposition_01. CPU8 threads and600seconds maximum; no LM loading/forward, training, TEST or submission. Persist numerical results in its receipt and the routing report.


### 2026-10-03 09:22 UTC: pre-execution configuration and termination repair

Independent static review reproduced a startup blocker: native SALL canonicalizes sae_hook_layers to a tuple, whereas JSON stores the same ordered values as a list. Direct comparison rejected the correct checkpoint. The repair compares sequence contents and order while retaining rejection of genuine field differences. Scheduler SIGTERM/SIGINT handling and bash exec were also added so terminating only the scheduler enters bounded child cleanup. Thirty-three CPU checks passed in an isolated candidate, including all three native configuration classes, negative controls, and actual SIGTERM/reaping of a fake CPU worker. No language model was loaded; these checks do not replace GPU qualification.

Immediately before installation at 09:22:55 UTC, pt-meoxfrko remained STARTING / worker Pending, with no execution directory or pod output. Original code, tests, configuration, freezes and execution certificate were preserved verbatim in the [before manifest](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/preexecution_amendment_01/before_manifest.json). The [amendment receipt](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/preexecution_amendment_01/amendment.json) records installed hashes and platform evidence. Only code_files hashes changed in the config: data, checkpoints, actions, precision, analysis recipe, resources and runtime limits remain identical. The original registration is unchanged. Execution and analysis freezes link their previous versions. The existing submitted job is retained, without resubmission or a new experiment. Incomplete stage directories are not overwritten in place; preserve the attempt and use a reviewed clean output location. Complete stages still require signature verification.


### 2026-10-03 09:38 UTC: post-hoc router-input comparison on the old finite panel

The purpose is to locate useful routing information, not to reselect an SAE winner. Old response/utility outcomes have already been seen, so this is explicitly post-hoc within evidence activity two. Reuse all true finite labels from Oct02 finite_panel_01: F-half1 FIT has 512 records × 16 events and R has 1024 × 16. No LM load/forward or remote submission occurs. Four actions use F-half0 domain-mean gradients with fixed full-step eta=0.05731845587090156 and delta_W=−eta M. The step was calibrated to pooled-source output-displacement RMS, not equal per-action weight norms. Do not use half-step outcomes. There is no directly measured common action or A/B transfer here. Select the strong fixed comparator using FIT finite CE.

Freeze eight families: base389; base plus PCA64 of a, c, x or (c,x); a_random64; SAE64; and full (c,x). Form x=r+a at cached activation precision before FP64. Fit all axes, atoms and standardization on FIT only. Ridge uses summed squared error plus 10 times squared coefficients, with an unpenalized intercept, matching the reusable frozen new-panel analysis functions. Seed1003 is fixed and all features precede the target. R targets score only. Full (c,x) has different dimension and is not a matched-64 comparison.

Retain four-action and zero-plus-four action sets with first-index exact tie breaking. Report all 8×2×5 receiving-scope rows. Controls are FIT-fixed, uniform random, global R usage-matched random, category usage-matched random, no update, target-informed oracle and paired difference from the full-(c,x) policy. Category labels are diagnostic only. Use 2000 category-stratified whole-record bootstrap draws, seed1003, reestimating global/category action proportions in each draw and retaining all 16 positions together. Intervals condition on this exposed panel, fixed bank and fits. Save predictions, choices, transformations, actual action tables, record-level quantities and source hashes for independent recomputation.

Benefits from c/x or their combination over a can motivate an information-availability hypothesis for the specified learner; dimension, scale, regularization and estimation error remain rivals. A null result proves neither absent information nor useless future expert learning. Freeze each family fit/selection before scoring and never select hyperparameters on R. Before fitting, register the exact recipe and script/helper/input hashes. Use eight CPU threads with an external 1800-second timeout and preserve failures. Output: /data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/cached_router_inputs_01.

A cross-panel identity audit also found four exact matches in both full text and 256-token prefix: two new source-A records and two new FIT records, with none in new R; old roles are one A, one B and two FIT, with none in old R. Roles remain disjoint within the new panel, but the two entire panels are not fully independent. Article-level near duplication remains Unknown. This fact does not change the frozen new panel/actions or make unread new R strict external confirmation.
