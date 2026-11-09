# A15_13_E17 Result Summary: DCLM SAE Candidate Hierarchy Reproduction

```text
Execution status: FULL_RUN_COMPLETE
Evidence eligibility: ELIGIBLE
Typed verdict: NONTRIVIAL_REPLICATED
Knowledge wording: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
Successful ACP job: pt-3c60qjz3
Worker run: full-20260904T023742Z
```

## Direct Answer

The completed E16 sparse autoencoder admits a reproducible nontrivial activation-containment graph under the registered E17 construction. The discovery graph contains 1,212 composite groups, 2,616 directed edges, 1,279 nodes, and maximum depth two. The disjoint DCLM validation source retains 24 groups, 91 edges, 53 nodes, and maximum depth two. This satisfies the registered `NONTRIVIAL_REPLICATED` gate, but it does not reproduce the historical six-level visual depth and does not yet qualify any node as a coarse or fine semantic teacher.

## Primary Result

| Graph | Composite groups | Edges | Nodes | Nodes by depth | Maximum depth |
|---|---:|---:|---:|---|---:|
| DCLM discovery candidates | 1,212 | 2,616 | 1,279 | 67 / 1,201 / 11 | 2 |
| Frozen relations on disjoint DCLM validation | 24 | 91 | 53 | 29 / 23 / 1 | 2 |

Only 24 of 1,212 discovery groups pass every replication rule, a retention rate of 1.98%. This sharp contraction is driven by the registered minimum joint-gain rule: 1,171 groups pass minimum one-sided containment, 1,210 pass the reverse-containment ceiling, but only 24 pass the minimum joint gain of 0.02.

## Central Evidence

### Discovery candidate graph

![Discovery candidate activation-containment graph](figures/candidate_hierarchy.png)

How to read: nodes are placed by longest-path depth, not by semantic meaning. The dense depth-one band and small depth-two band establish that the registered construction is non-flat, while the strong hub-and-spoke form warns against reading it as a balanced taxonomy.

### Replication-qualified graph

![Replication-qualified activation-containment graph](figures/replicated_hierarchy.png)

How to read: only frozen discovery groups that pass all validation-source gates remain. The single depth-two top node is feature 27,821; the graph is reproducible but shallow.

## Bounded Interpretation

The strict surviving graph contains one explicit depth-two chain: feature 27,821 includes feature 6,187 as one of five constituents, while feature 6,187 includes features 8,856 and 29,342. On the validation source, the minimum constituent-given-composite probabilities are 0.9845 for feature 27,821 and 0.9914 for feature 6,187, with joint gains 0.0796 and 0.0784. This is evidence for nested activation containment, not semantic composition. Direct and transitive edges coexist, so graph depth is also not a unique semantic level assignment.

## Claim Boundary

E17 establishes only that the frozen final-layer SAE contains a small, independently reproducible candidate activation-containment structure. It does not establish semantic parent--child relations, coarse/fine granularity, causal feature composition, layerwise Router readability, expert utility, or task-performance gain. Exact historical counts and depth were not a registered target and were not reproduced.

## One Next Decision

Decide whether to approve a separately frozen M2D2 semantic qualification of only the 24 replicated groups and 53 retained nodes, using coarse-label concentration, parent-conditioned fine-label concentration, and frequency/coverage-matched controls. Router and LoRA training remain outside that decision.

## Sources

- [Protocol](protocol.md)
- [Detailed evidence record](detailed.md)
- [Candidate groups](tables/composition_candidates.csv)
- [Replication gate breakdown](tables/gate_breakdown.csv)
- [Discovery nodes](tables/feature_nodes.csv)
- [Discovery edges](tables/feature_edges.csv)
- [Replication nodes](tables/replicated_feature_nodes.csv)
- [Replication edges](tables/replicated_feature_edges.csv)
