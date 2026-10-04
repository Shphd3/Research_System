> Historical reading copy. Scientific text matches the original snapshot; only original-context relative links are resolved. The candidate directory holds the current Anchor.

# Candidate Protocol: Common and specialized computation in sequential natural-text learning

Revision: 2026-10-03 capacity-r1. Temporary candidate. Owner: [Anchor](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261003_before_routing_refinement/reading/anchor.md). Old experiment contracts remain in [history](/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels/history/20261002_before_capacity_refinement/reading/protocol.md). This is one six-condition comparison family and its checkpoint intervention analysis.

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
