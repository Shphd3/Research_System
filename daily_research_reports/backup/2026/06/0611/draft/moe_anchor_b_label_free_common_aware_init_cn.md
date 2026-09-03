# Anchor B 中文拆分稿：无标签 Common-Aware 路由器初始化

Source: `daily_research_reports/0611/draft/moe_storyline_anchor_plan_0611.md`

Scope: This file extracts the Anchor B part. It assumes Anchor A has made the real/semi-real representation geometry worth testing. It asks whether hidden-state geometry can define a label-free router initialization.

## 0. researcher judgment record

父问题：稀疏 top-1 点积 MoE 的 early collapse 可能来自 common-logit bias。  
当前子问题：没有 slot labels 时，能否用 hidden-state geometry 初始化 router，降低 common-induced expert bias。  
核心假设：router rows 若初始化到 common-orthogonal 或 residual-cluster subspace，common margin 会下降，route diversity 和 feature/residual alignment 会改善。  
最小测试：比较 random、slot-init upper bound、common-orthogonal、common-equalized、residual-cluster、oracle cancellation。  
当前边界：目标不是立刻击败负载均衡，而是证明机制导出的初始化能降低早期 common-bias-driven collapse。  
下一步决策：如果 init-only 只改善早期但最终仍坍缩，下一锚点应转向 persistent common-control / anti-lockin。

## 1. Purpose

Anchor B 回答：

```text
Can we construct a router initialization from hidden-state geometry, without slot labels, that reduces common-induced expert bias and improves feature/residual-aligned routing?
```

中文含义：能否不用人工 slot 标签，只用 hidden states 的共享/残差几何，构造一个更少受 common bias 影响的 router 初始化。

这直接对齐导师的“router initialization method”方向。

## 2. Why This Is a Second Anchor

Anchor B 依赖 Anchor A。

Anchor A 问：

```text
真实/半真实表征中是否存在 common-logit 初始化问题？
```

Anchor B 问：

```text
如果存在，能否利用这个几何设计无标签初始化方法？
```

这两个问题的证据标准不同，所以必须分开。

## 3. Decision Question

```text
Can a label-free common-aware initialization reduce or equalize w_e^T C in real/synthetic hidden spaces, improving initialization-time routing diversity and feature/residual alignment without using slot labels?
```

中文表述：

```text
无标签 common-aware 初始化能否在真实/合成 hidden spaces 中降低或均衡 w_e^T C，
并在不使用 slot labels 的情况下改善初始化时的路由多样性和 feature/residual alignment？
```

## 4. Problem Definition

随机 router 初始化忽略 hidden-state common subspace。更好的初始化应做到至少一种：

1. 去掉 common projection。
2. 让所有 experts 对 common component 的投影近似相等。
3. 把 experts 分布到 residual/unique variation 上，而不是 common variation 上。

不在范围内：

- 不把“击败 load balance”作为第一目标。
- 不声称 full training stability 已解决。
- 不使用 oracle slot labels 作为主方法，只作为 upper bound。

## 5. Physical Prior

P1：router 不应根据 feature-independent common directions 分配流量。  
含义：如果 $c$ 不携带本轮 feature 身份，$w_e^Tc$ 造成的 expert preference 是偏置而不是专门化。  
可能错误的情况：common direction 本身承载任务相关信息，移除它会伤害 routing。

P2：初始化阶段应让 experts 覆盖 residual/unique variation。  
含义：残差部分 $R$ 更可能包含区分 feature 或 cluster 的信息。  
可能错误的情况：残差聚类不稳定，或者 feature 信息并不在 residual subspace 中。

P3：负载均衡和 common-aware init 解决的问题不同。  
含义：负载均衡控制每个专家收到多少样本，common-aware init 控制早期分配由什么信息决定。  
可能错误的情况：负载均衡 alone 已经同时解决 utilization 和 alignment。

## 6. Hypothesis

H1：common-orthogonal 或 common-equalized 初始化能降低 common margin。  
支持条件：初始化后 $w_e^TC$ 的 spread 明显低于 random init。  
削弱条件：common margin 没有下降，或下降不影响 routing。

H2：residual-cluster 初始化能改善 feature/residual alignment。  
支持条件：在相似 utilization 下，feature_NMI、slot_NMI、cluster_NMI 或 per-feature purity 高于 random init。  
削弱条件：只改善 max_load，不改善 alignment。

H3：common-aware init 与 load balance 互补。  
支持条件：LB + common-init 在 alignment 上优于 LB alone，且 utilization 不更差。  
削弱条件：LB dominates both utilization and feature alignment。

## 7. Minimal Mathematical Model

隐藏状态分解：

$$
H=C+R
$$

common-orthogonal 投影：

$$
P_{\perp C}=I-C(C^TC)^{-1}C^T
$$

初始化选项：

1. common-orthogonal init：

