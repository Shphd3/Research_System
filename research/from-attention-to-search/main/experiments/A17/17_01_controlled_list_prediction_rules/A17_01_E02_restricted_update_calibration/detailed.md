# Detailed: A17_01_E02 Restricted Update Smoke

[Summary](summary.md) · [Protocol](protocol.md) · [Full aligned Chinese ledger](detailed_cn.md)

## 0. Quick Recap

Repaired job pt-i3ianttt engineering PASS; independent gates 64/64 passed. Scientific verdict NOT_EVALUATED; researcher adoption Unknown. Original job failed at update0 from a baseline-state bug, not training or scientific evidence. One in-scope repair retry retained four arms/50 updates and reduced payload ceiling to1600s.

## 1. Terminology / Definitions

L updates only the original final Attention output projection; R8 freezes it and trains one shared rank8 factor pair. Negative after-minus-before CE is a raw local improvement in nats/answer. The80-row numerical panel is engineering readout, not complete-dev source or confirmatory qualification. Novelty is relative to task training.

## 2. Anchor Link And Decision Point

[A17 Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md). The researcher chooses the learner/window and numerical threshold. No scientific Focus closure or mechanism adoption follows from engineering completion.

## 3. Freeze, Conformance, And Deviations

Scope APPROVED_FOR_IMPLEMENTATION_AND_SMOKE. No Full/frequency/SAE/test. Before submission, finite dev probes were narrowed to80 stratified records; full800 capability unchanged. Amendment01 strengthened the native guard before pod runtime to exact full-vocabulary logits/CE. Amendment02 fixed precision baseline state isolation and added a CPU regression of actual probe(); original failed source and artifacts preserved. Raw failed probes are not mixed with repaired results. Original source/config/Protocol hashes and archived registered bodies are in each run's frozen_sources.json.

| Contract | Actual | Status / eligibility |
|---|---|---|
| Registered inputs | current local/remote strict receipts | ACCESSIBLE only |
| CPU contracts | eight tests incl. actual probe regression | PASS |
| First job | four H100 loads/native guards; update0 restore FAIL | zero trajectory updates; failed probes INELIGIBLE |
| One repair retry | same profile/four arms/50updates,1600s payload | PASS |
| Scientific source/numeric/adoption | no adopted thresholds | Unknown |

First durable payload upper64s plus retry1600s plus30s kill grace=1694s<original aggregate1800s; scheduling/container overhead is separate. Repair retry is not an independent scientific seed replicate. No data/model/LR/analysis-panel expansion.

## 4. Actual Setup

Parent model_qwen3_0p6b_base, native28-layer HF Qwen3. Train only model.layers.27.self_attn.o_proj: L2,097,152 original matrix weights or R8 shared24,576 factor parameters, rank8 alpha8 scale1, no bias/dropout. Freeze embedding/head/norm/MLP/other attention. FP32 weights/state, BF16 train, BF16/FP32 probes. Fixed downstream computation still responds; location is not format-only function.

Data data_a17_list_rules_v1: train4000/dev800; model test closed. Visible FIRST/LAST rule, prefix ends at 答案：, supervise only next full-vocabulary answer CE. Correct answer may legally occur in the list; never feed filled answer. Both novelty panels are reported rule-wise and record-weighted combined.

Four arms L/R8×AdamW1e-5/1e-4, seed17, betas(.9,.95),eps1e-8,decay0,clip1. Warmup40 valid answers then constant LR. Independent single-GPU micro5×accum4=20 answers/update,10/rule. Maximum50updates=1000 trajectory training answers,500/rule/arm. E01's different global batch is unmatched historical context.

Save/evaluate0/1/2/4/8/16/32/50. State contains declared trainables/AdamW/scheduler/Python+NumPy+CPU+CUDA RNG/counters/stateless cursor, with original Base required separately. At8, exit and restore in a new process; compare complete uninterrupted-next-update9 state/metric, then reset to8 and continue actual trajectory. Two extra20-answer reference updates are qualification compute outside the primary training exposure. Virtual-source/evaluation compute is also separate.

Precision boundary: BF16/FP32 recompute source gradients before evaluation, changing both update direction and reader. This is bounded engineering evidence, not fixed-perturbation reader-error qualification; scientific numeric qualification remains incomplete.

Probes at0/2/8/16:5 independent100-row sources/rule,20 words×5 each, selected before model outcomes; rule sources are not paired by list, explicit manifest flag false.80-dev panel selects one per rule×novelty×answer. PlainSGD eta1e-5/1e-4/1e-3, two precisions,60 contrasts/state. Restore weights/RNG before precision baselines and sources/scales/end; AdamW state untouched. Five no-op repeats/precision. No scientific CI/threshold adopted.

