# 1109 组会：共享参数为什么让长尾学得慢，分发怎样让它学得快

> 图表与原始数据：[figures_tables/README_cn.md](figures_tables/README_cn.md)。下文的判定都是 AI 判定；研究者的科学判断：Unknown。D1、D2 以及除 A1/A2 之外的逐 feature 对比都是探索性结果。

## 目的

我们想弄清两件事：共享参数为什么让长尾信息学得慢；按 teacher feature 分发为什么能让它学得快。目标是给出 MoE 分发“何时共享、何时分开”的**可计算准则**。

## 结论

**问题 1：共享参数学习长尾信息时，主要妨碍学习的是方向冲突，还是梯度噪声淹没了有效信号？**

**结论 1：对别组数据的伤害主要来自梯度噪声，而不是方向冲突。** 6 个跨簇对的方向项全部是帮助，没有一个是伤害。噪声伤害随 $\eta^2$ 增长、随 $1/n$ 下降；在 $n=32$、$\eta=1/4$ 时，噪声伤害约为方向帮助的 17 倍。

实验数据（R02：33B MoE，第 7 层第 7 号 expert，单步 SGD；[T1](figures_tables/T1_R02_summary.md)）：

| 量 | 跨簇 A→B | 同簇 B′→B |
|---|---|---|
| 噪声项对 $\log\eta$ 的斜率（$n$=32/64/128；理论值 2） | 2.06 / 2.04 / 1.95 | 2.17 / 2.01 / 2.02 |
| 噪声项对 $\log n$ 的斜率（$\eta$=1；理论值 −1） | −1.18 | −0.99 |
| 方向项 $g_B^\top\bar g$（z 值） | \(5.7\times10^{-5}\)（1.28） | \(2.7\times10^{-3}\)（5.2） |
| 单 batch SNR（$n$=32 → 128） | 0.006 → 0.024 | 0.004 → 0.018 |
| 交叉步长 $\eta^\*$（$n$=32/64/128，推导值） | 0.018 / 0.036 / 0.057 | 0.016 / 0.022 / 0.048 |

---

**问题 2：按 teacher feature 分发，能否让长尾信息学得快？为什么？**

**结论 2：学习效果跟着“同一信号的集中度” $\bar M$ 走。** teacher 分簇比随机分发更集中，但比原生 router 更分散，所以它胜过随机分发、输给原生分发。五个臂按 $\bar M$ 中位数的排序，与按 NLL 的排序完全一致。

实验数据 1（五个臂都训练到 2000 步，即 0.52B token，单种子；按总体 NLL 从低到高排列；[T2](figures_tables/T2_five_arms_step2000.md)）：

| 臂 | 分发方式 | 总体 NLL | 相对 A0 | $\bar M$ 中位数 | bin0 NLL（最低频） | bin9 NLL（最高频） |
|---|---|---:|---:|---:|---:|---:|
| A0 | 原生 router（可学习） | 4.0831 | 0 | **1.010** | 3.7946 | 4.0740 |
| A1-deep | 第 0–3 层原生，第 4–7 层 teacher 簇 | 4.0851 | +0.0020 | **0.871** | 3.7899 | 4.0767 |
| A4 | 原生 router，蒸馏到 teacher 簇 | 4.1294 | +0.0463 | **0.811** | 3.8672 | 4.1168 |
| A1 | teacher 簇固定分发（8 层） | 4.1576 | +0.0745 | **0.586** | 3.9011 | 4.1448 |
| A2 | 随机固定分发（8 层） | 4.2860 | +0.2029 | **0.257** | 4.1879 | 4.2563 |

![五个臂的集中度与 NLL](figures_tables/F4_concentration_vs_nll.png)

读图：左图横轴是 $\bar M$ 中位数，五个点单调下降。右图横轴改用按出现次数加权的平均 $\log\bar M$，A0 与 A1-deep、A1 与 A4 两组的次序互换，所以“单调”依赖于用哪种汇总方式。

实验数据 2（相同步数下的 NLL 差，负值表示前者更好；[T3](figures_tables/T3_contrasts_by_step.md)）：

| 步数 | A1−A2 | A1−A0 | A1-deep−A0 |
|---:|---:|---:|---:|
| 250 | −0.189 | −0.092 | −0.101 |
| 500 | −0.205 | −0.028 | −0.076 |
| 750 | −0.165 | +0.045 | −0.027 |
| 1000 | −0.163 | +0.054 | −0.006 |
| 1500 | −0.145 | +0.059 | −0.009 |
| 2000 | −0.128 | +0.074 | +0.002 |

![同步数差值](figures_tables/F7_contrasts_over_steps.png)

读图：A1 在所有步数都胜过 A2；A1 相对 A0 在 500 与 750 步之间由领先变为落后；A1-deep 逐渐追平 A0。

