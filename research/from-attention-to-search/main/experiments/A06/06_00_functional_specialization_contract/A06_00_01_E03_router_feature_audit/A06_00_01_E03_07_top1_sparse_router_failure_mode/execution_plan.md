# Execution Plan: H0526 Top-1 Sparse Router Failure Mode

Hypothesis purpose card:

The legacy purpose card was removed; this execution record is retained for
historical audit.

## 1. Run Goal

Implement and test a trainable top-1 sparse MoE router:

```text
router logits -> softmax -> selected top-1 probability and index -> one active expert per token -> output = selected_prob * selected_expert_output
```

The run decides whether sparse selected-gate routing forms functional expert specialization, or instead shows collapse / route-function mismatch / unstable specialization.

## 2. Data Construction

Use the same AB/CB setup as H0525a:

```text
A-only:       [A, r] -> y_A
B-only:       [r, B] -> y_B
AB-composite: [A, B] -> y_AB
CB-composite: [C, B] -> y_CB
background:   random background -> random background target
```

## 3. Model / Training / Evaluation Setup

Conditions:

| Condition | Model | Role |
|---|---|---|
| C0 | `hard_top1_no_gate` | negative control for gradient audit |
| C1 | `top1_selected_gate` | primary full run |

Training:

```text
steps: 1600
batch size: 384
lr: 0.0008
weight decay: 0.01
seeds: 20260521, 20260522, 20260523, 20260524
experts: 4
load balance: none
```

## 4. Configs And Commands

Config:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0526_top1_sparse_router_failure_mode.json
```

Runner:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0526_top1_sparse_router_failure_mode.py
```

Audit:

```bash
cd XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
CUDA_VISIBLE_DEVICES=1 python scripts/run_h0526_top1_sparse_router_failure_mode.py \
  --config configs/h0526_top1_sparse_router_failure_mode.json \
  --run-name h0526_top1_sparse_router_failure_mode_audit_20260524b \
  --run-stage smoke \
  --audit-only
```

Full:

```bash
cd XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
python scripts/run_h0526_top1_sparse_router_failure_mode.py \
  --config configs/h0526_top1_sparse_router_failure_mode.json \
  --run-name h0526_top1_sparse_router_failure_mode_10109_20260524 \
  --run-stage full \
  --parallel
```

## 5. Metrics And Artifacts

Primary validity metric:

```text
router grad > 0 and active experts per token = 1
```

Primary research metric:

```text
class x expert cross-entropy ablation delta
```

AB-specificity:

\[
S_{AB}
=
\max_e
\left[
\Delta L_{AB,e}
-
\max
\left(
\Delta L_{A,e},
\Delta L_{B,e},
\Delta L_{CB,e}
\right)
\right].
\]

Required artifacts:

```text
tables/gradient_audit.csv
tables/class_metrics_by_seed.csv
tables/load_entropy_by_seed.csv
tables/ablation_delta_class_expert.csv
figures/class_expert_ablation_delta_heatmap.png
```

## 6. Pass / Fail Criteria

If C1 gradient audit fails, stop and fix implementation.

If task accuracy is low, interpret as sparse optimization failure.

If task accuracy is high but no stable class-specific ablation appears, interpret as route-function mismatch / unstable specialization.

If load entropy is very low and one expert dominates, interpret as expert collapse.

## 7. Failure Modes To Check

- router gradient still zero;
- active expert count greater than one;
- full soft-mixture accidentally used;
- task not learned;
- expert load collapse;
- routing structure without functional ablation support;
- B-only / AB split without functional meaning.

## 8. Result Location

Curated result:

```text
main/experiments/H0521_router_feature_specialization/H0526_top1_sparse_router_failure_mode/
```

Remote raw result dir:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/h0526_top1_sparse_router_failure_mode/h0526_top1_sparse_router_failure_mode_10109_20260524
```
