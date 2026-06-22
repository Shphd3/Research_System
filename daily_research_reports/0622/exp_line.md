父问题：

uniform feature分布下，随机初始化的dot-product top-1 MoE为什么不能自然形成feature level的specialization？

↓

Anchor0603回答什么

如果输入本身是均匀高维分布，那么 random Gaussian dot-product gate 为什么仍有固定 load imbalance？

结论：
1. 在高维空间中，不同向量近似正交，因此由于gating centering方向分布不均的load imbalance减弱
2. 对于正式使用的dot-product，存在gating row-norm variation，这个因素会加剧load imbalance

作用：
为后续实验提供一个baseline和最理想情况，将最理想情况的机制拆解，从而分离出后续实验中出现 imbalance 情形可能的导致原因和机制。

↓

Anchor0604回答什么

当 uniform symbolic features 经过 embedding / transformer hidden-state formation 后，step-0 load imbalance 还是 row norm 主导吗？

结论：
1. 在这种情形下，hidden common component是synthetic hidden-state 情形下更显著的导致gating imbalance的主因。0603中的row-norm不是主因

作用：
1. 将实验推进到了real hidden state中，并且将row norm的imbalance作用程度收束，主机制转向了hidden-state common component. 
2. 同时保持推进，因为去掉common component，仍然存在imbalance，从而驱动我们去探究residual部分的导致imbalance来源

↓

Anchor0605回答什么

去掉 hidden common component 后，剩余 load 是 finite-sample noise，还是还有真实 residual geometry？

结论：
residual covariance 不是各向同性，这也致使了去掉common部分后的imbalance的产生

作用：
1. 对“centering 解决了初始化几何问题” 这个说法进行了严格化，防止过早得出错误结论

↓

Anchor0606回答什么

在 A06_05 的 residual geometry 仍存在的情况下，如果给 oracle feature labels / centroids，feature-level routing partition 是否可达？

结论：
可达。oracle feature centroid 可以做到 perfect held-out feature routing。

作用：
证明目标 partition 本身不是不可能；如果后面 label-free 方法失败，失败原因是方法没有找到 partition，而不是 partition 不存在。


↓

Anchor0607回答什么
不用 labels，只做 global common-centering / projection / whitening，能不能接近 A06_06 的 oracle partition？

结论：
不能。它们能显著改善 load，但几乎不改善 feature_NMI；whitening 甚至让 NMI 崩掉。

作用：
纠正了一个以往的错误观念：更加load balance不意味着feature的specialization的达成

↓

现在知道什么

1. uniform feature 不保证uniform routing，更不保证feature specialization
2. gate-only中，row-norm variance是另一个可以分离出的imbalance 机制
3. common是一个很大的load imbalance的source
4. common-centering之后，residual geometry仍然存在
5. label-free common/residual control还是找不到 pure feature partition

↓

还不知道什么

1. 是否存在label-free的discovery能够找到pseudo-feature的中心
2. 初期训练动力学：即使初始化找到了pseudo-feature centers，是否，初期训练是否能够保持这种partition和feature specialization
3. real dclm中，应该使用的是什么作为feature的定义
4. common control在真实训练中的作用：是否只能作为load的guard，但是主方法还需要进一步推理

↓

下一步最自然去哪

A. feature discovery before routing
在 residual hidden states 上做 clustering / dictionary learning / contrastive feature estimation，先找到 pseudo-feature centers，再初始化 router。

B. anti-lockin after partition
从 oracle 或 pseudo-oracle partition 出发，测试 top-1 training 什么时候破坏这个 partition，以及需要什么 anti-lockin 机制保护它。

如果进入 DCLM，必须先定义 feature/proxy specialization metric，不能只看 load。