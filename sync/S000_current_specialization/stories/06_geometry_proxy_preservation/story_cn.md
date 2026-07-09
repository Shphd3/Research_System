# A06 Router 训练动力学 Story

文档状态：
- 类型：研究线级 story
- 研究线：`06_geometry_proxy_preservation`
- 语言：中文 companion
- 当前模式：理论推进版
- 英文 canonical 文件：`story.md`

## 0. 术语约定

| 术语 / 缩写 | 中文含义 | 具体对象或公式 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 特征-专家绑定 | 某个 feature 稳定进入同一个目标 expert | $P(e=a(f)\mid f)$ 和 matched route margin | 06 线现在关心的不只是发现 center，而是训练后是否还绑定 | expert 是否真的有功能收益 |
| router row | router 中每个 expert 对应的打分向量 | $s_e(h)=w_e^\top h$ 中的 $w_e$ | 它决定 hidden state 落到哪个 expert 区域 | expert 自身是否有用 |
| route margin | 目标 expert 相对竞争 expert 的打分间隔 | $m_f=\min_{e\ne a(f)}(w_{a(f)}-w_e)^\top\mu_f$ | 它是 preservation 的局部安全缓冲 | center 外所有 token 都安全 |
| soft router | 连续路由；每个 expert 都有非零权重 | $p_e(h)=\operatorname{softmax}(w_e^\top h/\tau)$ | 它方便做干净梯度推导 | top-1 sparse router 的全部行为 |
| top-1 sparse router | 只选择最高分 expert 的稀疏路由 | $r(h)=\arg\max_e w_e^\top h$ | 它是当前主线模型的核心困难 | 连续比较所有 expert |
| expert advantage | 某个 expert 相比当前 mixture 是否更能降低 loss | $A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle$ | 它决定 router row 朝 hidden state 走，还是远离 hidden state | feature 语义 |
| 正确信号 | 能增加目标 feature margin 的梯度成分 | $\mathbb E[p_aA_a-p_bA_b\mid f]>0$ | 它是 router 真正学会绑定 feature 的来源 | 所有训练信号都正确 |
| 噪声信号 | 对目标 feature margin 没有稳定正贡献的梯度成分 | 条件均值约为 0，但方差非零 | 多步累积可以吃掉有限 margin | 所有噪声都是零均值 |
| common / background 信号 | 高频、共享、非 feature 区分的更新成分 | 沿 common 方向或背景 token 方向的系统漂移 | 它比零均值噪声更危险，因为可能有偏 | 当前 common estimator 是真因果 common |

## 1. 摘要

当前 A06 的核心认识是：feature center 可以被发现，也可以初始化出较好的 top-1 router；但这只说明 step 0 可达。训练后是否保持，取决于 route margin 是否能抵抗后续更新。

因此下一阶段不应先设计新 gate，也不应先跳到多词元预测。更小、更必要的问题是：

> 在最简单的 synthetic MoE 训练中，router row 每一步到底怎么动？

当前 story 将 06 线改写为一个训练动力学问题：

```text
初始 row-feature 对齐
-> 初始 margin
-> 每个样本产生 expert advantage
-> 正确 feature 信号增加目标 margin
-> 噪声 / common / background 信号消耗 margin
-> top-1 稀疏反馈让未选 expert 缺少逐个纠错信号
-> margin 被吃掉后发生 sign flip 或 expert lock-in
```

这一步的目标不是提出最终方法，而是建立一个能解释“router 为什么移动、往哪移动、什么时候失去 binding”的最小模型。

## 2. 研究问题

当前 A06 的新问题是：

> 在受控 synthetic setting 中，给定一个初始化在 feature center 附近的 router，训练样本如何通过梯度改变 router row 和 feature margin？

它分成三个层次：

1. soft router 中，连续梯度如何更新每个 row；
2. top-1 sparse router 中，选中 expert 和未选 expert 的更新有什么差异；
3. 多步训练中，正确信号、噪声信号、common 信号和 hidden drift 如何共同决定 margin crossing。

这比“能不能聚类出 feature center”更深一层，因为它直接研究训练过程本身。

## 3. 为什么这个问题容易混淆

第一，初始化成功不等于训练在学习正确路由。一个 router 可以在 step 0 有高 NMI，但后续训练只是在消耗初始 margin。

第二，task accuracy 不等于 specialization。A06_24 / A06_28 / A06_29 都显示，即使预测任务继续变好，feature margin 也可能变负。

