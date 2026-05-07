# 长尾低维特征组合 MoE 合成实验方案

## 0. 实验定位

本实验是当前方向的新起点，不是继续优化上一轮 synthetic natural language hierarchy 实验。

上一轮实验已经说明：当路径由真实标签指定时，Oracle-Routing hierarchical MoE 明显更强；但 learned router 只带来很小提升，说明当前瓶颈更像是 router/path selection 与 expert specialization 没有对齐。

这次实验的目标是把问题退回到最小数学世界：

> 如果表征空间本身真的由若干低维特征组合构成，并且这些组合按 Zipfian 长尾分布出现，那么 MoE 能不能把这些组合恢复出来？

换句话说，我们不先问真实语言是不是这样，而是先问：

> 如果这个假设是真的，我们的模型工具有没有能力学出来？

如果在完全可控的合成世界里都学不出来，那么后续用它验证真实语言假设就不可靠；如果能学出来，我们才有资格继续研究真实模型表征、SVD 谱空间、稀疏特征和语言长尾之间的关系。

### 0.1 当前版本锁定

本 plan 后续不再以“从 distractor 中恢复 clean component”的简版实验作为主要证据。简版实验最多保留为 pipeline smoke，不作为论文式结论。

当前正式实验必须显式生成并保存每个机制的真实函数：

$$
A_m=U_m W_m U_m^\top
$$

其中 $U_m$ 是机制 $m$ 的真实低维 feature 子空间，$W_m$ 是机制 $m$ 在该子空间内的局部变换。

因此，本实验要验证的不只是：

> 样本是否被 route 到同一 expert；

还必须验证：

> 匹配后的 expert 是否学到了对应机制的子空间和局部变换。

只有 route recovery、subspace recovery、matrix / function recovery 同时成立，才可以说 expert 学到了真实机制。

---

## 1. 实验目的

构造一个完全可控的合成表征空间，验证 MoE 是否能恢复长尾分布的低维特征组合。

更具体地说：

1. 人为构造 $M$ 个真实机制，每个机制只依赖 $k$ 个低维特征方向。
2. 让这些机制的出现频率服从 Zipfian 分布。
3. 为每个机制生成独立的局部变换 $W_m$ 和嵌入矩阵 $A_m$。
4. 用这些机制生成输入向量 $h$ 和目标输出 $y$。
5. 训练 Dense、Oracle-Routing MoE、Learned-Router MoE。
6. 检查模型是否只是 loss 变好，还是 expert 真的学到了真实低维特征组合和机制函数。

实验要回答的核心问题：

> MoE 的每个 expert 是否能对应一个真实机制，并抓到这个机制对应的 $k$ 个特征方向与局部变换？

---

## 2. 背景与动机

### 2.1 旧实验留下的问题

旧实验中，我们构造了满足 Zipfian 词频的 synthetic natural language dataset，并比较 dense、flat MoE、middle-band routing MoE、hierarchical MoE 和 Oracle-Routing routing MoE。

结果显示：

1. Learned hierarchical MoE 有一点收益，但收益不大。
2. Oracle-Routing routing MoE 明显更好。
3. Learned router 没有稳定恢复真实 hierarchy。
4. 只看 loss 不能证明 expert specialization。

因此，当前核心问题不是继续声称 hierarchical MoE 已经成功，而是要检查：

> 给定一个真实存在的低维机制结构，当前 MoE 是否真的能学到这些机制？

### 2.2 与语言 Zipfian 的关系

自然语言中的 token、phrase、concept 出现频率通常是长尾的。上一轮数据主要模拟的是表面 token / phrase 的 Zipfian 分布。

这次实验进一步抽象：

> 不只 token 频率长尾，潜在语义机制本身也可能长尾。

例如：

- 高频机制：通用语义模式；
- 中频机制：领域语义模式；
- 低频机制：稀有细粒度语义模式。

因此，本实验把语言表面的 token 去掉，只保留底层机制：

$$
mechanism\ frequency \sim Zipf(\alpha)
$$

这就是本实验和语言 Zipfian 的连接。

### 2.3 与 SVD 谱空间的关系

如果高频机制出现得多，它们对表征协方差的贡献更大；低频机制出现得少，它们可能落在中间或尾部谱方向。

整体协方差可以近似写成：

$$
\operatorname{Cov}(h)=\sum_{m=1}^{M}p_m B_mB_m^\top+\sigma^2I
$$

其中 $p_m$ 是机制 $m$ 的出现概率，$B_m$ 是机制 $m$ 的低维特征子空间。

SVD / PCA 是按方差大小排序，不是按机制语义排序。因此，一个重要问题是：

