# 全量 Anchor 新旧编号对照（审阅稿）

这是问题检索与编号提案，不是默认推进顺序。共 124 项：118 份非归档项目 Anchor、3 份未归属日期草案、3 份已归档历史。英语与中文伴随稿共享一个编号；本表不改变编号路径、归档状态或研究者判断。L1–L4 的文字修订已另行完成并记录来源哈希。

编号：主线.父问题.已有局部子问题。3 份历史不取得新的当前编号；日期草案仅分配待确认的候选号。缺号补齐和旧编号碰撞只在新表中消解，历史引用仍以完整路径识别。

“保留”只表示保留问题与证据，不表示应继续运行。L 是推理修订项，P 是移出默认推进的提案；具体边界见[整理方案](research_reorganization_20260926_cn.md)。

## 1. 共同性与功能分工的判定

先定义：什么才算共同方向、专家不同且确实有用？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 1.1 | [A06_00](../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md) | 父级/平铺问题 | 怎样才算真正的专家功能分化？ |
| 1.2 | [A01_01](../Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_01_common_operator_identifiability_anchor.md) | 父级/平铺问题 | 如何定义并识别“共同方向”？ |
| 1.3 | [A01_02](../Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_02_ground_truth_projector_recovery_anchor.md) | 父级/平铺问题 | 已知真值时能否找回共同子空间？ |
| 1.4 | [A01_03](../Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_03_gradient_common_vs_activation_common_anchor.md) | 父级/平铺问题 | 共同激活能否代表共同优化方向？ |
| 1.5 | [A06_04](../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor.md) | 父级/平铺问题 | 真实任务是否有稳定的专家价值余量？ |
| 1.5.1 | [A06_04_01](../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/subanchors/06_04_01_context_conditioned_expert_utility_anchor.md) | 子问题 | 上下文能否稳定决定哪个专家更有用？ |
| 1.6 | [A06_03](../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md) | 父级/平铺问题 | 稀疏探索能否把路由绑定到专家价值？ |

## 2. 路由锁定与分工形成

为什么早期分路会被保留，什么过程阻碍功能分工？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 2.1 | [A02](../Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/02_ntp_style_top1_router_lockin_anchor.md) | 父级/平铺问题 | 下一词训练为何早期锁定某种分路？ |
| 2.2 | [A05_03](../Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_03_uniform_collapse_common_offset_anchor.md) | 父级/平铺问题 | 共同偏移是否决定均匀任务的崩塌？ |
| 2.3 | [A05_04_02](../Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_02_dotproduct_common_logit_causality_anchor.md) | 父级/平铺问题 | 共同打分对点积路由有何因果作用？ |
| 2.4 | [A05_04_03](../Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_03_real_text_common_logit_initialization_anchor.md) | 父级/平铺问题 | 真实文本初始化由共同项主导吗？ |
| 2.5 | [A01_04](../Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_04_feedback_common_preservation_bridge_anchor.md) | 父级/平铺问题 | 共同分量能否解释反馈与分区保持？ |
| 2.6 | [A05_01](../Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md) | 父级/平铺问题 | 几何抑制能否阻止路由集中？ |
| 2.7 | [A05_02](../Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md) | 父级/平铺问题 | 放松特征假设后抑制法仍有效吗？ |
| 2.8 | [A05_04_01](../Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_01_uniform_feature_specialization_after_position_removal_anchor.md) | 父级/平铺问题 | 去掉位置后能否学成特征分工？ |
| 2.9 | [A06_01](../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md) | 父级/平铺问题 | 能否发现并保持可用的状态分区？ |
| 2.10 | [A06_02](../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md) | 父级/平铺问题 | 哪些动力学使分区保持或翻转？ |
| 2.11 | [A15_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/15_01_spectral_learning_and_feedback_dynamics_anchor.md) | 父级/平铺问题 | 谱学习速度与专家反馈如何形成锁定？ |
| 2.11.1 | [A15_01_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_01_selected_expert_feedback_lockin_anchor.md) | 子问题 | 只更新所选专家会否锁死发现过程？ |
| 2.11.2 | [A15_01_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_01_spectral_learning_and_feedback_dynamics/subanchors/15_01_02_low_variance_functional_delay_anchor.md) | 子问题 | 低方差方向是随机还是学得慢？ |

