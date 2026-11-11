# A5续训到1B：明早速报

AI分析；研究者判断 Unknown。更新：2026-11-11 05:34 北京时间。

**这条单种子轨迹中，A5在约1B仍优于原生baseline。** A5从R04第2000步完整状态继续到baseline的1B manifest指定第3816步；新增1816步。A5实际累计1000341504有效token，baseline恰1000000000，相差0.03415%。

| 模型 | EVAL NLL（nat，越低越好） | 硬集中度中位数 |
|---|---:|---:|
| A5@3816 | 3.763121999 | 1.338417415 |
| MoE baseline@1B | 3.779426355 | 1.049242805 |
| Dense@1B | 3.871651564 | 不适用 |

| pair            | band    |   difference |   ci95_low |   ci95_high |   documents |   replicates |
|:----------------|:--------|-------------:|-----------:|------------:|------------:|-------------:|
| A5-MoE_baseline | overall |   -0.0163020 | -0.0191177 |  -0.0126727 |        1871 |         2000 |
| A5-Dense        | overall |   -0.1085270 | -0.1127165 |  -0.1035535 |        1871 |         2000 |

P10：**支持**。P12：**比较口径不足**：原生baseline正式轨迹第2000步存档未保存；R03 A0起点代理的后段Jaccard为0.281250，前段旧臂配对中位数为0.630952，按代理数值套原规则为支持，主判断不把代理当精确原轨迹。

![A5与baseline曲线](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/a5_to_1B/loss_comparison.png)

左图到1B，右图约0.5B以后放大；横轴实际累计有效token，曲线只连实际评估。领先量见step_lead.csv/md：在真实baseline检查点间插值，超过范围标“测不出”。

AI分析：固定teacher原子分组的早期优势延续到更长训练，当前数据削弱“2000步后立即消失”的解释；不能据此转成无teacher可部署方案。

学习／遗忘：2000步后每250步及最后3750→3816的66步区间均已统计；阈值沿用R04。掌握率沿用teacher33B可学集合及ln2／2ln2迟滞，毛流量只统计可见快照，baseline稀疏采样会漏掉中间反复。完整表、解释和数据缺口见[分析报告](/data/250010109/Research_System/daily_research_reports/1111/meeting_report/a5_to_1B/README_cn.md)。

单种子；baseline来自原硬件训练；A5分发依赖teacher；提示泄露仍未排除。训练结束后分析在本次保留Reserved任务内完成，没有使用MIG，没有重复提交baseline前向。分析完成后控制器退出并释放任务，平台终态由监督回执核验。
