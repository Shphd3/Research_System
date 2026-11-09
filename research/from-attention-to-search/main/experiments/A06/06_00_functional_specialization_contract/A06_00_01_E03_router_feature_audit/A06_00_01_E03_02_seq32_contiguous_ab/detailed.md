# Detailed Report: H0521b Seq32 Contiguous AB

## TL;DR

H0521b 的主指标是 `source-token routing purity`。结果显示：模型学会了 seq_len=32 的连续 AB motif task，但 source-token gating 没有形成干净 A/B/background bucket。跨 seed 稳定交集只有 A token 在 A-only 和 AB 中 dominant expert 一致；B token 不稳定，A/B 是否进入不同 expert 也不稳定。因此，这轮进一步削弱了“source-token expert bucket 可以直接作为 feature-level Reverse Index”的路线。

## 实验回答什么

这轮不是在问 final prediction state 怎么分 expert，而是在问历史 source token 自己怎么被分 expert：

```text
A token 是否稳定进入 A expert？
B token 是否稳定进入 B expert？
background token 是否和 A/B 分开？
同一个 token 在不同 context 下是否进同一个 expert？
```

这直接对应 Reverse Index 的 source-token bucket 问题。

## 实验设置

输入长度：

```text
seq_len = 32
```

数据：

```text
A-only:       background 中插入 [A, r] -> y_A
B-only:       background 中插入 [r, B] -> y_B
AB-composite: background 中插入 [A, B] -> y_AB
background:  全 background token -> r_k
```

模型：

```text
dense tiny Transformer baseline
top-1 MoE tiny Transformer, no load balance
```

运行：

```text
ACP job: pt-tpobuqga
status: SUCCEEDED
seeds: 20260521, 20260522, 20260523, 20260524
runtime log: active/attention_search_hier_kv/logs/acp/h0521b_seq32_contiguous_ab_4gpu_20260521_20260521_131222.log
result dir: active/synthetic_data_understanding/results/h0521b_seq32_contiguous_ab/h0521b_seq32_contiguous_ab_4gpu_20260521/
```

不同 seed 会改变：

- model initialization；
- synthetic train/eval samples 的具体抽样；
- batch sampling order；
- optimization trajectory。

不同 seed 不改变：

- `seq_len=32`；
- A/B/background token 定义；
- A-only、B-only、AB-composite、background 的任务规则；
- 模型结构、训练步数、batch size、learning rate；
- 指标定义。

因此，routing 图不能跨 seed 直接平均后下结论。尤其 MoE expert id 有 permutation symmetry：seed 1 的 `E2` 不等于 seed 2 的 `E2` 有相同语义。正确读法是每个 seed 内判断 pattern，再看哪些 rule 在所有 seed 都成立。

## 指标怎么读

`source-token routing purity` 是主指标。它看的是 source token 自己进入哪个 expert，不是最后预测位置进入哪个 expert。

关键 seed-level 规则：

- `A_same_across_context`: A_in_A_only 和 A_in_AB 的 dominant expert 是否一致；
- `B_same_across_context`: B_in_B_only 和 B_in_AB 的 dominant expert 是否一致；
- `A_B_different_identity_expert`: A token 和 B token 的 identity-level dominant expert 是否不同；
- `identity_nmi`: token identity 与 expert id 的对齐程度；
- `role_nmi`: source role 与 expert id 的对齐程度。

主结论只使用跨 seed 稳定交集。

## 主要结果

### 任务可学

| Model | A-only acc | B-only acc | AB acc | background acc |
|---|---:|---:|---:|---:|
| dense | 1.000 | 1.000 | 0.999 | 0.008 |
| MoE | 1.000 | 1.000 | 1.000 | 0.008 |

background 是随机背景 target，低 accuracy 是预期的。

### 跨 Seed 稳定规则

| Rule | Result |
|---|---:|
| A_same_across_context | `4/4` |
| B_same_across_context | `1/4` |
| A_B_different_identity_expert | `2/4` |
| identity_nmi mean | `0.047` |
| role_nmi mean | `0.042` |

解释：A token 有一个弱稳定性，但整体 token identity / role 与 expert 的对齐非常弱。B token 不稳定，A/B 是否分开也不稳定。

### Source Identity Routing

主图是 per-seed 横排图。它显示 B 的 dominant expert 和 A/B separation 在不同 seed 下并不稳定。

![Source identity routing by seed](figures/source_identity_routing_matrix_by_seed_row.png)

平均 routing matrix 只用于粗略展示 A/B/background 都分散到多个 expert，不能作为主结论依据。

![Source identity routing](figures/source_identity_routing_matrix.png)

### Source Role Routing

per-seed role 图显示：A_in_A_only 和 A_in_AB 在每个 seed 内 dominant expert 一致；B_in_B_only 和 B_in_AB 只在 1/4 seed 内一致。

![Source role routing by seed](figures/source_role_routing_matrix_by_seed_row.png)

如果不只看 dominant expert，而看整条 routing distribution，B_in_B_only 与 B_in_AB 仍有 identity trace：seed `20260521` cosine 为 `0.995`，seed `20260522` 为 `0.987`；seed `20260523` 和 `20260524` 分别降到 `0.837` 和 `0.875`，说明 left context 对 B routing 有调制。

![B-only vs AB B source routing by seed](figures/b_only_vs_ab_b_source_routing_by_seed.png)

平均图只能帮助快速看整体趋势；结论仍然来自 per-seed rule。

![Source role routing](figures/source_role_routing_matrix.png)

### Source Position Routing

source position routing 用来检查 position shortcut。当前图用于提示位置影响，但主结论仍以 seed-level identity/role 规则为准。

![Source position routing](figures/source_position_routing_matrix.png)

## 从结果到判断

观察：

```text
task learned -> source identity NMI low -> A weakly stable -> B/context unstable -> A/B separation not stable across seeds
```

解释：

```text
普通 top-1 MoE 的 source-token gating 没有自然形成稳定 A/B/background token identity bucket。
```

边界：

```text
这不证明所有 router 都不能形成 source-token feature bucket；只说明当前 ordinary no-load-balance top-1 MoE 不能稳定形成。
```

## 没有证明什么

- 不能证明真实语言中的 source-token routing 一定混乱；
- 不能证明 top-k、load balance、router supervision 无效；
- 不能证明 prediction-position routing 没有用；
- 不能证明 Reverse Index 完全不可行；
- 不能用平均 routing matrix 替代逐 seed 稳定性判断。

## 下一步

下一步应做更小的 source-token rule audit：

```text
枚举 token identity × position × left context
直接分析 router score / expert id
判断 expert cell 的共同特征到底是 token identity、position embedding，还是 causal left context。
```
