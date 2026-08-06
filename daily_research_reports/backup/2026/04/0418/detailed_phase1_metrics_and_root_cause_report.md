# `Phase 1` 指标解释与真实失效机理详细报告

## 1. 写这份报告的目的

这份报告解决两个问题：

1. `Phase 1` 到底做了什么，为什么我们可以说“真实模型里存在 shared head，而且去掉它以后更可分”。
2. 为什么这条主线在 toy 中成立，但到了真实 `Phase 2 / Phase 3` 里没有直接闭环。

本报告会明确对齐两个来源：

- `Phase 1` 真实代码实现：
  - [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:1)
- 你指出的理论参考：
  - [report.pdf](/data/250010109/spectral_router/exp_hierarchical/docs/report.pdf)

其中，`report.pdf` 的关键点是：它把全局 head removal 的收益写成了一个**条件命题**，而不是无条件定理。  
这个条件命题恰好是理解 `Phase 1` 成功、但 `Phase 2 / 3` 没有完全闭环的核心。

## 2. `Phase 1` 真正做了什么

### 2.1 `Phase 1` 不是训练实验，而是表示审计实验

`Phase 1` 没有训练大模型 backbone。  
它做的是一个表示层面的 audit：

1. 读取冻结的 `Qwen3-8B`
2. 在候选层抓取 hidden state
3. 用 `DCLM + WoS` 的混合协方差池估计 centered covariance
4. 取 centered covariance 的 top-`k` 主方向
5. 比较三种表示：
   - `raw`
   - `centered`
   - `tail_residual`
6. 在这些表示上测线性 probe、聚类一致性和 Fisher-style separability

因此，`Phase 1` 回答的问题不是：

> head removal 是否已经直接改善了真实语言建模。

而是：

> 在真实模型 hidden state 的几何里，是否存在一个共享高方差子空间；切掉它之后，表示是否更适合承载 WoS domain 语义。

### 2.2 hidden state 是在哪里取的

代码里取的是每层的 `post_attention_layernorm` 输出，位置在：

- [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:207)

这意味着 `Phase 1` 看的不是最终 logits 空间，而是：

> attention 已经完成，但 FFN 还没有重新混合之前的那一层中间表示。

这是一个合理的位置，因为它比较接近“router 可能真正看到的表征”。

### 2.3 数据是怎么进来的

`Phase 1` 同时用两类数据：

- `DCLM`
  - 作为 common / general 分布
- `WoS`
  - 作为 tail / domain 语义分布

其中：

- 协方差池是 `DCLM + WoS`
- 但 probe 与聚类评估是在 `WoS` 上做的

正式运行的关键规模是：

- `WoS covariance docs = 448`
- `DCLM sequences = 1792`
- `WoS train docs = 896`
- `WoS test docs = 896`

这些信息也保存在：

- [qwen3_8b_phase1_local_best_config.json](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/results/qwen3_8b_phase1_local/qwen3_8b_phase1_local_best_config.json:1)
- [qwen3_8b_phase1_seed2_best_config.json](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/results/qwen3_8b_phase1_seed2/qwen3_8b_phase1_seed2_best_config.json:1)

### 2.4 三种表示是怎样定义的

对一篇文档，设第 `t` 个 token 的 hidden state 是 `h_t`，文档长度是 `T`。  
`Phase 1` 实际比较的是文档级 pooled 表示。

`raw` 表示是：

$$
\phi_{\mathrm{raw}}(x)
=
\frac{1}{T}\sum_{t=1}^{T} h_t.
$$

`centered` 表示是：

$$
\phi_{\mathrm{centered}}(x)
=
\frac{1}{T}\sum_{t=1}^{T} (h_t - \mu),
$$

其中：

$$
\mu = \mathbb{E}[h]
$$

是由混合协方差池估计出来的全局均值。

如果 `V_k` 表示 centered covariance 的 top-`k` 特征向量，投影矩阵定义为：

$$
P_t = I - V_k V_k^\top,
$$

则 `tail_residual` 表示是：

