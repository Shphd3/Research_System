---
experiment_id: A15_06_E04_30b_downstream_evaluation
anchor_id: A15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full_evaluation
approved_by: user
approval_date: 2026-08-09
resource_profile: 5090-8-spot
primary_metric: eight_task_zero_shot_accuracy_vector_at_30b
---

# Protocol: Six-Arm 30B Downstream Evaluation

## 0. Approval Snapshot

**Decision question.** Do the six seed-17 models trained to 30B tokens differ on the eight requested downstream benchmarks, and do those task-level results agree with or qualify their held-out-DCLM NLL ordering?

**Conditions.** Evaluate the immutable 30B endpoints for Vanilla-Full, Centered-Full, Local-HMT, Local-Random-Matched, Relay-HMT, and Relay-Random. No checkpoint is selected by downstream performance. All use the same tokenizer, evaluator version, task versions, zero-shot prompt contract, seed, maximum length, and offline task cache.

**Primary evidence.** The primary result is the vector of task accuracies for ARC-Challenge, ARC-Easy, HellaSwag, LAMBADA_OPENAI, PIQA, RACE, Social IQA, and Winogrande. Each task is reported separately. An unweighted macro average is navigation only, not a universal capability score.

**Validity first.** Before scoring, the evaluator must prove that Centered and projected/Relay Routers use the checkpointed running means and deployed subspaces in evaluation mode, that these buffers do not update, and that repeated inputs reproduce identical logits and routes.

**Approved scope.** Protocol, evaluator adaptation, tests, one limited smoke, one single-node 8x5090 full evaluation job, aggregation, figures, and result records are approved.

**Cannot claim.** One seed cannot establish method robustness. Task accuracy cannot identify the unique mechanism of a gain, universal H/M/T semantics, or training efficiency.

## A. Anchor Alignment — CONFIRMED

This is the terminal downstream clause already registered by A15_06 E03. It evaluates the completed 30B endpoints and does not reopen the failed two-seed 10B Relay-HMT certificate.

## B. Checkpoint Contract — CONFIRMED

All six endpoints are at step 38,147 (30,000,021,504 nominal tokens) under:

`/data/250010109/MoE_Router/outputs/online_spectral_router_training/osrt-30b-<arm>-s17/checkpoints/checkpoint-38147/`

Each must contain one model state and eight optimizer shards; downstream evaluation reads only the model state. The evaluator records checkpoint SHA-256, global step, total tokens, source manifest, arm configuration, and tokenizer digest. The already completed 1,024-document DCLM NLL at the same step remains the paired language-model reference.

## C. Router Evaluation-State Guard — CONFIRMED

For every arm, load the exact training runtime and set `model.eval()` before any benchmark request. Snapshot all persistent Router buffers before and after smoke and full evaluation.

Required arm-specific checks:

1. **Vanilla-Full:** `router_center_input=false`; no running mean may be subtracted.
2. **Centered-Full:** every layer uses the nonzero checkpointed `router_running_mean`; two identical forwards leave it bitwise unchanged.
3. **Local-HMT and Local-Random-Matched:** blocks 2--4 have initialized, orthogonal, nested deployed bases; effective Gate weights equal the registered projected weights for H/M/T. Because the deployed frames are checkpointed in BF16, the maximum Gram/nesting residual is required to be at most $10^{-3}$; the residual itself is reported rather than described as exact FP64 orthogonality.
4. **Relay-HMT and Relay-Random:** blocks 2--4 receive the block-1 Relay source, not their local Router source; the checkpointed shared center and deployed bases are used.
5. **All projected arms:** `online_covariance_ema`, `online_statistics_mean`, `online_u64`, `online_u320`, `online_random_haar`, refresh count, and last gamma remain unchanged during evaluation.

On one frozen token batch, replay native Router logits and top-1 winners from captured effective inputs and weights. Maximum logit error must be at most $2\times10^{-3}$ in BF16 and winner agreement must be 1.0 except exact ties, which must use the training operator's tie rule. Two repeated full forwards must have identical logits, routes, and buffer hashes.

