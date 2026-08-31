# 当前总体研究线

> Anchor 发布说明（2026-08-31）：本轮仅刷新根级 Anchor 镜像，不重写本文件的研究判断。镜像已同步 327 个通过链接校验的 Markdown 文件；已被其他对话占有的 `A15_13` 因两个源 Thinking Card 相对链接失效而暂缓发布，继续以项目内源 Anchor 为准。

## 结论

项目包含一条主要路由线、两条相互衔接的 MTP 支持线，以及一个等待研究者确认的长上下文跨线主题。它们回答不同问题，不能互相替代。

1. **路由主线：** 受控实验已经把问题从几何可分推进到专家功能和部分反馈；当前缺口是现实代码工作负载中是否存在稳定、可利用的专家效用差异。
2. **MTP 目标机制：** 信息性未来词元会给当前位置增加普通下一词元训练在同一位置没有的直接任务信号；该信号能传到共享参数，但当前位置形成信息不保证下一位置的标准头使用。
3. **MTP 结构任务：** E04 的 12 条 NTP 轨迹已经完成，但没有规模同时学会一步与两步，删行守卫也因双射补全而无效；线性模型只证明缺少表征方向足以造成 MTP/NTP 权衡。
4. **长上下文工作主题：** 名义上下文容量不等于功能使用；候选 Router 目标应从静态特征对齐转向固定预算下的标准头损失保持，但该目标仍待人的机制判断与协议批准。

## 当前主路由决策

当前不再继续设计合成初始化器或 Router 结构。唯一问题是：未筛选的仓库级代码补全中，在控制词元身份、局部上下文、负载匹配和划分过拟合后，是否仍存在跨划分稳定的最优专家差异和正的 oracle 路由收益。

通过该工作负载门槛后，才允许研究实际 Router 如何捕获这些差异；失败则停止把该代码任务当作专家专门化工作负载。

来源：[A06 研究图](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md) · [当前 A06 Anchor](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor_cn.md)

## MTP 支持线

### A11：目标函数的直接差异

最短分支任务让紧邻词元在两个分支中相同，而稍后词元首次揭示分支变量。结果支持：预测范围首次覆盖信息性词元时，当前位置出现新的直接更新；新增目标的作用取决于信息是否新增以及输出方向是否一致。该结果只解释信号形成，不解释结构化任务收益。

### A12：结构化组合与功能使用

任务要求先由第一张表得到中间实体，再用该实体查询第二张表。E04 的 NTP Stage A 未产生合格规模：2 层两步约 `0.250`，4 层两步约 `0.329`，一个 4 层一步种子仍为 `0.838`；而删去双射一行仍可由剩余值补全。下一步只能关闭 E04，或用新 Protocol 重开载体/能力设计；不得运行 MTP。

来源：[A11 当前故事](../../../Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md) · [A12 当前故事](../../../Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md)

## 等待确认的长上下文跨线主题

建议组会主题是：**从检索命中到功能效用：长上下文 Router 到底应该优化什么？**

问题链为：

```text
证据可访问
-> 信息形成与传递
-> 标准头因果使用
-> 有序组合
-> 固定预算下的 Router 选择
-> held-out 专家效用
```

R3/R4 已确切回答最小 Q0：在当前受控设置中，完美特征专门化不足以形成有效稀疏 KV 索引。建议的 Q1 是比较随机、局部、特征与 attention 选择器的 held-out 标准头损失差，但在研究者填写机制、最强竞争解释、不确定性和证伪条件之前，它仍不是正式实验。

来源：[工作主题](13_long_context_functional_retrieval_working_theme_cn.md)

## 边界

当前不能声称真实语义专家已经形成、Router 已可部署、百万词元上下文已被功能使用、attention 就是正确 Router、MTP 普遍优于 NTP、大模型受益来自表征秩、课程学习已在神经模型中得到解释，或合成组合任务会自动迁移到真实基准。
