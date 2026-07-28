# A10_02 频率-奇异谱 SGD 不稳定实验 Protocol

## 0. 审批快照

**审批状态：** 用户在 2026-07-03 当前对话中明确批准立即执行，包括本地执行；如果远程/SCO 可用，也允许提交远程执行。

**Anchor：** `Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_02_frequency_singular_sgd_instability_anchor.md`

**决策问题：** 在小型 nested-prefix causal model 中，Zipfian frequency 是否产生输出头 singular concentration，并预测高 LR SGD 不稳定？

**测试的物理先验：** 频繁 common prefix 产生一致梯度；一致梯度长出高增益奇异方向；高 LR SGD 先在这些方向上局部失稳。

**主指标：** instability-localization profile：高 LR SGD 必须在 common learning 与 singular concentration 之后失稳，并且失稳附近的 top spectral-band gradient mass $B_{\mathrm{top}}(G)$ 或 token-gradient concentration 升高。

**证伪条件：** 不稳定发生在 common learning 或 singular concentration 之前，或者不稳定没有 top 谱带/token column 局部化。

**claim 边界：** 只针对 controlled synthetic nested-prefix task；不 claim real text、不解释 Adam 全部优势、不提出最终 optimizer、不更新 MoE routing preservation。

## 1. 目的

这个实验把 0701 design 变成一个机制诊断。它不以 final validation loss 排名 optimizer，而是判断哪些几何量能预测高 LR SGD 不稳定。

## 2. 数据

使用 nested-prefix next-token 序列：

$$
A\to AB\to ABC\to ABCD\to ABCDE\to ABCDEF\to ABCDEFG.
$$

每个样本从 Zipfian 分布采样最大 prefix depth。训练标签是每个 prefix 位置的 next token。因此 $A$、$B$ 是 common targets，$F$、$G$ 是 rare targets。

## 3. 模型

一层单头 causal next-token model，包括 token embedding、position embedding、causal attention、小型 feed-forward block 和 output head。hidden dimension 足够小，可以完整记录 SVD。

默认设置：

| 项 | 值 |
| --- | --- |
| hidden dimension | 32 |
| maximum prefix depth | 7 |
| batch size | 192 |
| steps | 240 |
| seeds | 0, 1, 2 |
| logging interval | 5 steps |

## 4. 条件

| 条件 | 作用 | 学习率角色 |
| --- | --- | --- |
| `adamw_ce` | 稳定 adaptive baseline | 标准 CE AdamW |
| `sgd_safe_ce` | 安全 SGD baseline | 较低 LR SGD |
| `sgd_high_ce` | 不稳定 probe | 高 LR SGD |
| `sgd_high_row_clip` | 类 SGD-LL probe | 高 LR + output-row gradient clipping |
| `sgd_high_row_norm` | 类 SCALE probe | 高 LR + output-row gradient normalization |
| `sgd_high_label_smoothing` | margin-pressure probe | 高 LR + label smoothing |
| `sgd_high_spectral_clip` | 直接谱 probe | 高 LR + output-head singular-value cap |

## 5. 指标

主指标：
`instability_localization`：首次不稳定 step、该 step 附近的 $B_{\mathrm{top}}(G)$、token-gradient concentration，以及 common learning 和 singular concentration 是否已经发生。

辅助指标：
`common_accuracy`、`rare_accuracy`、`top_singular_value`、`top_energy_fraction`、`frequency_gradient_correlation`、`token_gradient_imbalance`、`extra_feature_effective_rank`、`extra_feature_top2_mass`、`final_eval_loss`、`stable`。

top 谱带梯度质量：

$$
B_{\mathrm{top}}(G)=\frac{\|G V_{\mathrm{top}}\|_F^2}{\|G\|_F^2+\epsilon}.
$$

extra-feature effective rank：

$$
\operatorname{erank}(E)=\exp\left(-\sum_i p_i\log p_i\right),\quad
p_i=\frac{s_i^2}{\sum_j s_j^2}.
$$

## 6. 通过 / 失败 / 证据不足

支持机制需要三件事同时成立：

1. frequency-gradient link：early output-head gradient row norm 与 realized target-token frequency 正相关。
2. temporal order：common accuracy 先提升，之后 top singular value / top energy 增长。
3. localization：high LR SGD 在上述变化之后失稳，并且 $B_{\mathrm{top}}(G)$ 或 token-gradient concentration 高于稳定 baseline。

削弱机制：
不稳定没有局部化、发生在 common learning 前，或没有 top singular concentration。

证据不足：
没有 high-LR 条件失稳；所有 high-LR 条件都在 common 学会前失败；或 Zipfian 频率差没有生成出来。

## 7. 输出

表格：
`tables/step_metrics.csv`、`tables/condition_summary.csv`、`tables/final_by_seed.csv`。

图：
`figures/temporal_profile.png`、`figures/stability_by_condition.png`、`figures/spectral_localization.png`、`figures/extra_feature_geometry.png`。

报告：
`summary.md`、`detailed.md`，以及 anchor evidence update。

## 8. 远程执行说明

本地存在 SCO binary：`/root/.sco/bin/sco`。如果 workspace 与 image 配置可用，同一脚本可以提交 ACP job。若远程提交失败，本地结果仍作为当前决策 artifact，并在 `detailed.md` 记录失败原因。
