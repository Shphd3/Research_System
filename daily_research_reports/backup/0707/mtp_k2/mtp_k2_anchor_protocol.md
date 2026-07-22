# K=2 Long-Horizon Branch Task：Anchor + Protocol

Created: 2026-07-06  
Status: protocol-ready draft  
Corresponding theory document: `mtp_k2_theory_proof.md`

---

# Part A. Anchor

## 1. Verdict

当前最小任务是证明并验证：

> 在 $K=2$ 的 branch-delayed 分布中，next-two prediction 比 next-one prediction 更直接监督同一个 prefix hidden state $h_T$ 保留早期 branch key $B$。

最小数据结构：

$$
X=(B,F_{1:L},U,A,S_B).
$$

其中：

$$
Y_1=A\quad\text{shared},
$$

$$
Y_2=S_B\quad\text{branch-specific}.
$$

---

## 2. Phenomenon

目标现象：

> 早期变量 $B$ 只在第二个未来 token $Y_2$ 上显现；当前位置的下一个 token $Y_1$ 是 shared token，因此 next-one loss 不直接要求 $h_T$ 区分 branch。

这对应导师的“第一章不同、最后一章不同、中间章节相同或不足以决定最后一章”的最小 token 版本。

---

## 3. Question

主问题：

```text
Does next-two prediction impose direct supervision on h_T to preserve branch information that next-one prediction does not impose?
```

中文表述：

> next-two 是否比 next-one 更直接地建立早期 branch key $B$ 和远处 token $S_B$ 之间的连接？

---

## 4. Minimal construction

Branch：

$$
B\sim\mathrm{Unif}([m]).
$$

Sequence：

$$
X=(\mathrm{BR}_B,F_1,\ldots,F_L,U,A,S_B).
$$

Decision state：

$$
h_T^{(B)}=f_\theta(\mathrm{BR}_B,F_1,\ldots,F_L,U).
$$

Targets：

$$
X_{T+1}=A,
$$

$$
X_{T+2}=S_B.
$$

Distinctness：

$$
S_b\neq S_{b'}\quad(b\neq b').
$$

Information condition：

$$
I(B;Y_1)=0,
$$

$$
I(B;Y_2)=\log m.
$$

---

## 5. Objective terms

Next-one：

$$
\mathcal L_1
=
\mathrm{CE}(q_1(\cdot\mid h_T),A).
$$

Next-two：

$$
\mathcal L_2
=
\mathrm{CE}(q_1(\cdot\mid h_T),A)
+
\lambda\mathrm{CE}(q_2(\cdot\mid h_T),S_B).
$$

其中 $\lambda>0$。

---

## 6. Claims to preserve

### Claim 1：next-one at T 不强制 branch memory

因为 $A$ 对所有 branch 相同，branch-blind 表示：

$$
h_T^{(1)}=\cdots=h_T^{(m)}
$$

仍可实现：

$$
q_1(A\mid h_T)=1.
$$

---

### Claim 2：branch-blind lower bound

如果 $h_T$ branch-blind，则：

$$
\inf_q \mathbb E[-\log q(S_B\mid h_T)]\ge \log m.
$$

Top-1 accuracy 至多：

$$
1/m.
$$

---

### Claim 3：next-two 直接排除 branch-blind state

如果 $h_T$ branch-blind，则：

$$
\mathcal L_2\ge \lambda\log m.
$$

因此低 next-two loss 要求 $h_T$ 暴露 $S_B$-relevant information。

---

### Claim 4：gradient path distinction

Next-one gradient：

$$
\nabla_{h_T}\mathcal L_1
=
W_1^\top(p_1-e_A).
$$

Next-two gradient：

$$
\nabla_{h_T}\mathcal L_2
=
W_1^\top(p_1-e_A)
+
\lambda W_2^\top(p_2-e_{S_B}).
$$

第二项随 $B$ 改变，是 branch-specific direct gradient。

---

## 7. Rival explanations

| Rival explanation | How protocol controls it |
|---|---|
| 只是多了 heads / capacity | 使用 direct-head fixed-next-one：有 offset heads，但只训练 offset 1 |
| NTP 也能 rollout，所以已学会 long-horizon | 区分 teacher-forced rollout 与 single-prefix offset-2 prediction |
| offset-2 head 没训练所以 fixed-next-one 失败 | 加 frozen probe $h_T\to B$，测 representation 而不只测 native head |
| 任务太简单，local context 泄露 branch | 设置 $A,U,F$ 对所有 branch 共享；branch-swap test 检查 causal dependence |
| MTP 只是记住 suffix | branch-swap + probe + target probability by branch 检查是否真依赖 $B$ |

---

## 8. Claim boundary

