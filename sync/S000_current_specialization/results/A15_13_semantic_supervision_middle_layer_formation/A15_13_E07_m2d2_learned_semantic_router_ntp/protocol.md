# Protocol: A15_13_E07 M2D2 Learned Semantic Router Next-Token Prediction

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_ANALYSIS
Approval status: HUMAN_CONFIRMED on 2026-09-01
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: data construction, implementation, tests, smoke, two-seed full run, analysis, curated result records
Design frozen at: 2026-09-01 before implementation
Purpose: measure whether fine-domain supervision gives a learned causal token Router functional value beyond task-only routing
Primary Anchor: 15_13_04_m2d2_causal_lm_semantic_routing_anchor.md
Experiment role: learned-method recovery audit
Primary metric: equal-domain held-out token NLL difference, task-only minus semantic supervision
Treatment: gold fine-domain route cross-entropy in stage two
Controls: task-only fine Router; balanced shuffled fine-route supervision
Changed variable: stage-two fine Router supervision target
Held fixed: data, base, insertion layer, LoRA capacity, coarse stage, initialization, updates, optimizer, language objective
Pass: treatment lowers NLL in both seeds with positive pooled interval, improves semantic routing, and passes deletion and substitution gates
Cannot claim: Oracle value, deep semantics, native representation formation, or deployment
```

## 1. Definitions

One target token is one of sequence positions 64--255. Its prediction uses the logit at the preceding position. Token NLL is the natural logarithm of the inverse target-token probability. A learned Router reads the uncentered block-14 state at that causal prediction position. The selected shared, parent, and child rank-eight LoRA residuals are scaled by their learned route probabilities, matching the preceding learned-Router implementation family.

## 2. Anchor Alignment And Rivals

The experiment tests the learned-recovery clause of the Anchor. The strongest rival is route appearance without function: correct supervision raises route-label agreement but does not lower confirmation NLL or create non-interchangeable experts. The shuffled control separates correct semantics from supervised balanced partitioning.

## 3. Data Construction And Supervision

Use only the nine official M2D2 files listed in the Anchor. Raw and processed data live under `/data/250010109/datasets/m2d2_wikipedia_3x3/`. Non-empty natural-text records are selected by deterministic hash, joined only within the same fine domain and official split using the tokenizer end-of-sequence token, and packed into non-overlapping 256-token windows. Exact token-window duplicates are removed globally. Per fine domain use 1,024 train, 256 development, and 512 confirmation windows. Confirmation is never used for fitting, stopping, thresholds, labels, or checkpoint choice.

Gold coarse and fine labels are metadata; their strings are never rendered. Stage one may use gold coarse labels. Stage two treatment uses gold fine labels; shuffled labels are deterministic, balanced within each coarse domain, and independent of text and true fine label. Route losses use only prediction positions 63--254 corresponding to targets 64--255.

## 4. Model And Objective

Freeze every original Qwen3-0.6B-Base parameter and the tied language head. Add rank-eight shared, three-parent, and three-children-per-parent LoRA residuals to zero-indexed block 14. Stage one trains shared LoRA, parent experts, and the coarse Router with

$$L=L_{\mathrm{NTP}}+L_{\mathrm{coarse-route}}.$$

Freeze the coarse Router and parent experts at the stage-one final checkpoint. Stage two trains shared LoRA, child experts, and fine Routers. `LEARNED_TASK_ONLY` uses only $L_{\mathrm{NTP}}$; `LEARNED_SEMANTIC` adds unit-weight gold fine-route cross-entropy; `LEARNED_SHUFFLED` adds unit-weight shuffled fine-route cross-entropy. No load-balancing, clustering, prototype, contrastive, reconstruction, or representation regularizer is allowed.

## 5. Optimization, Conditions, And Checkpoints

Seeds are 17 and 29. AdamW uses learning rate `3e-4`, weight decay `0.01`, clipping `1.0`, five-update linear warmup and cosine decay. Microbatch is 8 sequences with accumulation 16, giving effective batch 128 on each one-GPU arm. Each stage is two full train passes: 72 optimizer updates per pass and 144 per stage. The fixed update-144 checkpoint is primary; development does not select another checkpoint. Save updates 0, 1, 5, 36, 72, and 144.

All three stage-two conditions for a seed receive byte-identical stage-one state and child initialization. Conditions run independently on one GPU; distributed data parallelism is forbidden.

## 6. Frozen Analysis And Verdict

Compute mean confirmation NLL with equal weight over nine fine domains and both seeds. The primary contrast is `NLL_TASK_ONLY - NLL_SEMANTIC`; the shuffled contrast is explanatory but registered. Use 10,000 paired bootstrap draws that resample windows inside every fine domain and preserve condition pairing.

`PASS_LEARNED_RECOVERY` requires semantic minus task-only improvement in both seeds, a positive pooled 95% lower bound, higher route macro-F1 and normalized mutual information, and positive NLL increases in both seeds for deleting the predicted active child and replacing it with each other child inside the predicted parent. `FAIL_NO_LEARNED_FUNCTION` applies when eligible evidence misses any functional gate. Missing conditions, seeds, per-token arrays, causal-future invariance, or route/expert isolation yields `INSUFFICIENT`.

Secondary diagnostics are perplexity, per-domain NLL, route entropy and maximum load, route switch rate, position-binned route agreement, gradient alignment, shared/parent/child residual norms, linear-probe macro-F1, 5-nearest-neighbor accuracy, and X-MoE-style collapse ratios. They explain but never rescue the primary verdict.

## 7. Procedure, Artifacts, And Freeze Ledger

Preflight verifies archive hashes, counts, balance, absence of label strings added by the pipeline, no cross-split token-window duplicates, exact 192-target masks, and future-token invariance. Unit tests must fail before implementation and then pass. Smoke requires finite forward/backward loss, frozen-base identity, stage freeze, and complete per-token artifacts. Full execution uses one reserved four-H100 node as explicitly requested; no fallback changes the scientific body.

Required artifacts are manifest and hashes, prepared tensors, code/config hash, stage checkpoints, per-token NLL and routes, route metrics, interventions, representation arrays, bootstrap samples, figures, completion audit, environment inventory, and job receipts. Any post-start change to data, labels, objective, architecture, condition logic, update count, primary metric, or verdict is an append-only amendment and invalidates affected evidence unless bounded explicitly.

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
