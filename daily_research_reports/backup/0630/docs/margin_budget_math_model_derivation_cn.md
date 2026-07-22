# 数学建模笔记：早期训练保持的 Margin-Budget 动态

> 中文伴随版。英文原文仍是 canonical source：
> `margin_budget_math_model_derivation.md`

**状态：** Draft v0.1 for review  
**目的：** 解释 `A06_preservation_margin_budget` 背后的数学模型，以及每个实验如何控制或测量模型中的一项。

---

## 术语解释

**隐藏状态（hidden state）**  
含义：模型在某个 token / sample 位置产生的向量表示。  
具体对象：

$$
h_i(t)\in\mathbb{R}^d
$$

它重要是因为路由器接收的就是隐藏状态。它不能直接说明该表示中哪部分是有用特征。

**固定特征 / 代理标签（fixed feature / proxy label）**  
含义：审计时固定不变的 feature 或 cluster label。  
具体对象：

$$
y_i\in F
$$

它重要是因为 preservation 必须有一个固定对象。如果每个 checkpoint 都重新聚类，问题会变成 tracking，而不是 assignment preservation。

**特征中心（feature center）**  
含义：同一标签样本的隐藏状态均值。  
具体对象：

$$
\mu_f(t)=\frac{1}{|I_f|}\sum_{i\in I_f}h_i(t),
\quad
I_f=\{i:y_i=f\}.
$$

**路由行向量（router row）**  
含义：专家 $e$ 的线性打分向量。  
具体对象：

$$
w_e(t)\in\mathbb{R}^d.
$$

**成对路由 gap（pairwise router gap）**  
含义：原始 assigned expert 和某个竞争 expert 的打分方向差。  
具体对象：

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

它定义了 assigned expert 与 competitor 之间的决策边界方向。

**成对 margin（pairwise margin）**  
含义：feature center 在原专家一侧的安全距离，用 logit 差表示。  
具体对象：

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top\mu_f(t).
$$

如果 $\gamma_{f,e}(t)>0$，则 $\mu_f(t)$ 对原专家 $a(f)$ 的得分高于竞争专家 $e$。

---

## 1. 建模目标

目标是把一个定性的 preservation 问题：

> 为什么 feature-to-expert routing partition 能在早期训练中保持或失败？

转化为一个定量几何条件：

> 初始 routing margin 是否大于训练累积的 feature-center drift 和 router-boundary drift？

本文定义数学对象，推导 margin dynamics，并把每个实验审计映射到模型中的某一项。

---

## 2. 对象与定义

### 2.1 Hidden states

令：

$$
h_i(t)\in\mathbb{R}^d
$$

表示 token/sample $i$ 在训练步 $t$ 的隐藏状态。

### 2.2 Fixed feature / proxy label

令：

$$
y_i\in F
$$

表示样本 $i$ 的固定 feature/proxy label。在 synthetic setting 中它可以是真实特征标签；在 real-DCLM proxy setting 中它可以是固定 cluster label。

这个标签在审计中固定。如果每个 checkpoint 都重新聚类，preservation question 就变成 tracking question，而不是 assignment preservation。

### 2.3 Feature center

对特征 $f$：

$$
\mu_f(t)=\frac{1}{|I_f|}\sum_{i\in I_f}h_i(t),
\quad
I_f=\{i:y_i=f\}.
$$

这就是 feature center。

### 2.4 Router row

对专家 $e$：

$$
w_e(t)\in\mathbb{R}^d.
$$

top-1 router score 是：

$$
z_e(h,t)=w_e(t)^\top h.
$$

routed expert 是：

$$
\hat e(h,t)=\arg\max_e w_e(t)^\top h.
$$

### 2.5 Initial assignment

第 0 步，每个 feature center 被分给获胜专家：

$$
a(f)=\arg\max_e w_e(0)^\top \mu_f(0).
$$

这是要被测试是否保留的 target assignment。

### 2.6 Pairwise router gap

