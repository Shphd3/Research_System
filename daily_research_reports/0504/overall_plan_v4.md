# 最终统一 Hierarchical Synthetic Mechanism Recovery 实验计划

## Summary

最终实验统一使用 **hierarchical additive synthetic 数据**。Uniform 和 Zipf 只改变 leaf 机制频率，所有候选模型都跑在同一类数据构造上，避免之前 flat / hierarchical 数据不一致的问题。

最终报告只保留线性路由主线，不再汇报 $[h,h^2]$ + MLP top-1 MoE。

## 数据构造

基础公式仍保留为机制恢复的一般形式：

$$
m\sim p(m)
$$

$$
S_m\subset \{1,\dots,d\}
$$

$$
h=\sum_{j\in S_m}a_ju_j+\epsilon
$$

$$
y=A_mh+\eta,\quad A_m=U_mW_mU_m^\top
$$

Hierarchical 下机制细化为 leaf：

$$
m=(c,f),\quad C=10,\quad F=10,\quad M=CF=100
$$

每个 leaf 的输入由三部分组成：

$$
h=h_g+h_c+h_{c,f}+\epsilon
$$

其中：

$$
S_{c,f}=S_g\cup S_c\cup S_{c,f}^{tail}
$$

最终使用：

$$
d=1024,\quad |S_g|=16,\quad |S_c|=6,\quad |S_{c,f}^{tail}|=4
$$

所以 hierarchical leaf 的有效 support size 是：

$$
|S_{c,f}|=26
$$

输出矩阵为 additive ground truth：

$$
A_{c,f}=A_g+A_c+A_{c,f}^{tail}
$$

$$
A_g=U_gW_gU_g^\top
$$

$$
A_c=U_cW_cU_c^\top
$$

$$
A_{c,f}^{tail}=U_{c,f}^{tail}W_{c,f}^{tail}(U_{c,f}^{tail})^\top
$$

因此：

$$
y=(A_g+A_c+A_{c,f}^{tail})h+\eta
$$

Uniform：

$$
p(c,f)=\frac{1}{100}
$$

Zipf：

$$
p(\text{leaf}=r)=\frac{r^{-1}}{\sum_{j=1}^{100}j^{-1}}
$$

训练数据规模固定：

$$
\text{train}=20000,\quad \text{valid}=5000,\quad \text{test}=5000
$$

seeds 固定为 `[0,1,2]`。

## 模型候选池

### 1. 稠密模型

控制组，无路由：

$$
\hat y=Dh
$$

dense 使用 ridge 闭式拟合，只作为下界控制，不声明与 learned MoE 训练流程一致。

### 2. 真实路径混合专家

Oracle flat leaf MoE：

$$
e^*(h)=m=(c,f)
$$

$$
\hat y=E_{e^*(h)}(h)
$$

作用：验证如果路由正确，100 个 leaf 机制是否可恢复。

### 3. 学习式线性分发 MoE

所有 learned flat MoE 都使用线性 no-bias router，不使用 $h^2$，不使用 MLP。

主线 variants：

$$
\ell(h)=Wh
$$

$$
\ell(h)=Wh,\quad L=L_{\text{task}}+0.01L_{\text{balance}}
$$

$$
\ell(h)=W(h-\mu)
$$

$$
\ell(h)=W\Pi_{17:207}(h-\mu)
$$

$$
\ell(h)=W\Pi_{17:d}(h-\mu)
$$

所有 variants：

- expert 输入完整 $h$；
- 参数量完全一致；
- 同一 run / seed 下使用同一份 train / valid / test；
- 训练超参一致。

### 4. Hierarchical MoE

PCA 只用 train split 估计：

$$
\mu=\frac{1}{N}\sum_i h_i
$$

$$
\Sigma=\frac{1}{N}\sum_i(h_i-\mu)(h_i-\mu)^\top
$$

$$
\Sigma=P\Lambda P^\top
$$

$$
\Pi_{a:b}=P_{a:b}P_{a:b}^\top
$$

coarse routing：

$$
x_M=\Pi_{17:207}(h-\mu)
$$

$$
c^*=\arg\max_c W_Cx_M
$$

fine routing：

$$
x_{Mtail}=\Pi_{81:207}(h-\mu)
$$

$$
f^*=\arg\max_f W_F^{(c^*)}x_{Mtail}
$$

D1 conditional input：

$$
\hat y=E_g(h)+E^{cc}_{c^*}(x_M)+E^{tail}_{c^*,f^*}(x_{Mtail})
$$

D2 full input：

$$
\hat y=E_g(h)+E^{cc}_{c^*}(h)+E^{tail}_{c^*,f^*}(h)
$$

Oracle Hierarchical D1 / D2 使用真实 $(c,f)$ 路由。

### 5. Random Routing MoE

Flat random routing：

