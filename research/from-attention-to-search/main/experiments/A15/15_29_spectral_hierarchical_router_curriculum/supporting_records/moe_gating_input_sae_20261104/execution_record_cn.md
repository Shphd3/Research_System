# 冻结MoE33B末层gating输入的独立SAE

研究者于2026-11-04明确授权：冻结普通MoE精确33B，只训练最后一层router输入的独立SAE，对齐原28层Qwen末层MLP输入E16配方、预算1B原始激活位置。4卡H100reserve先完成smoke与真实进程重启恢复，通过后正式提交。

本记录是分析工具的支持材料，不改变P/F设计，不补训Dense，不预称特征语义或科学效果。

[执行约定](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/docs/protocol_cn.md) · [实际配置](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/configs/formal.json) · [来源冻结](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/audit/source_freeze.json) · [当前输入检查](/data/250010109/Research_System/assets/checks/20261104_moe_gate_sae_inputs.json)。

smoke:pt-28etcz4j，待资格结果；正式任务尚未提交。实际状态与保存资产记录见执行目录。


## 实际执行回执

smoke修订2 pt-3l4080ju及真实进程重启恢复全部通过。连续100步与60步退出后新进程恢复至100步的loss、样本、SAE/Adam/LR、四卡RNG、活动统计、计数和冻结bias逐项精确相等。首个尝试在0更新的指纹转换检查失败，修复与原日志单独保留。

正式任务 **pt-zgngnz9q** 已受理，4卡H100 reserve、单节点、244141步／1,000,001,536原始激活位置；最新状态与已核实进度以[执行回执](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/docs/receipt_cn.md)和[平台证书](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/audit/formal_execution_certificate.json)为准。当前仍在节点启动阶段，未核实正式更新，不称已训练。

smoke计算吞吐约25.4万位置/秒，规划训练1.5–2.5小时（不含排队／启动），完整1B吞吐未测。13个实际smoke payload及证据已登记，[严格检查](/data/250010109/Research_System/assets/checks/20261104_moe_gate_sae_smoke_outputs.json)通过。工程资格不是特征语义判断；正式1B端点尚未保存。
