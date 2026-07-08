# Whole Story Line: MTP, Long-Horizon Semantic Information, and Efficiency

Status: draft v1 for advisor-facing theory discussion
Language: Chinese meeting draft
Scope: controlled theory + boundary + next experiments

---

## 0. 一句话结论

我们现在最稳的故事不是“MTP 一定比 NTP 强”，而是：

> 在存在长程语义依赖的数据里，MTP 的确定优势是把“未来才显现的语义相关性”提前变成当前前缀状态 `h_T` 的直接监督；在这个基础上，如果这个未来监督的梯度确实降低语义恢复损失、且不破坏本地 next-token 学习，那么 MTP 比 NTP 具有更短的 credit-assignment path，因此应当表现为更快、更稳、更可用的长程语义表征学习。

当前我们已经有：

1. 表示要求定理：MTP 覆盖第一个语义显现 token 时，低 loss 数学上推出 `h_T` 含有早期语义变量 `Z`。
2. 直接梯度路径：future-token error 直接作用在同一个 `h_T` 上。
3. 效率桥梁：如果 future-token gradient 对语义恢复 loss 有正投影，则 MTP 一步更新比 NTP 多一个降低语义恢复 loss 的一阶项。

还没有无条件证明：MTP 在所有训练、所有数据、所有架构上都比 NTP 更快或最终上限更高。

---

## 1. 导师能听懂的开头版本

我们要回答的问题是：

> NTP 不是不能学长程信息；问题是它什么时候学得绕、学得慢、学得不稳定。MTP 的作用是把远处 token 的错误直接打到当前 hidden state 上，让模型更早知道“现在这个状态应该保留未来会用到的语义信息”。

用故事例子说：

> 第一章给了一个设定，最后一章要用这个设定；中间章节不是垃圾，但中间局部上下文不足以决定结局。NTP 只在每一步问“下一句是什么”，所以它可能一步步滚过去；MTP 在前面就问“后面几步会是什么”，所以如果后面某一步第一次需要第一章设定，MTP 就直接要求当前状态保留这个设定。

这就是我们现在的核心句子：

> MTP converts delayed semantic relevance into direct prefix-state supervision.

中文：

> MTP 把延迟出现的语义相关性，提前变成对当前状态的直接监督。

---

## 2. 为什么原问题需要拆开

原始目标是：

> 证明 MTP 在学习长程语义信息上比 NTP 好。

这个问题必须拆成三层，否则会过度 claim。

| 层次 | 问题 | 当前状态 |
|---|---|---|
| 表示要求 | MTP 是否要求 `h_T` 包含远处语义变量？ | 可以证明 |
| 学习效率 | MTP 是否更快、更稳地把语义变量学进 `h_T`？ | 需要理论桥梁 + 实验 |
| 表征可用性 | MTP 学到的语义方向是否更 readout-effective / gateable？ | 可提出理论判据 + 实验 |

所以我们的故事不能只说“有未来 token 相关，所以 MTP 有用”。真正要说的是：

1. 在数据有长程依赖的前提下，MTP 给当前状态更直接的语义监督。
2. 这种直接监督提供了更短的 credit-assignment path。
3. 如果梯度方向确实有利于语义恢复，并且不损害本地学习，那么它会带来学习效率优势。
4. 如果实验发现 NTP 最终也能学到，那么结论不是失败，而是说明上限可能相同；MTP 的优势要看速度、稳定性和表征可用性。

---

## 3. 什么是长程语义信息

### 3.1 定义

长程语义信息是：

> 早期出现、局部上下文不能恢复、但会决定更远未来输出的变量。

记为：

\[
Z.
\]

在受控实验里：

\[
Z=B,
\]

即 branch key。

在自然语言里，`Z` 可以是：

| 场景 | `Z` 的例子 |
|---|---|
| 故事 | 早期人物身份、承诺、因果设定 |
| 代码 | 变量定义、函数签名、类型约束 |
| 数学证明 | 早期假设、目标命题、符号定义 |
| 指令遵循 | 开头格式要求、角色要求、任务约束 |
| 长文问答 | 早期实体关系或事实 |

`Z` 不是某个 token 本身，而是 token 背后的 early semantic state。

### 3.2 第一个语义显现位置

令

