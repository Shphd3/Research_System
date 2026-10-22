# 10月18日实际分发诊断：离线讨论包

本包汇集已完成的项目材料，供主任 agent 与研究者讨论。**当前证据支持优先明确并校准评分；新评分是否有效、全局分组是否可行、学习是否改善仍未知。** 这是派生阅读副本，不替代项目正式记录，不授予新运行、训练或改设计权限。

先读[给主任 agent 的交接稿](director_agent_handoff_cn.md)，再读[一页概要](summary_cn.md)。需要完整定义与证据时读[Detailed](detailed_cn.md)、[四图读法](figures_cn.md)和[12张文本卡](text_cases_cn.md)。[English entry](README.md)。

## 包内阅读路径

- 科学问题与执行范围：[用户 Anchor 中文](design/anchor_cn.md)／[英文](design/anchor.md)，[Protocol 中文](protocol_cn.md)／[英文](protocol.md)。
- 结果与边界：[Summary 中文](summary_cn.md)／[英文](summary.md)，[Detailed 中文](detailed_cn.md)／[英文](detailed.md)，[分析入口](analysis_cn.md)。
- 图与源表：[四图说明中文](figures_cn.md)／[英文](figures.md)，`figures/` 中四图各有 PNG、SVG、PDF；`tables/` 中含小型汇总和下列选定逐feature源表。
- 解释审阅：[科研推理审计](reasoning_audit_cn.md)、[来源绑定](source_bindings_cn.md)、[唯一下一决策中文](next_decision_cn.md)／[英文](next_decision.md)。
- 历史脉络：[近期六段结果中文索引](recent_results/20261018_routing_progress_cn.md)／[英文](recent_results/20261018_routing_progress.md)。历史正式报告并未全部包入，索引中的包外路径仅用于追溯。

## 四图的便携数据

|包内文件|用途与范围|
|---|---|
|[expert_summary.csv](tables/expert_summary.csv)、[group_summary.csv](tables/group_summary.csv)|各专家输入量与组内接收汇总；位置分母与feature分母分开。|
|[feature_owner_summary.csv](tables/feature_owner_summary.csv)|原规则A/B1/B2、TRAIN/EVAL全部可靠feature的负责专家指标，是图2的完整逐feature源表。|
|[feature_owner_original_and_C_zero.csv](tables/feature_owner_original_and_C_zero.csv)、[expert_loads_original_and_C_zero.csv](tables/expert_loads_original_and_C_zero.csv)|图1原规则与C评分项置零的完整最终接收结果。|
|[paired_feature_summary.csv](tables/paired_feature_summary.csv)|同一feature在A/B规则各自负责专家的配对结果，便于逐项核查。|
|[winner_runner_margin_components.csv](tables/winner_runner_margin_components.csv)、[winner_vs_A0_margin_components.csv](tables/winner_vs_A0_margin_components.csv)|原冠亚军分差、赢家与A0分差的C／非C分解；两种比较对象不同。|
|[case_common_plot_source.csv](tables/case_common_plot_source.csv)|图3固定三个目标及TRAIN固定伴随项，区分负责专家与实际主要接收专家，共108行。|
|[text_case_scores.csv](tables/text_case_scores.csv)、[text_sampling.json](tables/text_sampling.json)|图4与12张文本卡的选择及评分；完整卡片见[text_cases_cn.md](text_cases_cn.md)。|
|[conflict_pairs.csv](tables/conflict_pairs.csv)|TRAIN选择的27个有限冲突对及同对EVAL复核，不是全局可行性求解。|

[完整可见前缀与机器卡片](text_cases.json)和[核心计数回执](provenance/core_receipt.json)、[评分回执](provenance/score_receipt.json)、[文本／共现回执](provenance/cases_receipt.json)、[执行绑定](provenance/execution_binding.json)、[设计冻结记录](provenance/design_freeze.json)已包入，可离线核查本轮参数与文本。JSON中的执行路径仅作来源标识。

## 原件与打包边界

项目正式结果源为 `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_19_feature_group_to_actual_dispatch/20261018_routing_audit/`。Anchor源为对应项目的 `main/problem_anchors/15_spectral_representation_and_functional_routing/15_19_feature_group_to_actual_dispatch/`。`recent_results/` 来自项目 `main/research_notes/qwen3_crosscoder_tooling/`。

上表额外四份完整最终源表只进入本讨论包，不回写项目：`feature_owner_summary.csv`、`feature_owner_original_and_C_zero.csv`、`expert_loads_original_and_C_zero.csv`、`winner_runner_margin_components.csv`。它们分别来自执行目录的 `metrics/core/` 或 `metrics/score/`，便于离线核查图1／2与评分分解。包内其余小表、四图与报告来自上述项目正式目录。

**没有打包：** 原hidden／z缓存、模型与checkpoint、完整feature×expert长表、约927k行／侧的伴随gzip大表、NPZ矩阵及完整原始日志。这些保留在执行根 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/routing_audit_20261018T143950Z/`。包内文本是精选的12张卡片，不包含原bin语料。

包内当前报告、Anchor、图和选定表使用相对链接即可阅读。历史报告、执行回执及原数据的绝对路径属于**包外来源**；离线无法访问并不妨碍阅读本轮结论，但本包不能独立复现缓存统计。仅修订副本的阅读链接，没有改变科学定义或结果。最终来源、原hash及包内文件hash由[payload manifest](payload_manifest.json)记录。

附加[原分组元数据快照](provenance/parent_grouping.json)保留线性边界、精确成员、原低／高名单、评分与tie定义；这是冻结JSON元数据，不是新增激活缓存或新分组。
