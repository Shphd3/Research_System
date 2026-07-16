# Theory Clarification and Meeting Anchor

Date: 2026-07-16

Status: AI theory audit; not the researcher's judgment, a formal anchor, or an
experimental Protocol.

Chinese companion:
[05_theory_clarification_and_meeting_anchor_cn.md](05_theory_clarification_and_meeting_anchor_cn.md)

## 1. Meeting Theme and Corrected Beliefs

> **Against a matched shared-aux control, does informative MTP produce a
> common-orthogonal update for a low-frequency latent feature that is locally
> useful to the standard NTP head?**

The smallest deliverable is not a proof that MTP works. It is the distinction
between three claims: a direction is new, it aligns with rare learning, and it
produces a functional loss improvement.

The recordings ask for a causal next-one/next-two contrast, easier separation
of mixed representations, and eventual expert allocation by feature type and
frequency. They do not establish that MTP solves common/rare imbalance. The
current low-hanging fruit reduces that bridge to a matched local effect at one
parameter point.

The three prior beliefs are corrected as follows:

1. A large activation singular value means high second-moment energy; a large
   weight singular value means high linear gain. Neither establishes semantic
   identity, learning speed, or common-to-rare assistance.
2. Rare learning can be slow through frequency starvation or fail through
   frequency-amplified negative gradient interaction. Positive common/rare
   alignment is constructive reuse, not conflict.
3. Raw MTP gradient alignment and norm are insufficient. First isolate
   $\Delta g_{\mathrm{info}}=G_{\mathrm{informative}}-G_{\mathrm{shared}}$,
   then separate geometric novelty from curvature-corrected functional effect.

## 2. Objects and Assumptions

Let $\theta$ contain only shared parameters accessible to the standard NTP
head. Let

$$
L(\theta)=\pi_C L_C(\theta)+\pi_RL_R(\theta),
$$

with $g_C=\nabla L_C$, $g_R=\nabla L_R$, and
$H_C=\nabla^2L_C$, $H_R=\nabla^2L_R$.

$P_C$ is a frozen orthogonal projector built at the checkpoint from the top
eigenspace of common-sample parameter-gradient covariance or empirical
Fisher. An activation-covariance subspace is only an auxiliary diagnostic;
weight SVD is explanatory only. Empirical Fisher is not generally identical
to the Hessian.

Assume local twice differentiability, a bounded third-order remainder when
used, the same frozen parameter point and evaluation data, matched active
heads/CE terms/nominal scale for informative and shared-aux conditions, and a
precommitted $P_C$ construction and rank. Claims are local, not full-trajectory
Transformer theorems.

## 3. Spectral Dynamics

### Lemma 1

For

$$
L(\theta^\star+e)=\frac12e^\top He,
\qquad
H=Q\operatorname{diag}(\lambda_i)Q^\top\succeq0,
$$

gradient descent gives

$$
e_{t+1,i}=(1-\eta\lambda_i)e_{t,i}.
$$

**Proof.** Expand $e_t$ in the orthonormal eigenbasis of $H$ and apply
$e_{t+1}=e_t-\eta He_t$ coordinatewise. $\square$

The dynamics are stable for $0<\eta<2/\lambda_{\max}$ and monotone in every
positive-curvature coordinate for $\eta\leq1/\lambda_{\max}$. Larger positive
curvature usually contracts faster within that regime, while
$\lambda_{\max}$ limits the global step size. If
$\lambda_C\gg\lambda_R>0$, a step of order $1/\lambda_C$ leaves rare
contraction at approximately $1-O(\lambda_R/\lambda_C)$, producing stiffness.
None of this identifies activation or weight singular values with Hessian
eigenvalues outside an explicitly specified model.

## 4. Starvation, Conflict, and Reuse

The NTP training gradient is

$$
G_N=\pi_Cg_C+\pi_Rg_R.
$$

### Lemma 2

The rare first-order descent drive is

$$
D_R=\langle g_R,G_N\rangle
=\pi_R\|g_R\|^2+\pi_C\langle g_R,g_C\rangle.
$$

**Proof.** Taylor-expand $L_R(\theta-\eta G_N)$. $\square$

Positive cross alignment is constructive reuse. Near-zero cross alignment
with small $\pi_R$ is frequency starvation: rare still improves, but slowly.
Negative cross alignment is conflict, and stall or regression occurs when

$$
\pi_C[-\langle g_R,g_C\rangle]_+
\geq\pi_R\|g_R\|^2,
$$

equivalently $D_R\leq0$ at first order.

## 5. MTP Geometry

For a weighted multi-horizon objective,

$$
G_{\mathrm{MTP}}=\sum_{k=1}^K\lambda_kg_k,
\qquad
H_{\mathrm{MTP}}=\sum_{k=1}^K\lambda_kH_k.
$$

