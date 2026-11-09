# Detailed: A17_04_E03 single-attention acquisition

Primary Anchor: [A17_04_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md). Protocol: [English](protocol.md), revision `a17_04_e03_single_attention_acquisition_v1`. Summary: [English](summary.md). [中文](detailed_cn.md).

Result state: `COMPLETE`; both acquisition arms are engineering-eligible within the bounded single-seed exposed-DEV diagnostic. The AdamW route qualifies; the tested SGD route does not. Researcher scientific judgment and parent question closure remain `Unknown`. Subsequent transfer and mechanism experiments are `NOT_RUN`.

## 0. Quick Recap

- Purpose: test whether the final attention layer's Q/K/V/O projection weights can acquire the original neutral-command rule.
- Model/logic: exactly four layer27 weights, 6,291,456 parameters, identical neutral data and seed29; compare inherited plain-SGD and AdamW packages. Fixed Main endpoint is1200 updates; each of four DEV cells must reach80%.
- Direct result: AdamW reaches800/800 combined DEV, all four cells200/200 and400/400 both-command list pairs; SGD reaches422/800, with the weakest cell93/200=46.5%.
- Eligibility: CPU/data checks, two real GPU paths, external-process Smoke replay, telemetry/frozen guards, independent analysis and actual asset access all pass.
- Verdict: `QUALIFIED_ROUTE` for `attn1_adam`; `NON_SUPPORT_WITHIN_BUDGET` for `attn1_sgd`. The latter is not an invalid run or proof that all SGD settings fail.
- Boundary: one seed and exposed DEV; no pure optimizer or capacity effect, Q/K/V-only result, mathematical minimality, transfer, SAE/expert mechanism or parent closure.
- Source: [Independent result record](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/results.json) and [analysis evidence manifest](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/analysis_manifest.json).

## 1. Terminology / Definitions

| Term | Concrete object / computation | Unit and purpose | Boundary |
| --- | --- | --- | --- |
| Neutral command | Visible甲 selects first;乙 selects last in mode one | One answer target per record | Requires learning command dependence, not merely candidate mass |
| Single-attention scope | Four layer27 projection weight tensors | 6,291,456 trainable parameters | Q/K normalization and all other parameters stay frozen |
| Tiny / Main | 64 fixed training targets / independent Base restart on 2,400 TRAIN targets | 160 / 1,200 updates | Tiny weights never initialize Main |
| Order-new / combination-new | Unseen ordering of a known unordered triple / unseen unordered triple | 400 DEV targets each | Already exposed DEV; not confirmation |
| Minimum DEV cell | Minimum accuracy over甲/乙 and both panels | Four cells of 200 targets; qualify at ≥80% | Combined mean alone cannot qualify |
| List-candidate mass | Sum of probabilities for three list words | Probability; access/selection CE accounting | Cannot by itself show command selection |

## 2. Anchor Link And Decision Point

E03 inherits A17_04_01's acquisition diagnosis. E02 provided projection-only failure and four-layer AdamW feasibility. This completed test establishes a smaller feasible trainable computation range: one final-layer Q/K/V/O scope under the tested AdamW package. Four trainable attention layers are therefore not necessary for acquisition on this data/setup. It does not identify an internal cause or modify the parent conditional-mapping transfer hypothesis. The user authorized this test only; execution stops after factual delivery.

## 3. Protocol Freeze, Conformance, And Deviations

Registered revision is `a17_04_e03_single_attention_acquisition_v1`. [Before-GPU freeze](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/freeze.json) bound36 files at2026-10-11 23:01:39 Asia/Shanghai (15:01:39UTC). [Final identity verification](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/postexecution_freeze_verification.json) passes all36 with zero mismatches. Frozen EN/CN Protocol, Anchor/Focus snapshots, source/config, data and Base identities are retained.

