# 小型锚点：特征到专家门控的 Margin-Budget 保持机制

> 中文伴随版。英文原文仍是 canonical source：
> `A06_preservation_margin_budget_mini_anchor.md`

**状态：** Draft v0.1 for review  
**锚点家族：** A06 preservation  
**短名：** `A06_preservation_margin_budget`  
**核心决策：** 早期训练中的分发保持，能不能建模成一个 margin budget 问题？

---

## 术语解释

**特征中心（feature center）**  
含义：同一个特征或代理标签下，隐藏状态向量的平均位置。  
具体对象：

$$
\mu_f(t)=\mathbb{E}[h_i(t)\mid y_i=f]
$$

它重要是因为路由器实际看到的是隐藏状态几何；如果特征中心移动，原来的路由边界可能不再适用。它不能单独证明专家有功能价值。

**路由行向量（router row）**  
含义：每个专家对应一个打分方向。  
具体对象：

$$
w_e(t)
$$

专家 $e$ 对隐藏状态 $h$ 的分数是 $w_e(t)^\top h$。它重要是因为 top-1 路由就是比较这些分数。它不能证明被选专家真的有用。

**初始特征到专家指派（initial feature-to-expert assignment）**  
含义：第 0 步时，每个特征中心被哪个专家选中。  
具体对象：

$$
a(f)=\arg\max_e w_e(0)^\top \mu_f(0)
$$

后续 preservation 问题测试的是这个初始指派是否保留，而不是每一步重新聚类后是否看起来仍然对齐。

**成对边际（pairwise margin）**  
含义：原本应属专家相对某个竞争专家的分数差。  
具体对象：

$$
\gamma_{f,e}(t)=\bigl(w_{a(f)}(t)-w_e(t)\bigr)^\top \mu_f(t),
\quad e\neq a(f)
$$

如果 $\gamma_{f,e}(t)>0$，特征中心 $\mu_f(t)$ 仍在原专家 $a(f)$ 一侧。它重要是因为 margin 是分发是否会翻转的几何安全区。它不能证明该分发有功能收益。

**最小边际（minimum margin）**  
含义：所有特征和所有竞争专家中最危险的边际。  
具体对象：

$$
\Gamma(t)=\min_f\min_{e\neq a(f)}\gamma_{f,e}(t)
$$

它是最保守的保持性预警指标。

**代理路由归一化互信息（proxy-route NMI）**  
含义：固定特征/代理标签 $y_i$ 和路由结果 $\hat e_i(t)$ 的一致程度。  
它重要是因为它能读出 route-label agreement。它不能证明语义专家存在，也不能证明专家有功能价值。

---

## 0. researcher judgment record

### 现象

用特征或代理中心初始化路由器时，第 0 步可以构造出一个 feature-to-expert 分区。但是早期训练后，路由指派可能退化：route NMI 下降、特征到专家的分工变弱，或者路由塌缩到少数专家。

### 机制猜想

第 0 步路由指派只有在初始 routing margin 足够大时才会被保留。这个初始 margin 必须吸收训练中三个对象的相对移动：

1. **特征中心**：训练过程中隐藏状态簇均值移动；
2. **路由行向量**：专家打分向量移动；
3. **公共/稠密方向**：共享成分吸引路由决策区域。

### 因果关系

如果：

$$
\Gamma(0) > \text{training-induced drift budget},
$$

则预期 feature-to-expert routing 会被保留。

如果：

$$
\Gamma(0) \leq \text{training-induced drift budget},
$$

则部分 margin 会变成负数，路由指派改变，proxy-route NMI 下降。

### 可观测指标

- 初始最小 margin：$\Gamma(0)$
- 特征中心漂移：$\|\mu_f(t)-\mu_f(0)\|$
- 路由 gap 漂移：$\|u_{f,e}(t)-u_{f,e}(0)\|$，其中 $u_{f,e}=w_{a(f)}-w_e$
- margin 消耗比例：drift budget / initial margin
- sign flip rate：$\gamma_{f,e}(t)<0$ 的比例
- step 5/10 的 proxy-route NMI
- LM loss guard

### 对立解释

