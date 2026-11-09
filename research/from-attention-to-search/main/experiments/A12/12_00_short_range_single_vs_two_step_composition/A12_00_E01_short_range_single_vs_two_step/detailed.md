# Detailed Record — A12_0_E01 Calibration

## 1. Conclusion First

Job `pt-3okyxyjm` completed successfully on four GPUs and produced all 24 preregistered calibration runs. The capability gate failed: no depth made both objectives reliably solve the two-step held-out-rule-pair task across seeds 1201 and 1202. The standard-head steps-to-threshold metric is therefore undefined for decision purposes, even though complete curves were recorded.

This result stops the experiment before threshold selection. Confirmation seeds 1301–1305 were not run.

## 2. Terminology / Definitions

| Item | Plain meaning | Concrete computation | Unit | Decision use | Cannot prove |
|---|---|---|---|---|---|
| \(q_1\) / standard head | common next-token output head | logits at position 6 predict token 7 | accuracy in \([0,1]\) | shared outcome across NTP/MTP | internal causal path |
| \(q_2\) / second head | head predicting two positions ahead | logits at position 5 predict token 7 | accuracy in \([0,1]\) | verifies direct MTP answer learning | deployment behavior |
| final accuracy | accuracy at step 20,000 | full 8-pair by 32-state test enumeration | fraction | capability snapshot | fastest or best transient accuracy |
| maximum trajectory accuracy | best recorded value over 100-step evaluations | maximum test \(q_1\) answer accuracy | fraction | detects transient learning | stable convergence |
| probe accuracy | linear ridge readout of \(B=r_1(A)\) | held-out 32-way classification | fraction | formation diagnostic | causal use by \(q_1\) |

## 3. Data and Model Contract

### Data

```text
[BOS, DEPTH_1|DEPTH_2, STATE_A, RULE_r1, RULE_r2,
 DECIDE, SHARED, ANSWER_Y, EOS]
```

- State cardinality: 32.
- Rule count: eight fixed random permutations generated with seed 1200.
- Ordered rule pairs: all \(8\times8=64\) pairs, split into 48 train, 8 validation, and 8 test pairs.
- Single-step label: \(Y=r_1(A)\); \(r_2\) is a matched distractor.
- Two-step label: \(B=r_1(A)\) and \(Y=r_2(B)\).
- Validation and test each enumerate every held-out rule pair over all 32 states.
- Data-manifest SHA-256: `ed5e183a65d9cbdbda27584564b1e4a9d624625a5fb2b870268ea61c4a4d9da3`.

### Model

- Decoder-only causal Transformer, random initialization.
- Pre-layer normalization, learned position embeddings, GELU, dropout 0.
- Width 128, four attention heads, feed-forward width 512.
- Depths: 1, 2, and 4 layers.
- Parameter counts: 211,456; 409,728; 806,272 respectively.
- The standard head is tied to token embeddings; the second head is separate.
- Both NTP and MTP instantiate and execute both heads.

### Objectives

\[
L_{\mathrm{NTP}}=\operatorname{CE}(q_1(h_t),x_{t+1}),
\]

\[
L_{\mathrm{MTP}}=\operatorname{CE}(q_1(h_t),x_{t+1})+
\operatorname{CE}(q_2(h_t),x_{t+2}).
\]

The second term has weight 0 for NTP and 1 for MTP. Parameter count and forward computation are matched; backward computation and gradient dose are not.

## 4. Training and Execution

| Setting | Value |
|---|---:|
| Optimizer | AdamW |
| Learning rate | \(10^{-3}\) |
| Minimum learning rate | \(10^{-4}\) |
| Betas | \((0.9,0.95)\) |
| Weight decay | 0.01 |
| Warmup | 200 steps |
| Schedule | cosine |
| Gradient clipping | 1.0 |
| Batch size | 512 |
| Precision | FP32 |
| Steps per run | 20,000 |
| Evaluation interval | 100 steps |
| Calibration seeds | 1201, 1202 |

Execution:

```text
ACP job: pt-3okyxyjm
state: SUCCEEDED
quota: reserved
worker: 1 x n6ls.iu.i40.4
accelerators: 4 x N6LS-80G
run: a12_0_short_composition_calibration_20260714_174654
```

Each GPU ran six independent conditions. All shards reported six completed runs and aggregation validated 24 unique run identifiers.

## 5. Complete Decision Evidence

### 5.1 Final standard-head accuracy

| Layers | Task | Objective | Seed 1201 | Seed 1202 | Mean | Verdict |
|---:|---|---|---:|---:|---:|---|
| 1 | single | NTP | 1.0000 | 1.0000 | 1.0000 | learned |
| 1 | single | MTP | 1.0000 | 1.0000 | 1.0000 | learned |
| 1 | two-step | NTP | 0.1797 | 0.1367 | 0.1582 | partial only |
| 1 | two-step | MTP | 0.1367 | 0.2148 | 0.1758 | partial only |
| 2 | single | NTP | 1.0000 | 1.0000 | 1.0000 | learned |
| 2 | single | MTP | 1.0000 | 1.0000 | 1.0000 | learned |
| 2 | two-step | NTP | 0.1016 | 0.0820 | 0.0918 | partial only |
| 2 | two-step | MTP | 0.1211 | 0.0781 | 0.0996 | partial only |
| 4 | single | NTP | 1.0000 | 1.0000 | 1.0000 | learned |
| 4 | single | MTP | 1.0000 | 1.0000 | 1.0000 | learned |
| 4 | two-step | NTP | 0.2969 | 0.9375 | 0.6172 | seed-unstable |
| 4 | two-step | MTP | 0.3008 | 0.2539 | 0.2773 | partial only |