\[
Y_j=X_{T+j}
\]

表示当前 prefix 后第 `j` 个 future token。

定义条件信息增量：

\[
\Delta_j=I(Z;Y_j\mid Y_{<j}).
\]

定义第一个语义显现位置：

\[
\tau=\min\{j:\Delta_j>0\}.
\]

直观意思：

- `j < tau`：这些 future token 不需要 `Z`。
- `j = tau`：第一个真正需要 `Z` 的 future token 出现。

所以，MTP 的关键不是“预测更多 token”，而是：

\[
K\ge \tau.
\]

如果 horizon 没覆盖到第一个语义显现位置，MTP 不应该被期待有确定的长程语义优势。

---

## 4. NTP 和 MTP 的目标函数差别

### 4.1 NTP

下一词元预测（NTP）在当前状态只训练：

\[
L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1).
\]

如果 `Y_1` 不依赖 `Z`，这个 loss 没有直接理由要求 `h_T` 保存 `Z`。

### 4.2 MTP / next-K

多词元预测（MTP）训练同一个状态预测多个未来 token：

\[
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
\]

如果 `K >= tau`，这个目标包含：

\[
\lambda_\tau\operatorname{CE}(q_\tau(\cdot\mid h_T),Y_\tau).
\]

如果

\[
Y_\tau=S_Z,
\]

那么这个项就是对 `h_T -> Z` 的直接监督。

---

## 5. K=2 已证明的最小机制

### 5.1 数据构造

令

\[
B\sim \operatorname{Unif}\{1,\ldots,m\}.
\]

序列为：

\[
X=(\operatorname{BR}_B,F_1,\ldots,F_L,U,A,S_B).
\]

当前状态：

\[
h_T^{(B)}=f_\theta(\operatorname{BR}_B,F_1,\ldots,F_L,U).
\]

未来两个 token：

\[
Y_1=A,
\]

\[
Y_2=S_B.
\]

其中 `A` 对所有 branch 相同，`S_B` 由早期 branch 决定，且 `B -> S_B` 一一对应。

于是：

\[
I(B;Y_1)=0,
\]

\[
I(B;Y_2\mid Y_1)=H(B)=\log m.
\]

这就是 `tau=2` 的最小 long-horizon semantic task。

### 5.2 Branch-blind lower bound

如果 `h_T` 不区分 branch：

\[
h_T^{(1)}=\cdots=h_T^{(m)}=c,
\]

则任何只看 `h_T` 的 predictor 都必须输出同一个分布。

因为 `S_B` 在 `m` 个 distinct token 上均匀分布，所以：

\[
\inf_q\mathbb E[-\log q(S_B\mid h_T)]=\log m.
\]

top-1 accuracy 至多：

\[
1/m.
\]

### 5.3 NTP 可以不要求 branch 信息

NTP 在 `h_T` 上只预测：

\[
Y_1=A.
\]

因为 `A` 共享，所以 branch-blind state `c` 可以令：

\[
q_1(A\mid c)=1.
\]

因此 `h_T` 不含 `B` 也能把当前 NTP loss 降到 0。

### 5.4 MTP 直接排除 branch-blind state

next-two loss 是：

\[
L_2(h_T)=\operatorname{CE}(q_1,A)+\lambda\operatorname{CE}(q_2,S_B).
\]

如果 `h_T` branch-blind，则第二项至少：

\[
\lambda\log m.
\]

如果 second-token CE 很小：

\[
\mathbb E[-\log q_2(S_B\mid h_T)]\le \varepsilon,
\]

则：

\[
I(h_T;B)\ge \log m-\varepsilon.
\]

这就是 K=2 的确定性保证：

> low MTP second-token loss forces `h_T` to contain early long-horizon information.

---

## 6. NextK 推广

### 6.1 一般构造

令 `Z` 是早期语义变量，未来 token 为：

\[
Y_1,\ldots,Y_K.
\]

定义：

\[
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
\]

干净确定性情形：

\[
Y_\tau=S_Z,
\]

且 `Z -> S_Z` 一一对应。

### 6.2 Theorem 1: non-covering horizons need not force `Z`

如果

\[
I(Z;Y_{1:K})=0,
\]

