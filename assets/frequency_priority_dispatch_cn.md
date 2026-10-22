# CrossCoder 频率优先与实际分发：缓存对照资产

[English](frequency_priority_dispatch.md)

资产 `analysis_crosscoder_frequency_priority_dispatch_20261018t160918z` 登记本轮已完成的 **CPU 缓存分发对照**。它不是新的表征缓存、模型或专家训练检查点。主实验始终读取原门控后 z 与原始命中 x，完整 h 不变；只改变路由候选名单、分组及同一父评分下的实际去向。本轮没有基座/CrossCoder 前向、GPU 分配或训练。

[用户 Anchor](../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_20_frequency_priority_actual_dispatch/15_20_frequency_priority_actual_dispatch_anchor_cn.md)、[用户 Protocol](../Projects/from-attention-to-search/main/experiments/A15/15_20_frequency_priority_actual_dispatch/20261019_dispatch/protocol_cn.md) 与[冻结执行设计](../Projects/from-attention-to-search/main/experiments/A15/15_20_frequency_priority_actual_dispatch/20261019_dispatch/design_freeze.json) 拥有本轮设计。[执行根目录](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_priority_dispatch/20261018T160918Z) 保存名单、路由、计数、评分、代码和回执。最终结果解释由同一实验目录中的 Summary/Detailed 承担；登记不授予科学批准。

父输入为 `representation_crosscoder_frequency_interval_moe_20261018t103820z`；旧逐 feature 审计与原始发现侧 φ 边分别通过 `analysis_crosscoder_feature_owner_routing_audit_20261018t143950z` 和 `analysis_crosscoder_feature_frequency_20261015t143300z` 绑定。tokenizer 与数据资产为 `tokenizer_qwen3_0p6b_base`、`dclm_token_bins_global01`。最终 A22 14层/F16384 字典及 Qwen3-0.6B Base 身份继承父缓存，本轮未重新加载权重。

已保存 O、F、T、Tφ、随机成员表 R11/R22/R33 的 TRAIN 130,712／EVAL 65,402 位置分析。完整输出含：9,615 项可靠池的名单与原频率，964 个固定低频目标，独立的 T10 与原 C=962 项名单；全部策略实际路由、逐专家/逐 feature 的 p/a/q/富集与 NA/分母；频率离散、接收代价、200次描述性上下文块 bootstrap；Tφ 原候选对的 TRAIN 重权、固定边 EVAL 复核及确定性交换记录。T10 是前 **10项**，不是前10%；被排除的评分项仍存在于完整输入，并计入实际频率画像。

Tφ 复用的是原始 `edges_D.csv`，不是旧社区名单。原候选由 global01/local0/shard1 的 D 侧生成，没有使用本轮 EVAL local2/shard247 选边；当前 TRAIN 重新计数后保留16,740条边。交换保持 T 的组人数，并满足平均 log频率离散不超过 T 的1.05倍。提高组内边权只是构造目标的变化，不能直接说明分发有效，更不能说明学习或容量改善。

P 联合第一奇异方向旁支为 **NOT RUN**。限定检查的父缓存、旧学习缓存、phase1/φ来源清单及已登记表征中，没有定位同预测位置、完成原预处理的14层联合 H；实际保存的 hidden 只有末层 `[N,1024]`。不能用末层 h 或 zD 替代，不为此补提取或分配 GPU；其他分支照常完成。

catalog 对已完成84份数值/路由文件及实际执行源码、原始中文文件、冻结设计和回执保存新算 SHA256。登记时图清单尚在生成，因此没有伪造图 hash 或将数值完成写成图已审阅。最终图、文本与便携包以实验交付清单及视觉审阅记录为准。

[本次限定 strict-access 快照](checks/2026-10-19_frequency_priority_dispatch_20261018T160918Z.json) 检查新产物与必要父输入。它不代表全库刷新、完整数据加载认证、文档独立性、科学判断或新的训练授权。EVAL 已被查看，原文档及近重复独立性未知。接收改善仅为分发观察，学习收益和容量提升本轮均未检验。
