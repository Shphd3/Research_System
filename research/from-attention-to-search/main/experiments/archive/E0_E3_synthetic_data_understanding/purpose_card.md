# Purpose Card: E0-E3 Synthetic Data Understanding

## 1. 总的抽象目的

建立学习的直觉，构建稳定的科研思路链条。

这组实验的作用不是马上证明 MoE、H-MoE 或 router retrieval 有用，而是在做模型实验前先把问题拆清楚：

- synthetic 数据里到底有什么可学习结构；
- dense Transformer FFN 会怎样学习不同频率的重复上下文 feature；
- Transformer MoE 是否能把不同 feature 分到不同 expert；
- synthetic 数据和真实语言数据的统计结构有哪些相同与不同。

## 2. 已知叙述 / 基于的知识

语言是 sequence。语言里的意思由上下文决定，而不是由孤立 token 决定。

因此，在这个 toy synthetic 世界里，feature 不能定义成单个 token，而应该定义成重复出现的上下文关系：

```text
A -> B
C D -> E
```

如果模型真的学到了 feature，证据不应只是 total loss 下降，而应表现为：

- 在对应 prefix 上提高目标 next-token 概率；
- feature-context 与 random-context 的预测熵不同；
- hidden state、FFN activation、logit-delta 或 MoE routing 中出现可诊断结构；
- 高频 feature 比低频 feature 更稳定、更可分，或对输出有更强因果影响。

## 3. 构建实验的原因

通过这组实验，我们最终想知道：

> 不同频率、具有特定上下文语义的表征，在 Transformer FFN 和 Transformer MoE 中是怎么被学习和分开的？模型学到这些表征时，外部预测和内部机制分别表现成什么？

## 4. 逻辑链

```text
根据认识构建 synthetic sequence
-> 审计 synthetic 数据是否真的含有目标 feature / frequency / collision
-> 用 dense Transformer 做 next-token prediction
-> 分析 FFN 是否学到不同频率 feature
-> 用 Transformer MoE 做同一任务
-> 分析 MoE 是否把不同 feature 分到不同 expert
-> 比较 synthetic 数据和真实数据特征的相同与不同
```

这条链条的核心顺序是：

```text
先理解数据 -> 再理解 dense model -> 再理解 MoE -> 最后检查 synthetic assumption 和 real data 的距离
```

## 5. Hypotheses To Decide

H0: synthetic corpus 真的含有受控的 pattern-level sequential features，而随机背景只产生可记录的 accidental collision。

H1: 在传统 Transformer 中，FFN 更倾向于学习训练数据中高频出现的 feature；feature 频率越高，其表征越稳定、越可分，对输出的因果影响越大。

H2: 在 Transformer MoE 中，如果 feature identity 是主要可学习机制，router / expert 会表现出高于随机的 feature-expert alignment。

H3: 真实语言也包含 repeated sequential patterns 和 heavy-tailed popularity，但真实数据的 hierarchy、ambiguity 和 context dependence 会比 toy synthetic 数据复杂。

## 6. Recursive Stage Map

| Stage | Role | Gate |
|---|---|---|
| `E0_data_sanity` | 验证数据本身是否受控 | 不通过则不能训练 dense / MoE |
| `E1_dense_feature_readback` | 验证 dense Transformer 是否能读出 feature | 不通过则不能讨论 MoE specialization |
| `E2_moe_feature_separation` | 验证 MoE 是否按 feature 分 expert | 只支持 controlled synthetic claim |
| `E3_synthetic_vs_real_statistics` | 比较 synthetic assumption 与真实数据统计 | 决定 toy 设定能代表真实数据的哪一部分 |
| `E4_hierarchical_phrase_extension` | 第二阶段 phrase hierarchy 扩展 | 只在 E0-E2 清楚后运行 |

## 7. What This Can Prove

这组实验可以证明：

- synthetic 数据构造是否受控；
- controlled feature 是否可被 dense NTP model 读出；
- MoE 在最简单 synthetic 条件下是否出现 feature-expert alignment；
- synthetic generator 捕捉了真实语言数据的哪些统计性质。

## 8. What This Cannot Prove

即使全线成功，也不能直接 claim：

- 真实 LLM 中的 FFN/MoE 以同样方式组织语义；
- H-MoE 优于 flat MoE；
- MoE router bucket 能作为 KV retrieval index；
- 真实推理速度会提升；
- synthetic 结果能无条件迁移到真实语言建模。

## 9. Next Decision

先执行 `E0_data_sanity`。只有数据审计通过，才进入 `E1_dense_feature_readback`。
