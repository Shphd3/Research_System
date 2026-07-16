# Initial Conditional Theory: General MTP Versus NTP

Date: 2026-07-16

Status: initial theorem package under explicit assumptions; not a universal
neural-network proof.

Chinese companion: [01_general_mtp_vs_ntp_theory_cn.md](01_general_mtp_vs_ntp_theory_cn.md)

> **Current-entry update:** this file remains background for the general
> objective and orthogonal two-mode result. The shared common-subspace
> conflict, matched information increment, curvature-corrected functional
> criterion, and meeting theme are consolidated in
> [05_theory_clarification_and_meeting_anchor.md](05_theory_clarification_and_meeting_anchor.md).

> **Scope correction:** Sections 5–6 analyze orthogonal common/rare modes.
> After the researcher defined the active failure as rare-feature absorption
> into a common-dominated shared subspace, those sections became a background
> null model rather than the current primary model. The current overlap model
> and necessary condition are in
> [04_recording_driven_low_hanging_fruit.md](04_recording_driven_low_hanging_fruit.md).

## 1. Working Object

Let $C_t=Y_{\leq t}$ be the current prefix and
$H_t=f_\theta(C_t)$ a shared hidden state. A shared-state $K$-horizon MTP
objective is

$$
\mathcal L_K(\theta,\phi_{1:K})
=
\mathbb E_t\left[
\sum_{k=1}^{K}\lambda_k
\ell\!\left(q_{\phi_k}(H_t),Y_{t+k}\right)
\right],
$$

where $\lambda_k\geq 0$. NTP is the $K=1$ case. Evaluation uses $q_{\phi_1}$
autoregressively.

This is a working abstraction, not every implementation called MTP. Sequential
prediction modules, detached branches, shared heads, different normalizations,
and speculative-decoding objectives require separate treatment.

## 2. Objective-Level Difference

Define

$$
\mathcal L_k
=
\mathbb E_t\left[
\ell\!\left(q_{\phi_k}(H_t),Y_{t+k}\right)
\right].
$$

Then

$$
\mathcal L_K=\sum_{k=1}^{K}\lambda_k\mathcal L_k.
$$

If each head is unrestricted and optimized for a fixed representation, its
minimum expected cross-entropy is

$$
\min_{\phi_k}\mathcal L_k
=H(Y_{t+k}\mid H_t).
$$

Therefore,

$$
\min_{\phi_{1:K}}\mathcal L_K
=
\sum_{k=1}^{K}\lambda_k H(Y_{t+k}\mid H_t)
=
\mathrm{constant}
-
\sum_{k=1}^{K}\lambda_k I(H_t;Y_{t+k}).
$$

Under a representation bottleneck, MTP asks $H_t$ to preserve a weighted set
of future-predictive variables, whereas NTP directly asks only for variables
predictive of $Y_{t+1}$ at that position.

Boundary: this ideal-head identity does not show that optimization reaches the
minimum, that future information is causally used, or that NTP cannot acquire
the same information through later positions and shared parameters.

## 3. Local Training-Dynamics Proposition

Let

$$
g_1=\nabla_\theta\mathcal L_1,\qquad
g_{\mathrm{aux}}=\sum_{k=2}^{K}\lambda_k\nabla_\theta\mathcal L_k.
$$

For a comparison that keeps the coefficient of $\mathcal L_1$ fixed, one MTP
step is

$$
\theta_M'=\theta-\eta(g_1+g_{\mathrm{aux}}),
$$

and the NTP step is

$$
\theta_N'=\theta-\eta g_1.
$$

A Taylor expansion of the primary NTP objective gives

$$
\mathcal L_1(\theta_M')-\mathcal L_1(\theta_N')
=
-\eta\langle g_1,g_{\mathrm{aux}}\rangle
+O(\eta^2).
$$

Thus, to first order:

- positive alignment helps the immediate NTP objective;
- negative alignment hurts it;
- orthogonality gives no immediate first-order NTP improvement, although it
  can still change the representation and future trajectory.

