# Detailed Notes: R0/R1 Post-Attention MoE Two-Pass RI

## 1. Run Record

运行脚本：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_post_attention_moe_two_pass_ri.py
```

配置：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/r0_r1_post_attention_moe_two_pass_ri.json
```

ACP job：

```text
pt-lzp3kcky
display name: ats-post-attn-moe-ri-resume-4gpu
```

ACP 状态显示 `SUSPENDED`，但所有 18 个 run 的 checkpoint 与 summary 均已生成。

## 2. Output Paths

原始输出：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/r0_r1_post_attention_moe_two_pass_ri_20260520/
```

原始图片：

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/r0_r1_post_attention_moe_two_pass_ri_20260520/
```

mainline-safe 汇总：

```text
ri_vs_random_ce_summary.csv
aggregate_ri_summary_by_generator.csv
figures/
```

## 3. Candidate Generator Comparison

每个模型都比较了以下 candidate generator：

| generator | 含义 |
|---|---|
| `ri_same_bucket` | 使用同 expert bucket KV，是本实验的 RI 方案 |
| `random_same_count` | 随机抽同样数量 KV，作为负对照 |
| `local_same_count` | 取最近邻局部 KV |
| `same_feature_oracle` | 使用真实 feature label 的 oracle 候选 |
| `oracle_dense_top_m` | 使用 full attention top-M，理论上界 |

## 4. Full Generator Table

### Uniform

| model | generator | ΔCE | attention mass |
|---|---|---:|---:|
| P0 | RI same bucket | 0.230 | 0.697 |
| P0 | random same count | 2.922 | 0.410 |
| P0 | local same count | 0.011 | 0.729 |
| P0 | same-feature oracle | 0.005 | 0.635 |
| P0 | dense top-M oracle | -0.000 | 0.775 |
| P1 | RI same bucket | 1.425 | 0.643 |
| P1 | random same count | 2.982 | 0.386 |
| P1 | local same count | 0.092 | 0.739 |
| P1 | same-feature oracle | -0.001 | 0.697 |
| P1 | dense top-M oracle | 0.001 | 0.828 |
| P2 | RI same bucket | -0.001 | 0.712 |
| P2 | random same count | 2.553 | 0.417 |
| P2 | local same count | -0.001 | 0.719 |
| P2 | same-feature oracle | 0.001 | 0.608 |
| P2 | dense top-M oracle | -0.001 | 0.749 |

### Zipf

| model | generator | ΔCE | attention mass |
|---|---|---:|---:|
| P0 | RI same bucket | 0.297 | 0.670 |
| P0 | random same count | 2.894 | 0.421 |
| P0 | local same count | 0.011 | 0.717 |
| P0 | same-feature oracle | 0.006 | 0.608 |
| P0 | dense top-M oracle | -0.000 | 0.754 |
| P1 | RI same bucket | 0.892 | 0.655 |
| P1 | random same count | 2.646 | 0.396 |
| P1 | local same count | 0.109 | 0.677 |
| P1 | same-feature oracle | -0.002 | 0.644 |
| P1 | dense top-M oracle | -0.001 | 0.822 |
| P2 | RI same bucket | 0.344 | 0.638 |
| P2 | random same count | 2.682 | 0.424 |
| P2 | local same count | 0.015 | 0.692 |
| P2 | same-feature oracle | 0.023 | 0.576 |
| P2 | dense top-M oracle | -0.000 | 0.736 |

## 5. Analysis Notes

`P1` 是重要反例：它有完美 feature-expert NMI，但 RI CE 不如 `P0/P2`。因此 feature purity 不是 RI 可用性的充分条件。

`P2` 在 uniform 上最好，说明 clean inhibition 的 functional pressure 可能更接近 RI 目标；但在 zipf 上 `P0` 与 `P2` 接近，不能说 inhibition 已经稳定胜出。

local 与 same-feature oracle 的 CE 接近 0，说明当前 synthetic task 里存在更强的候选结构。真正的下一步不是证明 RI 比 random 好，而是解释为什么 RI bucket 仍落后于这些候选上界。
