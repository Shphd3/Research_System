# E14-P1: Frozen coarse-path intervention and architecture audit

Status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_EVALUATION
Role: root-cause audit. Revision: 2026-09-06-v1.
Problem key: A15.gmm_pseudolabel_oracle_gap.
Primary Anchor: [A15_13_05](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md), clauses 7–8.
Confirmed Focus: [0906 task](../../../../focus/focus_gmm_pseudolabel_handoff.md).

## Approval snapshot

The researcher accepted the preceding four-condition design and explicitly instructed: “认同你的执行顺序，我们现在先开始执行第一步骤，将路径修复，然后进行架构审计”. This authorizes implementation, smoke, full frozen evaluation, and architecture audit within step 1. It does not authorize retraining, changed teachers, expert placement changes, publishing, commits, or pushing. Routine implementation details below operationalize that accepted design.

Question: how much of the deployed-versus-original-pseudo-path loss gap can be recovered by supplying only the original teacher parent, and are original child experts better than same-parent alternatives?

Hold the original base, language head, adapter, teacher, sample order, evaluation mask and unit coefficients fixed. A is predicted parent/predicted conditional child; B is teacher parent/predicted child constrained to that parent; C is teacher parent/teacher child; D is teacher parent/wrong same-parent child. The wrong child is enumerated over every alternative; losses are averaged per example across alternatives before token-weighted aggregation. These are external path interventions, not deployed repairs.

## A. Question and boundary — CONFIRMED

Main hypothesis: B improves upon A in both seeds. Rivals: child routing remains deficient, or C is not selectively better than D. The main falsifier is failure of a reproducible positive A-minus-B loss contrast after all path and replay guards pass. This is a within-checkpoint, intervention-order-dependent decomposition, not a unique causal fraction. Pseudo labels are not gold semantic labels or mathematically optimal expert assignments.

## B. Data and provenance — CONFIRMED

Read only `/data/250010109/datasets/a15_e14_benchmark/processed.pt`, `splits.evaluation`, all 512 examples and original 30,442 answer tokens. Original data SHA256: `e6320e7aba92c8d9caa36ce43bda5d695843070a54955e63776893334d58a6b6`.
Original run: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z`.
Read its benchmark pseudo assignments, child counts, checkpoint manifest, and seed-17/29 `benchmark__HIER_GMM_HARD_R8` final checkpoints. Checkpoint hashes must match the historical manifest. No fitting, sampling-based selection, or test-guided hyperparameter tuning. The evaluation set is already seen and may overlap the historical training mixture; this is an internal retrospective mechanism diagnostic, not new generalization evidence.

## C. Task — CONFIRMED

Full causal-LM forward on each original sequence; route interventions apply throughout the sequence. Score only shifted original answer labels not equal to -100. The teacher is the original per-example pseudo label expanded over positions. B must recompute the child argmax inside the supplied parent; never retain a child from A's possibly wrong parent. D preserves the correct parent and uses each other child in that parent's actual mapping. Enumerate consistent per-example wrong paths, not mixtures of hidden states or logits.

## D. Architecture — CONFIRMED

Frozen Qwen3-0.6B-Base; old rank-8 shared, parent and leaf banks injected into block-index-14 MLP down projection. Router reads the block input, experts read the 3,072-dimensional down-projection input. Coefficients remain 1. Base, head, all routers and all experts are eval-only and frozen. No change to input hook in this intervention experiment. Audit compares this hook with E15's MLP-pre hook as an architectural distinction, not a simultaneous treatment.

## E. Optimization — CONFIRMED

No optimizer, no parameter updates, no training stages, no new checkpoints. Read-only architecture diagnostics can perform tiny standalone gradient checks, with no optimizer and no mutation of historical files. Verify all adapter tensors match pre-run values afterwards.

## F. Evidence — CONFIRMED

For condition k, \(L_k=\sum_i s_{ki}/\sum_i n_i\), where s is summed answer-token negative log-likelihood and n is answer-token count. Primary contrast: \(L_A-L_B\). Supporting contrasts: \(L_B-L_C\) and \(L_D-L_C\). Report \((L_A-L_B)/(L_A-L_C)\) without clipping; report undefined if its denominator is zero. Never use the ratio alone as a verdict.

Report each seed separately and their unweighted mean. Use 2,000 paired example-level bootstrap draws, fixed analysis seed 20260906, percentile 95% intervals for each contrast. Draw identical sample indices across conditions. These intervals measure example variability conditional on each checkpoint, not training-seed population uncertainty. Auxiliary contrasts are descriptive; no multiple-testing-adjusted confirmatory claim.

Primary supported: A-minus-B point estimate and lower interval endpoint are positive in both seeds. Primary non-support: both seeds have nonpositive point estimates with upper endpoints <=0. Otherwise INSUFFICIENT. Guard failures are INELIGIBLE, incomplete arms are INCOMPLETE. Do not introduce a post-hoc numerical definition of “B close to C”; report the remaining absolute gap and uncertainty and leave the subsequent training choice to the researcher.

Outputs: four-condition loss table; per-seed contrasts with intervals; task-stratified descriptive rows; path checks; architecture audit; one two-panel loss/contrast figure. Figure units: nats/answer token; source: saved per-example arrays; higher positive contrasts favor the stated correction. The figure cannot establish deployable gain or semantic causation.

## G. Execution — CONFIRMED

Worker: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p1_coarse_path_intervention`.
Use the currently accessible single local MIG GPU sequentially; no cloud resource purchase. Start with microbatch 2; use matching batch for every arm. One smoke using first 8 evaluation examples checks path legality, nonfinite output, original A/C replay, and tensor freezing. Full run only after smoke passes. If local runtime differs from the historical runtime, record it and require replay before eligible interpretation.

