# 软路由与 Top-K 路由的高增益坍塌机制解释

## TL;DR

问题：路由器（router）的门控向量（gating vector）会不会被已有高增益方向吸引，导致路由坍塌、专家欠训练，并让门控学不到真正区分性方向。

结论：会，但不是无条件会。严格条件是：路由误差信号在某个高增益输出方向上有非零投影，并且 Top-K 选择让未选专家长期缺少任务梯度。此时高增益方向的一阶下降收益更大，路由会更容易强化已有方向。

负载均衡损失主要缓解“负载不均”；z-loss 主要缓解“router logit 过大和训练不稳定”。二者都不能单独保证门控向量学到专家条件化的区分性方向。

---

## 0. researcher judgment record

**Phenomenon:** MoE 训练中，少数专家或少数路由方向吸收大量 token，其他专家欠训练；门控向量可能学习公共高频方向，而不是专家真正需要的区分性方向。

**Mechanism guess:** 路由矩阵中已有高增益方向会放大对应的路由误差梯度；Top-K 选择造成“被选专家继续收到梯度，未选专家缺少梯度”的正反馈。

**Key variables:** 路由 logit `a`，路由概率 `q`，专家输出 `E_e(h)`，路由误差信号 `γ`，路由矩阵奇异值 `σ_i`，Top-K 选择集合 `S_K`，专家负载 `f_e`。

**Causal relation:**

$$
high\ σ_i + ⟨u_i,γ⟩≠0
⇒ large\ router\ gradient\ gain
⇒ larger\ TopK\ margin
⇒ selection\ lockin.
$$

**Decision:** 若高增益投影指标能预测后续负载集中和区分性失败，则继续研究“高增益路由病态”；否则转向专家能力差异或容量机制。

---

## 1. 基本对象

给定 token 隐藏表示 `h ∈ R^d`，路由矩阵为 `R ∈ R^{N×d}`，其中 `N` 是专家数。router logit 是：

$$
a = Rh,
\quad
 a_e = r_e^T h.
$$

其中 `r_e` 是第 `e` 个专家的门控向量。

软路由为：

$$
q_e = softmax(a)_e,
\quad
 y = Σ_e q_e E_e(h).
$$

Top-K 路由为：

$$
S_K(h)=TopK(a),
\quad
 y = Σ_{e∈S_K} q_e^K E_e(h).
$$

路由矩阵的奇异值分解写作：

$$
R = Σ_i σ_i u_i v_i^T.
$$

若 `σ_i` 大，则输入侧方向 `v_i` 会被强烈映射到专家-logit 侧方向 `u_i`：

$$
R v_i = σ_i u_i.
$$

---

## 2. 软路由的一阶梯度

设主损失为 `L(y)`，输出梯度为：

$$
g_y = ∇_y L.
$$

定义第 `e` 个专家的局部一阶代价：

$$
s_e = ⟨g_y, E_e(h)⟩.
$$

`s_e` 的含义是：如果增加专家 `e` 的权重，损失一阶上会变化多少。`s_e` 越小，说明专家 `e` 对当前 token 越有利。

令：

$$
s_{avg} = Σ_j q_j s_j.
$$

则 router logit 的梯度是：

$$
γ_e := ∂L/∂a_e = q_e(s_e-s_{avg}).
$$

解释：

- 若 `s_e < s_avg`，则 `γ_e < 0`，梯度下降会增大 `a_e`，提高专家 `e` 的路由概率。
- 若 `s_e > s_avg`，则 `γ_e > 0`，梯度下降会减小 `a_e`，降低专家 `e` 的路由概率。

所以软路由学到的是：提高比平均专家更有用的专家，压低更差的专家。

---

## 3. 门控向量如何学习

因为：

$$
a_e = r_e^T h,
$$

所以：

$$
∂L/∂r_e = γ_e h.
$$

梯度下降给出：

$$
Δr_e = -η γ_e h.
$$

因此：

- 若专家 `e` 对当前 token 更有用，即 `γ_e < 0`，则 `r_e` 会向该 token 的表示 `h` 靠近。
- 若专家 `e` 对当前 token 更差，即 `γ_e > 0`，则 `r_e` 会远离该 token 的表示方向。

核心机制：

$$
专家相对有用 ⇒ 该专家的 gating\ vector 吸收该 token 表示方向。
$$

