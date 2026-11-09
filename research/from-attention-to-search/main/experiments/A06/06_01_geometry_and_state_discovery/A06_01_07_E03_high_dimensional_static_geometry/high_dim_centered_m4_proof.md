---
proof_id: A07_high_dim_centered_m4_uniform_load
anchor_id: A06_2x2_expert_geometry_gate
status: proposed_proof_document
created: 2026-06-16
canonical_language: en
---

# Proof Document: Centered M4, Uniform Load, and the High-Dimensional Generalization

## Purpose

This document states exactly what can be proved after the 2D expert-geometry audit and what still requires high-dimensional experiment.

The advisor-facing need is to separate three claims:

1. raw M4 does not guarantee uniform load;
2. centered M4 gives exact 50/50 load in 2D uniform-circle input;
3. in high dimension, centering alone gives zero mean but not exact 50/50, so an additional spectral-spread or calibration argument is needed.

## 1. Setting

Let two experts be matrices

\[
A_1,A_2\in\mathbb{R}^{m\times d}.
\]

Define

\[
G_e=A_e^TA_e.
\]

Raw M4 matrix-response score:

\[
q_e(x)=x^TG_ex=\|A_ex\|^2.
\]

For two experts, the raw score difference is

\[
D(x)=q_1(x)-q_2(x)=x^THx,
\]

where

\[
H=G_1-G_2.
\]

The centered M4 score is

\[
\tilde q_e(x)=x^TG_ex-\frac{1}{d}\mathrm{tr}(G_e).
\]

The centered score difference is

\[
\tilde D(x)=\tilde q_1(x)-\tilde q_2(x)=x^TH_0x,
\]

where

\[
H_0=H-\frac{1}{d}\mathrm{tr}(H)I.
\]

By construction,

\[
\mathrm{tr}(H_0)=0.
\]

The routing rule assigns expert 1 when the score difference is positive and expert 2 when it is negative.

## 2. Raw M4 Does Not Guarantee Uniform Load

Assume `d=2` and `x=(cos theta, sin theta)` with `theta ~ Unif[0,2pi)`.

For a symmetric matrix

\[
H=\begin{pmatrix}h_{11}&h_{12}\\h_{12}&h_{22}\end{pmatrix},
\]

we have

\[
D(\theta)=h_{11}\cos^2\theta+2h_{12}\sin\theta\cos\theta+h_{22}\sin^2\theta.
\]

Using double-angle identities,

\[
D(\theta)=\mu+a\cos 2\theta+b\sin 2\theta,
\]

where

\[
\mu=\frac{1}{2}\mathrm{tr}(H),\qquad a=\frac{h_{11}-h_{22}}{2},\qquad b=h_{12}.
\]

The constant term `mu` is the average expert-energy bias. If `mu` is not zero, the positive and negative regions of `D(theta)` need not have equal measure.

For M4,

\[
\mu=\frac{1}{2}\left(\mathrm{tr}(G_1)-\mathrm{tr}(G_2)\right)=\frac{1}{2}(\|A_1\|_F^2-\|A_2\|_F^2).
\]

Random Gaussian experts do not guarantee equal Frobenius norms. Therefore raw M4 does not guarantee natural 50/50 load.

## 3. Centered M4 Gives Exact 50/50 Load in 2D

For `d=2`, centering gives a traceless symmetric matrix

\[
H_0=\begin{pmatrix}a&b\\b&-a\end{pmatrix}.
\]

Thus

\[
\tilde D(\theta)=a\cos 2\theta+b\sin 2\theta=\rho\cos(2\theta-\phi),
\]

where

\[
\rho=\sqrt{a^2+b^2}.
\]

If `rho>0`, then `2theta - phi` is uniform modulo `2pi`, so

\[
\mathbb{P}[\tilde D(\theta)>0]
=\mathbb{P}[\cos(2\theta-\phi)>0]
=\frac{1}{2}.
\]

Similarly,

\[
\mathbb{P}[\tilde D(\theta)<0]=\frac{1}{2}.
\]

Therefore centered M4 gives exact 50/50 load in the 2D uniform-circle setting whenever the centered score difference is not identically zero.

If `rho=0`, then all centered scores tie; this is the correct degeneracy mode.

## 4. Centered M4 Gives Positive Average Score Advantage in 2D

The selected-expert margin is

\[
\Delta(\theta)=|\tilde D(\theta)|.
\]

Since

\[
\tilde D(\theta)=\rho\cos(2\theta-\phi),
\]

we get

\[
\mathbb{E}\Delta(\theta)=\rho\mathbb{E}|\cos T|,
\]

with `T ~ Unif[0,2pi)`. Since

\[
\mathbb{E}|\cos T|=\frac{2}{\pi},
\]

we have

\[
\mathbb{E}\Delta(\theta)=\frac{2\rho}{\pi}.
\]

So centered M4 has positive average score advantage whenever `rho>0`.

For independent continuous random expert matrices, `rho=0` occurs with probability zero unless the model imposes identical centered response geometry.

Boundary: this is not a fixed positive lower bound. Experts can be nearly identical, making `rho` and the margin small.

## 5. High-Dimensional Centering Does Not Imply Exact 50/50

For `d>2`, centering gives

\[
\mathbb{E}_{x\sim Unif(S^{d-1})}[x^TH_0x]=\frac{1}{d}\mathrm{tr}(H_0)=0.
\]

But zero mean does not imply equal positive and negative probability.

Counterexample:

\[
H_0=\mathrm{diag}(d-1,-1,-1,\ldots,-1).
\]

This matrix is traceless. For `x ~ Unif(S^{d-1})`,

\[
x^TH_0x=(d-1)x_1^2-\sum_{i=2}^d x_i^2=dx_1^2-1.
\]