1. 代理标签本身不稳定；失败不是路由保持失败，而是被保持对象不稳定。
2. 第 0 步 router bridge 本来就弱；初始化没有真正对齐。
3. 特征中心漂移太大；需要追踪隐藏状态移动。
4. 路由行向量漂向公共/稠密方向；失败来自 router-side early lock-in。
5. 即使 center/router drift 很小，专家反馈或优化器几何也会破坏指派。
6. margin 只是和成功相关，不是因果机制。

### 决策规则

这个锚点只有在改变下一步决策时才有用：

- 如果 margin consumption 能预测 NMI drop，优先测试 anti-drift / anti-lock-in 干预。
- 如果 margin consumption 不能预测 NMI drop，把 margin 暂时作为二级诊断，转向 expert feedback、optimizer geometry、hidden-state feature instability 或 objective incompatibility。

---

## 1. 问题定义

### 父问题

top-1 MoE gating 能否形成稳定、可解释、且有用的 feature-level expert partition？

### 当前子问题

给定一个由 feature/proxy-center router initialization 产生的第 0 步 feature-to-expert partition：

> 这个 partition 能否穿过早期训练？是什么决定它能否穿过？

### 本锚点的具体问题

> early-training preservation 是否由 margin budget 决定：初始 routing margin 必须大于训练累积的 feature-center drift 和 router-boundary drift？

### 为什么这不只是调试问题

route NMI 下降只能说明 specialization 失败，但不能说明为什么失败。这个锚点把 preservation failure 转化为一个可分解的几何条件：

$$
\text{preservation failure}
=
\text{initial margin exhausted by drift}.
$$

如果这个模型有效，它会把局部诊断和机制解释连接起来。

---

## 2. 物理先验

### 先验 1：top-1 routing 是决策区域指派

对点积路由器来说，当：

$$
w_e(t)^\top h > w_j(t)^\top h,\quad \forall j\neq e
$$

专家 $e$ 赢得隐藏状态 $h$。因此，路由器把隐藏状态空间切成多个决策区域。塌缩不要求隐藏状态本身塌缩；只要路由决策区域把大量隐藏状态分给同一个专家，就会出现路由塌缩。

### 先验 2：特征信息和公共信息共存

对特征 $f$，写：

$$
\mu_f(t)=c(t)+r_f(t),
$$

其中：

- $c(t)$ 是共享公共/稠密成分；
- $r_f(t)$ 是 feature-specific residual component。

即使 $r_f(t)$ 仍包含特征信息，只要决策边界对齐到了 $c(t)$ 而不是 residual 方向，路由仍可能失败。

### 先验 3：训练同时移动隐藏状态和路由行向量

训练中：

$$
\mu_f(t)=\mu_f(0)+\Delta\mu_f(t),
$$

$$
w_e(t)=w_e(0)+\Delta w_e(t).
$$

所以 preservation 是一个耦合几何问题，不只由 feature-center movement 决定，也不只由 router-row movement 决定，而由它们对 margin 的相对影响决定。

### 先验 4：初始对齐不等于安全保持

第 0 步指派可以是正确的，但很脆弱。如果 assigned expert 和 competing expert 的 score gap 很小，那么隐藏中心或路由行向量的小移动就可能翻转指派。

---

## 3. 可证伪假设

### H1：Margin-buffer 假设

成功保持要求初始 margin 大于 drift budget。

预测：成功 seed/condition 有更低的 margin consumption ratio：

$$
R(t)=\frac{\text{drift budget}(t)}{\Gamma(0)}.
$$

当 $R(t)<1$，proxy-route NMI 应更高；当 $R(t)>1$，sign flip 和 NMI drop 应更可能出现。

证伪：跨 seed/condition 观察到 $R(t)\ll 1$ 但 NMI 仍塌缩，或 $R(t)\gg 1$ 但 NMI 仍保持高。

### H2：Router-side early-lock-in 假设

preservation 失败是因为 router decision boundary 漂向公共/稠密方向，而不是跟随 feature residual direction。

预测：feature center 相对稳定，但 router rows 或 pairwise gaps 与 common direction $c(t)$ 的对齐增强。sign flip 主要由下式主导：

$$
\Delta u_{f,e}(t)^\top \mu_f(0),
$$

