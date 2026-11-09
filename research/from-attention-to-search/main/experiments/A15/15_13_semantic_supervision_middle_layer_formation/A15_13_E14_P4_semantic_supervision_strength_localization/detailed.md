# Detailed: A15_13_E14_P4 Semantic-Supervision-Strength Localization

Primary Anchor: [A15_13 semantic supervision middle-layer formation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md)

Frozen Protocol and registered revision: [protocol.md](protocol.md), `20260907-P4-v1`; the successful worker used the pre-start snapshot hash `0c9b542fe20fe2e5689935990981f7edf44c643dae131aeba32a221d29f4bd9b`.

Summary: [summary.md](summary.md)

Result eligibility: `COMPLETE`; formal weak arms are eligible for the bounded development claim below. Two earlier jobs failed at the smoke import boundary and are explicitly ineligible.

## 0. Quick Recap

Purpose: localize whether the P3 seed reversal is caused by an overly strong 0.5/0.5 semantic auxiliary objective.

Hypothesis: a 0.25/0.25 auxiliary objective should beat current `H-sem` in both seeds for harm reduction; a stronger method-value claim additionally requires it to beat `H-task` in both seeds.

Experiment logic: reuse P3 controls and exact train/development artifacts; train only `H-sem-weak` at seeds 17 and 29 from update zero; compare update-512 development answer NLL with source-stratified paired bootstrap intervals.

Direct result: the weak arm did not beat current `H-sem` in either seed at update 512, and it beat `H-task` only in seed 17.

Eligibility: identity, tests, smoke, formal guards, data/teacher/control hashes, checkpoints, analysis, and artifact manifest all passed for the successful job. Resource naming is bounded to the actual `N6LS-80G-SXM5` worker label.

Verdict: `HALF_WEIGHT_REPAIR_NOT_REPLICATED`.

Claim boundary: exact 0.25/0.25 did not replicate the proposed repair or a net semantic benefit in this two-seed, development-only realization; no general method claim follows.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Development answer NLL | Average negative log likelihood on answer tokens held for development | `analysis/development_nll.csv` over 8,481 records and 572,552 answer tokens | \(\sum_i x_i / \sum_i n_i\) nat/token | Primary operating-point comparison | Not held-out test or free-generation quality |
| Harm reduction effect | Current semantic supervision NLL minus weak-arm NLL | `H-sem − H-sem-weak` per seed at update 512 | Positive favors weak | Tests whether lowering the weight repairs the current arm | Does not establish semantic value over task-only |
| Net semantic-benefit effect | Task-only NLL minus weak-arm NLL | `H-task − H-sem-weak` per seed at update 512 | Positive favors weak | Tests semantic benefit after harm comparison | Cannot rescue a failed harm conjunction |
| Replication unit | Independently trained model seed | Seeds 17 and 29 | No seed pooling in verdict | Prevents one seed from masking reversal | Two seeds are not a population estimate |
| Paired bootstrap interval | Source-stratified resampling interval over complete records | 2,000 draws, NumPy seed `20260907` | 2.5th/97.5th percentiles | Quantifies uncertainty for each contrast | Not a formal population-level generalization |

## 2. Anchor Link And Decision Point