> SVD middle band 是否真的保留了适合 routing 的机制信息，还是把多个机制混在一起？

本实验第一阶段不直接比较 SVD；先确认 MoE 能不能在原始合成表征上恢复机制。等核心实验跑通后，再对生成的 $h$ 做 SVD，并比较 full representation、middle spectrum 和 sparse feature coordinates 的 routing 效果。

---

## 3. 核心假设

### H1：低维长尾机制可被 MoE 恢复

如果表征空间由若干低维特征组合和机制特异局部变换生成，且组合频率服从 Zipfian 分布，那么合适的 MoE 应该能把不同组合分给不同 experts，并让 expert 权重对齐真实特征方向与真实机制矩阵。

### H2：Oracle-Routing MoE 应该显著优于 Dense

如果数据确实由多个机制生成，并且不同机制需要不同函数处理，那么知道真实机制编号的 Oracle-Routing MoE 应该比参数量匹配的 Dense 模型更容易拟合。

如果 Oracle-Routing MoE 不强，说明数据本身没有制造出专家分工需求。

### H3：Learned Router 的失败可以定位 routing 问题

如果 Oracle-Routing MoE 强，但 Learned-Router MoE 弱，说明 expert structure 本身有用，但 router 没有从任务损失中学到正确机制。

### H4：Zipfian 会暴露 rare mechanism 学习问题

在 Zipfian 设置下，高频机制更容易被学到，低频机制可能出现 routing collapse、feature recovery 低、Oracle-Routing regret 高等问题。

这能帮助我们理解语言长尾中 MoE 对 rare feature / rare mechanism 的困难。

---

## 4. 数学建模

### 4.1 表征空间

设表征空间维度为：

$$
d
$$

构造一组标准正交基础方向：

$$
u_1,u_2,\dots,u_d\in\mathbb{R}^{d}
$$

第一版直接使用标准坐标基：

$$
u_j=e_j
$$

这样 feature recovery 最容易解释：第 $j$ 个方向就是第 $j$ 个坐标。

### 4.2 真实机制

设有 $M$ 个真实机制。每个机制 $m$ 选择 $k$ 个方向：

$$
S_m\subset\{1,\dots,d\},\quad |S_m|=k
$$

其中 $S_m$ 就是机制 $m$ 的真实低维特征组合。

### 4.3 机制频率

机制编号按 Zipfian 分布采样：

$$
p(m)=\frac{m^{-\alpha}}{\sum_{i=1}^{M}i^{-\alpha}}
$$

其中：

- smoke test 先设 $\alpha=0$，即 uniform distribution；
- $d=1024$ 主实验设 $\alpha=1.0$；
- 后续可加 $\alpha\in\{0.5,1.0,1.2\}$ 做强度扫描。

### 4.4 输入生成

每条样本先采样真实机制：

$$
m\sim Zipf(\alpha)
$$

再在机制对应的 $k$ 个方向上采样系数：

$$
a_j\sim\mathcal{N}(0,1),\quad j\in S_m
$$

输入向量为：

$$
h=\sum_{j\in S_m}a_ju_j+\epsilon
$$

其中噪声：

$$
\epsilon\sim\mathcal{N}(0,\sigma^2I)
$$

### 4.5 输出生成：显式机制矩阵

为了让 expert 必须学习机制，不做简单重构任务，而是让不同机制对应不同函数：

$$
A_m=U_m W_m U_m^\top
$$

$$
y=A_mh+\eta
$$

其中：

- $A_m$ 是机制 $m$ 的真实映射；
- $A_m$ 只主要作用在 $S_m$ 对应的低维子空间；
- $\eta$ 是输出噪声。

最小实现中，令输出维度与输入相同：

$$
y\in\mathbb{R}^{d}
$$

正式实验必须显式构造：

$$
U_m=[u_j]_{j\in S_m}\in\mathbb{R}^{d\times k}
$$

$$
W_m\in\mathbb{R}^{k\times k}
$$

$$
A_m=U_m W_m U_m^\top
$$

其中 $W_m$ 是机制 $m$ 在真实低维子空间内的局部变换。建议第一版使用可稳定比较的 full-rank 局部线性变换：

$$
W_m=O_{out,m}\operatorname{diag}(s_m)O_{in,m}^\top
$$

其中 $O_{in,m},O_{out,m}$ 是 $k\times k$ 正交矩阵，$s_m$ 是带机制特异性的奇异值谱。这样每个机制不只由支持集合 $S_m$ 定义，还由一个可比较的函数指纹 $W_m$ 定义。