The full per-run table, including validation, second-head, format, loss, and probe metrics, is [calibration_final_metrics.csv](tables/calibration_final_metrics.csv).

### 5.2 Maximum trajectory accuracy

For the 4-layer two-step condition, the maximum test standard-head accuracies were:

| Objective | Seed 1201 | Step | Seed 1202 | Step |
|---|---:|---:|---:|---:|
| NTP | 0.3203 | 18,900 | 0.9492 | 13,400 |
| MTP | 0.3281 | 12,100 | 0.2734 | 10,300 |

Thus the final result is not hiding stable high-accuracy MTP trajectories. Conversely, one NTP trajectory demonstrates that the 4-layer architecture can sometimes learn this carrier, so the result is instability rather than an absolute architectural impossibility.

### 5.3 Secondary-head and probe observations

- On every single-step MTP run, the second-head final answer accuracy was 1.0.
- On 4-layer two-step MTP runs, second-head final answer accuracy was 0.3008 and 0.2539, matching the partial standard-head regime rather than solving the task early.
- Probe accuracy varied widely. The strongest shared-position probe was 0.7109 on the successful 4-layer NTP seed 1202; several unsuccessful runs also had above-chance probe scores.

These observations are diagnostic only. They do not establish intermediate-state causal use, and they do not make an objective comparison eligible.

## 6. Visualization Results

### Plot contract

- **Question answered:** did each objective reliably learn the standard-head answer function at each model depth and task structure?
- **Metric:** full test enumeration standard-head answer accuracy; unit is fraction correct.
- **Source:** `calibration_curves.csv` from job `pt-3okyxyjm`.
- **Aggregation:** solid line is the two-seed mean; band is the seed minimum-to-maximum range at each 100-step evaluation.
- **Axes:** horizontal is optimizer step; vertical is test answer accuracy.
- **Allowed conclusion:** whether a condition shows reliable or seed-unstable learning during calibration.
- **Limitation:** no threshold was fixed, and the plot cannot identify why a condition learns.

![A12_0 calibration learning curves](figures/a12_0_calibration_learning_curves.png)

The rendered artifact was checked at 2160 by 2160 pixels. Titles, axes, legend, scale, and seed bands are readable. The left panels show rapid single-step learning. The upper-right and middle-right panels remain partial. The bottom-right panel exposes a large NTP seed split and consistently partial MTP behavior. No threshold is drawn.

## 7. Failure Decomposition and Rival Explanations

1. **Capability failure:** the immediate blocker. There is no model scale with reliable two-step learning under both objectives.
2. **Held-out pair generalization:** validation and test require unseen ordered rule pairs. Failure may reflect failure to factor atomic rules compositionally, not inability to fit the training distribution.
3. **Optimization mismatch:** MTP has a second full-sequence loss with weight 1. Matching parameters and forward compute does not match backward gradient magnitude or interference.
4. **Generic auxiliary-loss conflict:** the second-head objective includes all two-ahead tokens, not only the answer. Its effect may be unrelated to intermediate-state supervision.
5. **Seed instability:** the successful 4-layer NTP trajectory cannot be generalized from one seed.
6. **Probe/use gap:** above-chance intermediate-state probes coexist with poor answer accuracy, so readout alone cannot repair the behavioral gate.

The run does not isolate which rival caused failure. It only establishes that the present surface is not eligible for the planned threshold comparison.

## 8. Stop Conditions and Decision Audit

- All 24 runs reached the full 20,000-step budget: satisfied.
- Threshold-based early stopping: not used.
- Accuracy threshold: remains `null`.
- Capability numerical rule: remains pending, but every reasonable mastery-level rule is blocked by the observed two-step trajectories.
- Confirmation seeds: not used.
- Mechanism verdict: not issued.

Choosing a threshold near 0.1–0.3 would be post hoc and would classify partial, unstable behavior as task completion. Choosing a mastery-level threshold would leave most two-step conditions uncrossed. Therefore threshold selection is not the next valid action.

## 9. Artifact Map

```text
research anchor:
  Projects/from-attention-to-search/main/problem_anchors/
    12_structured_compositional_mtp_workload/
    12_0_short_range_single_vs_two_step_composition/
    12_0_short_range_single_vs_two_step_composition_anchor.md

protocol and reports:
  Projects/from-attention-to-search/main/experiments/A12/
    12_0_short_range_single_vs_two_step_composition/
    A12_0_E01_short_range_single_vs_two_step/

runner:
  active/synthetic_data_understanding/scripts/
    run_a12_0_short_range_single_vs_two_step_calibration.py

config:
  active/synthetic_data_understanding/configs/
    a12_0_short_range_single_vs_two_step_calibration.json

submission script:
  active/synthetic_data_understanding/scripts/
    submit_a12_0_short_range_single_vs_two_step_calibration_4gpu_acp.sh

raw result directory:
  active/synthetic_data_understanding/results/
    a12_0_short_range_single_vs_two_step_calibration/
    a12_0_short_composition_calibration_20260714_174654/

runtime logs:
  active/synthetic_data_understanding/logs/acp/
    a12_0_short_composition_calibration_20260714_174654/
```

Required raw outputs exist: configuration snapshot, data manifest, four shard curve tables, four shard final tables, four shard status files, aggregate curves, aggregate final metrics, aggregate JSON summary, and rendered learning curves.

## 10. Claim Boundary and Exactly One Next Decision

The result supports a calibration-level capability failure only. It does not support an NTP/MTP ranking or a composition mechanism claim.

**Exactly one next decision:** whether to rerun the same fixed-length one-step/two-step comparison with train and evaluation sharing ordered-rule-pair support, thereby removing held-out pair generalization from the capability gate. If chosen, the resulting claim must be limited to learning the controlled in-support workload; causal intermediate-state use remains deferred to `12_03`.
