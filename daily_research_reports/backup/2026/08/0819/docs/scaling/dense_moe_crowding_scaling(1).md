# Unified Effective Crowding Bounds for Dense Width and MoE Routing



## Background

Modern neural representations often contain far more latent features than the dimensionality of the representation space, i.e., $F \gg d$. As a result, distinct features cannot all occupy mutually orthogonal directions and must partially share the same representational subspace, leading to feature interference or **crowding**.

We quantify this crowding through the weighted pairwise squared overlap between feature directions:

$$
C_{\mathrm{dense}}
=
\sum_{i\ne j}
w_i w_j
\langle u_i,u_j\rangle^2,
$$

where $u_i \in \mathbb{R}^d$ is the unit representation direction of feature $i$, and $w_i$ denotes its importance or frequency. A smaller value of $C$ therefore corresponds to a representation in which important features are more geometrically separable and interfere less with one another.

Given a parameter multiplier $B$, Dense scaling reduces feature crowding only by enlarging a single shared representation space, yielding $C_{\mathrm{dense}}^\star(B)=\Theta(B^{-1/2})$, whereas MoE additionally separates interfering features across experts, achieving $C_{\mathrm{moe}}^\star(B)\le O(B^{-1})$ and potentially faster scaling when the feature-interference graph is structurally partitionable.


This document gives the current self-contained theory for :

> How does feature crowding change when we spend additional parameters on dense width versus additional MoE experts?

The central object is not absolute representation quality. It is the amount of pairwise feature interference that remains active in the same computational space.

---

## 0. Main Conclusions

### 0.1 Dense Model Scaling Speed

For a dense model with representation dimension $d$, define the optimal dense crowding value:

$$
C_{\mathrm{dense}}^\star(d)
=
\min_{\|u_i\|_2=1}
\sum_{i\ne j}
w_iw_j
\langle u_i,u_j\rangle^2.
$$

Under diffuse feature weights, meaning that no small set of features dominates the total weight, the optimal value satisfies:

$$
\boxed{
C_{\mathrm{dense}}^\star(d)
=
\Theta\left(\frac{1}{d}\right)
}
$$

Dense transformer parameter count scales approximately as $P_{\mathrm{dense}}(d)\propto d^2$. Therefore, under a parameter multiplier $B$:

$$
d(B)\approx d_0\sqrt{B},
$$

so dense crowding scales as:

$$
\boxed{
C_{\mathrm{dense}}^\star(B)
=
\Theta\left(B^{-1/2}\right)
}
$$

This is the dense scaling speed predicted by the theory.

### 0.2 MoE Scaling Lower Bound on Improvement Rate

For MoE, the relevant quantity is effective crowding:

$$
C_{\mathrm{eff}}(S)
=
\sum_{i\ne j}
w_iw_jG_{ij}^2S_{ij}.
$$

Here $G_{ij}=\langle u_i,u_j\rangle$, and $S_{ij}$ is the probability that features $i$ and $j$ are processed in the same active expert space.

Under balanced assignment and specialization constraints, there exists a hard or soft assignment with:

$$
\boxed{
C_{\mathrm{moe}}^\star(E)
\le
O\left(\frac{1}{E}\right)
}
$$

Since increasing the number of experts approximately gives a parameter multiplier $B\approx E$ when active width is fixed, MoE has an achievable rate:

$$
\boxed{
C_{\mathrm{moe}}^\star(B)
\le
O\left(B^{-1}\right)
}
$$

This should be read carefully:

- It is an upper bound on the optimal crowding value.
- Equivalently, it is a lower bound on the achievable improvement rate.
- It does not say every learned router automatically reaches this rate.

### One Sentence Summary
 **Given a parameter multiplier $B$, Dense scaling reduces feature crowding only by enlarging a single shared representation space, yielding $C_{\mathrm{dense}}^\star(B)=\Theta(B^{-1/2})$, whereas MoE additionally separates interfering features across experts, achieving $C_{\mathrm{moe}}^\star(B)\le O(B^{-1})$ and potentially faster scaling when the feature-interference graph is structurally partitionable.**


### 0.3 Why MoE Has No Universal Tight Upper Speed

Dense width has a geometry-driven bottleneck: many weighted feature directions must live in one $d$-dimensional space.

MoE has an additional degree of freedom: it can decide which feature pairs should be co-routed. This depends on the real feature interference graph:

$$
I_{ij}
=
w_iw_jG_{ij}^2.
$$

If the high-interference edges of this graph are easy to cut, then graph-aware MoE routing can reduce effective crowding faster than $1/E$.