对竞争专家 $e\neq a(f)$，定义：

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

这个向量定义 assigned expert 和 competitor $e$ 之间的决策边界。

### 2.7 Pairwise margin

center-level margin 是：

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top\mu_f(t).
$$

如果 $\gamma_{f,e}(t)>0$，feature center $\mu_f(t)$ 对原专家 $a(f)$ 的得分高于竞争专家 $e$。

对特征 $f$，保留 center assignment 需要：

$$
\gamma_{f,e}(t)>0,\quad \forall e\neq a(f).
$$

对所有特征，保留 center assignment 需要：

$$
\Gamma(t)=\min_f\min_{e\neq a(f)}\gamma_{f,e}(t)>0.
$$

---

## 3. Margin dynamics 推导

### 3.1 Drift definitions

令：

$$
\Delta\mu_f(t)=\mu_f(t)-\mu_f(0),
$$

$$
\Delta u_{f,e}(t)=u_{f,e}(t)-u_{f,e}(0).
$$

则：

$$
\mu_f(t)=\mu_f(0)+\Delta\mu_f(t),
$$

$$
u_{f,e}(t)=u_{f,e}(0)+\Delta u_{f,e}(t).
$$

### 3.2 展开 margin

从：

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top\mu_f(t)
$$

开始。代入 drift decomposition：

$$
\gamma_{f,e}(t)
=
\bigl(u_{f,e}(0)+\Delta u_{f,e}(t)\bigr)^\top
\bigl(\mu_f(0)+\Delta\mu_f(t)\bigr).
$$

展开：

$$
\gamma_{f,e}(t)
=
u_{f,e}(0)^\top\mu_f(0)
+
\Delta u_{f,e}(t)^\top\mu_f(0)
+
u_{f,e}(0)^\top\Delta\mu_f(t)
+
\Delta u_{f,e}(t)^\top\Delta\mu_f(t).
$$

因为：

$$
\gamma_{f,e}(0)=u_{f,e}(0)^\top\mu_f(0),
$$

所以：

$$
\gamma_{f,e}(t)=
\gamma_{f,e}(0)
+
D^{\mathrm{router}}_{f,e}(t)
+
D^{\mathrm{feature}}_{f,e}(t)
+
D^{\mathrm{interaction}}_{f,e}(t),
$$

其中：

$$
D^{\mathrm{router}}_{f,e}(t)
=
\Delta u_{f,e}(t)^\top\mu_f(0),
$$

$$
D^{\mathrm{feature}}_{f,e}(t)
=
u_{f,e}(0)^\top\Delta\mu_f(t),
$$

$$
D^{\mathrm{interaction}}_{f,e}(t)
=
\Delta u_{f,e}(t)^\top\Delta\mu_f(t).
$$

### 3.3 每一项的意义

| Term | Formula | Meaning |
|---|---|---|
| Initial margin | $\gamma_{f,e}(0)$ | 第 0 步安全区 |
| Router-boundary drift | $\Delta u^\top \mu_0$ | router rows / decision boundaries 相对原中心移动 |
| Feature-center drift | $u_0^\top\Delta\mu$ | hidden feature center 相对原边界移动 |
| Interaction drift | $\Delta u^\top\Delta\mu$ | router 和 feature center 耦合移动 |

当：

$$
\gamma_{f,e}(t)<0
$$

margin 翻转。等价地：

$$
D^{\mathrm{router}}+
D^{\mathrm{feature}}+
D^{\mathrm{interaction}}
<
-\gamma_{f,e}(0).
$$

所以 preservation failure 可以读成：

> training-induced negative drift consumes the initial margin.

---

## 4. Margin budget bound

用 Cauchy-Schwarz 不等式：

$$
|D^{\mathrm{router}}|
=
|\Delta u^\top\mu_0|
\leq
\|\Delta u\|\|\mu_0\|,
$$

$$
|D^{\mathrm{feature}}|
=
|u_0^\top\Delta\mu|
\leq
\|u_0\|\|\Delta\mu\|,
$$

