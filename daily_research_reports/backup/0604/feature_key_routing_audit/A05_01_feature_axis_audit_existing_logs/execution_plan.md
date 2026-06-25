# Execution Plan: H0604b Feature-Axis Audit On Existing Logs

Anchor:

```text
../../problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md
```

Approved protocol:

```text
protocol_for_approval.md
```

Run status:

```text
completed
```

GPU status:

```text
not submitted to 4-GPU queue because H0604b is analysis-only on existing H0604a logs
```

## 1. Run Goal

本实验只回答一个决策问题：

> 当前 H0604a 中所谓 `feature` 到底更像是 `slot`、$B_i$，还是 `(slot,B_i)`？

这是 analysis-only，不重新训练，不需要 GPU。完整实验使用 H0604a 已有 route matrix logs。

## 2. Data / Material

Input raw result dir:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0604a_feature_key_routing_stability_center_only/h0604a_feature_key_routing_stability_4gpu_20260603/
```

Primary input file:

```text
feature_key_route_matrix.csv
```

Required columns:

```text
step, slot, b_idx, expert, count, fraction, main_expert, consistency,
mode, condition, seed
```

This file stores counts for exact feature `(slot,b_idx)` by expert. The audit reconstructs coarser labels by aggregation:

```text
slot: sum over b_idx
B_i: sum over slot
slot+B_i: original exact feature rows
```

## 3. Procedure

For each `condition / seed / step`:

1. load exact `(slot,b_idx) × expert` count matrix;
2. aggregate into three feature definitions:
   - `slot`;
   - `b_id`;
   - `slot_b_id`;
3. for each feature definition compute:
   - feature × expert matrix;
   - per-feature consistency $\max_e P(e\mid f)$;
   - mean consistency over features;
   - fraction with consistency $\ge 0.95$ and $\ge 0.99$;
   - `NMI(route; feature)`;
4. compute expert load:
   - load entropy norm;
   - max load fraction;
   - active experts;
5. apply collapse filters:

```text
strict collapse: active_experts <= 1 or max_load == 1
near collapse: max_load >= 0.95 or load_entropy_norm < 0.2
primary filtered read: active_experts > 1 and max_load < 0.95 and load_entropy_norm >= 0.2
```

6. choose branch:

| Branch | Condition |
|---|---|
| 2A | `slot_b_id` consistency is not stable after collapse filtering |
| 2B | `slot_b_id` stable but `slot` is weak / much lower than `slot_b_id` |
| 2C | `slot_b_id` stable and non-collapsed, with clear `slot` or `slot_b_id` structure |

## 4. Required Figures

| Figure | File | Question answered |
|---|---|---|
| feature × expert heatmap | `figures/feature_expert_heatmap_slot.png`, `feature_expert_heatmap_b_id.png`, `feature_expert_heatmap_slot_b_id.png` | Does each feature concentrate on one expert? |
| consistency bar plot | `figures/feature_axis_consistency_comparison.png` | Which feature definition has highest consistency: `slot`, $B_i$, or `slot+B_i`? |
| expert load histogram | `figures/expert_load_histogram.png` | Are results explained by all-to-one / near-all-to-one collapse? |
| NMI bar plot | `figures/feature_axis_nmi_comparison.png` | Which label has most route information: `slot`, $B_i$, or `slot+B_i`? |

Additional figure:

```text
figures/feature_axis_checkpoint_drift.png
```

This checks whether the dominant feature axis changes across step 0 / 800 / 1600.

## 5. Required Tables

```text
tables/feature_axis_consistency_by_condition.csv
tables/feature_axis_consistency_by_seed.csv
tables/feature_axis_nmi_by_condition.csv
tables/feature_expert_matrix_slot.csv
tables/feature_expert_matrix_b_id.csv
tables/feature_expert_matrix_slot_b_id.csv
tables/per_expert_composition_slot.csv
tables/per_expert_composition_b_id.csv
tables/per_expert_composition_slot_b_id.csv
tables/collapse_filtered_branch_decision.csv
```

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
|---|---|---|---|---|---|
| Input audit | Are H0604a route counts sufficient? | `feature_key_route_matrix.csv` columns | Pass if exact `(slot,b_idx) × expert` counts exist for all conditions/seeds/steps | `tables/input_audit.csv` | Continue analysis |
| Aggregation | Can three feature axes be reconstructed? | Aggregated count matrices | Pass if each axis has nonzero rows and expected feature count | feature matrix tables | Compute metrics |
| Collapse guard | Are valid seeds available? | load entropy / max load | Pass if at least one non-collapsed seed exists for key comparisons | `collapse_filtered_branch_decision.csv` | Branch decision |
| Figure generation | Are central visuals present? | PNG files | Pass if all four required plot families are generated and nonempty | `figures/` | Write summary/detailed |

## 7. Pass / Fail Criteria

Success:

The experiment succeeds if it assigns the evidence to exactly one branch:

1. `2A`: exact `(slot,B_i)` unstable after filtering;
2. `2B`: exact feature stable but slot unstable;
3. `2C`: exact feature stable and non-collapsed, with interpretable slot or slot+B_i structure.

Failure:

The current line is weakened if all non-collapsed seed-condition pairs have low consistency for all three feature definitions, or if all high-scoring cases are collapse.

Insufficient evidence:

The result is insufficient if the route matrix does not support reconstruction of feature labels, if too many seeds collapse for any branch decision, or if NMI and consistency disagree without readable feature × expert matrices.

## 8. Result Location

Research record:

```text
Projects/from-attention-to-search/main/experiments/A05/A05_01_feature_axis_audit_existing_logs/
```

Expected outputs:

```text
summary.md
detailed.md
tables/
figures/
```

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Runner:

```text
scripts/analyze_h0604b_feature_axis_audit.py
```