$$
\phi_{\mathrm{tail},k}(x)
=
\frac{1}{T}\sum_{t=1}^{T} P_t (h_t - \mu).
$$

这和 `report.pdf` 中给出的定义是一致的。

## 3. `Phase 1` 到底测了哪些指标

### 3.1 谱结构指标：判断 shared head 是否存在

这是 `Phase 1` 的第一类证据。  
代码会先估计 centered covariance：

$$
\Sigma_c
=
\mathbb{E}\big[(h - \mu)(h - \mu)^\top\big],
$$

然后做特征分解，得到特征值：

$$
\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_d \ge 0.
$$

再计算前 `k` 个主方向的累计解释方差：

$$
E_k
=
\frac{\sum_{i=1}^{k} \lambda_i}{\sum_{j=1}^{d} \lambda_j}.
$$

如果某层存在显著的低秩 shared head，那么应该出现：

1. 很小的 `k` 就能解释很大比例的总方差
2. 这个谱结构跨 seed 稳定
3. 它在某些层明显强，在某些层明显弱

这就是“shared head 存在”的判据。

### 3.2 `Sep_F`：理论上定义的 Fisher-style separability

这部分直接对应 `report.pdf` 的定义。

设 `z` 是 WoS domain 标签，`\pi_c` 是类别先验，`\mu_c` 是条件均值。  
定义类间散度与类内散度：

$$
B_z
=
\sum_c \pi_c (\mu_c - \mu)(\mu_c - \mu)^\top,
$$

$$
W_z
=
\sum_c \pi_c \,\mathrm{Cov}(x \mid z=c).
$$

对于一个投影 `P`，`report.pdf` 把 separability 定义为：

$$
\mathrm{Sep}_F(P; z)
=
\frac{\mathrm{tr}(P B_z P^\top)}{\mathrm{tr}(P W_z P^\top)}.
$$

`Phase 1` 代码里实现的 `sep_trace` 正是这个量的一个实际计算版本，代码在：

- [run_phase1_probe.py](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/scripts/run_phase1_probe.py:87)

### 3.3 线性 probe：看是否更容易被简单分类器分开

`Phase 1` 还训练了一个 `LogisticRegression`：

$$
\hat y
=
\arg\max_c \big(W \phi(x) + b\big)_c,
$$

并在 WoS test 上报告 `probe_accuracy`。

这一步测的是：

> 在给定表示上，是否存在一个简单线性分类器可以把不同 domain 分开。

### 3.4 聚类纯度与 NMI：看无监督结构是否更对齐标签

`Phase 1` 还对 test 表示做了 `KMeans`，再和真实标签比较：

1. `cluster_purity`
2. `cluster_nmi`

它们回答的是：

> 就算不给监督分类头，表示自身的簇结构是否已经更贴近 WoS domain。

因此，`Phase 1` 不是只用一个指标，而是用四个不同角度的证据：

1. 谱结构
2. `Sep_F`
3. 线性 probe
4. 聚类质量

## 4. 为什么我们可以说 shared head 是真的存在

### 4.1 shared head 的数学含义

如果某层 hidden state 可以写成：

$$
h = U a + r,
$$

其中：

- `U` 是一个很低秩的正交基
- `a` 是沿这些方向的高方差坐标
- `r` 是其余残差

那么 centered covariance 就近似满足：

$$
\Sigma_c
=
U \Lambda U^\top + \Sigma_r,
$$

其中：

- `\Lambda` 的前若干个特征值很大
- `\Sigma_r` 的谱更平、更分散

在这种情况下，top-`k` 特征值会吞掉很大一部分总方差。  
这就是“shared head”的统计定义。

### 4.2 `Phase 1` 的实际证据

在 `Qwen3-8B` 两个正式 seed 中，谱结构几乎重合。

`layer 35`：

- seed1:
  - `top4 = 0.2974`
  - `top8 = 0.4069`
  - `top16 = 0.4822`
- seed2:
  - `top4 = 0.2968`
  - `top8 = 0.4070`
  - `top16 = 0.4824`

`layer 11`：

- seed1:
  - `top8 = 0.0561`