其中：

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

证伪：router rows 稳定，common alignment 没有增强，但 NMI 仍塌缩。

### H3：Feature-center drift 假设

preservation 失败是因为 feature centers 自己离开了初始 router assignment。

预测：sign flip 主要由下式主导：

$$
u_{f,e}(0)^\top\Delta\mu_f(t).
$$

成功条件要么有更小的 $\|\Delta\mu_f(t)\|$，要么有追踪移动中心的机制。

证伪：$\Delta\mu_f(t)$ 很小，并且不沿着 margin reduction 方向，但 NMI 仍下降。

### H4：Margin intervention 假设

人为缩小或移除初始 margin 应降低 preservation，即使第 0 步指派最初仍不变。

预测：margin shrink/removal 会降低 step 5/10 proxy-route NMI，并提高 sign flip rate。

证伪：在控制 loss、load 和 initial assignment 后，margin shrink/removal 不影响 NMI 或 sign flip rate。

---

## 4. 数学模型

### 4.1 初始指派

令 $F$ 为 feature/proxy labels 集合，$E$ 为专家集合。对每个特征 $f$，第 0 步 assigned expert 是：

$$
a(f)=\arg\max_{e\in E} w_e(0)^\top \mu_f(0).
$$

这个指派就是要被保留的目标 partition。

### 4.2 成对路由 gap

对每个竞争专家 $e\neq a(f)$，定义：

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

这是 assigned expert 和 competitor 之间的成对决策边界向量。

### 4.3 成对 margin

center-level pairwise margin 是：

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top \mu_f(t).
$$

如果：

$$
\gamma_{f,e}(t)>0,\quad \forall e\neq a(f),
$$

则 feature center $\mu_f(t)$ 仍被分到原专家 $a(f)$。

最小 center margin 是：

$$
\Gamma_{\mathrm{center}}(t)=\min_f\min_{e\neq a(f)} \gamma_{f,e}(t).
$$

### 4.4 Cluster-aware margin

对单个隐藏状态：

$$
h_i(t)=\mu_f(t)+\epsilon_i(t),\quad y_i=f.
$$

则：

$$
u_{f,e}(t)^\top h_i(t)
=
\gamma_{f,e}(t)+u_{f,e}(t)^\top\epsilon_i(t).
$$

如果 $\|\epsilon_i(t)\|\leq \rho_f(t)$，则：

$$
u_{f,e}(t)^\top h_i(t)
\geq
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t).
$$

定义 cluster-aware margin：

$$
\tilde{\gamma}_{f,e}(t)
=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t).
$$

更强的充分条件是：

$$
\tilde{\gamma}_{f,e}(t)>0,\quad \forall e\neq a(f).
$$

实际使用时，$\rho_f(t)$ 应使用 robust quantile radius，而不是最大半径。

### 4.5 Margin dynamics

令：

$$
\Delta u_{f,e}(t)=u_{f,e}(t)-u_{f,e}(0),
$$

$$
\Delta\mu_f(t)=\mu_f(t)-\mu_f(0).
$$

则：

$$
\gamma_{f,e}(t)
=
\bigl(u_{f,e}(0)+\Delta u_{f,e}(t)\bigr)^\top
\bigl(\mu_f(0)+\Delta\mu_f(t)\bigr).
$$

展开得到核心分解：

$$
\gamma_{f,e}(t)
=
\gamma_{f,e}(0)
+
\underbrace{\Delta u_{f,e}(t)^\top \mu_f(0)}_{\text{router-boundary drift}}
+
\underbrace{u_{f,e}(0)^\top \Delta\mu_f(t)}_{\text{feature-center drift}}
+
\underbrace{\Delta u_{f,e}(t)^\top \Delta\mu_f(t)}_{\text{interaction drift}}.
$$

这就是本锚点的核心模型。

### 4.6 充分保持条件

由 Cauchy-Schwarz 不等式：

$$
|\Delta u^\top \mu_0|\leq \|\Delta u\|\|\mu_0\|,
$$

$$
|u_0^\top \Delta\mu|\leq \|u_0\|\|\Delta\mu\|,
$$

