派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/joint_freeze_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/joint_freeze_cn.md)；研究修改仍回到原件。

---

# R01共同冻结回执

A／B短测和连续训练／外部恢复逐位核验已通过。正式训练使用同一冻结配置，每组 **229,113,856 个有效预测token，874 个更新**；起点、中点、终点为0／437／874步，即0／114,556,928／229,113,856 token。冻结时刻：2026-11-06T16:50:35Z。最终测试模型指标未用于选设计或预算；已检查测试元数据与示例。

共同批量262,144 token＝4卡×每卡16条×累积2次×2048位置。warmup为87更新＝22,806,528 token，之后恒定学习率3e-4；首更新lr0沿用已验证训练器语义。其他超参以[实际配置](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/common_frozen.json)为准，配置SHA256 `dd768489b9a58a49c09b85fedb9009bb80d7530a63dd235a9bb960265e16f3d5`。A／B非profiler短测中位步时分别为2.0798338661／2.0384610565秒；预算按已注册规则取偶数步，预留1小时训练及1小时评估／IO。该时间是预算选择依据，不是质量比较横轴。

频率按本轮循环训练流的真实监督目标曝光统计，未使用测试频率决定阈值。正频率类型三分位阈值为49／447；边界同计数类型不拆开，零曝光单列。桶均按测试token平均NLL，并保留完整最终测试集整体NLL。

| Bucket | Token types | Test tokens | Test coverage |
| --- | ---: | ---: | ---: |
| low | 30259 | 1481 | 0.21147868% |
| mid | 29950 | 20752 | 2.96327182% |
| high | 30056 | 677902 | 96.80068884% |
| unseen | 61671 | 172 | 0.02456066% |

[原始冻结回执](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/joint_freeze_receipt.json)与[正式频率manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/supporting_sources/frequency_manifest_formal.json)保留源字节。smoke频率独立保存在执行侧data/frequency_smoke；formal保存在data/frequency_formal，未覆盖旧口径。代码与配置hash当前一致，后续必须继续核验。

CPU的initial_parameter_hashes.json使用seed17，只证明初始化实现规则；本轮实际seed是20261106，实际已保存初态的同形张量及router重叠行核验将单独记录。A恢复逐位PASS与B保存事实不自动证明所有正式checkpoint均已做外部恢复。

GPU资源与作业仍为pt-ds9bdaxb、单节点4H100 reserved。此回执仅证明工程关卡与预算已冻结；正式A已启动，A／B完整训练、最终比较、机制判断与科学接受尚未完成。科学接受Unknown。