- seed2:
  - `top8 = 0.0558`

也就是说，同一个模型里：

$$
E_8(\text{layer 35}) \approx 0.407
$$

而

$$
E_8(\text{layer 11}) \approx 0.056.
$$

这说明：

1. `layer 35` 上存在非常强的低秩高方差结构
2. 这种结构不是随机噪声，因为跨两个正式 seed 都稳定
3. shared head 不是“所有层都一样强”，而是一个真正的层依赖现象

因此，`Phase 1` 说“shared head 存在”，主要靠的是**谱证据**，不是靠分类准确率本身。

## 5. 为什么我们可以说去掉 head 之后更可分

### 5.1 先说最严格的理论条件

`report.pdf` 已经把 head removal 的收益条件写得很清楚。  
设被删掉的子空间基为 `U`，定义：

$$
\delta_b
=
\mathrm{tr}(U^\top B_z U),
$$

$$
\delta_w
=
\mathrm{tr}(U^\top W_z U).
$$

其中：

- `\delta_b` 表示被删子空间里包含了多少类间语义信号
- `\delta_w` 表示被删子空间里包含了多少类内共享噪声

若原始 separability 是：

$$
\mathrm{Sep}_F(I; z)
=
\frac{\mathrm{tr}(B_z)}{\mathrm{tr}(W_z)},
$$

删掉这个子空间之后的 separability 是：

$$
\mathrm{Sep}_F(P_t; z)
=
\frac{\mathrm{tr}(B_z) - \delta_b}{\mathrm{tr}(W_z) - \delta_w}.
$$

head removal 会提升 `Sep_F`，当且仅当：

$$
\frac{\mathrm{tr}(B_z) - \delta_b}{\mathrm{tr}(W_z) - \delta_w}
>
\frac{\mathrm{tr}(B_z)}{\mathrm{tr}(W_z)}.
$$

把两边交叉相乘可得：

$$
\mathrm{tr}(W_z)\big(\mathrm{tr}(B_z) - \delta_b\big)
>
\mathrm{tr}(B_z)\big(\mathrm{tr}(W_z) - \delta_w\big),
$$

即：

$$
\mathrm{tr}(B_z)\delta_w
>
\mathrm{tr}(W_z)\delta_b.
$$

再整理成比例形式，就是 `report.pdf` 的条件：

$$
\frac{\delta_b}{\mathrm{tr}(B_z)}
<
\frac{\delta_w}{\mathrm{tr}(W_z)}.
$$

这条不等式的含义非常本质：

> 只有当被删掉子空间里“类内共享噪声的占比”大于“类间语义信号的占比”时，head removal 才应该提升可分性。

### 5.2 `Phase 1` 里更可分的结论，具体来自哪些指标

在两个正式 seed 的最佳层 `layer 35` 上：

seed1：

- `raw`
  - `probe_accuracy = 0.7522`
  - `cluster_purity = 0.5000`
  - `cluster_nmi = 0.3327`
  - `sep_trace = 0.2815`
- `centered`
  - `probe_accuracy = 0.7533`
  - `cluster_purity = 0.5000`
  - `cluster_nmi = 0.3327`
  - `sep_trace = 0.2815`
- `tail_residual` 最优 `k = 32`
  - `probe_accuracy = 0.7690`
  - `cluster_purity = 0.5681`
  - `cluster_nmi = 0.3975`
  - `sep_trace = 0.1043`

seed2：

- `raw`
  - `probe_accuracy = 0.7444`
  - `cluster_purity = 0.4766`
  - `cluster_nmi = 0.3400`
  - `sep_trace = 0.2757`
- `centered`
  - `probe_accuracy = 0.7400`
  - `cluster_purity = 0.4766`
  - `cluster_nmi = 0.3400`
  - `sep_trace = 0.2757`
- `tail_residual` 最优 `k = 16`
  - `probe_accuracy = 0.7511`
  - `cluster_purity = 0.5725`
  - `cluster_nmi = 0.4064`
  - `sep_trace = 0.2104`

这里有两个非常明确的事实：

