# A14 Current Evidence Index

This file is the compact audit index after the 2026-07-20 archive cleanup.
The older full-chain ledger remains available under
[archive/legacy_full_chain](archive/legacy_full_chain/README.md).

## 1. Current Mathematical Evidence

### E01: strict/noisy propagation implementation

- [Protocol](A14_E01_theory_synthetic/protocol.md)
- [Summary](A14_E01_theory_synthetic/summary.md)
- [Detailed evidence](A14_E01_theory_synthetic/detailed.md)

Retained clauses: strict-rank implementation checks, noisy effective-rank
recurrence, and registered counterexamples. Broad sweeps are supporting
diagnostics rather than a separate language claim.

### E07: exact reachable-space accounting

- [Protocol](A14_E07_reachable_space_accounting/protocol.md)
- [Summary](A14_E07_reachable_space_accounting/summary.md)
- [Detailed evidence](A14_E07_reachable_space_accounting/detailed.md)

Primary metric: maximum absolute difference between the registered dimension
recurrence and an independent SVD measurement. Full-run value: 0 dimensions
over 950 records.

## 2. Current Boundary Evidence

### E06: two-sided direction-balanced split

- [Protocol](boundary/A14_E06_two_sided_split_robustness/protocol.md)
- [Summary](boundary/A14_E06_two_sided_split_robustness/summary.md)
- [Detailed evidence](boundary/A14_E06_two_sided_split_robustness/detailed.md)

Use only for the boundary that one model-general global shared-linear
gold-split operator is unsupported. Do not use it to reject tree composition,
conditional composition, nonlinear composition, or contextual composition.

## 3. Current Bridge Evidence

### E08: relation-reuse parameter-to-state reconstruction

- [Protocol](A14_E08_relation_reuse_state_bridge/protocol.md)
- [Summary](A14_E08_relation_reuse_state_bridge/summary.md)
- [Detailed evidence](A14_E08_relation_reuse_state_bridge/detailed.md)

Formal registered verdict: insufficient evidence because the original source
generator, training code, and checkpoints were unavailable. In the independent
reconstruction, the `share16` versus `random_unshared` state-rank gap was
positive in 3/3 seeds (3/3/2 dimensions), while the combined-QK gap was much
larger. Intermediate state conditions were nonmonotonic. Use E08 only as
conditional reconstruction evidence pending post-run review.

## 4. Archived Operationalizations

See [archive/README.md](archive/README.md) for E02--E05 and the precise reason
each experiment left the mainline. The archive preserves protocols, results,
figures, and links to worker-side machine artifacts.

## 5. Missing Mainline Evidence

No current experiment tests all of the following together:

1. a finite and predeclared set of conditions;
2. held-out low-dimensionality within each condition;
3. ordered condition-specific parent composition;
4. local low rank with potentially high global rank;
5. functional value on a language task.

E08 addresses only a toy parameter-to-state clause and does not test ordered
condition-specific parent composition or a real language task. It is retained
as bounded standalone reconstruction evidence. The current decision is to
review
[A14_02_E01](../../../14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/protocol_cn.md),
which separates exact frequency, shared composition, and lookup cardinality;
it does not authorize a Router protocol.
