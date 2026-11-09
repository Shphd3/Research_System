---
experiment_id: A15_06_E03_30b_single_seed_extension
legacy_experiment_id: A15_00_E03_30b_single_seed_extension
anchor_id: A15_06_online_spectral_routing_and_relay
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-08
resource_profile: 5090-8-spot
primary_metric: seed17六臂30B终点配对held-out NLL
---

# Protocol：A15_06_E03 六臂单 seed 30B 延长训练与下游评估

## 0. 审批与唯一问题

用户已批准每个 Router 变体使用一个共同 seed，加入 Local-Random-Matched，直接
提交单节点 8×5090 训练到总计 30B tokens，并在终点测下游任务。唯一问题是：
10B 时的六臂排序在继续训练到30B后是否持续、收敛或反转，以及30B终点的语言
模型损失排序是否与下游任务排序一致。

本实验是预算延长复核，不重新选择方法。只使用 seed 17，因此可回答配对轨迹和
该 seed 的终点排序，不能建立跨 seed 稳定性或普遍方法收益。

## 1. 六个条件

六臂为 Vanilla-Full、Centered-Full、Local-HMT、Local-Random-Matched、
Relay-HMT、Relay-Random。它们分别对应完整原始输入、完整去均值输入、本层
covariance H/M/T、运动匹配的本层随机子空间、第一层 covariance Relay、第一层
随机 Relay。专家始终读取完整表征，改变的只是 Gate 所读取的视图。

## 2. 精确续训与固定内容

- 每臂从其 seed17 的完整 `checkpoint-12716` 精确恢复，起点为
  10,000,269,312 tokens；不从头重复10B。
- 目标为 step 38,147，即30,000,021,504 tokens。
- 保持原100B余弦学习率 horizon、636步 warmup状态、AdamW/ZeRO-1、BF16、
  seq1024、global batch768、数据游标、RNG、负载损失、capacity与在线状态。
- 原10B目录只读；30B使用新的 run 目录，保存12B、15B、20B、25B、30B。
- 动态臂在1B以后继续每512步重放相同统计语料；EMA、Grassmann候选与连续性
  守卫不变。

## 3. 结果指标

主指标是30B终点同一1,024篇未见文档的逐文档 NLL，单位 nat/token，越低越好。
对任意两臂 \(A,B\)，报告

\[
\Delta_{A-B}=L_A(30B)-L_B(30B),
\]

并做文档级配对 bootstrap 95% 区间。单 seed 的文档区间只反映验证文档采样
不确定性，不等价于训练 seed 不确定性。

次级指标包括10B→30B的NLL轨迹、晚期斜率、负载、路由熵、capacity drop、
刷新 gamma/flip/lag、专家冲突和冗余。下游套件固定为5-shot的 LAMBADA、
HellaSwag、PIQA、ARC-Easy、OpenBookQA、SciQ；六臂全部测量，不按NLL筛选。

## 4. 裁定

- **该 seed 下持续：** 30B时某一关键差异与10B同向，逐文档区间不跨零。
- **该 seed 下反转/收敛：** 30B差异反向或区间包含零，并结合里程碑定位变化。
- **下游一致/不一致：** 六任务逐项报告；不得用无预注册权重的平均分掩盖任务差异。
- **Insufficient：** 任一臂未到30B且不可恢复，恢复/数据游标/在线状态不完整，
  终点逐文档NLL或下游产物缺失。

不得因早期性能、负载集中、gamma=0或某臂变差而提前停止；这些是科学结果。

## 5. 工程与结论边界

工程守卫包括 checkpoint 完整性、精确恢复、首个恢复步、token hash、投影正交/
嵌套、NaN/Inf、TensorBoard和里程碑闭环。每个任务为单节点8×5090 SPOT，允许
一次平台故障精确恢复。

本实验不能证明H/M/T具有普遍语义，不能用一个seed宣布方法稳定胜出，不能把
下游差异唯一归因于专家功能分工，也不能替代既有两seed 10B结论。训练完成后的
唯一下一决策是：是否由30B轨迹和六任务终点证据选择需要跨seed复核的一个候选。
