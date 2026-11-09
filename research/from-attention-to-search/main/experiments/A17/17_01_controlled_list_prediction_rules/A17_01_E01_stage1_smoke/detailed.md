# Detailed: A17_01_E01 Stage-1 Smoke

[Summary](summary.md) · [中文](detailed_cn.md) · [frozen Protocol](protocol.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md)

## 0. Quick Recap

Paired list data and the authorized short-training chain completed. Job `pt-2m4rvpt4` succeeded at 2026-10-09T15:34:48Z; independent engineering audit passed 31/31 gates. Scientific verdict `NOT_EVALUATED`; researcher interpretation `Unknown`. This record reports every planned stage, including limitations and skipped branches.

## 1. Definitions

The prefix contains a visible FIRST/LAST rule and an ordered three-word list; it ends at 答案：. Predict the next answer token from the full vocabulary. The correct word may legally be in the list; a completed answer field is never fed. Order-new holds out exact order within task-seen unordered content; combination-new holds out unordered content. Novelty is relative to constructed task training, not original pretraining. Loss is nats/answer; negative post-update minus pre-update loss means a measured improvement. Combined means record-weighted average. Answers, paired rules and permutations are not independent scientific replications; future uncertainty requires the declared content-group structure.

## 2. Anchor Decision

The active decision is acceptance/repair of engineering admission. It is distinct from a bounded scientific help/harm verdict, long-term training benefit, function decomposition or expert allocation. The researcher's scientific judgment remains Unknown; successful execution cannot change it.

## 3. Freeze, Conformance And Deviations

[Frozen sources](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/frozen_sources.json) identify source/config/Protocol, data manifest, inspected native loaders and actual HF implementation. Remote entry rechecked these digests before loading. No source/config/Protocol amendment, retry, exclusion, failed job, fallback or Full occurred. The lexicographic source selection below was the frozen implementation, not a later replacement. Documentation added after completion does not alter the frozen scientific Protocol.

| Contract | Actual evidence | State | Boundary |
|---|---|---|---|
| 5,600 rows, oracle, actual tokenizer continuation, both panels | data qualification + manifest | PASS | controlled finite carrier |
| four H100 ranks, one-answer loss, exact counters | runtime_rank_0..3 + metrics + local loss tests | PASS | no architecture causality |
| 16/32 saves, new process restoring16 | complete checkpoint manifests + four resume receipts/carrier | PASS | update32 restore NOT_CHECKED |
| telemetry with both valid-answer and update axes | two TensorBoard segments/carrier and auditor | PASS | answers are not all prefix tokens |
| initial/final separate and combined capability | per-model capability JSON | PASS | dev, not untouched confirmation |
| no-op/restoration and all finite effect cells | cross_rule_updates JSON | PASS | source guard not a gate for scientific support |

## 4. Setup And Data

Words: 红 蓝 绿 黄 黑 白 紫 灰 金 银 猫 狗 鸟 鱼 牛 马 羊 虎 龙 花. Qwen3 Base tokenizer is used without chat template or special tokens. Every actual prefix-plus-answer boundary qualifies as prefix IDs plus exactly one target ID. Input context words can be split into more tokens; only the answer continuation is single-token.

Twenty content cyclic orbits ×20 word-index shifts ×5 orderings yield2,000 train base lists. The remaining sixth order, divided over disjoint halves of train orbits, yields200 order-new dev and200 test lists. Five unused content orbits ×20 shifts ×2 orders per new-combination split yield200 dev and200 test lists. Pair expansion gives4,000/800/800 records. Train word/position counts are100/rule; every dev/test panel count10/rule. Ordered lists across splits do not overlap; order-new unordered content deliberately overlaps training; new-combination sets are disjoint across train/dev/test. This structured balancing carrier is not iid natural text.

Initial inputs: `model_dense_33b`, `model_qwen3_0p6b_base`, `model_s7_fresh_lambda0p1_33b`; dataset `data_a17_list_rules_v1`. Strict local and remote access snapshots passed before use. Dense exact33B uses native8 layers, width1024, FFN3072 and281,431,040 LM parameters. Qwen Base uses28 layers, width1024, FFN3072 and596,049,920 parameters. S7-fresh exact33B has342,902,064 parameters including its sidecar. Verified S7 native LM forward is preserved; objectives and pretraining histories differ. S7 is read-only; no SAE features or representations were collected.

