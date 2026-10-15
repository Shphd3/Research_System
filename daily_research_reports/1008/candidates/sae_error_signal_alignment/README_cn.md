# 1008 候选：SAE 相似 token 的真实误差信号是否同向

**状态：用户已授权直接 candidate 诊断，科学结论 Unknown。** 本轮使用研究者确认的 S7fresh（固定 exact 33B-token 测点）与 Qwen3-0.6B-Base 及其最后层 SAE。只测冻结表征和真实下一词 loss 梯度，不训练 Router、Expert、LoRA 或 SAE。

**执行完成：`pt-c33caya0` 已 SUCCEEDED，实际四卡 H100 reserved。** 两模型各测16,384位置，全部资格通过。先看[候选结果与三组图](summary_cn.md)：总体平均优势为正，但不同真实下一词的优势均转负，原生近邻也更好。完整状态、失败修复和来源见[执行记录](execution_record_cn.md)。

先读[中文 Anchor](anchor_cn.md)，理解 H2、竞争解释和能改变的判断；再读[中文 Protocol](protocol_cn.md)，核对配对、数据曝光、接口和运行条件。英文对应文件为 [anchor.md](anchor.md)、[protocol.md](protocol.md)。这些文件先留在当日 candidate，不创建或改动 Focus/canonical 结论。

本轮将“SAE 原子相似”落实为完整 Top-32 激活码相似，将 δ 定义为真实下一词 CE 对原生 SAE 观测张量的梯度。S7 在末 Attention 输出投影测量；Qwen 在末 MLP 归一化后输入测量。两者分别检验，不能混用 δ 与参数梯度公式。

主要比较：仅凭输入，从 fit 选五个 SAE 近邻，与同领域、同位置区间随机参考比较 δ 余弦。次级对照包括原生 a 近邻、严格相同当前 token 子群、中心化诊断和打乱 δ。两个模型独立报告，支持要求既有相对优势，也有绝对同向证据；零阈值不代表 Router 实用门槛。

数据固定为 1024 条，fit/test 各 512。与旧 1024 条面板精确重叠为零，但与历史 2048 条 NTP-statistics 面板重叠 768 条，来源 N8 曾被审计。因此是固定 readout，不是 fresh/untouched confirmation。

执行归属：`/data/250010109/MoE_Router/experiments/20261008_sae_error_signal_alignment`。原计划一个四卡 H100 reserved 任务，最长四小时；已记录两次原授权范围内的数值实现修正，新任务最长三小时三十分钟，合计预算保持十六 GPU 小时内。first-batch qualification 与正式采集在同一个任务内完成；它只核对实现，不是追加人审。提交前登记真实文件 hash；禁止虚构已冻结、已运行或已支持。

得到正结果最多说明指定 SAE 相似性与指定模型误差方向有关，不能直接证明 Router 训练获益。下一决策由研究者在读完两套结果及对照后作出。
