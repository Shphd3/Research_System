# Soft Router And Top-K Router Mechanism Note

## What This Note Establishes

This note gives a local mathematical mechanism for router-gradient amplification in soft routing and extends it to top-K sparse routing.

**Core claim:** a high-gain router direction does not unconditionally attract later features. It has an optimization advantage only when the router error signal has nonzero projection onto the corresponding output-side singular direction.

The local first-order descent scale for mode $i$ is

$$
\Delta L_i \approx -\eta \sigma_i^2 \langle u_i, g_a\rangle^2.
$$

Here $g_a=\nabla_a L$ is the router-logit error vector. Therefore, the decisive quantity is not $\sigma_i$ alone, but

$$
\sigma_i^2 \langle u_i, g_a\rangle^2.
$$

## 1. Terminology / Definitions

**Router logits:** the pre-softmax scores used to choose experts.

$$
a = R h.
$$

Here $h$ is the token hidden state and $R$ is the router matrix.

**Router probabilities:** the expert weights produced from router logits.

$$
q = \operatorname{softmax}(a).
$$

**Soft routing:** every expert receives a nonzero routing weight $q_e$ before pruning or sparsification.

**Top-K routing:** only the $K$ experts with largest router logits are kept active. The inactive experts are assigned zero routing weight.

**Router error signal:** the gradient of the loss with respect to router logits.

$$
g_a = \nabla_a L.
$$

It plays the same role for routing that $p-e_y$ plays for ordinary softmax classification.

**High-gain mode:** a singular mode of the router matrix with large singular value. If

$$
R=\sum_i \sigma_i u_i v_i^\top,
$$

then $v_i$ is the hidden-side direction, $u_i$ is the router-logit-side direction, and $\sigma_i$ is the gain.

## 2. Soft-Routing Model

Let the router logits be

$$
a = R h,
$$

and the routing probabilities be

$$
q_e = \frac{\exp(a_e)}{\sum_j \exp(a_j)}.
$$

The MoE output can be written locally as

$$
y = \sum_e q_e f_e(h),
$$

where $f_e(h)$ is the output of expert $e$.

For the router-gradient analysis, freeze the expert outputs at the current local point and define

$$
s_e = \frac{\partial L}{\partial q_e}.
$$

In a differentiable MoE output, if $g_y=\nabla_y L$, then locally

$$
s_e = \langle g_y, f_e(h)\rangle.
$$

The softmax derivative gives

$$
\frac{\partial L}{\partial a_e}
= q_e\left(s_e - \bar{s}\right),
$$

where

$$
\bar{s}=\sum_j q_j s_j.
$$

Therefore

$$
g_a = q \odot (s-\bar{s}\mathbf{1}).
$$

Interpretation:

- if $s_e<\bar{s}$, increasing $q_e$ lowers the loss relative to the current mixture;
- if $s_e>\bar{s}$, increasing $q_e$ raises the loss relative to the current mixture.

Under gradient descent,

$$
\delta a_e = -\eta g_{a,e}.
$$

So an expert with $s_e<\bar{s}$ has $g_{a,e}<0$ and receives a positive router-logit update.

## 3. Relation To Cross-Entropy

For ordinary classification, logits $z$ produce probabilities

$$
p=\operatorname{softmax}(z),
$$

and cross-entropy is

$$
L=-\log p_y.
$$

The key identity is

$$
\nabla_z L = p-e_y.
$$

This means:

- the true class has gradient $p_y-1<0$, so gradient descent raises its logit;
- each wrong class has gradient $p_j>0$, so gradient descent lowers its logit.

For a supervised router target $e^\star$, the same identity gives

$$
g_a = q-e_{e^\star}.
$$

For utility-driven routing, there is usually no fixed target expert. Then the router error is instead

$$
g_a = q \odot (s-\bar{s}\mathbf{1}).
$$

This is the correct analogue of $p-e_y$ for soft routing.

## 4. Singular-Mode Router Gradient

Use the singular value decomposition of the router matrix:

$$
R=\sum_i \sigma_i u_i v_i^\top.
$$

Since

$$
a=Rh,
$$

the router-score gradient back to the hidden state is

$$
\nabla_h L = R^\top g_a.
$$

Substitute the decomposition:

$$
R^\top g_a
= \sum_i \sigma_i v_i u_i^\top g_a
= \sum_i \sigma_i \langle u_i,g_a\rangle v_i.
$$

Define

$$
\alpha_i=\langle u_i,g_a\rangle.
$$

Then the hidden-state gradient component on mode $i$ is

$$
\sigma_i\alpha_i v_i.
$$

This is the first important condition:

$$
\alpha_i \neq 0.
$$

If $\alpha_i=0$, the high-gain mode has no first-order router-gradient effect on the current example, no matter how large $\sigma_i$ is.

## 5. Why The Descent Scale Contains $\sigma_i^2$

The gradient step on hidden state contributed by mode $i$ is

$$
\delta h_i = -\eta \sigma_i \alpha_i v_i.
$$

The induced router-logit change is

$$
\delta a_i = R\delta h_i.
$$

Because

$$
Rv_i=\sigma_i u_i,
$$

we get

$$
\delta a_i
= -\eta \sigma_i \alpha_i Rv_i
= -\eta \sigma_i^2 \alpha_i u_i.
$$

Using first-order Taylor expansion in router-logit space,

$$
\Delta L_i \approx \langle g_a,\delta a_i\rangle.
$$