1. `raw` 和 `centered` 几乎重合
2. `tail_residual` 在 `probe_accuracy / purity / NMI` 上稳定更好

因此，`Phase 1` 的“更可分”结论，主要来自：

- 线性 probe
- 聚类 purity
- 聚类 NMI

而不是来自 `sep_trace` 的单调提升。

### 5.3 为什么 `sep_trace` 没有同步变好，但我们仍然说“更可分”

这恰恰是最值得学习的地方。

在 `Phase 1` 的最佳配置上，`sep_trace` 反而下降了。  
这说明：

> `Sep_F` 的 trace-ratio 版本，并不是我们当前真实实验里最稳定的 operational witness。

这是可以严格解释的。

`Sep_F` 用的是：

$$
\frac{\mathrm{tr}(P B_z P^\top)}{\mathrm{tr}(P W_z P^\top)}.
$$

它对所有保留下来的方向做的是一种**各向同性平均**。  
但线性分类真正关心的，不是这个各向同性平均，而是判别方向上的广义信噪比。

对于二类情形，LDA 的判别强度更接近：

$$
\mathcal{M}(P)
=
(\mu_1 - \mu_2)^\top (P W P^\top)^\dagger (\mu_1 - \mu_2),
$$

其中：

- `\dagger` 表示广义逆

对多类情形，更接近广义特征值问题：

$$
P B_z P^\top v
=
\lambda \, P W_z P^\top v.
$$

也就是说，分类器更关心的是：

1. 某几个关键判别方向的广义信噪比
2. 而不是所有方向上 trace 的欧式平均

因此完全可能出现下面这种情况：

1. 删掉 head 时，也顺带删掉了一些类间能量，所以 `tr(PBP^\top)` 下降
2. 但删掉的类内 nuisance 更“卡脖子”，线性分类和聚类反而更容易
3. 于是 `probe_accuracy / purity / NMI` 提升，而 `sep_trace` 不升反降

这并不意味着 `Phase 1` 错了。  
它更准确地说明：

> 在真实大模型表征里，trace-ratio 版 `Sep_F` 只是一个粗粒度代理，而不是唯一可信的实践判据。

所以 `Phase 1` 的严格表述应该是：

1. shared head 的存在由谱结构支持
2. head removal 的实用收益由 `probe_accuracy / purity / NMI` 支持
3. `sep_trace` 在真实数据上的一致性不够强，这本身是下一步理论和指标设计要修补的地方

## 6. 为什么 toy 里成立，到了真实 `Phase 2 / 3` 却没有直接 work

下面进入更本质的失效分析。

## 6.1 原因一：toy 假设 tail 模块主要接受 tail 相关更新，但真实 `Phase 2 / 3` 不是这样

这是我现在认为最本质的一条。

在 toy 里，我们默认：

1. common 信号主要更新 common 参数
2. tail 信号主要更新 tail 参数
3. tail 更新稀疏，因此 WD 和 LR 会直接决定 tail 能否存活

但真实 `Phase 2` 代码里，tail 分支并不是只在 WoS / tail batch 上更新。  
训练损失是：

$$
L
=
L_{\mathrm{LM}} + \lambda_{\mathrm{dom}} \mathbf{1}_{\mathrm{WoS}} L_{\mathrm{dom}}.
$$

这里：

- 在 DCLM batch 上，`L_dom = 0`
- 但 `L_LM` 仍然会通过整个控制器反传

因此，对 tail 参数 `\theta_t`，期望梯度实际上是：

$$
\mathbb{E}[g(\theta_t)]
=
q \, \mathbb{E}\big[\nabla_{\theta_t} L_{\mathrm{LM}}^{\mathrm{DCLM}}\big]
+
(1-q)\,\mathbb{E}\big[\nabla_{\theta_t} L_{\mathrm{LM}}^{\mathrm{WoS}}\big]
+
(1-q)\lambda_{\mathrm{dom}} \,\mathbb{E}\big[\nabla_{\theta_t} L_{\mathrm{dom}}\big],
$$

其中：

$$
q = \frac{\text{DCLM ratio}}{\text{DCLM ratio} + 1}.
$$

