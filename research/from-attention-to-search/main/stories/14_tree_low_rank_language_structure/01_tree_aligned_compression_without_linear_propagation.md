# From “Language Trees Are Naturally Low-Rank” to Tree-Aligned Subspace Selection

## The Ending First

This line began from an attractive but underspecified idea: language recursively
composes short spans into longer spans; if leaf phrases are low-rank, perhaps
the whole language tree remains low-rank.

The research now separates two conclusions. First, the conditional theorem is
correct: if leaves share one low-dimensional state space and parents are formed
by a stable shared linear composition, rank-\(k\) approximation error obeys a
recursive bound. Second, the empirical evidence does not support that linear
propagation mechanism. Gold constituents, pretrained states, and controlled
training all show tree-aligned subspace geometry, but every registered bound
in a trained or pretrained model is vacuous. After replacing the original
content-changing control with same-parent and direction-balanced alternatives,
neither tested pretrained model shows a model-general gold-split advantage.

The strongest current story is therefore:

> In the tested representation coordinates, true hierarchical boundaries
> select or create shared low-dimensional directions. Hierarchical order can
> cause that alignment to emerge, but the current stable shared-linear model
> does not explain it.

## 1. The Objects Before the Claim

A **span** is a contiguous token sequence. A constituency tree recursively
groups spans into larger spans; it is a first computational approximation, not
a claim that language is literally a tree. Coreference, long-range dependence,
reuse, discourse, and external knowledge may require cross-branch edges, DAGs,
or feedback.

Each node \(v\) has a representation \(h_v\in\mathbb R^d\). One vector is not the
meaningful rank object: as a one-row matrix, every nonzero vector has rank one.
We instead stack comparable nodes from many examples into
\(H_\ell\in\mathbb R^{n_\ell\times d}\).

For a fixed budget \(k\), define the best rank-\(k\) error

\[
\Delta_k(H)
=
\min_{\operatorname{rank}(S)\le k}\lVert H-S\rVert_F
=
\sqrt{\sum_{i>k}\sigma_i(H)^2},
\]

and the tail-energy fraction

\[
\tau_k(H)=\frac{\Delta_k(H)^2}{\lVert H\rVert_F^2}.
\]

The 95%-energy rank \(r_{0.05}(H)\) is the smallest \(k\) with
\(\tau_k(H)\le0.05\). This is a coordinate-dependent linear concentration
measure. It does not measure behavioral use or nonlinear intrinsic dimension.

A **shared subspace** means that many nodes use the same small set of linear
directions. Individual simplicity is insufficient: \(d\) individually
one-dimensional leaves can occupy \(d\) mutually orthogonal directions and form
a full-rank matrix.

## 2. Why the Starting Intuition Was Plausible but Incomplete

Language reuses syntactic roles, semantic factors, and compositional patterns.
Long spans are often compressed summaries of local information rather than
fresh coordinate systems. This makes shared low-dimensional structure a
reasonable hypothesis.

The missing link was composition. A tree determines which nodes are related;
it does not determine their algebra. Different child transforms can map one
\(k\)-dimensional space into disjoint spaces and double dimension at each level.
A nonlinear map can also turn a one-dimensional latent variable into a
linearly full-rank curve. Tree structure alone therefore does not imply low
rank.

## 3. The Three Structural Priors

Here a **physical prior** means a pre-experimental judgment about the generating
mechanism, not a physical law.

1. **Shared-state reuse.** Recurrent local linguistic factors place leaf
   phrases near a common low-dimensional affine space. Reuse is plausible;
   exact global, coordinate-invariant low rank is not assumed.
2. **Composition preservation.** Parents mostly transform and aggregate child
   state rather than continually creating independent directions. Compression
   is plausible, but attention, gating, residual paths, and new entities need
   not equal a shared linear map.
3. **Learning origin.** If hierarchy causes the geometry, the effect should
   emerge during training and weaken when hierarchy is destroyed while token
   marginals, token multiset, and length are held fixed. This requires a
   control that changes hierarchy without changing content or capability.