---

## 4. 高增益方向如何放大路由学习

路由误差信号为：

$$
γ = ∇_a L.
$$

对隐藏表示的梯度是：

$$
∇_h L = R^Tγ = Σ_i σ_i⟨u_i,γ⟩v_i.
$$

如果：

$$
⟨u_i,γ⟩≠0,
$$

则误差信号会沿输入方向 `v_i` 被 `σ_i` 放大。

若对隐藏表示做一小步梯度下降：

$$
δh = -ηR^Tγ,
$$

诱导的 router logit 变化是：

$$
δa = Rδh = -ηRR^Tγ = -ηΣ_i σ_i^2⟨u_i,γ⟩u_i.
$$

一阶损失变化为：

$$
ΔL ≈ ⟨γ,δa⟩ = -ηΣ_i σ_i^2⟨u_i,γ⟩^2.
$$

关键结论：

$$
第 i 个路由模式的一阶下降收益 ∝ σ_i^2⟨u_i,γ⟩^2.
$$

因此，高增益 `σ_i` 大不是充分条件。真正条件是 `σ_i^2⟨u_i,γ⟩^2` 相对其他方向更大。

---

## 5. 为什么 gating vector 会偏向公共高增益方向

门控向量更新为：

$$
Δr_e = -ηγ_eh.
$$

若 token 表示 `h` 主要落在公共高增益子空间 `V_H` 中，则：

$$
||P_{V_H}Δr_e|| / ||Δr_e|| = ||P_{V_H}h|| / ||h||.
$$

这说明：门控向量更新方向由 token 表示本身决定。若 `h` 的主能量来自公共特征，例如高频语法、常见 token 模式、位置模式或通用上下文模式，那么 gating vector 会优先学习这些方向。

病态链条：

$$
公共高频方向快速降低损失
⇒ 门控对公共方向变敏感
⇒ TopK 更常选择已有专家
⇒ 其他专家缺少任务梯度
⇒ 更难学到区分性方向。
$$

---

## 6. Top-K 路由的推广

令：

$$
S = S_K(a)
$$

表示当前被选中的专家集合。在一个小邻域内，如果 Top-K 集合不变，可以把 `S` 当作固定集合分析。

若采用 Top-K 内重新归一化：

$$
q_e^K = exp(a_e) / Σ_{j∈S} exp(a_j),\quad e∈S.
$$

则：

$$
y = Σ_{e∈S} q_e^K E_e(h).
$$

此时路由梯度是：

$$
γ_e^K = q_e^K(s_e-s_{S,avg}),\quad e∈S;
$$

$$
γ_e^K = 0,\quad e∉S.
$$

所以未选专家在任务损失下没有一阶路由梯度。

若实现是“全 softmax 计算概率，但只 dispatch Top-K”，未选专家可能通过 softmax 分母获得梯度，但该梯度主要来自概率竞争，不是“该专家是否适合该 token”的直接专家效用梯度。因此其区分性学习信号仍弱于被选专家。

Top-K 的锁定变量是边界间隔：

$$
Δ_K = a_{(K)} - a_{(K+1)}.
$$

若 `Δ_K` 变大，Top-K 集合更稳定，未选专家更难进入集合。

---

## 7. 负载均衡损失能缓解什么

Switch 风格负载均衡损失可写作：

$$
L_{bal} = αNΣ_e f_eP_e.
$$

其中 `f_e` 是 batch 中被分配到专家 `e` 的 token 比例，`P_e=(1/T)Σ_t q_{e,t}` 是专家 `e` 的平均路由概率。

它能做的事：压低高负载专家，抬高低负载专家。

它不能保证的事：判断专家是否真的适合当前 token。

因此它能缓解负载坍塌（load collapse），但不一定缓解语义坍塌（semantic collapse）。可能出现：负载均匀了，但 token 只是被均匀打散，并不是专家分工真正清楚。

---

## 8. z-loss 能缓解什么

router z-loss 可写为：

$$
L_z = λ_z (1/T) Σ_t [log Σ_e exp(a_{e,t})]^2.
$$

令：

$$
z_t = log Σ_e exp(a_{e,t}).
$$

则：

$$
∂L_z/∂a_{e,t} = (2λ_z/T) z_t q_{e,t}.
$$

