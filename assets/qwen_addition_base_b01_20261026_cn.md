# Qwen3 基础加法B01 LoRA状态

基础DEV第20/40步分别297/300与300/300，按连续两次门槛在40步停止。这是看过DEV错误后的开发资格结果；TEST与A/B均未测量。[English](qwen_addition_base_b01_20261026.md)。

| 资产ID | 实际保存 | 达到进度 |
|---|---|---|
| `adapter_qwen_addition_base_b01_20261026_seed20261025_initial` | 零输出初始LoRA与初始恢复状态 | step0，0 token |
| `adapter_qwen_addition_base_b01_20261026_seed20261025_endpoint` | 确认终点LoRA、optimizer/RNG/数据位置等恢复状态 | step40，9,217有效token，2,560样本暴露 |

payload在 `/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/checkpoints/`，不含完整父模型。父模型/tokenizer为 `model_qwen3_0p6b_base` / `tokenizer_qwen3_0p6b_base`，训练数据为 `data_qwen_addition_qualification_20261025_seed20261025_v1`。只有block14 Q/K/V/O rank8 alpha16 dropout0 LoRA，81,920个FP32参数，原模型BF16全冻结。

端点SHA-256：`e0b5321c343d88aac3c8118fb400086ee853f2157c58a12d53a3ad77ea1aecbb`。[本次两产物strict收据](checks/20261025T161625Z_qwen_addition_b01_actual_checkpoints.json)。[一页结果](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/summary_cn.md)与[加载入口](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/source/load_start.py)保留完整配置、来源和边界。

未来经批准的两个分支必须加载完全相同的端点、各自统一新建优化器，不能继承本轮Adam历史。外部进程精确resume未检查，同进程状态恢复及adapter精确重载通过；访问和登记不授予下一轮执行权限，也不证明内部common功能。