可以 claim：

```text
In a K=2 branch-delayed distribution, next-two imposes direct branch-relevant supervision on h_T that next-one does not impose at the same prefix state.
```

不能 claim：

```text
MTP always outperforms NTP.
NTP cannot learn long-horizon dependencies.
Curriculum is better than full-horizon training.
Synthetic branch task proves real LLM long-range reasoning.
```

---

# Part B. Protocol

## 9. Purpose

实验验证理论中的三个对象：

1. next-one 是否能预测 shared $A$；
2. next-two 是否能让 $h_T$ 直接预测 branch-specific $S_B$；
3. 成功是否来自 multi-offset loss，而不是 architecture capacity。

---

## 10. Dataset protocol

### 10.1 Vocabulary

Required tokens：

```text
BR_1, ..., BR_m
F00, F01, ..., F{L-1}
U0, U1, ..., U{r-1}
A_SHARED
S_1, ..., S_m
STOP
```

Optional random filler vocabulary：

```text
RANDOM_000, ..., RANDOM_{V-1}
```

### 10.2 Sequence template

Clean version：

```text
BR_b F00 F01 ... F{L-1} U0 U1 A_SHARED S_b STOP
```

Evaluation prefix stops before `A_SHARED`：

```text
BR_b F00 F01 ... F{L-1} U0 U1
```

At this prefix：

```text
offset 1 target = A_SHARED
offset 2 target = S_b
```

### 10.3 Parameter grid

| parameter | stage 1 | stage 2 |
|---|---:|---:|
| num_branches | 3 | 4 or 8 |
| branch_delay_len L | 8 | 32, 128 |
| shared_context_len r | 2 | 4 |
| max_horizon | 2 | 2 |
| structured_probability | 1.0 | 0.3 |
| random_filler_probability | 0.0 | 0.7 |
| seeds | 971, 972, 973 | 971, 972, 973 |

Stage 1 先验证 clean theorem。Stage 2 再测试 filler entropy 与更长 delay。

---

## 11. Model conditions

### Minimal conditions

| condition | architecture | active loss | role |
|---|---|---|---|
| standard_lm | normal LM head | ordinary NTP | check rollout learnability |
| direct_heads_fixed_next_one | offset 1 and 2 heads exist | offset 1 only | capacity control |
| direct_heads_next_two | offset 1 and 2 heads exist | offset 1 + offset 2 | main test |

### Optional second phase

| condition | role |
|---|---|
| latent_decoder_fixed_next_one | capacity control for decoder path |
| latent_decoder_next_two | test whether decoder slots unpack branch info from $h_T$ |
| direct_heads_full_horizon_K2 | same as next-two if no curriculum; use as implementation sanity check |

For this K=2 task, curriculum is not the main claim. If included, it only means horizon 1 first, then horizon 2 activated later.

---

## 12. Training objectives

### Fixed next-one

$$
\mathcal L_{\mathrm{fixed1}}
=
\mathrm{CE}(q_1(\cdot\mid h_T),A).
$$

Offset-2 head exists but receives no training loss.

### Next-two

$$
\mathcal L_{\mathrm{next2}}
=
\mathrm{CE}(q_1(\cdot\mid h_T),A)
+
\mathrm{CE}(q_2(\cdot\mid h_T),S_B).
$$

### Standard LM

Train ordinary autoregressive NTP over the full sequence. Use it only to verify that the sequence distribution is learnable by rollout.

---

## 13. Evaluation metrics

### 13.1 Primary metrics

| metric | formula / procedure | purpose |
|---|---|---|
| offset1_accuracy | top-1 of $q_1(\cdot\mid h_T)$ on $A$ | both methods should pass |
| offset2_single_prefix_accuracy | top-1 of $q_2(\cdot\mid h_T)$ on $S_B$ | main behavioral test |
| offset2_target_probability | $q_2(S_B\mid h_T)$ | confidence on true branch target |
| worst_branch_offset2_probability | $\min_b q_2(S_b\mid h_T^{(b)})$ | detects brittle branch failure |
| branch_swap_consistency | replace `BR_b` with `BR_c`; check prediction switches from $S_b$ to $S_c$ | causal dependence on early key |
| frozen_probe_accuracy | freeze model; train linear probe $h_T\to B$ | representation-level branch info |

### 13.2 Secondary metrics

| metric | purpose |
|---|---|
| teacher_forced_next_token_accuracy | checks normal NTP learnability |
| autoregressive_rollout_accuracy | checks generation can finish sequence |
| offset2_loss_by_branch | checks branch imbalance |
| entropy of $q_2$ | checks whether fixed-next-one collapses to uniform |
| branch logit margin | $\ell_{S_b}(h_T^{(b)})-\max_{c\neq b}\ell_{S_c}(h_T^{(b)})$ |