则 Bayes-optimal predictor of `Y_{1:K}` 不需要 `Z`。因此存在一个 `Z`-blind hidden state 也能完成这些 active targets。

直观：如果被监督的 token 都不需要早期语义变量，那么目标函数没有理由强迫当前状态保存它。

### 6.3 Theorem 2: covering the first informative horizon forces `Z`

如果

\[
K\ge\tau,
\]

且

\[
Y_\tau=S_Z,
\]

`Z -> S_Z` 一一对应，且

\[
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le \varepsilon,
\]

则：

\[
I(h_T;Z)\ge H(Z)-\varepsilon.
\]

#### Proof

因为 `S_Z` 是 `Z` 的一一对应函数：

\[
H(S_Z)=H(Z).
\]

cross-entropy upper bounds conditional entropy：

\[
H(S_Z\mid h_T)\le \mathbb E[-\log q_\tau(S_Z\mid h_T)]\le \varepsilon.
\]

因此：

\[
I(h_T;S_Z)=H(S_Z)-H(S_Z\mid h_T)\ge H(Z)-\varepsilon.
\]

又因为 `S_Z` 是 `Z` 的函数，`h_T` 对 `S_Z` 的信息来自 `Z`，所以：

\[
I(h_T;Z)\ge I(h_T;S_Z)\ge H(Z)-\varepsilon.
\]

### 6.4 Theorem 3: gradient path distinction

若各 horizon head 为线性 readout：

\[
z_j=W_jh_T+b_j,
\]

则：

\[
\nabla_{h_T}L_K=\sum_{j=1}^{K}\lambda_j W_j^\top(q_j-e_{Y_j}).
\]

当 `K >= tau` 时，里面包含：

\[
\lambda_\tau W_\tau^\top(q_\tau-e_{S_Z}).
\]

这个项直接依赖 `Z`。

NTP 只包含：

\[
W_1^\top(q_1-e_{Y_1}).
\]

如果 `Y_1` 不含 `Z`，它没有直接 branch-specific target。

---

## 7. 从“直接地学”到“高效地学”的最小理论桥梁

### 7.1 为什么需要这个桥梁

表示定理证明的是：

> 如果 MTP 把相关 future token 预测好，那么 `h_T` 必须包含 `Z`。

但导师真正会追问：

> 那它是不是比 NTP 学得更快、更稳？

这不是上面那个定理自动推出的。我们需要一个最小优化桥梁。

### 7.2 定义语义恢复损失

令

\[
R_\phi(\theta)=\operatorname{CE}(s_\phi(h_T(\theta)),Z)
\]

表示从当前状态恢复 `Z` 的 probe/evaluation loss。

`R_phi` 越低，表示 `Z` 越容易从 `h_T` 中读出来。

设 NTP local gradient：

\[
g_1=\nabla_\theta L_1.
\]

设 informative future gradient：

\[
g_\tau=\nabla_\theta L_\tau.
\]

MTP update 使用：

\[
g_{MTP}=g_1+\lambda_\tau g_\tau.
\]

### 7.3 Theorem 4: first-order semantic efficiency gain

假设在当前训练点：

\[
\langle \nabla_\theta R_\phi,g_\tau\rangle\ge \gamma>0.
\]

也就是说，沿着 `-g_tau` 做梯度下降，会降低 branch-recovery loss。

则对足够小的学习率 `eta`，MTP 相比 NTP 在一阶近似下多降低：

\[
\eta\lambda_\tau\gamma
\]

的语义恢复损失。

#### Proof

NTP 一步更新：

\[
\theta_N^+=\theta-\eta g_1.
\]

MTP 一步更新：

\[
\theta_M^+=\theta-\eta(g_1+\lambda_\tau g_\tau).
\]

Taylor expansion：

\[
R_\phi(\theta_N^+)=R_\phi(\theta)-\eta\langle\nabla R_\phi,g_1\rangle+O(\eta^2).
\]

\[
R_\phi(\theta_M^+)=R_\phi(\theta)-\eta\langle\nabla R_\phi,g_1\rangle-\eta\lambda_\tau\langle\nabla R_\phi,g_\tau\rangle+O(\eta^2).
\]

两者相减：

\[
R_\phi(\theta_N^+)-R_\phi(\theta_M^+)
=\eta\lambda_\tau\langle\nabla R_\phi,g_\tau\rangle+O(\eta^2).
\]