Therefore

$$
\Delta L_i
\approx
\left\langle g_a,
-\eta \sigma_i^2 \alpha_i u_i
\right\rangle
= -\eta \sigma_i^2 \alpha_i^2.
$$

That is,

$$
\boxed{\Delta L_i \approx -\eta \sigma_i^2 \langle u_i,g_a\rangle^2.}
$$

The gain appears twice:

1. $R^\top$ amplifies the router error when it backpropagates to $h$;
2. $R$ amplifies the resulting hidden update when it maps back to router logits.

## 6. Mechanism Interpretation

A high-gain direction is not automatically reused.

The precise local statement is:

$$
\text{mode } i \text{ is favored if } \sigma_i^2 \langle u_i,g_a\rangle^2
\text{ is large.}
$$

Therefore, later features are attracted to an old high-gain direction only under two conditions:

1. the old direction has large gain $\sigma_i$;
2. the new example's router error signal has nonzero projection on $u_i$.

If two candidate modes are compared, old mode $i$ and new mode $j$, then the old mode has larger one-step descent only if

$$
\sigma_i^2 \langle u_i,g_a\rangle^2
>
\sigma_j^2 \langle u_j,g_a\rangle^2.
$$

This is the strict version of the phrase "high-gain directions attract later features".

## 7. Top-K Sparse Routing

For top-K routing, define the active expert set

$$
S_K(a)=\operatorname{TopK}(a).
$$

A common sparse normalized gate is

$$
q_e^{(K)}=
\begin{cases}
\dfrac{\exp(a_e)}{\sum_{j\in S_K(a)}\exp(a_j)}, & e\in S_K(a),\\
0, & e\notin S_K(a).
\end{cases}
$$

Away from top-K boundary changes, treat $S_K(a)$ as fixed. Then the within-active-set derivative is

$$
g_{a,e}^{(K)}
=
\begin{cases}
q_e^{(K)}\left(s_e-\bar{s}_K\right), & e\in S_K(a),\\
0, & e\notin S_K(a),
\end{cases}
$$

where

$$
\bar{s}_K=\sum_{j\in S_K(a)} q_j^{(K)}s_j.
$$

Thus top-K routing is the same local softmax-gradient mechanism, but restricted to the currently selected experts.

The singular-mode formula becomes

$$
\nabla_h L = R^\top g_a^{(K)}
=\sum_i \sigma_i \langle u_i,g_a^{(K)}\rangle v_i.
$$

The mode-wise first-order descent becomes

$$
\boxed{
\Delta L_i^{(K)}
\approx
-\eta \sigma_i^2
\langle u_i,g_a^{(K)}\rangle^2.
}
$$

So top-K does not remove the high-gain mechanism. It gates the mechanism by active-set membership.

## 8. What Changes From Soft Routing To Top-K

**Dense soft routing:** every expert can receive router-gradient signal because $q_e>0$ for all experts.

**Top-K routing with fixed active set:** only selected experts receive the normalized-gate gradient. Inactive experts have zero local gradient from the sparse gate.

**Top-K boundary:** the map $S_K(a)$ is discontinuous when two logits cross the K-th threshold. Standard gradients do not describe this boundary movement. Any gradient through the boundary comes from implementation choices such as straight-through estimation, dense-softmax auxiliary loss, noise, or load-balancing losses.

**Top-1 special case:** if top-1 is implemented as normalized softmax over only one selected expert, the selected gate weight is $1$ and the within-selected softmax derivative is zero. Router learning must then come from another path: unnormalized selected probabilities, straight-through gradients, auxiliary router losses, or changes in the selected expert caused by score boundary movement.

## 9. Claim Boundary

This note supports a local optimization claim:

$$
\text{given a fixed local router map and a fixed error signal, high }\sigma_i
\text{ increases first-order descent in proportion to }\sigma_i^2.
$$

It does not prove:

- that high-gain modes always align with useful features;
- that later features must reuse old modes;
- that top-K routing will preserve specialization;
- that route purity implies expert utility.

The missing empirical question is whether, over the data distribution,

$$
\mathbb{E}[\langle u_i,g_a\rangle^2]
$$

or

$$
\mathbb{E}[\langle u_i,g_a^{(K)}\rangle^2]
$$

is large for the same modes that already have high $\sigma_i$.

## 10. Minimal Falsification Test

For a trained or partially trained router, compute for each singular mode $i$:

$$
A_i = \mathbb{E}_{\text{tokens}}[\langle u_i,g_a\rangle^2],
$$

and

$$
D_i = \sigma_i^2 A_i.
$$

For top-K routing, replace $g_a$ with $g_a^{(K)}$.

The mechanism is supported if later-feature tokens concentrate their router-gradient descent mass on pre-existing high-$\sigma_i$ modes:

$$
D_i \text{ is large for old high-gain modes.}
$$

The mechanism is weakened if high-$\sigma_i$ modes have small $A_i$, or if later-feature tokens descend mainly through low-gain or newly formed modes.

## 11. Next Decision

The next concrete decision is whether to run a mode-level router-gradient audit:

1. compute router SVD at selected checkpoints;
2. compute $g_a$ for soft routing or $g_a^{(K)}$ for top-K routing;
3. measure $\sigma_i^2\langle u_i,g_a\rangle^2$ by token group;
4. test whether later or rare features reuse old high-gain modes, or only appear to do so because of load, shortcut, or active-set bias.
