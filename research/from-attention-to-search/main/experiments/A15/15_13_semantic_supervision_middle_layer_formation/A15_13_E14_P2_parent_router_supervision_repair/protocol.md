# Protocol: E14-P2 parent-only supervision repair

## 0. Approval Snapshot

Document status: `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_AND_ANALYSIS`. All A–G scientific choices and the Focus account are HUMAN_CONFIRMED by the execution instruction on 2026-09-06. Cross-block consistency: PASS.

Resource choice: researcher has authorized RESERVED resources for the next validation. Do not ask again for quota selection. Proposed ceiling: one H100, sequential conditions, maximum 90 minutes, no automatic retries. This request asks for a plan; final new experimental details remain for design review.

Owning Focus: [0906 handoff](../../../../focus/focus_gmm_pseudolabel_handoff.md), same problem and task owner as P1. This is step 2 of the existing four-step sequence, not a new workstream. Role: root-cause repair test. [Primary Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md) tests whether offline assignments can be handed to a causal block-14 Router while preserving task loss. Local clause: after P1 identified missing parent supervision, does training that parent predictor alone produce useful online dispatch? This does not replace the historical gold-Oracle verdict or test new labels.

Treatment: original parent classifier trained to predict original pseudo parents. Controls: original untrained parent; identically trained parent with example-permuted labels; supplied teacher parent with original predicted child; supplied full pseudo path. Experts, child Router, teacher, input hook, unit coefficients and evaluation examples remain fixed.

Primary metric: answer NLL reduction from original online routing, in nats/answer token. Qualification requires superiority to the shuffled-supervision control and improvement on record-disjoint evaluation. Pass requires positive lower paired-bootstrap endpoints for all these comparisons in both seeds. Fail means at least one required comparison has nonpositive upper endpoints in both seeds. Other eligible patterns are Insufficient. Report recovery continuously, without a post-hoc equivalence threshold.

Cannot claim: universal deployability, unpolluted public benchmark performance, final-layer label optimality, a causal-prefix teacher, or a newly successful two-stage expert-training method. No new expert training, teacher fitting or layer selection.

A–G: CONFIRMED; cross-block consistency PASS. Existing P1 design remains frozen. P2 implementation, smoke, full execution and four-part analysis are explicitly approved.

## 1. Terminology / Definitions

Parent means one of three coarse expert groups. Child means one of eight fine experts with parent sizes (3,3,2). Teacher means the original frozen pseudo-label assignment, not human semantic truth. A Router is the classifier that chooses an expert. NLL is summed negative log probability of reference answer tokens divided by their count. Online means routing decisions use causal model states without supplying teacher labels during evaluated inference; reference previous answer tokens remain available under ordinary teacher-forced likelihood evaluation. It is not a free-generation score.

## 2. Anchor Alignment

The Anchor's handoff clause and task-loss metric are retained. P1 fixed-path evaluation found parent correction recoveries 98.24%/93.96%, and no historical parent gradient in the eight-task hard-pseudo branch. Those observations motivate a repair, but do not establish learnability. Parent-only learning tests the missing supervision path while keeping the proposed teacher context and input representation unchanged. [P1 evidence](../A15_13_E14_P1_coarse_path_intervention/summary.md).

## 3. Tested Hypothesis

Adding original pseudo-parent classification supervision to the existing parent Router lowers fully online answer NLL in both checkpoints. The sample-specific teacher relation must outperform matched training with shuffled labels; class-frequency adjustment alone is insufficient to establish the proposed mechanism.

## 4. Rival Explanations

1. Category-prior correction rather than meaningful sample-label association: match label frequencies via fixed whole-example permutation.
2. Causal input cannot predict a full-sequence teacher, or the linear readout/finite optimization budget is inadequate: report parent classification losses and accuracy on train/development/evaluation, without inferring intrinsic impossibility from a negative result.
3. Improvement depends on repeated training items: predeclare the record-disjoint evaluation subset. It excludes two sources, so report its changed composition and do not generalize it to all eight tasks.

## 5. Data Construction And Provenance

Reuse `/data/250010109/datasets/a15_e14_benchmark/processed.pt` with SHA-256 `e6320e7aba92c8d9caa36ce43bda5d695843070a54955e63776893334d58a6b6`.
Eight sources: MMLU, MMLU-Pro, BBH, GSM8K, MATH, GPQA, HumanEval, MBPP. Existing splits: train 4096, development 512, evaluation 512; max length 512. Training contains 3434 unique record IDs. Evaluation contains 512 unique IDs and 30442 answer tokens. 128 evaluation IDs occur in training: 64 GPQA and 64 HumanEval. Record-disjoint evaluation consists of the remaining 384 examples; derive its token denominator from the immutable masks and record it before training. Retain full historical data for paired comparability; no repartition or new task download.

