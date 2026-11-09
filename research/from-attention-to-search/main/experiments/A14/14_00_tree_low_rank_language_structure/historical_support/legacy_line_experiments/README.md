# A14 Experiment Mainline

This directory now keeps only the evidence needed for the current A14 claim.

## Current Route

```text
mathematical proof
-> synthetic implementation audit (E01 and E07)
-> global-linear boundary evidence (E06)
-> probabilistic conditional active-tree theorem
-> E08 independent reconstruction: a small extreme-condition state-rank gap,
   a much larger QK-rank gap, and no source-replay provenance
-> formal E08 verdict: insufficient evidence; conditional reconstruction only
-> retain the reconstruction as bounded standalone evidence
-> hand off exact-frequency, rule-reuse, and lookup-cardinality separation
   to A14_02
```

## Active Evidence

| Role | Experiment | Current use |
| --- | --- | --- |
| Synthetic strict/noisy audit | [E01 theory synthetic](A14_E01_theory_synthetic/summary.md) | Keep the theorem implementation checks, effective-rank propagation audit, and counterexamples. |
| Exact reachable-space accounting | [E07 reachable-space accounting](A14_E07_reachable_space_accounting/summary.md) | Primary synthetic evidence for role compression, within-layer reuse, cross-layer reuse, and finite-sample activation. |
| Boundary evidence | [E06 two-sided split robustness](boundary/A14_E06_two_sided_split_robustness/summary.md) | Retained only to show that one model-general global shared-linear gold-split operator is unsupported. |
| Parameter-to-state bridge reconstruction | [E08 relation-reuse bridge](A14_E08_relation_reuse_state_bridge/summary.md) | Conditional evidence for a small extreme composite-condition state-rank gap; formal verdict remains insufficient because source replay is unavailable. |

## Current Bridge Contract

| Role | Artifact | Status |
| --- | --- | --- |
| Formal decision clause | [A14_01 anchor](../../../../../problem_anchors/14_tree_low_rank_language_structure/14_01_relation_reuse_parameter_state_bridge/14_01_relation_reuse_parameter_state_bridge_anchor.md) | Updated with the independent reconstruction and formal insufficient verdict |
| Minimal bridge test | [A14_E08 result](A14_E08_relation_reuse_state_bridge/summary.md) | Full run complete; retained as bounded standalone reconstruction evidence |
| Next decision line | [A14_02 experiment index](../../../14_02_relation_reuse_root_effective_rank/README.md) | Owns the matched shared-rule versus lookup root-rank protocol |

E08 treats `share16` through `random_unshared` as a composite manipulation of
relation reuse and independent-rule complexity. Even a positive result would
not establish that frequency alone causes low rank.

## Archived Evidence

[E02--E05](archive/README.md) are preserved for provenance but are no longer
part of the active evidential chain. They tested superseded or confounded
operationalizations rather than the candidate conditional local low-rank question.

## Reading Order

1. [Current summary](summary.md)
2. [Current detailed index](detailed.md)
3. [E07 result](A14_E07_reachable_space_accounting/summary.md)
4. [E08 result](A14_E08_relation_reuse_state_bridge/summary.md)
5. [E01 result](A14_E01_theory_synthetic/summary.md)
6. [E06 boundary result](boundary/A14_E06_two_sided_split_robustness/summary.md)