实验数据 3（2000 步，各频段 $\bar M$ 中位数；[T4](figures_tables/T4_Mbar_median_by_bin.md)）：

| 频段 | A0 | A1-deep | A4 | A1 | A2 |
|---|---:|---:|---:|---:|---:|
| bin0（最低频） | 1.11 | 1.01 | 0.93 | 0.74 | 0.27 |
| bin2 | 1.13 | 0.97 | 0.91 | 0.66 | 0.26 |
| bin4 | 1.07 | 0.92 | 0.88 | 0.61 | 0.26 |
| bin6 | 0.97 | 0.84 | 0.79 | 0.53 | 0.25 |
| bin8 | 0.87 | 0.71 | 0.66 | 0.50 | 0.25 |
| bin9（最高频） | 0.56 | 0.58 | 0.51 | 0.49 | 0.25 |

（10 个频段的完整数据见 T4 和 [F6](figures_tables/F6_Mbar_by_frequency.png)。）

实验数据 4（逐 feature 的收益 $G_i$ 与集中度差 $\Delta_i$ 的 Spearman 秩相关，30000 个 feature；[T5](figures_tables/T5_feature_spearman.md)）：

| 对比 | $\rho$（全部） | bin0 | bin9 | 状态 |
|---|---:|---:|---:|---|
| A1 vs A2 | 0.256 | 0.340 | 0.101 | 预登记的主读数 |
| A1 vs A0 | 0.372 | 0.139 | 0.214 | 探索性 |
| A1-deep vs A1 | 0.285 | 0.168 | 0.093 | 探索性 |
| A1-deep vs A0 | 0.293 | 0.092 | 0.285 | 探索性 |
| A4 vs A0 | 0.164 | 0.063 | 0.229 | 探索性 |

## 机制假设与模型

**一步更新模型（问题 1）。** 用 A 组一个 minibatch（$n$ 个 token）对参数 $\theta$ 走一步 SGD，B 组损失的期望变化为

$$
\mathbb{E}[\Delta L_B] \approx \underbrace{-\eta\, g_B^\top \bar g_A}_{\text{方向项}} + \underbrace{\frac{\eta^2}{2}\,\bar g_A^\top H_B\, \bar g_A}_{\text{均值曲率项}} + \underbrace{\frac{\eta^2}{2}\,\frac{\operatorname{tr}(H_B\Sigma_A)}{n}}_{\text{噪声项}}
$$

其中 $\bar g_A$ 是 A 的平均梯度，$\Sigma_A$ 是单 token 梯度的协方差，$g_B$、$H_B$ 是 B 损失的梯度和 Hessian。

- 噪声项的测法：$N(\eta,n)=\mathbb{E}_{\hat g_A}[\Delta L_B(-\eta\hat g_A)]-\Delta L_B(-\eta\bar g_A)$。两者的一阶项相同，相减后正好消掉，只剩噪声项。
- 交叉步长（帮助等于伤害处）：$\eta^\* \approx 2n\, g_B^\top\bar g_A/\operatorname{tr}(H_B\Sigma_A)$。
- 单 batch 信噪比：$\mathrm{SNR}_n = \|\bar g\|^2/(\operatorname{tr}(\Sigma)/n)$。

**分发模型（问题 2）。** 每个臂都按同一形式选 expert 并输出：$S_t=\operatorname{Top2}(s_t+b)$，$y_t=\sum_{e\in S_t} w_{t,e}\,E_e(h_t)$。

- 原生：$s_t=\operatorname{softmax}(W_r h_t)$。
- teacher 簇：$s_{t,e}=\hat a_t^\top\mu_e$，$\hat a_t$ 是 teacher SAE 编码（TopK32）归一化后的向量，$\mu_e$ 是冻结的簇心；固定分发的臂取 $w_{t,e}=\tfrac12$。
- load bias 更新：$b_e\leftarrow b_e+\gamma\,\operatorname{sign}(\bar n-n_e)$，$\gamma=0.001$。

**集中度。** 对 feature $i$ 和 expert $e$，覆盖率 $c_i(e)=P(e\in S_t\mid i\in A_t)$，纯度 $\pi_i(e)=P(i\in A_t\mid e\in S_t)$，参考频率 $p_i=P(i\in A_t)$。

$$
\bar M_i=\frac1L\sum_{l=1}^{L}\sum_{e}\frac{c^{(l)}_i(e)}{k}\cdot\frac{c^{(l)}_i(e)\,\pi^{(l)}_i(e)}{p_i},\qquad k=2,\ L=8
$$

参照值：dense 为 1，随机 Top-2/8 为 $k/E=1/4$，完全集中为 $E/k=4$。

