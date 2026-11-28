# Preserving Separability Capacity with Narrow Experts

We ask whether the transformation performed by a dense $D\times D$ matrix on a given input distribution can be assigned to $K$ smaller $d\times d$ matrices. Our hypothesis is that the input and output representations admit corresponding subspaces, so that each expert can process one subspace using its own parameters. If this structure holds, the model can omit the connections between subspaces. We derive the resulting parameter savings and ask how the assignment of directions to experts affects the number of effective dimensions available within each expert.

## 1. Separability capacity of a dense representation

Let $x$ and $y$ be independent draws from the same centered output distribution, with nonzero covariance $\Sigma$ and eigenvalues $\lambda_1,\ldots,\lambda_D$. We define **separability capacity** as the reciprocal of their normalized mean squared inner product. Independence gives $\mathbb E[(x^\top y)^2]=\operatorname{tr}(\Sigma^2)$, so

$$
C(\Sigma)
=\frac{\mathbb E\|x\|^2\,\mathbb E\|y\|^2}
       {\mathbb E[(x^\top y)^2]}
=\frac{(\operatorname{tr}\Sigma)^2}{\operatorname{tr}(\Sigma^2)}
=\frac{(\sum_i\lambda_i)^2}{\sum_i\lambda_i^2}.
$$

This effective rank has a direct interpretation. A representation with capacity $r$ has normalized mean squared overlap $1/r$, the value attained by an isotropic representation in $r$ dimensions when $r$ is an integer.

For an isotropic representation, all eigenvalues are equal and $C=D$. For a Zipf covariance spectrum, $\lambda_i=c/i$ with $c>0$. Writing $H_n=\sum_{i=1}^n i^{-1}$ and $H_{n,2}=\sum_{i=1}^n i^{-2}$ gives

$$
C=Z(D):=\frac{H_D^2}{H_{D,2}}
\sim\frac{6}{\pi^2}(\log D)^2.
$$

Thus capacity grows linearly with width under isotropy and as the square of the logarithm under a Zipf spectrum. These laws concern the covariance of the output under the chosen input distribution.

## 2. When narrow experts can replace a wide matrix

Take $D=Kd$ and fix the input and output coordinates used by the architecture. Write the input as $u=(u_1,\ldots,u_K)$ with $u_g\in\mathbb R^d$. If the dense transformation satisfies
$$
Wu=(B_1u_1,\ldots,B_Ku_K),\qquad B_g\in\mathbb R^{d\times d},
$$
on the input distribution, the experts reproduce its output on that distribution. A dense matrix stores $K^2$ blocks of this size. The expert construction stores only the $K$ blocks required by the transformation, giving
$$
P_{\rm dense}=D^2,\qquad P_{\rm experts}=Kd^2=\frac{D^2}{K}.
$$
The saving is a fraction $1-1/K$ of the matrix parameters. Any learned basis transformations or router parameters must be counted separately.

Preserving separability capacity requires a weaker condition than reproducing every output. Suppose the expert outputs occupy distinct coordinates through scoring, are uncorrelated across blocks, and together retain the eigenvalues of the dense output covariance. The full covariance is then block diagonal, and its eigenvalues are the union of the block spectra. Substitution into $C(\Sigma)$ gives **exactly the same global capacity for every partition**. For a router that activates only some experts on each input, this condition applies to the actual routed output, with inactive coordinates set to zero.

Keeping one Zipf spectrum intact gives global capacity $Z(Kd)$. If each block instead has its own copy of the spectrum $c,c/2,\ldots,c/d$ at the same scale, the global capacity is $KZ(d)$. The following comparison holds a single spectrum fixed, so that any difference can be attributed to how directions are grouped.

## 3. Local capacity under random and frequency-based grouping

For a block assigned the set of spectral ranks $S$, its **local capacity** is
$$
r(S)=\frac{(\sum_{i\in S}1/i)^2}{\sum_{i\in S}1/i^2}.
$$
We compare partitions with exactly $d$ directions per expert and give each expert equal weight. Global capacity depends on the complete spectrum. Local capacity depends on which spectral values an expert receives together.

**Random grouping.** Partition the $Kd$ directions uniformly at random. For a randomly chosen block, let $M=\min S$ be its highest-ranked direction. Every rank enters the block with probability $1/K$, and the denominator of $r(S)$ lies between $1/M^2$ and $H_{Kd,2}$. Applying Jensen's inequality to the numerator for the lower bound gives
$$
\frac{H_{Kd}^2}{K^2 H_{Kd,2}}
\le \mathbb E[r(S)]
\le H_{Kd}^2\,\mathbb E[M^2].
$$
The probability that the block misses all of the first $t$ ranks is at most $(1-1/K)^t$. Hence $\mathbb E[M^2]$ stays bounded as $d$ grows with $K$ fixed. Both bounds are of order $(\log d)^2$. Even a wide random block typically contains a few leading directions that dominate its squared spectrum.

**Frequency-based grouping.** Assign consecutive ranks to each block, so that $S_g=\{(g-1)d+1,\ldots,gd\}$. The first block retains the head of the spectrum and has capacity $Z(d)$. In every subsequent block, the ratio of the largest to the smallest eigenvalue is less than $g/(g-1)$. For fixed $g\ge2$, summing over this interval gives
$$
\sum_{i\in S_g}\frac1i\longrightarrow\log\frac g{g-1},
\qquad
\sum_{i\in S_g}\frac1{i^2}\sim\frac1{d\,g(g-1)}.
$$
Consequently,
$$
\frac{r(S_g)}{d}\longrightarrow
g(g-1)\left(\log\frac g{g-1}\right)^2.
$$
The limiting fraction approaches one farther into the tail. Thus every block beyond the first has local capacity proportional to its width. For fixed $K\ge2$, the ratio of the mean local capacity under consecutive grouping to its expectation under random grouping grows as $\Theta_K(d/(\log d)^2)$, where the constants may depend on $K$.

For routing based on a sparse autoencoder (SAE), the empirical hypothesis is that grouping features by activation frequency produces a similar grouping of covariance directions in the expert outputs. The model predicts a higher local effective rank in experts handling the tail. This prediction can be tested at a common readout point with the same data and expert widths.

## 4. A 10,000-dimensional example

Consider a dense matrix of width $D=10{,}000$ and experts of width $d=1{,}000$. **Ten experts suffice to accommodate all 10,000 directions.** Under the subspace conditions above, the matrix parameter count falls from $10{,}000^2=100$ million to $10\times1{,}000^2=10$ million, a **90% reduction**. If the spectrum is isotropic, global capacity remains 10,000. If it follows Zipf's law, global capacity remains $Z(10{,}000)=58.24$.

For the same Zipf spectrum, grouping has a much larger effect within individual experts.

| Assignment of the 10,000 directions | Mean local capacity per expert | Global capacity |
|---|---:|---:|
| Uniform random partition | 30.82 | 58.24 |
| Consecutive spectral ranks | 896.21 | 58.24 |

The random value is a Monte Carlo estimate from 50,000 independent balanced partitions (PCG64, seed 20261119). The central 95% of partition means ranged from 21.1 to 43.6. The consecutive-rank result follows directly from the finite sums: the head expert has 34.08 effective dimensions, while the other nine each have between 960.93 and 999.08.

In this example, the subspace decomposition saves 90% of the matrix parameters while preserving global separability. Within the same ten-expert architecture, grouping adjacent ranks yields **29.1 times the mean local capacity** of random grouping. A tail expert can use nearly all of its dimensions even when its directions account for little of the total variance.
