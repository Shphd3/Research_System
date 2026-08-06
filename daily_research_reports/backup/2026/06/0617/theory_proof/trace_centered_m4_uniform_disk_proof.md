# Theoretical Analysis: Trace-Centered M4 Separability On The Uniform Disk

## Objective

This note proves the two-dimensional statement needed for the current meeting:

For two $2\times2$ experts and features uniformly distributed in the unit disk,
the trace-centered M4 score can split the disk into two equal-area routing
regions, as long as the two experts have a nonzero directional difference.

The same symmetry argument also proves that M3 top-1 projection can split the
uniform disk into two equal-area routing regions when the two experts' top input
singular directions are not the same line.

The result explains why the A06_E02 uniform-disk experiment still gives nearly
50/50 load for both trace-centered M4 and M3 top-1, while the score margin
becomes smaller than on the unit circle.

## Plain-Language Picture

In the earlier random-centroid theory note, each expert owns an interval on the
circle. Random center placement can make those intervals unequal.

Here the routing rule is different. We do not assign by random expert centers.
Each expert is a $2\times2$ matrix $A_e$, and the score asks:

How strongly does this expert matrix respond to input direction $x$?

Raw M4 uses:

$$
q_e^{raw}(x)=x^\top A_e^\top A_ex.
$$

Raw M4 can be biased if one expert has larger average response energy. So we
remove each expert's average isotropic energy and use trace-centered M4:

$$
q_e(x)
=
x^\top\left(G_e-\frac{1}{2}\mathrm{tr}(G_e)I\right)x,
\qquad
G_e=A_e^\top A_e.
$$

The key geometric fact is simple:

For two-dimensional trace-centered quadratic scores, the score difference
changes sign when the input direction rotates by 90 degrees.

Therefore the positive-score region and negative-score region occupy equal
angle mass. On a uniform disk, radius only scales the score by $r^2$; it does
not change which expert wins.

## Objects

There are two experts:

$$
A_1,A_2\in\mathbb{R}^{2\times2}.
$$

Define:

$$
G_e=A_e^\top A_e.
$$

The trace-centered expert matrix is:

$$
\widetilde G_e
=
G_e-\frac{1}{2}\mathrm{tr}(G_e)I.
$$

The routing score is:

$$
q_e(x)=x^\top \widetilde G_ex.
$$

The top-1 routing rule is:

$$
g(x)=\arg\max_{e\in\{1,2\}}q_e(x).
$$

Expert 1 receives $x$ when:

$$
D(x)=q_1(x)-q_2(x)>0.
$$

Expert 2 receives $x$ when:

$$
D(x)<0.
$$

Ties are a measure-zero boundary and do not affect the continuous load.

## Input Distribution

The feature is uniformly distributed in the unit disk:

$$
x\sim\mathrm{Unif}(B_2),
\qquad
B_2=\{x\in\mathbb{R}^2:\|x\|\leq 1\}.
$$

Write the input in polar form:

$$
x=r
\begin{bmatrix}
\cos\theta\\
\sin\theta
\end{bmatrix},
\qquad
r\in[0,1],
\quad
\theta\in[0,2\pi).
$$

For the uniform disk:

$$
\theta\sim\mathrm{Unif}[0,2\pi),
$$

and:

$$
\mathbb{E}[r^2]=\frac{1}{2}.
$$

The important point is that $r$ and $\theta$ are independent, and $\theta$ is
uniform.

## Implementation-To-Theory Mapping

The A06_E02 experiment uses the same objects as this proof.

| Theory object | Meaning | Experiment object |
| --- | --- | --- |
| $A_e$ | expert matrix | generated $2\times2$ expert |
| $G_e=A_e^\top A_e$ | raw M4 response matrix | `G_e` in the score computation |
| $\widetilde G_e=G_e-\mathrm{tr}(G_e)I/2$ | trace-centered M4 matrix | `M4_trace_centered` |
| $q_e(x)=x^\top\widetilde G_ex$ | expert score | per-token score |
| $q_e^{M3}(x)=(v_{e,1}^\top x)^2$ | M3 top-1 projection score | `M3_top1_projection` |
| $g(x)=\arg\max_e q_e(x)$ | selected expert | top-1 assignment |
| $\Pr(g(x)=1)$ | true load of expert 1 | measured load over disk samples |
| $\mathbb{E}[|q_1(x)-q_2(x)|]$ | mean score margin | `mean_margin` |

## Theorem

