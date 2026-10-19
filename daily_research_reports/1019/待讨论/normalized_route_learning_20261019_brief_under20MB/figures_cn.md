# 图外读图说明与术语

所有图均有PNG、可放大的SVG和PDF；数字源表在tables，来源/文件SHA在curated_evidence_manifest.json。图中expert ID只在本模型内标识参数块，不能自动跨策略当成语义对应。

## 先分清对象

- feature ID：冻结CrossCoder字典原子的稳定编号，不是词、主题或模型层。
- TRAIN/EVAL：训练统计/监督侧与留出评价侧。它们来自不同bin，文档独立性未知，EVAL此前已查看。
- token位置：用当前token及其可见前文形成h，预测下一token；next/following片段只供事后读文本。
- z：14层联合编码得到的共享门控激活，不是每层独立激活。
- p_i：TRAIN命中频率，正激活位置数/有效位置数。此处p不是以前跨层解码占比图中的p分布。
- c28：z乘第28层decoder向量L2范数，单位为原CrossCoder的TRAIN中心化vector-RMS坐标幅度；不是有利任务的证据。
- a_i(t)：z乘原14层decoder范数和的路由幅度。表字段assigned_reception_a是旧字段名，指接收率，和这个a不是同一量。
- m_i：TRAIN中该feature激活时a_i的均值；μ_e：TRAIN组评分S0均值；均冻结。
- S0/S1/S2/S3：原评分/组级校准/条件幅度校准/频率与条件幅度校准，不叠加。S1是事前主方案。
- T/R11：固定频率组织名单/固定随机组织名单，候选与人数相同。R11的11是名单种子，不等于两模型种子构成两个随机名单。
- 接收率：feature命中时，被送入其名单指定expert的比例；宏平均是先算每feature再等权平均。
- q_i,e：实际送入expert e的位置中feature i命中的比例。与p的分母不同；无输入expert为NA。
- NLL：正确下一token负对数似然，单位nat/token，越低越好；M_L是964低频feature各自命中NLL的等权平均。
- Δ：后者按图注指定的差值；学习比较负更好；目标收益用before−after，所以正更好。
- W/ΔW：专家原矩阵/相对配对初始化变化。singular value是奇异值大小，不能说明方向相似；eigenvalue是响应协方差特征值。
- NA：按定义不可估；0是真实零。不能相互替换。

- router/gating：负责选择expert的路由器。gate multiplier是选中expert输出的乘数；W_gate则是SwiGLU专家内部的一个投影矩阵，两者不同。
- median/IQR：中位数/第25至75百分位之间的中间50%范围。CDF是累积比例，即数值小于等于横轴值的对象占比。
- Frobenius norm：矩阵全部元素平方和再开方，描述整体幅度；trace是协方差对角线之和，描述中心化响应总方差。都不是容量分数。
- bootstrap interval：将整个上下文块有放回重采样，再算配对差值的范围；这里不是原文档独立的总体确认。
- nat/token：使用自然对数的每个预测位置损失单位；不是准确率，越低越好。
- h/a的输入尺度、CrossCoder的TRAIN中心/尺度、S1/S2/S3的评分校准是三个独立处理，不能都简称同一种归一化。

## 每张图的问题、读法、观察与边界

### figure1_fixed_activation_profiles

频率、共享激活和末层贡献是否是同一件事？

![图](figures/figure1_fixed_activation_profiles.png)

读法：左侧TRAIN频率p用正数对数轴；中是log1p(z)，右是log1p(c28)，行同一feature，列同一token，两个split按同一量共享色阶。
观察：低频项能有突出激活；z图与末层幅度图并不相同。
边界：展示feature按窗口最大c选择，不能估计全体语义或因果作用。

[SVG](figures/figure1_fixed_activation_profiles.svg) · [PDF](figures/figure1_fixed_activation_profiles.pdf)

### figure2_conditional_amplitudes

低频feature激活时是否普遍更弱？

![图](figures/figure2_conditional_amplitudes.png)

读法：全TRAIN/EVAL正激活事件池的中位数和四分位范围；三个面板分别z、c28、a，纵轴对数。
观察：EVAL低频z/a中位数反而较高，c28稍低。
边界：按正事件汇总，不是各feature等权；不同量不能互代，支持数在源表。