第三，soft router 和 top-1 router 的梯度结构不同。soft router 会连续比较多个 expert；top-1 router 通常只通过被选中的 expert 接收任务反馈，未选 expert 没有“我本来会更好”的直接证据。

第四，噪声不是只有零均值随机扰动。背景 token、common 方向、高频模式会产生系统性 row drift，它可能比随机噪声更快吃掉 margin。

## 4. 数据和训练布局

理论分析先使用最小受控 synthetic 布局：

```text
一层 causal Transformer
-> 一层 MoE
-> 均匀 synthetic features
-> 无 learned absolute position
-> route-position hidden state
-> feature target 或全序列 LM loss
```

第一阶段先冻结 hidden state，只看 router row 怎么动：

$$
h=\mu_f+\epsilon.
$$

其中 $\mu_f$ 是 feature center，$\epsilon$ 是同一 feature 内的 token spread。

第二阶段再加入 hidden drift：

$$
\begin{aligned}
\Delta m_f
&=
(\Delta w_a-\Delta w_e)^\top\mu_f \\
&\quad+
(w_a-w_e)^\top\Delta\mu_f \\
&\quad+
(\Delta w_a-\Delta w_e)^\top\Delta\mu_f.
\end{aligned}
$$

这对应 A06 之前的 margin-budget 分解。新的 story 要进一步解释第一项：

$$
(\Delta w_a-\Delta w_e)^\top\mu_f.
$$

也就是 router row 自己为什么移动。

## 5. 物理直觉

router row 可以理解为可移动的决策边界。一个样本到来时，训练不会直接告诉 router “这个 feature 应该去 expert 2”。训练只告诉模型：当前被使用的 expert 组合有没有降低 loss。

因此 router row 的移动由两件事共同决定：

1. 当前样本 hidden state 的方向 $h$；
2. 某个 expert 对当前 loss 的局部好坏，即 expert advantage。

如果某个 expert 对 feature $f$ 真的有用，那么它在 feature $f$ 样本上应该获得正 advantage，router row 就会朝 $\mu_f$ 方向移动，margin 变厚。

如果更新来自背景 token 或 common 方向，router row 可能朝高频但非 feature 区分的方向移动，margin 变薄。

如果是 top-1 router，问题更严重：未选 expert 没有被真正试用，所以训练信号很难精确指出“哪个未选 expert 更适合这个 feature”。这会导致 early lock-in 和弱 correction。

## 6. 指标和变量定义

对 feature $f$，目标 expert 记为 $a(f)$。center-level margin 是：

$$
m_f(t)=\min_{e\ne a(f)}(w_{a(f)}(t)-w_e(t))^\top\mu_f(t).
$$

token-level margin 需要考虑 spread：

$$
h=\mu_f+\epsilon.
$$

如果：

$$
(w_a-w_e)^\top\mu_f > \|w_a-w_e\|\cdot\|\epsilon\|,
$$

则这个局部 token 仍在目标 expert 区域内。

soft router 的 expert 概率是：

$$
p_e(h)=\frac{\exp(w_e^\top h/\tau)}{\sum_j\exp(w_j^\top h/\tau)}.
$$

soft mixture 输出是：

$$
\hat y=\sum_e p_e(h)E_e(h).
$$

定义 expert advantage：

$$
A_e(h,y)
=
-\left\langle \nabla_{\hat y}\ell(\hat y,y), E_e(h)-\hat y\right\rangle.
$$

直观含义：

- $A_e>0$：增加 expert $e$ 的权重会降低 loss；
- $A_e<0$：增加 expert $e$ 的权重会升高 loss；
- $A_e\approx0$：当前 loss 对这个 expert 的路由权重不敏感。

## 7. 数学模型

### 7.1 soft router 的一阶梯度

对 soft mixture：

$$
\hat y=\sum_e p_eE_e(h),
$$

有：

$$
\frac{\partial L}{\partial w_e}
=
\frac{p_e}{\tau}
\left\langle \nabla_{\hat y}\ell, E_e(h)-\hat y\right\rangle h.
$$

所以梯度下降更新是：

$$
\Delta w_e
=
\eta\frac{p_e}{\tau}A_e(h,y)h.
$$

这条公式是当前 story 的核心。

它说明 router row 的移动只有三个因子：

1. 当前 expert 被 router 考虑的程度 $p_e$；
2. 这个 expert 是否比 mixture 更能降低 loss，即 $A_e$；
3. 当前样本 hidden direction $h$。

所以，router 不是抽象地“学习 feature”。它是在每个样本上沿 $h$ 的方向，按 expert advantage 改变 row。

