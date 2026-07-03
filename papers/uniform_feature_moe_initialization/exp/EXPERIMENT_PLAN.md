# Experiment Plan: Representation Geometry For Uniform MoE Routing

## 0. Scientific Target

This paper asks when a linear top-1 MoE router can obtain uniform expert usage
from representation geometry, rather than from a post-hoc capacity rule.

Main question: which geometric conditions on route-relevant features and expert
prototypes make expert usage naturally uniform?

Answer tested here: two ingredients are needed in the controlled static
setting. Token directions must be close to a uniform spherical distribution,
and expert prototypes must induce approximately equal-measure spherical cells.
If either side fails, top-1 load can be imbalanced even when the other side is
well behaved.

Secondary question: how does hidden spectral geometry relate to this routing
geometry?

Answer tested here: covariance spectrum is a second-order diagnostic, not the
same object as expert usage. In an elliptical toy setting, centering,
normalization, partial spectral shrinkage, and whitening move the feature
distribution toward the spherical geometry assumed by the top-1 theorem.
Whitening gives an exact covariance result in the full-rank sample case and a
useful controlled route to near-uniform routing under well-spread prototypes.

Capacity-constrained assignment is kept only as a diagnostic control. It proves
that load counts can be forced to be uniform, but it does not explain the
representation geometry that makes top-1 routing naturally uniform.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Expert usage frequency | Fraction of examples routed to each expert | $\widehat p_e=N^{-1}\sum_i 1\{a_i=e\}$ | Decides whether experts are used equally | Feature identity or utility |
| Directional uniformity | Feature directions are evenly spread on the sphere | $z=(h-\mu)/\|h-\mu\|$ is close to $\mathrm{Unif}(\mathbb S^{d-1})$ | Direct token-side condition for equal-cell top-1 load | Natural language semantics |
| Hidden spectral uniformity | Feature covariance has no dominant direction | condition number near 1, high effective rank | Second-order route toward directional uniformity in controlled settings | Expert usage by itself |
| Geometric uniformization | Center, flatten, and normalize the representation | $z=C^{-1/2}(h-\mu)/\|C^{-1/2}(h-\mu)\|$ | Converts an elliptical toy feature distribution back toward the spherical routing model | A trained model will learn it spontaneously |
| Prototype spread | Expert centers are well distributed over feature directions | pairwise cosine / equal-measure cell behavior | Expert-side condition for top-1 load uniformity | Expert functional quality |
| Balanced assignment | Capacity-constrained finite-batch routing | greedy capacity fill or exact assignment over expanded expert slots | Diagnostic control for forced usage uniformity | Natural top-1 geometry |
| Spectral shrinkage | Controlled flattening of feature covariance | multiply eigenmode $i$ by $\lambda_i^{-\beta/2}$ | Toy proxy for spectral regularization | A trained model will learn this spontaneously |

## 2. Theory-to-Experiment Map

| Claim | Theoretical object | Experiment |
| --- | --- | --- |
| Uniform sphere + equal-measure cells gives uniform expected expert load | Spherical Voronoi partition in $d$ dimensions | E1 |
| Random prototypes are only balanced in expectation over initializations | Monte Carlo estimate of high-dimensional cell masses | E2 |
| Expert singular directions are candidate prototypes, not a balance guarantee | Controlled expert matrices with prescribed principal directions | E3 |
| Forced load balance is not a representation-geometric explanation | Capacity-constrained assignment / OT-style expanded slots | E4 control |
| Spectral flattening can restore the spherical routing geometry in a toy setting | Centering, normalization, shrinkage, whitening | E5 |

## 3. E1: $d$-Dimensional Uniform Sphere And Prototype Geometry

Question: If token features are uniformly distributed on the high-dimensional
sphere, does prototype geometry determine expert usage?

Data:

$$
z_i \sim \mathrm{Unif}(\mathbb S^{d-1}).
$$

Full setting:

- $N=100000$ examples;
- $d\in\{64,128\}$;
- $E\in\{4,8,16\}$;
- 5 seeds.

Prototype modes:

1. `symmetric`: regular-simplex prototypes, padded to dimension $d$;
2. `random`: independent random unit prototypes;
3. `clustered`: prototypes generated around one shared direction.

Primary metric: LoadCV.

Pass: symmetric top-1 has low LoadCV; clustered top-1 has higher LoadCV.

Allowed claim: under $d$-dimensional spherical feature geometry, prototype
spread controls top-1 expert usage uniformity.

## 4. E2: High-Dimensional Random Prototype Geometry Floor

Question: Does increasing routed token count remove the load floor from one
random prototype realization in high dimension?

Construction:

1. sample random expert prototypes $u_e\in\mathbb S^{d-1}$;
2. estimate their true cell masses $p_e$ with a large Monte Carlo reference set;
3. sample smaller routed batches to measure $\widehat p_e$.

Metrics:

$$
\mathrm{init\_error}=E\max_e |p_e-1/E|,
$$

