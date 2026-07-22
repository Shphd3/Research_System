# A08 Common-Removed Differential Expert Proxy Anchor

## 0. 一句话裁定

MPI 的最大启发不是“最大奇异方向就是好 router”，而是：

```text
router row 应该是 expert 的功能代理，而不是一组完全自由学习的 gate id。
```

但 MPI 的主要缺口是：

```text
principal singular direction 很可能是 common / high-frequency / high-gain direction，
不一定是 rare / residual / feature-specific / functionally distinctive direction。
```

因此本合集 anchor 的核心不是继续追求 load balance，而是把问题推进到：

```text
从 dominant expert proxy 转向 common-removed differential functional proxy。
```

换言之：

```text
我们不应问“router 是否更均匀分发 token”，
而应问“router 是否把 rare / residual feature 放进了足够厚、可保持、有功能价值的 expert margin basin”。
```

---

## 1. 当前困惑的直接澄清

### 1.1 现在的方法首先应被视为 initialization，不应直接 claim 是新 router

当前的 residual differential expert proxy 更适合作为一个 **initialization / audit object**：

```text
用 expert 参数和 hidden common operator 构造一个更合理的初始 router row，
然后观察它能否改善 rare-margin、proxy consistency 和 early preservation。
```

它还不是完整新 router，原因是：

1. 它只规定了 step-0 router row 怎么来；
2. 它还没有规定训练过程中 router row 如何持续避免 common recapture；
3. 它还没有证明 residual proxy 在 step 5/10 后仍然保持；
4. 它还没有证明 selected expert 对对应 feature/group 有 causal utility。

所以本 anchor 的实验阶梯应该是：

```text
diagnostic audit
-> initialization method
-> preservation intervention
-> router design candidate
-> functional utility test
```

只有当前三步都通过后，才能把它提升为真正 router：

```text
1. common operator 稳定；
2. residual differential proxy 比 raw principal proxy 更好地改善 rare margin；
3. residual/common-controlled routing 在 early training 中保持 partition，且 LM loss 不明显恶化。
```

### 1.2 hidden 减均值路由必须加入，但它是 sanity baseline，不是最终贡献

需要把 hidden mean-subtracted routing 加进 anchor，而且必须非常清楚地区分它的地位。

令 router input 为：

\[
h_i = \mu + r_i
\]

其中 \(\mu\) 是 route-position hidden population 的均值或 common direction。

普通 router logit：

\[
z_{i,e}=w_e^\top h_i=w_e^\top\mu+w_e^\top r_i
\]

hidden mean-subtracted routing 使用：

\[
\tilde h_i=h_i-\mu
\]

\[
\tilde z_{i,e}=w_e^\top(h_i-\mu)=w_e^\top r_i
\]

这会直接去掉 expert-specific common bias：

\[
a_e=w_e^\top\mu
\]

因此它改善 load balance 是很平凡的：如果大多数 token 共享同一个 \(\mu\)，去掉 \(\mu\) 以后，router 被迫按 residual direction 分发，而不是按 expert 对 common 的不同投影分发。

所以 hidden mean subtraction 应该加入，但它的身份是：

```text
common-removal sanity baseline / diagnostic control
```

而不是：

```text
新 router 的最终贡献
```

### 1.3 需要区分三种“减均值”

这点很重要。

#### A. 对 hidden 减均值：会改变 routing

\[
z_e=w_e^\top(h-\mu)
\]

这等价于从每个 expert logit 中减去不同常数：

\[
z_e \leftarrow z_e-w_e^\top\mu
\]

因此会改变 top-1 / top-k ranking。

#### B. 对 router rows 减 expert-wise 均值：通常不改变 routing

如果：

\[
\tilde w_e=w_e-\bar w,
\qquad
\bar w=\frac{1}{E}\sum_e w_e
\]

则：

\[
\tilde z_e=(w_e-\bar w)^\top h=w_e^\top h-\bar w^\top h
\]

对同一个 token，\(-\bar w^\top h\) 是所有 experts 共享的相同 scalar，因此不改变 top-k ranking，也不改变 softmax probability。

所以 router-row mean subtraction 不是有效 intervention，除非它和 row normalization、projection、optimizer dynamics 结合。

#### C. 对 common subspace 做 projection：会改变 routing

如果定义：

\[
P_R=I-P_C
\]

使用：

\[
z_e=(P_Rw_e)^\top h=w_e^\top(P_Rh)
\]

这会去除 common subspace 中的 router-hidden interaction。它是比单一 mean subtraction 更一般的 common-controlled routing。

---

## 2. 新 router 的目的到底是什么？

