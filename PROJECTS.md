# Projects

Low-frequency project map: project scope, priorities and entrypoints. For a
named result, start at its Summary. For workstream selection, use this map and
the owning Focus. Run `python tools/check_current_entrypoints.py` before relying
on current entrypoints; it checks routing and versioning, not scientific approval.

## Default Analysis Route — Shared-Learning Mechanisms

Long-term question: which data should share parameters, and what explains their
cross-update effects? Keep local effects, prospective prediction and long-term
shared/separate Expert benefit distinct. Geometry alone is not a sharing verdict.

- Current discussion: [domain-update Focus](daily_research_reports/0930/focus_domain_update_geometry.md)
  ([中文](daily_research_reports/0930/focus_domain_update_geometry_cn.md)). Reuse this
  existing question; reporting does not reset its scientific judgment.
- Current evidence: [domain-update Summary](daily_research_reports/0930/docs/domain_update_geometry/summary_cn.md).
- Presentation: [0930 three-minute brief](daily_research_reports/0930/meeting_report/0930_组会汇报稿.md).
- Earlier separate test: [natural-NTP prediction Summary](daily_research_reports/0930/docs/summary_cn.md).
- Earlier controlled question: [0927 Focus](daily_research_reports/0927/focus_shared_update_conditional_interference.md).
- Historical route: [project roadmap](Projects/from-attention-to-search/main/roadmap.md).

This map selects owners and links, not current numerical results or a second next
step. Existing Focuses keep their identities, decisions and execution boundaries.
No question is closed, merged or launched by this navigation update.

## Project Surfaces

| Project | Role and retained boundary | Entry |
|---|---|---|
| from-attention-to-search | Active research home. Shared-update analysis is the default discussion route; A06, A15 and A16 retain independent scientific states. | [Roadmap](Projects/from-attention-to-search/main/roadmap.md); [Anchor index](Projects/from-attention-to-search/main/problem_anchors/README.md) |
| diffusion-language-models | Incubating; literature audit complete. D00–D03 are candidates; question, design and execution are not approved. | [Literature audit](Projects/diffusion-language-models/main/literature/2026-07-17_diffusion_language_model_evidence_audit.md) |
| decommon-router-training | Implementation surface. Pairs 01–04 invalidated/retired; no replacement production configuration approved. Engineering qualification does not establish functional value. | `Projects/decommon-router-training/` |
| decommon-router-evaluation | Evaluator and smoke qualification; no research-eligible trained-checkpoint result. | `Projects/decommon-router-evaluation/` |
| kv_cache | Read-only reference. Only `xyDeng` is managed; never push `main`. | `Projects/kv_cache/` |
| academic_writing | Course-delivery wrapper; does not own research state. | `Projects/academic_writing/` |

Execution artifacts stay under the verified `/data/250010109/MoE_Router/`
workspace. Project worker surface: `Projects/from-attention-to-search/XingyuD/`,
registered branch `Xingyu`; verify the actual checkout before Git operations.
Paths unavailable from a Windows checkout are unverifiable there, not stale.

## Active Research Workstreams

Keep previously registered workstreams and predecessor evidence as navigation.
Priority labels below are earlier registrations, not assertions of current result
or execution state. Check the owning Focus, Summary and Protocol before resuming.
The existing 0930 domain-update Focus is now linked here; this is not activation
of a new question, a global execution queue or a change to another workstream.

