# V2.2 Reading Guide

目的：帮助快速读懂 V2.2 文章，不把它误读成“谱各向同性自动产生好路由”。

## 一句话故事线

V2.2 回答的是：

```text
在 feature 频率均匀、整体谱各向同性的 clean case 中，
如果 feature family 在局部是可恢复的，
我们可以先恢复 feature family，
再把 family 均衡分配给 experts，
从而得到静态、均衡、保持 feature family 的分发。
```

## 阅读顺序

## 1. 先读 Abstract

你要抓住四个点：

```text
问题：静态 feature-family dispatch
否定：谱各向同性 alone 不够
条件：还需要 local recoverability
方法：BFSR = normalize -> cluster -> assign -> route
```

不要把 abstract 里的结果理解成“训练收益”。当前结果只支持静态分发。

## 2. 读 Introduction

Introduction 要回答：为什么 load balance 不等于 specialization。

核心理解：

```text
batch-level count balance 可以让专家数目均衡，
但它不一定让同一个 feature family 稳定地去同一个 expert。
```

V2.2 的目标不是“每个 expert token 数相等”这么弱，而是：

```text
每个 feature family 尽量完整地分到某个 expert，
同时 expert 总体负载均衡。
```

## 3. 读 Controlled Static Setting

这里定义 clean case：

```text
F ~ Uniform({1,...,K})
X | F=k = mu_k + eps
Cov(X_tilde) ≈ I
```

三个条件分别有不同作用：

```text
F uniform        -> 可以通过均衡 family assignment 得到 load balance
Cov isotropic    -> 给 clustering 一个干净 metric
recoverability   -> 让 feature-family dispatch 可识别
```

最重要的是：谱各向同性不是 feature identity 的来源。

## 4. 读 Static Good Dispatch

文章不使用 naive purity 作为主指标，因为通常 `K > E`。

例如 `K=32, E=4` 时，一个 expert 必然接收多个 feature families。此时 expert 内部有多个 family 是正常的。

主指标是：

```text
LoadCV: expert usage 是否均衡
Family consistency: 每个 family 是否主要去同一个 expert
Split rate: 一个 family 是否被切碎
I(G;F)/H(G): expert identity 是否携带 feature-family 信息
```

## 5. 读 Proposition 1

这是整篇文章的逻辑支点：

```text
如果 X ~ N(0,I)，F 与 X 独立，
那么任何 g(X) 都无法恢复 F。
```

所以：

```text
spectral isotropy alone 不能推出 feature specialization。
```

这一步把错误故事线堵死了。

## 6. 读 BFSR 方法

BFSR 很简单：

```text
fit whitening on calibration X
run k-means to recover K feature families
assign recovered families to experts evenly
route new examples by recovered family id
```

这里最重要的改变是：

```text
mass 不是靠 quantile 负责；
mass 来自 uniform family frequency + balanced family assignment。
```

Quantile-SPR 现在只是 baseline，用来说明：

```text
能 balance mass 不代表能 preserve feature families。
```

## 7. 读 Theory

理论只证明静态问题：

```text
Theorem 2: family 频率均匀 + 每个 expert 分到同样多 family -> expert mass 均衡
Theorem 3: family recovery error <= eta -> mass error <= eta
Theorem 4: family recovery error 控制 specialization error
```

这些理论不涉及训练动态。

## 8. 读 Experiments

实验逻辑是一个 anchor chain：

```text
E1: positive clean case 能成功
E2: isotropy alone 不能成功
E3: recoverability 越强，specialization 越强
E4: whitening 是 metric repair，不是制造 feature identity
E5: frequency uniformity 是 equal-number assignment 的 mass 条件
```

## 9. 最后读 Discussion / Limitations

这里必须记住边界：

```text
不解决真实 LM hidden states
不解决 learned router
不解决 training preservation
不解决 downstream utility
不解决 automatic K selection
```

## 和 V1 的区别

V1：

```text
如果 feature direction 在球面均匀，且 expert cells 等测度，
那么 top-1 routing usage 均匀。
```

V2.2：

```text
如果 feature families 频率均匀、整体谱各向同性、且 family 局部可恢复，
那么可以恢复 family，再把 family 均衡分给 experts，
得到静态 feature-family dispatch。
```

V1 是 continuous geometry mass result。

V2.2 是 discrete feature-family dispatch result。

## 当前结论

可以说：

```text
我们完成了 clean uniform-spectrum case 下的静态 feature-family dispatch。
```

不能说：

```text
我们已经证明 MoE 能学得更好。
我们已经解决真实 hidden state routing。
我们已经解决训练中的 route preservation。
```