[SVG](figures/figure2_conditional_amplitudes.svg) · [PDF](figures/figure2_conditional_amplitudes.pdf)

### figure3_train_low_position_ranks

TRAIN所选低频项由哪些位置贡献？

![图](figures/figure3_train_low_position_ranks.png)

读法：每小图一个feature，横轴64位置的贡献排名，纵轴c；前5橙点对应文本表。
观察：很多所选项在单个或少数位置突出。
边界：窗口内描述，0值保留，不由尖峰推出语义。

[SVG](figures/figure3_train_low_position_ranks.svg) · [PDF](figures/figure3_train_low_position_ranks.pdf)

### figure3_eval_low_position_ranks

EVAL所选低频项由哪些位置贡献？

![图](figures/figure3_eval_low_position_ranks.png)

读法：同TRAIN图，但使用独立固定EVAL窗。
观察：出现稀疏局部峰，全部64排名仍保存。
边界：不把所选强激活文本当总体典型。

[SVG](figures/figure3_eval_low_position_ranks.svg) · [PDF](figures/figure3_eval_low_position_ranks.pdf)

### figure4_train_same_text_scores

相同TRAIN文本换评分，去向如何变化？

![图](figures/figure4_train_same_text_scores.png)

读法：上T下R11，每列S0/S1/S2/S3；色为log1p评分，白点是最终专家。
观察：T的S0/S2集中，S1/S3明显分散。
边界：不同评分单位与色阶不同，只同一规则内读；不是模型层或解码热图。

[SVG](figures/figure4_train_same_text_scores.svg) · [PDF](figures/figure4_train_same_text_scores.pdf)

### figure4_eval_same_text_scores

相同EVAL文本换评分，去向如何变化？

![图](figures/figure4_eval_same_text_scores.png)

读法：同TRAIN图，固定EVAL窗；八组主要feature见文本附录与CSV。
观察：T的组校准能改变选择，R11原本就更分散。
边界：不凭这64位置评价整批分发或学习。

[SVG](figures/figure4_eval_same_text_scores.svg) · [PDF](figures/figure4_eval_same_text_scores.pdf)

### figure5_dispatch_outcomes

负载、目标接收与零接收是否一起改变？

![图](figures/figure5_dispatch_outcomes.png)

读法：左负载分母全部65402位置，中每个低feature接收率再宏平均，右固定964零接收数。
观察：S1接收33.4%/零5，S2为0%/零964，S3为41.7%/零0。
边界：接收不等于同频，不等于学习收益。

[SVG](figures/figure5_dispatch_outcomes.svg) · [PDF](figures/figure5_dispatch_outcomes.pdf)

### figure6_actual_frequency_profiles

实际专家中还含哪些高频信息？

![图](figures/figure6_actual_frequency_profiles.png)

读法：横轴9615项按TRAIN频率降序，包括Top10；纵轴专家，色为实际q∈[0,1]，空专家NA。
观察：高频信息仍随完整输入进入，主体低q在统一线性色阶下较暗。
边界：黑色低q应与图14和完整数值表合读，不能当成没有该信息。

[SVG](figures/figure6_actual_frequency_profiles.svg) · [PDF](figures/figure6_actual_frequency_profiles.pdf)

### figure7_primary_learning_curves

S1接收改善是否带来主比较学习收益？

![图](figures/figure7_primary_learning_curves.png)

读法：A/B/C，两个panel整体和M_L，横轴累计有效预测位置；实/虚线seed11/22。
观察：各曲线上升，B比A更差、比C稍好。
边界：固定epoch3终点；低频宏指标不是低频知识掌握。

[SVG](figures/figure7_primary_learning_curves.svg) · [PDF](figures/figure7_primary_learning_curves.pdf)

### figure7_learned_references_learning_curves

本设置λ=.01均衡项是否改善学习？

![图](figures/figure7_learned_references_learning_curves.png)

读法：仅D/E两参考；门乘数为选中softmax概率。
观察：E终点比D更差，两者都差于原基座。
边界：只裁定该结构/强度，不推广所有均衡损失。