All three priors are empirical premises, not theorem conclusions.

## 4. The Conditional Theorem

The first model is

\[
H_{\ell+1}=A_\ell H_\ell W_\ell^\top+E_{\ell+1},
\]

where \(A_\ell\) aggregates tree children, \(W_\ell\) is a feature transform
shared across the layer, and \(E_{\ell+1}\) is innovation, nonlinearity, and
unexplained error. Define

\[
g_\ell=\lVert A_\ell\rVert_2\lVert W_\ell\rVert_2,
\qquad
B_0=\Delta_k(H_0),
\qquad
B_{\ell+1}=g_\ell B_\ell+\lVert E_{\ell+1}\rVert_F.
\]

Then \(\Delta_k(H_\ell)\le B_\ell\) at every level. The proof propagates a
rank-\(k\) signal through the same matrices, whose multiplication cannot increase
its rank, while bounding the propagated residual by submultiplicativity.

The theorem says what follows if the model is true. It does not say real
language models obey the model. When
\(B_\ell/\lVert H_\ell\rVert_F\ge1\), the certificate is mathematically correct
but vacuous because it is larger than the state it is meant to explain.

## 5. Why the Evidence Chain Needed Six Stages

### Stage one: make the model survive its own counterexamples

Synthetic trees verified the implementation with a maximum normalized
violation of \(2.92\times10^{-8}\). Assumption-removal cases showed why each
clause matters: node-specific transforms expand rank one to full rank; sum
aggregation amplifies more than averaging; orthogonal innovations grow
effective rank; DAG reuse increases the aggregation norm. This establishes the
conditional theorem and its boundary, not a fact about language.

### Stage two: test gold syntax without a Transformer

Full-dimensional PPMI states were used to avoid making a Transformer both the
object and source of the premise. A training constituent subspace gave held-out
projection error 0.0606 on gold constituents versus 0.0921 on same-sentence,
same-length, frequency-matched nonconstituents, a 34.2% relative advantage.

This supports a tree-specific shared-subspace advantage. It does not support a
strong absolute low-rank premise: retaining 95% energy required 657 of 2,048
directions, or 32.1%, missing the registered 25% budget.

### Stage three: observe pretrained decoders with random baselines

Each span was encoded independently with a common single-token readout, so
mean pooling could not mechanically create length-dependent compression.
Pretrained checkpoints were compared with identical random architectures.

Qwen showed strong leaf and parent-child geometry with training increments;
Pythia did not replicate the same increment. Their pretrained bound ratios were
10.80 and 1.77. Tree-related geometry is observable, but a common stable linear
operator does not provide a non-vacuous explanation.

### Stage four: intervene on hierarchical order

Controlled sequence pairs preserved root state, length, and exact token
multiset while changing leaf order. Small Transformers began from identical
initialization and minibatches. The hierarchy-minus-shuffle tree-subspace
effect was \(+0.1796\) and positive in all 12 pairs, after a near-zero step-zero
difference. Latent-state count tracked leaf effective rank with Spearman
correlation 0.949.

This is the strongest evidence that hierarchical order can causally shape
tree-aligned geometry. Yet the composition effect was \(-0.0469\) in all 12
pairs, and none of 48 final hierarchy transitions had a non-vacuous bound.

### Stage five: keep the parent and every token fixed

The first clean split test fitted separate ordered maps to the annotated split
and the closest alternative boundary of the same parent. Qwen's gold advantage
was \(-0.0415\) with interval [-0.1079, 0.0213]. Pythia showed \(+0.1486\), but its
alternative moved right in 84.3% of records and the effect reversed sign for
left versus right shifts. No validation-eligible Qwen point had bound ratio
below one; the minimum was 1.3369.

### Stage six: balance both boundary directions within every parent

The robustness test retained only parents whose gold boundary could move one
word in both directions, fitted left and right controls separately, and gave
them equal weight. Qwen's effect became \(+0.0064\) and Pythia's \(-0.0001\); both
intervals crossed zero. Pythia's earlier positive aggregate disappeared, while
large and inconsistent initialization effects remained. The minimum eligible
Qwen bound was still 1.3061.

