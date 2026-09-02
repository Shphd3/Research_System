# 10B 五臂训练终点评估合同

状态：用户已批准在已完成训练上执行；不重训、不改模型、不改数据。

## 1. 唯一主裁定

在相同模型、初始化、数据顺序和约 10B 训练 token 下，哪个 Router 在同一批
1,024 篇未见文档上的 next-token NLL 最低？NLL 的单位是 nat/token，越低表示
模型给正确下一个 token 的概率越高。

每个 seed 内使用同一文档做配对差：

$$
\Delta L_{A-B}=L_A-L_B.
$$

$\Delta L<0$ 表示 A 更好。只有两 seed 都同向、且各自文档级 95% 配对区间均
低于零，才称 A 决定性优于 B。否则只报告点估计排序或“未分出胜负”。

## 2. 五个直接比较

| 比较 | 只允许回答 |
| --- | --- |
| Centered-Full − Vanilla-Full | 去掉 Router 输入均值的整体效应 |
| Local-HMT − Centered-Full | 动态本层 H/M/T 限制的整体效应 |
| Relay-HMT − Local-HMT | 固定浅层来源相对本层来源的整体效应 |
| Relay-HMT − Centered-Full | 完整 Relay 架构的整体效应 |
| Relay-HMT − Relay-Random | 在已实现随机对照条件下，covariance 频带身份是否额外有益 |

没有 Local-Random，因此 Local-HMT 即使胜出，也不能把收益单独归因于 covariance
H/M/T 身份；它也可能来自动态低维限制或正则化。

## 3. 在线更新目标与基准

在线更新器不是分类器。它的目标是在模型表征持续变化时，追踪固定统计语料上的
EMA covariance 目标子空间，同时不让一次刷新破坏当前路由。

- **精确目标：** 当前 checkpoint 中 EMA covariance 的精确 64/320 维特征子空间；
  Relay-Random 使用注册的固定 Haar 混合目标。
- **固定不更新基准：** 一直沿用 step-0 部署子空间。
- **直接硬切换基准：** 立即把部署子空间替换为精确目标；追踪误差为零，但可能
  让大量 token 突然换专家。
- **实际方法：** EMA + 嵌套 Grassmann + continuity 回溯得到的部署子空间。

追踪准确度使用子空间重合度：

$$
A(U,V)=\frac{\|U^\top V\|_F^2}{k}\in[0,1].
$$

1 表示两个 $k$ 维子空间完全相同；随机 64/320 维空间的期望约为
64/768=0.083 和 320/768=0.417。另报告 RMS 主角度，0°最好。

连续性同时报告高置信 route flip、全部 token flip、最大专家份额变化和
margin-normalized logit change。准确度必须与连续性共同解释。

## 4. 训练过程与机制指标

- 11 个保存点均报告 NLL、逐层负载、有效专家数、margin 和固定-token route churn。
- 在 0/2B/6B/10B 报告：强制遍历专家后的选择遗憾、实际使用专家上的梯度冲突、
  专家输出冗余。
- 训练 loss 在每次刷新前 16 步与后 16 步做事件研究，并减去同 seed
  Centered-Full 在相同步数的变化；它只能判断刷新与跳变是否同现，不能单独证明因果。

## 5. 结论边界

10B 配对 NLL 决定方法表现；负载、冲突、遗憾、冗余、gamma 和追踪准确度只解释
机制。行为更均衡、更新更平滑或冲突更低，都不能替代未见文本质量。
