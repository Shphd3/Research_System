# 理论澄清与明日汇报锚点

日期：2026-07-16

状态：AI 理论审计；不是研究者判断、正式 anchor 或实验 Protocol。

英文 companion：
[05_theory_clarification_and_meeting_anchor.md](05_theory_clarification_and_meeting_anchor.md)

## 0. 先给结论

明日主题应固定为：

> **Matched shared-aux 对照下，informative-MTP 是否给低频潜在特征产生了
> 对标准 NTP 主头局部有用的 common-orthogonal 更新？**

最小可交付不是“证明 MTP 有用”，而是关闭以下认识：

> **新方向、rare 对齐和实际功能改善是三个不同命题。**
> MTP 只有在 matched 对照下产生信息特异增量，并且该增量通过曲率修正的真实
> 一步 rare-loss 检验与 common guard，才能被称为“对标准头局部有用”。

录音确实要求比较 next-one 与 next-two、探索混合表征能否更容易拆分，并最终
服务不同类型/频率特征的专家分配；但录音没有给出“MTP 已能解决
common/rare”的结论。当前 low-hanging fruit 正是把这条连接降到同一参数点的
matched 局部效应。

## 1. 三条原认识的审计

### 认识一

原句：

> “大奇异方向可能是某个学得慢的语义特征，后来受到 common 特征促进。”

**保留：**它可以作为待检验的语义解释。
**否定：**不能由大激活奇异值或大权重奇异值推出“学得慢”“语义”“受到
common 促进”。
**未知：**该方向对应 batch mean、尺度、频率、架构偏置，还是一个功能潜变量。

修正后：

> 大激活奇异值只说明当前表征二阶矩在该方向能量大；大权重奇异值只说明线性
> 变换增益大。只有在显式线性模型中附加条件后，它们才可能与优化曲率相关；
> 一般情况下都不等于 Hessian/Fisher 特征值，也不决定学习速度。

### 认识二

原句：

> “rare 学不到可能分为更新慢和 common/rare 梯度冲突。”

**保留并收紧：**这是正确的 rival 拆分，但至少还要加“正向复用”。
**否定：**方向不同或 cosine 小，不自动等于破坏性冲突。
**未知：**现有 rare 失败主要由频率、负梯度、曲率、容量还是接口造成。

修正后：

> rare 可以因出现概率小而只有微弱正更新，也可以因 common 的负内积被高频
> 放大而停滞/倒退；若内积为正，common 反而帮助 rare。有限步长下还必须检查
> 曲率，因为一阶方向正确也可能因步长过大而失败。

### 认识三

原句：

> “区分 MTP 放大旧方向还是产生新方向，可以观察 MTP 梯度与 common 的对齐
> 程度和梯度模长。”

**部分保留：**投影和模长可用于描述几何。
**否定：**raw MTP gradient、common 对齐和模长不足以识别信息效应，也不足以
证明帮助 rare。
**未知：**信息特异增量能否在真实一步中改善标准头 rare loss。

修正后：

> 必须先做 matched shared-aux 差分
> $\Delta g_{\mathrm{info}}=G_{\mathrm{informative}}-G_{\mathrm{shared}}$。
> $E_\perp$ 判断是否出现 common 子空间外的新分量，$A_R$ 判断一阶 rare
> 对齐；最终仍需曲率修正和真实一步 $\Delta I_R$。

## 2. 对象与假设

### 2.1 对象

- $\theta$：普通 NTP 主头可访问的共享参数；不含 auxiliary-only 参数。
- $L_C(\theta)$、$L_R(\theta)$：在预先冻结的 common/rare 数据上，由普通
  NTP 主头计算的评价损失。
- $\pi_C,\pi_R$：训练分布中两类的质量，通常 $\pi_C\gg\pi_R$。
- $g_C=\nabla_\theta L_C$，$g_R=\nabla_\theta L_R$。
- $H_C=\nabla_\theta^2L_C$，$H_R=\nabla_\theta^2L_R$。
- $P_C$：在当前 checkpoint 上，由 common 样本的参数梯度协方差或 empirical
  Fisher top eigenspace 构造并冻结的正交投影。

注意：这里的 empirical Fisher 是梯度外积统计，不在一般神经网络中等于真实
Hessian。激活 covariance 子空间可作辅助诊断，权重 SVD 只能作解释，二者不能
替代 $P_C$。