$$
|D^{\mathrm{interaction}}|
=
|\Delta u^\top\Delta\mu|
\leq
\|\Delta u\|\|\Delta\mu\|.
$$

定义 drift budget：

$$
B_{f,e}(t)
=
\|\Delta u_{f,e}(t)\|\|\mu_f(0)\|
+
\|u_{f,e}(0)\|\|\Delta\mu_f(t)\|
+
\|\Delta u_{f,e}(t)\|\|\Delta\mu_f(t)\|.
$$

则：

$$
\gamma_{f,e}(t)
\geq
\gamma_{f,e}(0)-B_{f,e}(t).
$$

因此，一个充分保持条件是：

$$
\gamma_{f,e}(0)>B_{f,e}(t).
$$

这是充分条件，不是必要条件。实际符号可能相互抵消。因此应同时报告 exact decomposition terms 和 norm-bound budget。

---

## 5. Cluster-aware extension

center margin 只保证 center 的 assignment。单个 token 仍可能跨越边界。

令：

$$
h_i(t)=\mu_f(t)+\epsilon_i(t).
$$

则：

$$
u_{f,e}(t)^\top h_i(t)
=
u_{f,e}(t)^\top\mu_f(t)
+
u_{f,e}(t)^\top\epsilon_i(t)
=
\gamma_{f,e}(t)+u_{f,e}(t)^\top\epsilon_i(t).
$$

如果：

$$
\|\epsilon_i(t)\|\leq \rho_f(t),
$$

则：

$$
u_{f,e}(t)^\top h_i(t)
\geq
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t).
$$

定义 robust cluster-aware margin：

$$
\tilde{\gamma}_{f,e}(t)=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f^{(q)}(t),
$$

其中 $\rho_f^{(q)}(t)$ 是高分位半径，例如 90% 或 95%。

如果：

$$
\tilde{\gamma}_{f,e}(t)>0,
$$

则 feature $f$ 中大多数样本应仍在原边界一侧。

这个扩展区分三种情况：

1. center assignment 保持，但 cluster spread 增大；
2. center assignment 失败；
3. cluster assignment 比 center assignment 更早失败。

---

## 6. Common/residual decomposition

### 6.1 Feature center decomposition

令：

$$
\mu_f(t)=c(t)+r_f(t),
$$

其中：

$$
c(t)=\frac{1}{|F|}\sum_f \mu_f(t)
$$

是 common/dense component，

$$
r_f(t)=\mu_f(t)-c(t)
$$

是 feature residual。

### 6.2 Margin decomposition

则：

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top c(t)+u_{f,e}(t)^\top r_f(t).
$$

定义：

$$
C_{f,e}(t)=u_{f,e}(t)^\top c(t),
$$

$$
Q_{f,e}(t)=u_{f,e}(t)^\top r_f(t).
$$

所以：

$$
\gamma_{f,e}(t)=C_{f,e}(t)+Q_{f,e}(t).
$$

### 6.3 解释

- $C_{f,e}(t)$：common direction contribution。
- $Q_{f,e}(t)$：feature-residual contribution。

如果 router gaps $u_{f,e}(t)$ 旋向 common/dense directions，那么 $C_{f,e}(t)$ 可以占主导，使 feature residual separation 变得不再重要。

这连接到 common-component / early-lock-in 直觉：

> The feature signal may still exist in $r_f(t)$, but the router boundary no longer separates it.

中文含义：特征信号可能仍在残余成分 $r_f(t)$ 中，但路由边界已经不再按它分割。

### 6.4 Common-driven failure signature

common-driven failure 应表现为：

1. router gaps 与 $c(t)$ 的对齐增强；
2. residual term $Q_{f,e}(t)$ 下降或不稳定；
3. expert load concentration 增强；
4. proxy-route NMI 下降；
5. loss 仍可接受地下降，说明训练本身没有简单失败。

---

## 7. 对立解释及其特征

### R1：Proxy feature instability