## 3. 共享更新、优化与干扰

一次更新何时帮助或伤害另一目标，哪些优化过程造成差异？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 3.1 | [A07](../Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07.md) | 父级/平铺问题 | 嵌套共同骨架能否解释干扰与分路？ |
| 3.2 | [A07_01](../Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md) | 父级/平铺问题 | 嵌套分布能否形成稳定共同骨架？ |
| 3.3 | [A07_02](../Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md) | 父级/平铺问题 | 控制共同子空间能否改善尾部学习？ |
| 3.4 | [A07_03](../Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md) | 父级/平铺问题 | 正确嵌套分路是否对应专家功能？ |
| 3.5 | [A07_04](../Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md) | 父级/平铺问题；L1 | 分路能否减少共同—稀有梯度冲突？ |
| 3.6 | [A07_05](../Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_05_common_update_interference_diagnostic_anchor.md) | 父级/平铺问题 | 共同更新是否实际伤害稀有目标？ |
| 3.7 | [A07_06](../Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_06_projected_common_rare_conflict_splitting_anchor.md) | 父级/平铺问题 | 投影分路收益是否由冲突降低解释？ |
| 3.8 | [A10_01](../Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_01_common_projected_sgd_lr_anchor.md) | 父级/平铺问题 | 移除共同方向能否提高稳定学习率？ |
| 3.9 | [A10_02](../Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_02_frequency_singular_sgd_instability_anchor.md) | 父级/平铺问题 | 频率谱是否造成随机梯度下降不稳定？ |
| 3.10 | [A16_00](../Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/16_00_switch_lb_gradient_conflict_anchor.md) | 父级/平铺问题 | 负载均衡梯度是否与任务学习冲突？ |
| 3.10.1 | [A16_00_01](../Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor.md) | 子问题 | 共同均值是否维持已经形成的路由崩塌？ |
| 3.10.2 | [A16_00_02](../Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_02_multistage_gradient_pathway_anchor.md) | 子问题 | 中心化是否在所有训练阶段降低干扰？ |
| 3.11 | [草案 D1 · 0924](../Projects/from-attention-to-search/main/problem_anchors/shared_updates/shared_parameter_interference/anchor_cn.md) | 草案，归属待确认 | 共享参数更新是否产生可分离的域间干扰？ |
| 3.12 | [草案 D2 · 0925](../Projects/from-attention-to-search/main/problem_anchors/shared_updates/update_compatibility/anchor_cn.md) | 草案，归属待确认 | 可分任务是否存在稳定的负兼容更新对？ |
| 3.13 | [草案 D3 · 0925](../Projects/from-attention-to-search/main/problem_anchors/shared_updates/human_semantic_updates/anchor_cn.md) | 草案，归属待确认 | 人类语义距离能否预测共享更新代价？ |

## 4. 监督信号与任务必要性