**学习读数。** $\mathrm{NLL}_i$ 是 feature $i$ 激活位置上的平均 NLL；$G_i(X,Y)=\mathrm{NLL}_i(Y)-\mathrm{NLL}_i(X)$，$\Delta_i(X,Y)=\log\bar M_i(X)-\log\bar M_i(Y)$，$\rho=\operatorname{Spearman}(G_i,\Delta_i)$。

**假设（认识层面）。** 长尾信息学得慢，是因为它稀少的信号在共享参数里被噪声淹没。分发要起作用，就必须提高 $\bar M_i$。预测：在任何一对分发之间，$\bar M_i$ 更高的一方在 feature $i$ 上学得更好。

## 实验分析

### 问题 1

- **设置：** 一步干预，$n\in\{32,64,128\}$，$\eta$ 取 8 档，每档 32 个独立 minibatch。
- **读数：** 表 1，[F1](figures_tables/F1_noise_term_scaling.png)（噪声项标度），[F2](figures_tables/F2_help_to_harm_crossing.png)（帮助到伤害的交叉）。
- **为什么：** 误差的均值为零，所以不改变一阶项；B 的损失在当前点向上弯曲，往随机方向走一步，二阶上必然变差。
- **边界：** 单步、单 expert、单 checkpoint；A、B 的初始 loss 与 gate 权重没有匹配；交叉步长只到推导与事后估计，没有在网格内直接观测到。

### 问题 2

- **设置：** 五个臂的结构、数据、优化器全部一致，从零训练到 2000 步，只改分发方式。
- **读数：** 实验数据 1–4；[F3](figures_tables/F3_eval_nll_curves.png)（EVAL NLL 曲线）、[F4](figures_tables/F4_concentration_vs_nll.png)（五点图）、[F5](figures_tables/F5_contrast_by_frequency.png)（分频段差值）、[F8](figures_tables/F8_train_ce.png)（训练 CE）。
- **为什么（有诊断支持的部分）：**
  1. **teacher 分发的集中度被 load bias 稀释，并受到 8 簇共用划分的限制**（D2，探索性）。teacher 分数第 2 与第 3 高分之差的均值只有 0.036，而 2000 步时 load bias 的极差是 0.136，bias 足以改变 Top-2 的选择。用同一组分数离线重算：去掉 bias，$\bar M$ 中位数从 0.586 回到 0.697，这是所测几项规则里下降最大的一项。但即使去掉 bias，0.697 仍低于 A0 的每一层（0.83–0.97）；A1 的 8 层路由完全相同。所以剩下的差距来自“8 个粗簇、8 层共用”本身。bias 对不同频段的作用相反：去掉它，bin9 从 0.49 升到 0.68，bin0 却从 0.74 降到 0.66。
  2. **原生 router 在每一层都用 LM 梯度自适应，** 低频 feature 的 $\bar M$ 能到 1.11，高于 dense 参照 1（[F6](figures_tables/F6_Mbar_by_frequency.png)）。
  3. **A1 早期领先的原因还不清楚。** 原先猜测“原生 router 早期还没集中”，D1 否定了这个猜测：A0 从第 250 步起就比 A1 更集中（0.80 对 0.55），并不是在 500–750 步才反超。与 NLL 翻转同步的，是 A0 集中度从 0.80 增长到 0.93。候选解释是前 1000 步 warmup 期间学习率小、固定路由更容易优化，未检验（[D1 图](figures_tables/D1_Mbar_over_steps.png)）。
  4. **A4 被蒸馏向一个集中度更低的目标。** 它的 $\bar M$ 从 0.66 升到 0.81，但始终低于 A0 的 0.80→1.01，NLL 也落后 A0 0.046。
- **认识更新：** 分簇只是手段，真正决定学习的是实际集中度 $\bar M$。$\bar M$ 可以离线计算，因此可以用它先筛选分发设计——这就是目的里说的“可计算准则”。D2 也说明，同一组 teacher 分数换一种分发规则，$\bar M$ 就会变（0.44–0.77），所以分发规则本身也应纳入这个准则。
- **边界：**
  - 单种子，0.52B token；
  - teacher 训练时见过这批训练数据；
  - 可学习路由的 $\bar M$ 也可能是学得好的结果（反向因果），只有 A1 对 A2 这一对是外生操纵；
  - 用中位数排序时五个臂完全一致；改用加权平均 $\log\bar M$ 时，A0/A1-deep、A1/A4 两组次序互换；
  - 家族 bootstrap 区间 Unknown；D1、D2 是事后的探索性诊断。

## 下一步（AI 建议，待研究者决定）

1. **离线筛选 teacher 分发规则：** 缩放分数或改负载均衡方式，再加入逐层划分，用 $\bar M$ 先排序，挑出能接近 A0 的方案后再训练。只需前向。
2. **检验 A1 早期领先的原因：** 比较 warmup 期间固定路由与原生路由的梯度信噪比。
3. **补家族 bootstrap 区间，补第二个种子。**
