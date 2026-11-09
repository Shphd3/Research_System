# 五张主图：读图和结论边界

B1…B4是TRAIN激活频率从低到高的四段；每段两个固定接收槽，ID0/1、2/3、4/5、6/7。U是TRAIN零命中的907个feature。R0原幅度，R1除以段TRAIN均值，R2减去段TRAIN均值；R2b两阶段都减，C目标层h减均值后重编码。所有评价的真实专家输入仍是原h。

## 均值组成

![均值组成](figures/figure1_mean_components.png)

测量：有符号α，参考为原始坐标TRAIN均值；左图整对话1000次95%区间，右图feature等权cosine箱线（中位、四分位、1.5IQR须，离群点未绘但源表全保留）。TRAIN85548、复核22446位置；B1–B4人数1694/5673/7013/1097。

观察：B4段向量投影为负，预处理offset和decoder偏置不可忽略。

解释：高频幅度不等于真实均值的正向份额；cosine只是方向而非实际贡献。

限制与设计影响：α不是能量占比，负值不是无用；保留原坐标、偏置与残差，不给common语义命名。

[源表](tables/mean_components.csv) · [PDF](figures/figure1_mean_components.pdf)。

## 专家负载

![专家负载](figures/figure2_expert_loads.png)

测量：每接收槽的复核位置占比，三图同一0–100%纵轴，黑线为整对话95%区间，N22446。颜色只表示频率段。

观察：R0空5槽，R1/R2空2槽。

解释：评分改变了分发。

限制与设计影响：负载不认证功能或学习；必须接着看图3。

[源表](tables/expert_loads.csv) · [PDF](figures/figure2_expert_loads.pdf)。

## 目标接收与原输入混合

![目标接收与原输入混合](figures/figure3_receiving_composition.png)

测量：左图逐低频feature的接收率经验累计分布，1198可估、496NA；右图每位置先算c份额、再在专家内平均，数值为百分比，统一0–100色标，空槽NA。小于显示精度的正值可能显示0.0，原值不补零。

观察：R1接收高于R2；各槽仍有大量高频段幅度。

解释：把位置送进低频段和把已出现的低频feature送给owner不是一件事。

限制与设计影响：完整输入仍混频，激活个数和幅度不表示学习价值、梯度干扰或容量。

[源表](tables/input_composition.csv) · [PDF](figures/figure3_receiving_composition.pdf)。

## 分发转移

![分发转移](figures/figure4_transitions.png)

测量：行R0来源槽，列新槽；每格占全部22446个位置的百分比，而非行归一化，色标固定0–50%。未标数字的格为实际0计数。

观察：R0集中在高频槽，改评分后向多个槽迁移。

解释：保留流入和流出，不能只报最低频段的增长。

限制与设计影响：仅分配反事实，无专家更新。完整计数、行内比例及对话区间见表。

[源表](tables/route_transitions.csv) · [PDF](figures/figure4_transitions.pdf)。

## 完整固定文本

![完整固定文本](figures/figure5_fixed_text.png)

测量：预登记哈希选中的“苏格兰折耳猫”自然文本，233个答案预测位置全部分面。左图当前原z×末层decoder范数的占比，色标0–100%；右图数字为真实槽ID，颜色为频率段。横轴是同文本当前token位置，不是模型层号。

观察：同一完整文本在R0/R1/R2下分配不同。

解释：改变的是选择规则，未改变专家实际接收的h，也未凭空加强低频信号。

限制与设计影响：单条文本仅展示算法，不证明语义分工；原分数、TRAIN基线、比值、减法及所有路线在逐位置源表。完整可见前文和右文辅助分开。

[源表](tables/fixed_text_all_positions.csv) · [PDF](figures/figure5_fixed_text.pdf)。

## 补充：两阶段减法与原表征中心化

![补充负载](figures/supplement_centering_loads.png)

R2b填满8槽，C仍空5槽。这只描述接收槽负载，不能替代目标接收或编码质量判断。完整数值见[负载表](tables/expert_loads.csv)与[质量表](tables/reencoding_quality_summary.csv)。