Thus expert 1 receives the input when

\[
x_1^2>\frac{1}{d}.
\]

There is no general identity forcing

\[
\mathbb{P}\left[x_1^2>\frac{1}{d}\right]=\frac{1}{2}.
\]

Therefore centered M4 does not guarantee exact 50/50 load for every fixed high-dimensional expert pair.

## 6. A High-Dimensional Approximate-Balance Lemma

Let `H_0` be any fixed symmetric traceless matrix with eigenvalues `lambda_1,...,lambda_d`.

Let

\[
x=\frac{z}{\|z\|},\qquad z\sim N(0,I_d).
\]

Since `||z||^2>0`, the sign of `x^TH_0x` equals the sign of `z^TH_0z`.

Diagonalizing `H_0`,

\[
z^TH_0z=\sum_{i=1}^d \lambda_i z_i^2.
\]

Because `sum_i lambda_i = 0`, this can be written as

\[
S=\sum_{i=1}^d \lambda_i(z_i^2-1).
\]

The summands are independent, mean-zero random variables. Their variance is

\[
\sigma^2=\mathrm{Var}(S)=2\sum_i\lambda_i^2.
\]

A Berry-Esseen bound for independent sums gives

\[
\sup_t\left|\mathbb{P}\left[\frac{S}{\sigma}\le t\right]-\Phi(t)\right|
\le C\,\frac{\sum_i |\lambda_i|^3\,\mathbb{E}|z_i^2-1|^3}{\left(2\sum_i\lambda_i^2\right)^{3/2}}.
\]

Absorbing constants into `C0`,

\[
\left|\mathbb{P}[S>0]-\frac{1}{2}\right|
\le C_0\frac{\sum_i |\lambda_i|^3}{\left(\sum_i\lambda_i^2\right)^{3/2}}.
\]

Therefore high-dimensional centered M4 is approximately balanced when

\[
r_3(H_0)=\frac{\sum_i |\lambda_i|^3}{\left(\sum_i\lambda_i^2\right)^{3/2}}
\]

is small.

Interpretation:

- If many eigen-directions contribute comparably, `r_3` is small and load should be near 50/50.
- If one or a few eigenvalues dominate, `r_3` is large and load can be far from 50/50.

This gives a testable high-dimensional proof target rather than an unconditional exact theorem.

## 7. Margin Scale in High Dimension

The same Gaussian representation gives an approximate margin scale.

For sphere input,

\[
x^TH_0x=\frac{z^TH_0z}{\|z\|^2}.
\]

When `d` is large, `||z||^2` concentrates near `d`. If the normal approximation holds,

\[
z^TH_0z \approx N(0,2\|H_0\|_F^2).
\]

Thus the selected-expert margin approximately scales as

\[
\mathbb{E}|x^TH_0x| \approx \frac{2}{\sqrt{\pi}}\frac{\|H_0\|_F}{d}.
\]

This is only a scale heuristic, not a guaranteed lower bound. Near-identical experts can still have small `||H_0||_F` and therefore small margin.

## 8. Relation to Calibration

For high dimension, centered M4 removes the sphere-average energy bias:

\[
\frac{1}{d}\mathrm{tr}(G_e).
\]

If the realized load is still imbalanced, a threshold can be fit on a calibration distribution:

\[
g_\tau(x)=\arg\max_e(q_e(x)-\tau_e).
\]

For two experts, this is equivalent to choosing a threshold on the score difference.

Calibration can force load balance, but it cannot create expert preference. The margin after calibration must therefore be reported.

## 9. Extension to More Than Two Experts

For `K>2`, define centered scores

\[
\tilde q_e(x)=x^TG_ex-c_e.
\]

Possible choices:

\[
c_e=\frac{1}{d}\mathrm{tr}(G_e)
\]

for uniform-sphere theory, or

\[
c_e=\mathbb{E}_{x\sim\mathcal{D}_{ref}}[x^TG_ex]
\]

for empirical hidden-state distributions.

However, pairwise centering does not guarantee equal `1/K` load. For `K` experts, load control usually requires thresholds or balanced assignment:

\[
g(x)=\arg\max_e(q_e(x)-\tau_e).
\]

The proof obligation becomes:

1. thresholds enforce the target load;
2. selected-expert margins remain positive;
3. assignments are stable across calibration and evaluation samples;
4. the rule still tracks expert response geometry.

## 10. What Is Proved

Can claim:

- Raw M4 does not guarantee uniform load because it includes average expert-energy bias.
- Centered M4 gives exact 50/50 load in 2D uniform-circle input when the centered difference is nonzero.
- Centered M4 gives positive 2D average margin proportional to the amplitude of the centered score difference.
- In high dimension, centering alone guarantees zero mean score difference, not exact equal-measure partition.
- Approximate high-dimensional balance follows under a spectral-spread condition measured by `r_3(H_0)`.
- Calibration is mathematically allowed, but it must be read jointly with margin.

Cannot claim:

- centered M4 gives exact 50/50 load for all high-dimensional expert pairs;
- random high-dimensional experts always have large margin;
- a trainable router will learn centered M4;
- positive M4 margin means causal task utility;
- real text hidden states satisfy uniform-sphere assumptions.

## 11. Experimental Consequence

The next experiment must not merely test whether high-dimensional features are balanced. It must test the predicted mechanism:

```text
centered/calibrated M4 should work when the centered score-difference spectrum is spread out;
it should fail or require calibration when the spectrum is spiky;
calibration is acceptable only if margin survives.
```

The minimum reported quantities are:

```text
load error;
mean margin;
low-margin fraction;
r3 spectral-spread statistic;
operator-to-Frobenius ratio;
calibrated-vs-natural comparison;
near-identical expert caveat.
```