在当前设置里：

$$
q = \frac{4}{5} = 0.8.
$$

这意味着 tail 分支的大部分更新，实际上仍由 common-side 的 `DCLM` 语言建模目标驱动。  
因此它不是 toy 里那种“稀疏收到更新的纯 tail 模块”，而更像是：

> 一个被迫同时服务于 common LM 和 tail domain 的共享控制器。

`Phase 3` 也是一样。  
虽然 router loss 只在 WoS batch 上打开，但 router 和 experts 在 DCLM batch 上仍然通过 LM loss 获得梯度，因为 expert mixture 直接影响 token logits。

对 `Phase 3` 的 router / tail experts 参数 `\theta_r`，期望梯度更接近：

$$
\mathbb{E}[g(\theta_r)]
=
q \, \mathbb{E}\big[\nabla_{\theta_r} L_{\mathrm{LM}}^{\mathrm{DCLM}}\big]
+
(1-q)\,\mathbb{E}\big[\nabla_{\theta_r} L_{\mathrm{LM}}^{\mathrm{WoS}}\big]
+
(1-q)\lambda_{\mathrm{router}} \,\mathbb{E}\big[\nabla_{\theta_r} L_{\mathrm{router}}\big].
$$

这条公式的含义非常重要：

> 真实 `Phase 2 / 3` 中的“tail 模块”根本不是 toy 里那个只等 rare signal 来养活自己的模块。

所以，toy 里关于 LR 和 WD 的动力学直觉，不能直接一比一平移到当前真实 proxy。

## 6.2 原因二：head removal 的收益是条件命题，不是无条件命题

toy 和理论都默认：

$$
\frac{\delta_b}{\mathrm{tr}(B_z)}
<
\frac{\delta_w}{\mathrm{tr}(W_z)}.
$$

但在真实模型里，并不保证这个不等式在所有层、所有任务上都严格成立。  
真实 hidden state 更像是：

$$
h = U a(x) + V b(x) + \varepsilon,
$$

其中：

- `U a(x)` 是 top-eigenspace 上的共享高方差部分
- `V b(x)` 是残差子空间中的 tail 语义

如果标签 `y` 对 `a(x)` 仍有条件依赖：

$$
I(y; a(x) \mid b(x)) > 0,
$$

那就说明被删掉的 head 里并不只是 nuisance，还混入了有效语义。

此时，若一个语义方向 `s` 与被删子空间的主夹角是 `\theta`，那么删掉之后保留下来的语义能量是：

$$
\|P_{U^\perp} s\|^2
=
\|s\|^2 \sin^2 \theta.
$$

当 `\theta` 不够大时，head removal 会直接损伤任务相关信息。

这就解释了为什么：

- `Phase 1` 在 domain 区分上有收益
- 但 `Phase 2 / 3` 的 generative 指标并不总是一起变好

因为语言建模需要的有效信息，未必完全位于 tail residual 中。

## 6.3 原因三：`Phase 1` 的“更可分”是文档级结论，而 `Phase 2 / 3` 优化的是 token 级目标

`Phase 1` 的表示是文档级 mean pooling：

$$
\bar h
=
\frac{1}{T}\sum_{t=1}^{T} h_t.
$$

若 token 级噪声近似独立，则：

$$
\mathrm{Var}(\bar h)
\approx
\frac{1}{T}\mathrm{Var}(h_t).
$$

也就是说，文档级 pooling 会显著降低噪声。

因此，`Phase 1` 其实更接近在问：

> 一篇文档整体落在什么语义簇里。

但 `Phase 2 / 3` 训练的是 token-level next-token loss。  
它们更接近在问：

> 某个具体 token 在局部上下文里，是否能因为这个单层控制器而更好地预测下一个 token。

这两者之间并没有严格等价关系。

所以：

- `Phase 1` 成功
- `Phase 2 / 3` 不完全成功

并不矛盾。  
它只能说明：

> 文档级几何优势已经存在，但单层 token-level 控制器还没有稳定把这份优势吃成真实训练收益。

