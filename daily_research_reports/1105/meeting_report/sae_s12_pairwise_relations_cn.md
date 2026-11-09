# S12：单成员变化之外，类别间二元关系尚待独立确认

**问题：** 控制单个feature的出现率后，两个feature的关系是否仍随猫狗等类别稳定变化？

**当前结果：** 复用S11原32开发／64评估家族，四组细类、两套SAE、四措辞。显式48条预选共激活边中19条覆盖合格、0条通过全部复现标准；32条强度边覆盖均合格、0条通过。不能由未通过推出不存在关系，尤其29条二值边覆盖不足。

**关键原始数据：** MLP猫狗#14753–#29479共同出现5/64→11/64；但#29479自身13/64→29/64，严格固定边际与Top32的零模型均值5.44→12.04次。差异关系−0.113，家族95%区间[−1.226,1.022]。共同次数增大没有在此转化为可靠的额外配对关系。

**读出补充：** 显式8条件没有稳定的交互损失收益。保留正例：Attention交通工具属性表述收益+.04313nat，区间[.01479,.07473]；同组场景为负，不能称跨措辞复现。基础模型／SAE／router均未训练。

**怎么读图：** 关系图每行固定节点、坐标、色标，第三列为狗−猫；颜色是关系点估计，必须结合覆盖与区间。幅值散点每点为共同激活家族，不能将均值移动当相关改变。

**边界／决定：** 96家族都已被S11使用，新盲数据为0；每条件仅1短语。频率Q/G只是节点属性。当前未确认额外类别二元机制，也没有解释专家分工／记忆。下一科学决定Unknown；AI建议仅另设覆盖与功效足够的独立描述确认，NOT RUN。

[中文完整总结](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S12_pairwise_relations_1105/summary_cn.md) · [猫狗关系图](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S12_pairwise_relations_1105/figures/cat_dog_binary_graphs.png) · [强度散点](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S12_pairwise_relations_1105/figures/cat_dog_strength_scatter.png) · [完整表与代码](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S12_pairwise_relations_1105)。
