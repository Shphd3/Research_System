# PROJECTS.md 迁出内容：Current Focus Priority（2026-09-11 快照）

本文件保存 `PROJECTS.md` 中已移出的 `## Current Focus Priority` 段落**原文**，作为历史快照。
它**不是当前状态来源**：当前状态由各工作流的 `focus_<problem>.md` 拥有，由研究者维护，AI 不写 Focus。

---

## Current Focus Priority

| Problem key | Role | Owning Focus | Current state / resume point |
|---|---|---|---|
| `A15.m2d2_semantic_representation_geometric_form` | `PRIMARY` | `Projects/from-attention-to-search/main/focus/focus_m2d2_semantic_geometric_form.md` | PCA-64 and centered raw-1,024 full audits both complete with `RADIUS_CONTRIBUTING`; AI result wording awaits human confirmation; token screening requires new explicit approval |
| `A15.gmm_pseudolabel_oracle_gap` | `SECONDARY` | `Projects/from-attention-to-search/main/focus/focus_gmm_pseudolabel_handoff.md` | P3 matched retraining is complete and eligible: 12/12 core arms passed at 512/load-off, but H-task−H-sem is +0.010320 in seed 17 and -0.002078 in seed 29, so the researcher-confirmed verdict is `INSUFFICIENT`. A no-training audit finds the reversal persists from update 128 with no registered operational anomaly; the only next branch is a proposed 0/0.25/0.5 supervision-strength comparison, not yet approved for execution. [P3 Result](../../../experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E14_P3_matched_training_semantic_comparison/summary.md) |
| `A15.gold_label_layerwise_static_audit` | `SECONDARY` | `Projects/from-attention-to-search/main/focus/focus_gmm_pseudolabel_oracle_gap.md` | E15 one-H100-SPOT run `om-kqsc3ncy` completed with descriptive `(9,9)` layer estimates and zero two-layer-gap probability, but registered verdict is `UNQUALIFIED_SHUFFLE_CONTROL` because confirmation child-shuffle CE exceeded its fixed bound by `0.000132` nat; AI result wording awaits human confirmation; SAE and LoRA training remain unauthorized |
| `A15.layerwise_moe_insertion_validation` | `SECONDARY` | `Projects/from-attention-to-search/main/focus/focus_layerwise_moe_insertion_validation.md` | E02 job `pt-ny8pbfn9` completed 24/24 conditions and all evaluations with registered verdict `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS`: blocks 0/10/13 all have replicated positive \(H\), but no paired lead resolves; AI interpretation awaits human confirmation. E01 remains `INSUFFICIENT` and E19 remains `QUALIFICATION_FAILED`. |
| `A15.headwise_causal_semantic_retrieval_audit` | `SECONDARY` | `Projects/from-attention-to-search/main/focus/focus_headwise_causal_semantic_retrieval_audit.md` | Phase 1 job `om-6043dkfm` completed with typed verdict `NO_REPRODUCIBLE_HEAD_HETEROGENEITY`: block-20 heads `[4,5,13,7]` repeat descriptively, but both search-corrected null gates fail and coarse/fine profiles nearly coincide; AI result wording awaits human confirmation; Phase 2 remains unauthorized |
| `A15.sae_hierarchical_teacher_construction` | `SECONDARY` | `Projects/from-attention-to-search/main/focus/focus_sae_flat_router_functional_training.md` | Completed A6 found all four constant-`0.1` online SAE/GMM regularization arms worse than matched task-only in all three seeds. The approved A6R1 changes only the structural coefficient to a linear `0.01`-to-`0.001` schedule: repaired reserved four-H100 qualification `pt-b5lg9vmt` passed, and formal 4-arm × 3-seed × 512-update job `pt-b9r9id8m` is running on the exact reserved tuple. No A6R1 result exists yet; post-training S0--S6 remain unauthorized pending researcher review. |
| `A15.qwen3_30b_fixed_fact_expression_separability` | `SECONDARY` | `Projects/from-attention-to-search/main/focus/focus_qwen3_30b_semantic_representation_separability.md` | Independent execution may continue |
| `A15.counterfactual_utility_residual_expert_growth` | `SECONDARY` | `Projects/from-attention-to-search/main/focus/focus_gradient_consistent_hierarchical_routing.md` | Completed cycle; no implementation or run authorized |

The first row is the current main attention route. The remaining rows are
retained as secondary scientific routes and do not share a problem key with
the primary route. Other legacy evidence-closure rows below remain independently readable;
before any is resumed for edits or execution, register its stable problem key,
role, and current Focus here. Conversation task parts and possible overlaps
live only in `researchctl`. They are advisory reminders: several conversations
may work on different parts of the same problem, and the researcher decides
whether any overlap requires coordination.

