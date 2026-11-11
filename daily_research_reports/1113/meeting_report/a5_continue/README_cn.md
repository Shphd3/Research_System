# 1113｜A5 持续续训与梯度信噪比

AI 分析。研究者判断 Unknown。

A5 从 R06 第 3816 步完整状态续训。现有正式作业 `om-8v93ahuv` 在 share-space Reserved 上使用两台各两张 H100 80GB。初次提交的 5090 作业 `om-5a7km9c8` 已按研究者指示停止，未产生优化器更新。正式训练的前 20 步用于启动验收。

- [R07 执行协议](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A17/17_13_ntp_statistics_local_compatibility/R07_20261111_a5_continue/protocol_cn.md)
- [H100 单机与双机速度对比](H100_单双节点速度.md)
- [启动时长预估](/data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/eta_startup.json)
- [平台监督记录](/data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/supervision.jsonl)
- [A5 源存档与原生对齐节点](/data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/inputs.json)

测量 A 在每个新对齐存档发布后运行。它保存 A5 固定评估集的逐位置损失和每层 Top-2，与原生 MoE、Dense 的同里程碑结果做文档配对比较。区间反映评估文档抽样。每一步 A5 继续使用 262,144 个有效 token，A5 和基线的实际累计 token 均在表中列明。

测量 B 在训练验收后使用 MIG。低频和高频各用 4 份互不重叠的 DEV 批，每份 32 条序列。R03 A0 第 2000 步是独立标记的代理，因为正式原生 MoE 的这一步存档缺失。报告区分总体 expert/FFN 参数块和按路由名额加权的逐专家读数。梯度只用于测量，模型和偏置保持冻结。

## 已出结果

H100 任务通过第 3817–3836 步验收，四个 rank 都完成了在线编码。训练 CE 均值 3.7644，每步有效 token 为 262,144。启动段计算更新中位数 2.926 秒。第 3836 步完整滚动存档已发布。[启动回执](/data/250010109/MoE_Router/experiments/20261111_a5_continue/evidence/startup_h100_2x2.json) · [存档清单](/data/250010109/MoE_Router/experiments/20261111_a5_continue/checkpoints_index.md)

同等训练批量下，历史单机四 H100 的 A5 更新略快。本轮双机延续 R06 的 8×4 微批与累积，历史单机是 16×2。拓扑本身的耗时差需要同一存档、同一微批与累积的对照。[持续更新的速度表](H100_单双节点速度.md)

测量 B 已完成六份可用存档的初始测量。约 1B 时，A5／原生 MoE 的整个 expert 参数块梯度信噪比，低频为 **1.203**，高频为 **0.936**，符合预写方向。逐 expert 计算再按名额加权时，比值为 **0.925** 和 **0.813**，低频优势没有出现。第 2000 步只具备 R03 A0 代理，该比较也没有出现低频优势。结果支持约 1B 的整体梯度读数，对专家内部的梯度改善仍缺乏支持。六存档测量和固定 teacher 分数缓存耗时约 347 秒。[比值与预测](B_比值与预测.md) · [逐专家表](B_逐专家.csv) · [信噪比图](B_梯度信噪比.png)

测量 A 已接入 R06 的 1B 起点和配对区间。3B、5B、10B 分析随对齐存档发布更新。[里程碑表](A_里程碑总体NLL.md) · [NLL 差图](A_里程碑评估损失差.png)
