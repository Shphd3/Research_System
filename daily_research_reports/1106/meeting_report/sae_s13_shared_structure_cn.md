# 1106：结论一补充——细类共享了什么

## 目的

把“细类共有成员的平均参考频率较低”拆开，回答导师11月4日的两问：共享是否向较少见成员延伸；区分类别的成员是否也统一更少见。本次只分析已有组织，不训练或干预。

## 结论

**1. 同父细类保留多数粗类共有成员，同时额外共享相对少见的成员。** 八组显式类别、两SAE都出现这一构成；两参考轴的额外成员项均降低平均频率，移除粗类独有成员则部分抵消下降。

MLP猫狗原始数据：粗共有22.33，保留20.71，仅粗共有1.63；猫狗共有28.46，其中额外7.75。逐家族平均保留率92.80%，16场景簇95%区间[91.70%,93.88%]。保留成员Q参考均值49.34%，额外14.89%[11.40%,18.71%]。Q均值下降7.14pp，可精确分成额外项+9.74pp与粗独有项−2.60pp；这不是因果贡献。

![集合与频率](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106/figures/main_shared_sets.png)

读图：左边每组上条粗共有、下条细共有；绿色两份名单都有，金色仅粗共有，蓝色仅细共有。右边同色点为该部分参考频率，越左越少见；区间固定参考，只重采样场景簇。

**2. 额外共有不等于父类缺席，也不等于细类专属。** 额外7.75个中平均4.40个已经在动物文本激活，只是没同时进入交通工具文本；只有3.35个是猫狗都有、动物没入选。MLP动物组额外成员中仅11.0%达到严格的稳定组内限定规则，其余可能背景依赖；不能把全部额外成员都叫细类语义。

**3. 一个成员可以既共享，又有强弱差。** MLP #17366的Q/G参考频率1.25%/1.78%；动物42/48、猫41/48、狗48/48，其他14细类0/672。共同激活的41家族中，狗−猫原始z差+4.158，完整Top32L2归一化差+.03668。旧S11同ID显式猫63/64、狗64/64，也保留这一使用范围，但两轮都已看过，不称新确认。

![类别覆盖](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106/figures/feature_scope.png)

**4. 少见成员确有细类偏向，但“细类差异统一更低频”仍未成立。** #22958在显式猫48/48、狗0/48，Q/G为0.43%/0.85%；不含类别名的表述中明显减弱。高频共享成员也能呈强弱差。旧S11区分分布6支持/5相反/4未决/1不足不改判。

反例：MLP动物N007共有成员22→27，但Q均值42.00%→43.76%，方向相反；Attention乐器#13389钢琴28/48、吉他46/48，未达稳定共享门槛。

## 机制直觉与假设

观察与“广泛共享＋较窄范围共享＋类别差异”的工作模型相容；这些角色可以重叠。较低参考频率是分析线索，不等于长尾知识、功能专属、因果交互或专家最优分工。“先学共享再学细类”的学习依赖尚未检验。

## 实验分析

复用S13确认48家族/16场景簇、8粗类16细类、4表述、两独立Top32字典。每家族既拆粗/细两共有名单的三部分，也拆父类和两细类的七区域。Q/G各6000参考文档不变。候选只从复用DEV显式固定，同ID检查四措辞与旧S11；全部新增统计属于事后探索。2000整簇bootstrap固定参考，不替代S13原联合区间。隐式仍受原行为门槛限制。

[完整中文结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106/summary_cn.md) · [逐项和分母](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106/detailed_cn.md) · [真实文本/ID案例](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106/casebook_cn.md) · [完整原始表与代码](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_shared_structure_1106) · [结果包](../20261106_S13_shared_structure.zip)。结果包18997021bytes，SHA256 `6c42905c0735ed9370c37a45806c0b737777bf8e114e5f234ba658a2ed7c9555`，CRC/解压哈希与2398777项便携数值检查通过。未训练、未做新前向或干预；未commit/push。

唯一下一步问题（AI建议，未运行）：在行为可靠、没有类别名的新表达中，同一批固定成员的共享范围与强弱差是否保留？
