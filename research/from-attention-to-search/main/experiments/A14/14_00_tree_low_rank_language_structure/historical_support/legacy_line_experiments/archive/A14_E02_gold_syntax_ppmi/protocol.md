# Protocol: A14_E02 Gold Syntax and Non-Transformer Leaf-Premise Audit

## 0. Approval Snapshot

Approval status: **approved for direct implementation and execution** by the
researcher on 2026-07-18.

Purpose: test whether short constituents in real English share a
cross-sentence low-dimensional affine subspace under a full-dimensional,
non-Transformer distributional representation.

Primary anchor:
[A14 tree low-rank language structure](../../../../../problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md)

Experiment role: audit the leaf premise on real syntax without using a
Transformer representation.

Decision question: does a low-dimensional subspace learned from training
constituents generalize to held-out constituents better than to matched
non-constituent spans?

Approval decision: execute without another review pause. Corpus access failure
may change only the data source, not the metrics or decision thresholds.

## 1. Terms and Objects

- Gold constituent: a contiguous word span licensed by an annotated
  phrase-structure tree.
- Coarse leaf: a constituent selected by recursively descending the gold tree
  until a node contains at most four words. Length-one leaves are reported but
  excluded from the primary matched comparison.
- PPMI vector: one row of an uncompressed 2,048-dimensional positive
  pointwise-mutual-information word-context matrix built only from training
  sentences with a symmetric context window of five.
- Span vector: the mean of its word PPMI vectors. Mean composition is only a
  measurement device in E02; E02 cannot establish a linguistic composition
  mechanism.
- Shared-subspace error: after subtracting the training-constituent mean,
  squared energy outside the training PCA basis, divided by total centered
  energy.

## 2. Data and Leakage Guard

Use the parsed NLTK Penn Treebank sample if it is retrievable. Split by source
file, never by node: sorted file identifiers are deterministically assigned
70% train, 15% validation, and 15% test. No sentence, token occurrence, or
node from a test file may enter vocabulary counts, PPMI counts, centering, rank
selection, or subspace estimation.

Normalize tokens by lowercasing and replacing digit-bearing tokens with
`<num>`. Keep the 2,047 most frequent training tokens plus `<unk>`. Context and
target vocabularies are identical.

For each length-2-to-4 test coarse leaf, select a same-sentence contiguous span
of identical length that is not any gold constituent. Among eligible spans,
choose the one closest in mean training log frequency; break ties by start
position. Discard a leaf only if no eligible control exists.

## 3. Conditions

1. Gold coarse leaves.
2. Same-sentence, same-length, frequency-matched non-constituent controls.
3. A coordinate-wise sample permutation null, preserving each coordinate's
   marginal values while destroying cross-coordinate covariance (secondary).

The primary matrices are centered with the training gold-leaf mean. Uncentered
metrics are diagnostic only.

## 4. Rank Selection and Primary Metric

Choose once on centered training gold leaves:

$$
k=r_{0.05}(H^{train}_{gold}).
$$

Freeze both $k$ and the corresponding right singular subspace $U_k$. For a
held-out matrix $X$ define

$$
PE(X)=\frac{\|(X-\mu)(I-U_kU_k^\top)\|_F^2}
{\|X-\mu\|_F^2}.
$$

The decisive comparison is

$$
Adv=\frac{PE(X_{control})-PE(X_{gold})}{PE(X_{control})}.
$$

Use a paired sentence-level bootstrap with 1,000 replicates. Each replicate
resamples test sentences and recomputes both energy ratios from the selected
pairs. Report the percentile 95% interval for $Adv$.

## 5. Falsifiable Hypothesis and Decision Rule

Support requires all of:

1. $k/2048\le0.25$;
2. $PE(X_{gold})\le0.075$ on the held-out test split;
3. $Adv\ge0.10$ and the bootstrap 95% lower bound is positive.

Fail if $k/2048>0.50$, if $Adv\le0$, or if the lower confidence bound is not
positive with at least 500 matched test pairs. Otherwise the result is
insufficient rather than supportive.

These thresholds are fixed before reading the data.

## 6. Rival Explanations and Guards

- Global anisotropy: center using the training mean and report uncentered
  results separately.
- Span length: exact within-pair length matching.
- Word frequency: within-sentence nearest-frequency matching.
- Shape-induced low rank: rank is computed across many spans with
  $n\gg d$, not inside a length-four token matrix.
- Learned dimensionality reduction: PPMI remains 2,048-dimensional; PCA is
  used only to measure held-out projection, not to create the word vectors.
- Data leakage: all lexical statistics and subspaces are training-only.

## 7. Outputs

- `metrics.json` with split sizes, $k$, effective ranks, projection errors,
  advantage, and bootstrap interval;
- `span_records.parquet` with sentence-cluster identifiers and row energies;
- `spectrum.png`, `projection_error.png`, and a data-quality table;
- exact environment, corpus file identifiers, and seed in `run_manifest.json`.

## 8. Claim Boundary

Pass would support only this representation-specific leaf premise: short gold
constituents share a held-out PPMI subspace more than matched spans. It would
not show that language itself has coordinate-invariant linear rank, that the
tree causes the rank, that internal tree nodes preserve it, or that a
Transformer uses this mechanism.

