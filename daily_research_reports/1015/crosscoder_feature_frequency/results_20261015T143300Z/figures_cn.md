# 五图：如何读，以及本轮能说明什么

[结果摘要](summary_cn.md) · [完整记录](detailed_cn.md)

数据固定为final14/F16384、单bin已接触D/V。所有频率与图的“复核侧”均不是独立文档确认集。五类图各有PDF/SVG/PNG，原表与绘图来源在执行侧；图4另有全部186组的分页PDF。

## 图1：特征激活频率排名

[PDF](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure1_frequency_rank.pdf) · [SVG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure1_frequency_rank.svg) · [PNG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure1_frequency_rank.png)

![图1：特征激活频率排名](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure1_frequency_rank.png)

**怎么读：** 横轴按D频率排序，V沿用完全相同feature顺序。纵轴是激活频率百分比，使用对数轴；右栏单列零命中，不使用epsilon。

**观察：** 两侧曲线总体接近，频率跨度很大；D有353个零命中、V有393个。V正频率中位约0.380%、最大99.264%。

**对主问题的意义：** 这是频率使用不均与窗口内稳定的描述，不能从曲线直接认定天然层级，也不说明每个feature可解释。

**下一步：** 保留频率和可靠性标签；支持不足feature未裁定，不能当作无关系。

## 图2：两侧频率稳定性

[PDF](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure2_frequency_stability.pdf) · [SVG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure2_frequency_stability.svg) · [PNG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure2_frequency_stability.png)

![图2：两侧频率稳定性](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure2_frequency_stability.png)

**怎么读：** 每个点是同一feature，x为D频率、y为V频率，均为百分比对数轴；虚线y=x。右栏分开仅D为零、仅V为零、两侧均为零。

**观察：** 全字典Spearman为0.99792；仅D为零63个、仅V为零103个、两侧均为零290个。低频点偏离相对更明显。

**对主问题的意义：** 频率排序在此窗口内可复核；总体相关高不能替代低频支持检查，不能解决原文档/近重复依赖。

**下一步：** 冻结D候选后保留V缺失，不按V回删feature。需要跨独立文档时另建确认资格。

## 图3：关系矩阵与分组

[PDF](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure3_relations_groups.pdf) · [SVG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure3_relations_groups.svg) · [PNG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure3_relations_groups.png)

![图3：关系矩阵与分组](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure3_relations_groups.png)

**怎么读：** 横纵为相同的固定300feature ID顺序，细线分隔D组；矩阵颜色为phi，旁边频率色条有独立图例。自相关对角线遮罩；phi在±0.1外颜色饱和，原数值完整保留。

**观察：** 全量而非这300点的结果为D/V非单成员组186/185、平均匹配Jaccard0.54838。300点按186组轮询，前114组各2点、后72组各1点，因此不期待大块组内纹理。

**对主问题的意义：** 可检查关系存在，但主展示不是完整分区证据。q=20时组数65/61，说明具体组尺度依赖邻居数；图上没有因果方向或模型深度。

**下一步：** 保留完整组及全pair值，后续分配不能把186当天然专家数K；正式H1仍需完整null与文档资格。

## 图4：逐组同频与随机对照

[PDF](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure4_group_frequency_controls.pdf) · [SVG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure4_group_frequency_controls.svg) · [PNG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure4_group_frequency_controls.png)

![图4：逐组同频与随机对照](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure4_group_frequency_controls.png)

**怎么读：** 主图预定显示D组大小排序前20组，点为真实V log10频率SD，越低越同频；蓝/绿分别同size与D均值匹配随机组，线/小提琴表示95%随机范围而非数据置信区间。绿色NA是控制链资格不足。全部186组见下方分页PDF。

**观察：** 全186组平均真实SD0.35331dex，同size随机0.67565dex；均值匹配只覆盖142组/48.37%成员，整体T_b=NA。全流程随机基线NOT_QUALIFIED，99次formal未启动，下方明确不计算p。

**对主问题的意义：** 简单随机组提示同频，但没有排除phi/组均值的偏好。44组NA不能当零、不能挑142组宣布全体支持。其失败主要是控制预算与链资格，不能写成无同频规律。

**下一步：** AI建议先修复控制预算与组大小的联动、重新登记复验；本轮保留所有NA及失败，不后调门槛。

## 图5：输入和特征激活案例

[PDF](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure5_inputs_activations.pdf) · [SVG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure5_inputs_activations.svg) · [PNG](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure5_inputs_activations.png)

![图5：输入和特征激活案例](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure5_inputs_activations.png)

**怎么读：** 顶部为V全部位置的未命中/恰一组/多组占比。下方按D组大小取前3个有样例组，各展示一个冻结随机与高score样例；【】标目标token。组内激活成员写feature ID:z，其他组命中单列。

**观察：** V未命中34.66%、恰一组39.52%、多组25.82%。176组共保存1,760条，10组门槛无法实现。案例来自评论、技术文本、词片等多种上下文。

**对主问题的意义：** 案例可定位不等于纯语义或功能；随机是hit-context均匀再选位置，不是uniformtoken。多组重叠对top1专家映射形成实际限制。

**下一步：** 后续先明确多组冲突、未命中与K专家容量的规则；不能直接拿组标签启动H2训练。

全部186组：[10页逐组PDF](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/figure4_all_groups.pdf)。固定组SD条件性bootstrap的整体95%范围为0.35267–0.35769dex（1000次中997次全组可估；3次缺失保存在原表），不是主均值匹配效应区间。输入三比例95%条件性区间见Summary。

图表来源：[完整图源manifest](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/plot_provenance.json)、[全组分页来源](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/all_groups_provenance.json)。所有绘图源表位于 /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_frequency/20261015T143300Z/figures/source_tables；排版只调整字体、色条、饱和范围和对角mask，统计数据未改变。
