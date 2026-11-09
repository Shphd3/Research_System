# R04交付与证据清单

- 结论/完整过程：`summary_cn.md`、`detailed_cn.md`；冻结协议/对象：`protocol_cn.md`、`objects_and_settings_cn.md`。
- 图与实例：3张PNG（PDF在执行侧及讨论包内）、`figures_cn.md`、`examples_cn.md`；完整120+72输入：`texts_cn.md`。
- 精确数字：`tables/results.json`、两字典候选/方向/逐feature统计与CSV；原始逐token稀疏z、参考计数、原空间decoder尺度、分类器/随机组/置换值留在 `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027`，附录给出字段。
- 小证据payload例外逐项列于`selected_provenance_manifest.json`；完整hash在`artifact_manifest.json`及执行侧`execution_manifest.json`。原始模型与字典未复制、未改动。
- 数据ID：`data_a15_27_r04_domain_native_dual_20261027`；实际缓存/分析ID：`analysis_a15_27_r04_native_sae_joint_cc_domain_20261027`；当前选择性访问检查见`provenance/output_access.json`。
- 实际456/512条；8条重放/前缀检查通过，52项原始数据核查与40项独立统计核查通过；只修复一次进度JSON序列化并重用已完成检查。没有新增模型/字典训练，未用剩56条扩样。
- 本地交付与reading sync，不代表已推送/发布或机制验收；旧R01/R02/R03、谱补测与旧zip不改写。