更早的任务相关监督，何时真正改变后续答案计算？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 4.1 | [A11_01](../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/11_01_informative_horizon_supervision_anchor.md) | 父级/平铺问题 | 更远监督何时提供有效学习信号？ |
| 4.1.1 | [A11_01_01](../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_informative_horizon_supervision/subanchors/11_01_01_information_and_geometry_controls_anchor.md) | 子问题 | 信息量与输出几何能否分开？ |
| 4.2 | [A11_02](../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/11_02_hidden_to_parameter_transmission_anchor.md) | 父级/平铺问题 | 隐状态收益能传到实际参数更新吗？ |
| 4.2.1 | [A11_02_01](../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_02_hidden_to_parameter_transmission/subanchors/11_02_01_reachability_and_background_sign_anchor.md) | 子问题 | 传递失败来自不可达还是背景抵消？ |
| 4.3 | [A11_03](../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/11_03_cross_position_standard_head_use_boundary_anchor.md) | 父级/平铺问题 | 学到的状态是否被后续标准输出头使用？ |
| 4.3.1 | [A11_03_01](../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_01_cross_position_proxy_falsification_anchor.md) | 子问题 | 跨位置代理指标是否真的测到使用？ |
| 4.3.2 | [A11_03_02](../Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_cross_position_standard_head_use_boundary/subanchors/11_03_02_standard_head_causal_use_anchor.md) | 子问题 | 更严格干预能否证明标准头因果使用？ |
| 4.4 | [A12_01](../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/12_01_compositional_workload_capability_gate_anchor.md) | 父级/平铺问题；P4 | 两步组合任务是否适合比较学习目标？ |
| 4.4.1 | [A12_01_01](../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/subanchors/12_01_01_workload_validity_and_learner_guard_anchor.md) | 子问题；P4 | 失败来自任务不合法还是学习器不足？ |
| 4.5 | [A12_02](../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_02_interference_capacity_curriculum_boundary/12_02_interference_capacity_curriculum_boundary_anchor.md) | 父级/平铺问题 | 干扰、容量与课程各限制什么？ |
| 4.5.1 | [A12_02_01](../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_02_interference_capacity_curriculum_boundary/subanchors/12_02_01_rank_and_curriculum_controls_anchor.md) | 子问题 | 秩和课程对照能否隔离容量解释？ |
| 4.6 | [A12_03](../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md) | 父级/平铺问题 | 组合中间态是否被标准头因果使用？ |
| 4.7 | [A12_0](../Projects/from-attention-to-search/main/problem_anchors/12_structured_compositional_mtp_workload/12_0_short_range_single_vs_two_step_composition/12_0_short_range_single_vs_two_step_composition_anchor.md) | 父级/平铺问题；P4 | 短距一步与两步组合能否形成合格对照？ |
| 4.8 | [A13_00](../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/13_00_task_properties_to_standard_head_utility_anchor.md) | 父级/平铺问题；L2 | 什么任务属性使中继表征具有功能？ |
| 4.8.1 | [A13_00_01](../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_01_query_conditioned_relay_carrier_anchor.md) | 子问题；P4 | 带查询绑定的中继能否稳定学会？ |
| 4.8.2 | [A13_00_02](../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_02_single_value_relay_carrier_anchor.md) | 子问题；P4 | 简化为单值中继后载体是否合格？ |
| 4.8.3 | [A13_00_03](../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_03_relay_necessity_objective_interaction_anchor.md) | 子问题 | 中继必要性是否改变训练目标收益？ |
| 4.8.4 | [A13_00_04](../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_04_relay_target_localization_anchor.md) | 子问题 | 把监督放在中继位置是否足够？ |
| 4.8.5 | [A13_00_05](../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_05_task_relevant_relay_target_anchor.md) | 子问题；L2 | 任务相关性是否比无关监督更关键？ |
| 4.8.6 | [A13_00_06](../Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_06_soft_relay_mtp_ntp_audit_anchor.md) | 子问题；P4 | 软中继能否区分多步与下一词目标？ |

## 5. 频率、复用与低维结构

