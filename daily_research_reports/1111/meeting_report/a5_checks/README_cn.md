# A5增益来源检查（AI分析）

研究者判断：Unknown。接续R04；主模型冻结，原结果只读。启动A1缓存微差9.91e-6 nat已追溯至既有重算记录，用户明确接受后继续。

|检查|问题／一句话结论|预登记规则套用|原始表|
|---|---|---|---|
|1|A0宿主A5提示量-0.000665 nat|泄露不是主要解释|[check1_hint_probes.csv](check1_hint_probes.csv)；[check1a_route_information.csv](check1a_route_information.csv)|
|2|可观测晚期领先量总体斜率为正；末点仍右删失，不能由nat差缩小断言追平|可见区间未支持持续缩小；完整1000–2000判定不足|[check2_step_lead.csv](check2_step_lead.csv)；[check2_lead_trend.csv](check2_lead_trend.csv)|
|3|A5−A0=-0.044024，文档95%区间[-0.047218,-0.040423]不跨0|仅固定模型EVAL文档抽样；种子方差Unknown|[check3_document_bootstrap.csv](check3_document_bootstrap.csv)|
|4|bias使A5/A1集中度相对改变0.56%/15.95%|10% bias干扰分支触发|[check4_score_bias.csv](check4_score_bias.csv)；[check4_concentration_variants.csv](check4_concentration_variants.csv)；[check4_atom_groups.csv](check4_atom_groups.csv)；[check4_group_top_atoms.csv](check4_group_top_atoms.csv)；[check4_group_contexts.csv](check4_group_contexts.csv)；[check4_A5_A0_spearman.csv](check4_A5_A0_spearman.csv)|
|5|塌缩层bias改变Top2 70.17%，maxgate中位数0.99902|联合阈值未同时满足|[check5_layer_gates.csv](check5_layer_gates.csv)；[check5_layer_groups.csv](check5_layer_groups.csv)；[check5_seven_arm_scatter.csv](check5_seven_arm_scatter.csv)|
|6|L7 MLP一致率45.7%–56.5%；自举M中位数0.988–1.185|L7>60%配置0/3；自举M≥1.08配置3/6，<1.01配置2/6；10pp规则见check6a_rules.csv|[check6a_readability.csv](check6a_readability.csv)；[check6a_rules.csv](check6a_rules.csv)；[check6b_bootstrap_atoms.csv](check6b_bootstrap_atoms.csv)|

原始CSV保留精度；Markdown表、PNG/PDF图同目录。协议：[protocol_cn.md](protocol_cn.md)；输入微差：[input_gate_trace.csv](input_gate_trace.csv)。

探针阴性不等于任何解码器都不能取得提示；观察到的提示量按原阈值判断，仍不单独隔离训练中的因果增益。检查6为时间允许项；未完成项目按状态表保留。所有新训练只更新小探针或小字典，未训练／续训主模型。
