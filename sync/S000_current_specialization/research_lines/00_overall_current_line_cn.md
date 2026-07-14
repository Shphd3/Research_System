# 当前总体研究线

## 结论

项目包含一条主要路由线和两条相互衔接的 MTP 支持线。它们回答不同问题，不能互相替代。

1. **路由主线：** 受控实验已经把问题从几何可分推进到专家功能和部分反馈；当前缺口是现实代码工作负载中是否存在稳定、可利用的专家效用差异。
2. **MTP 目标机制：** 信息性未来词元会给当前位置增加普通下一词元训练在同一位置没有的直接任务信号；该信号能传到共享参数，但当前位置形成信息不保证下一位置的标准头使用。
3. **MTP 结构任务：** 两张完整映射表构成的深度二任务能严格隔离有序组合，但当前从零训练小模型未学会；线性模型只证明缺少表征方向足以造成 MTP/NTP 权衡。

## 当前主路由决策

当前不再继续设计合成初始化器或 Router 结构。唯一问题是：未筛选的仓库级代码补全中，在控制词元身份、局部上下文、负载匹配和划分过拟合后，是否仍存在跨划分稳定的最优专家差异和正的 oracle 路由收益。

通过该工作负载门槛后，才允许研究实际 Router 如何捕获这些差异；失败则停止把该代码任务当作专家专门化工作负载。

来源：[A06 研究图](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md) · [当前 A06 Anchor](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor_cn.md)

## MTP 支持线

### A11：目标函数的直接差异

最短分支任务让紧邻词元在两个分支中相同，而稍后词元首次揭示分支变量。结果支持：预测范围首次覆盖信息性词元时，当前位置出现新的直接更新；新增目标的作用取决于信息是否新增以及输出方向是否一致。该结果只解释信号形成，不解释结构化任务收益。

### A12：结构化组合与功能使用

任务要求先由第一张表得到中间实体，再用该实体查询第二张表。构造有效，但当前小模型答案准确率仍接近八分类机会水平。下一步只建立一个通过能力门槛的共享预训练检查点，然后才比较 NTP 与 MTP 是否增强标准头对中间实体的因果使用。

来源：[A11 当前故事](../../../Projects/from-attention-to-search/main/stories/11_informative_future_branch_mechanism/01_informative_future_branch_signal_and_use_boundary_cn.md) · [A12 当前故事](../../../Projects/from-attention-to-search/main/stories/12_structured_compositional_mtp_workload/01_structured_composition_workload_and_standard_head_use_cn.md)

## 边界

当前不能声称真实语义专家已经形成、Router 已可部署、MTP 普遍优于 NTP、大模型受益来自表征秩、课程学习已在神经模型中得到解释，或合成组合任务会自动迁移到真实基准。
