# Anchor A: K=2 Semantic Efficiency After Objective-Level Separation

Version: v0  
Purpose: decide whether the K=2 representation guarantee becomes a learning-efficiency claim.

---

## Verdict

The K=2 theorem already proves an objective-level advantage: next-two forces $h_T$ to contain the early branch variable when $Y_1$ is shared and $Y_2$ is branch-specific. The next question is whether this pressure makes learning faster, more stable, or more robust than NTP under matched architecture and budget.

---

## Research question

In the K=2 long-horizon semantic task,

$$
Y_1=A,
\qquad
Y_2=S_Z,
$$

does next-two prediction recover the early semantic variable $Z$ in $h_T$ faster or more robustly than NTP / fixed next-one?

---

## Motivation

The existing proof establishes:

$$
\text{low offset-2 loss}\Rightarrow I(h_T;Z)\text{ large}.
$$

It does not establish:

$$
\text{next-two learns }Z\text{ faster than NTP}.
$$

This anchor tests the missing link from representation requirement to learning efficiency.

---

## Physical prior

If $Y_1$ is shared, NTP at the decision state receives no direct branch-specific gradient. If $Y_2=S_Z$, next-two receives a direct branch-specific gradient at the same state. Therefore next-two should recover $Z$ earlier, unless optimization interference or insufficient capacity blocks the signal.

---

## Formal setup

Early semantic variable:

$$
Z\sim\operatorname{Unif}\{1,\ldots,m\}.
$$

Sequence:

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,S_Z).
$$

Decision state:

$$
h_T=f_\theta(\operatorname{BR}_Z,F_{1:L},U).
$$

Targets:

$$
Y_1=A,
\qquad
Y_2=S_Z.
$$

Information structure:

$$
I(Z;Y_1)=0,
\qquad
I(Z;Y_2\mid Y_1)=H(Z).
$$

---

## Hypothesis

### H1: representation pressure

Next-two should make $h_T$ branch-informative, while fixed next-one may remain branch-blind.

### H2: learning efficiency

Next-two should reach a guarded semantic recovery threshold earlier than fixed next-one:

$$
T_\theta(2)<T_\theta(1).
$$

### H3: local guard

The gain should not come from destroying immediate next-token learning:

$$
L_1^{(2)}(t)\le L_1^{(1)}(t)+\epsilon_{\mathrm{local}}.
$$

---

## Main metric

Define

$$
Q_K(t)=\min\{A_K(t),P_K(t),S_K(t)\}.
$$

- $A_K(t)$: informative-horizon accuracy, here $h_T\to S_Z$.
- $P_K(t)$: frozen evaluation probe accuracy, $h_T\to Z$.
- $S_K(t)$: branch-swap consistency.

Efficiency metrics:

$$
T_\theta(K)=\inf\{t:Q_K(t)\ge\theta\},
$$

$$
\operatorname{AUC}_Q(K)=\frac{1}{T_{\max}}\int_0^{T_{\max}}Q_K(t)dt.
$$

---

## Pass criteria

Strong support if:

1. next-two reaches $Q_K\ge0.9$ earlier than fixed next-one;
2. next-two has larger $\operatorname{AUC}_Q$;
3. local $Y_1$ loss/accuracy is not worse beyond tolerance;
4. gradient usefulness for $L_2$ is positive:

$$
\langle \nabla_{\theta_s}R_\phi,\nabla_{\theta_s}L_2\rangle>0.
$$

---

## Fail criteria

The efficiency claim is weakened if:

1. fixed next-one matches next-two on $Q_K(t)$;
2. next-two only wins by hurting $Y_1$ learning;
3. branch probe is high but head-2 and branch-swap are weak;
4. the noisy target control behaves like the branch-specific target.

---

## Claim if passed

In the controlled K=2 long-horizon semantic task, next-two prediction is not only a stronger representation objective; it also learns the early semantic variable faster or more robustly than next-one under matched architecture and budget.

---

## Claim if failed

The K=2 theorem still stands as an objective-level separation, but the experiment does not support a learning-efficiency advantage in this setup.

