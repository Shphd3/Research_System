# 1104组会：先观察组合，再检验输出作用

主实验先完成384条、每域16家族、固定8/8和双SAE留出／措辞对照，之后执行14976个临时干预条件。原模型／SAE权重、文本、候选和主缓存均保留。

**认识更新一：组合不是“父类成员全部保留后再加成员”。** 同32预算内只有部分保留并更替，候选也有8/8和0/8。显式类内重叠高于跨类，但共同强弱的复现范围更窄；动物属性猫3/8限制语义判断，交通工具MLP固定列表只有5/8合格。

**认识更新二：稳定响应并不等于分类时必需。** 删除大共同组经常增强正确候选边际，MLP动物／交通约增加.849／1.493nats，也同步改变无关类别分布。共同组找不到完整同频同幅匹配，不能判定类别专属作用。

**认识更新三：Attention动物有小的局部强弱方向作用。** alpha.5朝反侧模式移动，8家族平均正确边际损失.01236nats；等范数同成员打乱.00613，差.00623[.00135,.01340]，Holm p=.03125。各主要条件仍16/16正确，支持分数敏感性，没有翻转概念。

**原始例子紧接结论。** F09原文“Asked what the survey was about, the researcher replied that it concerned a cat. The interview then ended. / Description:”。Attention共同#23899/#18691/#9522：原[29.234,1.816,2.736]，反侧.5后[28.966,4.081,3.119]；cat/dog完整S从−11.20893/−14.14577变为−11.17121/−14.07189。cat全词表rank174→167、dog2364→2234，但cat在四候选中的概率.94743→.94577，两词都增强时相对偏好仍可变弱。

机制直觉（AI）：同一共同组可能同时承载背景尺度与细微判别偏向，删大组和重新分配强弱会经过不同的非线性后续计算。当前数据没有把这个直觉升级为自然机制；方向注入只能识别本模型、hook、位置和强度下的输出作用。

实验分析：h新=h原+Wdecoder(z新−z原)，偏置抵消、原残差保留；发现集冻结组合/典型模式，留出执行删除、计数/范数对照、alpha剂量、同成员打乱和其他组对照。完整前向与末层重算最大分数差6.44e−6；完整两token计分、全词表排名/概率和top20都记录。原始匹配不足、反向、身份改变和超范围保留。

控制几何审核还发现，交通工具Attention只有两个共同成员，固定长度后只剩一个比例自由度；部分打乱等范数操作会与目标几乎相同或反向。因此不能把跨大类差异唯一归于语义组织。主检验未更改。

边界：词面复述、属性词线索、小样本和广泛输出变化仍在；没有真实概念转换或MoE/router分工证据。H1局部组合关联、H2条件组合关联和干预的局部作用分开报告。科研接受和下一决策Unknown。

[主实验](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/summary_cn.md) · [干预Summary](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/summary_cn.md) · [完整反例／排名／分布](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/casebook_cn.md)
