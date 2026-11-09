# Detailed: A12_0_E04 Balanced Per-Sample Dual-Map Carrier — Stage A

Primary anchor: [12_0 short-range single-step versus two-step composition](../../../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md)
Protocol: [protocol.md](protocol.md)
Summary: [summary.md](summary.md)

## 0. Quick Recap

- **Purpose:** qualify or reject E04's balanced short carrier using NTP only, before any MTP result.
- **Protocol verdict:** `stage_a_blocked`.
- **Completed evidence:** 12 of 12 trajectories, 201 evaluations per trajectory, three seeds per scale/task, remote job succeeded.
- **Capability result:** no eligible layer count; no mastery threshold frozen.
- **Validity result:** the row-removal necessity guard fails because a missing bijection row is recoverable by elimination.
- **Consequence:** Stage B is blocked. These results do not adjudicate MTP.

The protocol-defined pass/fail result above is mechanical. A researcher-authored post-result mechanism judgment has not yet been supplied; this record therefore does not promote a mechanism explanation beyond the measurements.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Decision role | Cannot prove |
|---|---|---|---|---|---|
| final-window pass | stable task mastery at the end of training | every accuracy evaluation from steps 19,000--20,000 is at least `0.95` | Boolean | trajectory capability | generalization outside the generator |
| scale eligibility | shared capability for a layer count | both tasks, all three seeds, all final-window evaluations pass; no early sustained exact group | Boolean | permits threshold selection | MTP benefit |
| first hit | first recorded checkpoint at or above a threshold | minimum evaluated optimizer step; no interpolation | optimizer steps | future speed metric support | stable mastery by itself |
| seed spread | dependence on random initialization/training stream | minimum-to-maximum accuracy across three seeds | accuracy range | detects unstable capability | cause of instability |
| first-hop-only error | returning intermediate \(B\) on a two-step question | standard-head top-1 equals \(B\), plus probability assigned to \(B\) | fraction / probability | localizes partial composition | a causal hidden state |
| post-run guard correction | logic audit performed after training completed | recompute the row-removal claim using the bijection constraint | pass/fail | protects carrier validity | changes the already measured curves |

## 2. Anchor Link And Decision Point

The anchor asks whether a later MTP speed gain is larger for two ordered map applications than for one while length, position, and format are matched. Stage A is upstream: if NTP cannot stably learn both tasks at one scale, steps-to-threshold cannot be compared without a floor effect.

The Stage-A hypothesis required at least one of the 2- or 4-layer scales to learn both depths across all three seeds. This hypothesis failed under the approved 20,000-step contract.

## 3. Protocol Compliance Audit

| Audit item | Status | Evidence / issue |
|---|---|---|
| approved conditions match actual conditions | pass | 2/4 layers × one/two-step × seeds 1201--1203; NTP only |
| objective restriction | pass | 12 final rows all label `objective=ntp`; second head instantiated but absent from loss |
| primary metric exists | pass | complete 100-step calibration accuracy curves |
| seeds and checkpoints recorded | pass | 12 unique run IDs; 201 checkpoints per trajectory |
| central figure and tables exist | pass | learning-curve figure plus raw and curated CSV tables |
| fixed calibration balance | pass | both \(B\) and \(Y\) exactly balanced over 128 aliases |
| fixed split overlap | pass | zero base-fingerprint overlap |
| paired serialization | pass | positions 1--29 identical; only `DEPTH` and final answer differ |
| wrong-order rejection | pass | two-step reverse-order accuracy is exactly `0.0` |
| row-removal necessity | **fail** | four visible rows of a bijection uniquely determine the fifth output |
| confirmation-set sealing | pass with note | only generator structure/fingerprints were audited; no model prediction used it |
| device utilization metric | missing secondary evidence | startup GPU inventory exists, but no during-training utilization trace was saved |
| success/failure rule applied | pass | no eligible scale, no threshold, Stage B blocked |

The original job-time automatic audit incorrectly set both row-removal booleans to `true`. The post-run audit corrected the runner and regenerated the aggregate without rerunning training. The corrected aggregate has `all_data_audits_passed=false`. Because the corrected runner now stops before training on this known guard failure, the original uncommitted training source is not an immutable replay artifact; the training logic is otherwise unchanged. This is recorded as a reproducibility limitation, not hidden as a passed audit.

