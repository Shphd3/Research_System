# Execution Plan: E4 Raw-Attention Dingyi-Style Oracle Init

## 1. Scope

本轮先不跑 Reverse Index，不做 shortcut controls。只在 `unique_uniform` 上验证 raw attention-output Oracle-MoE。

实验分两组：

```text
C0-C6 = 我们原来的 C-series 机制，但全部改为 raw attn_out routing
C7   = 完全按 Dingyi oracle-init prototype router 流程做可比实现
```

旧 E4-LN 结果只作为 legacy reference；本轮报告必须标明：

```text
old E4 = LN(attention_output)
new E4 = raw attention_output
```

## 2. Code And Config

Workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Training script:

```text
scripts/run_oracle_moe_router_phase1.py
```

Config:

```text
configs/e4_raw_attn_dingyi_oracle_init.json
```

Output:

```text
outputs/oracle_moe_raw_attn_dingyi_c7_20260519/
figures/oracle_moe_raw_attn_dingyi_c7_20260519/
```

## 3. Oracle-MoE Definition

For every variant:

```text
attention_output = Attention(LN(x0))
expert_input     = x0 + attention_output
gate_input       = attention_output
router_input     = attention_output
```

There is no router LayerNorm in this new config:

```text
router_input_norm = raw
router_has_layernorm = false
```

Sanity file must confirm:

```text
router_logits_input = raw_attention_output
router_has_layernorm = false
```

## 4. Dingyi-Style Prototype Router

For C7 variants:

$$
s_{t,e}
=
\tau \cdot
\cos(z_t, c_e)
b_e
$$

where:

```text
z_t = raw attention_output at token t
c_e = expert center / prototype
tau = 5.0, matching Dingyi temperature T=0.2
b_e = trainable prototype bias
```

Top-1 routing:

$$
e^* = \arg\max_e s_{t,e}
$$

## 5. Oracle Center Initialization

For each seed:

1. Train raw-attention linear warmup for `1000` steps.
2. Collect raw-attention router inputs at feature prefix-end positions.
3. Normalize vectors.
4. Run KMeans with `k=4`, `steps=25`.
5. Save centers and audit:

```text
oracle_center_kmeans_nmi
oracle_center_kmeans_purity
oracle_center_cluster_counts
```

The centers initialize C7b/C7c/C7d/C7e.

## 6. Variants

### 6.1 Our C-Series, Raw Attention

这些是我们原来的 C0-C6，只改变 router input：从旧 `LN(attention_output)` 改成 raw `attention_output`。

| ID | Name | Definition |
|---|---|---|
| C0 | `standard_oracle_linear_raw_attn` | raw-attn linear router with LB |
| C1 | `fixed_parameter_center_raw_attn` | fixed parameter-center router |
| C2 | `trainable_center_repulsion_raw_attn` | trainable center + repulsion |
| C3 | `inhibition_margin_raw_attn` | old CE-margin inhibition |
| C4 | `center_inhibition_raw_attn` | center + old CE-margin inhibition |
| C5 | `linear_clean_expert_inhibition_raw_attn` | linear + clean expert inhibition |
| C6 | `center_clean_expert_inhibition_raw_attn` | center + clean expert inhibition |
| C5-noLB | `linear_clean_expert_inhibition_raw_attn_no_lb` | no-LB ablation |
| C6-noLB | `center_clean_expert_inhibition_raw_attn_no_lb` | no-LB ablation |

### 6.2 Dingyi-Style C7, Raw Attention

C7 follows Dingyi's oracle-init prototype-router logic, with only the surrounding model kept comparable to our Oracle-MoE setting.

| ID | Name | Definition |
|---|---|---|
| C7a | `dingyi_random_prototype_raw_attn` | warm-start model, random prototype centers |
| C7b | `dingyi_frozen_oracle_router_raw_attn` | KMeans centers, centers frozen |
| C7c | `dingyi_oracle_init_raw_attn` | KMeans centers, centers trainable |
| C7d | `dingyi_oracle_init_inhibition_raw_attn` | C7c + attraction + score-margin inhibition + homeostasis |
| C7e | `dingyi_oracle_init_performance_raw_attn` | C7c + performance-gated router feedback + homeostasis |

## 7. Losses

All variants use NTP loss:

$$
L_{\text{NTP}}
=
\mathrm{CE}(\text{LM logits}, y)
$$

C0-C4/C5/C6 use their original coefficients from our E4 setting, but with raw `attention_output`.

C0 uses LB:

$$
L = L_{\text{NTP}} + 0.01 L_{\text{LB}}
$$

C7a/C7b/C7c follow Dingyi control style:

$$
L = L_{\text{NTP}}
$$

C7d follows Dingyi inhibition:

$$
L =
L_{\text{NTP}}
+0.05L_{\text{attract}}
+0.05L_{\text{score-inhibit}}
+0.1L_{\text{homeostasis}}
$$

where:

$$
L_{\text{attract}}
=
1-\cos(z_t,c_{e^*})
$$

$$
L_{\text{score-inhibit}}
=
\max(0,\ m+\max_{e\neq e^*}s_{t,e}-s_{t,e^*})
$$

C7e follows Dingyi performance-gated feedback:

$$
L =
L_{\text{NTP}}
+0.05L_{\text{homeostasis}}
+0.1L_{\text{performance-gate}}
$$

`performance-gate` uses detached per-expert CE to choose the best expert as router target. It trains the router, not loser experts.

## 8. Run Parameters

```text
steps = 10000
warmup_steps = 1000
batch_size = 128
seq_len = 32
d_model = 64
n_heads = 4
ffn_dim = 128
num_experts = 4
seeds = [20260513, 20260514, 20260515, 20260516, 20260517]
```

## 9. Metrics

Core:

```text
readback_accuracy_p_gt_0_5
feature-expert NMI
expert load entropy / dead expert count
router confidence
center cosine matrix
oracle center KMeans NMI / purity
expert utility matrix
router_selects_best_expert_rate
utility_gap_ce
boundary-feature alignment
SVD band energy
```

## 10. Acceptance Before Full Run

Before full run, user confirms this setting.

After implementation but before run:

```text
python -m py_compile scripts/run_oracle_moe_router_phase1.py
python -m json.tool configs/e4_raw_attn_dingyi_oracle_init.json
```

Already checked locally.

## 11. Full Run Command

Run only after user confirmation:

```bash
cd /data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding
python scripts/run_oracle_moe_router_phase1.py \
  --config configs/e4_raw_attn_dingyi_oracle_init.json \
  --mode full
```

ACP submission can reuse the existing phase1 submit wrapper by setting:

```bash
CONFIG_PATH=configs/e4_raw_attn_dingyi_oracle_init.json
RUN_NAME=oracle_moe_raw_attn_dingyi_c7_20260519
JOB_NAME=ats-oracle-moe-raw-attn-dingyi-c7-4gpu
ORACLE_MOE_PHASE1_ALLOW_REAL_SUBMIT=1
bash scripts/submit_oracle_moe_phase1_4gpu_acp.sh
```

## 12. Report Plan

After run:

1. Add local summary under this version folder.
2. Update stage `summary.md` to separate:
   - legacy E4-LN；
   - C5/C6 clean expert inhibition；
   - C7 raw-attn Dingyi oracle-init。
3. Rewrite big closure for advisor-facing report.
4. Keep claims short and self-contained.
