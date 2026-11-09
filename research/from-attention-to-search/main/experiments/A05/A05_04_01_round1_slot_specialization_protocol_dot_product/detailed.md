## 0. Quick Recap

Purpose:

Run the standard dot-product-router version of the Round-1 minimal slot-block collapse audit for sparse top-1 MoE.

Hypothesis:

If slot information is visible in `h_B` but vanilla dot-product top-1 routing still collapses, then the failure is not missing representation. If supervised slot initialization preserves routing, then the slot partition is reachable under favorable initialization.

Experiment logic:

Use the balanced moving-block dataset `D_min_block_shift`; zero and freeze position embeddings; compute loss and routing metrics only at the `B_CONST` position; compare random-init baseline against supervised slot-centroid router initialization.

Conclusion:

The dot-product baseline reproduces collapse. Slot signal is perfectly decodable from `h_B`. P3 shows common-component dominance in the dot-product router margin. Supervised P5 initialization reaches perfect slot-level specialization in all 8 seeds.

Evidence:

P1 has mean `max_load=0.969`, mean `slot_to_expert_NMI=0.080`, and accuracy 1.0. P2 held-out-block-start slot probe accuracy is 1.0 in all P1 seeds. P3 common component dominates 290 / 320 final P1 margin rows. P5 has `slot_to_expert_NMI=1.0`, `max_load=0.25`, and accuracy 1.0 in all 8 seeds.

---

## 1. Anchor Mapping And Scope

Primary anchor:

`Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_01_uniform_feature_specialization_after_position_removal_anchor.md`

Experiment folder:

`Projects/from-attention-to-search/main/experiments/A05/A05_04_01_round1_slot_specialization_protocol_dot_product/`

Source protocol:

`daily_research_reports/0609/round1_slot_specialization_protocol.md`

Stage mapping:

- P0 Dataset Audit -> validate data and routed/loss positions.
- P1 Clean Baseline Re-Collapse -> test whether vanilla dot-product top-1 still collapses.
- P2 Slot Signal Probe -> test whether missing slot signal explains collapse.
- P3 Logit Trajectory Decomposition -> decompose dot-product router margins.
- P4 Forced-Routing Utility Audit -> not run.
- P5 Slot-Initialized Positive Control -> test reachability under supervised slot initialization.

Executed stages:

P0, P1, P2, P3, P5.

Explicitly not run:

P4, P6, P7.

---

## 2. Execution Record

ACP job:

`pt-eajzxnl3`

ACP status:

`SUCCEEDED`

Run name:

`round1_slot_specialization_dot_product_4gpu_20260609`

Submit log:

`logs/acp/round1_slot_specialization_dot_product_4gpu_20260609_submit_20260609_150220.log`

Runtime log:

`logs/acp/round1_slot_specialization_dot_product_4gpu_20260609_runtime_20260609_150408.log`

Runner:

`scripts/run_round1_slot_specialization_protocol_dot_product.py`

Submit script:

`scripts/submit_round1_slot_specialization_dot_product_4gpu_acp.sh`

Full command shape:

```bash
python "${EXP_DIR}/scripts/run_round1_slot_specialization_protocol_dot_product.py" \
  --output-dir "${EXP_DIR}" \
  --run-name "round1_slot_specialization_dot_product_4gpu_20260609" \
  --run-stage full \
  --variants "P1_clean_baseline,P5_slot_centroid_init" \
  --router-metrics "dot_product" \
  --seeds "20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528" \
  --train-steps "1600" \
  --train-repeats-per-pair "500" \
  --eval-repeats-per-pair "32" \
  --calibration-repeats-per-pair "32" \
  --batch-size "384" \
  --eval-batch-size "512" \
  --parallel \
  --max-parallel "4"
```

Smoke check:

A one-seed local smoke run completed before submission. It verified P0 artifact generation, P1 collapse behavior, P5 step-0 NMI = 1.0, and figure/table generation.

---

## 3. Dataset And Model Setup

Dataset:

`D_min_block_shift`

