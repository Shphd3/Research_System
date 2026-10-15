# A17 R03 机制实验完整阅读包

派生读本：只调整引用，不更改研究结论、审批或 Unknown。

先读完整组会稿，再读 R03 Summary/Detailed，最后核对协议与证据表。

- [A17 R02 组会汇报：新规则为什么会改坏旧规则？](documents/daily_research_reports/1012/meeting_report/a17_r02_mechanism_meeting_cn.md)
- [A17 R02 meeting script: why does learning a new rule damage the old rule?](documents/daily_research_reports/1012/meeting_report/a17_r02_mechanism_meeting.md)
- [实验总结：A17_04_E01 R03，反转迁移的有限机制审计](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R03_mechanism_audit/summary_cn.md)
- [Summary: A17_04_E01 R03 finite mechanism audit of reversed transfer](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R03_mechanism_audit/summary.md)
- [实验详细记录：A17_04_E01 R03，反转迁移机制审计](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R03_mechanism_audit/detailed_cn.md)
- [Detailed: A17_04_E01 R03 finite mechanism audit](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R03_mechanism_audit/detailed.md)
- [Detailed：A17_04_E01 R02 单层 AdamW 条件映射迁移](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/detailed_cn.md)
- [Protocol：A17_04_E01 R02 单层 AdamW 条件映射迁移](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/protocol_cn.md)
- [实验总结：A17_04_E01 R02 单层 AdamW 条件映射迁移](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary_cn.md)
- [执行契约：A17_04_E01 R03，已有 R02 的有限机制审计](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R03_mechanism_audit/protocol_cn.md)
- [实验总结：A17_04_E03 单层 Attention 获取诊断](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/summary_cn.md)
- [条件映射变化与跨任务学习](documents/Projects/from-attention-to-search/main/focus/focus_conditional_mapping_transfer_cn.md)
- [A17_04：条件映射变化与跨任务学习](documents/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor_cn.md)
- [项目研究入口](documents/Projects/from-attention-to-search/main/roadmap_cn.md)
- [Detailed: A17_04_E01 R02 single-layer AdamW mapping transfer](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/detailed.md)
- [Protocol: A17_04_E01 R02 single-layer AdamW mapping transfer](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/protocol.md)
- [Summary: A17_04_E01 R02 single-layer AdamW mapping transfer](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md)
- [Protocol: A17_04_E01 R03 finite mechanism audit of R02](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R03_mechanism_audit/protocol.md)
- [Summary: A17_04_E03 single-attention acquisition](documents/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/summary.md)
- [Conditional mapping transfer](documents/Projects/from-attention-to-search/main/focus/focus_conditional_mapping_transfer.md)
- [A17_04: Conditional mapping transfer](documents/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md)
- [Research roadmap](documents/Projects/from-attention-to-search/main/roadmap.md)

## Selected evidence / 精选证据

五张图为同一 System 仓库中的精确交付副本，来源固定到项目提交 `839cdf5585744115903a0a526f7adb3fafd98f1c`；七张表完整保留 CSV 数值，另附小型审计及来源记录。原始权重、表征数组和逐样本预测没有上传。

- [execution_certificate.md](selected_provenance/execution_certificate.md)
- [01_data_construction.png](../../../../sync/1012_a17_mechanism_evidence/01_data_construction.png)
- [02_early_trajectory.png](../../../../sync/1012_a17_mechanism_evidence/02_early_trajectory.png)
- [03_matrix_interventions.png](../../../../sync/1012_a17_mechanism_evidence/03_matrix_interventions.png)
- [04_weight_interpolation.png](../../../../sync/1012_a17_mechanism_evidence/04_weight_interpolation.png)
- [05_representation_bridge.png](../../../../sync/1012_a17_mechanism_evidence/05_representation_bridge.png)
- [comprehensive_audit.json](selected_provenance/comprehensive_audit.json)
- [figure_provenance.json](selected_provenance/figure_provenance.json)
- [finite_outputs_audit.json](selected_provenance/finite_outputs_audit.json)
- [full_registration_receipt.json](selected_provenance/full_registration_receipt.json)
- [mapping_audit_results.json](selected_provenance/mapping_audit_results.json)
- [meeting_reading_audit.json](selected_provenance/meeting_reading_audit.json)
- [r02_posthoc_rule_choice.json](selected_provenance/r02_posthoc_rule_choice.json)
- [r02_results.json](selected_provenance/r02_results.json)
- [representation_analysis.json](selected_provenance/representation_analysis.json)
- [source_R02_end_verification.json](selected_provenance/source_R02_end_verification.json)
- [delta_stats.csv](selected_tables/delta_stats.md)
- [full_interpolation_compatibility.csv](selected_tables/full_interpolation_compatibility.md)
- [full_parameter_rollback.csv](selected_tables/full_parameter_rollback.md)
- [r02_trajectories_by_seed_panel.csv](selected_tables/r02_trajectories_by_seed_panel.md)
- [r02_trajectories_equal_seed_means.csv](selected_tables/r02_trajectories_equal_seed_means.md)
- [representation_per_record.csv](selected_tables/representation_per_record.md)
- [representation_signed_response.csv](selected_tables/representation_signed_response.md)

[来源、精确字节与读本哈希](manifest.json) · [未选入的依赖](UNAVAILABLE.md)