### 7.2 feature margin 的一步变化

对 feature $f$，比较目标 expert $a$ 和竞争 expert $b$：

$$
m_{f,a,b}=(w_a-w_b)^\top\mu_f.
$$

如果先冻结 hidden center，那么一步更新近似为：

$$
\Delta m_{f,a,b}
=
(\Delta w_a-\Delta w_b)^\top\mu_f.
$$

代入 soft-router 更新：

$$
\Delta m_{f,a,b}
\approx
\eta\frac{1}{\tau}
\left[p_aA_a-p_bA_b\right]h^\top\mu_f.
$$

如果当前样本来自 feature $f$，且 $h^\top\mu_f>0$，那么 margin 是否增加主要由：

$$
p_aA_a-p_bA_b
$$

决定。

这给出一个很清楚的可测量量：

> matched expert 的概率加权 advantage 是否大于竞争 expert 的概率加权 advantage？

### 7.3 正确信号

正确信号是指对 feature $f$，目标 expert 的概率加权 advantage 系统性更大：

$$
\mathbb E[p_aA_a-p_bA_b\mid f]>0.
$$

如果成立，feature margin 的期望会增长。

这才是“router 学会 feature binding”的最小梯度条件。

### 7.4 零均值噪声

零均值噪声指：

$$
\mathbb E[p_aA_a-p_bA_b\mid f]\approx 0,
$$

但：

$$
\operatorname{Var}(p_aA_a-p_bA_b\mid f)>0.
$$

单步看它不系统改变 margin，但多步会形成随机游走。若初始 margin 很薄，随机波动也可以造成 boundary crossing。

这对应 A06_23 的直觉：不是“只要 margin 正就安全”，而是 margin 必须大到能承受后续累计扰动。

### 7.5 有偏 common / background 信号

common 或 background 信号更危险，因为它可能有系统偏置：

$$
\mathbb E[p_aA_a-p_bA_b\mid f]\ne 0,
$$

但这个非零均值不是沿 feature-discriminative direction，而是沿高频背景方向。

如果 $h=c+r_f$，其中 $c$ 是 common 方向，$r_f$ 是 feature residual，那么 row 更新包含：

$$
\Delta w_e
\propto
p_eA_e(c+r_f).
$$

当 common 项频繁出现时，累计更新可能让 $w_e$ 重新吸收 common 方向，导致 feature margin 被压住或反转。

但 A06_29 已经说明：简单 mean-DNS 不能直接解决这个问题。因此 story 里只能说 common/background 是候选漂移项，不能说当前 common estimator 已经是因果解释。

## 8. top-1 sparse router 的离散更新

令：

$$
r(h)=\arg\max_e w_e^\top h.
$$

如果实现中使用 full softmax 概率 $p_r$ 作为被选 expert 的门控权重，即：

$$
\hat y=p_r(h)E_r(h),
$$

那么对任意 row $w_j$：

$$
\frac{\partial L}{\partial w_j}
=
\frac{p_r}{\tau}
(1_{j=r}-p_j)
\left\langle\nabla_{\hat y}\ell,E_r(h)\right\rangle h.
$$

定义 selected expert benefit：

$$
B_r=-\left\langle\nabla_{\hat y}\ell,E_r(h)\right\rangle.
$$

则：

$$
\Delta w_j
=
\eta\frac{p_r}{\tau}(1_{j=r}-p_j)B_rh.
$$

这说明 top-1 的更新有一个很强的非对称性：

1. 如果被选 expert 有用，$B_r>0$，被选 row 朝 $h$ 走，未选 row 远离 $h$。
2. 如果被选 expert 无用，$B_r<0$，被选 row 远离 $h$，未选 row 共同朝 $h$ 走。
3. 但未选 row 的更新没有区分“哪个未选 expert 最好”，因为它们没有被实际试用。

因此 top-1 的纠错机制弱于 soft routing。

如果实现是纯 hard argmax 且输出不乘 gate probability，那么 task loss 对 router score 的梯度可能为 0；这时 router 主要被 auxiliary loss 或手写 balancing 项移动。这是另一个必须在 protocol 里明确的 implementation boundary。

## 9. 定理和证明状态

### 命题 1：soft-router row 更新沿当前 hidden direction

在 soft mixture 中：

$$
\Delta w_e
=
\eta\frac{p_e}{\tau}A_eh.
$$

证明：直接对 $p_e=\operatorname{softmax}(w_e^\top h/\tau)$ 求导。