### 2.2 局部理论假设

1. $L_C,L_R$ 在分析点邻域内二阶可微；若使用三阶余项，则三阶导数局部有界。
2. 所有条件在同一个参数点、同一批冻结评价数据上计算。
3. informative-MTP 与 shared-aux 的活跃头数、CE 项数、名义 loss scale 和
   可更新共享参数相同。
4. $P_C$ 的构造规则、rank 和稳定性阈值在观察结果前固定。
5. 理论结论只描述局部一步或局部二次模型，不声称覆盖完整 Transformer 轨迹。

## 3. 谱动力学：什么能推出“学得快”

### Lemma 1：局部二次模型的谱收敛

设局部损失为

$$
L(\theta^\star+e)
=\frac12e^\top He,
\qquad H=Q\operatorname{diag}(\lambda_i)Q^\top,
$$

且 $H\succeq0$。梯度下降满足

$$
e_{t+1}=(I-\eta H)e_t,
\qquad
e_{t+1,i}=(1-\eta\lambda_i)e_{t,i}.
$$

**证明。**把 $e_t$ 展开到 $H$ 的正交特征基，逐坐标应用
$e_{t+1}=e_t-\eta He_t$ 即得。$\square$

**含义与边界：**

- 当 $0<\eta<2/\lambda_{\max}$ 时局部稳定；
- 当 $0<\eta\leq1/\lambda_{\max}$ 时，各正曲率坐标单调收缩，较大的
  $\lambda_i$ 通常更快；
- $\lambda_{\max}$ 限制全局稳定步长；
- 若 common 与 rare 的有效曲率满足 $\lambda_C\gg\lambda_R>0$，取
  $\eta=O(1/\lambda_C)$ 后，rare 每步收缩约为
  $1-O(\lambda_R/\lambda_C)$，形成 stiff dynamics；
- $\lambda_i=0$ 时局部二次模型不给该方向学习信号；负曲率不是这里的收敛模态。

“大激活/权重奇异值 $\Rightarrow$ 大 $\lambda_i$”一般不成立。只有在特定线性
平方损失模型中，Hessian 才可能由输入 covariance 以可写出的张量结构决定；
Transformer 交叉熵下不能偷换。

## 4. 频率饥饿、冲突与复用

NTP 训练梯度为：

$$
G_N=\pi_Cg_C+\pi_Rg_R.
$$

### Lemma 2：rare 的一阶下降驱动力

对一步 $\theta'=\theta-\eta G_N$，