The parent Anchor asks whether semantic supervision organizes an effective middle representation and distinguishes semantic supervision from generic adaptation. This P4 subdecision tests only whether the registered P3 reversal can be localized to the exact 0.5/0.5 auxiliary weight. It does not reopen P3 or adjudicate expert function, representation accessibility, or test performance.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Scientific body | P4-v1, 0.25/0.25 only | Snapshot hash `0c9b542f...f4bd9b` used by worker | PASS | `protocol_snapshot.md`, `receipts/identity.json` | None |
| Data | P3 processed tensor, 39,576/8,481/8,481 split; train plus existing development only | Hash `b2e1b4c5...ac13`; each output has 8,481 records and 572,552 answer tokens | PASS | identity receipt, `analysis/development_nll.csv` | None |
| Teacher | P3 train-only assignments | Hash `8a04a8cc...0929`, copied unchanged | PASS | identity receipt, artifact manifest | None |
| Architecture | Frozen Qwen3-0.6B, block-14 H hierarchy, load-off | Same P3 worker; 393,216 expert + 11,275 router = 404,491 trainable parameters | PASS | formal eligibility guards | None |
| Objective | \(L=L_{answer}+0.25L_{parent}+0.25L_{child\mid teacher\ parent}\) | `H-sem-weak`, `aux_weight=0.25`, seeds 17/29 | PASS | formal receipt and train logs | None |
| Seeds and checkpoints | 17, 29; 0/128/256/384/512 plus final/recovery | Both arms complete with all checkpoints and guards | PASS | formal receipt and manifest | None |
| Smoke | Two updates, seed 17, finite/changing banks, discard weights | PASS; smoke weights marked discarded | PASS | `receipts/smoke.json` | None |
| Primary analysis | Four seed-separated paired intervals; 2,000 draws; no pooling | Four update-512 contrasts emitted with registered seed and bootstrap | PASS | `analysis/weight_localization_effects.csv` | None |
| Resource | One serial H100 80GB, reserved, retry zero | ACP one node, one `n6ls.iu.i40.1` GPU; platform reports `N6LS-80G-SXM5`, reserved, retry zero | BOUNDED | job `pt-ahj3yiaw` description | Claim is bounded to actual worker label; no scientific variables changed |
| Failed attempts | No failed arm may enter analysis | `pt-yajflax0` and `pt-n4ilzz1d` failed at smoke import and were not reused | PASS | append-only amendment P4-A1 and failure receipts | Excluded from all comparisons |

Frozen Protocol revision: `20260907-P4-v1` before execution; amendment P4-A1 records only runtime propagation repairs.

Execution scope approved: implementation, disposable smoke, two weak-arm formal runs, frozen analysis, and result recording. No extra weight, seed, layer, teacher, H-hard/H-oracle, commit, push, sync, or publication was performed.

Amendments: P4-A1 only; scientific body and decision rule unchanged.

Retries and exclusions: successful job retry count 0; the two earlier failed jobs are excluded and retained as failure evidence.

Missing conditions or artifacts: none for the registered P4 matrix. P4 test was intentionally not used; P3 controls were reused as registered.

Post-hoc analyses: none entered the verdict. The figure and trajectory rows are generated by the registered analysis script.

## 4. Actual Setup

Research question: does reducing semantic auxiliary supervision from 0.5/0.5 to 0.25/0.25 repair P3's opposite seed directions, and if so does it still beat task-only training?

Data construction and provenance: exact P3 processed tensor `/data/250010109/datasets/a15_e14_p3_clean/processed.pt`, 39,576 train, 8,481 development, 8,481 test records after global ID and normalized content deduplication. P4 did not open or score the test split.

Train / development / confirmation split: training rows fit the added modules; development rows provide the primary NLL; test remains untouched for P4.

Learning task and permitted supervision: next reference-answer token prediction; weak arm receives train-only parent and conditional child pseudo-labels, while routers use the online block-14 input. Teacher state, future tokens, source IDs, and test fields are forbidden online.

Model / architecture / algorithm: frozen Qwen3-0.6B-Base with the P3 block-14 online hierarchical residual system; load balancing off. Router input width 1,024; expert down-projection input width 3,072; rank-8 shared/parent/leaf residuals.

Training objective and constraints: \(L=L_{answer}+0.25L_{parent}+0.25L_{child\mid teacher\ parent}\). P3 `H-sem` and `H-task` controls use 0.5/0.5 and 0/0 respectively. No new condition was trained.

Optimizer or update rule: P3 AdamW groups, learning rates `2e-4` experts and `5e-4` routers, betas `(0.9,0.999)`, epsilon `1e-8`, weight decay `0.01`, clip `1.0`, 26-update warmup, cosine decay, microbatch 8, accumulation 16, effective batch 128, 512 updates.

Training steps / tokens / batch size: 512 optimizer updates per formal arm; development output contains 572,552 answer tokens per condition.

Checkpoints: update 0, 128, 256, 384, 512, final and recovery state.

Seeds: 17 and 29.

Conditions and plain-language labels: `H-sem-weak` is the only newly trained weak semantic arm; `H-sem` is current semantic supervision; `H-task` is matched task-only. Existing controls are reused only after exact same-seed initial-state checks.

Changed variables: semantic auxiliary coefficient only, from 0.5/0.5 to 0.25/0.25.