若内积至少为 `gamma`，则 MTP 在一阶上比 NTP 多降低约：

\[
\eta\lambda_\tau\gamma.
\]

这就是从“更直接地学”到“更高效地学”的最小理论桥梁。

### 7.4 Local-learning guard

MTP 不能以破坏 next-token 学习为代价。

令 local loss 就是 `L1`。MTP 一步后：

\[
L_1(\theta_M^+)=L_1(\theta)-\eta\|g_1\|^2-\eta\lambda_\tau\langle g_1,g_\tau\rangle+O(\eta^2).
\]

若

\[
\langle g_1,g_\tau\rangle\ge -\rho \|g_1\|^2/\lambda_\tau
\]

且 `rho < 1`，则 MTP 仍然保留一部分 local progress：

\[
L_1(\theta_M^+)\le L_1(\theta)-\eta(1-\rho)\|g_1\|^2+O(\eta^2).
\]

所以效率 claim 需要两个条件：

1. future gradient 对语义恢复有正投影；
2. future gradient 不严重破坏 local next-token 更新。

这正好对应实验里的两个指标：

```text
gradient usefulness: <grad R_phi, g_tau> > 0
local guard: Y1 loss/accuracy not degraded
```

---

## 8. 表征空间中“更容易发现和固定”的理论角度

用户提出的第二个方向很重要：

> 长程语义信息在表征空间的存在形式是否 MTP 比 NTP 更容易发现，并且能更高效地固定？

这可以比单纯 probe 更严格地说。

### 8.1 Readout-effective information

仅仅 `h_T` 含有 `Z` 还不够。`Z` 必须以输出头或下游 gate 能利用的方式存在。

对线性 future head：

\[
\ell_y(h)=w_y^\top h+b_y.
\]

如果 branch `z` 的正确 future token 是 `S_z`，那么正确 logit margin 是：

\[
M_z(h)=\ell_{S_z}(h)-\max_{y\ne S_z}\ell_y(h).
\]

若 CE 很低，则正确 token 概率高，margin 也高。

### 8.2 Theorem 5: low future-token CE implies output-facing separation

如果对每个 branch：

\[
q_\tau(S_z\mid h_z)\ge 1-\delta,
\]

则对任意 competitor `y`：

\[
\ell_{S_z}(h_z)-\ell_y(h_z)
\ge \log\frac{1-\delta}{\delta}.
\]

#### Proof

softmax 下：

\[
\frac{q(S_z\mid h_z)}{q(y\mid h_z)}=\exp(\ell_{S_z}(h_z)-\ell_y(h_z)).
\]

若 `q(S_z)>=1-delta`，任意 competitor 概率 `q(y)<=delta`，所以：

\[
\ell_{S_z}(h_z)-\ell_y(h_z)
=\log\frac{q(S_z\mid h_z)}{q(y\mid h_z)}
\ge \log\frac{1-\delta}{\delta}.
\]

这说明：MTP 不是只把 `Z` 藏在某个 arbitrary subspace；若 future head 成功，`Z` 必须被组织成能增加正确 future-token logit 的 readout-effective form。

### 8.3 与 MoE gating 的关系

MoE gating 需要的是可分、可稳定路由的 hidden-space feature。

如果 MTP 让 branch states 在 output-facing directions 上有稳定 margin，那么这些方向也可能成为 gate rows 的候选方向。

但这里要有边界：

- 可以说：MTP 可能让长程语义变量更 gateable。
- 不能说：MTP 已经证明能带来真实 expert utility。

要实验验证：

```text
linear gate Z accuracy
route NMI with Z
route margin
sign flip rate under training
local LM loss guard
branch-output alignment
```

这可以和原来的 nested learning / MoE gating 主线接上：

> MTP 可能不是直接提高下游性能，而是让早期语义变量在 hidden space 中更稳定、更线性、更可路由，从而降低 MoE gate 发现和保存该变量的难度。

---

## 9. NTP 仍可能学到：必须保留的边界

在 all-position LM-style training 中，NTP 或 non-covering K 也可能恢复 `Z`。

原因：

