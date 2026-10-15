# 三类图：分开阅读

图1只展示统计图的h；图2展示同一Feature的14层解码幅度占比；图3比较全体15,537个Feature的h与幅度平均位置L。不能将图1的箭头解释为模型层间传播，也不能将图3的L解释为整分布平移。

## 图1：锚点937的完整出边可达子图

纵轴为完整V图h，横轴仅排版。节点标ID、nV、pV；箭头方向A→u。密集底部边的支持单列于下方分面，完整101边见graph1_edges.csv；两面板没有重复计成独立图证据。

![图1锚点937](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937.png)

![图1锚点937支持分面](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_937_details.png)

## 图1：锚点3461的完整出边可达子图

纵轴为完整V图h，横轴仅排版。节点标ID、nV、pV；箭头方向A→u。密集底部边的支持单列于下方分面，完整101边见graph1_edges.csv；两面板没有重复计成独立图证据。

![图1锚点3461](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461.png)

![图1锚点3461支持分面](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure1_anchor_3461_details.png)

## 图2：同30节点的14层解码幅度分布

行按h再ID排序，列为实际模型层2、4、…、28，色值p每行和为1。937和3461同h但轮廓不同。完整平均p表可查看全Q各h的形状，不由L单独断定整个分布变化。

![图2解码分布](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure2_decoder_distribution.png)

## 图3：全部15,537节点的趋势

纵轴L只表示幅度平均位置，横轴h。橙色为中位数／Feature四分位范围，不是置信区间。h=5两点单列，整体相关−0.277976。图例置于绘图区外，所有点保留。

![图3全体趋势](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure3_all_features.png)

每幅图同时有PDF和SVG可缩放版本。