## 6.4 原因四：当前 `Phase 2 / 3` 的控制器容量受限，逼近误差可能盖过几何收益

真实 `Phase 2 / 3` 不是对整个 backbone 做改造，而是只插一个单层 low-rank 控制器。  
如果理想修正映射是 `M^\star`，但我们只能用秩不超过 `r` 的映射：

$$
M = B A,
\qquad
\mathrm{rank}(M) \le r,
$$

那么根据 Eckart-Young 定理，最佳低秩逼近误差满足：

$$
\inf_{\mathrm{rank}(M)\le r} \|M - M^\star\|_F^2
=
\sum_{i>r} \sigma_i(M^\star)^2,
$$

其中：

- `\sigma_i(M^\star)` 是 `M^\star` 的奇异值

这条式子的意思是：

> 如果真正需要的修正不是低秩且不是单层局部可实现，那么再好的几何也可能被控制器容量瓶颈掩盖。

当前真实 proxy 同时有四个强约束：

1. 只改一层
2. 只在 `post-attention / pre-FFN` 注入
3. low-rank 很小
4. backbone 完全冻结

因此完全可能出现：

- `Phase 1` 已经找到对的几何方向
- 但 `Phase 2 / 3` 这套小模块没有足够表达能力去兑现它

## 6.5 原因五：辅助目标与 LM 目标的梯度可能不对齐

`Phase 2 / 3` 的总损失都是：

$$
L = L_{\mathrm{LM}} + \lambda L_{\mathrm{aux}}.
$$

于是总梯度是：

$$
\nabla_\theta L
=
\nabla_\theta L_{\mathrm{LM}}
+
\lambda \nabla_\theta L_{\mathrm{aux}}.
$$

如果两者夹角满足：

$$
\cos \angle
\big(
\nabla_\theta L_{\mathrm{LM}},
\nabla_\theta L_{\mathrm{aux}}
\big)
<
0,
$$

那就意味着：

1. 辅助目标想往一个方向推
2. LM 目标想往相反方向推

这时就会出现我们已经观察到的典型现象：

- domain / purity 指标有改善
- 但 `ppl` 变差

或者：

- 为了保住 `ppl`
- 系统自动压制本该形成 specialization 的 tail 分工

因此，当前真实结果里“指标不是同向一起提升”，从优化角度看并不奇怪。

## 6.6 原因六：`WD + LR` 同时解耦，在真实 noisy 梯度里会放大不稳定性

你已经明确说了，现阶段不应该继续把 `learning rate` 和 `weight decay` 绑在一起解决。  
我同意，而且这个结论可以写得更严格。

考虑一个一维近似的随机更新：

$$
\theta_{t+1}
=
(1 - \eta \gamma)\theta_t
- \eta \bar g
- \eta \xi_t,
$$

其中：

- `\eta` 是学习率
- `\gamma` 是 weight decay
- `\bar g` 是平均有效梯度
- `\xi_t` 是零均值梯度噪声

这可以看成一个离散 Ornstein-Uhlenbeck 过程。  
在小步长近似下，其稳态方差满足：

$$
\mathrm{Var}[\theta]
\approx
\frac{\eta \, \mathrm{Var}[\xi]}{2\gamma}.
$$

这条式子的含义非常直接：

1. 提高学习率 `\eta` 会放大稳态方差
2. 降低 weight decay `\gamma` 也会放大稳态方差
3. 如果两件事一起做，方差会被双重放大

所以，当我们把 `WD` 和 `LR` 同时朝“更容易让 tail 长大”的方向推时，真实结果未必是“更好学”，也可能是：

> 更高噪声、更大范数、更不稳定。

这和 `Phase 2` 里观察到的现象高度一致：

- `split_decoupled_optim` 的 `tail_branch_norm` 远大于 `split_coupled_optim`
- 但指标并没有更好

这说明 tail 分支不是“没长起来”，而是“长偏了”。

因此，现阶段更合理的研究策略是：

1. 先把 `LR` 因子固定住
2. 只研究 `WD-only decoupling`
3. 看看是否能够在不过度放大噪声的前提下，保住 tail 相关参数

