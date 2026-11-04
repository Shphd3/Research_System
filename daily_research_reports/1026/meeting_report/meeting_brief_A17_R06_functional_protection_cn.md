# 已学行为怎样继续有效：监督组织与局部保护

**会议问题。** 我们希望复用已学计算，让新增区别继续学习；关键前提是旧行为怎样在后续更新中继续有效。本轮的有界判断是：持续提供正确旧监督，比当前参数限制或局部旧loss不增的一阶约束，更稳定地维持了旧新规则的正确使用。

**已有证据。** A17是带模式标记的两套可兼容三词列表规则：模式一甲取首、乙取尾，模式二反转。共享参数混训可以共存，纯新续训会丢失旧行为；原Top-16保护未解决该问题。我们尚未找到可复用计算子空间，本轮也不是数学知识层级形成实验。

**本轮唯一问题。** 固定每步36条新题、损失分母72及240步，共8640次新曝光，改变旧有效监督0/4/36条，比较普通U、Top-16衰减S、旧损失梯度投影F及仅缩步长D。36条轨迹全部完成，三个顺序共用一个旧模型；全部方法另读64条旧TRAIN探针，F/D使用这些标签，因此0:1仅指训练目标没有旧重放项。

**结果如何更新判断。** U旧／新准确率随旧新监督0:1、1:9、1:1分别为0.125%／99.833%、93.125%／99.042%、99.708%／99.458%；F为11.292%／98.792%、68.250%／98.208%、99.750%／98.792%。F在零旧目标档有有限收益，1:9档三个顺序却全部弱于U，且同达90%新学习门槛时仍较差；没有单调频率规律。新增逐题证据表明，U0主要把旧题答成新规则（99.833%），U1:9降至6.792%，F1:9仍28.708%，列表外输出均为0。90个F检查点中实际最终内积没有超数值容差的违背，但69次实际探针loss上升；9个终点的有限读出还显示模式差异存在，却不保证模型正确使用，且差异更大不一定表现更好。

**边界与下一步。** 观测支持“旧监督组织与局部保护并不等价”，并把失败具体化为条件规则混淆；它不能说明旧电路删除或必须分专家。旧监督次数同时改变旧目标权重，局部有限步误差、探针代表性与学习路径尚未分离。**AI建议优先研究输入条件怎样持续组织正确功能更新，同时把局部约束有效范围作为竞争诊断；暂不继续追逐大奇异方向或直接扩展MoE。** 支持该选择的新证据是模式配对错误、同批有限步核验及模式差异不等于正确使用，而不只是平均准确率改善。

[三张主图及逐图四句说明](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/meeting_analysis_20261026/figures_and_captions_cn.md) · [完整结果解读](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/meeting_analysis_20261026/summary_cn.md) · [逐种子、损失、90点与真实例子附录](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/meeting_analysis_20261026/appendix_cn.md) · [执行/未执行清单](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/meeting_analysis_20261026/coverage_cn.md)