结论：router row 的一阶运动不是任意的；它总是沿当前样本 hidden state $h$ 的方向，只是符号和大小由 $p_eA_e$ 决定。

### 命题 2：feature margin 增长需要 matched expert advantage

若：

$$
\mathbb E[p_aA_a-p_bA_b\mid f]>0,
$$

且 feature 样本满足 $\mathbb E[h^\top\mu_f\mid f]>0$，则：

$$
\mathbb E[\Delta m_{f,a,b}\mid f]>0.
$$

边界：这只是在 frozen hidden / one-step 条件下成立。多步训练还要加入 hidden drift、optimizer momentum、batch composition 和 token spread。

### 命题 3：top-1 task feedback 不是完整 expert comparison

在 probability-weighted top-1 中，梯度只使用被选 expert 的输出 $E_r(h)$。未选 expert 只通过 softmax denominator 收到方向相反的弱更新。

因此如果初始选错 expert，训练并不会自动知道哪个未选 expert 更适合。这个机制可以解释 early lock-in 和 weak modification。

### 经验命题：A06 已经支持 margin 是 preservation 尺子，但还没直接测 router advantage

A06_21 / A06_23 支持正 margin buffer 是 controlled preservation 的关键。但还没有直接测：

$$
p_eA_e,\qquad
\Delta w_e,\qquad
\Delta m_f^{\mathrm{pred}},
\qquad
\Delta m_f^{\mathrm{actual}}.
$$

所以现在最小前进不是再加方法，而是补这个一阶动力学 audit。

## 10. 机制分解

一个 synthetic router 训练过程应拆成下面八步：

| 步骤 | 具体对象 | 要回答的问题 |
|---|---|---|
| 1. 初始 row-feature 对齐 | $(w_e^\top\mu_f)$ | 随机或中心初始化是否已经给某些 feature 更大优势？ |
| 2. 初始 margin | $m_f(0)$ | 初始安全缓冲有多厚？ |
| 3. 样本分配 | $p_e$ 或 $r(h)$ | 当前样本主要影响哪些 expert？ |
| 4. expert advantage | $A_e$ 或 $B_r$ | 哪个 expert 的输出真正降低 loss？ |
| 5. row 更新 | $\Delta w_e$ | router row 是否朝 feature center 移动？ |
| 6. margin 更新 | $\Delta m_f$ | 这一步增厚还是消耗目标 feature margin？ |
| 7. hidden drift | $\Delta\mu_f$ | feature center 自己是否移动过边界？ |
| 8. crossing / lock-in | sign flip, matched preserve | 是否发生边界穿越或错误专家锁定？ |

这个分解可以把“初始化不均衡”“训练无法纠正”“common 吞掉 margin”“top-1 离散反馈弱”放进同一个数学框架。

## 11. A06 证据链如何接入这个 story

结果：

- A06_17 / A06_21：正确 route-position center 可以保持，因为 current margin 和 cluster-aware margin 为正。
- A06_23：正 margin 不是越小越安全；存在有限 safe threshold。
- A06_24_synthetic：全位置 common subtraction 不能可靠分开 rare features；row projection 是较强 preservation clue，但不是完整解。
- A06_27：embedding-gradient top1 在 pointwise synthetic bridge 中能找到 route-relevant states。
- A06_28：全序列 LM 下，raw embedding-gradient selector 有 feature signal，但 margin guard 失败。
- A06_29：mean-DNS routing 不支持；row projection 有部分改善，但不能保持正 margin。

解释：

这些结果共同说明，A06 的缺口不是“hidden state 完全没有 feature 信息”，也不是“永远找不到 center”。缺口是：

> 普通训练更新是否给 router 一个足够强、足够持续、足够 feature-aligned 的 row movement。

边界：

这些 evidence 还不能证明 real-DCLM 的 collapse 已被解释，也不能证明 common 方向是唯一原因。

## 12. 可借鉴文献

这些文献提供数学语言，但不直接替代我们的 synthetic A06 分析。

