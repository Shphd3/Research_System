## 0. Quick Recap

Purpose:

Test whether the hidden common component \(c\) in the original uniform MoE toy setting is caused by fixed routed position, positional embedding, or fixed sequence template.

Hypothesis:

If fixed routed position is a causal source, then zeroing the routed position embedding should reduce \(||\text{mean}_f h_f||^2 / \text{mean}_f ||h_f||^2\) and reduce step-0 max-load before training.

Experiment logic:

Run step-0 position ablations and full 1600-step training variants on the original uniform feature distribution. Keep the feature key \((slot, B_i)\) and target token rule unchanged. For random feature position, move the contiguous slot-code, B-token, and target-token block; measure route at the logical B-token position.

Conclusion:

The result supports fixed routed position as a major causal source of the step-0 common component. Removing positional embeddings throughout training reduces final load concentration while preserving target accuracy. Random feature position weakens step-0 common geometry but does not reliably prevent final collapse.

Evidence:

`tables/p7_position_source_metrics_by_seed.csv`, `tables/p7_position_source_summary.csv`, `tables/p7_required_decision_table.csv`, and figures in `figures/`.

## 1. Run Integrity

| Item | Value |
|---|---|
| ACP job id | `pt-om3xw253` |
| ACP state | `SUCCEEDED` |
| GPU spec | `n6ls.iu.i40.4`, 4 H100-class GPUs |
| runtime log | `logs/acp/a05_03_position_template_source_ablation_4gpu_20260608_runtime_20260608_042305.log` |
| completed tasks | 24 / 24 |
| config | `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0605a_true_token_conditioned_inhibition_replay.json` |
| runner | `scripts/run_a05_03_position_template_source_ablation.py` |
| seeds | `20260521, 20260522, 20260523` |
| patterns | `repeated`, `distributed_complex` |
| train steps | 1600 |
| train samples per slot | 5000 |
| batch size | 384 |
| eval batch size | 512 |
| variants per feature key | 16 |

Repro command is recorded in `commands.sh`.

## 2. Operational Definitions

Feature key:

\[
f=(slot, B_i)
\]

Feature centroid:

\[
h_f = \mathbb{E}_{x: feature(x)=f}[h(x, route\_pos)]
\]

Common ratio:

\[
\frac{||\text{mean}_f h_f||^2}{\text{mean}_f ||h_f||^2}
\]

Step-0 max-load:

Fraction of feature centroids assigned to the most-used expert before training.

Final max-load:

Same metric after 1600 training steps.

Random feature position:

The slot-code, B-token, and target-token block is moved to variable valid positions. Target token identity remains \(Y_{slot,B_i}\), and routing is measured at the logical B-token position, not at a fixed absolute index.

## 3. Required Decision Table

| Pattern | Variant | n | common_ratio | step0_max_load | common_score_agreement | final_max_load | accuracy | Interpretation |
|---|---|---:|---:|---:|---:|---:|---:|---|
| distributed_complex | baseline_pos | 3 | 0.510 | 0.629 | 1.000 | n/a | n/a | original fixed-position step-0 geometry |
| distributed_complex | zero_all_pos_step0 | 3 | 0.035 | 0.364 | 1.000 | n/a | n/a | all-position removal gives strong step-0 reduction |
| distributed_complex | zero_routed_pos_step0 | 3 | 0.045 | 0.357 | 1.000 | n/a | n/a | routed-position removal gives strong step-0 reduction |
| distributed_complex | shuffle_pos_vectors_step0 | 3 | 0.506 | 0.503 | 1.000 | n/a | n/a | shuffling reduces load but leaves common ratio high |
| distributed_complex | random_feature_position_eval_only | 3 | 0.082 | 0.411 | 1.000 | n/a | n/a | variable position lowers step-0 common but does not fully balance |
| distributed_complex | fixed_position_baseline | 3 | 0.268 | 0.629 | 1.000 | 0.921 | 1.000 | baseline has frequent final collapse |
| distributed_complex | no_pos_frozen_train | 3 | 0.068 | 0.364 | 1.000 | 0.744 | 0.998 | no-position training reduces final load with accuracy preserved |
| distributed_complex | random_feature_position_train_eval | 3 | 0.192 | 0.411 | 1.000 | 0.766 | 1.000 | mixed; one seed still collapses |
| repeated | baseline_pos | 3 | 0.506 | 0.616 | 1.000 | n/a | n/a | original fixed-position step-0 geometry |
| repeated | zero_all_pos_step0 | 3 | 0.035 | 0.329 | 1.000 | n/a | n/a | all-position removal gives strong step-0 reduction |
| repeated | zero_routed_pos_step0 | 3 | 0.046 | 0.334 | 0.667 | n/a | n/a | routed-position removal breaks most of the step-0 common shift |
| repeated | shuffle_pos_vectors_step0 | 3 | 0.506 | 0.518 | 1.000 | n/a | n/a | shuffling reduces load but leaves common ratio high |
| repeated | random_feature_position_eval_only | 3 | 0.081 | 0.394 | 1.000 | n/a | n/a | variable position lowers step-0 common but does not fully balance |
| repeated | fixed_position_baseline | 3 | 0.299 | 0.616 | 1.000 | 0.701 | 0.997 | one seed collapses, two remain partially spread |
| repeated | no_pos_frozen_train | 3 | 0.048 | 0.329 | 0.333 | 0.432 | 0.998 | strongest final non-collapse among position variants |
| repeated | random_feature_position_train_eval | 3 | 0.290 | 0.394 | 1.000 | 1.000 | 1.000 | variable position does not prevent final collapse |