### 2.1 不是为了负载均衡

负载均衡只是 guard。它只能说明没有明显 single-expert collapse，不能说明 feature specialization。

一个 load-balanced router 仍可能失败：

```text
feature A 被随机分到多个 expert；
rare feature 和 common feature 仍共享同一高增益通道；
expert 对被 routed group 没有 causal utility；
step 0 看起来均匀，但 step 5/10 被 training overwrite。
```

### 2.2 目标是 rare / residual feature 的可保持分发

本线真正希望达成的是：

```text
common 不再决定 expert 分配；
rare/residual feature 拥有正 routing margin；
这个 margin 在 early training step 5/10 不跨 boundary；
selected expert 对对应 group 有更高 functional utility；
rare-feature interference 降低。
```

更形式化地，目标不是：

\[
\mathrm{Load}(e)\approx \frac{1}{E}
\]

而是：

\[
\mathrm{margin}_{rare}(i)
=
z_{i,e_i^\star}-\max_{j\ne e_i^\star}z_{i,j}
>0
\]

并且：

\[
\mathrm{margin}_{rare}^{t=10}(i)
\not<0
\]

### 2.3 设计目标的三层版本

#### Level 1: diagnostic router

用途：证明 common removal / residual routing 是否确实改变 rare margin。

形式：

\[
z_e=w_e^\top(h-\mu)
\]

或：

\[
z_e=w_e^\top P_Rh
\]

它不是最终方法，只是 causal diagnostic。

#### Level 2: initialization router

用途：用更好的 expert proxy 初始化 router rows。

形式：

\[
w_e^{init}=u_e^{diff}
\]

其中：

\[
u_e^{diff}=\mathrm{TopEig}^+\left(P_R(M_e-\bar M)P_R\right)
\]

这是当前最应该先做的 method object。

#### Level 3: actual router candidate

只有 Level 1/2 通过后，才进入。

可能形式：

\[
z_e=(P_Rw_e)^\top(P_Rh)
\]

或者在线 residual differential power update：

\[
\hat w_e=w_e\,P_R(M_e-\bar M)P_R
\]

\[
w_e\leftarrow C\frac{\hat w_e}{\|\hat w_e\|_2}
\]

这个才是接近“新 router”的版本。

---

## 3. 故事线

### 3.1 MPI 的正面启发

MPI 正确提出：

```text
router row 应该显式编码对应 expert 的信息。
```

这比 vanilla router 更有原则。

### 3.2 MPI 的关键不足

MPI 把 expert proxy 定义为 principal singular direction：

\[
u_e^{raw}=\mathrm{TopEig}(M_e)
\]

其中：

\[
M_e=W_eW_e^\top
\]

问题是：

```text
最大奇异方向代表 dominant gain，
但 dominant gain 往往来自 common / high-frequency / generic prediction channel，
不一定代表 rare / residual feature utility。
```

因此：

```text
MPI 解决了 expert-router coupling，
但没有解决 expert proxy 的功能语义选择。
```

### 3.3 我们的推进

我们不否定 MPI 的动机，而是把它推进一步：

```text
expert proxy 不应是 dominant proxy，
而应是 common-removed differential functional proxy。
```

即：

\[
u_e^{raw}=\mathrm{TopEig}(M_e)
\]

升级为：

\[
u_e^{diff}=\mathrm{TopEig}^+\left(P_R(M_e-\bar M)P_R\right)
\]

其中：

\[
\bar M=\frac{1}{E}\sum_j M_j
\]

\[
P_R=I-P_C
\]

### 3.4 最终可写成的论文问题

```text
What should an expert proxy represent?
```

不是：

```text
the dominant direction of an expert matrix
```

而是：

```text
the expert-distinctive residual direction that preserves rare-feature routing margin under early training.
```

---

## 4. Core Mathematical Model

### 4.1 Hidden decomposition

\[
h_i=c_i+r_i
\]

\[
c_i=P_Ch_i
\]

\[
r_i=(I-P_C)h_i=P_Rh_i
\]

### 4.2 Router logit decomposition

\[
z_{i,e}=w_e^\top h_i=w_e^\top c_i+w_e^\top r_i
\]

如果 \(c_i\approx c\) 对大量 token 共享，则：

\[
a_e=w_e^\top c
\]

成为 expert-specific common bias。

### 4.3 Expert gain matrix

对 expert \(e\)，定义 input-side gain：

\[
M_e=W_{g,e}W_{g,e}^\top
\]

或更一般地：

\[
M_e=J_e^\top J_e
\]

其中 \(J_e\) 是 expert 对输入 hidden 的局部 Jacobian。

### 4.4 Raw principal proxy