| Registered item | Expected | Actual | Status / eligibility |
| --- | --- | --- | --- |
| Scope | Two one-layer acquisition arms; no later experiment | Exactly `attn1_sgd` and `attn1_adam`; no TEST/new-mode input | Conforms |
| Data/split | Registered neutral TRAIN/tiny/panel/DEV | Selected hashes and quantities match; no new data | PASS |
| Trainable scope | Four layer27 Q/K/V/O weights,6,291,456 | Runtime inventory and first-step per-tensor changes agree; others frozen | PASS |
| Objective |20 answers/update,micro5×4,sum CE/20 | Actual records and native reader agree; all updates completed | PASS |
| Optimizers | Registered SGD/AdamW; global four-tensor clip1 | Actual gradient/update records, optimizer saves and states agree | PASS; actual displacement not matched |
| Budget/stages | Tiny160 then independent Base-reset Main1200 per arm | Each completed3,200+24,000 targets | PASS;54,400 formal targets total |
| Smoke bookkeeping | Per-arm/per-stage3 updates; original aggregate typo120 |12 completed updates=240 targets; replay80 separately | A01 arithmetic erratum; no code/config/exposure change |
| Saves | Tiny0/1/160;Main0/1/240/600/1200 |16 formal states and12 Smoke states saved | PASS; actual families registered |
| Resources |4H100 reserved node,2 independent workers | Actual node has4H100;GPU0/1 train,GPU2/3 unused | PASS; not DDP or replicas |
| Replay/telemetry/freeze | Fresh-process step1→2;7tags; unchanged inputs/source | Both arms/stages replay exactly; all tags/counters and36 identities pass | PASS; Full continuation itself `NOT_RUN` |
| Analysis | Four final cells, separate/combined panels, all milestones |34 prediction files/17,184 record readings independently checked | PASS; single-seed diagnostic only |

Amendment A01 in [Protocol](protocol.md) preserves the original frozen wording and corrects its aggregate Smoke arithmetic from120 to240. The specified three updates per arm/stage never changed. Smoke platform startup waited about5minutes before execution; cause is `Unknown` and is not attributed to resource shortage, code or a particular preparation step. No failed run, retry, arm exclusion, new seed, adaptive continuation or added training occurred. Platform terminal success, engineering validity and acquisition qualification remain separate evidence types.

## 4. Actual Setup

The exact parent is registered official Qwen3-0.6B Base at `/data/250010109/model_cache/Qwen3-0.6B-Base-official`, asset `model_qwen3_0p6b_base_official_a5`, using `tokenizer_qwen3_0p6b_base_official_a5`. Dataset asset is `data_a17_mapping_acquisition_diagnostic_v1`. The four neutral files retain original IDs, spaced prefixes, lists, labels and tokenization. No new data is constructed.

| Arm | Trained weights | Parameters | Fixed optimizer package |
| --- | --- | ---: | --- |
| `attn1_sgd` | Layer27 Q/K/V/O | 6,291,456 | Plain SGD lr .01; momentum0; decay0 |
| `attn1_adam` | Same four weights | 6,291,456 | AdamW lr1e-4; betas(.9,.999); eps1e-8; decay0 |

Shapes are Q[2048,1024], K[1024,1024], V[1024,1024], O[1024,2048]. All other weights, including Q/K normalization, MLPs, embeddings and LM head, are frozen. Native FP32 SDPA forward runs in evaluation mode with deterministic algorithms, dropout disabled and TF32 disabled. There is no fixed-upstream activation cache.

Seed29 selects identical paired list order for both arms within each stage. Each independent worker consumes 20 answer targets/update through four microbatches of five. Tiny has64 targets and160updates=3,200 exposures/arm. Main independently resets exact Base/optimizer/RNG and has2,400 targets and1,200updates=24,000 exposures/arm. Main saves0/1/240/600/1200; Tiny saves0/1/160. The two fitting arms total54,400 targets. Smoke consumed240 targets and external replay80 separately (A01 corrects the frozen aggregate arithmetic typo). No adaptive extension or early stopping occurs.

