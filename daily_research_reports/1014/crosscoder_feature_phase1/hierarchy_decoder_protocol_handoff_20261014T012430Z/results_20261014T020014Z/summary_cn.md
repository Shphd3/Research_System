# 结果摘要：统计图层级与跨层解码幅度分布（图表修订版）

**整体负相关不能把 h 解释为模型深度；同级内的完整 p 轮廓仍须保留。** 本版按用户要求修订图与叙述；新增峰值比例只作事后描述，原主结果和科学状态不变。

## 目的

回答固定问题：统计图层级较高的 Feature，其跨层解码幅度分布是否更偏深层？本轮帮助判断 h 能承担哪种描述，不评估共享／分离学习或专家分发收益。

## 方法

固定最终 14 个选定模型层、16,384 个 Feature 的 CrossCoder，复用冻结 TRAIN 归一化和原推理规则产生的已有统计图与 decoder 几何。主集合是 D/V 支持均 ≥200、且 V 图非孤立的同一批 **15,537 个 Feature**。各统计图层级 h 的样本数依次为 **20、8,896、5,347、1,209、63、2**。每个 Feature 等权；图中四分位范围描述节点差异，不是置信区间。

三类图回答不同问题：图1看固定节点的统计关联；图2及图4—7看跨层解码幅度占比 p；图3看全部合格 Feature 的 h—L 关系。图8是频率解释边界。TRAIN 归一化坐标与恢复原始坐标使用同一批节点；恢复原始坐标是将各层范数乘回保存的 TRAIN 向量 RMS，再计算 p 和 L。

本次按用户要求重画已有结果，并从保存的 p **新增一次事后峰值比例描述**：逐 Feature 取 14 层最大 p，分为“第 2 层最大”“第 28 层最大”“其他层最大”。两种坐标均无精确并列最大值。类别只描述幅度峰值，不命名功能。没有重跑推理、训练、缓存扫描、关系计数或频率比较，也没有新 GPU 任务。


h 是统计图中的最长出边路径；p 是同一 Feature 各模型层 decoder 范数的占比；L 是 p 加权的模型层号。**L 变大只表示幅度加权平均层号 L 变大，不证明整条 p 分布向深层移动。** 激活频率是命中位置比例，与 p 是不同的量。

## 现象

整体描述性 Spearman 在 TRAIN 归一化坐标为 **−0.277976**，恢复原始坐标为 **−0.157788**；方向保留，数值差异明显。TRAIN 归一化坐标下，h=1、2、3 的 L 中位数为 **19.902、15.007、14.305**，h=4 回升至 16.226；不是逐级严格单调。

完整 6×14 组平均 p 显示，TRAIN 归一化坐标下 h=1、2、3 的第 2 层平均 p 为 **15.39%、25.06%、30.20%**，第 28 层平均 p 为 **17.00%、13.95%、13.25%**。浅层和深层可以同时有幅度，不能把 L 的变化说成整条分布平移。两种坐标的完整热图使用相同 0–40% 色标。

事后峰值比例中，TRAIN 归一化坐标下 h=1、2、3 的“第 2 层最大”分别占 **34.95%、60.58%、74.19%**；恢复原始坐标下，这一类别均为 0，但第 2 层的 p 并非为 0。h=0 的 20 个节点在两种坐标下都以第 28 层为最大分量，完整轮廓仍不同。h=5 仅 937、3461 两点，其 TRAIN 归一化坐标 L 分别为 **22.118、14.899**。


完整均值图及逐节点图见 [图索引](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures_cn.md)；精确值见 [源表索引](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables_cn.md)。

## 解释

为什么整体负相关，频率内却有 7 格为正？两者比较的对象与权重不同。整体相关包含不同 h 组之间的频率构成差异，使用全部 15,537 个节点的秩；频率格只比较固定频率组的共同范围内、某一对相邻 h 的 L 中位数。建边规则要求箭头指向至少常见两倍的节点，所以 h 与激活频率本来就耦合。不同频率构成可能与整体负向同时出现，但本轮没有识别它造成了多少差异。

