# K=2 Long-Horizon Branch Task：理论证明文档

Created: 2026-07-06  
Status: draft-for-review  
Scope: `next-two token prediction` vs `next-one token prediction`。

---

## 0. 一句话结论

在一个最小 long-horizon branch 分布中，令第一个未来 token 对所有 branch 相同、第二个未来 token 由早期 branch key 决定：

$$
X=(B,F_{1:L},U,A,S_B).
$$

那么：

1. `next-one prediction` 在位置 $T$ 只要求 $h_T\to A$，因此不强制 $h_T$ 保留 $B$；
2. 如果 $h_T$ 丢掉 $B$，则任何从 $h_T$ 预测 $S_B$ 的 predictor 都有交叉熵下界 $\log m$；
3. `next-two prediction` 在同一个 $h_T$ 上额外监督 $h_T\to S_B$，因此低 loss 会排除 branch-blind 表示，并迫使 $h_T$ 暴露 branch-relevant information。

这证明的是 **objective-level separation**，不是证明 MTP 在所有任务上必然优于 NTP。

---

## 1. 术语与符号

### 1.1 Token 与位置

令序列为：

$$
X_1,X_2,\ldots,X_T,X_{T+1},X_{T+2}.
$$

模型在读完前缀 $X_{\le T}$ 后产生 hidden state：

$$
h_T=f_\theta(X_{\le T}).
$$

这里的 $T$ 是 decision position，即我们检查一个 prefix hidden state 是否已经包含未来信息的位置。

### 1.2 Branch key

早期分支变量：

$$
B\sim \mathrm{Unif}([m]),\qquad [m]=\{1,\ldots,m\}.
$$

可以把 $B$ 理解为“第一章不同的部分”或一个早期出现的控制变量。

### 1.3 Filler 与 shared local context

中间 filler：

$$
F_{1:L}=(F_1,\ldots,F_L).
$$

shared local context：

$$
U.
$$

二者的作用是制造 long horizon：它们把 $B$ 和最终目标隔开，并使当前位置附近的局部上下文不足以决定远处 token。

### 1.4 Future tokens

当前文档只做 $K=2$：

$$
Y_1=X_{T+1},\qquad Y_2=X_{T+2}.
$$

最小构造中设定：

$$
Y_1=A,
$$

$$
Y_2=S_B.
$$

其中 $A$ 对所有 branch 相同，$S_B$ 由 $B$ 决定。

---

## 2. 与原 design 的关系

原 design 的正确主线是：

> 同一个 causal hidden state $h_T$ 不只预测 $x_{T+1}$，还预测 $x_{T+2},\ldots,x_{T+k}$。如果多个 future tokens 共享同一个早期 cause，则多 offset loss 会给 $h_T$ 更强的 branch-relevant pressure。

本文保留原 design 的四点：

1. long-horizon dependency 的对象是“早期 branch key 影响远处 suffix”；
2. next-k 的核心是同一个 $h_T$ 预测多个 future offsets；
3. gradient 机制是多个 future losses 直接作用到同一个 prefix state；
4. 实验应关注 single-prefix suffix prediction，而不是只看 autoregressive rollout。

本文修改原 design 的一点：

原 design 写作：

$$
Y_{1:k}=s_B.
$$

这适合一般 next-k 叙事，但对于导师要求的 $K=2$ 最小分离不够干净。因为如果 $Y_1$ 已经由 $B$ 决定，那么 next-one loss 本身就已经给 $h_T$ branch supervision。

因此本文采用更干净的 $K=2$ 构造：

$$
Y_1=A\quad\text{shared},
$$

$$
Y_2=S_B\quad\text{branch-specific}.
$$

---

## 3. 最小生成模型

### Definition 1：K=2 branch-delayed distribution

给定 branch 数 $m\ge 2$。令：

$$
B\sim \mathrm{Unif}([m]).
$$

对每个 branch $b\in[m]$，定义一个 branch-specific token：

$$
S_b\in\mathcal V,
$$

并要求：