$$
|\Delta u^\top \Delta\mu|\leq \|\Delta u\|\|\Delta\mu\|.
$$

因此，center assignment preservation 的一个充分条件是：

$$
\gamma_{f,e}(0)
>
\|\Delta u_{f,e}(t)\|\|\mu_f(0)\|
+
\|u_{f,e}(0)\|\|\Delta\mu_f(t)\|
+
\|\Delta u_{f,e}(t)\|\|\Delta\mu_f(t)\|.
$$

对 token-level preservation，还要加入 cluster radius：

$$
\gamma_{f,e}(0)
>
B_{f,e}(t)
+
\|u_{f,e}(t)\|\rho_f(t),
$$

其中：

$$
B_{f,e}(t)
=
\|\Delta u_{f,e}(t)\|\|\mu_f(0)\|
+
\|u_{f,e}(0)\|\|\Delta\mu_f(t)\|
+
\|\Delta u_{f,e}(t)\|\|\Delta\mu_f(t)\|.
$$

### 4.7 Margin consumption ratio

定义：

$$
R_{f,e}(t)
=
\frac{B_{f,e}(t)}{\gamma_{f,e}(0)+\varepsilon}.
$$

聚合时可以用：

$$
R_{\max}(t)=\max_f\max_{e\neq a(f)}R_{f,e}(t),
$$

也可以用 high quantile 提高稳定性。

预测：

- $R(t)<1$：assignment 更稳定；
- $R(t)\approx 1$：边界情况；
- $R(t)>1$：sign flip 和 NMI drop 更可能发生。

### 4.8 Common/residual decomposition

使用：

$$
\mu_f(t)=c(t)+r_f(t),
$$

pairwise margin 可写成：

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top c(t)+u_{f,e}(t)^\top r_f(t).
$$

这分成：

**common term**

$$
C_{f,e}(t)=u_{f,e}(t)^\top c(t)
$$

**residual feature term**

$$
R^{\mathrm{feat}}_{f,e}(t)=u_{f,e}(t)^\top r_f(t)
$$

preservation 要求正确专家的 residual advantage 不被 common-driven router drift 淹没。

---

## 5. 计算实现

### 输入对象

每个 seed、condition、checkpoint $t\in\{0,5,10\}$ 需要：

1. hidden states $h_i(t)$；
2. fixed proxy/feature labels $y_i$；
3. router rows $w_e(t)$；
4. route assignments $\hat e_i(t)=\arg\max_e w_e(t)^\top h_i(t)$；
5. training loss / LM loss；
6. expert load。

### 派生对象

1. feature centers：

$$
\mu_f(t)=\mathrm{mean}_{i:y_i=f}h_i(t)
$$

2. common center：

$$
c(t)=\mathrm{mean}_f\mu_f(t)
$$

也可以用预先指定的 common direction。

3. residual centers：

$$
r_f(t)=\mu_f(t)-c(t)
$$

4. initial assignment：

$$
a(f)=\arg\max_e w_e(0)^\top\mu_f(0)
$$

5. pairwise margins：$\gamma_{f,e}(t)$

6. drift decomposition terms：
   - router-boundary drift
   - feature-center drift
   - interaction drift

7. margin consumption ratio：$R_{f,e}(t)$

8. sign flip rate：

$$
\mathrm{SFR}(t)=
\frac{
\#\{(f,e):\gamma_{f,e}(t)<0\}
}{
\#\{(f,e):e\neq a(f)\}
}
$$

9. proxy-route NMI：

$$
\mathrm{NMI}(y_i,\hat e_i(t))
$$

### 主指标

$$
\mathrm{proxy\_route\_NMI}@\{5,10\}
$$

### 机制指标

- $\Gamma_{\mathrm{center}}(0)$
- $\Gamma_{\mathrm{center}}(t)$
- $R_{\max}(t)$ 或 high-quantile $R(t)$
- sign flip rate
- margin term attribution：
  - router-boundary drift contribution
  - feature-center drift contribution
  - interaction contribution
- common alignment gain：

$$
u_{f,e}(t)^\top c(t)-u_{f,e}(0)^\top c(0)
$$

### 保护指标

