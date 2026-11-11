# R05：蒸馏与自举原子路由结果

AI分析；研究者判断 Unknown。A8、A9、A9d均已完成；本轮不提交新架构训练。训练结果与统计分析完成范围见 F_coverage，旧对照缺失的55个总体／频段区间单列。

本轮问：teacher原子分组A5的训练收益，能否由学生原生router蒸馏获得，或由学生自己的冻结稀疏字典分发实现？A8从共同初始化训练2000步；A9全8层、A9d后4层在原生A0第1000步切换，各新增1000步。NLL是固定EVAL的逐位置负对数似然，单位nat，越低越好；集中度  $\bar M$  描述同一teacher原子被分到哪些expert，先跨8层平均、再跨原子取中位数。

**A9d比A9好0.02681nat，但新三臂在2000步都未超过A0；提高集中度也没有自动变成loss收益。**

| arm     |      NLL |   M_median |
|:--------|---------:|-----------:|
| A5      | 4.039119 |   1.344968 |
| A0      | 4.083142 |   1.010460 |
| A1-deep | 4.085093 |   0.870829 |
| A9d     | 4.098041 |   1.026740 |
| A8      | 4.102006 |   1.113494 |
| A9      | 4.124848 |   0.967771 |
| A4      | 4.129442 |   0.810892 |
| A1      | 4.157604 |   0.585752 |
| A6      | 4.174997 |   0.924780 |
| A2      | 4.286028 |   0.256799 |

终点数据：[逐臂NLL与集中度](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/distill_self_atom/F_endpoint_summary.csv)；[配对文档区间](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/distill_self_atom/A_bootstrap_differences.csv)。

| pair   |   difference |   ci95_low |   ci95_high |
|:-------|-------------:|-----------:|------------:|
| A8-A0  |     0.018864 |   0.017118 |    0.020535 |
| A8-A5  |     0.062888 |   0.059057 |    0.066572 |
| A8-A4  |    -0.027435 |  -0.029164 |   -0.025726 |
| A9-A0  |     0.041705 |   0.039531 |    0.043695 |
| A9d-A0 |     0.014899 |   0.013455 |    0.016281 |
| A9-A9d |     0.026807 |   0.025567 |    0.028002 |

**预登记判据：P5支持、P6削弱；P7两臂均为“恢复尚未完成”；P8两臂支持；P9支持。** 两个P7分支来自末250步下降0.085077／0.085756，均大于冻结阈值0.0817，不能改判为路线无效。

![详细loss](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/distill_self_atom/F_loss_detailed.png)

上行是训练CE原始淡线与50步均值，下行是固定EVAL NLL；右列放大后段。A9/A9d第1000点是零更新切换快照，不能与原生1000点混成同一条件。

A8集中度相对A0提高10.20%，A9降低4.22%，A9d提高1.61%；见[集中度拆解](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/distill_self_atom/concentration_cn.md)。A9/A9d切换即时NLL分别增加1.10504／0.27760nat；原子翻转率与损失冲击的相关分别0.4871／0.5366。到终点，29871／29915个合格原子曾恢复到原生1000步水平以下，但仍未超过继续训练到2000步的原生参照。

AI分析：当前更支持“成熟expert对既有输入分发存在适配，硬切换需要修复，且早层干预代价更大”；gate固定0.5、bias重置和冻结字典漂移仍是共同变化的竞争解释。[学习／遗忘说明](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/distill_self_atom/learning_forgetting_cn.md)区分了修复与新增收益。

数据只含seed17；文档bootstrap仅反映EVAL抽样。A9/A9d迁移到5090，原生基线是在H100训练；附加同权重5090前向的总体差为数个  $10^{-6}$  nat，但并非逐位置／训练轨迹一致。后续架构与提训决定留待研究者讨论。

完整设置、判据、缺口和证据链：[Detailed](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R05_20261110_distill_self_atom_routing/detailed_cn.md)；[汇报入口](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/distill_self_atom/README_cn.md)。
