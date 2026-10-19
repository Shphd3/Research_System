# 全部源表索引

CSV保留原始精度。路径下的表是本轮派生输出，原输入hash与绝对位置见provenance/input_reuse_manifest.json。没有原模型权重或15GiB缓存副本。

| 表 | 数据行数 | 用途 |
|---|---|---|
| [hierarchy_counts.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_counts.csv) | 84 | 全字典h、资格、孤立性分类计数 |
| [hierarchy_members.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_members.csv) | 16384 | 全16384节点支持、h、资格及L |
| [feature_layer_response.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/feature_layer_response.csv) | 229376 | 全16384×14层norm、p、L及未归一幅度 |
| [depth_vs_layer_summary.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/depth_vs_layer_summary.csv) | 18 | 主V、固定D及raw的逐h摘要 |
| [hierarchy_mean_p.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/hierarchy_mean_p.csv) | 18 | 主V／D／raw，各h的14层平均p（无量纲） |
| [frequency_overlap_comparison.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/frequency_overlap_comparison.csv) | 50 | 主V与D全部50格，不隐藏不足 |
| [frequency_bin_counts.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/frequency_bin_counts.csv) | 60 | 固定D频率分组内各h样本量 |
| [graph1_nodes.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/graph1_nodes.csv) | 30 | 图1／图2固定30节点 |
| [graph1_edges.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/graph1_edges.csv) | 101 | 完整101边ID、支持、条件概率 |
| [figure2_source.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/figure2_source.csv) | 420 | 热图420格p原始值 |
| [figure3_source.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/figure3_source.csv) | 15537 | 全15537散点与固定排版抖动 |
| [text_layer_amplitude.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/text_layer_amplitude.csv) | 3360 | 240位置×14层幅度 |

派生几何数组derived_geometry.npz供复绘使用；完整文本为text_examples.jsonl；统计公式和冻结选择见provenance/protocol_frozen.md及code。

## 本次图表修订新增展示源表

除峰值类别计数外均为原表／已存几何的展示转换。峰值计数为用户要求的事后描述，没有新增正式检验。

| 表 | 数据行数 | 用途 |
|---|---:|---|
| [figure1_nodes_display.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/figure1_nodes_display.csv) | 30 | 图1术语修订：V命中、激活频率百分比与h；原节点未变 |
| [figure3_coordinate_comparison_source.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/figure3_coordinate_comparison_source.csv) | 15,537 | 图3同一15537节点、h、固定抖动及两坐标L |
| [group_mean_p_source.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/group_mean_p_source.csv) | 168 | 原V均值表转长表，2坐标×6h×14层；p仍为0—1 |
| [peak_feature_labels_posthoc.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/peak_feature_labels_posthoc.csv) | 31,074 | 事后描述：每个坐标—Feature唯一最大层及峰值类别 |
| [peak_composition_posthoc.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/peak_composition_posthoc.csv) | 36 | 事后描述：2坐标×6h×3类别计数与比例 |
| [h0_individual_source.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/h0_individual_source.csv) | 560 | 全部20合格h0节点，2坐标×14层p |
| [h5_curves_source.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/h5_curves_source.csv) | 56 | 937、3461的2坐标×14层p及L |
| [frequency_comparison_25cells_source.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/frequency_comparison_25cells_source.csv) | 25 | 原V全部25格加显示标记；不足显示为NA而非0 |

CSV中的p与share保留0—1原始精度，图中乘100显示%。原12张表均未覆盖修改。来源hash见 [修订记录](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/provenance/visual_revision_record.json)。
