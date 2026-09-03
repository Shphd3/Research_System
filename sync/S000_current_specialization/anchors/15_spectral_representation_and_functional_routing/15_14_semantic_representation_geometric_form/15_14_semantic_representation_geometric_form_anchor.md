# A15_14: Geometric Form of Natural-Language Semantics in Frozen Representations


## 1. Problem Definition

The decision question is whether coarse and parent-conditional fine M2D2
domain semantics in frozen Qwen3-0.6B-Base layer representations are carried
primarily by vector direction, vector radius, class-conditional distribution
shape, or a mixture of these objects. If radius is not a primary semantic
carrier, the experiment also asks whether it covaries with model surprise or
lexical rarity.

This is a representation-accessibility and geometry audit. It does not train
Qwen, a Router, or experts, and it cannot establish native Gate use, expert
utility, or language-model gain.

## 2. Physical Priors

A hidden vector can be separated into direction and magnitude only after the
origin and coordinate system have been fixed. A train-only mean and a common
train-only principal-component basis therefore define the registered local
coordinate system at each layer. Direction may encode semantic identity while
radius reflects confidence, familiarity, difficulty, or generic activation
strength. Class-dependent covariance can carry information even when class
mean directions are similar.

Clustering families have unequal capacity. A stronger diagonal Gaussian fit
cannot by itself prove that covariance is the intrinsic carrier. A paired
radius-permutation control is required to isolate the incremental contribution
of observed radius while preserving each sample direction.

## 3. Falsifiable Hypotheses

The primary hypothesis is direction dominance: directional models recover
coarse and fine labels above a matched shuffled-label null, while full-shape
models improve normalized mutual information by no more than 0.02 and observed
radius does not beat the paired radius-permutation control.

The strongest rival is mixed or shape-dependent semantics. It predicts a
stable confirmation-set gain from observed radius, or a diagonal-covariance
gain beyond both directional and Euclidean-centroid models that cannot be
explained by radius alone.

## 4. Mathematical Model

For layer $\ell$, let $h_i^{(\ell)}$ be the mean frozen hidden state over token
positions 64--255. Fit the training mean $\mu_\ell$ and a rank-$q$ PCA basis
$P_\ell$, with registered primary rank $q=64$:

$$
z_i^{(\ell)}=P_\ell^\top(h_i^{(\ell)}-\mu_\ell),\qquad
r_i^{(\ell)}=\lVert z_i^{(\ell)}\rVert_2,\qquad
u_i^{(\ell)}=\frac{z_i^{(\ell)}}{\max(r_i^{(\ell)},\epsilon)}.
$$

Radius-only models observe $\log r$. Directional models observe $u$. Euclidean
centroid and diagonal Gaussian models observe $z$. The paired radius control
uses $\tilde z_i=r_{\pi(i)}u_i$, where $\pi$ permutes radii within the same
layer and split without accessing labels.

Normalized mutual information (NMI) and adjusted Rand index (ARI) compare
cluster assignments with held-out domain labels after fitting has ended. NMI
is the primary unit. Raw hidden norm $\lVert h\rVert_2$ is reported separately
and is never substituted for PCA radius.

## 5. Computational Realization

Use the official M2D2-Wikipedia train, validation, and test files for a balanced
three-parent by three-child hierarchy: Culture and the arts (Mass media,
Performing arts, Visual arts), Health and fitness (Exercise, Nutrition, Public
health), and Natural and physical sciences (Biology, Earth sciences, Physical
sciences). Per child use 1,024 train, 256 development, and 512 confirmation
windows of 256 tokens. Labels remain metadata and are never rendered.

Freeze the local official Qwen3-0.6B-Base model and extract the embedding output
plus all 28 block outputs. The primary pooled object is the mean over positions
64--255; final-position pooling is a registered guard. At each layer, fit PCA
on train only, use development only for unsupervised objective selection, and
open confirmation labels only for the frozen analysis. Primary PCA rank is 64;
ranks 32 and 128 are sensitivity checks.

The carrier verdict is fixed at hidden-state index 15, the output of
zero-indexed Transformer block 14 that the adjacent Router workstream intends
to consume, under mean pooling and rank 64. The full 29-location atlas answers
where accessibility appears but cannot select a more favorable verdict layer
after confirmation labels are opened.

For the coarse task fit three clusters globally. For the fine task fit three
clusters separately inside each known parent and average the three parent
scores equally. The fitted families are one-dimensional Gaussian mixture on
log radius, spherical k-means, directional von Mises--Fisher mixture,
Euclidean k-means, and diagonal Gaussian mixture. Twenty deterministic
restarts are selected only by their train/development unsupervised objective.