Thus there is no universal tight exponent:

$$
C_{\mathrm{moe}}^\star(E)
=
\Theta(E^{-1})
$$

without assumptions on graph partitionability. Instead, one may observe:

$$
C_{\mathrm{moe}}^\star(E)
\approx
E^{-(1+\beta)}
$$

where $\beta\ge 0$ is a property of the feature graph, not just the architecture.

In the extreme case, if the high-interference graph becomes perfectly separable across experts, the remaining same-expert interference can drop much faster than $1/E$, or even become zero for the relevant edge set.

### 0.4 Real-Data Scaling From Our Measurements

Our current data gives the following empirical slopes on log-log plots.

All empirical rates below use the parameter multiplier $B$ as the x-axis whenever dense and MoE are compared.

For dense models, we convert width to parameter multiplier by:

$$
B
=
\left(\frac{d}{128}\right)^2.
$$

For MoE models with fixed active width, we use:

$$
B
=
E.
$$

| Curve | Meaning | Frequency weights | Energy weights |
|---|---|---:|---:|
| Dense observed | dense crowding vs $B=(d/128)^2$ | $-0.440$ | $-0.402$ |
| Green line | learned-router effective MoE crowding vs $B=E$ | $-0.938$ | $-0.925$ |
| Purple line | graph-aware hard partition on the real feature graph vs $B=E$ | $-1.415$ | $-1.776$ |

Interpretation:

- Dense observed scaling is roughly $B^{-0.4}$ to $B^{-0.44}$, somewhat slower than the ideal $B^{-1/2}$ rate. This is plausibly due to finite training, finite SAE quality, and non-asymptotic model sizes.
- The learned MoE router, shown by the green line, is close to the universal $B^{-1}$ achievable rate.
- The graph-aware hard partition, shown by the purple line, is substantially faster than $B^{-1}$, which means the measured feature graph is more separable than the worst-case theory requires.
- The gap between green and purple means the learned token-level router has not fully exploited the graph partitionability visible in the SAE feature graph.

The purple line is not a formal global lower bound unless the graph partition problem is solved exactly. In our current implementation it is a greedy graph-aware feasible partition, so it is best interpreted as an empirical target curve showing available partition structure.

---

## 1. Latent Features, Weights, and Directions

Assume there are $F$ latent features.

Feature $i$ has weight:

$$
w_i\ge 0,
\qquad
\sum_{i=1}^{F}w_i=1.
$$

The weight may represent firing frequency, activation energy, loss importance, or another feature importance measure.

Feature $i$ has a unit representation direction:

$$
u_i\in\mathbb{R}^d,
\qquad
\|u_i\|_2=1.
$$

The squared overlap between two features is:

$$
G_{ij}^2
=
\langle u_i,u_j\rangle^2.
$$

The weighted pairwise interference is:

$$
I_{ij}
=
w_iw_jG_{ij}^2.
$$

We set $I_{ii}=0$ because self-overlap is not superposition between distinct features.

---

## 2. Dense Crowding

In a dense model, all features share the same active representation space. Therefore every pair can interfere:

$$
C_{\mathrm{dense}}(U)
=
\sum_{i\ne j}
w_iw_j
\langle u_i,u_j\rangle^2.
$$

The dense optimum is:

$$
C_{\mathrm{dense}}^\star(d)
=
\min_{\|u_i\|_2=1}
C_{\mathrm{dense}}(U).
$$

The question is how $C_{\mathrm{dense}}^\star(d)$ scales with dimension $d$.

---

## 3. Dense Lower Bound: Weighted Frame Potential

Define:

$$
A
=
\sum_i
w_i u_i u_i^\top.
$$

Since each $u_i$ has unit norm:

$$
\operatorname{tr}(A)
=
\sum_i w_i
=
1.
$$

The weighted frame potential is:

$$
\mathrm{FP}(U)
=
\sum_{i,j}
w_iw_j
\langle u_i,u_j\rangle^2.
$$

It can be written as:

$$
\mathrm{FP}(U)
=
\|A\|_F^2.
$$

For any positive semidefinite $d\times d$ matrix $A$:

$$
\|A\|_F^2
\ge
\frac{\operatorname{tr}(A)^2}{d}.
$$

Because $\operatorname{tr}(A)=1$:

$$
\mathrm{FP}(U)
\ge
\frac{1}{d}.
$$

But:

$$
\mathrm{FP}(U)
=
\sum_i w_i^2
+
\sum_{i\ne j}
w_iw_j
\langle u_i,u_j\rangle^2.
$$

Therefore:

