# 组会一页摘要：Top-32成员更替是否向较低参考频率移动？

**结论：局部支持，存在明确反例，没有统一的粗细频率阶梯。** 以下为S11原判定：6支持、5反向、4未决、1不足；未按本轮结果改判。Q为6000题干，G为6000 DCLM。

**定义：**同一背景中，一侧进入Top-32、另一侧未进入的成员为更替成员。DEV32家族按净入选率差绝对值定权，CONF64家族按实际更替归一化统计。它不是所有类别区别，也不包括共同成员的强弱。

| SAE | 同父细类 | Q：粗→细均值%与判定 | G：粗→细均值%与判定 |
|---|---|---|---|
| Attention | 猫–狗 | 5.33→3.16，支持 | 5.30→2.72，支持 |
| Attention | 汽车–自行车 | 5.33→5.55，不足 | 5.30→5.66，未决 |
| Attention | 苹果–香蕉 | 5.42→8.22，反向 | 5.95→6.74，未决 |
| Attention | 椅子–沙发 | 5.42→4.72，未决 | 5.95→5.82，未决 |
| MLP输入 | 猫–狗 | 6.73→4.94，支持 | 6.25→4.18，支持 |
| MLP输入 | 汽车–自行车 | 6.73→13.50，反向 | 6.25→10.59，反向 |
| MLP输入 | 苹果–香蕉 | 10.65→6.39，支持 | 8.18→4.54，支持 |
| MLP输入 | 椅子–沙发 | 10.65→19.00，反向 | 8.18→14.18，反向 |


**支持例：MLP猫狗。** 粗6.727%→细4.940%，差+1.787pp，原联合区间[0.389,3.218]。#22958在猫64/64、狗0/64，Q26/6000=0.433%，占猫狗归一化更替质量69.1%。它跨家族稳定，但结果集中于少数坐标，不能说很多细类成员都低频。

**反向例：MLP汽车/自行车。** 粗6.727%→细13.497%，差−6.770pp，原区间[−8.683,−4.842]。既有#16830（Q0.117%，汽车0/64、自行车64/64），也有#8048（Q74.683%，54/64对15/64，39次更替均汽车侧）。稀有与常见成员同时参与，因此有低频偏向成员不保证整个分布下降。

**本轮更新：**沿原公式检查S13复用数据，猫狗局部下降及MLP交通/家具反向仍可见；全部是事后探索。猫狗支持对#22958等少数成员敏感，交通反向也受#8048影响；删一个家族不能改变这几项方向。已有数据足以拒绝统一解释；若要确认跨新背景/新描述的稳定规律，需要独立新材料。已冻结[独立确认设计](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_turnover_audit_1106/confirmation_protocol_cn.md)，尚未创建材料或运行。无新前向、训练、router、读出或功能干预。

[完整中文报告](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_turnover_audit_1106/summary_cn.md) · [真实案例](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_turnover_audit_1106/casebook_cn.md) · [原始表/代码](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/posthoc_turnover_audit_1106) · [审阅包](../20261106_Top32_turnover_audit.zip)。包11575209bytes，SHA256 `27ef3727ac106399ccc8710c79b93b2098f85021b6512784bf28b69e9ee3cc10`，CRC、解压哈希和34720项模型外复算通过。
