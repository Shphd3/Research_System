# R02：匹配参考频率、面板缓存与分析资产

[一页结论](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/summary_cn.md) · [完整清单](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/artifact_manifest_cn.md) · [严格访问快照](checks/20261027_natural_language_feature_r02_outputs.json)

复用official Qwen3-0.6B与原生E16 FP32 Top32字典，模型/字典哈希、hook和实际计算见[资产核验](../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/asset_audit_cn.md)。不训练新字典。CrossCoder只复用其独立配套模型/共享z旧缓存，不与E16编号对齐。

| ID | 实际保存对象 | 资格与用途 |
| --- | --- | --- |
| `data_natural_language_feature_panel_r02_20261026` |12基础情境、120受控编辑序列及token/配对/距离清单 |文本资格通过；不是原样自然语料 |
| `data_e16_fp32_reference_windows_r02_20261026` |1024固定TRAIN窗口 |窗口输入；频率另存下项 |
| `reference_e16_fp32_dclm_r02_20261026` |245760位置的原计数/逐窗计数 |匹配BF16模型/FP32编码/Top32；仅估计固定窗口语料，低支持保留NA |
| `representation_natural_language_feature_r02_20261026` |120序列、360位置的z/尺度校正贡献/候选读数 |重构通过，但前缀数值资格FAIL；不能用于本轮确认性结论 |
| `analysis_natural_language_feature_r02_20261026` |冻结组、全流程空模型、三问题统计与图 |Q1/Q2/Q3均INSUFFICIENT；不提升为专家或功能证据 |

payload保留执行侧`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/`。三项输出严格访问通过只证明当前可访问和身份记录完整，不改变失败与证据不足。R02前向1160条，加R01共1452/1500。