低维结构来自频率、函数复用，还是构造中的先验假设？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 5.1 | [A04](../Projects/from-attention-to-search/main/problem_anchors/09_common_rare_spectral_discrimination/04_ntp_zipf_feature_factorization_anchor.md) | 父级/平铺问题 | 频率偏斜影响路由还是特征写入？ |
| 5.2 | [A09_01](../Projects/from-attention-to-search/main/problem_anchors/09_common_rare_spectral_discrimination/09_01_common_band_rare_discrimination_anchor.md) | 父级/平铺问题 | 共同高方差方向是否保留稀有判别？ |
| 5.3 | [A14_00](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md) | 父级/平铺问题 | 层级语言结构为何可能带来低秩？ |
| 5.4 | [A14_01](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_01_relation_reuse_parameter_state_bridge/14_01_relation_reuse_parameter_state_bridge_anchor.md) | 父级/平铺问题 | 关系复用能否连接状态秩与参数秩？ |
| 5.5 | [A14_02](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md) | 父级/平铺问题 | 共享规则是否降低任务所需状态秩？ |
| 5.5.1 | [A14_02_01〔现版〕](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_01_frequency_mapping_rank_separation_anchor.md) | 子问题 | 固定映射后频率本身是否必然增加秩？ |
| 5.5.2 | [A14_02_02〔现版〕](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_02_rare_common_subspace_reuse_anchor.md) | 子问题 | 稀有更新是否复用共同参数子空间？ |
| 5.6 | [A14_03](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_03_state_parameter_functional_rank_demand/14_03_state_parameter_functional_rank_demand_anchor.md) | 父级/平铺问题 | 状态低秩能否推出参数功能低秩？ |
| 不重编号 | [A14_02_01〔旧版归档〕](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor.md) | 历史保留；P5 | 已见组件能否可靠组合成未见配对？ |
| 不重编号 | [A14_02_02〔旧版归档〕](../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e03_v0_low_frequency_common_mapping_rank/14_02_02_low_frequency_common_mapping_rank_anchor.md) | 历史保留；P5 | 低频调用是否还使用已学共同映射？ |

## 6. 表征结构与测量边界

哪些层、谱位置、方向和长度差异可以稳定测到？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 6.1 | [A15_00](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/15_00_router_input_spectral_geometry_anchor.md) | 父级/平铺问题 | 真实路由输入偏好哪些方差方向？ |
| 6.1.1 | [A15_00_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_01_cross_document_subspace_stability_anchor.md) | 子问题 | 共同子空间能否跨文档稳定存在？ |
| 6.1.2 | [A15_00_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_02_gate_common_residual_preference_anchor.md) | 子问题 | 门控更偏好共同还是残差方向？ |
| 6.1.3 | [A15_00_03](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_00_router_input_spectral_geometry/subanchors/15_00_03_condition_local_residual_modes_anchor.md) | 子问题 | 不同条件有互不兼容的残差空间吗？ |
| 6.2 | [A15_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md) | 父级/平铺问题 | 语义粒度如何随层和谱位置改变？ |
| 6.2.1 | [A15_02_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_01_controlled_layer_information_identity_anchor.md) | 子问题 | 受控组合信息究竟出现在哪层哪带？ |
| 6.2.2 | [A15_02_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_02_natural_hierarchy_role_localization_anchor.md) | 子问题 | 同一概念当父/子角色时位置会变吗？ |
| 6.2.3 | [A15_02_03](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_03_architectural_head_channel_concentration_anchor.md) | 子问题 | 语义集中在真实注意力头还是任意通道？ |
| 6.2.4 | [A15_02_04](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_04_compositional_attention_write_atlas_anchor.md) | 子问题 | 更多组合步骤是否使注意力写入移向尾部？ |
| 6.2.5 | [A15_02_05](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_05_balanced_taxonomy_attention_write_atlas_anchor.md) | 子问题 | 平衡粗细标签后细粒度是否额外右移？ |
| 6.2.6 | [A15_02_06](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_06_mlp_parameter_geometry_and_semantic_location_anchor.md) | 子问题 | 参数共同性与语义位置能否组成机制？ |
| 6.2.7 | [A15_02_07](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_07_matched_semantic_complexity_anchor.md) | 子问题 | 匹配复杂度后仍有细语义谱迁移吗？ |
| 6.3 | [A15_04](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor.md) | 父级/平铺问题 | 局部右移是否进入跨层共享尾部？ |
| 6.4 | [A15_09](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/15_09_layerwise_coarse_fine_reuse_geometry_anchor.md) | 父级/平铺问题 | 粗细判别方向是否稳定复用？ |
| 6.4.1 | [A15_09_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/subanchors/15_09_01_native_g_domain_consensus_variance_atlas_anchor.md) | 子问题 | 原生路由空间是否有跨域共同方向？ |
| 6.5 | [A15_14](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_14_semantic_representation_geometric_form/15_14_semantic_representation_geometric_form_anchor.md) | 父级/平铺问题 | 自然领域语义主要在方向、长度还是形状？ |
| 不重编号 | [A15_03〔归档〕](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/archive/15_03_middle_band_information/15_03_middle_band_information_anchor.md) | 历史保留；P5 | 中部谱稳定是真结构还是平均假象？ |