$$
C_{\mathrm{dense}}(U)
\ge
\frac{1}{d}
-
\|w\|_2^2.
$$

So for every possible feature geometry:

$$
\boxed{
C_{\mathrm{dense}}^\star(d)
\ge
\max\left(
0,
\frac{1}{d}-\|w\|_2^2
\right)
}
$$

This is a true lower bound. It does not rely on random directions.

---

## 4. Dense Upper Bound: Probabilistic Method, Not A Real-Model Assumption

To prove the dense optimum is not much worse than $1/d$, we need an upper bound on the optimum.

It is enough to show that at least one deterministic configuration of directions achieves crowding at most $O(1/d)$.

We use the probabilistic method:

1. Randomly construct candidate directions.
2. Compute their expected crowding.
3. Conclude that at least one deterministic candidate achieves no more than the expectation.

This does not assume trained feature directions are random.

Let $u_i$ be independent uniformly random unit vectors in $\mathbb{R}^d$. For $i\ne j$:

$$
\mathbb{E}
\left[
\langle u_i,u_j\rangle^2
\right]
=
\frac{1}{d}.
$$

Therefore:

$$
\mathbb{E}
\left[
C_{\mathrm{dense}}(U)
\right]
=
\frac{1}{d}
\sum_{i\ne j}
w_iw_j.
$$

Since:

$$
\sum_{i\ne j}
w_iw_j
=
1-\|w\|_2^2
\le
1,
$$

we get:

$$
\mathbb{E}
\left[
C_{\mathrm{dense}}(U)
\right]
\le
\frac{1}{d}.
$$

Thus there exists at least one deterministic geometry $U$ such that:

$$
\boxed{
C_{\mathrm{dense}}^\star(d)
\le
\frac{1}{d}
}
$$

This proves achievability. It does not claim that every geometry, or every trained dense model, reaches this value.

---

## 5. Dense Rate Under Diffuse Weights

The lower bound is meaningful when $\|w\|_2^2$ is small.

Define diffuse weights by:

$$
\|w\|_2^2
\le
\frac{c}{d}
$$

for some constant $0<c<1$.

Equivalently, the effective number of important features:

$$
N_{\mathrm{eff}}
=
\frac{1}{\|w\|_2^2}
$$

satisfies:

$$
N_{\mathrm{eff}}
\ge
\frac{d}{c}.
$$

Under this condition:

$$
C_{\mathrm{dense}}^\star(d)
\ge
\frac{1-c}{d}.
$$

Together with the upper bound:

$$
C_{\mathrm{dense}}^\star(d)
\le
\frac{1}{d},
$$

we get:

$$
\boxed{
C_{\mathrm{dense}}^\star(d)
=
\Theta\left(\frac{1}{d}\right)
}
$$

For dense transformers, increasing width by a factor $a$ increases parameters by roughly $a^2$. Therefore a parameter multiplier $B$ gives $a=\sqrt{B}$, and:

$$
\boxed{
C_{\mathrm{dense}}^\star(B)
=
\Theta\left(B^{-1/2}\right)
}
$$

---

## 6. Unified MoE View: Co-Routing Matrix

MoE does not only change the geometry $G_{ij}^2$. It also changes whether two features are active in the same expert space.

Define:

$$
S_{ij}
\in
[0,1]
$$

as the probability that feature $i$ and feature $j$ are processed by the same active expert.

Then effective crowding is:

$$
C_{\mathrm{eff}}(S)
=
\sum_{i\ne j}
I_{ij}S_{ij}.
$$

Dense is the special case:

$$
S_{ij}=1
\qquad
\forall i\ne j.
$$

The ideal MoE goal is:

$$
\text{make } S_{ij} \text{ small when } I_{ij} \text{ is large.}
$$

---

## 7. Soft Assignment Formulation

Let $q_i(e)$ be the probability or fractional assignment of feature $i$ to expert $e$:

$$
q_i(e)\ge 0,
\qquad
\sum_{e=1}^{E}
q_i(e)
=
1.
$$

Collect these probabilities into:

$$
Q\in\mathbb{R}^{F\times E},
\qquad
Q_{ie}=q_i(e).
$$

Then:

$$
S_{ij}
=
\sum_{e=1}^{E}
q_i(e)q_j(e).
$$

In matrix form:

$$
S=QQ^\top.
$$

The effective crowding objective becomes:

$$
C_{\mathrm{eff}}(Q)
=
\sum_{i\ne j}
I_{ij}
(QQ^\top)_{ij}.
$$

Since $I_{ii}=0$, this is:

$$
C_{\mathrm{eff}}(Q)
=
\operatorname{Tr}(Q^\top I Q).
$$