为防止只靠“看到了哪个 support”就完成实验，主实验应加入一个小比例的 functional-pair probe：

1. 两个机制可以有高度重叠或相同的 $S_m$；
2. 它们的系数分布使用不同中心 $\mu_m$ 或不同 cone，使 $h$ 中仍然有可识别机制的信息；
3. 它们的 $W_m$ 明显不同。

这类 probe 的作用是区分：

> expert 只是学到了输入方向；

和：

> expert 真的学到了机制函数。

这样模型要学习的是：

$$
h\rightarrow y
$$

同时我们检查：

$$
expert_e\leftrightarrow (S_m,W_m,A_m)
$$

是否成立。

---

## 5. 什么叫 expert 必须学习机制？

“expert 必须学习机制”的意思是：数据不是由一个统一函数生成，而是由多个不同函数生成。

对于机制 $m$：

1. 输入只激活 $S_m$ 对应的 $k$ 个方向；
2. 输出由该机制自己的 $A_m$ 生成；
3. $A_m$ 中包含机制特异的局部矩阵 $W_m$；
4. 如果一个 expert 想在机制 $m$ 上表现好，它必须识别并使用 $S_m$ 对应方向，同时学习 $A_m$ 的局部映射。

所以“学到机制”不是一个抽象口号，而是三个可测事实：

1. 机制 $m$ 的样本主要被送到某个 expert；
2. 这个 expert 的权重主要依赖 $S_m$ 的方向；
3. 这个 expert 的有效矩阵接近真实 $A_m$ 或子空间内的 $W_m$；
4. 这个 expert 在机制 $m$ 上的 loss 比其他 expert 更低。

因此，单独看 right singular vectors / 输入方向是不够的。它只能说明 expert 看到了正确子空间，不能说明 expert 学到了正确机制函数。正式判断必须加入矩阵级与功能级指标。

---

## 6. 数据构建方案

### 6.1 Smoke Test 数据

用于确认 pipeline 正确。

| 项目 | 数值 |
|---|---:|
| 表征维度 $d$ | 64 |
| 机制数 $M$ | 4 |
| 每个机制维度 $k$ | 4 |
| expert 数 $E$ | 4 |
| Zipf 指数 $\alpha$ | 0，即均匀 |
| train samples | 20000 |
| valid samples | 4000 |
| test samples | 4000 |
| noise $\sigma$ | 0.01 |

Smoke test 通过标准：

1. Oracle-Routing MoE 明显优于 Dense；
2. Learned-Router MoE 至少能恢复大部分机制；
3. routing purity 和 feature recovery 显著高于随机水平。

### 6.2 主实验数据

Smoke test 结束后立即执行。

| 项目 | 数值 |
|---|---:|
| 表征维度 $d$ | 1024 |
| 机制数 $M$ | 100 |
| 每个机制维度 $k$ | 10 |
| expert 数 $E$ | 100 |
| Zipf 指数 $\alpha$ | 1.0 |
| train samples | 1,000,000 |
| valid samples | 100,000 |
| test samples | 100,000 |
| noise $\sigma$ | 0.01 |

如果资源紧张，主实验可以先用：

| 项目 | 数值 |
|---|---:|
| train samples | 200,000 |
| valid samples | 20,000 |
| test samples | 20,000 |

但报告中要注明这是 small-scale 主实验。

### 6.3 数据保存字段

每条样本保存：

| 字段 | 含义 | 用途 |
|---|---|---|
| `h` | 输入表征 | 模型输入 |
| `y` | 目标输出 | 任务监督 |
| `mechanism_id` | 真实机制编号 $m$ | routing purity / Oracle-Routing routing |
| `active_features` | 真实特征集合 $S_m$ | feature recovery |
| `U_m` 或 `basis_indices` | 真实机制子空间 | subspace alignment |
| `W_m` | 子空间内真实局部变换 | matrix recovery |
| `A_m` 或低秩表示 | 嵌入到 $d$ 维空间的真实机制矩阵 | function recovery |
| `frequency_rank` | Zipf 排名 | 高频/低频分析 |
| `frequency_bucket` | high / mid / rare | 长尾分桶分析 |
| `noise_sigma` | 噪声强度 | 复现实验 |

机制级元数据必须单独保存到 `mechanism_table.json`，至少包含：

| 字段 | 含义 |
|---|---|
| `mechanism_id` | 机制编号 |
| `support` | $S_m$ |
| `basis_indices` | 构造 $U_m$ 的 basis id |
| `local_transform` | $W_m$ |
| `embedded_transform_ref` | $A_m$ 的保存路径或低秩分解 |
| `coefficient_mean` | $\mu_m$，用于 functional-pair probe |
| `zipf_prob` | 机制采样概率 |
| `frequency_bucket` | high / mid / rare |
| `functional_pair_id` | 若属于同 support / 高 overlap 诊断对，则记录 pair id |