## 4. Setup

### Data construction

Each base example contains five active aliases, two distinct relation headers, and two fresh random bijections. A valid query \(A\) is sampled so that \(A\), \(B=\pi_1(A)\), and \(Y=\pi_2(B)\) are distinct and reverse composition does not equal \(Y\). Rows inside each table and the order of the two table blocks are independently shuffled.

The paired sequences are:

```text
[DEPTH, A, r1, r2,
 MAP, header, key1, value1, ..., key5, value5,
 MAP, header, key1, value1, ..., key5, value5,
 DECIDE, SHARED, ANSWER]
```

The one-step answer is \(B\) and the two-step answer is \(Y\). Both sequences have 31 tokens and share positions 1--29 exactly.

### Model and objective

| Setting | Value |
|---|---|
| architecture | causal decoder-only pre-LN Transformer |
| layers | 2 or 4 |
| width / attention heads / FFN width | 128 / 4 / 512 |
| dropout | 0 |
| heads | tied standard vocabulary head plus independent second vocabulary head |
| trained objective | full-position standard next-token cross-entropy only |
| MTP | not implemented or run in Stage A |
| parameters | 438,912 at 2 layers; 835,456 at 4 layers |

### Optimization and evaluation

| Setting | Value |
|---|---|
| optimizer | AdamW, betas \((0.9,0.95)\), weight decay `0.01` |
| learning rate | `1e-3` to `1e-4` cosine, 200-step warmup |
| gradient clipping | `1.0` |
| batch / steps | 512 examples / 20,000 optimizer steps |
| examples per trajectory | 10,240,000 online training examples |
| evaluation | 8,192 fixed calibration examples every 100 steps |
| final window | steps 19,000--20,000 inclusive |
| seeds | 1201, 1202, 1203 |
| precision | FP32 |
| compute | one 4×H100-80GB reserved ACP worker; one shard per GPU |
| job wall interval | 08:40:17--08:49:17 UTC, approximately 9 minutes |

Within a layer count and seed, one-step and two-step runs used the same initialization seed and the same base-instance/serialization stream. The task depth token and final answer were the intended differences.

## 5. Metrics And Decision Rules

### Primary capability metric

For each trajectory, compute standard-head final-answer accuracy at every 100-step evaluation. Capability requires:

\[
\min_{t\in\{19000,19100,\ldots,20000\}}
\operatorname{Acc}^{q_1}(t)\ge 0.95.
\]

A layer count is eligible only if all six trajectories at that scale pass. The non-saturation guard additionally rejects a task group whose median first step of three consecutive exact-accuracy evaluations is at or before step 2,000.

### Threshold freeze

Only eligible scales may enter threshold selection over `0.80`, `0.90`, `0.95`, and `0.99`. Because no scale is eligible, every threshold is formally ineligible and none is selected.

### Secondary metrics

- first-hit step at each candidate threshold;
- final-window minimum and mean;
- final top-1 rate and probability assigned to intermediate \(B\) on two-step examples;
- token-class cross-entropies;
- generator-aware query-hidden and fixed-position baselines.

## 6. Main Results

### 6.1 Group-level decision table

| Layers | Task depth | Finals by seed | Mean final | All final windows pass? | Median sustained exact | Non-saturated? | Scale eligible? |
|---:|---|---|---:|---|---|---|---|
| 2 | one-step | 0.6187, 0.3727, 0.8716 | 0.6210 | no | never | yes | no |
| 2 | two-step | 0.2504, 0.2485, 0.2499 | 0.2496 | no | never | yes | no |
| 4 | one-step | 0.9993, 0.8375, 0.9983 | 0.9450 | no | never | yes | no |
| 4 | two-step | 0.3281, 0.3268, 0.3308 | 0.3286 | no | never | yes | no |

The non-saturation condition passes because no group reached three consecutive exact evaluations, but non-saturation cannot rescue a failed capability condition.

### 6.2 Full trajectory table

Blank threshold cells mean the trajectory never reached that level.