$$
e^*(h)=\operatorname{RandomBalanced}(h)
$$

Hierarchical random routing：

$$
c^*,f^*=\operatorname{Random}(h)
$$

作用：排除“多 expert 参数”本身带来的收益。

## Implementation Changes

需要整理三个入口：

1. `run_synthetic_hierarchical_recovery.py`
   - 保留当前 additive hierarchical 数据构造；
   - 确认 Uniform / Zipf 都在 leaf 层面采样；
   - hierarchical router 使用 linear PCA projection；
   - flat leaf baseline 改为 linear no-bias router，不能再用 $[h,h^2]$ + MLP。

2. 新增 final configs
   - `final_hierarchical_uniform_linear.json`
   - `final_hierarchical_zipf_linear.json`

3. 重写报告
   - 目标文件：`synthetic_mechanism_recovery_presentation_report.md`
   - 只引用 final run 结果；
   - 删除旧 flat single-mechanism 主线；
   - 删除旧 quadratic hierarchical 结果；
   - 删除 CE pretrain / supervised router / longer training。

## Training Consistency

所有 learned 模型统一：

$$
\text{epochs}=30,\quad \text{batch}=256,\quad \text{lr}=0.003
$$

$$
\text{weight decay}=10^{-4},\quad \text{grad clip}=1.0
$$

训练目标：

$$
L_{\text{task}}=\mathbb{E}\left[\|\hat y-y\|_2^2\right]
$$

LB variant：

$$
L=L_{\text{task}}+0.01L_{\text{balance}}
$$

$$
L_{\text{balance}}=E\sum_e\bar p_e^2-1,\quad
\bar p_e=\frac{1}{B}\sum_{i=1}^{B}p_e(h_i)
$$

报告中明确：

- learned 模型之间训练流程一致；
- dense / oracle / random 是控制组；
- 同一 run / seed 下所有模型共享同一份数据。

## Metrics

预测误差：

$$
L_{\text{model}}=\mathbb{E}\left[\|\hat y-y\|_2^2\right]
$$

路由混淆矩阵：

$$
C[m,e]=\#\{i:m_i=m,\ r(h_i)=e\}
$$

Purity：

$$
\operatorname{Purity}(m)=\frac{\max_e C[m,e]}{\sum_e C[m,e]}
$$

NMI：

$$
\operatorname{NMI}(M,E)=\frac{I(M;E)}{\sqrt{H(M)H(E)}}
$$

Usage：

$$
\operatorname{UsageNorm}=\frac{H(E)}{\log E}
$$

LocalCos：

$$
\hat W_{e,m}=U_m^\top \hat A_eU_m
$$

$$
\operatorname{LocalCos}(e,m)=
\frac{\langle \hat W_{e,m},W_m\rangle_F}
{\|\hat W_{e,m}\|_F\|W_m\|_F}
$$

Hierarchical 额外汇报：

- global matrix cosine；
- coarse matrix cosine；
- tail matrix cosine；
- coarse NMI / leaf NMI；
- high / mid / rare bucket loss。

## Experiment Runs

先 quick verify：

- `final_hierarchical_uniform_linear --quick`
- `final_hierarchical_zipf_linear --quick`

检查：

- PCA projector 来自 train split；
- router metadata 不出现 `raw_square` / MLP；
- flat leaf baseline 不使用 $h^2$；
- D1 / D2 参数量一致；
- summary 和 bucket summary 正常生成。

再 full run：

- `final_hierarchical_uniform_linear`
- `final_hierarchical_zipf_linear`

每个 full run 使用 seeds `[0,1,2]`。

## Report Structure

报告按你给的结构写：

1. 目的  
   构造可控 synthetic representation space，验证 MoE 是否恢复长尾低维特征组合。

2. 假设  
   【H1】如果表征空间由若干低维特征组合生成，且组合频率服从 Zipf，那么合适的 MoE 应把不同组合分给不同 expert，并让 expert 权重对齐真实机制方向。

3. 数学建模  
   先写基础机制公式，再写 hierarchical 细化。

4. 实验流程  
   - 模型选择；
   - 数据构造；
   - 训练流程；
   - 指标。

5. 实验结果  
   - Uniform；
   - Zipf；
   - Zipf high / mid / rare。

6. 结论  
   - 正确路由是否必要；
   - 线性分发 variation 的差异；
   - hierarchical 是否利用了 additive 结构；
   - rare leaf 是否仍是主要困难。

## Assumptions

- 最终主线只使用 hierarchical additive 数据。
- Uniform 和 Zipf 只改变 leaf 采样频率。
- 不再汇报 $[h,h^2]$ + MLP top-1 MoE。
- 不再汇报旧 hierarchical quadratic router。
- 不再汇报 CE pretrain / supervised router。
- 参数量控制采用组内严格：flat linear variants 内一致，D1/D2 内一致。
