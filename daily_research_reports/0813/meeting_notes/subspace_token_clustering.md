# Subspace-Based Analysis and Clustering of Token Representations

## Problem setup

Suppose there are $N = 1{,}000{,}000$ token representations. Each token is a vector in a $D = 1000$-dimensional embedding space:

$$
x_i \in \mathbb{R}^{D}, \qquad i = 1, \ldots, N.
$$

We also have a reference subspace described by $K = 500$ vectors in the same embedding space. Put them into a matrix

$$
U = [u_1, u_2, \ldots, u_K] \in \mathbb{R}^{D \times K}.
$$

The aim is to use variation within this $K$-dimensional subspace to discover groups of similar tokens.

## Why analyze a subspace?

The original embedding has 1000 coordinates, but the selected vectors in $U$ express a particular notion of signal that is of interest. Projecting into their span asks a deliberately narrower question: *how do tokens differ with respect to this signal?*

If the columns of $U$ are orthonormal, the orthogonal projection of a token is

$$
\hat x_i = UU^\top x_i.
$$

Its coordinate vector $a_i = U^\top x_i$ contains all information needed to reconstruct that projection:

$$
\hat x_i = Ua_i.
$$

Moreover, distances are preserved within the selected subspace:

$$
\left\|\hat x_i-\hat x_j\right\|_2 = \left\|a_i-a_j\right\|_2.
$$

This is the central justification for comparing 500-dimensional coordinates rather than repeatedly comparing projected 1000-dimensional vectors.

## Step 1: Project each token into the subspace

For each token, compute its subspace coordinates:

$$
a_i = U^\top x_i \in \mathbb{R}^{K}.
$$

Stack these coordinates as columns:

$$
A = [a_1, a_2, \ldots, a_N] \in \mathbb{R}^{K \times N}.
$$

For this problem,

$$
A \in \mathbb{R}^{500 \times 1{,}000{,}000}.
$$

Each column of $A$ is one token represented by its 500 coordinates in the chosen subspace.

If $U$ is not orthonormal, $U^\top x_i$ is not generally an orthogonal projection. First orthonormalize the span of $U$, for example using QR decomposition, then use the resulting orthonormal basis.

## Step 2: Center the projected tokens

Compute the mean projected token coordinate:

$$
\mu = \frac{1}{N}\sum_{i=1}^{N}a_i.
$$

Center every token:

$$
\tilde a_i = a_i-\mu.
$$

The centered data matrix is

$$
\tilde A = [\tilde a_1, \tilde a_2, \ldots, \tilde a_N].
$$

Centering removes the common offset shared by the token population. The subsequent analysis then measures how tokens differ from a typical token, rather than how far they are from the arbitrary origin of the embedding space.

## Step 3: Compute covariance in the subspace

The matrix

$$
AA^\top \in \mathbb{R}^{K \times K}
$$

is an uncentered second-moment matrix. It is not generally the covariance matrix.

The sample covariance is

$$
C = \frac{1}{N-1}\tilde A\tilde A^\top
  = \frac{1}{N-1}\sum_{i=1}^{N}\tilde a_i\tilde a_i^\top.
$$

For this problem,

$$
C \in \mathbb{R}^{500 \times 500}.
$$

Its diagonal entries are variances along the selected subspace directions. Its off-diagonal entries show which directions tend to vary together.

Covariance summarizes the shape of the million-token cloud without materializing all pairwise token distances. Its important directions are the directions along which the token coordinates are most spread out.

## Step 4: Find main variation directions with PCA

Eigendecompose the covariance matrix:

$$
C = V\Lambda V^\top,
$$

where $V$ contains orthonormal eigenvectors and

$$
\Lambda = \operatorname{diag}(\lambda_1, \ldots, \lambda_K),
\qquad \lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_K \geq 0.
$$

Choose the first $r$ eigenvectors, with $r \ll 500$:

$$
V_r = [v_1, \ldots, v_r] \in \mathbb{R}^{K \times r}.
$$

The reduced representation for token $i$ is

$$
z_i = V_r^\top\tilde a_i \in \mathbb{R}^{r}.
$$

For every token at once,

$$
Z = V_r^\top\tilde A \in \mathbb{R}^{r \times N}.
$$

The retained variance fraction is

$$
\frac{\sum_{j=1}^{r}\lambda_j}{\sum_{j=1}^{K}\lambda_j}.
$$

### Why PCA before clustering?

PCA rotates the projected coordinate system into uncorrelated directions ordered by how much token variation they explain. Retaining strong directions can remove redundant correlation, suppress low-variation noise, and reduce the cost of clustering one million tokens.

PCA does not create clusters. It chooses a compact, well-conditioned coordinate system in which a distance-based clustering method can more reliably compare individual tokens. Select $r$ using explained variance, cluster stability, and whether the resulting groups remain useful and interpretable.

## Step 5: Cluster the individual token representations

The covariance matrix is a global summary. It does not itself assign tokens to groups. Cluster the individual reduced vectors $z_i$.

For $M$ clusters, k-means solves

$$
\min_{c_1,\ldots,c_N,\,m_1,\ldots,m_M}
\sum_{i=1}^{N}\left\|z_i-m_{c_i}\right\|_2^2,
$$

where $c_i \in \{1,\ldots,M\}$ is token $i$'s cluster assignment and $m_j \in \mathbb{R}^{r}$ is cluster $j$'s center.

This distinction matters: covariance answers “along which directions do tokens vary?” Clustering answers “which individual tokens lie near one another in those directions?” Different point clouds can have the same covariance but different grouping structure.

For one million tokens, mini-batch k-means is a practical default because it processes small batches instead of repeatedly scanning all tokens. It is best suited to compact, roughly spherical groups in PCA space. A Gaussian mixture model is useful if soft membership probabilities are desired:

$$
p(c_i=j \mid z_i).
$$

If groups have substantially different spreads, elongated shapes, or strong overlap, a Gaussian mixture or another geometry-aware method may be more appropriate.

## Recommended end-to-end workflow

1. Form $A = U^\top X$, where $X = [x_1,\ldots,x_N]$.
2. Subtract the projected mean to form $\tilde A$.
3. Compute $C = \tilde A\tilde A^\top/(N-1)$.
4. Eigendecompose $C$ and retain $r$ principal components.
5. Form $Z = V_r^\top\tilde A$.
6. Cluster the columns of $Z$, for example using mini-batch k-means.
7. Choose the cluster count using resampling stability, separation checks on a representative sample, and interpretation of the resulting groups.

## Scope and limitation

This procedure finds groups based only on differences visible inside the selected 500-dimensional subspace. Two tokens that differ strongly in orthogonal directions can still look similar after projection.

When $U$ is orthonormal, the orthogonal residual is

$$
r_i = x_i-UU^\top x_i.
$$

If these residual differences matter for the application, include residual features, expand the subspace, or compare against clustering in the original representation space.