Construction:

- `S=4` slots: `SLOT_0..SLOT_3`
- `E=4` experts
- sequence length `L=12`
- one fixed `B_CONST`
- deterministic target rule: `SLOT_s -> Y_s`
- each sequence contains `SLOT_s B_CONST Y_s`
- valid block starts: `0..9`
- slot position: `block_start`
- routed `B_CONST` position: `block_start + 1`
- target position: `block_start + 2`

Sampling:

The full run used `train_repeats_per_pair=500`, so each seed trained on `4 * 10 * 500 = 20000` balanced examples. Evaluation used `eval_repeats_per_pair=32`, so each checkpoint used 1280 balanced examples.

Model:

- small causal Transformer + MoE
- sparse top-1 selected-gate router
- dot-product router: `z_e = w_e^T h_B`
- `d_model=128`
- `n_heads=4`
- `ffn_dim=256`
- `num_experts=4`
- position embeddings zeroed and frozen
- no auxiliary load-balance loss

Evaluation checkpoints:

`0, 1, 2, 5, 10, 20, 50, 100, 200, 500`, then every 100 steps through 1600.

---

## 4. P0 Dataset Audit

Purpose:

Verify that the dataset does not create a trivial imbalance or fixed-position shortcut.

How it was done:

P0 counted slot frequencies, block-start frequencies, `(slot, block_start)` frequencies, target mappings, route positions, and loss targets.

Result:

All checks passed.

Key values:

- each slot count: 320
- each block-start count: 128
- each `(slot, block_start)` count: 32
- each slot maps to exactly one target
- each block start contains all four targets
- route position is always `B_CONST`
- loss target is always `Y_s`

Interpretation:

Simple data imbalance and fixed-position shortcut are weakened as explanations.

Boundary:

P0 validates data construction only. It does not test representation, routing mechanism, or expert utility.

---

## 5. P1 Clean Baseline Re-Collapse

Purpose:

Test whether ordinary random-initialized dot-product sparse top-1 routing collapses in the clean minimal setting.

How it was done:

Train `P1_clean_baseline` for 1600 steps across 8 seeds with dot-product router, no position embeddings, fixed `B_CONST`, balanced moving block positions, and no load-balance auxiliary loss.

Metrics:

- `max_load`: collapse metric.
- `slot_to_expert_NMI`: slot-level routing specialization metric.
- `target_accuracy`: task learning check.

Result:

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| `target_accuracy` | 1.000 | 1.000 | 1.000 |
| `max_load` | 0.969 | 0.750 | 1.000 |
| `slot_to_expert_NMI` | 0.080 | 0.000 | 0.637 |
| `active_experts` | 1.125 | 1.000 | 2.000 |
| `per_slot_route_purity` | 1.000 | 1.000 | 1.000 |

Seed-level result:

Seven of eight seeds route all slots to one expert. Seed `20260527` uses two experts but still has `max_load=0.75`, so it remains hard-collapsed under the protocol threshold.

Central figure:

![P1 route heatmaps](figures/round1_slot_specialization_dot_product_4gpu_20260609/p1_route_heatmaps.png)

Interpretation:

The model learns the target perfectly but does not form a non-collapsed slot-to-expert partition.

Boundary:

High `per_slot_route_purity=1.0` is not positive specialization evidence here. It only says each slot routes consistently; all slots can consistently route to the same expert.

---

## 6. P2 Slot Signal Probe

Purpose:

Test whether P1 collapse is caused by missing slot information in the routed hidden state `h_B`.

How it was done:

At each checkpoint, collect `h_B` at `B_CONST` and train linear probes:

- random split probe: `h_B -> slot_id`
- held-out-block-start probe: train on most block starts, test on held-out starts
- block-start probe: `h_B -> block_start`

Final P1 result:

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| `slot_probe_accuracy_random_split` | 1.000 | 1.000 | 1.000 |
| `slot_probe_accuracy_heldout_position` | 1.000 | 1.000 | 1.000 |
| `position_probe_accuracy` | 0.175 | 0.049 | 0.383 |
| `slot_component_variance_ratio` | 0.999 | 0.995 | 1.000 |
| `position_component_variance_ratio` | 0.0004 | 0.0000 | 0.0028 |

