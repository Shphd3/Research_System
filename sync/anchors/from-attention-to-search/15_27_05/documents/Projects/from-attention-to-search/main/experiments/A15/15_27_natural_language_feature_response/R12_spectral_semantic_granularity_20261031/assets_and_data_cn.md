派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031/assets_and_data_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031/assets_and_data_cn.md)；研究修改仍回到原件。

---

# 本轮资产与数据读取口径

Owner: A15_27_05 / R12. Execution root: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R12_spectral_semantic_granularity_20261031`.

原始h/z来自R11已登记缓存；本轮没有模型前向。A22是14层联合编码、共享z；用最后block27模型尺度decoder重构。只读访问通过不等于重新加载／重新哈希了5.6GB权重。原端点哈希及接口由旧生产记录绑定，当前缓存、谱和decoder文件哈希另存。

- model_qwen3_0p6b_base_official_a5
- tokenizer_qwen3_0p6b_base_official_a5
- crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013
- analysis_a15_27_03_r09_domain_difference_decomposition_20261029
- analysis_a15_27_04_r10_domain_member_atlas_20261030
- data_a15_27_r11_qualified_three_domain_A02_20261030
- representation_a15_27_r11_A02_dv_native_jointz_h27_20261030
- representation_a15_27_r11_A02_h_native_jointz_h27_20261030

主面板100候选→96文档／96位置；39／20／37原分割；每个目标token279，位置96–191末次。含混细标签不跨任务偷换。旧H不是新盲确认。

[Exact input IDs](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031/provenance/asset_inputs.json) · [Coverage](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031/evidence/coverage.csv) · [Result](summary_cn.md)

复用已有谱不构成独立复现；CrossCoder同时读取14层，重构可访问性不等于最后层独立编码质量。原始大数组、模型和字体不进入阅读包。

block27实际TRAIN RMS为 **374.349512102**。14个选定层的实际RMS、TRAIN均值形状／哈希、R09尺度逐值核对及原生门控说明保留在[asset_inputs.json](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R12_spectral_semantic_granularity_20261031/provenance/asset_inputs.json)。本轮没有用评估数据重新估计归一化。