## 7. 信息增量、使用与迁移

额外可读的信息有多少，能否被使用或迁移？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 7.1 | [A15_07](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md) | 父级/平铺问题 | 监督低维方向能否跨表达保留功能？ |
| 7.1.1 | [A15_07_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/subanchors/15_07_01_layerwise_domain_direction_atlas_anchor.md) | 子问题 | 不同领域方向的层间位置和共享度怎样？ |
| 7.2 | [A15_08](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor.md) | 父级/平铺问题；L6, L7, P3 | 层增量提供了旧状态之外什么信息？ |
| 7.2.1 | [A15_08_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_01_layerwise_long_range_compositional_innovation_anchor.md) | 子问题 | 深层是否增加长距组合的可读信息？ |
| 7.2.2 | [A15_08_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md) | 子问题 | 哪些层增加条件细粒度可读性？ |
| 7.2.3 | [A15_08_03](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_03_function_admitted_update_representation_rank_anchor.md) | 子问题；L5 | 功能增量是否处于稳定低秩空间？ |
| 7.2.4 | [A15_08_04](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_04_transition_object_spectrum_sensitivity_anchor.md) | 子问题 | 低秩外观是否由对象定义和归一化造成？ |
| 7.2.5 | [A15_08_05](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_05_aligned_geometric_rank_scale_anchor.md) | 子问题 | 统一模型、样本和指标后秩差还在吗？ |
| 7.2.6 | [A15_08_06〔8B复现〕](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_qwen8b_geometric_rank_replication_anchor.md) | 子问题 | 大模型是否复现宽谱与对象差异？ |
| 7.2.7 | [A15_08_06〔语义子空间〕](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_semantic_conditioned_functional_subspace_anchor.md) | 子问题 | 语义条件能否揭示局部与共享功能维度？ |
| 7.2.8 | [A15_08_09](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md) | 子问题 | 随机投影能保住已有线性语义结构吗？ |
| 7.3 | [A15_10](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_10_cross_parent_fine_function_transfer/15_10_cross_parent_fine_function_transfer_anchor.md) | 父级/平铺问题 | 一个父类的细粒度功能能转移到另一父类吗？ |
| 7.4 | [A15_12](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_12_semantic_representation_separability/15_12_semantic_representation_separability_anchor.md) | 父级/平铺问题 | 相同事实换表达后能否共用分类边界？ |
| 7.5 | [A15_16](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_16_headwise_causal_semantic_retrieval/15_16_headwise_causal_semantic_retrieval_anchor.md) | 父级/平铺问题 | 不同注意力头是否承担不同粗细语义角色？ |

## 8. 稀疏自编码约束与表征变化

SAE 条件下，集中和复用变化伴随什么信息变化？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 8.1 | [A15_17](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md) | 父级/平铺问题 | 旁路自编码约束如何改变可复用表征？ |
| 8.1.1 | [A15_17_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md) | 子问题 | 更集中是否因为反复使用相同稀疏特征？ |
| 8.1.2 | [A15_17_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md) | 子问题 | 更集中是否伴随更好原生领域区分？ |

## 9. 表征坐标驱动的路由方法

