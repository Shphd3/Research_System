# Result Summary: H0521b Seq32 Contiguous AB

Hypothesis purpose card:

The legacy purpose card was removed; this summary is the surviving result
source.

## Observation

最重要指标是 `source-token routing purity`：在训练后 inference 阶段，分别看 A token、B token、background token 自己被 routed 到哪个 expert，并且先逐 seed 判断，再取跨 seed 稳定交集。

4 seeds 的直接结果：

| Rule | Cross-seed result |
|---|---:|
| A token 在 A-only 和 AB 中 dominant expert 是否一致 | `4/4` |
| B token 在 B-only 和 AB 中 dominant expert 是否一致 | `1/4` |
| A 与 B 是否进入不同 dominant expert | `2/4` |
| source identity NMI | mean `0.047`, min `0.020`, max `0.068` |
| source role NMI | mean `0.042`, min `0.024`, max `0.058` |

模型本身学会了任务：dense 和 MoE 在 A-only、B-only 上都是 `1.0` accuracy，AB-composite 分别是 `0.9992` 和 `0.9997`。

Seed 改变的是模型初始化、synthetic train/eval 样本抽样、训练 batch 顺序和优化轨迹；不变的是数据生成规则、模型结构、超参、token 定义和指标定义。由于 expert id 有 permutation symmetry，不同 seed 的 `E2` 不应直接当作同一个语义 expert；判断必须在每个 seed 内看 routing pattern，再取跨 seed 稳定交集。

## Interpretation

这轮不支持“source-token gating 形成干净 token identity bucket”。A token 的 dominant expert 在 A-only 和 AB 中跨 seed 一致，但 A 的 dominant fraction 只有 `0.413-0.479`，并不强；B token 的 context-stability 只在 `1/4` seed 成立。

因此，当前更稳的结论是：

```text
source-token gating 没有形成可直接用作 feature-level Reverse Index 的干净 A/B/background bucket。
```

prediction-position routing 有 task-level 结构，但这不是主指标。它说明 final decision state 可能按任务类型分，但不能替代 source-token bucket 质量。

## Limitation

source-token hidden state 是 causal 的：连续 `[A,B]` 中，A 的 source hidden 看不到未来的 B，B 的 source hidden 可以看到前面的 A。这是符合 KV source-token 语义的，但它也意味着 A_in_AB 不应被期待天然知道完整 AB motif。

## Key Figures

主图是 per-seed 横排图。平均图只做辅助展示，不作为主结论依据。

![Source identity routing by seed](figures/source_identity_routing_matrix_by_seed_row.png)

![Source role routing by seed](figures/source_role_routing_matrix_by_seed_row.png)

给汇报用的 B-only vs AB 对比图：

![B-only vs AB B source routing by seed](figures/b_only_vs_ab_b_source_routing_by_seed.png)

平均图：

![Source identity routing average](figures/source_identity_routing_matrix.png)

![Source role routing average](figures/source_role_routing_matrix.png)

![Source position routing](figures/source_position_routing_matrix.png)

## Claim Update

Supported:

```text
在 seq_len=32 连续 AB motif setup 中，source-token expert bucket 不是干净 token identity / feature bucket。
```

Weakened:

```text
直接用 source-token expert bucket 作为 feature-level Reverse Index candidate 的假设进一步变弱。
```

Still unclear:

```text
是否存在经过训练目标或架构约束后更稳定的 source-token feature bucket；
prediction-position routing 的 task-level 结构能否帮助 query-side routing。
```

## Next Decision

下一步不要只看平均 routing matrix。应继续做更小的 source-token rule audit：枚举 token identity、source position、left context，判断 router score 到底主要由 token identity、position embedding 还是 left context 决定。
