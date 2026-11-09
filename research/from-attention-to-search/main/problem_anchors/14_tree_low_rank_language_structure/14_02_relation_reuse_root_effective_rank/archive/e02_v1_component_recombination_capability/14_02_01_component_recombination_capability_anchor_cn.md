---
anchor_id: 14_02_01_component_recombination_capability
status: closed_falsified
canonical_language: en
companion_language: zh
parent_anchor: 14_02_relation_reuse_root_effective_rank
---

# A14_02_01 NTP 下的组件重组能力

研究者判断记录 来源：
A14_02 关系复用与 ROOT 功能秩

## 1. Problem Definition

上位 A14_02 要问的是：共享组合规则是否比匹配的独立 lookup 只需更少的
任务功能 ROOT 方向。但在 shared 条件真正学会可复用计算之前，秩差没有
可解释性。

**唯一决策问题：**

> 在 NTP 下，当两个组件都分别与其他组件共同出现过，但这一组件配对从未
> 出现在训练中时，注册的 shared-rule 任务能否正确完成该新配对？

**未见组件配对**指有序对 $(\alpha,\beta)$ 未进入训练，而 $\alpha$ 和
$\beta$ 各自在其他训练配对中出现。组件重组准确率是在这些未见配对的所有
实体和新 nuisance context 上计算 exact answer-token accuracy。它是能力
指标，不是秩指标。

## 2. Physical Priors

1. 若模型学到可复用的两阶段计算，组件分别在其他配对中学会后，应能在新
   配对中再次调用。
2. 重复完整输入—输出表不等于学会组件复用。
3. 新 context 不变性是前置门：连已见映射都不能在新 context 中完成时，
   尚未到达可以讨论组合能力的表面。

如果 seen-pair 能力通过，而 shared 的未见配对仍接近随机水平，则本任务上
的主要先验被否定。

## 3. Falsifiable Hypotheses

**主假设：**多样 context 的 NTP 训练能使 shared generator 完成未见组件
配对。

**最强 rival：**Transformer 记住完整的
$(\alpha,\beta,a)\mapsto y$ 表，而没有形成可复用组件；因此已见配对能做，
未见配对不能做。

判据：

- 支持：seen-pair 新 context 能力通过，并且至少 4/5 seeds 的 shared
  未见配对 accuracy 不低于 $0.80$；
- 否定：两组 seen-pair 能力都通过，但 shared 未见配对保持在
  $1/17$ 附近；
- 证据不足：任一主条件未通过 seen-pair 门、跨 seed 不稳定，或生成器／
  泄漏守卫失败。

## 4. Mathematical Model

实体为 $a\in\mathbb Z_{17}$。两类组件分别为
$\alpha\in\{0,1,2,3\}$ 和 $\beta\in\{1,2,4,8\}$。shared 任务为：

$$
u=a+\alpha\pmod {17},
\qquad
y=\beta u\pmod {17}.
$$

从 16 个组件配对中固定移除构成 perfect matching 的 4 对。剩余 12 对使
每个 $\alpha$ 与每个 $\beta$ 都在训练中各出现三次，所以成功不能用“测试
时看到了新 primitive token”解释。

lookup 控制为每个完整配对采样独立的 $\mathbb Z_{17}$ 随机 permutation。
它与 shared 使用完全相同的前缀、split、答案边际、曝光量、模型和目标。
lookup 应能在新 context 中完成已见配对，但对从未观察过的随机表没有可用
重组规则。

## 5. Computational Realization

每条序列统一为：

```text
[alpha] [entity] [nuisance-context] [beta] [ROOT] [ANSWER]
```

使用 2 层、1 头、宽度 64 的 causal Transformer，训练 full-position NTP
cross-entropy。每个已见 relation 使用 8 个不同训练 context；calibration
与 test context 和训练互斥。checkpoint 只由 seen-pair calibration 选择，
未见配对结果不参与选点或调参。

## 6. Minimal Falsification Tests

决定性实验为
[A14_02_E02 历史 Protocol](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/protocol_cn.md)。

必须通过：

- prefix、样本数与答案边际精确匹配；
- 所有 primitive component 都出现在训练中；
- 每个 relation 的 train、calibration、test context 互斥；
- shared 与 lookup 都通过 seen-pair 新 context 能力门；
- lookup 的未见配对结果低于泄漏阈值。

本实验不测 ROOT rank、参数 rank、Jacobian 或 Router。

## 7. Current Evidence

上位
[A14_02_E01](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary_cn.md)
对 shared-versus-lookup 秩问题的正式结论是证据不足。它确认 duplicate
exposure 不能形成新 context invariance，但 shared 条件没有通过注册的组合
能力门。

独立的
[A14_02_E02 历史 full run](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary_cn.md)
完成 10/10 个训练单元，全部生成器守卫通过。shared 与 lookup 的已见配对
新 context 能力均为 5/5 通过，平均 accuracy 分别为 0.9990 与 0.9949。
决定性的 shared 未见组件配对为 0/5 通过：平均 accuracy 0.2125，低于
0.80 门槛；四个 held-out pair 的平均 accuracy 也都低于 0.70。lookup
平均为 0.0640，接近 $1/17$ 随机水平，且没有泄漏失败。

shared 在五个配对 seeds 中都高于 lookup，但结果从 0.088 到 0.515 波动，
从未达到能力门。这与“利用了部分共享结构”相容，但不能称为已经学会可复用
算法。

## 8. Claim Boundary And Next Decision

注册的能力假设在这一受控表面被否定：模型学会已见配对的新 context 任务，
但没有形成可靠的未见组件配对重组。因此当前任务不具备继续解释
shared-versus-lookup ROOT 功能秩的资格。

不能据此声称 NTP 普遍不能学习组合、模型只用了 lookup 记忆、受控条件功能
秩定理错误、自然语言没有层级结构，或 Router 已有价值。

**唯一下一决策：**决定是否暂停当前 A14_02 合成表面，而不是在未通过组合
能力门的任务上启动 ROOT rank 实验。
