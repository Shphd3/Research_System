# V2 符号辅助数据

资产 ID：`data_symbolic_moe_v2_20261024`。

数据位于[执行目录](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_data/)。
[生成与取样实现](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_engine/data.py)
保留原方案的 32 个符号、四个 F 操作和四个 G 操作。每个操作是一张固定置换表。
每对操作的 32 个输入划分为 20 个训练、6 个验证、6 个测试输入。
全部符号都出现在单操作训练中；父模型的验证和测试只改变措辞，不能称为未见符号泛化。

[本次严格访问检查](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/symbolic_input_access.json)
覆盖该数据、准确的官方 Base 及其 tokenizer。
[数据审计](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_data/audit.json)、
[曝光审计](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/symbolic_data/exposure_audit.json)
和 [API 审计](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/symbolic_api_audit.json)
记录实际文件、标签规则、随种子改变的批次内容及精确高低频曝光量。
这些 CPU 检查不证明模型已经学会，也不证明功能复用。

答案为 `s0` 至 `s31`。已用真实 tokenizer 核对其多 token 编码；评价开放生成的完整符号答案。
C 父模型采用另一套固定置换，错误规则的干扰仍是竞争解释。答案符号的曝光频率已保存，未声称完全匹配。

## 实际保存的产物

[本次限定输出访问检查](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/audit/actual_output_access_20261024T160859729494Z.json)
覆盖截至 2026-10-25 00:08 北京时间已存在的一个工程 Smoke 状态、三个前缀缓存和五个完成的检查点家族。
它不覆盖计划轨迹或后续新增保存点。
[登记清单](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/registration_actual.json)
列出确切 ID；各完成轨迹的 `registration_actual.json` 保存实际成员路径、大小、计数、张量接口及恢复字段。

[登记工具](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/source/register_actual.py)
提供 `register_completed_run(result, cfg)`，可在后续轨迹完成时调用。
工具持有协作写入锁后最小新增，保留已有登记。终点 SHA-256 为本次实际计算；中间保存点和大缓存的 hash 明确记为 `NOT_RECOMPUTED`。
这些增量不包含完整模型，加载需要准确的官方 Base。
未通过科学资格的状态仍可保存和登记；登记不会把它变为合格模型。

后续调用保留既有家族，核对当前成员集合、路径及大小后复用历史验证证据。
当前清单明确标注这种复用，不声称重新计算了 hash 或重新反序列化张量。
首次登记的新家族仍需完整元数据、实际参数范围和计数检查。
已完成的外进程工程状态、原生逐题预测、诊断激活及方向、匹配单项读出和重载报告分别登记。
每组都需要实际完成依据，不纳入计划文件或尚未写完的结果。

最终限定访问检查覆盖 [52 个实际输出组](checks/20261024T165200_order_v2_final_actual_outputs.json)。
[覆盖记录](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/actual_output_coverage.json)
核对全部 152 个检查点文件、4 个前缀缓存和 32 个派生分析组。
152 个检查点包括 148 个任务轨迹状态、3 个外进程恢复工程状态和 1 个原始 Smoke 状态。
三个订单诊断目录各有 36 个实际文件，均已登记；完成状态、缓存和诊断文件没有遗漏。
[终态作业索引](/data/250010109/MoE_Router/experiments/20261024_order_moe_v2/provenance/final_job_terminal_index.json)
保留本轮全部五个作业的完整平台终态，五个作业均已成功终止。
工程收束不改变单项资格失败，也不将内部复用从 Unknown 升级为支持。