There is no unconditional training-speed ordering. A compute-efficiency claim
also requires a denominator such as tokens, FLOPs, or wall-clock time.

If an implementation averages active losses, the coefficient of
$\mathcal L_1$ changes. A matched shared-aux control is then required to
separate information content from active-head count, loss-term count, and
nominal scale.

## 4. Informative-Future Condition

Let $Z$ be an input-accessible latent feature that matters to a later
decision, and let $B_t$ denote the remaining nuisance context. Horizon $k$
contains incrementally new target information about $Z$ when

$$
I\!\left(
Z;Y_{t+k}
\mid B_t,Y_{t+1:t+k-1}
\right)>0.
$$

This condition permits a horizon-$k$ target to add a direct discriminative
signal for the $Z$ component of $H_t$ after earlier targets are accounted for.
Conditioning on the entire prefix would be inappropriate when $Z$ is itself a
deterministic feature of that prefix; $B_t$ explicitly excludes the candidate
feature. If $Z$ is neither present nor inferable from the input, no objective
can learn to predict it reliably. The condition is not sufficient for
standard-head use.

A11 gives controlled support for the earlier direct signal and
shared-parameter reachability. It also shows that formation is not sufficient
for a reliable later behavioral-use increment.

## 5. Target-Count Lemma for Common and Rare Events

Consider a target token at interior position $s$. Under $K$ uniformly active
horizons it appears as a target from positions
$s-1,\ldots,s-K$. Therefore, away from boundaries, both common and rare target
occurrences are repeated by the same factor.

For target class $a$, its weighted target mass is

$$
M_K(a)
=
\sum_{s:Y_s=a}
\sum_{k=1}^{\min(K,s-1)}\lambda_k.
$$

If classes have the same position distribution away from boundaries, then

$$
\frac{M_K(\mathrm{rare})}{M_K(\mathrm{common})}
\approx
\frac{N(\mathrm{rare})}{N(\mathrm{common})}.
$$

Hence standard MTP is not, by itself, a class-frequency reweighting scheme.
Any relative long-tail effect must arise from horizon-conditioned
predictability, gradient geometry, capacity allocation, boundary correlation,
or another named mechanism.

## 6. Two-Mode Relative-Learning Theorem

### 6.1 Model

Let a shared parameter $w$ have orthonormal common and rare directions
$v_c,v_r$. Write the parameter error as

$$
e=w-w^\star=e_c v_c+e_r v_r.
$$

For horizon $k$, assume the exact quadratic population loss

$$
\mathcal L_k(w)
=
\frac12 e^\top Q_k e,
$$

with

$$
Q_k=q_{k,c}v_cv_c^\top+q_{k,r}v_rv_r^\top,
\qquad q_{k,c},q_{k,r}>0.
$$

Here $q_{k,j}$ is the informative curvature for mode $j$ at horizon $k$. It
combines how often that mode appears, its feature energy, and how predictively
it enters that horizon. It is not token frequency alone.

### 6.2 Dynamics

For the weighted MTP objective,

$$
Q_M=\sum_{k=1}^{K}\lambda_kQ_k.
$$

Gradient flow obeys

$$
\dot e_c=-Q_{M,c}e_c,\qquad
\dot e_r=-Q_{M,r}e_r,
$$

where

$$
Q_{M,j}=\sum_{k=1}^{K}\lambda_kq_{k,j}.
$$

Therefore,

$$
e_j(t)=e_j(0)\exp(-Q_{M,j}t).
$$

Define the rare-to-common relative convergence ratio

$$
\rho_M
=
\frac{Q_{M,r}}{Q_{M,c}}
=
\frac{\sum_k\lambda_kq_{k,r}}
{\sum_k\lambda_kq_{k,c}}.
$$

For NTP,

$$
\rho_N=\frac{q_{1,r}}{q_{1,c}}.
$$

### 6.3 Theorem

MTP improves the rare mode's convergence rate relative to the common mode if
and only if

