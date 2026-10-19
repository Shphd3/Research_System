# 附录：统计随机化、组平均频率与来源

[返回原报告补充版](report_cn.md)

## 独立列位置置乱：仅组贡献表征谱

固定seed=20261016，对每个feature的131,072个系数独立打乱位置，完整保留零值及非零值多重集、激活频率、幅度和原decoder。两种分组共享同一份置乱列；只做1次，不给名义p值或随机化区间。它破坏原有跨feature对齐，但不保证该一次样本协方差精确为零，也不是合法模型输入干预。

![置乱后的归一化谱](figures/appendix_shuffled_figure3_normalized_spectrum.png)

1. 统计对象：独立列位置置乱后的同频/混频组贡献表征，实际第28个block，每组14成员、131,072位置，每规则1,119有效组。
2. 计算方法：沿用同一分组与decoder、按位置中心化求协方差，再逐组归一化、组等权汇总；本次零总方差组0。
3. 实际观察：置乱后同频/混频平均第一方向占比为0.353690/0.441058，与原始贡献谱0.359414/0.441889的方向相同，差值从−0.082475变为−0.087369。
4. 推断边界：边际频率、幅度及decoder几何仍能产生该方向，不能据一次置乱证明共同出现不起作用，也不判断差值变化是否显著。

![置乱后的第一方向占比](figures/appendix_shuffled_figure4_first_direction_share.png)

1. 统计对象：同一置乱实例中各个可估组的第一方向占比，包含全部1,119组每规则。
2. 计算方法：逐组计算最大特征值/总方差，用散点、箱体和均值菱形保留组间分布；箱须为1.5IQR规则，不是置信区间。
3. 实际观察：同频中位数0.308719，混频0.375288，两边仍有较宽分布和重叠。
4. 推断边界：这属于统计代理检查，不是训练、文本输入操作或容量/共同学习因果证据；相同方向也不将所有组变成同一种机制。

## 两方案的组平均频率分布

两方案各feature只用一次且组大小相同，所以组等权总体mean(p)=0.01623850、mean(log10p)=−2.501287相同是恒等关系。逐组的均值分布却不同，不能称为逐组匹配。

| 量 | 规则 | 最小 | P25 | 中位数 | P75 | 最大 |
| --- | --- | --- | --- | --- | --- | --- |
| 平均p_D | 同频 | 2.085e-05 | 0.000630613 | 0.00395824 | 0.0151824 | 0.855755 |
| 平均log10p_D | 同频 | -4.68119 | -3.20024 | -2.4025 | -1.81866 | -0.0736852 |
| 平均p_D | 混频 | 0.008586 | 0.00988768 | 0.0120711 | 0.0189838 | 0.0795059 |
| 平均log10p_D | 混频 | -2.65974 | -2.57176 | -2.50582 | -2.42966 | -2.32367 |

[p10/p90及全部分位数](data/grouping_D_frequency_distribution.csv) · [每组D频率数值](data/grouping_D_frequency.csv) · [完整成员表](data/grouping_members.csv)

## 原始hidden的命中支持与样本构成

所有组固定14成员、128位置，现有支持均足够，没有缺口或零方差组。同频最少240个命中位置，混频最少49,566个；组内样本覆盖context分别中位109/112、最少31/99，同频某组单个context最多占30.47%，混频最多4.69%，所以等位置数没有解决context构成差异。

不同组还复用原始位置：同频全部抽样槽位143,232个，对应121,607个不同位置；混频143,232槽位对应124,086个不同位置，两规则共享31,194个不同位置。不能据组数或槽位数声称拥有同样数量的独立样本。

图5/6是这一份评估缓存的原始hidden；图3/4及置乱图是另一结构V窗口的decoder贡献。矩阵、位置选择和出处都不同，两个谱方向不同本身不能定位哪一个因素造成差异。[采样与秩诊断](provenance/raw_hidden_sampling_and_rank_diagnostics.json)记录每组context集中度，第128个理论零方向的最大浮点占比低于2.3e−17，其余尾部补零未被解释为额外实测方向。

## 作图数据、脚本与来源

- [图1两柱](data/figure1_plot_data.csv) · [完整186对照](data/full_group_controls.csv)
- [图2种子曲线](data/figure2_seed_plot_data.csv) · [图2均值](data/figure2_mean_plot_data.csv) · [总体损失另表](data/overall_loss_table.csv)
- [贡献谱逐组结果](data/per_group_spectrum_metrics.csv) · [贡献谱均值曲线](data/normalized_spectrum_plot_data.csv)
- [原始hidden逐组结果](data/raw_hidden_per_group_raw_hidden_metrics.csv) · [原始hidden均值曲线](data/raw_hidden_normalized_spectrum_plot_data.csv) · [可用位置支持](data/raw_hidden_per_group_position_support.csv)
- [贡献谱冻结配置](provenance/contribution_frozen_config.json) · [原始hidden冻结配置](provenance/raw_hidden_frozen_config.json)
- [贡献谱数值汇总](provenance/contribution_spectrum_summary.json) · [原始hidden数值汇总](provenance/raw_hidden_raw_hidden_summary.json)
- [作图及计算脚本](code/)：figures12.py、plot_spectrum.py、plot_raw_hidden.py；compute_spectrum.py和raw_hidden.py保留计算定义与资格。字体为既有NotoSansCJK外部运行资源，未复制进报告或Git。

完整特征系数抽样矩阵和原hidden缓存留在执行目录，不进入阅读报告。选定谱NPZ只含组级特征值、归一化比例和定位索引，作为图形数据例外列入产物清单。
