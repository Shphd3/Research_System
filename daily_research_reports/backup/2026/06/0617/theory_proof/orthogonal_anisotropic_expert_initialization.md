# Theoretical Proposal: Orthogonal Anisotropic Expert Initialization

## researcher judgment record

当前问题：如何修改专家随机初始化，让高维均匀表征可以被 $d$ 个 experts 均匀分发？

判断：最小可证明方案是先给每个 expert 指定一个不同的正交输入主方向，再让该 expert 在这个方向上响应更强。

关键结论：如果 $x$ 来自旋转对称分布，例如 uniform sphere 或 uniform ball，并且 $d$ 个 experts 的主方向组成正交基，那么 M3 top-1 和 trace-centered M4 的静态 top-1 路由都会把空间均匀分成 $d$ 份。

最危险边界：这证明的是二次分数的静态 oracle 均分，不证明普通线性 gate 能精确实现这个二次规则。

下一步决策：先实验验证 structured expert initialization 是否在高维 uniform sphere / ball 上稳定得到低 load error 和正 margin，再决定是否用 lifted linear gate 或 paired-sign linear gate 近似它。

## Objective

This note gives a mathematically controlled expert initialization for the next
high-dimensional step.

The target is not to calibrate the router after random expert initialization.
The target is to modify expert initialization so that expert geometry itself
contains a balanced partition of a uniform representation space.

The desired property is:

$$
\Pr[g(x)=e]=\frac{1}{d},
\qquad e=1,\ldots,d,
$$

for $d$ experts and $d$-dimensional features under a rotationally symmetric
input distribution.

## Setting

There are $d$ experts and $d$-dimensional input features:

$$
x\in\mathbb{R}^d,
\qquad
e\in\{1,\ldots,d\}.
$$

The input distribution is rotationally symmetric:

$$
x\sim \mathrm{Unif}(S^{d-1})
$$

or:

$$
x\sim \mathrm{Unif}(B_d).
$$

Here $S^{d-1}$ is the unit sphere and $B_d$ is the unit ball. The proof only
uses rotational symmetry and continuity, so ties have probability zero.

Each expert is represented by an input-to-output matrix:

$$
A_e\in\mathbb{R}^{d\times d}.
$$

The M4 response matrix is:

$$
G_e=A_e^\top A_e.
$$

## Initialization Construction

Choose an orthonormal basis:

$$
u_1,\ldots,u_d,
\qquad
u_i^\top u_j=\delta_{ij}.
$$

The vector $u_e$ is the intended top input direction of expert $e$.

Choose two singular-value scales:

$$
\sigma_{\parallel}>\sigma_{\perp}>0.
$$

Initialize expert $e$ so that:

$$
G_e
=
A_e^\top A_e
=
\sigma_{\perp}^2 I
+
(\sigma_{\parallel}^2-\sigma_{\perp}^2)u_eu_e^\top.
$$

This means expert $e$ responds more strongly to the input direction $u_e$ than
to directions orthogonal to $u_e$.

One concrete way to sample $A_e$ is:

$$
A_e
=
O_e
\operatorname{diag}(s_{e,1},\ldots,s_{e,d})
Q^\top,
$$

where:

$$
Q=[u_1,\ldots,u_d],
$$

$O_e$ is a random orthogonal matrix, and:

$$
s_{e,e}=\sigma_{\parallel},
\qquad
s_{e,j}=\sigma_{\perp}\quad j\neq e.
$$

Then:

$$
A_e^\top A_e
=
Q\operatorname{diag}(s_{e,1}^2,\ldots,s_{e,d}^2)Q^\top
=
\sigma_{\perp}^2 I
+
(\sigma_{\parallel}^2-\sigma_{\perp}^2)u_eu_e^\top.
$$

This keeps random output-side orientation through $O_e$, while making the
input-side expert geometry controlled.

## Algorithm Specification

Inputs:

- feature dimension $d$;
- number of experts $E=d$;
- target average response scale $c$;
- anisotropy ratio $\rho>1$;
- random seed.

Procedure:

1. Sample or choose an orthogonal matrix $Q\in\mathbb{R}^{d\times d}$.
2. Set expert input directions $u_e=Q[:,e]$.
3. Compute $\sigma_{\perp}$ and $\sigma_{\parallel}$ from $c$ and $\rho$.
4. For each expert $e$, create singular values:

   $$
   s_{e,e}=\sigma_{\parallel},
   \qquad
   s_{e,j}=\sigma_{\perp}\quad j\neq e.
   $$

5. Sample a random orthogonal output matrix $O_e$.
6. Initialize:

   $$
   A_e=O_e\operatorname{diag}(s_{e,1},\ldots,s_{e,d})Q^\top.
   $$

Outputs:

