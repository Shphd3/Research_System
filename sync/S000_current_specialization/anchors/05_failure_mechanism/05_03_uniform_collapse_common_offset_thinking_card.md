# Thinking Card — 05_03 Uniform Collapse Common-Offset Anchor

> Migrated from [05_03_uniform_collapse_common_offset_anchor.md](05_03_uniform_collapse_common_offset_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

Parent problem: ordinary top-1 MoE routing collapses even when feature frequencies are uniform.

Current subproblem: explain why a bias-free linear router still develops a dominant expert in the original uniform feature setting.

Core hypothesis: a shared hidden component creates an expert-specific effective bias $w_e^T c$; top-1 training then amplifies the early winner.

Minimal test: verify data/init, measure common-score prediction, cancel the common offset, and causally ablate routed-position / positional embedding sources.

Current boundary: P0-P5 support common-offset as the step-0 driver; the 4GPU position-source ablation supports fixed routed position / positional embedding as a major causal source of the step-0 common component, but not a full solution to final collapse. The no-position slot-init/inhibition supplement shows that cosine slot-init can sustain slot-level route structure, while current true token-conditioned inhibition still amplifies lock-in.

Next decision: use no-position `S0-cos` as the positive slot-structure control, and do not continue the current inhibition formulation as the main anti-collapse path without a separate lock-in fix.
