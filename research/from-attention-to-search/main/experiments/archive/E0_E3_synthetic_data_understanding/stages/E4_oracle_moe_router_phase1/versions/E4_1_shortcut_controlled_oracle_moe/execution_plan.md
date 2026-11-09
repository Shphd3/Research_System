# Execution Plan: E4.1 Shortcut-Controlled Oracle-MoE

## 1. Run Goal

检验 E4 raw-attention C-series / C7 中的 routing 是否真的按上下文关系分 expert，而不是按 token、target 或 attention source shortcut 分 expert。

主判据不是单个 NMI，而是四项同时成立：

```text
feature assignment
boundary alignment
expert utility
readback
```

## 2. Data Construction

所有数据保持：

```text
vocab_size = 1000
corpus_length = 1000000
feature_count = 3900 / 3900 / 3900 / 3900
seq_len = 32
```

### Dataset A: `unique_uniform`

标准基线：

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
```

用途：复现 E4 raw-attention 主结果。

### Dataset B: `shared_prefix_end_uniform`

控制 prefix-end token shortcut：

```text
ABC: [1,2] -> 22
DBF: [3,2] -> 23
GHI: [6,7] -> 20
JLI: [8,7] -> 21
```

判断：如果 router 主要看 prefix-end token，则 `[1,2]` 与 `[3,2]`、`[6,7]` 与 `[8,7]` 会更容易 route 相似。

### Dataset C: `shared_target_uniform`

控制 target-token shortcut：

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 22
GHI: [6,7] -> 20
JKL: [8,9] -> 20
```

判断：如果 router 主要看 target token 或 readback direction，则同 target 的 features 会 route 相似。

### Dataset D: `crossed_factorial_uniform`

同时打散 first-token、prefix-end-token、target-token 与 feature relation 的一一对应：

```text
F00: [1,2] -> 22
F01: [1,4] -> 23
F10: [3,2] -> 23
F11: [3,4] -> 22
```

判断：如果 router 仍能按 feature relation 分，说明它不是只靠单 token shortcut。

## 3. Model / Training Setup

沿用 E4 raw-attention Oracle-MoE：

```text
attention_output = Attention(LN(x0))
expert_input     = x0 + attention_output
gate_input       = attention_output
router_input     = attention_output
router_input_norm = raw
```

默认训练参数：

```text
steps = 10000
batch_size = 128
seq_len = 32
d_model = 64
n_heads = 4
ffn_dim = 128
num_experts = 4
lr = 0.0006
seeds = [20260513, 20260514, 20260515, 20260516, 20260517]
```

## 4. Variants

优先 full run：

| ID | 目的 |
|---|---|
| C0 | 普通 raw-attn linear router baseline |
| C6 | center + clean expert inhibition，检查功能排他性是否帮助 relation routing |
| C7a | Dingyi random prototype baseline |
| C7b | Dingyi frozen oracle centers，检查 oracle center upper bound |
| C7c | Dingyi trainable oracle-init centers，检查 centers 是否可在 NTP 中保持 |
| C7d | Dingyi oracle-init + inhibition/homeostasis，检查 center sharpening 是否有效 |

可选补充：

```text
C5, C7e, and full C0-C7
```

若算力不足，先跑：

```text
datasets = [unique_uniform, crossed_factorial_uniform]
variants = [C0, C6, C7a, C7c, C7d]
seeds = [20260513, 20260514, 20260515]
```

## 5. Metrics And Artifacts

基础指标：

```text
NTP loss
readback_accuracy_p_gt_0_5
target probability
feature-expert NMI
expert load entropy
dead expert count
router confidence / margin / entropy
```

Shortcut 诊断：

```text
MI(expert; feature)
MI(expert; prefix_end_token)
MI(expert; target_token)
MI(expert; first_token)
MI(expert; attention_source_token)
```

Boundary 诊断：

```text
feature direction vs router boundary cosine
token direction vs router boundary cosine
target direction vs router boundary cosine
SVD band energy of router boundary
```

Utility 诊断：

```text
forced expert CE matrix
forced expert target-prob matrix
router_selects_best_expert_rate
selected_minus_best_CE
utility diagonality
```

Counterfactual 诊断：

```text
same feature, changed filler
shared prefix-end, changed first token
shared target, changed feature
crossed-factorial controlled swaps
route flip rate
gate_input cosine before/after
```

## 6. Required Figures

```text
fig_e4_1_routing_matrix_by_dataset.png
fig_e4_1_factor_mi_by_dataset.png
fig_e4_1_boundary_alignment_by_dataset.png
fig_e4_1_utility_matrix_by_dataset.png
fig_e4_1_readback_vs_specialization.png
fig_e4_1_counterfactual_flip_summary.png
```

## 7. Pass / Fail Criteria

Strong support:

- crossed-factorial 中 feature assignment 仍高；
- router boundary 更对齐 feature direction，而不是 prefix/target direction；
- forced expert utility 接近 diagonal；
- router selected expert 接近 best expert；
- readback 保持良好；
- 结果跨多数 seeds 稳定。

Weak support:

- readback 良好，但 feature assignment 或 utility 不稳定；
- C7 oracle-init 比 C7a 强，但只在 `unique_uniform` 明显；
- C6 selected-best 高，但 feature-boundary alignment 弱。

No support:

- shared-prefix-end 或 shared-target 后 routing 跟 token/target 走；
- crossed-factorial 中 feature assignment 崩掉；
- utility matrix 不 diagonal；
- readback 靠 shared path 完成，expert utility 无差异。

## 8. Result Location

Mainline-safe report:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E4_oracle_moe_router_phase1/versions/E4_1_shortcut_controlled_oracle_moe/
  summary.md
  detailed.md
  figures/
```

Ignored workspace output:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
  outputs/e4_1_shortcut_controlled_oracle_moe_<date>/
  figures/e4_1_shortcut_controlled_oracle_moe_<date>/
```

## 9. Decision After E4.1

If E4.1 passes:

```text
Proceed to Reverse Index R1 source decomposition.
```

If E4.1 fails:

```text
Do not use feature-aligned routing as RI premise.
Diagnose whether the current synthetic task creates token shortcuts or whether expert utility is redundant.
```