$$
S_b\neq S_{b'}\quad\text{for }b\neq b'.
$$

序列模板为：

$$
X=(\mathrm{BR}_B,F_1,\ldots,F_L,U,A,S_B).
$$

其中：

- $\mathrm{BR}_B$：早期 branch token；
- $F_{1:L}$：中间 filler；
- $U$：所有 branch 共享的局部上下文；
- $A$：第一个 future token，所有 branch 共享；
- $S_B$：第二个 future token，由 $B$ 决定。

令模型在读完：

$$
P_B=(\mathrm{BR}_B,F_1,\ldots,F_L,U)
$$

后产生：

$$
h_T^{(B)}=f_\theta(P_B).
$$

于是：

$$
X_{T+1}=A,
$$

$$
X_{T+2}=S_B.
$$

### 关键条件

第一个未来 token 不含 branch 信息：

$$
I(B;Y_1)=I(B;A)=0.
$$

第二个未来 token 完全含 branch 信息：

$$
I(B;Y_2)=I(B;S_B)=\log m.
$$

局部上下文不足以决定 $Y_2$：

$$
H(Y_2\mid U,A)=\log m.
$$

但知道 branch 后 $Y_2$ 确定：

$$
H(Y_2\mid B,U,A)=0.
$$

这就是导师“第一章影响最后一章，中间内容不是垃圾但不足以单独决定最后结果”的最小 token 版本。

---

## 4. 训练目标

### 4.1 Next-one objective at position T

在位置 $T$，next-one loss 是：

$$
\mathcal L_{1,T}(\theta)
=
\mathrm{CE}(q_1(\cdot\mid h_T),A).
$$

它只要求 $h_T$ 支持第一个未来 token $A$。由于 $A$ 对所有 branch 相同，该 loss 不直接要求 $h_T$ 区分 $B$。

### 4.2 Next-two objective at position T

next-two loss 是：

$$
\mathcal L_{2,T}(\theta)
=
\mathrm{CE}(q_1(\cdot\mid h_T),A)
+
\lambda\mathrm{CE}(q_2(\cdot\mid h_T),S_B),
$$

其中 $\lambda>0$。

第二项直接要求同一个 $h_T$ 预测 $S_B$，因此它是 branch-specific supervision。

---

## 5. Branch-blind lower bound

### Definition 2：branch-blind representation

如果：

$$
h_T^{(1)}=h_T^{(2)}=\cdots=h_T^{(m)},
$$

则称 $h_T$ 是 branch-blind。

更一般地，如果 predictor 无法区分 branches：

$$
q(\cdot\mid h_T^{(1)})=\cdots=q(\cdot\mid h_T^{(m)}),
$$

也称其在该预测任务上是 branch-blind。

### Lemma 1：branch-blind 表示不能低损失预测 $S_B$

假设：

1. $B\sim\mathrm{Unif}([m])$；
2. $S_1,\ldots,S_m$ 两两不同；
3. $h_T$ branch-blind。

则任意 predictor $q$ 满足：

$$
\mathbb E[-\log q(S_B\mid h_T)]\ge \log m.
$$

并且 deterministic top-1 accuracy 至多：

$$
\frac{1}{m}.
$$

### Proof

由于 $h_T$ branch-blind，所有 branch 下 predictor 看到的是同一个输入。因此它只能输出同一个分布：

$$
q(\cdot\mid h_T^{(1)})=\cdots=q(\cdot\mid h_T^{(m)})=:q(\cdot).
$$

期望交叉熵为：

$$
\mathcal L^{\mathrm{blind}}
=
\frac{1}{m}\sum_{b=1}^{m}-\log q(S_b).
$$

由于 $S_1,
\ldots,S_m$ 两两不同，真实目标分布是在 $\{S_1,\ldots,S_m\}$ 上的均匀分布。交叉熵在 $q(S_b)=1/m$ 时最小。因此：

$$
\min_q\mathcal L^{\mathrm{blind}}
=
-\frac{1}{m}\sum_{b=1}^{m}\log\frac{1}{m}
=
\log m.
$$

top-1 accuracy 方面，一个 common predictor 至多把一个 token 放在最高概率位置；由于真实 branch 均匀，最多命中 $m$ 个 branch 中的一个，因此 accuracy 至多 $1/m$。

证毕。

---

## 6. Next-one 不强制 $h_T$ 保留 branch 信息

### Proposition 1：在该构造中，next-one loss at T 有 branch-blind 最优解

在 K=2 branch-delayed distribution 中，存在 branch-blind 表示：

$$
h_T^{(1)}=\cdots=h_T^{(m)}=c,
$$

使得位置 $T$ 的 next-one loss 为 0。

### Proof

由于：

$$
Y_1=A
$$

对所有 branch 相同，只需令：

$$
q_1(A\mid c)=1.
$$

于是：

$$
\mathrm{CE}(q_1(\cdot\mid c),A)=0.
$$

该构造没有使用 $B$，所以 $h_T$ 可以 branch-blind。也就是说，next-one loss at $T$ 不区分：

$$
h_T\text{ 保留 }B
$$

和：

$$
h_T\text{ 丢掉 }B.
$$

证毕。

---

## 7. Autoregressive rollout 不推出 single-prefix future decodability

### Proposition 2：存在 NTP rollout 成功但 $h_T\to S_B$ 不可解码的模型

存在一个 causal sequence model，使得：

1. standard next-token rollout 在训练分布上成功；
2. 但 $h_T$ branch-blind；
3. 因而任何从 $h_T$ 预测 $S_B$ 的 predictor 都有 loss 下界 $\log m$。

### Proof by construction

构造模型如下。

在位置 $T$，令：

$$
h_T^{(B)}=c
$$

对所有 $B$ 相同，并令 next-token head 输出：

$$
p(A\mid h_T=c)=1.
$$

因此位置 $T$ 的 next-token loss 为 0。

在位置 $T+1$，模型已经读到完整 prefix：

$$
(\mathrm{BR}_B,F_{1:L},U,A).
$$

对于 Transformer-like causal model，位置 $T+1$ 的 hidden state 可以重新 attend 到早期 $\mathrm{BR}_B$。令：

$$
h_{T+1}^{(B)}=r_B,
$$

并令 next-token head 输出：

$$
p(S_B\mid h_{T+1}^{(B)})=1.
$$

则位置 $T+1$ 的 next-token loss 也为 0。

因此 autoregressive rollout 可以成功：

$$
h_T\to A,
$$

$$
h_{T+1}\to S_B.
$$

但由于：

$$
h_T^{(1)}=\cdots=h_T^{(m)}=c,
$$

由 Lemma 1 得：

$$
\inf_q\mathbb E[-\log q(S_B\mid h_T)]\ge \log m.
$$

所以 rollout success 不推出 single-prefix future decodability。

证毕。

### Architecture caveat

该命题依赖一个常见但需要明说的条件：later state 可以从完整 prefix 重新计算或重新访问早期 token。例如 causal Transformer 在后续位置可以 attend 到 earlier tokens。

如果架构是严格 recurrent bottleneck：

$$
h_{T+1}=F(h_T,A),
$$

且 $h_T$ 是唯一信息通道，那么 $h_T$ 丢掉 $B$ 后，$h_{T+1}$ 无法恢复 $B$。在这种架构下，NTP 可能也被迫让 $h_T$ 保留 $B$。

因此 Proposition 2 是 objective-level non-identifiability result，不是 universal architecture theorem。

---

## 8. Next-two 直接排除 branch-blind 表示

### Proposition 3：next-two low loss forces branch-relevant information

在 K=2 branch-delayed distribution 中，令：

$$
\mathcal L_{2,T}
=
\mathrm{CE}(q_1(\cdot\mid h_T),A)
+
\lambda\mathrm{CE}(q_2(\cdot\mid h_T),S_B),
$$

其中 $\lambda>0$。

如果 $h_T$ branch-blind，则：

$$
\mathcal L_{2,T}\ge \lambda\log m.
$$

### Proof

第一项非负：

$$
\mathrm{CE}(q_1(\cdot\mid h_T),A)\ge 0.
$$

由 Lemma 1，若 $h_T$ branch-blind，则：

$$
\mathrm{CE}(q_2(\cdot\mid h_T),S_B)\ge \log m.
$$

所以：

$$
\mathcal L_{2,T}
\ge
0+
\lambda\log m
=
\lambda\log m.
$$

证毕。

### Corollary 3.1：next-two 可以区分 branch-informative 与 branch-blind 表示

若模型容量足够，可以令：

$$
h_T^{(B)}=e_B,
$$

并令 heads 满足：

$$
q_1(A\mid e_B)=1,
$$

$$
q_2(S_B\mid e_B)=1.
$$

则：

$$
\mathcal L_{2,T}=0.
$$

因此 next-two objective 明确偏好 branch-informative 表示，而 branch-blind 表示存在不可消除的 loss gap：

$$
\lambda\log m.
$$

---

## 9. 信息论版本

### Proposition 4：低 offset-2 loss 推出 $h_T$ 含有 branch 信息

若存在只看 $h_T$ 的 decoder $q_2$，满足：

$$
\mathbb E[-\log q_2(S_B\mid h_T)]\le \varepsilon,
$$

则：

$$
I(h_T;B)\ge \log m-\varepsilon.
$$

### Proof

交叉熵上界条件蕴含：

$$
H(S_B\mid h_T)
\le
\mathbb E[-\log q_2(S_B\mid h_T)]
\le
\varepsilon.
$$

因为 $B\sim\mathrm{Unif}([m])$，且 $B\mapsto S_B$ 是一一映射，所以：

$$
H(S_B)=\log m.
$$

于是：

$$
I(h_T;S_B)
=
H(S_B)-H(S_B\mid h_T)
\ge
\log m-\varepsilon.
$$

由于 $S_B$ 与 $B$ 一一对应，二者生成同一个 sigma-field，因此：

$$
I(h_T;B)=I(h_T;S_B).
$$

所以：

$$
I(h_T;B)\ge \log m-\varepsilon.
$$

证毕。

### Interpretation

这给出 MTP 的 representation requirement：如果 offset-2 prediction 从 $h_T$ 做得好，那么 $h_T$ 必须包含接近 $\log m$ 的 branch 信息。

---

## 10. 梯度路径版本

### Proposition 5：next-two 有 branch-specific direct gradient

设 offset heads 是线性 head：

$$
z_j=W_jh_T+b_j,
$$

$$
p_j=\mathrm{softmax}(z_j).
$$

next-one loss 的梯度为：

$$
\nabla_{h_T}\mathcal L_{1,T}
=
W_1^\top(p_1-e_A).
$$

next-two loss 的梯度为：

$$
\nabla_{h_T}\mathcal L_{2,T}
=
W_1^\top(p_1-e_A)
+
\lambda W_2^\top(p_2-e_{S_B}).
$$

其中 $e_y$ 是 token $y$ 的 one-hot vector。

第一项只依赖 shared target $A$，不直接区分 branch。第二项含有 $e_{S_B}$，因此目标 token 随 $B$ 改变，是 branch-specific direct supervision。

### Proof

softmax cross-entropy 对 logits 的梯度是：

$$
\nabla_{z_j}\mathrm{CE}(p_j,y)=p_j-e_y.
$$

又因为：

$$
z_j=W_jh_T+b_j,
$$

所以：

$$
\nabla_{h_T}\mathrm{CE}(p_j,y)=W_j^\top(p_j-e_y).
$$

把 $j=1$ 和 $j=2$ 的项相加，即得上述公式。

证毕。

### Boundary

该命题证明的是“梯度路径存在且更直接”，不是证明优化一定成功。优化是否成功还取决于：

- head 初始化；
- learning rate；
- branch signal 与其他梯度是否冲突；
- model capacity；
- data mixing ratio；
- filler entropy。

原 design 中的 signal-to-noise ratio theorem 可以作为后续加强版，但需要额外假设，例如 residual gradients 弱相关、branch-relevant gradients 对齐。因此不作为本 K=2 证明主线。

---

## 11. 总 theorem package

### Theorem：K=2 next-two gives direct long-horizon supervision unavailable to next-one

在 K=2 branch-delayed distribution 中：

$$
X=(B,F_{1:L},U,A,S_B),
$$

其中 $A$ 对所有 branch 共享，$S_B$ 由早期 $B$ 一一决定。

则：

1. next-one loss at $T$ 只要求 $h_T\to A$，存在 branch-blind 零损失解；
2. branch-blind $h_T$ 从 $h_T\to S_B$ 的最优 cross-entropy 至少为 $\log m$；
3. next-two loss at $T$ 含有 $h_T\to S_B$ 的直接监督项，因而 branch-blind 表示有 loss gap $\lambda\log m$；
4. 若 offset-2 loss $\le\varepsilon$，则 $I(h_T;B)\ge \log m-\varepsilon$；
5. 对线性 heads，offset-2 的 branch-specific error 通过 $W_2^\top(p_2-e_{S_B})$ 直接回传到 $h_T$。

因此，next-two 比 next-one 更直接地建立早期 branch key 与远处 token 之间的连接。

### Proof

由 Proposition 1 得 next-one at $T$ 不强制保留 $B$。由 Lemma 1 得 branch-blind 表示无法预测 $S_B$，其 loss 下界为 $\log m$。由 Proposition 3 得 next-two loss 直接把该下界作用到 training objective，因此 low next-two loss 排除 branch-blind 表示。由 Proposition 4 得 low offset-2 loss 对应 branch information lower bound。由 Proposition 5 得这种监督在优化上表现为从 offset-2 error 到同一 $h_T$ 的直接梯度项。

证毕。

---

## 12. 实验设计：验证 K=2 theorem

### 12.1 实验目标

验证：

> 在 $Y_1$ shared、$Y_2$ branch-specific 的数据中，next-two training 会比 fixed next-one training 更容易让 $h_T$ 支持 $S_B$ 的 single-prefix prediction。

### 12.2 Dataset

模板：

```text
BR_b F00 F01 ... F{L-1} U0 U1 A_SHARED S_b .
```

评估 prefix 停在：

```text
BR_b F00 F01 ... F{L-1} U0 U1
```

此时：

```text
offset 1 = A_SHARED
offset 2 = S_b
```

推荐参数：

| parameter | value |
|---|---:|
| num_branches | 3 or 4 |
| branch_delay_len L | 8, 32, 128 |
| shared_context_len | 2 or 4 |
| max_horizon | 2 |
| structured_example_probability | 1.0 first, then 0.3 |
| random_filler_probability | 0.0 first, then 0.7 |
| seeds | 971, 972, 973 |

先用 clean deterministic version，再加 random filler。

### 12.3 Model conditions

| condition | architecture | active loss | role |
|---|---|---|---|
| standard LM | normal LM head | NTP | checks rollout learnability |
| direct-head fixed next-one | heads for offsets 1,2 exist | only offset 1 | capacity control |
| direct-head next-two | heads for offsets 1,2 exist | offset 1 + offset 2 | main MTP condition |

可选第二阶段：加入 latent decoder。第一阶段先用 direct heads，因为它最直接对应 $h_T\to Y_j$。

### 12.4 Training losses

Fixed next-one：

$$
\mathcal L_{\mathrm{fixed1}}
=
\mathrm{CE}(q_1(\cdot\mid h_T),A).
$$

Next-two：

$$
\mathcal L_{\mathrm{next2}}
=
\mathrm{CE}(q_1(\cdot\mid h_T),A)
+
\mathrm{CE}(q_2(\cdot\mid h_T),S_B).
$$

### 12.5 Primary metrics

| metric | definition | expected fixed-next-one | expected next-two |
|---|---|---:|---:|
| offset1_accuracy | $q_1(A\mid h_T)$ top-1 | high | high |
| offset2_single_prefix_accuracy | $q_2(S_B\mid h_T)$ top-1 | near $1/m$ or unstable | high |
| offset2_target_prob | $q_2(S_B\mid h_T)$ | low | high |
| worst_branch_offset2_prob | $\min_b q_2(S_b\mid h_T^{(b)})$ | low | high |
| branch_swap_consistency | change only $BR_b$, prediction changes to $S_b$ | fail | pass |
| frozen_probe_accuracy | train linear probe $h_T\to B$ after freezing model | low/unstable | high |

### 12.6 Diagnostic metrics

Gradient branch variation:

$$
G_j(B)=\nabla_{h_T}\mathrm{CE}(q_j(\cdot\mid h_T),Y_j).
$$

$$
V_j=\mathbb E_B\left\|G_j(B)-\mathbb E_{B'}G_j(B')\right\|^2.
$$

Prediction:

$$
V_1\approx 0,
$$

$$
V_2>0.
$$

This directly tests that offset 2 produces branch-dependent gradient while offset 1 does not.

### 12.7 Pass / fail criteria

Strong support if:

```text
fixed-next-one:
  offset1_accuracy high
  teacher-forced rollout high
  offset2_single_prefix low
  branch_swap fails
  frozen_probe weak or unstable

next-two:
  offset1_accuracy high
  offset2_single_prefix high
  branch_swap passes
  frozen_probe strong
```

Weak support if:

```text
next-two native offset2 passes,
but frozen probe only moderately improves.
```

Failure / revision if:

```text
fixed-next-one matches next-two on offset2_single_prefix and frozen_probe.
```

Interpretation: the dataset or architecture did not create the intended representation separation, even though the theorem remains logically valid.

---

## 13. Claim boundary

可以声称：

> 在 K=2 branch-delayed distribution 中，next-two objective 比 next-one objective 对 $h_T$ 施加更强的 direct branch-relevant supervision。

不可以声称：

1. MTP 一定优于 NTP；
2. NTP 一定学不到 long-horizon；
3. curriculum 一定优于 full-horizon；
4. synthetic result 直接推广到自然语言大模型；
5. gradient path 存在就保证 optimization 成功。

---

## 14. 下一步

把本文压缩成 formal anchor，再按 protocol 跑最小实验：

```text
B ... U A S_B
fixed-next-one vs next-two
single-prefix offset2 accuracy + branch-swap + frozen probe
```