它主要惩罚 router logit 的整体尺度过大，降低数值不稳定和过强 softmax 饱和。

z-loss 能缓解：logit scale runaway、数值不稳定、过度尖锐的路由概率。

z-loss 不能直接保证：专家 `e` 的 gating vector 学到专家 `e` 的真实专长。

所以 z-loss 对高增益坍塌的作用是间接的：它可能减慢 logit margin 变大，但不消除高增益方向带来的相对一阶优势。

---

## 9. loss-free balancing 能缓解什么

无辅助损失负载均衡（loss-free balancing）的思想是：不把负载均衡写成反传损失，而是在 Top-K 选择前给每个专家加动态偏置。

选择时使用：

$$
ã_{e,t} = a_{e,t}+b_e.
$$

若专家 `e` 近期负载过高，则降低 `b_e`；若负载过低，则提高 `b_e`。

典型更新为：

$$
b_e ← b_e + u sign(c_{avg}-c_e).
$$

它的优点：控制负载，同时不向主损失注入负载均衡梯度。

它的边界：它只控制“谁被选中”，不直接定义“为什么该专家适合这个 token”。所以它能缓解负载坍塌，但仍需额外指标判断是否缓解区分性路由失败。

---

## 10. 机制判断

可以严格说：

$$
第 i 个路由模式的一阶收益 ∝ σ_i^2⟨u_i,γ⟩^2.
$$

不能直接说：

$$
σ_i 大 ⇒ 必然吸引后续特征。
$$

更准确的条件是：

$$
σ_i^2⟨u_i,γ⟩^2 ≫ σ_j^2⟨u_j,γ⟩^2.
$$

若同时出现 Top-K margin 增大，未选专家任务梯度下降，则该高增益模式会形成路由锁定。

---

## 11. 最小验证实验

### Test 1: 高增益投影是否预测路由坍塌

定义高增益梯度占比：

$$
C_r = [Σ_{i≤r} σ_i^2⟨u_i,γ⟩^2] / [Σ_i σ_i^2⟨u_i,γ⟩^2].
$$

若早期 `C_r` 升高能预测后续负载不均、Top-K margin 增大或区分性下降，则支持高增益机制。

### Test 2: 负载均衡是否只修复表面负载

比较：无辅助损失、负载均衡损失、z-loss、负载均衡 + z-loss、loss-free balancing。

记录：Load MaxVio、Top-K margin、`C_r`、未选专家任务梯度范数、router-utility alignment。

若负载均衡改善 MaxVio，但 `C_r` 和 router-utility alignment 没改善，则说明它修复的是负载，不是区分性路由。

### Test 3: 高增益方向干预

对 router 做谱约束、行归一化，或投影去除公共高增益子空间。

若干预后 Top-K 锁定下降、未选专家获得更多任务梯度，并且主损失不明显恶化，则支持“高增益方向导致病态学习”。

---

## 12. Claim boundary

**Can claim:**

- 软路由下，router logit 梯度为 `q_e(s_e-s_avg)`。
- 路由高增益方向的一阶下降收益含有 `σ_i^2` 放大。
- Top-K 会削弱或切断未选专家的任务梯度，从而放大早期选择偏差。
- 负载均衡和 z-loss 不能单独证明门控学到了区分性方向。

**Cannot claim yet:**

- 不能声称所有 MoE 路由坍塌都由高增益方向导致。
- 不能声称负载均衡或 z-loss 无效；它们可能有效缓解负载和稳定性问题。
- 不能声称高增益方向必然导致坍塌；必须同时观察 `⟨u_i,γ⟩` 和 Top-K 锁定。

**Next decision:**

先做诊断，不先设计新方法。最小下一步是验证：`C_r` 是否早期预测 Top-K margin、负载不均和 router-utility alignment 下降。若成立，再研究直接控制高增益路由子空间的方法；若不成立，转向专家能力差异、容量限制或辅助损失干扰机制。

---

## References

1. Shazeer et al., *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*, 2017.
2. Lepikhin et al., *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding*, 2020.
3. Fedus, Zoph, Shazeer, *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*, 2021.
4. Zoph et al., *ST-MoE: Designing Stable and Transferable Sparse Expert Models*, 2022.
5. Wang et al., *Auxiliary-Loss-Free Load Balancing Strategy for Mixture-of-Experts*, 2024.
