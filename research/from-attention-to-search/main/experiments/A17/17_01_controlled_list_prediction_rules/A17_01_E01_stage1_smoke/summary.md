# Summary: A17_01_E01 Stage-1 Smoke

Engineering: `PASS` (31/31 gates). Platform: `SUCCEEDED`, job `pt-2m4rvpt4`. Scientific result: `NOT_EVALUATED`. Researcher mechanism judgment: `Unknown`.

## 1. Purpose

Qualify paired FIRST/LAST data and a bounded training/update-measurement pipeline. Measure whether the three existing models already perform this specific task before adaptation. This round does not decide whether shared learning helps or interferes stably.

## 2. Hypothesis

The generator and runner can preserve correct one-answer supervision, both novelty definitions, four-rank answer normalization, telemetry, saves and external-process resume. Scientific rivals remain useful cross-rule learning versus harmful shared updates; saturation, source-batch coverage and numerical resolution can obscure either relation.

## 3. Analysis Method

The 5,600-row release contains 4,000 train, 800 dev and 800 test records, with FIRST/LAST pairs. Order-new holds out exact ordering but retains unordered content seen in task training. Combination-new also holds out unordered content. These definitions make no pretraining novelty claim.

All model metrics use dev only. Each separate panel has 400 answers; combined has 800. Values below are full-vocabulary top-1 accuracy / mean answer CE in nats. Dense/Qwen independently trained 32 AdamW updates, 64 valid answers/update, hence 2,048 answers/model. S7 was initial-capability-only. A restored plain-SGD probe separately read all four source/recipient rule cells, with no-op reference. Ten CPU tests and 31 GPU engineering gates were checked; no scientific CI was computed.

## 4. Conclusion

| Model | State | Order-new | Combination-new | Combined |
|---|---|---|---|---|
| S7-fresh exact33B | initial | 0.00% / 10.577504 | 0.00% / 10.579289 | 0.00% / 10.578396 |
| Dense exact33B | initial | 0.00% / 10.902297 | 0.00% / 10.91214 | 0.00% / 10.907218 |
| Dense exact33B | final | 100.00% / 0.02564373 | 100.00% / 0.027313172 | 100.00% / 0.026478451 |
| Qwen3-0.6B-Base | initial | 73.75% / 1.0347961 | 72.25% / 1.0303237 | 73.00% / 1.0325599 |
| Qwen3-0.6B-Base | final | 98.75% / 0.053326474 | 98.75% / 0.11264566 | 98.75% / 0.082986065 |

Qwen Base shows substantial prior performance, but it had not answered every example correctly in this fixed Chinese format. Dense reaches all-correct observed dev performance after short adaptation. Initial zero top-1 accuracy does not establish absence of list-reading ability; final all-correct dev does not establish universal mastery. Carrier architectures and pretraining histories differ, so this is not a clean architecture comparison.

The engineering chain passed: actual four H100 ranks, correct token coordinates, finite losses, TensorBoard, update16/32 saves, new-process resume from16, and finite restored four-cell readouts. All actual saved states are registered; update32 restoration and uninterrupted-trajectory parity remain `NOT_CHECKED`, and GB payload SHA256 is `NOT_COMPUTED`.

Finite updates do not establish stable help/harm. The combined self-rule guard fails for Dense LAST and Qwen FIRST; Qwen FIRST produces zero measured deltas at this resolution. Smoke sources are lexicographic first32 training rows/rule: all FIRST answers are 红. They qualify plumbing, not representative rule-average learning. Separate panels can have opposite signs and cancel when combined. Saturation, one selected source batch, one seed and uncalibrated numerical resolution prevent a scientific verdict. Test stayed unopened by models; S7 was not trained. No frequency or Full run was submitted.

AI suggestion for the researcher's next decision: accept or repair the engineering chain, then prospectively define earlier operating checkpoints, balanced independent source batches and a numerical-resolution check before a separate scientific Protocol. This suggestion grants no run approval.

[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md) · [Protocol](protocol.md) · [Detailed](detailed.md) · [terminal verification](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/terminal_verification.json) · [execution certificate](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/execution_certificate.md).