Held fixed: data, teacher, architecture, initialization per seed, order, optimizer, budget, load policy, evaluator, checkpoint rule, and primary metric.

Code / config / data identities: code hashes are recorded in `receipts/identity.json`; processed data hash is `b2e1b4c5...ac13`; teacher hash is `8a04a8cc...0929`; frozen Protocol snapshot hash is above.

Script and result paths: runner `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/p4_weight_localization.py`; successful result root `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/p4-weight-20260907T024100Z`.

Known setup limitations: two seeds and development-only evidence; actual platform resource label is recorded as bounded; no P4 test or free-generation confirmation.

## 5. Metrics And Registered Decision Rules

For each seed, the worker computes per-record answer loss sums and token counts, then \(L_m=\sum_i x_i^m/\sum_i n_i\). Paired resampling is within each of eight sources, preserving source counts, with 2,000 percentile draws and NumPy seed `20260907`. Positive means lower weak-arm NLL.

The harm conjunction requires both `H-sem − H-sem-weak` lower endpoints to exceed zero. The benefit conjunction requires both `H-task − H-sem-weak` lower endpoints to exceed zero. A failed harm conjunction cannot be rescued by the benefit conjunction. The registered map yields `HALF_WEIGHT_REPAIR_NOT_REPLICATED` when a harm interval has upper endpoint at most zero; the actual mixed/negative pattern is assigned that typed verdict by the worker.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Formal weak arm completed | Both seeds, 512 updates, guards PASS | formal checkpoints, histories, guards | `p4_weight_localization.py` worker | One model per seed; no pooling | seed 17 903.29 s; seed 29 907.75 s; both PASS | ELIGIBLE, bounded to actual worker label | Execution complete | Does not prove scientific benefit |
| Harm reduction, seed 17 | Lower endpoint > 0 | `development_nll.csv`, matched arrays | paired record bootstrap | 2,000 source-stratified draws | `-0.001374`, CI `[-0.001529,-0.001214]` | ELIGIBLE | Fails harm conjunction | Negative favors current H-sem |
| Harm reduction, seed 29 | Lower endpoint > 0 | same | same | same | `-0.0000475`, CI `[-0.000142,0.0000474]` | ELIGIBLE | Not positive | Interval straddles zero |
| Net semantic benefit, seed 17 | Lower endpoint > 0 | same | same | same | `+0.008722`, CI `[+0.008222,+0.009244]` | ELIGIBLE | Positive single-seed contrast | Not replicated |
| Net semantic benefit, seed 29 | Lower endpoint > 0 | same | same | same | `-0.002357`, CI `[-0.002732,-0.001971]` | ELIGIBLE | Negative | Opposite seed direction |
| Typed P4 verdict | Section 15 conjunction map | `analysis/verdict.json` | registered classifier | Four primary intervals, no seed pooling | `HALF_WEIGHT_REPAIR_NOT_REPLICATED` | ELIGIBLE, bounded | Registered verdict | Cannot generalize beyond exact arm |

## 7. Main Results

### Eligible decision evidence

At update 512, the weak arm's development NLL was 0.688535 for seed 17 and 0.689528 for seed 29. Current `H-sem` was 0.687162 and 0.689481; task-only `H-task` was 0.697257 and 0.687171 respectively. These values are the source rows for the four registered effects above.

### Bounded evidence

The result is bounded to the actual ACP worker label `N6LS-80G-SXM5` and to the existing P3 development/control arrays. The protocol's expected “H100 80GB” wording and platform's N6LS label are recorded as a resource-naming deviation; no data, objective, metric, or condition was changed.

### Stage-level profiling evidence

The 128/256/384 trajectories are descriptive only. At update 512, harm effects are negative or straddle zero, while benefit effects reverse across seeds. No trajectory or load diagnostic overrides the primary rule.

### Failed / ineligible evidence

Jobs `pt-yajflax0` and `pt-n4ilzz1d` failed at the smoke import boundary with `ModuleNotFoundError: transformers` after environment propagation defects. Their outputs were never used in the analysis. P4 smoke weights were discarded as required.

## 8. Visualization Results, When Decision-Relevant

### P4 harm-reduction and semantic-benefit effects