- expert matrices $A_1,\ldots,A_d$;
- intended expert directions $u_1,\ldots,u_d$;
- response matrices $G_e=A_e^\top A_e$;
- expected oracle routing rule $g(x)=\arg\max_e(u_e^\top x)^2$.

## Rectangular Expert Extension

Real expert matrices may be rectangular:

$$
A_e\in\mathbb{R}^{h\times d}.
$$

If $h\geq d$, replace $O_e$ with a random Stiefel matrix:

$$
R_e\in\mathbb{R}^{h\times d},
\qquad
R_e^\top R_e=I_d.
$$

Then initialize:

$$
A_e
=
R_e
\operatorname{diag}(s_{e,1},\ldots,s_{e,d})
Q^\top.
$$

This still gives:

$$
A_e^\top A_e
=
Q\operatorname{diag}(s_{e,1}^2,\ldots,s_{e,d}^2)Q^\top.
$$

So the same M3/M4 routing proof applies.

If $h<d$, the expert cannot realize full-rank anisotropy over all $d$ input
directions with this construction. That case needs a separate low-rank version.

## Scale Matching To Gaussian Initialization

To keep the average response scale comparable to a standard random
initialization, choose a target average squared response $c>0$:

$$
\frac{1}{d}\mathrm{tr}(G_e)=c.
$$

Let:

$$
\rho=\frac{\sigma_{\parallel}^2}{\sigma_{\perp}^2}>1.
$$

Then choose:

$$
\sigma_{\perp}^2
=
\frac{cd}{\rho+d-1},
\qquad
\sigma_{\parallel}^2
=
\frac{\rho cd}{\rho+d-1}.
$$

The parameter $\rho$ controls how strongly each expert prefers its assigned
input direction.

## M4 Score And Equivalent Routing Rule

Raw M4 score is:

$$
q_e^{raw}(x)
=
x^\top G_ex.
$$

Substituting the proposed $G_e$ gives:

$$
q_e^{raw}(x)
=
\sigma_{\perp}^2\|x\|^2
+
(\sigma_{\parallel}^2-\sigma_{\perp}^2)(u_e^\top x)^2.
$$

The first term is identical for all experts. Therefore:

$$
\arg\max_e q_e^{raw}(x)
=
\arg\max_e (u_e^\top x)^2.
$$

Trace-centered M4 gives the same top-1 routing. Since:

$$
\mathrm{tr}(G_e)
=
(d-1)\sigma_{\perp}^2+\sigma_{\parallel}^2,
$$

define:

$$
\widetilde G_e
=
G_e-\frac{1}{d}\mathrm{tr}(G_e)I.
$$

Then:

$$
x^\top\widetilde G_ex
=
(\sigma_{\parallel}^2-\sigma_{\perp}^2)
\left((u_e^\top x)^2-\frac{1}{d}\|x\|^2\right).
$$

The term $-\|x\|^2/d$ is also identical for all experts, so:

$$
\arg\max_e x^\top\widetilde G_ex
=
\arg\max_e (u_e^\top x)^2.
$$

## M3 Top-1 Score

Under this initialization, the top input singular direction of expert $e$ is
$u_e$. Therefore M3 top-1 uses:

$$
q_e^{M3}(x)=(u_e^\top x)^2.
$$

So M3 top-1 and trace-centered M4 induce the same top-1 routing rule:

$$
g(x)=\arg\max_e (u_e^\top x)^2.
$$

The difference is score scale. M4 keeps the anisotropy strength:

$$
\sigma_{\parallel}^2-\sigma_{\perp}^2,
$$

while M3 top-1 keeps only the direction.

## Balanced-Load Theorem

Let:

$$
x\sim\mathrm{Unif}(S^{d-1})
$$

or:

$$
x\sim\mathrm{Unif}(B_d).
$$

Let $u_1,\ldots,u_d$ be an orthonormal basis and define:

$$
g(x)=\arg\max_{e\in\{1,\ldots,d\}}(u_e^\top x)^2.
$$

Then:

$$
\Pr[g(x)=e]=\frac{1}{d}
$$

for every expert $e$.

## Proof

Let:

$$
y=Q^\top x,
\qquad
Q=[u_1,\ldots,u_d].
$$

Because $x$ is rotationally symmetric and $Q$ is orthogonal, $y$ has the same
distributional symmetry as $x$.

The routing rule becomes:

$$
g(x)=\arg\max_e y_e^2.
$$

The random variables:

$$
y_1^2,\ldots,y_d^2
$$

are exchangeable. That means permuting their indices does not change their
joint distribution.

Since the distribution is continuous, ties have probability zero. Therefore
the events:

$$
\{y_e^2=\max_j y_j^2\},
\qquad
e=1,\ldots,d,
$$

are disjoint, cover probability one, and have equal probability by
exchangeability.

