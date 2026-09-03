# 01_03 Anchor：Gradient Common vs Activation Common


## 1. Problem Definition

**Parent problem：** common 可能覆盖 proxy routing、削弱 expert specialization，但在方法使用 common 前，必须先定义 common 的机制。

**Sharper subproblem：** 判断 optimization interference 相关的 common 更接近 activation covariance common，还是 cross-group gradient common。

**Decision question：**

```text
Is optimization-relevant common better explained by activation covariance or by cross-group gradient covariance?
```

**Not in scope：** real-DCLM preservation rescue、最终 MoE 架构、layerwise common role、utility claim。

## 2. Physical Priors

**P1：** activation energy 和 update interference 是不同物理对象。

含义：高方差 hidden-state 方向可以与 group-gradient overlap 无关；低方差 shared direction 反而可以支配更新。

**P2：** useful shared common 和 harmful optimization common 可以不同。

含义：一个方向可以对 shared prediction 有用，但不是造成 redundant group update 的主方向。

## 3. Falsifiable Hypotheses

**H1：** gradient-intersection common 更能解释 optimization interference。

支持条件：$P_{\mathrm{grad}}$ 在多数 activation-gradient mismatch regimes 中比 $P_{\mathrm{act}}$ 有更高 `gradient_overlap_reduction`。

削弱条件：$P_{\mathrm{act}}$ 在同一指标上等于或超过 $P_{\mathrm{grad}}$。

**H2：** useful shared common 和 gradient common 可以分离。

支持条件：functional shared estimator 赢 shared-loss sensitivity，而 $P_{\mathrm{grad}}$ 赢 gradient-overlap reduction。

## 4. Mathematical Model

activation common：

$$
C_h=\mathbb{E}[hh^\top], \qquad
P_{\mathrm{act}}=U_k U_k^\top
$$

gradient common：

$$
G_g=\mathbb{E}[\delta_g h^\top\mid g]
$$

$$
C_{\cap}=\frac{1}{|G|(|G|-1)}
\sum_{g\neq g'}G_g^\top G_{g'}
$$

$$
P_{\mathrm{grad}}=V_k V_k^\top
$$

残差化后：

$$
G_g^r(P)=\mathbb{E}[\delta_g((I-P)h)^\top\mid g]
$$

主指标：

$$
\Delta C(P)=\overline{\cos(G_g,G_{g'})}
-\overline{\cos(G_g^r(P),G_{g'}^r(P))}
$$

## 5. Minimal Test

受控构造 activation-gradient mismatch regimes，然后比较：

- activation PCA；
- gradient intersection；
- functional shared；
- random control。

主指标：

```text
gradient_overlap_reduction_advantage
```

Pass：

```text
P_grad 在多数 mismatch regimes 中稳定胜过 P_act。
```

Fail：

```text
P_act 在 optimization metric 上等于或胜过 P_grad。
```

Insufficient：

```text
random control 胜出，或者 shared-loss guard 显示比较被目标破坏主导。
```

## 6. Claim Boundary

可以 claim：

```text
在受控 activation-gradient mismatch 中，gradient common 是否比 activation common 更解释 optimization interference。
```

当前结果：

```text
n_passed_mismatch_regimes = 4 / 4
```

四个 mismatch regimes 中，$P_{\mathrm{grad}}$ 都比 $P_{\mathrm{act}}$ 更能降低 cross-group gradient overlap，seed win rate 都是 1.0。

功能性 guard：

```text
functional_gradient_split 中，
functional_shared 赢 shared_loss_sensitivity = 8.5791，
gradient_intersection 赢 gradient_overlap_reduction = 0.6494，
且 gradient_intersection 的 shared_loss_sensitivity 只有 0.0037。
```

解释：

```text
useful shared common 和 optimization-interference common 可以分离；
下一步应把 gradient common 带入 functional/feedback bridge。
```

不能 claim：

```text
真实 DCLM preservation rescue；
最终 MoE 方法；
所有层的 common estimator；
utility improvement。
```

下一步：

```text
进入 functional/feedback bridge；
检验 gradient common 是 useful shared structure、harmful redundant update signal，
还是 step0 到 step5/10 proxy-route collapse 的 contributor。
```
