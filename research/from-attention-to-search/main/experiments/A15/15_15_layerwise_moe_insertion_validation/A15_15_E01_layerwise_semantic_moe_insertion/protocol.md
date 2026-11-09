# Protocol: A15_15_E01 Layerwise Semantic MoE Insertion

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
Approval source: explicit researcher approval in codex-thread:01a054b9-ff32-7012-aae0-ccfea85152cf on 2026-09-04
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: worker implementation, regression tests, smoke, full run, unified analysis, figures, summary, and detailed evidence
Design frozen at: 2026-09-04 before implementation
Purpose: test whether frozen static semantic readability predicts a functionally better MoE insertion block, and close the missing flat Oracle control
Primary Anchor: 15_15_layerwise_moe_insertion_validation_anchor.md
Primary metric: learned-to-Oracle NLL-gap interaction I = G_1 - G_9
Pass: I > 0 in both seeds, with no task-headroom reversal and non-worse block-9 route/function guards
Fail: I <= 0 in both seeds
Insufficient: seed directions disagree, any registered arm is missing/ineligible, or a validity guard fails
Cannot claim: an all-layer optimum, monotone depth law, or universal architecture rule
```

## 1. Terminology And Definitions

- **Block index:** zero-indexed Qwen Transformer block. Block 9 is the E15 descriptive high-readability candidate; block 1 is the frozen low-readability contrast.
- **Task-only:** no semantic classification loss; the Router receives only language-model gradients through selected probability coefficients.
- **Learned semantic path:** the Router predicts the path causally and receives true parent/child route cross-entropy in addition to next-token loss.
- **Oracle path:** true source labels choose experts directly and expert output has coefficient one; a shadow Router remains diagnostic.
- **Expert utility:** increase in held-out next-token NLL after deleting or substituting the selected expert. It is not route-label agreement.

## 2. Anchor Alignment

This is an operationalization and causal follow-up to the descriptive E15 layer map. The changed variable is insertion block 1 versus 9. Data, base weights, active LoRA rank, stage budgets, optimizer, seeds, splits, and evaluation are held fixed. Flat Oracle at block 14 closes a missing topology reference but does not determine the primary layer verdict.

## 3. Tested Hypothesis

Block 9 has a smaller learned-to-Oracle confirmation NLL gap than block 1 because its current-token state makes the true coarse/fine partition easier for the causal Router to recover.

## 4. Rival Explanations

1. Static readout is only correlational and does not predict learned routing or expert function.
2. One block trains better for generic LoRA reasons rather than semantic reasons; task-only and Oracle controls separate this.
3. A result is caused by parent-expert freezing or coarse-row-space subtraction; the 2×2 learned-semantic ablation separates these implementation choices.

## 5. Data Construction And Provenance

Use `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`, SHA-256 `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8`. It contains nine equal cells, each with 1,024 train, 256 development, and 512 confirmation windows of length 256. Positions 0--63 are context; next-token cross-entropy is computed at targets 64--255. Domain names never enter the text. Train builds parameters, development supplies fixed curves only, and confirmation is evaluated after checkpoints freeze.

The flat Oracle closure reuses `/data/250010109/datasets/a15_e14_benchmark/processed.pt` and the exact E14 train/development/evaluation split and hashes. True source labels are permitted only as route supervision or forced paths in registered semantic/Oracle arms.

## 6. Learning Task And Permitted Supervision

The task is causal next-token prediction. At token \(t\), a Router may read only the selected block state at positions at most \(t\). M2D2 task-only uses no route labels; learned semantic uses true parent and child labels in route cross-entropy; Oracle uses them as forced paths. The flat closure uses the eight dataset-source labels. Confirmation truth never selects checkpoints or changes configuration.

## 7. Model And Frozen Variants

All Qwen3-0.6B-Base parameters and the language head are frozen. Exactly one block's MLP `down_proj` receives LoRA residuals.

For M2D2, each token activates shared rank 8, one parent rank 8, and one child rank 8, total active rank 24. The learned-semantic 2×2 factors are: child Router reads native state or state with the centered parent-Router row space projected out; parent experts freeze or remain trainable in stage two. Parent Router always freezes in stage two. The registered mainline arm is native child input with trainable parent experts.

For Flat Oracle, one of eight rank-24 experts is selected by the true source label. Its output coefficient is one. The flat shadow Router receives route cross-entropy but cannot select or scale experts.

## 8. Training Objective And Optimization

M2D2 task loss is mean next-token cross-entropy over 192 target positions. Learned semantic adds unit-weight parent route cross-entropy in stage one and unit-weight conditional-child route cross-entropy in stage two. Oracle adds the same shadow-Router losses, detached from expert selection. AdamW uses learning rate `3e-4`, weight decay `0.01`, five-update warmup, cosine decay over the full 288-update lineage, and gradient clipping `1.0`. Microbatch is 8, accumulation 16, effective batch 128.

Flat Oracle follows E14 exactly: four deterministic data passes, 128 updates, microbatch 8, accumulation 16, effective batch 128, LoRA learning rate `2e-4`, Router learning rate `5e-4`, five-update warmup, cosine decay, weight decay `0.01`, and clipping `1.0`.

## 9. Conditions, Seeds, And Checkpoints

Seeds are 17 and 29.

For each of blocks 1 and 9:

1. hierarchical task-only, native child input, parent experts trainable in stage two;
2. hierarchical forced-gold Oracle, unit expert coefficients, parent experts trainable in stage two;
3. learned semantic: native input / frozen parent experts;
4. learned semantic: coarse-row-space removed / frozen parent experts;
5. learned semantic: native input / trainable parent experts;
6. learned semantic: coarse-row-space removed / trainable parent experts.

At block 14 add Flat Oracle for both seeds. Existing E14 block-14 Flat task-only, hierarchical task-only, and hierarchical Oracle checkpoints are reused read-only only after identity checks.

## 10. Primary Metric And Frozen Analysis Plan

For each seed and block, confirmation NLL is balanced equally over nine M2D2 cells. Let \(G_\ell=N^L_\ell-N^O_\ell\) for the native-input/trainable-parent learned arm. The primary interaction is \(I=G_1-G_9\) in nats per target token. Report both seeds and their arithmetic mean; seeds are the independence unit. No condition is excluded for an unfavorable result.

Pass requires \(I>0\) in both seeds, block-9 Oracle headroom \(N^T_9-N^O_9\) not smaller than block 1 in either seed, and block-9 learned route agreement plus both deletion and wrong-child NLL increments not worse than block 1 in their two-seed means. Fail requires \(I\le0\) in both seeds. All other complete outcomes are Insufficient.

## 11. Secondary Metrics And Guards

Report development learning curves versus optimizer update; parent/child route accuracy and normalized mutual information with true labels; expert load; deletion, wrong-child-one, and wrong-child-two NLL increments; task-only-to-Oracle headroom; each E12 factor effect; Flat Oracle versus Flat task-only and hierarchical Oracle on NLL, internal eight-task score, and interventions. Route metrics cannot substitute for task NLL.

## 12. Known Good, Bad, And Confusing Cases

- Known good: forced-gold paths must exactly equal stored labels and coefficients must equal one.
- Known bad: shuffled labels must not be accepted as gold; a future-token perturbation must not alter an earlier route.
- Confusing: block 9 is only a descriptive E15 candidate because one shuffle qualification edge missed by `0.000132` nat; this experiment tests function directly rather than treating E15 as qualified truth.

## 13. Scientific Procedure And Stage Contracts

| Stage | Trainable objects | Frozen objects | Data / updates | Objective | Handoff |
|---|---|---|---|---|---|
| M2D2 stage 1 | shared LoRA, parent experts, parent Router or Oracle shadow Router | Qwen, language head, child experts and child Router | 2 passes, 144 updates | next-token CE + parent route CE for semantic/Oracle; next-token CE only for task-only | save exact adapter, optimizer, scheduler, update and RNG state |
| M2D2 stage 2 | shared LoRA, child experts/Router, and parent experts only in trainable-parent arms | Qwen, language head, parent Router; optionally parent experts | 2 passes, updates 145--288 | next-token CE + child route CE for semantic/Oracle; next-token CE only for task-only | final checkpoint, curves, frozen confirmation evaluation |
| Flat Oracle closure | eight flat experts and shadow Router | Qwen and language head | 4 passes, 128 updates | answer-token CE + eight-way shadow route CE | final checkpoint, E14-matched NLL/benchmark/intervention evaluation |

Optimizer/scheduler states continue across the two M2D2 stages. Each layer/seed/supervision family has its own stage-one lineage; the four learned-semantic stage-two ablations share the exact same learned-semantic stage-one checkpoint.

## 14. Algorithm, Output, And Provenance Contract

Worker root: `/data/250010109/MoE_Router/experiments/20260904_a15_15_e01_layerwise_moe_insertion`. Required outputs are immutable configuration, test and smoke logs, stage checkpoints, final checkpoints, per-window confirmation arrays, route arrays, interventions, learning curves, Flat Oracle benchmark predictions, analysis tables, figures, completion audit, and job receipt.

The selected resource is one reserved four-H100 ACP node: workspace `share-space`, cluster `share-cluster`, worker spec `n6ls.iu.i40.4`, one worker, four visible GPUs, normal priority, image `ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`. All data/model access is local and offline; if an ACP process unexpectedly contacts Hugging Face it must use `https://hf-mirror.com`.