| Run | Final | Final-window min | Final-window mean | Best (step) | Hit .80 | Hit .90 | Hit .95 | Hit .99 | Final \(B\) top-1 | Final \(p(B)\) | Pass? |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| L2 single s1201 | 0.6187 | 0.6128 | 0.6156 | 0.6193 (19500) | — | — | — | — | 0.6187 | 0.5506 | no |
| L2 single s1202 | 0.3727 | 0.3641 | 0.3705 | 0.3779 (15700) | — | — | — | — | 0.3727 | 0.3466 | no |
| L2 single s1203 | 0.8716 | 0.8685 | 0.8720 | 0.8774 (19900) | 13600 | — | — | — | 0.8716 | 0.8428 | no |
| L2 two s1201 | 0.2504 | 0.2504 | 0.2553 | 0.2657 (16800) | — | — | — | — | 0.2454 | 0.2475 | no |
| L2 two s1202 | 0.2485 | 0.2462 | 0.2501 | 0.2610 (10500) | — | — | — | — | 0.2516 | 0.2452 | no |
| L2 two s1203 | 0.2499 | 0.2443 | 0.2483 | 0.2590 (3600) | — | — | — | — | 0.2572 | 0.2493 | no |
| L4 single s1201 | 0.9993 | 0.9988 | 0.9992 | 0.9995 (18500) | 14600 | 14900 | 15000 | 15300 | 0.9993 | 0.9960 | yes |
| L4 single s1202 | 0.8375 | 0.8257 | 0.8314 | 0.8375 (20000) | 16300 | — | — | — | 0.8375 | 0.8080 | no |
| L4 single s1203 | 0.9983 | 0.9830 | 0.9949 | 0.9983 (20000) | 12900 | 13400 | 18900 | 19200 | 0.9983 | 0.9922 | yes |
| L4 two s1201 | 0.3281 | 0.3268 | 0.3311 | 0.3365 (16400) | — | — | — | — | 0.1332 | 0.1204 | no |
| L4 two s1202 | 0.3268 | 0.3181 | 0.3255 | 0.3350 (10300) | — | — | — | — | 0.1311 | 0.1220 | no |
| L4 two s1203 | 0.3308 | 0.3257 | 0.3324 | 0.3373 (19400) | — | — | — | — | 0.1321 | 0.1243 | no |

### 6.3 What each trajectory contributes

1. **L2 single s1201:** reaches only moderate partial learning and remains stable near `0.616`; shows that failure is not a transient final-checkpoint dip.
2. **L2 single s1202:** remains at `0.373`; exposes large initialization/stream sensitivity within the same formal setup.
3. **L2 single s1203:** reaches `0.80` late but never `0.90`; even the best 2-layer single-step seed misses capability.
4. **L2 two s1201:** remains near `0.25`; does not show late learning.
5. **L2 two s1202:** independently reproduces the same plateau, ruling out one unlucky seed.
6. **L2 two s1203:** reproduces the plateau a third time; 2-layer two-step failure is cross-seed stable.
7. **L4 single s1201:** crosses `0.95` at step 15,000 and finishes near exact; proves that one-step rule learning is possible at this scale.
8. **L4 single s1202:** crosses `0.80` but not `0.90`; prevents treating the successful 4-layer seeds as stable capability.
9. **L4 single s1203:** reaches `0.95` only at step 18,900 and finishes near exact; confirms a late phase transition rather than early saturation.
10. **L4 two s1201:** plateaus at `0.328`; extra layers help over the 2-layer plateau but do not approach mastery.
11. **L4 two s1202:** reproduces the same final level and excludes seed-specific failure.
12. **L4 two s1203:** again reproduces the plateau; all three 4-layer two-step runs fail consistently.

### 6.4 First-hop error decomposition

For 2-layer two-step runs, \(B\) top-1 rates (`0.245`--`0.257`) and answer accuracies (`0.249`--`0.250`) are both near a roughly uniform choice among the five active aliases. For 4-layer two-step runs, final-answer accuracy rises to about `0.329`, while \(B\) top-1 falls to about `0.132` and \(p(B)\) to about `0.122`.

