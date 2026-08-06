# Todo3 实验设计：Head Removal 是否提升 MoE-relevant Separability

## 背景主线
MoE 的核心不是把 token 分给更多 expert，而是先把表示中的共享部分和长尾语义部分分开，再让 router 在真正有语义区分力的子空间里分流。
Todo3 要证明的是：去掉 centered representation 中的 shared head 后，语义组更容易被简单 router 分开；这种“更可分”会直接转化成更好的 expert specialization。

## 核心命题
Centered head removal 只有在一个条件下才有用：
被删掉的子空间主要承载组内共享噪音，而不承载组间语义信号。
形式上，若
delta_b / b < delta_w / w
则 head removal 会提升 separability。

## 研究问题
1. 去掉全局均值是否真的能提升 separability？
2. 去掉共享高方差 head 是否能提升 separability？
3. 如果语义信号泄漏到 head 中，head removal 是否会开始伤害 separability？

## 表示分解
对输入做 centered：
x_c = x - mu

估计 centered covariance 的 top-k 主方向 V_k，定义：
P_t = I - V_k V_k^T

得到 tail 表示：
x_tail = P_t x_c

## Separability 定义
对语义标签 z，定义：

- 组间散度
B_z = sum_c pi_c (mu_c - mu)(mu_c - mu)^T

- 组内散度
W_z = sum_c pi_c Cov(x | z=c)

- 几何 separability
Sep_F(P; z) = tr(P B_z P^T) / tr(P W_z P^T)

实验里再配一个 MoE-relevant 指标：

- 固定线性 router 的准确率
Sep_R(P; z) = linear-router accuracy on z

## 实验 A：Mean-only control
### 目的
证明“去掉均值更可分”不是理论核心。

### 数据
x = mu + m_z + eps
其中没有共享高方差 head，只有全局均值和语义均值。

### 对比
1. raw x
2. centered x - mu
3. centered 后随机删 k 维

### 预期
- raw 和 centered 的 Fisher separability 基本相同
- raw 和 centered 的线性 router 准确率基本相同
- 随机删维通常不会稳定变好，可能变差

### 结论用途
说明“去均值”本身不是你们要 claim 的深刻结论。

## 实验 B：Shared covariance head
### 目的
证明真正有用的是去掉 shared high-variance head。

### 数据
设 d = 16, head 维度 k_h = 4, 语义组数 K = 4

x = mu + U h + V m_z + eps

其中：
- U 是 head 子空间基
- h ~ N(0, alpha^2 I)，与 z 无关
- m_z 是不同语义组在 tail 子空间中的均值
- eps 是小噪音
- U^T V = 0

### 对比
1. raw
2. centered only
3. centered + PCA 去 top-k（ours）
4. centered + 随机删 k 维
5. oracle 去真实 U（上界）

### 指标
1. Fisher separability
2. 线性 softmax router 准确率
3. routing purity / NMI
4. 可选：固定“每组一个 expert”的 toy task loss

### 预期
- centered only 基本无明显提升
- ours 明显提升 Fisher ratio 和线性 router 准确率
- 随机删维不稳定
- oracle 最好，ours 接近 oracle

### 结论用途
证明“去 shared covariance head”而不是“去均值”，才是 non-trivial 的关键。

## 实验 C：Signal leakage sweep
### 目的
证明 head removal 不是 tautology，而是有条件命题。

### 数据
x = mu + U(h + rho q_z) + V m_z + eps

其中 rho 控制语义信号在 head 中的泄漏强度。

### sweep
rho in {0, 0.25, 0.5, 1.0}

### 预期
- rho 小时，去 head 明显有益
- rho 增大后，收益下降
- rho 足够大时，去 head 会伤害 separability

### 结论用途
说明只有当被删掉的 top-k 主要是共享噪音时，head removal 才成立。

## 推荐统一设置
- 训练样本：50k
- 测试样本：10k
- router：单层线性 softmax
- 不加 weight decay，避免和 Todo1 混在一起
- 先固定 k_h，再 sweep head 强度 alpha
- 再固定 alpha，sweep leakage rho

## 最后要汇报的图表
1. Sep_F vs alpha
2. 线性 router 准确率 vs alpha
3. Sep_F / 准确率 vs rho
4. raw / centered / ours / random-drop 的对比表

## 预期主结论
1. 去均值本身不是核心，几何指标基本不变
2. 去 shared high-variance head 能提升语义 separability
3. 提升是有条件的：只有删掉的主要是共享噪音而不是语义信号
4. 这种 separability 提升会直接转化成更低的 routing error，因此对 MoE specialization 有真实意义