## 15. Success, Failure, And Insufficient Evidence

The registered Pass/Fail/Insufficient mapping is exactly Section 10. Full-run completion additionally requires all 26 final checkpoints (24 layer-study plus 2 Flat Oracle), all interventions, two Flat Oracle 512-item benchmark prediction files, finite values, frozen-base invariance, and figures generated from frozen tables.

## 16. What This Cannot Claim

The experiment cannot identify the globally optimal layer, prove a monotone relation over depth, show that labels are available without supervision, or generalize beyond the two selected blocks, frozen model, datasets, and LoRA topology.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Status | Basis |
|---|---|---|
| A question/boundary | CONFIRMED | user explicitly requested a new problem line testing layer choice |
| B data | CONFIRMED | user requested the existing natural-language setup and static-audit linkage |
| C task/supervision | CONFIRMED | causal next-token task and existing semantic/Oracle definitions |
| D architecture | CONFIRMED | user requested layer-9 MoE plus low-readability comparator and existing ablations |
| E optimization | CONFIRMED | exact inherited E12/E14 matched settings |
| F comparison/evidence | CONFIRMED | static-readability-to-functional-value question |
| G execution | CONFIRMED | explicit implementation, full run, and reserved 4×H100 approval |

Cross-block consistency: `PASS`. The scientific body freezes before the first implementation edit. Any outcome-changing change after start must be appended here with eligibility impact; it may not silently replace the registered body.