SGD computes one Euclidean norm over all four gradient tensors, applies one clipping coefficient, and updates every tensor. This replaces E02's single-tensor branch. AdamW also clips all four tensors globally. Both preserve sum-of-answer-CE divided by20; prefix and padding positions contribute no objective or primary target count. Actual displacement, preconditioning and optimization scale are not matched between optimizer packages.

Reuse actual native Base/AnswerLM, collation, paired order, checkpoint fields and telemetry; adapt scope, multi-tensor SGD and two-arm analyzer; reject historical endpoint re-audit, data variants, transfer and SAE/expert paths. Exact reuse decisions and inspected old hashes are in [reuse sources](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/configs/reuse_sources.json); implementation is described in [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/IMPLEMENTATION.md](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/IMPLEMENTATION.md).

| Identity | Path | SHA-256 |
| --- | --- | --- |
| Run config | [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json) | `bb48841e814e7b93725b165b8eadc4f8481763f01f1746401b570080445f6aa8` |
| Diagnostic data manifest | [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/manifest.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/manifest.json) | `05dfb9ac05ebf20dcf560b51d880acdb9472596b2a0a346aa8401d0dc9438a89` |
| Trainer | [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/diagnose.py](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/diagnose.py) | `1df552946bd8f70c517f3aba332f7d5722fdf75736ea364f7c8528ea845879a0` |
| Analyzer | [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/analyze.py](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/analyze.py) | `915a7a1df77232ac2e0185ee416c242aed806e6816ce7b8caec2a4ccbe7e5de1` |

These identities match the36-file before-GPU freeze and final zero-mismatch verification. All raw files remain execution-side; no state payload is copied into the canonical repository.

## 5. Metrics And Registered Decision Rules

Primary `Q_j` is the minimum full-vocabulary accuracy over four DEV cells, each200targets. Main update1200 is fixed primary endpoint. A valid arm qualifies when every cell is at least80%; valid nonqualification is non-support within this budget. Missing or invalid required evidence is insufficient. Report order-new, combination-new and combined800-target means separately, all four cells, the seen400-target panel and both-command paired success. The first saved qualifying checkpoint is descriptive; it does not select a new endpoint.

Secondary outputs are native answer CE, list-candidate mass, access CE, conditional-selection CE, correct-versus-opposite margin, full-vocabulary margin and paired command response. Exact decomposition is `CE = -log(list mass) - log[p(correct)/list mass]`. Positive mass or mean margin cannot replace primary accuracy. There is one training realization, not800 independent training replicas.

## 6. Evidence Lineage

| Claim / decision | Registered criterion | Raw artifact / computation | Observed value | Eligibility and limitation |
| --- | --- | --- | --- | --- |
| Real one-layer training paths are valid | Exact tensor scope/objective/freeze/TB | Worker scope/completion, stage telemetry and [smoke_gate.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_gate.json) | Both arms/stages PASS | Engineering, not acquisition |
| Recovery works for tested next step | Separate process loads step1 and matches step2 | `resume_worker_attn1_sgd.json`, `resume_worker_attn1_adam.json` | Both tiny/main paths exact | Smoke recovery only; Full continuation NOT_RUN |
| AdamW supplies a feasible route | Final four DEV cells≥80% | `full/attn1_adam/main/eval_dev_01200.json`; frozen analyzer recomputes | Four200/200; combined800/800; all400 pairs correct | QUALIFIED_ROUTE; one exposed-DEV seed |
| Registered SGD package is insufficient | Same final cell rule | `full/attn1_sgd/main/eval_dev_01200.json`; same analyzer |422/800;minimum93/200=46.5% | NON_SUPPORT_WITHIN_BUDGET; not all SGD settings |
| Tiny fitting and DEV differ | Independently reset Main; separate tiny reader | Tiny160 readers and Main baseline/order identities |Adam64/64 tiny but523/800 DEV | Fitting/generalization distinction; not a Main initialization effect |
| Candidate concentration alone is insufficient | Secondary accounting cannot rescue failed accuracy | Per-record output CE/mass/margins |SGD98.2288% list mass,52.75% accuracy | Output accounting; no parameter mechanism |
| Actual outputs are reusable | Required saves and selected strict access | [Peer audit record](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/independent_final_audit.json) | Second-agent CPU verification report | PASS; no separate audit script saved | Engineering/evidence verification; native records remain primary |
| [full_registration_receipt.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_registration_receipt.json), access snapshot |16 states/4 families+native analysis;5IDs PASS | Availability; not science approval |
| Independent result check is complete | Registered readers and state identities | [analysis/analysis_manifest.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/analysis_manifest.json) |34files,17,184readings,16 deserialized states;maxerror1.623109e-6 | PASS; records repeat across stages/checkpoints, not independent replicas |