解释：feature/proxy label 本身不稳定；preservation 失败是因为要被保持的对象并不真实或不稳定。

特征：

- checkpoint 间 cluster stability 低；
- feature centers 不可恢复；
- step-0 routing 已经弱或 seed-unstable。

区分方式：

- 检查 cluster stability；
- 检查 step-0 proxy-route NMI；
- 检查 $\mu_f(t)$ 是否仍可区分。

如果为真：margin model 不是第一失败点。

### R2：Weak linear bridge

解释：router 从一开始就没有真正对齐 proxy partition。

特征：

- 低 $\gamma(0)$；
- 低 step-0 NMI；
- 初始 assignment 不稳定。

区分方式：

- step-0 bridge audit；
- initial margin audit。

如果为真：preservation 问题提出过早，应回到 initialization。

### R3：Feature-center drift dominates

解释：hidden feature centers 离开初始位置的速度超过 router 保持 assignment 的能力。

特征：

$$
u_0^\top\Delta\mu
$$

是 margin change 的主导负项。

区分方式：

- feature center drift audit；
- replaying fixed router on checkpoint hidden states；
- center-tracking oracle。

如果为真：下一步决策是是否需要 tracking 或 representation stabilization。

### R4：Router-boundary drift dominates

解释：router rows 或 decision boundaries 离开 feature-residual directions，可能漂向 common/dense directions。

特征：

$$
\Delta u^\top\mu_0
$$

是主导负项。

区分方式：

- router row drift audit；
- frozen hidden replay；
- common alignment audit。

如果为真：下一步是 anti-lock-in 或 common-controlled routing。

### R5：Coupled drift dominates

解释：hidden drift 或 router drift 单独都不能解释失败，二者交互项重要。

特征：

$$
\Delta u^\top\Delta\mu
$$

很大且为负。

区分方式：

- joint trajectory analysis；
- 比较 frozen-router、frozen-hidden replay 和 ordinary training。

如果为真：下一步应建模 co-adaptation dynamics，而不是单边 drift。

### R6：Expert feedback / objective incompatibility

解释：即使 margin 几何上保持，expert learning dynamics 或 next-token objective 也会让 partition 在功能上不稳定。

特征：

- margins remain positive but NMI or functional utility still drops；
- 只有 partition 破坏时 loss 才改善；
- positive preservation control 伤害 loss。

区分方式：

- LM loss guard；
- expert ablation utility；
- fixed-router / positive preservation control。

如果为真：preservation 可能与目标不兼容，或者本身没有用。

### R7：Margin is correlational, not causal

解释：大 margin 只是更好 condition 的标记，不是 preservation 的原因。

特征：

- natural seeds 有相关性，但 margin shrink/removal 不改变 NMI；
- 改变 margin 的干预不改变 preservation。

区分方式：

- controlled margin shrink/removal；
- matched-load and matched-loss comparisons。

如果为真：margin 只是 diagnostic，不是 mechanism。

---

## 8. 实验如何控制每个量

### 8.1 Initial margin control

量：

$$
\gamma_{f,e}(0)
$$

改变方式：

1. scale center-initialized router rows；
2. interpolate between center initialization and random initialization；
3. reduce pairwise separation among router rows；
4. reduce selected-gate confidence while preserving argmax where possible。

风险：global row scaling 会改变 softmax confidence 和 router gradients。除非被控制，否则应标为 diagnostic。

### 8.2 Feature-center drift control

量：

$$
\Delta\mu_f(t)
$$

测量方式：

- 用固定 labels 在 checkpoints 计算 $\mu_f(t)$；
- 比较 $\|\Delta\mu_f(t)\|$；
- 把 $\Delta\mu_f(t)$ 投影到 initial router gaps $u_{f,e}(0)$。

控制方式：

1. 如果可行，freeze earlier layers 或 hidden generator；
2. replay checkpoint hidden states through fixed router；
3. 比较 controlled synthetic setting 和 real-DCLM proxy setting；
4. center-tracking oracle。