Let $x\sim\mathrm{Unif}(B_2)$ and define trace-centered M4 scores:

$$
q_e(x)=x^\top\left(G_e-\frac{1}{2}\mathrm{tr}(G_e)I\right)x.
$$

Let:

$$
H
=
\widetilde G_1-\widetilde G_2.
$$

If $H\neq 0$, then the routing rule:

$$
g(x)=
\begin{cases}
1, & x^\top Hx>0,\\
2, & x^\top Hx<0
\end{cases}
$$

assigns exactly half of the disk area to each expert:

$$
\Pr(g(x)=1)=\Pr(g(x)=2)=\frac{1}{2}.
$$

The margin is positive almost everywhere:

$$
|q_1(x)-q_2(x)|>0
$$

except on the decision boundary.

## Proof

Because each $\widetilde G_e$ is trace-centered:

$$
\mathrm{tr}(\widetilde G_e)=0.
$$

Therefore:

$$
\mathrm{tr}(H)=0.
$$

Every two-dimensional symmetric trace-zero matrix can be written as:

$$
H=
\begin{bmatrix}
a & b\\
b & -a
\end{bmatrix}.
$$

For:

$$
x=r
\begin{bmatrix}
\cos\theta\\
\sin\theta
\end{bmatrix},
$$

the score difference is:

$$
D(x)=x^\top Hx.
$$

Substituting polar coordinates gives:

$$
D(r,\theta)
=
r^2(a\cos 2\theta+b\sin 2\theta).
$$

Let:

$$
\rho=\sqrt{a^2+b^2}.
$$

If $H\neq 0$, then $\rho>0$. There is an angle $\phi$ such that:

$$
a\cos 2\theta+b\sin 2\theta
=
\rho\cos(2\theta-\phi).
$$

So:

$$
D(r,\theta)=r^2\rho\cos(2\theta-\phi).
$$

For every $r>0$, the sign of $D(r,\theta)$ is determined only by:

$$
\cos(2\theta-\phi).
$$

Since $\theta$ is uniform on $[0,2\pi)$:

$$
\Pr[\cos(2\theta-\phi)>0]=\frac{1}{2},
$$

and:

$$
\Pr[\cos(2\theta-\phi)<0]=\frac{1}{2}.
$$

The radius factor $r^2$ is nonnegative and does not change the sign. The point
$r=0$ has zero probability under the continuous disk distribution.

Therefore:

$$
\Pr[D(x)>0]=\Pr[D(x)<0]=\frac{1}{2}.
$$

This proves exact balanced load on the uniform disk.

## Geometry Of The Decision Boundary

The decision boundary is:

$$
D(x)=x^\top Hx=0.
$$

Using:

$$
D(r,\theta)=r^2\rho\cos(2\theta-\phi),
$$

the boundary is:

$$
\cos(2\theta-\phi)=0.
$$

This gives two lines through the origin. These two lines divide the disk into
four sectors. Two opposite sectors go to expert 1, and the other two opposite
sectors go to expert 2.

The total area of expert 1's two sectors equals the total area of expert 2's
two sectors.

So the split is balanced, but it is not a single straight-line half-plane
split. It is a quadratic split.

## M3 Top-1 Projection Separability

M3 top-1 projection keeps only the first input-side singular direction of each
expert. Let:

$$
u=v_{1,1},
\qquad
v=v_{2,1},
\qquad
\|u\|=\|v\|=1.
$$

The M3 top-1 score is:

$$
q_1^{M3}(x)=(u^\top x)^2,
\qquad
q_2^{M3}(x)=(v^\top x)^2.
$$

The score difference is:

$$
D_{M3}(x)
=
q_1^{M3}(x)-q_2^{M3}(x)
=
x^\top(uu^\top-vv^\top)x.
$$

Define:

$$
H_{M3}=uu^\top-vv^\top.
$$

Because:

$$
\mathrm{tr}(uu^\top)=\mathrm{tr}(vv^\top)=1,
$$

we have:

$$
\mathrm{tr}(H_{M3})=0.
$$

So M3 top-1 does not need an extra trace-centering step: subtracting two
rank-one projection scores already removes the isotropic trace term.

Therefore $H_{M3}$ is again a two-dimensional symmetric trace-zero quadratic
form. If the two top singular directions are not the same line, meaning:

$$
uu^\top\neq vv^\top,
$$

then:

$$
H_{M3}\neq 0.
$$

So the same trace-zero proof applies:

$$
\Pr[D_{M3}(x)>0]
=
\Pr[D_{M3}(x)<0]
=
\frac{1}{2}
$$

for $x\sim\mathrm{Unif}(B_2)$.

The boundary has an especially simple form:

$$
(u^\top x)^2=(v^\top x)^2.
$$

Equivalently:

$$
((u-v)^\top x)((u+v)^\top x)=0.
$$

So M3 top-1 also produces two decision lines through the origin. These two
lines split the disk into four sectors, with two opposite sectors routed to
each expert.

To see the margin explicitly, rotate coordinates so:

$$
u=
\begin{bmatrix}
1\\
0
\end{bmatrix},
\qquad
v=
\begin{bmatrix}
\cos\alpha\\
\sin\alpha
\end{bmatrix}.
$$

Here $\alpha$ is the angle between the two top singular direction lines, and
the non-degenerate case is $\sin\alpha\neq 0$. For:

$$
x=r
\begin{bmatrix}
\cos\theta\\
\sin\theta
\end{bmatrix},
$$

we get:

$$
D_{M3}(r,\theta)
=
r^2\left(\cos^2\theta-\cos^2(\theta-\alpha)\right)
=
-r^2\sin\alpha\sin(2\theta-\alpha).
$$

Thus:

$$
\Delta_{M3}(x)=|D_{M3}(x)|
=
r^2|\sin\alpha||\sin(2\theta-\alpha)|.
$$

On the unit circle:

$$
\mathbb{E}_{S^1}[\Delta_{M3}]
=
\frac{2|\sin\alpha|}{\pi}.
$$

On the uniform disk:

$$
\mathbb{E}_{B_2}[\Delta_{M3}]
=
\frac{|\sin\alpha|}{\pi}
=
\frac{1}{2}\mathbb{E}_{S^1}[\Delta_{M3}].
$$

This proves that M3 top-1 can also give exact balanced load on the uniform disk
when the two top singular directions are distinct.

The claim is weaker than the M4 claim. M3 top-1 only uses one direction per
expert and ignores singular-value scale and secondary directions. It can
therefore match M4 on balanced load while giving a smaller score margin.

## Why The Margin Is Smaller Than On The Unit Circle

The selected-expert margin is:

$$
\Delta(x)=|D(x)|
=
r^2\rho|\cos(2\theta-\phi)|.
$$

For the unit circle, $r=1$, so:

$$
\mathbb{E}_{S^1}[\Delta]
=
\rho\mathbb{E}[|\cos(2\theta-\phi)|].
$$

Because:

$$
\mathbb{E}[|\cos(2\theta-\phi)|]=\frac{2}{\pi},
$$

we get:

$$
\mathbb{E}_{S^1}[\Delta]
=
\frac{2\rho}{\pi}.
$$

For the uniform disk:

$$
\Delta(x)=r^2\rho|\cos(2\theta-\phi)|.
$$

Since $r$ and $\theta$ are independent:

$$
\mathbb{E}_{B_2}[\Delta]
=
\mathbb{E}[r^2]\rho\mathbb{E}[|\cos(2\theta-\phi)|].
$$

Using:

$$
\mathbb{E}[r^2]=\frac{1}{2},
$$

we get:

$$
\mathbb{E}_{B_2}[\Delta]
=
\frac{1}{2}\cdot\frac{2\rho}{\pi}
=
\frac{\rho}{\pi}.
$$

Therefore:

$$
\mathbb{E}_{B_2}[\Delta]
=
\frac{1}{2}\mathbb{E}_{S^1}[\Delta].
$$

This is the reason the uniform disk keeps balanced load but has weaker margin.

## Why Raw M4 Does Not Have The Same Guarantee

Raw M4 uses:

$$
q_e^{raw}(x)=x^\top G_ex.
$$

The raw score difference is:

$$
D_{raw}(x)=x^\top(G_1-G_2)x.
$$

In two dimensions, this can be decomposed into:

$$
D_{raw}(r,\theta)
=
r^2\left(\mu+\rho\cos(2\theta-\phi)\right),
$$

where:

$$
\mu=\frac{1}{2}\mathrm{tr}(G_1-G_2).
$$

The term $\mu$ is the average response-energy bias between the two experts.
If $\mu\neq 0$, then the positive and negative angular regions are not
generally equal.

Trace-centering removes this bias:

$$
G_e
\mapsto
G_e-\frac{1}{2}\mathrm{tr}(G_e)I.
$$

