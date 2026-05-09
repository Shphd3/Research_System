# EXP summary

## 1. 主线确认

我们现在的研究主线是：

1. 先把 common / tail 分开，再做 routing，是否优于直接对原表征路由。
2. 即使不做 routing，只把 common branch 和 tail branch 分开，是否已经能改善 long-tail 学习。
3. 如果 tail 内部还有 coarse/fine 结构，再继续分层是否值得。

## 2. 最重要的假设确认

现阶段的最重要的假设确认：

- H1[Shared-Head Hypothesis]：真实 hidden 中存在 shared high-variance head，tail residual 比 raw hidden 更适合 long-tail 语义区分。
    $$
    x_t = P_t(x - \mu)
    $$
    【现阶段结论证明，将表征分开并不能导致更好的专家专业化。（哪个实验能支撑呢）】
- H2[Single-Layer Split-First Hypothesis]]：在我们使用单层替换的情况下，将common和tail分开学 优于 flat raw MoE；其主要收益先来自 split，再可能来自 tail-conditioned 的routing。当前证据也进一步表明，主要收益来自于：
    $$
    E_c(x) + E_t(x_t)
    $$
    【但是现阶段不能确定是否是参数量带来的性能差异。（哪个实验能支撑呢？）】

- H3[Recursive-Tail Hypothesis]：如果 tail 内部存在 coarse/fine hierarchy，则 recursive factorization / routing 还能进一步改善更细粒度的rare tail部分。
  【我们做了toy model的理想的实验，发现分发从一开始的coarse就没有分发好，最后导致fine的专家也学不好，首要还是要解决routing的问题】

## 2. 实验部分

令

$$
x_t=P_t(x-\mu),\qquad P_t=I-V_kV_k^\top
$$

其中$x_t$ 就是去均值并去掉 shared head 后的 `tail residual`。

| 配置                             | 数学形式                                                        | router 看什么 | expert 看什么 | 它在控制什么                     |
| -------------------------------- | --------------------------------------------------------------- | ------------- | ------------- | -------------------------------- |
| `baseline_ffn`                   | \(h_{\text{out}}=h_{\text{in}}+E(x)\)                           | 无            | full \(x\)    | 普通单层 FFN 基线                |
| `flat_moe_raw_uniform`           | \(h_{\text{out}}=h_{\text{in}}+E_c(x)+\sum_i g_i(x)E_i(x)\)     | raw \(x\)     | raw \(x\)     | flat raw MoE                     |
| `split_dense_tail_uniform`       | \(h_{\text{out}}=h_{\text{in}}+E_c(x)+E_t(x_t)\)                | 无            | tail \(x_t\)  | 只看 split，本身有没有收益       |
| `uniform_expert_mixture_tail`    | \(h_{\text{out}}=h_{\text{in}}+E_c(x)+\frac1N\sum_i E_i(x_t)\)  | 无            | tail \(x_t\)  | 只加多 expert 容量，不做 routing |
| `router_tail_expert_raw_uniform` | \(h_{\text{out}}=h_{\text{in}}+E_c(x)+\sum_i g_i(x_t)E_i(x)\)   | tail \(x_t\)  | raw \(x\)     | 只改 router 输入                 |
| `router_raw_expert_tail_uniform` | \(h_{\text{out}}=h_{\text{in}}+E_c(x)+\sum_i g_i(x)E_i(x_t)\)   | raw \(x\)     | tail \(x_t\)  | 只改 expert 输入                 |
| `hier_moe_tail_uniform`          | \(h_{\text{out}}=h_{\text{in}}+E_c(x)+\sum_i g_i(x_t)E_i(x_t)\) | tail \(x_t\)  | tail \(x_t\)  | full split-first 单层 hier       |

给出最重要的几个决定性的实验：

### Phase1：真实表征审计

目的：验证H1
更新作用：更新H1
当前结论：真实hidden 中存在低秩shared head，并且`tail residual`的probe / purity / NMI 稳定优于raw/centered; 这是所有的split-first结构的基础。【有个问题是，现在标签都不可靠，所以NMI是不要报告的，purity是不是指每个类别的纯净程度呢？至少我们知道，去掉tail能更分开了吧？】

### Phase2【不主要】：单层 split 控制器实验

目的：几何上的split优势是否能转换为训练收益，同时测试optimizer（LR）/WD是否为主要矛盾
更新：弱更新H2
当前结论：WD/LR 对于训练的影响不是主线。

### Phase3 【不主要】：使用了domain的auxiliary loss，不能反映目前真实训练范式下的情形，因此决定不汇报

### Phase4 【主要】

一句话版本：

目的：
步骤：
结果：
结论：
可信版本更新：

### Phase5 【主要】

一句话版本：这个实验我们探究了使用一层hierarchical结构分开，是否能够比普通moe在任务

目的：
步骤：
结果：
结论：
可信版本更新：

### Phase6 【主要】

一句话版本：

目的：
步骤：
结果：
结论：
可信版本更新：


## 3.阶段性结论