### 8.3 Router-boundary drift control

量：

$$
\Delta u_{f,e}(t)
=
\Delta w_{a(f)}(t)-\Delta w_e(t)
$$

测量方式：

- router row norm drift；
- router gap norm drift；
- $u(t)$ 和 $u(0)$ 的 cosine；
- 投影到 $\mu_f(0)$、$c(0)$ 和 $r_f(0)$。

控制方式：

1. freeze router；
2. slow router learning rate；
3. router regularization toward initial rows；
4. anti-lock-in window；
5. common-controlled router input。

### 8.4 Common-direction alignment control

量：

$$
u_{f,e}(t)^\top c(t)
$$

测量方式：

- common term $C_{f,e}(t)$；
- router gaps 和 common direction 的 cosine；
- step 0 到 step 5/10 的 common alignment gain。

控制方式：

1. router-input centering；
2. common-logit cancellation；
3. residual-only router diagnostic；
4. 比较 full hidden input 与 common-controlled input。

### 8.5 Token-level robustness control

量：

$$
\tilde{\gamma}_{f,e}(t)
=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t)
$$

测量方式：

- within-feature radius；
- high-quantile distance to center；
- token-level sign flip rate；
- 每个 feature 内的 route purity。

控制方式：

1. 在 synthetic setting 中降低 hidden noise；
2. 比较 center routing 和 token routing；
3. 测量 training 中 cluster spread 是否增长。

---

## 9. 指标表

| Metric | Formula | Meaning | Main use |
|---|---|---|---|
| Center margin | $\gamma_{f,e}(t)$ | feature center assignment safety | 核心 preservation 对象 |
| Min margin | $\Gamma(t)$ | worst-case safety | 早期预警 |
| Drift budget | $B_{f,e}(t)$ | margin consumption 的上界 | 充分条件 |
| Consumption ratio | $R=B/(\gamma(0)+\varepsilon)$ | margin budget 是否耗尽 | 预测失败 |
| Sign flip rate | $\Pr[\gamma<0]$ | 成对 assignment 翻转比例 | 机制读数 |
| Cluster-aware margin | $\tilde{\gamma}$ | token-level robust margin | 解释 NMI 与 center margin 的差距 |
| Router drift term | $\Delta u^\top\mu_0$ | router-side failure | lock-in 诊断 |
| Feature drift term | $u_0^\top\Delta\mu$ | hidden-side failure | tracking 诊断 |
| Interaction term | $\Delta u^\top\Delta\mu$ | co-adaptation failure | 耦合动态 |
| Common term | $u^\top c$ | common/dense alignment | common-component 诊断 |
| Residual term | $u^\top r_f$ | feature-specific separation | specialization 诊断 |
| proxy-route NMI | $\mathrm{NMI}(y_i,\hat e_i)$ | route-label agreement | 主结果 |
| LM loss | loss | predictive guard | 防止坏保持 |

---

## 10. 建议分析表

### Table 1: Per-condition summary

| condition | seed | step | proxy_route_NMI | LM_loss | max_load | initial_min_margin | margin_consumption_q90 | sign_flip_rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|

### Table 2: Drift attribution

| condition | seed | step | router_term_mean | feature_term_mean | interaction_term_mean | dominant_negative_term |
|---|---:|---:|---:|---:|---:|---|

### Table 3: Common/residual audit

| condition | seed | step | common_alignment_gain | residual_term_drop | NMI_drop | interpretation |
|---|---:|---:|---:|---:|---:|---|

### Table 4: Margin intervention

| intervention | step0_assignment_ok | margin_change | NMI@5 | NMI@10 | loss_guard | interpretation |
|---|---|---:|---:|---:|---:|---|

---

## 11. 预期图