$$
L_R(\theta')=L_R(\theta)-\eta D_R+O(\eta^2),
$$

其中：

$$
D_R
=\langle g_R,G_N\rangle
=\pi_R\|g_R\|^2+\pi_C\langle g_R,g_C\rangle.
$$

**证明。**对 $L_R$ 作一阶 Taylor 展开并代入 $G_N$。$\square$

据此可分：

- **正向复用：**$\langle g_R,g_C\rangle>0$，common 更新一阶上帮助 rare。
- **频率饥饿：**$\langle g_R,g_C\rangle\approx0$ 且 $\pi_R$ 小，
  $D_R\approx\pi_R\|g_R\|^2>0$，rare 仍学但很慢。
- **负冲突：**$\langle g_R,g_C\rangle<0$。
- **停滞或倒退：**

$$
\pi_C[-\langle g_R,g_C\rangle]_+
\geq\pi_R\|g_R\|^2
\quad\Longleftrightarrow\quad D_R\leq0.
$$

若只看到 rare 学得慢而没有 cross term，就不能声称冲突。

## 5. MTP 改变了什么

对 $K$ 个预测距离的加权损失：

$$
L_{\mathrm{MTP}}=\sum_{k=1}^K\lambda_kL_k,
\qquad
G_{\mathrm{MTP}}=\sum_{k=1}^K\lambda_kg_k,
\qquad
H_{\mathrm{MTP}}=\sum_{k=1}^K\lambda_kH_k.
$$

梯度与 Hessian 的可加性来自微分的线性性，在固定参数点精确成立。若把 Fisher
或 empirical Fisher 代替 Hessian，必须另行说明近似，不能写成恒等式。

为了隔离未来信息，定义：

$$
\Delta g_{\mathrm{info}}
=G_{\mathrm{informative}}-G_{\mathrm{shared}}.
$$

其中 shared-aux 重复 next-token 信息，并匹配 active heads、CE 项数和名义
scale。

令：

$$
A_R=\langle g_R,\Delta g_{\mathrm{info}}\rangle,
$$

$$
E_\perp
=\frac{\|(I-P_C)\Delta g_{\mathrm{info}}\|^2}
{\|\Delta g_{\mathrm{info}}\|^2+\epsilon}.
$$

四种局部情况：

| 情况 | 观测 | 允许的解释 |
| --- | --- | --- |
| 只放大/复用 common | $E_\perp\approx0$，增量主要落在 $P_C$ | 没有新方向；是否帮助 rare 仍看 $A_R$ 与功能量 |
| 提高已有 rare 速率 | $A_R>0,E_\perp\approx0$ | 在已有子空间内帮助 rare，不支持“分离新方向” |
| 候选新 rare 方向 | $A_R>0,E_\perp>0$ | 新且一阶对齐；仍需曲率、真实一步和 common guard |
| 新冲突/无关方向 | $A_R\leq0,E_\perp>0$ | 几何上新，但不支持帮助 rare，可能有害或是 nuisance |

若 $A_R$、$E_\perp$ 都不显著，当前参数点没有信息特异的局部机制证据。

### Lemma 3：共享子空间封闭性

若分析邻域内

$$
g_C,\;g_R,\;G_{\mathrm{shared}},\;G_{\mathrm{informative}}
\in\operatorname{range}(P_C),
$$

则它们的任意线性组合仍在 $\operatorname{range}(P_C)$，因此局部更新不能产生
$P_C$ 正交补中的分量。

**证明。**线性子空间对加法与标量乘法封闭。$\square$

它只是不可能性条件；$E_\perp>0$ 也不保证该方向对 rare 有用。

## 6. Main proposition：曲率修正的一步功能效应

定义普通标准头 rare loss 的一步改善：

$$
I_R(G)=L_R(\theta)-L_R(\theta-\eta G).
$$

令 $G_i=G_{\mathrm{informative}}$，
$G_s=G_{\mathrm{shared}}$。则：

### Proposition

在第 2.2 节假设下，

$$
\Delta I_R
=I_R(G_i)-I_R(G_s)
$$

满足：

$$
\Delta I_R
=
\eta A_R
-\frac{\eta^2}{2}
\left(
G_i^\top H_RG_i-G_s^\top H_RG_s
\right)
+O(\eta^3).
$$

### Proof

分别对 $L_R(\theta-\eta G_i)$ 与
$L_R(\theta-\eta G_s)$ 在同一 $\theta$ 作二阶 Taylor 展开：

$$
L_R(\theta-\eta G)
=L_R(\theta)
-\eta g_R^\top G
+\frac{\eta^2}{2}G^\top H_RG
+O(\eta^3).
$$

转成 $I_R(G)$ 后相减。一阶差为
$\eta g_R^\top(G_i-G_s)=\eta A_R$，二阶差为上式中的曲率项。$\square$

### 可判定含义

- $A_R>0$：只表示 infinitesimal limit 中 informative 比 shared 更对齐 rare。
- 若二阶曲率代价超过一阶收益，有限步长下仍可能 $\Delta I_R\leq0$。
- 因此要在小学习率扫描中比较 Taylor 预测与真实一步。
- 还必须有 common guard：

$$
I_C(G_i)-I_C(G_s)\geq-\tau_C,
$$

其中 $\tau_C$ 必须在运行前注册。否则只是 rare/common 性能交换。

## 7. Counterexamples

1. **大奇异值但零学习。**激活有巨大 batch mean 或权重有大增益，但输出误差
   与该方向正交，则梯度为零；不能由奇异值推出学习速度。
2. **一阶对齐但真实一步变差。**取 $A_R>0$，同时 $H_R$ 在 $G_i$ 方向曲率
   极大；足够大的 $\eta$ 使二阶代价超过一阶收益。
3. **新方向但无用。**令 $(I-P_C)\Delta g_{\mathrm{info}}\neq0$，但它与
   $g_R$ 正交或反向；此时 $E_\perp>0$ 而 $A_R\leq0$。
4. **多头而无新增信息。**两个 auxiliary 目标都重复 next-token；raw MTP
   gradient 变大，但 informative 与 matched shared 的差为零。
5. **MTP 加剧 common。**更远 horizon 的梯度更集中于 common，导致 common
   曲率或更新占比增加，rare/common 失衡变差。
6. **局部帮助但长期无使用。**一步 $\Delta I_R>0$，但后续梯度旋转、新方向被
   擦除，或跨位置运输/普通头接口失败；A11 已提示 formation/use 必须分开。

## 8. Transformer claim boundary

本文件没有证明：

- Transformer 训练全程服从固定 Hessian 或固定 $P_C$；
- 参数空间中的正交方向等于可辨识的语义特征；
- empirical Fisher 等于 Hessian；
- 一步 rare-loss 改善会形成长期独立表征；
- 当前位置形成的信息会被跨位置运输并由标准头因果使用；
- MTP 对代码、规划、长上下文或 MoE Router 一般有效。

真实网络中 $g_C,g_R,H_R,P_C$ 会随轨迹旋转，参数重参数化也会改变几何描述。
所以当前结论是**同一参数点的局部因果对照**，不是一般 Transformer 定理。

## 9. 可检验预测

若“informative-MTP 产生局部有用的新 rare 更新”成立，则在预注册条件下应看到：

1. 相比 matched shared-aux，$E_\perp$ 显著大于噪声/稳定性阈值；
2. $A_R>0$，且 norm-matched 后方向效应仍存在；
3. 小 $\eta$ 区间内 Taylor 预测与真实 $\Delta I_R$ 一致；
4. 真实 $\Delta I_R>0$；
5. common guard 通过。

结果解释：

- $\Delta I_R>0,E_\perp>0$：支持局部有用的新更新，不证明长期表征；
- $\Delta I_R>0,E_\perp\approx0$：支持旧子空间强化/复用；
- $\Delta I_R\leq0,E_\perp>0$：新但无用或有害；
- native 有效、norm-matched 无效：主要是模长效应；
- 两者都不显著：此 checkpoint 没有检测到信息特异局部机制。

## 10. 完整研究线路，但一次只过一个 gate

```text
G0 定义 rare 与 NTP 失败
-> G1 同点 matched 对照：信息特异梯度是否局部有用
-> G2 新方向是否长期形成并稳定存在
-> G3 信息是否跨位置运输并被标准头因果使用
-> G4 哪种任务属性放大该机制，而不是“代码/NLP”标签
-> G5 针对已确认失败改进 MTP
-> G6 MTP 表征是否预测 held-out expert utility
-> G7 才设计更好的 Router
```

长上下文 retrieval、代码和规划是 workload motivation；Router 是远端目标。
它们不能替代 G1 的当前判定。

项目线的分工保持为：

- **A06：**Router 主线，最终需要 held-out conditional expert utility；
- **A07：**common/rare 与子空间控制的受控证据；
- **A11：**informative future signal 的形成、可达与 standard-head use 边界；
- **A12：**当前 carrier gate 失败，暂不承载 NTP/MTP 结论。

因此本问题是 A11 $\rightarrow$ A07 的候选机制桥；只有通过 G1–G3 后，才可能
向 A06 提供 Router 信号。

## 11. 明日一页汇报结构

1. **问题：**MTP 是复用 common，还是产生标准头局部可用的新 rare 更新？
2. **旧认识纠正：**奇异值、曲率、语义和学习速度不能混为一谈。
3. **理论答案：**$D_R$ 分开饥饿/冲突；$E_\perp$ 分开新/旧；
   $\Delta I_R$ 分开几何/功能。
4. **现有证据：**A11 只到 signal/reachability，A07 只支持受控
   common-subspace 现象，尚无 MTP 的 local utility 证据。
5. **唯一下一决定：**研究者是否批准同点 matched 一步实验。

建议汇报原句：

> 我们确认标准 MTP 不会因增加预测 horizon 自动解决 common/rare 失衡。
> 当前最小判据不是梯度更大或表征可读，而是 matched 信息增量能否带来标准头
> rare loss 的曲率修正真实一步改善，并通过 common guard。新方向与有用方向
> 将分别判定。

到此进入人类
[Thinking Card](03_mtp_mainline_thinking_card_cn.md)。未获批准前不进入实验。
