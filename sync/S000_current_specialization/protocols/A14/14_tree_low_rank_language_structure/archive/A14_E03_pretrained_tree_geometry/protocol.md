# Protocol: A14_E03 Pretrained Decoder Tree Geometry and Shared Composition

## 0. Approval Snapshot

Approval status: **approved for direct implementation and execution** by the
researcher on 2026-07-18.

Purpose: test whether independently encoded gold constituents show
tree-specific shared-subspace compression and parent-child predictability in a
pretrained decoder, beyond span length, readout position, global anisotropy,
and an identical randomly initialized architecture.

Primary model: `Qwen/Qwen2.5-0.5B`. Replication model:
`EleutherAI/pythia-410m`. Exact downloaded revisions are frozen in the run
manifest.

Primary anchor:
[A14 tree low-rank language structure](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md)

## 1. Node Representation

Each constituent or control span is encoded independently. Append exactly one
common EOS token to its tokenizer IDs and take the hidden state at that token.
The readout therefore has causal access to the entire span and occurs at a
matched token position. Mean pooling over content tokens is diagnostic only.

Primary layer: final transformer layer. Embedding-output and middle-layer
states are diagnostics. For every pretrained model, instantiate the identical
configuration with random weights under seed 1403 and run the same inputs.

All primary matrices subtract the training-gold mean. Uncentered matrices are
diagnostic only.

## 2. Data and Sampling

Use the same file-level Penn Treebank splits and token normalization as E02.

Leaf audit:

- training: at most 8,192 deterministic length-2-to-4 coarse gold leaves;
- test: at most 2,048 gold leaves paired to same-sentence spans that are not
  constituents;
- every pair matches word length and exact tokenizer subtoken length, then
  minimizes mean training-log-frequency difference.

Composition audit:

- use naturally binary gold nodes; do not introduce artificial binarization
  nodes;
- both children must be tree constituents, parent length 2--16 words;
- at most 4,096 train, 1,024 validation, and 1,024 test triples, sampled by
  whole sentence under seed 1403;
- every parent, left child, and right child is independently encoded.

No node from a validation/test source file may enter centering, rank selection,
ridge fitting, or regularization selection.

## 3. Leaf Subspace Test

On centered training gold leaves select and freeze

$$
k=r_{0.05}(H^{train}_{leaf})
$$

and its basis $U_k$. Compute held-out projection errors for gold and matched
controls exactly as in E02. Define leaf advantage

$$
Adv_{leaf}=\frac{PE_{control}-PE_{gold}}{PE_{control}}.
$$

Use 1,000 paired sentence-level bootstrap replicates.

## 4. Shared Parent Operator

For each binary node define

$$
x_p=\frac{h_{left}+h_{right}}{2}.
$$

Fit a shared affine ridge map on training triples,

$$
h_p-\mu_y=(x_p-\mu_x)W^\top+e_p,
$$

with $\lambda\in\{10^{-6},10^{-5},\ldots,10^2\}$ selected once by validation
normalized squared residual. On test triples compare true children with a
permutation of child averages across parents within exact
left/right-subtoken-length bins (falling back to total-child-length bins only
when a bin has fewer than two examples).

Define

$$
CE=\frac{\|Y-\widehat Y\|_F^2}{\|Y-\mu_y\|_F^2},
\qquad
Adv_{comp}=\frac{CE_{perm}-CE_{true}}{CE_{perm}}.
$$

Use 1,000 sentence-level bootstrap replicates.

For the one-step theorem diagnostic, stack left and right test children into
$H_c$, use the frozen leaf rank $k$, $\|A\|_2=1/\sqrt2$, and compute

$$
B_p=\frac{\|W\|_2}{\sqrt2}\Delta_k(H_c)+\|E_{test}\|_F.
$$

Report $B_p/\|Y\|_F$ and whether it is below one. This bound is descriptive;
the fitted test innovation makes validity tautological, while non-vacuity is
not tautological.

## 5. Falsifiable Decision Rule

The primary Qwen final-layer result supports the pretrained bridge only if all
conditions hold:

1. $k/d\le0.50$ and held-out gold $PE\le0.075$;
2. $Adv_{leaf}\ge0.10$ with bootstrap lower bound above zero;
3. pretrained $Adv_{leaf}$ exceeds random initialization by at least 0.05;
4. $CE_{true}<0.90$, $Adv_{comp}\ge0.10$, and its lower bound is positive;
5. pretrained $Adv_{comp}$ exceeds random initialization by at least 0.05;
6. $B_p/\|Y\|_F<1$.

The replication model is reported separately and does not change the primary
verdict.

Fail if capability holds ($CE_{true}<0.90$) but either pretrained advantage is
non-positive with a non-positive confidence lower bound. Otherwise, including
mixed geometry or a vacuous theorem bound, the verdict is insufficient.

## 6. Rival Explanations and Guards

- Pooling artifact: common EOS readout is primary; mean pooling is diagnostic.
- Readout position: exact subtoken-length matching for leaf pairs.
- Global anisotropy: training-mean centering.
- Architecture prior: identical random-weight model.
- Probe memorization: file-level split, validation-only ridge selection, and
  one shared linear map.
- Parent length or child balance: within-length permutation.
- Artificial parse structure: only naturally binary annotated nodes.
- Sample-shape rank: training sample count must exceed four times hidden width.

## 7. Outputs

Per model/checkpoint: leaf spectra, paired projection records, composition
records, selected ridge penalty, operator norm, innovation norm, theorem bound,
bootstrap intervals, and figures. The manifest records model revisions,
tokenizer, dtype, device, package versions, seeds, data hash, and exact sample
identifiers.

## 8. Claim Boundary

Pass would show model- and treebank-specific trained geometry consistent with
the theorem premises. It would not show that the model internally constructs
the gold tree, that the linear probe is its causal computation, that language
is globally a tree, or that hierarchy caused the geometry. Causality is left
to E04's controlled training intervention.

