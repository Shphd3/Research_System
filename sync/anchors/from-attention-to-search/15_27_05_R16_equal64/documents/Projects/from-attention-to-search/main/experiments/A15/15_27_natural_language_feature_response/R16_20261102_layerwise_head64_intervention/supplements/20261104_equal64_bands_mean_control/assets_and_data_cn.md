派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/assets_and_data_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/assets_and_data_cn.md)；研究修改仍回到原件。

---

# 资产、数据与原始结果入口

模型：Qwen3-0.6B Base官方checkpoint，路径/data/250010109/model_cache/Qwen3-0.6B-Base-official。权重SHA256：cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba。tokenizer及模型绑定不变，不使用Dense。原资产ID：model_qwen3_0p6b_base_official_a5、tokenizer_qwen3_0p6b_base_official_a5、analysis_a15_27_05_layerwise_head64_intervention_20261102。当前输入可读检查见audit/input_access.json，读通不代替数值重放。

PCA与数据原载体：/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/data。bases/layer01.npz至layer28.npz逐层包含mean(1024)、V(1024,1024)、eigenvalues(1024)、n等；每层均为同60篇TRAIN文档9600位置。无评估拟合、无新谱基；本轮不是独立PCA复现。positions.jsonl为737位置及完整可见前文、后继ID、0基位置；evaluation_documents.jsonl为180篇物理文档的192-token窗口。175篇自然面板700位置和37篇the面板分开分析。旧头64、均值和随机参照在原R16结果中复用。

本轮执行目录：/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control。

- analysis/chunks/*.npz：每篇文档全部条件。ints和floats为逐行对齐矩阵，字段名另存int_fields/float_fields。top10_ids与top10_probs形状为(本篇条件位置数,10)，同行对应；condition_names给出条件编号。首选token精确ID位于ints，完整输入用index连接positions.jsonl。完整性与版本由freeze_sha256绑定。
- analysis/position_metrics.csv.gz：逐位置完整数值。
- analysis/document_metrics.csv.gz：文档内汇总；source区分NEW与R16_REUSED_EXACT。
- analysis/summary_metrics.csv：全部层/段/均值形式/范围/分组，含文档数及逐点区间。
- analysis/paired_mean_effect.csv：同一段加均值减不加均值的配对差。
- analysis/paired_head_vs_band.csv：等维头64减其他段的配对差。
- analysis/paired_band_vs_baseline.csv：加均值段减仅均值；不加均值段减零向量。它们不是语义信息百分比。
- analysis/fixed_case_outputs.jsonl、fixed_mean_only_outputs.jsonl：旧9例所有层的前10候选，后者为旧均值控制复用。完整前文和固定4层读数见casebook_cn.md。
- analysis/CPU_geometry.csv、CPU_rounding_diagnostic.csv：范数几何与理想向量BF16舍入诊断，未增加模型前向。

读者从summary_cn.md看结果，matrix_cn.md逐项核对16段，再到casebook_cn.md核对输入与输出。audit/validation.json在完整计算后记录实际核查，completion_manifest.json记录实际数量与资源；未生成前不表示完成。

Output asset: `analysis_a15_27_05_equal64_bands_mean_control_20261104`; current selected input/output access check: [audit/output_access.json](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/audit/output_access.json). Actual unique rows1,403,985 plus9,525 preserved repair-version rows; all737 oldhead comparisons exact.
