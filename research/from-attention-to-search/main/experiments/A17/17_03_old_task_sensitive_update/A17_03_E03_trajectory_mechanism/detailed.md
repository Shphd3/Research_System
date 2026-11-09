# A17_03_E03 Detailed execution and evidence ledger

[Summary](summary.md) · [中文总结](summary_cn.md) · [Protocol](protocol.md)

## 1. Result recap

Smoke12, replay4 and Full108 cells completed. Within-state initially-wrong pair-margin contrast out_norm-full is negative in24/36 cases. Mechanism/closure Unknown. No extra training/checkpoints.

## 2. Terminology and actual setup

State/history, three update directions, original wrong/correct groups, CE/pair/full-vocabulary metrics and exact resource scope are defined in the frozen Protocol. Parent model and22 input IDs: [config](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/config.json). Three seeds29/43/71; two orders; histories ordinary/protected; saved new steps1/16/50. Source batch is next20 original records; original ordinary next-step reference norm is used within each history pair. Actual model is full native FP32 Qwen3 last-o_proj, SDPA, deterministic/no TF32, no SAE.

## 3. Frozen contract and conformance

| Item | Expected / actual | Status | Evidence |
|---|---|---|---|
| Input/model/state identity |22 registered input assets, exact selected files |PASS|input access and freeze|
| Cells |12Smoke+4replay+108Full |PASS|qualification, worker, completion|
| Source/step/history matching |next20 at t, same ordinary external norm |PASS|batch diagnostics and independent audit|
| Readouts |dev800, two panels; smoke40 |PASS|raw record arrays|
| Freeze/no-op/restoration |byte/version guard, exact source20 restore |PASS|workers, replay receipts|
| Test boundary |closed |PASS|config and completion|
| New training |zero |PASS|analysis-only counters|
| Chinese exposition |expanded after submission, no numeric/scope changes |EXPOSITION_ONLY|frozen copy remains unchanged|

## 4. Primary criteria and evidence lineage

Primary: out_norm-full old pair and strongest-competitor margin change on the initial-old-error group, with repair counts; report all cases, both panels and equal case/seed/order summaries. No p-values/CI or selected winner. A missing argmax flip is not absence of a margin effect.

| Claim | Raw / computation | Unit and boundary |
|---|---|---|
| Repair gap by saved step |original E01 eval records -> trajectory.py -> trajectory/aggregate.json |six related case conditions, three seeds; only saved intervals|
| Same-state operator effects |baseline/cells -> audit_summarize.py -> case_contrasts.json |one finite update; fixed-source, fixed-state comparison|
| History interaction |two separately restored states at same t |includes source-gradient/downstream differences|
| Output mass vs choice |per-record CE/access/selection,b/h |identity, not parameter modules|
| Completion |worker/checksum/replay/audit receipts |engineering does not confirm science|

## 5. Eligible main results

| Saved step | Ordinary repairs | Restricted repairs | Ordinary losses | Restricted losses |
|---|---:|---:|---:|---:|
| 1 | 3 | 2 | 10 | 6 |
| 16 | 27 | 6 | 29 | 23 |
| 50 | 55 | 18 | 49 | 47 |
| 100 | 72 | 36 | 80 | 75 |

| Step | Restored history | Initial-old-error pair-margin contrast | Full-competitor-margin contrast | Net repair-count contrast, case mean |
|---|---|---:|---:|---:|
| 1 | ordinary | -0.000850 | -0.000851 | -1.333 |
| 1 | protected | -0.000885 | -0.000865 | -0.667 |
| 16 | ordinary | -0.000183 | -0.000218 | -0.167 |
| 16 | protected | -0.000441 | -0.000698 | -0.500 |
| 50 | ordinary | -0.001535 | -0.001228 | +0.333 |
| 50 | protected | -0.002458 | -0.001982 | -0.667 |

All108 Full cells qualified. No skipped/retried branches; complete per-case/panel tables are linked below. Support is bounded to the measured operators/states; the total100-step effect is not decomposed by summing these values.

## 6. Stage evidence and failures

Preflight strict input access passed. Three inherited component tests and source/math checks passed. Smoke12 cells and four independent exact replays passed. Full108 cells completed. Independent audit values: {"cells": 108, "aggregates": 3888, "decomposition_checks": 86400}; maxima: {"rounding": 0.00017014634885805427, "leakage": 1.139854310301962e-06, "baseline_replay": 0.0, "gradient_split": 4.198696973374788e-06, "finite_norm_match": 1.6391277313232422e-07}. Source CE improves for full36/36, out_norm36/36 states. No implementation failure/retry in this round.

## 7. Round record

Question: immediate operator versus accumulated state in old-error repair. Setup: registered Qwen3 last-o_proj and fixed Q, three finite operators. Training data used only to obtain source gradients; no cumulative training. Evaluation: exposed dev800, equal two panels; test never loaded. Result: above qualified finite matrix and saved trajectory. Insight/boundary: local effects can narrow the explanation, not identify full mediation. Next human mechanism decision Unknown; round two remains unexecuted.

## 8. Interpretation and boundary

Initially wrong/correct groups are determined before this round from old_endpoint. Their counterfactual effects are not full-population effects. Norm control distinguishes deletion and remaining-direction amplification; it does not convert CE sensitivity to a function label. Across steps the source batch changes. Across histories the model, gradient and downstream sensitivity change jointly. No expert/capacity/architecture claim.

## 9. Execution record and artifacts

Jobs: Smoke pt-c1i5f9pl, Full pt-8aoyrzuw. Profile h100-4-reserved, envelope default image, one node/four independent processes. Mounted pod logs under /data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/acp_receipts/pod. Reproduction: launch/prepare_submit.py with smoke/full; source/run.py reads frozen run config. Certificates and receipts bind exact command/image. Analysis source identities recorded before Full outcome reading.

[run](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z) · [frozen input/source](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/freeze.json) · [Full completion](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/completion.json) · [trajectory](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/trajectory/aggregate.json) · [all changes](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/metric_changes.json) · [case contrasts](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/case_contrasts.json) · [audit](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/analysis/full/engineering_audit.json) · [registered outputs](/data/250010109/MoE_Router/experiments/20261011_a17_trajectory_mechanism/runs/trajectory_20261011T090921Z/registration/receipt.json) · [current access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_trajectory_20261011T090921Z.json)

Registered IDs: representation_a17_03_trajectory_smoke_20261011t090921z, representation_a17_03_trajectory_full_20261011t090921z. Actual payload manifest enumerates freshly hashed readout files; no new model checkpoint was saved or claimed.
