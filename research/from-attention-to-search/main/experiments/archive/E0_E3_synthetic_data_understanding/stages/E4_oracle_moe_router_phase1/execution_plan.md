# Execution Plan: E4 Oracle-MoE Router Phase 1

## 1. Run Goal

完成两个连续阶段：

1. 训练 C0-C4 五种 Oracle-MoE router。
2. 加载 checkpoint 做 D0-D7 router behavior diagnostic。

本阶段不做 Reverse Index。

## 2. Data Construction

使用 existing `unique_uniform` synthetic trigram 数据：

```text
data_config = e3_gating_failure_modes_data.json
data_dir = data_e3_gating_failure_modes/
regime = unique_uniform
features = ABC / DEF / GHI / JKL
relations = [1,2]->22, [3,4]->23, [6,7]->20, [8,9]->21
```

## 3. Model / Training / Evaluation Setup

固定模型：

```text
1-layer Transformer + 1 Oracle-MoE block
gate_input = attention_output
expert_input = original_hidden / residual entering MoE
full attention
seq_len = 32
d_model = 64
n_heads = 4
num_experts = 4
expert_ffn_dim = 128
```

训练：

```text
steps = 10000
batch_size = 128
lr = 0.0006
weight_decay = 0.01
grad_clip = 1.0
seeds = 20260513,20260514,20260515,20260516,20260517
```

Variants：

```text
C0 standard_oracle_linear
C1 fixed_parameter_center
C2 trainable_center_repulsion
C3 inhibition_margin
C4 center_inhibition
```

## 4. Configs And Commands

Workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
```

Config:

```text
configs/e4_oracle_moe_router_phase1.json
```

Local smoke:

```bash
python scripts/run_oracle_moe_router_phase1.py \
  --config configs/e4_oracle_moe_router_phase1.json \
  --mode smoke \
  --steps 200 \
  --device cuda

python scripts/run_oracle_moe_router_behavior_diagnostic.py \
  --config configs/e4_oracle_moe_router_phase1.json \
  --mode smoke \
  --device cuda
```

ACP training dry-run:

```bash
bash scripts/submit_oracle_moe_phase1_4gpu_acp.sh
```

ACP training submit:

```bash
ORACLE_MOE_PHASE1_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_phase1_4gpu_acp.sh
```

ACP diagnostic submit after checkpoints exist:

```bash
ORACLE_MOE_DIAGNOSTIC_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_behavior_diagnostic_4gpu_acp.sh
```

## 5. Metrics And Artifacts

Training outputs per `(variant, seed)`:

```text
checkpoint.pt
training_logs.jsonl
model_sanity.json
metrics_summary.csv
feature_expert_contingency.csv
expert_load.csv
router_confidence.csv
center_cosine_matrix.csv
assigned_representation_geometry.csv
utility_matrix_ce.csv
utility_matrix_target_prob.csv
inhibition_diagnostics.csv
```

Diagnostic outputs:

```text
sanity_check.md
router_cell_exemplars.csv
router_cell_exemplar_summary.md
expert_cell_composition.csv
expert_factor_mi.csv
counterfactual_route_flip.csv
counterfactual_route_flip_summary.md
boundary_walk.csv
boundary_walk_summary.md
common_direction_removal.csv
common_direction_removal_summary.md
expert_utility_alignment.csv
utility_matrix_ce.csv
utility_matrix_target_prob.csv
inhibition_diagnostics.csv
analysis.md
```

## 6. Pass / Fail Criteria

Smoke passes only if:

- `model_sanity.json` confirms `gate_input=attention_output`;
- `expert_input=original_hidden`;
- C2 center gradients are nonzero;
- C3 inhibition losses are finite;
- no NaN/OOM/Traceback;
- core CSVs and figures exist.

Full run is interpretable only if:

- all C0-C4 have at least one successful seed;
- diagnostic `analysis.md` exists;
- utility matrix and feature-expert contingency are both available;
- result interpretation does not rely on NMI alone.

## 7. Failure Modes To Check

- gate/expert input accidentally mixed;
- hard top-1 router receives too little NTP gradient;
- center separation succeeds geometrically but not semantically;
- inhibition creates exclusivity while harming NTP;
- all experts remain functionally redundant;
- router follows token/target/common geometry rather than planted feature.

## 8. Result Location

Ignored workspace:

```text
outputs/oracle_moe_router_phase1_20260519/
outputs/router_behavior_diagnostic_20260519/
figures/oracle_moe_router_phase1_20260519/
figures/router_behavior_diagnostic_20260519/
logs/acp/
```

Mainline-safe result, after completion:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E4_oracle_moe_router_phase1/summary.md
main/experiments/E0_E3_synthetic_data_understanding/stages/E4_oracle_moe_router_phase1/detailed.md
```