Pseudo assignments: original E14 run `full-20260903T042000Z/pseudo_labels/benchmark/assignments.pt`, digest `64baa7bc0d737f26927a509727716481a5a8862f953d7d60db1c5bc435f705fa`. They were fitted to train-only projections/clusters of frozen final-layer whole-sequence means, including reference answers. No refit in P2. Model training may use train states/labels only; development is monitoring only; evaluation cannot choose hyperparameters or checkpoints. Historical evaluation is already seen and is not called untouched confirmation.

## 6. Learning Task And Permitted Supervision

At each position predicting an answer token, read the original causal block-14 input vector and predict the example's pseudo parent. Broadcast the per-example parent to those prediction positions only. Exclude padding and positions whose next-token target is masked. Input is the 1024-dimensional causal hidden state; no source ID, future-token aggregate, answer label, teacher logits or child assignment is appended as a feature.

Train supervision is original parent labels in treatment and a fixed example permutation of those labels in the control. Use NumPy generator seed 20260906 for one permutation of the 4096 train-example indices, preserving counts; broadcast after permutation. Reuse it across checkpoint seeds. Do not permute individual tokens or development/evaluation ground targets. Log permutation indices, digest and fraction unchanged. No claim that every permuted label differs.

## 7. Model / Architecture And Frozen Variants

Base: frozen Qwen3-0.6B-Base. Start from original `benchmark__HIER_GMM_HARD_R8__seed17/final.pt` and seed29 counterpart in the E14 source run. Digests: `a783d46fcc77233ed94afdaaf898cb9f31033f76a568dcb66de3a93f983862c2` and `6e933452334524a22147e6d065e4e27f89a5badf6a64aa4fcfee94802cc70cac`.

Only the existing 1024-to-3 parent linear classifier (3075 parameters including bias) changes. Initialize from that checkpoint's parent, with a fresh optimizer. Shared, parent and child expert banks, child Router, base and language head are frozen. Preserve block-14 pre-attention input capture and rank-8 expert banks in its MLP down projection. All inference expert coefficients remain one. No capacity increase, extra context, new input hook, or probability weighting.

Extract/cache bf16 causal states at answer-prediction positions using each original checkpoint in eval mode; block input precedes the adapter and is not a function of the parent output at that block. Verify cached states/logits against direct forwards. Classifier weights originate in bf16 and are cast to float32 for optimization; cast trained weights to bf16 for deployment. Both treatment and shuffled control use identical casts; zero-step deployed weights must reproduce the original checkpoint exactly.

## 8. Training Objective And Optimization

Exactly one parent-only training stage, not rerunning expert stages. Objective: mean cross entropy over valid answer-prediction positions in each original eight-example microbatch, divided by accumulation 16; no task-loss term, no child loss, no balance loss. Gradients reach only parent weight and bias. At batch boundaries reproduce the old sample-balanced ordering, `balanced_order(source, seed, epoch)`.

128 optimizer updates; 4 full passes through 4096 training records; microbatch 8, accumulation 16. AdamW, learning rate 5e-4, weight decay 0.01, betas (0.9,0.999), epsilon 1e-8; warmup 5 updates followed by cosine decay to zero as the historical schedule; clip parent gradient norm at 1.0. Effective example batch 128. Train token exposures must equal 911644. Identical setup for shuffled control. No hyperparameter sweep.

Save update 0, 32, 64, 96, 128 parent states and train/development classification metrics. Select final update 128 regardless of development score. Development observations cannot cause extra epochs, stopping for performance, or selection. Degenerate labels, nonfinite values, unexpected counts or frozen-parameter mutation stop execution as an engineering failure. Optimization adequacy remains a boundary of a negative result.

## 9. Conditions, Seeds, And Checkpoints

| Condition | Training | Evaluated selection | Protected comparison |
|---|---|---|---|
| O: original | None | Original predicted parent/child | Baseline |
| R: repaired | Parent only; true original pseudo labels | Trained parent, original child reselected within predicted parent | Missing-supervision repair |
| S: shuffled | Parent only; permuted pseudo labels | Trained parent, original child reselected within predicted parent | Frequency/optimization rival |
| B: teacher parent | None | Supplied parent, original child reselected there | P1 correction reference |
| C: full teacher | None | Supplied parent and child | Residual fine-path reference |

Two source seeds, 17/29; R/S both start afresh from the corresponding same original checkpoint. Total: four parent training runs, 512 optimizer updates across runs. One deployment evaluation per condition and source seed on the complete 512 examples. B and C are privileged references, not new trained models or mathematical lower bounds. P1 D wrong-child result remains background; no repeat necessary to adjudicate P2. Check that supplied-parent B and full-teacher C are invariant to parent replacement.

