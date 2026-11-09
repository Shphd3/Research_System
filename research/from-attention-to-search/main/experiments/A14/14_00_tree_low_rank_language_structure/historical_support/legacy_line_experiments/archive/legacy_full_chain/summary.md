# A14 Overall Summary: Tree-Aligned Compression Exists, but Stable Linear Low-Rank Propagation Is Not Supported

## Overall Adjudication

The conditional theorem is correct, and three independent empirical surfaces
show that true tree spans can have distinctive low-dimensional geometry.
However, the proposed full mechanism is **not supported**: absolute leaf
low-rank is representation-dependent, much parent-child predictability exists
at random initialization, and every pretrained or trained one-step bound is
vacuous.

| Audit | Direct verdict | Decisive result |
| --- | --- | --- |
| [E01 theorem/synthetic](../../A14_E01_theory_synthetic/summary.md) | pass | maximum normalized violation $2.92\times10^{-8}$; 17/17 counterexamples reproduced |
| [E02 gold syntax + PPMI](../A14_E02_gold_syntax_ppmi/summary.md) | insufficient | gold projection advantage 34.2%, but $k/d=32.1\%>25\%$ |
| [E03 pretrained decoders](../A14_E03_pretrained_tree_geometry/summary.md) | insufficient | strong Qwen gaps, but bound ratio 10.80 and Pythia training increment does not replicate |
| [E04 causal training](../A14_E04_causal_hierarchy_training/summary.md) | insufficient | descriptive tree effect +0.180, composition effect -0.047, 0/48 non-vacuous bounds |
| [E05 same-parent split](../A14_E05_same_parent_split_stability/summary.md) | insufficient | Qwen split advantage -0.0415; Pythia +0.1486 but reverses with boundary direction; minimum Qwen bound 1.3369 |
| [E06 two-sided split](../../boundary/A14_E06_two_sided_split_robustness/summary.md) | insufficient | direction-balanced Qwen/Pythia effects +0.0064/-0.0001; no compatible stability point |

## What Is Established

1. Under the stated shared-linear model, best rank-$k$ error propagates below
   the recursive bound. This is a mathematical/computational result.
2. Gold constituents are more aligned than matched non-constituents with a
   training-learned PPMI subspace.
3. Independently encoded gold spans can share low-dimensional coordinates,
   but gold split preference is not model-general once parent content and
   boundary direction are controlled.
4. In the paired synthetic intervention, hierarchy-aligned order causally
   creates tree-boundary subspace compression: all 12 hierarchy-minus-shuffle
   effects are positive and initialization effects are near zero.
5. Learned leaf effective rank tracks the generator's latent state count in
   the controlled system (Spearman 0.949).

## What Is Not Established

1. **Universal leaf low rank:** the PPMI leaf matrix needs 657/2,048
   directions for 95% energy and misses the registered budget.
2. **A learned shared-linear composition mechanism:** the original control was
   content-confounded; under same-parent controls Qwen has no 5% gold-split
   effect and Pythia's positive E05 effect disappears under two-sided balancing.
3. **A non-vacuous propagation explanation:** Qwen/Pythia bound ratios are
   10.80/1.77; every final controlled hierarchy transition exceeds one.
4. **Direction-independent gold-split specificity:** E06 gives +0.0064 for
   Qwen and -0.0001 for Pythia, with both confidence intervals crossing zero.

## Current Mechanism Reading

The evidence is more consistent with **tree-conditioned subspace selection or
compression** than with one globally stable linear propagation operator.
Same-parent controls now hold content fixed and still do not recover a
direction-independent gold-split effect. A realistic alternative may need
node-type/scale-specific subspaces or nonlinear gating. This is an
interpretation, not a proven replacement theorem.

## Claim Boundary

The strongest current claim is:

> In the tested representations, true hierarchical spans exhibit shared
> subspace geometry, and controlled hierarchical order can cause that geometry
> to emerge; the present shared-linear norm-bound model does not give a
> non-vacuous explanation of it.

No result proves that natural language is globally a tree, that these linear
spaces are coordinate-invariant, or that low-rank directions are behaviorally
necessary.

## Exactly One Next Decision

Close A14's global shared-linear propagation claim. If the line continues,
open a separate adjudicable question on node-type/depth-conditioned or gated
subspaces rather than adding another global linear split probe.
