---
anchor_id: 15_05_05_matched_fixed_band_dispatch
legacy_anchor_id: 15_03_matched_band_dispatch_effect
parent_anchor: 15_05_functional_coordinate_admission
status: completed_fail_distribution_only
created: 2026-07-31
canonical_language: en
depends_on: 15_00_router_input_spectral_geometry
---

# A15_05_05 匹配频带分发的 2B 因果消融

## 1. Problem Definition

**唯一决策问题：** 从同一个 0.629B-token 四层 MoE checkpoint 分叉后，让
Gate 分别只使用 head、middle、tail、middle+tail 或逐一同维随机子空间，训练到
2B tokens，哪些条件真正改变 token-to-expert 分发，哪些条件还改善或损害
matched-compute held-out NLL？

## 2. Physical Priors

频带限制首先改变路由，路由再改变专家收到的数据和更新；长期结果可能放大、
抵消或反转静态/一步指标。真实频带必须超过同维随机才能称为 rank-specific。

## 3. Falsifiable Hypotheses

**H1：频带特异训练效应。** 至少一个真实频带相对 native 明显改变固定 token
路由，并在 2B matched-compute held-out NLL 上与其同维 random 有可复现差异。

**R0：只有降维。** true band 与 equal-rank random 的分发和 NLL 相同。
**R1：只有负载。** loss 差由 overflow/drop/load 差异解释。
**R2：固定 basis 失效。** 训练后 projector 已不再对应当前谱带。
**R3：只改分发、不改功能。** route divergence 大，但 NLL 与专家功能指标无收益。

**Pass：** manipulation check 通过，某 true band 相对 native 改变分发，并相对
equal-rank random 的 paired held-out NLL 改善。**Fail：** 精确显示所有 true
bands 不优于各自 random/native。**Insufficient：** 训练、resume、compute、load、
basis identity 或 held-out 评估护栏失败。

## 4. Mathematical Model

在 branch checkpoint 的实际 Gate input 上估计 \(\mu_\ell,U_\ell\)。对冻结
projector \(P_{\ell,a}\)：

\[
r'_{\ell,a}=\mu_\ell+P_{\ell,a}(r_\ell-\mu_\ell),
\qquad z_{\ell,a}=W_\ell r'_{\ell,a}.
\]

用 \(W(P r)\) 的等价形式实现，使所有臂保留同形状 Gate 与 token-level Gate
FLOPs。主指标为 2B 共同终点的 \(\Delta L_{a:b}\)（nat/token）；路由 divergence
是必须通过的 manipulation check，不替代 NLL。

## 5. Computational Realization

[A15_05_05_E01 Protocol](../../../../experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/protocol_cn.md)
使用 H768、4 layers、8 sparse experts + 1 shared、top-1、DCLM、8×RTX5090。
九臂为 native、H64、M256、T448、N704，以及 R64/R256/R448/R704。所有臂
从完全相同的 step-800 model/optimizer/scheduler/data cursor/RNG 分叉并到
step-2544（约 2.001B nominal tokens）。

## 6. Minimal Falsification Tests

1. native projector 必须与原生 logits/top-1 no-op 一致。
2. 每个 true band 只与同维 random 比较；参数、数据、token、capacity、kernel
   和 Gate 路径匹配。
3. 固定 token route disagreement 必须证明 intervention 实际改变分发。
4. held-out DCLM NLL 为主结果；Web of Science domain/topic 只解释路由结构。
5. 训练后重估谱并测 frozen/current overlap；失效时只称 fixed-subspace。

## 7. Current Evidence

[E01 结果](../../../../experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary_cn.md)
已完成九个匹配条件并全部到达 2.000683B tokens。真实 H/M/T/N 相对 native
分别改变 4.98%、19.80%、21.88%、13.26% 的固定 DCLM token 路由，因此干预
有效；但 held-out NLL 分别更差 +0.001784、+0.005600、+0.003697、
+0.003308 nat/token。head 优于 random64 但仍输给 native；middle 与
middle+tail 输给同维随机；tail 与 random448 无法区别。计算、负载、重放、
训练完成和 basis 护栏均通过。

## 8. Claim Boundary And Next Decision

该结果严格证明：在一个四层配对分叉中，固定 covariance band 会影响分发，却
不能改善 2B DCLM 训练。它不能排除 head+residual 增量视图、可学习的任务条件
坐标或直接面向专家更新效用的目标，也不能建立跨 seed 普遍性。WOS 标签结构
仍只是诊断，不是语言模型收益目标。

**唯一下一决策：** 关闭固定 covariance-rank band-only dispatch；下一种
Router 表征必须先通过独立的专家更新兼容性或任务效用准入，才允许匹配大训练。
