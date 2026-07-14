# 06 路由几何、保持与专家功能主线

## 当前结论

这条线已经从特征能否被路由推进到专家是否真的产生不同功能：

1. 已知任务相关状态时，目标分区在几何上可达；真实 DCLM 代理中心也能在第 0 步被线性路由。
2. 普通训练会迅速覆盖该代理路由。局部保持状态是低尾路由间隔，而不是中心是否静止。
3. 间隔变化同时受专家效用、背景梯度投影、表征运动、Router 运动和优化器传递尺度影响；单独的 common 能量不是稳定根因。
4. 正确条件暴露能产生留出专家功能；只观察被选专家的 top-1 反馈可以保持正确专家，却无法从错误排名发现未选中的有用专家。
5. 在冻结四专家桥接模型中，每步增加一个轮换挑战者可补足反事实反馈，较低尾效用证书可安全切回 top-1。

这些结论均有受控边界，不能直接推出联合预训练 LLM 中的 Router 有效。

当前材料被收敛为五个父问题：怎样定义有功能的专家分工；怎样发现可训练的状态分区；
分区为何保持或越界；专家功能怎样形成并被稀疏反馈发现；真实工作负载是否真的存在
值得路由的功能余量。局部消融和失败控制只作为这些问题的子证据，不再占据平行主线。

## 当前问题

现实工作负载必须先证明存在值得路由的功能差异。唯一决策是：未筛选仓库代码补全中，控制词元、局部信息、负载和划分过拟合后，留出最优专家身份是否稳定，oracle 路由相对基线是否仍有正收益。

最重要指标是 held-out oracle routing headroom：它直接衡量如果每个样本能选择最优专家，相比基线能减少多少损失。路由平衡或高 NMI 只能说明分配结构，不能代替功能收益。

## 通过与停止

- **通过：** 校准集和测试集上的最优专家身份稳定，强干扰控制后仍有正的留出 oracle 收益，并在匹配激活计算和负载的条件下保持。
- **停止：** 收益仅来自词元身份、局部上下文、负载不匹配或划分过拟合；此时不进入 Router 方法设计。

## 来源

- [整线故事](../../../Projects/from-attention-to-search/main/stories/06_geometry_proxy_preservation/01_functional_specialization_and_utility_routing_cn.md)
- [Anchor 研究图](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/research_map.md)
- [当前工作负载 Anchor](../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_04_real_workload_utility_headroom/06_04_real_workload_utility_headroom_anchor_cn.md)
