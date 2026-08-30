# Representation-Separability Metric Audit for Qwen3-30B-A3B

```text
type: literature_and_method_audit
status: NON_EXECUTABLE_CANDIDATE
date: 2026-08-30
scope: semantic separability of frozen Qwen3-30B-A3B gate-input representations
execution_authority: NONE
anchor_change: NONE
protocol_change: NONE
```

## Conclusion First

No single scalar, including X-MoE's representation-collapse score, can answer
whether the current representation is "linearly separable enough." The minimum
defensible evaluation must jointly measure:

1. **readability**: whether a regularized linear readout generalizes to unseen
   expression families;
2. **low-tail robustness**: whether difficult held-out rows retain positive,
   scale-normalized multiclass margin;
3. **failure localization**: which semantic class pairs overlap and whether
   the overlap comes from within-class spread or weak center separation;
4. **readout complexity**: how many discriminant dimensions and how many
   labelled examples are needed;
5. **stability**: whether the same discriminant structure transfers across
   expression banks and layers.

The recommended primary stack is therefore a cross-template regularized linear
probe, a normalized margin distribution, a pairwise class-distance normalized
variance matrix, and a shrinkage Fisher spectrum. Manifold capacity and
minimum-description-length probing are explanatory secondary analyses. X-MoE
RC is retained only as a comparability diagnostic.

## 1. Exact Decision Question

At Qwen3-30B-A3B layers 4, 12, 20, 28, 36, and 44, does the actual MLP/gate
input at the final `Classification:` token support a **stable, low-complexity,
positive-low-tail linear readout** of:

- the eight parent labels;
- the eight child labels conditional on the known parent;
- the joint 64 parent--child labels;

when the readout is evaluated on expression families that were not used to fit
or select it?

This is a semantic-readout question. It does not establish that the same
partition maximizes expert utility or improves language-model loss.

## 2. Why X-MoE RC Is Not the Primary Answer

For class labels $y$, define pooled within-class covariance $\Sigma_W$ and
between-class covariance $\Sigma_B$. X-MoE adopts a neural-collapse statistic
of the form

$$
RC = \operatorname{Tr}(\Sigma_W\Sigma_B^{\dagger}),
$$

where $\dagger$ is the Moore--Penrose pseudoinverse. In X-MoE, the classes are
the router's expert assignments and larger RC is interpreted as less routing-
induced representation collapse.

That direction is not transferable without qualification. Under external
semantic labels, a smaller within-class spread relative to separated class
centres is normally evidence for easier semantic classification, not a defect.
Furthermore:

- expert assignments are endogenous outputs of the router, whereas semantic
  labels are external audit labels;
- $\operatorname{rank}(\Sigma_B)\leq C-1$, so a pseudoinverse is unavoidable
  and unstable directions can dominate when hidden width exceeds sample size;
- one trace hides the worst class pair and the low-margin rows;
- the score does not directly test held-out linear prediction;
- a value has no universal good/bad threshold across layers, label systems, or
  feature normalization choices.

RC can be reported after shrinkage and null calibration, but it must not be the
sole verdict or share X-MoE's interpretation mechanically.

## 3. Metric Families and Decision Roles

### 3.1 Cross-template regularized linear probe: primary capability metric

Fit multinomial logistic regression on frozen representations using only the
training expression families. Select regularization using a disjoint
development family, freeze every choice, and evaluate on an unseen family.

Report:

- balanced accuracy;
- cross-entropy in nats per row;
- normalized accuracy gain

$$
G_{\mathrm{acc}}=\frac{\mathrm{BA}-1/C}{1-1/C};
$$

- bootstrap confidence intervals with the expression family or semantic cell
  as the resampling unit.

This answers whether a linear readout generalizes. It does not by itself show
that every row is safely separated, that the feature is used by the model, or
that the readout is cheap to learn.

Required controls are label permutation within parent, a template-identity
probe, and identical preprocessing and regularization search at every layer.

### 3.2 Scale-normalized multiclass margin: primary robustness metric

For held-out row $i$ with true class $y_i$, define the geometric one-versus-
nearest-competitor margin

