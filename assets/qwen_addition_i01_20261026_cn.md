# Qwen3 加法I01独立分支终点

A/B分别训练至200步，均未达到连续两次95%目标DEV门槛：A277/300、基础0/300；B273/300、基础2/300。未做混训、频率或TEST测量。[English](qwen_addition_i01_20261026.md)。

共同起点是已登记B01端点 `adapter_qwen_addition_base_b01_20261026_seed20261025_endpoint`，SHA-256 `e0b5321c343d88aac3c8118fb400086ee853f2157c58a12d53a3ad77ea1aecbb`。两分支保留完全相同的已训练LoRA值，分别用同一种子和空AdamW开始。原模型/tokenizer和固定数据身份继承其已核实父记录，没有重置LoRA或从A继续B。

- `adapter_qwen_addition_i01_20261026_A_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/independent_learning/i01_ab_seed20261025/A/checkpoints/endpoint.pt)，SHA-256 `75a114093129fba0eed9f74cd6559380af56b43a66604ed3e1ba2f7345831f43`；step200，12,800次目标暴露、46,463个有效监督token。
- `adapter_qwen_addition_i01_20261026_B_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/independent_learning/i01_ab_seed20261025/B/checkpoints/endpoint.pt)，SHA-256 `746511b8fcc0db570a77819ab9f05f27467fe3b7edc00a9f2b590169e874c38a`；step200，12,800次目标暴露、46,934个有效监督token。

[两产物当前strict收据](checks/20261025T164223Z_qwen_addition_i01_endpoints.json)、[一页结果](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/independent_learning/i01_ab_seed20261025/summary_cn.md)与[完整配置](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/independent_learning/i01_ab_seed20261025/config.json)保留证据。状态仅包含block14 Q/K/V/O rank8/alpha16/dropout0共81,920个FP32 LoRA参数及optimizer/RNG/order/counters，父模型BF16冻结、不含完整父模型。加载为 `/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/independent_learning/i01_ab_seed20261025/source/engine.py::load_reusable`。外部进程exact resume未验证，同进程状态恢复通过；资格未过只限此设置预算，不能归因容量或A/B共同训练。访问登记不授权后续实验。
