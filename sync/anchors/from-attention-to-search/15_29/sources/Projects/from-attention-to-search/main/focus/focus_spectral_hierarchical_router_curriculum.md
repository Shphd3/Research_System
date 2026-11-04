# Progressive versus full spectral routing supervision

problem_key: `spectral_hierarchical_router_curriculum`
anchor_id: `15_29`
question_state: `USER_ACTIVATED`
design_state: `USER_FIXED_P_F_CONTRACT`
task_state: `PARTIAL_P_FORMAL_SUBMITTED_F_SCHEDULING_BLOCKED`
result_state: `NO_TRAINING_RESULT`
human_result_judgment: `Unknown`
question_closure: `Unknown`

The researcher's current instruction fixes one question: does progressively enabling the same head/middle/tail teacher routing hierarchy help relative to enabling all levels from the start? P/F each train50B valid targets with identical controls. This is one experiment with two arms.

Three steps: construct and independently check a frozen contextual teacher tree; implement and qualify exact loss/gradients/data/recovery on2x5090spot; submit P then F as separate8x5090spot jobs under a shared8GPU maximum. This conversation completes on actual accepted IDs and verified requests after smoke PASS, not on50B completion.

Lower matched validation loss for P is directional within-seed support; equal or worse P is non-support; target or execution qualification failures are insufficient. Cross-seed, semantic hierarchy and adaptive convergence claims remain out of scope. Scientific acceptance stays Unknown. Existing baseline is retained.

[Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_29_spectral_hierarchical_router_curriculum/15_29_spectral_hierarchical_router_curriculum_anchor.md) · [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_29_spectral_hierarchical_router_curriculum/R01_progressive_vs_full/protocol.md) · [Execution](/data/250010109/MoE_Router/experiments/20261031_spectral_hierarchical_router/README_cn.md).
