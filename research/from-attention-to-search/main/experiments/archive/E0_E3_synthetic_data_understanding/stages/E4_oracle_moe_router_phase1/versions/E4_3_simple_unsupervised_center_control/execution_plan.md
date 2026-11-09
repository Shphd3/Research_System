# Execution Plan: E4.3 Simple Unsupervised Center Control

## 1. Run Scope

只跑两个新 variants：

| variant | center init | loss |
|---|---|---|
| U1 | random token-position KMeans | C7d loss: NTP + attract + score inhibition + homeostasis |
| U2 | random token-position KMeans | C7e loss: NTP + performance loss |

O1/O2 不重跑，直接引用已有 uniform C7d/C7e oracle-init 结果。

## 2. Config

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/e4_3_simple_unsup_center_uniform.json
```

Key settings:

```text
dataset = unique_uniform
steps = 10000
batch_size = 128
seeds = 20260513,20260514,20260515
gate_input = raw attention_output
expert_input = original hidden / residual
random_position_sample_size = 100000
performance_loss_extra_forward = num_experts = 4
```

## 3. Commands

Training:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
CONFIG_PATH=configs/e4_3_simple_unsup_center_uniform.json \
RUN_NAME=e4_3_unsup_center_uniform_train_20260520 \
JOB_NAME=ats-e4-3-unsup-center-uniform-4gpu \
VARIANTS="U1 U2" \
SEEDS="20260513 20260514 20260515" \
ORACLE_MOE_PHASE1_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_phase1_4gpu_acp.sh
```

Diagnostic:

```bash
CONFIG_PATH=configs/e4_3_simple_unsup_center_uniform.json \
RUN_NAME=e4_3_unsup_center_uniform_diag_20260520 \
JOB_NAME=ats-e4-3-unsup-center-uniform-diag-4gpu \
VARIANTS="U1 U2" \
SEEDS="20260513 20260514 20260515" \
ORACLE_MOE_DIAGNOSTIC_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_behavior_diagnostic_4gpu_acp.sh
```

## 4. Metrics

Compare U1/U2 against existing O1/O2:

| metric | meaning |
|---|---|
| `readback_accuracy` | feature prefix 下 target probability 是否超过 0.5 |
| `feature_expert_NMI` | feature label 与 expert assignment 的一致性 |
| `router_selects_best_expert_rate` | router 选中 expert 是否为 forced-routing CE 最低 expert |
| `selected_minus_best_CE` | router 选中 expert 比 best expert 差多少 |
| `feature_boundary_alignment` | router boundary 与 feature centroid difference 的平均对齐 |
| `top_shared_energy` | boundary 是否主要落在 common/high-variance directions |
| `expert_load_entropy` | expert allocation 是否 collapse |
| `dead_expert_count` | 未使用 expert 数量 |

## 5. Output Contract

Running outputs:

```text
outputs/e4_3_simple_unsup_center_uniform/
outputs/e4_3_simple_unsup_center_uniform_diagnostic/
figures/e4_3_simple_unsup_center_uniform/
figures/e4_3_simple_unsup_center_uniform_diagnostic/
```

Mainline-safe outputs:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E4_oracle_moe_router_phase1/versions/E4_3_simple_unsupervised_center_control/
  summary.md
  detailed.md
  figures/
```

Required figures:

```text
unsup_vs_oracle_core_metrics.png
unsup_vs_oracle_feature_expert_heatmap.png
unsup_vs_oracle_boundary_energy.png
```

## 6. Pass / Fail Logic

- If U1/U2 approach O1/O2 on NMI, readback, selected-best, and no collapse: random-position unsupervised KMeans is enough.
- If U1/U2 readback succeeds but NMI drops: oracle feature-prefix init is the main source of feature-aligned routing.
- If U2 selected-best succeeds but NMI drops: utility routing does not imply one-feature-one-expert.
- If U1/U2 collapse: random-position KMeans does not stabilize allocation.