Therefore the 4-layer failure is not well described as “the first lookup is learned and the model simply outputs \(B\).” The model has learned some reproducible structure that favors \(Y\) over \(B\), but behavioral outputs do not identify which operation or shortcut produced the `0.329` plateau.

## 7. Visualization Results

### NTP-only answer capability by scale and task depth

![NTP-only answer capability by scale and task depth](figures/stage_a_learning_curves.png)

- **Purpose:** decide whether at least one formal scale stably learns both tasks without an early ceiling.
- **Data source:** all 12 calibration trajectories from job `pt-9863fywz`.
- **Aggregation:** line is the three-seed mean; shading is seed minimum to maximum at each checkpoint.
- **Axes:** optimizer step on x; standard-head final-answer accuracy on y.
- **Reference lines:** horizontal `0.95` capability level; vertical step 2,000 non-saturation boundary.
- **Expected if supported:** both panels for one layer count exceed `0.95` for every seed in the final window, with no early exact plateau.
- **Observed:** 4-layer single-step learning undergoes a late, seed-dependent rise; both two-step panels remain far below `0.95`.
- **Take-home:** there is no shared capable scale and no basis for a steps-to-threshold objective comparison.
- **Remaining uncertainty:** whether the floor is due to model capacity, optimization, redundant-bijection task structure, or another operational detail.
- **Cannot prove:** absence of an internal intermediate state or failure of MTP.

Rendered-artifact audit: the PNG renders, all four condition labels and reference lines are readable, the y-axis unit is accuracy, and the result is understandable without source-code access.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What it rules out |
|---|---|---|---|---|
| infrastructure | ACP job succeeded; 12 unique final rows | passed | none | incomplete-run explanation |
| serialization/balance | exact pairing, exact answer balance, zero split overlap | passed | none | basic length/frequency/overlap confounds |
| necessary-row guard | missing bijection row inferred by unused output | failed | mathematical redundancy of a bijection table | claim that each displayed core row is individually necessary |
| grammar/format | final standard-format accuracy is `1.0` in every trajectory | passed | none | failure to learn `DECIDE→SHARED` format |
| 2-layer one-step | finals `0.373`--`0.872` | failed | seed-unstable partial learning | stable small-scale capability |
| 2-layer two-step | finals near `0.250` | failed | stable floor | unlucky-seed explanation |
| 4-layer one-step | two pass, one at `0.838` | failed group gate | seed instability | all-seed one-step capability |
| 4-layer two-step | finals near `0.329` | failed | stable floor | task mastery at the larger formal scale |
| threshold freeze | no eligible scale | blocked | upstream capability failure | valid Stage-B steps-to-threshold comparison |

- **Falsified physical prior:** not the broad idea that fresh maps can test composition; the current data/model realization did not meet its prerequisite.
- **Falsified operationalization:** yes. E04 as specified fails both a data necessity guard and the shared NTP capability gate.
- **Falsified implementation:** the original row-removal audit implementation was wrong and has been corrected. The training/evaluation path completed.
- **Falsified metric:** no. The strict final-window accuracy rule correctly exposed floor and seed-instability risks.
- **Remaining rival explanations:** capacity/optimization floor, task redundancy from full bijections, and other generator-induced structure. Stage A does not separate them.

## 9. Generator Guard Results

| Predictor / check | One-step | Two-step | Interpretation |
|---|---:|---:|---|
| symbolic full oracle | 1.0000 | 1.0000 | task label construction is internally consistent |
| query-hidden generator-aware | 0.5668 | 0.5668 | rejection constraints leak more than candidate chance |
| frequency-only | 0.2009 | 0.2031 | near five-active-alias chance |
| first serialized row value | 0.2024 | 0.2004 | row position is balanced |
| swapped relation order | 0.2146 | 0.0000 | reverse answer is excluded for two-step |
| header-blind serialized order | 0.6033 | 0.4958 | random table order leaves a roughly half-correct table-choice shortcut |
| delete queried row | identifiable | identifiable | fails because the missing bijection value is recoverable |

The query-hidden value is below all proposed mastery thresholds, so it would not alone block threshold selection. It is nevertheless a material property of the generator and must not be described as five-way chance.

## 10. Observation, Interpretation, Decision, Boundary

### Observation

