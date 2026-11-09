# 执行修订：用户要求的本地冻结诊断

范围仍为[三个冻结诊断](analysis_contract_cn.md)，数据、第168步权重、种子、混合系数和NLL比较均不变。

用户提出：“是否可以在本地冻结诊断？远端似乎资源不足。”助手已接受为在本地执行本次有界冻结诊断的指令。本条记录构成相对默认 execution envelope 的本阶段资源例外。

当前只读检查确认一个 CUDA 设备：NVIDIA H100 80GB HBM3 MIG 3g.40gb，报告显存42,412,802,048字节，计算能力9.0；PyTorch2.3.0a0+6ddf5cf85e.nv24.04。四个 checkpoint 在 cuda:0 顺序执行；单 worker allocated显存上限16GiB，总CPU线程不超过8。记录实际运行环境、数值重放门槛及源码身份。

输出独立放在 `ablation/local_gpu`。保留全 DEV 原顺序、原batch128、实际专家dispatch形状、各比较共享的缓存残差、原final RMSNorm/LM head和BF16推理。不更新参数，不增加目标，不选模型。

先前GPU创建因成员配额失败。用户随后明确选择“优先完成冻结诊断，再重提普通 MoE”；未启动的普通MoE任务pt-50sa30mo停止后，远端诊断pt-t9lutqt0已接受提交。之后的本地请求替换此次诊断的执行面。保留所有receipt，避免重复运行诊断。普通MoE仍按原冻结配置和h100-4-reserved恢复提交，记录新ID以及旧任务是否存在实际训练进度。

本修订仅改变执行地点与任务次序。资产、身份、数值及科学边界检查继续有效。实际job/device状态和完成情况以执行receipt为准。
