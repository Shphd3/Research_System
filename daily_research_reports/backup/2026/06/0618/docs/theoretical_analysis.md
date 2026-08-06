# Theoretical Analysis: Load Variance In Two-Dimensional Random Routing

## Objective

Model the two sources of load imbalance in the two-dimensional experiment:

1. Random centroid initialization creates unequal expert-owned intervals on the circle.
2. Finite token count creates sampling noise around those true interval sizes.

The goal is to explain why increasing the number of tokens reduces sampling error but does not remove the load imbalance caused by random centroid placement.

## Plain-Language Picture

In the two-dimensional experiment, every token is a point on a circle.

Each expert has one centroid, also on the circle. A token is routed to the expert whose centroid points in the most similar direction. On a circle, this means each expert owns one interval of angles around its centroid.

For example, if there are \(m=4\) experts and the centroids are perfectly evenly spaced, each expert owns one quarter of the circle:

\[
p_j = \frac{1}{4}.
\]

But if the centroids are random, some centroids land close together and some land far apart. Then some experts own short intervals and some experts own long intervals.

That interval length is the expert's true load before sampling any finite batch of tokens.

This document uses:

- \(p_j\): the true fraction of the circle owned by expert \(j\).
- \(\widehat p_j\): the measured fraction of sampled tokens routed to expert \(j\).

The important idea is simple: each expert owns the part of the circle closer to its centroid than to any other centroid.

We call that expert-owned interval a **Voronoi cell**. In this document, a Voronoi cell means:

\[
\Omega_j
=
\{x \text{ on the circle}: x \text{ is routed to expert } j\}.
\]

In two dimensions, \(\Omega_j\) is an interval of angles on the circle. Its length as a fraction of the full circle is:

\[
p_j = \Pr(x \in \Omega_j).
\]

So when this document says "cell size," it means the fraction of the circle routed to one expert.

## How The 2D Features, Gate, And Expert Centers Are Computed

This experiment is a simplified gate-only model implemented in [two_dim_routing.py](/Users/lishang/Documents/MOE%20Gating/src/moe_gating/two_dim_routing.py). It does not train expert matrices. Each expert is represented by one routing center on the unit circle.

This is the two-dimensional version of the routing problem only:

\[
d = 2,\qquad k = 2,\qquad z=x.
\]

There is no learned projection \(A\) in this first experiment. The goal is to isolate the geometry of random routing centers before adding the \(d \rightarrow k\) bottleneck.

### Token features

Each token feature is a two-dimensional unit vector:

\[
x_i =
\begin{bmatrix}
\cos \theta_i \\
\sin \theta_i
\end{bmatrix},
\qquad
\theta_i \in [0,2\pi).
\]

For the dense-grid experiment, implemented by `unit_circle_tokens`, token angles are evenly spaced with a half-step offset:

\[
\theta_i
=
\frac{\pi}{n_{\text{tokens}}}
+
\frac{2\pi i}{n_{\text{tokens}}},
\qquad
i=0,\ldots,n_{\text{tokens}}-1.
\]

The offset avoids placing many tokens exactly on decision boundaries.

For the token-sensitivity experiment, implemented by `random_unit_circle_tokens`, token angles are sampled uniformly:

\[
\theta_i \sim \operatorname{Uniform}(0,2\pi).
\]

### Expert/gate centers

For each expert \(j\), `random_unit_centroids` samples a two-dimensional Gaussian vector:

\[
r_j \sim \mathcal{N}(0,I_2).
\]

Normalize it to the unit circle:

\[
c_j = \frac{r_j}{\lVert r_j\rVert_2}.
\]

So each expert center is:

\[
c_j =
\begin{bmatrix}
\cos \phi_j \\
\sin \phi_j
\end{bmatrix},
\]

where \(\phi_j\) is the expert center angle. Because the Gaussian is rotationally symmetric, \(\phi_j\) is uniformly distributed on the circle:

\[
\phi_j \sim \operatorname{Uniform}(0,2\pi).
\]

### Gate score

The gate score in `route_top1` is the dot product:

\[
s_{ij} = x_i^\top c_j.
\]

Because both vectors have unit norm:

\[
s_{ij} = \cos(\theta_i-\phi_j).
\]

So maximizing score is the same as choosing the expert center with the smallest angular distance from the token.

### Routing rule

The top-\(1\) routing rule in `route_top1` is:

\[
g(x_i) = \arg\max_j s_{ij}.
\]

Equivalently:

\[
g(x_i)
=
\arg\min_j d_{\mathrm{circle}}(\theta_i,\phi_j),
\]