## 6. How the Cleaner Controls Resolved the Measurement Failure

A parent string literally concatenates its two child strings. The original
cross-parent permutation therefore changed child tokens as well as parent-child
structure. A model with no syntax can exploit lexical containment. The large
random-initialization advantage and the negative controlled-training effect
show that this metric does not isolate hierarchy.

This was an operationalization failure, not a theorem violation. E05 then kept
one parent and exactly the same tokens fixed, and E06 balanced left/right
alternative directions within each parent. The cleaned result is not a hidden
positive composition effect: it is approximately zero across both pretrained
models, with no non-vacuous stability point.

## 7. What Survived and What Did Not

The surviving core is that hierarchy is a useful first approximation,
approximate shared-subspace geometry is the right rank object, gold boundaries
show held-out subspace advantage, controlled order can cause that advantage to
emerge, and the theorem is a valid stability test for candidate mechanisms.

The rejected or weakened claims are that a tree alone implies rank, individual
leaf simplicity implies a common subspace, leaf low rank necessarily reaches
the root, parent predictability identifies syntax, coordinate-specific rank is
a property of language itself, one global split operator identifies the gold
tree, or geometric concentration proves behavioral use.

## 8. The More Plausible Current Mechanism

The evidence is more consistent with **tree- or scale-conditioned subspace
selection**. Different node types, depths, or contexts may select different but
partially aligned low-dimensional directions. Composition may be nonlinear,
gated, or state-dependent rather than one global \(W_\ell\).

This interpretation explains how held-out tree-aligned compression can coexist
with large worst-case spectral-norm bounds. It is a candidate explanation
induced by the failure pattern, not a new established theorem.

## 9. Scope and Claim Boundary

This line studies node-matrix geometry in chosen representation coordinates,
not the intrinsic dimension of language. Gold English constituency is one
proxy for hierarchy. PPMI, Qwen, Pythia, and controlled small models are
different coordinate systems. The evidence does not cover all languages,
model scales, dependency graphs, discourse, coreference, or cycles, and it
does not show that the low-energy directions improve prediction, reasoning,
compression, retrieval, or MoE routing.

The strongest safe claim is:

> In the tested representations, true hierarchical spans exhibit shared
> subspace geometry, and controlled hierarchical order can cause that geometry
> to emerge; the present shared-linear norm-bound model does not give a
> non-vacuous explanation.

## 10. Audit Endpoint

- **Question:** Does stable shared composition propagate a common
  low-dimensional leaf state through language hierarchy?
- **Direct observation:** gold constituents have held-out subspace advantage;
  hierarchical-order intervention creates such advantage; model propagation
  bounds are vacuous; content-fixed direction-balanced split effects are near
  zero.
- **Interpretation:** hierarchy relates to low-dimensional geometry, but the
  evidence fits conditioned subspace selection better than global linear
  propagation.
- **Established claim:** the conditional theorem is correct, tree-aligned
  compression exists in tested coordinates, and controlled order can cause it.
- **Strongest rival:** parent prediction and split contrasts are driven by
  architecture, boundary position, child length, and representational
  anisotropy rather than one global syntactic composition map.
- **Cannot claim:** language is globally low-rank, Transformers implement the
  theorem, the concentrated directions are behaviorally used, or the effect is
  universal across languages and scales.
- **Exactly one next decision:** close A14's global shared-linear propagation
  claim. If the research continues, first approve a separate research question
  for a finite node-type/depth/context-conditioned or gated-subspace question.

## Sources

- [A14 anchor](../../problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md)
- [A14 overall evidence](../../experiments/A14/14_00_tree_low_rank_language_structure/historical_support/legacy_line_experiments/summary.md)
- [A14 detailed evidence ledger](../../experiments/A14/14_00_tree_low_rank_language_structure/historical_support/legacy_line_experiments/detailed.md)
