# Result Summary: E4.3 Simple Unsupervised Center Control

### Observation

E4.3 只跑 uniform `unique_uniform`，新增 U1/U2 两个无监督 center 初始化对照，并引用已有 O1/O2 oracle-init 结果作为 reference。

设置：

```text
gate_input = raw attention_output
expert_input = original hidden / residual
center init for U1/U2 = KMeans over 100000 random token positions
seeds = 20260513, 20260514, 20260515
```

总表：

| variant | init | loss | readback | NMI | selects_best | selected_minus_best_CE | top_shared_energy | load_entropy | dead_experts |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| O1_C7d_oracle_init | oracle feature-prefix | C7d loss | 0.999 | 0.772 | 1.000 | 0.001 | 0.743 | 0.852 | 1.000 |
| O2_C7e_oracle_init | oracle feature-prefix | C7e loss | 1.000 | 0.920 | 1.000 | 0.000 | 0.728 | 1.178 | 0.600 |
| U1_unsup_random_position | random-position KMeans | C7d loss | 1.000 | 0.000 | 1.000 | 0.000 | 0.383 | 0.000 | 3.000 |
| U2_unsup_random_position | random-position KMeans | C7e loss | 1.000 | 0.212 | 1.000 | 0.000 | 0.288 | 0.187 | 2.667 |

### Interpretation

U1/U2 都能完成 readback，也能让 router 选中 forced-routing 下的 best expert；但它们没有保持 feature-level one-feature-one-expert。

关键点：

- U1 的 NMI 为 0，且 3 个 experts dead，说明 C7d prototype regularization 在 random-position KMeans init 下 collapse。
- U2 的 NMI 只有 0.212，且平均 2.667 个 experts dead，说明 performance loss 可以保留 utility selection，但不能自动恢复 feature-aligned routing。
- O1/O2 明显强于 U1/U2，说明前面 C7d/C7e 的好结果主要依赖 oracle feature-prefix center initialization。

### Limitation

本实验只测试最简单的 random-position KMeans。它不能否定更复杂的无监督 center selection，例如 high-loss positions、middle-PC subspace、online center update 或真实语料中的更强统计结构。

U2 还需要 all-expert forced forward 来构造 performance loss，额外 expert forward 约等于 `num_experts=4`。因此即使 U2 有效，也不是低成本方法；本次结果里 U2 仍没有形成 clean feature routing。

### Key Figures

![core metrics](figures/unsup_vs_oracle_core_metrics.png)

![feature expert heatmap](figures/unsup_vs_oracle_feature_expert_heatmap.png)

![boundary energy](figures/unsup_vs_oracle_boundary_energy.png)

### Claim Update

可以说：在当前 uniform synthetic setting 中，random-position unsupervised KMeans center init 不能替代 oracle feature-prefix center init。

不能说：所有无监督 center init 都不可行；只能说最简单的 random token-position KMeans 不够。

### Decision

保留 C7d/C7e 作为 synthetic routing reference，但必须明确其 oracle-init 边界。下一步如果要追真实可用方法，应设计更强的无监督 center selection，而不是把现有 C7d/C7e 直接当作真实方法。
