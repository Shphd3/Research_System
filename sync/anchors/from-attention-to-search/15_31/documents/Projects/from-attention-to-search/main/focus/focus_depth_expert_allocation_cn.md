派生阅读副本；原件位置：`Projects/from-attention-to-search/main/focus/focus_depth_expert_allocation_cn.md`。
[精确原始文件](../../../../../sources/Projects/from-attention-to-search/main/focus/focus_depth_expert_allocation_cn.md)；研究修改仍回到原件。

---

# 把固定专家容量向深层移动，能否改善相对低频 token 的学习？

```text
problem_key: depth_expert_allocation
anchor_id: 15_31
task_state: AUTHORIZED_PAIR_AND_REPORTS_COMPLETE
question_state: USER_ACTIVATED
design_state: USER_SCOPE_WITH_JOINT_ENGINEERING_FREEZE_COMPLETE
result_state: PAIRED_MEASUREMENTS_COMPLETE_PENDING_RESEARCHER_JUDGMENT
human_result_judgment: Unknown
```

## 问题、假设与边界

研究者要比较：总参数相等、top-k与专家宽度相同、训练数据顺序与token预算相同时，把浅层专家移到深层，能否改善相对低频token预测并保持整体语言建模？竞争解释是没有收益，或只是不同频率组之间的权衡。token频率是代理，语义长尾知识与专家因果机制是独立问题。

## 必要比较与已有证据

本问题只含一个核心实验：8层普通MoE的均匀组对深层递增组。研究者在11月6日本轮请求中已明确授权设计、来源与数据核查、共同可用的短测、冻结共同预算，以及4卡H100 reserved上的完整A／B训练和评估。同一范围不重复请求批准。两组短测后冻结最终配置；失败只阻止依赖该检查的阶段，不把未完成写为完成。

白话分析分三步：①核验参数、共同初始化、数据曝光及分桶；②共同短测，冻结预算并完成两组；③比较注册的低频终点，同时报告整体／高频代价、计算和路由负载。完成需两组预算及完整证据链，或明确的失败记录。

可靠低频改善支持进一步验证；改善伴随通用损失则识别权衡；未见优势削弱本具体分配；公平性失效或证据缺失则不足以判断。评估区间不能代替训练种子。导师的分配直觉不是已测结果；既有SAE发现也不能证明本架构的语义或因果收益。

## 研究者判断与唯一下一决定

科学接受、机制判断与问题关闭仍为Unknown。完成有界成对结果后的唯一下一决定是：实测潜力是否值得推进实体／关系及表征或功能验证。不自动启动下一架构或干预。

## 来源

[Anchor](../problem_anchors/15_spectral_representation_and_functional_routing/15_31_depth_expert_allocation/15_31_depth_expert_allocation_anchor_cn.md) · [Protocol](../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/protocol_cn.md)。结果在注册时为NOT RUN；后续事实记录须保留失败和缺失。精确执行由Protocol持有。

当前执行事实：A／B均完成229,113,856个有效目标、874次更新及全部起点／中点／终点评估。共同配置和预算见[冻结回执](../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/joint_freeze_cn.md)，完整结果由[Summary](../experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/summary_cn.md)持有。低频终点实测B−A为+0.217210 nat/token，整体为+0.014258；原始指标显示本轮B更差。实际输出登记、独立复核及报告已完成，科学接受、机制判断及是否继续仍待研究者决定。
