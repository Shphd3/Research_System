# A14 Overall Detailed Record

## Evidence Chain

The executed chain was:

```text
conditional theorem and numerical audit
-> deterministic assumption-removal counterexamples
-> gold syntax with non-Transformer PPMI states
-> pretrained Qwen/Pythia with identical random baselines
-> paired from-scratch hierarchy/shuffle intervention
-> same-parent same-token alternative split
-> within-parent two-sided direction-balanced split
```

Every split was at file, sentence, or full-sequence level. All rank budgets
were selected on training/validation leaves and frozen for held-out analysis.
The final codebase has 20 passing unit tests.

## Cross-Audit Claim Matrix

| Clause | E01--E04 state | E05 | E06 | Current state |
| --- | --- | --- | --- | --- |
| theorem implementation | synthetic pass | no violation | no violation | established conditional theorem |
| absolute leaf low rank | representation-dependent | Qwen 2.68%, Pythia 33.79% | Qwen 2.57%, Pythia 33.69% | representation-dependent |
| held-out tree-span geometry | positive relative evidence | parent variation aligns with leaf $U$ | same | supported only as relative geometry |
| gold split specificity | control confounded | Qwen negative; Pythia direction-sensitive | both near zero | not model-general |
| training-created split effect | mixed | Qwen numeric increment; final effect negative | initialization effects remain large | not supported |
| non-vacuous theorem bound | no real/trained model | minimum Qwen 1.3369 | minimum Qwen 1.3061 | fails empirical bridge |

## Central Numerical Results

| Quantity | Value |
| --- | ---: |
| E01 maximum normalized violation | $2.92\times10^{-8}$ |
| E02 PPMI gold/control projection error | 0.0606 / 0.0921 |
| E02 selected PPMI rank | 657/2,048 |
| Qwen pretrained leaf/composition advantage | 0.2766 / 0.6651 |
| Qwen leaf/composition training increment | +0.0754 / +0.2130 |
| Qwen/Pythia pretrained bound ratio | 10.803 / 1.772 |
| E04 all-pair descriptive tree effect | +0.1796 [0.1492, 0.2066] |
| E04 all-pair descriptive composition effect | -0.0469 [-0.0628, -0.0345] |
| E04 latent-rank Spearman | 0.9487 |
| E04 non-vacuous final hierarchy bounds | 0/48 |
| E05 Qwen/Pythia split advantage | -0.0415 / +0.1486 |
| E05 minimum eligible Qwen bound ratio | 1.3369 |
| E06 Qwen/Pythia two-sided advantage | +0.0064 / -0.0001 |
| E06 minimum eligible Qwen bound ratio | 1.3061 |

## Implementation Surface

Code and raw outputs remain on the worker surface:

[tree_low_rank worker project](../../../../../../XingyuD/Attention_Search_Experiments/active/tree_low_rank/)

Registered configs:

- `configs/exp1_theory_synthetic.yaml`
- `configs/exp2_gold_syntax_ppmi.yaml`
- `configs/exp3_pretrained_tree_geometry.yaml`
- `configs/exp4_causal_hierarchy_training.yaml`
- `configs/exp5_same_parent_split_stability.yaml`
- `configs/exp6_two_sided_split_robustness.yaml`

The local research records deliberately copy only central figures and curated
metrics; corpora, model cache, raw matrices, and generated checkpoints remain
outside the research mainline.

## Failure Decomposition

### Theorem versus mechanism

No theorem violation occurred. The empirical failure is bound usefulness:
spectral norms and innovations dominate the recursive certificate.

### Leaf premise

The leaf premise is neither uniformly true nor uniformly false. PPMI misses a
strict 25% budget; Qwen EOS states are extremely concentrated; random Qwen is
not. Linear rank therefore belongs to a representation and checkpoint, not to
language alone.

### Composition control

The original parent-child permutation rival changed child content. E05 fixed
that flaw by holding the parent and all tokens constant. Qwen then showed no
gold-split advantage, while Pythia's positive aggregate reversed by shift
direction. E06 gave every parent equally weighted left and right alternatives;
both pretrained effects became approximately zero. The remaining evidence
therefore supports subspace alignment, not one global gold-split operator.

### Capability guard

The E04 root-state probe is downstream of hierarchy and therefore unsuitable
as a neutral equality guard. The pre-registered result remains insufficient;
the all-pair randomized effects are retained only as clearly labeled
descriptive causal evidence.

## Artifact Map

- [theory-package execution map](plan_execution_map.md) and
  [Chinese companion](plan_execution_map_cn.md)

- [E01 protocol](../../A14_E01_theory_synthetic/protocol.md),
  [summary](../../A14_E01_theory_synthetic/summary.md), and
  [details](../../A14_E01_theory_synthetic/detailed.md)
- [E02 protocol](../A14_E02_gold_syntax_ppmi/protocol.md),
  [summary](../A14_E02_gold_syntax_ppmi/summary.md), and
  [details](../A14_E02_gold_syntax_ppmi/detailed.md)
- [E03 protocol](../A14_E03_pretrained_tree_geometry/protocol.md),
  [summary](../A14_E03_pretrained_tree_geometry/summary.md), and
  [details](../A14_E03_pretrained_tree_geometry/detailed.md)
- [E04 protocol](../A14_E04_causal_hierarchy_training/protocol.md),
  [summary](../A14_E04_causal_hierarchy_training/summary.md), and
  [details](../A14_E04_causal_hierarchy_training/detailed.md)
- [E05 protocol](../A14_E05_same_parent_split_stability/protocol.md),
  [summary](../A14_E05_same_parent_split_stability/summary.md), and
  [details](../A14_E05_same_parent_split_stability/detailed.md)
- [E06 protocol](../../boundary/A14_E06_two_sided_split_robustness/protocol.md),
  [summary](../../boundary/A14_E06_two_sided_split_robustness/summary.md), and
  [details](../../boundary/A14_E06_two_sided_split_robustness/detailed.md)

## Visualization Audit

All eight central figures were opened after rendering. E01 colors bind each
actual curve to its corresponding bound. E02 explicitly marks the rank budget.
E03 includes the failed theorem guard rather than only positive advantages.
E04 displays every paired effect and the full min--max range of bound ratios.
E05 exposes the same-token split contrast and all eligible frontier points.
E06 displays both left/right components so cancellation cannot be hidden.
No cropped labels, unreadable legends, or scale inconsistencies were found in
the final copies.
