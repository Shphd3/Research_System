# Protocol 中文版：A01_01 common operator identifiability full run

## 0. 审批快照

审批状态：用户在 2026-06-29 的持续目标中明确要求开始执行 full run。

目的：判断 common 是单一 hidden-state 几何对象，还是必须按机制判据定义的 operator family。

主 anchor：`01_01_common_operator_identifiability_anchor.md`。辅助 anchor：`01_02_ground_truth_projector_recovery_anchor.md`。

决策问题：common 能不能只从 hidden geometry 和 loss 中选出来？还是不同机制标准会选出不同 operator？

测试的物理先验：activation common、shared-prediction common、gradient common 可以不是同一个对象。

核心模型项：候选 projector $P$ 作用在 hidden state $h$ 和梯度外积 input side 上。

主指标：`criterion_winner_diversity`，即不同判据下胜出的 estimator 种类数。

最小设置：构造已知真实 $P_c^*$ 的 synthetic hidden states，比较 activation PCA、group mean、gradient-intersection、feedback-drift、random control。

条件：activation-dominant、unique-dominant、mean-offset、gradient-intersection、feedback-drift。

Pass：多个 estimator 分别在不同机制判据下胜出，说明 common 不能作为单一无条件几何对象处理。

Fail：同一个 estimator 在所有条件和所有主要判据下都胜出，说明单一 common operator 路线仍可行。

不能 claim：真实 DCLM common operator、preservation rescue、shared expert 有效、residualized MoE 有效。

## 1. 核心公式

合成 hidden state：

$$
h = s_c A z_c + s_u B_g z_g + s_n N z_n + \epsilon
$$

真实 common projector：

$$
P_c^* = AA^\top
$$

group-conditioned gradient：

$$
G_g=\mathbb{E}[\delta_g h^\top \mid g]
$$

残差化梯度：

$$
G_g^r(P)=\mathbb{E}[\delta_g ((I-P)h)^\top \mid g]
$$

## 2. 判据

1. recovery：$\hat P$ 是否恢复真实 $P_c^*$。
2. shared-loss sensitivity：删除 $\hat P h$ 是否伤 shared target。
3. rare-loss sensitivity：删除 $\hat P h$ 是否伤 rare target。
4. gradient-overlap reduction：删除 $\hat P h$ 是否降低跨 group 梯度重叠。

## 3. 结果解释规则

如果不同判据选出不同 estimator，则推进结论为：

```text
common operator 是机制条件化对象；
不能把 PCA / mean / gradient / feedback 中任一个直接叫做 common。
```

如果同一个 estimator 全面胜出，则推进结论为：

```text
单一 common operator 路线仍可行；
下一步应把该 estimator 带入真实 DCLM bridge。
```

