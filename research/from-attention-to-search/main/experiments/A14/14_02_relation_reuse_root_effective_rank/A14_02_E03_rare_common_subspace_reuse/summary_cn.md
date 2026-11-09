---
experiment_id: A14_02_E03_rare_common_subspace_reuse
status: parked_before_full_run
verdict: parked_e02_common_space_gate_failed
completed_date: 2026-07-26
canonical_summary: summary.md
---

# 结果摘要：E03 rare–common 子空间复用

主 anchor：[A14_02_02](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_02_rare_common_subspace_reuse_anchor_cn.md)  
Protocol：[批准的条件执行合同](protocol_cn.md)

## 直接结论

**Verdict：**`parked_e02_common_space_gate_failed`。E03 full treatment 没有执行。

原因不是 E02 没学会，也不是 rank 测量失败，而是 E03 定义
“outside-common parameter direction”所依赖的 common AdamW step space 不稳定。
注册指标为：

\[
C_{\mathrm{common}}
=
\frac{\|P_{G_c}V_{\mathrm{test}}\|_F^2}
{\|V_{\mathrm{test}}\|_F^2}.
\]

- \(G_c\)：用 32 个 leave-target-out common step contrasts 拟合的空间；
- \(V_{\mathrm{test}}\)：另 32 个从未用于拟合的 common contrasts；
- 单位：held-out update energy fraction；
- 预注册门：至少 8 个 seeds 达到 \(0.80\)；
- 实际：均值 \(0.5717\)，范围 \(0.4780\)--\(0.6314\)，0/10 通过。

即使拟合空间已经使用 24--26 个方向，它仍只能捕获大约一半的 held-out
common-step energy。因此，把 rare update 在这个空间之外的部分叫作“new”会把
普通 common surface 变化误判为 rare novelty。

## 指标状态

原计划的 target-attributable effect：

\[
v_r
=
\theta_T^{\mathrm{rare}}
-\theta_T^{\mathrm{ctrl}}.
\]

原计划的新方向比例：

\[
\rho_{\mathrm{new}}
=
\frac{\|v_{\mathrm{new}}\|_2^2}{\|v_r\|_2^2}.
\]

原计划的 exact endpoint 主因果指标：

\[
\Delta CE_{\mathrm{drop-new}}
=
CE(\theta_T^{\mathrm{rare}}-v_{\mathrm{new}})
-CE(\theta_T^{\mathrm{rare}}).
\]

这些指标没有进入 full confirmation measurement，因为 \(G_c\) 不稳定时
\(v_{\mathrm{new}}\) 没有可审计定义。smoke 数据不升级为科学结论。

## 中心图

![Common parameter-space gate](figures/common_space_gate.png)

每个柱对应一个 LowF seed；虚线是冻结的 0.80 门。全部柱子低于门，因此按
Protocol 停止，而不是事后增大 rank 或换 probe。

## 认识更新

E02 的“功能状态复用”与 E03 的“raw optimizer update 空间共享”不是同一个
命题。当前证据允许前者成立，同时表明后者在逐 cell AdamW contrasts 上并不
自动稳定。

因此理论故事应更新为：

> common mapping 可以使答案任务所需的 ROOT 功能方向保持低维，但这不自动
> 要求不同 surface 的原始参数更新落进同一个低维线性空间。

这与 T6 的边界一致：参数几何和 ROOT 功能几何之间仍需要显式、可测的桥。

## 不能声称与下一决策

不能声称 rare 增加或不增加新参数/功能方向，也不能用 E03 gate failure 反驳
E02。下一步若重开，应在新 Protocol 中使用 fresh probes，优先考虑直接定义
ROOT-functional common space，而不是事后扩大当前 raw-update \(G_c\)。