Dense/Qwen independently adapted all LM parameters, in sequential four-rank runs. FP32 parameters/state, BF16 autocast, new AdamW LR1e-4, betas(.9,.95), epsilon1e-8, weight_decay0, gradientclip1. New task optimizer intentionally replaces old pretraining optimizer; this is not exact pretraining continuation. Micro8/rank ×4 ranks ×accum2 =64 answer targets/update, balanced rules, warmup256 targets. Seed17, data seed1009. Each carrier performs32updates/2,048answers, saves at16/1,024 and32/2,048, exits at16 and resumes in a new4-rank process. Test model reader is forbidden.

Hardware: one4×H10080GB reserved node, profile h100-4-reserved, spec n6ls.iu.i40.4, image shphd-lite-0911, torch2.3/CUDA12.4 with existing mounted Python3.10 transformers4.53.3 layer. A process-local Python protobuf implementation repairs the pre-existing TensorBoard import compatibility; no package installation or image change occurred.

## 5. Metrics And Frozen Analysis

Capability is full-vocabulary top1 and mean answer CE; each rule/panel n200, panel ALL n400, combined/rule n400, combined ALL n800. Models opened only train/dev; generated test underwent structural/data qualification, not model evaluation. There is no scientific CI, seed replication or test-driven selection.

After update32, separately use32 training examples per source rule and plainSGD eta1e-5 on all LM parameters from identical weights. Source gradient is batch-averaged; no AdamW state is changed. Recipients are independent full dev rule/panel subsets. Restore weights and RNG between sources, then compare a no-op restored reference. The descriptive source guard is strictly negative combined same-rule dev delta; it has no uncertainty threshold and is not a scientific source-efficacy certificate.

Engineering PASS is the conjunction of31 registered gates. It does not require positive scientific signal, non-saturation or representative probe sources.

## 6. Evidence Lineage

| Statement | Raw source | Computation | Observation / eligibility |
|---|---|---|---|
| data is structurally admitted | [qualification](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/data/list_rules_v1/qualification.json), [manifest](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/data/list_rules_v1/manifest.json) | independent oracle/token-boundary/pair/balance/novelty checks | PASS; declared carrier only |
| CPU implementation checks | [test receipt](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/local_test_receipt.json) |10 meaningful invalid-data/loss/aggregation/reader/restore tests |10 PASS; not GPU evidence |
| job completed | [platform](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/completed_platform_status.json), [pod log](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/acp_receipts/pod/a17-list-rules-smoke-20261009t152323z-20261009T152934Z.log) | ACP receipt + worker output | SUCCEEDED with actual GPU computation |
| capability observations | per-model initial/final_capability.json linked in artifact manifest | globally aggregate answer loss/correct counts | dev values below; not universal mastery |
| training and resume | per-model metrics, TensorBoard, checkpoint manifests, resume_rank receipts | counters, source/hash checks, saved-size checks, sampled weight identity |32updates each;16resume qualified; uninterrupted parity NOT_CHECKED |
| finite effects | [Dense effects](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/dense/cross_rule_updates.json), [Qwen effects](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/qwen_base/cross_rule_updates.json) | real SGD and recipient reevaluation from common state | descriptive four cells and no-op below |
| engineering terminal status | [terminal verification](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/terminal_verification.json) | source/audit.py independently reads files/telemetry |31/31 PASS; scientific NOT_EVALUATED |

## 7. Results

### 7.1 Capability

Cells are accuracy / CE (nats/answer). Initial=before task adaptation; final=after32 task updates. S7 has no final measurement because training was excluded.

| Model | State | Order-new | Combination-new | Combined |
|---|---|---|---|---|
| S7-fresh exact33B | initial | 0.00% / 10.577504 | 0.00% / 10.579289 | 0.00% / 10.578396 |
| Dense exact33B | initial | 0.00% / 10.902297 | 0.00% / 10.91214 | 0.00% / 10.907218 |
| Dense exact33B | final | 100.00% / 0.02564373 | 100.00% / 0.027313172 | 100.00% / 0.026478451 |
| Qwen3-0.6B-Base | initial | 73.75% / 1.0347961 | 72.25% / 1.0303237 | 73.00% / 1.0325599 |
| Qwen3-0.6B-Base | final | 98.75% / 0.053326474 | 98.75% / 0.11264566 | 98.75% / 0.082986065 |

Rule-specific values are retained, rather than replaced by panel totals:

