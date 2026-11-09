# Protocol: A15_13_E13 Qwen-0.6B Mixed Answer-Only Semantic Router

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_RUN
Approval status: HUMAN_APPROVED_2026-09-02
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: DATA PREPARATION, IMPLEMENTATION, FULL TRAINING, EVALUATION, ANALYSIS, CURATED RESULT WRITING
Primary metric: fixed-development answer-token NLL learning efficiency
Seeds: 17 and 29
Resource: reserved four-H100 ACP job; no fallback
```

## 1. Purpose

Test whether offline semantic labels improve answer-only post-training efficiency and expert differentiation over parameter- and compute-matched ordinary LoRA routing.

## 2. Data And Evidence Boundary

Construct a balanced eight-source mixture. The intended senior-figure sources were MMLU, MMLU-Pro, BBH, GSM8K, MATH, GPQA, HumanEval, and MBPP. The reserved container has no external network and the shared cache contains only four of those exact sources. Before training, the executable cached-only mixture is therefore MMLU, RACE-high, ARC-Challenge, GSM8K, MetaMathQA, SciQ, HumanEval, and MBPP. RACE-high substitutes for harder broad comprehension, ARC-Challenge for difficult reasoning, MetaMathQA for MATH, and SciQ for science QA; these are explicit approximations, not renamed benchmarks. The dataset source is the eight-way semantic label. Prompts contain only task content and formatting instructions; source names are removed. Loss is computed only on reference-answer tokens. Use deterministic, source-balanced train, development, and evaluation partitions.

The researcher explicitly permits overlap with conventional evaluation material because this is a within-mixture controlled comparison. Consequently, per-source evaluation measures fitted-task behavior only. It must not be reported as uncontaminated benchmark generalization or compared numerically with the senior's 7B scores.

## 3. Models And Conditions

Freeze Qwen3-0.6B-Base and its language head; modify only zero-index block 14 MLP `down_proj`.

- `DENSE_R24`: one rank-24 LoRA adapter.
- `FLAT_TASK_R24`: eight rank-24 experts and an eight-way causal Router, trained only by answer-token cross entropy.
- `FLAT_SEM_R24`: the same model with source-label Router cross entropy.
- `FLAT_SHUFFLED_R24`: the same model with frequency-matched shuffled labels.
- `HIER_TASK_R8`: one shared, three coarse, and eight leaf rank-eight experts with task-only routing. The coarse groups are general/reading QA (MMLU, RACE-high, ARC-Challenge, SciQ), mathematical reasoning (GSM8K, MetaMathQA), and code (HumanEval, MBPP).
- `HIER_SEM_R8`: the same hierarchy with fixed source-to-coarse and source-to-leaf supervision.
- `HIER_GOLD_R8`: gold forced routes with unit expert coefficients, while shadow Routers are trained and logged; expert output is never multiplied by Router probability.

For `FLAT_TASK_R24`, `FLAT_SEM_R24`, `HIER_TASK_R8`, and `HIER_SEM_R8`, add a matched `LFB` variant. Loss-free load balance uses a non-gradient bias only for Top-1 selection: after each optimizer update, \(b_e\leftarrow b_e+10^{-3}(1/E-f_e)\), where \(f_e\) is observed route fraction; subtract the bias mean and clamp to \([-0.1,0.1]\). The original un-biased softmax probability remains available for diagnostics and residual scaling. No auxiliary load-balancing loss enters the objective.

## 4. Training

Use seeds 17 and 29, identical sample order inside each seed, sequence length 512, source-balanced batches, four data passes, global effective batch 128 examples, AdamW, learning rate \(2\times10^{-4}\) for LoRA and \(5\times10^{-4}\) for Routers, weight decay 0.01, five-update warmup, cosine decay, and gradient norm clip 1.0. Save and evaluate at 0%, 5%, 10%, 20%, 40%, 60%, 80%, and 100% of the exact optimizer-update budget. Checkpoint selection uses development answer-token NLL only.

## 5. Metrics And Decisions

The primary comparison is semantic versus task-only within the same topology and load-bias setting. Report development NLL curve area, target-loss token speedup, and final evaluation answer-token NLL. Separately report exact-match or pass/fail accuracy appropriate to each source, route-label agreement, route entropy/load, expert deletion and wrong-expert NLL, LoRA update singular-value effective rank, and pairwise Frobenius cosine similarity.

Semantic supervision improves learning efficiency only if both seeds have lower development curve area, reach the task-only 75%-budget loss with fewer answer tokens, and do not worsen final evaluation NLL. Lower expert similarity is only geometric evidence; non-interchangeable function additionally requires positive matched deletion or substitution cost. Loss-free bias is a load control, not semantic evidence.

## 6. Guards And Completion

Tests must prove answer-only masking, label-name absence from prompts, causal future invariance, matched parameter/active-rank accounting, unit coefficients for forced Oracle routes, shadow-Router logging, and loss-free-bias zero contribution to autograd loss. Completion requires every registered condition and both seeds, all scheduled development evaluations, per-source evaluation, routing arrays, expert intervention arrays, spectral metrics, code/data/model hashes, job receipt, and completion audit.

This is a Qwen-0.6B one-layer controlled reproduction of the senior-style evidence pattern. It cannot reproduce the senior's 7B absolute scores or all-layer geometry.

## 7. Append-Only Amendment

### C001 — 2026-09-02 — Cached-only task substitution

- Trigger: a live preflight inside the assigned reserved H100 worker confirmed `Network is unreachable`; the shared cache audit found exact MMLU, GSM8K, HumanEval, and MBPP data but no MMLU-Pro, BBH, MATH, or GPQA data.
- Decision: preserve eight balanced natural-language sources and the answer-only causal training design using the four explicit substitutes in Section 2. This follows the researcher's instruction to approximate the senior figure while finishing the controlled model comparison.
- Boundary: no result may be called an eight-benchmark reproduction or compared to the senior's absolute benchmark average. The eligible claim concerns learning efficiency, semantic routing, expert geometry, and intervention value inside this cached eight-source mixture only.

### C002 — 2026-09-02 — Executable coarse grouping audit

- After the cached-source substitution, the hierarchy is explicitly grouped by the actual source semantics: general and reading/science question answering contains MMLU, RACE-high, ARC-Challenge, and SciQ; mathematical reasoning contains GSM8K and MetaMathQA; code contains HumanEval and MBPP.
- A first partial launch inherited an obsolete source-index table and was intentionally stopped before any final checkpoint existed. Its early checkpoints are ineligible and excluded from every analysis.
- The corrected source-to-parent table is covered by a unit test. Full execution begins from initialization under a new run stamp; no weight or metric from the invalid partial launch may be reused.
- All other conditions, seeds, budgets, loss-free controls, and completion requirements remain frozen.

### C003 — 2026-09-02 — Random-label null correction and full rerun

- Post-run control audit found that the first executable `FLAT_SHUFFLED_R24` implementation used one fixed bijection from source ID to route ID. That operation only renamed the eight experts and preserved the source partition; normalized mutual information is invariant to that renaming. It was therefore not the registered random-label null.
- The corrected null assigns a deterministic sample-level label that is exactly balanced over eight routes and contains multiple route labels inside every source. It is fixed before training, uses no evaluation labels, and is covered by a unit test.
- The primary semantic-versus-task, Oracle, and loss-free comparisons from run `full-20260902T182655Z` did not depend on the invalid null, but that run is retained only as an audit trail. The complete 22-model and 62-evaluation suite must be rerun from initialization under one new run stamp so the canonical E13 record has a single code version.
