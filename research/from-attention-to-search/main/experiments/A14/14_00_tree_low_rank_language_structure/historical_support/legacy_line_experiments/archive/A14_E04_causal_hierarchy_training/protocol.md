# Protocol: A14_E04 Controlled Hierarchy-Training Intervention

## 0. Approval Snapshot

Approval status: **approved for direct implementation and execution** by the
researcher on 2026-07-18.

Purpose: test whether changing only the organization of paired leaf tokens
changes learned low-rank tree geometry in an otherwise identical causal
Transformer.

Primary anchor:
[A14 tree low-rank language structure](../../../../../problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md)

Experiment role: controlled causal example, not a natural-language claim.

## 1. Paired Generative Data

Generate full binary latent trees of depth five (32 leaves). The root state is
uniform over $k_\star$ states. At each depth, left and right child states are
shared modular transforms of the parent plus 15% transition noise. Each leaf
emits one of the vocabulary tokens assigned to its state. Use
$k_\star\in\{4,8,16,32\}$, content vocabulary 256, and seeds 0--2.

For every generated sequence create two paired training conditions:

1. **hierarchy:** leaves remain in depth-first tree order;
2. **shuffled:** independently permute the 32 leaves within that sequence.

The pair therefore has exactly the same length, token multiset, root state,
unigram counts, and number of examples. The intervention removes alignment
between contiguous spans and the generating tree while changing local
conditional statistics; that intended change is why language-model loss is an
outcome rather than a capability-matching variable.

Generate 20,000 train, 2,000 validation, and 2,000 test pairs per
$k_\star$/seed. Datasets are generated once and frozen before either model is
trained.

## 2. Model and Training

Train identical decoder-only Transformers:

- 4 layers, hidden width 128, 4 heads, feed-forward width 512;
- learned token and position embeddings; causal attention;
- each document is `[BOS] + 32 leaves + [EOS]`, and training appends the next
  `[BOS]` target so EOS is also an input position and its hidden state receives
  gradient;
- tied language-model head;
- AdamW, learning rate $3\times10^{-4}$, batch 128, 800 updates;
- checkpoints at steps 0, 200, 400, and 800.

For each seed, hierarchy and shuffled models start from the exact same state
dict and receive paired minibatch indices. Record validation next-token NLL.

## 3. Capability Guard

Language-model NLL is not directly comparable because shuffling intentionally
changes conditional entropy. Instead, fit the same ridge linear probe from the
full-sequence EOS state to the known root latent state. Fit on 2,000 frozen
probe examples and evaluate on 2,000 test examples.

The final causal comparison is capability-guarded when both paired models have
root-state accuracy at least 0.50 and differ by at most 0.05. Otherwise the
pair is marked insufficient for the primary geometry contrast.

## 4. Tree Geometry

Independently encode every contiguous gold span of lengths 2, 4, 8, 16, and 32
as `[BOS] + span + [EOS]`; use the EOS hidden state.

On validation hierarchy spans of length two select
$k=r_{0.05}(H^{val}_{2})$ and freeze it across all test levels. Report
$\tau_k$, $r_{0.05}$, and normalized rank at every level.

For lengths 2, 4, 8, and 16, construct a boundary-crossing control by shifting
every gold start by half its span length and retaining only in-range spans.
Learn each level's validation gold subspace and compute test gold-versus-shift
projection advantage. Average the four level advantages:

$$
Adv_{tree}=\frac14\sum_m
\frac{PE_{shift,m}-PE_{gold,m}}{PE_{shift,m}}.
$$

## 5. Shared Composition and Theorem Diagnostic

At each adjacent pair of levels, fit on validation sequences

$$
h_{parent}=W\frac{h_{left}+h_{right}}2+b+e
$$

and evaluate on test sequences. Compare true children with children permuted
across parents within level. Average the four relative residual advantages to
obtain $Adv_{comp}$.

For every level transition compute the one-step bound with the frozen base
rank and report the fraction with $B/\|H_{parent}\|_F<1$.

## 6. Falsifiable Decision Rule

For each seed and $k_\star$, define paired effects

$$
D_{tree}=Adv_{tree}^{hier}-Adv_{tree}^{shuffle},
\qquad
D_{comp}=Adv_{comp}^{hier}-Adv_{comp}^{shuffle}.
$$

Primary support requires:

1. at least 10 of 12 final pairs pass the root-state capability guard;
2. the seed/$k_\star$ cluster-bootstrap 95% lower bounds for mean $D_{tree}$
   and mean $D_{comp}$ are positive, and both point estimates are at least
   0.05;
3. step-0 paired effects have absolute magnitude below 0.02, while final
   effects exceed 0.05;
4. Spearman correlation between $k_\star$ and the median hierarchical
   length-two $r_{0.05}$ is at least 0.8;
5. at least half of hierarchical final level transitions have a non-vacuous
   theorem bound.

Fail if at least 10 pairs pass capability but both final paired effects are
non-positive with non-positive confidence lower bounds. Otherwise the verdict
is insufficient.

## 7. Outputs and Guards

Save immutable data hashes, configs, seeds, checkpoint metrics, loss curves,
root-probe accuracy, per-level spectra, projection and composition records,
theorem bounds, paired-effect tables, and central figures. Unit tests must
verify exact paired token multisets, causal masking, gold/shift span indexing,
and identical step-0 parameters.

Pre-execution implementation note: the smoke path initially omitted the next
BOS target, which would have left EOS outside the model input. This was fixed
before any registered full run; no condition, metric, threshold, or observed
effect was used to tune the protocol.

## 8. Claim Boundary

Pass would establish a controlled synthetic causal example: reorganizing
hierarchical evidence changes learned tree-aligned geometry. It would not show
that natural language has the generator, that pretrained LLMs learned by the
same route, or that low-rank directions are behaviorally necessary.