| Model | State | Rule | Order-new | Combination-new | Combined |
|---|---|---|---|---|---|
| S7-fresh exact33B | initial | FIRST | 0.00% / 10.325733 | 0.00% / 10.330257 | 0.00% / 10.327995 |
| S7-fresh exact33B | initial | LAST | 0.00% / 10.829275 | 0.00% / 10.82832 | 0.00% / 10.828797 |
| Dense exact33B | initial | FIRST | 0.00% / 10.474888 | 0.00% / 10.468495 | 0.00% / 10.471691 |
| Dense exact33B | initial | LAST | 0.00% / 11.329706 | 0.00% / 11.355785 | 0.00% / 11.342745 |
| Dense exact33B | final | FIRST | 100.00% / 0.017565764 | 100.00% / 0.017197206 | 100.00% / 0.017381485 |
| Dense exact33B | final | LAST | 100.00% / 0.033721696 | 100.00% / 0.037429139 | 100.00% / 0.035575418 |
| Qwen3-0.6B-Base | initial | FIRST | 69.50% / 1.1395787 | 70.00% / 1.1232676 | 69.75% / 1.1314231 |
| Qwen3-0.6B-Base | initial | LAST | 78.00% / 0.93001355 | 74.50% / 0.9373798 | 76.25% / 0.93369667 |
| Qwen3-0.6B-Base | final | FIRST | 100.00% / 3.1035646e-06 | 100.00% / 6.5285802e-06 | 100.00% / 4.8160724e-06 |
| Qwen3-0.6B-Base | final | LAST | 97.50% / 0.10664984 | 97.50% / 0.22528478 | 97.50% / 0.16596731 |

Qwen already performs this carrier well but has216/800 initial errors. Final Qwen has10/800 errors, all LAST; FIRST dev accuracy is100% and mean CE≈4.82e-6. Dense final has0/800 observed errors and CE≈.02648. Dense/S7 initial zero means their unrestricted top1 choices did not match the correct answer in this format; it does not establish no useful internal ability. Saturation is a measurement warning, not a hypothesis verdict. No unseen-template/new-vocabulary or natural-language generalization result is available.

### 7.2 Four-cell finite updates

Units are nats/answer, after minus before. Every cell starts at the same update32 base within its model. Sign describes this particular finite probe; it is not a stable rule incompatibility verdict.

| Model | Source → recipient | Order-new | Combination-new | Combined |
|---|---|---|---|---|
| Dense exact33B | FIRST → FIRST | -0.0002076101415 | +5.335594105e-05 | -7.712710023e-05 |
| Dense exact33B | FIRST → LAST | +2.06774519e-05 | -2.567980679e-05 | -2.501177441e-06 |
| Dense exact33B | LAST → FIRST | -0.0001506422108 | +4.551036545e-06 | -7.304558712e-05 |
| Dense exact33B | LAST → LAST | -0.0001632075394 | +0.0001860331221 | +1.141279135e-05 |
| Qwen3-0.6B-Base | FIRST → FIRST | +0 | +0 | +0 |
| Qwen3-0.6B-Base | FIRST → LAST | +0 | +0 | +0 |
| Qwen3-0.6B-Base | LAST → FIRST | +6.496430363e-08 | -3.099544983e-08 | +1.69844269e-08 |
| Qwen3-0.6B-Base | LAST → LAST | -0.01443916529 | -0.02247138387 | -0.01845527458 |

| Model | Source | Combined self-rule loss decreased |
|---|---|---|
| Dense exact33B | FIRST | True |
| Dense exact33B | LAST | False |
| Qwen3-0.6B-Base | FIRST | False |
| Qwen3-0.6B-Base | LAST | True |

| Model | FIRST gradient norm | LAST gradient norm | Gradient dot | No-op loss drift |
|---|---|---|---|---|
| Dense exact33B | 0.6643844322 | 4.19089028 | +0.02294991768 | 0.0 |
| Qwen3-0.6B-Base | 0.0002172169021 | 66.98821593 | -5.305072301e-05 | 0.0 |

Source FIRST has32/32 targets 红, while LAST covers15 target words. This follows lexicographic record-ID selection in frozen runner lines176–177, verified from the train records. Full training marginals are balanced; these selected probe batches are not. The batch cannot identify a representative rule-average effect. No alternate batches were substituted post hoc.

Dense FIRST combined LAST delta is−2.50118e-6, but order-new is positive and combination-new negative. Dense LAST combined self-rule loss increases; its source guard fails. Qwen FIRST yields zero deltas at current precision; its guard fails. Qwen LAST improves LAST by−.0184553 combined, while its FIRST change≈+1.70e-8 is unresolved for scientific interpretation and panel signs differ. The mean gradient dot is a diagnostic from the source batches, not a proof of conditional-rule function, causality or useful expert separation.

### 7.3 Training, Telemetry And Saves

