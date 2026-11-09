# A05_03 Position / Template Source Ablation Summary

## 0. Verdict

Fixed routed position is a causal source of the step-0 common hidden component: zeroing the routed position embedding reduces common ratio from about 0.51 to about 0.045 and lowers step-0 max-load from about 0.62 to about 0.33-0.36. Removing positional embeddings throughout training also reduces final load collapse while preserving target accuracy, but randomizing feature position does not reliably prevent final collapse.

## 1. Setup

Question: is the common component \(c\) caused by fixed routed position, positional embedding, or fixed sequence template?

Run: 4GPU ACP job `pt-om3xw253`, status `SUCCEEDED`.

Seeds: `20260521, 20260522, 20260523`.

Patterns: `repeated`, `distributed_complex`.

Training: full 1600 steps, batch size 384, train samples per slot 5000, variants per key 16.

Main variants:

- step-0: `baseline_pos`, `zero_all_pos_step0`, `zero_routed_pos_step0`, `shuffle_pos_vectors_step0`, `random_feature_position_eval_only`;
- full training: `fixed_position_baseline`, `no_pos_frozen_train`, `random_feature_position_train_eval`.

## 2. Decision Table

| Pattern | Variant | common_ratio | step0_max_load | common_score_agreement | final_max_load | accuracy | Interpretation |
|---|---|---:|---:|---:|---:|---:|---|
| distributed_complex | baseline_pos | 0.510 | 0.629 | 1.000 | n/a | n/a | original fixed-position step-0 geometry |
| distributed_complex | zero_routed_pos_step0 | 0.045 | 0.357 | 1.000 | n/a | n/a | routed position embedding is a causal step-0 source |
| distributed_complex | zero_all_pos_step0 | 0.035 | 0.364 | 1.000 | n/a | n/a | all-position removal gives similar step-0 reduction |
| distributed_complex | random_feature_position_eval_only | 0.082 | 0.411 | 1.000 | n/a | n/a | variable route position reduces common but not as much as zero-pos |
| distributed_complex | fixed_position_baseline | 0.268 | 0.629 | 1.000 | 0.921 | 1.000 | final collapse remains frequent |
| distributed_complex | no_pos_frozen_train | 0.068 | 0.364 | 1.000 | 0.744 | 0.998 | position removal lowers final load with accuracy preserved |
| distributed_complex | random_feature_position_train_eval | 0.192 | 0.411 | 1.000 | 0.766 | 1.000 | helps relative to baseline but still has one collapsed seed |
| repeated | baseline_pos | 0.506 | 0.616 | 1.000 | n/a | n/a | original fixed-position step-0 geometry |
| repeated | zero_routed_pos_step0 | 0.046 | 0.334 | 0.667 | n/a | n/a | routed position removal breaks most of the step-0 common shift |
| repeated | zero_all_pos_step0 | 0.035 | 0.329 | 1.000 | n/a | n/a | all-position removal gives similar step-0 reduction |
| repeated | random_feature_position_eval_only | 0.081 | 0.394 | 1.000 | n/a | n/a | variable route position reduces common but does not erase load concentration |
| repeated | fixed_position_baseline | 0.299 | 0.616 | 1.000 | 0.701 | 0.997 | one seed collapses, two remain partially spread |
| repeated | no_pos_frozen_train | 0.048 | 0.329 | 0.333 | 0.432 | 0.998 | strongest non-collapse result among position variants |
| repeated | random_feature_position_train_eval | 0.290 | 0.394 | 1.000 | 1.000 | 1.000 | random feature position does not prevent training-time collapse here |

Full CSV: `tables/p7_required_decision_table.csv`.

## 3. Figures

![Position source max-load and common ratio](figures/position_source_max_load_and_common_ratio.png)

Interpretation: removing position embeddings sharply reduces step-0 common ratio and max-load; full-training no-pos reduces final load, while random feature position is mixed.

Required per-seed route heatmaps are in `figures/`:

- `route_heatmap_step0_baseline_*`
- `route_heatmap_step0_position_ablation_*`
- `route_heatmap_final_baseline_*`
- `route_heatmap_final_position_ablation_*`
- `route_heatmap_final_random_feature_position_*`

## 4. Conclusions For Meeting Brief

Question 1: did we causally identify the step-0 common source?

Conclusion: yes for routed position embedding as a major causal source. Zeroing only the routed position embedding reduces common ratio from about 0.51 to about 0.045 and lowers step-0 max-load from about 0.62 to about 0.33-0.36.

Question 2: is the fixed sequence template the only source?

Conclusion: no. Randomizing the feature block position reduces step-0 common ratio to about 0.081-0.082, but not to the all-zero-position level, and final repeated-pattern training still collapses. Position is a major source, but training dynamics and non-position common structure remain.

Question 3: can we remove positional embeddings without destroying the toy task?

Conclusion: yes in this toy setting. `no_pos_frozen_train` keeps final accuracy near 0.998 and reduces final max-load relative to baseline in both patterns.

Question 4: does this solve collapse?

Conclusion: no. No-pos reduces collapse, but distributed-complex final max-load remains 0.744 on average; random feature position has a repeated-pattern final max-load near 1.0. The result isolates a source of early common offset, not a complete anti-collapse mechanism.

## 5. Claim Boundary

Can claim:

- fixed routed position / positional embedding is a major causal source of the step-0 common component;
- zeroing routed position and zeroing all positions produce similar step-0 reductions;
- no-position full training preserves target accuracy in this toy task and reduces final load concentration;
- randomizing feature position weakens step-0 common geometry but is not sufficient to prevent final collapse.

Cannot claim:

- position embedding is the only source of common shift;
- position ablation solves final collapse;
- random feature position is a clean anti-collapse method;
- load balance after position removal equals feature specialization.

## 6. Next Decision

Use no-position and routed-position-zero diagnostics as the causal-source control for the common-offset claim; do not move to anti-lockin interpretation until the position-source result is incorporated into the 05_03 anchor boundary.