CSV: `tables/p7_required_decision_table.csv`

## 4. Experiment A: Step-0 Position Embedding Ablation

Question:

Does removing positional embedding reduce common ratio and step-0 load concentration before training?

Observation:

| Pattern | Variant | common_ratio | step0 max-load | logit-cancel max-load | cos(c, routed pos) |
|---|---|---:|---:|---:|---:|
| distributed_complex | baseline_pos | 0.510 | 0.629 | 0.286 | 0.967 |
| distributed_complex | zero_all_pos_step0 | 0.035 | 0.364 | 0.285 | n/a |
| distributed_complex | zero_routed_pos_step0 | 0.045 | 0.357 | 0.285 | n/a |
| distributed_complex | random_feature_position_eval_only | 0.082 | 0.411 | 0.284 | 0.121 |
| repeated | baseline_pos | 0.506 | 0.616 | 0.284 | 0.968 |
| repeated | zero_all_pos_step0 | 0.035 | 0.329 | 0.282 | n/a |
| repeated | zero_routed_pos_step0 | 0.046 | 0.334 | 0.281 | n/a |
| repeated | random_feature_position_eval_only | 0.081 | 0.394 | 0.278 | 0.119 |

Interpretation:

Zeroing only the routed position embedding nearly matches zeroing all position embeddings. This is direct causal evidence that the routed position embedding is a major step-0 common-source component.

Boundary:

This is a step-0 forward ablation. It does not prove that removing position embeddings solves training-time collapse.

## 5. Experiment B: Train Without Positional Embedding

Question:

If position embedding is removed throughout training, does final collapse reduce?

Observation:

| Pattern | Variant | final max-load | collapse rate | final accuracy | final common_ratio |
|---|---|---:|---:|---:|---:|
| distributed_complex | fixed_position_baseline | 0.921 | 0.667 | 1.000 | 0.268 |
| distributed_complex | no_pos_frozen_train | 0.744 | 0.000 | 0.998 | 0.068 |
| repeated | fixed_position_baseline | 0.701 | 0.333 | 0.997 | 0.299 |
| repeated | no_pos_frozen_train | 0.432 | 0.000 | 0.998 | 0.048 |

Interpretation:

No-position training reduces final load concentration in both patterns while preserving accuracy. This means the toy target rule does not require absolute position embeddings for high accuracy.

Boundary:

The distributed-complex no-position final max-load remains 0.744, so position removal is not a complete anti-collapse solution.

## 6. Experiment C: Randomize Feature Position

Question:

If the same logical feature appears at variable sequence positions, does the common component tied to fixed routed position disappear?

Observation:

| Pattern | Variant | route positions | step0 common_ratio | step0 max-load | final max-load | final accuracy |
|---|---|---:|---:|---:|---:|---:|
| distributed_complex | random_feature_position_eval_only | 26 | 0.082 | 0.411 | n/a | n/a |
| distributed_complex | random_feature_position_train_eval | 26 | 0.082 | 0.411 | 0.766 | 1.000 |
| repeated | random_feature_position_eval_only | 26 | 0.081 | 0.394 | n/a | n/a |
| repeated | random_feature_position_train_eval | 26 | 0.081 | 0.394 | 1.000 | 1.000 |

Interpretation:

Randomizing logical feature position weakens the initial common component, but it does not reliably prevent final collapse. In the repeated pattern, all three seeds end near full collapse despite perfect accuracy.

Boundary:

This result argues against a simple "fixed absolute position is the whole story" claim. It supports a narrower claim: fixed routed position is a major early common-source component, while final collapse can still emerge from training dynamics or other shared structure.

## 7. Per-Seed Final Results

| Pattern | Variant | Seed | Final max-load | Active experts | Accuracy |
|---|---|---:|---:|---:|---:|
| distributed_complex | fixed_position_baseline | 20260521 | 1.000 | 1 | 1.000 |
| distributed_complex | fixed_position_baseline | 20260522 | 1.000 | 1 | 1.000 |
| distributed_complex | fixed_position_baseline | 20260523 | 0.762 | 4 | 1.000 |
| distributed_complex | no_pos_frozen_train | 20260521 | 0.700 | 4 | 0.997 |
| distributed_complex | no_pos_frozen_train | 20260522 | 0.688 | 4 | 0.998 |
| distributed_complex | no_pos_frozen_train | 20260523 | 0.845 | 4 | 0.999 |
| distributed_complex | random_feature_position_train_eval | 20260521 | 1.000 | 1 | 1.000 |
| distributed_complex | random_feature_position_train_eval | 20260522 | 0.562 | 3 | 1.000 |
| distributed_complex | random_feature_position_train_eval | 20260523 | 0.737 | 3 | 1.000 |
| repeated | fixed_position_baseline | 20260521 | 0.600 | 3 | 1.000 |
| repeated | fixed_position_baseline | 20260522 | 1.000 | 1 | 0.990 |
| repeated | fixed_position_baseline | 20260523 | 0.505 | 3 | 1.000 |
| repeated | no_pos_frozen_train | 20260521 | 0.282 | 4 | 0.997 |
| repeated | no_pos_frozen_train | 20260522 | 0.580 | 4 | 0.999 |
| repeated | no_pos_frozen_train | 20260523 | 0.434 | 4 | 0.997 |
| repeated | random_feature_position_train_eval | 20260521 | 1.000 | 1 | 1.000 |
| repeated | random_feature_position_train_eval | 20260522 | 1.000 | 1 | 1.000 |
| repeated | random_feature_position_train_eval | 20260523 | 0.999 | 2 | 1.000 |

Full seed-level table: `tables/p7_position_source_metrics_by_seed.csv`

## 8. Figures

![Position source max-load and common ratio](figures/position_source_max_load_and_common_ratio.png)

Interpretation: position removal sharply lowers step-0 common ratio and max-load; full-training no-pos reduces final load, but random feature position is mixed.

Required route heatmaps:

```text
figures/route_heatmap_step0_baseline_*.png
figures/route_heatmap_step0_position_ablation_*.png
figures/route_heatmap_final_baseline_*.png
figures/route_heatmap_final_position_ablation_*.png
figures/route_heatmap_final_random_feature_position_*.png
```

Interpretation: heatmaps are seed-level evidence; they should be used to inspect whether load reduction is broad expert use or a different concentrated map.

## 9. Claim Update

Can claim:

- The common-source claim is now stronger: fixed routed position / positional embedding is causally implicated, not merely correlated.
- The strongest step-0 evidence is `zero_routed_pos_step0`: it reduces common ratio to about 0.045 and step-0 max-load to about 0.33-0.36.
- No-position training preserves accuracy and reduces final load concentration.

Cannot claim:

- Position embedding is the only common-source mechanism.
- Position removal solves final collapse.
- Random feature position is a reliable anti-collapse intervention.
- Load balance produced by position removal is feature specialization.

Next decision:

In the 05_03 anchor, revise the common-source statement to: "fixed routed position / positional embedding is a major causal source of step-0 common offset; final collapse remains a separate training-time phenomenon."

## 10. Artifact Map

| Artifact | Path |
|---|---|
| summary | `summary.md` |
| detailed | `detailed.md` |
| commands | `commands.sh` |
| runner | `scripts/run_a05_03_position_template_source_ablation.py` |
| ACP submitter | `scripts/submit_a05_03_position_template_source_ablation_4gpu_acp.sh` |
| run manifest | `tables/p7_position_source_run_manifest.json` |
| required table | `tables/p7_required_decision_table.csv` |
| full metrics | `tables/p7_position_source_metrics_by_seed.csv` |
| summary table | `tables/p7_position_source_summary.csv` |
| route heatmap table | `tables/p7_position_source_route_heatmap.csv` |
| runtime log | `logs/acp/a05_03_position_template_source_ablation_4gpu_20260608_runtime_20260608_042305.log` |
| figures | `figures/*.png` |