这也是为什么我认为当前 `Phase 3` 里最值得继续保留的是：

$$
\text{tail residual router} + \text{WD-only decoupling}.
$$

## 6.7 原因七：`Phase 3` 的监督目标并不等于真实 specialization 目标

`Phase 3` 的 router 监督本质上是：

$$
L_{\mathrm{router}}
=
\mathrm{CE}(r(x), y_{\mathrm{domain}}),
$$

即让 router 去预测 WoS domain 标签。

但真正有利于语言建模的 expert specialization，优化目标更接近：

$$
E^\star
=
\arg\min_E
H(X_{t+1} \mid C, E),
$$

其中：

- `C` 是上下文
- `E` 是 expert assignment
- `X_{t+1}` 是下一个 token

这两个目标只有在一个很强的条件下才等价：

$$
X_{t+1}
\perp E
\mid
(C, Y_{\mathrm{domain}}).
$$

也就是说，只有当 domain 标签已经是“预测模式”的充分统计量时，最大化 domain purity 才等于最大化真正的 expert specialization。

真实语言里这个条件通常不成立。  
因此完全可能出现：

1. 相对 `domain` 标签的 purity / NMI 变好了
2. 但真正的 LM 并没有因此更好

或者反过来：

1. 某种 routing 对 LM 更好
2. 但它不一定最对齐 WoS 的人工 domain 标签

所以 `Phase 3` 现在测到的是一个**supervised proxy**，而不是 specialization 的真值。

## 7. 当前最本质的结论应该怎么写

我会把目前整个 `exp_hierarchical` 的状态压成下面这三条。

### 7.1 关于 `Phase 1`

`Phase 1` 的结论是成立的，而且是比较扎实的：

1. shared head 在真实 `Qwen3-8B` hidden state 中确实存在
2. `raw -> centered` 不是关键
3. `tail_residual` 在操作性指标上更有利于 domain 区分

但这条结论的最准确表述应该是：

> `Phase 1` 证明了几何主线成立，不是证明了 head removal 会自动改善真实 generative training。

### 7.2 关于 `Phase 2 / Phase 3`

真实实验没有直接复现 toy 的强版本，不是因为主线被推翻，而是因为下面几个条件同时失真了：

1. tail 模块并没有被真正“tail-only”地训练
2. 删除的 head 并不一定纯粹是 nuisance
3. 文档级几何优势不等于 token-level 训练优势
4. 单层 low-rank 控制器的表达能力有限
5. `domain/router` 监督目标和 LM 目标不完全一致

### 7.3 关于下一步策略

基于以上分析，当前最合理的研究收缩是：

1. 暂时把 `LR` 因子冻结，不和 `WD` 一起继续扫
2. 主线收缩到 `WD-only decoupling`
3. 保留 `tail residual router`
4. 优先重做 `Phase 3` 的 objective，而不是继续沿用当前 domain-supervised proxy 放大算力

## 8. 我建议你现在怎么读这几个文档

如果你现在最关心“从理论到实现的闭环理解”，建议按这个顺序看：

1. [report.pdf](/data/250010109/spectral_router/exp_hierarchical/docs/report.pdf)
2. [这份详细报告](./detailed_phase1_metrics_and_root_cause_report.md)
3. [Phase 1 正式报告](/data/250010109/spectral_router/exp_hierarchical/phase1_real_representation_probe/docs/report_qwen3_8b_phase1_local.md:1)
4. [长程 `Phase 2` 报告](/data/250010109/spectral_router/exp_hierarchical/phase2_split_ffn_decoupling/docs/report_local_1h_len256.md:1)
5. [长程 `Phase 3` 报告](/data/250010109/spectral_router/exp_hierarchical/phase3_hierarchical_moe/docs/report_local_1h_len256.md:1)

如果后面你愿意，我下一步可以继续把这份报告再往前推进一层，直接写成：

> “为什么当前 `Phase 2 / Phase 3` 的 loss 设计不等价于我们真正想验证的理论命题”

也就是把现在的根因分析进一步变成一份**下一轮实验重设计文档**。
