# Protocol: A15_14_E01 M2D2 Direction, Radius, and Covariance Atlas

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_ANALYSIS
Approval status: HUMAN_CONFIRMED on 2026-09-01
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: data construction, implementation, tests, smoke, four-GPU full extraction, frozen analysis, figures, curated result records
Design frozen at: 2026-09-01 before implementation
Purpose: locate the geometric carrier of coarse and conditional-fine natural-language semantics in frozen Qwen representations
Primary Anchor: 15_14_semantic_representation_geometric_form_anchor.md
Experiment role: representation geometry and metric audit
Primary metric: confirmation normalized mutual information (NMI)
Treatment families: radius-only, direction-only, full-vector centroid, diagonal-covariance density
Primary control: keep direction and permute radius within the same layer and split
Held fixed: data, frozen model, pooling, train-only PCA basis, number of clusters, restart budget, splits
Pass types: DIRECTION_DOMINANT, RADIUS_CONTRIBUTING, SHAPE_CONTRIBUTING, MIXED
Insufficient: semantic readability, extraction identity, split isolation, or required comparison fails
Cannot claim: native Gate use, expert utility, causal semantic use, or next-token gain
```

## 1. Definitions

Direction means the unit vector after subtracting the training mean and
projecting through the same train-only PCA basis. Radius means the length of
that projected centered vector. Shape means class-dependent axiswise variance
available to a diagonal Gaussian mixture. NMI ranges from zero to one and
measures agreement between unsupervised cluster assignments and held-out
labels; it does not measure causal use.

## 2. Question, Hypothesis, And Rival

The question is where coarse and parent-conditional fine domain semantics are
geometrically accessible across the frozen model depth. The primary prediction
is that direction is sufficient. The strongest rival is that radius or
class-dependent covariance supplies a stable, held-out increment that a
directional model misses.

## 3. Data And Split Contract

Use only the nine M2D2-Wikipedia domains named in the Anchor. Deterministically
hash-select non-empty records inside each official split, concatenate only
within one fine domain with the tokenizer end-of-sequence token, and pack
non-overlapping 256-token windows. Remove exact token-window duplicates
globally. Per fine domain retain 1,024 train, 256 development, and 512
confirmation windows, for totals 9,216 / 2,304 / 4,608.

Labels are stored as metadata and never rendered in the input. Train fits PCA
and clustering. Development selects restarts only by the model's unsupervised
objective. Confirmation is untouched until code, models, thresholds, and
layerwise analysis are frozen; labels are then used only for NMI, ARI, nulls,
and stratified uncertainty.

## 4. Frozen Model And Representation Contract

Use `/data/250010109/model_cache/Qwen3-0.6B-Base-official` with every parameter
frozen and `output_hidden_states=True`. Extract the embedding output and all 28
block outputs. Primary pooling averages token positions 64--255. Final-token
pooling at position 255 is the registered guard. Also record mean next-token
NLL over targets 64--255.

At every layer and pooling, fit a rank-64 PCA basis on train only. Repeat the
final analysis at ranks 32 and 128 as sensitivity checks. Store raw hidden norm
separately from projected radius. No Router, expert, optimizer, backward pass,
training step, or checkpoint is permitted.

The primary carrier verdict is fixed before extraction at hidden-state index
15, namely the output of zero-indexed Transformer block 14, with mean pooling
and PCA rank 64. The all-layer curve localizes accessibility; final-token
pooling, the final block, and PCA ranks 32/128 are guards. None may replace a
failed primary cell or be selected by confirmation labels.

## 5. Comparison Matrix And Unsupervised Fit

For every layer use the same samples and PCA basis. Coarse clustering uses
three clusters over all windows. Fine clustering uses three clusters inside
each gold parent, but child labels remain hidden during fitting; parent-local
NMI and ARI are averaged equally.

The registered families are: a one-dimensional Gaussian mixture on log
radius; spherical k-means on direction; a von Mises--Fisher mixture on
direction; Euclidean k-means on the full projected vector; and diagonal
Gaussian mixture on the full projected vector. Each fit uses restart seeds
0--19. Restart selection uses train likelihood/inertia with development
likelihood/inertia as a tie-breaker, never label agreement.

The paired radius control replaces each observed radius with a deterministic
within-split random permutation while retaining direction. The same full-vector
families are refit on this control. A label-permutation null uses 1,000
stratified permutations. Confirmation uncertainty uses 10,000 stratified
window bootstraps with seed 1701; optimization spread is reported separately.

## 6. Metrics, Verdict, And Meaning Of Radius

Primary results are confirmation NMI for coarse and equal-parent fine tasks.
ARI is the robustness metric. The von Mises--Fisher mixture is the fixed
primary directional model; spherical k-means is a simplification guard. A
task is semantically readable when the fixed primary directional NMI exceeds
the 97.5th percentile of its matched label-permutation null.

- `DIRECTION_DOMINANT`: semantic readability passes; the 95% upper bound of
  diagonal-Gaussian minus best-directional NMI is at most 0.02; radius-only is
  not above null; observed radius does not beat radius permutation by a lower
  bound above 0.02.
- `RADIUS_CONTRIBUTING`: observed radius beats radius permutation by a lower
  95% bound above 0.02, or radius-only NMI is above its matched null.
- `SHAPE_CONTRIBUTING`: diagonal Gaussian beats both best directional and
  Euclidean k-means by lower 95% bounds above 0.02, without a radius advantage
  sufficient to explain the gain.
- `MIXED`: more than one contribution gate passes or the registered families
  do not permit one exclusive attribution.
- `INSUFFICIENT`: semantics are not readable or any required identity,
  split-isolation, model-family, pooling, rank, null, or uncertainty artifact
  is missing.

To interpret radius without redefining the verdict, report Spearman
correlations of log projected radius and raw hidden norm with frozen-model NLL
and train-token lexical rarity. Also report correlations after removing coarse
and fine domain means. These are associations, not causal meanings.

## 7. Execution, Completion, And Artifact Contract

Implementation follows test-first development: geometry decomposition, label-
blind fitting, radius permutation, synthetic direction/radius/shape recovery,
split isolation, and output schema tests must be observed failing before the
implementation is added, then pass. A model smoke verifies four expected CUDA
devices, finite pooled states, exact layer count, frozen parameter identity,
and finite NLL.

Full extraction must run on one ACP SPOT node with exactly four NVIDIA RTX
5090 GPUs: workspace `share-space`, cluster `computing-cluster-5090-01g`, worker
spec `n12lp.nn.i10a.4`, one node, four distributed extraction ranks. Any H100
device or any visible-device count other than four aborts the job. Reserved
H100 is forbidden and there is no resource fallback.

Full completion requires all 16,128 windows, both poolings, 29 hidden-state
locations, both semantic granularities, all registered model families and 20
restarts for the rank-64 atlas, rank-32/rank-128 sensitivity at the fixed
primary layer, radius controls, 1,000 nulls and 10,000 bootstraps for the
primary verdict cell, radius-
meaning correlations, source tables, two audited central figures, environment
inventory, hashes, four rank receipts, completion audit, and ACP job receipt.
Raw representations and logs remain on the worker surface.

| Block | State |
| --- | --- |
| A question and boundary | CONFIRMED |
| B data | CONFIRMED |
| C task and supervision | CONFIRMED |
| D model and representation | CONFIRMED |
| E comparison and estimator | CONFIRMED |
| F metric and verdict | CONFIRMED |
| G execution and artifacts | CONFIRMED |

Cross-block consistency: `PASS`.

Execution clarification `C001` (2026-09-01, before extraction): the mean-
pooled rank-64 hidden-state index 15 cell owns the carrier verdict. The full
rank-64 atlas and fixed-layer rank sensitivity remain required but cannot be
used for post-hoc best-layer selection. No data, label, model family, threshold,
resource, or claim boundary changed.

Execution clarification `C002` (2026-09-01, before extraction): the von
Mises--Fisher mixture owns directional readability and the shape-minus-
direction comparison. Spherical k-means remains required but cannot be chosen
post hoc because its confirmation score is larger.

Execution record `C003` (2026-09-01): `pt-ul0gol39` failed at ACP startup and
produced no run directory. `pt-l4czs4tk` verified four RTX5090 devices but
failed before tests because the analysis-runtime script incorrectly required
an add-on manifest when the base image already supplied the dependencies. The
single startup fix was reproduced locally and kept all experiment tests green.
Neither attempt produced scientific evidence. `pt-zkuak3ej` is the sole
eligible smoke/full job.

Analysis record `C004` (2026-09-01): the first finalizer displayed bootstrap
means as point estimates. Before result reporting, the finalizer was corrected
to display direct full-confirmation NMI while retaining the same 10,000 draws,
intervals, nulls, thresholds, prediction arrays, and typed verdict. A pooling-
guard figure was also promoted from the already registered final-position
analysis. Revision hashes are stored in the eligible run logs.