谱带、接力和增量坐标，是否有超出匹配对照的分流价值？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 9.1 | [A15_05](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/15_05_functional_coordinate_admission_anchor.md) | 父级/平铺问题 | 谱坐标能否获准用于专家分流？ |
| 9.1.1 | [A15_05_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_01_shallow_feature_guidance_anchor.md) | 子问题 | 浅层特征能否指导深层专家？ |
| 9.1.2 | [A15_05_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_02_shallow_feature_specificity_pilot_anchor.md) | 子问题 | 浅层头部指导试验能否排除随机坐标？ |
| 9.1.3 | [A15_05_03](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_03_progressive_band_source_routing_anchor.md) | 子问题；L3, P1 | 逐层头—中—尾分流能改善训练吗？ |
| 9.1.4 | [A15_05_04](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_04_fixed_band_cross_update_compatibility_anchor.md) | 子问题 | 非头部几何能额外预测共同训练兼容性吗？ |
| 9.1.5 | [A15_05_05](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_05_functional_coordinate_admission/subanchors/15_05_05_matched_fixed_band_dispatch_anchor.md) | 子问题；P1 | 固定谱带分流在匹配训练中是否有益？ |
| 9.2 | [A15_06](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/15_06_online_spectral_routing_and_relay_anchor.md) | 父级/平铺问题；L4, P2 | 在线谱追踪与跨层接力能改善路由吗？ |
| 9.2.1 | [A15_06_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_01_local_random_identity_control_anchor.md) | 子问题；P2 | 谱身份是否比同样运动的随机空间更好？ |
| 9.2.2 | [A15_06_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_06_online_spectral_routing_and_relay/subanchors/15_06_02_router_expert_specialization_anchor.md) | 子问题；P2 | 谱路由是否更会利用非同质专家？ |
| 9.3 | [A16_01](../Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/16_01_incremental_information_lb_routing_anchor.md) | 父级/平铺问题 | 真实负载均衡下新增信息路由能改善训练吗？ |
| 9.3.1 | [A16_01_01](../Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_01_incremental_information_lb_routing/subanchors/16_01_01_regret_distilled_conditional_innovation_anchor.md) | 子问题 | 专家遗憾值蒸馏能否给增量路由功能资格？ |

## 10. 语义与效用监督的路由方法

指定分组的价值能否变成可学习的路由和专家结构？

| 拟编号 | 旧编号与原文 | 身份 / 审阅项 | 问题 |
|---|---|---|---|
| 10.1 | [A15_11](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md) | 父级/平铺问题 | 效用监督能否驱动残差专家树增长？ |
| 10.2 | [A15_13](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md) | 父级/平铺问题 | 末层语义能否组织更有效的中层专家？ |
| 10.2.1 | [A15_13_01](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_01_clinc150_one_layer_backward_hierarchical_router_anchor.md) | 子问题 | 末层向中层的监督链改善意图表征吗？ |
| 10.2.2 | [A15_13_02](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_02_frozen_base_staged_semantic_lora_router_anchor.md) | 子问题 | 冻结底座的分阶段层级能改善细意图吗？ |
| 10.2.3 | [A15_13_03](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_03_semantic_gradient_functional_alignment_anchor.md) | 子问题 | 真实意图分组是否有梯度和任务价值？ |
| 10.2.4 | [A15_13_04](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md) | 子问题 | 语义分组价值能否扩展到语言建模？ |
| 10.2.5 | [A15_13_05](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md) | 子问题 | 充分匹配训练后语义监督仍额外有效吗？ |
| 10.2.6 | [A15_13_06](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_06_dclm_final_layer_topk_sae_teacher_anchor.md) | 子问题 | 最终层稀疏自编码器能成为合格教师候选吗？ |
| 10.2.7 | [A15_13_07](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_07_true_label_layerwise_static_audit_anchor.md) | 子问题 | 真实粗细标签在什么层稳定可读？ |
| 10.2.8 | [A15_13_08](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_08_dclm_sae_candidate_hierarchy_anchor.md) | 子问题 | 自编码特征包含关系能否跨数据复现？ |
| 10.2.9 | [A15_13_09](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_09_dataset_conditioned_sae_semantic_hierarchy_anchor.md) | 子问题 | 激活包含图是否对应粗细语义分类？ |
| 10.2.10 | [A15_13_10](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md) | 子问题 | 自编码/聚类结构正则能改善在线路由吗？ |
| 10.2.11 | [A15_13_11](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_11_structural_routing_incremental_learning_anchor.md) | 子问题 | 结构路由能否支持增量学习和局部增长？ |
| 10.3 | [A15_15](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md) | 父级/平铺问题 | 静态可读性是否决定最佳专家插入层？ |