MPI-style proxy：

\[
u_e^{raw}=\mathrm{TopEig}(M_e)
\]

它最大化：

\[
u^\top M_eu
\]

但它不区分 common gain 与 residual functional gain。

### 4.5 Common-removed proxy

\[
M_e^{res}=P_RM_eP_R
\]

\[
u_e^{res}=\mathrm{TopEig}(M_e^{res})
\]

它去掉 common subspace，但仍然是 expert 自己的 residual dominant direction。

### 4.6 Differential residual proxy

\[
M_e^{diff}=P_R(M_e-\bar M)P_R
\]

\[
\bar M=\frac{1}{E}\sum_jM_j
\]

\[
u_e^{diff}=\mathrm{TopEig}^+(M_e^{diff})
\]

它表示：

```text
expert e 相对平均 expert 更敏感、且不在 common subspace 里的方向。
```

这才更接近 specialization proxy。

---

## 5. Hypotheses

### H1. Raw principal expert direction is common-dominated

\[
u_e^{raw}\]

可能与 \(C\) 高重合。

Supported if:

```text
overlap(u_raw, C) high;
raw principal routing increases common-bias spread;
raw principal routing does not improve rare margin.
```

Weakened if:

```text
overlap(u_raw, C) low;
raw principal routing improves rare margin and preservation.
```

### H2. Hidden mean subtraction improves load trivially but may not improve specialization

Supported if:

```text
hidden-mean routing lowers max_load / raises effective_experts,
but proxy_NMI, rare_margin, sign_flip, and utility do not improve.
```

This would show:

```text
load improvement from common removal is not sufficient evidence.
```

### H3. Residual differential proxy improves rare margin beyond mean-subtraction baseline

Supported if:

```text
u_diff improves rare_margin and proxy_NMI beyond hidden-mean routing and row-normalization controls.
```

This is the main positive evidence needed.

### H4. Initialization alone may not be enough

Supported if:

```text
u_diff improves step-0 margin, but ordinary training erases it by step 5/10.
```

This would move the project from initialization to preservation router design.

### H5. A real router candidate must preserve margin without harming LM loss

Supported if:

```text
residual router input or online residual projection preserves proxy_NMI / rare_margin through step 5/10,
and LM loss is not materially worse.
```

---

## 6. 合集 anchor 拆分

本 A08 是合集，不应一次性做成一个大实验。建议拆成以下小 anchors。

---

### A08_00 MPI Mechanism Reinterpretation Anchor

**问题**

MPI 的 improvement 到底来自：

```text
row retraction / norm equalization
```

还是：

```text
principal-direction expert coupling
```

**Variants**

```text
V0 vanilla router
V1 row normalization only
V2 raw MPI-style power + retraction
V3 hidden mean-subtracted routing
```

**Primary metrics**

```text
max_load only as guard
common_bias_spread
rare_margin
proxy_route_NMI
LM loss
```

**Decision**

如果 V1/V3 改善 load，但不改善 rare_margin / proxy_NMI，则说明：

```text
balance gain 是 common/scale control，不是 specialization。
```

---

### A08_01 Common Operator And Hidden-Centering Sanity Anchor

**问题**

能否定义稳定的 common operator \(P_C\)，并证明 hidden mean / common-subtracted routing 的效果不是 projector artifact？

**Common candidates**

```text
mean common vector: mu = E[h]
top hidden PC: C = span(PC_1:k)
route-position mean common
frequency-conditioned common
running EMA common
router-row-aligned common subspace
```

**Variants**

```text
raw h routing
h - mean(h) routing
(I - P_C)h routing for multiple P_C definitions
```

**Primary metrics**

```text
common_bias_spread
rare_margin
proxy_NMI
sign_flip@0->5/10
LM loss
projector robustness
```

**Decision**

如果 conclusion 随 \(P_C\) 定义翻转，则不能进入 method claim。

---

### A08_02 Raw Principal Common-Dominance Audit Anchor

**问题**

expert 的 principal singular direction 是否主要是 common direction？

**Objects**

\[
u_e^{raw}=\mathrm{TopEig}(M_e)
\]

\[
M_e=W_{g,e}W_{g,e}^\top
\]

**Metrics**

```text
overlap(u_raw, C)
overlap(u_raw, residual proxy clusters)
inter-expert diversity of u_raw
common_bias_spread induced by u_raw
rare_margin induced by u_raw
forced utility correlation
```

**Decision**

如果 \(u_e^{raw}\) 高度 common-aligned 且不改善 rare margin，则可正式提出 MPI proxy critique。

---

### A08_03 Residual Differential Expert Proxy Initialization Anchor

