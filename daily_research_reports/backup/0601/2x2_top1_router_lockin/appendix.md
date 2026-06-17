## Mechanistic Lemma: Top-1 / Top-k Selected-Gate Routing Reinforces Early Assignment

### Setup

Let the router logit for expert $e$ be

$$
z_e = w_e^\top h,
$$

where $h\in \mathbb{R}^d$ is the routed hidden state and $w_e$ is the router row for expert $e$.

Let

$$
p_e=\frac{\exp(z_e)}{\sum_j \exp(z_j)}
$$

be the router softmax probability.

We consider a selected-gate sparse MoE where the selected expert output is multiplied by the selected gate. This matches the mechanism we want to audit: selected experts receive token traffic and unselected experts receive little or no update.

---

## Proposition 1: Top-1 selected-gate routing reinforces the initially selected expert

### Statement

Let

$$
s=\arg\max_e z_e
$$

be the top-1 selected expert for hidden state $h$. Suppose the model output is

$$
o=p_s f_s(h),
$$

and the loss is $\ell(o,y)$.

Define

$$
a_s=\frac{\partial \ell}{\partial p_s}
=\left\langle \nabla_o \ell,\ f_s(h)\right\rangle.
$$

If

$$
a_s < 0,
$$

then increasing the selected gate $p_s$ decreases the loss. Under one gradient descent step on the router weights, the selected expert logit $z_s$ increases on the same hidden state $h$, while every unselected expert logit $z_j$, $j\neq s$, decreases. Therefore the logit margin

$$
z_s-z_j
$$

strictly increases for every $j\neq s$.

### Proof

Since only $p_s$ is used in the selected-gate output,

$$
\frac{\partial \ell}{\partial z_j}
=
\frac{\partial \ell}{\partial p_s}
\frac{\partial p_s}{\partial z_j}.
$$

For softmax,

$$
\frac{\partial p_s}{\partial z_s}=p_s(1-p_s),
$$

and for $j\neq s$,

$$
\frac{\partial p_s}{\partial z_j}=-p_s p_j.
$$

Therefore,

$$
\frac{\partial \ell}{\partial z_s}
=
a_s p_s(1-p_s),
$$

and

$$
\frac{\partial \ell}{\partial z_j}
=
-a_s p_s p_j,\qquad j\neq s.
$$

Because $z_j=w_j^\top h$,

$$
\frac{\partial \ell}{\partial w_j}
=
\frac{\partial \ell}{\partial z_j}h.
$$

A gradient descent update with step size $\eta>0$ gives

$$
w_j^+ = w_j-\eta \frac{\partial \ell}{\partial w_j}.
$$

Thus the change in logit on the same hidden state $h$ is

$$
z_j^+ - z_j
=
(w_j^+-w_j)^\top h
=
-\eta \frac{\partial \ell}{\partial z_j}\|h\|^2.
$$

For the selected expert $s$,

$$
z_s^+-z_s
=
-\eta a_s p_s(1-p_s)\|h\|^2.
$$

Since $a_s<0$,

$$
z_s^+-z_s>0.
$$

For any unselected expert $j\neq s$,

$$
z_j^+-z_j
=
\eta a_s p_s p_j\|h\|^2.
$$

Since $a_s<0$,

$$
z_j^+-z_j<0.
$$

Therefore,

$$
(z_s^+-z_j^+) - (z_s-z_j)
=
-\eta a_s p_s(1-p_s+p_j)\|h\|^2>0.
$$

So the selected expert becomes more preferred for the same hidden state $h$. This proves that, when the selected expert is loss-improving, top-1 selected-gate routing reinforces the initial assignment.

### Expert starvation consequence

In top-1 sparse routing, only expert $s$ receives this token's expert update. For $j\neq s$,

$$
\frac{\partial \ell}{\partial \theta_j}=0.
$$

Thus the selected expert receives both expert-function learning and router reinforcement, while unselected experts receive no expert update for this token. This creates a positive feedback loop:

$$
\text{early selection}
\rightarrow
\text{more update for selected expert}
\rightarrow
\text{higher selected gate confidence}
\rightarrow
\text{more future selection}.
$$

This is the local gradient mechanism behind early lock-in and expert starvation.

---

## Proposition 2: Top-k selected-gate routing reinforces useful experts inside the selected set and starves unselected experts

### Statement

Let $S=\operatorname{TopK}(z)$ be the selected expert set, and assume the top-k set does not change under an infinitesimal update.

Let the top-k normalized gate be

$$
q_e=\frac{\exp(z_e)}{\sum_{r\in S}\exp(z_r)},\qquad e\in S.
$$

The output is

$$
o=\sum_{e\in S}q_e f_e(h).
$$

Define

$$
a_e=\frac{\partial \ell}{\partial q_e}
=
\left\langle \nabla_o\ell,\ f_e(h)\right\rangle,
$$

and

$$
\bar a = \sum_{r\in S} q_r a_r.
$$

Then for $e\in S$,

$$
\frac{\partial \ell}{\partial z_e}
=
q_e(a_e-\bar a).
$$

Thus, under gradient descent,

$$
z_e^+-z_e
=
-\eta q_e(a_e-\bar a)\|h\|^2.
$$

Therefore:

* if $a_e<\bar a$, increasing expert $e$'s gate reduces loss more than the selected-set average, so $z_e$ increases;
* if $a_e>\bar a$, expert $e$ is worse than the selected-set average, so $z_e$ decreases;
* if $j\notin S$, then $j$ receives no top-k gate update and no expert update under the masked top-k path.

### Proof

For $e\in S$, the softmax derivative inside the selected set is

$$
\frac{\partial q_r}{\partial z_e}
=
q_r(\mathbf{1}_{r=e}-q_e).
$$

Therefore,

$$
\frac{\partial \ell}{\partial z_e}
=
\sum_{r\in S}
\frac{\partial \ell}{\partial q_r}
\frac{\partial q_r}{\partial z_e}
=
\sum_{r\in S}
a_r q_r(\mathbf{1}_{r=e}-q_e).
$$

This becomes

$$
\frac{\partial \ell}{\partial z_e}
=
a_e q_e - q_e\sum_{r\in S}q_r a_r
=
q_e(a_e-\bar a).
$$

Since

$$
z_e=w_e^\top h,
$$

one gradient descent step gives

$$
z_e^+-z_e
=
-\eta q_e(a_e-\bar a)\|h\|^2.
$$

So if $a_e<\bar a$, then $z_e$ increases; if $a_e>\bar a$, then $z_e$ decreases.

For $j\notin S$, the masked top-k output does not use $q_j$, and expert $j$ receives no token traffic. Thus

$$
\frac{\partial \ell}{\partial \theta_j}=0.
$$

So top-k routing has two lock-in effects:

1. inside the selected set, relatively useful experts receive increasing gate probability;
2. outside the selected set, unselected experts receive little or no learning signal for this token.

This proves that top-k selected-gate routing still creates path dependence: early inclusion in the selected set gives experts a chance to improve, while early exclusion causes starvation.

---

## Corollary: Why NTP does not guarantee feature-level specialization

Even if two features are linearly separable in hidden space, NTP loss does not directly require the router to assign them to different experts.

If early top-1 or top-k routing assigns multiple features to the same expert or selected expert set, the selected experts receive more token traffic and more router reinforcement. Unselected experts receive little or no update for those features.

Therefore, selected-gate sparse MoE can learn the token prediction task while failing to recover feature-level route separation. This explains why task learning does not imply route-pattern specialization.
