# Protocol CN: A01_03 Gradient Common vs Activation Common Full Run

## 0. Approval Snapshot

Approval status：用户在 active goal 中明确要求执行 full run。

Purpose：判断 optimization-relevant common 更应该用 activation covariance 估计，还是用 cross-group gradient covariance 估计。

Primary anchor：`01_03_gradient_common_vs_activation_common_anchor.md`。

Anchor decision question：

```text
Is optimization-relevant common better explained by activation covariance or by cross-group gradient covariance?
```

Physical prior：activation energy 和 update interference 是不同物理对象。

Core model term：

\[
G_g^r(P)=\mathbb{E}[\delta_g((I-P)h)^\top\mid g]
\]

Primary metric：

```text
gradient_overlap_reduction_advantage
```

定义：

```text
P_grad 的 gradient-overlap reduction - P_act 的 gradient-overlap reduction
```

Basic setup：构造受控 hidden states，让 activation nuisance、functional shared common、gradient common、group-unique component 可以分开。

Configuration：hidden dimension 32，common rank 2，6 groups，20 seeds，每 group 500 samples。

Conditions：

```text
aligned_common
activation_nuisance
unique_variance
functional_gradient_split
entangled_residual
```

Pass：

```text
P_grad 在四个 mismatch regimes 中至少三个胜过 P_act，
并且 seed win rate >= 0.8。
```

Fail：

```text
P_act 在多数 mismatch regimes 中等于或胜过 P_grad。
```

Insufficient：

```text
random control 胜出，metric 符号不稳定，
或 shared-loss guard 显示比较被 target destruction 主导。
```

Cannot claim：

```text
不能 claim real-DCLM preservation rescue；
不能 claim residualized MoE utility；
不能 claim 最终 layerwise estimator。
```

Approval decision：执行 controlled full run。

## 1. 实验逻辑

我们要区分两个对象：

activation common：

\[
P_{\mathrm{act}}=\mathrm{TopEig}(\mathbb{E}[hh^\top])
\]

gradient common：

\[
G_g=\mathbb{E}[\delta_g h^\top\mid g]
\]

\[
P_{\mathrm{grad}}=\mathrm{TopEig}
\left(
\frac{1}{|G|(|G|-1)}\sum_{g\neq g'}G_g^\top G_{g'}
\right)
\]

如果 optimization-common 是 gradient object，那么移除 \(P_{\mathrm{grad}}h\) 应该比移除 \(P_{\mathrm{act}}h\) 更能降低跨 group 梯度重叠。

## 2. 数据构造

受控 hidden state：

\[
h = s_g A_g z_g + s_f A_f z_f + s_u B_g z_u + s_n A_n z_n + \epsilon
\]

其中：

- \(A_g\)：gradient-common basis；
- \(A_f\)：functional shared basis；
- \(B_g\)：group-unique basis；
- \(A_n\)：activation nuisance basis。

## 3. 指标

主指标：

```text
gradient_overlap_reduction_advantage
```

保护指标：

```text
shared_loss_sensitivity
gradient_common_alignment
functional_common_alignment
random_control_winner_check
```

## 4. 输出

预期输出：

```text
summary.md
detailed.md
tables/gradient_vs_activation_scores.csv
tables/gradient_vs_activation_summary.csv
tables/gradient_vs_activation_winner_summary.json
figures/gradient_overlap_reduction_by_regime.png
figures/gradient_advantage_by_regime.png
figures/criterion_winners_by_regime.png
```

## 5. Claim Boundary

这个实验只裁定 controlled activation-gradient mismatch 下的 estimator 机制分离。

它不能裁定真实 DCLM preservation，也不能证明 MoE 方法有效。

