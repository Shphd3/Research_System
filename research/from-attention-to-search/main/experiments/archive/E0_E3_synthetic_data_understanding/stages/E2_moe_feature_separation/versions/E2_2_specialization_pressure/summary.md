# Result Summary: E2.2 Specialization Pressure Test

## Purpose And Hypothesis

E2.2 的目的，是在不修改 router objective 的前提下，测试增加分工压力是否会让 MoE 形成更 clean 的 feature-aligned specialization。

主假设：

```text
如果 E2 没有 one-feature-one-expert 是因为任务太容易或 expert 容量太大，
那么降低 expert capacity 或增加 feature count 应该提高 feature-expert alignment。
```

## Observation

三组条件：

| Condition | Feature count | ffn_dim | Seeds |
|---|---:|---:|---|
| baseline | 4 | 128 | 5 |
| bottleneck | 4 | 16 | 3 |
| pressure | 16 | 16 | 3 |

Main summary:

| Condition | Variant | CE | NMI | ARI | Readback | Ablation drop | Routing entropy | Dominant frac | Load imbalance |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | no-LB | 6.624 | 0.816 | 0.838 | 0.913 | 0.503 | 0.208 | 0.909 | 0.356 |
| baseline | LB | 6.625 | 0.823 | 0.841 | 0.948 | 0.479 | 0.126 | 0.935 | 0.015 |
| bottleneck | no-LB | 6.626 | 0.627 | 0.548 | 0.945 | 0.029 | 0.150 | 0.937 | 0.607 |
| bottleneck | LB | 6.625 | 0.644 | 0.591 | 0.917 | 0.003 | 0.204 | 0.922 | 0.014 |
| pressure | no-LB | 6.250 | 0.584 | 0.316 | 0.987 | 0.043 | 0.146 | 0.940 | 0.641 |
| pressure | LB | 6.250 | 0.534 | 0.241 | 0.986 | 0.065 | 0.114 | 0.953 | 0.027 |

16-feature pressure 中，readback 依然很强：高频 feature 接近 0.999，低频 `F16` 也约 0.947-0.948。

## Interpretation

E2.2 反驳了“只要加 specialization pressure，MoE 就会更 clean feature-aligned”的简单猜想。

降低 expert capacity 没有提高 feature-expert alignment，反而让 NMI / ARI 下降。更关键的是，readback 仍然很高，但 dominant expert ablation drop 从 baseline 的约 0.48-0.50 降到 0.00-0.03。这说明模型仍能预测 feature，但不再强依赖 MoE expert output。

16-feature pressure 也没有带来更干净的 routing specialization。readback 几乎全部成功，dominant fraction 也很高，但 NMI / ARI 低于 baseline，ablation drop 仍很小。这说明 feature 数量增加后，模型没有被迫形成 one-feature-one-expert；相反，它更像通过 shared path 或共享 expert computation 解决任务。

训练动力学解释：

```text
NTP loss 只奖励 target prediction
-> 如果 shared attention/residual/LM head 已能读回 feature
-> router 没有必要建立 feature-identity boundary
-> expert capacity 下降时，模型可能绕开 expert path
-> routing 可以稳定但不具备强因果专门化
```

所以当前 router 更像按“够用的 loss-compatible path”划分，而不是按 PCA、feature identity 或 one-feature-one-expert 目标划分。

## Limitation

E2.2 只跑了 3 seeds 的新增压力条件，且训练步数为 5000。它足够显示趋势，但不是完整 sweep。

本实验没有改 router objective，也没有削弱 shared attention / residual / LM head，因此不能排除“如果强制 expert path 必须承担预测，specialization 会增强”。

## Key Figures

![NMI](figures/specialization_pressure_nmi.png)

![Readback](figures/specialization_pressure_readback.png)

![Routing entropy](figures/specialization_pressure_entropy.png)

![Dominant fraction](figures/specialization_pressure_dominant_fraction.png)

![Load imbalance](figures/specialization_pressure_load_imbalance.png)

![16-feature pressure](figures/sixteen_feature_pressure_by_feature.png)

## Claim Update

Supported:

- Lowering expert capacity alone does not force cleaner feature-aligned specialization.
- Increasing feature count to 16 does not force one-feature-one-expert under current NTP objective.
- High readback can survive while dominant expert ablation effect collapses.
- Current model can route stably without making expert output causally necessary.

Weakened:

- “MoE did not separate because capacity was too high” is weakened.
- “More features will naturally force specialization” is weakened.
- “Routing alignment implies expert path carries the feature computation” is weakened.

Still unclear:

- whether shared attention/residual/LM head is carrying most feature prediction under pressure;
- whether top-2 routing would expose explicit expert sharing;
- whether reducing shared path capacity, not expert capacity, would force expert specialization.

## What Cannot Be Claimed

不能声称 MoE 不能 specialization。只能说：在当前 toy NTP setup 中，不改 router objective、只降低 expert capacity 或增加 feature count，没有推动更 clean feature-aligned specialization。

## Next Decision

下一步应该诊断 shared path：比较 attention/residual/LM head 与 MoE expert output 对 feature logits 的贡献。不要急着追求 one-feature-one-expert；先确认 feature computation 到底绕过了哪里。
