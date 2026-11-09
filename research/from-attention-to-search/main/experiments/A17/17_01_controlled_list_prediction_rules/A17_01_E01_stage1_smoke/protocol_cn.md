# A17_01_E01：第一阶段工程Smoke契约

[完整英文Protocol](protocol.md) · [中文Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor_cn.md)

授权范围：数据与代码实现、四卡H100 reserved Smoke，以及Base/Dense/S7的初始能力检查；Dense和Qwen Base短训练，S7只读。研究者已明确要求现在开始代码和测量。Full、频率训练及表征研究未授权。科学判断Unknown。

## 0. Approval Snapshot

状态APPROVED_FOR_IMPLEMENTATION_AND_SMOKE。A–G仅对工程Smoke确认，跨块PASS。以下例数、优化器和时间上限为授权范围内固定的工程选择，不是后续科学操作点。问题是数据/答案损失/训练/更新读出能否核验。

## 1. Terminology / Definitions

顺序未见：组合训练见过，完整顺序没见过；组合未见：组合也没见过。每三词不同，首/末项规则目标前可见，答案在答案标记后预测。

## 2. Anchor Alignment

真实接收损失差，负帮助正伤害，四格与不更新参照齐全。帮助变少不叫伤害。

## 3. Tested Hypothesis

仅核验工程链路；共享解析帮助与局部伤害的科学竞争尚未判定。初始能力不是完整规则掌握证明。

## 4. Rival Explanations

位置偏好、已有能力饱和、目标错位、恢复失败和步长过大。保留oracle、初始能力、不更新与恢复检查。

## 5. Data Construction And Provenance

20个中文单词元，唯一固定句式；训练每规则2,000、开发400、测试400，共5,600行。开发/测试分别含顺序未见200和组合未见200个基础列表。循环平移的无序组合轨道用于精确均衡；训练每词每位置100次，每评价类型10次。开发/测试有序列表不重复，组合未见内容组互斥；顺序未见有意与训练共享无序组。所有实际前文＋答案都做单续写词元资格。

## 6. Learning Task And Permitted Supervision

只输入前文，从最后有效位置取隐藏状态，映射全词表并算一个答案CE。训练/评价读取train/dev文件，不由模型打开test；test只做构造资格检查。

## 7. Model / Architecture And Frozen Variants

Dense exact33B：8层1024宽，281,431,040参数；Qwen3-0.6B-Base：原生28层。分别独立四rank短训全LM参数，新任务AdamW重置，不沿用原预训练优化器。S7-fresh exact33B保留原生sidecar前向，只读初始能力。不是干净架构对照。

## 8. Training Objective And Optimization

仅答案全词表CE，FP32参数与状态＋BF16 autocast，AdamW学习率1e-4，betas0.9/0.95，epsilon1e-8，weight decay0，clip1。四rank、每rank微批8、累积2，每完成更新64个有效答案且首末均衡。warmup256答案。每模型32更新=2,048答案，非有限立即失败，无跳步。

## 9. Conditions, Seeds, And Checkpoints

种子17，数据1009；S7只读先测，Dense和Qwen分别0→16保存退出，独立四rank进程恢复16→32。16/32保存权重、AdamW、scheduler、各rank所有RNG、进度/确定性下一数据位置。不按test挑模型。

## 10. Primary Metric And Frozen Analysis Plan

工程判据为全部资格门。按规则×两类未见报告CE/准确率，再按答案数合并。单种子Smoke不报机制置信区间。开发全对标OBSERVED_ALL_CORRECT，不等于完整掌握。32更新后，从同一状态分别取32训练首项/末项来源，普通SGD步长1e-5，算四格有限损失；恢复全部权重和RNG，不改AdamW。梯度内积/范数为次级描述。

## 11. Secondary Metrics And Guards

完整全词表top1、正确答案概率及首尾偏好。必需TensorBoard记录遵从根观测契约，只rank0写全局加权值，tokens轴按完成更新累计有效答案；恢复独立segment保留两个坐标。记录梯度、显存、答案吞吐。

## 12. Known Good / Known Bad / Known Confusing Cases

oracle和合并计数为已知好例；重复顺序、缺配对、错误答案、分词错位、非法组合交叉应失败；顺序未见共享组合合法，饱和仅限制解释。CPU小模型检验答案损失、计数和恢复，GPU另行核验。

## 13. Scientific Procedure And Stage Contracts

数据资格→当前资产/四H100运行核验→三模型初始开发能力→两模型短训保存/外进程恢复→最终开发/四格更新→独立产物审计。任何数据/运行门失败立即停止，不提交Full。

## 14. Algorithm, Output, And Provenance Contract

执行根/data/250010109/MoE_Router/experiments/20261009_a17_list_rules。数据、原始日志、权重、配置与源清单均在执行侧。必需数据manifest/qualification、访问快照、三模型初始能力、训练metrics/TB、16/32状态/各rank恢复回执、最终能力/四格/不更新、terminal_verification、pod日志、ACP回执与执行证书。实际保存状态按资产生命周期登记。

## 15. Success / Failure / Insufficient Evidence

所有工程门完成为PASS；真实违规为FAIL；排队或产物缺失为不足。低准确率或饱和不自动令工程失败。科学结果NOT_EVALUATED。

## 16. What This Cannot Claim

不能推出专家必要性、共享/差异功能唯一分解、自然预训练、纯架构效应、长期收益或频率效果；开发结果不变成确认集。

## 17. Block Confirmation, Freeze, And Amendment Ledger

本会话确认工程范围并要求开始；运行前固定Protocol/代码/数据/配置hash。开始后科学契约不覆盖，改动append-only登记。启动观察最多5分钟，排队则交接原job，不重提交。任务硬上限1,800秒=最多2GPU小时。不自动重试或升Full。

