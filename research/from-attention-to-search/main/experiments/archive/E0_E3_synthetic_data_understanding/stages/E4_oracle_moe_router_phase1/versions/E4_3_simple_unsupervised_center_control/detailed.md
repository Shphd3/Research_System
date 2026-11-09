# Detailed Notes: E4.3 Simple Unsupervised Center Control

## Run Records

Training:

```text
job: pt-vj5m5cup
name: ats-e4-3-unsup-center-uniform-4gpu
status: SUCCEEDED
config: configs/e4_3_simple_unsup_center_uniform.json
variants: U1 U2
seeds: 20260513 20260514 20260515
```

Diagnostic:

```text
job: pt-4f9eytfh
name: ats-e4-3-unsup-center-uniform-diag-4gpu
status: SUCCEEDED
analysis: 6/6
boundary audit: 1/1
```

## Output Paths

Running outputs:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e4_3_simple_unsup_center_uniform/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e4_3_simple_unsup_center_uniform_diagnostic/
```

Mainline-safe summary table:

```text
e4_3_unsup_vs_oracle_summary_table.csv
```

## Metric Meaning

- `readback`: planted feature prefix 下 target probability 是否超过 0.5。
- `NMI`: feature label 与 expert assignment 的一致性。
- `selects_best`: router 选中的 expert 是否是 forced-routing 下 CE 最低 expert。
- `selected_minus_best_CE`: 选中 expert 相比 best expert 的 CE 差值。
- `top_shared_energy`: router boundary 在 top/high-variance subspace 的能量。
- `load_entropy`: expert load 熵；越低越 collapse。
- `dead_experts`: feature-prefix positions 上未被使用的 experts 数。

## Main Table

见 `e4_3_unsup_vs_oracle_summary_table.csv`。

核心数值：

```text
O2_C7e_oracle_init: NMI=0.920, load_entropy=1.178, dead_experts=0.600
U2_unsup_random_position: NMI=0.212, load_entropy=0.187, dead_experts=2.667
```

## Interpretation Detail

U1/U2 的 `selects_best=1.0` 说明它们没有完全失去 task utility；但它们几乎只使用少数 experts。因此 selected-best 成功并不等价于 one-feature-one-expert。

U2 的 performance loss 需要对每个 expert 做 forced forward，计算成本约为 `num_experts=4` 倍 expert forward。本次即使付出该成本，也没有恢复 oracle-init 的 feature assignment。
