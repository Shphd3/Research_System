# Execution Plan: E4.2 Zipf Raw-Attention Oracle-MoE

## 1. Config

```text
configs/e4_zipf_raw_attn_c0_c7.json
```

数据：

```text
data_config = e1_all_trigram_v1000.json
data_dir = ../data_all_trigram_v1000
regime = four_feature_all_trigram_v1000
```

## 2. Model

```text
gate_input = raw attention_output
expert_input = original hidden / residual
num_layers = 1
num_experts = 4
seq_len = 32
d_model = 64
n_heads = 4
ffn_dim = 128
```

## 3. Training

```text
steps = 10000
batch_size = 128
lr = 0.0006
weight_decay = 0.01
seeds = 20260513-20260517
```

Variants:

```text
C0 C1 C2 C3 C4 C5 C6 C5-noLB C6-noLB C7a C7b C7c C7d C7e
```

## 4. Submission

训练：

```bash
CONFIG_PATHS="configs/e4_zipf_raw_attn_c0_c7.json" \
RUN_NAME="oracle_moe_zipf_raw_attn_c0_c7_full_20260519" \
JOB_NAME="ats-oracle-moe-zipf-raw-c0c7-full-4gpu" \
ORACLE_MOE_MULTI_PHASE1_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_multi_config_phase1_4gpu_acp.sh
```

诊断：

```bash
CONFIG_PATHS="configs/e4_zipf_raw_attn_c0_c7.json" \
RUN_NAME="router_behavior_zipf_raw_attn_c0_c7_full_20260519" \
JOB_NAME="ats-oracle-moe-zipf-raw-c0c7-diag-4gpu" \
ORACLE_MOE_MULTI_DIAGNOSTIC_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_oracle_moe_multi_config_diagnostic_4gpu_acp.sh
```

## 5. Metrics

和 E4 / E4.1 一致，同时额外按 feature frequency 分析：

- high-frequency features: ABC / DEF；
- low-frequency features: GHI / JKL；
- per-feature readback；
- per-feature routing entropy；
- per-feature dominant expert rate；
- per-feature selected-best expert rate；
- low-frequency feature utility gap。

## 6. Result Record

The surviving `summary.md`, `detailed.md`, and `figures/` in this experiment
folder own the Zipf result.