[SVG](figures/figure7_learned_references_learning_curves.svg) · [PDF](figures/figure7_learned_references_learning_curves.pdf)

### figure7_expanded_fixed_learning_curves

四种评分和两名单的所有结果是什么？

![图](figures/figure7_expanded_fixed_learning_curves.png)

读法：全部8个固定条件×2seed；颜色条件，实/虚线seed。
观察：T的S0/S2较少恶化，R11多种评分彼此接近；仍全差于基座。
边界：不是从扩展中选最好再宣称独立主方案。

[SVG](figures/figure7_expanded_fixed_learning_curves.svg) · [PDF](figures/figure7_expanded_fixed_learning_curves.pdf)

### figure8_primary_paired_differences

预登记主门槛是否满足？

![图](figures/figure8_primary_paired_differences.png)

读法：点为B−A或B−C；线段1000次配对EVAL块95%区间；负差更好。
观察：B−A为正，B−C为负；联合要求失败。
边界：区间不是文档独立总体显著性；两seed范围有限。

[SVG](figures/figure8_primary_paired_differences.svg) · [PDF](figures/figure8_primary_paired_differences.pdf)

### figure9_same_input_expert_probes

同一输入换expert会改变预测吗？

![图](figures/figure9_same_input_expert_probes.png)

读法：左强制门1的绝对NLL，右替换expert但保留自然门后的差值。
观察：输出/损失有差异，撤回旁支通常更接近原基座。
边界：expert ID跨策略不代表功能对应，不能由差异贴语义标签。

[SVG](figures/figure9_same_input_expert_probes.svg) · [PDF](figures/figure9_same_input_expert_probes.pdf)

### figure10_target_assignment

暂未用于背景更新的目标交给谁更安全？

![图](figures/figure10_target_assignment.png)

读法：左目标收益before−after对旧损害；右各expert绝对目标NLL随0/8/32步。
观察：所有终点收益为负且旧损害>.01，安全候选为空。
边界：该条件留出不是真正新知识；expert6原始最好但不安全，不能称归属成功。

[SVG](figures/figure10_target_assignment.svg) · [PDF](figures/figure10_target_assignment.pdf)

### figure11_parameter_spectra

参数几何变化是否与初始化区分开？

![图](figures/figure11_parameter_spectra.png)

读法：三行初始/终点/ΔW，三列gate/up/down，前16奇异值按8expert取中位数；全谱/范数另存。
观察：S0很多expert未更新，分布中位数可能接近初始化或0。
边界：奇异值不是方向，ΔW包含衰减，谱平不是容量高。

[SVG](figures/figure11_parameter_spectra.svg) · [PDF](figures/figure11_parameter_spectra.pdf)

### figure12_response_spectra

响应幅度与形状是否应分开？

![图](figures/figure12_response_spectra.png)

读法：同探针输出按位置中心化协方差；左绝对eigenvalue，中除完整trace，右所有expert的trace。
观察：不同条件的响应能量和形状各异，零响应项在归一化中NA。
边界：同输入几何描述，不构成功能或学习成功条件。

[SVG](figures/figure12_response_spectra.svg) · [PDF](figures/figure12_response_spectra.pdf)

### figure13_group_to_actual_expert

名单分组是否转化为实际分发？

![图](figures/figure13_group_to_actual_expert.png)

读法：行是原feature名单组，列实际expert；每格占该组全部feature命中事件的百分比。
观察：S1/S3改变实际去向，但有组外共入。
边界：一个token可贡献多个feature事件，行不是互斥token群。

[SVG](figures/figure13_group_to_actual_expert.svg) · [PDF](figures/figure13_group_to_actual_expert.pdf)

### figure14_expert_frequency_distributions

每个专家内真实频率分布是什么？

![图](figures/figure14_expert_frequency_distributions.png)

读法：正q对数横轴；纵轴所有9615项中q≤横轴值的比例，q=0纳入起始比例；空专家单列NA。
观察：列表分组未让完整输入自动同频；各expert零暴露与正频率形状差异可见。
边界：不是只看正命中的条件分布，不由曲线断容量。

[SVG](figures/figure14_expert_frequency_distributions.svg) · [PDF](figures/figure14_expert_frequency_distributions.pdf)