Thus each event has probability:

$$
\frac{1}{d}.
$$

Therefore:

$$
\Pr[g(x)=e]=\frac{1}{d}.
$$

This proves exact balanced load in the population limit.

## Margin

For M4, the selected-expert margin against the runner-up is:

$$
\Delta_{M4}(x)
=
(\sigma_{\parallel}^2-\sigma_{\perp}^2)
\left(
\max_e (u_e^\top x)^2
-
\max_{j\neq g(x)}(u_j^\top x)^2
\right).
$$

For M3 top-1, the same expression holds without the multiplicative factor:

$$
\Delta_{M3}(x)
=
\max_e (u_e^\top x)^2
-
\max_{j\neq g(x)}(u_j^\top x)^2.
$$

The margin is positive almost everywhere, but it may shrink as $d$ grows
because the largest coordinate energies can become close. Therefore high
dimension should be judged by both load error and margin, not by load alone.

Increasing $\rho$ increases the M4 score margin without changing the top-1
partition.

## Relation To Linear Gating

This construction gives a clean expert-side geometry and a clean quadratic
oracle rule:

$$
g(x)=\arg\max_e (u_e^\top x)^2.
$$

A standard linear gate:

$$
\ell_e(x)=w_e^\top x
$$

cannot exactly represent this sign-invariant quadratic rule, because:

$$
(u_e^\top x)^2
$$

treats $u_e$ and $-u_e$ as the same direction, while $w_e^\top x$ changes sign.

There are three minimal options for the next router construction:

1. Lifted linear gate. Use features $\phi(x)$ containing coordinate squares or
   low-rank quadratic features, then set:

   $$
   \ell_e(\phi(x))=\phi(x)^\top \phi(u_e)
   $$

   or directly initialize the lifted weight to represent $u_eu_e^\top$.

2. Paired-sign linear gate. Use two signed routes per geometric direction,
   $+u_e$ and $-u_e$, then merge their loads or outputs into expert $e$.

3. Plain linear baseline. Set $w_e=u_e$. This also gives balanced load by
   exchangeability, but it selects the largest signed coordinate, not the
   largest response energy. It is therefore a load baseline, not an exact
   M3/M4 implementation.

The immediate theory result supports the expert initialization. It does not yet
solve the linear-router implementation problem.

## Minimal Experiment Contract

Test two expert initializations:

- random Gaussian experts;
- orthogonal anisotropic experts from this note.

Test two input distributions:

- uniform sphere;
- uniform ball.

Evaluate these static routing scores:

- M3 top-1: $q_e(x)=(u_e^\top x)^2$;
- raw M4: $q_e(x)=x^\top G_ex$;
- trace-centered M4: $q_e(x)=x^\top(G_e-\mathrm{tr}(G_e)I/d)x$;
- plain linear baseline: $\ell_e(x)=u_e^\top x$;
- optional lifted linear gate implementing $u_eu_e^\top$.

Primary metric:

$$
\max_e\left|\widehat p_e-\frac{1}{d}\right|.
$$

This measures whether routing is actually balanced.

Secondary metrics:

- mean selected-vs-runner-up margin;
- low-margin fraction;
- tie or near-tie rate;
- agreement with the M3/M4 oracle;
- sensitivity to $\rho$ and $d$.

Expected result:

- structured experts plus M3/M4 should have near-zero load error in the
  large-sample limit;
- random Gaussian experts should not guarantee equal load for every seed;
- plain linear gate may balance load but should disagree with the quadratic
  M3/M4 oracle on sign-flipped regions;
- lifted linear gate should recover the quadratic oracle if the lifted features
  are implemented correctly.

## Falsifiable Claim

For $d$ experts and $d$-dimensional rotationally symmetric features, the
orthogonal anisotropic initialization guarantees population-level balanced
load under M3 top-1 and trace-centered M4:

$$
\Pr[g(x)=e]=\frac{1}{d}.
$$

The claim is falsified if, with enough samples and no implementation bug,
M3 top-1 or trace-centered M4 under this initialization shows persistent load
error away from zero on uniform sphere or uniform ball inputs.

## Claim Boundary

This proposal proves a static geometric routing property under a controlled
expert initialization. It does not prove semantic specialization, downstream
task utility, training stability, or exact implementability by an ordinary
linear gate.

The proof assumes:

- the number of experts equals the feature dimension;
- the input distribution is rotationally symmetric;
- the expert top input directions form an orthonormal basis;
- ties have probability zero;
- the router can evaluate the M3/M4 quadratic score, or an equivalent lifted
  representation.

If the number of experts differs from $d$, the orthonormal-basis construction
is no longer the exact object. A regular simplex or a transitive spherical
frame may give an analogous symmetry proof, but that is a separate next step.
