# 0706 Meeting Brief：V2.2 静态 Feature-Family Dispatch

## 1. 我们今天回答了什么？

我们回答的是导师要求的 clean case：

```text
feature 频率均匀；
整体表示谱各向同性；
先不考虑训练动态和真实大模型；
只问静态路由能不能把 feature family 均衡、稳定地分给 experts。
```

我们的结论是：

```text
可以，但还需要一个关键条件：feature family 在局部必须可恢复。
```

所以完整答案不是：

```text
谱各向同性 -> 好路由
```

而是：

```text
谱各向同性提供干净 metric；
feature 频率均匀提供 mass balance 条件；
局部可恢复的 feature family 提供 specialization 条件。
```

## 2. V2.2 和 V1 有什么不同？

V1 讲的是连续几何：

```text
如果 feature direction 在球面上均匀，expert cell 又等测度，
那么 top-1 router 的 expert usage 均匀。
```

V2.2 讲的是 feature family：

```text
如果存在一组频率均匀、整体谱各向同性、局部可恢复的 feature families，
我们可以先恢复这些 families，
再把 families 均衡分给 experts。
```

一句话区别：

```text
V1 解决“几何 cell 的均匀 usage”；
V2.2 解决“离散 feature family 的静态均衡分发”。
```

## 3. 方法是什么？

方法叫 BFSR：Balanced Feature-Specializing Routing。

步骤：

```text
1. 在 calibration features 上做谱归一化 / whitening；
2. 用 k-means 从 features 中恢复 K 个 feature families；
3. 把 recovered families 均衡分配给 E 个 experts；
4. 新样本先判断属于哪个 family，再送到对应 expert。
```

这次不把 quantile 当主方法。

原因：

```text
quantile 能让 token 数均衡，
但可能把同一个 feature family 切碎。
```

所以 quantile 在 V2.2 里只是 baseline，用来说明：

```text
mass balance 不等于 feature specialization。
```

## 4. 实验说明了什么？

E1 positive clean case：

```text
BFSR-Cluster: LoadCV 0.003，family consistency 0.990，cluster accuracy 0.986。
```

说明：在 clean case 中，BFSR 可以做到均衡且保持 feature family。

E2 isotropy-only null：

```text
当 X 是 isotropic Gaussian，F 和 X 独立时，label-free 方法的信息量约 0.002。
```

说明：谱各向同性 alone 不够。

E3 recoverability sweep：

```text
separation 0.45 -> 2.50 时，cluster accuracy 0.063 -> 0.942，family consistency 0.294 -> 0.956。
```

说明：specialization 来自 local recoverability。

E4 whitening ablation：

```text
结构化数据被强各向异性扭曲后，whitening 让 cluster accuracy 0.250 -> 0.958；
null data 上 whitening 后信息量仍约 0.002。
```

说明：谱归一化是 metric repair，不是制造 feature identity。

E5 frequency ablation：

```text
frequency 不均匀时，equal-number BFSR LoadCV 0.149；
mass-aware BFSR LoadCV 0.029。
```

说明：feature 频率均匀是 equal-number family assignment 能 balance mass 的原因。

## 5. 现在能说什么？

可以说：

```text
我们已经完成了 uniform-spectrum clean case 下的静态 feature-family dispatch。
```

更准确地说：

```text
在整体谱各向同性、feature 频率均匀、feature family 局部可恢复的条件下，
BFSR 能构造一个静态、均衡、保持 feature family 的分发。
```

## 6. 现在不能说什么？

不能说：

```text
谱各向同性本身就能带来好路由；
BFSR 已经证明能让真实 MoE 学得更好；
BFSR 已经解决 learned router；
BFSR 已经解决训练过程中的 route preservation；
BFSR 已经能处理真实 LM hidden states；
K 可以自动选出来。
```

## 7. 下一步是什么？

我建议先做组会闭环，不急着继续加实验。

组会要讲清楚：

```text
我们把导师的 clean case 拆清楚了；
我们证明 isotropy alone 不够；
我们找到可解条件：local recoverability；
我们提出 BFSR；
E1--E5 支持这个静态结论；
边界是：还没到真实训练和真实 hidden states。
```

组会后再决定下一步。可能方向有三个：

```text
1. Static utility：这种 dispatch 是否真的让固定 expert 学得更好？
2. Real hidden-state audit：真实 LM hidden states 是否满足 local recoverability？
3. Training preservation：静态 partition 在训练中能否保持？
```

## 8. 一句话总结

```text
V2.2 不是证明“谱各向同性自动给出好路由”，
而是证明：在谱各向同性的 clean metric 下，
如果 feature family 频率均匀且局部可恢复，
我们可以恢复 family，并把 family 均衡分给 experts，
从而完成静态 feature-family dispatch。
```