### 13.3 Gradient diagnostic

At the decision prefix, compute:

$$
G_1(B)=\nabla_{h_T}\mathrm{CE}(q_1(\cdot\mid h_T),A),
$$

$$
G_2(B)=\nabla_{h_T}\mathrm{CE}(q_2(\cdot\mid h_T),S_B).
$$

Branch-gradient variation:

$$
V_j=
\mathbb E_B\left\|G_j(B)-\mathbb E_{B'}G_j(B')\right\|^2.
$$

Expected:

$$
V_1\approx 0,
$$

$$
V_2>0.
$$

---

## 14. Controls

### Control 1：capacity control

Use `direct_heads_fixed_next_one`.

Interpretation:

```text
If next-two succeeds and fixed-next-one fails,
then success is not merely due to having offset heads.
```

### Control 2：negative data control

Set:

$$
Y_2=S_0
$$

shared across branches.

Expected:

```text
next-two should not improve branch probe or branch-swap,
because offset 2 carries no branch information.
```

### Control 3：anti-separation data control

Set:

$$
Y_1=S_B.
$$

Expected:

```text
fixed next-one should improve branch information,
because offset 1 already contains branch supervision.
```

This verifies that the clean separation depends on `Y1 shared, Y2 branch-specific`.

---

## 15. Expected outcomes

### Strong support

```text
direct_heads_fixed_next_one:
  offset1_accuracy high
  teacher_forced_rollout high
  offset2_single_prefix_accuracy near chance or unstable
  branch_swap_consistency fails
  frozen_probe weak or much lower than next-two

direct_heads_next_two:
  offset1_accuracy high
  offset2_single_prefix_accuracy high
  offset2_target_probability high
  worst_branch_offset2_probability high
  branch_swap_consistency passes
  frozen_probe strong
```

### Weak support

```text
next-two native offset2 succeeds,
but frozen_probe only moderately improves.
```

Interpretation: future head learns useful readout, but representation separation is not clean enough.

### Falsification / route revision

```text
fixed-next-one matches next-two on offset2_single_prefix_accuracy,
branch_swap_consistency,
and frozen_probe_accuracy across seeds.
```

Interpretation: this dataset or architecture does not instantiate the intended separation. The theorem remains logically valid, but the empirical task fails to expose the mechanism.

---

## 16. Reporting table templates

### 16.1 Behavioral metrics

| seed | condition | offset1_acc | offset2_acc | offset2_prob | worst_branch_prob | branch_swap | rollout_acc |
|---:|---|---:|---:|---:|---:|---:|---:|
| 971 | fixed_next_one |  |  |  |  |  |  |
| 971 | next_two |  |  |  |  |  |  |
| 972 | fixed_next_one |  |  |  |  |  |  |
| 972 | next_two |  |  |  |  |  |  |
| 973 | fixed_next_one |  |  |  |  |  |  |
| 973 | next_two |  |  |  |  |  |  |

### 16.2 Representation metrics

| seed | condition | frozen_probe_acc | branch_logit_margin | V1_gradient_variation | V2_gradient_variation |
|---:|---|---:|---:|---:|---:|
| 971 | fixed_next_one |  |  |  |  |
| 971 | next_two |  |  |  |  |
| 972 | fixed_next_one |  |  |  |  |
| 972 | next_two |  |  |  |  |
| 973 | fixed_next_one |  |  |  |  |
| 973 | next_two |  |  |  |  |

---

## 17. Mapping from theory to protocol

| Theory object | Protocol measurement |
|---|---|
| $Y_1=A$ shared | offset1 accuracy should be high for all methods |
| $Y_2=S_B$ branch-specific | offset2 single-prefix prediction |
| branch-blind lower bound $\log m$ | fixed-next-one offset2 loss / accuracy near chance |
| next-two direct supervision | next-two offset2 probability high |
| $I(h_T;B)$ lower bound under low offset2 loss | frozen probe $h_T\to B$ |
| branch-specific gradient term | gradient variation $V_2>V_1$ |
| causal dependence on early key | branch-swap consistency |

---

## 18. Minimal next action

Implement only the K=2 clean experiment first:

```text
BR_b F00 ... F{L-1} U0 U1 A_SHARED S_b STOP
```

Compare:

```text
direct_heads_fixed_next_one
vs
direct_heads_next_two
```

Report:

```text
offset1_acc
offset2_single_prefix_acc
offset2_target_prob
worst_branch_offset2_prob
branch_swap_consistency
frozen_probe_acc
```

Only after this passes should we return to longer next-k, curriculum schedule, SNR, or compositional branch rules.
