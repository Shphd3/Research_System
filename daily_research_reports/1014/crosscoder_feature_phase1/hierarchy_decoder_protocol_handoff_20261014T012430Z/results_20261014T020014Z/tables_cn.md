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