No layer count passes shared NTP capability. Two-step results are stable across seeds at low plateaus. The data audit also fails the individual-row necessity clause.

### Interpretation

The 2/4-layer setup is not a valid carrier for comparing objective learning speed. The two-step plateau cannot be interpreted as an MTP mechanism result because MTP was not run and the shared capability prerequisite failed.

### Decision

Set `eligible_layers=[]`, `selected_accuracy_threshold=null`, and keep `formal_comparison_allowed=false`.

### Boundary

Do not infer that two-step composition is generally unlearnable, that MTP would or would not help, or that the standard head does not use \(B\). Do not average successful one-step seeds with failed two-step conditions to manufacture a threshold.

## 11. Full Experiment Record

| Item | Value |
|---|---|
| run name | `a12_0_e04_stage_a_20260715_0840` |
| ACP job | `pt-9863fywz` |
| job state | `SUCCEEDED` |
| worker spec | `n6ls.iu.i40.4`, reserved, 4×H100 80GB |
| completed trajectories | 12 / 12 |
| objective labels | NTP only |
| training examples | 10,240,000 per trajectory; 122,880,000 total |
| calibration size | 8,192 fixed examples |
| sequence length | 31 tokens |
| evaluation interval | 100 steps |
| generator manifest hash | see `data_manifest.json` in the raw result directory |
| current corrected runner SHA-256 | `4a2b7711830b36ef51c15d8089c2cb25a68c80e6cf5a191149636f82d27e030f` |
| config SHA-256 | `fa61685a341ee8a6582622eeb8c457e48434204f4503aab5b5d440d9960caa2e` |

## 12. Claim Boundary

### Supported

- The run completed the approved NTP matrix without infrastructure loss.
- The current 2- and 4-layer settings do not give shared, cross-seed capability on this carrier.
- No accuracy threshold can be frozen under the approved rule.
- A missing row in a full bijection table is not individually necessary.

### Not supported

- any NTP/MTP comparison;
- any composition-specific MTP advantage;
- an explicit or causally used intermediate \(B\);
- a general depth, scaling, or transfer law;
- wall-clock or FLOP efficiency of MTP;
- impossibility of learning with another capacity or valid carrier.

## 13. Next Decision

The only next decision is whether to close E04 under its frozen contract or reopen carrier/capability design in a new Protocol. Stage B remains blocked until a structurally valid carrier has at least one NTP-eligible scale and a frozen threshold.

## 14. Links And Artifact Map

- **Anchor:** [12_0 anchor](../../../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md)
- **Protocol:** [protocol.md](protocol.md)
- **Summary:** [summary.md](summary.md)
- **Code workspace:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`
- **Runner:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a12_0_e04_stage_a_ntp_capability.py`
- **Submitter:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a12_0_e04_stage_a_4gpu_acp.sh`
- **Config:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a12_0_e04_stage_a_ntp_capability.json`
- **Raw result directory:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a12_0_e04_stage_a_ntp_capability/a12_0_e04_stage_a_20260715_0840`
- **Raw log directory:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a12_0_e04_stage_a_20260715_0840`
- **Curated figure:** [stage_a_learning_curves.png](figures/stage_a_learning_curves.png)
- **Curated raw finals:** [final_metrics.csv](tables/final_metrics.csv)
- **Curated trajectory table:** [trajectory_decision_table.csv](tables/trajectory_decision_table.csv)
- **Curated group table:** [group_result_table.csv](tables/group_result_table.csv)
- **Capability table:** [capability_by_group.csv](tables/capability_by_group.csv)
- **Threshold table:** [threshold_eligibility.csv](tables/threshold_eligibility.csv)
- **Guard table:** [data_guard_summary.csv](tables/data_guard_summary.csv)
- **Reproduction command:** `RUN_NAME=<new_name> A12_0_E04_STAGE_A_ALLOW_REAL_SUBMIT=1 bash active/synthetic_data_understanding/scripts/submit_a12_0_e04_stage_a_4gpu_acp.sh`
- **Important replay note:** the corrected runner now blocks before training on the failed row-removal guard. Reproducing the historical trajectories requires an explicit, documented override in a newly approved Protocol; do not bypass the guard silently.
