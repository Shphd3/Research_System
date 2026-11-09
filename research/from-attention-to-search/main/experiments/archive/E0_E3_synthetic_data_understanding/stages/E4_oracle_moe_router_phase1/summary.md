# Result Summary: E4 Oracle-MoE Router Phase 1

### Observation

E4 已统一为 raw-attention Oracle-MoE 设置：

```text
gate_input = raw attention_output
expert_input = original hidden / residual
```

本阶段包含三组关键结果：

| version | did | direct result |
|---|---|---|
| E4.1 uniform shortcut controls | 跑 `unique/shared-B/shared-target/crossed-factorial` C0-C7e | C7e 在四个控制数据上最强 |
| E4.2 Zipf | 跑 long-tail `10000/5000/500/100` C0-C7e | C7d/C7e 仍是最强候选 |
| E4.3 unsupervised center control | random token-position KMeans vs oracle feature-prefix KMeans | random-position KMeans 不能替代 oracle sampling |

### Interpretation

E4 的逻辑链现在是：

```text
natural router 能 readback
但不稳定 one-feature-one-expert
-> oracle feature-prefix sampling 可以取到 rule-context representations
-> KMeans center init + regularization / utility feedback 可以稳定 routing
-> random-position KMeans 失败，说明关键不是 KMeans 本身，而是如何找到应该聚类的位置
```

所以本阶段把问题从“router 为什么分错”推进为：

```text
如何无 oracle 地发现值得聚类的 rule-context 表征？
```

### Key Results

Uniform shortcut controls 中，C7e 最强：

| dataset | readback | NMI | feature-boundary alignment | selects-best |
|---|---:|---:|---:|---:|
| `unique_uniform` | 1.000 | 0.920 | 0.413 | 1.000 |
| `shared_b_uniform` | 1.000 | 0.919 | 0.402 | 1.000 |
| `shared_target_uniform` | 1.000 | 0.893 | 0.400 | 1.000 |
| `crossed_factorial_uniform` | 1.000 | 0.834 | 0.392 | 1.000 |

Zipf 中，C7d/C7e 仍最强：

| variant | readback | NMI | selects-best |
|---|---:|---:|---:|
| C7d | 0.994 | 0.819 | 0.990 |
| C7e | 0.997 | 0.822 | 0.993 |

E4.3 显示 random-position KMeans 失败：

| variant | init | readback | NMI | load entropy | dead experts |
|---|---|---:|---:|---:|---:|
| C7d oracle init | oracle feature-prefix | 0.999 | 0.772 | 0.852 | 1.000 |
| C7e oracle init | oracle feature-prefix | 1.000 | 0.920 | 1.178 | 0.600 |
| U1 random KMeans | random token positions | 1.000 | 0.000 | 0.000 | 3.000 |
| U2 random KMeans | random token positions | 1.000 | 0.212 | 0.187 | 2.667 |

### Key Figures

![uniform core metrics](figures/e4_uniform_shortcut_core_metrics.png)

![zipf core metrics](figures/e4_zipf_core_metrics.png)

![random vs oracle KMeans](versions/E4_3_simple_unsupervised_center_control/figures/unsup_vs_oracle_core_metrics.png)

### Claim Update

可以说：

- C7d/C7e 是当前最强 synthetic routing reference。
- C7 的好结果来自 oracle feature-prefix sampling 后的 KMeans center init，再加正则或 utility feedback。
- 最简单 random-position KMeans 不能自动找到 feature centers。

不能说：

- natural MoE 已经自发形成 relation-level one-feature-one-expert；
- C7 是真实语言可直接使用的无监督方法；
- NMI 高本身就证明 functional specialization。

### Decision

E4 不直接推进 Reverse Index。下一步应先解决：

```text
不用 oracle feature-prefix positions，如何自动定位 rule-context 表征？
```

候选方向包括 high-loss sampling、repeated-context mining、attention-source selection 和 online center update。