$$
w_e^{(0)} \leftarrow P_{\perp C}\xi_e
$$

2. common-equalized init：

$$
w_e^T c \approx constant \quad \forall e
$$

3. residual-cluster init：

$$
w_e^{(0)} \propto \mu_e(P_{\perp C}H)
$$

关键指标：

- common margin：是否成功降低 common-induced expert bias。
- route diversity：max_load、active experts、entropy。
- feature/residual alignment：slot_NMI、feature_NMI、cluster_NMI、purity。
- accuracy：检查初始化是否牺牲任务可学性。

## 8. Minimal Tests

Experiment 1：Synthetic label-free init。  
比较条件：

- random init。
- oracle slot-init upper bound。
- common-orthogonal init。
- common-equalized init。
- residual-cluster init。
- oracle common-logit cancellation upper bound。

主要指标：

- slot_NMI。
- per-slot purity。
- accuracy。
- max_load。
- common margin。
- slot margin。

Experiment 2：Real frozen init audit。  
问题：同样初始化方法在真实/半真实 hidden states 中是否改善 step-0 routing。  
主要指标：step-0 route concentration、common margin、feature/residual purity。

Experiment 3：Small training sanity。  
优先在合成设置中训练；如果时间允许，再做小型真实/半真实 MoE。  
目的：检查 init-only 的早期收益是否能保持，还是训练后又 lock-in / collapse。

Experiment 4：Load balance comparison。  
用 2x2 表：

| | no common-aware init | common-aware init |
|---|---|---|
| no load balance | baseline | common init only |
| load balance | LB only | LB + common init |

测量：

- max_load。
- active experts。
- feature_NMI / route purity。
- common margin。
- accuracy。

## 9. How To Compare With Load Balance

不要写成：

```text
common-aware init beats load balance.
```

应写成：

```text
load balance 控制每个 expert 得到多少流量；
common-aware init 控制早期 assignment 由什么信息决定。
```

中心比较：

```text
At similar utilization, does common-aware initialization improve feature/residual alignment compared with load balance alone?
```

中文含义：在专家使用率相近时，common-aware 初始化是否比单独负载均衡更能保留 feature/residual structure。

如果 common-aware init 只降低 max_load，但 feature/residual alignment 不变，那么它只是另一个 utilization trick，不足以支撑机制方法 claim。

## 10. Falsifiable Outcomes

Supported if:

- common-aware init lowers common margin.
- route diversity improves.
- feature/residual alignment improves at same or similar load.
- LB + common-init improves alignment beyond LB alone.

Weakened if:

- common-aware init only improves max_load but not feature/residual alignment.
- residual-cluster init is unstable across seeds or representation sources.
- gains disappear immediately after short training.

Failure if:

- common-aware init does not reduce common margin.
- LB dominates both utilization and feature alignment.
- method depends on oracle slot labels.

## 11. Current Evidence

Observation：slot-init interpolation 显示 basin transition。  
Interpretation：初始化可以把 routing 推入更 slot-aligned 的 basin。  
Boundary：slot-init 使用 oracle slot labels，不能作为真实方法。

Observation：common cancellation improves slot_NMI。  
Interpretation：common-logit 是可干预机制，不只是相关性。  
Boundary：oracle cancellation 仍不是无标签初始化。

Observation：no-attention-residual routing suggests common-source control improves routing but not perfectly。  
Interpretation：控制 common/source signal 有帮助，但不是完整解法。  
Boundary：不能声称 full stability 或 functional specialization。

## 12. Claim Boundary And Next Decision

Can claim, if supported:

```text
a mechanism-derived, label-free common-aware initialization principle can reduce early common-bias-driven route collapse.
```

Cannot claim:

- 初始化 alone 解决完整训练坍缩。
- common-aware init 可以替代 load balance。
- 已证明完整语言模型中的功能性专家专门化。
- 方法已经在大规模 MoE 中可部署。

Next decision:

```text
If init-only helps early routing but final collapse returns, the next anchor should be persistent common-control / anti-lockin.
```

## 13. Agent Task Extraction

Agent Task B：Synthetic Label-Free Initialization。

Deliverables:

- common-orthogonal init。
- common-equalized init。
- residual-cluster init。
- compare to random / slot-init / oracle cancellation。

Metrics:

- slot_NMI。
- per-slot purity。
- accuracy。
- max_load。
- common margin。
- slot margin。

Agent Task C：Load Balance Comparison。

Deliverable:

```text
2x2 table:
baseline
LB only
common-init only
LB + common-init
```

Goal:

```text
show whether LB and common-aware initialization solve different parts of the problem.
```

Agent Task D：Expert Count Scaling。

Deliverables:

- $E=4,8,16,32,64,128$。
- random init vs common-aware init。
- synthetic and frozen-real variants if possible。

Main question:

```text
Does common-projection winner dominance grow with E, and does common-aware init suppress it?
```