1. **NMI vs margin consumption ratio**：x-axis 是 $R(t)$，y-axis 是 proxy-route NMI。
2. **Margin trajectory**：$\Gamma(0), \Gamma(5), \Gamma(10)$。
3. **Drift attribution stacked bar**：router term、feature term、interaction term。
4. **Common vs residual term plot**：训练中的 $u^\top c$ 和 $u^\top r_f$。
5. **Sign flip heatmap**：feature $f$ by competitor expert $e$，颜色表示 $\gamma_{f,e}$ 是否翻转。

---

## 12. 如何读结果

### Outcome A：Margin model supported

观察：

- initial margin predicts preservation；
- margin consumption predicts NMI drop；
- margin shrink reduces NMI；
- sign flips track NMI drop。

解释：

```text
Preservation is at least partly governed by a margin budget.
```

允许下一步：

```text
Test interventions that increase initial margin, reduce drift, or track moving centers.
```

### Outcome B：Router drift dominates

观察：

- feature centers stable；
- router gaps rotate；
- common alignment increases；
- NMI drops。

解释：

```text
Failure is router-side early lock-in or common-direction attraction.
```

允许下一步：

```text
Test common-controlled router input, common-logit cancellation, router slow update, or anti-lock-in window.
```

### Outcome C：Feature drift dominates

观察：

- router rows stable；
- feature centers move across decision boundaries；
- tracking oracle helps。

解释：

```text
Failure is hidden-side feature-center drift.
```

允许下一步：

```text
Test tracking or representation-stabilization mechanisms.
```

### Outcome D：Margin not predictive

观察：

- margin metrics 和 NMI 没有关系；
- margin intervention 不影响 preservation。

解释：

```text
Margin is not the right central mechanism.
```

允许下一步：

```text
Park margin; inspect expert feedback, optimizer geometry, objective incompatibility, or metric definition.
```

### Outcome E：Preservation hurts loss

观察：

- margin 或 tracking 保持了 NMI；
- LM loss 明显变差。

解释：

```text
Preserving the partition may conflict with predictive learning.
```

允许下一步：

```text
Do not claim method success. Move to utility/objective compatibility analysis.
```

---

## 13. 与当前研究主线的关系

这个模型不替代更广的 05/06/07 chain。它只锐化第 3 层：preservation。

当前路线变成：

```text
05 failure mechanism:
common component and early feedback can create wrong routing basins.

06 initialization:
feature/proxy centers can initialize step-0 routing.

06 preservation:
margin-budget model tests whether early training exhausts the assignment margin.

07 utility:
only after preservation succeeds should common/rare interference or expert utility be tested.
```

它防止一个常见错误：

```text
High step-0 NMI does not imply training preservation.
Preservation does not imply utility.
Utility must be tested after preservation.
```

---

## 14. Codex 实现检查清单

运行代码前，必须明确这些字段：

```text
data:
model:
checkpoints:
fixed labels:
router row source:
initial assignment definition:
conditions:
primary metric:
secondary metrics:
known good case:
known bad case:
known confusing case:
success criterion:
failure criterion:
insufficient-evidence criterion:
claim boundary:
```

Codex 应输出：

```text
tables/margin_by_feature_expert.csv
tables/drift_decomposition.csv
tables/condition_summary.csv
figures/nmi_vs_margin_consumption.png
figures/margin_trajectory.png
figures/drift_attribution.png
summary.md
detailed.md
```

不要允许 Codex 添加超出 approved protocol 的新 claim。

---

## 15. 审阅问题

批准这个模型前，检查：

1. $a(f)$ 是从 step 0 固定，还是每步重新计算？
2. feature/proxy labels 是否固定，且足够有意义以支持 preservation？
3. router row scale 是否被控制，还是 scaling 改变了训练动态？
4. 解释 token-level NMI 时是否包含 cluster radius？
5. common/residual components 是否定义一致？
6. 模型是否区分 center assignment 和 token assignment？
7. 实验是否包含 LM loss guard？
8. 什么结果会证伪 margin-budget hypothesis？
9. 什么结果会迫使我们放弃把 margin 作为中心机制？
10. 这个结果会改变哪一个确切的下一步决策？
