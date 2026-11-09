# Execution Plan: R0/R1 Post-Attention MoE Two-Pass RI

## 1. Run Scope

运行目录：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

配置：

```text
configs/r0_r1_post_attention_moe_two_pass_ri.json
```

脚本：

```text
scripts/run_post_attention_moe_two_pass_ri.py
scripts/submit_post_attention_moe_ri_4gpu_acp.sh
```

输出：

```text
outputs/r0_r1_post_attention_moe_two_pass_ri_20260520/
figures/r0_r1_post_attention_moe_two_pass_ri_20260520/
```

## 2. Model

模型结构：

```text
token embedding
-> 1-layer full causal attention
-> post-attention router / MoE FFN
-> LM head
```

第一遍 full forward 记录：

- attention output；
- Q/K/V；
- full attention weights；
- router expert id。

第二遍 restricted forward：

- 使用第一遍 expert bucket 生成候选 KV；
- 在候选 KV 上重新计算 exact QK attention；
- 将 restricted attention output 送入同一个 MoE/readout；
- 计算 CE 与 full forward 的差。

## 3. Data

数据集：

- `uniform`: all-trigram uniform feature counts。
- `zipf`: all-trigram long-tail feature counts。

Feature：

```text
ABC: [1,2] -> 22
DEF: [3,4] -> 23
GHI: [6,7] -> 20
JKL: [8,9] -> 21
```

## 4. Variants

| ID | 模型 | 训练信号 |
|---|---|---|
| `P0` | natural post-attention router | NTP + LB |
| `P1` | oracle feature-router | NTP + LB + feature-router CE |
| `P2` | clean inhibition router | NTP + LB + expert-only inhibition |

每个 dataset / variant 运行 3 个 seed：

```text
20260513, 20260514, 20260515
```

## 5. Metrics

- `routing_nmi`: feature label 与 expert id 的一致性。
- `RI ΔCE`: same-bucket restricted CE minus full-attention CE；越低越好。
- `random ΔCE`: random same-count candidate CE minus full CE。
- `RI advantage vs random`: `random ΔCE - RI ΔCE`；越大说明 RI bucket 越优于 random。
- `RI mass`: restricted attention 保留的 full-attention mass。

## 6. Completion Check

应有：

```text
18 checkpoint.pt
18 ri_summary_by_generator.csv
aggregate_ri_summary_by_generator.csv
ri_vs_random_ce_summary.csv
```

本轮已完成上述文件。
