# 项目研究入口

[English](roadmap.md) · [System 项目列表](../../../PROJECTS.md) · [Focus 索引](focus/README_cn.md)

这是 from 项目自己的研究入口。优先读用户指定的结果；未指定时从下方选择研究线路。
Focus 持有研究者判断，Anchor 持有科学设计，Protocol 持有精确执行契约，Summary/Detailed 持有结果。
目录归类不产生新的科学问题、依赖、优先级或运行批准。

## A17 本对话当前路线

研究者于 2026-10-11 激活同级的[条件映射 Focus](focus/focus_conditional_mapping_transfer_cn.md)：把同向／反向任务关系比较合为一项实验，配输出诊断与资格检查后的有限训练。当前执行入口由其 [Anchor](problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor_cn.md) 和 [Protocol](experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/protocol_cn.md) 持有。旧列表、频率、敏感方向问题保留各自身份与科学判断。

研究者激活[A17](problem_anchors/17_shared_and_interference_learning/README_cn.md)：[列表Focus](focus/focus_list_rule_shared_update_cn.md)拥有直接末层投影/LoRA容量对照及匹配SAE；[独立频率Focus](focus/focus_fixed_pool_frequency_shared_learning_cn.md)拥有固定池呈现策略。Smoke→Full→频率→SAE完整顺序已授权并要求终点监督；具体运行见各Protocol。旧领域记录保留身份与判断。


## 默认阅读线路：共享学习机制

长期问题是哪些数据值得共享 Expert。现有默认入口继续沿用领域更新几何问题，
局部更新作用与长期共享/分开训练的收益需要不同证据。

- [当前 Focus](focus/focus_domain_update_geometry_cn.md)：研究问题、边界及待决点。
- [领域更新 Summary](experiments/shared_updates/domain_update_geometry/20260930/summary_cn.md)：本轮结果与资格限制。
- [共享更新研究线](problem_anchors/shared_updates/README_cn.md)：既有设计、各自实验及前后关系。
- [近期统计与相容性结果](experiments/shared_updates/ntp_statistics_local_compatibility/20260930/summary_cn.md)：独立的后续分析记录；完成不等于更换当前 Focus 或确认科学解释。
- [0930 组会稿](../../../daily_research_reports/0930/meeting_report/0930_组会汇报稿.md)：主讲和问答；不承担科学原件职责。

## 已登记的其他研究线路

以下登记保留原有工作流及角色，SECONDARY/PRIMARY 属于原线路，不是统一运行队列。
没有独立 Focus 的前序证据继续保持这一身份。具体判断请读原件。

| Workstream | Routing role | Current Focus | Evidence or contract |
|---|---|---|---|
| Shared-update mechanisms: domain update geometry | Default analysis route | [Focus](focus/focus_domain_update_geometry.md) | [Summary](experiments/shared_updates/domain_update_geometry/20260930/summary_cn.md); [Anchor](problem_anchors/shared_updates/domain_update_geometry/anchor.md) |
| A15_17 SAE representation audit | Registered SECONDARY line | [Focus](focus/focus_sae_n8_separability.md) | [Subanchor](problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md); [E01 Summary](experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E01_n8_17b_separability_audit/summary.md); [E02 Detailed](experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_02_E02_n8_15b17b_matrix/detailed.md) |
| A15 M2D2 semantic representation geometric form | Registered PRIMARY within its line | [Focus](focus/focus_m2d2_semantic_geometric_form.md) | [E01 Summary](experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E01_m2d2_direction_norm_covariance_atlas/summary.md); [E02 Summary](experiments/A15/15_14_semantic_representation_geometric_form/A15_14_E02_m2d2_full_dimension_geometry_robustness/summary.md) |
| A15 gold-label layerwise static audit | Registered SECONDARY line | [Focus](focus/focus_gmm_pseudolabel_oracle_gap.md) | [Summary](experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E15_true_label_layerwise_static_audit/summary.md) |
| A15 layerwise MoE insertion validation | Registered SECONDARY line | [Focus](focus/focus_layerwise_moe_insertion_validation.md) | [Anchor](problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md); [Summary](experiments/A15/15_15_layerwise_moe_insertion_validation/A15_15_E02_exploratory_functional_candidate_test/summary.md) |
| A15 headwise causal semantic retrieval audit | Registered SECONDARY line | [Focus](focus/focus_headwise_causal_semantic_retrieval_audit.md) | [Summary](experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/summary.md) |
| A15 final-layer SAE flat-router functional training | Registered SECONDARY line | [Focus](focus/focus_sae_flat_router_functional_training.md) | [A6 Summary](experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6_online_regularized_router/summary.md); [A6R1 Protocol](experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E20_sae_flat_router_eight_task_mixed_training/A6R1_online_regularized_router_decay/protocol.md) |
| A15 Qwen3-30B fixed-fact cross-expression semantic separability | Registered SECONDARY line | [Focus](focus/focus_qwen3_30b_semantic_representation_separability.md) | [Summary](experiments/A15/15_12_semantic_representation_separability/A15_12_E02_expression_bank_boundary_coverage_controls/summary.md) |
| A15 native-G domain-consensus MVP | Predecessor evidence; no separate current Focus | No separate Focus | [Protocol](experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_01_E01_native_g_domain_consensus_variance_atlas/protocol.md) |
| A15 rank-specific multi-representation subspace audit | Registered line; consult its Focus | [Focus](focus/focus_rank_specific_multirepresentation_subspace.md) | [Summary](experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_06_E06_rank_specific_multirepresentation_shared_scaling/summary.md) |
| A15 cross-parent fine-function transfer | Predecessor evidence; no separate current Focus | No separate Focus | [Summary](experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/summary.md) |
| A15 counterfactual-utility residual expert growth | Registered SECONDARY line | [Focus](focus/focus_gradient_consistent_hierarchical_routing.md) | [Summary](experiments/A15/15_11_gradient_consistent_hierarchical_routing/A15_11_E03_counterfactual_utility_residual_tree/summary.md) |
| A15 native-Router representation boundary | Registered line; consult its Focus | [Focus](focus/focus_random_projection_router_preservation.md) | [Summary](experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_09_E03_native_router_representation_controls/summary.md) |
| A15 stable discriminant-space evidence | Registered line; consult its Focus | [Focus](focus/focus_stable_domain_discriminant_subspaces.md) | [Summary](experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E01_stable_domain_discriminant_subspaces/summary.md) |


## 按需阅读

[Anchor 索引](problem_anchors/README.md) · [研究备查](research_notes/README_cn.md) ·
[阶段综述](stories/shared_updates/README_cn.md) · [Parking lot](parking_lot/README.md) ·
[跨仓库读取与旧路径](../../../docs/project_access_cn.md)

原有问题、优先级与判断保持不变。运行仍由对应 Protocol 和执行工作区的记录决定。

旧规则获取前提现已由[E02 Summary](experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/summary_cn.md)完成诊断，设计属于[子Anchor A17_04_01](problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor_cn.md)。子结果不替换父迁移实验的证据不足状态，也不自动启动新迁移运行。

随后获明确授权的单层AdamW迁移已完成，见[E01 R02总结](experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary_cn.md)。顺序反转产生旧规则损害，联合监督给出兼容实例；当前Focus保留诊断范围与研究者判断边界。