$$
\frac{\sum_k\lambda_kq_{k,r}}
{\sum_k\lambda_kq_{k,c}}
>
\frac{q_{1,r}}{q_{1,c}}.
$$

Equivalently,

$$
\sum_{k=2}^{K}\lambda_k
\left(q_{k,r}q_{1,c}-q_{k,c}q_{1,r}\right)>0.
$$

Proof: $\nabla\mathcal L_K=Q_Me$. Projection onto $v_c$ and $v_r$ gives the
two scalar differential equations and their exponential solutions. Since all
denominators are positive, comparing $\rho_M$ and $\rho_N$ and
cross-multiplying yields the equivalent sign condition above.

### 6.4 Consequences

1. If every horizon has the same rare/common curvature ratio, MTP does not
   change relative learning; it only rescales time.
2. If later horizons are relatively rare-enriched, MTP helps the rare mode
   relative to the common mode.
3. If later horizons are relatively common-enriched, MTP worsens the relative
   imbalance.

This is the smallest formal answer to whether standard MTP automatically
solves common/long-tail conflict: it does not.

## 7. Relation to the 0625 Two-Phase Singular-Mode Proof

The earlier rank-one proof establishes

$$
1-c(t)^2
=
\left(1-c_0^2\right)
\exp\!\left(-(\sigma(t)^2-\sigma_0^2)\right).
$$

It explains how one feature direction can align early while its gain keeps
growing. It does not identify a common mode, a rare mode, their competition,
or any MTP effect.

The two-mode theorem supplies the missing between-mode comparison. Combining
the two ideas suggests, but does not yet prove in neural networks, the
following candidate mechanism:

> A frequent mode may align early and continue to amplify; MTP changes the
> common/rare imbalance only when its additional horizons alter the relative
> informative energy or interaction of the two modes.

A07 supports the common-backbone and explicit-control mechanisms only on
controlled surfaces. It is not evidence that MTP performs that control.

## 8. Physical Interpretation

At position $t$, NTP asks the state to support one immediate conditional
prediction. MTP asks the same state to satisfy several future constraints.
Under limited capacity, this can favor a latent state that summarizes
future-coherent variables earlier.

The strongest justified intuitive statement is:

> MTP can move useful future constraints earlier in the computation.

It does not follow that MTP performs multi-step reasoning, stores the state
until it is needed, or makes the ordinary head use it.

## 9. Necessary Gates for Information-Mediated Main-Head Benefit

For a benefit specifically mediated by MTP's additional future information,
the following chain is necessary under the stated causal interpretation:

1. **Conditional novelty:** an auxiliary target carries task-relevant
   information absent from the matched next-token target.
2. **Shared reachability:** its gradient changes parameters on a path available
   to the ordinary head.
3. **State formation:** the relevant variable changes the shared state.
4. **Transport or persistence:** the change reaches the later decision state.
5. **Readout sensitivity:** the ordinary head's output function depends on the
   transported component.
6. **Target alignment:** that dependence reduces the correct test risk.
7. **Structural necessity:** if the claim is necessity rather than redundant
   use, removing the component must damage behavior after bypasses are
   controlled.

Conditional novelty is not required for a generic regularization benefit. The
chain applies to the stronger claim that additional MTP information causes the
ordinary-head gain.

## 10. Claim Boundary and Next Decision

Established under explicit assumptions:

- MTP adds horizon-specific gradients with no unconditional alignment sign.
- Standard MTP does not automatically change common/rare target frequency.
- In the two-mode quadratic model, relative tail improvement occurs exactly
  under the horizon-curvature ratio condition.

Not established:

- real neural training dynamics;
- code/planning causal benefit;
- long-context value;
- standard-head causal use;
- representation disentanglement;
- Router utility.

The previously proposed two-mode relative-learning decision is now a
background question. The active decision is the matched same-point rare-loss
one-step question in the
[Thinking Card](03_mtp_mainline_thinking_card_cn.md).
