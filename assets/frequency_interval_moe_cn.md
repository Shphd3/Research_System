# 频率区间残差MoE：实存缓存与Smoke状态

[English](frequency_interval_moe.md) · [Protocol](../Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/frequency_interval_residual_moe/protocol_cn.md) · [本次限定访问检查](checks/2026-10-18_frequency_interval_moe_20261018T103820Z.json)

生产任务`pt-vv7zkyxf`，run为`20261018T103820Z`，72.462秒完成有界诊断。缓存准备和工程Smoke通过。TRAIN正分数路由覆盖未通过事前门槛，正式八臂比较**NOT RUN**。登记不证明学习收益，也不授予科学批准。

- `representation_crosscoder_frequency_interval_moe_20261018t103820z`：[缓存owner](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/cache)。TRAIN/EVAL分别保存130,712/65,402个有效下一token预测位置，来自128/64个完整上下文。192个源上下文共196,608个raw token；另有8个上下文用于原生零旁支检查。缓存包含第28层最终norm前BF16 residual-post、真实t+1标签、完整正值FP32共享CrossCoder z的CSR、源位置、固定A/B路由与冻结评价mask。h/z来自原学习窗口中的同一次提取；与旧h/target/CSR IDs/context/offset逐项完全一致。
- `checkpoint_crosscoder_frequency_interval_moe_smoke_20261018t103820z`：[四个实际Smoke文件](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/smoke/fit_attempt_0)。A/B/C/D每个checkpoint均为**step16、2,048次重复目标曝光、128个唯一源位置**。Smoke完成32更新，但没有保存step32或正式checkpoint。文件包含专家/router参数、实际存在的AdamW状态、RNG、TRAIN输入归一化、完整排列及计数/cursor。原Base/head/CrossCoder仍是独立必需父资产。同进程序列化下一步一致检查通过；外部进程恢复为`NOT_QUALIFIED`。

冻结字典复用已有独立资产`crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`。[补充strict访问检查](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/exact_dictionary_asset_access.json)明确标记为**提取后的元数据核验**，不冒称提取前收据，也不重复提取。实际源码绑定原freeze及Smoke前的[可观测性修订](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/freeze_observability_amendment.json)。

catalog记录实际大小、hash、界面、code/config/Protocol与父ID。缓存hash沿用生产者当次计算值；Smoke checkpoint hash在登记时重新核验。本次访问快照只覆盖两个新family及所选父资产。原文档及近重复独立性仍Unknown；冻结字典训练见过这些文本。后续保存结果分析已登记为`analysis_crosscoder_frequency_interval_moe_20261018t103820z`；见[分析访问检查](checks/2026-10-18_frequency_interval_moe_analysis_20261018T103820Z.json)与[结果owner](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/analysis_results.json)。主q分母为专家位置数；空专家为NA；A/B矩阵统一A频率参考行；低频位置并集独立计数。正式NLL差与训练后谱仍为缺测。