Central figure:

![P2 probe trajectory](figures/round1_slot_specialization_dot_product_4gpu_20260609/p2_probe_accuracy_trajectory.png)

Interpretation:

Slot information is present and linearly decodable from `h_B`, including across held-out block starts. Missing slot representation is therefore not the main explanation for dot-product baseline collapse.

Boundary:

P2 does not show that experts have slot-specific utility. That would require P4.

---

## 7. P3 Dot-Product Logit Trajectory Decomposition

Purpose:

Determine whether top-1 dot-product routing decisions are driven by slot, common, block-position, or residual hidden components.

How it was done:

For each checkpoint, collect `h_B` and compute cell means:

\[
m_{s,p} = mean(h_B \mid slot=s, block\_start=p)
\]

Decompose each cell mean:

\[
m_{s,p} = c + r_s + u_p + residual_{s,p}
\]

where:

- `c` is the global common component;
- `r_s = mean_p(m_{s,p}) - c` is the slot component;
- `u_p = mean_s(m_{s,p}) - c` is the block-position component;
- `residual_{s,p} = m_{s,p} - c - r_s - u_p`.

For each `(slot, block_start)` cell, compute dot-product router logits, identify top-1 expert `e_1` and runner-up expert `e_2`, and define:

\[
\Delta w = w_{e_1} - w_{e_2}
\]

Then decompose the top-2 margin:

\[
\Delta w^T m_{s,p}
= \Delta w^T c
+ \Delta w^T r_s
+ \Delta w^T u_p
+ \Delta w^T residual_{s,p}
\]

Dominant component is the component with the largest absolute margin contribution.

Result:

In P1, the common component dominates the top-2 margin in most rows.

| Step | Rows | Common dominant | Slot dominant | Position dominant | Residual dominant |
|---:|---:|---:|---:|---:|---:|
| 0 | 320 | 286 | 18 | 15 | 1 |
| 1 | 320 | 263 | 40 | 15 | 2 |
| 2 | 320 | 250 | 48 | 21 | 1 |
| 5 | 320 | 299 | 18 | 3 | 0 |
| 10 | 320 | 280 | 37 | 3 | 0 |
| 20 | 320 | 280 | 40 | 0 | 0 |
| 50 | 320 | 290 | 30 | 0 | 0 |
| 1600 | 320 | 290 | 30 | 0 | 0 |

Route lock-in:

- P1 has 32 seed-slot rows.
- All 32 rows have `stable_lock_step <= 10`.
- 7 rows ever switch dominant expert.

Central figure:

![P3 margin decomposition](figures/round1_slot_specialization_dot_product_4gpu_20260609/p3_margin_decomposition_plots.png)

Interpretation:

Dot-product router decisions are usually dominated by the common component, not the slot component. This supports non-slot logit dominance plus early lock-in as the mechanism.

Boundary:

P3 is logit-level evidence. It does not prove common-logit cancellation will solve the problem and does not test expert causal utility.

---

## 8. P4 Forced-Routing Utility Audit (Not Run)

Purpose if run:

P4 would test whether slot-specific experts have causal utility for prediction by forcing each slot through each expert and measuring target loss.

Primary missing evidence:

The forced-route loss matrix by `(slot, expert)`.

Boundary:

Because P4 was not run, this experiment cannot claim that router-selected experts are functionally useful for their slots. It can only claim assignment collapse, representation visibility, logit dominance, and supervised reachability.

---

## 9. P5 Slot-Initialized Positive Control

Purpose:

Test whether the slot partition is reachable and stable if the dot-product router is placed into the intended slot-reading partition before normal training.

How it was done:

P5 is supervised initialization/calibration:

1. Build a balanced calibration set.
2. Collect step-0 `h_B`.
3. Compute slot centroids `\mu_s = mean(h_B \mid slot=s)`.
4. Center and whiten centroid directions.
5. Normalize the directions and copy them into router weight rows.
6. Calibrate only router weights as a bias-free classifier from `h_B` to `slot_id` for 400 steps.
7. Require step-0 `slot_to_expert_NMI >= 0.90`.
8. Train normally for 1600 steps.

Result:

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| `target_accuracy` | 1.000 | 1.000 | 1.000 |
| `slot_to_expert_NMI` | 1.000 | 1.000 | 1.000 |
| `per_slot_route_purity` | 1.000 | 1.000 | 1.000 |
| `max_load` | 0.250 | 0.250 | 0.250 |
| `active_experts` | 4.000 | 4.000 | 4.000 |

Central figure:

![P5 baseline vs positive control](figures/round1_slot_specialization_dot_product_4gpu_20260609/p5_baseline_vs_positive_control.png)

Interpretation:

Under supervised slot initialization, the dot-product router reaches perfect slot-level specialization in all 8 seeds. Therefore the slot partition is reachable and stable in this minimal setting.

Boundary:

P5 is not unsupervised discovery, not common-component removal, and not a deployable anti-lock-in method.

---

## 10. Required Final Questions

### 1. Did the clean minimal dataset reproduce collapse?

Yes. P1 dot-product baseline has accuracy 1.0, mean `max_load=0.969`, mean `slot_to_expert_NMI=0.080`, and hard collapse rate 1.0.

### 2. Was slot information decodable from the routed hidden state?

Yes. P2 final slot probe accuracy is 1.0 for both random split and held-out-block-start split in all P1 seeds.

### 3. Which logit component drove route changes?

The common component is the dominant final margin component in 290 / 320 P1 rows. This supports common-component dot-product logit dominance.

### 4. Was slot specialization reachable under positive control?

Yes. P5 reaches perfect final slot specialization in all 8 seeds: NMI 1.0, max load 0.25, all 4 experts active, accuracy 1.0.

### 5. What is the next decision?

Test a label-free intervention that can make the trainable router enter the reachable slot/exact-feature partition without supervised slot labels.

---

## 11. Result Files

Result directory:

`results/round1_slot_specialization_dot_product_4gpu_20260609/`

Figure directory:

`figures/round1_slot_specialization_dot_product_4gpu_20260609/`

Core tables:

- `summary_by_variant.csv`
- `final_metrics_by_seed.csv`
- `metrics_by_step.csv`
- `p2_probe_metrics_by_checkpoint.csv`
- `p3_margin_decomposition_by_checkpoint.csv`
- `p3_route_switch_table.csv`
- `route_confusion_by_step.csv`

Core figures:

- `p1_route_heatmaps.png`
- `p1_max_load_trajectory.png`
- `p1_slot_nmi_trajectory.png`
- `p2_probe_accuracy_trajectory.png`
- `p3_margin_decomposition_plots.png`
- `p5_baseline_vs_positive_control.png`

Checkpoint artifacts:

Per-seed checkpoint artifacts are stored under:

`results/round1_slot_specialization_dot_product_4gpu_20260609/dot_product/<variant>/seed_<seed>/checkpoint_artifacts/`

These are audit artifacts and should not be committed as curated Git artifacts by default.

---

## 12. Claim Boundary

Can claim:

1. In `D_min_block_shift`, vanilla dot-product sparse top-1 routing collapses despite perfect task learning.
2. Slot information is linearly decodable from `h_B`.
3. Common-component dot-product logit dominance is the strongest Round-1 logit-level mechanism.
4. Supervised slot initialization reaches perfect slot-level routing in all 8 seeds.

Cannot claim:

1. P5 is label-free.
2. P5 removes the common component.
3. P4-style expert causal utility is established.
4. The result automatically transfers to longer sequences, multi-B exact-feature routing, or real language-model settings.

---

## 13. Next Step

Use the dot-product version as the standard Round-1 result. Next test whether a label-free intervention can enter the same reachable partition.
