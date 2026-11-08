派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/source_review_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/source_review_cn.md)；研究修改仍回到原件。

---

# 本轮来源、导师直觉与已有证据

**当前可核实的是来源与参数，不是本轮架构收益。**本轮问题、H1–H3、公平原则、4卡H100 reserved执行及结果边界均来自研究者11月6日本轮明确请求。

| 来源类别 | 当前资料 | 能支持的内容 | 不能补出的内容 |
| --- | --- | --- | --- |
| 导师直觉 | [用户附件原字节副本](supporting_sources/meeting_1106_source.md)，主线1 06:26–11:38、主线2 00:00–01:00 | 浅层少专家／低维，深层更多专家／高维，层级结构与记忆／压缩设想 | 浅层必然只学粗概念、深层专家已证实是独立记忆、已压缩一个数量级 |
| 机制直觉 | 同一来源主线1 01:49–02:31及会议摘要补充 | 信噪比可能解释长尾收益、可能关联学习率和效率 | 已测梯度信噪比，或本文模型已由此改善 |
| 学长口头报告 | 同一来源主线1 00:03–01:35 | 报告教师feature分布指导分发时低频feature对应数据改善较大 | 缺完整指标、数值、样本与对照，不能量化收益或归到本轮 |
| 本人口头报告 | 同一来源本人汇报02:16–02:48 | 报告记忆任务小幅提升、通用任务下降较多 | 缺正式对应数值；不能认定是频率／容量／路由导致 |
| 本人已有SAE结果 | [R17_D1 Summary](../../../../../../../../UNAVAILABLE.md) | 共同粗响应可复用；细分结论受答案词／读出语境、字典保留、支持与内容覆盖限制 | 不能把稀有SAE配置等同语义长尾知识；两SAE独立，不能对齐原子ID |
| 原生模型事实 | [A15_30 Anchor](../../../../../../../../UNAVAILABLE.md)及执行侧model.py | Dense281,431,040参数；普通MoE507,988,992；旧跨模型数据顺序只在明确边界内匹配 | 旧模型总容量不等，不能代替本轮A／B公平实验 |
| 本轮假设 | [15_31 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_31_depth_expert_allocation/15_31_depth_expert_allocation_anchor_cn.md) | 固定容量重新分配可能改善低频预测，可能有代价或无收益 | 当前尚无本轮训练结果或因果机制 |

附件未包含原始录音。现有文件是勘误文字转写和会议总结；【待核】与来源分层必须保留。会议摘要／用户会后补充不能倒填为导师逐字原话。保存副本的SHA与来源说明见 [source_manifest.json](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/source_manifest.json)。

执行参考：`/data/250010109/MoE_Router/experiments/20261101_moe_baseline_speedup/moe_baseline/model.py` 是本轮优先适配的架构源；`speedup/train_fixed.py` 是固定DDP归约与训练流程参考。新实验须隔离适配固定8专家假设、ROOT和初值路径、日志循环及输入配置校验，不能直接当作逐层专家数版本运行。真实复用／适配清单与当前数据资产访问检查由执行侧审计保存，本文不宣称已完成全部短测。

## 实际运行来源附注

初版CPU初值哈希使用seed17；本轮实际seed20261106另有已保存状态PASS审计。短测恢复与部分矩阵FLOPs、分桶例阅读时序及外部注册IO边界由[执行附注](execution_record_cn.md)持有。这里保留区别，不把旧证据改名为实际种子。正式成对结果仍待完成。