必须看全部 **25 格**：11 格可比较，7 正、4 负；其余 10 格缺组、1 格无共同范围、3 格样本不足。可比较格的差值大小并不对称，例如 +0.170 与 −8.982 都各被算作“一格”。h=0↔1 和 h=4↔5 都没有合格格，不能用 11 格替代整体。五分位和范围交集也不保证组内频率分布相同。这不是“控制频率后的效应”。

![全部25格频率共同范围内比较](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure8_frequency_all25.png)

读图：横轴为相邻统计图层级 h 对，纵轴为预定的 5 个 D 激活频率组。颜色是高 h 减低 h 的 L 中位差，单位为模型层号；每格标低 h／高 h 的样本数。灰格保留原因，不表示差值为 0。缺组／无共同范围格另标交集前组内人数。[完整频率源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/frequency_comparison_25cells_source.csv)。

坐标尺度是另一条边界：恢复原始坐标后，整体负向仍在，但相关数值和峰值类别明显改变。这说明数值依赖层尺度；它没有删除 Feature，也不能被讲成功能差异。峰值类别相同也不代表完整 p 相同。

D 图参照的描述性 Spearman 为 **−0.279321**，D 频率检查也有 11 个合格格、7 正 4 负。D/V 来自同 bin，V 曾参与资格筛选和原始边复核，文档独立性未知；这些不是独立总体检验。节点也不独立，不报告 p 值或独立节点置信区间。h=5 只有两个节点，不能代表最高统计图层级的总体规律。


## 结论

### 认识一：统计图层级 h 不能直接承担模型深度的正向排序，需要另外测跨层分布

![相同15537节点两种坐标的h—L对照](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure3_all_features.png)

关键数据：两面板使用完全相同的 **15,537 个 Feature、横向抖动、坐标范围和绘图规则**，分别给出中位数、四分位范围、各组 n 与描述性 Spearman；h=5 单列两个点。相关分别为 −0.277976、−0.157788。[逐点双坐标源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/figure3_coordinate_comparison_source.csv)；[中位数与四分位源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/depth_vs_layer_summary.csv)。

推断的变化：保留 h 作为统计关联结构的描述，不再直接用“h 更高”代替“模型中更深”。**下一项研究决策（待研究者讨论）：选取学习对象时，是否要求明确所用坐标，并同时保留完整 p，而不是只按 h 排序？** 本报告不因此启动新的学习实验。

### 认识二：同级内部存在不同轮廓，后续应同时看具体节点、关联分支和跨层分布

![同级内部峰值类别比例，事后描述](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure5_peak_composition_posthoc.png)

关键数据：TRAIN 归一化坐标 h=1 有 3,109 个“第 2 层最大”、4,493 个“第 28 层最大”、1,294 个“其他层最大”，都在同一个 h 内。h=5 的 937 与 3461 也具有不同 p 轮廓。恢复原始坐标改变峰值排序，因此不把类别命名成功能。[完整峰值比例与计数（事后描述）](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/peak_composition_posthoc.csv)。

![最高统计图层级的两个个体轮廓](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures/figure7_h5_individual_curves.png)

图7保留两个节点各自的 14 层 p 与 L；n=2，不作最高级总体推断。[两个节点逐层源表](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/tables/h5_curves_source.csv)。全部 20 个 h=0 节点的逐个热图、固定 30 节点热图，以及原关联分支见 [完整图与读图说明](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/figures_cn.md)。

推断的变化：组平均和 L 能概括差异，但不能替代个体轮廓。不同 h 组含不同 Feature，本轮没有观察“同一个 Feature 随 h 增长而移动”。**下一项研究决策（待研究者讨论）：比较候选学习对象时，是否将具体节点、关联分支和 p 作为共同保留的信息，而不是仅使用层级或峰值类别？** 当前不能据此判断 common／unique、共享／分离学习或专家收益。


原文本 150 条随机＋90 条高激活记录原样保留；本次没有新增文本抽样。[完整报告及执行追溯](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/detailed_cn.md)；[全部文本](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/text_examples_cn.md)。此次完成图表与报告修订后停止，不 commit/push，不进入训练或新实验。