Different models correspond to different feasible sets:

| Model | Constraint on $Q$ or $S$ |
|---|---|
| Dense | $E=1$, so $S_{ij}=1$ |
| Hard-assignment MoE | each row of $Q$ is one-hot |
| Soft-assignment MoE | each row of $Q$ lies in the simplex |
| Learned token router | $Q$ or $S$ is induced by the trained router and token distribution |

This is the unified view.

---

## 8. Why Unconstrained $S$ Is Not Meaningful

If we ignore MoE feasibility and solve:

$$
\min_{0\le S_{ij}\le 1}
\sum_{i\ne j}
I_{ij}S_{ij},
$$

the solution is:

$$
S_{ij}=0
\qquad
i\ne j.
$$

This gives zero crowding, but it is not a meaningful MoE model. It would mean every feature pair can be separated independently, which is impossible when the number of experts is far smaller than the number of feature types.

Therefore the real problem must constrain $S$ through an assignment matrix $Q$ and practical constraints such as:

- finite expert count $E\ll F$,
- load balance,
- top-$k$ routing,
- token-level routing rather than direct feature-level routing,
- limited router capacity.

---

## 9. MoE Achievable $1/E$ Bound

The simplest feasible soft assignment is uniform:

$$
q_i(e)
=
\frac{1}{E}
\qquad
\forall i,e.
$$

Then:

$$
S_{ij}
=
\sum_{e=1}^{E}
\frac{1}{E^2}
=
\frac{1}{E}.
$$

Therefore:

$$
C_{\mathrm{eff}}(Q_{\mathrm{uniform}})
=
\frac{1}{E}
\sum_{i\ne j}
I_{ij}
=
\frac{C_{\mathrm{raw}}}{E}.
$$

Since this is a feasible soft assignment:

$$
\boxed{
C_{\mathrm{soft}}^\star(E)
\le
\frac{C_{\mathrm{raw}}}{E}
}
$$

This proves a $1/E$ achievable rate for the soft-assignment feasible set.

For hard assignment, assign each feature independently and uniformly to one expert:

$$
r(i)
\sim
\operatorname{Uniform}\{1,\dots,E\}.
$$

Then:

$$
\mathbb{E}
\left[
\mathbf{1}\{r(i)=r(j)\}
\right]
=
\frac{1}{E}.
$$

So:

$$
\mathbb{E}
\left[
C_{\mathrm{hard}}(r)
\right]
=
\frac{C_{\mathrm{raw}}}{E}.
$$

By the probabilistic method, there exists a deterministic hard assignment with:

$$
\boxed{
C_{\mathrm{hard}}^\star(E)
\le
\frac{C_{\mathrm{raw}}}{E}
}
$$

Again, this is an existence proof, not a claim that learned routers are random.

With diffuse weights, random hard assignment also satisfies approximate load balance with high probability up to constant slack. Therefore the same $O(1/E)$ crowding rate remains achievable under balanced hard assignment, up to constants.

---

## 10. Why MoE Can Beat $1/E$

The $1/E$ proof ignores graph structure. It only says that random or uniform co-routing reduces pair collisions by a factor of $E$.

Graph-aware MoE can do better because it tries to cut high-interference edges:

$$
I_{ij}
=
w_iw_jG_{ij}^2.
$$

For a hard partition $r$, the objective is:

$$
C_{\mathrm{hard}}(r)
=
\sum_{i\ne j}
I_{ij}
\mathbf{1}\{r(i)=r(j)\}.
$$

This is a weighted graph partitioning objective: keep low-weight edges inside experts and cut high-weight edges across experts.

Suppose the feature graph has a partitionability exponent $\beta\ge 0$ such that graph-aware partitioning reduces the average within-expert interference intensity by:

$$
\mu_{\mathrm{within}}(E)
\propto
E^{-\beta}.
$$

Balanced expert mass contributes the basic factor:

$$
\sum_e W_e^2
\propto
\frac{1}{E}.
$$

Then:

$$
C_{\mathrm{hard}}^\star(E)
\propto
\frac{1}{E}
E^{-\beta}
=
E^{-(1+\beta)}.
$$

This explains how MoE can decay faster than $1/E$.

The exponent $\beta$ is not universal. It depends on whether the real feature graph has clusters, communities, domains, syntactic groups, semantic groups, or other structure that lets high-interference edges be separated by experts.

---

## 11. Why There Is No Universal MoE Upper Speed

For dense models, the lower bound comes from a dimension bottleneck:

$$
\|A\|_F^2
\ge
\frac{\operatorname{tr}(A)^2}{d}.
$$