## 10. Primary Metric And Frozen Analysis Plan

For condition k, \(L_k=\sum_i s_{ki}/\sum_i n_i\) where s is summed answer negative log probability and n the answer-token count. Primary repair effect is \(L_O-L_R\). Qualification effect is \(L_S-L_R\). Compute both on full evaluation and record-disjoint evaluation, separately per seed. Recovery relative to supplied-parent reference is \((L_O-L_R)/(L_O-L_B)\); report undefined for zero denominator and do not clip. Also report R−B and R−C; a positive recovery is not equivalence.

Use float64 reductions and 2000 paired-example percentile 95% bootstrap intervals with NumPy seed 20260906. Identical resampled indices across all conditions within each population, independently resample the full and disjoint populations. Unit of independence is evaluation record, not token. No pooled seed-population interval; report seeds individually and a descriptive unweighted mean. All required positive contrasts form a conjunction, not a menu for picking a favorable result. Auxiliary accuracy and residual intervals are descriptive. No post-hoc exclusions, outlier removal or threshold changes. Any missing required output yields Incomplete, not a negative scientific verdict.

## 11. Secondary Metrics And Guards

Report true-parent agreement at answer-prediction positions, parent CE, per-parent predicted loads, per-source answer losses, and wrong-parent versus correct-parent strata. Agreement is not expert utility or end-task gain; load is not semantic evidence. Full and disjoint NLL protect the decision. No free-generation score required.

Verify original data/checkpoint/assignment hashes, record-ID intersections, answer masks and source counts. Eval routes must not consume teacher labels in O/R/S. Prefix invariance check: changing suffix tokens cannot alter an earlier cached state or Router logits within the fixed numerical tolerance. Freeze/nonfinite/path-validity guards and source-code/config hashes are mandatory.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: one forced parent selects only its allowed children; real CE backward produces finite nonzero parent gradients while all other learned tensors remain frozen. Known bad: intentional parent-child mismatch or label leakage is caught. Known confusing: parent accuracy rises but task loss does not; this is not a successful repair. An aggregate improvement that fails shuffled or disjoint qualification cannot be promoted.

## 13. Scientific Procedure And Stage Contracts

| Phase | Input / operation | Output / handoff | Gate and failure |
|---|---|---|---|
| Identity and cache | Original data/checkpoints; extract causal states and train-only targets | Immutable cache, IDs, masks, hashes; no updates | Reject source mismatch, suffix dependence or mask errors |
| Small smoke | Fresh disposable copies; 8 examples and 2 parent updates per label condition | Gradient/freeze checks, direct/cache comparisons, O/B/C replay | Replay paths exact and absolute aggregate loss error <=1e-4; no-op weights exact; never carry smoke weights to full training |
| Parent-only stage | Fresh original parent; real/shuffled labels; fixed 128-update schedule | Four final parent checkpoints, curves, full parameter accounting | No parameters outside parent change; finite final output and exact budget |
| Full model evaluation | Inject each final parent; original frozen experts and child Router | O/R/S/B/C paired arrays and task metrics | Predicted-route modes cannot access teacher; B/C remain invariant |
| Analysis | Fixed arrays, full/disjoint masks, registered bootstrap | Summary, Detailed, tables and inspected figures | Use the one verdict rule; no post-result tuning |

Cache/direct Router logits should match exactly when identical bf16 operations are used; for a float32 diagnostic cast use maximum absolute logit tolerance 1e-5 against the same float32 direct calculation. Causal suffix check uses max hidden difference 1e-5 after conversion to float32, in the same runtime and batch shape. A failure stops promotion and is investigated without relaxing thresholds using task results.

## 14. Algorithm, Output, And Provenance Contract

