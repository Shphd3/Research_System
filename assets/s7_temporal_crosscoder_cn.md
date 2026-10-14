# S7 跨checkpoint CrossCoder 输入与提交任务（A24）

[English](s7_temporal_crosscoder.md)。精确地址、身份和当前访问证据由 `catalog.json` 及检查记录持有，本指南不替代资产库或科学记录。

两家族各使用实际存在的精确1B、5B、15B、31B预训练保存点，31B是双方最接近30B的共同保存点。fresh是原lambda0.1末层Attention SAE sidecar预训练的8层/hidden1024模型；Dense是原无SAE的8层/hidden1024训练轨迹，包含后期续训目录。预训练token数不是CrossCoder曝光数。

8个精确输入ID为 `model_s7_temporal_fresh_{1,5,15,31}b_a24_20261013` 与 `model_s7_temporal_dense_{1,5,15,31}b_a24_20261013`。[本轮严格访问检查](checks/2026-10-13_s7_temporal_A24_inputs.json)逐项列出；每个条目的 `A24_current_CPU_qualification` 绑定新核验文件哈希和原生CPU严格加载结果。GPU加载与恢复仍待目标节点验证。[输入选择](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/docs/s7_temporal_inputs_A24.json)。

复用数据/分词器ID：`dclm_crosscoder_direct_bins_1b_a15_20261013`、`tokenizer_qwen3_0p6b_base`。已有DCLM文件级留出，不声称完成原始文档或近重复独立去重。32组checkpoint×层表示严格对应同一文本位置，不是32倍独立样本。

已授权并提交：fresh任务`pt-5akx5toz`、Dense任务`pt-lful461t`，各8RTX5090Spot、共享32768特征、约10亿位置。[执行合同](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/docs/s7_temporal_scope_A24_cn.md)、[状态入口](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/docs/current_s7_temporal_handoff_A24.json)。提交不等于训练开始；实际保存的完整状态才由任务登记为资产。0.5B保存是要求，不是已完成事实。

共同编码读取后期checkpoint，层间及时间间decoder强度只能描述当前字典的重建覆盖，不能直接证明特征因果起源、学习机制或expert收益。之后使用输入仍须重新执行当前严格访问检查。
