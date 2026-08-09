---
anchor_id: 15_01_01_selected_expert_feedback_lockin
legacy_anchor_id: 15_04_expert_feedback_tail_lockin
parent_anchor: 15_01_spectral_learning_and_feedback_dynamics
status: completed_pass_feedback_lockin
canonical_language: en
thinking_card: 15_01_01_selected_expert_feedback_lockin_thinking_card_cn.md
created: 2026-07-31
---

# A15_01_01: Does Selected-Expert Feedback Lock In Head-First Routing?

## 1. Problem Definition

A linear Gate learns high-variance head coordinates sooner. The unresolved
question is whether subsequent selected-expert training creates an incumbent
utility advantage that prevents useful middle/tail (M/T) variables from
correcting the early coarse partition.

The decision question is:

> With H/M/T all required by construction for the loss-optimal expert, does
> selected-only expert training reduce later M/T route correction relative to
> equal-compute oracle-functional expert coverage?

This anchor tests a feedback mechanism in a controlled MoE. It does not test
whether covariance M/T is useful in DCLM; A15_05 did not certify that claim.

## 2. Physical Priors

1. Under anisotropic covariance, a linear Gate learns high-variance
   coordinates sooner.
2. Top-1 selection gives chosen experts more task-specific updates than
   unchosen challengers.
3. A chosen expert can become a locally better action even when the original
   partition omits a target-relevant variable.
4. If this feedback matters, changing expert update coverage while holding
   Router observations and active update count fixed should change M/T
   correction.

## 3. Falsifiable Hypotheses

**H1, feedback lock-in.** Selected-only expert updates create incumbent
advantage and challenger starvation. Oracle-functional coverage restores the
relative utility of the correct fine expert and increases held-out M/T route
correction.

**Strongest rival, variance-only delay.** M/T correction is determined by Gate
input variance and optimization time. Expert update coverage does not produce
a material paired-seed difference once Router input, initialization, data,
optimizer, and active expert updates are matched.

**Additional rivals.** The M/T signal may be unreadable; the expert task may
not require specialization; or an apparent gain may come from extra expert
compute. Known-good signal and expert-function controls plus one-update-per-
token accounting address these alternatives.

## 4. Mathematical Model

Let independent balanced bits be $h,m,t\in\{-1,+1\}$ and define the
loss-optimal expert

$$
e^*(h,m,t)=4\mathbf 1[h=+1]+2\mathbf 1[m=+1]+\mathbf 1[t=+1].
$$

Each equal-dimensional band encodes one necessary bit:

$$
x_b=s_b\left(bv_b+\sigma\epsilon_b\right),\qquad
(s_H,s_M,s_T)=(4,2,1),
$$

where the standardized signal-to-noise ratio is identical across bands. A
payload $p$ has target $y=A_{e^*}p$, with distinct fixed maps $A_e$. Expert
$e$ learns $W_ep$. The stochastic top-1 Router samples
$a\sim\operatorname{softmax}(Wx)$ and receives only the selected loss
$\ell_a=\|W_ap-y\|_2^2$.

The two causal arms differ only in the expert update recipient:

$$
a_{\mathrm{update}}=
\begin{cases}
a,&\text{selected-only},\\
e^*,&\text{oracle-functional coverage}.
\end{cases}
$$

Both execute exactly one expert update per token. The primary outcome is fine
correction accuracy,

$$
C_{MT}=\tfrac12\left[
\Pr(\hat m=m\mid\hat h=h)+
\Pr(\hat t=t\mid\hat h=h)
\right].
$$

## 5. Computational Realization

Use a minimal synthetic eight-expert MoE with a 24-dimensional Router input
(three 8-D bands), linear stochastic Gate, and eight trainable linear experts.
The same generated minibatches, initial Gate, expert initialization, policy
optimizer, entropy schedule, and training horizon are paired across arms.
Formal seeds are distributed over one 8-GPU node; each GPU owns complete,
independent seeds and writes rank-local evidence before deterministic merge.

The initial Gate encodes the head bit and favors one incumbent in each head
half, creating the registered early coarse partition without using M/T.

## 6. Minimal Falsification Tests

1. **Signal gate:** supervised routing from H/M/T must recover $e^*$ on held-
   out data; otherwise the task is not informative.
2. **Expert-function gate:** fixed oracle experts must make $e^*$ the unique
   held-out loss minimizer.
3. **Matched feedback test:** compare selected-only and oracle-functional
   coverage with one expert update per token in both arms.
4. **Mechanism audit:** measure correct-challenger update share and the loss
   advantage of the incumbent over the correct challenger.
5. **Variance rival:** keep the identical anisotropic Router input in both
   causal arms; a coverage effect therefore cannot be attributed to changed
   band variance.

## 7. Current Evidence

A15_00 established that the actual trained Gate responds much more strongly
to covariance head directions, while A15_00_E03-S established a controlled
causal effect of variance on finite-time learning speed. A15_05 found no
stable DCLM compatibility increment for fixed covariance M/T bands. These
results motivate a controlled sufficiency test in which M/T utility is known
by construction; none establishes selected-expert feedback lock-in.

The associated E01 Protocol is researcher-preauthorized for implementation and
full execution on 2026-07-31.

E01 completed on 32 paired formal seeds. Selected-only training ended at
median $C_{MT}=0.500$, while oracle-functional coverage reached 0.977. The
paired median effect was +0.477 with 95% interval [0.476,0.479]. M and T
component effects were both about +0.477. All 32 seeds passed compute,
readability, bandit-feedback, and initial-head guards; all 32 also showed the
registered early incumbent-better/challenger-starved direction. The formal
8×5090 job `pt-15rmvipu` succeeded.

## 8. Claim Boundary And Next Decision

The result establishes that selected-expert co-adaptation is sufficient to
lock in a head-first partition in this controlled system. It does not show
that the mechanism explains a real DCLM checkpoint, that natural M/T bands are
useful, or that oracle coverage is deployable.

**Exactly one next decision:** test whether sparse challenger or counterfactual
coverage breaks the same loop in a four-layer controlled hierarchy with known
layer-specific latent variables. Completion requires matched compute,
layerwise functional targets, and held-out task loss rather than route recovery
alone.
