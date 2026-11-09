# 数据、统计和缺项附录

新增模型前向0，训练0，领域角色重选0，新Work/Codex任务0；R04/R05前向台账SHA未变。原120篇文档身份与两字典完整CSR/z精确一致，主统计40篇原留出，数学/生物各20独立文档组。

主指标逐位置计算，随后head/query/document等权；八个指标×两域×两字典×三个固定对比=96主检验合并BH。区间/效应而非仅显著性见下列文件。没有按结果换head、feature、距离或语义标签；其它分层与强度仅描述。模型输出预测、功能干预、POS词性、信息传递本轮未测。

- [完整主对比与辅助对比](tables/paired_contrasts.csv)
- [全部组成均值及文档区间](tables/composition_means.csv)
- [所有64冻结成员的逐领域/组命中率](tables/frozen_feature_hits/README.md)
- [角色成员覆盖与集中度（描述性）](tables/role_member_coverage_descriptive.csv)
- [逐文档共同支持](tables/support_by_document.csv)与[汇总支持](tables/support_summary.csv)
- [实际Attention/距离分位数与pair数](tables/pooled_attention_distance_distributions.csv)
- [文档等权Attention/距离/token形态/独立tokenID频率](tables/document_weighted_diagnostics.csv)
- [空白token辅助诊断](tables/whitespace_document_weighted.csv)
- [例子的全部活跃feature/z/贡献](tables/example_all_active_features.csv)
- [逐前文位置完整组成](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/source_position_composition.csv)
- [全部实际配对及token/probability/distance诊断](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/pair_diagnostics.csv)
- [输入/原缓存身份逐项检查](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/analysis/cache_identity.json)
- [逐文档可复算统计数组](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/analysis/document_values.npz)
- [独立权重/零位置/BH检查](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/analysis/audit.json)
- [全部96项效应/p独立重算与源哈希守卫](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/analysis/final_audit.json)
- [工程修订与原失败日志](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/engineering_repairs.json)
- [实际统计源代码](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/analyze_endpoints.py)

在已有源端位置中，零激活位置SAE=0、CC=0；实现另用全零虚拟矩阵验证“总数0、占比NA、成员命中率0”，没有把NA当0。SAE32是门控事实，不是信息量相等。

主例子只显示原顺序前12R04候选及4个最小数字ID源独有坐标，未看效应挑选，全部64角色图及完整活跃清单另附。图4远高是段落换行，不能用查询之后的单配/遗传检测解释当前读数。来源/术语/位置/字符类未完全控制；高是档内排名，近远概率量级不同。

这些补充是探索性来源端组成，既不重判原R04/R05/R06，也不将R06候选外推领域。没有额外推断训练/专家/自然簇/长短程分工。用户机制接受与下一问题Unknown。


原40篇“留出”已用于R04/R05，不是这次新增的独立确认数据。本轮明确标探索性。逐文档来源、子体裁和规范文档组见[文档清单](tables/document_manifest.csv)，原频率组全坐标ID/角色ID/原生贡献范数另存group_coordinate_ids.npz；没有重新按当前面板分组。
