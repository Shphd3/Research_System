# 结果摘要：自然 NTP 表征预测局部更新相容性

[Anchor](anchor_natural_ntp_representation_compatibility_cn.md) · [冻结 Protocol](protocol_cn.md) · [完整证据记录](detailed_cn.md) · [English](summary.md)  
结果状态：**主检验合格且 `NON_SUPPORT`；确认集有限步 `NOT_RUN_BY_BRIDGE`；14 个结构读出 `NOT_RUN_BY_GATE`**。研究者科学判断：**Unknown**。

## 1. 目的

检验看见真实下一词之前的原生表征，能否预测两个自然下一词任务在同一注意力矩阵上的连续局部更新相容性。

## 2. 假设

在未见文档上，仅用矩阵输入表征预测梯度内积 \(K\)，相比训练集均值常数可至少降低 5% 的均方误差。竞争解释是：真实下一词和下游误差信号中剩余的变化，使本次指定读出器难以从表征提取足够信息；\(K\) 的梯度恒等式本身不保证预测成功。

## 3. 分析方法

- 固定 S7 的 33B 训练词元检查点和末块注意力输出矩阵；每个文档取一个“256 词元前缀→1 个真实目标”事件。训练集 32,768 对、开发集 512 对、确认集 1,024 对；确认对不共享文档端点。训练四维几何读出器与完整 \(c\) 读出器，由 DEV 选定，先封存预测再开放 CONFIRM 真值。
- 在确认集计算 \(Q=1-\mathrm{MSE}(q_*)/\mathrm{MSE}(m_{\rm TRAIN})\)，对文档对重抽样 2,000 次形成 95% 区间。预定支持门槛为 0.05；区间上界低于门槛即“不支持”。
- 独立用 DEV 校准临时、仅修改 \(W\) 的共同 SGD 步长；只有主结果支持时才运行 14 个结构读出。

## 4. 结论

**本次指定设置下，“表征可带来至少 5% 的留出预测改善”不获支持。**开封前 DEV 选中的完整表征读出器，在确认集得到 \(Q=-0.000138\)，条件性 95% 区间 \([-0.002768,0.002294]\)，整个区间低于 0.05。1,024 对上的常数预测 MSE 为 0.638792，选中读出器为 0.638881。几何读出器 \(Q=-0.001285\)，区间 \([-0.003768,0.001165]\)。主检验所需的数据、数值、拟合、封存与身份资格均通过，因此这是该预注册比较的“不支持”，不是程序失败。[原始预测](</data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/frozen/confirmation_predictions.npz>) · [主分析](</data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/analysis/primary.json>)。

开封后补齐、未用于重选的预定描述性读数：预测与真 \(K\) 的 Spearman 秩相关为完整表征 −0.0043、几何 −0.0072；数据对梯度余弦均值为 0.00101；1,024 对中 508 对的 \(K\) 为正。其条件区间及来源见 [secondary.csv](</data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/analysis/secondary.csv>)。这些描述不改变主裁决。

| 预定判断 | 实测 | 资格 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| 主 \(Q\)：95% 区间下界 >0.05 才支持；上界 <0.05 为不支持 | 完整表征 \(-0.000138\)，区间 \([-0.002768,0.002294]\) | 合格；DEV 预选，确认 1,024 对 | `NON_SUPPORT` | [primary.json](</data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/analysis/primary.json>) |
| 有限步 DEV 桥：两种步长均须至少 80% 一阶作用高于数值分辨率，另有其他护栏 | 最大候选步长 62.5%，半步 50%；其余候选更低 | 仅有限步桥不合格 | 确认有限步及 \(Q_I\) 未运行 | [DEV 有限步记录](</data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/finite/dev_finite.jsonl>) |
| 结构比较须以主结果支持为门槛 | 主结果 `NON_SUPPORT` | 依预定门槛跳过 | 14 个读出均未运行 | [条件台账](</data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/structure/condition_ledger.json>) |

![确认集真实与预测 K，以及 Q 区间](../figures/primary_q_and_prediction.png)

**读图：**左侧每点是一对确认文档；真实 \(K\) 有正有负且跨度大，预测集中在训练均值附近。右侧两种读出器的 \(Q\) 区间均靠近零，距离 0.05 门槛较远。[图源](../figures/SOURCES.md)。

**边界：**结论限于这个 2.81 亿参数主干、33B 训练词元检查点、矩阵、DCLM 文档开头总体和指定读出器。不能由此断言表征普遍没有信息、条件方差不可消除、自然冲突群已找到、有限步损失预测已失败，或分开训练／Router有益。95% 区间只覆盖固定读出器和本语料的配对抽样；历史事件曝光不能完全核实。

**下一决定：**研究者判断仍为 **Unknown**。供讨论的 **AI 建议** 是判断本次操作化是否到此为止，还是针对“读出器／样本能力不足”与“矩阵输入信息不足”的竞争解释设计一次新的前瞻测试；不能再用本次已开封 CONFIRM 调参。
