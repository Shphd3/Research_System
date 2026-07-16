# Thinking Card — 05_01 Inhibition And Early Lock-In Anchor

> Migrated from [05_01_geometric_inhibition_anchor.md](05_01_geometric_inhibition_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

Parent problem: ordinary top-1 MoE routing can look consistent without forming interpretable feature-level specialization.

Current subproblem: decide whether inhibition should be pursued before the collapse mechanism is controlled.

Core hypothesis: token-conditioned inhibition is the relevant mechanism class, but selected-expert self-reinforcement can amplify early geometry into collapse.

Minimal test: compare baseline and inhibition runs on uniform features with route-load, feature assignment, hidden-router cosine, margin, and common-direction diagnostics.

Current boundary: collapse is early-geometry dominated in the audited uniform setting; the audit does not prove a full repair.

Next decision: test a minimal anti-lock-in control before using inhibition for route-utility binding.