![P4 harm-reduction and semantic-benefit effects](</data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/p4-weight-20260907T024100Z/figures/weight_localization_effects.png>)

Purpose: show the registered update-512 effects and intervals for the two distinct questions.

Setup: two model seeds, four source-stratified paired bootstrap intervals, positive values favor weak supervision.

Metric definition and unit: baseline development answer NLL minus weak development answer NLL, nat per answer token.

Raw source and lineage row: `analysis/weight_localization_effects.csv`, rows with `update=512`; lineage rows in Section 6.

Aggregation and uncertainty: complete-record paired bootstrap, 2,000 draws, seed `20260907`; seeds remain separate.

How to read: orange harm-reduction points should both lie above zero for the registered repair; blue benefit points should both lie above zero for replicated net semantic benefit.

Expected under registered outcomes: positive orange conjunction for repair; positive blue conjunction for stronger benefit claim.

Observed result: orange seed 17 is negative and seed 29 straddles zero; blue seed 17 is positive and seed 29 is negative.

Take-home: the exact 0.25/0.25 repair is not replicated and there is no two-seed semantic-benefit conjunction.

Remaining uncertainty: other causes of the P3 reversal remain live.

What this figure does not prove: global weight optimality, teacher truth, route function, test performance, or deployment benefit.

Anchor update implication: preserve the P3 boundary and do not promote the weight-only explanation; human confirmation is required before changing the Anchor or Focus.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| Identity audit | `receipts/identity.json` | Passed | None; 27 P3 inputs verified, same-seed initial tensors match | Reuse mismatch and obvious data/teacher drift | Other mechanism causes |
| Unit tests | `logs/tests.log` | Passed | 21/21 tests | Registered coefficient/verdict path regressions in this worker | Scientific outcome |
| Smoke | `receipts/smoke.json` | Passed | Finite history, changed banks, frozen embedding/head | Basic weak path/gradient failure | Full-run behavior |
| Formal seed 17 | guard, checkpoints, history | Passed | 512/512, guard PASS | Missing/invalid seed-17 arm | Cross-seed replication |
| Formal seed 29 | guard, checkpoints, history | Passed | 512/512, guard PASS | Missing/invalid seed-29 arm | Other mechanism explanation |
| Frozen analysis | CSV, JSON, figure, manifest | Passed | Exact registered bootstrap and classifier | Ad hoc pooled or retuned verdict | Generalization and causal mechanism |
| Earlier attempts | two failure receipts | Failed / ineligible | Runtime propagation import failure | Their outputs cannot influence result | No scientific conclusion from failed attempts |

Falsified physical prior: not adjudicated; this P4 only tests one operational weight explanation.

Falsified mathematical model: not adjudicated.

Falsified operationalization / proxy: the exact 0.25 repair was not supported as a two-seed repair.

Falsified implementation: no successful-run implementation failure; earlier environment failures were repaired and excluded.

Falsified metric: not shown; the registered metric produced a complete typed verdict, but remains development-only.

Remaining rival explanations: seed-sensitive optimization, route/path effects, load or expert-utilization effects, pseudo-label quality, and other supervision interactions remain unresolved.

## 10. Full Experiment Record

The successful ACP job was `pt-ahj3yiaw`, created 2026-09-07 02:41 UTC and completed 2026-09-07 03:00 UTC. It used one node, one `n6ls.iu.i40.1` GPU, reserved quota, normal priority, and automatic retry zero. The remote command activated the audited runtime layer and ran the P4 runner with the frozen P3 root and a new P4 output root.

The worker elapsed time was 1,893.14 seconds. Formal seed elapsed times were 903.29 seconds (17) and 907.75 seconds (29). The successful run's completion receipt, formal receipt, smoke receipt, identity receipt, logs, checkpoints, analysis outputs, figure, and manifest are all under the result root listed in Section 15.

## 11. Interpretation

Observation: lowering the semantic coefficient to 0.25 did not produce a positive harm-reduction effect in both seeds. The task-only comparison is positive in seed 17 but negative in seed 29.

Protocol-grounded interpretation: the exact “current semantic supervision is too strong” explanation is not supported by the registered two-seed criterion. The result also does not support a replicated net semantic-supervision benefit.

