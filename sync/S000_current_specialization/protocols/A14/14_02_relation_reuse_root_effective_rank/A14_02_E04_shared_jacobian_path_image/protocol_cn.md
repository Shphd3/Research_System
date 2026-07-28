# 协议：A14_02_E04 共享 Jacobian / 路径像

英文 [protocol.md](protocol.md) 是执行合同；本文是同步中文说明。

## 0. 执行快照

**授权状态：** 用户已在 2026-07-25 明确授权自主实现、smoke、正式运行和最小
后续实验，不设置新的审批停点。

**唯一问题：**

> 在一个已经学会同一任务映射、并能把它应用到未见 alias--entity 组合和独立
> contexts 的单层单头 causal Transformer 中，calibration 定义的任务参数方向
> $G_m$ 是否在 held-out contexts 上进入同一个低维 ROOT Jacobian/path image？

**主指标：**

$$
\tau_J^2(8)
=
\frac{\sum_{i>8}\lambda_i(C_{\mathrm{test}})}
{\sum_i\lambda_i(C_{\mathrm{test}})},
\qquad
C_{\mathrm{test}}
=
\frac1{ng}\sum_x
[J_\rho(x)G_m][J_\rho(x)G_m]^\top.
$$

同时要求 calibration 得到的前八维 ROOT image 在 final test 上解释至少
$85\%$ Jacobian 能量。

**支持：** 能力和数值守卫通过，至少 4/5 seeds 满足
$\tau_J^2(8)\le0.10$ 且 calibration-to-test capture $\ge0.85$。

**反驳：** 能力和数值守卫通过，至少 4/5 seeds 满足
$\tau_J^2(8)\ge0.25$ 或 capture $\le0.70$。

**证据不足：** 能力通过不足 4 seeds；task-gradient 前八维能量低于 $0.80$；
两种有限差分步长的 Jacobian 相对差异超过 $0.05$；known-good/known-bad
控制失效；或结果落在两个裁定区间之间。

## 1. 设置

序列为：

```text
ALIAS_r ENTITY_a CONTEXT_c ROOT ANSWER_pi(a)
```

16 个 surface aliases 共同调用同一个非恒等 permutation $\pi$；答案与 alias
和 context 无关。每个 alias 留出 2/8 个 entity cells 不参与训练，但每个 alias
和 entity 都在其他组合中充分出现。每个 relation 的训练、calibration 和 final
test contexts 分离；所有 context token 又会在其他 relation 的训练中出现，避免
未训练 embedding 混杂。

模型是宽度 64 的单层单头 pre-norm causal Transformer，使用全位置 NTP。
checkpoint 只读 calibration capability，不读取 test Jacobian 或投影结果。

## 2. H9 的操作化

只在 calibration 数据上，对第一层 attention 与 MLP 参数计算逐样本 answer CE
梯度。其前八个右奇异方向定义 $G_m$。对每个 held-out context 计算

$$
Z_x=J_\rho(x)G_m.
$$

如果这些矩阵的列跨 context 仍主要落在同一个八维 ROOT 空间，H9 在该注册模型中
得到支持；如果它们旋转成大规模方向并集，H9 被该模型反驳。

## 3. 必要控制

- 未训练 checkpoint：判断共享性是否只是架构先验；
- 同维随机参数方向：判断任何参数子空间是否都会显得低维；
- 人工固定 image：known-good；
- context 随机旋转 image：known-bad；
- 冻结输出头可见空间与其零空间分解：判断 raw H9 失败是否只来自任务不可见
  gauge/nuisance；
- calibration ROOT image 投影 + 冻结原输出头：检查几何结论是否保持任务功能。

## 4. 结论边界

实验只裁定该单层模型和冻结生成分布中的 H9。它不能证明自然语言、任意
Transformer、多层 LLM、完整参数矩阵或 raw hidden state 普遍低秩，也不能推出
Router 价值。