## 7. Main Results

### Fixed Main endpoint

Sources: [analysis/results.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/results.json) and [analysis/trajectories.csv](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/trajectories.csv). Each arm is one seed. Full-vocabulary counts are shown explicitly. DEV contains400 records per panel and800 combined; paired metrics have400 lists.

| Arm | Seen TRAIN | Order-new DEV | Combination-new DEV | Combined DEV | Minimum cell | Both commands correct | Same answer across commands | First saved qualification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| attn1_sgd | 246/400 (61.5%) | 208/400 (52%) | 214/400 (53.5%) | 422/800 (52.75%) | 46.5% | 67/400 (16.75%) | 305/400 (76.25%) | Not reached / 未达标 |
| attn1_adam | 400/400 (100%) | 400/400 (100%) | 400/400 (100%) | 800/800 (100%) | 100% | 400/400 (100%) | 0/400 (0%) | 240 |

| Arm | 甲/order | 乙/order | 甲/combination | 乙/combination |
| --- | --- | --- | --- | --- |
| attn1_sgd | 112/200 (56%) | 96/200 (48%) | 121/200 (60.5%) | 93/200 (46.5%) |
| attn1_adam | 200/200 (100%) | 200/200 (100%) | 200/200 (100%) | 200/200 (100%) |

AdamW answers every DEV record correctly; SGD is correct on422 of the same800 records. The paired endpoint difference is378 additional correct records,47.25percentage points. This comparison changes optimizer and rate together; it is not an isolated optimizer-family causal estimate.

### Saved Main trajectory

| Arm | Update | Valid targets | Combined DEV | Minimum cell | CE, nat | Operational gate |
| --- | ---: | ---: | --- | --- | ---: | --- |
| attn1_sgd | 0 | 0 | 266/800 (33.25%) | 30.5% | 2.44652492 | BELOW_THRESHOLD |
| attn1_sgd | 1 | 20 | 299/800 (37.375%) | 33% | 2.33569756 | BELOW_THRESHOLD |
| attn1_sgd | 240 | 4800 | 358/800 (44.75%) | 41.5% | 1.13323379 | BELOW_THRESHOLD |
| attn1_sgd | 600 | 12000 | 357/800 (44.625%) | 42.5% | 1.07828572 | BELOW_THRESHOLD |
| attn1_sgd | 1200 | 24000 | 422/800 (52.75%) | 46.5% | 0.941982446 | BELOW_THRESHOLD |
| attn1_adam | 0 | 0 | 266/800 (33.25%) | 30.5% | 2.44652492 | BELOW_THRESHOLD |
| attn1_adam | 1 | 20 | 324/800 (40.5%) | 36.5% | 2.05406645 | BELOW_THRESHOLD |
| attn1_adam | 240 | 4800 | 795/800 (99.375%) | 98.5% | 0.0243161194 | PASS |
| attn1_adam | 600 | 12000 | 800/800 (100%) | 100% | 0.00114245424 | PASS |
| attn1_adam | 1200 | 24000 | 800/800 (100%) | 100% | 0.000691031676 | PASS |

