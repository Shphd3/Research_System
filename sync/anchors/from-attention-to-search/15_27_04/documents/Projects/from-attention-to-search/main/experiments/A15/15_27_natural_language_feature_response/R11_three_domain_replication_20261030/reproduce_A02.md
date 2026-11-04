派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/reproduce_A02.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/reproduce_A02.md)；研究修改仍回到原件。

---

# R11 A02：复现与原始统计入口 / reproducibility

[中文结果](summary_A02_cn.md) · [English Summary](summary_A02.md) · [完整过程](detailed_A02_cn.md)

实际执行根目录：`/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R11_three_domain_replication_20261030/qualified_three_domain_A02`。没有授权再做模型前向；462/462次已用完。以下入口用于读取现有缓存或离线复算。不要重新运行finish_pipeline.py或run_native_cc.py；它们是原执行入口，不是无副作用读图命令。保留所有旧结果，复算另设输出目录。

## 必要对象与冻结

- [450文档身份manifest](../../../../../../../../UNAVAILABLE.md)
- [数据资格](../../../../../../../../UNAVAILABLE.md)
- [450文档和token IDs](../../../../../../../../UNAVAILABLE.md)
- [H前科学冻结，352文件hash](../../../../../../../../UNAVAILABLE.md)
- [462调用账本](../../../../../../../../UNAVAILABLE.md)
- [4精确重放＋8试读](../../../../../../../../UNAVAILABLE.md)
- [D/V缓存完成](../../../../../../../../UNAVAILABLE.md)
- [H缓存完成](../../../../../../../../UNAVAILABLE.md)

## 全部成员与旧新映射

- [16,384全字典筛选与支持](../../../../../../../../UNAVAILABLE.md)
- [逐阶段数量和辅助零异域ID](../../../../../../../../UNAVAILABLE.md)
- [冻结主／近／严格／Top及敏感性全部ID](../../../../../../../../UNAVAILABLE.md)
- [易读冻结名单及排序](../../../../../../../../UNAVAILABLE.md)
- [289名发现／开发／留出＋频率＋各测试状态](../../../../../../../../UNAVAILABLE.md)
- [全部H得分、区间、三域支持与来源层](../../../../../../../../UNAVAILABLE.md)
- [独立来源门槛](../../../../../../../../UNAVAILABLE.md)
- [全16,384旧新映射（各旧集合独立列）](../../../../../../../../UNAVAILABLE.md)
- [旧新名单交集分母](../../../../../../../../UNAVAILABLE.md)
- [原16迁移全部来源层](../../../../../../../../UNAVAILABLE.md)
- [原16新三域token表](../../../../../../../../UNAVAILABLE.md)
- [原16中文阅读表](legacy16_tokens_A02_cn.md)

## 五项统计与图

### 频率

[frequency_composition_D.csv](../../../../../../../../UNAVAILABLE.md) · [frequency_sensitivity.csv](../../../../../../../../UNAVAILABLE.md)

### 谱几何

[spectral_band_profiles.csv](../../../../../../../../UNAVAILABLE.md) · [PC1_decomposition.csv](../../../../../../../../UNAVAILABLE.md) · [geometry_sensitivity.csv](../../../../../../../../UNAVAILABLE.md) · [member_band_heatmaps.npz](../../../../../../../../UNAVAILABLE.md) · [pairwise_absolute_cosines.npz](../../../../../../../../UNAVAILABLE.md) · [actual_direction_subspace_checks.csv](../../../../../../../../UNAVAILABLE.md)

### 谱重合与背景

[geometry_results.json](../../../../../../../../UNAVAILABLE.md) · [main_background_ids.npz](../../../../../../../../UNAVAILABLE.md) · [near_background_ids.npz](../../../../../../../../UNAVAILABLE.md) · [strict_background_ids.npz](../../../../../../../../UNAVAILABLE.md) · [main_background_strata.csv](../../../../../../../../UNAVAILABLE.md)

### 输入token