Replay guard: identical sample masks and sources; exact A/C route identity; absolute whole-run A/C NLL discrepancy <=1e-4 from stored results. Record per-example errors, not only the aggregate. A threshold failure stops scientific promotion; do not tune it against results. Stop on illegal paths, hash mismatch, nonfinite loss, mutated tensors, or missing data. Engineering restart may resume only exact immutable config and finished arrays; otherwise use a new output directory and preserve failure logs.

Expected arrays: A/B/C and each D alternative for each seed, then a per-example averaged D array. Preserve seed checkpoints and original outputs unchanged. Raw outputs and logs remain under worker `runs/`; curated tables and PNGs plus summary/detailed remain beside this Protocol. Architecture audit covers stage dispatch, parent/child gradient reachability, snapshot changes, hook locations, teacher context, and local-versus-historical runtime.

## Freeze ledger

- A–G accepted through the user-confirmed four-condition plan and explicit execution instruction in this task; engineering guards and local resource choice implement that scope.
- Cross-block consistency: PASS. No changed teacher, expert, training budget, or data branch.
- Scientific body frozen before implementation. Future material amendments must be appended with timing and eligibility impact; never rewrite this body using observed results.
- Next execution action: implement tested intervention wrapper, run smoke, then full matrix and audit.

## Append-only execution receipts

2026-09-06: local implementation and two path tests passed. First smoke failed before model load on an ONNX/protobuf dependency mismatch; selecting the pure-Python protobuf implementation repaired import only. The next smoke at batch 2 failed the registered historical A replay tolerance. A batch-8 diagnostic matching the historical batch also failed. Both are preserved as ineligible smoke artifacts; no local full evaluation ran. Base weights and config hashes matched the original manifest. The local runtime is PyTorch 2.3/Python 3.10, whereas the historical runner pins PyTorch 2.8/Python 3.12. No metric threshold or condition was changed.

A single-H100 batch-evaluation submitter using the historical image is prepared, with a 90-minute process limit and zero retries. Resource migration and quota selection await the researcher; this receipt does not authorize cloud submission. Microbatch 8 will match the historical evaluator and be used consistently across every arm. Scientific conditions, data, analysis and replay guards remain frozen.

2026-09-06 resource amendment APPROVED: the researcher explicitly selected standard reserved quota and instructed “选择标准配额，开始执行实验”. Approved resource: one H100, one ACP worker, `n6ls.iu.i40.1`, reserved quota, historical NGC 25.06 image; process timeout 5,400 seconds, zero retries. This supersedes the local-only resource restriction in section G. Batch 8 matches the historical evaluator. All scientific conditions and numerical guards remain unchanged. Scope: smoke followed by full frozen evaluation if smoke passes, with analysis and architecture evidence records. No retraining.

Submission receipt: ACP `pt-a4qkvyya`, submitted 2026-09-06 09:20:25 UTC; RUNNING at 09:20:37 UTC. Verified single `n6ls.iu.i40.1` worker and RESERVED quota. Run root: worker `runs/reserved-20260906-p1-v1/`. Job command: `RUN_STAMP=reserved-20260906-p1-v1 timeout 5400 bash <worker>/run_remote.sh`.

Engineering amendment after first remote smoke: A and C replay exactly matched historical arrays in the original runtime, but B failed its parent-equality guard. The new wrapper set `context.forced_parent` before calling the base forward, which overwrote it with its default None. The wrapper now forwards `forced_parent` explicitly through the base method. A full-model integration test reproduced the failure before repair and passes afterwards. No scientific condition, numerical tolerance, checkpoint or analysis rule changed. The failed first remote smoke is excluded; rerun from a fresh output directory on the same authorized single-H100 reserved resource.

Replacement receipt: ACP `pt-5xgwtcam`, RUNNING from 2026-09-06 09:24:08 UTC, same one-H100 RESERVED configuration. Run root `runs/reserved-20260906-p1-v2/`. All three tests passed; the eight-example smoke completed both seeds with exact A/C per-example losses and routes, all path guards, and immutable adapter tensors. Full frozen evaluation started after this successful smoke. The earlier job reported FAILED before replacement submission.

Completion receipt: replacement job `pt-5xgwtcam` reported SUCCEEDED. Both seeds completed all arms with exact historical A/C array replay and frozen-parameter guards. Full runner elapsed 42.315 seconds, optimizer updates zero. Analysis uses float64 reduction of stored per-example losses to avoid float32 summation noise; scientific definitions and guards are unchanged. Curated evidence is recorded in [Summary](summary.md) and [Detailed](detailed.md); interpretation awaits researcher confirmation.