AdamW first qualifies at saved update240:795/800=99.375%, weakest cell197/200=98.5%. It reaches100% by600 and remains there at1200. SGD does not qualify at any saved milestone. All arms nevertheless run the fixed1200budget; no outcome-based stopping occurred.

### Tiny fitting is separate

| Arm | Tiny seen64 | Both-command tiny pairs | DEV after tiny-only160 | DEV CE, nat |
| --- | --- | --- | --- | ---: |
| attn1_sgd | 38/64 (59.375%) | 6/32 (18.75%) | 370/800 (46.25%) | 1.12980054 |
| attn1_adam | 64/64 (100%) | 32/32 (100%) | 523/800 (65.375%) | 1.95976332 |

AdamW fits64/64 tiny targets but reaches only523/800=65.375% DEV in that trajectory. Main independently restarts Base and reaches800/800. A tiny fit is therefore not a sufficient generalization proxy, and its fitted weights did not carry into Main.

### Endpoint output accounting

| Arm | Answer CE, nat | List candidate mass | Access CE, nat | Conditional selection CE, nat | Command response a |
| --- | ---: | --- | ---: | ---: | ---: |
| attn1_sgd | 0.941982446 | 98.2288% | 0.0181517312 | 0.923830715 | 0.266854887 |
| attn1_adam | 0.000691031676 | 99.9994% | 5.93932e-06 | 0.000685092356 | 17.5246531 |

SGD places98.2288% of mass on the three list words but often does not switch its answer:305/400=76.25% of list pairs retain the same argmax. Only67/400=16.75% satisfy both commands. AdamW has all400 pairs correct and none with the same answer. These output measurements distinguish candidate concentration from command-controlled selection; they do not identify which internal parameter operation caused success.

### Actual exposure and update scale

Source: [analysis/training_exposure.csv](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/training_exposure.csv). Prefix-token counts are separately logged and do not replace valid-answer exposure.

| Arm | Stage | Updates | Valid answers | Prefix tokens | Mean step norm | Sum step norms | Last20 training CE |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| attn1_sgd | tiny | 160 | 3200 | 65100 | 0.0100000001 | 1.60000002 | 0.927465092 |
| attn1_sgd | main | 1200 | 24000 | 489600 | 0.0100000002 | 12.0000002 | 0.86540369 |
| attn1_adam | tiny | 160 | 3200 | 65100 | 0.0439364153 | 7.02982645 | 0.000172431538 |
| attn1_adam | main | 1200 | 24000 | 489600 | 0.0152092912 | 18.2511494 | 3.76110808e-05 |

Equal targets and tensor count do not imply equal parameter displacement. SGD Main path length is12.0000002; AdamW18.2511494. These whole-trajectory values include changing model states and cannot isolate preconditioning from step size.

### Engineering and assets

Smoke `pt-gwd1382k` and Full `pt-8fizcddl` both succeeded. Full started2026-10-11 23:09:55 and completed23:15:03 Asia/Shanghai. [Platform terminal receipt](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_platform_terminal_status.json) does not replace the tensor/reader checks. The independent analyzer deserializes all16 formal states, checking four FP32 projection shapes/finiteness, optimizer tensor-step/moment shape/finiteness, parent/config/data identities and target/update counters. It validates34 prediction files/17,184 record readings and loss identities; the maximum1.623109e-6nat is below the registered2e-5tolerance.

