# Thinking Card — 05_02 Feature Assumption Relaxation Anchor

> Migrated from [05_02_feature_assumption_relaxation_anchor.md](05_02_feature_assumption_relaxation_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

Parent problem: ordinary top-1 MoE route consistency may reflect collapse, shortcut, or early lock-in rather than feature-level specialization.

Current subproblem: relax one simplifying feature assumption at a time and test whether route structure remains interpretable.

Core hypothesis: if ordinary top-1 truly follows target-relevant features, route structure should survive compositional tokens and structured many-feature grouping under non-collapse.

Minimal test: P1 compositional target-rule routing and P3 same-expert family grouping, both with target accuracy and load guards.

Current boundary: P1 and P3 are negative or bounded; target learning succeeds but routing often collapses or behaves like seed-dependent buckets.

Next decision: do not use assumption-relaxation results as positive specialization evidence until an explicit non-collapse or anti-lock-in guard changes P3b.
