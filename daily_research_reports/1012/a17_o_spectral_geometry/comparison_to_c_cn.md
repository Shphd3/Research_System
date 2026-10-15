# 直接比较A→C与B→C：主要参数通道有什么不同

[English](comparison_to_c.md) · [正式Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/comparison_to_c/summary_cn.md) · [全部逐顺序与rank数据](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/comparison_to_c/detailed_cn.md)

## 目的

**A、B、C有参数差别，直接比较后B比A更接近C。** 本轮专门在参数空间检验这个排序，并分析主要通道怎么变化，没有计算梯度。它服务于总问题：什么时候共享学习，什么时候需要按条件分开处理？

## 模型

A是同向新规则续训；B是只学反转新规则；C从相同旧起点同时监督旧规则与反转新规则。既有旧／新准确率分别是A100%／100%、B0%／99.25%、C99.83%／99.67%。

对O矩阵，Wc=Σ_i σ_i u_i(v_iᵀc)。它表示：矩阵读取输入在v_i方向的分量，按σ_i放大后沿u_i输出。**大奇异方向就是强线性处理通道；它的任务作用还取决于输入是否用到该通道。**

我们做两种直接比较：①T_AC=C-A与T_BC=C-B的SVD，研究端点差别集中在哪些方向；②各完整O只保留前16项后，再比较两算子的差，研究原本最强处理通道有没有变化。两种“前16”含义不同。端点差值也不是实际训练路径。

## 假设

此前候选预期是A/C可能更近。竞争解释是B/C共同学习反转新映射，O可能更接近；但C额外保持旧监督，所以旧功能不同。新标签、旧监督、新曝光及Q/K/V没有在本比较中单独隔离。

## 结论

1200步、三个续训顺序等权平均：

| 参数读数 | A→C | B→C |
| --- | ---: | ---: |
| 完整O差值范数 | 3.7996 | 2.9888 |
| 完整差值／C完整范数 | 8.876% | 6.982% |
| 差值最大奇异值 | 1.2233 | 1.0479 |
| 差值自身前16项能量 | 79.621% | 78.237% |
| 完整O前16项算子的差／C前16项算子范数 | 38.697% | 30.316% |
| 完整O前16项算子的有符号余弦 | 0.9222 | 0.9526 |

**完整矩阵与前16项算子都显示B/C更近，三个续训顺序均成立。** rank8／16／32的均值排序一致，但rank8有一个顺序例外，不能说所有截断、所有顺序均无例外。

![各完整O主要处理算子的直接差值](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/to_c_20261012_v1/figures/02_to_c_truncated_operator_distance.png)

横轴是保留8／16／32项，纵轴是两个截断算子差值除以C截断算子范数；点为均值，线段为三个续训顺序的范围。1200步B/C前16项差30.32%，A/C为38.70%，这个百分比不是任务效果，也不是完整矩阵变化比例。

## 分析

### 主要差别在哪

约79%的端点差值能量集中在差值自己的前16项。但以完整C最强16个输入和输出通道作参照，A/C差值88.58%、B/C差值85.88%落在两侧其余坐标。**完整矩阵的大方向与“端点差值自己的主要方向”不是同一个对象。** 完整C前16项原本仅占矩阵约5.5%能量，其余坐标不能叫无用。

再以C相对旧起点的变化D_C为参照：

| 差值在D_C前16坐标中的位置 | A→C | B→C |
| --- | ---: | ---: |
| 主要输入和输出都在内 | 65.11% | 34.55% |
| 主要输出内、输入在其余坐标 | 12.59% | 38.38% |

B/C差别更多涉及“沿着C变化的主要输出方向，连接不同输入方向”。这比只说“谱不同”更具体，但仍是参数侧定位，不能直接称为旧规则保护成分。

![完整C和C变化两种参照下的差值分布](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/to_c_20261012_v1/figures/03_to_c_four_block_energy.png)

横轴是端点差值，纵轴为四个正交块的平方能量比例；上排参照完整C，下排参照C相对旧起点的变化。四块衡量矩阵差别的位置，不是预测贡献。

### 为什么会这样，以及主线改变了什么

一个符合设置的候选解释是：B和C共享反转的新要求，所以部分算子更接近；A保持同向映射，与C的新要求不同。C又得到旧模式监督，所以参数更接近B的同时仍能保持旧规则。这是AI候选解释，本轮并未把这些因素独立操纵成因果证明。

因此，这轮没有否定“大方向体现矩阵处理能力”；它补上了强度、符号和输入输出配对，确实测到大通道有变化。它要求修正的是：**不能因为A/C都保持旧规则，就预期其参数一定比B/C更近。** 共享参数能否兼容，需要解释变化如何作用于不同模式，而不能由几何距离替代。

不做梯度也能继续检验功能：固定其余参数，仅加入T_BC前16项或其余项，再评估旧新任务。这是AI建议，尚未执行；当前仅完成参数空间分析，没有确认这些方向的任务因果作用，也未测量分开模块净收益。

### 执行与证据

先写[补充Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R04_o_spectral_geometry/comparison_to_c/protocol_cn.md)，再完成12次CPU FP64 SVD；12项数值测试通过。独立审计重算91项SHA、19实际O、2个Gram谱、36个截断算子、72个四块及180个重合读数，最大误差7.54e-15。原始全谱见[谱图](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/to_c_20261012_v1/figures/01_to_c_difference_spectra.png)；[图源清单](/data/250010109/MoE_Router/experiments/20261012_a17_o_spectral_geometry/runs/to_c_20261012_v1/figures/figure_manifest.json)绑定CSV和绘图脚本。

实际资产`analysis_a17_04_o_to_c_20261012_v1`已登记并通过当前访问核验。研究者机制接受与问题闭合Unknown。图仍在执行机，本次未commit或push。
