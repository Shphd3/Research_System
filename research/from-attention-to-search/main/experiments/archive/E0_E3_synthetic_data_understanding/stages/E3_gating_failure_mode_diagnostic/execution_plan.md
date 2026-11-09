# Execution Plan: E3 Gating Failure Mode Diagnostic

## 1. Run Goal

先 smoke，再 full run。目标是输出 failure-mode attribution matrix，回答 natural top-1 router 为什么不自然按 synthetic feature label 干净分 expert。

## 2. Data Construction

全部数据使用：

```text
vocab_size = 1000
corpus_length = 1000000
feature_count = 3900 / 3900 / 3900 / 3900
```

Datasets:

| dataset | relations | purpose |
|---|---|---|
| `unique_uniform` | `[1,2]->22`, `[3,4]->23`, `[6,7]->20`, `[8,9]->21` | standard baseline |
| `shared_b_uniform` | `[1,2]->22`, `[3,2]->23`, `[6,7]->20`, `[8,7]->21` | prefix-end token shortcut control |
| `shared_target_uniform` | `[1,2]->22`, `[3,4]->22`, `[6,7]->20`, `[8,9]->20` | target-token shortcut control |
| `crossed_factorial_uniform` | `[1,2]->22`, `[1,4]->23`, `[3,2]->23`, `[3,4]->22` | crossed relation control |

## 3. Model / Training Setup

Model:

```text
1-layer causal Transformer
d_model = 64
n_heads = 4
num_experts = 4
ffn_dim = 128
seq_len = 32
```

Variants:

```text
moe_top1_no_lb
moe_top1_lb
router_aux_lam_1_0
```

Full run:

```text
steps = 10000
batch_size = 128
feature_router_batch_size = 128
lr = 0.0006
seeds = 20260513, 20260514, 20260515, 20260516, 20260517
```

Dynamics checkpoints:

```text
step = 0, 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000
```

## 4. Commands

Smoke:

```bash
python scripts/run_e3_gating_failure_modes.py --mode smoke
```

Full:

```bash
python scripts/run_e3_gating_failure_modes.py --mode full
```

## 5. Metrics And Artifacts

Main outputs:

```text
outputs/e3_gating_failure_modes/
figures/e3_gating_failure_modes/
```

Aggregated tables:

```text
aggregate/predictor_group_accuracy_table.csv
aggregate/conditional_importance_table.csv
aggregate/component_ablation_table.csv
aggregate/oracle_routing_comparison_table.csv
aggregate/early_final_agreement_table.csv
aggregate/utility_matrix_by_step.csv
aggregate/gradient_by_feature_expert_table.csv
```

Key figures:

```text
predictor_accuracy_by_group_<dataset>.png
component_ablation_readback_drop.png
nmi_over_training_steps.png
early_to_final_route_agreement.png
```

## 6. Pass / Fail Criteria

Smoke passes only if:

- crossed-factorial data generates and audits;
- `moe_top1_no_lb` and `router_aux_lam_1_0` run for 500 steps;
- predictor table is generated;
- component ablation table is generated;
- dynamics checkpoint analysis is generated.

Full run passes only if:

- all four datasets finish 3 variants x 5 seeds;
- aggregate predictor/component/dynamics tables exist;
- report figures exist;
- `summary.md` can identify strongest supported failure modes.

## 7. Failure Modes To Check

| failure mode | strongest evidence |
|---|---|
| token shortcut | token-only predictors explain expert id; shared-token controls alter routing |
| target shortcut | target-only predictor strong; shared-target pairs route similarly |
| difficulty/scale | CE/margin/norm predictors strong |
| expert utility degeneracy | many experts have similar forced utility for same feature |
| shared-path bypass | zero MoE drop small relative to other component drops |
| early lock-in | early route assignment agrees with final |
| objective insufficiency | supervised router clean while natural router not clean |

## 8. Result Location

Mainline-safe reports:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E3_gating_failure_mode_diagnostic/
```

Ignored run workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```
