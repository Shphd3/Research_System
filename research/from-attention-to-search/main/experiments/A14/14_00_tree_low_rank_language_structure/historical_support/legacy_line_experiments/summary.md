# A14 Current Experiment Summary

## Result Snapshot

**What is established:** the synthetic implementation agrees exactly with the
reachable-space accounting. Global dimension growth is controlled by role-map
compression and reuse of directions within and across layers; finite samples
may activate less than the mechanism permits.

**What the language evidence shows:** the direction-balanced E06 control does
not support one model-general global shared-linear gold-split operator. It does
not reject tree composition or a constrained conditional local model.

**New bridge evidence:** E08 independently reconstructed the ABCD share
experiment. The extreme composite contrast produced a small held-out
task-state-rank gap (mean 11.0 versus 13.7) and a much larger combined-QK rank
gap (29.7 versus 50.7). The formal verdict is insufficient because the original
generator, code, and checkpoints were unavailable; intermediate state ranks
were also nonmonotonic.

**What comes next:** E08 is retained as bounded standalone reconstruction
evidence. Review
[A14_02_E01](../../../14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/protocol_cn.md),
which separates exact frequency, rule reuse, and function cardinality through
matched shared-rule and lookup conditions. Router experiments remain outside
the current decision.

## Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Reachable space | Directions permitted by the leaf space and role maps | Layerwise sum of role-image subspaces | Upper-bounds observable rank | That finite language data activate every direction |
| Role compression | A role map keeps fewer dimensions than it receives | Dimension of one role-image space | Can slow layer-rank growth | That discarded directions are linguistically irrelevant |
| Within-layer reuse | Different child roles use overlapping output directions | Overlap among role-image spaces | Prevents role dimensions from simply adding | Global low rank |
| Cross-layer reuse | A new layer reuses directions already present in earlier layers | New-layer intersection with cumulative history | Directly limits global new directions | That language exhibits this reuse |
| Boundary evidence | Evidence that narrows what cannot be claimed | E06 direction-balanced null result | Closes the global shared-linear proxy | The failure of all tree composition |

## Mainline Evidence

| Evidence | Direct result | Current role |
| --- | --- | --- |
| [E01 synthetic theorem audit](A14_E01_theory_synthetic/summary.md) | Maximum normalized violation \(2.92\times10^{-8}\); 17/17 registered counterexamples reproduced | Numerical audit of the older strict/noisy propagation implementation |
| [E07 reachable-space audit](A14_E07_reachable_space_accounting/summary.md) | 950/950 registered records matched exact dimension accounting; maximum mismatch 0 | Primary synthetic implementation evidence for the refined theory |
| [E06 direction-balanced split](boundary/A14_E06_two_sided_split_robustness/summary.md) | Qwen/Pythia gold-split effects \(+0.0064/-0.0001\); every stability bound remained vacuous | Negative boundary for a model-general global shared-linear operator |
| [E08 relation-reuse bridge](A14_E08_relation_reuse_state_bridge/summary.md) | Extreme state ranks 13/10/10 versus 16/13/12; QK gap much larger; source replay unavailable | Conditional reconstruction evidence, formally insufficient under the registered provenance gate |

## Archived Operationalizations

E02--E05 are indexed in [the archive](archive/README.md). Their measurements
remain reproducible, but they are not used to validate the current theory:

- E02 used averaged PPMI word co-occurrence vectors rather than compositional semantic states;
- E03 was a one-step independent-span prediction probe with lexical-containment and role-averaging mismatches;
- E04 had a failed registered capability guard and inherited the parent-content confound;
- E05 fixed parent content but had a boundary-direction imbalance and was superseded by E06.

## Claim Boundary

Can claim:

- the refined reachable-space implementation is exact on the registered synthetic cases;
- low-dimensional leaves and finite depth do not alone guarantee global low rank;
- the tested global shared-linear gold-split proxy is unsupported in E06.

Cannot claim:

- that natural language or a Transformer is globally low rank;
- that a Transformer internally recurses over a gold syntax tree;
- that conditional local low-rank composition has already been observed;
- that E08 isolates frequency, establishes monotonicity, or exactly reproduces the source study;
- that any MoE or Router design follows from A14.

## Exactly One Next Decision

Review and freeze the
[A14_02_E01 Chinese protocol](../../../14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/protocol_cn.md).
Do not run it before approval; Router experiments remain parked.
