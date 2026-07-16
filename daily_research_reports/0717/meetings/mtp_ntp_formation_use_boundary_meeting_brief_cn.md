# MTP 相比 NTP 改变了什么：从提前监督到标准头使用

## 执行摘要

**核心结论：** MTP 已验证的作用是把信息性未来目标的直接监督提前到较早的共享状态；该信号能够更新共享参数，但不自动成为普通 next-token 主头可稳定使用的功能信息。

**认识更新：**

1. MTP 增加的是未来目标到Branch的直接监督路径，具有直接的一阶梯度更新量。NTP能够随着训练逐渐习得这种更新量
2. 预测范围 $K$ 本身不是关键；只有首次覆盖携带新增任务信息的未来目标时，才产生相应的直接语义更新。越大的K可能意味着更强的梯度冲突。
3. 正的直接语义更新不等于正的完整 MTP 的语义增益学习；其他位置和预测距离的梯度可以抵消它。
4. MTP能达到受控的长程信息形成并且对于共享主干的参数有确定的更新作用，未建立稳定的NTP主头可使用的信息增量。


**研究问题：** NTP 让当前位置直接预测下一个词元；MTP 让同一位置同时预测多个未来词元。当 MTP 首次覆盖紧邻目标不包含的任务信息时，它增加了什么，普通 next-token 主头能否使用该增量？

**我的初始判断：** MTP 引入更远目标的监督，会使 hidden state 包含更多长程语义信息，并自然改善普通 next-token 主头的长程推理能力。

**本次结果：** 受控 K=2 结果建立了 MTP 特有的较早直接语义更新及其共享参数可达性；但完整 MTP 净更新并非始终为正，标准头强使用假说也未通过。

**机制解释：** “直接信号”是较早状态预测信息性未来目标这一项损失造成的更新；“完整目标效应”是所有位置和预测距离的损失造成的净更新，前者可被其他梯度抵消。信息写入后还须经过状态运输、注意力接口和普通主头读出，才能成为功能收益。

**决定性证据：**

1. 较早直接损失对“hidden state 与正确分支输出方向的对齐”产生正更新：均值 `0.002617`，`5/5` seeds 为正且均强于稍后 NTP 路径 `0.001438`；但完整 MTP 更新只在 `4/5` seeds 为正。
2. 信息性 MTP 相对 matched shared-aux（第二个辅助头重复 next-token 目标）的强答案控制增量为 `0.01675<0.10`，`0/5` seeds 达到注册阈值；所有能力与干预有效性检查均通过。
3. 三种目标下，早期位置的注意力 key/value（source K/V）均达到分支线性探针准确率 `1.0`；信息性 MTP 主要把同一分支内由无关变化造成的离散度压缩至 shared-aux 的 `0.021–0.373` 倍，而非普遍拉大分支中心距离，因此只支持“重组已有信息”的二级解释。

**结论边界：** 当前结论仅适用于受控短程 K=2 任务；现有 carrier 存在答案旁路且 matched 表示可读性已饱和，不能定位强使用未出现的原因，也不能推出真实长程语义、组合推理、一般表征可拆分性或 MoE Router 收益。source K/V 信息审计因打乱标签检查失败，正式判定为“证据不足”。

**执行动作：** 下一步只定义并验证一个“必须传递早期信息（relay-required）”的长程组合载体：局部窗口信息不足、早期证据具有反事实必要性、多个证据必须组合、无直接答案旁路，且 matched baseline 可学习但未饱和；全部有效性检查通过后再比较 NTP/MTP，否则重新设计载体。

**来源：** [A11 shared-parameter path decomposition](../../../Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md)；[A11 standard-head causal-use result](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E01_model_local_kv_causal_use/summary.md)；[A11 source-information audit](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md)。