These are exact derivative identities at a fixed point; a Fisher
approximation requires separate justification.

Use the information-specific contrast

$$
\Delta g_{\mathrm{info}}
=G_{\mathrm{informative}}-G_{\mathrm{shared}},
$$

and define

$$
A_R=\langle g_R,\Delta g_{\mathrm{info}}\rangle,
\qquad
E_\perp=
\frac{\|(I-P_C)\Delta g_{\mathrm{info}}\|^2}
{\|\Delta g_{\mathrm{info}}\|^2+\epsilon}.
$$

- $A_R>0,E_\perp\approx0$: helpful reuse inside an existing subspace.
- $A_R>0,E_\perp>0$: a new, first-order rare-aligned candidate; not yet a
  functional result.
- $A_R\leq0,E_\perp>0$: geometrically new but unhelpful or harmful to rare.
- Neither significant: no detected local information-specific mechanism.

If all relevant gradients remain in $\operatorname{range}(P_C)$, their linear
combinations also remain there. MTP then cannot create a common-orthogonal
update locally; it can only reweight the existing compromise.

## 6. Main Proposition: Curvature-Corrected Functional Effect

Define

$$
I_R(G)=L_R(\theta)-L_R(\theta-\eta G).
$$

Let $G_i=G_{\mathrm{informative}}$ and
$G_s=G_{\mathrm{shared}}$.

### Proposition

Under the stated assumptions,

$$
\Delta I_R
=I_R(G_i)-I_R(G_s)
=
\eta A_R
-\frac{\eta^2}{2}
\left(G_i^\top H_RG_i-G_s^\top H_RG_s\right)
+O(\eta^3).
$$

### Proof

Taylor-expand $L_R(\theta-\eta G_i)$ and
$L_R(\theta-\eta G_s)$ at the same $\theta$, convert each to $I_R$, and
subtract. The first-order difference is
$\eta g_R^\top(G_i-G_s)=\eta A_R$; the remaining displayed difference is the
second-order curvature correction. $\square$

Thus $A_R>0$ only establishes infinitesimal alignment. A finite step can still
fail if its curvature penalty dominates. A small learning-rate scan must
compare Taylor prediction against an actual one-step update. A common guard
must also hold:

$$
I_C(G_i)-I_C(G_s)\geq-\tau_C,
$$

with $\tau_C$ preregistered.

## 7. Counterexamples and Transformer Boundary

Counterexamples include:

1. large activation mean or weight gain with output error orthogonal to that
   direction, producing zero gradient;
2. $A_R>0$ but sufficiently large rare curvature and step size, giving
   $\Delta I_R\leq0$;
3. $E_\perp>0$ with the new component orthogonal or opposed to $g_R$;
4. extra heads that duplicate next-token information, increasing raw gradient
   while leaving $\Delta g_{\mathrm{info}}=0$;
5. future horizons that amplify common structure and worsen imbalance;
6. a positive local step whose direction is later erased or cannot be
   transported and read by the standard head.

The result does not prove a fixed Hessian or fixed $P_C$ over Transformer
training, identify parameter orthogonality with semantic features, equate
empirical Fisher and Hessian, establish long-run representation formation or
standard-head causal use, or imply benefits for code, planning, long context,
or MoE routing.

## 8. Testable Predictions and Research Gates

A locally useful new rare update predicts, relative to matched shared-aux:

1. stable, above-noise $E_\perp$;
2. $A_R>0$, persisting under norm matching if it is a direction effect;
3. agreement between Taylor prediction and actual $\Delta I_R$ at small
   learning rates;
4. actual $\Delta I_R>0$;
5. a passing common-loss guard.

Interpretation remains local:

- $\Delta I_R>0,E_\perp>0$: useful new local update;
- $\Delta I_R>0,E_\perp\approx0$: existing-subspace strengthening or reuse;
- $\Delta I_R\leq0,E_\perp>0$: new but not useful;
- native-only benefit: primarily a norm effect.

The ordered research line is:

```text
define rare and the NTP failure
-> matched same-point local utility
-> long-run formation
-> transport and standard-head causal use
-> workload property
-> MTP modification
-> held-out expert utility
-> Router design
```

Project roles remain unchanged: A06 is the Router mainline, A07 supplies
controlled common/rare evidence, A11 supplies formation/reachability/use
evidence for informative future supervision, and A12 currently lacks a valid
carrier. This question is a candidate A11-to-A07 bridge; only after the local
and formation/use gates could it supply A06 with a Router signal.

The only current decision is whether the researcher approves the matched
same-point one-step question in the
[Thinking Card](03_mtp_mainline_thinking_card_cn.md). Stop before a formal
anchor, Protocol, implementation, or run.
