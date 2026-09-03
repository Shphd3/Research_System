# Protocol: A15_13_E14 Unified Diagonal-GMM Pseudo-Label Oracle-Gap Audit

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_FULL_RUN_UNIFIED_ANALYSIS
Approval status: HUMAN_CONFIRMED in the 2026-09-03 execution request
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope: data acquisition, implementation, tests, every missing two-seed training arm, immutable checkpoint manifest, unified evaluation, completion audit, figures, summary, and detailed record
Design frozen at: 2026-09-03 before E14 implementation
Primary Anchor: 15_13_05_gmm_pseudolabel_oracle_gap_anchor.md
Primary evidence: answer/target-token development NLL and learning-efficiency gap to Oracle, guarded by the registered task score and selective expert interventions
Final verdict vocabulary: A / B / C only
```

## 1. Question And Evidence Boundary

Can train-only final-layer diagonal-GMM hierarchical pseudo labels train a causal semantic Router closer to a forced-correct-path unit-coefficient Oracle while preserving task performance, and does gradient-free load balancing further close that gap? Training-result checks cannot delete a condition, change a hyperparameter, or select a checkpoint. Route semantics, balanced load, and parameter geometry never substitute for task likelihood, task scores, or expert interventions.

## 2. Data And Pseudo-Label Contract

### 2.1 M2D2 surface

Reuse the hash-recorded M2D2-Wikipedia balanced `3×3` windows: 1,024 train, 256 development, and 512 confirmation windows per fine domain; sequence length 256; positions 0--63 are context and positions 64--255 receive next-token cross entropy. Domain names are absent from model input.

Fit a rank-64 principal-component basis to TRAIN frozen-Qwen final-layer means over the complete 256-token window. On the complete projected vectors fit a three-component diagonal-covariance Gaussian mixture, then a three-component child mixture inside each predicted parent. Every fit uses 20 deterministic restarts, at most 100 expectation-maximization iterations, and train mean log likelihood alone for selection. Truth cannot affect fitting, restart selection, permutation, or frozen assignments. Save states, PCA, every restart trace, posterior probabilities, assignments, source hashes, and label hashes.

### 2.2 Eight-task surface

Use MMLU, MMLU-Pro, BBH, GSM8K, MATH, GPQA, HumanEval, and MBPP. Freeze 512 train, 64 development, and 64 internal-evaluation records per source using deterministic source-local ordering; if a source has fewer unique records, cycle only after exhausting all unique records and record every repeated identifier. Prompts never contain source names. Sequence length is 512; preserve the answer suffix when truncating the prompt; cross entropy applies only to answer tokens including end-of-sequence.

For eight pseudo leaves, fit the same train-only PCA-64 and parent diagonal mixture. Sort parents by train assignment count and allocate child counts `3,3,2`; ties use numeric component index. Fit child diagonal mixtures with the same 20-restart, 100-iteration likelihood-only rule. Source truth is used only after freezing for diagnostics. All task scores are labeled `mixed-task internal capability diagnostics`, not uncontaminated benchmark generalization.

## 3. Architecture And Training Conditions

Freeze Qwen3-0.6B-Base and the language head. Add modules only to zero-indexed block 14 `down_proj`. A hierarchical token activates rank-eight shared, parent, and leaf LoRA residuals, total active rank 24. A flat token activates one rank-24 expert. Online Routers read only the current or earlier causal block-14 state.

M2D2 adds, for seeds 17 and 29: diagonal-GMM learned hierarchy; its load-bias version; diagonal-GMM hard pseudo path with coefficient one and shadow Router; its load-bias version; and a frequency-matched random pseudo-label hierarchy if absent. Each has stage one with 144 updates over two passes, training shared LoRA, coarse experts, and coarse Router. Stage two freezes only the coarse Router; coarse experts remain trainable while shared LoRA, fine experts, and fine Router train for 144 more updates. Total is 288. No coarse-row-space subtraction is allowed.

The exact eight-task surface trains, for seeds 17 and 29: one rank-24 LoRA; flat task-only; hierarchical task-only; frequency-matched random hierarchy; gold-source-supervised hierarchy; diagonal-GMM learned hierarchy with and without load bias; diagonal-GMM hard pseudo path with and without load bias; and gold-source forced-path unit-coefficient Oracle. Use four deterministic train passes and 128 optimizer updates, microbatch 8, accumulation 16, effective batch 128, AdamW weight decay `0.01`, LoRA learning rate `2e-4`, Router learning rate `5e-4`, five-update warmup, cosine decay, and gradient clipping `1.0`. All matched conditions share initialization family, example order, answer-token budget, optimizer, and fixed final-checkpoint rule.

Route cross entropy has unit weight and updates Routers only. Task loss updates active LoRA parameters and, for learned paths, the selected probability coefficient. Hard pseudo and Oracle paths select experts from frozen labels with coefficient exactly one while training a shadow Router for diagnostics. Gradient-free load bias enters only top-one selection; its counts aggregate every valid token across the entire effective batch before one bias update.

## 4. Preflight And Training-Time Guards

Before full training, unit tests must verify: frozen-weight invariance; finite loss; correct stage trainable sets; exact 144-to-144 M2D2 handoff; label leakage guards; route-loss gradient isolation; hard-path coefficient one; future-token perturbations do not change earlier routes; full-effective-batch load accumulation; and checkpoint recovery. Fixed development checks verify finite loss, saved checkpoints, unchanged frozen parameters, and no fully inactive route or expert. They cannot change the frozen design.

## 5. Immutable Checkpoint Manifest Gate

Formal final evaluation starts only after every required checkpoint exists and a manifest records model name, data version/hash, seed, optimizer updates, seen answer/target tokens, trainable and active parameters, supervision source, load-bias state, expert-training path, checkpoint path, and SHA-256. Reused old models enter only when their data, architecture, and evaluator contracts exactly match; historical nonmatching eight-source E13 models remain contextual evidence and do not enter the exact-task primary comparison.

## 6. Unified Evaluation

All models use one frozen evaluator, prompt set, decoding configuration, answer extraction, and per-item output schema. MMLU, MMLU-Pro, and GPQA report multiple-choice accuracy; BBH exact match; GSM8K and MATH final-answer accuracy; HumanEval and MBPP sandboxed executable `pass@1`. Report each seed and the two-seed mean. Teacher-forced token accuracy is not a benchmark score.

Learning efficiency reports fixed-development answer-token NLL against seen answer tokens, normalized area under the loss curve, answer tokens to reach task-only's 75%-budget loss, final NLL, and equal-token-budget differences. Routing reports truth agreement, accuracy after train-only mapping, entropy, loads, max/min load, probability calibration, and learned-to-Oracle path agreement. Expert interventions report NLL changes for deletion, same-parent wrong leaf, other-parent expert, unit coefficient, and allowed forced pseudo/gold paths. Parameter analysis reports pairwise update cosine, singular values, stable/effective rank, and update norms.

## 7. Frozen Comparisons And Verdict

The first result table is the complete eight-task table. The first curve compares matched task-only, diagonal-GMM learned routing, diagonal-GMM hard pseudo routing, and Oracle on identical axes. Every learned semantic model reports final-NLL gap, loss-target token ratio, eight task differences, path agreement, and deletion/substitution intervention gaps to Oracle.

- `A`: hard diagonal-GMM shrinks final-NLL and curve-area Oracle gaps versus learned diagonal-GMM in both seeds, does not reduce the two-seed task macro average versus matched task-only, and moves at least one selective expert intervention toward Oracle.
- `B`: route semantics are learned, but the complete eligible task, efficiency, or functional evidence fails A.
- `C`: any registered condition, seed, per-item prediction, curve, route array, intervention, geometry artifact, finite-value check, or completion audit is missing or ineligible.

Load bias is effective only if on versus off improves the decision-bearing task quantity in both seeds. Higher clustering agreement, entropy, load balance, or parameter difference alone cannot change B to A.

## 8. Execution And Artifact Contract

Approved compute is one reserved four-H100 ACP node, one independent one-GPU shard per GPU. The worker root is `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/`; datasets live under the verified writable root `/data/250010109/datasets/` (`/data/25001019/` was rejected by the filesystem before acquisition). Raw logs, checkpoints, datasets, predictions, and arrays remain in the worker root or dataset root. Canonical `summary.md`, `detailed.md`, audited figures, and tables are written beside this Protocol only after completion.

Expected execution order is: acquire and hash data; fit and freeze labels; train all missing arms; build and hash the checkpoint manifest; run all formal evaluations; render and inspect figures; run completion audit; write evidence records. Any failure or restart is retained in the run ledger.
