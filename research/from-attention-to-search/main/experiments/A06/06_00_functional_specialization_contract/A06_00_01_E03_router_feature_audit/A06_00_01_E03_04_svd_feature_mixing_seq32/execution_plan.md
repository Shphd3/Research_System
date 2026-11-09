# Execution Plan: H0522 SVD Feature Mixing Seq32

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

在 H0521b 已训练 `seq_len=32` top-1 MoE checkpoint 上，判断 prediction-position AB-dominant expert 是 feature-level specialist 还是 mixed bucket。

## 2. Data Construction

构造 balanced fixed-position eval set：

| Class | Prefix motif | Target |
|---|---|---|
| background | no A/B token | random background token |
| A-only | `[A, r]` | `y_A` |
| B-only | `[r, B]` | `y_B` |
| AB-composite | `[A, B]` | `y_AB` |

默认参数：

- `seq_len=32`
- `motif_position=15`
- `n_eval_per_class=4096`
- background tokens exclude `A/B/y_A/y_B/y_AB`

## 3. Model / Evaluation Setup

Checkpoint source:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0521b_seq32_contiguous_ab/h0521b_seq32_contiguous_ab_4gpu_20260521/
```

Analyzed model:

```text
moe_top1_no_lb
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Local run uses two visible GPUs:

```text
CUDA_VISIBLE_DEVICES=0,1
```

## 4. Configs And Commands

Command:

```bash
CUDA_VISIBLE_DEVICES=0,1 python Projects/from-attention-to-search/main/experiments/H0521_router_feature_specialization/H0522_svd_feature_mixing_seq32/scripts/analyze_h0522_svd_feature_mixing_seq32.py \
  --n-eval-per-class 4096 \
  --motif-position 15
```

## 5. Metrics And Artifacts

Primary metric:

```text
ProjectionScore(v_A, S_e), ProjectionScore(v_B, S_e), ProjectionScore(v_AB_int, S_e)
```

Decision metric:

```text
class-wise CE delta after masking AB-dominant expert
```

Artifacts:

- `tables/class_metrics.csv`
- `tables/routing_prediction_by_seed.csv`
- `tables/feature_direction_norms.csv`
- `tables/svd_projection_scores.csv` with expert, global, random matched, and permutation-label feature rows
- `tables/ab_expert_deep_dive.csv`
- `tables/expert_ablation_delta_loss.csv`
- `figures/routing_prediction_by_seed.png`
- `figures/ab_expert_projection_by_seed.png`
- `figures/ab_expert_ablation_delta_loss_by_seed.png`

## 6. Pass / Fail Criteria

Pass:

- all 4 seed checkpoints load;
- base class accuracy is high enough to make routing/function analysis meaningful;
- SVD and ablation tables are produced per seed;
- conclusion is stated per seed first, then across-seed only where stable.

Fail:

- model does not solve the task;
- `v_AB_int` norm is too small to interpret interaction projection;
- ablation delta is numerically near zero for all experts/classes.

## 7. Failure Modes To Check

- Expert id permutation across seeds: never compare raw expert id across seeds as semantic identity.
- Average routing plots: use only for overview, not main conclusion.
- `v_AB_raw` confusion: do not treat raw AB direction as interaction.
- SVD sample size: check number of samples in each expert bucket.

## 8. Result Location

```text
Projects/from-attention-to-search/main/experiments/H0521_router_feature_specialization/H0522_svd_feature_mixing_seq32/
```
