# CrossCoder阶段一：1014讨论文件包

这是既有阶段一结果的派生读本，仅将引用改成可携带路径，保留审批、Unknown和结论边界。

建议阅读顺序：

1. [1014讨论入口](../../meeting_report/meeting_brief_crosscoder_feature_phase1_cn.md)
2. [一页中文总结](documents/summary_cn.md)／[English Summary](documents/summary.md)
3. [候选指标](selected_tables/candidate_metrics.md)、[完整局部图与14层热图](figures_cn.md)、[随机与高激活文本](pair_examples_cn.md)
4. [完整记录](documents/detailed_cn.md)／[English Detailed](documents/detailed.md)
5. [Protocol](documents/protocol_cn.md)／[English Protocol](documents/protocol.md)、[原Anchor](documents/anchor.md)

证据： [候选及分块指标](selected_provenance/pair_metrics.json)、[Top10逐个删除](selected_provenance/sensitivity.json)、[层贡献原始数值](selected_tables/layer_contribution.md)、[空列表J=0诊断](selected_tables/empty_list_J0_diagnostics.md)、[完成核对](selected_provenance/completion_audit.json)、[来源清单](manifest.json)。

图片在同仓库sync/1014_crosscoder_feature_phase1_evidence中，通过相对路径引用。完整仓库克隆无需执行机即可阅读。可下载zip会把图放入包内；正式Markdown、数值及图源一致。

关键边界：同bin复核、文档独立性未知；高J共同项87.5%为Top10；J高不等于直接共激活或学习收益。0/3无both，1/17仅2例，按实交付。四对不是独立重复。阶段一已停止。

未包含：模型权重、激活缓存、完整共同计数矩阵、120,380,886对全池数组、全量图／全节点及原始日志；这些是执行侧资产。见[外部依赖](EXTERNAL_DEPENDENCIES.md)，不伪称本包携带它们。
