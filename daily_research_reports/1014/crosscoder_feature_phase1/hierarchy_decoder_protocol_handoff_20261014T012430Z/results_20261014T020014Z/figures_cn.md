# 图与读图说明（修订版）

三类证据分开：**关联分支**看统计边；**跨层解码幅度占比 p**看幅度分布；**全体 h—L**看整体关系。频率格是解释边界。图1—3主类保留，图4—8补充完整分布与边界。

所有图提供 PNG／PDF／SVG。图节点写“V 激活频率”，不再用 pV；解码占比专用 p。图3及分布图使用相同 Q，n=15,537；原输入与阈值未改变。每个 Feature 的 p 合计 100%，L 只是其加权平均层号。

## 图1a：937 关联分支

19 节点、45 边；纵轴为统计图层级 h，横向只排版。节点频率以 V 的 5,247,663 位置为分母。箭头 A→更常见的 u；边编号查支持数表。

![图1a：937 关联分支](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937.svg)

## 图1a密集边分面

同一分支的 h=1→0 边，标 D/V 共同命中与 V 条件概率；不改变完整图层级。

![图1a密集边分面](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937_details.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937_details.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937_details.svg)

## 图1b：3461 关联分支

22 节点、56 边；与另一分支合并为 30 节点、101 边。图的高低不表示模型深浅。

![图1b：3461 关联分支](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461.svg)

## 图1b密集边分面

同一边与支持数分面，避免密集区遮蔽。频率单位为 %，不是 p。

![图1b密集边分面](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461_details.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461_details.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461_details.svg)

## 图2：固定30节点的跨层解码幅度占比 p

TRAIN 归一化坐标；行按 h 再 ID，列为模型层号 2、4、…、28。每行 100%，不是激活概率。

![图2：固定30节点的跨层解码幅度占比 p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure2_decoder_distribution.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure2_decoder_distribution.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure2_decoder_distribution.svg)

## 图3：全体h—L的双坐标对照

相同 15,537 节点、抖动、范围和规则。橙色是中位数及四分位范围，不是置信区间；h=5 单列两点。负向保留，幅度依赖坐标。

![图3：全体h—L的双坐标对照](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure3_all_features.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure3_all_features.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure3_all_features.svg)

## 图4a：TRAIN归一化坐标的6×14平均p

全部 h 的等权平均 p；样本数逐行标明，共用 0–40% 色标，颜色上限截断时仍标真实值。不能替代个体轮廓。

![图4a：TRAIN归一化坐标的6×14平均p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_train.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_train.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_train.svg)

## 图4b：恢复原始坐标的6×14平均p

相同 Feature、层号和色标。恢复层 RMS 后计算 p，单位 %；不据尺度差异命名功能。

![图4b：恢复原始坐标的6×14平均p](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_raw.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_raw.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure4_mean_p_raw.svg)

## 图5：各h的峰值类别比例【事后描述】

同一 15,537 节点；每柱 100%；第 2 层／第 28 层／其他层最大。小于 3% 的段仍保留。没有精确并列最大；类别不是功能标签。

![图5：各h的峰值类别比例【事后描述】](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure5_peak_composition_posthoc.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure5_peak_composition_posthoc.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure5_peak_composition_posthoc.svg)

## 图6：全部20个合格h=0节点

两个坐标各 20×14，共用 0–50% 色标，逐格标 p。峰值类别相同不等于完整轮廓相同；不含 847 个孤立节点。

![图6：全部20个合格h=0节点](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure6_h0_individual.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure6_h0_individual.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure6_h0_individual.svg)

## 图7：h=5的两个个体

937 与 3461 各自完整 p；横轴实际模型层号、纵轴 %。n=2，只描述这两个节点。

![图7：h=5的两个个体](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure7_h5_individual_curves.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure7_h5_individual_curves.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure7_h5_individual_curves.svg)

## 图8：频率共同范围内比较

全部 25 格；颜色是高 h 减低 h 的 L 中位差，单位模型层号；11 合格格，14 灰格。格内人数和不足原因保留；不是严格控制频率的效应。

![图8：频率共同范围内比较](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure8_frequency_all25.png)

[PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure8_frequency_all25.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure8_frequency_all25.svg)

所有图的源表对应关系与处理记录见 [修订记录](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/provenance/visual_revision_record.json)；[源表索引](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables_cn.md)。图已逐幅视觉检查，图6色标移至绘图区外后复查。没有只用公式检查代替实际渲染检查。

## 大范围补图：整体概览、320节点连接与同ID热图

[完整阅读入口及冻结选择规则](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/README_cn.md)。总体概览用全部15,537个节点；连接图含320个节点与1,250条已有直接边（261条跨h）。h=0至5展示数为20、80、80、75、63、2，主图同时标总体数；这是分层展示子图，不是总体比例。

[主图PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections.pdf) · [主图SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections.svg) · [17页直接边分面](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections_facets.pdf) · [同ID解码占比热图](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_train.pdf)。原19／22节点图仅代表各自可达分支，保留为局部图，不代表整体层级数量。