Both carriers completed exact32steps/2,048 valid answers, with no nonfinite/skip. Globally answer-weighted train LM and total losses are identical because no auxiliary loss is active. TensorBoard contains required answer/update axes and optimizer/throughput diagnostics in separate initial/resume segments; audit confirms32points and agreement with metrics. Four per-rank receipts confirm restore from16 of optimizer/scheduler/RNG/counters plus sampled weights and stateless next-update data coordinates. Both16/32 checkpoints contain state.pt plus four per-rank RNG files. Update32 reload and uninterrupted trajectory equivalence were not tested. Complete file existence/sizes are verified; large checkpoint bytes were not rehashed.

## 8. Failure Decomposition And Stage Coverage

All data/local/remote engineering stages ran and passed. No worker failure artifact, retry or fallback occurred. Earlier STARTING/Pending/RUNNING snapshots record startup history and are superseded for current state by completed_platform_status.json; they are preserved. The package compatibility setting preceded submission.

Scientific limitations are distinct from engineering failure: final-state saturation; lexicographic source coverage; source guard failures; one seed and one batch/source; BF16 readout with no calibrated resolution band; no CI/replication. No model opened confirmation test. S7 training, frequency experiment, representation/SAE analysis, expert allocation and Full were NOT RUN, excluded by scope rather than failed tests.

## 9. Completed Round Record

1. Question/hypothesis: qualify the paired conditional-rule carrier and bounded pipeline; empirical help/harm remains open.
2. Setup/controls: two independent adaptation carriers, third initial-only, visible rule, shared list generator, balanced training, four-cell/no-op/restoration controls.
3. Data:4,000 training rows, equal rule exposures, one supervised answer each.
4. Confirmation split:800dev evaluated in two panels,800test generated/qualified but model-sealed.
5. Result:platformSUCCEEDED;31/31engineeringPASS; capability/effect observations above; scientificNOT_EVALUATED.
6. Insight/boundary/next decision: usable carrier and execution chain; fast saturation and selected-source coverage limit science. Researcher may accept/repair engineering, then choose a separate prospective scientific contract.

## 10. Interpretation And Claim Boundary

Observation: Qwen has incomplete pre-existing task performance; Dense learns this carrier quickly. Interpretation under review: this carrier may reach saturation too rapidly at32updates for an informative update probe. Competing explanations for initial zero include task-format conditioning and answer prior, not only absent rule knowledge.

Not established: stable shared help/harm, distinct reusable/unique internal functions, acquisition from random initialization, a clean architecture effect, pretraining novelty, long-term benefit or necessity of experts. Even a measured net local sign would need an explicit bridge to long-term decisions. Scientific and researcher judgment remain unchanged.

The research-reasoning-auditor checks were applied to prevent observation→mastery, finite probe→stable interference, source-batch gradient→rule function, and engineering success→scientific support leaps. Missing scientific qualification is an untested link; existing data/implementation evidence is present and must not be described as absent.

## 11. Next Decision

One researcher-owned decision: accept or repair engineering admission. AI suggestion for a future scientific Protocol: select earlier unsaturated operating states prospectively; balance independent source batches; calibrate precision/no-op resolution and finite step sizes; freeze uncertainty/replication and untouched test use. This is a suggestion, not scientific adoption or Full authorization. No further training is submitted in this record.

## 12. Artifact Manifest And Asset Lifecycle

[Execution artifact manifest](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/artifact_manifest.json) records identities/paths/small-file digests and checkpoint sizes. Input access: [scoped snapshot](/data/250010109/Research_System/assets/checks/2026-10-09_a17_inputs.json), local/remote run snapshots. Data: `data_a17_list_rules_v1`.

Actual output assets:

- `model_a17_list_rules_dense_smoke_20261009t152323z_u32`.
- `model_a17_list_rules_qwen_base_smoke_20261009t152323z_u32`.

Each selected asset is final32; its registry entry explicitly enumerates actual16/32 files and loader, optimizer/RNG, parent input, code/config/data/Protocol/job provenance. Strict current output access passed at2026-10-09T15:38:30.055714+00:00: [snapshot](/data/250010109/Research_System/assets/checks/2026-10-09_a17_smoke_outputs.json). Large payload SHA256 remains NOT_COMPUTED;16resume qualified,32restore NOT_CHECKED. These are Smoke states, not scientific confirmation checkpoints.

## 13. Navigation And Reuse

[Execution README](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/README.md), [runner](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/source/runner.py), [generator](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/source/data.py), [auditor](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/source/audit.py), [config](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/configs/smoke.json), [certificate](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/execution_certificate.md). Reused native Dense/S7 LM implementations and tokenizer fingerprint helper; adapted approved DDP/telemetry/save-resume patterns. New code implements list construction, answer-only wrapper, novelty panels and real four-cell probe. Existing pretraining loops were not reused as task training. Code/raw outputs/checkpoints stay in execution; canonical science stays here.