| Workstream | Priority / registration | Current Focus | Evidence or contract |
|---|---|---|---|
| Natural-text domain update geometry | Current discussion; existing Focus | [Focus](daily_research_reports/0930/focus_domain_update_geometry.md) ([中文](daily_research_reports/0930/focus_domain_update_geometry_cn.md)) | [Summary](daily_research_reports/0930/docs/domain_update_geometry/summary_cn.md) |
| Controlled S7 shared-update interference | Earlier registration; see owning record | [Focus](daily_research_reports/0927/focus_shared_update_conditional_interference.md) ([中文](daily_research_reports/0927/focus_shared_update_conditional_interference_cn.md)) | [Candidate Anchor](daily_research_reports/0927/docs/shared_update_research_pack/documents/anchor.md); [draft Protocol](daily_research_reports/0927/docs/shared_update_research_pack/documents/protocol.md) |
| A15_17 SAE representation audit | Registered SECONDARY; verify in owning Focus | `daily_research_reports/0923/focus_sae_n8_separability.md` | Parent [Anchor](Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md); active [subanchor](Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md); E01 [Protocol](Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/protocol.md), [Summary](Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/summary.md), and [Detailed](Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/detailed.md); E02 [Detailed](Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E02_n8_15b17b_matrix/detailed.md). |
| A15 M2D2 semantic representation geometric form | Registered PRIMARY; verify in owning Focus | `daily_research_reports/0901/focus_m2d2_semantic_geometric_form.md` | E01 Summary: `Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E01_m2d2_direction_norm_covariance_atlas/summary.md`; E02 Summary: `Projects/from-attention-to-search/main/experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E02_m2d2_full_dimension_geometry_robustness/summary.md` |
| A15 gold-label layerwise static audit | Registered SECONDARY; verify in owning Focus | `daily_research_reports/0903/focus_gmm_pseudolabel_oracle_gap.md` | E15 [Anchor](Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md), [Protocol](Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/protocol.md), [Summary](Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/summary.md), and [Detailed](Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/detailed.md) |
| A15 layerwise MoE insertion validation | Registered SECONDARY; verify in owning Focus | `daily_research_reports/0904/focus_layerwise_moe_insertion_validation.md` | [Anchor](Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md); E02 [Summary](Projects/from-attention-to-search/main/experiments/A15/15_15_layerwise_moe_insertion_validation/A15_15_E02_exploratory_functional_candidate_test/summary.md), [Detailed](Projects/from-attention-to-search/main/experiments/A15/15_15_layerwise_moe_insertion_validation/A15_15_E02_exploratory_functional_candidate_test/detailed.md), and [Protocol](Projects/from-attention-to-search/main/experiments/A15/15_15_layerwise_moe_insertion_validation/A15_15_E02_exploratory_functional_candidate_test/protocol.md) |
| A15 headwise causal semantic retrieval audit | Registered SECONDARY; verify in owning Focus | `daily_research_reports/0904/focus_headwise_causal_semantic_retrieval_audit.md` | [Anchor](Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_16_headwise_causal_semantic_retrieval/15_16_headwise_causal_semantic_retrieval_anchor.md); [Protocol](Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/protocol.md); [Summary](Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/summary.md); [Detailed](Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/detailed.md) |
| A15 final-layer SAE flat-router functional training | Registered SECONDARY; verify in owning Focus | `daily_research_reports/0907/focus_sae_flat_router_functional_training.md` | A6 [Summary](Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/summary.md), [Detailed](Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/detailed.md), current [Anchor](Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md), and [A6R1 Protocol](Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/protocol.md) |
| A15 Qwen3-30B fixed-fact cross-expression semantic separability | Registered SECONDARY; verify in owning Focus | `daily_research_reports/backup/2026/08/0830/focus_qwen3_30b_semantic_representation_separability.md` | `Projects/from-attention-to-search/main/experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/summary.md` |
| A15 native-\(G\) domain-consensus MVP | Earlier registration; see owning record | No separate Focus; predecessor evidence under the A15 primary workstream | `Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_01_E01_native_g_domain_consensus_variance_atlas/protocol.md` |
| A15 rank-specific multi-representation subspace audit | Earlier registration; see owning record | `daily_research_reports/backup/2026/08/0827/focus_rank_specific_multirepresentation_subspace.md` | `Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/summary.md` |
| A15 cross-parent fine-function transfer | Earlier registration; see owning record | No separate Focus; predecessor evidence under the A15 primary workstream | `Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/summary.md` |
| A15 counterfactual-utility residual expert growth | Registered SECONDARY; verify in owning Focus | `daily_research_reports/backup/2026/08/0829/focus_gradient_consistent_hierarchical_routing.md` | `Projects/from-attention-to-search/main/experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03_counterfactual_utility_residual_tree/summary.md`; H100 package: `daily_research_reports/backup/2026/08/0829/docs/gradient_consistent_hierarchical_routing_h100/README.md` |
| A15 native-Router representation boundary | Earlier registration; see owning record | `daily_research_reports/backup/2026/08/0824/focus_random_projection_router_preservation.md` | `Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/summary.md` |
| A15 stable discriminant-space evidence | Earlier registration; see owning record | `daily_research_reports/backup/2026/08/0820/focus_stable_domain_discriminant_subspaces.md` | `Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E01_stable_domain_discriminant_subspaces/summary.md` |

## On-Demand Navigation

- [Ten question families](docs/research_reorganization_20260926_mapping_cn.md)
  map existing Anchors for retrieval. Proposed numbering is not an execution
  order; canonical paths and identifiers are retained.
- [Parking lot](Projects/from-attention-to-search/main/parking_lot/README.md)
  holds important inactive questions and their reopening conditions.
- [Published reading entry](sync/S000_current_specialization/README.md) and
  [Anchor index](sync/S000_current_specialization/anchor_index.md) are derived.
  Root sync, external sync, Graph edits, commit and push require explicit requests.
- `Projects/graphs/expert_specialization.graph.yaml` is optional navigation;
  its known stale A06 active markers do not override canonical owners. The old
  A05→A06→A07 method dependency is not a prerequisite for shared-update analysis.
- [Pre-refactor project map](docs/archive/project_map_20260926_before_refactor.md)
  preserves long historical explanations and former resume wording as a dated
  snapshot. It is not current guidance. The earlier priority snapshot remains
  at `daily_research_reports/0911/0911_PROJECTS_current_focus_priority_archive_cn.md`.

Writing, training, artifact ownership and approval rules are defined once in
[AGENTS](AGENTS.md) and its task-specific contracts. Repository skills are loaded
only for the task. `daily_research_reports/` holds dated reading surfaces;
`paper_reading/` and `papers/` hold reading and paper work; root `templates/`
is the maintained reusable-template home. Do not read these inventories by default.