### 6.4 数据 sanity check

训练前必须检查：

1. 机制频率是否符合设定的 Zipfian 分布；
2. 每个机制是否恰好有 $k$ 个 active features；
3. 不同机制之间的 feature overlap 分布；
4. $W_m$ 是否 full-rank，且不同机制的 $W_m$ 距离分布足够分散；
5. functional-pair probe 是否可由 $h$ 中的系数分布识别，不构造不可辨识的多值映射；
6. 用真实机制编号的 Oracle-Routing predictor 是否可以明显降低 loss；
7. train / valid / test 的机制分布是否一致。

---

## 7. 模型设计

第一轮只跑三个核心模型。不要一开始引入 attention，以免混淆变量。

### 7.1 Dense 模型

无 router，无 expert 分发。

$$
\hat y=F_{dense}(h)
$$

作用：

> 判断一个普通模型能不能直接吃掉所有机制。

如果 Dense 已经接近 Oracle-Routing，说明任务太简单，无法验证专家分工。

### 7.2 Oracle-Routing MoE

直接使用真实机制编号 $m$ 选择 expert。

$$
\hat y=E_m(h)
$$

作用：

> 判断数据是否真的需要专家分工。

如果 Oracle-Routing MoE 明显优于 Dense，说明数据构造有效。

### 7.3 Learned-Router MoE

router 根据 $h$ 选择 expert。

$$
q(h)=\operatorname{softmax}(W_rh)
$$

$$
e^*=\arg\max_e q_e(h)
$$

$$
\hat y=E_{e^*}(h)
$$

训练目标默认使用任务损失：

$$
\mathcal{L}_{task}=\|\hat y-y\|_2^2
$$

如果出现所有样本进入少数 expert 的 collapse，再加入很小的负载均衡项：

$$
\mathcal{L}=\mathcal{L}_{task}+\lambda_{lb}\mathcal{L}_{balance}
$$

其中 $\lambda_{lb}$ 建议从 $0.01$ 开始。

负载均衡项的作用不是证明假设，而是防止训练退化。

---

## 8. 可选诊断模型

这部分不是第一轮必须跑，但如果 Learned-Router MoE 失败，需要快速定位原因。

### 8.1 Random Routing MoE

随机把样本送到 expert。

作用：

> 排除 MoE 只是因为参数更多而提升。

### 8.2 Supervised-Router MoE

给 router 额外机制标签监督：

$$
\mathcal{L}=\mathcal{L}_{task}+\lambda_{router}\mathcal{L}_{router-ce}
$$

其中 $\mathcal{L}_{router-ce}$ 是 router 预测真实机制编号的交叉熵。

作用：

> 区分“表征里没有机制信息”和“任务损失不能自动训练 router”。

如果 supervised router 能学好但 learned router 学不好，说明问题在 routing optimization，不在数据表征。

### 8.3 Attention + MoE 序列扩展

这是第二阶段，不进入第一轮最小实验。

当向量实验跑通后，再构造序列数据，让单个 token 的 $h_t$ 不足以判断机制，需要 attention 从上下文恢复机制。

模型：

1. Attention + Dense FFN；
2. Attention + Oracle-Routing MoE；
3. Attention + Learned-Router MoE。

作用：

> 连接回真实 Transformer 场景：真实 token 的机制往往需要上下文识别。

---

## 9. 实验步骤

### Step 1：实现数据生成器

输入参数：

- `d`
- `M`
- `k`
- `alpha`
- `num_train`
- `num_valid`
- `num_test`
- `noise_sigma`
- `seed`

输出：

- `train.pt`
- `valid.pt`
- `test.pt`
- `mechanism_table.json`
- `mechanism_transforms.pt`
- `data_sanity_report.json`

### Step 2：运行 smoke test

配置：

$$
d=64,\quad M=4,\quad k=4,\quad \alpha=0
$$

运行模型：

1. Dense；
2. Oracle-Routing MoE；
3. Learned-Router MoE。

必须输出：

1. train / valid / test MSE；
2. routing purity；
3. feature recovery；
4. subspace alignment；
5. mechanism matrix recovery；
6. expert usage entropy；
7. selected expert advantage；
8. Oracle-Routing regret。

### Step 3：如果 smoke test 通过，立即运行主实验

配置：

$$
d=1024,\quad M=100,\quad k=10,\quad \alpha=1.0
$$

