# S11组会：共享与区分成员的相对频率

## 目的

使用固定SAE观察粗细类别的共有和区分成员如何分布在独立参考频率上。扩展至动物、交通工具、水果、家具，各设两个子类；不用高/中/低硬分段。

## 结论

**本轮共有成员的频率趋势较一致，区分成员的频率依赖类别、字典和参考位置。不能概括成高频负责共享、低频负责细类区别。**

1. **H1局部支持：细类配对的共有成员相对更低频，绝对频率仍可很高。** 显式4组细类×2SAE×2参考轴的16/16比较通过预设条件；名称改写13/16通过。MLP题干轴：动物–交通工具50.396%，猫–狗43.095%；差7.301个百分点，联合95%区间[6.347,8.306]。这些值是成员的参考入选频率均值，不是重叠度或准确率。

2. **H2局部支持，但统一的均值下移未获支持。** 成员差异16项：6支持、5明确相反、4未决、1参考支持不足。MLP汽车–自行车细比较13.497%，粗比较6.727%；细类反而更高，差−6.770个百分点，区间[−8.683,−4.842]。同时，开发候选前三名在64确认家族中如下：

| MLP ID | 题干末冒号频率 | 汽车/自行车入选次数 | F001原始z：汽车/自行车 |
|---|---|---|---|
| 16830 | 7/6000 = 0.117% | 0/64、64/64 | 0 / 12.348351 |
| 19178 | 141/6000 = 2.350% | 60/64、0/64 | 4.436555 / 0 |
| 8048 | 4481/6000 = 74.683% | 54/64、15/64 | 6.007303 / 0 |

它们同时包含少见与常见成员。低频尾部也可增加而整体均值上升；对应四分位的后续检验明确记为事后探索，不用来改判主结果。

3. **H3局部支持表征关联，联合机制证据不足。** 显式出现率与共同强弱的16个开发固定方向均复现；原始/RMS强度同向。但纯固定共有清单只有3/8条件同时满足开发和确认的完整激活覆盖。不能把动态共同成员结果全部称为同一整套成员只改强弱，也不能据此证明超出单成员边际的联合机制。

## 机制直觉与假设

类别差异可能借助少见坐标，也可能借助常见坐标的入选和幅值变化。这个解释与观察相容，仍不是已确认的语义或路由机制。频率本身还依赖位置：#8048在末冒号为74.683%，同批题干正文8位置仅108/48000=0.225%；正文独立单位仍是6000篇。

## 实验分析

- 新96家族，32开发/64确认；12标签×4措辞=4608主文本，另96条位置/措辞对照复用同样家族。新6000题干（Magicoder/GSM8K/MMLU各2000）和6000 DCLM文档只用于频率参照。全部新前向，不把旧缓存计作新增。
- 同一Qwen3-0.6B Base，第27层Attention输出与实际MLP输入分别分析。共有成员统一取正激活交集；区别方向/权重在开发锁定；幅值分布和有符号复现分别统计。分母、零分母、有效家族和反向贡献全部保存。
- 各2000次家族/参考文档重采样，主项Holm24/参考轴，方向Holm16；主位置为统一Description:末冒号。原始强度、正文位置、参考规模、家族打乱、子类混合及同义/属性/场景均附表。
- 子类混合粗比较的16项共享差、位置/措辞补充的8项共享差仍正向，属于同批家族控制。保留属性香蕉21/64、沙发1/64等弱条件；MMLU截取重复不换样本。Top-32退出不是原始响应归零，两个字典ID不对应。

**边界：** 单一短语反复换背景不等于许多独立类别表述；粗细与类别身份未完全分离。频率不是语义深度，共同出现不是共同作用。未训练、未干预、未启动router，也没有效率提升证据。主均值/判定经独立实现复核，四分位的数值边界修正另记，未改主结果。

**唯一下一问题（AI建议，未启动）：** 在新的、通过行为检查且读取位置一致的独立类别表述中，少见与常见成员并用的分布形状是否复现？

[完整总结](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/summary_cn.md) · [详细结果](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/detailed_cn.md) · [协议](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/protocol_cn.md)

![主图](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/figures/main_relative_frequency.png)

读图：每行一套SAE，每列一种对象；正值为细类频率较低。第三列是强弱差异质量对应的频率，不是幅值差本身。横线为参考文档与64家族的联合区间；空心点保留反向、未决或不足条件。

![具体例子](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/figures/mixed_frequency_case.png)

读图：同一feature的两个柱子对应同一背景下汽车/自行车文本的原始z；横轴第二行是独立参考频率。#47在这一例两侧都未入选，也按预定开发候选保留。

[完整192条件审计图](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/figures/audit_all_conditions.png) · [频率位置控制图](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/figures/reference_position_control.png) · [四个不同家族案例](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/figures/four_cases.png)