As a diagnostic only, compare projected-arm native routes with a full-weight no-projection replay. Nonzero divergence proves that the projection is active; the ablation output is never used for benchmark scoring.

## D. Benchmark Contract — CONFIRMED

Evaluator versions are pinned to `lm-eval==0.4.12`, `transformers==4.53.3`, and the frozen training tokenizer. The suite is zero-shot, maximum length 1,024, no chat template, no added BOS, seeds 42, request caching enabled, and 10,000 evaluator bootstrap iterations where supported.

| Task | lm-eval name | Registered metric |
| --- | --- | --- |
| ARC-Challenge | `arc_challenge` | `acc_norm` |
| ARC-Easy | `arc_easy` | `acc_norm` |
| HellaSwag | `hellaswag` | `acc_norm` |
| LAMBADA_OPENAI | `lambada_openai` | `acc` |
| PIQA | `piqa` | `acc_norm` |
| RACE | `race` | `acc` |
| SIQA | `social_iqa` | `acc` |
| Winogrande | `winogrande` | `acc` |

The task cache must be fully available offline before full submission. The smoke evaluates two examples from LAMBADA, PIQA, and one multiple-choice task for all six arms. Missing cache, task-version drift, or any network fetch requirement blocks full evaluation until repaired without changing the suite.

## E. Analysis Contract — CONFIRMED

Report all six-by-eight task scores and evaluator standard errors/intervals. For each task, compare every arm with Centered-Full and report paired item-level differences when lm-eval sample outputs provide item identity. Also report the frozen 30B DCLM NLL and load metrics beside downstream scores.

No single scalar determines a universal winner. A descriptive `downstream_breadth` label is allowed only when one arm is strictly higher than Centered-Full on at least six of eight tasks and lower on no more than one, with item-level uncertainty supporting the same direction on at least four tasks. Otherwise report task-specific mixed evidence. The macro average is unweighted and marked navigation-only.

The main verdict is:

- **Pass for task transfer:** an arm meets the breadth rule relative to Centered-Full.
- **Fail for broad transfer:** complete evidence does not meet the rule; task-specific gains remain visible.
- **Insufficient:** checkpoint/Router guard, suite identity, task completion, or immutable result reconstruction fails.

## F. Execution And Reproducibility — CONFIRMED

The full evaluator uses one ACP `5090-8-spot` node. Six worker processes bind one arm each to one GPU and run the eight tasks; the remaining GPUs are unused or reserved for smoke/diagnostics. The job name is `a15-30b-downstream-eighttask-s17`. Raw outputs live under `/data/250010109/MoE_Router/outputs/online_spectral_router_training/downstream_30b_e04/` and are immutable per arm/task.

Required outputs are: suite YAML and hash, checkpoint manifest, environment/package manifest, Router guard JSON, raw lm-eval JSON, item-level samples, per-task summary, job ledger, logs, and source manifest. No result file may be overwritten.

## G. Failure And Freeze Rules — CONFIRMED

NaN/Inf, OOM, missing task cache, model-state mismatch, Router-buffer mutation, route replay failure, inconsistent tokenizer, task failure, or missing raw result stops the affected arm and makes the full comparison Insufficient until exact repair. Low accuracy, collapse, or disagreement with NLL is a scientific result and never triggers deletion or checkpoint replacement.

Cross-block consistency: `PASS`. The scientific suite, zero-shot contract, arm set, endpoint, metrics, and verdict rule freeze at the first smoke execution. Post-start changes require an append-only amendment.

## H. Amendment 1 — Effective LB Status Of The Source Models (2026-08-09)

The six source runs declared `lambda_lb=0.01`, but the A16 differentiability audit established that their re-entrant activation-checkpoint path returned LB inside a nested auxiliary dictionary that did not connect to backward. Paired one-step replay produced identical model tensors and all eight optimizer shards with nominal LM+LB versus LM-only until activation checkpointing was disabled, after which LB changed both optimizer and model state.

The downstream evaluation remains valid as a comparison of the six immutable trained models. However, it must describe them as models trained with LB telemetry configured but without an effective LB gradient, and it cannot attribute task differences to LB regularization. No benchmark, checkpoint, Router evaluation behavior, metric, or verdict rule changes.