运行模型：

1. Dense；
2. Oracle-Routing MoE；
3. Learned-Router MoE。

主实验必须额外输出分桶结果：

1. high-frequency mechanism performance；
2. mid-frequency mechanism performance；
3. rare-frequency mechanism performance；
4. functional-pair probe performance；
5. true-vs-learned mechanism distance correlation。

### Step 4：如果 learned router 明显失败，运行诊断模型

诊断顺序：

1. Random Routing MoE；
2. Supervised-Router MoE；
3. Learned-Router MoE + small load-balance；
4. SVD router input diagnostic。

不要一次性全跑复杂消融。每个诊断都要对应一个明确问题。

### Step 5：SVD 分析

对主实验生成的 $h$ 做 SVD / PCA。

比较三种 router 输入：

1. full $h$；
2. top spectrum；
3. middle spectrum；
4. sparse ground-truth active coordinates。

目的：

> 判断 SVD middle band 是否真的适合恢复机制，还是只是保留了高方差信息但混合了机制。

---

## 10. 指标定义与解释

### 10.1 Task Loss

定义：

$$
\mathcal{L}_{task}=\|\hat y-y\|_2^2
$$

解释：

> 模型是否完成了基本拟合任务。

但 task loss 不是最终证据。loss 下降只能说明模型表现更好，不能说明 expert 学到了真实特征。

### 10.2 Oracle-Routing Gap

定义：

$$
Gap_{Oracle-Routing}=L_{dense}-L_{Oracle-Routing}
$$

解释：

> 数据是否真的需要专家分工。

如果这个 gap 很小，说明 Dense 一个模型就能处理所有机制，当前数据不适合验证 MoE specialization。

### 10.3 Learned Gap

定义：

$$
Gap_{learned}=L_{dense}-L_{learned}
$$

解释：

> Learned-Router MoE 是否真的比 Dense 好。

如果 Oracle-Routing Gap 大但 Learned Gap 小，说明问题在 learned routing。

### 10.4 Routing Purity

对每个真实机制 $m$，统计它的样本被分到各 expert 的比例。

$$
Purity(m)=\max_e P(e|m)
$$

整体指标：

$$
Purity=\frac{1}{M}\sum_{m=1}^{M}Purity(m)
$$

解释：

> 同一个机制的数据是否主要进入同一个 expert。

如果 purity 低，说明 router 没有按真实机制分发。

### 10.5 Mechanism-Expert Matching Accuracy

由于 expert 编号可以任意置换，不能直接比较 expert id 和 mechanism id。

需要根据 confusion matrix 做 permutation-invariant matching。

解释：

> 在允许重新匹配 expert 编号后，router 是否恢复真实机制分组。

### 10.6 Feature Recovery

对每个 expert $e$，取其输入权重绝对值最大的 $k$ 个输入方向，记为：

$$
\hat S_e
$$

如果 expert $e$ 匹配到机制 $m$，则：

$$
FeatureRecovery(e,m)=\frac{|\hat S_e\cap S_m|}{k}
$$

解释：

> expert 权重主要依赖的方向，是否就是真实机制的 active features。

这是回答“是否看到了真实方向”的核心指标，但它不是最终证据。最终证据还需要 matrix recovery 和 functional specialization。

### 10.7 Subspace Alignment

如果 expert 权重不是简单坐标方向，而是一个子空间，则使用：

$$
Alignment(e,m)=\frac{1}{k}\|Q_e^\top U_m\|_F^2
$$

其中：

- $Q_e$ 是 expert 学到的输入子空间；
- $U_m$ 是真实机制子空间。

解释：

> expert 学到的子空间和真实机制子空间有多接近。

Smoke test 可以先用 Feature Recovery，主实验再加 Subspace Alignment。

### 10.8 Expert Effective Matrix

为了比较 expert 是否学到了真实机制函数，需要先为每个 expert 提取有效矩阵。

如果 expert 是线性或低秩线性结构，例如：

$$
E_e(h)=B_eA_eh
$$

则定义：

$$
\hat A_e=B_eA_e
$$

如果 expert 是非线性 MLP，则不要直接比较原始参数。应使用机制 $m$ 的样本估计局部线性化：

$$
\hat A_{e,m}^{Jac}=\mathbb{E}_{h\sim m}\left[\frac{\partial E_e(h)}{\partial h}\right]
$$

或者拟合一个 ridge linear surrogate：

$$
\hat A_{e,m}^{fit}=\arg\min_A \mathbb{E}_{h\sim m}\|E_e(h)-Ah\|_2^2+\lambda\|A\|_F^2
$$

解释：

