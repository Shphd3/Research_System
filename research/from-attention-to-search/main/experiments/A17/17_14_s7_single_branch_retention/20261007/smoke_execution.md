# S7 single-branch Smoke execution record

[中文](smoke_execution_cn.md). 2026-10-07, Asia/Shanghai.

**Engineering qualification passed; the formal scientific experiment remains NOT RUN.** ACP job `pt-1r3ei3wj` was verified as `SUCCEEDED`; all four arm receipts report `PASS`. No formal training, automatic retry or follow-up mechanism job was submitted.

## Purpose

The formal question concerns new prediction learning and old prediction damage at equal training compute. This Smoke checked whether training, recovery and measurements can support that question. Incorrect target shifting, freeze failure, inconsistent recovery or SAE reconstruction replacing native prediction would invalidate a learning interpretation.

## Operations

Four reserved H100 GPUs ran independent Dense/MoE models with paired seeds 17/29. Only the final Attention-output LoRA factors and applicable router were trainable; there was one insertion point, one selected expert per MoE position and no added shared expert. The backbone and original FP32 SAE remained frozen. Each arm took eight GSM8K updates, then eight MMLU updates, without old-data replay.

After new-task update four, a separate process restored the state, reproduced update five and completed update eight. There were 64 logical updates plus four discarded continuous-reference updates. Each arm saw 3,876 valid answer targets: 3,812 GSM8K and 64 MMLU. Task losses were evaluated separately rather than interpreted through a pooled mean.

Fixed development records supplied native Attention outputs, frozen-SAE codes and reconstruction residuals. Replaying old outputs through the frozen native tail tested loss restoration. Full-vector software replay qualifies the interface; it is not selected-direction causal evidence or a trainable method.

## Result and boundary

Output factors changed; both MoE arms had nonzero router gradients after the zero-output initialization step. All frozen backbone/SAE state hashes remained unchanged. External-process recovery reproduced factors, optimizer, RNG, counters and next-step loss exactly. Event-file axes and valid-target counts passed; paired exposure matched for both seeds.

Old native-loss restoration had absolute error **0.0** in every arm. SAE displacement/residual bookkeeping passed registered numerical tolerances. This changes the implementation judgment from unqualified to qualified for this bounded frozen version.

It does not establish better MoE retention. The subset and training are small, full FLOPs are not aligned, and capacity/probability-attenuation rivals remain. Internal cache splits include official-test-origin benchmark records and are not an untouched official confirmation set. Smoke effects cannot select scientific margins.

## Provenance and next decision

Contract: [Smoke Protocol](smoke_protocol.md). Formal [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_14_s7_single_branch_retention/17_14_s7_single_branch_retention_anchor.md) and [Protocol](protocol.md) remain review drafts.

Evidence: [execution certificate](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/receipts/execution_certificate.md), [terminal verification](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/receipts/terminal_verification.json), [complete engineering receipt](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/runs/20261007T145134Z/smoke_receipt.json). The [freeze manifest](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/receipts/freeze_manifest.json) owns code, contracts, configuration, data and reused-source hashes.

The next decision is researcher review of formal data eligibility, full compute budget, practical learning/damage margins and new-learning non-inferiority guards. Qualification does not start formal training.
