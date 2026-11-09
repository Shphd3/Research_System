# Execution Plan: E4.1 Raw-Attention Shortcut-Controlled Oracle-MoE

## 1. Run Scope

本轮和 E4 主实验一起 full run。所有模型使用：

```text
gate_input = raw attention_output
expert_input = original hidden / residual
num_layers = 1
num_experts = 4
seq_len = 32
d_model = 64
n_heads = 4
ffn_dim = 128
batch_size = 128
steps = 10000
seeds = 20260513-20260517
```

## 2. Datasets

数据来自：

```text
configs/e3_gating_failure_modes_data.json
data_e3_gating_failure_modes/
```

本轮控制数据：

| config | regime | feature construction |
|---|---|---|
| `configs/e4_1_raw_attn_shared_b_uniform_c0_c7.json` | `shared_b_uniform` | `[1,2]->22`, `[3,2]->23`, `[6,7]->20`, `[8,7]->21` |
| `configs/e4_1_raw_attn_shared_target_uniform_c0_c7.json` | `shared_target_uniform` | `[1,2]->22`, `[3,4]->22`, `[6,7]->20`, `[8,9]->20` |
| `configs/e4_1_raw_attn_crossed_factorial_uniform_c0_c7.json` | `crossed_factorial_uniform` | `[1,2]->22`, `[1,4]->23`, `[3,2]->23`, `[3,4]->22` |

对照 E4 主数据：

```text
configs/e4_raw_attn_dingyi_oracle_init.json
regime = unique_uniform
```

## 3. Variants

训练 C0-C7 全部 variants：

```text
C0 C1 C2 C3 C4 C5 C6 C5-noLB C6-noLB C7a C7b C7c C7d C7e
```

C7 系列使用 Dingyi-style warmup + center initialization family，但保持本项目 Oracle-MoE 可比设置：

```text
router input = raw attention_output
expert input = residual hidden
```

## 4. Submission

训练任务：

```bash
CONFIG_PATHS="configs/e4_raw_attn_dingyi_oracle_init.json configs/e4_1_raw_attn_shared_b_uniform_c0_c7.json configs/e4_1_raw_attn_shared_target_uniform_c0_c7.json configs/e4_1_raw_attn_crossed_factorial_uniform_c0_c7.json" \
RUN_NAME="oracle_moe_raw_attn_c0_c7_e41_full_20260519" \
JOB_NAME="ats-oracle-moe-raw-c0c7-e41-full-4gpu" \
ORACLE_MOE_MULTI_PHASE1_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_multi_config_phase1_4gpu_acp.sh
```

诊断任务在训练完成后提交：

```bash
CONFIG_PATHS="configs/e4_raw_attn_dingyi_oracle_init.json configs/e4_1_raw_attn_shared_b_uniform_c0_c7.json configs/e4_1_raw_attn_shared_target_uniform_c0_c7.json configs/e4_1_raw_attn_crossed_factorial_uniform_c0_c7.json" \
RUN_NAME="router_behavior_raw_attn_c0_c7_e41_full_20260519" \
JOB_NAME="ats-oracle-moe-raw-c0c7-e41-diag-4gpu" \
ORACLE_MOE_MULTI_DIAGNOSTIC_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_multi_config_diagnostic_4gpu_acp.sh
```

资源规则：单任务只申请 4 卡，不设置 `QUOTA_TYPE=spot`。

## 5. Metrics

每个 `(dataset, variant, seed)` 汇总：

- NTP loss；
- feature readback probability；
- $P(\mathrm{expert}\mid\mathrm{feature})$；
- expert load；
- router confidence / entropy；
- center cosine matrix；
- forced-routing utility matrix；
- router-selected expert 是否等于 best forced expert；
- D* boundary-feature alignment；
- router boundary SVD band energy；
- common direction removal 后 NMI 变化。

## 6. Pass / Fail Logic

强支持 relation-level functional specialization 需要同时满足：

1. readback 高；
2. feature assignment clean；
3. router boundary 与 feature direction 对齐；
4. forced-routing utility matrix 近似 diagonal；
5. 在 shared / crossed 控制数据中仍稳定。

如果只满足 readback，但 routing / utility 不 clean，则说明模型会做任务，但没有 one-feature-one-expert。

如果 unique 成功、shortcut control 失败，则说明 unique 中的 feature routing 主要依赖 token / target shortcut。

## 7. Artifacts

训练输出在 ignored workspace：

```text
outputs/oracle_moe_raw_attn_dingyi_c7_20260519/
outputs/e4_1_raw_attn_shortcut_controls/*/oracle_moe_raw_attn_c0_c7_20260519/
figures/oracle_moe_raw_attn_dingyi_c7_20260519/
figures/e4_1_raw_attn_shortcut_controls/*/oracle_moe_raw_attn_c0_c7_20260519/
```

诊断输出：

```text
outputs/router_behavior_raw_attn_dingyi_c7_20260519/
outputs/e4_1_raw_attn_shortcut_controls/*/router_behavior_raw_attn_c0_c7_20260519/
```

汇报结果复制到：

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E4_oracle_moe_router_phase1/
```