[H_native_token_details.csv](../../../../../../../../UNAVAILABLE.md) · [H_native_token_top10.csv](../../../../../../../../UNAVAILABLE.md) · [H_native_token_member_summary.csv](../../../../../../../../UNAVAILABLE.md) · [H_native_token_group_composition.csv](../../../../../../../../UNAVAILABLE.md) · [H_available_token_background.json](../../../../../../../../UNAVAILABLE.md) · [token_definitions_D.json](../../../../../../../../UNAVAILABLE.md)

### 同token上下文

[H_same_token_group_effects.csv](../../../../../../../../UNAVAILABLE.md) · [H_same_token_member_effects.csv](../../../../../../../../UNAVAILABLE.md) · [H_same_token_matches.csv](../../../../../../../../UNAVAILABLE.md) · [H_same_token_examples.json](../../../../../../../../UNAVAILABLE.md)

主／辅助完整逐PC投影和1024PC基分别见R10原analysis与本轮[projection_secondary.npz](../../../../../../../../UNAVAILABLE.md)、[basis_three_domain_D.npz](../../../../../../../../UNAVAILABLE.md)。严格生物／物理空组reference NPZ占位数组不可当概率分布；正式overlap为NA。D未见词表槽数不代表实际未见token类型数。

- [F1/F2/G及98.333%区间](../../../../../../../../UNAVAILABLE.md)
- [全部3000选择重采样](../../../../../../../../UNAVAILABLE.md)
- [文档重采样索引](../../../../../../../../UNAVAILABLE.md)
- [固定p90逐成员辅助](../../../../../../../../UNAVAILABLE.md)
- [p90全部token](../../../../../../../../UNAVAILABLE.md)
- [p90成员等权组成](../../../../../../../../UNAVAILABLE.md)
- [D已知条件频率组成](../../../../../../../../UNAVAILABLE.md)
- [feature/token频率散点统计](../../../../../../../../UNAVAILABLE.md)
- [预定同词面实例](context_examples_A02_cn.md)
- [绘图来源hash](../../../../../../../../UNAVAILABLE.md)
- [项目阅读图片来源hash](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/payload_manifest.json)

## 离线复现顺序与实际代码

原scripts按analysis_helpers.py→analyze_discovery.py→geometry_appendix.py→freeze_science.py→evaluate_holdout.py→tokens_holdout.py→context_holdout.py→bootstrap_selection.py→plot_results.py顺序执行；freeze_science与前向步骤是原流程身份，不应在完成目录改写。数据源和脚本全部在科学冻结manifest列出，图表展示代码另存presentation。

- [原科学代码目录](../../../../../../../../UNAVAILABLE.md)
- [冻结表连接与全异域反例](../../../../../../../../UNAVAILABLE.md)
- [预定p90辅助离线补统计](../../../../../../../../UNAVAILABLE.md)
- [清晰主图和三域总图](../../../../../../../../UNAVAILABLE.md)
- [未知频率与散点附录](../../../../../../../../UNAVAILABLE.md)
- [三个独立核查及覆盖账本](../../../../../../../../UNAVAILABLE.md)
- [原主统计流程完成](../../../../../../../../UNAVAILABLE.md)

仅重绘当前展示可在相同Python环境运行presentation/plot_clear_report.py（不调用模型、不选人）；原科学复算需读取相同冻结数据和配置并写新目录。运行环境spectral-hier，torch2.5.1+cu121、transformers5.6.0.dev0、tokenizers0.22.2。图中前64是64/1024维；token计数分母28,800D位置，feature参考分母65,536DCLM位置。项目只跟踪小型文本和选定PNG；大数组、原始网页和checkpoint留执行侧。

## 几何阅读附录

[全部成员分布与全字典均值](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/appendix_all_member_distribution.png) · [成员×谱段热图](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/appendix_member_heatmaps.png) · [逐PC与PC2–64曲线](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/appendix_perPC_profiles.png)。分布图使用对数纵轴保留极端值；热图显示0–50%范围，逐PC图使用对数份额。全部原始矩阵仍在执行侧。