Human judgment status: the protocol-typed verdict is recorded, but the researcher must still confirm the Focus-level result wording, cannot-claim boundary, and one next decision.

## 12. Claim Boundary

Can claim: under the exact frozen architecture, data, load-off policy, coefficient, development metric, and two seeds, the 0.25/0.25 weak arm completed validly but did not replicate repair or net benefit.

Cannot claim: semantic supervision generally works or fails; 0.25 is optimal; P3's verdict changes; GMM groups are semantic truth; router agreement implies expert utility; or any test/free-generation/deployment/public-benchmark gain.

## 13. Next Decision

Decision: **AI 建议 — stop the exact weight-only repair branch and ask the researcher to select one new mechanism question or close this local branch.**

Completion criterion: researcher confirms the P4 result, boundary, and exactly one next decision in the active Focus.

Resume action: only after confirmation, update the Anchor/Focus; a new experiment requires a new or amended frozen Protocol and explicit execution scope.

## 14. Artifact Manifest

The machine-generated manifest is `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/p4-weight-20260907T024100Z/artifact_manifest.json`, status `COMPLETE`, SHA-256 `ca1c067323d0a0490a06846c3d3339800458566d0336ba187dccec8d992b669c`.

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `protocol_snapshot.md` | Frozen contract used by worker | P4 worker | canonical Protocol before amendment | `0c9b542f...f4bd9b` | yes | yes | Scientific body frozen |
| `receipts/identity.json` | Data/teacher/control/code identity | P4 worker | P3 manifest, processed tensor, teacher | `8d7ad09b...05648` | yes | yes | 27 inputs, no mismatches |
| `receipts/smoke.json` | Smoke acceptance | P4 worker | two-update seed-17 smoke | `1076903b...7d2415` | yes | guard only | Smoke weights discarded |
| `receipts/formal.json` | Formal arm completion | P4 worker | seeds 17/29 | `aa5289b5...28f6f93` | yes | yes | Both guards PASS |
| `analysis/development_nll.csv` | Primary NLL rows | registered analysis | formal/control arrays | `d8634ba1...85af15` | yes | yes | 24 rows, 4 checkpoints |
| `analysis/weight_localization_effects.csv` | Four primary intervals plus trajectories | registered analysis | matched dev arrays | `7da15b7d...a5e1b` | yes | yes | 16 rows |
| `analysis/verdict.json` | Typed verdict | registered classifier | primary effects | `fb0a72ce...b1b74` | yes | yes | `HALF_WEIGHT_REPAIR_NOT_REPLICATED` |
| `figures/weight_localization_effects.png` | Decision-bearing figure | registered analysis | effects CSV | recorded in manifest | yes | yes | Orange/blue contrasts |
| `receipts/completion.json` | End-to-end completion | P4 worker | all stages | `af5015a1...0d08ba` | yes | yes | 1,893.14 seconds |
| formal checkpoints, histories, guards | Reproducible raw run evidence | P4 worker | seeds 17/29 | full hashes in machine manifest | yes | bounded | Remain in execution workspace |
| failed receipts for `pt-yajflax0`, `pt-n4ilzz1d` | Failure audit | failed workers | smoke logs | paths in amendment P4-A1 | yes | no | Excluded from all comparisons |

## 15. Links

anchor: `main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md`

protocol: `protocol.md`

summary: `summary.md`

code workspace: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training`

runner: `p4_weight_localization.py`

config: `config.py`, `runtime.py`, `condition_worker.py`

data / manifest: `/data/250010109/datasets/a15_e14_p3_clean/processed.pt`; P3 reversal manifest under the P3 run root; P4 `artifact_manifest.json`

result dir: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/p4-weight-20260907T024100Z`

figure dir: `<result dir>/figures`

logs / checkpoints: `<result dir>/logs`, `<result dir>/conditions/formal_512`

repro command: `source /data/250010109/MoE_Router/experiments/20260730_h768_4layer_switch_5090_smoke/scripts/activate_runtime_layer.sh && PYTHONPATH=<P4 root>:$PYTHONPATH python p4_weight_localization.py --p3-run-root <P3 run root> --p4-run-root <new P4 run root> --protocol <canonical protocol>`

job ids: failed/ineligible `pt-yajflax0`, `pt-n4ilzz1d`; successful `pt-ahj3yiaw`.