**问题**

比 raw principal proxy 更好的 expert proxy 是否应来自 residual differential gain？

**Proxy candidates**

\[
u_e^{raw}=\mathrm{TopEig}(M_e)
\]

\[
u_e^{res}=\mathrm{TopEig}(P_RM_eP_R)
\]

\[
u_e^{diff}=\mathrm{TopEig}^+(P_R(M_e-\bar M)P_R)
\]

**Variants**

```text
random init
row-normalized random init
raw principal proxy init
residual principal proxy init
differential residual proxy init
hidden-centered routing baseline
```

**Primary metrics**

```text
rare_margin@step0
proxy_route_NMI@step0
oracle-to-linear agreement
forced utility correlation
max_load as guard only
```

**Decision**

如果 differential residual proxy 明显优于 raw principal proxy 与 hidden-centering baseline，才能说它捕获了更接近 specialization 的 expert proxy。

---

### A08_04 Early Preservation Anchor

**问题**

好的 residual differential initialization 是否能穿过 early training？

**Variants**

```text
u_diff init + ordinary training
u_diff init + hidden-centered router input for steps 0-10
u_diff init + P_R router input for steps 0-10
u_diff init + router-row residual projection after optimizer step
u_diff init + early anti-lock-in temperature / softened routing
positive preservation control
```

**Primary metrics**

```text
rare_margin@0/5/10
proxy_route_NMI@0/5/10
sign_flip_rate@0->5/10
cluster-aware margin
LM loss
common_bias_spread
```

**Decision**

如果 init-only 失败，而 residual router input 成功，则说明问题已经从 initialization 上升为 router preservation mechanism。

---

### A08_05 Functional Value Anchor

**问题**

如果 partition 被保持，它是否有功能价值？

**Metrics**

```text
rare-feature loss
common/rare interference
selected-expert ablation delta
non-selected expert ablation delta
forced-routing utility correlation
route-function binding
```

**Decision**

只有这里通过，才能说 partition 有 expert specialization value。

---

### A08_06 Online Router Candidate Anchor

**前提**

只有 A08_01--A08_05 至少部分通过后才进入。

**候选 router**

Residual-input router:

\[
z_e=w_e^\top P_Rh
\]

Residual-row router:

\[
z_e=(P_Rw_e)^\top h
\]

Symmetric residual router:

\[
z_e=(P_Rw_e)^\top(P_Rh)
\]

Online residual differential MPI:

\[
\hat w_e=w_eP_R(M_e-\bar M)P_R
\]

\[
w_e\leftarrow C\frac{\hat w_e}{\|\hat w_e\|_2}
\]

**Decision**

如果 online residual router 比 initialization-only 更好地保持 rare margin，并且 LM loss 不恶化，才可以进入 “new router” claim。

---

## 7. 实验顺序

建议按以下顺序执行。

### Step 1: 先做 sanity split

```text
vanilla
row normalization only
hidden mean-subtracted routing
raw MPI-style principal proxy
```

目的：

```text
把 load balance gain 从 specialization gain 中拆出来。
```

### Step 2: common operator robustness

```text
mean common
top hidden PC
route-position mean
EMA common
router-row subspace common
```

目的：

```text
确保 common conclusion 不随 projector 翻转。
```

### Step 3: raw principal critique

```text
测 u_raw 与 C 的 overlap；
测 u_raw 是否改善 rare margin；
测 u_raw 是否只是降低 load。
```

目的：

```text
证明 MPI-style proxy 的问题不只是直觉，而是可测量的 common dominance。
```

### Step 4: residual differential proxy initialization

```text
u_raw vs u_res vs u_diff
```

目的：

```text
找出更好的 initialization proxy。
```

### Step 5: early preservation

```text
init-only vs residual router input vs residual row projection
```

目的：

```text
判断是否需要从 initialization 升级到 router mechanism。
```

### Step 6: functional value

```text
rare loss
interference
route-function binding
ablation utility
```

目的：

```text
避免只凭 route purity / load 误称 specialization。
```

---

## 8. Success Criteria

### 8.1 不能算成功的情况

```text
只改善 max_load；
只降低 balance loss；
只让 active experts 变多；
只在 step 0 有 proxy_NMI；
只在某个 P_C 定义下有效；
LM loss 明显恶化；
rare margin 没有改善；
sign flip 没有减少；
forced utility correlation 没有提升。
```

### 8.2 可以算 anchor 支持的情况