where \(d_{\mathrm{circle}}\) is the shorter angular distance around the circle.

This is why the circle is divided into expert-owned intervals. The boundary between two neighboring expert centers is the midpoint angle between them. Every token between two neighboring boundaries is routed to the same expert.

## Implementation-to-Theory Mapping

The theory uses the same objects computed by the code.

| Theory object | Meaning | Implementation |
| --- | --- | --- |
| \(x_i\) | token feature on the unit circle | row of `tokens` |
| \(c_j\) | expert routing center on the unit circle | row of `centroids` |
| \(s_{ij}\) | score of token \(i\) for expert \(j\) | `scores = tokens @ centroids.T` |
| \(g(x_i)\) | selected expert for token \(i\) | `assignments = np.argmax(scores, axis=1)` |
| \(\widehat p_j\) | measured token load for expert \(j\) | `loads = load_fraction(assignments, m)` |
| \(p_j\) | true Voronoi cell size for expert \(j\), measured as a fraction of the circle | `arc_lengths = circular_voronoi_arc_lengths(centroids)` |
| \(\max_j |\widehat p_j - 1/m|\) | absolute load error | `TwoDimRun.load_error` |
| \(\frac{\max_j |\widehat p_j - 1/m|}{1/m}\) | normalized load error | `TwoDimRun.normalized_load_error` |
| \(\max_j |\widehat p_j - p_j|\) | sampling error against true interval size | `TwoDimRun.arc_error` |

The main experiment uses:

\[
\texttt{token\_mode}=\texttt{grid}.
\]

In this mode, \(\widehat p_j\) is almost exactly \(p_j\), because the tokens densely cover the circle.

The token-count sensitivity experiment uses:

\[
\texttt{token\_mode}=\texttt{random}.
\]

In this mode, \(\widehat p_j\) includes finite-token sampling noise.

## Falsifiable Conjecture

For uniform tokens on the unit circle, observed load imbalance decomposes as:

\[
\widehat p_j - \frac{1}{m}
=
\left(p_j - \frac{1}{m}\right)
+
\left(\widehat p_j - p_j\right),
\]

where:

- \(m\) is the number of experts.
- \(p_j\) is the true fraction of the circle owned by expert \(j\).
- \(\widehat p_j\) is the measured token fraction routed to expert \(j\).
- \(p_j - 1/m\) is initialization variance.
- \(\widehat p_j - p_j\) is finite-token sampling variance.

The conjecture predicts:

- Increasing \(n_{\text{tokens}}\) reduces \(\widehat p_j - p_j\).
- Increasing \(n_{\text{tokens}}\) does not reduce \(p_j - 1/m\).
- Therefore normalized load error approaches a nonzero initialization floor for random centroids.

## 2. Physical Priors
Random centroids on the circle are unbiased but not evenly spaced. Uneven centroid spacing creates unequal expert-owned intervals. More tokens estimate those unequal intervals more accurately; more tokens do not make the intervals equal.

## Model 1: Random Initialization Variance

Let \(m\) centroids be sampled independently and uniformly on the unit circle. Sort their angles. Let the circular gaps between adjacent centroids be:

\[
G_1,\ldots,G_m.
\]

For random points on a circle:

\[
(G_1,\ldots,G_m) \sim \operatorname{Dirichlet}(1,\ldots,1),
\]

with:

\[
\sum_{i=1}^m G_i = 1.
\]

Here \(G_i\) is measured as a fraction of the full circle, not radians.

For cosine nearest-centroid routing, expert \(j\)'s owned interval is half of the gap to its previous neighbor plus half of the gap to its next neighbor:

\[
p_j = \frac{G_{j-1}+G_j}{2}.
\]

The expected interval size is:

\[
\mathbb{E}[p_j] = \frac{1}{m}.
\]

So random centroids are balanced in expectation.

This expectation is across many random initializations. It does not say that one specific initialization is balanced.

The variance of one expert-owned interval size is:

\[
\operatorname{Var}(p_j)
=
\frac{m-2}{2m^2(m+1)}.
\]

Therefore the normalized standard deviation of one expert-owned interval is:

\[
m\sqrt{\operatorname{Var}(p_j)}
=
\sqrt{\frac{m-2}{2(m+1)}}.
\]

This quantity does not go to zero as \(m\) increases. It approaches:

\[
\frac{1}{\sqrt{2}}.
\]

This explains why random centroid initialization has persistent relative imbalance.

## Model 2: Finite-Token Sampling Variance

Given fixed true expert-owned interval sizes:

\[
p_1,\ldots,p_m,
\]

the routed token counts follow:

