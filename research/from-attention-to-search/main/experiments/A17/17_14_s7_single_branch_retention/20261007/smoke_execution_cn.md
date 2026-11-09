# S7 单处支路：Smoke 执行记录

[English](smoke_execution.md)。2026-10-07，北京时间。

**工程资格通过；正式科学实验尚未运行。** ACP 任务 `pt-1r3ei3wj` 已核实为 `SUCCEEDED`，四组工程收据均为 `PASS`。没有提交正式训练、自动重试或后续机制任务。

## 为什么做

正式问题是：相同训练计算下，MoE 能否保留新任务学习，同时更少损伤旧任务。这次只检查回答该问题所需的训练、恢复和测量链是否可信。若目标错移、冻结失效、恢复不一致或 SAE 替代原生预测，损失差异就不能解释为学习现象。

## 实际操作

在四张 H100 reserved 上分别运行 Dense／MoE、种子 17／29，共四个独立单卡模型。从同一个 fresh S7 检查点开始，只训练末层 Attention 输出投影处的 LoRA；MoE 每个位置选择一个专家，没有额外共享专家。主干和源 FP32 SAE 冻结。先做 8 次 GSM8K 更新，再做 8 次 MMLU 更新，不重放旧数据。

每组在新阶段第 4 步保存状态，通过另一个进程恢复并核对第 5 步，再完成第 8 步。四组共 64 次逻辑更新，另计算并丢弃 4 次恢复参考更新。每组逻辑累计 3,876 个有效答案目标，包含 3,812 个 GSM8K 目标和 64 个 MMLU 目标。两任务分别评价，不用混合均值判断学习。

同一批开发记录保存原生 Attention 输出、固定 SAE 编码及重构残差。把旧输出放回冻结的后续计算，检查能否重现旧损失。这个完整向量重放检查接口，不检验选择出来的方向是否有害，也不代表可训练方法。

## 证据改变了什么判断

支路输出因子确实更新；两组 MoE 在零输出初始化之后有非零路由梯度。主干／SAE 的全部冻结状态哈希不变。独立进程恢复的权重、优化器、随机状态、计数和下一步损失精确一致。TensorBoard 坐标及有效目标计数检查通过，两个种子的配对数据曝光量一致。

四组原生输出恢复后的旧损失绝对误差均为 **0.0**。SAE 位移与重构残差记账通过注册容差。这些结果把“当前实现尚未通过接口资格”更新为“当前冻结版本通过有限工程资格”。

不能据此判断 MoE 更少遗忘。样本很少、训练很短，完整 FLOPs 未对齐；更多存储容量、概率门控使更新变小等解释尚未排除。旧缓存的内部划分含官方 test 来源记录，不是新的官方确认集。Smoke 效果不能用于挑选科学阈值。

## 版本与下一判断

合同：[Smoke 协议](smoke_protocol_cn.md)；正式设计仍为待审 [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_14_s7_single_branch_retention/17_14_s7_single_branch_retention_anchor_cn.md)／[Protocol](protocol_cn.md)。

证据：[执行证书](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/receipts/execution_certificate.md)、[独立终态核验](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/receipts/terminal_verification.json)、[完整工程收据](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/runs/20261007T145134Z/smoke_receipt.json)。[冻结清单](/data/250010109/MoE_Router/experiments/20261007_s7_single_branch_retention_smoke/receipts/freeze_manifest.json)记录代码、合同、配置、数据与原实现哈希。

唯一下一判断是审核正式数据边界、完整计算预算、学习／损伤的实用界以及新学习不劣要求；不自动开始正式运行。
