# Anchor B: K=3 First-Informative-Horizon Test

Version: v0  
Purpose: test whether the MTP advantage is controlled by coverage of the first semantic horizon, not by next-two specifically.

---

## Verdict

K=3 is necessary if we want to claim a NextK principle. The key comparison is not NTP vs next3 alone. It is:

$$
K=1\quad\text{vs}\quad K=2\quad\text{vs}\quad K=3
$$

under a distribution where the first semantic token appears only at horizon 3.

---

## Research question

If the early semantic variable $Z$ first appears in the third future token,

$$
Y_1=A,
\qquad
Y_2=C,
\qquad
Y_3=S_Z,
$$

does next3 improve semantic recovery while next2 behaves like NTP?

---

## Motivation

The K=2 result could be dismissed as a special case of next-two. K=3 tests the general mechanism:

> MTP helps when the prediction horizon covers the first token that reveals the early semantic variable.

If this is correct, next2 should not help in a $\tau=3$ task, while next3 should help.

---

## Formal setup

Early variable:

$$
Z\sim\operatorname{Unif}\{1,\ldots,m\}.
$$

Sequence:

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,C,S_Z).
$$

Decision state:

$$
h_T=f_\theta(\operatorname{BR}_Z,F_{1:L},U).
$$

Targets:

$$
Y_1=A,
\qquad
Y_2=C,
\qquad
Y_3=S_Z.
$$

Information:

$$
I(Z;Y_1)=0,
$$

$$
I(Z;Y_2\mid Y_1)=0,
$$

$$
I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

Thus

$$
\tau=3.
$$

---

## Hypothesis

### H1: coverage threshold

$$
K<3\Rightarrow\text{no direct semantic supervision on }h_T.
$$

$$
K=3\Rightarrow\text{direct supervision }h_T\to S_Z.
$$

### H2: behavioral pattern

$$
Q_3(t)>Q_2(t)\approx Q_1(t).
$$

### H3: falsification by leakage

If $Q_2(t)$ is high, then either:

1. the data leaks $Z$ into $Y_1,Y_2$;
2. the model uses a shortcut;
3. the first-informative-horizon mechanism is incomplete.

---

## Core theorem instantiated at K=3

For $K=1$ or $K=2$, a $Z$-blind $h_T$ can predict all active targets because $Y_1,Y_2$ are shared.

For $K=3$, if

$$
\mathbb E[-\log q_3(S_Z\mid h_T)]\le\varepsilon,
$$

then

$$
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

Therefore K=3 has a direct semantic representation requirement that K=1 and K=2 do not have in this distribution.

---

## Pass criteria

Strong support if:

1. K=3 reaches semantic threshold, K=1 and K=2 do not;
2. or K=3 reaches threshold much earlier than K=1/K=2;
3. local $Y_1,Y_2$ losses remain matched;
4. branch-swap succeeds only for K=3;
5. noisy and redundant controls do not show the same pattern.

---

## Fail criteria

The NextK story is weakened if:

1. K=2 performs like K=3 in the $\tau=3$ task;
2. K=3 fails to recover $Z$ even when the task is realizable;
3. all conditions recover $Z$ equally fast;
4. gains appear only in branch probe but not in informative-horizon prediction or branch-swap.

---

## Claim if passed

The MTP advantage is horizon-coverage dependent: the advantage appears when $K$ reaches the first future token that contains early semantic information.

---

## Claim if failed

Either the construction leaks semantic information before horizon 3, or the first-informative-horizon theory is insufficient to explain the observed learning dynamics.

