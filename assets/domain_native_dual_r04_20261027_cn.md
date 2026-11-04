# R04两套原生字典的领域分析资产

固定数据ID `data_a15_27_r04_domain_native_dual_20261027`，实际激活与分析ID `analysis_a15_27_r04_native_sae_joint_cc_domain_20261027`。[一页结论](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/summary_cn.md)；[本次选择性访问检查](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/provenance/output_access.json)。

E16读取block27 MLP输入，FP32原生Top32；A22用14层原共享z，最后层贡献=z×decoder27范数×TRAIN RMS27，不能说成最后层独立编码。两套同Base字节、tokenizer和文本，候选/验证独立。实际456/512条，120文档、72受控前缀、256DCLM窗口（65536位置、254文档组）。

领域使用和固定读出在本留出复现，但固定目标组级确认不足。来源/词面/中性前导语/编辑量与稀疏支持限制结论。登记实际数据，不代表自然簇、机制或功能通过；无新模型/字典训练、资源、Attention、谱、干预、重聚类或封存TEST。
