# 图证据与渲染核查

共同设置：原生MoE33B／匹配末层SAE，旧CONF48家族／16场景，显式文本末冒号为主；父类包含在图一1152文本中，图二三为八个细类对。均是实际测量，不是机制示意。英文坐标用于稳定绘制，中文结论在总结逐图解释。

| 图 | 问题、源表、尺度 | 汇总与观察 | 结论边界 |
| --- | --- | --- | --- |
| 01_actual_expert_loads | 两个位置用哪些expert？源results/all_label_expert_loads.csv与top2_pair_counts.csv；左r/2、右gate，数字为百分比，expert零起算 | 1152文本等权；冒号98.00%用1/6，正文97.48%用4/7；不标统计误差，因为此图描述固定面板实际计数 | 不代表全文、全语料或模型整体路由；不解释bias因果 |
| 02_primary_questions | 三个硬选择问题是否有差别？源results/primary_questions.csv；横轴TV×100，不同面板分别标尺度 | 点估计、2000场景bootstrap95%原统计区间；空心家具不足；全部主检验未过校正 | 零下界不是等价性证明；区间不是null差值CI；组数不是独立实验 |
| 03_gate_weight_sensitivity | 硬选择相似时权重是否仍有差异？源primary_questions.csv及gate_weighted_resampling.csv；同为TV×100 | Q3点估计，蓝圆硬、橙方gate，空心家具不足；餐具6.511vs0.298pp，CI另见表 | 本图不编码显著性；完整192校正后餐具未过，不是权重主检验通过 |

实际PNG均已打开检查，标签、坐标、图例和区间清楚。图三初稿未标家具不足，补为空心并明确点估计；数值与主表不变。SVG同源导出，PNG渲染核查不声称所有外部SVG阅读器一致。颜色用作辅助，图例、形状和数值共同解释。绘图代码code/cases_and_figures.py，图表各自哈希在artifact_manifest.json。