## 5. Metrics And Decision Rules

Engineering PASS needs exact scope/targets/native logits/frozen bytes/finite tags/saves/external resume/panels. Known violations FAIL; missing evidence INSUFFICIENT. Raw source own-panel decrease is not full-dev source efficacy or scientific eligibility. Any tiny nonzero sign remains unresolved until precision/meaning thresholds are adopted.

## 6. Evidence Lineage

| Readout | Raw / computation | Observation / eligibility | Limit |
|---|---|---|---|
| Scope/native/freeze | runtime / arm_completion | terminal audit | parameter position is not function |
| Capability | per-record JSON CE/argmax→weighted aggregate | table below | dev/single seed/fixed format |
| Finite four cells | probes JSON paired after-before | raw_source_window_readout |80-row panel, unresolved numeric thresholds |
| Saves/resume | checkpoint manifest/resume receipt | separately qualified | final50 restore NOT_CHECKED |
| Terminal | independent audit.py | PASS | engineering only |

## 7. Main Results

| Arm | Update | Order-new | Combination-new | Combined | Combined CE | Raw record |
|---|---:|---:|---:|---:|---:|---|
| l_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00000.json) |
| l_lr-5 | 50 | 78.00% | 77.25% | 77.62% | 0.89746392 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00050.json) |
| l_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00000.json) |
| l_lr-4 | 50 | 80.25% | 82.50% | 81.38% | 0.64701936 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00050.json) |
| r8_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00000.json) |
| r8_lr-5 | 50 | 73.50% | 73.00% | 73.25% | 1.02801167 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00050.json) |
| r8_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00000.json) |
| r8_lr-4 | 50 | 73.75% | 76.00% | 74.88% | 0.96421549 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00050.json) |


Every state and per-rule/panel CE/probability remains in source JSON. All dual-precision sources/scales and their contradictory/zero signs are retained, not selected for favorable outcomes. No scientific confirmation interval or SAE/expert analysis.

## 9. Stage Evidence And Failure Decomposition

The first zero-state guard detected that FP32 baseline retained a BF16 virtual update. The state-isolation regression exercises the actual probe() and now verifies identical baselines across precisions;8/8 CPU contracts passed. This is an engineering failure, not falsification of rank capacity, location prior or shared-learning mechanism. Retry outputs are independently audited.

## 10. Full Round Record

2026-10-10 Asia/Shanghai: question qualify restricted-update measurement; same parent/four arms and train4000; dev800/numeric80, test closed. First job failed with0 trained updates and4 saved initial states; one repaired job pt-i3ianttt currentPASS. Interpretation/adoption Unknown; no frequency/SAE round.

## 11. Interpretation

LoRA versus direct matrix changes parameterization/capacity/optimization; equal LR is not equal functional displacement. Effects are conditional on trainables/state/step. Initial zero-factor gradients are legitimate; all-correct accuracy can retain CE error; tiny signs need numeric qualification.

## 12. Claim Boundary

Can establish qualified implementation and bounded dev observations. Cannot claim LoRA superiority, format-only change, stable harm, functional decomposition, natural pretraining acquisition, expert necessity or frequency utility. Scientific NOT_EVALUATED.

## 13. Next Decision

Unknown: researcher selects/repairs learner/window and adopts precision/source rules. No further run is authorized by this result.

## 14. Artifact Manifest

[Retry freeze](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/frozen_sources.json) · [repair amendment](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/repair_amendment_02.json) · [failed actual saved assets](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_20261009T162413Z/registered_outputs.json) · [retry run](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z).

Actually saved retry asset IDs/access: [registered_outputs](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/registered_outputs.json).

Config SHA256 `81fce24c82c5effa4cc74013113cbece295cc8b8348ac7fabe9db1da5c748530`; runner `0ddc70175e069641bb811fbd99b471f17392e487630e06497cb5a3c59b6bcdba`; frozen Protocol `b27e76e749426ea3bf680a8490b608b2b1dbdd2f9698001f79f4a5ff93e042df`. Saved state SHA256 is in each manifest and recomputed by audit. Original Base GB hashes were not recomputed this round.

## 15. Links

[Runner](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/source/runner.py) · [config](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/configs/smoke_retry_01.json) · [independent audit](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/source/audit.py) · [raw source-window](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/raw_source_window_readout.json). Jobs pt-bw3s1pxw failed→pt-i3ianttt sole repair retry. Inspect existing jobs; do not resubmit.