### Execution record amendment 1 — 2026-09-04

- First ACP job: `pt-owrlkt10`.
- Observed state: tests passed `11/11`; GPU smoke stopped before any training because the audit enumerated the injected adapter through `backbone.parameters()` and misclassified its expected gradient as a frozen-base gradient.
- Change: the frozen-gradient guard now records base-parameter identities before injection and checks only those identities. A regression test failed before the repair and the complete local suite then passed `12/12`.
- Scientific-body impact: none. Data, task, models, layers, objectives, conditions, seeds, metrics, and verdict rules are unchanged. The failed job produced no training checkpoint and is ineligible evidence; the replacement job starts from step zero.

### Execution record amendment 2 — 2026-09-04

- Replacement ACP job: `pt-lxue71oe`; run stamp `20260904T011100Z`; resource remains the registered single-node reserved 4×H100 profile.
- Pre-training evidence: the complete regression suite passed `12/12`. GPU smoke passed the causal-prefix check at blocks 1 and 9, frozen-base gradient boundary, exact Flat Oracle forced path, and unit expert coefficient.
- Current state at synchronization: ACP reports `RUNNING`. The observed smoke losses are finite but are debug-only and ineligible for scientific comparison.
- Eligibility impact: none yet. No result may be declared until all registered checkpoints, unified evaluations, interventions, tables, figures, and the completion audit are complete.

### Execution record amendment 3 — 2026-09-04

- Replacement ACP job `pt-lxue71oe` finished with platform state `SUCCEEDED`.
- The immutable manifest contains all 38 registered checkpoint records. Unified evaluation produced 96 layer-study intervention arrays, 6 Flat Oracle intervention arrays, and 1,024 Flat Oracle per-item benchmark predictions.
- The first frozen analysis returned typed verdict `INSUFFICIENT`; seed interactions were `+0.000625` and `-0.000911` nat/token. No registered condition was removed.
- Three additional explanatory figures were rendered only from the already frozen E15 and E01 tables. No checkpoint, metric, comparison, or verdict rule changed. The completion audit was rerun and again returned `FULL_RUN_COMPLETE` with no errors.
