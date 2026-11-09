# Protocol: A15_13_E08 M2D2 Hard Semantic Route Next-Token Prediction

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_ANALYSIS
Approval status: HUMAN_CONFIRMED on 2026-09-01
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: data construction, implementation, tests, smoke, two-seed full run, analysis, curated result records
Design frozen at: 2026-09-01 before implementation
Purpose: decide whether the correct coarse-fine M2D2 partition itself has next-token functional value
Primary Anchor: 15_13_04_m2d2_causal_lm_semantic_routing_anchor.md
Experiment role: Oracle functional-value audit
Primary metric: worst-control equal-domain confirmation token NLL advantage
Treatment: hard gold fine-domain path with expert coefficient 1
Controls: balanced random within-parent path and one common child per parent
Changed variable: stage-two child grouping rule only
Held fixed: data, base, stage-one state, child initialization, active rank, updates, optimizer, NTP objective, shadow Router
Pass: semantic path beats both controls in both seeds with positive pooled interval and both child interventions
Cannot claim: learned routing, label discovery, deep semantics, native representation formation, or deployment
```

## 1. Definitions

A hard route uses document metadata to select one parent and child for every token. The selected expert output coefficient is exactly `1.0`; no Router probability or straight-through estimator enters expert computation. A shadow Router reads a detached uncentered block-14 state and predicts the same metadata only for diagnosis. It does not select or scale experts and its loss cannot update Base or LoRA experts.

The common control uses one rank-eight child per coarse domain. The random control assigns each sequence to one of three children using a deterministic balanced permutation within each coarse domain and split. The semantic treatment uses its true fine domain. The task target is always the next token and never the domain label.

## 2. Data, Task, And Causal Boundary

The dataset construction, 1,024/256/512 windows per fine domain, official split roles, 256-token length, 64-token context, 192-token target mask, global exact-window deduplication, forbidden rendered labels, and untouched confirmation boundary are identical to E07. The Router or hard selection attached to the logit predicting target \(x_j\) can use only the block-14 state at position \(j-1\). A suffix change after that position must leave the recorded route and injected residual unchanged.

## 3. Model, Stages, And Objective

Freeze Qwen3-0.6B-Base and its language head. Add block-14 rank-eight shared, three-parent, and three-children-per-parent LoRA residuals plus detached shadow Routers.

Stage one uses hard gold coarse routing with coefficient one and trains shared LoRA, parent experts, and the shadow coarse Router for two train passes. Stage two freezes parent experts and the coarse shadow Router, then trains shared LoRA, the condition-specific child bank, and shadow fine Router for two train passes. All arms optimize standard target-token NLL plus the detached shadow route loss; the latter updates only shadow Router parameters.

Use AdamW `3e-4`, weight decay `0.01`, clipping `1.0`, five-update warmup and cosine decay, microbatch 8, accumulation 16, effective batch 128, 72 updates per pass and 144 per stage. Seeds are 17 and 29. Fixed update 144 is primary. Save updates 0, 1, 5, 36, 72, and 144. All stage-two arms for one seed share byte-identical stage-one state and child initialization.

## 4. Conditions And Frozen Analysis

Run `HARD_COMMON`, `HARD_RANDOM`, and `HARD_SEMANTIC` for both seeds. Confirmation NLL is averaged first across target tokens in a window, then equally across the nine fine domains and seeds. Per seed compute semantic advantages over random and common; the primary statistic is their minimum. Use 10,000 paired within-fine-domain bootstrap draws.

`PASS_SEMANTIC_FUNCTIONAL_VALUE_NTP` requires both semantic advantages positive in both seeds, a positive pooled 95% lower bound, and positive NLL increases in both seeds with positive pooled lower bounds for active-child deletion and mean within-parent wrong-child substitution. `FAIL_NO_SEMANTIC_VALUE_NTP` applies to complete evidence that misses any value gate. Missing eligibility, isolation, causal, condition, seed, array, or intervention evidence yields `INSUFFICIENT`.

Perplexity, per-domain and position-bin NLL, shadow route agreement, route entropy, gradient same-fine versus different-fine alignment, residual norms, probe/nearest-neighbor readability, and collapse diagnostics are secondary. They cannot rescue a failed Oracle verdict.

## 5. Guards, Procedure, And Artifacts

Known-good isolation: changing shadow logits changes shadow predictions but not expert indices, weights, language logits, or LoRA gradients. Known-bad stop: any hard expert coefficient differs from one or any shadow loss gradient reaches a non-shadow parameter. No-op identity: zero child residuals make the three arms produce identical logits from the shared stage-one state. A balanced random arm may have balanced load and low semantic agreement; balanced load is not called semantic.

Data preflight precedes unit tests, GPU smoke, two seed-matched stage-one runs, six stage-two runs, confirmation unseal, interventions, analysis, figures, and completion audit. Full execution uses one reserved four-H100 node as explicitly requested. Artifacts and freeze/amendment rules match E07; raw outputs remain under the worker experiment root and only curated evidence enters Research_System.

| Block | State |
| --- | --- |
| A question and boundary | CONFIRMED |
| B data | CONFIRMED |
| C task and supervision | CONFIRMED |
| D architecture | CONFIRMED |
| E objective and optimization | CONFIRMED |
| F comparison and evidence | CONFIRMED |
| G execution | CONFIRMED |

Cross-block consistency: `PASS`.

Execution correction `C001` (2026-09-01, smoke only): PyTorch 2.8 rejected the trusted locally generated dataset cache because its new default `weights_only=True` excludes NumPy arrays. The loader now explicitly uses `weights_only=False` only for this SHA-recorded local cache and experiment checkpoints. The first smoke stopped before model training; no data, objective, condition, metric, or eligibility rule changed.