\[
(N_1,\ldots,N_m) \mid p
\sim
\operatorname{Multinomial}(n_{\text{tokens}}, p_1,\ldots,p_m).
\]

The measured load is:

\[
\widehat p_j = \frac{N_j}{n_{\text{tokens}}}.
\]

Conditioned on \(p_j\):

\[
\mathbb{E}[\widehat p_j \mid p_j] = p_j,
\]

and:

\[
\operatorname{Var}(\widehat p_j \mid p_j)
=
\frac{p_j(1-p_j)}{n_{\text{tokens}}}.
\]

For roughly balanced expert intervals, \(p_j \approx 1/m\), so:

\[
\operatorname{Std}(\widehat p_j - p_j)
\approx
\sqrt{\frac{(1/m)(1-1/m)}{n_{\text{tokens}}}}.
\]

After normalizing by \(1/m\), the finite-token sampling scale is approximately:

\[
m\sqrt{\frac{(1/m)(1-1/m)}{n_{\text{tokens}}}}
=
\sqrt{\frac{m-1}{n_{\text{tokens}}}}.
\]

This term shrinks as:

\[
O(n_{\text{tokens}}^{-1/2}).
\]

So token-count sensitivity should mainly affect the sampling error, not the initialization error.

## Metric Used In The Viewer

The viewer's load error is normalized by the ideal load:

\[
\operatorname{LoadError}
=
\frac{\max_j |\widehat p_j - 1/m|}{1/m}
=
m \max_j |\widehat p_j - 1/m|.
\]

Using the decomposition:

\[
\widehat p_j - \frac{1}{m}
=
\left(p_j - \frac{1}{m}\right)
+
\left(\widehat p_j - p_j\right),
\]

the normalized load error is controlled by:

\[
m \max_j \left|p_j - \frac{1}{m}\right|
\]

from centroid initialization, plus:

\[
m \max_j |\widehat p_j - p_j|
\]

from finite-token sampling.

## Interpretation Of Current Results

The token sensitivity experiment shows:

- The sampling error decreases when \(n_{\text{tokens}}\) increases.
- The normalized load error remains large even at \(n_{\text{tokens}}=100000\).

This matches the theory:

\[
\text{sampling noise} \rightarrow 0
\quad \text{as} \quad
n_{\text{tokens}} \rightarrow \infty,
\]

but:

\[
\text{initialization imbalance}
\not\rightarrow 0
\]

for random finite \(m\) centroids.

## Why \(m=2\) Is Special

For two centroids on the circle, each expert-owned interval is exactly a half-circle as long as the centroids are distinct. Therefore:

\[
p_1 = p_2 = \frac{1}{2}.
\]

So the initialization variance is zero:

\[
\operatorname{Var}(p_j)=0.
\]

This explains why the \(m=2\) experiment is exactly balanced.

## Prediction For Correction Methods

If the above model is correct, then methods that only increase token count will not solve finite-\(m\) imbalance. Methods that change centroid geometry should help.

The next correction experiments should compare:

1. Random centroids.
2. Evenly spaced centroids on the circle.
3. Minimum-angle rejection sampling.
4. Repulsive centroid optimization.
5. Capacity-constrained assignment.

The predicted result is:

- Evenly spaced centroids should make:

\[
p_j = \frac{1}{m}
\]

for every expert.

- Random centroids should keep nonzero initialization variance.
- Finite-token sampling noise should still decay as \(O(n_{\text{tokens}}^{-1/2})\) in both cases.

## Implementation Contract

To test this model, add a theory-comparison experiment that records:

- true expert-owned interval probabilities \(p_j\);
- measured token loads \(\widehat p_j\);
- initialization error:

\[
m\max_j |p_j - 1/m|;
\]

- sampling error:

\[
m\max_j |\widehat p_j - p_j|;
\]

- total observed load error:

\[
m\max_j |\widehat p_j - 1/m|.
\]

Pass condition:

- Sampling error decreases with \(n_{\text{tokens}}\).
- Initialization error does not decrease with \(n_{\text{tokens}}\).
- Total load error approaches initialization error for large \(n_{\text{tokens}}\).

Fail condition:

- Total load error continues to shrink toward zero with token count for random centroids.
- Sampling error does not scale like \(n_{\text{tokens}}^{-1/2}\).
- Initialization error does not match analytic circular interval imbalance.

## Claim Boundary

This analysis applies to the two-dimensional circle experiment with uniform tokens and cosine nearest-centroid routing. It does not yet prove the same scaling for high-dimensional semantic features, learned projections, nonuniform token distributions, or trained MoE models.