[Post-execution identity check](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/postexecution_freeze_verification.json) confirms all36 files unchanged. Actual Smoke12states and formal16states are registered as four checkpoint families per phase, plus each phase's native analysis family:10IDs total. Selected current strict output access passes. Strict access does not itself deserialize tensors; the independent analyzer supplies that separate validation. A second read-only peer agent independently loaded16 states on CPU and checked equal Base-reset weights, Adam state, saved order, seven tags,34files and36hashes; it also passed. The [peer audit record](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/independent_final_audit.json) is root's attributed report of that audit; no separate audit script was saved and this is not a new primary measurement source. The [final selected14-asset access](/data/250010109/Research_System/assets/checks/2026-10-11_a17_single_attention_delivery_access.json) passes. Exact external-process replay was performed only for Smoke. A Full restart/continuation test was `NOT_RUN`; ordinary complete training is not such a test.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | State | What is established / remains open |
| --- | --- | --- | --- |
| CPU helper | Actual multi-tensor helper/toy attention | PASS | Four updates/normalization/restoration checked; not Qwen science |
| Neutral data and inputs | Existing release; current strict inputs; frozen members | PASS | No changed data/presentation; tokenization remains inherited |
| Real GPU Smoke/replay | [smoke_gate.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_gate.json) | PASS | Both actual optimizers/stage resets/replay work |
| Tiny fitting |64-target readers at160 | Adam100%;SGD59.375% | Tiny success alone does not establish DEV generalization |
| Main acquisition | Fixed1200 all-cell DEV | Adam qualifies;SGD valid non-support | One feasible single-layer route; broad necessity claims unresolved |
| Independent analysis/saves |16states;34files;17,184readings | PASS | Tensor/optimizer/counter and readout validation complete |
| Final identity/platform |36file match; bothjobsSUCCEEDED | PASS | No source/config drift or retry; not scientific mechanism evidence |

A strong claim that this neutral task must train four attention layers is weakened by the one-layer AdamW success on identical data. No pure capacity limit, universal optimizer failure or internal-mechanism hypothesis is adjudicated. The SGD outcome cannot be explained by only a missing update to Q/K/V: actual four-tensor changes and saves were verified. Its optimization package may still be restrictive. Candidate concentration alone remains a failed proxy for acquisition.

## 9. Full Experiment Record

Round2026-10-11 (Asia/Shanghai):

1. Question: can one final-layer Q/K/V/O scope acquire the neutral mapping under either inherited optimization package?
2. Setup: exact registered Base, same four weights and all other weights frozen; same seed29 and finite budgets. Only the optimization package/rate differs between arms.
3. Training:64-target independent tiny pool for160steps, then independent Base restart on2,400TRAIN records for1200steps;54,400formal answer exposures across arms.
4. Measurement: fixed400-target seen panel and800-target DEV separated into order-new/combination-new; no TEST or untouched confirmation.
5. Result: both jobs and engineering guards pass. Adam finalDEV800/800, all fourcells200/200;SGD422/800, weakest93/200. All16formal states and12Smoke states registered; independent analysis/final36filecheck pass. A01 corrects only aggregate Smoke arithmetic to240, replay80 unchanged.
6. Insight/boundary/next: one-layer four-projection AdamW is a feasible acquired starting point for this case, smaller than the prior four-layer route. Optimizer/rate and one-seed exposed-DEV limits remain. Stop after this factual result; later transfer/mechanism/distribution work remainsNOT_RUN pending researcher authorization.

## 10. Interpretation

Observed: one-layer AdamW meets the full-vocabulary cellwise criterion and switches correctly on every paired list. Derived: the tested scope is one quarter of the25,165,824-parameter four-layer scope and three times the2,097,152-parameter O-only scope. AI interpretation: four-layer trainability is not necessary for acquisition on these data, and no data change was needed for the successful one-layer route. This does not identify capacity as the cause: trainable computational locations and optimizer dynamics vary in the broader historical comparison. The two new arms also differ in learning-rate scale/preconditioning/trajectory; their result cannot assign success to AdamW alone or conclude SGD cannot work.

## 11. Claim Boundary

Can claim: the bounded two-arm test is complete; one final-layer Q/K/V/O route using the tested AdamW package acquired the neutral rules on the fixed seen/DEV panels; the tested SGD package did not qualify within1200steps; all prescribed outputs and guards are available.