## 6. Minimal Falsification Tests

Semantic readability requires the registered von Mises--Fisher directional
model's confirmation NMI to exceed the 97.5th percentile of 1,000 matched
label permutations. Spherical k-means is a simplified directional guard and
cannot replace it after confirmation is opened. Direction dominance
additionally requires the upper 95% paired-bootstrap bound of diagonal-
Gaussian minus von Mises--Fisher NMI to be at
most 0.02 and no positive observed-radius advantage over radius permutation.

Radius contribution requires a lower 95% paired-bootstrap bound above 0.02 for
the best full-vector model using observed radius over its radius-permuted
counterpart, or radius-only NMI above the matched null. Shape contribution
requires diagonal Gaussian to exceed both the best directional and Euclidean
centroid models by more than 0.02 at the lower bound while the radius control
does not explain the gain. Otherwise the typed result is mixed or
insufficient.

Ten thousand stratified window bootstraps quantify confirmation uncertainty;
layers are not independent replicates. The full label set is used only after
all extraction, model-family, layer, and threshold choices are frozen.

## 7. Current Evidence

**Evidence wording status:** `AI_EVIDENCE_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
The approved four-RTX5090 full run completed all 16 registered guards. At the
fixed mean-pooled hidden-state-index-15, PCA-rank-64 cell, directional vMF NMI
is 0.1289 for coarse domains and 0.3223 for parent-conditional fine domains,
well above matched label-null 97.5% thresholds 0.0014 and 0.0028. Radius-only
NMI is 0.0315 and 0.1397, also above its nulls. Observed-radius versus
radius-permuted diagonal-Gaussian differences have 95% intervals [0.1237,
0.1451] and [0.0321, 0.0619]. Both tasks therefore receive the registered
`RADIUS_CONTRIBUTING` verdict.

Independent shape contribution does not pass: the diagonal-Gaussian minus
direction lower bounds are 0.0094 coarse and 0.0162 fine, below the required
0.02. Its fine NMI also varies from 0.4252 at PCA rank 32 to 0.2055 at rank
128, while directional vMF remains 0.3187--0.3223.

The final-position guard changes the interpretation. At the same fixed layer,
directional NMI is only 0.0017 coarse and 0.0057 fine. The eligible positive
evidence therefore belongs to whole-window mean pooling. Fine-domain vMF NMI
is already 0.1777 at the embedding aggregate, keeping lexical/topic
composition alive as a strong rival to abstract deep semantic organization.

Canonical evidence: [Summary](/Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E01_m2d2_direction_norm_covariance_atlas/summary.md) and [Detailed record](/Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E01_m2d2_direction_norm_covariance_atlas/detailed.md).

The raw-1024-dimensional replication preserves the same typed verdict. At the
same fixed mean-pooled cell, directional vMF NMI is 0.1298 coarse and 0.3180
fine, while radius-only NMI is 0.0321 and 0.1283. Diagonal-Gaussian NMI is
0.1615 and 0.3151, so independent covariance-shape contribution still does
not pass. Final-position direction remains near zero at 0.0014 coarse and
0.0060 fine. This rules out PCA rank 64 as the sole source of the
direction-primary, radius-contributing result, while the fine diagonal-Gaussian
drop from 0.3569 after PCA to 0.3151 in raw coordinates warns against treating
one covariance model as coordinate-invariant. Canonical replication evidence:
[E02 Summary](/Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E02_m2d2_full_dimension_geometry_robustness/summary.md).

## 8. Claim Boundary And Next Decision

Pending human wording confirmation, the strongest admissible claim is that
mean-pooled M2D2 domain information at the fixed block is direction-primary
and radius-contributing under the registered model families, and that this
typed verdict replicates without PCA in the raw 1024-dimensional state. It is not an
intrinsic ontology theorem and cannot establish per-token accessibility,
causal use, expert specialization, or task benefit.

Exactly one next decision follows: before selecting token-Router geometry,
compare the current-token state with a deployable causal-prefix aggregate at
block 14 under lexical controls. Only a causal Router-visible object that
retains the direction/radius result may enter a later functional protocol.

**Pre-extraction clarification C001 (2026-09-01):** hidden-state index 15,
mean pooling, and PCA rank 64 own the carrier verdict. This clarification was
frozen before any Qwen extraction or M2D2 geometry result existed and prevents
post-hoc best-layer selection.

**Pre-extraction clarification C002 (2026-09-01):** the von Mises--Fisher
mixture is the fixed primary directional model. Spherical k-means is a guard;
the better confirmation score is not selected post hoc.
