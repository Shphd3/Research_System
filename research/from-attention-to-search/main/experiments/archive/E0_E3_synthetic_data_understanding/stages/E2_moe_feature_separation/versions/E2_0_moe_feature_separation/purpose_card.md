# Experiment Card: E2 MoE Feature Separation

## 1. 总目的

E2 的总目的，是在 E1 已经证明 dense Transformer 能读回 synthetic context feature 之后，进一步判断 MoE 是否会把这些 feature 分到不同 expert。

这个实验服务于整条 data-first 主线：

```text
先确认数据中有什么 feature
-> 再确认 dense model 能不能学到 feature
-> 再问 MoE 是否会把 feature 分开
```

E2 不追求证明真实 LLM 中的 expert 语义，只追求在 controlled toy world 中建立一个可检验的学习直觉。

## 2. 在主线中的位置

E0/E1 已经关闭了两个前置问题：

- E0：all-trigram synthetic corpus 中的 feature 足够干净；
- E1：dense toy Transformer 能通过 NTP 读回这些 feature。

因此 E2 的位置是：

```text
如果 dense model 能学到这些 feature，
那么 MoE 会不会在 routing/expert 层面把这些 feature 分开？
```

只有 E2 有清楚结果后，才适合继续问真实数据统计、MoE hierarchy 或更复杂 router 结构。

## 3. 已知知识 / 前提

本实验使用的 feature 不是单个 token，而是上下文关系：

```text
[A,B] -> [C]
```

已知前提：

- sequence 中的意义来自上下文关系；
- E1 表明 clean all-trigram feature 可以被 dense Transformer 学到；
- E1 的 shuffled unigram control 不能读回 feature，因此当前要检验的是 sequential relation 驱动的 expert preference，而不是 token frequency;
- MoE expert 不直接知道 feature label；
- 如果 MoE 真的按 feature 学习，信号应该出现在 routing distribution、expert purity 和 expert ablation 中，而不只是 loss 下降。

## 4. 实验目的

E2 要回答：

```text
在同一个 NTP 任务中，MoE 的 expert preference 是否与 feature identity 对齐？
```

主判据是 feature identity separation。frequency 只作为辅助解释：高频 feature 是否更稳定，低频 feature 是否更容易混合。

## 5. 假设与细化假设

主假设 H2：

```text
在 controlled synthetic sequence 中，
MoE 会通过 next-token loss 学到 feature-level expert preference。
```

细化假设：

- H2a：不同 feature 的 $P(\text{expert}\mid\text{feature})$ 明显不同。
- H2b：某些 expert 的 $P(\text{feature}\mid\text{expert})$ 高于 random routing。
- H2c：如果 ablate 一个 feature 的 dominant expert，该 feature 的 target probability 或 logit margin 会下降。
- H2d：如果 routing 主要由 load balance、token identity 或 optimization noise 主导，那么 feature-expert alignment 会弱、不稳定，或在 LB 后被打散。

## 6. 实验对象

实验对象是 E0/E1 已验证的 all-trigram clean long-tail corpus：

| Feature | Relation | Frequency |
|---|---|---:|
| ABC | `[1,2] -> 22` | 10000 |
| DEF | `[3,4] -> 23` | 5000 |
| GHI | `[6,7] -> 20` | 500 |
| JKL | `[8,9] -> 21` | 100 |

模型对象是 tiny Transformer MoE：在 E1 dense Transformer 的基础上，把 FFN 替换为 4-expert MoE。

## 7. 实验范式

E2 使用同一数据、同一 NTP 任务，比较两个 MoE 设定：

```text
no-LB MoE: 看自然 routing 是否形成 feature preference
LB MoE: 看 load balance 是否改变或削弱 feature preference
```

观察对象分三层：

- 外部行为：每个 feature 的 target probability / logit margin；
- routing 结构：feature 到 expert 的分布是否非随机；
- 因果诊断：屏蔽 dominant expert 是否破坏对应 feature readback。
- 对照诊断：shuffled unigram control 是否移除 readback、transition 和 ablation effect。
- force-routing 诊断：强制把 feature prefix hidden state 分别送入每个 expert，检查 router-selected expert 是否也是最直接支持 feature prediction 的 expert。

## 8. 预期结果与假设更新逻辑

如果结果显示：

```text
readback 成功
+ feature routing matrix 非均匀
+ purity 高于 random
+ ablation 会损伤对应 feature
```

则 H2 得到支持：MoE 在 controlled synthetic world 中可以形成 feature-level expert preference。

如果结果显示：

```text
readback 成功
但 routing 与 feature identity 接近随机
```

则更新为：MoE 能学到任务，但 expert 分工不一定自然对齐 feature identity。

如果结果显示：

```text
no-LB 有 alignment
LB 后 alignment 变弱
```

则说明 load balance 可能改变或压制自然 feature specialization。

如果结果显示：

```text
routing 有差异
但 ablation 不影响 feature readback
```

则只能说 routing 有相关性，不能说 expert 对 feature 输出有因果作用。

如果 force-routing 显示：

```text
dominant router expert 不是 best forced expert
或所有 expert 的 forced probability 接近
```

则说明 dominant expert 的作用可能来自 router path / residual context，而不是 expert 本身更擅长该 feature。

## 9. 不能声称什么

即使 E2 成功，也不能声称：

- 真实 LLM expert 也按语义 feature 分工；
- H-MoE 优于 flat MoE；
- MoE router 可以直接作为 KV retrieval index；
- synthetic 结果能直接迁移到真实语言；
- routing matrix 本身就是 mechanistic proof。

## 10. 下一步决策

E2 strong support：进入 E3，比较 synthetic feature 假设和真实数据统计结构。

E2 weak / no support：优先诊断 routing 是否被 load balance、token identity、frequency 或 optimization instability 主导。
