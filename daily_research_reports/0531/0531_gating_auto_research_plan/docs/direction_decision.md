# Direction Decision: 0531 Gating Research

## 0. 结论

当前 gating 研究应继续沿着：

```text
route-function binding under compositional NTP synthetic
```

而不是：

```text
继续加 hierarchy depth
```

最小下一步是 router-factor attribution。目标是判断 ordinary flat / common_flat / current hierarchy 的 routing logits 到底由哪个因素控制。

## 1. 当前 safest claim

```text
当前 failure 不是单纯的 representation 不可分。slot / context feature 在 hidden state 中可见，oracle routing 可用，但 learned routing 不稳定地绑定到 utility-best experts。
```

因此要找的方法必须同时满足：

```text
feature alignment + causal expert utility + train stability + inference stability
```

## 2. 四条候选路线排序

### Route 1: router-factor attribution first（必须先做）

Mainline impact:

```text
- affects hypothesis? yes
- affects claim boundary? yes
- affects next decision? yes
- recommendation: pursue
```

问题：router logits 主要由 common / identity / head-frequency / slot 中哪一个控制？

决定后续路线：

```text
common/head dominates -> representation decomposition / whitening
utility collapse dominates -> explicit route-function binding objective
slot visible but expert utility absent -> expert write-in / tail reweight
all unclear -> metric or synthetic construction failure
```

### Route 2: representation decomposition / residual gating（优先候选）

Mainline impact:

```text
- affects hypothesis? yes
- affects claim boundary? yes
- affects next decision? yes
- recommendation: pursue after H0531a supports common/head dominance
```

候选方法：

```text
true common residual gate
PCA / learned common residual gate
router input whitening
frequency-balanced router normalization
common path + residual leaf router
```

核心判断：不是 residual 是否让 loss 下降，而是 residual 是否同时提高 route-slot NMI 和 forced expert utility diagonal。

### Route 3: explicit route-function binding regularizer（优先候选）

Mainline impact:

```text
- affects hypothesis? yes
- affects claim boundary? yes
- affects next decision? yes
- recommendation: pursue if H0531a shows route follows utility collapse or joint training fails to form expert utility
```

候选方法：

```text
stop-gradient utility target KL
counterfactual forced-expert responsibility matching
target-position binding margin
expert write-in pressure / tail reweight
```

核心判断：这个方法能否让 router 选中的 expert/path 成为 utility-best path，而不是只提高 CE。

### Route 4: nonlinear / prior router（后置候选）

Mainline impact:

```text
- affects hypothesis? unclear until factor attribution
- affects claim boundary? yes if successful
- affects next decision? yes after Routes 2/3 fail or only partially work
- recommendation: park until H0531a/H0531b/H0531c produce diagnosis
```

候选方法：

```text
small MLP router
bilinear factorized router
orthogonal / diversity-constrained linear router
semantic centroid init + anti-decay regularizer
route consistency augmentation
```

风险：非线性 router 可能靠 memorization 或 surface token identity 通过 synthetic，不一定提供可迁移 mechanism。

## 3. 不建议现在做的方向

### 不继续加 hierarchy depth

理由：现有证据显示 common path 有帮助，但 two-level hierarchy 本身没有稳定超过 common_flat。增加层数只会增加自由度，不能解释 routing 是由哪个 factor 控制。

### 不直接上真实语料

理由：当前 synthetic 中 route-function binding 还没稳定；真实语料会隐藏 factor ground truth，无法判断 failure 来自 routing、expert write-in、frequency、metric 还是数据构造。

### 不把 load balance 当主解

理由：load balance 可改善 expert load，但可能抹平 locality；它最多是 control / supporting ablation，不是 feature-level specialization 的主机制。

## 4. 目标陈述

最终目标不是找到一个 synthetic trick，而是找到一个满足下面合同的 routing mechanism：

```text
在 synthetic 中：
- 不同 target-deciding features 稳定分到不同 expert/path；
- route 与 expert causal utility 一致；
- 训练末期 route 不塌缩；
- 推理扰动下 route 稳定；
- Zipf/common feature stress 下不把所有 tail feature 压到同一路径。

迁移到真实训练前：
- 方法不依赖 synthetic label 才能运行；
- regularizer 或 normalization 可在真实 NTP 中计算；
- 只需要 hidden state、router logits、expert outputs、counterfactual/ablation diagnostics 或 batch statistics。
```
