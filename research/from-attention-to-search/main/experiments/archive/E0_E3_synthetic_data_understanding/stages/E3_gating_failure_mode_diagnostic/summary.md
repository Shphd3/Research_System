# Result Summary: E3 Gating Failure Mode Diagnostic

## Observation

E3 full run 已完成：4 个 uniform synthetic trigram datasets，3 个 router variants，5 个 seeds，共 60 个训练 run。smoke test 先通过，full run 后生成 predictor decomposition、training dynamics、component ablation 和 forced-routing utility。

核心结论：

```text
当前模型和代码链路可以 clean specialize；
但 natural NTP router 不会自然形成 one-feature-one-expert。
```

在所有数据集上，`router_aux_lam_1_0` 都达到 `NMI = 1.000`、`ARI = 1.000`，同时 readback probability 保持在约 `0.996-0.997`。这说明只要给 router 明确的人工 feature label 信号，4-expert MoE 可以干净分开。

Natural router 也能完成 NTP readback，但 routing 不干净。`moe_top1_no_lb` 的 readback probability 约 `0.995-0.997`，但 NMI 只有 `0.560-0.724`；`moe_top1_lb` 的 NMI 约 `0.556-0.592`，没有因为 LB 变成 clean specialization。

## Interpretation

E3 支持的主解释是：

```text
feature identity 在 hidden state 中可读出，
但 NTP objective 不要求 router 按 feature identity 切分 expert。
```

最关键证据是 predictor decomposition：

| dataset / natural variants | feature-linear-probe | feature-only -> expert | router-projection -> expert | PCA-only -> expert |
|---|---:|---:|---:|---:|
| unique / no-LB | 1.000 | 0.539 | 0.973 | 0.941 |
| shared-B / no-LB | 1.000 | 0.510 | 0.984 | 0.968 |
| shared-target / no-LB | 1.000 | 0.435 | 0.963 | 0.908 |
| crossed-factorial / no-LB | 1.000 | 0.457 | 0.978 | 0.957 |

含义：hidden state 足够线性读出人工 feature label；但 learned router 的 expert choice 不是简单按这个 label 走。router choice 更容易被 router 自己的投影方向或 hidden geometry 主方向解释。

组件诊断显示 natural router 下多个 expert 都能支持同一个 feature prediction。以 learned route 为基准，`force_random_expert_expectation` 和 `mean_expert_output` 仍然给出较高 target probability；supervised router 则明显更依赖对应 expert。这说明 natural NTP 下存在 expert utility degeneracy：不是只有一个 expert 会做某个 feature。

## Limitation

E3 不能证明真实语言 MoE 的 expert 语义分工规律。这里的 `feature_id` 是人工标签，只用于 synthetic diagnosis。E3 也不能说明应该在真实语言中加入 feature supervision。

本轮可以更有把握地说：在这个 controlled setting 中，`representation separability` 不自动推出 `router specialization`。

## Key Figures

![predictor accuracy unique](figures/predictor_accuracy_by_group_unique_uniform.png)

![predictor accuracy crossed](figures/predictor_accuracy_by_group_crossed_factorial_uniform.png)

![routing dynamics](figures/nmi_over_training_steps.png)

![component ablation](figures/component_ablation_readback_drop.png)

## Claim Update

可以声称：

- 模型容量和代码链路不是主要问题：supervised router 可以在所有 control datasets 上 clean specialize。
- Natural top-1 router 可以学会任务读回，但不会自然形成干净的 one-feature-one-expert。
- Hidden representation 中存在可线性读出的 feature identity；router 没有必然使用这组人工 feature boundary。
- 当前 failure mode 更像 objective insufficiency + expert utility degeneracy，而不是单纯 token shortcut 或模型不会分。

不能声称：

- MoE 在真实语言中不会形成语义 expert。
- 线性 router 完全没有 specialization 能力。
- LB 一定有害；这里只说明在本设置中 LB 没有把 routing 变成 clean feature partition。

## Decision

E3 已经把 failure mode 从“模型是否能分”推进到更清楚的问题：

```text
在 hidden feature 可分时，natural router 为什么选择非 feature-aligned 的低损失 partition？
```

下一步不应继续重复普通 MoE full run，而应测试能否增加 specialization pressure，例如更强组合关系、更低 expert redundancy、更少 shared bypass，或比较 learned router 与 feature-oracle router 的 loss/utility 差异。