- LM loss
- maximum expert load
- active experts
- step-0 assignment validity
- cluster radius / within-feature dispersion

---

## 6. 最小可证伪测试

### Test 1：Margin-preservation correlation

问题：更大的初始 margin 是否预测更好的 preservation？

设置：比较不同 initial margins 的 seeds / conditions。

主读数：initial minimum margin / margin consumption ratio 和 step 5/10 proxy-route NMI 的相关性。

通过：更低的 $R(t)$ 预测更高 NMI 和更低 sign flip rate。

失败：margin consumption 和 preservation 没有关系。

证据不足：NMI 变化主要由 loss/load artifacts 主导。

### Test 2：Margin shrink / removal

问题：margin 是因果相关，而不只是相关吗？

设置：构造降低 initial margin 的干预，同时尽量保留 initial assignment 和 architecture。

候选干预：

1. global router-row scaling diagnostic；
2. pairwise margin shrink perturbation；
3. reduced center-init strength；
4. temperature / softmax confidence control。

通过：margin shrink 导致 step-5/10 NMI 更低、sign flip rate 更高。

失败：margin shrink 不影响 preservation。

注意：global scaling 会改变 softmax confidence 和 gradients；除非有控制，否则只能标为 diagnostic。

### Test 3：Drift attribution

问题：失败主要来自 feature-center drift 还是 router-boundary drift？

设置：计算：

$$
\Delta u^\top\mu_0,\quad u_0^\top\Delta\mu,\quad \Delta u^\top\Delta\mu.
$$

通过：主导负项能识别 failure mode。

失败：分解项不能解释 margin 或 NMI change。

解释：

- router-boundary term dominates：router-side early lock-in；
- feature-center term dominates：hidden-state feature object drift；
- interaction dominates：coupled instability。

### Test 4：Common-direction audit

问题：router 是否漂向 common/dense direction，从而解释 preservation failure？

设置：追踪 common term：

$$
u_{f,e}(t)^\top c(t)
$$

以及 residual term：

$$
u_{f,e}(t)^\top r_f(t).
$$

通过：失败 seed 显示 common alignment 增强、residual separation 降低。

失败：common alignment 不变，但 margin 被消耗。

### Test 5：Tracking oracle / slow router control

问题：追踪移动中的 feature centers 是否能救回 preservation？

设置：比较 ordinary training 和：

1. frozen router；
2. slow-updated router；
3. EMA center-tracking router；
4. oracle center-tracking diagnostic。

通过：tracking 提升 NMI，且 LM loss 没有不可接受的退化。

失败：tracking 不起作用，说明 feature partition 可能与目标不兼容，或者失败在 expert side。

---

## 7. 当前应挂接的证据

本锚点应挂接：

1. baseline feature-center initialization result；
2. step-0 NMI and load；
3. step-5/10 NMI and load；
4. margin shrink/removal table；
5. center drift table；
6. router drift table；
7. margin decomposition table；
8. NMI vs margin consumption plot；
9. LM loss guard table。

当前证据状态：

```text
Draft anchor only. Evidence tables must be attached before claim update.
```

---

## 8. Claim boundary and next decision

### 若测试支持，可以说

```text
In the tested synthetic/proxy setting, early-training preservation is partly governed by a margin budget: initial feature-to-expert margins must exceed training-induced feature-center and router-boundary drift.
```

中文含义：在被测试的 synthetic/proxy 设置中，早期训练保持至少部分由 margin budget 支配：初始 feature-to-expert margin 必须大于训练造成的 feature-center 和 router-boundary drift。

### 不能说

即使测试支持，也不能证明：

```text
1. real natural-language semantic experts exist;
2. MoE specialization is functionally useful;
3. margin control alone solves gating;
4. common-component control is a deployable architecture;
5. load balance implies specialization;
6. real-DCLM preservation has been solved.
```

### 下一步决策

如果 margin-budget evidence 通过：

```text
Test whether common-controlled router input, anti-lock-in training, or center-tracking expands the margin-safe region while preserving LM loss.
```

如果 margin-budget evidence 失败：

```text
Park margin as a secondary diagnostic and decompose preservation failure into expert feedback, optimizer geometry, hidden-state feature instability, or objective incompatibility.
```
