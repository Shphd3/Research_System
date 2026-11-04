派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/local_dynamics_20261026/deviations.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R06_functional_protection_20261025/local_dynamics_20261026/deviations.md)；研究修改仍回到原件。

---

# 差异记录

- 读取新结果前：为保证六状态完整且总序列<12000，缩放诊断只测旧探针64和独立旧DEV64，新36只在五个主候选测量；计划11424序列。
- 全部第120步检查点存在，无需回退选择其他时间点。

- 事后数值复放：当前既有H100 MIG与原完整H100训练的第121步提案长度最大绝对差4.871e−8，实际长度最大差4.913e−8；本轮噪声标定在当前同状态内部独立完成，未把跨环境差并入放宽τ。原始数值保持并单列，未宣称跨设备逐字节复放。