> 不同 expert 学成什么样，必须通过有效函数或局部 Jacobian 比较，而不是只看 route id。

### 10.9 Mechanism Matrix Recovery

匹配 expert $e$ 与机制 $m$ 后，比较 expert 的有效矩阵和真实机制矩阵：

$$
MatrixCos(e,m)=
\frac{\langle \hat A_e,A_m\rangle_F}
{\|\hat A_e\|_F\|A_m\|_F}
$$

更稳的比较是在真实子空间内部：

$$
\hat W_{e,m}=U_m^\top\hat A_eU_m
$$

$$
LocalMatrixCos(e,m)=
\frac{\langle \hat W_{e,m},W_m\rangle_F}
{\|\hat W_{e,m}\|_F\|W_m\|_F}
$$

也报告归一化误差：

$$
LocalMatrixError(e,m)=
\frac{\|\hat W_{e,m}-c^\star W_m\|_F}{\|W_m\|_F}
$$

其中 $c^\star$ 是最佳标量缩放，用来避免训练尺度差异污染方向判断。

解释：

> 这个指标直接回答 expert 是否学到了机制 $m$ 的局部变换 $W_m$，而不是只学到输入方向。

### 10.10 Off-Support Leakage

定义机制投影：

$$
P_m=U_mU_m^\top
$$

输入侧 leakage：

$$
Leak_{in}(e,m)=
\frac{\|\hat A_e(I-P_m)\|_F}{\|\hat A_e\|_F}
$$

输出侧 leakage：

$$
Leak_{out}(e,m)=
\frac{\|(I-P_m)\hat A_eP_m\|_F}{\|\hat A_eP_m\|_F}
$$

解释：

> 如果 leakage 高，说明 expert 虽然可能 route 对了，但函数并没有集中在真实机制子空间上。

### 10.11 Functional Loss Matrix

对每个真实机制 $m$ 和每个 expert $e$，计算：

$$
L_{m,e}=\mathbb{E}_{h\sim m}\|E_e(h)-y\|_2^2
$$

匹配后的 expert $e(m)$ 应满足：