$$
\mathrm{sampling\_error}=E\max_e |\widehat p_e-p_e|,
$$

$$
\mathrm{total\_error}=E\max_e |\widehat p_e-1/E|.
$$

Full setting:

- reference samples: 100000;
- $d\in\{16,64,128\}$;
- $E\in\{4,8,16\}$;
- routed batch sizes $N\in\{1000,10000,50000\}$;
- 5 seeds.

Pass: sampling error decreases with $N$; initialization error does not depend on
$N$; total error approaches the geometry floor.

Allowed claim: in high dimension, random prototype imbalance is a
single-realization geometry effect, not merely finite-token noise.

## 5. E3: Expert Spectral Prototypes

Question: Can expert principal singular directions serve as router prototypes,
and does spectral alignment alone guarantee uniform expert usage?

Expert construction:

$$
W_e = \sigma_1 v_e a_e^\top + \sigma_0 \Xi_e,
$$

where $v_e$ is the prescribed input-side top direction, $a_e$ is a random unit
vector, and $\Xi_e$ is small Gaussian noise.

Prototype modes for $v_e$:

1. symmetric;
2. random;
3. clustered.

Router variants:

1. `exact_svd`: exact top input-side singular direction;
2. `mpi_1`: one power-then-retract step;
3. `mpi_5`: five power-then-retract steps;
4. `random_router`: random rows.

Metrics:

$$
\lambda_e=\frac{\|r_e^\top W_e\|_2}{\|r_e\|_2\|W_e\|_2},
$$

plus LoadCV and max/min load ratio.

Pass: exact SVD and MPI recover high alignment; clustered spectral prototypes
still have high LoadCV.

Allowed claim: expert spectral directions can define centers, but spectral
alignment does not imply load uniformity unless the recovered centers are well
spread.

## 6. E4: Capacity Assignment As A Non-Geometric Control

Question: How different is forced usage balance from representation-geometric
top-1 balance?

Methods:

1. unconstrained top-1 assignment;
2. greedy capacity-feasible assignment;
3. exact optimal-transport-style balanced assignment using expanded expert slots.

Full setting:

- $N=2048$;
- $d=64$;
- $E=8$;
- 5 seeds;
- symmetric, random, and clustered prototypes.

Metrics:

- LoadCV;
- max/min load ratio;
- selected-score drop relative to top-1.

Pass: both balanced methods reach zero LoadCV and therefore serve as a forced
capacity control; exact balanced assignment has lower score drop than greedy.

Allowed claim: capacity constraints can force the count metric to be uniform,
but this is not the mechanism studied by the main representation-geometry
story. It does not prove directional uniformity, feature identity,
specialization, or utility.

## 7. E5: Hidden Feature Spectral Uniformization

Question: Can controlled spectral flattening move an anisotropic representation
back toward the spherical geometry required by the top-1 theorem?

Data:

Start from $z_i\sim\mathrm{Unif}(\mathbb S^{d-1})$ and form anisotropic
features:

$$
h_i=Dz_i,\qquad D=\mathrm{diag}(\alpha,1,\ldots,1).
$$

Sweep:

$$
\alpha\in\{1,2,5,10,20\}.
$$

Preprocessing variants:

1. raw;
2. centered;
3. centered + row normalization;
4. partial spectral shrinkage with $\beta=0.5$;
5. whitening + row normalization.

Spectral shrinkage uses:

$$
x_\beta=(h-\mu)U\Lambda^{-\beta/2}U^\top,
$$

where $U\Lambda U^\top$ is the empirical covariance eigendecomposition.

Metrics:

- covariance condition number;
- effective rank;
- LoadCV under a fixed symmetric router as a downstream diagnostic.

Pass: raw anisotropy increases condition number and lowers effective rank;
partial shrinkage improves both; whitening returns condition number near 1 and
effective rank near $d$.

Allowed claim: in the elliptical toy setting, explicit geometric
uniformization can flatten the covariance spectrum and restore the downstream
top-1 routing diagnostic under well-spread prototypes. This does not prove that
language-model hidden states naturally become spectrally uniform.

## 8. Claim Boundary

Can claim:

- expert usage frequency uniformity is achievable in the controlled setting by
  the combination of spherical feature directions and equal-cell prototype
  geometry;
- capacity-constrained assignment can force balanced counts, but only as a
  non-geometric control;
- hidden feature spectral uniformity is achievable in toy or controlled
  representations by centering, shrinkage, and whitening, and can restore the
  spherical routing diagnostic in the elliptical toy setting;
- spectral expert alignment supplies candidate router centers but does not
  guarantee uniform expert usage.

Cannot claim:

- balanced expert usage proves feature identity;
- balanced expert usage proves expert utility;
- hidden spectral uniformity proves expert usage uniformity;
- expert usage uniformity proves hidden spectral uniformity;
- these controlled transformations occur naturally in trained language models.