After this operation, $\mu=0$, so only the directional expert difference
remains.

## Connection To A06_E02 Results

In A06_E02, for the non-degenerate anisotropic conditions C3 and C5, the
uniform-disk result for trace-centered M4 was:

| Distribution | Method | Load error | Mean margin |
| --- | --- | ---: | ---: |
| unit circle | trace-centered M4 | 0.0000 | 1.9315 |
| uniform disk | trace-centered M4 | 0.0030 | 0.9702 |

The small nonzero load error comes from finite sampling. The theoretical value
is exactly zero.

The margin ratio is:

$$
\frac{0.9702}{1.9315}\approx 0.50,
$$

which matches the proof prediction:

$$
\mathbb{E}_{B_2}[\Delta]
=
\frac{1}{2}\mathbb{E}_{S^1}[\Delta].
$$

M3 top-1 had the same balanced-load behavior but a smaller score margin:

| Distribution | Method | Load error | Mean margin |
| --- | --- | ---: | ---: |
| uniform disk | M3 top-1 projection | 0.0030 | 0.2587 |
| uniform disk | trace-centered M4 | 0.0030 | 0.9702 |

This matches the theory: both scores are trace-zero quadratic separators in 2D,
so both can balance the disk. The difference is that M3 top-1 is a low-rank
directional proxy, while trace-centered M4 uses the full centered matrix
response, so M4 can produce a clearer score advantage.

For random unconstrained experts C1, the uniform-disk load errors were:

| Method | Uniform-disk load error |
| --- | ---: |
| raw M4 | 0.2544 |
| trace-centered M4 | 0.0027 |
| distribution-centered M4 | 0.0896 |

This supports the theoretical distinction:

- raw M4 keeps average expert-energy bias;
- trace-centered M4 removes the bias in the correct homogeneous quadratic way;
- distribution-centered M4 is not the same proof object when radius varies.

## Falsifiable Conjecture

For uniform-disk features in 2D, trace-centered M4 should produce exact 50/50
load in the infinite-sample limit whenever:

$$
H=\widetilde G_1-\widetilde G_2\neq 0.
$$

It should fail as a strong specialization signal when:

$$
H\approx 0,
$$

because then the margin is small even if the load is balanced.

The conjecture predicts:

- increasing token count should reduce measured load error toward zero;
- increasing token count should not increase the true margin;
- near-identical experts should remain low-margin cases;
- raw M4 should remain load-biased when the two experts have different trace.

## Implementation Contract

To test this proof against simulations, record:

- input distribution: uniform disk;
- expert matrices $A_1,A_2$;
- trace-centered matrices $\widetilde G_1,\widetilde G_2$;
- score difference $D(x)=x^\top(\widetilde G_1-\widetilde G_2)x$;
- if testing M3 top-1, top singular directions $v_{1,1},v_{2,1}$ and score
  difference $D_{M3}(x)=x^\top(v_{1,1}v_{1,1}^\top-v_{2,1}v_{2,1}^\top)x$;
- measured load:

$$
\widehat p_1=\Pr_{\text{sample}}[D(x)>0];
$$

- measured load error:

$$
|\widehat p_1-1/2|;
$$

- measured mean margin:

$$
\frac{1}{n}\sum_i |D(x_i)|.
$$

Pass condition:

- load error approaches zero as sample count increases;
- mean margin is positive for non-degenerate experts;
- disk mean margin is about half of the unit-circle mean margin for the same expert pair;
- M3 top-1 has balanced load when $v_{1,1}v_{1,1}^\top\neq v_{2,1}v_{2,1}^\top$,
  but may have smaller margin than trace-centered M4.

Fail condition:

- trace-centered M4 keeps nonzero load imbalance on uniform disk as sample count grows;
- raw M4 and trace-centered M4 show no difference under trace-imbalanced experts;
- M3 top-1 shows persistent load imbalance despite distinct top singular direction lines;
- near-identical experts show high confidence despite small $\|H\|$.

## Claim Boundary

This proof applies to two experts, two-dimensional inputs, uniform-disk
features, and trace-centered M4 routing. The M3 top-1 extension applies when
the two top input singular directions are distinct lines. The proof establishes
static oracle separability and balanced load under the stated symmetry. It does
not prove that M3 is better than M4, that a trainable linear gate can learn
these quadratic rules, that the same result holds in high dimension without
extra assumptions, or that balanced routing implies semantic expert
specialization.