Proposed worker: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair`. Worker holds cache, code, raw arrays, gradients, logs, parent checkpoints and job receipts. Use original PyTorch 2.8/Python 3.12 NGC 25.06 image on one reserved H100, historical bf16 backbone/evaluator and batch 8. Do not modify E14 or P1 worker sources. Verify source digests and snapshot dependencies at execution, since other tasks may edit shared files.

Resource ceiling: one `n6ls.iu.i40.1` H100 worker, sequential runs, 5400-second timeout, zero automatic retries; stop after the registered conditions. Runtime is an upper bound, not an ETA. No task submission in this planning turn. Once the design is confirmed, existing reserved-resource consent need not be requested again.

Expected outputs: run metadata; source/data/pseudo/code/protocol hashes; ID overlap counts and mask; immutable cache map; shuffled assignment permutation; per-update train/development metrics; four final parent checkpoints; per-example loss sums, token counts, source/record IDs and routes for ten evaluations; frozen checks; bootstrap contrasts; one verdict JSON. Canonical `summary.md`, `detailed.md`, tables and inspected figures live beside this Protocol only after evidence exists.

Figure contract: (1) per-seed O/R/S/B/C NLL and full/disjoint repair/control contrasts, nats/answer token, source paired arrays, bootstrap intervals; allowed claim is bounded online repair. (2) parent agreement versus task-loss improvement, distinct axes and explicit units, descriptive only; optional if it changes interpretation. No diagram is fabricated from missing data.

## 15. Success / Failure / Insufficient Evidence

After all technical guards pass, form four contrasts per seed: O−R and S−R on full and disjoint populations.
- `ONLINE_PARENT_REPAIR_SUPPORTED`: all eight lower 95% endpoints exceed zero.
- `ONLINE_PARENT_REPAIR_NOT_SUPPORTED`: at least one of the four named comparisons has upper endpoint <=0 in both seeds. State which clause failed; do not imply zero benefit everywhere.
- `INSUFFICIENT`: every other eligible pattern, including seed disagreement or intervals crossing zero.
- `INELIGIBLE` / `INCOMPLETE`: technical guard failures / missing required arms.

Report remaining R−B/R−C and recovery magnitude irrespective of verdict. No result automatically licenses a larger model, new teacher or extra training.

## 16. What This Cannot Claim

Passing shows this finite-budget parent-only supervised repair benefits these frozen models on this internal workload. It does not validate a universal semantic hierarchy, compare teacher layers, prove full-sequence labels are causal, repair contamination, or prove staged coarse-to-fine expert learning. Disjoint records are only an ID-based safeguard, not a semantic decontamination audit. Failure does not prove absent information: classifier capacity, optimization and target ambiguity remain rivals.

One subsequent decision: determine whether the parent-only repair is sufficient to serve as the fixed online baseline for the next diagnosis. If it passes, retain it and quantify remaining gap before changing teacher or fine routing. If it fails or is insufficient, inspect registered training/held-out readout diagnostics to choose a bounded layer/context/readout test; do not start all third-step candidates simultaneously.

## 17. Block Confirmation, Freeze, And Amendment Ledger

2026-09-06: researcher stated the first experiment is understood, requested the next validation plan and repositioning within the four-step plan, and explicitly authorized reserved resources. This is not recorded as confirmation of newly proposed shuffled control, subset qualification or training settings.

A question, B data, C supervision, D architecture, E optimization, F evidence, G execution details: PROPOSED. Source identities and prior results: VERIFIED_SOURCE. Reserved quota: HUMAN_CONFIRMED. Scientific implementation/smoke/full-run promotion: pending confirmation of this draft and its Focus account. Internal consistency: PASS_AS_DRAFT; human confirmation: PENDING. No design freeze timestamp or run exists. Confirming the proposed design does not change any P1 result or historical protocol. Any post-start change must be append-only, with timing, old/new values, reason and eligibility impact.

Execution approval receipt 2026-09-06T10:38:42.908632+00:00: researcher explicitly confirmed the experiment and requested completion through the audited four-part analysis. All A–G and Focus experiment-two design confirmed; implementation, smoke, four training runs and full evaluation/analysis approved on the already authorized single reserved H100. The earlier draft-status entries below the scientific body are historical. Scientific body frozen as revision 20260906-P2-v1; subsequent material changes require append-only amendments.

Engineering receipt: first reserved job `pt-i5ukbgg1` stopped during seed-17 cache smoke before any formal parent training. O/B/C replay and causal suffix guards had passed. The cache guard recomputed parent logits over 511 positions but compared with the 512-position forward sliced afterwards; this was not the registered identical-operation comparison. Repair recomputes full-shape logits before masking, preserving strict equality, all tolerances and all scientific settings. First failure retained; restart in a fresh directory with the same approved resource.

Replacement submission receipt: reserved single-H100 job `pt-diap9xc9` RUNNING from 2026-09-06 10:44:34 UTC; fresh worker output `runs/reserved-20260906-p2-v2/full`. Original-path replay, prefix invariance and repaired matched-shape cache checks passed before formal training. The worker holds an immutable `protocol_snapshot.md` of the approved pre-run scientific body; live receipts do not alter the hashed snapshot.

Completion receipt: replacement reserved job `pt-diap9xc9` SUCCEEDED. Four full parent fits each completed 128 updates and 911644 target exposures; ten full path evaluations complete; original O/B/C losses and routes replay exactly for both seeds. Registered analysis and rendered-figure audits are complete. Full runner elapsed 128.280 seconds. See [Summary](summary.md), [Chinese four-part audit](summary_cn.md), and [Detailed](detailed.md). No post-result settings were changed.