$$
\gamma_i=
\min_{j\neq y_i}
\frac{(w_{y_i}-w_j)^\top z_i+b_{y_i}-b_j}
{\lVert w_{y_i}-w_j\rVert_2}.
$$

The feature transformation and classifier must be frozen before the held-out
bank is opened. Report the 5th percentile, 10th percentile, median, positive-
margin fraction, and bootstrap interval. Raw logits or unnormalized margins
are not comparable across layers because arbitrary feature or weight scaling
changes them.

The 5th percentile is an operational low-tail requirement: $q_{0.05}>0$ means
at least 95% of the evaluated rows are on the correct side of their nearest
linear decision boundary. It is a chosen engineering standard, not a theorem
that the representation is universally sufficient.

### 3.3 Pairwise class-distance normalized variance: primary localization metric

For classes $c$ and $c'$, define

$$
CDNV(c,c')=
\frac{\sigma_c^2+\sigma_{c'}^2}
{2\lVert\mu_c-\mu_{c'}\rVert_2^2},
$$

using a training-frozen normalized or shrinkage-whitened feature space.
Smaller values mean the two centres are far apart relative to their within-
class spread. Report the full pairwise matrix, its median and 90th percentile,
and the identity of the worst pairs. Do not report only the mean.

This separates two failure modes hidden by accuracy: broad semantic manifolds
and nearly coincident class centres. It remains a centre-and-variance summary,
so non-Gaussian tails still require the margin analysis.

### 3.4 Shrinkage Fisher spectrum: primary complexity metric

Solve the regularized generalized eigenproblem

$$
S_Bv_k=\lambda_k(S_W+\rho I)v_k,
$$

with shrinkage $\rho$ selected without confirmation data. Report:

- the eigenvalue spectrum $\lambda_k$;
- the shrinkage H-score or regularized trace summary;
- effective discriminant rank;
- the minimum rank $r_{90}$ retaining 90% of held-out probe gain.

This answers whether semantic information is concentrated in a small linear
subspace that a low-capacity router can plausibly learn. High accuracy with a
large $r_{90}$ means "linearly readable but diffuse," not "easy to route."
Because the active view has width 2,048 and only 1,920 rows, unregularized
covariance inversion is forbidden.

### 3.5 Manifold capacity, radius, and dimension: explanatory geometry

Treat all expression variants of one semantic object as a nuisance manifold.
Estimate linear manifold capacity $\alpha_c$, effective radius $R_M$, effective
dimension $D_M$, and centre correlations under controlled random projections.
This family can explain *why* separability improves or degrades: smaller radius,
smaller effective dimension, and lower harmful correlations can raise linear
classification capacity.

This is especially relevant because the rows are deliberately generated from
multiple expression families. It is a secondary analysis for the first audit
because implementation and estimation are more involved than a frozen linear
probe and margin distribution.

### 3.6 Description length and sample-efficiency curves: secondary ease metric

Minimum-description-length probing measures how many bits and labelled examples
are needed to transmit the labels from the representation, not merely the final
accuracy. A simpler first implementation is a learning curve over fixed sample
fractions. This distinguishes "the information exists" from "a router can learn
it efficiently."

### 3.7 Pairwise Gaussian overlap and kernel alignment: secondary diagnostics

- Gaussian Bhattacharyya overlap can identify class pairs whose fitted
  distributions overlap after low-dimensional, training-frozen projection and
  covariance regularization.
- Centred kernel--target alignment measures agreement between the representation
  Gram matrix and a label Gram matrix. It is a useful global label-alignment
  diagnostic but does not guarantee robust held-out linear separation.

### 3.8 CKA and discriminant-subspace transfer: stability, not separability

Centred kernel alignment (CKA) can compare the global geometry of two layers or
expression banks. However, high CKA can coexist with poor semantic separation,
and low CKA can coexist with equally good but rotated discriminant subspaces.
Therefore the decision-bearing stability test is direct transfer of the frozen
probe or discriminant projector from C4E to C5E, supplemented by principal
angles or projector overlap. CKA is descriptive only.

### 3.9 Metrics that must not carry the verdict

- training accuracy, because a width-2,048 representation can support
  memorization without expression-family generalization;
- raw class-centre distance, because it ignores within-class spread and scale;
- silhouette or Davies--Bouldin cluster indices, because Euclidean cluster
  compactness is neither necessary nor sufficient for a stable linear decision
  boundary in this high-dimensional supervised task;
- PCA explained variance, because high-variance directions need not be the
  semantic discriminant directions;
- UMAP or t-SNE separation, because the visualization algorithm changes local
  and global geometry;
- neural-collapse simplex metrics such as NC2, because the semantic hierarchy
  is not hypothesized to form an equiangular simplex.

## 4. Recommended Minimum Audit on Existing Data

### Data

- `TAX-C4E`: 1,920 rows, 30 expression rows in each of 64 parent--child cells;
- `TAX-C5E`: 1,920 rows from a disjoint expression bank over the same original
  facts;
- Qwen3-30B-A3B gate-input views with shape `[6, 1920, 2048]` at layers 4, 12,
  20, 28, 36, and 44.

The exact paths, hashes, and representation identities are registered in the
[A15 dataset registry](../../../Projects/from-attention-to-search/main/datasets/README.md).

`TAX-C4A` is a separate fact-shift diagnostic and must not be pooled into the
expression-generalization verdict because its masked Wikipedia prose has a
different naturalness boundary.

### Comparisons

For each layer and each of the three label tasks:

1. fit on the 15 C4E template families marked `half=A`, selecting
   regularization only by grouped cross-validation within that half;
2. evaluate the frozen choices on the 15 C4E template families marked
   `half=B`;
3. freeze preprocessing, regularization, classifier, and metric code;
4. transfer directly to all 30 C5E template families without refitting;
5. compare against within-parent label permutation and template-identity
   controls.

Because C4E and C5E have already been opened, this is a registered diagnostic
and replay, not a pristine confirmation experiment.

### Primary outputs

One layer-by-task table must contain:

| Capability | Robustness | Location | Complexity | Stability |
|---|---|---|---|---|
| balanced accuracy and cross-entropy | $q_{0.05}$ margin and positive-margin fraction | worst-pair and 90th-percentile CDNV | Fisher effective rank and $r_{90}$ | C4E-to-C5E accuracy/margin drop |

Two figures are sufficient:

1. layer-wise curves for normalized accuracy gain and 5th-percentile margin;
2. a worst-pair CDNV heatmap for parent, conditional-child, and joint labels.

No UMAP or t-SNE panel is decision-bearing.

## 5. Verdict Vocabulary

Use the following evidence-bounded labels rather than a universal scalar cutoff.

| Verdict | Required observation | Meaning |
|---|---|---|
| `NOT_READABLE` | held-out probe is indistinguishable from its registered null | no established linear semantic signal under this audit |
| `READABLE_NOT_ROBUST` | average held-out performance exceeds null, but low-tail margin is non-positive or transfer fails | average linear information exists, but it is not enough for reliable semantic routing |
| `ROBUST_BUT_DIFFUSE` | cross-template low-tail margin is positive, but effective rank/sample requirement is large | linear separation exists but may be expensive for a small router to learn |
| `ROBUST_LOW_COMPLEXITY` | capability, low-tail, transfer, and low-rank requirements jointly pass | the current representation is a plausible input for a simple semantic router |
| `SHORTCUT_SENSITIVE` | random-row or same-template performance is high but family-held-out transfer fails | probe exploited expression or template nuisance rather than stable semantics |

The operational `ROBUST_LOW_COMPLEXITY` gate should require all of:

- cross-template performance above the permutation-null upper confidence bound;
- held-out $q_{0.05}$ geometric margin with lower confidence bound above zero;
- no isolated parent or conditional-child block whose failure is hidden by the
  macro average;
- C4E-to-C5E transfer remaining above null without refitting;
- a pre-registered low-rank or sample-efficiency budget.

The low-rank budget must be chosen from the intended router capacity before
seeing the layer ranking. It cannot be inferred post hoc from whichever layer
looks best.

## 6. How to Say How Good or How Bad

Report a separability profile rather than one adjective:

$$
\mathcal{S}_{\ell,t}=
(G_{\mathrm{acc}}, q_{0.05}(\gamma), p_{\gamma>0},
CDNV_{0.90}, r_{90}, \Delta_{C4\rightarrow C5}),
$$

for layer $\ell$ and task $t$. Here $\Delta_{C4\rightarrow C5}$ is the frozen
transfer loss in accuracy and margin.

- **How good?** State the fraction of chance-corrected performance recovered,
  the protected low-tail margin, the fraction of positive-margin rows, and the
  smallest discriminant rank retaining the result.
- **Where bad?** Name the parent or child pair with the largest CDNV and the
  expression family producing the largest transfer loss.
- **How bad?** Quantify the negative low-tail margin, bad-pair fraction, excess
  rank above the router budget, and C4E-to-C5E degradation.

This profile prevents a high mean accuracy from being described as "sufficient
separability" when the difficult rows, a parent block, or a template shift still
fails.

## 7. Claim Boundary and Next Decision

This audit can establish the strength, weakness, location, complexity, and
expression stability of **linear semantic readout** in the frozen Qwen3-30B-A3B
gate-input representation. It cannot establish causal use by the native router,
expert competence, counterfactual expert utility, or language-model gain.

The next decision is whether the researcher accepts the five-dimensional
definition of "enough": capability, low-tail robustness, failure localization,
low complexity, and expression stability. Only after that confirmation should
these metrics be promoted into an executable Protocol.

## 8. Primary Literature

- Chi et al., [On the Representation Collapse of Sparse Mixture of
  Experts](https://arxiv.org/abs/2204.09179), 2022.
- Zhu et al., [A Geometric Analysis of Neural Collapse with Unconstrained
  Features](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f92586a25bb3145facd64ab20fd554ff-Abstract.html),
  NeurIPS 2021.
- Galanti et al., [On the Role of Neural Collapse in Transfer
  Learning](https://arxiv.org/abs/2112.15121), ICLR 2022.
- Bao et al., [An Information-Theoretic Approach to Transferability in Task
  Transfer Learning](https://arxiv.org/abs/2212.10082), introducing H-score.
- Ibrahim et al., [Newer Is Not Always Better: Rethinking Transferability
  Metrics, Their Peculiarities, Stability and
  Performance](https://arxiv.org/abs/2110.06893), introducing a shrinkage
  repair for covariance-based H-score estimation.
- Chung et al., [Classification and Geometry of General Perceptual
  Manifolds](https://doi.org/10.1103/PhysRevX.8.031003), Physical Review X 2018.
- Mamou et al., [Emergence of Separable Manifolds in Deep Language
  Representations](https://proceedings.mlr.press/v119/mamou20a.html), ICML 2020.
- Hewitt and Liang, [Designing and Interpreting Probes with Control
  Tasks](https://aclanthology.org/D19-1275/), EMNLP-IJCNLP 2019.
- Voita and Titov, [Information-Theoretic Probing with Minimum Description
  Length](https://aclanthology.org/2020.emnlp-main.14/), EMNLP 2020.
- Kornblith et al., [Similarity of Neural Network Representations
  Revisited](https://proceedings.mlr.press/v97/kornblith19a.html), ICML 2019.
- You et al., [LogME: Practical Assessment of Pre-trained Models for Transfer
  Learning](https://proceedings.mlr.press/v139/you21b.html), ICML 2021.
- Huang et al., [Frustratingly Easy Transferability
  Estimation](https://proceedings.mlr.press/v162/huang22d.html), ICML 2022.
- Pándy et al., [Transferability Estimation Using Bhattacharyya Class
  Separability](https://openaccess.thecvf.com/content/CVPR2022/html/Pandy_Transferability_Estimation_Using_Bhattacharyya_Class_Separability_CVPR_2022_paper.html),
  CVPR 2022.
- Cristianini et al., [On Kernel--Target
  Alignment](https://papers.neurips.cc/paper_files/paper/2001/hash/1f71e393b3809197ed66df836fe833e5-Abstract.html),
  NeurIPS 2001.

## Mainline Update Check

- **Hypothesis:** unchanged; this audit does not claim the representation is
  already sufficient.
- **Experiment design:** changed at the candidate level from a single RC or
  accuracy number to a five-dimensional separability contract.
- **Interpretation:** strengthened boundary between semantic readability and
  router/expert utility.
- **Next decision:** human confirmation of the definition of "enough" before
  Protocol promotion or execution.