```text
1. raw principal proxy 与 common subspace 高重合；
2. hidden mean subtraction 改善 load 但不足以改善 rare margin；
3. residual differential proxy 比 raw principal proxy 改善 rare margin；
4. residual/common-controlled routing 减少 early sign flip；
5. proxy_route_NMI@step5/10 提高；
6. LM loss 不明显恶化；
7. conclusion 对 common projector 稳健。
```

### 8.3 可以升级为新 router 的情况

必须同时满足：

```text
initialization-only 不足；
residual router input / row projection 能保持 margin；
online residual differential coupling 进一步改善；
LM loss guard 通过；
functional value 有初步支持。
```

---

## 9. Claim Boundary

### 9.1 当前可以 claim

```text
MPI 提供了一个正确动机：router row 应该是 expert proxy。
但 principal singular direction 只代表 dominant gain，不保证代表 specialization。
因此有必要从 raw principal proxy 转向 common-removed differential functional proxy。
```

### 9.2 当前不能 claim

```text
我们已经有新 router；
common removal 本身就是 specialization；
hidden mean subtraction 是最终方法；
load balance improvement 证明 expert 功能分化；
real-DCLM 已经有语义 expert；
rare-feature utility 已经成立。
```

### 9.3 最安全的表述

```text
We reinterpret expert-proxy routing as a residual-margin preservation problem.
A valid expert proxy should be evaluated not by load balance, but by whether it removes common bias, improves rare-feature routing margin, survives early training, and eventually binds to expert utility.
```

---

## 10. Recommended Minimal Experiment: Raw Principal vs Residual Differential Proxy Audit

这是本合集 anchor 的第一优先推荐实验。

### 10.1 Question

```text
MPI-style raw principal expert proxy 到底是在学 expert function，还是在学 common high-gain direction？
Residual differential proxy 是否更接近 rare / residual specialization proxy？
```

### 10.2 Fixed objects

固定：

```text
same model checkpoint
same MoE layer(s)
same route-position hidden states H
same expert weights W_e
same audit batch
same proxy clusters or rare-feature labels if available
same common operator candidates P_C
```

### 10.3 Proxy definitions

Raw principal proxy:

\[
u_e^{raw}=\mathrm{TopEig}(M_e)
\]

Residual principal proxy:

\[
u_e^{res}=\mathrm{TopEig}(P_RM_eP_R)
\]

Differential residual proxy:

\[
u_e^{diff}=\mathrm{TopEig}^+(P_R(M_e-\bar M)P_R)
\]

Hidden mean-subtracted routing baseline:

\[
z_e=w_e^\top(h-\mu)
\]

Row-normalized random baseline:

\[
w_e=C\frac{w_e}{\|w_e\|_2}
\]

### 10.4 Variants

```text
V0 vanilla random router
V1 row-normalized random router
V2 hidden mean-subtracted router input
V3 raw principal proxy init
V4 residual principal proxy init
V5 differential residual proxy init
V6 differential residual proxy init + hidden mean-subtracted router input
V7 differential residual proxy init + P_R router input
```

### 10.5 Primary metrics

Do not use load as primary.

Primary:

```text
overlap(u, C)
common_bias_spread = Var_e(u_e^T c)
rare_margin@step0
rare_margin@step5/10 if trained
proxy_route_NMI@step0/5/10
sign_flip_rate@0->5/10
forced-routing utility correlation
LM loss
```

Guard:

```text
max_load
effective_experts
empty_expert_count
router entropy
selected gate probability entropy
gradient norm
```

### 10.6 Expected adjudication

#### Case A: hidden mean subtraction improves load only

Conclusion:

```text
Common removal produces trivial balance improvement, but not specialization.
Need residual differential proxy or preservation mechanism.
```

#### Case B: raw principal proxy has high common overlap

Conclusion:

```text
MPI-style expert proxy is dominant-gain proxy, not necessarily functional-specialization proxy.
```

#### Case C: residual differential proxy improves rare margin beyond hidden centering

Conclusion:

```text
Expert-distinctive residual gain is a better proxy target than raw principal singular direction.
Proceed to early preservation anchor.
```

#### Case D: residual differential proxy improves step-0 but fails step-5/10

Conclusion:

```text
Initialization is insufficient. Upgrade to residual/common-controlled router mechanism.
```

#### Case E: residual router input preserves margin without LM loss regression

Conclusion:

```text
This is the first point where a new router claim becomes plausible.
```

### 10.7 Final decision rule

Proceed only if:

```text
u_diff improves rare_margin over u_raw and hidden-mean baseline;
projector conclusion is robust;
LM loss guard passes;
step-5/10 sign flip decreases.
```

Park if:

```text
all gains reduce to load balance;
projector choice flips the result;
rare_margin does not improve;
LM loss worsens materially.
```
