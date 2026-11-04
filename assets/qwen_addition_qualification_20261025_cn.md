# Qwen3 加法资格初筛数据

本次只完成零更新 DEV 资格测量；严格输出基础资格未通过，未进行训练或 TEST 模型评测。

- 固定数据 ID：`data_qwen_addition_qualification_20261025_seed20261025_v1`。
- 存储：`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/data`。
- 种子 20261025；x、y 均为 10–99，包含相等数对；先划分 2,400/300/300 个无序数对，再生成基础/A/B，所有任务在同一集合，和值可跨集合。
- 原始父模型与 tokenizer：`model_qwen3_0p6b_base` / `tokenizer_qwen3_0p6b_base`。
- 生成器、完整清单及内容哈希位于 execution；[一页结果](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/summary_cn.md)、[完整来源和边界](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/detailed_cn.md)。

数据字节在模型评测前锁定并核验，注册在评测后补齐；不声称事前登记已完成。TEST 只用于生成、哈希和数对划分检查，未输入 tokenizer/模型。没有适配器或训练检查点产出。此访问记录不授予未来执行权限或科学资格。
