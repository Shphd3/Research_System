---
anchor_id: 15_05_low_variance_route_stability
parent_line: 15_linear_gate_spectral_training_bias
status: completed_weak_pass_delay_strong_fail
canonical_language: en
thinking_card: 15_05_low_variance_route_stability_thinking_card_cn.md
created: 2026-07-31
---

# A15_05: Is Low-Variance Routing Random-Like Or Merely Delayed?

## 1. Problem Definition

Route stability is often measured by low assignment churn, but a random Gate
can be persistently wrong. The decision question is therefore functional:

> When the same learnable label is encoded at matched standardized SNR in
> equal-dimensional H/M/T blocks, does the native low-variance tail fail to
> become both correct and persistent like a label-free random basis, or does it
> only require more optimization time?

## 2. Physical Priors

1. Raw SGD updates scale with input amplitude, so low-variance coordinates can
   take longer to override a fixed random initialization.
2. Low variance does not remove label information when standardized SNR is
   held fixed.
3. Assignment churn alone is ambiguous: stable-wrong and stable-correct routes
   have different functional meanings.
4. Equalizing band energy should remove a variance-induced timing difference
   but cannot rescue a label-free random control.

## 3. Falsifiable Hypotheses

**H1-strong, random-like tail.** At the registered horizon, native tail does
not reach functional stability and is not materially better than its
label-free matched random control, while equal-energy tail does reach it.

**H1-weak, finite-time delay.** Native H, M, and T all eventually reach the
same correct stable partition, but $T_{FS,H}<T_{FS,M}<T_{FS,T}$ and energy
equalization contracts the gap.

**Strongest rival.** Apparent tail drift is an artifact of measuring flips
before accuracy or of using unmatched signal strength. Once correctness and
standardized SNR are controlled, tail is slower but not random-like.

## 4. Mathematical Model

For balanced $z\in\{-1,+1\}$, each 8-D block independently encodes the same
label:

$$
x_b=s_b(zv_b+\sigma\epsilon_b),\qquad(s_H,s_M,s_T)=(4,2,1).
$$

Each band trains an equal-capacity binary linear Gate from the same random
initialization distribution. Equal-energy controls multiply M and T to the H
amplitude. Matched random controls replace $zv_b$ with label-independent
noise while retaining dimension and scale.

On a fixed held-out panel, let $A_b(k)$ be accuracy and $F_b(k)$ the fraction
of predictions that changed since the previous evaluation. Functional
stability time is

$$
T_{FS,b}=\min\{k: A_b\ge0.90\ \land\ F_b\le0.02
\text{ for three consecutive evaluations}\}.
$$

The unit is optimizer steps. No crossing by the registered horizon is right-
censored rather than assigned an invented numeric value.

## 5. Computational Realization

Generate paired online minibatches and a fixed held-out panel. Train native H,
M,T Gates; equal-energy H,M,T Gates; and label-free random controls with the
same optimizer, batch size, initialization norm, evaluation cadence, and
horizon. Formal seeds run independently over one 8-GPU node and are merged
only after rank-local completeness checks.

## 6. Minimal Falsification Tests

1. **Learnability guard:** equal-energy H/M/T must exceed 0.90 held-out
   accuracy and reach functional stability.
2. **Random guard:** label-free controls must remain near chance and must not
   pass functional stability.
3. **Native ordering:** estimate paired $T_{FS}$ contrasts H--M--T and their
   seed uncertainty.
4. **Equalization test:** compare native and equal-energy T for time to
   functional stability.
5. **Long-horizon guard:** if native T crosses later, report delay rather than
   randomization.

## 7. Current Evidence

A15_00_E03-S showed that controlled covariance ratios change finite-time Gate
learning speed and that equalization restores the ordering. Existing A15
experiments did not measure whether a band-specific route was both correct and
persistent, nor did they compare native tail against a label-free random
control under matched standardized SNR. The present anchor owns that missing
functional-stability distinction.

The associated E01 Protocol is researcher-preauthorized for implementation and
full execution on 2026-07-31.

E01 completed all 32 formal seeds. Native H/M/T all reached functional
stability in 32/32 seeds, with restricted mean times 552, 912, and 1,938 steps.
Equal-energy T required 615 steps, a 68.3% reduction from native T. Random
H/M/T had zero false crossings and final accuracy near 0.50. Native T final
accuracy was 0.953 and every seed crossed by step 2,460. Thus the strong
random-like conjecture failed and the finite-time delay conjecture passed.

## 8. Claim Boundary And Next Decision

The result supports variance-induced delay and rejects random-like tail under
the registered matched-SNR linear system. It does not prove semantic stability,
real-DCLM convergence, or expert-training utility.

**Exactly one next decision:** use correctness plus persistence as the
stability axis in a controlled four-layer layer×band portrait. Completion
requires a known layer-specific latent target; without it, route churn remains
ambiguous.