1. Jacobs, Jordan, Nowlan, Hinton, 1991, [Adaptive Mixtures of Local Experts](https://www.cs.toronto.edu/~fritz/absps/jjnh91.pdf)。  
   可借鉴点：soft gate 可以看成给 expert 分配 responsibility；expert 好坏会反馈到 gate。

2. Jordan and Jacobs, 1994, [Hierarchical Mixtures of Experts and the EM Algorithm](https://direct.mit.edu/neco/article/6/2/181/5779/Hierarchical-Mixtures-of-Experts-and-the-EM)。  
   可借鉴点：用 responsibility / EM 视角理解“谁应该解释这个样本”。

3. Shazeer et al., 2017, [Outrageously Large Neural Networks](https://arxiv.org/abs/1701.06538)。  
   可借鉴点：现代 sparse top-k MoE 的 practical router 形式。

4. Chen, Deng, Wu, Gu, Li, 2022, [Towards Understanding the Mixture-of-Experts Layer in Deep Learning](https://proceedings.neurips.cc/paper_files/paper/2022/file/91edff07232fb1b55a505a9e9f6c0ff3-Paper-Conference.pdf)。  
   可借鉴点：在 cluster-structured 数据中，理论上 router 可以学习 cluster-center features；但它的假设和我们的 top-1 margin erosion setting 不同。

5. Nguyen, Nguyen, Ho, 2023, [Demystifying Softmax Gating Function in Gaussian Mixture of Experts](https://arxiv.org/abs/2305.03288)。  
   可借鉴点：softmax gating 与 expert 参数存在内在耦合，gating 参数有可识别性和收敛率问题。

6. Nguyen, Akbarian, Yan, Ho, 2023, [Statistical Perspective of Top-K Sparse Softmax Gating Mixture of Experts](https://arxiv.org/abs/2309.13850)。  
   可借鉴点：top-k sparse softmax 会把输入空间切成不同行为区域，这正好对应我们的 boundary / margin 视角。

7. Nguyen, Ho, Rinaldo, 2024, [Sigmoid Gating is More Sample Efficient than Softmax Gating in Mixture of Experts](https://arxiv.org/abs/2405.13997)。  
   可借鉴点：softmax expert competition 可能带来 sample efficiency 和 collapse 问题；这支持我们检查 router competition 项。

8. Chi et al., 2022, [On the Representation Collapse of Sparse Mixture of Experts](https://arxiv.org/abs/2204.09179)。  
   可借鉴点：sparse routing 可能推动 hidden states 向 expert centroids 聚集，说明 router 与 representation 会互相塑形。

## 13. 反例和竞争解释

竞争解释 1：不是 router 梯度问题，而是 hidden state drift 问题。  
回应：这可能成立，所以第一阶段要 freeze hidden，只测 row update；第二阶段再加入 $\Delta\mu_f$。

竞争解释 2：不是 top-1 问题，soft router 也会失败。  
回应：需要做 soft-router one-step audit。如果 soft 也没有 feature-aligned advantage，那么问题是 objective / expert utility；如果 soft 有而 top-1 没有，问题是 sparse feedback。

竞争解释 3：不是噪声，而是 common biased drift。  
回应：需要把零均值噪声和 common/background biased update 分开测。

竞争解释 4：初始化太差，训练本来就没机会。  
回应：先用 near-feature initialization 和 controlled margin sweep，把初始 margin 作为显式变量。

竞争解释 5：feature partition 没有 utility。  
回应：这是 A07 的问题。06 当前只证明 binding dynamics，不证明 utility。

## 14. 结论边界

可以说：

- 06 线下一步应进入 router one-step dynamics，而不是继续堆 initialization 方法。
- soft router 给出清楚的一阶公式：row 更新等于 routing probability、expert advantage 和 hidden direction 的乘积。
- top-1 router 的 task feedback 是 selected-expert feedback，不是完整 expert comparison；这可以解释 weak correction 和 lock-in。
- A06 已有 margin evidence 足够支持建立 signal/noise margin-budget 模型。

不能说：

- 已经有新 gating 方法。
- MTP 已经应该进入当前 anchor。
- real-DCLM collapse 已被这个 synthetic 模型解释。
- common direction 是唯一或已验证的 collapse 原因。
- 高 NMI 的 feature routing 已经有 expert utility。

## 15. Anchor 分解和下一步

### 06_30：无背景 full-slot preservation 诊断

决策问题：

> 如果把 32 个位置全部变成 feature-bearing token，并去掉背景 token，ideal center 初始化是否还能在 full-LM 长训练中保持？

当前结果：

8 seeds full run 支持该诊断：oracle all-position / predictive-position / last-predictive-position centers 在 2000 步后保持 all-position feature NMI 1.000，margin p05 约 4.566；random control 仍为负 margin。

机制更新：

这说明 mixed full-LM 中 ideal center 被破坏不是“长训练必然破坏 top-1 routing”。背景或非 feature 位置是必要机制候选。下一步不应直接跳到新 gate，而应做 graded background-ratio margin-budget audit。

### 06_31：soft-router 一步梯度动力学

决策问题：

> 在 frozen hidden synthetic setting 中，soft router 的实际 $\Delta w_e$ 和 $\Delta m_f$ 是否符合 advantage-weighted 公式？

核心测量：

$$
A_e,\quad p_eA_e,\quad \Delta w_e,\quad
\Delta m_f^{\mathrm{pred}},\quad
\Delta m_f^{\mathrm{actual}}.
$$

可证伪点：

- 如果公式预测和实际更新不一致，说明实现或数学建模错了。
- 如果正确 feature 样本没有 matched advantage，说明路由没有可用的 task signal。
- 如果噪声/common 样本的 margin 消耗大于正确样本的 margin 增益，说明 preservation 失败来自 signal-noise imbalance。

### 06_32：top-1 离散更新动力学

决策问题：

> top-1 router 的 selected-expert feedback 是否解释 early lock-in 和错误初始化难以纠正？

核心测量：

$$
r(h),\quad B_r,\quad \Delta w_r,\quad \Delta w_{j\ne r},\quad \Delta m_f.
$$

可证伪点：

- 如果未选 expert 也获得有效区分性纠错，说明 top-1 correction gap 不是主因。
- 如果错误选中的 expert 被持续强化，支持 lock-in。

### 06_33：signal-noise margin budget

决策问题：

> 多步训练中的 margin crossing 能否由正确 feature signal、零均值噪声、common/background biased signal 和 hidden drift 的累计预算预测？

核心表达式：

$$
\begin{aligned}
m_f(T)
&\approx
m_f(0)
+ \sum_{t<T}\Delta m_f^{\mathrm{signal}}(t) \\
&\quad
+ \sum_{t<T}\Delta m_f^{\mathrm{noise}}(t) \\
&\quad
+ \sum_{t<T}\Delta m_f^{\mathrm{common}}(t) \\
&\quad
+ \sum_{t<T}\Delta m_f^{\mathrm{hidden}}(t).
\end{aligned}
$$

可证伪点：

- 如果预算预测不了 crossing，说明缺了关键动力学项。
- 如果预测成功，就可以把 preservation 从经验现象变成可审计的机制量。

### 06_34：soft-to-sparse 温度桥

决策问题：

> 随着 soft-router temperature 降低，是否连续逼近 top-1 的 lock-in / weak-correction 行为？

核心测量：

$$
\tau,\quad \operatorname{entropy}(p),\quad \Delta m_f,\quad sign\ flip,\quad NMI.
$$

可证伪点：

- 如果低温 soft 仍有强纠错而 top-1 没有，说明 discontinuous top-1 selection 本身是关键。
- 如果低温 soft 和 top-1 同样失败，说明主要问题是竞争过强或 signal/noise 预算不足。

## 16. 与主线的关系

这条 story 暂时不进入 MTP。

原因是：MTP 可以提供更强的 feature-aligned hidden signal，但它不能替代 router 动力学分析。如果不知道 router 如何把 signal 转成 row movement，直接上 MTP 会把“表示是否更好”和“路由是否能保持”混在一起。

因此当前顺序应为：

```text
06 router basic dynamics
-> 06 signal/noise margin budget
-> 07 utility / interference value
-> 11 MTP or nested objective as signal source
```

MTP 以后可以作为“更强正确信号来源”接回来，但不是当前最小步。

## 17. 下一步唯一决策

下一步应写并审核：

```text
06_33_signal_noise_margin_budget_anchor.md
```

最小问题：

> 从 no-background full-slot 出发，逐步加入背景位置时，正确 feature signal、background signal、router drift 和 hidden drift 中哪一项首先把 matched margin 推向负值？

如果 graded background audit 能预测 margin crossing，再进入 soft/top-1 one-step dynamics 去解释每一类信号的 row update。  
如果它不能预测 crossing，先修正 margin-budget 分解，不应继续设计新 gating。

## Source Map

- A06 research map: `../../problem_anchors/06_geometry_proxy_preservation/research_map.md`
- A06 closure report: `../../problem_anchors/06_geometry_proxy_preservation/closure/06_geometry_proxy_preservation_closure_report_cn.md`
- A06_28 summary: `../../experiments/A06/A06_28_full_sequence_lm_gradient_selector_guard/summary.md`
- A06_29 summary: `../../experiments/A06/A06_29_dns_routing_preservation_audit/summary.md`
- A11 story boundary: `../11_long_horizon_mtp_objective/story_cn.md`