1. later positions 可以直接看到更接近 `S_Z` 的上下文；
2. causal Transformer 的 later states 可以 attend back to `BR_Z`；
3. all-position losses 会通过 shared parameters 间接改变早期 `h_T`；
4. 所以 NTP 上限可能和 MTP 接近，尤其在小 synthetic 任务里。

因此正确说法是：

> MTP 不是唯一能学，而是监督路径更短、更直接。最终上限是否更高不保证；效率、稳定性和可用性才是接下来要测的“好”。

---

## 10. 当前证据应该怎么放入故事

### K=2

K=2 已经证明并实验支持：

\[
Y_1=A,
\qquad
Y_2=S_Z.
\]

NTP/fixed-next-one 可以学 `A`，但不必让 `h_T` 暴露 `Z`。Next-two 预测 `S_Z`，所以会直接要求 `h_T` 含有 `Z`。

### K=3

K=3 检验 first-informative-horizon：

\[
Y_1=A,
\qquad
Y_2=C,
\qquad
Y_3=S_Z.
\]

decision-only 中 K=1/K=2 不覆盖 `tau=3`，K=3 覆盖，所以 K=3 应该更强。

all-position 中 K=1/K=2 也可能通过 indirect transfer 恢复 `Z`，这不是推翻理论，而是说明真实 LM-style 训练有间接路径。

### 现在最重要的缺口

当前还没有彻底证明：

\[
\text{direct supervision} \Rightarrow \text{faster / more stable learning}.
\]

所以必须做 learning curve，而不是只看 final table。

---

## 11. 接下来实验要回答的问题

### Experiment A: Semantic efficiency

问题：

> 在 all-position controlled LM training 中，覆盖 `tau` 的 MTP 是否比 NTP/non-covering K 更快、更稳地恢复 `Z`？

主指标：

\[
Q_K(t)=\min\{A_K(t),P_K(t),S_K(t)\}.
\]

其中：

- `A_K`: informative horizon prediction accuracy；
- `P_K`: frozen probe `h_T -> Z`；
- `S_K`: branch-swap consistency。

效率指标：

\[
T_\theta(K)=\inf\{t:Q_K(t)\ge \theta\},
\]

\[
\operatorname{AUC}_Q(K)=\frac{1}{T_{max}}\int_0^{T_{max}}Q_K(t)dt.
\]

必须加 local guard：

```text
Y1/Y2 local loss not degraded
```

### Experiment B: Representation form and gateability

问题：

> MTP 学到的长程语义信息是否比 NTP 更 readout-effective、更线性可分、更适合 MoE gating？

指标：

```text
branch-output alignment
future-token logit margin
linear probe margin
route NMI with Z
route margin
sign flip rate
gradient usefulness <grad R_phi, g_tau>
local guard
```

如果成立，可以说：

> MTP 不只是更快读出 `Z`，还让 `Z` 以更适合输出和 gating 的形式存在。

---

## 12. 最终 claim 模板

如果实验通过，可以写：

> In controlled long-horizon semantic tasks, MTP has a deterministic representation-supervision advantage over NTP when its horizon covers the first future token that reveals an early semantic variable. Under measured positive gradient usefulness and local-loss preservation, this direct supervision translates into faster or more stable recovery of the semantic variable in the prefix state. The resulting representation is not only more recoverable but also more output-facing and potentially more gateable.

中文：

> 在受控长程语义任务中，当 MTP 的预测范围覆盖第一个显现早期语义变量的未来 token 时，它对当前前缀状态具有 NTP 没有的确定性表示监督优势；如果该未来 token 的梯度确实降低语义恢复损失，并且不破坏本地 next-token 学习，这种直接监督会表现为更快或更稳的语义恢复。同时，成功的 MTP 表示应当更贴近输出方向，也更可能成为可路由的语义特征。

不能写：

> MTP universally outperforms NTP.

也不能写：

> NTP cannot learn long-horizon semantics.

---

## 13. 下一步决策

当前最小决策不是继续扩 K，也不是立刻声称自然语言提升。

最小决策是：

> MTP 的直接长程语义监督是否在 all-position controlled training 中转化为学习效率和表征可用性优势？

两个 protocol：

1. Semantic efficiency protocol：测 `T_theta`、AUC、local guard。
2. Representation form / gateability protocol：测 alignment、margin、route NMI、gradient usefulness。
