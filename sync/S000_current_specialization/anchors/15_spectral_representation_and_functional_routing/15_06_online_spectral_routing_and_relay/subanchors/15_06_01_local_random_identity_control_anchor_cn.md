---
anchor_id: 15_06_01_local_random_identity_control
parent_anchor: 15_06_online_spectral_routing_and_relay
status: completed_control_recorded
canonical_language: zh
companion_en: 15_06_01_local_random_identity_control_anchor.md
updated: 2026-08-08
---

# A15_06_01 本层随机频带身份对照

Thinking Card：[15_06_01_local_random_identity_control_thinking_card_cn.md](15_06_01_local_random_identity_control_thinking_card_cn.md)

本子 Anchor 从临时编号 `A15_01` 迁入；原始 worker 产物保留该历史编号。

## 1. Problem Definition

本子 Anchor 继承 A15_06，只裁定一个未决点：Local-HMT 的弱终点优势究竟来自
covariance 排名身份，还是任意平滑、动态、同维的本层子空间也能复现。主指标是
既有 Local-HMT 与新 Local-Random-Matched 在 10B 终点的逐文档配对 NLL 差，
单位 nat/token，越低越好。

## 2. Physical Priors

随机对照只有在维度和随时间变化的目标运动量都与 H/M/T 匹配时才具有因果解释力。
对当前嵌套 H/M/T 基底左乘一个固定正交矩阵，可以严格保持相邻刷新间的全部
principal angles，同时删除 covariance 排名身份。

## 3. Falsifiable Hypotheses

- **H1，covariance 身份：**两个 seed 中 Local-HMT 都优于
  Local-Random-Matched，且逐文档配对区间均低于零。
- **R1，一般动态约束：**随机对照匹配或优于 HMT，或者两个 seed 方向不一致。
- **R2，追踪失配：**HMT 表面更好，但随机臂的实际部署—目标追踪明显更差；此时
  不能完成 covariance 归因，只能判 insufficient。

## 4. Mathematical Model

第 $\ell$ 层第 $k$ 次刷新得到嵌套目标
$F_{\ell,k}=(U_{64},U_{320})$。对每个 seed 和层固定采样 Haar 正交矩阵
$O_{s,\ell}$，并定义

$$
F^{rand}_{\ell,k}=(O_{s,\ell}U_{64},O_{s,\ell}U_{320}).
$$

正交左旋转严格保持嵌套、秩以及相邻目标间的 principal angles。随后部署基底使用
与 Local-HMT 相同的 EMA、Procrustes/Grassmann 候选与路由连续性守卫。

## 5. Computational Realization

新 arm 只改变第2--4层使用的目标嵌套基底。第一层仍为 Centered-Full；后续
Router 各自读取本层表征，并沿用 64/256/448 的 H/M/T 维度。专家始终接收完整
本层状态。模型、同 seed 的 step-0 参数、DCLM 数据顺序、优化器、学习率、LB、
statistics/guard 文本、里程碑、验证文档与 10B 预算均与 E01 配对。

## 6. Minimal Falsification Tests

只补 seed 17 和 29。Full 前必须用单元测试和 8 卡 smoke 验证目标运动等距、
嵌套投影合法、step-0 一致、token hash 配对、exact resume 和完整 telemetry。
终点直接复用已完成的 Local-HMT 与 Centered-Full 逐文档 NLL。

## 7. Current Evidence

E02 两个新任务均完成10B。Local-Random-Matched 的终点 NLL 为
3.60411/3.60076（seed 17/29）。Local-HMT 减 Local-Random 的逐文档配对差为
$-0.005370$ [$-0.006858,-0.003969$] 与
$+0.001272$ [$-0.000265,+0.002925$]。Seed 17 明确偏向 HMT，seed 29 点估计
反转且区间跨零，因此 covariance 身份未跨 seed 复现。

随机旋转把相邻目标 principal-angle 运动保持到最大
$1.23\times10^{-14}$ radians，且随机臂的部署—目标 overlap 高于 HMT，全部
追踪可比性 guard 通过。因此裁定为 `fail_no_stable_covariance_identity_advantage`，
不是 tracking insufficient。

Protocol：[A15_06_E02](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/protocol_cn.md)

结果：[Summary](/Projects/from-attention-to-search/main/experiments/A15/15_06_online_spectral_routing_and_relay/A15_06_E02_local_random_identity_control/summary_cn.md)

## 8. Claim Boundary And Next Decision

本四层模型、两个 seed、10B 设置不支持把 Local 效应归因于 covariance 排名
身份。本结果不能建立 H/M/T 的普遍语义、规模普适性，也不能否定由损失或专家
效用定义的区分性方向。唯一下一决策是：先做 held-out 功能准入，检验专家相对
效用定义的区分性 side 是否增量预测 expert choice regret 或共同训练兼容性；
通过前不再扩大固定 H/M/T Router。