$$
L_{m,e(m)}\ll L_{m,e'},\quad e'\neq e(m)
$$

报告：

$$
FunctionalMargin(m)=\min_{e'\neq e(m)}L_{m,e'}-L_{m,e(m)}
$$

解释：

> 这是“专家是否真的专业化”的功能性证据。route purity 高但 functional margin 低，说明只是分开了，不代表 expert 学好了机制函数。

### 10.12 True-vs-Learned Mechanism Geometry

真实机制之间的函数距离：

$$
D^{true}_{m,n}=1-
\frac{\langle A_m,A_n\rangle_F}
{\|A_m\|_F\|A_n\|_F}
$$

匹配后的 expert 函数距离：

$$
D^{learned}_{m,n}=1-
\frac{\langle \hat A_{e(m)},\hat A_{e(n)}\rangle_F}
{\|\hat A_{e(m)}\|_F\|\hat A_{e(n)}\|_F}
$$

报告两者的 Spearman correlation。

解释：

> 如果 learned expert 的函数几何保留了真实机制几何，说明不同 expert 学到的不只是不同 route label，而是和真实机制差异相一致的函数差异。

### 10.13 Expert Usage Entropy

定义：

$$
H(E)=-\sum_e p(e)\log p(e)
$$

解释：

> router 是否 collapse 到少数 experts。

如果 entropy 很低，说明大部分 expert 没被使用。

### 10.14 Selected Expert Advantage

对每个样本，比较 router 选中的 expert 和其他 expert 的 loss。

$$
Adv(x)=\frac{1}{E-1}\sum_{e\neq e^*}L_e(x)-L_{e^*}(x)
$$

解释：

> router 选中的 expert 是否真的比其他 expert 更适合当前样本。

如果 routing purity 高但 advantage 低，说明分发看起来对了，但 expert 没有真正专业化。

### 10.15 Oracle-Routing Regret

定义：

$$
Regret(x)=L_{e^*}(x)-\min_e L_e(x)
$$

解释：

> 当前 router 选择和事后最优 expert 之间差多少。

越低说明 router 越接近最优分发。

### 10.16 Frequency-Bucket Metrics

按机制频率分成：

- high；
- mid；
- rare。

分别报告：

1. task loss；
2. routing purity；
3. feature recovery；
4. subspace alignment；
5. mechanism matrix recovery；
6. functional margin；
7. Oracle-Routing regret。

解释：

> Zipfian 长尾是否导致 rare mechanisms 学不好。

---

## 11. 结果解释树

### 情况 A：Oracle-Routing MoE 不强

观察：

$$
L_{dense}\approx L_{Oracle-Routing}
$$

结论：

> 数据没有制造出专家分工需求。

更新假设：

> 当前合成机制太弱，不能检验 MoE specialization。

下一步：

1. 降低 dense 容量；
2. 增强不同机制之间的函数冲突；
3. 增加机制数量或 overlap。

### 情况 B：Oracle-Routing 强，Learned-Router 弱

观察：

$$
L_{Oracle-Routing}\ll L_{dense},\quad L_{learned}\approx L_{dense}
$$

结论：

> 专家结构有用，但 learned router 没学会正确分发。

更新假设：

> 当前瓶颈是 routing optimization，而不是 expert capacity。

下一步：

1. supervised router；
2. router pretraining；
3. Oracle-Routing distillation；
4. small load-balance；
5. advantage-aware routing。

### 情况 C：Learned-Router loss 好，但 Feature Recovery 低

观察：

$$
L_{learned}\downarrow,\quad FeatureRecovery\downarrow
$$

结论：

> 模型找到了别的拟合方式，但没有恢复我们定义的真实特征机制。

更新假设：

> loss improvement 不能等价为 expert specialization。

下一步：

分析 learned expert 的实际子空间，判断它是否发现了另一种有效机制。

### 情况 D：Route / Subspace 对，但 Matrix Recovery 低

观察：

$$
Purity\uparrow,\quad SubspaceAlignment\uparrow,\quad LocalMatrixCos\downarrow
$$

结论：

> router 把样本分到了看似正确的 expert，expert 也看到了正确子空间，但没有学到真实机制函数 $W_m$。

更新假设：

> “数据方向匹配”不足以证明“不同 expert 学到了不同 feature / mechanism”。必须把 expert 的有效矩阵和真实 $A_m/W_m$ 对齐后再判断。

下一步：

1. 增强不同 $W_m$ 之间的函数冲突；
2. 加 functional-pair probe；
3. 检查 expert rank 是否足够表示 $W_m$；
4. 报告 local matrix cosine、off-support leakage、functional loss matrix。

### 情况 E：Functional Pair 失败

观察：

$$
S_{m_1}\approx S_{m_2},\quad W_{m_1}\neq W_{m_2}
$$

但 learned MoE 不能区分两个机制，或者两个机制被同一个 expert 以平均函数拟合。

结论：

> 当前模型只学到了 support-level 分组，没有学到机制函数级分工。

下一步：

1. 确认 $h$ 中有可识别机制的 coefficient cue，避免构造不可辨识问题；
2. 加 supervised router 或 oracle-distillation；
3. 增大 expert rank / capacity；
4. 增加机制函数差异。

### 情况 F：高频机制学得好，低频机制学不好

观察：

$$
Recovery_{high}\gg Recovery_{rare}
$$

结论：

> Zipfian 长尾导致 rare mechanism 难以被 router 和 expert 学到。

更新假设：

> 语言长尾中 MoE 的主要困难可能不是有没有 expert，而是 rare mechanism 缺少足够稳定的 routing / update。

下一步：

1. rare mechanism reweighting；
2. expert capacity protection；
3. sparse feature routing；
4. router auxiliary objective。

### 情况 G：Routing Purity 高，但 Selected Expert Advantage 低

结论：

> router 把样本分开了，但 expert 没有形成真正功能专门化。

更新假设：

> “分得开”不等于“分得好”，更不等于“专家专业化”。

下一步：

检查 expert 输入限制、expert 容量、训练目标和 gradient conflict。

---

## 12. 实验完成后的报告模板

### 目的

构造一个完全可控的合成表征空间，验证混合专家是否能恢复长尾分布的低维特征组合。

### 假设

【H1】如果表征空间由若干低维特征组合生成，且组合频率服从 Zipfian 分布，那么合适的混合专家应该能把不同组合分给不同 experts，并让 expert 权重对齐真实特征方向。

### 数学建模

$$
m\sim Zipf(\alpha)
$$

$$
S_m\subset\{1,\dots,d\},\quad |S_m|=k
$$

$$
h=\sum_{j\in S_m}a_ju_j+\epsilon
$$

$$
y=A_mh+\eta
$$

模型学习：

$$
h\rightarrow y
$$

并检查：

$$
expert_e\leftrightarrow (S_m,W_m,A_m)
$$

是否成立。

### 实验步骤

先做 smoke test：

$$
d=64,\quad M=4,\quad k=4
$$

确认 pipeline 能跑通，并检查 Dense、Oracle-Routing MoE、Learned-Router MoE 的 loss、routing purity 和 feature recovery。

smoke test 通过后，立即执行主实验：

$$
d=1024,\quad M=100,\quad k=10,\quad \alpha=1.0
$$

比较三类模型：

1. 稠密模型；
2. 真实路径混合专家；
3. 学习式分发混合专家。

核心指标：

1. task loss；
2. Oracle-Routing gap；
3. routing purity；
4. feature recovery；
5. subspace alignment；
6. mechanism matrix recovery；
7. off-support leakage；
8. functional loss matrix / selected expert advantage；
9. Oracle-Routing regret；
10. true-vs-learned mechanism distance correlation；
11. high / mid / rare mechanism 分桶表现。

### 预期结果与假设更新

如果 Oracle-Routing MoE 明显优于 Dense，说明数据确实制造了专家分工需求。

如果 Learned-Router MoE 接近 Oracle-Routing，并且 feature recovery、subspace alignment、matrix recovery 都高，说明 MoE 能恢复我们人为设定的低维机制组合和机制函数，支持 H1。

如果 Oracle-Routing MoE 强但 Learned-Router MoE 弱，说明结构有用但 learned router 没学会正确分发，应把后续重点转向 router training。

如果 Learned-Router MoE loss 下降但 feature recovery 或 matrix recovery 低，说明 loss 不能证明 expert specialization，后续必须继续用 feature-level 和 function-level 指标审查 expert。

如果高频机制恢复好、低频机制恢复差，说明 Zipfian 长尾会系统性影响 rare mechanism learning，这将把主线推进到 rare mechanism routing 和 sparse feature routing。

---

## 13. 30 秒汇报话术

这次我准备把实验重新退回到一个完全可控的数学世界。我们先不做自然语言，而是直接构造一个 $d$ 维表征空间，里面人为埋入 $M$ 个真实机制；每个机制有自己的低维 feature 子空间 $S_m$，也有自己的局部变换 $W_m$，并且这些机制按 Zipfian 长尾分布出现。模型要学习从输入表征 $h$ 到目标 $y=A_mh$ 的映射。我们比较稠密模型、真实路径 MoE 和学习式分发 MoE。重点不只看 loss，也不只看 route purity，而是看每个 expert 是否对应一个机制、是否抓到了对应的子空间、有效矩阵是否接近真实 $A_m/W_m$、以及它在该机制上的 loss 是否真的低于其他 expert。如果 Oracle-Routing 强但 learned router 弱，就说明问题主要在分发；如果 learned router 能恢复这些机制和机制函数，才说明 MoE 工具有能力支撑我们后续研究真实语言表征里的长尾低维结构。

---

## 14. 怎么表达得更清楚

### 14.1 不要这样说

> 我们又做了一个 synthetic dataset，然后看 MoE 有没有提升。

这样听起来像普通 benchmark，导师会继续追问：到底回答什么机制问题？

### 14.2 应该这样说

> 这个实验不是为了证明模型提升，而是为了验证工具是否能恢复我们亲手埋进去的机制。

### 14.3 最关键的一句话

> 如果模型连合成空间里已知的 $100$ 个 $10$ 维机制子空间和对应局部变换都恢复不了，那么我们不能用它去判断真实语言表征里是否存在类似结构。

### 14.4 回答“为什么要做这个实验”

> 因为现在我们有两个不确定性：第一，我们关于表征空间的假设可能是错的；第二，即使假设是对的，当前 MoE/router 也可能学不出来。这个实验先把第一个不确定性拿掉，构造一个假设一定成立的世界，专门检查模型工具能不能学出来。

### 14.5 回答“学出来是什么意思”

> 不是 loss 下降就叫学出来。学出来至少要满足四点：同一机制的数据被分到同一 expert；这个 expert 的输入/输出子空间对齐真实特征方向；这个 expert 的有效矩阵接近真实 $A_m/W_m$；这个 expert 在对应机制上的 loss 比其他 expert 更低。

---

## 15. 最小执行清单

第一天最小目标：

1. 写完数据生成器；
2. 跑通 $d=64,M=4,k=4$；
3. 得到 Dense / Oracle-Routing / Learned 三个模型的 loss；
4. 画 routing confusion matrix；
5. 计算 feature recovery；
6. 计算 local matrix cosine 和 functional loss matrix。

第二步立即执行：

1. 扩展到 $d=1024,M=100,k=10,\alpha=1.0$；
2. 复用同一套模型；
3. 输出 high / mid / rare 分桶指标；
4. 输出 functional-pair probe 指标；
5. 判断失败点属于 data、router、expert-function 还是 Zipfian rare mechanism。