Cannot claim: Q/K/V-only sufficiency, training every attention-module parameter, mathematically minimum parameter scope, pure parameter-count or optimizer-family causation, single-layer universal sufficiency, allSGD failure, statistical/untouched confirmation, new-mode transfer, interference, benefit from separated experts or SAE mechanism. The parent question remains scientifically open.

## 12. Next Decision

The authorized small test and factual delivery are complete. Stop execution here. Researcher scientific judgment remains `Unknown`; consistent/reversed transfer, parameter mechanisms, routing/separate-training benefits and extra arms/seeds are `NOT_RUN` and require subsequent authorization. A qualified checkpoint is an available input, not permission to launch a later experiment.

## 13. Artifact Manifest

| Artifact | Purpose / producer | Identity and completeness | Claim eligibility |
| --- | --- | --- | --- |
| [Protocol](protocol.md) / frozen snapshots | Registered contract | v1 + appendedA01; original body preserved | Authorized scope; no result-derived design rewrite |
| [freeze.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/freeze.json) / [postexecution_freeze_verification.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/postexecution_freeze_verification.json) | Root before/after36file binding | All36match,zero mismatches | Engineering provenance |
| [config.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json) / implementation reuse manifest | Fixed settings and inspected source | ExactSHA in§4,unchanged | Reproducible execution |
| [execution_certificate.md](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/execution_certificate.md) | Profile/image/command/counters | Actual4H100reserved,two independent workers | Execution certificate |
| [smoke_gate.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_gate.json) / resume receipts | Real smoke/next-step recovery | Botharms/twostagesPASS | Engineering only; no accuracy gate |
| [smoke_terminal_status.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_terminal_status.json) | ACP completion | `pt-gwd1382k`,SUCCEEDED | Platform, not learning |
| [full_platform_terminal_status.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_platform_terminal_status.json) | ACP completion | `pt-8fizcddl`,SUCCEEDED | Platform, not learning |
| [full_worker_qualification.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_worker_qualification.json) | Actual worker completion | Both exit0,fixed160/1200 | Engineering completion |
| [analysis/results.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/results.json) / trajectories / training exposure | Frozen analyzer over actual outputs | PASS;34files,17,184readings,16deserialized states | Bounded DEV measurement |
| [analysis/analysis_manifest.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/analysis_manifest.json) | Per-file member hashes/readout lineage | Prediction/state members listed | Exact artifact provenance |
| [smoke_registration_receipt.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_registration_receipt.json) | Actual12states/4families + native family |5IDs,selected strict accessPASS | Availability, not science |
| [full_registration_receipt.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_registration_receipt.json) | Actual16states/4families + native family |5IDs,selected strict accessPASS | Availability, not science |

Checkpoint IDs follow `adapter_a17_04_single_attention_20261011t145214z_{smoke|full}_{attn1_sgd|attn1_adam}_{tiny|main}`. Native analysis IDs follow `analysis_a17_04_single_attention_20261011t145214z_{smoke|full}`. Each receipt links its current strict access snapshot. Together these are28saved state members, eight checkpoint families and two analysis families; no standalone Base is resaved. All adapters require the exact registered Base.

## 14. Links And Reproduction

- Canonical: [Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md), [Protocol](protocol.md), [Summary](summary.md).
- Execution: [package](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition), [run](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z), [source](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source), [configuration](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json); [logs](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/logs), [checkpoint families](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full).
- Worker interface: `python source/diagnose.py --config RUN/config.json --run RUN --arm attn1_sgd --phase full`; this is reproduction documentation, not permission to duplicate completed jobs.
- Frozen analysis: `python source/analyze.py --config RUN/config.json --run RUN` under the inspected runtime; actual results and analyzer hashes are in the manifest.
- Jobs: Smoke `pt-gwd1382k`; Full `pt-8fizcddl`. BothSUCCEEDED, neither retried. Subsequent transfer/mechanism/distribution testsNOT_RUN.