This applies to all dense feature geometries in one shared $d$-dimensional space.

For MoE, the remaining crowding depends on the cut structure of the graph $I$.

Two graphs with the same total raw crowding can behave very differently:

- A uniform expander-like graph is hard to partition, so MoE may only get the basic $1/E$ reduction.
- A clustered or nearly $E$-partite graph can be partitioned so that most high-interference edges are cut, giving faster-than-$1/E$ reduction.

Therefore there is no graph-independent tight law:

$$
C_{\mathrm{moe}}^\star(E)
=
\Theta(E^{-\alpha})
$$

for a fixed universal $\alpha$.

The only universal statement is the achievable $O(1/E)$ crowding upper bound. Faster rates require assumptions about graph partitionability.

---

## 12. Relationship Between Theoretical Optima and Empirical Curves

Let:

$$
C_{\mathrm{learned}}(E)
$$

be the measured router-conditioned crowding from a trained MoE.

Let:

$$
C_{\mathrm{greedy}}(E)
$$

be the value achieved by our graph-aware greedy hard partition on the measured feature graph.

Let:

$$
C_{\mathrm{hard}}^\star(E)
$$

be the true optimum over all balanced hard partitions.

Because the greedy partition is a feasible hard partition:

$$
C_{\mathrm{hard}}^\star(E)
\le
C_{\mathrm{greedy}}(E).
$$

Because the learned router is constrained by token-level routing, optimization, architecture, and training dynamics, it is not guaranteed to equal the hard-partition optimum.

In our data:

$$
C_{\mathrm{learned}}(E)
>
C_{\mathrm{greedy}}(E)
$$

for the measured settings.

This means the real feature graph contains partitionable structure that the learned router has not fully captured.

---

## 13. Empirical Results From The Current Experiment

The current experiment measured crowding using SAE features trained on model MLP-input activations.

For dense models, we varied $d$ and measured:

$$
C_{\mathrm{dense}}(d)
=
\sum_{i\ne j}
w_iw_jG_{ij}^2.
$$

For MoE models, we fixed active dimension and varied expert count $E$. We measured router-conditioned effective crowding:

$$
C_{\mathrm{learned}}(E)
=
\sum_{i\ne j}
w_iw_jG_{ij}^2S_{ij}^{\mathrm{router}}.
$$

We also measured graph-aware hard partition crowding:

$$
C_{\mathrm{greedy}}(E)
=
\sum_{i\ne j}
w_iw_jG_{ij}^2
\mathbf{1}\{r_{\mathrm{greedy}}(i)=r_{\mathrm{greedy}}(j)\}.
$$

For dense models, we use parameter multiplier:

$$
B
=
\left(\frac{d}{128}\right)^2,
$$

The dense observed slopes against $B$ were:

$$
\text{dense observed vs } B
\approx
-0.440
$$

for frequency weights, and:

$$
\text{dense observed vs } B
\approx
-0.402
$$

for energy weights.

These should be compared to the dense parameter-budget theory target:

$$
C_{\mathrm{dense}}(B)
\sim
B^{-1/2}.
$$

The learned-router MoE slopes were:

$$
\text{green line}
\approx
-0.938
$$

for frequency weights, and:

$$
\text{green line}
\approx
-0.925
$$

for energy weights.

The graph-aware hard-partition slopes were:

$$
\text{purple line}
\approx
-1.415
$$

for frequency weights, and:

$$
\text{purple line}
\approx
-1.776
$$

for energy weights.

These results support three conclusions:

1. Learned MoE routing captures the basic $1/E$ co-routing reduction.
2. The real feature graph supports substantially faster graph-aware partitioning.
3. Router design should explicitly learn to reduce $S_{ij}$ for high-interference pairs $I_{ij}$.

---

## 14. Architectural Implication

The unified theory says that a better MoE router should not only balance load or predict the next token well.

It should also minimize:

$$
C_{\mathrm{eff}}(Q)
=
\operatorname{Tr}(Q^\top I Q),
$$

where:

$$
I_{ij}
=
w_iw_jG_{ij}^2.
$$

In words:

$$
\boxed{
\text{high-interference feature pairs should have low co-routing probability.}
}
$$

This suggests a router-improvement direction:

- learn feature-aware or activation-aware routing signals,
- encourage high-interference features to route apart,
- preserve load balance,
- preserve token-level modeling quality,
- and exploit graph partitionability beyond the universal $1/E$ baseline.

The green-purple gap in our experiment is direct evidence that this may be possible: the feature graph has exploitable structure, but the learned router only partially uses it.
