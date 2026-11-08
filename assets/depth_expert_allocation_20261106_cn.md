# 分层专家分配的实际输出资产

<!-- owner: depth_expert_allocation actual registration guide -->

[English](depth_expert_allocation_20261106.md) · [当前限定访问快照](checks/20261106T175506021038Z_depth_expert_allocation_full_outputs.json) · [登记收据](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/asset_registration_full_20261106T175506021038Z/registration_receipt.json)

| 资产 ID | 实际对象 |
|---|---|
| `checkpoint_family_depth_expert_allocation_smoke_20261106` | 7个完整保存状态 |
| `data_depth_expert_allocation_formal_frequency_20261106` | 分层MoE正式共同预算真实目标token频率与冻结分桶 |
| `checkpoint_family_depth_expert_allocation_A_20261106` | 3个完整保存状态 |
| `checkpoint_family_depth_expert_allocation_B_20261106` | 3个完整保存状态 |
| `analysis_depth_expert_allocation_20261106` | 分层MoE共同预算A/B频率桶与路由计算完整分析 |

这里只列已经登记、确实保存的对象。载荷保留在 /data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation。快照仅检查所选输出与输入的读取条件，不是全库刷新。科学接受保持 Unknown。

formal_frequency按共同预算定义的完整目标流计数；登记该文件不证明两组已经完成这些曝光。checkpoint成员分别保存实际step/token计数、完整manifest匹配的当前文件SHA256与大小，并通过CPU meta/mmap检查优化器、调度器和4rank RNG结构。该结构检查没有进行模型推理。

连续训练与外部恢复的逐位证据只适用于replay_micro16.json记录的A Smoke比较终态；其他成员的逐成员外部恢复仍为NOT_CHECKED。step0是随机初始化，不继承预训练模型权重，只复用已有tokenizer和DCLM派生数据接口。Smoke与正式状态使用不同资产身份；登记不证明语义长尾知识或路由因果机制。

[正式R01 Protocol](../Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/protocol_cn.md) · [实际成员清单](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/actual_output_members)


## 2026-11-07逐层路由时间诊断

新资产 `analysis_depth_expert_allocation_routing_temporal_20261107` 保存两组各874步训练日志的事后检查。[中文分析](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/routing_audit_20261107/routing_review_cn.md)、[产物清单](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/routing_audit_20261107/artifact_manifest.json)与[本次输入／输出访问检查](checks/20261107_routing_temporal_analysis_access.json)绑定实际保存产物。本次无新前向或训练。整轮零接收专家仍为0；短时出现零接收的层更新为A2/B37，均在warmup内，后期负载恢复均衡；因果机制Unknown。新访问快照仅覆盖父分析与该派生输出，未刷新全部模型资产。


## 2026-11-07固定权重偏置干预

资产 `analysis_depth_expert_allocation_bias_intervention_20261107` 保存10个既有状态在同一完整DEV上的保留偏置、同隐藏状态去偏置及完整传播去偏置选路。[中文分析](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/bias_ablation_20261107_v3/review_cn.md)、[产物清单](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/analysis/bias_ablation_20261107_v3/artifact_manifest.json)、[本次访问](checks/20261107_bias_ablation_analysis_access.json)。本次无训练；10状态与同设备原评估器逐文档精确一致，对原四卡NLL的2e-5复现门槛仍FAIL并单独保留。正式早期权重缺失，浮点资格通过的排序约束覆盖A75/136、B69/152个集中层更新。训练历史因果仍Unknown。
